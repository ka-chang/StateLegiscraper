# This python program analyzes texts of hearings from hhs/finance assemnly and senate:
# We focus on the topic of COVID-19.
# Tasks:
# (1) Word Counting (by month)
# (2) Sentiment Analysis (by month)
# (3) TF-IDF
# (4) Visualizations

import json
import os
from pathlib import Path
import sys
from string import punctuation
import re
import math
import datetime

import nltk
# nltk.download()
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
from sentence_transformers import SentenceTransformer, util
import torch
from collections import defaultdict


github_file_path = str(Path(os.getcwd()).parents[1]) # Sets to local Github directory path
sys.path.insert(1, github_file_path)

from LegTextScraper.states.nv import NVProcess
from LegTextScraper.dashboard_helper import NVHelper

cleaned_data = NVProcess.nv_text_clean("nv_hhs_2021_raw.json", trim=True)
with open("cleaned_data.json", 'w') as f: 
    json.dump(cleaned_data, f, ensure_ascii=False)

data_by_date = NVHelper.nv_extract_date("cleaned_data.json")
data_by_month = NVHelper.nv_extract_month("cleaned_data.json")
### Data Cleaning
raw = {}
for i in data_by_month.keys():
    raw[i] = json.dumps(data_by_month[i]) # convert json to string

text = {}
for i in raw.keys():
    text[i]= [word.lower() for word in word_tokenize(raw[i])]

stopwords_en = set(stopwords.words('english')) # set checking is faster than list

text_no_stopwords = {} # without stopwords

for i in text.keys():
    text_no_stopwords[i] = [word for word in text[i] if word not in stopwords_en]

text_no_stopwords_punc = {} # without punctuations
for i in text_no_stopwords.keys():
    text_no_stopwords_punc[i] = [word for word in text_no_stopwords[i] if word not in punctuation]

wnl = WordNetLemmatizer()

def penn2morphy(penntag):
    """ Converts Penn Treebank tags to WordNet. """
    morphy_tag = {'NN':'n', 'JJ':'a',
                  'VB':'v', 'RB':'r'}
    try:
        return morphy_tag[penntag[:2]]
    except:
        return 'n' 
    
def lemmatize_sent(text): 
    return [wnl.lemmatize(word.lower(), pos=penn2morphy(tag)) 
            for word, tag in pos_tag(text)]

text_no_stopwords_punc_lemma = {} # after lemmatization
for i in text_no_stopwords_punc.keys():
    text_no_stopwords_punc_lemma[i]=lemmatize_sent(text_no_stopwords_punc[i])

text_no_stopwords_punc_lemma_md = {}
for i in text_no_stopwords_punc_lemma.keys():
    text_no_stopwords_punc_lemma_md[i]=[word for word in text_no_stopwords_punc_lemma[i] if nltk.pos_tag([word])[0][1] != 'MD']

### Word Counting
textdist = {}
for i in text_no_stopwords_punc_lemma_md.keys():
    textdist[i] = FreqDist(text_no_stopwords_punc_lemma_md[i])

textdistcov = {}
for i in textdist.keys():
    textdistcov[i] = textdist[i].freq('covid-19')*100

covlist = textdistcov.items()
covlist = sorted(covlist)
x1,y1 = zip(*covlist)
plt.plot(x1,y1) # Output Plot: word frequency of COVID-19 by month

text_no_stopwords_punc_lemma_onn={} # only include non texts
for i in text_no_stopwords_punc_lemma.keys():
    text_no_stopwords_punc_lemma_onn[i]=[word for word in text_no_stopwords_punc_lemma[i] if nltk.pos_tag([word])[0][1] == 'NN' ]

textdistn = {}
for i in text_no_stopwords_punc_lemma_onn.keys():
    textdistn[i] = FreqDist(text_no_stopwords_punc_lemma_onn[i])

textdistncov = {}
for i in textdistn.keys():
    textdistncov[i] = textdistn[i].freq('covid-19')*100

covnlist = textdistncov.items()
covnlist = sorted(covnlist)
x2,y2 = zip(*covnlist)
plt.plot(x2,y2) # Output Plot: word frequency of COVID-19 in non texts by month

### Filter the COVID-19 Sentences
list_sen=[]
k = 0
for i in data_by_date.keys():
    temp = nltk.tokenize.sent_tokenize(data_by_date[i])
    for j in range(len(temp)):
        list_sen.append({'text':temp[j], 'metadata': i.strftime("%m/%d/%Y")+"-"+str(j)})
        k += 1
corpus = [text['text'] for text in list_sen]
embedder = SentenceTransformer('all-MiniLM-L6-v2')
corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
query = 'COVID 19'
top_k = len(corpus)//20

results = set()
query_embedding = embedder.encode(query, convert_to_tensor=True)
cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
top_results = torch.topk(cos_scores, k=top_k)
for score, idx in zip(top_results[0], top_results[1]):
    if len(corpus[idx]) > 10:
        results.add(corpus[idx])
filter = {}
for i in data_by_date.keys():
    temp=nltk.tokenize.sent_tokenize(data_by_date[i])
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
    filter_m[month].append(temp) # filtered sentences by month

### Sentiment Analysis
for i in filter_m.keys():
    filter_m[i]=sum(filter_m[i], [])    #### erase the square brackets of the dictionary value
blob={}
for i in filter_m.keys():
    blob[i] = TextBlob(' '.join(filter_m[i]))
listsen_cov_pol={}
listsen_cov_sen={}
for i in blob.keys():
    polarity=1
    for j in range(len(blob[i].sentences)):
        if blob[i].sentences[j].sentiment.polarity<polarity:
            polarity=blob[i].sentences[j].sentiment.polarity
            sentence=blob[i].sentences[j]
    listsen_cov_pol[i]=polarity
    listsen_cov_sen[i]=sentence
listsen_cov_polp={}
listsen_cov_senp={}
for i in blob.keys():
    polarity=-1
    for j in range(len(blob[i].sentences)):
        if blob[i].sentences[j].sentiment.polarity>polarity:
            polarity=blob[i].sentences[j].sentiment.polarity
            sentence=blob[i].sentences[j]
    listsen_cov_polp[i]=polarity
    listsen_cov_senp[i]=sentence
covsen={}
for i in blob.keys():
    covsen[i]=blob[i].sentiment.polarity
covlistsen = listsen_cov_pol.items()
covlistsen = sorted(covlistsen)
x3,y3 = zip(*covlistsen)
covlistsenp = listsen_cov_polp.items()
covlistsenp = sorted(covlistsenp)
x4,y4 = zip(*covlistsenp)
covsensen = covsen.items()
covsensen = sorted(covsensen)
x5,y5 = zip(*covsensen)
plt.plot(x3,y3)
plt.plot(x4,y4)
plt.plot(x5,y5)
plt.legend(['Lowest', 'Highest', 'Ave']) #label the line
plt.show()
print('The lowest scores are got by the following sentences:\n',listsen_cov_sen)
print('The highest scores are got by the following sentences:\n',listsen_cov_senp)

### TF-IDF
termdist = {} # TF
for i in textdist.keys():
    count_words = len(textdist[i].keys())
    termdist[i] = textdist[i]
    for word, count in textdist[i].items():
        termdist[i][word] = count / count_words

idfdist = {} # IDF
for i in termdist.keys():
    for word, count in termdist[i].items():
        if word in idfdist:
            idfdist[word] += 1
        else:
            idfdist[word] = 1
doc_count = len(termdist.keys())
for word, count in idfdist.items():
    idfdist[word] = math.log(doc_count/(count+1))

tfidfdist = {} # TF-IDF
for i in termdist.keys():
    tfidfdist[i] = termdist[i]
    for word, count in termdist[i].items():
        tfidfdist[i][word] = count * idfdist[word]

sort_dict = {} # sorted TF-IDF
for i in tfidfdist.keys():
    sort_dict[i] = dict(sorted(tfidfdist[i].items(), key=lambda item: item[1], reverse=True))


### Word Cloud
stopwords = set(STOPWORDS)
stopwords.update(["covid", "state", "nevada", "pandemic", "program", "project"])
unique_string = {}
wordcloud = {}
for i in filter_m.keys():
    month_string = ""
    for j in range(len(filter_m[i])):
        month_string += (" ").join(filter_m[i][j])
    unique_string[i] = month_string
    wordcloud[i] = WordCloud(stopwords=stopwords, background_color="white").generate(unique_string[i])
    plt.imshow(wordcloud[i], interpolation='bilinear')
    plt.axis("off")
    plt.show() # Output Plots: word cloud plots by month
