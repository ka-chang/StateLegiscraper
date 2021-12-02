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

from LegTextScraper.states.nv import nv_preprocess

github_file_path = str(Path(os.getcwd()).parents[1]) # Sets to local Github directory path
sys.path.insert(1, github_file_path) 
data = nv_preprocess("nv_fin_new.json", trim=True) # Input file

### Data Cleaning
raw = {}
for i in data.keys():
    raw[i] = json.dumps(data[i]) # convert json to string

text = {}
for i in raw.keys():
    text[i]= [word.lower() for word in word_tokenize(raw[i])

stopwords_en = set(stopwords.words('english')) # set checking is faster than list

text_no_stopwords = {} # without stopwords

for i in text.keys():
    text_no_stopwords[i] = [word for word in text[i] if word not in stopwords_en]

text_no_stopwords_punc = {} # without punctuations
for i in text_no_stopwords.keys():
    text_no_stopwords_punc[i] = [word for word in text_no_stopwords[i] if word not in punctuation]

wnl = WordNetLemmatizer()

text_no_stopwords_punc_lb = {} # without line breaks
for i in text_no_stopwords_punc.keys():
    text_no_stopwords_punc_lb[i] = [word for word in text_no_stopwords_punc[i] if not word.startswith('\\n')]+ [word[2:] 
                                for word in text_no_stopwords_punc if  word.startswith('\\n')]

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

text_no_stopwords_punc_lb_lemma = {} # after lemmatization
for i in text_no_stopwords_punc_lb.keys():
    text_no_stopwords_punc_lb_lemma[i]=lemmatize_sent(text_no_stopwords_punc_lb[i])

text_no_stopwords_punc_lb_lemma_md = {}
for i in text_no_stopwords_punc_lb_lemma.keys():
    text_no_stopwords_punc_lb_lemma_md[i]=[word for word in text_no_stopwords_punc_lb_lemma[i] if nltk.pos_tag([word])[0][1] != 'MD']

### Word Counting
textdist = {}
for i in text_no_stopwords_punc_lb_lemma_md.keys():
    textdist[i] = FreqDist(text_no_stopwords_punc_lb_lemma_md[i])

textdistcov = {}
for i in textdist.keys():
    textdistcov[i] = textdist[i].freq('covid-19')*100

covlist = textdistcov.items()
covlist = sorted(covlist)
x1,y1 = zip(*covlist)
plt.plot(x1,y1) # Output Plot: word frequency of COVID-19 by month

text_no_stopwords_punc_lb_lemma_onn={} # only include non texts
for i in text_no_stopwords_punc_lb_lemma.keys():
    text_no_stopwords_punc_lb_lemma_onn[i]=[word for word in text_no_stopwords_punc_lb_lemma[i] if nltk.pos_tag([word])[0][1] == 'NN' ]

textdistn = {}
for i in text_no_stopwords_punc_lb_lemma_onn.keys():
    textdistn[i] = FreqDist(text_no_stopwords_punc_lb_lemma_onn[i])

textdistncov = {}
for i in textdistn.keys():
    textdistncov[i] = textdistn[i].freq('covid-19')*100

covnlist = textdistncov.items()
covnlist = sorted(covnlist)
x2,y2 = zip(*covnlist)
plt.plot(x2,y2) # Output Plot: word frequency of COVID-19 in non texts by month

### Sentiment Analysis
sentidata = {}
for i in data.keys():
    sentidata[i]=' '.join(data[i])
    
listsen = {}
for i in sentidata.keys():
    listsen[i]=nltk.tokenize.sent_tokenize(sentidata[i])

listsen_cov = {} # filter the sentences which have covid-19
for i in listsen.keys():
    listsen_cov[i]=[sen for sen in listsen[i] if ' COVID-19' in sen]

blob = {}
for i in listsen_cov.keys():
    blob[i] = TextBlob(' '.join(listsen_cov[i]))

listsen_cov_pol = {}
listsen_cov_sen = {}
for i in blob.keys():
    polarity=1
    for j in range(len(blob[i].sentences)):
        if blob[i].sentences[j].sentiment.polarity<polarity:
            polarity=blob[i].sentences[j].sentiment.polarity
            sentence=blob[i].sentences[j]
    listsen_cov_pol[i]=polarity
    listsen_cov_sen[i]=sentence

covlistsen = listsen_cov_pol.items()
covlistsen = sorted(covlistsen)
x3,y3 = zip(*covlistsen)
plt.plot(x3,y3) # Output Plot: the lowest polarity of covid sentenses by month

listsen_cov_polp = {}
listsen_cov_senp = {}
for i in blob.keys():
    polarity=-1
    for j in range(len(blob[i].sentences)):
        if blob[i].sentences[j].sentiment.polarity>polarity:
            polarity=blob[i].sentences[j].sentiment.polarity
            sentence=blob[i].sentences[j]
    listsen_cov_polp[i]=polarity
    listsen_cov_senp[i]=sentence

covlistsenp = listsen_cov_polp.items()
covlistsenp = sorted(covlistsenp)
x4,y4 = zip(*covlistsenp)
plt.plot(x4,y4) # Output Plot: the highest polarity of covid sentenses by month

covsen = {}
for i in blob.keys():
    covsen[i]=blob[i].sentiment.polarity
covsensen = covsen.items()
covsensen = sorted(covsensen)
x5,y5 = zip(*covsensen)
plt.plot(x5,y5) # Output Plot: the polarity of covid sentences by month

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
stopwords.update(["department", "program", "state", "nevada", "legislative", "project"])
unique_string = {}
wordcloud = {}
for i in data.keys():
    unique_string[i]=(" ").join(data[i])
    wordcloud[i] = WordCloud(stopwords=stopwords, background_color="white").generate(unique_string[i])
    plt.imshow(wordcloud[i], interpolation='bilinear')
    plt.axis("off")
    plt.show() # Output Plots: word cloud plots by month