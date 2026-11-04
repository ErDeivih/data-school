import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Los límites del eje y el número de marcas: el gráfico se puede leer de verdad.
fig, ax = plt.subplots()
ax.plot([0, 1, 2, 3], [10, 22, 19, 30], marker="o")

ax.set_ylim(0, 35)
ax.set_yticks([0, 10, 20, 30])

print("limites y:", ax.get_ylim())
print("marcas y :", ax.get_yticks().astype(int).tolist())
