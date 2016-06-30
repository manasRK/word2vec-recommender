#!/usr/bin/env python
# @Author: Akhil Gupta
# @Date:   2016-06-30
# @Email: akhilgupta.official@gmail.com 
# @Github Username: codeorbit

import redis
from bottle import route, run


redis_obj = redis.Redis(host = 'localhost', port = 6379, db =3)
@route('/search/redis/<input_dic>')
def search(input_dic):
	input_dic = eval(input_dic)
	global redis_obj
	res_dic = {}
#	pids = ['B005MYAMS4','B00534M24A','B0043M666I','B000GHG9VG','0299128741']
	for ids in input_dic["pids"]:
		try:
			res = redis_obj.get(ids)
			if len(eval(res))==4:
				res_dic.update({ids:res})
		except:
			pass
	return res_dic
run(host = '0.0.0.0', port = 8002, debug = True) 
	
