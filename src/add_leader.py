import pandas as pd
import numpy as np
import os
from multiprocessing import Pool, cpu_count

def detect_leader(df):
    '''Detects leaders for each vehicle in the dataframe.
    
    inputs
    - df: the tested dataframe where leaders are not flagged

    returns
    - df_out: dataframe where thee leader has been flagged
    '''
    df_out = pd.DataFrame(columns=df.columns)
    df_out['leader'] = []
    df['r'] = np.sqrt(df['xloc-kf']**2 + df['yloc-kf']**2)
    df['theta'] = np.arctan2(df['yloc-kf'], df['xloc-kf'])
    lanes = pd.unique(df['lane-kf'])

    for t in pd.unique(df['time']):
        at_t = df[df['time'] == t]
        for l in lanes:
            lane_at_t = at_t[at_t['lane-kf'] == l]
            lane_at_t.sort_values(by='r', ascending=False, inplace=True)
            lane_at_t = lane_at_t.reset_index()
            leader = [np.nan]
            for k in range(len(lane_at_t['ID']) - 1):
                leader.append(lane_at_t['ID'][k])
            lane_at_t['leader'] = leader
            df_out = pd.concat([df_out, lane_at_t])
    return df_out
