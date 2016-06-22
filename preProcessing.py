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
import timeit


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def getRange(price):
  
  if price != "unknown":
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
  else:
    return 0 


def processData(data,category,output_file):
  '''
  INPUT : data, category, output_file
  FUNCTION : writing processed reviews in file
  OUTPUT : output_file.txt
  '''
  
  try:
    review = data["review/text"]
    if len(review.split())>10:
      print "old price ", data["product/price"], "new price ", getRange(data["product/price"])
      price = getRange(data["product/price"])
      final_data = "<" + str(price) + "> <" + category + "> <" + data["product/productId"] + "> " + data["product/title"] + ". " + review + " <" + str(price) + "> <" + category + "> <" + data["product/productId"] + ">"
      print final_data
      fobj = open(BASE_DIR+"/"+ output_file + ".txt","a")
      fobj.write(final_data+"\n")

  except Exception as e:
    print e
    pass

def parse(filename):
  
  f = gzip.open(filename, 'r')
  entry = {}
  for l in f:
    l = l.strip()
    colonPos = l.find(':')
    if colonPos == -1:
      yield entry
      entry = {}
      continue
    eName = l[:colonPos]
    rest = l[colonPos+2:]
    entry[eName] = rest
  yield entry


def loadData(data_folder, output_folder):
  '''
    INPUT : data_folder, output_file 
    FUNCTION : loading data from file 
    OUTPUT : processed data
  '''
  
  start = timeit.default_timer()

  for file in os.listdir(BASE_DIR+"/"+data_folder):
    category = file.strip('reviews json gz . _').replace('_', ' ')
    for row in parse(BASE_DIR+"/"+data_folder+"/"+file):
      processData(row, category, output_folder)
  
  stop = timeit.default_timer()

  print "processing time ", stop - start

loadData(sys.argv[1], sys.argv[2])