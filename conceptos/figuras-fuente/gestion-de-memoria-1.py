"""gestion-de-memoria-1.py — cuanto cuesta repartir un objeto grande entre procesos y por qué
el número de copias manda más que el algoritmo. La figura de la pagina (fase 11)."""

import numpy as np

from comun import *

estilo()

GiB = 1024.0                      # el DataFrame del ejemplo: 2 GiB y 8 trabajadores
datos = 2.0
trabajadores = 8
total = datos * (trabajadores + 1)          # el padre conserva su copia: M x (N + 1)

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.2))

# --- Izquierda: donde va a parar la memoria cuando se reparte por pickle ------
etiquetas = ["1 sola copia:\nel proceso padre", "padre + 8 trabajadores:\n9 copias por pickle"]
valores = [datos, total]
colores = [VERDE, ROJO]
for i, (valor, color) in enumerate(zip(valores, colores)):
    ejes[0].bar(i, valor, width=0.5, color=color)
    ejes[0].text(i, valor + 0.35, f"{valor:.0f} GiB", ha="center", fontsize=10, color=TEXTO)

anotar(ejes[0], f"cada hijo recibe su propia copia: el dato se multiplica por {trabajadores + 1}",
       xy=(1, total), xytext=(0.02, 0.97), color=ROJO)

ejes[0].set_xticks(range(2))
ejes[0].set_xticklabels(etiquetas, fontsize=9)
ejes[0].set_ylim(0, 22)
ejes[0].set_ylabel("GiB de memoria del conjunto")
titulo(ejes[0], "Repartir un DataFrame no lo reparte",
       "pickle no comparte memoria: la envia copiada a cada proceso")
rejilla(ejes[0])
numeros(ejes[0], "y")

# --- Derecha: como crece con el numero de trabajadores ------------------------
n = np.arange(1, 17)
ejes[1].plot(n, datos * n, color=ROJO, linewidth=2.0, marker="o", markersize=3,
             label="copia por pickle: M x N")
ejes[1].axhline(datos, color=VERDE, linewidth=2.0)
ejes[1].text(4.2, datos + 0.9, "memoria compartida: M, no crece", color=VERDE, fontsize=8.5)
anotar(ejes[1], "cada trabajador de más son 2 GiB más de memoria",
       xy=(2, datos * 2), xytext=(0.04, 0.13), color=ROJO)

ejes[1].set_xlabel("procesos trabajadores")
ejes[1].set_ylabel("GiB de memoria")
ejes[1].set_xlim(1, 16)
ejes[1].set_ylim(0, 45)
titulo(ejes[1], "La memoria crece con el número de procesos",
       "el doble de trabajadores pide el doble de copias del mismo dato")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "gestion-de-memoria-copias-por-proceso")
