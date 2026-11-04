import pandas as pd

retornos = pd.Series([0.01, 0.02, -0.01, 0.03, 0.0, 0.02, 0.01, -0.02, 0.01, 0.01],
                     index=pd.date_range("2024-01-01", periods=10, freq="B"))
print(round(float(retornos.sum()), 6))                                      # -> 0.08
print(round(float((1 + retornos).resample("ME").prod().iloc[0] - 1), 6))    # -> 0.081893
print(round(float(retornos.resample("ME").mean().iloc[0]), 6))              # -> 0.008

# Semanas naturales: la etiqueta por defecto es el domingo que cierra la semana
semanas = pd.Series(range(1, 11), index=pd.date_range("2024-01-01", periods=10, freq="D"))
print(semanas.resample("W").sum().tolist())                       # -> [28, 27]
print([d.strftime("%a") for d in semanas.resample("W").sum().index])   # -> ['Sun', 'Sun']
print(semanas.resample("W", label="left", closed="left").sum().tolist())   # -> [21, 34]

# Alinear por el instante mas cercano: merge_asof, no merge
operaciones = pd.DataFrame({
    "hora": pd.to_datetime(["2024-01-01 09:00", "2024-01-01 12:00", "2024-01-03 10:00"]),
    "importe": [100, 50, 30]})
precios = pd.DataFrame({"hora": pd.to_datetime(["2024-01-01 08:59", "2024-01-01 11:30"]),
                        "precio": [1.5, 1.7]})
unido = pd.merge_asof(operaciones, precios, on="hora", direction="backward",
                      tolerance=pd.Timedelta("1D"))
print(unido["precio"].tolist())           # -> [1.5, 1.7, nan]
print(int(unido["precio"].isna().sum()))  # -> 1
