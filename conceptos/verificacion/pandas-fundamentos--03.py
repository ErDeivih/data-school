import pandas as pd

a = pd.Series([10, 20, 30], index=["a", "b", "c"])
b = pd.Series([1, 2, 3], index=["b", "c", "d"])

suma = a + b                    # se alinea por etiqueta, no por posicion
print(suma.index.tolist())      # -> ['a', 'b', 'c', 'd']
print(suma.tolist())            # -> [nan, 21.0, 32.0, nan]
print(int(suma.notna().sum()))  # -> 2

# Filtrar por una condicion y quedarse con dos columnas
print(a[a > 10].tolist())       # -> [20, 30]
