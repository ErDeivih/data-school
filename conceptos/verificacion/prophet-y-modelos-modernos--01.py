import numpy as np

# Serie mensual sintetica: tendencia lineal + ciclo anual, los componentes de Prophet
rng = np.random.default_rng(3)
t = np.arange(48)
y = (100 + 0.8 * t + 6 * np.sin(2 * np.pi * t / 12)
     + 2 * np.cos(2 * np.pi * t / 12) + rng.normal(0, 1.5, 48))

# Base de Fourier de periodo 12 y orden 2: la estacionalidad tal como la escribe Prophet
def diseno(t, periodo=12, k=2):
    columnas = [np.ones_like(t, dtype=float), t.astype(float)]
    for j in range(1, k + 1):
        columnas += [np.sin(2 * np.pi * j * t / periodo),
                     np.cos(2 * np.pi * j * t / periodo)]
    return np.column_stack(columnas)

beta, *_ = np.linalg.lstsq(diseno(t), y, rcond=None)
ajuste = diseno(t) @ beta
pron = diseno(np.arange(48, 51)) @ beta

print("intercepto %.2f  pendiente %.3f" % (beta[0], beta[1]))   # -> intercepto 100.05  pendiente 0.798
print("coeficientes sin1 cos1 sin2 cos2 %.2f %.2f %.2f %.2f" % tuple(beta[2:]))
# -> coeficientes sin1 cos1 sin2 cos2 5.40 2.12 -0.39 -0.52
print("RMSE del modelo %.2f" % np.sqrt(np.mean((y - ajuste) ** 2)))            # -> RMSE del modelo 1.53
print("RMSE del naive estacional %.2f" % np.sqrt(np.mean((y[12:] - y[:-12]) ** 2)))
# -> RMSE del naive estacional 9.75
print("pronostico %.1f %.1f %.1f" % tuple(pron))                # -> pronostico 139.9 143.1 145.6
