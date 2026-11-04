"""metricas-y-alertas-1.py — el presupuesto de error de un mes y la explosión de cardinalidad
de una etiqueta con identificador de usuario. La figura de la pagina de métricas, SLO y alertas
(fase 11)."""

import numpy as np

from comun import *

estilo()

SLO = 0.999
DIAS = 30
# Los numeros de la pagina: 6 horas al 4 % de error dejan el 33 % del presupuesto del mes.
TASA_INCIDENTE = 0.04
HORAS_INCIDENTE = 6
DIA_DEL_INCIDENTE = 12

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.4))

# --- Izquierda: como se gasta el presupuesto a lo largo de la ventana ---------------
dias = np.arange(1, DIAS + 1, dtype=float)
horas_del_dia = np.where(dias == DIA_DEL_INCIDENTE, HORAS_INCIDENTE, 0.0)
# Cuota del presupuesto mensual que se gasta cada dia: lo normal mas el incidente.
cuota = (1 / DIAS) + horas_del_dia * (TASA_INCIDENTE - (1 - SLO)) / (DIAS * 24)
consumido = np.cumsum(cuota)
objetivo = dias / DIAS

izq.plot(dias, objetivo, color=REJILLA, linewidth=1.2, linestyle="--",
         label="ritmo que lo gasta justo")
izq.step(dias, consumido, where="post", color=AZUL, linewidth=1.6, label="consumo real")
izq.axhspan(0.95, 1.10, color=ROJO, alpha=0.10, linewidth=0)
# La banda naranja marca el dia del incidente: es la unica vertical del mes que se sale del ritmo.
izq.axvspan(DIA_DEL_INCIDENTE, DIA_DEL_INCIDENTE + 1, color=NARANJA, alpha=0.30, linewidth=0)
anotar(izq, "un solo dia: el 33 % del\npresupuesto del mes", xy=(13, consumido[12]),
       xytext=(0.34, 0.74), color=MORADO)
izq.text(29.7, 0.965, "presupuesto agotado", color=ROJO, fontsize=8.5, ha="right", va="bottom")
izq.set_xlim(0, 30)
izq.set_ylim(0, 1.12)
izq.set_xlabel("dias de la ventana")
izq.set_ylabel("presupuesto consumido")
izq.legend(loc="upper left")
titulo(izq, "El presupuesto se gasta a golpes, no por igual",
       "SLO 99,9 %: el mes entero cabe en 43,2 minutos")
rejilla(izq)
numeros(izq, ejes="both")

# --- Derecha: cada etiqueta multiplica las series, no las suma ----------------------
etiquetas = ["base", "+ 5 rutas", "+ 3 regiones", "+ 4 metodos", "+ 100.000 usuarios"]
series = np.array([20, 20 * 5, 20 * 5 * 3, 20 * 5 * 3 * 4, 20 * 5 * 3 * 4 * 100_000],
                  dtype=float)
colores = [VERDE, VERDE, VERDE, AZUL, ROJO]
# Barras horizontales: las etiquetas de categoria van a la izquierda y el logaritmo a lo ancho,
# asi no hay que girar el texto ni apretarlo contra el borde.
posiciones = np.arange(len(series))
barras = der.barh(posiciones, series, color=colores, height=0.55)
# Escala logaritmica: sin ella, las cuatro primeras barras serian invisibles.
der.set_xscale("log")
etiquetas_x = ["%s" % f"{int(v):,}".replace(",", ".") for v in series]
der.bar_label(barras, labels=etiquetas_x, padding=3, fontsize=8)
der.set_yticks(posiciones)
der.set_yticklabels(etiquetas, fontsize=8.5)
der.set_xlim(5, 1e9)
# En escala logaritmica el formateador de coma decimal escribe los nueve exponentes seguidos y se
# solapan. Se abrevian a k y M: las cifras exactas ya van en la etiqueta de cada barra.
def abreviar(v):
    if v >= 1e6:
        return "%gM" % (v / 1e6)
    if v >= 1e3:
        return "%gk" % (v / 1e3)
    return "%g" % v


marcas = [10 ** k for k in range(1, 10)]
der.set_xticks(marcas)
der.set_xticklabels([abreviar(m) for m in marcas], fontsize=8)
anotar(der, "una sola etiqueta con el id\nde usuario multiplica por 100.000",
       xy=(series[4], 4), xytext=(0.06, 0.60), color=ROJO)
der.set_xlabel("series temporales por métrica")
titulo(der, "La etiqueta que tumba el sistema de métricas",
       "las series se multiplican, no se suman")
rejilla(der, eje="x")

guardar(fig, "metricas-presupuesto-y-cardinalidad")
