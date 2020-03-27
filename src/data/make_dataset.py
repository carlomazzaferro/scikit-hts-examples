"""
Generate train and test datasets, doin
"""
import os

import pandas
from sklearn.model_selection import train_test_split

from src.settings import drop


def create_datasets(input_dir: str, train_output_dir: str):
    df = pandas.read_csv(os.path.join(input_dir, 'base.csv'))
    x = df.drop(drop, 1).copy()
    y_cnt = df['cnt']

    x_train, x_test, y_train, y_test = train_test_split(x.drop(['cnt', 'registered', 'casual'], 1), y_cnt)
    x_train.to_csv(os.path.join(train_output_dir, 'x_train.csv'))
    x_test.to_csv(os.path.join(train_output_dir, 'x_test.csv'))
    y_train.to_csv(os.path.join(train_output_dir, 'y_train.csv'))
    y_test.to_csv(os.path.join(train_output_dir, 'y_test.csv'))
