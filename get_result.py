#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'James Z'

import pdb
import csv

def get_result():
	result_line_num = set()
	with open('result.txt', 'rb') as f:
		num = 1
		lines = f.readlines()
		for line in lines:
			linedata = line[1:-2].strip()
			data = linedata.split('  ')
			if float(data[1].strip()) > 0.03:
				result_line_num.add(num)
			num += 1
		print len(result_line_num)

	csvfile = file('final_result.csv', 'wb')
	writer = csv.writer(csvfile)

	num = 0# online.csv 多了一行列名，csv.reader 不会跳过第一行
	temp_ui = set()
	for line in csv.reader(file('train_sample/22to31_combine.csv', 'rb')):
		if num in result_line_num:
			temp_ui.add((line[0], line[1]))
		num = num + 1

	sub_item = set()
	for line in csv.reader(file('tianchi_fresh_comp_train_item.csv', 'rb')):
		sub_item.add(line[0])

	count = 0

	for ui in temp_ui:
		if ui[1] in sub_item:
			writer.writerow((ui[0], ui[1]))
			count += 1

	print count

if __name__ == '__main__':
	get_result()