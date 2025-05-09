import mlflow
import itertools

def run_experiments():
    param_grid = {
        "model_name": ["XGBoost", "RandomForest", "GradientBoosting"],
        "n_estimators": [100, 300],
        "max_depth": [3, 5],
        "learning_rate": [0.05, 0.1],
        "gamma": [0, 1],
        "reg_alpha": [0, 1],
        "reg_lambda": [1, 2],
        "subsample": [0.8, 1.0],
        "colsample_bytree": [0.8, 1.0]
    }

    keys, values = zip(*param_grid.items())
    experiments = [dict(zip(keys, v)) for v in itertools.product(*values)]

    print(f"Starting MLflow experiments with {len(experiments)} runs...")

    for i, params in enumerate(experiments, 1):
        model_name = params.pop("model_name")  
        print(f"\nRun {i}/{len(experiments)} - Model: {model_name} - Params: {params}")

    
        mlflow_params = {**params, "model_name": model_name}

        run = mlflow.projects.run(
            uri=".",
            entry_point="main",
            parameters=mlflow_params,
            synchronous=True 
        )

        print(f"Run {i} finished with run_id: {run.run_id}")

if __name__ == "__main__":
    run_experiments()

