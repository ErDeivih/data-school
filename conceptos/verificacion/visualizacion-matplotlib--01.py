import numpy as np
import matplotlib
matplotlib.use("Agg")          # sin ventana: solo calcular, no mostrar
import matplotlib.pyplot as plt

rng = np.random.default_rng(0)
fig, ax = plt.subplots()

# Histograma: hay que pasar los bordes IZQUIERDOS y la anchura, no los centros.
datos = rng.normal(100, 15, size=5000)
frec, bordes = np.histogram(datos, bins=30)
anchos = np.diff(bordes)
ax.bar(bordes[:-1], frec, width=anchos, align="edge")

print("intervalos:", len(frec))
print("borde mayor:", bordes[-1])
print("suma de frecuencias:", frec.sum())
