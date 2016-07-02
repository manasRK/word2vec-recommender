#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Akhil Gupta
# @Email:  akhilgupta.official@gmail.com  
# @Github username: @codeorbit
# @Last Modified by:   Manas Ranjan Kar
# @Last Modified time: 2016-06-28



import json 
import gzip 
import redis


data_obj = redis.Redis("localhost", port=6379, db=9) # 2, 9

def preProcess(row):
    #print row
    temp = []
    
    productId = row["asin"]
    
    try:
        boughtTogether = row["related"]["bought_together"]
        for ele in boughtTogether:
            temp.append(ele)
    except:
        pass
    
    try:
        alsoBought = row["related"]["also_bought"]
        for ele in alsoBought:
            temp.append(ele)
    except:
        pass
    
    try:
        alsoViewed = row["related"]["also_viewed"]
        for ele in alsoViewed:
            temp.append(ele)
    except:
        pass
    
    if temp ==[]:
        pass
    else:
        data_obj.set(productId, temp)
    
    

def parse(path): 
    g = gzip.open(path, 'rb') 
    for l in g: 
        yield (eval(l)) 
 
def main():
    count = 0
    for row in parse("data/metadata/meta_Clothing_Shoes_and_Jewelry.json.gz"): 
        count+=1
        if( (count)%5000 == 0 ):
            print "Metas loaded: %s" % ( count )
        preProcess(row)
main()

print 'Loaded !'