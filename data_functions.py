import pandas as pd
import json
import matplotlib.pyplot as plt
from datetime import datetime
import os

def load_lines_from_raw(n_lines=50):
    home = os.environ['HOME']
    data_path = os.path.join(home, 'dkb-data', 'raw', 'cdn_20200117-20200123.log')
    lines = []
    with open(data_path, 'r') as f:
        for count, line in enumerate(f):
            #lines.append(line)
            lines.append(json.loads(line))
            if count == n_lines:
                break
        return pd.DataFrame(lines)
    

def create_target_report(target, target_col):
    data_path = os.path.join(os.environ['HOME'], 'dkb-data', 'reports', target_col)
    # change this directory to your code because Flask needs 
    os.makedirs(data_path, exist_ok=True)

    f, axes = plt.subplots(nrows=2)
    f.suptitle(target_col)
    
    _1 = axes[0].plot(target.loc[:, target_col])
    _2 = axes[1].hist(target.loc[:, target_col])

    f.savefig(os.path.join(data_path, 'f1'+'_'+datetime.now().strftime('%d-%m-%y-%H:%m:%s.png') ))
    #f.savefig(os.path.join(data_path, 'f1.png')
    
    f, axes = plt.subplots(nrows = 1)
    f.suptitle(target_col)
    
    _3 = axes.boxplot(target.loc[:, target_col])

    f.savefig(os.path.join(data_path, 'f2'+'_'+datetime.now().strftime('%d-%m-%y-%H:%m:%s.png') ))
    
    
def create_target_report_gleb(target, target_col):

    f, axes = plt.subplots(nrows=2)
    f.suptitle(target_col)
    
    _1 = axes[0].plot(target.loc[:, target_col])
    _2 = axes[1].hist(target.loc[:, target_col])

    return _1


features = [
    'ClientRequestBytes',
    'CacheResponseBytes',
    'OriginResponseTime',
    'ClientCountry',
    'EdgeEndTimestamp'
]
aggs = ['min', 'max', 'mean', 'std', 'count']


def groupby_country(features, aggs, data):
    data = data.loc[:, features]
    cols = data.columns[:3]
    cols = {col: aggs for col in cols}
    countries = data.groupby('ClientCountry').agg(cols)
    new_cols = []
    for col in countries.columns:
        new_cols.append(col[0] + '_' + col[1])
    countries.columns = new_cols
    return countries