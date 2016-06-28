#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Akhil Gupta
# @Date:   2016-06-28
# @Email:  akhilgupta.official@gmail.com  Github username: @codeorbit
# @Last Modified by:   Akhil Gupta
# @Last Modified time: 2016-06-28


import redis
import gzip

robj = redis.Redis("localhost", port=6379, db=3)

def redisPush(data):
	
	product_id = data["asin"]
	dic = {}
	val_list = []
	try:
		title = data["title"]
		val_list.append(title)
	except:
		pass
	try:
		price = data["price"]
		val_list.append(price)
	except:
		pass
	try:
		category = data["salesRank"].keys()[0]
		val_list.append(category)
	except:
		pass
	try:
		img_url = data["imUrl"]
		val_list.append(img_url)
	except:
		pass

	robj.set(product_id, val_list)



def parse(path):
  g = gzip.open(path, 'r')
  for l in g:
    yield eval(l)

print 'Starting loading to Redis !'

for l in parse("metadata.json.gz"):
	redisPush(l)

print 'Finished loading to Redis !'