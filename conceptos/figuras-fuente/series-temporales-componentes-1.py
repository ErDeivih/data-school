"""series-temporales-componentes-1.py — la serie que se ve es la suma de la tendencia,
el patron que se repite y el ruido; y por qué una estacionalidad multiplicativa hay que
llevarla al logaritmo. La figura de la pagina de componentes de una serie temporal."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Tres anos de ventas diarias de una panaderia: tendencia + semana + ano + ruido.
dias = np.arange(3 * 365)
tendencia = 100 + 0.05 * dias
semana = np.tile(np.array([-8, -6, -4, -2, 6, 14, 10], dtype=float), dias.size // 7 + 1)[:dias.size]
ano = 6 * np.sin(2 * np.pi * dias / 365.25)
ruido = azar.normal(0, 4.0, dias.size)
serie = tendencia + semana + ano + ruido

fig = plt.figure(figsize=(11.0, 6.4))
rejilla_gs = fig.add_gridspec(2, 2)
eje_serie = fig.add_subplot(rejilla_gs[0, :])
eje_tend = fig.add_subplot(rejilla_gs[1, 0])
eje_sem = fig.add_subplot(rejilla_gs[1, 1])

# Arriba: la serie tal cual, con las semanas sombreadas de dos en dos.
eje_serie.plot(dias, serie, color=AZUL, linewidth=0.8)
for inicio in range(0, dias.size, 14):
    eje_serie.axvspan(inicio, min(inicio + 7, dias.size), color=REJILLA, alpha=0.18, zorder=0)
eje_serie.set_title("Ventas diarias: suben y además tienen ritmo semanal")
eje_serie.set_xlabel("dia")
eje_serie.set_ylabel("ventas")
anotar(eje_serie, "las franjas grises son las semanas:\nlo que sube de una a otra es la tendencia,\nlo que se repite dentro es la estacionalidad",
       (60, serie[60]), (0.02, 0.96), TEXTO)
rejilla(eje_serie)
numeros(eje_serie)

# Abajo izquierda: la tendencia, que es la parte que se extrapola.
eje_tend.plot(dias, serie, color=REJILLA, linewidth=0.6, label="ventas diarias")
media_movil = np.convolve(serie, np.ones(365) / 365, mode="valid")
eje_tend.plot(dias[364:], media_movil, color=MORADO, linewidth=2.0, label="media de 365 dias")
eje_tend.set_title("La tendencia: la dirección de fondo, no una recta")
eje_tend.set_xlabel("dia")
eje_tend.set_ylabel("ventas")
eje_tend.legend(loc="upper left", fontsize=8)
anotar(eje_tend, "promediar un ano entero cancela el patron\nsemanal y el anual: queda la dirección",
       (700, media_movil[336]), (0.34, 0.16), MORADO)
rejilla(eje_tend)
numeros(eje_tend)

# Abajo derecha: el ritmo anual, que se estima comparando un mismo mes de anos distintos.
anual = np.array([0, -2, -3, -1, 5, 9, 12, 10, 4, 2, -4, -6], dtype=float)
eje_sem.bar(np.arange(1, 13), anual, color=MORADO, alpha=0.85, width=0.6)
eje_sem.axhline(0, color=TEXTO, linewidth=0.9, alpha=0.6)
eje_sem.set_xticks([1, 3, 5, 7, 9, 11])
eje_sem.set_title("El patron anual: se repite, luego se aprende")
eje_sem.set_xlabel("mes del ano")
eje_sem.set_ylabel("ventas sobre la media")
anotar(eje_sem, "doce efectos que suman cero: si no\nsuman cero, has metido tendencia en el patron",
       (1, anual[0]), (0.66, 0.13), TEXTO)
rejilla(eje_sem)
numeros(eje_sem)

guardar(fig, "series-temporales-tendencia-y-patron")

# --- Segunda figura: aditiva o multiplicativa -------------------------------------
fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.3), sharey=True)
semanas = np.arange(1, 105)
patron = 12 * np.sin(2 * np.pi * semanas / 7)     # el fin de semana, 12 arriba y 12 abajo
nivel = 100 + 3.0 * semanas                       # la panaderia crece: 100 -> 412
aditiva = nivel + patron
multiplicativa = nivel * (1 + patron / 100)       # el sabado sube un 12 % del nivel

for eje, valores, color, titulo_panel, nota in (
    (ejes[0], aditiva, AZUL, "Aditiva: el sabado suma lo mismo siempre",
     "la brecha entre sabado y lunes\nno cambia al crecer la serie"),
    (ejes[1], multiplicativa, NARANJA, "Multiplicativa: el sabado sube con el nivel",
     "la misma proporción: la brecha crece\ncon el nivel"),
):
    eje.plot(semanas, valores, color=color, linewidth=1.2)
    eje.set_title(titulo_panel)
    eje.set_xlabel("semana")
    anotar(eje, nota, (45, valores[44]), (0.30, 0.14), color)
    rejilla(eje)
    numeros(eje)
ejes[0].set_ylabel("ventas")
eje_zoom = ejes[0].inset_axes([0.58, 0.62, 0.38, 0.32])
eje_zoom.plot(semanas[:21], aditiva[:21], color=AZUL, linewidth=1.2)
eje_zoom.plot(semanas[:21], multiplicativa[:21], color=NARANJA, linewidth=1.2)
eje_zoom.set_xticks([])
eje_zoom.set_yticks([])
eje_zoom.set_title("al principio coinciden", fontsize=7.5)
rejilla(eje_zoom)
eje_zoom2 = ejes[1].inset_axes([0.04, 0.54, 0.42, 0.36])
eje_zoom2.plot(semanas, np.log(multiplicativa), color=MORADO, linewidth=1.1)
eje_zoom2.set_xticks([])
eje_zoom2.set_yticks([])
eje_zoom2.set_title("la misma serie en logaritmo: aditiva", fontsize=7.5)
rejilla(eje_zoom2)

guardar(fig, "series-temporales-aditiva-y-multiplicativa")
