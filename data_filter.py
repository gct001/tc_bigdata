#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'James Z'

from itertools import islice

# 4直接计算outlier,耗时太长
def del_outlier_user():
	print 'loading data...'
	uscan = {}
	ubasket = {}
	ubuy = {}
	# 记录用户购买次数,浏览次数，加购物车次数
	with open('uihas3.csv', 'rb') as f:
		for line in f:
			line = line.split(',')
			if line[2] == '4':
				if line[0] in ubuy.keys():
					ubuy[line[0]] += 1
				else:
					ubuy[line[0]] = 1
			elif line[2] == '1':
				if line[0] in uscan.keys():
					uscan[line[0]] += 1
				else:
					uscan[line[0]] = 1
			elif line[2] == '2':
				if line[0] in ubasket.keys():
					ubasket[line[0]] += 1
				else:
					ubasket[line[0]] = 1
	# 计算用户浏览次数和购买次数的比值
	print len(ubuy)
	scan_buy = {}
	for k,v in uscan.items():
		if k in ubuy.keys():
			rel = v // ubuy[k]
			scan_buy[k] = rel

	basket_buy = {}
	for k,v in basket_buy.items():
		if k in ubuy.items():
			rel = v // ubuy[k]
			basket_buy[k] = rel

	cutuser = set()
	# 此处数字要通过分析后才可以初步估计，最好在训练模型后，进行交叉验证
	for k,v in scan_buy.items():
		if v >= 50:
			cutuser.add(k)

	print '浏览／购买比值过大人数%d' % len(cutuser)

	for k,v in basket_buy.items():
		if v >= 10:
			cutuser.add(k)

	print '+购物车／购买比值过大人数%d' % len(cutuser)

	for u in cutuser:
		if ubuy[u] > 20:
			cutuser.discard(u)
	print '从cutuser中删除购买物品较多的人%d' % len(cutuser)

	with open('uihas3.csv', 'rb') as fr, open('uihas4.csv', 'wb') as fw:
		for line in fr:
			line = line.split(',')
			if line[0] not in cutuser:
				fw.write('%s' % ','.join(line))

# 4通过pandas分析之后进行筛选，快速，这组参数会删掉1088人，此时剩余10377人，4373137条数据
def del_outlier_user2():
	cutuser = set()
	with open('bizhi.csv','rb') as fr:
		for line in islice(fr, 1, None):# 跳过第一行
			line = line.split(',')
			if float(line[7]) > 80:# 行为1/4
				cutuser.add(line[0])
			if float(line[8]) > 10:# 行为3/4
				cutuser.add(line[0])
			if int(line[4]) > 20:# 购买量>20
				cutuser.discard(line[0])
		print len(cutuser)
	with open('uihas3.csv', 'rb') as fr, open('uihas4.csv', 'wb') as fw:
		i = 0
		for line in fr:
			line = line.split(',')
			if line[0] not in cutuser:
				fw.write('%s' % ','.join(line))
				i += 1
		print i


# 1删除没有收藏，购物车，购买行为的用户	
def del_noaction_user():
	## 选择有交互(收藏，购物车，购买)的ui对
	ui = set()
	with open('tianchi_fresh_comp_train_user.csv', 'rb') as fr:
		for line in fr:
			line = line.split(',')
			if line[2] in ('2', '3', '4'):
				ui.add((line[0],line[1]))
	with open('tianchi_fresh_comp_train_user.csv', 'rb') as fr, open('uihas.csv', 'wb') as fw:
		for line in fr:
			line = line.split(',')
			if (line[0], line[1]) in ui:
				fw.write('%s' % ','.join(line))

# 2删除没有购买行为的用户
def del_nobuy_user():
	ubuy = set()
	with open('uihas.csv', 'rb') as f:
		for line in f:
			line = line.split(',')
			if line[2] == '4':
				ubuy.add(line[0])

	with open('uihas.csv', 'rb') as fr, open('uihas2.csv', 'wb') as fw:
		for line in fr:
			line = line.split(',')
			if line[0] in ubuy:
				fw.write('%s' % ','.join(line))
	print '购买物品人数%d' % len(ubuy)

# 3删除对商品子集无交互的用户
def del_noaction_user_part():
	item = set()
	with open('tianchi_fresh_comp_train_item.csv', 'rb') as fr:
		for line in fr:
			item.add(line.split(',')[0])
	print '商品种数%d' % len(item)

	user = set()
	with open('uihas2.csv', 'rb') as fr:
		for line in fr:
			line = line.split(',')
			if line[1] in item:
				user.add(line[0])

	with open('uihas2.csv', 'rb') as fr, open('uihas3.csv', 'wb') as fw:
		for line in fr:
			line = line.split(',')
			if line[0] in user:
				fw.write('%s' % ','.join(line))

if __name__ == '__main__':
	pass

