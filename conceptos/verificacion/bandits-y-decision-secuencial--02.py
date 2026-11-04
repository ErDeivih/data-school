import numpy as np

# Tres brazos. Thompson no necesita arranque: empieza creyendo que todos valen 0,5.
medias = np.array([0.30, 0.60, 0.45])
rng = np.random.default_rng(7)
alfa, beta = np.ones(3), np.ones(3)     # prior Beta(1, 1): no sabe nada de ninguno
n = np.zeros(3)

for _ in range(2000):
    i = int(np.argmax(rng.beta(alfa, beta)))   # sortea una media de cada brazo y actua
    premio = 1.0 if rng.random() < medias[i] else 0.0
    alfa[i] += premio                          # acierto: la creencia sube
    beta[i] += 1.0 - premio                    # fallo: la creencia baja
    n[i] += 1

print("tiradas por brazo", n.astype(int))                    # -> [   8 1883  109]
print("media que cree   ", np.round(alfa / (alfa + beta), 2))  # -> [0.1  0.6  0.47]
print("confianza alfa+beta", (alfa + beta).astype(int))        # -> [  10 1885  111]
