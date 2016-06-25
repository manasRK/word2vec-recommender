
import os
import sys
import ast
import gensim
import json
from gensim import utils
import multiprocessing
from gensim.models import Word2Vec

import logging
import argparse

logger = logging.getLogger(__name__)

import redis

data_obj = redis.Redis("localhost", port=6379, db=10) # 2, 9 (smaller), 10 (larger)

class ContextCorpus(object):
    def __init__(self, redis_obj, context_prefix='C', example_prefix='C'):
        """
        ContextCorpus(contexts)
        Parameters
        ---------
        contexts : dict of sets
            Each set in the dict should be an observation occurring within
            the same context. E.g., every set should contain all pins by
            one client or all fixes by one client.
        context_prefix : str, optional
            This string will be prepended to all context keys
        example_prefix : str, optional
            This string will be prepended to all non-context words
        Examples
        ------
        # If user 1 bought items 0, 1, 2, 3 and user 2
        # bought 3, 4, 5 and user bought item 10
        contexts = {1:{0,1,2,3}, 2:{3,4,5}, 3:{10}}
        cc = ContextCorpus(contexts)
        """
        self.redis_obj = redis_obj
        self.context_prefix = context_prefix
        self.example_prefix = example_prefix

    def __iter__(self):
        """Create 'sentences' that start with the context as a word
           and then also have items as words on the same line """
        count = 0
        for key in self.redis_obj.keys("*"):
            count+=1
            line = [self.context_prefix + str(key)]
            line += [self.example_prefix + str(i) for i in ast.literal_eval(self.redis_obj.get(key))]
            count+=1
            if count%5000 == 0 :
                print "Meta loaded: %s" %count
            #print count
            #print line
            yield line


def train(model_file):
    contexts = ContextCorpus(data_obj)
    model = gensim.models.Word2Vec(contexts, min_count=5, workers= multiprocessing.cpu_count(), negative=3, sg=1, size = 300, sample=1e-3, hs=1, window = 5) #a1 
    #model = gensim.models.Word2Vec(contexts, min_count=5, workers=4, negative=3, sg=0, size = 300, sample=1e-5, hs=0, window = 5) #a2 
    #model = gensim.models.Word2Vec(contexts, min_count=5, workers=4, negative=5, sg=0, size = 300, sample=1e-3, hs=1, window = 5) #a3
    #model = gensim.models.Word2Vec(contexts, min_count=5, workers=4, negative=10, sg=1, size = 300, sample=1e-3, hs=0, window = 5) #a4
    #model = gensim.models.Word2Vec(contexts, min_count=5, workers=4, negative=10, sg=1, size = 300, sample=1e-5, hs=0, window = 5) #a5
    #model = gensim.models.Word2Vec(contexts, min_count=5, workers=4, negative=3, sg=0, size = 300, sample=1e-4, hs=1, window = 5) #a6
    # ./word2vec -train train100B.txt -read-vocab voc -output vectors.bin -cbow 1 -size 300 -window 5 -negative 3 -hs 0 -sample 1e-5 -threads 12 -binary 1 -min-count 10
    model.init_sims(replace=True)
    model.save(model_file)

if __name__ == "__main__":
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s", ' '.join(sys.argv))
    
    model_file = 'data/models/user_local_context_v1_large.txt'
    train(model_file)
    
    logger.info("Saving model file %s in %s", model_file, os.path.abspath(model_file))
    

