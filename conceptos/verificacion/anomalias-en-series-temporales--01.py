import numpy as np

# Serie con deriva, ciclo semanal y ruido; ocho anomalias encima (dias 41, 42, 43...)
azar = np.random.default_rng(9)
n = 300
t = np.arange(n)
y = 120 + 0.45 * t + 9.0 * np.sin(2 * np.pi * t / 7) + azar.normal(0.0, 2.6, n)
pos = np.array([41, 42, 43, 118, 171, 229, 230, 275])
y[pos] += np.array([22.0, 25.0, 21.0, -23.0, 19.0, -26.0, -21.0, 24.0])
real = np.zeros(n, dtype=bool)
real[pos] = True


def z_robusto(r, k, w=29):
    """Tipifica el residuo con mediana y MAD de una ventana centrada."""
    mad = np.empty(n)
    for i in range(n):
        a = max(0, i - w // 2)
        vecinos = np.delete(r[a:min(n, i + w // 2 + 1)], i - a)
        mad[i] = np.median(np.abs(vecinos - np.median(vecinos)))
    return np.abs(r - np.median(r)) / (1.4826 * mad + 1e-9) > k


d7 = np.zeros(n)
d7[7:] = y[7:] - y[:-7]                     # misma comparacion que el dia 7 anterior
marca = z_robusto(d7, k=4.0)
zeker = np.abs((y - y.mean()) / y.std()) > 4.0     # la regla ciega, para comparar

print("desviacion de la serie %.2f  desviacion del ruido %.2f" % (y.std(), 2.6))
# -> desviacion de la serie 39.48  desviacion del ruido 2.60
print("z global maximo %.2f  marcas %d" % (np.abs((y - y.mean()) / y.std()).max(), zeker.sum()))
# -> z global maximo 2.23  marcas 0
print("diferencia estacional: aciertos %d de %d  marcas totales %d"
      % (int((marca & real).sum()), int(real.sum()), int(marca.sum())))
# -> diferencia estacional: aciertos 7 de 8  marcas totales 15
print("dias marcados:", np.where(marca)[0].tolist())
# -> dias marcados: [41, 42, 48, 49, 50, 118, 125, 171, 178, 229, 230, 236, 237, 275, 282]
