import pandas as pd
import numpy as np
import os
from multiprocessing import Pool, cpu_count


def compute_DHW(df):
    '''Compute Distance Headway (DHW) and Time Headway (THW) for each vehicle in the dataframe.'
 
    inputs
    - df: the tested dataframe where leaders are not flagged
    
    returns
    - df_out: dataframe with, at each frame where it makes sense, DHW and THW'''
    df_out = pd.DataFrame(columns=df.columns)
    df_out['DHW'] = []
    df_out['THW'] = []

    for t in pd.unique(df['time']):
        at_t = df[df['time'] == t]
        for lane in pd.unique(at_t['lane-kf']):
            lane_at_t = at_t[at_t['lane-kf'] == lane]
            lane_at_t.sort_values(by='r', ascending=False, inplace=True)
            lane_at_t = lane_at_t.reset_index()
            DHW, THW = [], []
            for k in range(len(lane_at_t['ID'])):
                if lane_at_t['leader'][k] > 0:
                    lead_df = lane_at_t[lane_at_t['ID'] == lane_at_t['leader'][k]]
                    ID_df = lane_at_t[lane_at_t['ID'] == lane_at_t['ID'][k]]
                    DHW.append(np.sqrt(
                        (list(lead_df['xloc-kf'])[0] - list(ID_df['xloc-kf'])[0])**2 +
                        (list(lead_df['yloc-kf'])[0] - list(ID_df['yloc-kf'])[0])**2))
                    THW.append(DHW[-1] / lane_at_t['speed-kf'][k])
                else:
                    DHW.append(np.nan)
                    THW.append(np.nan)
            lane_at_t['DHW'] = DHW
            lane_at_t['THW'] = THW
            df_out = pd.concat([df_out, lane_at_t])
    return df_out


def compute_DV(df):
    '''Compute speeddelta with leader.
    
     inputs
    - df: the tested dataframe where leaders are not flagged
    
    returns
    - df_out: dataframe with, at each frame where it makes sense, the speeddelta with leader
    '''
    df_out = pd.DataFrame(columns=df.columns)
    df_out['speeddelta'] = []

    for t in pd.unique(df['time']):
        at_t = df[df['time'] == t]
        for lane in pd.unique(at_t['lane-kf']):
            lane_at_t = at_t[at_t['lane-kf'] == lane]
            lane_at_t.sort_values(by='r', ascending=False, inplace=True)
            lane_at_t = lane_at_t.reset_index(drop = True)
            Delta_speed = []
            for k in range(len(lane_at_t['ID'])):
                if lane_at_t['leader'][k] > 0:
                    lead_df = lane_at_t[lane_at_t['ID'] == lane_at_t['leader'][k]]
                    ID_df = lane_at_t[lane_at_t['ID'] == lane_at_t['ID'][k]]
                    Delta_speed.append(list(lead_df['speed-kf'])[0] - list(ID_df['speed-kf'])[0])
                else:
                    Delta_speed.append(np.nan)
            lane_at_t['speeddelta'] = Delta_speed
            df_out = pd.concat([df_out, lane_at_t])
    return df_out