import numpy as np

precios = np.array([100.0, 102.0, 101.0, 105.0, 103.0, 106.0, 108.0])
ret = np.diff(precios) / precios[:-1]

# Version tramposa: la senal de la barra t cobra el retorno de la barra t.
trampa = (ret > 0) * ret

# Version honesta: la posicion de hoy la decide el retorno de ayer (shift de una barra).
posicion = np.concatenate([[0.0], (ret[:-1] > 0).astype(float)])
honesto = posicion * ret

rotacion = np.abs(np.diff(posicion)).sum()
coste = rotacion * 0.001

print(f"retornos          {np.round(ret * 100, 2).tolist()}")
# -> [2.0, -0.98, 3.96, -1.9, 2.91, 1.89]
print(f"sin desplazar     {trampa.sum():+.2%}")     # -> +10.76%
print(f"desplazado        {honesto.sum():+.2%}")    # -> -1.00%
print(f"rotacion          {rotacion:.0f}  coste {coste:.2%}")  # -> rotacion 5  coste 0.50%
print(f"neto de costes    {honesto.sum() - coste:+.2%}")       # -> -1.50%
