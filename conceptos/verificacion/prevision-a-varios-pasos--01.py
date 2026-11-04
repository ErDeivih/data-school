import numpy as np

# Proceso autorregresivo estable: y_t = 0.5 + 0.6*y_{t-1} + ruido
azar = np.random.default_rng(4)
n = 260
y = np.empty(n)
y[0] = 10.0
for t in range(1, n):
    y[t] = 0.5 + 0.6 * y[t - 1] + azar.normal(0.0, 1.0)
ventana = y[:200][-60:]          # las 60 ultimas observaciones de entrenamiento
h = np.arange(1, 13)

i = np.arange(len(ventana) - 1)
A = np.column_stack([np.ones(len(i)), ventana[i]])
c, phi = np.linalg.lstsq(A, ventana[i + 1], rcond=None)[0]

# Recursiva: la prediccion vuelve a entrar como si fuera un dato observado
hist = [ventana[-1]]
recursiva = []
for _ in range(len(h)):
    v = c + phi * hist[-1]
    hist.append(v)
    recursiva.append(v)

# Directa: un modelo por horizonte, sin realimentar nada
directa = []
for k in h:
    j = np.arange(len(ventana) - k)
    Ak = np.column_stack([np.ones(len(j)), ventana[j]])
    ck = np.linalg.lstsq(Ak, ventana[j + k], rcond=None)[0]
    directa.append(ck[0] + ck[1] * ventana[-1])

media = c / (1 - phi)
print("c=%.4f phi=%.4f media implicita=%.3f" % (c, phi, media))
# -> c=0.8652 phi=0.3957 media implicita=1.432
print("recursiva h=1,2,12: %.3f %.3f %.3f" % (recursiva[0], recursiva[1], recursiva[11]))
# -> recursiva h=1,2,12: 1.909 1.620 1.432
print("formula cerrada h=1,2,12: %.3f %.3f %.3f"
      % (media + phi * (ventana[-1] - media), media + phi**2 * (ventana[-1] - media),
         media + phi**12 * (ventana[-1] - media)))
# -> formula cerrada h=1,2,12: 1.909 1.620 1.432
print("directa h=1,2,12: %.3f %.3f %.3f" % (directa[0], directa[1], directa[11]))
# -> directa h=1,2,12: 1.909 1.339 1.490
