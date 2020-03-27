"""
Main module responsible for training the model and serializing. Will also generate reports
"""

import os

import pandas
from sklearn.externals import joblib
from sklearn.metrics import r2_score, max_error, mean_absolute_error
from sklearn.pipeline import Pipeline

from src.models.base import rf
from src.settings import MODELS_PATH, REPORTS_PATH, cyclic, categorical
from src.transformers.build_features import DataFrameOHETransformer, CyclicFeatureTransform


def train_clf(train_path, save=True, report=True):

    x_train, x_test, y_train, y_test = [pandas.read_csv(os.path.join(train_path, i), index_col=0)
                                        for i in ['x_train.csv', 'x_test.csv', 'y_train.csv', 'y_test.csv']]

    cyclic_trans = CyclicFeatureTransform(feature_names=cyclic)
    ohe_trans = DataFrameOHETransformer(feature_names=categorical)

    pipe = Pipeline([
        ('categ', ohe_trans),
        ('cyclic', cyclic_trans),
        ('reg', rf)
    ])

    pipe.fit(x_train, y_train)
    if save:
        store(pipe)

    if report:
        produce_report(pipe, x_train, x_test, y_train, y_test)


def produce_report(pipeline, x_train, x_test, y_train, y_test):
    with open(os.path.join(REPORTS_PATH, 'results.txt'), 'w') as rep:
        for sc in [max_error, mean_absolute_error, r2_score]:
            score = r2_score(y_test, pipeline.predict(x_test))
            rep.write(f'{str(sc.__name__)}: {score}\n')


def store(mdl):
    p = os.path.join(MODELS_PATH, 'pipe.joblib')
    joblib.dump(mdl, p)
