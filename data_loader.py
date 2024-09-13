import pandas as pd

def load_all_data(years):
    """
    Load a dataset containing aFRR activation and input features for multiple years.
    
    Parameters
    ----------
    years : list
        List of years to load the data for.
    
    Returns
    -------
    pd.DataFrame
        A DataFrame containing all the merged data for the given years.
    """
    # Initialiser un DataFrame vide pour stocker toutes les années
    all_data = pd.DataFrame()

    # Parcourir chaque année et charger les fichiers correspondants
    for year in years:
        if year == 2024:
            # Charger les fichiers afrr et input_features pour l'année 2024 (données de test)
            afrr_path = f'Data/Test/afrr_activation_test.csv'
            features_path = f'Data/Test/input_features_test.csv'
        else:
            # Charger les fichiers afrr et input_features pour les autres années
            afrr_path = f'Data/Training/afrr_activation_{year}.csv'
            features_path = f'Data/Training/input_features_{year}.csv'

        # Charger les données
        afrr = pd.read_csv(afrr_path)
        df = pd.read_csv(features_path)

        # Renommer les colonnes (si nécessaire)
        afrr.columns = ['date_utc', 'ActivatedBalancingVolume_CH_aFRRPositive',
                        'ActivatedBalancingVolume_CH_aFRRNegative']

        df.columns = ['date_utc', 'Generation_CH_HydroLake', 'Generation_CH_HydroPumpedStorage',
                      'Generation_CH_HydroRunOfRiver', 'Generation_CH_Solar', 'Generation_CH_Nuclear',
                      'InstalledCapacity_CH_HydroLake', 'InstalledCapacity_CH_HydroPumpedStorage',
                      'InstalledCapacity_CH_HydroRunOfRiver', 'InstalledCapacity_CH_Solar', 
                      'InstalledCapacity_CH_Nuclear', 'Generation_FR_Nuclear', 'Generation_FR_Solar',
                      'Generation_FR_WindOnshore', 'InstalledCapacity_FR_Nuclear', 
                      'InstalledCapacity_FR_Solar', 'InstalledCapacity_FR_WindOnshore', 
                      'Generation_DE_Lignite', 'Generation_DE_HardCoal', 'Generation_DE_Gas', 
                      'Generation_DE_Solar', 'Generation_DE_WindOnshore', 'InstalledCapacity_DE_Lignite', 
                      'InstalledCapacity_DE_HardCoal', 'InstalledCapacity_DE_Gas', 
                      'InstalledCapacity_DE_Solar', 'InstalledCapacity_DE_WindOnshore', 
                      'Generation_AT_Solar', 'Generation_AT_WindOnshore', 'Generation_AT_Gas', 
                      'Generation_AT_HydroLake', 'Generation_AT_HydroPumpedStorage', 
                      'Generation_AT_HydroRunOfRiver', 'InstalledCapacity_AT_Solar', 
                      'InstalledCapacity_AT_WindOnshore', 'InstalledCapacity_AT_Gas', 
                      'InstalledCapacity_AT_HydroLake', 'InstalledCapacity_AT_HydroPumpedStorage', 
                      'InstalledCapacity_AT_HydroRunOfRiver', 'Generation_IT_Solar', 
                      'Generation_IT_WindOnshore', 'Generation_IT_Gas', 'Generation_IT_HydroLake', 
                      'Generation_IT_HydroPumpedStorage', 'Generation_IT_HydroRunOfRiver', 
                      'InstalledCapacity_IT_Solar', 'InstallecCapacity_IT_WindOnshore', 
                      'InstallecCapacity_IT_Gas', 'InstalledCapacity_IT_HydroLake', 
                      'InstalledCapacity_IT_HydroPumpedStorage', 'InstalledCapacity_IT_HydroRunOfRiver', 
                      'Weather_CH_DailyMeanTemperature', 'Weather_DE_DailyMeanTemperature', 
                      'Weather_FR_DailyMeanTemperature', 'Weather_AT_DailyMeanTemperature', 
                      'Weather_IT_DailyMeanTemperature', 'Weather_CH_DailyPrecipitationEnergy', 
                      'Weather_FR_DailyPrecipitationEnergy', 'Weather_AT_DailyPrecipitationEnergy', 
                      'Prices_CH_Dayahead', 'Prices_DE_Dayahead', 'Prices_FR_Dayahead', 
                      'Prices_AT_Dayahead', 'Prices_IT_Dayahead', 'Consumption_CH_Total', 
                      'Consumption_DE_Total', 'Consumption_FR_Total', 'Consumption_AT_Total', 
                      'Consumption_IT_Total', 'CommercialBorderFlow_CH-DE', 'CommercialBorderFlow_CH-FR', 
                      'CommercialBorderFlow_CH-IT', 'CommercialBorderFlow_AT-CH', 
                      'NetTransferCapacity_CH-DE', 'NetTransferCapacity_DE-CH', 
                      'NetTransferCapacity_CH-FR', 'NetTransferCapacity_FR-CH', 
                      'NetTransferCapacity_CH-IT', 'NetTransferCapacity_IT-CH', 
                      'NetTransferCapacity_AT-CH', 'NetTransferCapacity_CH-AT', 
                      'Weather_CH_GlobalIrradianceClearSky', 'Holidays_CH', 'Holidays_DE', 
                      'Holidays_AT', 'Holidays_IT', 'Holidays_FR', 'Weekday', 'Week', 'DayOfYear', 
                      'Hour', 'QuarterHour']

        # Fusionner les deux DataFrames sur la colonne 'date_utc'
        calendar_df = afrr.merge(df, on='date_utc', how='inner')

        # Ajouter les données de cette année au DataFrame global
        all_data = pd.concat([all_data, calendar_df], ignore_index=True)

    return all_data