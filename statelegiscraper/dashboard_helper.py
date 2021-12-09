"""
Helper Functions for Plotly Dash Dashboard
"""
import math
import json
import re
from string import punctuation

from collections import defaultdict
import datetime
from datetime import date

import nltk
# nltk.download()
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from sentence_transformers import SentenceTransformer, util
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import torch


class NVHelper:

    def nv_extract_month(nv_json_path):
        """
       
       Parameters
       ----------
       Local path of cleaned nv_json file. 
       
       Returns
       -------
       A new json file with month as the keys. We can call new_json_file[month] if we want the transcripts of meetings for this month.
       Eg: call new_json_file[4], we would get the transcripts for April.
   
       """
        data = open(nv_json_path)
        json_file = json.load(data)

        new_json_file = defaultdict(list)

        for key in json_file.keys():
            temp = json_file[key]
            match = re.search(
                r'(January|February|March|April|May|June|July|August|September|October|November|December)[ ]([1-9]|[12][0-9]|3[01])[,][ ]\d{4}',
                temp)
            date = datetime.datetime.strptime(match.group(), '%B %d, %Y').date()
            month = date.month
            new_json_file[month].append(temp)

        return (new_json_file)

    def nv_extract_date(nv_json_path):
        """

       Parameters
       ----------
       Local path of cleaned nv_json file. 

       Returns
       -------
       """
        data = open(nv_json_path, 'r', encoding='utf-8')
        json_file = json.load(data)

        new_json_file = defaultdict(list)

        for key in json_file.keys():
            temp = json_file[key]
            match = re.search(
                r'(January|February|March|April|May|June|July|August|September|October|November|December)[ ]([1-9]|[12][0-9]|3[01])[,][ ]\d{4}',
                temp)
            date = datetime.datetime.strptime(match.group(), '%B %d, %Y').date()
            new_json_file[date] = temp

        return (new_json_file)

    def filter_covid_sentences(data_by_date):
        """

        Parameters
        ----------
        data_by_date json file 
        Returns
        -------
        """
        list_sen = []
        k = 0
        for i in data_by_date.keys():
            temp = nltk.tokenize.sent_tokenize(data_by_date[i])
            for j in range(len(temp)):
                list_sen.append({'text': temp[j], 'metadata': i.strftime("%m/%d/%Y") + "-" + str(j)})
                k += 1
        corpus = [text['text'] for text in list_sen]
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
        query = 'COVID 19'
        top_k = len(corpus) // 20

        results = set()
        query_embedding = embedder.encode(query, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k)
        for score, idx in zip(top_results[0], top_results[1]):
            if len(corpus[idx]) > 10:
                results.add(corpus[idx])
        filter = {}
        for i in data_by_date.keys():
            temp = nltk.tokenize.sent_tokenize(data_by_date[i])
            filter[i] = []
            for j in range(len(temp)):
                if temp[j] in results:
                    filter[i].append(temp[j])
                else:
                    pass
        filter_m = defaultdict(list)
        for key in filter.keys():
            temp = filter[key]
            month = key.month
            filter_m[month].append(temp)  # filtered sentences by month
        for i in filter_m.keys():
            filter_m[i] = sum(filter_m[i], [])

        with open("filtered_sentences_hhs.json", 'w') as f:
            json.dump(filter_m, f, ensure_ascii=False)


class NVSemanticSearching:

    def __init__(self, json_name, query, top_k):
        self.json = json_name
        self.query = query
        self.top_k = top_k

    def __save_corpus(self, corpus, corpus_embeddings, save_path):
        with open(save_path + "corpus.json", 'w') as outfile:
            json.dump(corpus, outfile)
        torch.save(corpus_embeddings, save_path + 'corpus_embedding.pt')
        # with open(save_path + "corpus_embedding.json", 'w') as em_outfile:
        #     json.dump(corpus_embeddings, em_outfile)

    def __sort_results(self, results):
        json_filter = {}
        for i in self.json.keys():
            temp = nltk.tokenize.sent_tokenize(self.json[i])
            str_i = i.strftime("%m/%d/%Y")
            json_filter[str_i] = []
            for j in range(len(temp)):
                if temp[j] in results:
                    json_filter[str_i].append(temp[j])
                else:
                    pass
        return json_filter

    def generate_corpus(self, archive=False, save_path=''):
        # Break text to sentences
        list_sen = []
        for i in self.json.keys():
            temp = nltk.tokenize.sent_tokenize(self.json[i])
            for j in range(len(temp)):
                list_sen.append({'text': temp[j], 'metadata': i.strftime("%m/%d/%Y") + "-" + str(j)})

        corpus = [sens['text'] for sens in list_sen]
        embedder = SentenceTransformer("dashboard//model")

        # Corpus with all sentences
        corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

        if archive:
            self.__save_corpus(corpus, corpus_embeddings, save_path)
            return corpus, corpus_embeddings
        else:
            return corpus, corpus_embeddings

    def semantic_searching(self, corpus, corpus_embeddings):
        # embedder = SentenceTransformer('all-MiniLM-L6-v2')
        embedder = SentenceTransformer("dashboard//model")
        query_embedding = embedder.encode(self.query, convert_to_tensor=True)

        # Use cosine-similarity and torch.topk to find the highest scores
        cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=self.top_k * len(corpus))

        results = set()
        for score, idx in zip(top_results[0], top_results[1]):
            if len(corpus[idx]) > 10:
                results.add(corpus[idx])
            else:
                pass
        json_filter = self.__sort_results(results)
        return json_filter

    def rapid_searching(self, corpus_path):
        # Load corpus
        file_corpus = open(corpus_path + "corpus.json", 'r', encoding='utf-8')
        corpus = json.load(file_corpus)
        corpus_embeddings = torch.load(corpus_path + "corpus_embedding.pt")
        # semantic searching
        json_filter = self.semantic_searching(corpus, corpus_embeddings)
        return json_filter

    def conventional_searching(self):
        # Generate corpus
        corpus, corpus_embeddings = self.generate_corpus()
        # Semantic searching
        json_filter = self.semantic_searching(corpus, corpus_embeddings)
        return json_filter


class NVTextProcessing:

    def __init__(self, json_name, stop_words=True, punctuations=True, lemmatization=True, remove_md=True):
        self.json = json_name
        self.stop_words = stop_words
        self.punctuations = punctuations
        self.lemmatization = lemmatization
        self.remove_md = remove_md

    def __penn2morphy(self, penntag):
        """ Converts Penn Treebank tags to WordNet. """
        morphy_tag = {'NN': 'n', 'JJ': 'a',
                      'VB': 'v', 'RB': 'r'}
        try:
            return morphy_tag[penntag[:2]]
        except:
            return 'n'

    def __lemmatize_sent(self, text):
        wnl = WordNetLemmatizer()
        return [wnl.lemmatize(word.lower(), pos=self.__penn2morphy(tag))
                for word, tag in pos_tag(text)]

    def word_tokenization(self):
        for i in self.json.keys():
            self.json[i] = json.dumps(self.json[i])  # convert json to string
            self.json[i] = " ".join([w for w in self.json[i].split() if w.isalpha()])  # remove numbers symbols

        for i in self.json.keys():
            self.json[i] = [word.lower() for word in word_tokenize(self.json[i])]

    def remove_stop_words(self):
        stopwords_en = set(stopwords.words('english'))  # set checking is faster than list

        for i in self.json.keys():
            self.json[i] = [word for word in self.json[i] if word not in stopwords_en]

    def remove_punctuations(self):
        for i in self.json.keys():
            self.json[i] = [word for word in self.json[i] if word not in punctuation]

    def lemmatize_words(self):
        for i in self.json.keys():
            self.json[i] = self.__lemmatize_sent(self.json[i])

    def remove_md_words(self):
        for i in self.json.keys():
            self.json[i] = [word for word, tag in pos_tag(self.json[i]) if tag[:2] != 'MD']

    def text_processing(self):
        self.word_tokenization()
        if self.stop_words:
            self.remove_stop_words()
        else:
            pass
        if self.punctuations:
            self.remove_punctuations()
        else:
            pass
        if self.lemmatization:
            self.lemmatize_words()
        else:
            pass
        if self.remove_md:
            self.remove_md_words()
        else:
            pass

class NVTextAnalysis:

    def __init__(self, json_name):
        self.json = json_name

    def __sort_dict(self, input_dict):
        sort_dict = {}  # sorted TF-IDF
        for i in input_dict.keys():
            sort_dict[i] = dict(sorted(input_dict[i].items(), key=lambda item: item[1], reverse=True))
        return sort_dict

    def word_frequency(self):
        word_freq_dist = {}
        for i in self.json.keys():
            word_freq_dist[i] = FreqDist(self.json[i])
        sorted_dict = self.__sort_dict(word_freq_dist)
        return word_freq_dist, sorted_dict

    def tf_idf_analysis(self):
        _, word_freq_dict = self.word_frequency()
        for i in word_freq_dict.keys():
            for k, v in word_freq_dict[i].items():
                word_freq_dict[i][k] = v/len(self.json[i])
        # IDF
        idf_dict = {}
        for i in word_freq_dict.keys():
            for word, count in word_freq_dict[i].items():
                if word in idf_dict:
                    idf_dict[word] += 1
                else:
                    idf_dict[word] = 1
        doc_count = len(word_freq_dict.keys())
        for word, count in idf_dict.items():
            idf_dict[word] = math.log(doc_count / (count + 1))
        # TF-IDF
        tf_idf_dict = {}
        for i in word_freq_dict.keys():
            tf_idf_dict[i] = word_freq_dict[i]
            for word, count in word_freq_dict[i].items():
                tf_idf_dict[i][word] = count * idf_dict[word]
        sorted_dict = self.__sort_dict(tf_idf_dict)
        return tf_idf_dict, sorted_dict

    def key_word_by_month(self):
        tf_idf_dict, _ = self.tf_idf_analysis()
        dict_by_month = {}
        for i in tf_idf_dict.keys():
            month = i[:2]
            if month not in dict_by_month:
                dict_by_month[month] = tf_idf_dict[i]
            else:
                for word, freq in tf_idf_dict[i].items():
                    if word in dict_by_month[month].keys():
                        dict_by_month[month][word] += freq
                    else:
                        dict_by_month[month][word] = freq
        sorted_dict = self.__sort_dict(dict_by_month)
        return dict_by_month, sorted_dict

    def sentiment_analysis(word_freq_dict):
        listsen_cov_pol={}
        listsen_cov_sen={}
        for i in word_freq_dict.keys():
            polarity=1
            for j in range(len(word_freq_dict[i].sentences)):
                if word_freq_dict[i].sentences[j].sentiment.polarity<polarity:
                    polarity=word_freq_dict[i].sentences[j].sentiment.polarity
                    sentence=word_freq_dict[i].sentences[j]
            listsen_cov_pol[i]=polarity
            listsen_cov_sen[i]=sentence
        listsen_cov_polp={}
        listsen_cov_senp={}
        for i in word_freq_dict.keys():
            polarity=-1
            for j in range(len(word_freq_dict[i].sentences)):
                if word_freq_dict[i].sentences[j].sentiment.polarity>polarity:
                    polarity=word_freq_dict[i].sentences[j].sentiment.polarity
                    sentence=word_freq_dict[i].sentences[j]
            listsen_cov_polp[i]=polarity
            listsen_cov_senp[i]=sentence
        covsen={}
        for i in word_freq_dict.keys():
            covsen[i]=word_freq_dict[i].sentiment.polarity
        covlistsen = listsen_cov_pol.items()
        covlistsen = sorted(covlistsen)
        return covlistsen, listsen_cov_polp, covsen


class NVVisualizations:

    def word_cloud(word_freq_dict, save_path, save_name):
        cloud_stopwords = set(["state", "nevada", "pandemic", "program", "project", "health", "human", "services"])
        for i in word_freq_dict.keys():
            if i in cloud_stopwords:
                word_freq_dict[i] = 0
        word_cloud = WordCloud(stopwords=cloud_stopwords, background_color="white").generate_from_frequencies(word_freq_dict)
        plt.imshow(word_cloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(save_path + save_name + '.png', bbox_inches='tight', pad_inches=0)

    def key_word_display(key_word_dict, top_k):
        results = {}
        stop_words = ['january', 'february', 'march', 'april', 'may']
        for i in key_word_dict.keys():
            temp = list(key_word_dict[i].items())[:top_k]
            app_temp = [word[0] for word in temp if word[0] not in stop_words]
            results[i] = app_temp
        return results

    def sentiment_plot(covlistsen, listsen_cov_polp, covsen, save_path):
        x1,y1 = zip(*covlistsen)
        covlistsenp = listsen_cov_polp.items()
        covlistsenp = sorted(covlistsenp)
        x2,y2 = zip(*covlistsenp)
        covsensen = covsen.items()
        covsensen = sorted(covsensen)
        x3,y3 = zip(*covsensen)
        plt.plot(x1,y1)
        plt.plot(x2,y2)
        plt.plot(x3,y3)
        plt.legend(['Lowest', 'Highest', 'Ave']) #label the line
        plt.savefig(save_path + 'sentiment.png', bbox_inches='tight', pad_inches=0)
        
        

