import argparse
import mlflow
import os

def run_experiment(args):
    if not os.path.exists("Original Data.csv"):
        raise FileNotFoundError("Original Data.csv not found in current directory")
    
    mlflow.set_experiment("Sales_Forecasting")
    

    run = mlflow.run(
        ".",
        entry_point="main",
        parameters={
            "model_name": args.model_name,
            "n_estimators": args.n_estimators,
            "max_depth": args.max_depth,
            "learning_rate": args.learning_rate,
            "gamma": args.gamma,
            "reg_alpha": args.reg_alpha,
            "reg_lambda": args.reg_lambda,
            "subsample": args.subsample,
            "colsample_bytree": args.colsample_bytree
        },
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run sales forecasting experiments')
    

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
    
    run_experiment(args)