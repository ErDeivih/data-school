"""cap-y-consistencia-1.py — lo que cuesta esperar a un cuorum y cuando el cuorum garantiza la
intersección. La figura de la pagina de CAP y consistencia (fase 11)."""

import numpy as np
from matplotlib.colors import to_rgb

from comun import *

estilo()

# Latencias de 5 replicas con cola, como las reales: lognormal con mediana de 10 ms.
rng = np.random.default_rng(0)
muestras = rng.lognormal(mean=np.log(10.0), sigma=0.6, size=(200_000, 5))
ordenadas = np.sort(muestras, axis=1)

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.6, 4.2))

# --- Izquierda: la mediana no cambia, la cola si ------------------------------------
estrategias = ["1 replica\nal azar", "el más rapido\nW=1", "3 de 5\n(cuorum)", "los 5\nW=N"]
series = [muestras[:, 0], ordenadas[:, 0], ordenadas[:, 2], ordenadas[:, 4]]
medianas = [float(np.median(s)) for s in series]
p99 = [float(np.percentile(s, 99)) for s in series]

x = np.arange(len(estrategias))
ancho = 0.38
# Dos barras por estrategia: lo tipico y lo peor, que es lo que sufre el usuario.
izq.bar(x - ancho / 2, medianas, ancho, color=AZUL, label="mediana")
izq.bar(x + ancho / 2, p99, ancho, color=ROJO, label="p99 (peor 1 %)")
izq.set_xticks(x)
izq.set_xticklabels(estrategias, fontsize=8.5)
# La raya marca la mediana de una sola replica: el cuorum no la mejora, solo la iguala.
izq.axhline(medianas[0], color=REJILLA, linewidth=1.0, linestyle="--")
anotar(izq, "leer de una replica:\nla peor cola", xy=(0.19, p99[0]), xytext=(0.05, 0.66),
       color=ROJO)
anotar(izq, "el cuorum no toca la mediana:\ncorta la cola", xy=(2.19, p99[2]), xytext=(0.40, 0.44),
       color=MORADO)
izq.set_ylim(0, 74)
izq.set_ylabel("latencia de la lectura (ms)")
titulo(izq, "El cuórum no baja la mediana, corta la cola",
       "5 réplicas con latencias de cola (mediana 10 ms)")
# La leyenda va fuera del area de datos: dentro chocaria con las anotaciones.
izq.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0), ncols=2, fontsize=8.5)
rejilla(izq)
numeros(izq, ejes="y")

# --- Derecha: que parejas (W, R) cruzan de verdad -----------------------------------
# Para cada W y cada R se comprueba la condicion del cuorum: W + R > N.
n = 5
valido = np.zeros((n, n))
for w in range(1, n + 1):
    for r in range(1, n + 1):
        valido[w - 1, r - 1] = 1 if w + r > n else 0
# Rejilla de dos colores: azul si la pareja garantiza interseccion, gris claro si no.
# Se construye con los colores del modulo en vez de un mapa de color de matplotlib, para no
# salirse de la paleta del portal.
colores = np.zeros((n, n, 3))
for w in range(n):
    for r in range(n):
        colores[w, r] = to_rgb(AZUL) if valido[w, r] else tuple(0.90 * c for c in to_rgb(REJILLA))
der.imshow(colores, origin="lower", aspect="auto")
for w in range(n):
    for r in range(n):
        # El blanco sobre el azul y el negro sobre el gris: el texto se lee en las dos celdas.
        der.text(r, w, "cruza" if valido[w, r] else "no", ha="center", va="center",
                 fontsize=8, color="white" if valido[w, r] else TEXTO)
der.set_xticks(range(n))
der.set_xticklabels([f"R={r}" for r in range(1, n + 1)], fontsize=8.5)
der.set_yticks(range(n))
der.set_yticklabels([f"W={w}" for w in range(1, n + 1)], fontsize=8.5)
der.set_xlabel("acuses que se piden en la lectura (R)")
der.set_ylabel("acuses que se piden en la escritura (W)")
titulo(der, "Con N=5 solo cruzan 15 de 25 parejas",
       "las celdas azules cumplen W + R > N")
rejilla(der)
# La rejilla se dibuja sola en imshow; numeros() solo pondria la coma decimal en unos ejes
# que llevan texto (W= y R=), asi que aqui no hace falta.

guardar(fig, "cap-consistencia-coste-de-esperar")
