"""evaluacion-de-modelos-generativos-1.py — dos formas de fallar que una sola métrica no
distingue: colapsar en un modo o repartir de más. La figura de evaluación de modelos
generativos (fase 7)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)


def fid(mu_r, S_r, mu_g, S_g):
    vals, vecs = np.linalg.eigh(S_r)
    raiz = vecs @ np.diag(np.sqrt(vals)) @ vecs.T
    A = raiz @ S_g @ raiz
    return float(((mu_r - mu_g) ** 2).sum() + np.trace(S_r) + np.trace(S_g)
                 - 2 * np.sqrt(np.linalg.eigvalsh(A)).sum())


# Datos reales: dos modos bien separados, la mitad de la masa en cada uno
n = 120
real = np.vstack([azar.normal([-1.2, 0.0], 0.35, (n, 2)),
                  azar.normal([1.2, 0.0], 0.35, (n, 2))])
# Modelo A: se ha quedado con un solo modo (colapso)
A = azar.normal([1.2, 0.0], 0.30, (2 * n, 2))
# Modelo B: cubre todo, pero reparte de mas y sin forma
B = azar.normal([0.0, 0.0], 1.40, (2 * n, 2))

radio = 0.60
d_A_real = np.linalg.norm(A[:, None, :] - real[None, :, :], axis=2)
d_B_real = np.linalg.norm(B[:, None, :] - real[None, :, :], axis=2)
d_real_A = np.linalg.norm(real[:, None, :] - A[None, :, :], axis=2)
d_real_B = np.linalg.norm(real[:, None, :] - B[None, :, :], axis=2)
prec_A, rec_A = (d_A_real.min(1) <= radio).mean(), (d_real_A.min(1) <= radio).mean()
prec_B, rec_B = (d_B_real.min(1) <= radio).mean(), (d_real_B.min(1) <= radio).mean()

S_r = np.cov(real.T)
fid_A = fid(real.mean(0), S_r, A.mean(0), np.cov(A.T))
fid_B = fid(real.mean(0), S_r, B.mean(0), np.cov(B.T))
print(f"precisión A {prec_A:.4f}   recall A {rec_A:.4f}   FID A {fid_A:.4f}")
print(f"precisión B {prec_B:.4f}   recall B {rec_B:.4f}   FID B {fid_B:.4f}")

fig, ejes = plt.subplots(1, 2, figsize=(8.4, 3.9))

# --- Izquierda: los dos fallos, uno al lado del otro ---
ax = ejes[0]
ax.plot(real[:, 0], real[:, 1], "o", color=REJILLA, markersize=2.6, label="datos reales")
ax.plot(A[:, 0], A[:, 1], "o", color=AZUL, markersize=2.6, alpha=0.55,
        label="modelo A: un solo modo")
ax.plot(B[:, 0], B[:, 1], "o", color=NARANJA, markersize=2.6, alpha=0.45,
        label="modelo B: reparte de más")
ax.set_xlim(-4.5, 4.5)
ax.set_ylim(-3.2, 3.2)
ax.set_xlabel("primera variable")
ax.set_ylabel("segunda variable")
ax.legend(loc="upper left", fontsize=8.5, markerscale=3)
anotar(ax, "A nunca genera la mitad izquierda:\nrecall bajo",
       (-1.2, 0.0), (0.03, 0.20), color=AZUL, fondo=True)
anotar(ax, "B lo cubre todo, pero la mayoría\nde sus muestras no se parece a nada",
       (4.0, 0.9), (0.97, 0.62), color=NARANJA, align="right", fondo=True)
titulo(ax, "Dos formas de fallar, no una", "la misma métrica única para los dos casos")
rejilla(ax, eje="both")
numeros(ax, ejes="both")

# --- Derecha: las dos cifras que sí los separan ---
ax = ejes[1]
pos = np.arange(2)
ancho = 0.34
ax.bar(pos - ancho / 2, [prec_A, prec_B], ancho, color=AZUL, label="fidelidad (precisión)")
ax.bar(pos + ancho / 2, [rec_A, rec_B], ancho, color=NARANJA, label="cobertura (recall)")
ax.set_xticks(pos)
ax.set_xticklabels([f"modelo A\n(un solo modo)\nFID {fid_A:.2f}".replace(".", ","),
                    f"modelo B\n(reparte de más)\nFID {fid_B:.2f}".replace(".", ",")])
ax.set_ylim(0, 1.45)
ax.set_ylabel("proporción")
ax.legend(loc="upper center", fontsize=8.5, ncols=2)
titulo(ax, "El número único elige al peor", "el FID más bajo es el del modelo B")
rejilla(ax)
numeros(ax, ejes="y")

guardar(fig, "evaluacion-generativos-fidelidad-y-cobertura")
