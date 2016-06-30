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
import queryFormation as QF
import re
import urllib2
import helpers

redis_obj = redis.Redis(host = 'localhost', port = 6379, db = 3)
model = gensim.models.Word2Vec.load('modelPath')



@route('/search/review/<query>')
def search(query):
	
	global redis_obj
	tokens = QF.queryTokenize(query)
	print tokens
	res_pid = []
	for key, val in tokens.items():
		if key == "items":
			for item in val:
				res = model.most_similar(positive = [item], topn = 1000)
				res_pid = res_pid + helpers.filterPid(res)
		if key == "pid":
			res = model,most_similar(positive = [val],topn = 1000)
				res_pid = res_pid + helpers.filterPid(res)


	meta_module_input["pids"] = res_pid
	meta_module_input["price"] = tokens["price"] 
	result_meta_module = urllib2.urlopen('api call to meta model').read()
	result_meta_module = eval(result_meta_module)
	return result_meta_module
run(host = '0.0.0.0', port = 8000, debug = True) 
