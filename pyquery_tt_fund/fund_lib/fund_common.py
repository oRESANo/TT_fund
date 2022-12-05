import os
import pandas as pd

fund_data_folder_path = 'E:\python_progams\web_crawler\\fund_data'

def cal_sharpe_ratio(df, add_cols, time_period):
    # rolling accumulative gain
    daily_gain = (df[['DWJZ', 'LJJZ']]-df[['DWJZ', 'LJJZ']].shift(1))/df[['DWJZ', 'LJJZ']].shift(1)
    daily_gain_mean = daily_gain.rolling(time_period).mean()
    daily_std = daily_gain.rolling(time_period).std()
    df[add_cols] = daily_gain_mean/daily_std
    return df

if __name__ == '__main__':
    pass