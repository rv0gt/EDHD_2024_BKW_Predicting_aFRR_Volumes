import xgboost as xgb
from sklearn.metrics import mean_squared_error
import pandas as pd
import plotly.graph_objects as go

def train_xgboost(train_df, target_col, features):
    """
    Train an XGBoost model to predict the target column.
    
    Parameters
    ----------
    train_df : pd.DataFrame
        The training data.
    target_col : str
        The target column for prediction.
    features : list
        The list of features for training.

    Returns
    -------
    model : XGBRegressor
        The trained model.
    """
    X_train = train_df[features]
    y_train = train_df[target_col]
    
    XGB_PARAMS = {
        "colsample_bytree": 1,
        "gamma": 0,
        "learning_rate": 0.01,
        "max_depth": 10,
        "min_child_weight": 1.5,
        "n_estimators": 350,
        "reg_alpha": 0,
        "reg_lambda": 1,
        "subsample": 0.5,
        "colsample_bylevel": 0.5,
        "objective": "reg:squarederror",
        "seed": 7,
        "tree_method": "hist",
    }
    
    model = xgb.XGBRegressor(**XGB_PARAMS)
    model.fit(X_train, y_train)
    
    return model

def day_by_day_training_prediction(calendar_df, target_col, test_start, test_end, features_to_forecast):
    """
    Train day-by-day and predict for the next day within a given test period.
    
    Parameters
    ----------
    calendar_df : pd.DataFrame
        DataFrame containing the features and target.
    target_col : str
        The column name of the target variable.
    test_start : str
        Start date for the test period.
    test_end : str
        End date for the test period.
    features_to_forecast : list
        List of features to be used for forecasting.

    Returns
    -------
    pd.DataFrame
        DataFrame containing date_locale, true_values, and forecast.
    """
    
    test_start = pd.to_datetime(test_start)
    test_end = pd.to_datetime(test_end)
    test_days = pd.date_range(start=test_start, end=test_end, freq='D')

    all_predictions = []
    all_actuals = []
    all_dates = []
    
    for test_day in test_days:
        train_end_day = test_day - pd.Timedelta(days=2)
        train_df = calendar_df[calendar_df.date_locale < train_end_day + pd.Timedelta(hours=23, minutes=45)]
        test_df = calendar_df[calendar_df.date_locale.dt.date == test_day.date()]
        
        if len(test_df) == 0:
            continue
        
        model = train_xgboost(train_df, target_col, features_to_forecast)
        
        X_test = test_df[features_to_forecast]
        y_test = test_df[target_col]
        
        y_pred = model.predict(X_test)
        
        all_predictions.extend(y_pred)
        all_actuals.extend(y_test)
        all_dates.extend(test_df.date_locale)
        
    forecast_df = pd.DataFrame({
        'date_locale': all_dates,
        'true_values': all_actuals,
        'forecast': all_predictions
    })
    
    return forecast_df