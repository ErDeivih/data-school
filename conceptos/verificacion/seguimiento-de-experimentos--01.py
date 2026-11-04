import pandas as pd

# Cada fila es una ejecucion: la configuracion, la semilla y la metrica de validacion
runs = pd.DataFrame([
    {"config": "lr-1e-3", "semilla": 0, "val_acc": 0.842},
    {"config": "lr-1e-3", "semilla": 1, "val_acc": 0.851},
    {"config": "lr-1e-3", "semilla": 2, "val_acc": 0.838},
    {"config": "lr-1e-3", "semilla": 3, "val_acc": 0.849},
    {"config": "lr-1e-3", "semilla": 4, "val_acc": 0.845},
    {"config": "lr-3e-4", "semilla": 0, "val_acc": 0.851},
    {"config": "lr-3e-4", "semilla": 1, "val_acc": 0.856},
    {"config": "lr-3e-4", "semilla": 2, "val_acc": 0.849},
    {"config": "lr-3e-4", "semilla": 3, "val_acc": 0.858},
    {"config": "lr-3e-4", "semilla": 4, "val_acc": 0.852},
])

resumen = runs.groupby("config")["val_acc"].agg(["count", "mean", "std"])
for config, fila in resumen.iterrows():
    print(f"{config}: {int(fila['count'])} ejecuciones, media {fila['mean']:.4f}, "
          f"desviacion {fila['std']:.4f}")
# -> lr-1e-3: 5 ejecuciones, media 0.8450, desviacion 0.0052
# -> lr-3e-4: 5 ejecuciones, media 0.8532, desviacion 0.0037
print("mejor de cada configuracion:")
print(runs.loc[runs.groupby("config")["val_acc"].idxmax(), ["config", "semilla", "val_acc"]].to_string(index=False))
