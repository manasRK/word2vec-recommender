#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Akhil Gupta
# @Email:  akhilgupta.official@gmail.com  
# @Github username: @codeorbit
# @Last Modified by:   Akhil Gupta
# @Last Modified time: 2016-07-1

import json
import gzip
import redis

price_obj = redis.Redis("localhost", port=6379, db=1)

def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield json.dumps(eval(l))

print 'Starting loading to Redis !'

for l in parse("data/metadata.json.gz"):
  price_obj.set(l.get('asin'), l.get('price'))

print 'Loaded to Redis !'