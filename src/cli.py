# -*- coding: utf-8 -*-

"""Console script for scikit-hts-examples."""

import click

from src.data.make_dataset import create_datasets
from src.models.predict_model import predict_results
from src.models.train_model import train_clf

__author__ = "Carlo Mazzaferro"
__copyright__ = "Carlo Mazzaferro"


@click.group()
def cli():
    """Facet's CLI. With it, you can perform pretty much all operations you desire
        Shown below are all the possible commands you can use.
        Run ::
            $ facet --help
        To get an overview of the possibilities.
    """


@cli.command()
@click.option('--raw', required=True)
@click.option('--train', required=True)
def make_dataset(raw, train):
    create_datasets(raw, train)


@cli.command()
@click.option('--train', required=True)
@click.option('--store', is_flag=True, default=True,  required=False)
@click.option('--report', is_flag=True, default=True,  required=False)
def train_model(train, store, report):
    train_clf(train, store, report)


@cli.command()
@click.option('--file', required=True)
def predict(file):
    predict_results(test_file=file)


cli.add_command(make_dataset)
cli.add_command(train_model)
cli.add_command(predict)

