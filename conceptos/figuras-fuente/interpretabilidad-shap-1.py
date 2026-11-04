"""interpretabilidad-shap-1.py — el reparto de Shapley de una predicción, con la suma
comprobada abajo (izquierda) y la PDP frente a las curvas ICE (derecha): un promedio
plano puede esconder dos efectos opuestos (fase 6)."""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.2))

# --- Izquierda: el reparto, en cascada -----------------------------------------
# Modelo de tres variables. La prediccion de la fila vale 8 y la media 0, asi que las
# atribuciones (1,75 / 2,50 / 3,75, calculadas en la pagina) tienen que sumar 8.
valores = np.array([1.75, 2.50, 3.75])
nombres = ["var. a", "var. b", "var. c"]
acumulado = np.concatenate([[0.0], np.cumsum(valores)])
colores = [AZUL, VERDE, NARANJA]

for i, color in enumerate(colores):
    # Cada barra arranca donde acabo la anterior: es una cascada, no un diagrama de barras.
    ejes[0].barh(i, valores[i], left=acumulado[i], height=0.52, color=color)
    ejes[0].text(acumulado[i + 1] + 0.15, i, "+" + ("%g" % valores[i]).replace(".", ","),
                 va="center", fontsize=9, color=TEXTO)

# Cuarta barra: la suma de las tres, dibujada aparte para comprobar que cierra el hueco.
ejes[0].barh(3, valores.sum(), left=0, height=0.52, color=REJILLA, alpha=0.35)
ejes[0].text(valores.sum() + 0.15, 3, "suma = 8", va="center", fontsize=9, color=TEXTO)

ejes[0].plot([8.0, 8.0], [-0.55, 3.35], color=ROJO, linewidth=1.6, linestyle="--")
ejes[0].plot([0.0, 0.0], [-0.55, 3.35], color=TEXTO, linewidth=1.0, alpha=0.5)
ejes[0].set_yticks(range(4))
ejes[0].set_yticklabels(nombres + ["las tres"])
ejes[0].invert_yaxis()          # var. a arriba, como se lee una cascada
ejes[0].set_xlim(-1.2, 9.9)
ejes[0].set_ylim(3.75, -0.65)
ejes[0].set_xlabel("puntos de predicción atribuidos")
ejes[0].text(0.15, -0.50, "media, 0", color=TEXTO, fontsize=8.5, va="center")
ejes[0].text(7.9, -0.50, "predicción de la fila, 8", color=ROJO, fontsize=8.5,
             ha="right", va="center")
anotar(ejes[0], "La suma de las tres atribuciones es la\npredicción entera: es la propiedad de\neficiencia, no una coincidencia",
       xy=(4.0, 3.0), xytext=(0.20, 0.30))
titulo(ejes[0], "La predicción, repartida entre variables",
       "suma de las atribuciones = predicción − media")
rejilla(ejes[0], eje="x")
numeros(ejes[0], ejes="x")

# --- Derecha: la PDP frente a las ICE -----------------------------------------
rejilla_x = np.linspace(0, 1, 25)
azar = np.random.default_rng(7)
# Cada observacion tiene su propio efecto: la mitad sube con x y la otra mitad baja.
pendientes = azar.normal(0.0, 1.5, 60)
ice = 1.2 + pendientes[:, None] * (rejilla_x - 0.5) + 0.08 * np.cos(
    2 * np.pi * (rejilla_x - 0.5)) * azar.normal(1.0, 0.4, 60)[:, None]
pdp = ice.mean(axis=0)      # la PDP es literalmente la media de todas las ICE

for fila in ice:
    ejes[1].plot(rejilla_x, fila, color=MORADO, linewidth=0.6, alpha=0.16)
ejes[1].fill_between(rejilla_x, ice.min(axis=0), ice.max(axis=0), color=MORADO, alpha=0.09)
ejes[1].plot(rejilla_x, pdp, color=ROJO, linewidth=2.2, label="PDP (media de las ICE)")
ejes[1].axhline(1.2, color=TEXTO, linewidth=0.8, linestyle=":", alpha=0.5)
ejes[1].set_xlabel("valor impuesto a la variable")
ejes[1].set_ylabel("predicción del modelo")
ejes[1].set_ylim(-3.4, 5.6)
ejes[1].legend(loc="lower right", fontsize=8.5)
anotar(ejes[1], "La PDP sale casi plana, pero cada curva ICE se\nmueve: los efectos de signo contrario se cancelan",
       xy=(0.62, 1.05), xytext=(0.05, 0.80))
titulo(ejes[1], "Una media plana, mil pendientes debajo",
       "cada línea es una observación; la roja es su promedio")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "shap-reparto-y-pdp-ice")
