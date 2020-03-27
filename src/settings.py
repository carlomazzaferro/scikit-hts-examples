RAW_DATA_PATH = 'data/raw'
PROCESSED_DATA_PATH = 'data/processed'
OUTPUT_DATA_PATH = 'data/output'
MODELS_PATH = 'models'
REPORTS_PATH = 'reports'


continuous = ['temp', 'atemp','hum', 'windspeed', 'registered', 'cnt', 'casual', 'yr']
cyclic = ['season', 'mnth', 'hr', 'weekday']
categorical = ['holiday', 'workingday', 'weathersit']
drop = ['instant', 'dteday']
all_cols = continuous + cyclic + categorical + drop
