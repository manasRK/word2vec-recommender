#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Akhil Gupta
# @Email:  akhilgupta.official@gmail.com  
# @Github username: @codeorbit
# @Last Modified by:   Akhil Gupta
# @Last Modified time: 2016-07-1

import re
'''
Types of query 
q1 = "michael jackson, jazz, price 50"
q2 = "michael jackson"
q3 = "pid B123"
'''
def queryTokenize(query):
	
	tokens = {}
	tokens["items"] = []  #for one or more item in query e.g. q1
	for ele in query.split(","):
		ele = ele.strip()
		if re.search('\d+',ele):
			temp = ele.split()
			if temp[0] == "pid":
				tokens.update({"orig_pid":temp[1]})
			if temp[0] == "price":
				tokens.update({"price":temp[1]})
		else:
		
			tokens["items"].append(ele.replace(" ","_"))
			

	return tokens

