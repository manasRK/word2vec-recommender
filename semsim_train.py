#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Manas Ranjan Kar
# @Date:   2016-06-20
# @Email:  manas@jsm.email  
# @Github username: @manasRK
# @Last Modified by:   Manas Ranjan KAr
# @Last Modified time: 2016-06-26



import re
import os
import sys

from nltk.corpus import stopwords
stop = stopwords.words('english')

import gensim
import string
import redis
import json
import gzip
from unidecode import unidecode

import logging
import argparse

from phrases_extractor import get_phrases

price_obj = redis.Redis("localhost", port=6379, db=1)

logger = logging.getLogger(__name__)


def parse(filename):
    g = gzip.open(filename,"r")
    for l in g:
      yield json.dumps(eval(l))


def getRange(price):
    
    price  = float(price)
    if price <= 0:
      return 0
    elif 0 < price <= 10:
      return 10
    elif 10 < price <= 25:
      return 25
    elif 25 < price <= 50:
      return 50
    elif 50 < price <= 100:
      return 100
    elif 100 < price <= 200:
      return 200
    elif 200 < price <= 500:
      return 500
    elif price > 500:
      return 999


def process_phrases(text):
    text = unidecode(text) 
    phrases = get_phrases(text)
    for phrase in phrases:
      text = text.replace(phrase, phrase.replace(' ', '_'))
    return text


def pre_process(m):
    m = unidecode(m)
    m = m.lower().strip() #normalize
    #print m
    #m=re.sub("[^a-zA-Z]", " ",m) #keep text only
    #m="".join(l for l in m if l not in string.punctuation) #remove punctuation
    #m = m.strip("./@!#")
    m=[i for i in m.split() if i not in stop] #remove stopwords
    m=[i.strip("./@!#") for i in m] #remove stopwords
    #m=m.split()
    #print m
    return m


#iterator on Amazon Reviews  
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        print os.listdir(self.dirname)
        count=0
        l=0
        for fname in os.listdir(self.dirname):
            logger.info('Processing file %s', fname)
            for e in parse((os.path.join(self.dirname, fname))):
                review= json.loads(e).get("reviewText")
                title = json.loads(e).get("summary")
                category = fname.strip('reviews json gz . _')
                all_text = title + ". " + review
                all_text = process_phrases(all_text)
              
                if len(review.split())>10: # don't consider reviews less than 10 words
                  productId = json.loads(e).get("asin")
                  try:
                    price = getRange(price_obj.get(productId))
                  except:
                    price = 0
                  
                  count +=1
                  final_data = "<" + str(price) + "> <" + category + "> <" + productId + "> " + all_text + " <" + str(price) + "> <" + category + "> <" + productId + ">"
                  sents = pre_process(final_data)
                  l+=len(sents)
                  print 'Count: '," ",count," ",l," ",sents
                  yield sents

                
def train(data_folder, model_path):
    sentences = MySentences(data_folder)
    #model = gensim.models.Word2Vec(sentences, min_count=25, workers=8, negative=10, sg=1, size = 300, sample=1e-3, hs=1, window = 10) #a1 
    #model = gensim.models.Word2Vec(sentences, min_count=10, workers=6, negative=3, sg=0, size = 300, sample=1e-5, hs=0, window = 5) #a2 
    #model = gensim.models.Word2Vec(sentences, min_count=10, workers=4, negative=5, sg=0, size = 300, sample=1e-3, hs=1, window = 5) #a3
    #model = gensim.models.Word2Vec(sentences, min_count=10, workers=8, negative=10, sg=1, size = 300, sample=1e-3, hs=0, window = 7) #a4
    #model = gensim.models.Word2Vec(sentences, min_count=10, workers=8, negative=10, sg=1, size = 300, sample=1e-5, hs=0, window = 5) #a5
    model = gensim.models.Word2Vec(sentences, min_count=10, workers=8, negative=3, sg=0, size = 300, sample=1e-4, hs=1, window = 10) #a6
    # ./word2vec -train train100B.txt -read-vocab voc -output vectors.bin -cbow 1 -size 300 -window 5 -negative 3 -hs 0 -sample 1e-5 -threads 12 -binary 1 -min-count 10
    model.init_sims(replace=True)
    model.save(model_path)

if __name__ == "__main__":
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s", ' '.join(sys.argv))

    # check and process cmdline input
    program = os.path.basename(sys.argv[0])
    if len(sys.argv) < 2:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "-d", "--data", required=True,
        help="Input data folder.")
    parser.add_argument(
        "-m", "--model_output", required=True,
        help="Output model file, in word2vec format")
    args = parser.parse_args()
    
    data_folder, model_path = (args.data, args.model_output)
    logger.info('Picking data from %s...', data_folder)
    
    train(data_folder, model_path)
    
    logger.info("Saving model file %s in %s", model_path, os.path.abspath(model_path))
    logger.info("Finished running %s", program)
    

