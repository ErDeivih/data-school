"""consenso-y-replicacion-1.py — por qué los pares no aportan y por qué hay que sortear el tiempo
de espera de la elección. La figura de la pagina de consenso y replicación (fase 11)."""

import numpy as np

from comun import *

estilo()

fig, (arriba, abajo) = plt.subplots(2, 1, figsize=(7.6, 6.2))

# --- Arriba: mayoria y fallos tolerados --------------------------------------------
nodos = np.arange(1, 8)
mayorias = nodos // 2 + 1
tolerados = (nodos - 1) // 2

# Barra ancha para la mayoria y estrecha delante para los fallos, en la misma categoria.
arriba.bar(nodos, mayorias, width=0.62, color=AZUL, label="votos para decidir (mayoría)")
arriba.bar(nodos, tolerados, width=0.26, color=NARANJA, label="fallos que tolera")
for n, q, f in zip(nodos, mayorias, tolerados):
    arriba.text(n, q + 0.12, f"{q}", ha="center", fontsize=8.5, color=AZUL)
    arriba.text(n, -0.42, f"{f}", ha="center", fontsize=8.5, color=NARANJA)
# Los pares y el impar que les sigue toleran lo mismo: la llave lo deja a la vista.
for par in (2, 4, 6):
    # Un corchete fino entre el par y el impar que le sigue: mismo numero de fallos tolerados.
    # Va por encima de la barra mas alta (el 4 de N=7) para no tacharla.
    arriba.annotate("", xy=(par, 4.75), xytext=(par + 1, 4.75),
                    arrowprops=dict(arrowstyle="<->", color=ROJO, linewidth=1.1))
    arriba.text(par + 0.5, 4.84, "misma tolerancia", ha="center", fontsize=8, color=ROJO)
arriba.set_xticks(nodos)
arriba.set_ylim(-0.8, 6.0)
arriba.set_xlabel("nodos con voto (N)")
arriba.set_ylabel("nodos")
titulo(arriba, "Los clústeres pares no compran tolerancia",
       "la barra naranja son los fallos que aguanta sin dejar de decidir")
# La leyenda va fuera del area de datos: dentro se pisaria con los corchetes.
arriba.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncols=2, fontsize=8.5)
rejilla(arriba)
numeros(arriba, ejes="y")

# --- Abajo: el sorteo del tiempo de espera rompe los empates ------------------------
rng = np.random.default_rng(7)
rondas = 20_000


def empate(timeouts):
    """Hay empate si más de un nodo expira en el mismo instante mínimo."""
    return int((timeouts == timeouts.min()).sum()) > 1


aleatorios = rng.integers(150, 301, size=(rondas, 5))
iguales = np.full((rondas, 5), 200)
porcentajes = [100 * sum(map(empate, aleatorios)) / rondas,
               100 * sum(map(empate, iguales)) / rondas]

etiquetas = ["tiempos sorteados\n(150 a 300 ms)", "tiempos fijos\n(200 ms)"]
barras = abajo.bar(etiquetas, porcentajes, color=[VERDE, ROJO], width=0.45)
abajo.bar_label(barras, labels=[f"{p:.1f} %".replace(".", ",") for p in porcentajes],
                padding=3, fontsize=9)
anotar(abajo, "el clúster se queda\ndando vueltas sin elegir", xy=(1, 90), xytext=(0.30, 0.60),
       color=ROJO)
abajo.set_ylim(0, 118)
abajo.set_ylabel("% de rondas con empate")
titulo(abajo, "Sortear el tiempo de espera evita el empate",
       "5 nodos: la ronda siguiente resuelve los empates que quedan")
rejilla(abajo)
numeros(abajo, ejes="y")

guardar(fig, "consenso-mayorias-y-elección")
