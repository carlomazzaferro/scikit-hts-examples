"""
Generate train and test datasets, doin
"""

import os
import json

import pandas


def create_datasets(input_dir: str, train_output_dir: str, dataset_name: str):
    input_path = os.path.join(input_dir, dataset_name)
    output_path = os.path.join(train_output_dir, dataset_name)

    if not os.path.exists(input_path):
        os.makedirs(input_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if dataset_name == 'm5':
        _create_m5_dataset(input_path, output_path)


def _create_m5_dataset(input_path, output_path):
    train = pandas.read_csv(os.path.join(input_path, 'sales_train_validation.csv'),
                            encoding='utf-8',
                            engine='c')

    # Ensures uniqueness of category, dept, and item across hierarchies
    train['cat_id'] = (train['store_id'] + '_' + train['cat_id'])
    train['dept_id'] = (train['store_id'] + '_' + train['dept_id'])
    train['id'] = (train['store_id'] + '_' + train['id'])

    calendar = pandas.read_csv(os.path.join(input_path, 'calendar.csv'))
    day_cols = [col for col in train.columns if col.startswith('d_')]
    idx = [int(col.split('d_')[1]) for col in day_cols]
    train_date_id = pandas.to_datetime(calendar[calendar.d.apply(lambda x: int(x.split('d_')[1])).isin(idx)].date)

    def transpose(df, column, index, day_col):
        """
        Turn the row oriented time series into a column oriented one
        """
        ts = []
        new_cols = df[column].unique()

        for value in new_cols:
            value_ts = df[train[column] == value]
            vertical = value_ts[day_col].sum().T
            vertical.index = index
            ts.append(vertical)
        return pandas.DataFrame({k: v for k, v in zip(new_cols, ts)})

    state_ts = transpose(train, 'state_id', train_date_id, day_cols)
    store_ts = transpose(train, 'store_id', train_date_id, day_cols)
    cat_ts = transpose(train, 'cat_id', train_date_id, day_cols)
    dept_ts = transpose(train, 'dept_id', train_date_id, day_cols)
    item_ts = transpose(train, 'id', train_date_id, day_cols)

    transposed = pandas.concat([state_ts, store_ts, cat_ts, dept_ts, item_ts], 1)

    # Total column is the root node -- the sum of of all demand across all stores (we have data on, at least)
    transposed['total'] = transposed['CA'] + transposed['TX'] + transposed['WI']
    transposed.to_csv(os.path.join(output_path, 'hierarchy.csv'))

    states = train.state_id.unique()
    stores = train.store_id.unique()
    depts = train.dept_id.unique()
    cats = train.cat_id.unique()
    items = train.id.unique()

    # Here we build the tree as a dictionary. Each node (key in dict) has a list of
    # children value in dict, which in turn may also be a key in the dict, and have
    # children as well
    total = {'total': list(states)}
    state_h = {k: [v for v in stores if v.startswith(k)] for k in states}
    store_h = {k: [v for v in cats if v.startswith(k)] for k in stores}
    dept_h = {k: [v for v in depts if v.startswith(k)] for k in cats}
    item_h = {k: [v for v in items if v.startswith(k)] for k in depts}

    hierarchy = {**total, **state_h, **store_h, **dept_h, **item_h}

    with open(os.path.join(output_path, 'hierarchy.json'), 'w') as j:
        json.dump(hierarchy, j)
