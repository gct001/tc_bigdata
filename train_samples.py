#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'James Z'

import fetch_feature
import os
import pandas as pd


def fetch_slide_feature():
    start = 1
    end = 10

    for index in range(21):
        fetch_feature.fetch_ui_f(start, end)
        fetch_feature.fetch_user_f(start, end)
        fetch_feature.fetch_item_f(start, end)
        start += 1
        end += 1


def combine_feature():
    start = 1
    end = 10

    for _ in range(21):
        name = str(start) + 'to' + str(end)
        filename1 = name + '_i_f.csv'
        filename2 = name + '_u_f.csv'
        filename3 = name + '_ui_f.csv'
        filename4 = name + '_combine.csv'

        df1 = pd.read_csv('item_feature/' + filename1)
        df2 = pd.read_csv('user_feature/' + filename2)
        df3 = pd.read_csv('ui_feature/' + filename3)
        df4 = pd.merge(df1, df2, on=['user_id', 'item_id'])
        df4 = pd.merge(df4, df3, on=['user_id', 'item_id'])

        df4.to_csv('train_sample/' + filename4, index=False)

        start += 1
        end += 1


def combine_all():
    files = os.listdir('train_sample/')
    if '.DS_Store' in files:
        files.remove('.DS_Store')

    print len(files)

    dfs = [pd.read_csv(f) for f in files]
    total_df = pd.concat(dfs)

    print total_df.count()  # 5301880
    print total_df[total_df.label == 1].count()  # 34597

    totaldf = totaldf.drop('item_id', 1)
    totaldf = totaldf.drop('user_id', 1)
    
    total_df.to_csv('train_sample/train_sample.csv', index=False)

if __name__ == '__main__':
    combine_feature()
