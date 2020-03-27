"""
Custom data transformers. Wrapped in the scikit-leatn api so that they can be placed inside a pipeline transformer
"""
from functools import partial

import numpy
import pandas
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder


def cos(nunique, p):
    return numpy.cos(2*numpy.pi*p/nunique)


def sin(nunique, p):
    return numpy.sin(2*numpy.pi*p/nunique)


class DataFrameOHETransformer(BaseEstimator, TransformerMixin):

    def __init__(self, feature_names=None):
        self.fnames = feature_names
        self.col_transf = None
        self.fit_est = None
        self.features = None

    def fit(self, X, y=None):
        ohes = []
        for feature in self.fnames:
            ohes.append(
                (feature, OneHotEncoder(dtype='int'), [feature])
            )
        self.col_transf = ColumnTransformer(ohes, remainder='drop')
        self.col_transf.fit(X, y)
        return self

    def fit_transform(self, X, y=None, **fit_params):
        return self.fit(X, y).transform(X, y)

    def transform(self, X, y=None):
        tf = pandas.DataFrame(self.col_transf.transform(X),
                              columns=self.col_transf.get_feature_names(),
                              index=X.index)
        return pandas.concat([tf, X.drop(self.fnames, 1)], 1)


class CyclicFeatureTransform(BaseEstimator, TransformerMixin):

    def __init__(self, feature_names=None):
        self.fnames = feature_names
        self.fnx = self.fny = {k: None for k in feature_names}

    def fit(self, X, y=None):
        for feature in self.fnames:
            nunique = X[feature].nunique()
            self.fnx[feature] = partial(sin, nunique)
            self.fny[feature] = partial(cos, nunique)
        return self

    def transform(self, X, y=None, **fit_params):
        for feature in self.fnames:
            col = X[feature]
            x_name = f'x{feature}'
            y_name = f'y{feature}'
            X[x_name] = col.apply(self.fnx[feature])
            X[y_name] = col.apply(self.fnx[feature])
        x = X.drop(self.fnames, 1)
        return x

    def fit_transform(self, X, y=None, **fit_params):
        return self.fit(X, y).transform(X, y)
