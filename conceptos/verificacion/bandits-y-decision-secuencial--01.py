import numpy as np

# Cinco variantes con una tasa de exito real distinta. El algoritmo no la conoce.
medias = np.array([0.30, 0.60, 0.45, 0.35, 0.50])
T = 2000


def simula(explora, rng):
    n = np.zeros(medias.size)
    suma = np.zeros(medias.size)                    # premios acumulados por brazo
    perdido = 0.0
    for t in range(T):
        if n.min() == 0:
            i = int(np.argmin(n))                   # todos los brazos necesitan un tiro
        elif explora:
            i = int(np.argmax(suma / n + np.sqrt(2 * np.log(t) / n)))   # indice UCB1
        else:
            i = int(np.argmax(suma / n))            # codicioso: solo la media observada
        premio = 1.0 if rng.random() < medias[i] else 0.0
        n[i] += 1
        suma[i] += premio
        perdido += medias.max() - medias[i]         # lo que habrias ganado con el mejor
    return perdido, n


perdido_ucb, tiradas = simula(True, np.random.default_rng(7))
perdido_cod, _ = simula(False, np.random.default_rng(7))
print(f"UCB1      pierde {perdido_ucb:>4.0f} premios   tiradas {tiradas.astype(int)}")
# -> UCB1      pierde  126 premios   tiradas [ 102 1204  308   72  314]
print(f"codicioso pierde {perdido_cod:>4.0f} premios")   # -> codicioso pierde  201 premios
