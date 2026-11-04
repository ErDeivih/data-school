"""hmm-regimenes-1.py — el estado no se ve, se estima.

Una cadena de Markov oculta con dos regimenes: uno tranquilo y otro agitado. La probabilidad
suavizada de estar en el regimen agitado se dibuja con su banda de decisión, que es exactamente la
salida que miraria un gestor de riesgo. La figura de la pagina de cadenas de Markov ocultas (fase 5).

El titulo de dos lineas se comia el arranque de la serie y las dos notas del panel de arriba se
salían por el borde inferior. Ahora el titulo va corto con subtitulo, la leyenda se acorta para
no entrar en las franjas sombreadas y cada nota cae en la banda de arriba, que la serie no visita."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Dos regimenes con sus emisiones: el tranquilo (media 0, desv 1) y el agitado (media 2, desv 3)
medias = np.array([0.0, 2.0])
desvs = np.array([1.0, 3.0])
P = np.array([[0.95, 0.05], [0.10, 0.90]])   # matriz de transicion real

n = 180
s = np.zeros(n, int)
for t in range(1, n):
    s[t] = azar.choice(2, p=P[s[t - 1]])
y = azar.normal(medias[s], desvs[s])


def densidad(v, mu, sigma):
    return np.exp(-0.5 * ((v - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))


B = np.column_stack([densidad(y, medias[k], desvs[k]) for k in range(2)])

al = np.zeros((n, 2))                        # probabilidad filtrada: solo el pasado
al[0] = 0.5 * B[0]
al[0] /= al[0].sum()
for t in range(1, n):
    al[t] = (al[t - 1] @ P) * B[t]
    al[t] /= al[t].sum()

be = np.ones((n, 2))                         # probabilidad hacia atras: usa el futuro
for t in range(n - 2, -1, -1):
    be[t] = P @ (B[t + 1] * be[t + 1])
    be[t] /= be[t].sum()

g = al * be
g /= g.sum(1, keepdims=True)                 # gamma: probabilidad suavizada
acierto = (g.argmax(1) == s).mean()

fig, ejes = plt.subplots(2, 1, figsize=(9.8, 6.4), sharex=True,
                         gridspec_kw={"height_ratios": [1.15, 1.0]})

# --- Panel 1: los datos y el regimen que los genero ---------------------------
ejes[0].plot(y, color=REJILLA, linewidth=1.0, zorder=1)
# Etiquetas cortas: la leyenda va arriba a la izquierda y con el texto largo se metia dentro de
# las franjas sombreadas y del primer arranque del regimen agitado.
for k, color in enumerate((AZUL, ROJO)):
    ejes[0].plot(np.where(s == k, y, np.nan), color=color, linewidth=1.6, zorder=3,
                 label="regimen tranquilo: media 0 y desviación 1" if k == 0
                 else "regimen agitado: media 2 y desviación 3")
# La sombra marca los tramos en los que el estado oculto era el agitado
inicio = None
for t in range(n + 1):
    dentro = t < n and s[t] == 1
    if dentro and inicio is None:
        inicio = t
    elif not dentro and inicio is not None:
        ejes[0].axvspan(inicio, t, color=ROJO, alpha=0.10, zorder=0)
        inicio = None
titulo(ejes[0], "La serie que ves: un trazo, dos comportamientos",
       "el azul es el regimen tranquilo y el rojo el agitado; la sombra marca la verdad oculta")
ejes[0].set_ylabel("retorno observado")
ejes[0].set_ylim(-10.6, 9.6)
ejes[0].legend(loc="upper left", fontsize=8)
rejilla(ejes[0])
numeros(ejes[0])
# La banda de en medio esta llena de datos (todo se mueve entre -2 y 2) y la leyenda ocupa la
# esquina de arriba a la izquierda, asi que las dos notas van a las franjas que la serie no
# visita: la roja por encima de 7 entre los picos, y la negra por debajo de -4 a la derecha.
anotar(ejes[0], "el estado que genera cada dato\nno se observa: hay que estimarlo",
      xy=(30, y[30]), xytext=(0.97, 0.90), color=TEXTO, flecha=False, align="right")
anotar(ejes[0], "la sombra roja es la verdad,\nque el modelo no ve",
      xy=(100, -6.5), xytext=(0.95, 0.06), color=ROJO, flecha=False, align="right")

# --- Panel 2: la probabilidad suavizada del regimen agitado -------------------
ejes[1].plot(g[:, 1], color=MORADO, linewidth=2.0, zorder=4)
ejes[1].axhline(0.5, color=TEXTO, linewidth=1.0, linestyle="--")
ejes[1].set_ylim(-0.05, 1.12)
titulo(ejes[1], "La probabilidad suavizada de estar en el agitado")
ejes[1].set_xlabel("día")
ejes[1].set_ylabel("P(agitado)")
rejilla(ejes[1])
numeros(ejes[1])
# A la izquierda y apuntando al primer tramo: ahi la curva aun esta en el suelo, asi que ni el
# texto ni la flecha cruzan ninguna meseta.
anotar(ejes[1], "por encima de 0,5 el modelo dice agitado;\nla etiqueta acierta el %d%% de los dias"
      % round(100 * acierto),
      xy=(25, 0.5), xytext=(0.02, 0.80), color=TEXTO)

guardar(fig, "hmm-regimenes-probabilidad-suavizada")
