import numpy as np
import pandas as pd

ancho = pd.DataFrame({"ene": [1, 4], "feb": [2, 5], "mar": [3, 6]}, index=["A", "B"])
larga = ancho.stack()                          # de columnas a filas: Series con dos niveles

print(type(larga).__name__, larga.index.nlevels)     # -> Series 2
print(larga.loc["A"].to_dict())                      # -> {'ene': 1, 'feb': 2, 'mar': 3}
print(larga.unstack().equals(ancho))                 # -> True  la vuelta es exacta

# Al desapilar, los huecos del producto cartesiano se rellenan con NaN...
parcial = pd.Series([1.0, np.nan, 3.0],
                    index=pd.MultiIndex.from_tuples([("A", "ene"), ("A", "feb"), ("B", "ene")]))
print(parcial.unstack().to_numpy().tolist())              # -> [[1.0, nan], [3.0, nan]]
# ...pero fill_value solo rellena los que faltaban por combinacion, no los que ya eran nulos
print(parcial.unstack(fill_value=0).to_numpy().tolist())  # -> [[1.0, nan], [3.0, 0.0]]
