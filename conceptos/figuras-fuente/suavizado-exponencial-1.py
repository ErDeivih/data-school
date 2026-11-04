"""suavizado-exponencial-1.py — que significa de verdad el parámetro alfa.

Cuatro cosas que la formula no deja ver a la primera: cuanto pasado entra en cada pronostico, por
que un alfa muy bajo llega tarde, por qué un alfa alto copia el ruido, y que el alfa bueno esta en
medio y hay que estimarlo sobre datos que el modelo no ha visto. La figura de la pagina de
suavizado exponencial (fase 5)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

n = 80
t = np.arange(n)
# Ventas diarias: nivel 100, una rampa suave (el negocio ha cambiado) y ruido
ventas = 100 + 0.18 * t + azar.normal(0, 3.0, n)
K = 10                                       # el nivel se arranca con los diez primeros datos


def suavizar(y, alfa):
    """Recursión del SES: nivel_t = alfa*y_t + (1-alfa)*nivel_{t-1}."""
    nivel = float(y[:K].mean())
    pred = np.full(y.size, np.nan)
    for i in range(K, y.size):
        pred[i] = nivel                      # el pronostico de hoy se hizo ayer
        nivel = alfa * y[i] + (1 - alfa) * nivel
    return pred


def error_cuadratico(y, alfa, desde):
    """Suma de errores al cuadrado a un paso desde el índice `desde`."""
    pred = suavizar(y, alfa)
    return float(np.nansum((y[desde:] - pred[desde:]) ** 2))


def memoria(alfa):
    """Cuantos dias del pasado reunen el 90% del peso. La cola decae como (1-alfa)^k."""
    k, acumulada = 0, 0.0
    while acumulada < 0.9:
        acumulada += alfa * (1 - alfa) ** k
        k += 1
    return k


alfas = [0.15, 0.35, 0.60]
colores = [AZUL, ROJO, MORADO]

fig, ejes = plt.subplots(2, 2, figsize=(10.6, 6.8))
arriba, abajo = ejes[0], ejes[1]

# --- Panel 1: la misma serie pronosticada con tres alfas ----------------------
arriba[0].plot(t, ventas, color=REJILLA, linewidth=1.4, zorder=1)
for alfa, color in zip(alfas, colores):
    arriba[0].plot(t, suavizar(ventas, alfa), color=color, linewidth=1.9, zorder=3,
                   label="alfa = %s" % coma(alfa))
arriba[0].set_xlim(45, 81)
arriba[0].set_ylim(98, ventas.max() + 2)
arriba[0].set_title("Cuanto pesa el pasado: tres memorias a la vez")
arriba[0].set_xlabel("dia")
arriba[0].set_ylabel("ventas")
arriba[0].legend(loc="lower right")
rejilla(arriba[0])
numeros(arriba[0])
anotar(arriba[0], "con alfa = 0,15 el pronostico\nva por detras del nivel",
      xy=(72, suavizar(ventas, 0.15)[72]), xytext=(0.03, 0.72), color=AZUL)
anotar(arriba[0], "con alfa = 0,60 copia el ruido\ndel último dia",
      xy=(76, suavizar(ventas, 0.60)[76]), xytext=(0.44, 0.80), color=MORADO)

# --- Panel 2: los pesos que la formula esconde --------------------------------
k = np.arange(0, 18)
for alfa, color in zip(alfas, colores):
    pesos = alfa * (1 - alfa) ** k
    abajo[0].plot(k, pesos, color=color, linewidth=1.8, marker="o", markersize=3,
                  label="alfa = %s: el 90%% del peso son %d dias" % (coma(alfa), memoria(alfa)))
    abajo[0].vlines(memoria(alfa), 0, alfa * (1 - alfa) ** memoria(alfa),
                    color=color, linewidth=0.9, linestyle=":")
abajo[0].set_title("Cada dato pesa (1 menos alfa) veces el anterior")
abajo[0].set_xlabel("dias hacia atras")
abajo[0].set_ylabel("peso de ese dato")
abajo[0].legend(loc="upper right")
rejilla(abajo[0])
numeros(abajo[0])
anotar(abajo[0], "los pesos suman 1 en los tres casos:\nes una media, no una suma que crece",
      xy=(4, 0.15 * 0.85 ** 4), xytext=(0.26, 0.40), color=TEXTO)

# --- Panel 3: el error de cada alfa y el minimo -------------------------------
rejilla_alfa = np.arange(0.05, 1.0, 0.05)
errores = np.array([error_cuadratico(ventas, a, K) for a in rejilla_alfa])
mejor = rejilla_alfa[int(np.argmin(errores))]
arriba[1].plot(rejilla_alfa, errores, color=CIAN, linewidth=1.8)
for alfa, color in zip(alfas, colores):
    arriba[1].axvline(alfa, color=color, linewidth=1.0, linestyle=":")
arriba[1].axvline(mejor, color=ROJO, linewidth=1.2, linestyle="--")
arriba[1].set_ylim(580, 1160)
arriba[1].set_title("El alfa bueno lo dice el error, no la intuición")
arriba[1].set_xlabel("alfa")
arriba[1].set_ylabel("suma de errores al cuadrado")
rejilla(arriba[1])
numeros(arriba[1])
anotar(arriba[1], "el mínimo de la curva es el alfa elegido:\n%s, ni el más bajo ni el más alto" % coma(round(mejor, 2)),
      xy=(mejor, errores.min()), xytext=(0.28, 0.62), color=ROJO)

# --- Panel 4: el alfa optimo cambia al pasar a datos nuevos -------------------
corte = 45
e_pasado = np.array([error_cuadratico(ventas[:corte], a, K) for a in rejilla_alfa])
e_futuro = np.array([error_cuadratico(ventas, a, corte) for a in rejilla_alfa])
abajo[1].plot(rejilla_alfa, e_pasado / e_pasado.max(), color=NARANJA, linewidth=1.8,
              label="error dentro de la muestra (dias 1 a 45)")
abajo[1].plot(rejilla_alfa, e_futuro / e_futuro.max(), color=VERDE, linewidth=1.8,
              label="error fuera de muestra (dias 46 a 80)")
abajo[1].axvline(rejilla_alfa[int(np.argmin(e_pasado))], color=NARANJA, linewidth=1.1, linestyle="--")
abajo[1].axvline(rejilla_alfa[int(np.argmin(e_futuro))], color=VERDE, linewidth=1.1, linestyle="--")
abajo[1].set_title("El alfa que gana cambia al mirar datos nuevos")
abajo[1].set_xlabel("alfa")
abajo[1].set_ylabel("error, en tanto por uno del máximo")
abajo[1].legend(loc="upper center")
rejilla(abajo[1])
numeros(abajo[1])
anotar(abajo[1], "las dos rayas verticales no coinciden:\npor eso el alfa se valida hacia delante",
      xy=(rejilla_alfa[int(np.argmin(e_futuro))], 0.31), xytext=(0.36, 0.42), color=VERDE)

guardar(fig, "suavizado-exponencial-alfa-y-memoria")
