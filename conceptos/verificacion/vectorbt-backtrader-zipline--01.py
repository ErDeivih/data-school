import numpy as np

precios = np.array([100, 102, 99, 103, 101, 105, 107, 104, 108, 110], dtype=float)
ret = np.diff(precios) / precios[:-1]
ventanas = (2, 3, 4)
acum = np.concatenate([[0.0], np.cumsum(precios)])


def media_movil(w):
    """Media simple de las w barras anteriores; NaN en las primeras w-1."""
    mm = np.full(precios.size, np.nan)
    mm[w - 1:] = (acum[w:] - acum[:-w]) / w
    return mm


def backtest(w):
    senal = (precios > media_movil(w)).astype(float)   # NaN compara False -> 0
    posicion = senal[:-1]        # el retorno de i a i+1 se cobra con lo decidido en i
    return float((posicion * ret).sum())


bucle = np.array([backtest(w) for w in ventanas])

# Lo mismo en una sola operacion, con una matriz (variante x barra): el barrido vectorizado.
mm = np.vstack([media_movil(w) for w in ventanas])
senal = (precios[None, :] > mm).astype(float)
posicion = senal[:, :-1]
matriz = (posicion * ret).sum(axis=1)

print("ventanas            ", list(ventanas))                 # -> [2, 3, 4]
print("una a una (bucle)   ", np.round(bucle, 4).tolist())    # -> [-0.0393, -0.0099, -0.0099]
print("de golpe (matriz)   ", np.round(matriz, 4).tolist())   # -> [-0.0393, -0.0099, -0.0099]
print("coinciden           ", bool(np.allclose(bucle, matriz)))  # -> True
