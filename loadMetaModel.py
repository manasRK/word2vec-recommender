#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Akhil Gupta
# @Date:   2016-06-20
# @Email:  akhilgupta.official@gmail.com  
# @Github username: @codeorbit
# @Last Modified by:   Akhil Gupta
# @Last Modified time: 2016-06-30

import redis
import loadRedis as lr
from bottle import route, run
import ast
import gensim
import urllib2
import redis
redis_obj = redis.Redis(host = 'localhost', port = 6379, db = 3)
model = gensim.models.Word2Vec.load('output_models/user_local_context_v1_large.txt')

@route('/search/meta/<input_dic>')
def search(input_dic):
	input_dic = eval(input_dic)
	global redis_obj
	temp = []
	temp_res = []
	for pid in input_dic["pids"]:
		try:
			print pid
			pid = "C"+pid
			res = model.most_similar(positive = [pid], topn = 10000)
			temp_res = temp_res +res
		except:
			pass

	for ids in temp_res:
		temp.append(ids[0][1:])
	
	redis_input = input_dic
	redis_input["pids"] = temp
#	print "Redis input : ",redis_input
	print "Redis input : ", len(redis_input)
	result_from_redis = lr.redisSearch(redis_input)
	print type(result_from_redis)	
	return result_from_redis
	
run(host = '0.0.0.0', port = 8000, debug = True) 
