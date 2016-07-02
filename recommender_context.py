#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Manas Ranjan Kar
# @Date:   2016-06-21
# @Email:  manas@jsm.email  
# @Github username: @manasRK
# @Last Modified by:   Manas Ranjan KAr
# @Last Modified time: 2016-06-26


import os
import sys
import ast
import gensim
import json
from gensim import utils
from gensim.models import Word2Vec

import logging
import argparse

logger = logging.getLogger(__name__)

import redis

data_obj = redis.Redis("localhost", port=6379, db=2)

class ContextCorpus(object):
    def __init__(self, redis_obj, context_prefix='C', example_prefix='I'):
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
        for key in self.redis_obj.keys("*"):
            line = [self.context_prefix + str(key)]
            line += [self.example_prefix + str(i) for i in ast.literal_eval(self.redis_obj.get(key))]
            yield line


def train(model_file):
    contexts = ContextCorpus(data_obj)
    #model = gensim.models.Word2Vec(contexts, min_count=5, workers=4, negative=10, sg=1, size = 300, sample=1e-3, hs=1, window = 5) #a1 
    #model = gensim.models.Word2Vec(contexts, min_count=5, workers=4, negative=3, sg=0, size = 300, sample=1e-5, hs=0, window = 5) #a2 
    #model = gensim.models.Word2Vec(contexts, min_count=5, workers=4, negative=5, sg=0, size = 300, sample=1e-3, hs=1, window = 5) #a3
    #model = gensim.models.Word2Vec(contexts, min_count=5, workers=4, negative=10, sg=1, size = 300, sample=1e-3, hs=0, window = 5) #a4
    #model = gensim.models.Word2Vec(contexts, min_count=5, workers=4, negative=10, sg=1, size = 300, sample=1e-5, hs=0, window = 5) #a5
    model = gensim.models.Word2Vec(contexts, min_count=5, workers=4, negative=3, sg=0, size = 300, sample=1e-4, hs=1, window = 5) #a6
    # ./word2vec -train train100B.txt -read-vocab voc -output vectors.bin -cbow 1 -size 300 -window 5 -negative 3 -hs 0 -sample 1e-5 -threads 12 -binary 1 -min-count 10
    model.init_sims(replace=True)
    model.save(model_file)

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
        "-m", "--model_output", required=True,
        help="Output model file, in word2vec format")
    args = parser.parse_args()
    
    model_file = args.model_output
    logger.info('Picking data from %s...', data_obj)
    
    train(model_file)
    
    logger.info("Saving model file %s in %s", model_file, os.path.abspath(model_file))
    logger.info("Finished running %s", program)
    

