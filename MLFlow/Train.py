import argparse
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.datasets import load_diabetes

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
    mlflow.log_param("model_name", args.model_name)

    # Log all passed arguments as params
    for arg, value in vars(args).items():
        if arg != "model_name":
            mlflow.log_param(arg, value)

    data = load_diabetes()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = get_model(args.model_name, args)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("r2", r2)

    mlflow.sklearn.log_model(model, "model")

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
