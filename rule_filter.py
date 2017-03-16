#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'James Z'

import csv

def filter18():
	buy18 = set()
	with open('18buy.csv', 'rb') as fr:
		for line in fr:
			line = line.split(',')
			buy18.add((line[0], line[1]))

	sub_item = set()
	for line in csv.reader(file('tianchi_fresh_comp_train_item.csv', 'rb')):
		sub_item.add(line[0])

	with open('18.23basket.csv', 'rb') as fr, open('rule18.csv', 'wb') as fw:
		i = 0
		for line in fr:
			line = line.split(',')
			if (line[0],line[1]) not in buy18:
				if line[1] in sub_item:
					fw.write(','.join([line[0],line[1]]) + '\n')
					i += 1
		print i


def combine():
	set1 = set()
	for line in csv.reader(file('final_result.csv', 'rb')):
		set1.add((line[0],line[1]))

	set2 = set()
	for line in csv.reader(file('rule18.22.csv', 'rb')):
		set2.add((line[0],line[1]))
		
	set3 = set1 | set2
	print len(set3),len(set1),len(set2)

	csvfile = file('tianchi_mobile_recommendation_predict.csv', 'wb')
	writer = csv.writer(csvfile)
	for ui in set3:
		writer.writerow((ui[0], ui[1]))


if __name__ == '__main__':
	# filter18()
	combine()