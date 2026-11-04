"""prevision-a-varios-pasos-1.py — las dos formas de llegar al horizonte h.
La figura de la página de previsión a varios pasos (fase 5).

Izquierda: la recursiva mete la predicción de un paso dentro del modelo para dar el paso
siguiente, así que el error se va realimentando y el pronóstico se pega a la media.
Derecha: la directa ajusta un modelo por horizonte, no propaga error, pero cada horizonte
se estima con menos historia."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(4)

# Serie estacionaria con memoria: los mismos datos que el ejemplo de la página.
n = 260
y = np.empty(n)
y[0] = 10.0
for t in range(1, n):
    y[t] = 0.5 + 0.6 * y[t - 1] + azar.normal(0.0, 1.0)
entrena = y[:200]
ventana = entrena[-60:]
h = np.arange(1, 13)

# Coeficientes de un paso, por mínimos cuadrados sobre la ventana de entrenamiento.
idx = np.arange(len(ventana) - 1)
A = np.column_stack([np.ones(len(idx)), ventana[idx]])
c, phi = np.linalg.lstsq(A, ventana[idx + 1], rcond=None)[0]
media = c / (1.0 - phi)

# Recursiva: la predicción vuelve a entrar como retardo.
recursiva = []
hist = [ventana[-1]]
for _ in range(len(h)):
    v = c + phi * hist[-1]
    hist.append(v)
    recursiva.append(v)
recursiva = np.array(recursiva)

# Directa: un ajuste por horizonte, todos con la misma información.
directa = []
for k in h:
    i = np.arange(len(ventana) - k)
    Ak = np.column_stack([np.ones(len(i)), ventana[i]])
    ck = np.linalg.lstsq(Ak, ventana[i + k], rcond=None)[0]
    directa.append(ck[0] + ck[1] * ventana[-1])
directa = np.array(directa)

# La recursiva es exactamente la media más phi^h veces la desviación inicial.
teorica = media + phi ** h * (ventana[-1] - media)

fig, ejes = plt.subplots(1, 2, figsize=(7.4, 3.9))

# --- Panel izquierdo: la recursiva se realimenta ------------------------------
ax = ejes[0]
ax.axhline(media, color=REJILLA, linewidth=1.0, linestyle=":")
ax.plot(h, recursiva, "o-", color=AZUL, linewidth=1.6, markersize=4, label="recursiva")
ax.plot(h, teorica, "--", color=NARANJA, linewidth=1.4, label="media + phi^h · (y_T - media)")
ax.scatter([0], [ventana[-1]], color=TEXTO, s=22, zorder=4)
anotar(ax, "arrastra el error de cada paso", (h[3], recursiva[3]), (0.30, 0.30), color=AZUL)
anotar(ax, "el pronóstico converge a la media", (h[-1], media), (0.36, 0.56), color=REJILLA, flecha=False)
ax.set_xlabel("horizonte h (pasos)")
ax.set_ylabel("valor pronosticado")
ax.legend(loc="upper right")
titulo(ax, "Recursiva: el error vuelve a entrar", "la predicción de un paso alimenta el siguiente")
rejilla(ax)
numeros(ax)

# --- Panel derecho: la directa, un modelo por horizonte ----------------------
ax = ejes[1]
ax.plot(h, recursiva, "o-", color=AZUL, linewidth=1.4, markersize=3.4, label="recursiva")
ax.plot(h, directa, "s-", color=VERDE, linewidth=1.4, markersize=3.4, label="directa")
anotar(ax, "no arrastra error, pero\nestima doce modelos", (h[-1], directa[-1]), (0.30, 0.06),
       color=VERDE, flecha=False)
ax.set_xlabel("horizonte h (pasos)")
ax.set_ylabel("valor pronosticado")
ax.set_ylim(1.1, 2.1)
ax.legend(loc="upper right")
titulo(ax, "Directa: un modelo por horizonte", "más varianza, ningún error que propagar")
rejilla(ax)
numeros(ax)

guardar(fig, "prevision-varios-pasos-recursiva-frente-a-directa")
