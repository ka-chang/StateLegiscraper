"""
Helper Functions for Plotly Dash Dashboard
"""
import math
import json
import re
from string import punctuation

from collections import defaultdict
import datetime

import nltk
# nltk.download()
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from textblob import TextBlob
from sentence_transformers import SentenceTransformer, util
from wordcloud import WordCloud, STOPWORDS
import torch
import matplotlib.pyplot as plt


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
        data = open(nv_json_path, 'r', encoding='utf-8')
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
    """
    NVSemanticSearching conducts semantic searching based on Sentence Transformer.
    Given an input query and a json file of texts, it filters out query-related sentences.
    Attributes
    ----------
    json: json file of texts
    query: topic to search for
    top_k: the most top_k% related sentences to filter out
    Methods
    -------
    generate_corpus(self, archive=False, save_path=''):
        Generate a tensor as the encoded representation of a text corpus.
    semantic_searching(self, corpus, corpus_embeddings):
        Filter out query-related sentences from the encoded corpus.
    rapid_searching(self, corpus_path):
        Rapid semantic searching based on an encoded text corpus.
    conventional_searching(self):
        Semantic searching on a text corpus.
    """

    def __init__(self, json_name, query, top_k):
        self.json = json_name
        self.query = query
        self.top_k = top_k

    def __save_corpus(self, corpus, corpus_embeddings, save_path):
        """
        Save the embedded sentences to the save_path.
        """
        with open(save_path + "corpus.json", 'w') as outfile:
            json.dump(corpus, outfile)
        torch.save(corpus_embeddings, save_path + 'corpus_embedding.pt')

    def __sort_results(self, results):
        """
        Filter sentences in self.json and keep the ones in results.
        """
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
        """
        Generate a tensor as the encoded representation of a text corpus.
        """
        # Sentence tokenization
        list_sen = []
        for i in self.json.keys():
            temp = nltk.tokenize.sent_tokenize(self.json[i])
            for j in range(len(temp)):
                list_sen.append({'text': temp[j], 'metadata': i.strftime("%m/%d/%Y") + "-" + str(j)})
        corpus = [sens['text'] for sens in list_sen]

        # Load the model
        embedder = SentenceTransformer("data//dashboard//model//")

        # Sentence embeddings
        corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

        # Save the results
        if archive:
            self.__save_corpus(corpus, corpus_embeddings, save_path)
            return corpus, corpus_embeddings
        else:
            return corpus, corpus_embeddings

    def semantic_searching(self, corpus, corpus_embeddings):
        """
        Filter out query-related sentences from the encoded corpus.
        """
        # Load the model
        embedder = SentenceTransformer("data//dashboard//model//")
        # Query embedding
        query_embedding = embedder.encode(self.query, convert_to_tensor=True)

        # Use cosine-similarity and torch.topk to find the highest scores
        cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=int(self.top_k * len(corpus) / 100))

        results = set()
        for score, idx in zip(top_results[0], top_results[1]):
            if len(corpus[idx]) > 10:
                results.add(corpus[idx])
            else:
                pass

        # Sort the filtered sentences as the input json
        json_filter = self.__sort_results(results)
        return json_filter

    def rapid_searching(self, corpus_path):
        """
        Rapid semantic searching based on an encoded text corpus.
        """
        # Load corpus
        file_corpus = open(corpus_path + "corpus.json", 'r', encoding='utf-8')
        corpus = json.load(file_corpus)
        corpus_embeddings = torch.load(corpus_path + "corpus_embedding.pt")
        # Semantic searching
        json_filter = self.semantic_searching(corpus, corpus_embeddings)
        return json_filter

    def conventional_searching(self):
        """
        Semantic searching on a text corpus.
        """
        # Generate corpus
        corpus, corpus_embeddings = self.generate_corpus()
        # Semantic searching
        json_filter = self.semantic_searching(corpus, corpus_embeddings)
        return json_filter


class NVTextProcessing:
    """
    NVTextProcessing conducts text cleaning on a json file.
    Given an input json file of texts, it can clean stop words, punctuations, lemmatized words, md words.
    Attributes
    ----------
    json: json file of texts
    Methods
    -------
    word_tokenization(self):
        Convert values of self.json to string. Break the string into words and remove numbers and symbols.
    remove_stop_words(self):
        Remove stop words from self.json.
    remove_punctuations(self):
        Remove punctuations from self.json.
    lemmatize_words(self):
        Lemmatize self.json.
    remove_md_words(self):
        Remove md words from self.json.
    text_processing(self):
        Text cleaning on self.json.
    """

    def __init__(self, json_name, stop_words=True, punctuations=True, lemmatization=True, remove_md=True):
        self.json = json_name
        self.stop_words = stop_words
        self.punctuations = punctuations
        self.lemmatization = lemmatization
        self.remove_md = remove_md

    def __penn2morphy(self, penntag):
        """
        Converts Penn Treebank tags to WordNet.
        """
        morphy_tag = {'NN': 'n', 'JJ': 'a',
                      'VB': 'v', 'RB': 'r'}
        try:
            return morphy_tag[penntag[:2]]
        except:
            return 'n'

    def __lemmatize_sent(self, text):
        """
        Lemmatize the given string.
        """
        wnl = WordNetLemmatizer()
        return [wnl.lemmatize(word.lower(), pos=self.__penn2morphy(tag))
                for word, tag in pos_tag(text)]

    def word_tokenization(self):
        """
        Convert values of self.json to string. Break the string into words while removing numbers and symbols.
        """
        for i in self.json.keys():
            self.json[i] = json.dumps(self.json[i])
            # Remove numbers and symbols
            self.json[i] = " ".join([w for w in self.json[i].split() if w.isalpha()])

        for i in self.json.keys():
            self.json[i] = [word.lower() for word in word_tokenize(self.json[i])]

    def remove_stop_words(self):
        """
        Remove stop words from self.json.
        """
        stopwords_en = set(stopwords.words('english'))  # set checking is faster than list

        for i in self.json.keys():
            self.json[i] = [word for word in self.json[i] if word not in stopwords_en]

    def remove_punctuations(self):
        """
        Remove punctuations from self.json.
        """
        for i in self.json.keys():
            self.json[i] = [word for word in self.json[i] if word not in punctuation]

    def lemmatize_words(self):
        """
        Lemmatize self.json.
        """
        for i in self.json.keys():
            self.json[i] = self.__lemmatize_sent(self.json[i])

    def remove_md_words(self):
        """
        Remove md words from self.json.
        """
        for i in self.json.keys():
            self.json[i] = [word for word, tag in pos_tag(self.json[i]) if tag[:2] != 'MD']

    def text_processing(self):
        """
        Text cleaning on self.json.
        """
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
    """
    NVTextAnalysis conducts text analysis on a json file.
    Given an input json file of texts, apply word frequency analysis, sentiment analysis,
    and key word extraction by tf-idf.
    Attributes
    ----------
    json: json file of texts
    Methods
    -------
    word_frequency(self):
        Word frequency analysis on self.json.
    tf_idf_analysis(self):
        TF-IDF on self.json for key-word extraction.
    sentiment_analysis(word_freq_dict):
        Sentiment analysis on self.json.
    """

    def __init__(self, json_name):
        self.json = json_name

    def __sort_dict(self, input_dict):
        """
        Sort input_dict according to values of its items (freq_dict).
        """
        sort_dict = {}
        for i in input_dict.keys():
            sort_dict[i] = dict(sorted(input_dict[i].items(), key=lambda item: item[1], reverse=True))
        return sort_dict

    def word_frequency(self):
        """
        Word frequency analysis on self.json.
        """
        word_freq_dist = {}
        for i in self.json.keys():
            word_freq_dist[i] = FreqDist(self.json[i])
        sorted_dict = self.__sort_dict(word_freq_dist)
        return word_freq_dist, sorted_dict

    def tf_idf_analysis(self):
        """
        TF-IDF for key-word extraction.
        """
        _, word_freq_dict = self.word_frequency()
        # TF
        for i in word_freq_dict.keys():
            for k, v in word_freq_dict[i].items():
                word_freq_dict[i][k] = v / len(self.json[i])
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
            idf_dict[word] = math.log(doc_count / (count + 1)) / 10000
        # TF-IDF
        tf_idf_dict = {}
        for i in word_freq_dict.keys():
            tf_idf_dict[i] = word_freq_dict[i]
            for word, count in word_freq_dict[i].items():
                tf_idf_dict[i][word] = count * idf_dict[word]
        sorted_dict = self.__sort_dict(tf_idf_dict)
        return tf_idf_dict, sorted_dict

    def sort_dict_by_month(self, input_dict):
        dict_by_month = {}
        for i in input_dict.keys():
            month = i[:2]
            if month not in dict_by_month:
                dict_by_month[month] = input_dict[i]
            else:
                for word, freq in input_dict[i].items():
                    if word in dict_by_month[month].keys():
                        dict_by_month[month][word] += freq
                    else:
                        dict_by_month[month][word] = freq
        sorted_dict = self.__sort_dict(dict_by_month)
        return dict_by_month, sorted_dict

    def sentiment_analysis(self):
        """
        Sentiment analysis on self.json.
        """
        with open('filtered_sentences_hhs.json', 'r') as file:
              filter_m= json.load(file)
        blob={}
        for i in filter_m.keys():
            blob[i] = TextBlob(' '.join(filter_m[i]))
        listsen_cov_pol = {}
        listsen_cov_sen = {}
        for i in blob.keys():
            polarity = 1
            for j in range(len(blob[i].sentences)):
                if blob[i].sentences[j].sentiment.polarity < polarity:
                    polarity = blob[i].sentences[j].sentiment.polarity
                    sentence = blob[i].sentences[j]
            listsen_cov_pol[i] = polarity
            listsen_cov_sen[i] = sentence
        listsen_cov_polp = {}
        listsen_cov_senp = {}
        for i in blob.keys():
            polarity = -1
            for j in range(len(blob[i].sentences)):
                if blob[i].sentences[j].sentiment.polarity > polarity:
                    polarity = blob[i].sentences[j].sentiment.polarity
                    sentence = blob[i].sentences[j]
            listsen_cov_polp[i] = polarity
            listsen_cov_senp[i] = sentence
        covsen = {}
        for i in blob.keys():
            covsen[i] = blob[i].sentiment.polarity
        return listsen_cov_pol, listsen_cov_polp, covsen


class NVVisualizations:
    """
    NVVisualizations plot and sort the text analysis results.
    Attributes
    ----------
    Methods
    -------
    word_cloud(word_freq_dict, save_path, save_name):
        Plot word cloud according to word_freq_dict. Save the .png file as specified by save_path and save_name.
    key_word_display(key_word_dict, top_k):
        Sort the top_k key words from key_word_dict.
    sentiment_plot(covlistsen, listsen_cov_polp, covsen, save_path):
        Plot sentiment analysis and save.
    """

    def word_cloud(word_freq_dict, save_path, save_name):
        """
        Plot word cloud according to word_freq_dict. Save the .png file as specified by save_path and save_name.
        """
        cloud_stopwords = set(["state", "nevada", "pandemic", "program", "project", "health", "human", "services"])
        for i in word_freq_dict.keys():
            if i in cloud_stopwords:
                word_freq_dict[i] = 0
        word_cloud = WordCloud(stopwords=cloud_stopwords, background_color="white", width=400,
                               height=200).generate_from_frequencies(word_freq_dict)
        word_cloud.to_file(save_path + save_name + '.png')

    def key_word_display(key_word_dict, top_k):
        """
        Sort the top_k key words from key_word_dict.
        """
        results = {}
        stop_words = ['january', 'february', 'march', 'april', 'may']
        for i in key_word_dict.keys():
            temp = list(key_word_dict[i].items())[:top_k]
            app_temp = [word[0] for word in temp if word[0] not in stop_words]
            results[i] = app_temp
        return results

    def sentiment_plot(listsen_cov_pol, listsen_cov_polp, covsen, save_path):
        """
        Plot sentiment analysis and save.
        """
        covlistsen = listsen_cov_pol.items()
        covlistsen = sorted(covlistsen)
        x1, y1 = zip(*covlistsen)
        covlistsenp = listsen_cov_polp.items()
        covlistsenp = sorted(covlistsenp)
        x2, y2 = zip(*covlistsenp)
        covsensen = covsen.items()
        covsensen = sorted(covsensen)
        x3, y3 = zip(*covsensen)
        plt.plot(x1, y1)
        plt.plot(x2, y2)
        plt.plot(x3, y3)
        plt.legend(['Lowest', 'Highest', 'Ave'])  # label the line
        plt.savefig(save_path + 'sentiment.png', bbox_inches='tight', pad_inches=0)

