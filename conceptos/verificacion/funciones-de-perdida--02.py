import numpy as np

# Focal: el factor (1 - p)^gamma apaga los ejemplos que ya se aciertan con holgura.
p_correcta = np.array([0.95, 0.60, 0.10])   # probabilidad de la clase verdadera
gamma = 2.0

bce = -np.log(p_correcta)
focal = (1 - p_correcta) ** gamma * bce

for p_i, b, f in zip(p_correcta, bce, focal):
    # zip recorre los tres arrays a la vez, en paralelo, y se para en el mas corto
    print(f"p={p_i:.2f}  BCE {b:.3f}  focal {f:.4f}")
# -> p=0.95  BCE 0.051  focal 0.0001
# -> p=0.60  BCE 0.511  focal 0.0817
# -> p=0.10  BCE 2.303  focal 1.8651
