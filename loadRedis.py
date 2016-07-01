#!/usr/bin/env python
# @Author: Akhil Gupta
# @Date:   2016-06-30
# @Email: akhilgupta.official@gmail.com 
# @Github Username: codeorbit

import ast
import redis
redis_obj = redis.Redis(host = 'localhost', port = 6379, db =3)
def redisSearch(input_dic):
#	input_dic = eval(input_dic)
	global redis_obj
	res_dic = {}
#	pids = ['B005MYAMS4','B00534M24A','B0043M666I','B000GHG9VG','0299128741']
	res_count = 0
	try:
		price = float(input_dic["price"]) 
	except:
		price = 0.0
	print "price : ",price
	for ids in input_dic["pids"]:
		if res_count<=15:
			try:
				res = redis_obj.get(ids)
				res = eval(res)
#				print "price from redis : ", float(res[0])
				if len(res)==2 and float(res[0])>price:
					res.insert(0,ids)
					res.insert(2,"music")
					res_dic.update({ids:res})
					res_count = res_count+1		
			except:
				pass
	return res_dic
