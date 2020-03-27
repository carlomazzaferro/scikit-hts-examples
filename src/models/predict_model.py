"""
Load model stored from path and generate predictions
"""

import os

import pandas
from sklearn.externals import joblib

from src.settings import MODELS_PATH, OUTPUT_DATA_PATH


def predict_results(test_file):
    df = pandas.read_csv(test_file, index_col=0)

    mdl = joblib.load(os.path.join(MODELS_PATH, 'pipe.joblib'))

    df.to_csv(os.path.join(OUTPUT_DATA_PATH, 'output.csv'))
