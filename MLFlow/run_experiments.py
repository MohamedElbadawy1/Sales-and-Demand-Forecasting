import itertools
import subprocess

param_grid = {
    "model_name": ["XGBoost", "RandomForest", "GradientBoosting"],
    "n_estimators": [100, 300],
    "max_depth": [3, 5],
    "learning_rate": [0.05],
    "gamma": [0],
    "reg_alpha": [1],
    "reg_lambda": [2],
    "subsample": [0.8],
    "colsample_bytree": [0.8]
}

keys, values = zip(*param_grid.items())
experiments = [dict(zip(keys, v)) for v in itertools.product(*values)]

data_path = "Original Data.csv"

for i, exp in enumerate(experiments):
    print(f"\n Running experiment {i+1}/{len(experiments)} with parameters: {exp}")

    cmd = [
        "mlflow", "run", ".",
        "-P", f"data_path={data_path}"
    ]
    for key, val in exp.items():
        cmd += ["-P", f"{key}={val}"]

    subprocess.run(cmd)
