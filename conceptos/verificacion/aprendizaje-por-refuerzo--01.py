import numpy as np

medias = np.array([0.3, 0.5, 0.4])       # probabilidad real de exito de cada brazo
rng = np.random.default_rng(0)


def bandido(epsilon, pasos=2000):
    q = np.zeros(3)                      # valor estimado de cada brazo
    n = np.zeros(3)                      # veces que se ha tirado de cada brazo
    premio, optimo = 0.0, 0
    for _ in range(pasos):
        if rng.random() < epsilon:
            a = int(rng.integers(3))     # explorar
        else:
            a = int(np.argmax(q))        # explotar
        r = float(rng.random() < medias[a])
        n[a] += 1
        q[a] += (r - q[a]) / n[a]        # media incremental: no hace falta guardar todo
        premio += r
        optimo += int(a == 1)            # el brazo 1 es el mejor
    return premio / pasos, optimo / pasos


for eps in (0.0, 0.01, 0.1):
    media, opt = bandido(eps)
    print(f"epsilon={eps:<5} recompensa media={media:.3f}  elige el mejor brazo={opt:.1%}")
# -> epsilon=0.0   recompensa media=0.289  elige el mejor brazo=0.0%
# -> epsilon=0.01  recompensa media=0.417  elige el mejor brazo=59.0%
# -> epsilon=0.1   recompensa media=0.486  elige el mejor brazo=89.9%
