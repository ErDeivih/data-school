"""generacion-de-senales-1.py — de una idea a un número, con las tres cuentas que hay que
hacer antes de ilusionarse: el IC medido al horizonte al que vas a operar, la ley
fundamental corregida por la autocorrelación de la señal y el coste anual del giro.

Tres paneles: los dos primeros dicen si la señal predice; el tercero, si queda algo después
de pagar la operación. Página de generación de señales (fase 9)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(3)

# El mismo panel del ejemplo de la página: 300 días, 80 activos y una reversión de corto
# plazo del 4 %. La señal de hoy se mide contra el retorno de mañana, nunca al revés.
T, N = 300, 80
R = azar.normal(0, 0.02, (T, N))
R[1:] += -0.04 * R[:-1].copy()
senal = -R[:-1]
futuro = R[1:]


def rangos(a):
    """Rango de cada elemento dentro de su fila: una sección cruzada por fila."""
    return np.argsort(np.argsort(a, axis=1), axis=1).astype(float)


def ic_por_dia(a, c):
    # Las dos matrices describen las mismas fechas: se recorta lo que sobre por el final.
    filas = min(a.shape[0], c.shape[0])
    ra, rc = rangos(a[:filas]), rangos(c[:filas])
    ra -= ra.mean(axis=1, keepdims=True)
    rc -= rc.mean(axis=1, keepdims=True)
    return (ra * rc).sum(axis=1) / np.sqrt((ra ** 2).sum(axis=1) * (rc ** 2).sum(axis=1))


# ── Panel 1: el IC al horizonte al que se mide ────────────────────────────────
horizontes = np.array([1, 2, 3, 5, 8, 10, 15, 20])
# Suma acumulada de los retornos. La fila t del acumulado a h días es A[t+h] − A[t]:
# el retorno que va de t+1 a t+h, que es el que la señal de t intenta predecir.
suma = np.vstack([np.zeros((1, N)), np.cumsum(R, axis=0)])
ic_h = []
for h in horizontes:
    # A[i] acumula los retornos hasta i−1, así que el retorno de t+1 a t+h es A[t+h+1] − A[t+1].
    filas = (T - 1) - (h - 1)
    acumulado = suma[1 + h: 1 + h + filas] - suma[1: 1 + filas]
    ic_h.append(float(ic_por_dia(senal[: filas], acumulado).mean()))
ic_h = np.array(ic_h)

# ── Panel 2: la ley fundamental y su corrección por autocorrelación ───────────
ic_medio, activos, dias = 0.03, 80, 252
amplitud = activos * dias
ir_ingenuo = ic_medio * np.sqrt(amplitud)
rho = np.linspace(0.0, 0.97, 200)
ir_efectivo = ic_medio * np.sqrt(amplitud * (1 - rho) / (1 + rho))

# ── Panel 3: el coste anual del giro ──────────────────────────────────────────
giros = np.array([0.05, 0.10, 0.15, 0.20, 0.30])
coste_5pb = 100 * giros * dias * 0.0005
coste_2pb = 100 * giros * dias * 0.0002

fig, ejes = plt.subplots(2, 2, figsize=(10.8, 7.4))

# Arriba a la izquierda: la señal caduca, y eso fija cada cuánto puedes rebalancear.
eje = ejes[0, 0]
eje.plot(horizontes, ic_h, color=AZUL, linewidth=1.9, marker="o", markersize=4)
eje.axhline(0, color=TEXTO, linewidth=0.9, linestyle="--")
eje.set_ylim(0, max(ic_h) * 1.42)
anotar(eje, f"a un día: {ic_h[0]:+.4f}",
       xy=(1, float(ic_h[0])), xytext=(0.05, 0.86), color=AZUL)
anotar(eje, "un IC de 0,03 ya es aprovechable;\na 15 días no queda señal que cobrar",
       xy=(horizontes[-2], float(ic_h[-2])), xytext=(0.34, 0.22), color=MORADO)
anotar(eje, f"a {horizontes[-1]:.0f} días: {ic_h[-1]:+.4f}",
       xy=(horizontes[-1], float(ic_h[-1])), xytext=(0.97, 0.06), color=ROJO, align="right")
titulo(eje, "La misma señal, medida a plazos distintos",
       "Si el IC cae, hay que operar rápido; si sube, rebalanceabas de más")
eje.set_xlabel("días al horizonte al que se mide el IC")
eje.set_ylabel("IC medio de rango")
rejilla(eje)
numeros(eje, "x")

# Arriba a la derecha: la raíz de la amplitud promete, la autocorrelación devuelve a la
# realidad. Es la misma señal medida en un universo de 80 activos.
eje = ejes[0, 1]
eje.plot(rho, ir_efectivo, color=AZUL, linewidth=1.9, label="IR con la amplitud efectiva")
eje.axhline(ir_ingenuo, color=NARANJA, linewidth=1.6, linestyle="--",
            label=f"ley fundamental sin corregir: {ir_ingenuo:.2f}")
eje.set_xlim(0, 0.97)
eje.set_ylim(0, ir_ingenuo * 1.12)
eje.text(0.90, ir_ingenuo * 0.62, f"ρ = 0,90 → IR "
         f"{ic_medio * np.sqrt(amplitud * (1 - 0.9) / 1.9):.2f}",
         ha="center", fontsize=8.5, color=VERDE)
eje.text(0.95, ir_ingenuo * 0.40, f"ρ = 0,95 → {ic_medio * np.sqrt(amplitud * 0.05 / 1.95):.2f}",
         ha="right", fontsize=8.5, color=VERDE)
eje.legend(loc="center right", fontsize=8)
titulo(eje, "Un IR de 4,26 no existe: la señal se repite",
       "Amplitud efectiva = activos · días · (1 − ρ)/(1 + ρ)")
eje.set_xlabel("autocorrelación de la señal, ρ")
eje.set_ylabel("ratio de información")
rejilla(eje)
numeros(eje, "x")
anotar(eje, "la señal de este panel se renueva cada día:\nsu ρ es casi cero y la corrección, poca",
       xy=(0.05, float(ir_ingenuo * 0.97)), xytext=(0.30, 0.16), color=MORADO, flecha=False)

# Abajo: el giro se paga siempre, acierte o no la señal.
eje = ejes[1, 0]
pos = np.arange(giros.size)
ancho = 0.36
eje.bar(pos - ancho / 2, coste_5pb, width=ancho, color=ROJO, label="5 puntos básicos por unidad")
eje.bar(pos + ancho / 2, coste_2pb, width=ancho, color=VERDE, label="2 puntos básicos por unidad")
for xi, valor in zip(pos - ancho / 2, coste_5pb):
    eje.text(xi, valor + 0.09, f"{valor:.2f}".replace(".", ","), ha="center", fontsize=8,
             color=ROJO)
eje.set_xticks(pos)
eje.set_xticklabels([f"{g:.2f}".replace(".", ",") for g in giros])
eje.set_ylim(0, max(coste_5pb) * 1.22)
titulo(eje, "Lo que cuesta el giro antes de saber si acierta",
       "252 días de negociación al año, sobre el capital bruto")
eje.set_xlabel("giro diario, en fracción de la exposición bruta")
eje.set_ylabel("coste anual (% del capital)")
eje.legend(loc="upper left", fontsize=8)
rejilla(eje)
numeros(eje, "y")
anotar(eje, "ese 2 % de coste se resta del retorno bruto\nantes de comparar nada",
       xy=(float(giros[3]), float(coste_5pb[3])), xytext=(0.42, 0.72), color=MORADO)

# Abajo a la derecha: cómo se reparte el IC de esos 299 días. No es una curva suave: hay
# días buenos y días en los que la señal va en contra, y eso es lo que hay que aguantar.
eje = ejes[1, 1]
ic_diario = ic_por_dia(senal, futuro)
eje.hist(ic_diario, bins=26, color=CIAN, alpha=0.85)
eje.axvline(0, color=TEXTO, linewidth=1.0, linestyle="--")
eje.axvline(float(ic_diario.mean()), color=ROJO, linewidth=1.6,
            label=f"media: {ic_diario.mean():+.4f}")
eje.set_ylim(0, 42)
titulo(eje, "El IC de cada día, no solo su media",
       f"{ic_diario.size} días con IC positivo el {100 * (ic_diario > 0).mean():.0f} % de las veces")
eje.set_xlabel("IC de rango del día")
eje.set_ylabel("nº de días")
eje.legend(loc="upper left", fontsize=8)
rejilla(eje)
numeros(eje, "x")
anotar(eje, "hay días en los que la señal apunta\nal revés: la media sola no lo cuenta",
       xy=(float(ic_diario.min()), 2), xytext=(0.03, 0.62), color=ROJO)

guardar(fig, "generacion-de-senales-ic-horizonte-y-coste")
