#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'James Z'

import pandas as pd
from sklearn.externals import joblib
from sklearn import cross_validation, metrics


def modify_online_data():
    df = pd.read_csv('train_sample/22to31_combine.csv')
    df = df.drop('item_id', 1)
    df = df.drop('user_id', 1)
    df.to_csv('online_sample/online.csv', index=False)


def modify_data(csvname):
	df = pd.read_csv('train_sample/'+csvname)
    df = df.drop('item_id', 1)
    df = df.drop('user_id', 1)
    return df

def get_online_data():
    df = pd.read_csv('online_sample/online.csv')
    test_X = df.drop('label', 1).values
    return test_X


def get_online_result(test_X):
    model = joblib.load('GBDT.m')
    y_predprob = model.predict_proba(test_X)
    with open('result.txt', 'w') as f:
        for i in range(len(y_predprob)):
            f.write(str(y_predprob[i]) + '\n')


def predict(test_X, test_y):
    model = joblib.load('GBDT.m')
    y_pred = model.predict(test_X)
    y_predprob = model.predict_proba(test_X)

    print "Accuracy : %.4g" % metrics.accuracy_score(test_y, y_pred)
    print "AUC Score (Train): %f" % metrics.roc_auc_score(test_y, y_predprob)
    print 'F1 Score: %f' % metrics.f1_score(test_y, y_pred)


if __name__ == '__main__':
    # csvname = '10to19_combine.csv'
    # test_df = modify_data(csvname)
    # test_y = test_df['label'].values  # dataframe to ndarray
    # test_X = test_df.drop('label', 1).values
    # predict(test_X,test_y)
	test_X = get_online_data()
    get_online_result(test_X)