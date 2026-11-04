import numpy as np

datos = np.array([-1.0, 0.0, 1.0, 4.0, 5.0, 6.0])   # dos grupos evidentes
mu = np.array([0.0, 4.0])                            # arranque: dos centros distintos
var = np.array([1.0, 1.0])
pi = np.array([0.5, 0.5])

# Densidad normal escrita a mano (no hace falta scipy): una fila por componente y
# una columna por observacion. Ya lleva multiplicado el peso pi[k].
def densidades(datos, mu, var, pi):
    return np.array([pi[k] * np.exp(-(datos - mu[k]) ** 2 / (2 * var[k]))
                     / np.sqrt(2 * np.pi * var[k]) for k in range(2)])

for _ in range(50):
    # Paso E: responsabilidad de cada componente en cada punto.
    r = densidades(datos, mu, var, pi)
    # axis=0 suma sobre las componentes: en cada punto las responsabilidades suman 1.
    r = r / r.sum(axis=0)
    # Paso M: con esas responsabilidades, reestimar pesos, medias y varianzas.
    nk = r.sum(axis=1)                 # peso total de cada componente
    pi = nk / datos.size
    mu = (r * datos).sum(axis=1) / nk
    # mu[:, None] pasa mu de (2,) a (2,1) para poder restarlo a los 6 datos.
    # La division es entre nk (suma de responsabilidades), no entre el numero de puntos.
    var = (r * (datos - mu[:, None]) ** 2).sum(axis=1) / nk

ll = np.log(densidades(datos, mu, var, pi).sum(axis=0)).sum()
print("medias:", np.round(mu, 4).tolist())        # -> [0.0, 5.0]
print("varianzas:", np.round(var, 4).tolist())    # -> [0.6667, 0.6667]
print("pesos:", np.round(pi, 4).tolist())         # -> [0.5, 0.5]
print("log-verosimilitud:", round(float(ll), 3))  # -> -11.456
