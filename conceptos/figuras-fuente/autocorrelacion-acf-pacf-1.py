"""autocorrelacion-acf-pacf-1.py — que mide la ACF, en que se nota que una serie no es
estacionaria y que anade la PACF. La figura de la pagina de autocorrelación."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)


def acf(x, nlags):
    """Autocorrelaciones muestrales con el estimador de denominador n."""
    d = x - x.mean()
    g0 = (d @ d) / d.size
    return np.array([1.0] + [(d[k:] @ d[:-k]) / d.size / g0 for k in range(1, nlags + 1)])


def pacf(r, nlags):
    """Durbin-Levinson: el último coeficiente de cada AR(k)."""
    phi = np.zeros((nlags + 1, nlags + 1))
    phi[1, 1] = r[1]
    for k in range(2, nlags + 1):
        num = r[k] - phi[k - 1, 1:k] @ r[k - 1:0:-1]
        den = 1 - phi[k - 1, 1:k] @ r[1:k]
        phi[k, k] = num / den
        phi[k, 1:k] = phi[k - 1, 1:k] - phi[k, k] * phi[k - 1, k - 1:0:-1]
    return np.array([phi[k, k] for k in range(1, nlags + 1)])


n = 500
ar = np.zeros(n)
for t in range(1, n):                       # AR(1): cada valor copia el 80 % del de ayer
    ar[t] = 0.8 * ar[t - 1] + azar.normal(0, 1)
ar = ar[100:]
paseo = np.cumsum(azar.normal(0, 1, n))

retardos = np.arange(0, 21)
r_ar = acf(ar, 20)
r_paseo = acf(paseo, 20)
p_ar = pacf(r_ar, 3)
banda = 1.96 / np.sqrt(ar.size)

# --- Figura 1: el decaimiento lento delata la raiz unitaria ------------------------
fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.3))

for eje, serie, titulo_panel, color, nota, donde_nota in (
    (ejes[0], ar, "Estacionaria: siempre vuelve a su media", AZUL,
     "la ACF de esta serie baja rapido:\nla memoria se agota en pocos retardos", 0.06),
    (ejes[1], paseo, "Con raiz unitaria: se va y no vuelve", ROJO,
     "su ACF sigue en 0,6 tras 20 retardos:\neso no es memoria, es una tendencia", 0.04),
):
    eje.plot(serie, color=color, linewidth=1.0)
    media = serie.mean()
    color_media = NARANJA if color == ROJO else ROJO
    eje.axhline(media, color=color_media, linewidth=1.1, linestyle="--")
    eje.set_title(titulo_panel)
    eje.set_xlabel("instante")
    menor, mayor = float(serie.min()), float(serie.max())
    margen = max(0.30 * (mayor - menor), 2.0)
    eje.set_ylim(menor - margen, mayor + margen)
    eje.text(0.30, 0.60, "media de todo el periodo", transform=eje.transAxes,
             color=color_media, fontsize=8.5, va="bottom")
    eje.text(0.03, donde_nota, nota, transform=eje.transAxes, color=color, fontsize=8.5,
             va="bottom")
    rejilla(eje)
    numeros(eje)
ejes[0].set_ylabel("valor de la serie")

guardar(fig, "acf-decaimiento-lento")

# --- Figura 2: la ACF y la PACF del mismo AR(1) -----------------------------------
fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.3), sharey=True)
k = np.arange(1, 9)

eje = ejes[0]
eje.bar(k, r_ar[1:9], color=AZUL, width=0.55)
eje.axhline(0, color=TEXTO, linewidth=0.9)
for signo in (1, -1):
    eje.axhline(signo * banda, color=ROJO, linewidth=1.0, linestyle="--")
eje.text(8.3, r_ar[2] + 0.05, "0,8² = 0,64 en teoría", color=AZUL, fontsize=10, ha="right")
eje.set_title("ACF: el parecido total baja poco a poco")
eje.set_xlabel("retardo k")
eje.set_ylabel("autocorrelación")
eje.set_ylim(-0.4, 1.0)
anotar(eje, "las lineas rojas son la banda ±1,96/√n:\ncon n = 400, cualquier barra por debajo de 0,10 es ruido",
       (6, banda), (0.34, 0.10), ROJO)
rejilla(eje)
numeros(eje)

eje = ejes[1]
eje.bar(k, np.concatenate([p_ar, np.zeros(5)]), color=MORADO, width=0.55)
eje.axhline(0, color=TEXTO, linewidth=0.9)
for signo in (1, -1):
    eje.axhline(signo * banda, color=ROJO, linewidth=1.0, linestyle="--")
eje.set_xticks(k)
eje.set_title("PACF: solo el retardo 1 tiene relación directa")
eje.set_xlabel("retardo k")
eje.set_ylim(-0.4, 1.0)
anotar(eje, "el 0,60 del retardo 2 era la cadena\n0,8 · 0,8, no una relación directa",
       (2, p_ar[1]), (0.36, 0.52), MORADO)
rejilla(eje)
numeros(eje)

guardar(fig, "acf-pacf-de-un-ar1")
