"""arbitraje-estadistico-1.py — el nivel del residuo vuelve a su sitio, pero el coste de
cada reajuste decide si esa vuelta es un negocio. Figura de la pagina de arbitraje
estadístico (fase 9).

Tres paneles, en el orden del argumento: (1) el nivel del residuo de un activo vuelve a
su media movil; (2) su s-score es lo que dispara el peso, y sale de la banda cientos de
veces; (3) la cartera entera con la misma senal, pagando 0, 5 y 10 puntos basicos por
unidad de giro. La distancia entre esas tres curvas es el concepto."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)
T, N = 1400, 8
ventana = 60

# El NIVEL acumulado del residuo es lo que revierte (phi = 0,92); su retorno no.
X = np.zeros((T, N))
for t in range(1, T):
    X[t] = 0.92 * X[t - 1] + azar.normal(0, 0.002, N)
dX = np.diff(X, axis=0, prepend=np.zeros((1, N)))          # retorno del residuo

# Cada periodo: s-score del nivel con ventana movil, pesos contra la desviacion y
# neutralidad en dolares restando la media.
pesos = np.zeros((T, N))
for t in range(ventana, T - 1):
    hist = X[t - ventana:t + 1]
    s = (hist[-1] - hist.mean(axis=0)) / hist.std(axis=0, ddof=1)
    w = -np.clip(s, -3.0, 3.0)                             # se apuesta contra la desviacion
    pesos[t] = w / np.abs(w).sum() - w.mean() / np.abs(w).sum()

usados = np.arange(ventana, T - 1)
elegido = 0
nivel = X[usados, elegido]
media_movil = np.array([X[t - ventana:t + 1, elegido].mean() for t in usados])
desv_movil = np.array([X[t - ventana:t + 1, elegido].std(ddof=1) for t in usados])
s_activo = (nivel - media_movil) / desv_movil
bruto = np.array([pesos[t] @ dX[t + 1] for t in usados])
# `giro` sale de una diferencia, asi que se rellena por delante: la cartera se abre.
giro = np.r_[0.0, np.abs(np.diff(pesos[usados], axis=0)).sum(axis=1)]
equilibrio_pb = 1e4 * bruto.sum() / giro.sum()

fig, ejes = plt.subplots(3, 1, figsize=(7.0, 7.6), sharex=True)

# ── 1. El nivel vuelve a su media movil ───────────────────────────────────────
eje = ejes[0]
eje.plot(nivel, color=AZUL, linewidth=1.1, label="nivel del residuo")
eje.plot(media_movil, color=ROJO, linewidth=1.4, linestyle="--",
         label="su media de los últimos 60 periodos")
eje.fill_between(usados, media_movil - desv_movil, media_movil + desv_movil,
                 color=REJILLA, alpha=0.16, zorder=0)
titulo(eje, "El nivel del residuo vuelve a su media móvil",
       "La banda gris es ±1 desviación; lo que revierte es este nivel, no su retorno")
eje.set_ylabel("nivel\nacumulado")
eje.legend(loc="upper right", fontsize=8)
rejilla(eje)
i_sale = int(np.argmax(s_activo > 1.5))
i_vuelve = i_sale + int(np.argmax(s_activo[i_sale:] < 0.2))
anotar(eje, "cuando se aleja de la media, la posición\nse abre en contra",
       (float(i_sale), float(nivel[i_sale])), (0.03, 0.30), color=MORADO)
anotar(eje, "y al volver al centro se cierra",
       (float(i_vuelve), float(nivel[i_vuelve])), (0.74, 0.72), color=VERDE)

# ── 2. El s-score: el numero que decide el peso ───────────────────────────────
eje = ejes[1]
eje.plot(s_activo, color=CIAN, linewidth=0.9)
eje.axhspan(-1, 1, color=REJILLA, alpha=0.16, zorder=0)
eje.axhline(0, color=TEXTO, linewidth=0.9, linestyle="--")
titulo(eje, "Ese alejamiento, medido en desviaciones, es el s-score",
       "Cuanto más fuera de la banda, más peso se le da a ese activo")
eje.set_ylabel("s-score\ndel activo")
eje.set_ylim(-4, 4.4)
rejilla(eje)
eje.text(0.015, 0.90, "el signo del s-score dice la dirección y su tamaño, cuánto peso",
         transform=eje.transAxes, fontsize=8.5, color=TEXTO, va="top")

# ── 3. La misma senal con tres costes: aqui se decide el negocio ──────────────
eje = ejes[2]
coste_cum = np.cumsum(giro)
acumulado_bruto = np.cumsum(bruto)
x = np.arange(acumulado_bruto.size)
eje.plot(x, acumulado_bruto, color=AZUL, linewidth=1.8, label="sin coste (bruto)")
eje.plot(x, acumulado_bruto - coste_cum * 0.0005, color=CIAN, linewidth=1.8,
         label="a 5 pb por unidad girada")
eje.plot(x, acumulado_bruto - coste_cum * 0.0010, color=ROJO, linewidth=1.8,
         label="a 10 pb por unidad girada")
eje.axhline(0, color=TEXTO, linewidth=0.9, linestyle="--")
titulo(eje, "El mismo acierto, tres costes: dos negocios y una ruina",
       "Resultado acumulado de la cartera de residuos, en unidades de retorno")
eje.set_xlabel("periodo desde el final de la ventana de estimación")
eje.set_ylabel("resultado\nacumulado")
eje.set_xlim(-40, x[-1] + 300)
rejilla(eje)
eje.legend(loc="upper left", fontsize=8)
numeros(eje, "y")
# Cada etiqueta va a la derecha del final de su curva, en su misma altura.
final = {clave: float((acumulado_bruto - coste_cum * pb)[-1])
         for clave, pb in (("bruto", 0.0), ("5 pb", 0.0005), ("10 pb", 0.0010))}
eje.text(x[-1] + 20, final["bruto"], f"bruto {final['bruto']:+.2f}",
         color=AZUL, fontsize=8.5, va="center")
eje.text(x[-1] + 20, final["5 pb"], f"a 5 pb queda {final['5 pb']:+.2f}",
         color=CIAN, fontsize=8.5, va="center")
eje.text(x[-1] + 20, final["10 pb"], f"a 10 pb se pierde {abs(final['10 pb']):.2f}",
         color=ROJO, fontsize=8.5, va="center")
eje.text(0.30, 0.10, f"coste de equilibrio de esta señal: {equilibrio_pb:.1f} pb "
                     f"por unidad de giro (giro medio {giro.mean():.2f})",
         transform=eje.transAxes, fontsize=8.5, color=MORADO, va="bottom", zorder=5,
         bbox=dict(boxstyle="round,pad=0.2", facecolor="none", edgecolor="none"))

guardar(fig, "arbitraje-estadistico-coste-se-come-el-bruto")
