#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'James Z'

from collections import defaultdict
# 时间间隔太远参考性低，正负样本分布不均，采取滑动窗口
# 11.18号是第一天，以10天为滑窗进行特征提取，如11.18～12.27，12.28号贴label
# 为了避免双十二影响，采用对数平滑?

# ui_f,需扩展，加入购物车未购买，最后访问距label日间距，行为天数
# 四种行为次数
def fetch_ui_f(start, end):
	ui_set = set()
	ui_dict = [{} for i in range(4)]
	ui_label = set()
	with open('uihas4.csv', 'rb') as fr:	
		for line in fr:
			line = line.split(',')
			ui = (line[0], line[1])			
			type_ = int(line[2]) - 1
			time = line[-1][:10].split('-')
			month = int(time[1])
			day = int(time[2])
			index = (month - 11) * 30 + (day - 17)
			if index >= start and index <= end:
				ui_set.add(ui)
				if ui in ui_dict[type_]:
					ui_dict[type_][ui] += 1
				else:
					ui_dict[type_][ui] = 1

			if index == end + 1 and type_ == 3:
				ui_label.add(ui)

	filename = str(start) + 'to' + str(end) + '_ui_f.csv'
	with open('ui_feature/' + filename, 'wb') as fw:
		fw.write('user_id,item_id,scan,store,basket,buy,label\n')
		for ui in ui_set:
			ui_l = list(ui)# 使用list来存储打印行
			for i in range(4):
				ui_l.append(str(ui_dict[i][ui]) if ui in ui_dict[i] else '0')
			ui_l.append('1' if ui in ui_label else '0')
			fw.write(','.join(ui_l) + '\n')

# 四种行为的次数，四种行为的商品数，行为天数，浏览量／购买量，购物车量／购买量,其他行为量／购买量，浏览商品数／购买商品数，购物车商品数／购买商品数，其他行为商品数／购买商品数
# 扩展：行为后第二天购买率，平滑处理次数,label日前12小时
def fetch_user_f(start, end):
	ui_set = set()# 记录ui对，便于贴标签
	u_i_num = [defaultdict(dict) for _ in range(4)]# 记录四种行为用户的商品访问量,[{u:{i1:v1, i2:v2, ...}, ...}, {}, {}, {}]
	u_actday = defaultdict(set)# 记录行为天数
	with open('uihas4.csv', 'rb') as fr:
		for line in fr:
			line = line.split(',')
			u = line[0]
			i = line[1]
			ui = (u, i)		
			type_ = int(line[2]) - 1
			time = line[-1][:10].split('-')
			month = int(time[1])
			day = int(time[2])
			index = (month - 11) * 30 + (day - 17)
			if index >= start and index <= end:
				ui_set.add(ui)
				u_actday[u].add(index)
				if u in u_i_num[type_]:
					if i in u_i_num[type_][u]:
						u_i_num[type_][u][i] += 1
					else:
						u_i_num[type_][u][i] = 1
				else:
					u_i_num[type_][u][i] = 1

	filename = str(start) + 'to' + str(end) + '_u_f.csv'
	with open('user_feature/' + filename, 'wb') as fw:
		fw.write('user_id,item_id,u_scan,u_store,u_basket,u_buy,u_scan_i,u_store_i,u_basket_i,u_buy_i,u_actday,buy_scan,buy_basket,transfer1,buy_scan_i,buy_basket_i,tranfer2\n')
		for ui in ui_set:
			u = ui[0]
			i = ui[1]
			u_l = list(ui)# 使用list来存储打印行
			for j in range(4):
				u_l.append(str(sum(u_i_num[j][u].values())))
			for k in range(4):
				u_l.append(str(len(u_i_num[k][u])))
			u_l.append(str(len(u_actday[u])))
			u_l.append(str(round(float(sum(u_i_num[0][u].values())) / float(sum(u_i_num[3][u].values())), 1)) if sum(u_i_num[3][u].values()) != 0 else '0')
			u_l.append(str(round(float(sum(u_i_num[2][u].values())) / float(sum(u_i_num[3][u].values())), 1)) if sum(u_i_num[3][u].values()) != 0 else '0')
			u_l.append(str(round(float(sum(u_i_num[0][u].values()) + sum(u_i_num[1][u].values()) + sum(u_i_num[2][u].values())) / float(sum(u_i_num[3][u].values())), 1)) if sum(u_i_num[3][u].values()) != 0 else '0')
			u_l.append(str(round(float(len(u_i_num[0][u])) / float(len(u_i_num[3][u])), 1)) if len(u_i_num[3][u]) != 0 else '0')
			u_l.append(str(round(float(len(u_i_num[2][u])) / float(len(u_i_num[3][u])), 1)) if len(u_i_num[3][u]) != 0 else '0')
			u_l.append(str(round(float(len(u_i_num[0][u]) + len(u_i_num[1][u]) + len(u_i_num[2][u])) / float(len(u_i_num[3][u])), 1)) if len(u_i_num[3][u]) != 0 else '0')
			fw.write(','.join(u_l) + '\n')

# 四种行为次数，四种行为的用户数，浏览量／购买量，购物车量／购买量，总行为数／购买次数，浏览用户／购买用户，购物车用户／购买用户,其他行为用户数。购买用户数，用户平均行为次数(4种行为总数／4种行为总人数)，老客户率
# 扩展：老客户率
def fetch_item_f(start, end):
	ui_set = set()
	old = dict()
	i_u_num = [defaultdict(dict) for _ in range(4)]# 记录四种行为商品的用户访问量,[{i:{u1:v1, u2:v2, ...}, ...}, {}, {}, {}]
	with open('uihas4.csv', 'rb') as fr:
		for line in fr:
			line = line.split(',')
			u = line[0]
			i = line[1]
			ui = (u, i)		
			type_ = int(line[2]) - 1
			time = line[-1][:10].split('-')
			month = int(time[1])
			day = int(time[2])
			index = (month - 11) * 30 + (day - 17)
			if index >= start and index <= end:
				ui_set.add(ui)
				if i in i_u_num[type_]:
					if u in i_u_num[type_][i]:
						i_u_num[type_][i][u] += 1
					else:
						i_u_num[type_][i][u] = 1
				else:
					i_u_num[type_][i][u] = 1
	# 筛选对某一商品多次购买的用户数
	for ui in ui_set:
		u = ui[0]
		i = ui[1]
		if i in i_u_num[3]:
			if u in i_u_num[3][i]:
				if i_u_num[3][i][u] > 1:
					old.setdefault(i, 0)
					old[i] += 1

	filename = str(start) + 'to' + str(end) + '_i_f.csv'
	with open('item_feature/' + filename, 'wb') as fw:
		fw.write('user_id,item_id,i_scan,i_store,i_basket,i_buy,i_scan_u,i_store_u,i_basket_u,i_buy_u,buy_scan,buy_basket,transfer1,buy_scan_u,buy_basket_u,transfer2,u_mean,old\n')
		for ui in ui_set:
			i = ui[1]
			i_l = list(ui)# 使用list来存储打印行
			
			for j in range(4):
				i_l.append(str(sum(i_u_num[j][i].values())))
			for k in range(4):
				i_l.append(str(len(i_u_num[k][i])))
			
			i_l.append(str(round(float(sum(i_u_num[0][i].values())) / float(sum(i_u_num[3][i].values())), 1)) if sum(i_u_num[3][i].values()) != 0 else '0')
			i_l.append(str(round(float(sum(i_u_num[2][i].values())) / float(sum(i_u_num[3][i].values())), 1)) if sum(i_u_num[3][i].values()) != 0 else '0')
			i_l.append(str(round(float(sum(i_u_num[0][i].values()) + sum(i_u_num[1][i].values()) + sum(i_u_num[2][i].values())) / float(sum(i_u_num[3][i].values())), 1)) if sum(i_u_num[3][i].values()) != 0 else '0')
			i_l.append(str(round(float(len(i_u_num[0][i])) / float(len(i_u_num[3][i])), 1)) if len(i_u_num[3][i]) != 0 else '0')
			i_l.append(str(round(float(len(i_u_num[2][i])) / float(len(i_u_num[3][i])), 1)) if len(i_u_num[3][i]) != 0 else '0')
			i_l.append(str(round(float(len(i_u_num[0][i]) + len(i_u_num[1][i]) + len(i_u_num[2][i])) / float(len(i_u_num[3][i])), 1)) if len(i_u_num[3][i]) != 0 else '0')
			i_l.append(str(round(float(sum(i_u_num[0][i].values()) + sum(i_u_num[1][i].values()) + sum(i_u_num[2][i].values()) + sum(i_u_num[3][i].values())) / float(len(i_u_num[0][i]) + len(i_u_num[1][i]) + len(i_u_num[2][i]) + len(i_u_num[3][i])), 1)))
			#添加老用户率（多次购买用户／所有购买用户）标签
			if i in old:
				i_l.append(str(round(float(old[i]) / float(len(i_u_num[3][i])), 1)))
			else:
				i_l.append('0')
			fw.write(','.join(i_l) + '\n')

if __name__ == '__main__':
	pass
