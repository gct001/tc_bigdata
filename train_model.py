#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'James Z'

from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
# from sklearn.grid_search import GridSearchCV
# from sklearn import preprocessing
from sklearn.externals import joblib


def get_vector_X_y(train_data):
    df = pd.read_csv('train_sample/' + train_data)
    train_y = df['label'].values  # dataframe to ndarray
    train_X = df.drop('label', 1).values
    return train_X, train_y


def feature_predo(raw_X):
    train_X = preprocessing.StandardScaler().fit_transform(raw_X)
    return train_X


# n_estimators,maxdepth,min_samples_leaf,min_samples_split,max_features,subsample
def gradient_boosting_classifier(train_X, train_y):
    model = GradientBoostingClassifier(random_state=10)
    model.fit(train_X, train_y)
    joblib.dump(model, 'GBDT.m')


if __name__ == '__main__':
    train_data = 'train_sample.csv'
    train_X, train_y = get_vector_X_y(train_data)
    # train_X = feature_predo(train_X)
    gradient_boosting_classifier(train_X, train_y)
