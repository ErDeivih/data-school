import numpy as np

rng = np.random.default_rng(7)
sigma, delta, reps = 8.0, 2.0, 20000

# Simulacion: la maquina esta descentrada 2 mm. Contamos cuantas veces el
# contraste con sigma conocida lo detecta, para n = 25 y para n = 126.
for n in (25, 126):
    medias = rng.normal(delta, sigma / np.sqrt(n), size=reps)
    z = medias / (sigma / np.sqrt(n))          # estadistico z con mu0 = 0
    detectado = np.mean(np.abs(z) > 1.96)
    print(f"n = {n:>3}  potencia simulada {detectado:.3f}")
# -> n =  25  potencia simulada 0.237
# -> n = 126  potencia simulada 0.801
