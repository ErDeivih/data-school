"""regimenes-de-mercado-1.py — la estación y el tiempo no son lo mismo. Arriba, la cadena de
Markov (calma y tensión) con la volatilidad móvil de 20 días que la detecta y el umbral
calibrado a mano; abajo a la izquierda, cuándo avisa el filtro y con qué retardo; abajo a la
derecha, el golpe repartido por todo el episodio y no en los primeros días.

Página de regímenes de mercado (fase 9)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(5)

n = 3000
# La misma cadena del ejemplo: 30 % del tiempo en tensión, episodios de 10 días de media.
P = np.array([[0.95, 0.05],
              [0.10, 0.90]])
estado = np.zeros(n, dtype=int)
for t in range(1, n):
    if azar.random() < P[estado[t - 1], 1 - estado[t - 1]]:
        estado[t] = 1 - estado[t - 1]
    else:
        estado[t] = estado[t - 1]

media = np.where(estado == 0, 0.0005, -0.0008)
vol = np.where(estado == 0, 0.008, 0.020)
r = azar.normal(media, vol)

# Volatilidad móvil de 20 días: en t se usan solo los datos hasta t, nada del futuro.
v = np.zeros(n)
for t in range(19, n):
    v[t] = r[t - 19:t + 1].std(ddof=1)
umbral = 0.012
alerta = v > umbral

fig, ejes = plt.subplots(2, 2, figsize=(10.8, 7.2))

# ── Arriba: el estado oculto y lo único que tú ves ────────────────────────────
eje = ejes[0, 0]
tramo = slice(700, 1000)
dias = np.arange(700, 1000)
eje.plot(dias, v[tramo], color=AZUL, linewidth=1.3, label="volatilidad móvil de 20 días")
eje.axhline(umbral, color=NARANJA, linewidth=1.5, linestyle="--",
            label="umbral fijo: 0,012")
tension = estado[700:1000] == 1
eje.fill_between(dias, 0, 0.033, where=tension, color=ROJO, alpha=0.13)
# El borde izquierdo de cada banda es el día en que empieza el episodio real; el filtro
# cruza el umbral unos días después.
arranques = dias[tension & ~np.concatenate([[False], tension[:-1]])]
# En el eje solo se marcan el principio y el final: las líneas rojas ya señalan los inicios
# y cinco fechas seguidas en 45 días se solapan.
eje.set_xticks([700, 1000])
eje.set_xticklabels(["700", "1000"], fontsize=8)
eje.set_ylim(0, 0.033)
eje.set_xlim(700, 1000)
anotar(eje, "las bandas rojas son el episodio real:\nel filtro avisa con retraso y sigue "
            "avisando después",
       xy=(float(arranques[0]), 0.0300), xytext=(0.14, 0.80), color=ROJO)
titulo(eje, "Lo único que ves es la volatilidad, no el estado",
       "Trescientos días de la cadena simulada, calma y tensión")
eje.set_xlabel("día (las marcas rojas son el inicio de cada episodio)")
eje.set_ylabel("volatilidad diaria")
eje.legend(loc="upper right", fontsize=7.5)
rejilla(eje)
numeros(eje, "x")

# ── Arriba a la derecha: el detector, medido por clases ───────────────────────
eje = ejes[0, 1]
acierto_filtro = float((alerta == (estado == 1)).mean())
acierto_calma = float((estado == 0).mean())
precision = float((alerta & (estado == 1)).sum() / alerta.sum())
exhaustividad = float((alerta & (estado == 1)).sum() / (estado == 1).sum())
metricas = ["decir siempre\n«calma»", "acierto del\nfiltro", "precisión\nen tensión",
            "exhaustividad\nen tensión"]
valores = [acierto_calma, acierto_filtro, precision, exhaustividad]
colores = [REJILLA, AZUL, ROJO, NARANJA]
eje.bar(np.arange(4), valores, width=0.55, color=colores, alpha=0.9)
for i, val in enumerate(valores):
    eje.text(i, val + 0.02, f"{val:.3f}".replace(".", ","), ha="center", fontsize=8.5,
             color=colores[i])
eje.set_xticks(np.arange(4))
eje.set_xticklabels(metricas, fontsize=8)
eje.set_ylim(0, 0.92)
anotar(eje, "el acierto lo domina la clase mayoritaria",
       xy=(0, acierto_calma), xytext=(0.22, 0.82), color=MORADO, flecha=False)
titulo(eje, "El acierto no sirve con clases desbalanceadas",
       "Hay que mirar la precisión de la clase minoritaria")
eje.set_ylabel("proporción de días")
rejilla(eje)
numeros(eje, "y")

# ── Abajo a la izquierda: dónde está el golpe ─────────────────────────────────
eje = ejes[1, 0]
# Para cada episodio de tensión, el retorno medio de sus cuatro primeros días y el del resto.
primeros, resto = [], []
for t in range(1, n):
    if estado[t] == 1 and estado[t - 1] == 0:
        primeros.append(r[t:t + 4].mean())
        fin = t
        while fin < n and estado[fin] == 1:
            fin += 1
        if fin - t > 4:
            resto.append(r[t + 4:fin].mean())
primeros = np.array(primeros) * 100
resto = np.array(resto) * 100
cajas = eje.boxplot([primeros, resto], widths=0.5, patch_artist=True,
                    tick_labels=["primeros 4\ndías de tensión", "resto del\nepisodio"])
for caja, col in zip(cajas["boxes"], (ROJO, AZUL)):
    caja.set_facecolor(col)
    caja.set_alpha(0.55)
    caja.set_edgecolor(col)
for mediana in cajas["medians"]:
    mediana.set_color(TEXTO)
eje.axhline(0, color=TEXTO, linewidth=0.9, linestyle="--")
anotar(eje, "la media de los dos tramos es casi la misma",
       xy=(1.0, float(np.median(primeros))), xytext=(0.10, 0.74), color=MORADO)
titulo(eje, "El aviso es de volatilidad, no de caída",
       "El detector no evita un desplome: evita exposición durante todo el episodio")
eje.set_ylabel("retorno medio del tramo (%)")
rejilla(eje)
numeros(eje, "y")

# ── Abajo a la derecha: el retardo, medido sobre los 108 episodios ────────────
eje = ejes[1, 1]
retardos = []
for t in range(1, n):
    if estado[t] == 1 and estado[t - 1] == 0 and alerta[t:].any():
        retardos.append(int(np.argmax(alerta[t:])))
retardos = np.array(retardos)
eje.hist(retardos, bins=np.arange(-0.5, 21.5), color=CIAN, alpha=0.85)
eje.axvline(float(np.median(retardos)), color=ROJO, linewidth=1.8,
            label=f"retardo mediano: {np.median(retardos):.0f} días")
eje.axvline(10, color=NARANJA, linewidth=1.5, linestyle="--",
            label="duración media del episodio: 10 días")
titulo(eje, "Cuándo llega el aviso dentro del episodio",
       f"{retardos.size} episodios de tensión detectados con la ventana de 20 días")
eje.set_xlabel("días desde el inicio del episodio hasta la primera alerta")
eje.set_ylabel("nº de episodios")
eje.legend(loc="upper right", fontsize=8)
rejilla(eje)
numeros(eje, "x")
anotar(eje, "muchas alertas llegan con el episodio\ncasi terminado: son falsos positivos",
       xy=(float(np.percentile(retardos, 85)), 4), xytext=(0.34, 0.62), color=ROJO)

guardar(fig, "regimenes-de-mercado-detector-y-retardo")
