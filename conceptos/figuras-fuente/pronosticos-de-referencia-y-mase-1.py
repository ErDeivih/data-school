"""pronosticos-de-referencia-y-mase-1.py — los tres pronosticos de referencia sobre una serie
mensual y su MASE: el liston que hay que batir esta en 1."""

import numpy as np

from comun import *

estilo()

# La misma serie del ejemplo de la pagina: 4 anos, ciclo anual fuerte y deriva suave.
azar = np.random.default_rng(3)
t = np.arange(48)
y = 100 + 0.5 * t + 20 * np.sin(2 * np.pi * t / 12) + azar.normal(0, 4, 48)

entrena, prueba = y[:36], y[36:]
h = np.arange(1, 13)
ingenuo = np.repeat(entrena[-1], 12)
estacional = entrena[-12:]
deriva = entrena[-1] + h * (entrena[-1] - entrena[0]) / (len(entrena) - 1)
escala = np.abs(entrena[12:] - entrena[:-12]).mean()
metodos = (("ingenuo", ingenuo, ROJO), ("estacional", estacional, VERDE),
           ("deriva", deriva, NARANJA))
mase = {n: np.abs(prueba - f).mean() / escala for n, f, _ in metodos}

meses = np.arange(48)
futuro = np.arange(36, 48)

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.3))

eje = ejes[0]
eje.plot(meses[:36], entrena, color=AZUL, linewidth=1.3)
eje.plot(meses[36:], prueba, color=TEXTO, linewidth=1.6)
eje.axvline(35.5, color=REJILLA, linewidth=1.1, linestyle="--")
for nombre, f, color in metodos:
    eje.plot(futuro, f, color=color, linewidth=1.3, marker="o", markersize=2.5)
eje.set_title("Solo el naive estacional copia el ciclo anual")
eje.set_xlabel("mes")
eje.set_ylabel("valor de la serie")
eje.set_ylim(80, 152)
eje.text(17, 147, "datos para ajustar", color=AZUL, fontsize=9, ha="center")
eje.text(42, 147, "año a juzgar", color=TEXTO, fontsize=9, ha="center")
anotar(eje, "el ingenuo se queda plano y la deriva\nse salta los meses: ninguna de las dos\nreproduce el ciclo anual",
       (24, 100), (0.03, 0.82), color=ROJO, flecha=False)
rejilla(eje)
numeros(eje)

eje = ejes[1]
nombres = ["ingenuo", "estacional", "deriva"]
valores = [mase[n] for n in nombres]
eje.barh(nombres, valores, color=[ROJO, VERDE, NARANJA], height=0.55)
eje.axvline(1, color=TEXTO, linewidth=1.2, linestyle="--")
eje.set_title("El listón está en 1: MASE del ingenuo")
eje.set_xlabel("MASE (errores por encima de 1 = peor que el ingenuo)")
eje.set_xlim(0, 2.1)
for i, v in enumerate(valores):
    eje.text(v + 0.04, i, ("%.3f" % v).replace(".", ","), va="center", fontsize=9.5)
anotar(eje, "solo este baja del listón", (valores[1], 1), (0.44, 0.63), color=VERDE,
       flecha=False, fondo=True)
rejilla(eje, eje="x")
numeros(eje, ejes="x")

guardar(fig, "pronosticos-de-referencia-y-mase")
print("escala %.3f  MASE %s" % (escala, {n: round(mase[n], 3) for n in nombres}))
