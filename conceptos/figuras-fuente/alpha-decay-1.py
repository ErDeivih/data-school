"""alpha-decay-1.py — los dos decaimientos que se confunden todo el rato. Arriba, el que se
presupuesta: la capacidad predictiva cae con el horizonte y la autocorrelación de la señal
fija su vida media. Abajo, el que no se arregla con más datos: el IC de una señal que se
apaga a mitad de la muestra.

Página del decaimiento del alpha (fase 9)."""

import numpy as np

from comun import *

estilo()


def rangos(a):
    """Rango de cada elemento dentro de su fila (una sección cruzada por fila)."""
    return np.argsort(np.argsort(a, axis=1), axis=1).astype(float)


def ic_por_dia(a, c):
    filas = min(a.shape[0], c.shape[0])
    ra, rc = rangos(a[:filas]), rangos(c[:filas])
    ra -= ra.mean(axis=1, keepdims=True)
    rc -= rc.mean(axis=1, keepdims=True)
    return (ra * rc).sum(axis=1) / np.sqrt((ra ** 2).sum(axis=1) * (rc ** 2).sum(axis=1))


def senal_ar1(rho, T, N, semilla, ruido=0.37):
    """Señal AR(1) por activo: la rho que se mide en la página al estimarla."""
    azar = np.random.default_rng(semilla)
    s = np.zeros((T, N))
    s[0] = azar.normal(0, 1, N)
    for t in range(1, T):
        s[t] = rho * s[t - 1] + azar.normal(0, ruido, N)
    return s


# ── Arriba a la izquierda: cuánto aguanta la señal ────────────────────────────
s = senal_ar1(0.93, 2000, 100, 11)
retardos = np.arange(1, 31)
# Autocorrelación realizada de la señal a cada retardo: en un AR(1) decae como ρ^k.
autocorr = np.array([float(np.corrcoef(s[k:].ravel(), s[:-k].ravel())[0, 1])
                     for k in retardos])
vida_media = float(retardos[np.argmax(autocorr < 0.5)])

fig, ejes = plt.subplots(2, 2, figsize=(10.8, 7.4))

eje = ejes[0, 0]
eje.plot(retardos, autocorr, color=AZUL, linewidth=1.9, marker="o", markersize=3)
eje.axhline(0.5, color=NARANJA, linewidth=1.4, linestyle="--")
eje.axvline(vida_media, color=ROJO, linewidth=1.4, linestyle=":")
eje.set_ylim(0, 1.05)
eje.set_xlim(0, 31)
anotar(eje, f"vida media: {vida_media:.0f} periodos, hasta aquí\nla mitad de la información",
       xy=(vida_media, 0.5), xytext=(0.40, 0.72), color=ROJO)
titulo(eje, "Cuánto aguanta la información de la señal",
       "Autocorrelación realizada de una señal AR(1) con ρ = 0,93 y 100 activos")
eje.set_xlabel("retardo entre la señal de hoy y la de dentro de k periodos")
eje.set_ylabel("autocorrelación")
rejilla(eje)
numeros(eje, "x")

# ── Arriba a la derecha: de dónde sale esa vida media ─────────────────────────
rhos = np.array([0.5, 0.7, 0.8, 0.9, 0.95, 0.99])
vidas = -np.log(2) / np.log(rhos)
eje = ejes[0, 1]
eje.bar(np.arange(rhos.size), vidas, width=0.5, color=MORADO, alpha=0.9)
for i, v in enumerate(vidas):
    eje.text(i, v + 0.5, f"{v:.1f}".replace(".", ","), ha="center", fontsize=8.5, color=MORADO)
eje.set_xticks(np.arange(rhos.size))
eje.set_xticklabels([f"{r:.2f}".replace(".", ",") for r in rhos])
eje.set_ylim(0, max(vidas) * 1.20)
anotar(eje, "una señal que se renueva rápida\nobliga a girar la cartera cada poco",
       xy=(0, float(vidas[0])), xytext=(0.05, 0.72), color=MORADO)
titulo(eje, "Vida media = −ln(2) / ln(ρ)",
       "Cuánto tarda la señal en perder la mitad de su información")
eje.set_xlabel("autocorrelación de la señal, ρ")
eje.set_ylabel("vida media (periodos)")
rejilla(eje)
numeros(eje, "y")

# ── Abajo: el decaimiento secular, el que no se arregla con más datos ─────────
azar = np.random.default_rng(12)
T, N = 1200, 60
s2 = azar.normal(0, 1, (T, N))
# El alpha muere en t = 700: antes la señal explica el retorno, después ya no.
b = np.where(np.arange(T) < 700, 0.001, 0.0)[:, None]
r = b * s2 + azar.normal(0, 0.02, (T, N))
ic = ic_por_dia(s2, r)

eje = ejes[1, 0]
eje.plot(np.arange(ic.size), ic, color=CIAN, linewidth=0.7, alpha=0.65)
eje.plot(np.arange(24, ic.size), np.convolve(ic, np.ones(25) / 25, mode="valid"),
         color=AZUL, linewidth=2.2)
eje.axvline(700, color=ROJO, linewidth=1.5, linestyle="--")
eje.axhline(0, color=TEXTO, linewidth=0.9)
anotar(eje, f"antes: {ic[:700].mean():+.4f}", xy=(250, 0.055), xytext=(0.04, 0.90), color=VERDE)
anotar(eje, f"después: {ic[700:].mean():+.4f}", xy=(950, -0.045), xytext=(0.62, 0.10),
       color=ROJO)
anotar(eje, "el día 700 el alpha se apaga", xy=(700, 0.10), xytext=(0.44, 0.94), color=ROJO,
       flecha=False)
titulo(eje, "El decaimiento que no se arregla con más datos",
       "IC diario y su media móvil de 25 días sobre 1200 días")
eje.set_xlabel("periodo")
eje.set_ylabel("IC de rango del día")
rejilla(eje)
numeros(eje, "x")

# ── Abajo a la derecha: qué dice cada tramo y con qué se confunde ─────────────
eje = ejes[1, 1]
tramos = ["antes\ndel corte", "después\ndel corte", "últimos\n200 días"]
valores = np.array([ic[:700].mean(), ic[700:].mean(), ic[-200:].mean()])
colores = [VERDE, ROJO, ROJO]
eje.bar(np.arange(3), valores, width=0.5, color=colores, alpha=0.9)
eje.axhline(0, color=TEXTO, linewidth=1.0)
for i, v in enumerate(valores):
    eje.text(i, v + (0.004 if v > 0 else -0.006), f"{v:+.4f}".replace(".", ","),
             ha="center", va="bottom" if v > 0 else "top", fontsize=8.5, color=colores[i])
eje.set_xticks(np.arange(3))
eje.set_xticklabels(tramos)
eje.set_ylim(min(valores) * 1.9, max(valores) * 1.30)
titulo(eje, "Mirar por tramos, no la media del total",
       "La media de toda la muestra mezcla las dos épocas y no describe ninguna")
eje.set_ylabel("IC medio del tramo")
rejilla(eje)
numeros(eje, "y")
anotar(eje, "cero con ruido alrededor: no es un mes\nmalo, es un alpha apagado",
       xy=(1, float(valores[1])), xytext=(0.24, 0.60), color=ROJO)

guardar(fig, "alpha-decay-horizonte-y-corte-secular")
