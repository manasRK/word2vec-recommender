#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Akhil Gupta
# @Date:   2016-06-21
# @Email:  akhilgupta.official@gmail.com  Github username: @codeorbit
# @Last Modified by:   Akhil Gupta
# @Last Modified time: 2016-06-21

'''
  USAGE : python preProcessing.py <data_folder> <output_file>
'''

import gzip
import os
import sys
import simplejson
import json
import timeit
import redis
import glob
import np



from phrases_extractor import get_phrases

price_obj = redis.Redis("localhost", port=6379, db=1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_CNT = 0

def getRange(price):

  price  = float(price)
  if price <= 10:
    return 10
  elif 10 < price <= 100:
    return 100
  elif 100 < price <= 250:
    return 250
  elif 250 < price <= 500:
    return 500
  elif 500 < price <= 1000:
    return 1000
  elif 1000 < price <= 2000:
    return 2000
  elif 2000 < price <= 5000:
    return 5000
  elif price > 5000:
    return 9999



def process_phrases(text):
  phrases = get_phrases(text)

  for phrase in phrases:
    text = text.replace(phrase, phrase.replace(' ', '_'))
  return text

def processData(data,category,output_file):
  '''
  INPUT : data, category, output_file
  FUNCTION : writing processed reviews in file
  OUTPUT : output_file.txt
  '''
  global PROCESSED_CNT
  try:
    review = data["reviewText"]
    title = data["summary"]
    all_text = title + ". " + review
    all_text = process_phrases(all_text)
    fobj = open(BASE_DIR+"/output/output.txt","a")
    if len(review.split())>10:
      productId = data["asin"]
      try:
        price = getRange(price_obj.get(productId))
      except:
        price = 0
      final_data = "<" + str(price) + "> <" + category + "> <" + productId + "> " + all_text + " <" + str(price) + "> <" + category + "> <" + productId + ">"
      print final_data
      fobj = open(BASE_DIR+"/"+ output_file + ".txt","a")
      fobj.write(final_data+"\n")
      PROCESSED_CNT+=1
  except Exception as e:
    print "Exception ",e
    fobj.write(str({"EXCEPTION":e,"DATA":data}))
    pass

def parse(filename):
  g = gzip.open(filename,"r")
  for l in g:
    yield eval(l)
def loadData(data_folder, output_folder):
  '''
    INPUT : data_folder, output_file 
    FUNCTION : loading data from file 
    OUTPUT : processed data
  '''
  global PROCESSED_CNT
  fobj = open(BASE_DIR+"/output/output.txt","a")
  start = timeit.default_timer()

  for file in glob.glob(BASE_DIR+"/"+data_folder+"/*.json.gz"):
    category = file.strip('reviews json gz . _').replace('_', ' ')
    for row in parse(BASE_DIR+"/"+data_folder+"/"+file):
      processData(row, category, output_folder)
  
  stop = timeit.default_timer()
  total_time  = np.round(stop - start)
  print "processing time ", total_time
  fobj.write(str({"TOTAL_TIME":total_time}+"\n"))
  fobj.write(str({"PROCESSED_CNT":PROCESSED_CNT}))

loadData(sys.argv[1], sys.argv[2])