import numpy as np

# Barras de tiempo frente a barras de volumen: la misma serie, dos criterios.
rng = np.random.default_rng(0)
precios = 100 + np.cumsum(rng.normal(0, 0.05, size=600))
volumen = rng.integers(10, 200, size=600).tolist()

def barras_por_tiempo(p, tam):
    return p[::tam]

def barras_por_volumen(p, v, objetivo):
    cierres, acumulado = [], 0
    for i, precio in enumerate(p):
        acumulado += v[i]
        if acumulado >= objetivo:            # se cierra la barra y se reinicia el contador
            cierres.append(precio)
            acumulado = 0
    return np.array(cierres)

por_tiempo = np.diff(barras_por_tiempo(precios, 20).astype(float))
por_volumen = np.diff(barras_por_volumen(precios.tolist(), volumen, 1000))

print("barras por tiempo :", por_tiempo.size)                # -> 29
print("barras por volumen:", por_volumen.size)               # -> 59
print("desv. por tiempo  :", round(por_tiempo.std(ddof=1), 4))     # -> 0.2245
print("desv. por volumen :", round(por_volumen.std(ddof=1), 4))    # -> 0.1475
