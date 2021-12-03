"""
Helper Functions for Plotly Dash Dashboard
"""
import json
import re

from collections import defaultdict
import datetime
from datetime import date

import nltk
# nltk.download()
from nltk import word_tokenize
from sentence_transformers import SentenceTransformer, util
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
           match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)[ ]([1-9]|[12][0-9]|3[01])[,][ ]\d{4}', temp)
           date = datetime.datetime.strptime(match.group(), '%B %d, %Y').date()
           month = date.month
           new_json_file[month].append(temp)
           
       return(new_json_file)
  
   def nv_extract_date(nv_json_path):
       """
       
       Parameters
       ----------
       Local path of cleaned nv_json file. 
       
       Returns
       -------
       """
       data = open(nv_json_path)
       json_file = json.load(data)
   
       new_json_file = defaultdict(list)
   
       for key in json_file.keys():
           temp = json_file[key]
           match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)[ ]([1-9]|[12][0-9]|3[01])[,][ ]\d{4}', temp)
           date = datetime.datetime.strptime(match.group(), '%B %d, %Y').date()
           new_json_file[date] = temp
           
       return(new_json_file)

    def filter_covid_sentences(data_by_date):
        """
       
        Parameters
        ----------
        data_by_date json file 
        Returns
        -------
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
        for i in filter_m.keys():
            filter_m[i]=sum(filter_m[i], [])

        with open("filtered_sentences_hhs.json", 'w') as f: 
            json.dump(filter_m, f, ensure_ascii=False)
