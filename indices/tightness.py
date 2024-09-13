
import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt

#
path = 'Data/Training'
#if 1:
def load_and_merge(year, path: str='Data/Training'):    
    
    f1 = f'{path}/afrr_activation_{year}.csv'
    f2 = f'{path}/input_features_{year}.csv'

    df1 = pd.read_csv(f1, parse_dates=True)
    df2 = pd.read_csv(f2, parse_dates=True)
    # rename the 1st column to 'TimeStamp'
    df2 = df2.rename(columns={df2.columns[0]: 'TimeStamp'})
    if year == '2019':
        df1['TimeStamp'] = pd.to_datetime(df1['TimeStamp'], format='%Y-%m-%d %H:%M:%S')
        # time format is different, only for input_features: it is dd-mm-yyyy hh:mm:ss
        df2['TimeStamp'] = pd.to_datetime(df2['TimeStamp'], format='%d.%m.%Y %H:%M')
        
    df = df1.merge(df2, on='TimeStamp')
    df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])

    return df


# implement flow vs capacity ratio

def flow_capacity_ratio(df):
    flow_cols = ['CommercialBorderFlow_CH-DE', 'CommercialBorderFlow_CH-FR',
       'CommercialBorderFlow_CH-IT', 'CommercialBorderFlow_AT-CH']
    
    flow_cap_cols = ['NetTransferCapacity_CH-DE', 'NetTransferCapacity_DE-CH',
       'NetTransferCapacity_CH-FR', 'NetTransferCapacity_FR-CH',
       'NetTransferCapacity_CH-IT', 'NetTransferCapacity_IT-CH',
       'NetTransferCapacity_AT-CH', 'NetTransferCapacity_CH-AT']
    
    consum_cols = ['Consumption_CH_Total', 'Consumption_DE_Total', 'Consumption_FR_Total',
       'Consumption_AT_Total', 'Consumption_IT_Total']
    
    
    df['TotalFlow'] = df[flow_cols].sum(axis=1)
    df['TotalCapacity'] = df[flow_cap_cols].sum(axis=1)
    df['TotalConsumption'] = df[consum_cols].sum(axis=1)

    
    df2 = df[['TotalFlow', 'TimeStamp', 'TotalCapacity', 'TotalConsumption'] + flow_cols]

    # let's split the flow columns (signed) into import and export.
    # when flow CH-X is positive, it means CH exported to X
    # when flow CH-X is negative, it means CH imported from X
    # we can split the flow into import and export
    
    # create a new dataframe with the same columns as df2
    df3 = df2.copy()
    # create new columns for import and export
    for col in flow_cols:
        # first we need to identify the source and destination countries
        # the names of cols are in the format 'CommercialBorderFlow_CH-DE', so we should drop all text before _ and then split on -
        src, dest = col.split('_')[1].split('-')
        # create new columns for import and export
        df3[f'Flow-{src}-{dest}'] = df3[col].clip(upper=0) * -1.0
        df3[f'Flow-{dest}-{src}'] = df3[col].clip(lower=0)
        
    # drop the original flow columns
    df3.drop(flow_cols, axis=1, inplace=True)
    
    # cleanup column names to remove leading term "CommercialBorder"
    df3.columns = df3.columns.str.replace('CommercialBorder', '')
    # cleanup column names - substitute AT-CH with CH-AT
    #df3.columns = df3.columns.str.replace('AT-CH', 'CH-AT') 

    # set index to 'TimeStamp' of df and df3
    df.set_index('TimeStamp', inplace=True)
    df3.set_index('TimeStamp', inplace=True)

    # now we want to use flow_cap_cols to calculate the flow capacity utilization, let's call them 
    # tightness_index as a percentage. Each country pair should be matched. 
    # for example, NetTransferCapacity_CH-DE should be matched with CommercialBorderFlow_CH-DE
    # we can calculate the tightness_index as follows:
    # tightness_index = flow / flow_capacity
    # we can create new columns for each flow capacity pair
    country_pairs = ['CH-DE', 'DE-CH', 'CH-FR', 'FR-CH', 'CH-IT', 'IT-CH', 'CH-AT', 'AT-CH']

    for pair in country_pairs:
        cap_col = 'NetTransferCapacity_' + pair
        df3[cap_col]    = df[cap_col]
        

    for pair in country_pairs:
        flow_col = 'Flow-' + pair
        cap_col = 'NetTransferCapacity_' + pair
        #print(flow_col, cap_col, pair)
        #print(df3[flow_col])
        if not flow_col in df3.columns:
            print(f'Warning: Realised flow {flow_col} not in columns')
            continue
        if not cap_col in df3.columns:
            print(f'Warning: capacity NTC {cap_col} not in columns')
            continue
        
        #df3['TightnessIndex_' + pair] = df3[flow_col] / df[cap_col]
        idx = df3[flow_col] / df3[cap_col]
        df3['TightnessIndex_' + pair] = idx

    # add more columns: export_tightness_index, import_tightness_index. Each should be the average of all tightness indexes for the respective direction
    # for example, ExportTightnessIndex should be the average of all TightnessIndex_CH-X where X is the destination country
    df3['ExportTightnessIndex'] = df3.filter(like='TightnessIndex_CH').mean(axis=1)
    # filter with a regex that has TightnessIndex_XX-CH
    df3['ImportTightnessIndex'] = df3.filter(regex='TightnessIndex_[A-Z]{2}-CH').mean(axis=1)


    return df2, df3


if __name__ == '__main__':
    # load all data from 2018 to 2023
    D = []

    for y in range(2018, 2024):
        D.append(load_and_merge(str(y)))
        
    df = pd.concat(D)
    df.shape
    _df = df.copy()

    print(df.info())
    
    # calculate flow ratios
    df2, df3 = flow_capacity_ratio(df)

    
    # add in calendar features
    df3['Year'] = df3.index.year
    df3['Month'] = df3.index.month
    df3['Day'] = df3.index.day
    df3['Hour'] = df3.index.hour
    df3['Weekday'] = df3.index.weekday
    df3['doy'] = df3.index.dayofyear
    
    print(df3.info())
    
    df3.to_csv('ratios.csv')