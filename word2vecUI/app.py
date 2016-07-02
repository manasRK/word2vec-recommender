#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Akhil Gupta
# @Email:  akhilgupta.official@gmail.com  
# @Github username: @codeorbit
# @Last Modified by:   Manas Ranjan Kar
# @Last Modified time: 2016-07-1



from flask import Flask, render_template
import test as t
import urllib2
import requests

app = Flask(__name__)

@app.route("/")
def template_test():
    return render_template('search.html',title = "WORD2VEC") 

@app.route("/search/review/<query>")
def search(query = ""):

	resDic = requests.get("http://173.255.113.135:8080/search/review/"+str(query))
	resDic = eval(resDic.text)
	print type(resDic)	
	result = resDic
	print result
	return render_template('result.html',result = result ,title = query.upper())

if __name__ == '__main__':
    app.run(debug=True, threaded = True)
