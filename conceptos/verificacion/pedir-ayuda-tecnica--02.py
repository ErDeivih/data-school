import pandas as pd

# Un ejemplo minimo tambien lleva escrito lo que esperabas. Sin esa linea, quien
# ayuda no sabe si el fallo esta en el codigo o en tu expectativa.
minimo = pd.Series(["10,50", "20,00"])
esperado = pd.Series([10.5, 20.0])
obtenido = pd.to_numeric(minimo, errors="coerce")

print(f"esperaba {esperado.tolist()}")            # -> [10.5, 20.0]
print(f"obtuve   {obtenido.tolist()}")            # -> [nan, nan]
print(f"coincide {obtenido.equals(esperado)}")    # -> False
