import pandas as pd

# El mismo dato agregado y desagregado: dos historias distintas.
datos = pd.DataFrame({
    "gravedad":    ["leve", "leve", "grave", "grave"],
    "tratamiento": ["A", "B", "A", "B"],
    "casos":       [10, 100, 40, 10],
    "exitos":      [9, 80, 20, 4],
})
datos["tasa"] = datos.exitos / datos.casos

global_ = datos.groupby("tratamiento")[["exitos", "casos"]].sum()
global_["tasa"] = global_.exitos / global_.casos

print(datos[["gravedad", "tratamiento", "tasa"]].to_string(index=False))
print()
print("agregado:")
print(global_.to_string())
