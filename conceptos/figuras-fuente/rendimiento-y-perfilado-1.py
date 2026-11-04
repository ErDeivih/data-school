"""rendimiento-y-perfilado-1.py — donde se va el tiempo de verdad (y no donde parece) y por
que medir la memoria antes de tocar nada. La figura de la pagina de perfilado (fase 11)."""

import numpy as np

from comun import *

estilo()

# Los tiempos del ejemplo de la pagina, en segundos: 22,8 s de proceso.
etapas = ["validación con iterrows()", "lectura del CSV", "escritura del resultado",
          "media por grupo"]
segundos = np.array([18.7, 3.1, 0.6, 0.4])
colores = [ROJO, NARANJA, AZUL, VERDE]          # en rojo, lo que se lleva el 82 por ciento
total = segundos.sum()

fig, ejes = plt.subplots(1, 2, figsize=(11.4, 4.3))

# --- Izquierda: el perfil del ejemplo, de mayor a menor -----------------------
filas = np.arange(len(etapas))
ejes[0].barh(filas, segundos, height=0.55, color=colores)
ejes[0].invert_yaxis()          # la etapa mas lenta, arriba
for i, s in enumerate(segundos):
    # El porcentaje se escribe a la derecha de la barra: dentro no cabe en las cortas.
    ejes[0].text(s + 0.35, i, f"{s:.1f} s   {100 * s / total:.0f} %", va="center",
                 fontsize=8, color=TEXTO)

anotar(ejes[0], "el bucle fila a fila se lleva el 82 % del tiempo",
       xy=(9.35, 0), xytext=(0.04, 0.76), color=ROJO)
anotar(ejes[0], "la estadística que parecia cara son 0,4 s",
       xy=(0.4, 3), xytext=(0.45, 0.02), color=VERDE)

ejes[0].set_yticks(filas)
ejes[0].set_yticklabels(etapas, fontsize=9)
ejes[0].set_xlim(0, 22)
ejes[0].set_xlabel("segundos de las 500.000 filas")
titulo(ejes[0], "El culpable no era el cálculo",
       "lo caro fue recorrer las filas una a una para validarlas")
rejilla(ejes[0], "x")
numeros(ejes[0], "x")

# --- Derecha: lo que ocupa lo mismo, segun como se guarde ---------------------
int_lista = 200_000 * 36 / 1024 / 1024          # 28 bytes de cada entero + 8 del puntero
int_array = 200_000 * 8 / 1024 / 1024           # int64: 8 bytes planos, sin cabecera
series = [("lista de enteros de Python", int_lista, ROJO),
          ("array de NumPy int64", int_array, VERDE)]

for i, (etiqueta, mib, color) in enumerate(series):
    ejes[1].barh(i, mib, height=0.42, color=color)
    ejes[1].text(mib + 0.15, i, f"{mib:.1f} MiB", va="center", fontsize=8, color=TEXTO)

anotar(ejes[1], "la lista ocupa 4,5 veces más: un entero de Python son 28 bytes",
       xy=(3.4, 0), xytext=(0.02, 0.86), color=ROJO)
anotar(ejes[1], "el array guarda 8 bytes por número, sin objetos de por medio",
       xy=(0.75, 1), xytext=(0.10, 0.78), color=VERDE)

ejes[1].set_yticks(range(len(series)))
ejes[1].set_yticklabels([s[0] for s in series], fontsize=9)
ejes[1].set_ylim(-0.6, 2.5)
ejes[1].set_xlim(0, 8.6)
ejes[1].set_xlabel("MiB para 200.000 enteros")
titulo(ejes[1], "Cambiar la representación gana 4,5x",
       "mismo dato, misma operación, la mitad del tiempo en copiarlo")
rejilla(ejes[1], "x")
numeros(ejes[1], "x")

guardar(fig, "rendimiento-perfil-y-memoria")
