#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Akhil Gupta
# @Email:  akhilgupta.official@gmail.com  
# @Github username: @codeorbit
# @Last Modified by:   Akhil Gupta
# @Last Modified time: 2016-07-1

import re
def filterPid(res):
	res_pid = []  
	pids = re.findall(r'(?<=\<).+?(?=\>)',res)
	for pid in pids:
		res_pid.append(pid.upper())
	return res_pid