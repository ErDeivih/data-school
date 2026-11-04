"""frecuencia-y-agregacion-temporal-1.py — lo que se gana y lo que se pierde al agregar.
La figura de la página de frecuencia, granularidad y agregación (fase 5).

Izquierda: la misma serie a 5 minutos y agregada por hora y por día. El pico de media hora
sobrevive a la hora y desaparece del día.
Derecha: el cociente entre la señal y el ruido de un pico que dura 30 minutos, medido a cada
granularidad (eje logarítmico): la señal cae mucho más deprisa que el ruido."""

import numpy as np
import pandas as pd

from comun import *

estilo()
azar = np.random.default_rng(2)
minutos = pd.date_range("2026-01-05", periods=5 * 24 * 60, freq="5min")
t = np.arange(len(minutos))

# Ritmo diario, ritmo semanal y ruido; y un pico de media hora a partir del minuto 300.
senal = (50 + 6 * np.sin(2 * np.pi * t / (24 * 12)) + 2 * np.sin(2 * np.pi * t / (7 * 24 * 12))
         + azar.normal(0.0, 0.8, len(t)))
senal[300:306] += 12.0
s = pd.Series(senal, index=minutos)

por_hora = s.resample("1h").mean()
por_dia = s.resample("1D").mean()

fig, ejes = plt.subplots(1, 2, figsize=(7.4, 3.9))

# --- Panel izquierdo: 36 horas de serie a tres granularidades -----------------
ax = ejes[0]
ventana = slice(0, 36 * 12)
ax.plot(np.arange(36 * 12) / 12.0, s.iloc[ventana].values, color=REJILLA, linewidth=1.3,
        label="cada 5 minutos")
ax.plot(np.arange(36) + 0.5, por_hora.iloc[:36].values, color=AZUL, linewidth=1.6,
        marker="o", markersize=3, label="media por hora")
anotar(ax, "el pico dura media hora:\nla hora lo diluye, el día lo borra", (25.5, 60.5),
       (0.30, 0.20), color=ROJO)
ax.set_xlabel("horas desde el lunes")
ax.set_ylabel("medida")
ax.set_xlim(0, 36)
ax.legend(loc="upper right")
titulo(ax, "Agregar es promediar, no resumir", "cada salto de escala aplana la señal")
rejilla(ax)
numeros(ax)

# --- Panel derecho: el pico medido en desviaciones del ruido de cada nivel ----
niveles = [("5 minutos", 1), ("15 minutos", 3), ("1 hora", 12), ("1 día", 288)]
amplitudes = []
ruidos = []
for _, factor in niveles:
    a = s.resample(f"{5 * factor}min").mean()
    amplitudes.append(a.max() - np.median(a))
    # el ruido del nivel es lo que queda despues de quitar el ciclo diario
    ciclo = a.groupby(a.index.hour).transform("median") if factor < 288 else np.median(a)
    ruidos.append(float((a - ciclo).std()))

x = np.arange(len(niveles))
ax = ejes[1]
ax.bar(x - 0.19, amplitudes, 0.36, color=NARANJA, label="amplitud del pico")
ax.bar(x + 0.19, ruidos, 0.36, color=CIAN, label="ruido del nivel agregado")
for xi, valor in zip(x - 0.19, amplitudes):
    ax.text(xi, valor + 0.5, "%.1f" % valor, ha="center", fontsize=8.5, color=NARANJA)
ax.set_ylim(0, 21)
ax.set_xticks(x)
ax.set_xticklabels([n for n, _ in niveles])
ax.set_xlabel("granularidad de la agregación")
anotar(ax, "el pico se desploma,\nel ruido aguanta", (2.6, 8.0), (0.40, 0.72), color=NARANJA,
       flecha=False)
ax.legend(loc="upper right")
titulo(ax, "El pico se diluye, el ruido no", "la misma anomalía, cuatro granularidades")
rejilla(ax)
numeros(ax, ejes="y")

guardar(fig, "frecuencia-agregacion-pico-y-ruido")
