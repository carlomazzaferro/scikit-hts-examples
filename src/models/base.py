"""
See notebook to get an understanding of how the model parameters were decided
"""

from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(bootstrap=True, ccp_alpha=0.0,
                           criterion='mse', max_depth=None,
                           max_features='auto', max_leaf_nodes=None,
                           max_samples=None,
                           min_impurity_decrease=0.0,
                           min_impurity_split=None,
                           min_samples_leaf=1, min_samples_split=2,
                           min_weight_fraction_leaf=0.0,
                           n_estimators=100, n_jobs=None,
                           oob_score=False, random_state=None,
                           verbose=0, warm_start=False)
