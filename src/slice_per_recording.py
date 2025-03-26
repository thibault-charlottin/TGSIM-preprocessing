import src.add_leader as lead
import src.add_traffic_indicators as indicators
import pandas as pd
import os


def clean_run(run, df_path, path_out):
    '''Clean data for a specific run.
    inputs
    - run: number of the recording to be extracted from the datasheet and in wich we compute the indicators
    - df_path: path of the dataframe containing all the TGSIM runs for a given experiment
    - path_out: path where we want to save the data
    
    returns
    None'''
    df = pd.read_csv(df_path)
    out = df[df['run-index'] == run]
    out = lead.detect_leader(out)
    out = indicators.compute_DHW(out)
    out = indicators.compute_DV(out)
    out.to_csv(os.path.join(path_out, f'{run}.csv'), index=False)

def clean_data(df_path, path_out):
    '''
    function to call the script and link it witht the tywo others modules (leader detection and indicators producer)'''
    df = pd.read_csv(df_path)
    for run in df['run-index']:
        clean_run(run, df_path, path_out)
    
