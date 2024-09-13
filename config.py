# config.py

# Configuration for calendar-related features
calendar_features = [
    'hour',
    'minute',
    'weekday',
    'year',
    'month',
    'dayofmonth',
    'season'
]

# Configuration for best features
best_features = [
    'hour',
    'minute',
    'weekday',
    'year',
    'month',
    'dayofmonth',
    'season',
    'daily_sum_Prices_CH_Dayahead_0h_ago',
    'daily_sum_Prices_DE_Dayahead_0h_ago',
    'daily_sum_Prices_FR_Dayahead_0h_ago',
    'Prices_CH_Dayahead_0h_ago',
    'Prices_DE_Dayahead_0h_ago',
    'Prices_FR_Dayahead_0h_ago',
    'sum_until_10h_ActivatedBalancingVolume_CH_aFRRPositive_24h_ago',
    'sum_until_10h_ActivatedBalancingVolume_CH_aFRRNegative_24h_ago',
    'sum_until_10h_Consumption_CH_Total_24h_ago',
    'sum_until_10h_sum_generation_24h_ago',
    'sum_until_10h_sum_borderflow_24h_ago',
    'sum_until_10h_sum_nettransfer_24h_ago',
    'ActivatedBalancingVolume_CH_aFRRPositive_48h_ago',
    'ActivatedBalancingVolume_CH_aFRRNegative_48h_ago',
    'daily_sum_ActivatedBalancingVolume_CH_aFRRNegative_48h_ago',
    'daily_sum_ActivatedBalancingVolume_CH_aFRRPositive_48h_ago'
]

# Configuration for explicative features
explicative_features = [
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
    'Weather_CH_DailyPrecipitationEnergy', 
    'sum_generation',
    'sum_borderflow', 
    'sum_nettransfer_toCH', 
    'sum_nettransfer_fromCH',
    'ratio_net_toCH', 
    'ratio_net_fromCH', 
    'hour', 
    'minute',
    'weekday', 
    'year', 
    'month', 
    'dayofmonth', 
    'season'
]

# Defining the target columns
targets_features = [
    'ActivatedBalancingVolume_CH_aFRRPositive', 
    'ActivatedBalancingVolume_CH_aFRRNegative'
]

# Combine all configurations into a dictionary for easier access
features = {
    'best_features': best_features,
    'calendar_features': calendar_features,
    'explicative_features': explicative_features
}

# Configuration for test and training periods
test_start = '2024-01-01'
test_end = '2024-01-02'