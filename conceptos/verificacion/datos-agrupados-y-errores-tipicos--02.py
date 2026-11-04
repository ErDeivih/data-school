import numpy as np
import pandas as pd

# La misma tabla en pandas, que es como llega casi siempre: una fila por intervalo.
tabla = pd.DataFrame({"marca": [10.0, 30.0, 50.0, 70.0, 90.0], "frecuencia": [8, 14, 42, 38, 18]})
n = int(tabla["frecuencia"].sum())
media = np.average(tabla["marca"], weights=tabla["frecuencia"])
var_entre = np.average((tabla["marca"] - media) ** 2, weights=tabla["frecuencia"]) * n / (n - 1)

print(f"media {media:.2f}  varianza {var_entre:.1f}  error tipico {np.sqrt(var_entre / n):.2f}")
# -> media 57.33  varianza 470.1  error tipico 1.98
print(f"el error tipico equivocado seria {np.sqrt(var_entre / len(tabla)):.2f} con {len(tabla)} filas")
# -> el error tipico equivocado seria 9.70 con 5 filas
print(f"filas {len(tabla)}  observaciones {n}")
# -> filas 5  observaciones 120
