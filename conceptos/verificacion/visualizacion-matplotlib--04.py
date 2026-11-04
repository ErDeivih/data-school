import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Por que el recorte del eje enganna: las longitudes dibujadas cambian de proporcion.
antes, ahora = 94.2, 91.4

# Caso honesto: el eje empieza en cero.
fig1, ax1 = plt.subplots()
ax1.bar(["antes", "ahora"], [antes, ahora])
honesto = ax1.get_ylim()[1]
proporcion_cero = antes / ahora

# Caso engannoso: el eje recortado exagera la diferencia.
fig2, ax2 = plt.subplots()
ax2.bar(["antes", "ahora"], [antes, ahora])
ax2.set_ylim(90, 95)
proporcion_recortada = (antes - 90) / (ahora - 90)

print(f"altura dibujada  honesto {proporcion_cero:.2f}  recortado {proporcion_recortada:.2f}")
print("eje por defecto llega a", honesto)
