"""fechas-y-horas-1.py — el desfase de Madrid frente a UTC a lo largo del anio y los dos
dias del anio que no duran 24 horas. La figura de la pagina de fechas y horas (fase 3)."""

import calendar
import datetime as dt
from zoneinfo import ZoneInfo

import numpy as np

from comun import *

estilo()
madrid = ZoneInfo("Europe/Madrid")
anio = 2026
utc = dt.timezone.utc


def ultimo_domingo(mes):
    """El dia del cambio de hora en la Union Europea: el último domingo del mes."""
    ultimo = dt.date(anio, mes, calendar.monthrange(anio, mes)[1])
    return ultimo - dt.timedelta(days=(ultimo.weekday() + 1) % 7)   # 6 es domingo


cambio_primavera = ultimo_domingo(3)     # 29 de marzo de 2026
cambio_otono = ultimo_domingo(10)        # 25 de octubre de 2026


def duracion_del_dia_local(d):
    """Horas reales entre la medianoche local de d y la del dia siguiente."""
    ini = dt.datetime(d.year, d.month, d.day, tzinfo=madrid)
    fin = ini + dt.timedelta(days=1)     # misma hora de pared, no 24 horas despues
    return (fin.astimezone(utc) - ini.astimezone(utc)).total_seconds() / 3600


# Desfase de Madrid frente a UTC, muestreado cada dia a las 12:00 UTC
inicio = dt.datetime(anio, 1, 1, 12, tzinfo=utc)
fechas = [inicio + dt.timedelta(days=int(d)) for d in np.arange(365)]
desfase = np.array([f.astimezone(madrid).utcoffset().total_seconds() / 3600 for f in fechas])
dia_del_anio = np.arange(1, 366)

fig, ejes = plt.subplots(1, 2, figsize=(9.2, 3.9))

ejes[0].step(dia_del_anio, desfase, color=AZUL, linewidth=1.8, where="post")
ejes[0].set_yticks([1, 2], labels=["UTC+1\n(invierno)", "UTC+2\n(verano)"])
ejes[0].set_ylim(0.5, 2.6)
ejes[0].set_xlabel("día del año")
ejes[0].set_ylabel("desfase de Madrid frente a UTC")
titulo(ejes[0], "El desfase de Madrid no es un número fijo")

# Las dos fechas en que el reloj salta. Cada etiqueta se queda en su franja de invierno, que
# es la unica banda vacia: en la de verano la escalera pasa justo por el medio.
for fecha, etiqueta, texto, punta in (
        (cambio_primavera, "cambio de marzo", (0.03, 0.09), (88, 1.02)),
        (cambio_otono, "cambio de octubre", (0.60, 0.52), (300, 1.08))):
    dia = (fecha - dt.date(anio, 1, 1)).days + 1
    ejes[0].axvline(dia, color=ROJO, linewidth=1.0, linestyle=":")
    anotar(ejes[0], etiqueta, xy=punta, xytext=texto, color=ROJO, align="left")
rejilla(ejes[0])
numeros(ejes[0], ejes="x")

etiquetas = ["un día\ncualquiera", "domingo de\nmarzo", "domingo de\noctubre"]
valores = [duracion_del_dia_local(dt.date(anio, 6, 15)),
           duracion_del_dia_local(cambio_primavera),
           duracion_del_dia_local(cambio_otono)]
colores = [REJILLA, NARANJA, MORADO]
barras = ejes[1].bar(etiquetas, valores, color=colores, width=0.55)
for barra, valor in zip(barras, valores):
    ejes[1].text(barra.get_x() + barra.get_width() / 2, valor + 0.25, "%.0f h" % valor,
                 ha="center", color=TEXTO, fontsize=9)
ejes[1].set_ylim(0, 27.5)
ejes[1].set_ylabel("horas reales que dura el día")
titulo(ejes[1], "Los dos días que no duran 24 horas")
rejilla(ejes[1])
numeros(ejes[1], ejes="y")

guardar(fig, "fechas-y-horas-utc-y-horario-de-verano")
