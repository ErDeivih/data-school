"""metricas-de-riesgo-1.py — la misma estrategia medida a dos frecuencias da dos números
distintos: la vista mensual no ve el mínimo de dentro del mes. Figura de la pagina de
Metricas de riesgo (fase 9)."""

import numpy as np

from comun import *


def pct(x, decimales=1):
    """Porcentaje con coma decimal, como se escribe en el portal."""
    return f"{x * 100:.{decimales}f} %".replace(".", ",")


estilo()

azar = np.random.default_rng(7)
n = 630                                       # unas 21 sesiones por mes, 30 meses
diario = azar.normal(0.0008, 0.003, n)
# Un susto de cuatro sesiones que se recupera a medias antes del cierre de mes: el minimo
# cae ENTRE dos observaciones mensuales y la vista mensual no llega a verlo.
diario[318:330] = np.array([-0.045, -0.05, -0.03, -0.01, 0.012, 0.015,
                            0.018, 0.015, 0.012, 0.010, 0.008, 0.007])
capital = 100 * np.cumprod(1 + diario)

fin_de_mes = np.arange(20, n, 21)
mensual = capital[fin_de_mes]

picos_d = np.maximum.accumulate(capital)
caidas_d = (picos_d - capital) / picos_d
mdd_diario = float(caidas_d.max())
i_fondo = int(caidas_d.argmax())

picos_m = np.maximum.accumulate(mensual)
mdd_mensual = float(((picos_m - mensual) / picos_m).max())

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 5.8))

# --- arriba: la curva diaria y lo que alcanza a ver quien mira una vez al mes
ejes[0].plot(capital, color=AZUL, linewidth=1.0, alpha=0.9, zorder=2)
ejes[0].plot(fin_de_mes, mensual, color=MORADO, linewidth=1.6, marker="o", markersize=4,
             zorder=3)
ejes[0].plot(i_fondo, capital[i_fondo], marker="o", markersize=7, color=ROJO, zorder=4)
ejes[0].set_ylim(capital.min() - 7, capital.max() + 14)
anotar(ejes[0], f"el mínimo de verdad: la cuenta cayo un {pct(mdd_diario)}\ndesde su máximo, en cuatro sesiones",
       xy=(i_fondo, capital[i_fondo]), xytext=(0.97, 0.12), color=ROJO, align="right")
anotar(ejes[0], "la linea morada es la misma cuenta\nmirada solo el último dia de cada mes",
       xy=(fin_de_mes[6], mensual[6]), xytext=(0.02, 0.93), color=MORADO)
titulo(ejes[0], "La misma cuenta, dos formas de mirarla",
       "una caida que empieza y se recupera entre dos cierres de mes")
ejes[0].set_ylabel("capital (base 100)")
ejes[0].set_xlabel("sesiones")
rejilla(ejes[0])
numeros(ejes[0], "y")

# --- abajo: el numero que sale en cada caso
etiquetas = ["medida cada sesion\n(630 datos)", "medida una vez al mes\n(30 datos)"]
valores = [mdd_diario * 100, mdd_mensual * 100]
ejes[1].bar([0, 1], valores, width=0.45, color=[AZUL, MORADO], alpha=0.8, zorder=2)
for xi, v in zip([0, 1], valores):
    ejes[1].text(xi, v + 0.35, f"{v:.1f} %".replace(".", ","), ha="center", fontsize=10, color=TEXTO)
ejes[1].set_xlim(-0.7, 1.7)
ejes[1].set_ylim(0, max(valores) * 1.45)
ejes[1].set_xticks([0, 1])
ejes[1].set_xticklabels(etiquetas)
titulo(ejes[1], "La caida maxima del mismo periodo",
       "no es una propiedad de la estrategia: es una propiedad de como la mides")
ejes[1].set_ylabel("caida maxima (%)")
anotar(ejes[1], "por eso toda métrica se pública\ncon la frecuencia con la que se midio",
       xy=(0.80, valores[1]), xytext=(0.97, 0.93), color=TEXTO, align="right")
rejilla(ejes[1])
numeros(ejes[1], "y")

guardar(fig, "metricas-riesgo-frecuencia-de-medida")
