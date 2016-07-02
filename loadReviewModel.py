#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Akhil Gupta
# @Email:  akhilgupta.official@gmail.com  
# @Github username: @codeorbit
# @Last Modified by:   Akhil Gupta
# @Last Modified time: 2016-07-1

import redis
from bottle import route, run
import gensim
import queryFormation as QF
import re
import urllib2
import helpers
import ast
import requests
redis_obj = redis.Redis(host = 'localhost', port = 6379, db = 3)
model = gensim.models.Word2Vec.load('output_models/music_v4.txt')

@route('/search/review/<query>')
def search(query):
	
	global redis_obj
	tokens = QF.queryTokenize(query)
	print tokens
	res_pid = []
	for key, val in tokens.items():
		if key == "items":
			for item in val:
				print "item : ", item
				res = model.most_similar(positive = [item], topn = 1000)
				res_pid = res_pid + helpers.filterPid(str(res))
		if key == "orig_pid":
			try:
				val = "<"+str(val.lower())+">"
				print val
#				print type(val)
				res = model.most_similar(positive = [val],topn = 1000)
#				print "res :: ",res 
				res_pid = res_pid + helpers.filterPid(res)
				
			except Exception as e:
				print "Exception from review model : ",e
				pass
				
	print "final result length : ", len(res_pid)
	meta_module_input = {}
	meta_module_input = tokens
	meta_module_input["pids"] = res_pid[:10]
	print "meta module ",meta_module_input 
	result_meta_module = requests.get('''http://173.255.113.135:8000/search/meta/'''+str(meta_module_input))
	print type(eval(result_meta_module.text))	
	return eval(result_meta_module.text)
run(host = '0.0.0.0', port = 8080 , debug = True)
