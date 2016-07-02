#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Akhil Gupta
# @Date:   2016-06-20
# @Email:  akhilgupta.official@gmail.com  
# @Github username: @codeorbit
# @Last Modified by:   Akhil Gupta
# @Last Modified time: 2016-07-1



import json 
import gzip 
import redis

data_obj = redis.Redis("localhost", port=6379, db=2)

def preProcess(row):
	print row
	temp = []
	
	productId = row["asin"]
	
	try:
		boughtTogether = row["related"]["bought_together"]
		for ele in boughtTogether:
			temp.append("b_t_"+ele)
	except:
		pass
	
	try:
		alsoBought = row["related"]["also_bought"]
		for ele in alsoBought:
			temp.append("a_b_"+ele)
	except:
		pass
	
	try:
		alsoViewed = row["related"]["also_viewed"]
		for ele in alsoViewed:
			temp.append("a_v_"+ele)
	except:
		pass
	
	if temp ==[]:
		pass
	else:
		data_obj.set(productId, temp)
	
	

def parse(path): 
	g = gzip.open(path, 'r') 
	for l in g: 
		yield (eval(l)) 
 
def main():
	count = 0
	for row in parse("metadata.json.gz"): 
		count+=1
		print count
		preProcess(row)


main()