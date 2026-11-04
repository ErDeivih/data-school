import pandas as pd

t = pd.Series([10.0, 20.0, 30.0, 40.0],
              index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-05", "2024-01-06"]))

print(t.rolling("3D").sum().tolist())     # -> [10.0, 30.0, 30.0, 70.0]  ventana de tiempo
print(t.rolling(3).sum().tolist())        # -> [nan, nan, 60.0, 90.0]    ventana de filas
print(t.rolling("3D").count().tolist())   # -> [1.0, 2.0, 1.0, 2.0]
print(t.rolling("3D", min_periods=2).sum().tolist())   # -> [nan, 30.0, nan, 70.0]

print(t.shift(1).tolist())                # -> [nan, 10.0, 20.0, 30.0]  fila anterior
print(t.shift(freq="D").index.tolist()[:2])   # -> [2024-01-02, 2024-01-03]  mueve la etiqueta
print(t.diff().tolist())                  # -> [nan, 10.0, 10.0, 10.0]
