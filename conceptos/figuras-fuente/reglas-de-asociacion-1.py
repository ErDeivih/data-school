"""reglas-de-asociacion-1.py — las tres medidas de una regla sobre la mesa y por qué el lift
es la única que distingue un hallazgo de una obviedad. Página de reglas de asociación (fase 6)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)


def miles(n):
    """2479 -> «2.479»: el portal separa los millares con punto, no con coma."""
    return f"{int(n):,}".replace(",", ".")


fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

# --- Izquierda: las tres reglas del ejemplo de la página.
nombres = ["pan →\nmantequilla", "café →\nazúcar", "pan →\nleche"]
soporte_b = np.array([0.10, 0.50, 0.30])        # cuánto aparece B por su cuenta: la referencia
confianza = np.array([0.40, 0.667, 0.15])       # de las cestas con A, cuántas llevan B
lift = confianza / soporte_b                    # veces más probable que por azar
print("lift:", np.round(lift, 3).tolist())

posiciones = np.arange(len(nombres))
ancho = 0.36
ejes[0].bar(posiciones - ancho / 2, soporte_b, width=ancho, color=NARANJA,
            label="soporte de B: lo normal sin saber nada de A")
ejes[0].bar(posiciones + ancho / 2, confianza, width=ancho, color=AZUL,
            label="confianza: lo que pasa cuando ya hay A")
for k in range(len(nombres)):
    ejes[0].text(posiciones[k], max(soporte_b[k], confianza[k]) + 0.035,
                 "lift " + f"{lift[k]:.2f}".replace(".", ","), ha="center", color=ROJO,
                 fontsize=9)
anotar(ejes[0], "en pan → leche la confianza\nqueda por debajo del azar",
       xy=(2.2, 0.15), xytext=(0.62, 0.62), color=ROJO, flecha=False)
titulo(ejes[0], "Confianza alta no es buena regla",
       "la barra naranja es el azar; la azul, la regla; el lift es su cociente")
ejes[0].set_xticks(posiciones, nombres)
ejes[0].set_ylabel("proporción de cestas")
ejes[0].set_ylim(0, 0.86)
ejes[0].legend(loc="upper left", fontsize=8.5)
rejilla(ejes[0])
numeros(ejes[0], ejes="y")

# --- Derecha: lo que cuesta bajar el soporte mínimo en Apriori.
# 300 artículos con popularidad muy desigual y 20 000 cestas de 8 artículos.
n_articulos, n_cestas, tam = 300, 20000, 8
pesos = 1.0 / np.arange(1, n_articulos + 1) ** 0.8
pesos = pesos / pesos.sum()
# Truco de Gumbel: sumar ruido extremo al logaritmo de los pesos y quedarse con los mayores
# equivale a muestrear sin reemplazo respetando esas probabilidades, pero de golpe y sin bucles.
claves = np.log(pesos) + azar.gumbel(size=(n_cestas, n_articulos))
elegidos = np.argpartition(-claves, tam, axis=1)[:, :tam]
cuenta = np.zeros((n_articulos, n_articulos))
i, j = np.triu_indices(tam, 1)
np.add.at(cuenta, (elegidos[:, i].ravel(), elegidos[:, j].ravel()), 1.0)
cuenta = cuenta + cuenta.T                      # cada par se contó una sola vez: se simetriza
soportes = cuenta[np.triu_indices(n_articulos, 1)] / n_cestas
posibles = n_articulos * (n_articulos - 1) // 2
umbrales = np.geomspace(0.0006, 0.03, 90)
frecuentes = np.array([(soportes >= u).sum() for u in umbrales])
n10, n2 = int((soportes >= 0.010).sum()), int((soportes >= 0.002).sum())
print("pares frecuentes en 0,010:", n10, "en 0,002:", n2, "pares posibles:", posibles)

ejes[1].plot(umbrales, frecuentes, color=AZUL, linewidth=2.0)
ejes[1].fill_between(umbrales, 1, frecuentes, color=AZUL, alpha=0.10)
for u in (0.002, 0.010, 0.030):
    n = max(int((soportes >= u).sum()), 1)
    ejes[1].plot([u], [n], "o", color=ROJO, markersize=5, zorder=4)
    ejes[1].text(u * 1.08, n * 1.30, miles(n), color=ROJO, fontsize=8.5)
ejes[1].axhline(posibles, color=REJILLA, linewidth=1.2, linestyle="--")
anotar(ejes[1], "todos los pares posibles: " + miles(posibles),
       xy=(umbrales[0], posibles), xytext=(0.97, 0.90), color=REJILLA, flecha=False,
       align="right")
anotar(ejes[1], f"de 0,010 a 0,002: de {miles(n10)} a {miles(n2)} pares",
       xy=(0.002, n2), xytext=(0.28, 0.72), color=ROJO)
titulo(ejes[1], "Bajar el soporte multiplica los pares",
       "300 artículos y 20 000 cestas simuladas; en un súper real hay 20 000 referencias")
ejes[1].set_xlabel("soporte mínimo exigido")
ejes[1].set_ylabel("pares que lo superan")
ejes[1].set_yscale("log")                       # de 1 a 1 000: sin escala log no se ve la cola
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="x")

guardar(fig, "reglas-soporte-confianza-lift")
