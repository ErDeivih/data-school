"""seleccion-de-features-1.py — anadir columnas que no aportan no da información: da
varianza. La figura de la pagina de selección de variables."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# --- Izquierda: el camino de lasso, alpha de 0 a 2 ---------------------------------
n, d = 120, 6
X = azar.normal(size=(n, d))
beta = np.array([3.0, 0.0, 0.0, -2.0, 0.0, 0.0])          # solo la 1 y la 4 tienen efecto
y = X @ beta + azar.normal(0, 0.5, n)

alphas = np.linspace(0.001, 2.0, 120)
caminos = np.zeros((alphas.size, d))
for i, a in enumerate(alphas):
    # Descenso por coordenadas con soft-threshold: es el mismo algoritmo que usa Lasso.
    coef = np.zeros(d)
    for _ in range(200):
        for j in range(d):
            r = y - X @ coef + coef[j] * X[:, j]
            rho = X[:, j] @ r
            coef[j] = np.sign(rho) * max(abs(rho) - a * n, 0.0) / (X[:, j] @ X[:, j])
    caminos[i] = coef

colores = [AZUL, CIAN, MORADO, ROJO, NARANJA, VERDE]
etiquetas = ["x1 (efecto real)", "x2 (ruido)", "x3 (ruido)",
             "x4 (efecto real)", "x5 (ruido)", "x6 (ruido)"]

# --- Derecha: el mismo modelo con y sin 45 columnas de ruido -----------------------
n2 = 60
solo_real, con_ruido = [], []
for s in range(12):
    r = np.random.default_rng(100 + s)
    Xr = r.normal(size=(n2, 5))
    yr = Xr @ np.array([2.0, -1.0, 0.5, 0.0, 0.0]) + r.normal(0, 1.0, n2)
    R = r.normal(size=(n2, 45))
    Xa = np.hstack([Xr, R])
    # Validacion cruzada de 5 pliegues, hecha a mano para no depender de sklearn.
    idx = r.permutation(n2)
    pliegues = np.array_split(idx, 5)
    r2_real, r2_ruido = [], []
    for p in pliegues:
        prueba = np.zeros(n2, dtype=bool)
        prueba[p] = True
        for Xm, destino in ((Xr, r2_real), (Xa, r2_ruido)):
            A = np.column_stack([np.ones((~prueba).sum()), Xm[~prueba]])
            b, *_ = np.linalg.lstsq(A, yr[~prueba], rcond=None)
            pred = np.column_stack([np.ones(prueba.sum()), Xm[prueba]]) @ b
            ss_res = ((yr[prueba] - pred) ** 2).sum()
            ss_tot = ((yr[prueba] - yr[prueba].mean()) ** 2).sum()
            destino.append(1 - ss_res / ss_tot)
    solo_real.append(np.mean(r2_real))
    con_ruido.append(np.mean(r2_ruido))
solo_real, con_ruido = np.array(solo_real), np.array(con_ruido)

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.3))

# Panel izquierdo
eje = ejes[0]
for j in range(d):
    ancho = 2.4 if j in (0, 3) else 1.2
    eje.plot(alphas, caminos[:, j], color=colores[j], linewidth=ancho, label=etiquetas[j])
eje.axhline(0, color=TEXTO, linewidth=0.8, alpha=0.4)
eje.set_title("Lasso: subir la penalización anula variables")
eje.set_xlabel("alpha (fuerza de la penalización)")
eje.set_ylabel("coeficiente")
eje.legend(ncol=2, fontsize=7.5, loc="upper right")
anotar(eje, "x2, x3, x5 y x6 caen a cero exacto:\nL1 no las deja pequenas, las expulsa",
       (1.15, 0.0), (0.30, 0.38), TEXTO)
rejilla(eje)
numeros(eje)

# Panel derecho
eje = ejes[1]
pos = [1, 2]
eje.bar(pos, [solo_real.mean(), con_ruido.mean()], width=0.5,
        color=[VERDE, ROJO], alpha=0.85)
for i, (p, vals) in enumerate(zip(pos, (solo_real, con_ruido))):
    eje.scatter(np.full(vals.size, p) + azar.uniform(-0.10, 0.10, vals.size), vals,
                color=TEXTO, s=14, alpha=0.65, zorder=5)
eje.axhline(0, color=TEXTO, linewidth=1.0)
eje.set_xticks(pos)
eje.set_xticklabels(["5 variables reales", "las 5 + 45 de ruido"])
eje.set_ylim(min(con_ruido.min() - 1.5, -4), max(solo_real.max() + 0.4, 1.0))
eje.set_title("Con 60 filas, 45 columnas de ruido hunden el R2")
eje.set_ylabel("R2 en validación cruzada")
eje.text(1.0, solo_real.mean() + 0.15, f"media {solo_real.mean():.2f}".replace(".", ","),
         color=VERDE, fontsize=9, ha="center")
eje.text(2.0, con_ruido.mean() - 0.35, f"media {con_ruido.mean():.2f}".replace(".", ","),
         color=ROJO, fontsize=9, ha="center", va="center")
anotar(eje, "por debajo de 0 el modelo predice\npeor que decir siempre la media",
       (2.0, con_ruido.mean()), (0.03, 0.10), ROJO)
rejilla(eje)
numeros(eje)

guardar(fig, "seleccion-de-features-lasso-y-ruido")
