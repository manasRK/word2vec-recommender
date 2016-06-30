#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Akhil Gupta
# @Date:   2016-06-20
# @Email:  akhilgupta.official@gmail.com  
# @Github username: @codeorbit
# @Last Modified by:   Akhil Gupta
# @Last Modified time: 2016-06-30

import redis
from bottle import route, run
import gensim
import urllib2

redis_obj = redis.Redis(host = 'localhost', port = 6379, db = 3)
model = gensim.models.Word2Vec.load('modelPath')

@route('/search/meta/<input_dic>')
def search(input_dic):
	input_dic = eval(input_dic)
	global redis_obj
	temp = []
	for pid in input_dic["pids"]:
		pid = "C"+pid
		res = model.most_similar(positive = [pid], topn = 1000)
	for ids in res:
		temp.append(ids[1:])

	redis_input = input_dic
	redis_input["pids"] = temp

	result_from_redis  = urllib2.urlopen('url here').read()
	result_from_redis = eval(result)

	return result_from_redis
	
run(host = '0.0.0.0', port = 8001, debug = True) 
