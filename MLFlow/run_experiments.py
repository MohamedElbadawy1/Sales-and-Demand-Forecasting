import mlflow
import subprocess


models = {
    "RandomForest": {
        "n_estimators": [100, 200, 300],
        "max_depth": [3, 5, 7],
        "min_samples_split": [2, 5, 10]
    },
    "GradientBoosting": {
        "n_estimators": [100, 200, 300],
        "max_depth": [3, 5, 7],
        "learning_rate": [0.01, 0.1, 0.2]
    },
    "XGBoost": {
        "n_estimators": [100, 200, 300],
        "max_depth": [3, 5, 7],
        "learning_rate": [0.01, 0.1, 0.2],
        "reg_alpha": [0, 0.1, 1],
        "reg_lambda": [0, 1, 2]
    }
}

def run_experiment(model_name, params):
    print(f"\nRunning experiment for {model_name} with params: {params}")
    command = ["mlflow", "run", ".", "-P", f"model_name={model_name}"]
    
    for param, value in params.items():
        command.extend(["-P", f"{param}={value}"])
    
    subprocess.run(command)

if __name__ == "__main__":
    
    for model_name, param_grid in models.items():
        
        if model_name == "RandomForest":
            for n_estimators in param_grid["n_estimators"]:
                for max_depth in param_grid["max_depth"]:
                    for min_samples_split in param_grid["min_samples_split"]:
                        params = {
                            "n_estimators": n_estimators,
                            "max_depth": max_depth,
                            "min_samples_split": min_samples_split
                        }
                        run_experiment(model_name, params)
                        
        elif model_name == "GradientBoosting":
            for n_estimators in param_grid["n_estimators"]:
                for max_depth in param_grid["max_depth"]:
                    for learning_rate in param_grid["learning_rate"]:
                        params = {
                            "n_estimators": n_estimators,
                            "max_depth": max_depth,
                            "learning_rate": learning_rate
                        }
                        run_experiment(model_name, params)
                        
        elif model_name == "XGBoost":
            for n_estimators in param_grid["n_estimators"]:
                for max_depth in param_grid["max_depth"]:
                    for learning_rate in param_grid["learning_rate"]:
                        for reg_alpha in param_grid["reg_alpha"]:
                            for reg_lambda in param_grid["reg_lambda"]:
                                params = {
                                    "n_estimators": n_estimators,
                                    "max_depth": max_depth,
                                    "learning_rate": learning_rate,
                                    "reg_alpha": reg_alpha,
                                    "reg_lambda": reg_lambda
                                }
                                run_experiment(model_name, params)