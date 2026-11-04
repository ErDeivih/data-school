import numpy as np
import pandas as pd

# La respuesta del modelo: "usa .std() para la desviacion tipica". Es correcta y ambigua:
# pandas y NumPy no dividen entre lo mismo, y la diferencia se ve en la tercera cifra.
serie = pd.Series([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])

print(f"pandas .std()       {serie.std():.5f}")             # -> 2.13809
print(f"numpy  .std()       {np.std(serie):.5f}")           # -> 2.00000
print(f"numpy  .std(ddof=1) {np.std(serie, ddof=1):.5f}")   # -> 2.13809
print(f"se llevan           {serie.std() / np.std(serie) - 1:.1%}")   # -> 6.9%
