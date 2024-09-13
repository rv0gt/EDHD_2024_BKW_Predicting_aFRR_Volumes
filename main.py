from data_preparation import prepare_data
from model_training import day_by_day_training_prediction
from visualization import generate_heatmap, plot_correlation_matrix
from data_loader import load_all_data  # Import the new data loader
import pandas as pd
import config  # Import the configuration file

# Définir les années à charger
years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]

# Charger les données pour toutes les années spécifiées
all_data = load_all_data(years)

# Préparer les données
pretrained_data = prepare_data(all_data)

if False:
    # Exemple : Générer des heatmaps pour le volume positif de l'aFRR
    heatmap_fig = generate_heatmap(
        pretrained_data, 
        title="aFRR Positive Heatmap", 
        value_col='ActivatedBalancingVolume_CH_aFRRPositive', 
        color_scale='Reds'
    )
    heatmap_fig.show()

if False:
    # Boucle sur les targets et les features configurées
    for target in config.targets_features:
        for feature_name, feature_set in config.features.items():
            print(f"Running model for target: {target} with feature set: {feature_name}")
            
            # Exécution de la prédiction avec l'ensemble de features sélectionné
            forecast_df = day_by_day_training_prediction(
                pretrained_data.copy(), 
                target_col=target, 
                test_start=config.test_start, 
                test_end=config.test_end, 
                features_to_forecast=feature_set
            )

            # Sauvegarder les résultats des prédictions
            forecast_df.to_pickle(f'TEST_forecast_{feature_name}_{target[-8:]}.pkl')

if False:
    # Exemple : Générer la matrice de corrélation
    correlation_matrix = pretrained_data.corr()
    fig = plot_correlation_matrix(correlation_matrix, title="Correlation Matrix Heatmap")
    fig.show()


