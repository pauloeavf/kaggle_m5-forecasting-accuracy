import argparse
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder
import os
import gc

parser = argparse.ArgumentParser(description='preprocess_pytorch.py')

# Locations
parser.add_argument('-data', required=True,
                    help='Path where the raw datasets are')
parser.add_argument('-save_dir', required=False, default='.',
                    help='Directory to save preprocessed data')

# Preprocessing options
parser.add_argument('-scaler', required=False, default='minmax',
                    help='Scaler method to preprocess the data [minmax|standardscaler]')

opt = parser.parse_args()

if opt.save_dir and not os.path.exists(opt.save_dir):
    os.makedirs(opt.save_dir)

if opt.scaler == 'minmax':
    scaler = MinMaxScaler()
else:
    scaler = StandardScaler()

oh_enc = OneHotEncoder(handle_unknown='ignore')

def main():
    print('Loading datasets...')
    df_train = pd.read_csv(os.path.join(opt.data, 'sales_train_validation.csv'))
    df_prices = pd.read_csv(os.path.join(opt.data, 'sell_prices.csv'))
    df_calendar = pd.read_csv(os.path.join(opt.data, 'calendar.csv'))

    print('Preprocessing calendar dataset...')
    df_calendar['date'] = pd.to_datetime(df_calendar['date'], format='%Y-%m-%d')
    df_calendar['weekend_flag'] = df_calendar['weekday'].isin(['Saturday', 'Sunday'])
    df_calendar['month'] = df_calendar['date'].dt.month_name()
    df_calendar.drop(['weekday', 'wday', 'year'], axis=1, inplace=True)

    print('Transforming sales dataset to long format...')
    # transform to long format
    df_final = pd.melt(df_train,
                       id_vars=df_train.columns[:6].to_list(),
                       value_vars=df_train.columns[6:].to_list(),
                       var_name='day',
                       value_name='value')
    # memory cleanup
    del df_train
    gc.collect()

    print('Merging datasets...')
    # merge calendar and prices
    df_final = df_final.\
        merge(df_calendar, how='left', left_on='day', right_on='d').\
        merge(df_prices, how='left', on=['store_id', 'item_id', 'wm_yr_wk'])
    del df_calendar, df_prices
    gc.collect()

    print('Preprocessing final dataset...')


    df_final.to_csv(opt.save_dir)

if __name__ == '__main__':
    main()