import pandas as pd

def prepare_data(all_data):
    """
    Prepare and preprocess the data by engineering features, calculating sums, 
    and applying time shifts for selected columns.
    
    Parameters
    ----------
    all_data : pd.DataFrame
        The original DataFrame containing the raw data with datetime, generation, balancing, 
        prices, and other related columns.

    Returns
    -------
    pd.DataFrame
        A processed DataFrame ready for model training with new features, including sums and time-shifted columns.
    """
    
    # Selecting the relevant columns from all_data
    final_df = all_data[[
        'date_utc',
        'ActivatedBalancingVolume_CH_aFRRPositive',
        'ActivatedBalancingVolume_CH_aFRRNegative',
        'Generation_CH_HydroLake',
        'Generation_CH_HydroPumpedStorage',
        'Generation_CH_HydroRunOfRiver',
        'Generation_CH_Solar',
        'Generation_CH_Nuclear',
        'Prices_CH_Dayahead',
        'Prices_DE_Dayahead',
        'Prices_FR_Dayahead',
        'Consumption_CH_Total',
        'CommercialBorderFlow_CH-DE',
        'CommercialBorderFlow_CH-FR',
        'CommercialBorderFlow_CH-IT',
        'CommercialBorderFlow_AT-CH',
        'NetTransferCapacity_CH-DE',
        'NetTransferCapacity_DE-CH',
        'NetTransferCapacity_CH-FR',
        'NetTransferCapacity_FR-CH',
        'NetTransferCapacity_CH-IT',
        'NetTransferCapacity_IT-CH',
        'NetTransferCapacity_AT-CH',
        'NetTransferCapacity_CH-AT',
        'Weather_CH_GlobalIrradianceClearSky',
        'Weather_CH_DailyMeanTemperature',
        'Weather_CH_DailyPrecipitationEnergy'
    ]].copy()

    # Creating new aggregated columns
    final_df['sum_generation'] = final_df[[
        'Generation_CH_HydroLake',
        'Generation_CH_HydroPumpedStorage',
        'Generation_CH_HydroRunOfRiver',
        'Generation_CH_Solar',
        'Generation_CH_Nuclear',]].sum(1)

    final_df['sum_borderflow'] = final_df[[
        'CommercialBorderFlow_CH-DE',
        'CommercialBorderFlow_CH-FR',
        'CommercialBorderFlow_CH-IT',
        'CommercialBorderFlow_AT-CH',]].sum(1)

    final_df['sum_nettransfer'] = final_df[[
        'NetTransferCapacity_CH-DE',
        'NetTransferCapacity_DE-CH',
        'NetTransferCapacity_CH-FR',
        'NetTransferCapacity_FR-CH',
        'NetTransferCapacity_CH-IT',
        'NetTransferCapacity_IT-CH',
        'NetTransferCapacity_AT-CH',
        'NetTransferCapacity_CH-AT',]].sum(1)

    
    final_df['sum_nettransfer_toCH'] = final_df[[
    'NetTransferCapacity_DE-CH',
    'NetTransferCapacity_FR-CH',
    'NetTransferCapacity_IT-CH',
    'NetTransferCapacity_AT-CH']].sum(1)

    final_df['sum_nettransfer_fromCH'] = final_df[[
    'NetTransferCapacity_CH-DE',
    'NetTransferCapacity_CH-FR',
    'NetTransferCapacity_CH-IT',
    'NetTransferCapacity_CH-AT']].sum(1)

    final_df['ratio_net_toCH'] = final_df.sum_borderflow / final_df.sum_nettransfer_toCH
    final_df['ratio_net_fromCH'] = final_df.sum_borderflow / final_df.sum_nettransfer_fromCH
    
  #  train = final_df[['date_utc', 
  #            'ActivatedBalancingVolume_CH_aFRRPositive',
#              'ActivatedBalancingVolume_CH_aFRRNegative', 
#              'Prices_CH_Dayahead',
#              'Prices_DE_Dayahead', 
#              'Prices_FR_Dayahead', 
#              'Consumption_CH_Total', 
#              'sum_generation', 
#              'sum_borderflow', 
#              'sum_nettransfer']].copy()
    
    train = final_df.copy()

    # Step 1: Convert UTC to local timezone (Europe/Zurich) and remove tzinfo
    train['date_locale'] = pd.to_datetime(train['date_utc']).dt.tz_localize('UTC').dt.tz_convert('Europe/Zurich').dt.tz_localize(None)

    # Step 2: Add columns for hour, minute, weekday, year, month, day of the month
    train['hour'] = train['date_locale'].dt.hour
    train['minute'] = train['date_locale'].dt.minute
    train['weekday'] = train['date_locale'].dt.weekday  # 0=Monday, 6=Sunday
    train['day'] = train['date_locale'].dt.date
    train['year'] = train['date_locale'].dt.year
    train['month'] = train['date_locale'].dt.month
    train['dayofmonth'] = train['date_locale'].dt.day

    # Step 3: Create 'season' column based on the month
    def get_season(month):
        if month in [12, 1, 2]:
            return 0  # Winter
        elif month in [3, 4, 5]:
            return 1  # Spring
        elif month in [6, 7, 8]:
            return 2  # Summer
        elif month in [9, 10, 11]:
            return 3  # Autumn

    train['season'] = train['month'].apply(get_season)

    pretrained = train.copy()

    # List of columns to calculate daily sums
    columns_to_shift = [
        'ActivatedBalancingVolume_CH_aFRRPositive',
        'ActivatedBalancingVolume_CH_aFRRNegative',
        'Prices_CH_Dayahead',
        'Prices_DE_Dayahead',
        'Prices_FR_Dayahead',
        'Consumption_CH_Total',
        'sum_generation',
        'sum_borderflow',
        'sum_nettransfer'
    ]

    # Calculate daily sums
    for col in columns_to_shift:
        pretrained[f'daily_sum_{col}'] = pretrained.groupby('day')[col].transform('sum')

    pretrained = pretrained.copy()
    # Calculate sum until 10 AM
    for col in columns_to_shift:
        intermediate_df = pretrained[pretrained['hour'] <= 10].groupby('day')[col].sum().reset_index()
        intermediate_df.columns = ['day', f'sum_until_10h_{col}']

        pretrained = intermediate_df.merge(pretrained)
        
    # Set index to 'date_utc' to facilitate time shifting
    pretrained.set_index('date_utc', inplace=True)
    pretrained = pretrained.copy()

    # Apply time shifts
    time_shifts = [48, 72, 96, 120, 144, 168]  # in hours
    for shift in time_shifts:
        for col in columns_to_shift:
            pretrained[f'{col}_{shift}h_ago'] = pretrained[col].shift(periods=shift * 4)  # 4 periods per hour (each period = 15 minutes)

    # Additional time shift for daily sums and other variables
    more_columns_to_shift = [
        'daily_sum_Prices_CH_Dayahead', 
        'daily_sum_Prices_DE_Dayahead',
        'daily_sum_Prices_FR_Dayahead', 
        'Prices_CH_Dayahead',
        'Prices_DE_Dayahead',
        'Prices_FR_Dayahead',
        'daily_sum_ActivatedBalancingVolume_CH_aFRRPositive',
        'daily_sum_ActivatedBalancingVolume_CH_aFRRNegative',
    ]
    pretrained = pretrained.copy()

    more_time_shifts = [0, 24, 48, 72, 96, 120, 144, 168]  # in hours
    for shift in more_time_shifts:
        for col in more_columns_to_shift:
            pretrained[f'{col}_{shift}h_ago'] = pretrained[col].shift(periods=shift * 4)

    # Apply time shifts for variables until 10 AM
    columns_until_10h = [
        'sum_until_10h_ActivatedBalancingVolume_CH_aFRRPositive',
        'sum_until_10h_ActivatedBalancingVolume_CH_aFRRNegative',
        'sum_until_10h_Consumption_CH_Total',
        'sum_until_10h_sum_generation',
        'sum_until_10h_sum_borderflow', 
        'sum_until_10h_sum_nettransfer'
    ]
    for col in columns_until_10h:
        pretrained[f'{col}_24h_ago'] = pretrained[col].shift(periods=24 * 4)  # 24 hours = 4 periods/hour * 24
    pretrained.dropna(inplace=True)
    return pretrained