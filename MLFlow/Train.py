import json
import os
import argparse
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder

def preprocess_data():
    sales = pd.read_csv('Original Data.csv', encoding='latin-1')
    
    mlflow.log_param("data_file", "Original Data.csv")
    mlflow.log_param("data_shape", sales.shape)
    mlflow.log_param("data_columns", list(sales.columns))
    
    sales.drop(columns=['Row ID', 'Order ID', 'Customer ID', 'Postal Code', 'Product ID'], inplace=True)

    encoder = LabelEncoder()
    categorical_columns = ['Order Priority', 'Ship Mode', 'Segment', 'Market', 
                         'Category', 'Region', 'Product Name', 'City', 'State', 
                         'Country', 'Customer Name', 'Sub-Category']
    
    for col in categorical_columns:
        if col in sales.columns:
            sales[col] = encoder.fit_transform(sales[col].astype(str))
    
    sales['Order Date'] = (pd.to_datetime(sales['Order Date']) - pd.Timestamp('1970-01-01')).dt.days
    sales['Ship Date'] = (pd.to_datetime(sales['Ship Date']) - pd.Timestamp('1970-01-01')).dt.days

    sales['Month'] = pd.to_datetime(sales['Order Date'], unit='D').dt.month
    sales['Year'] = pd.to_datetime(sales['Order Date'], unit='D').dt.year
    sales['Day_of_Week'] = pd.to_datetime(sales['Order Date'], unit='D').dt.dayofweek
    sales['Is_Weekend'] = sales['Day_of_Week'].isin([5, 6]).astype(int)
    sales['Day_of_Month'] = pd.to_datetime(sales['Order Date'], unit='D').dt.day


    sales['Total_sales'] = sales['Sales'] * sales['Quantity']

    sales.sort_values('Order Date', inplace=True)
    sales['Sales_Lag_1D'] = sales['Total_sales'].shift(1)
    sales['Sales_Lag_7D'] = sales['Total_sales'].shift(7)
    sales['Sales_Lag_30D'] = sales['Total_sales'].shift(30)
    sales['Sales_Lag_90D'] = sales['Total_sales'].shift(90)

    sales.dropna(inplace=True)

    X = sales.drop('Total_sales', axis=1)
    y = sales['Total_sales']

    return train_test_split(X, y, test_size=0.2, random_state=30)
    
def get_model(name, args):
    if name == "RandomForest":
        return RandomForestRegressor(
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            random_state=30
        )
    elif name == "GradientBoosting":
        return GradientBoostingRegressor(
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            random_state=30
        )
    elif name == "XGBoost":
        return XGBRegressor(
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            learning_rate=args.learning_rate,
            gamma=args.gamma,
            reg_alpha=args.reg_alpha,
            reg_lambda=args.reg_lambda,
            subsample=args.subsample,
            colsample_bytree=args.colsample_bytree,
            random_state=30,
            verbosity=0
        )
    else:
        raise ValueError("Invalid model name.")

def main(args):
    mlflow.start_run()
    
    mlflow.log_params(vars(args))
    
    X_train, X_test, y_train, y_test = preprocess_data()
    
    mlflow.log_metric("train_size", X_train.shape[0])
    mlflow.log_metric("test_size", X_test.shape[0])
    
    model = get_model(args.model_name, args)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    mlflow.log_metrics({
        "rmse": rmse,
        "mae": mae,
        "r2": r2
    })


    mlflow.sklearn.log_model(model, "model")
    

    sample_data = pd.concat([X_train.head(100), y_train.head(100)], axis=1)
    mlflow.log_table(sample_data, "data_sample.json")

    mlflow.log_artifact('Original Data.csv', "input_data")

    print(f"Model: {args.model_name}, RMSE: {rmse:.4f}, MAE: {mae:.4f}, R²: {r2:.4f}")
    mlflow.end_run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="XGBoost")
    parser.add_argument("--n_estimators", type=int, default=300)
    parser.add_argument("--max_depth", type=int, default=5)
    parser.add_argument("--learning_rate", type=float, default=0.05)
    parser.add_argument("--gamma", type=float, default=0)
    parser.add_argument("--reg_alpha", type=float, default=1)
    parser.add_argument("--reg_lambda", type=float, default=2)
    parser.add_argument("--subsample", type=float, default=0.8)
    parser.add_argument("--colsample_bytree", type=float, default=0.8)
    
    args = parser.parse_args()
    
    main(args)