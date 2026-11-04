import numpy as np

rng = np.random.default_rng(0)
centros = rng.normal(0, 1, size=(8, 32))
# Ruido alto a proposito: los grupos se solapan y la frontera del IVF se nota.
base = np.vstack([c + rng.normal(0, 2.0, size=(75, 32)) for c in centros])
base /= np.linalg.norm(base, axis=1, keepdims=True)

def dist2(X, Y):
    """Distancias al cuadrado de todos los pares, sin bucles: (n, m)."""
    # ||x||^2 + ||y||^2 - 2·x·y: la identidad que evita restar matrices de formas distintas
    return (X ** 2).sum(1)[:, None] + (Y ** 2).sum(1)[None, :] - 2 * X @ Y.T

def kmeans(X, k, semilla=0, iteraciones=50):
    """k-means basico: devuelve los k centroides, sin devolver la asignacion."""
    r = np.random.default_rng(semilla)
    # centros iniciales = k vectores reales elegidos al azar (sin reemplazo)
    C = X[r.choice(len(X), k, replace=False)].copy()
    for _ in range(iteraciones):
        # cada vector se asigna al centroide mas cercano (argmin devuelve el indice)
        etiquetas = np.argmin(dist2(X, C), axis=1)
        # .mean(0) promedia las filas del grupo; el if evita el nan de un grupo vacio
        C = np.array([X[etiquetas == j].mean(0) if np.any(etiquetas == j) else C[j]
                      for j in range(k)])
    return C

C = kmeans(base, 8)
asignacion = np.argmin(dist2(base, C), axis=1)          # a que grupo va cada vector

def exactos(q, k=10):
    """Los k indices verdaderamente mas cercanos: el barrido completo, sin indice."""
    return set(np.argsort(dist2(q[None, :], base)[0])[:k])

consultas = base[rng.choice(len(base), 30, replace=False)] + rng.normal(0, 0.1, (30, 32))
for nprobe in (1, 2, 4):
    aciertos = 0.0
    for q in consultas:
        # solo se comparan los centroides: elegir los nprobe grupos mas cercanos a la consulta
        cercanos = np.argsort(dist2(q[None, :], C)[0])[:nprobe]   # grupos a visitar
        # isin da una mascara; flatnonzero la convierte en los indices de esos vectores
        cand = np.flatnonzero(np.isin(asignacion, cercanos))
        d = dist2(base[cand], q[None, :])[:, 0]
        encontrados = set(cand[np.argsort(d)[:10]])
        # interseccion de conjuntos: cuantos de los 10 verdaderos recupero el IVF
        aciertos += len(encontrados & exactos(q, 10)) / 10
    print(f"nprobe={nprobe}  visitados {100 * nprobe // 8}%  recall@10 {aciertos / 30:.3f}")
