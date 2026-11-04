"""naive-bayes-1.py — de dónde sale el posterior y qué arregla el suavizado de Laplace.
Página de Naive Bayes (fase 6)."""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

# --- Izquierda: la previa manda. Se deja fija la razon de verosimilitud en 20 y se mueve
# solo P(spam), que es lo unico que cambia entre un corpus y otro.
previas = np.linspace(0.01, 0.99, 300)
razon_verosimilitud = 20.0                  # P(gratis | spam) / P(gratis | no spam)
odds_previas = previas / (1 - previas)      # odds(p) = p / (1 - p)
posterior_exacto = (odds_previas * razon_verosimilitud) / (1 + odds_previas * razon_verosimilitud)

# La version "suma de indicios": cada palabra vista en spam se apunta como confirmacion.
# Es lo que hace de verdad un Naive Bayes y por eso sus probabilidades salen tan extremas.
indicios = 3.0
posterior_naive = previas ** indicios / (previas ** indicios + (1 - previas) ** indicios)

ejes[0].plot(previas, posterior_exacto, color=AZUL, linewidth=2.0,
             label="una palabra decisiva (razón de verosimilitud 20)")
ejes[0].plot(previas, posterior_naive, color=ROJO, linewidth=2.0, linestyle="--",
             label="tres indicios contados por separado")
ejes[0].axhline(0.5, color=REJILLA, linewidth=1.1, linestyle=":")
anotar(ejes[0], "por debajo del 5 % de previa\nel correo se clasifica como legítimo",
       xy=(0.05, 0.5), xytext=(0.04, 0.27), color=TEXTO)
anotar(ejes[0], "un 30 % de previa ya basta\npara decidir «spam»", flecha=False,
       xy=(0.30, 0.5), xytext=(0.48, 0.84), color=TEXTO)
titulo(ejes[0], "El posterior vive pegado a la previa",
       "misma evidencia, distinta frecuencia de spam en el corpus")
ejes[0].set_xlabel("previa P(spam) en el corpus")
ejes[0].set_ylabel("posterior P(spam | correo)")
ejes[0].set_xlim(0, 1)
ejes[0].set_ylim(0, 1.02)
ejes[0].legend(loc="lower right", fontsize=8)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: el suavizado de Laplace sobre el ejemplo de la pagina.
# "gratis" aparece en 3 de los 4 spam y en 0 de los 2 correos legitimos.
cuenta_spam, total_spam = 3.0, 4.0
cuenta_limpio, total_limpio = 0.0, 2.0
vocabulario = 2                              # el vocabulario son dos palabras
alphas = np.logspace(-3, 2, 200)

prob_spam = []
for a in alphas:
    # Suavizado de Laplace: (n_j + alpha) / (n + alpha * V). Con alpha = 0 el conteo cero
    # deja P(gratis | no spam) = 0 y el producto entero se anula: esa clase nunca gana.
    p_spam = (cuenta_spam + a) / (total_spam + a * vocabulario)
    p_limpio = (cuenta_limpio + a) / (total_limpio + a * vocabulario)
    # Puntajes en logaritmos y luego normalizados, que es como decide el clasificador.
    puntajes = np.array([0.5 * p_limpio, 2.0 * p_spam])
    prob_spam.append(puntajes[1] / puntajes.sum())

ejes[1].plot(alphas, prob_spam, color=VERDE, linewidth=2.0)
ejes[1].axvline(1.0, color=REJILLA, linewidth=1.0, linestyle=":")
anotar(ejes[1], "sin pseudo-cuentas el conteo cero\ndesploma la probabilidad",
       xy=(float(alphas[0]), float(prob_spam[0])), xytext=(0.13, 0.92), color=VERDE)
anotar(ejes[1], "el valor por defecto de scikit-learn",
       xy=(1.0, 0.72), xytext=(0.40, 0.60), color=TEXTO)
titulo(ejes[1], "El suavizado decide cuánto pesa el indicio",
       "correo con «gratis» dos veces: probabilidad de spam según alpha")
ejes[1].set_xlabel("alpha: pseudo-cuentas que se suman a cada palabra")
ejes[1].set_ylabel("P(spam | correo)")
ejes[1].set_xscale("log")
ejes[1].set_ylim(0.4, 1.02)
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="y")

guardar(fig, "naive-bayes-previa-y-suavizado")
