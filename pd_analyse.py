#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'James Z'

## data = data.groupby['user_id','behavior_type'].count().iloc[:,:1]
## data.to_csv('1234user.csv', index = False)

## data = pd.read_csv('1234.csv')
## data1 = data[data.behavior_type==1]
## data2 = data[data.behavior_type==4]
## data3 = data[data.behavior_type==3]
## data2.columns = ['user_id','behavior_type4','num4']
## data3.columns = ['user_id','behavior_type3','num3']
## data4 = pd.merge(data1,data2,on='user_id')
## data5 = pd.merge(data3,data4,on='user_id')
## bizhi14 = data6['num']/data6['num4']
## bizhi34 = data6['num3']/data6['num4']
## data5.insert(7,'bizhi14',bizhi14)
## data5.insert(8,'bizhi34',bizhi34)
## data5.to_csv('bizhi.csv', index = False, float_format = '%.1f')
## 此时一共有11465人,3981802次浏览，516753次加购物车，178596次购买
## 购买数量>10有5580人，>20有2703人，>30有1419人，>50有489人
## 浏览／购买比值
## data6[data6.bizhi14>20].count()# 5298
## data6[data6.bizhi14>40].count()# 2217
## data6[data6.bizhi14>50].count()# 1563
## data6[data6.bizhi14>60].count()# 1180
## data6[data6.bizhi14>80].count()# 701
## data6[data6.bizhi14>100].count()# 467
## data6[data6.bizhi14>200].count()# 121
## 购物车／购买比值
## data6[data6.bizhi34==1].count()# 5430!!!
## data6[data6.bizhi34>5].count()# 2257
## data6[data6.bizhi34>7].count()# 1410
## data6[data6.bizhi34>8].count()# 1142
## data6[data6.bizhi34>10].count()# 804
## data6[data6.bizhi34>15].count()# 405
## data6[data6.bizhi34>20].count()# 226