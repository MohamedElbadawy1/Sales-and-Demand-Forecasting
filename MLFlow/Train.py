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

def load_preprocessed_data():
    sales = pd.read_csv("processed_data_for_ML.csv")
    
    mlflow.log_param("data_file", "processed_data_for_ML.csv")
    mlflow.log_param("data_shape", sales.shape)
    mlflow.log_param("data_columns", list(sales.columns))
    
    X = sales.drop('Total_sales', axis=1)
    y = sales['Total_sales']
    
    return train_test_split(X, y, test_size=0.2, random_state=30)

def get_model(name, args):
    if name == "RandomForest":
        return RandomForestRegressor(
            random_state=30
        )
    elif name == "GradientBoosting":
        return GradientBoostingRegressor(
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
        raise ValueError("Invalid model name. Available options: XGBoost, RandomForest, GradientBoosting")

def run_model(model_name, args):
    with mlflow.start_run(run_name=model_name):
        mlflow.set_tag("model_type", model_name)
        mlflow.log_params(vars(args))
        
        X_train, X_test, y_train, y_test = load_preprocessed_data()
        
        mlflow.log_metric("train_size", X_train.shape[0])
        mlflow.log_metric("test_size", X_test.shape[0])
        
        model = get_model(model_name, args)
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

        from mlflow.models.signature import infer_signature
        signature = infer_signature(X_train, model.predict(X_train))
        
        mlflow.sklearn.log_model(
            model, 
            "model",
            signature=signature,
            input_example=X_train.iloc[:5]
        )
        
        print(f"\n{'='*50}")
        print(f"Model: {model_name}")
        print(f"RMSE: {rmse:.4f}")
        print(f"MAE: {mae:.4f}")
        print(f"R²: {r2:.4f}")
        print("="*50)

def main():
    parser = argparse.ArgumentParser(description="Train machine learning models.")
    parser.add_argument('--model_name', type=str, required=True,
                       choices=['XGBoost', 'RandomForest', 'GradientBoosting'],
                       help="Model to train: XGBoost, RandomForest, or GradientBoosting")
    
    parser.add_argument('--n_estimators', type=int, default=300,
                       help="Number of estimators (trees)")
    parser.add_argument('--max_depth', type=int, default=5,
                       help="Maximum depth of trees")
    parser.add_argument('--learning_rate', type=float, default=0.05,
                       help="Learning rate for boosting models")
    parser.add_argument('--gamma', type=float, default=0,
                       help="Gamma for XGBoost")
    parser.add_argument('--reg_alpha', type=float, default=1,
                       help="L1 regularization term (XGBoost)")
    parser.add_argument('--reg_lambda', type=float, default=2,
                       help="L2 regularization term (XGBoost)")
    parser.add_argument('--subsample', type=float, default=0.8,
                       help="Subsample ratio of training instances")
    parser.add_argument('--colsample_bytree', type=float, default=0.8,
                       help="Subsample ratio of columns when constructing each tree")
    
    args = parser.parse_args()
    
    print(f"\nStarting training for {args.model_name} model...")
    run_model(args.model_name, args)

if __name__ == "__main__":
    main()