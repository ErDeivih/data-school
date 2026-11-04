import numpy as np

# Valle estrecho: curvatura 1 en x y 100 en y. Para SGD, el factor de contraccion
# en y es (1 - 100*eta), asi que el limite de estabilidad es eta < 0.02.
def valle(eta, beta=None, pasos=20):
    q = np.array([1.0, 1.0])
    v = np.zeros(2)                      # velocidad del momento, del tamano de q
    for _ in range(pasos):
        g = np.array([q[0], 100.0 * q[1]])
        if beta is None:                 # SGD puro
            q = q - eta * g
        else:                            # momento: la velocidad acumula el gradiente
            v = beta * v + g
            q = q - eta * v
    return q

def adam(eta, pasos=20):
    q = np.array([1.0, 1.0]); m = np.zeros(2); v = np.zeros(2)
    for t in range(1, pasos + 1):        # t empieza en 1: la correccion usa 0.9 ** t
        g = np.array([q[0], 100.0 * q[1]])
        m = 0.9 * m + 0.1 * g            # media del gradiente
        v = 0.999 * v + 0.001 * g ** 2   # media del gradiente al cuadrado
        q = q - eta * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8)
    return q

for nombre, q in [("sgd  eta=0.015", valle(0.015)),
                  ("sgd  eta=0.025", valle(0.025)),
                  ("mom  eta=0.015", valle(0.015, 0.9)),
                  ("adam eta=0.050", adam(0.05))]:
    perdida = 0.5 * (q[0] ** 2 + 100 * q[1] ** 2)
    # +.2e imprime con signo y en notacion cientifica: con .2f esta coordenada saldria 0.00
    print(f"{nombre}  x {q[0]:+.4f}  y {q[1]:+.2e}  perdida {perdida:.3e}")
# -> sgd  eta=0.015  x +0.7391  y +9.54e-07  perdida 2.732e-01
# -> sgd  eta=0.025  x +0.6027  y +3.33e+03  perdida 5.529e+08
# -> mom  eta=0.015  x -0.1247  y -3.91e-01  perdida 7.669e+00
# -> adam eta=0.050  x +0.1112  y +1.11e-01  perdida 6.247e-01
