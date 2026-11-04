"""cuantizacion-y-destilacion-1.py (segunda figura) — qué información lleva la distribución
del profesor y por qué la temperatura la hace visible. Página de cuantización y destilación."""

import numpy as np

from comun import *

estilo()

# Logits del profesor para un ejemplo: la clase correcta, una confusión razonable y una absurda.
logits = np.array([5.0, 2.0, 0.5])
clases = ["correcta", "confusión", "absurda"]


def softmax(z):
    """Softmax estable: se resta el máximo antes de exponenciar."""
    e = np.exp(z - z.max())
    return e / e.sum()


fig, ejes = plt.subplots(1, 2, figsize=(8.4, 3.9))

# --- Izquierda: la temperatura reparte la masa entre las clases que no ganan ---
ax = ejes[0]
temperaturas = [1, 2, 4]
colores = [AZUL, NARANJA, MORADO]
alto = 0.24
for k, (tau, color) in enumerate(zip(temperaturas, colores)):
    p = softmax(logits / tau)
    desplazamiento = k * 1.15
    ax.barh(desplazamiento + np.arange(3) * alto, p, height=alto * 0.85, color=color,
            label=f"temperatura {tau}")
    for i, valor in enumerate(p):
        ax.text(valor + 0.015, desplazamiento + i * alto, f"{valor:.3f}".replace(".", ","),
                fontsize=8, color=color, va="center")
ax.set_yticks([0.24, 1.39, 2.54])
ax.set_yticklabels([f"τ = {t}" for t in temperaturas])
for etiqueta, color in zip(ax.get_yticklabels(), colores):
    etiqueta.set_color(color)
ax.set_xlim(0, 1.16)
ax.set_ylim(-0.25, 3.05)
ax.set_xlabel("probabilidad que el profesor da a cada clase")
anotar(ax, "con τ = 1 la clase absurda recibe 0,011:\nsu señal se pierde en el gradiente",
       (0.0105, 0.0), (0.30, 0.55), color=ROJO)
anotar(ax, "con τ = 4 recibe 0,181, diecisiete veces más",
       (0.1807, 2.48), (0.32, 0.24), color=MORADO, flecha=False)
titulo(ax, "La temperatura destapa las clases perdedoras",
       "el estudiante aprende de todas, no solo de la ganadora")
rejilla(ax, eje="x")
numeros(ax, ejes="x")

# --- Derecha: la etiqueta dura no dice nada de la clase absurda ---
ax = ejes[1]
otro_logit = np.linspace(-4, 8, 400)
profesor = np.stack([np.full_like(otro_logit, 5.0), otro_logit, np.full_like(otro_logit, 0.5)], axis=1)
p = np.exp(profesor - profesor.max(axis=1, keepdims=True))
p = p / p.sum(axis=1, keepdims=True)
perdida_dura = -np.log(p[:, 0])
perdida_suave = -(softmax(logits / 2) * np.log(p)).sum(axis=1)

ax.plot(otro_logit, perdida_dura, color=ROJO, linewidth=1.7, label="etiqueta dura: solo la correcta")
ax.plot(otro_logit, perdida_suave, color=MORADO, linewidth=1.7, label="profesor con τ = 2")
ax.axvline(2.0, color=REJILLA, linewidth=1.1, linestyle="--")
ax.set_xlim(-4, 8)
ax.set_ylim(0, 5.6)
ax.set_xlabel("logit que el profesor da a la clase «confusión»")
ax.set_ylabel("pérdida del estudiante")
ax.legend(loc="upper left", fontsize=8.5)
anotar(ax, "la etiqueta dura es plana: muevas lo que muevas\nel segundo logit, el estudiante no se entera",
       (6.0, 0.13), (0.98, 0.62), color=ROJO, flecha=False, align="right")
anotar(ax, "el profesor sí: aprende que un 8\nse parece a un 3 mucho más que a un 1",
       (2.0, 0.556), (0.97, 0.09), color=MORADO, flecha=False, align="right")
titulo(ax, "El profesor enseña la forma, no solo la respuesta",
       "lo que se pierde al destilar con etiquetas duras")
rejilla(ax)
numeros(ax)

guardar(fig, "destilacion-temperatura-y-sennal")
