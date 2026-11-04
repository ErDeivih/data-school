import numpy as np

rng = np.random.default_rng(0)
clases, n = 10, 256
y = rng.integers(0, clases, n)     # etiquetas al azar: no hay patron que aprender

def entropia_cruzada(logits):
    z = logits - logits.max(axis=1, keepdims=True)        # resta estable antes de exponenciar
    logp = z - np.log(np.exp(z).sum(axis=1, keepdims=True))
    return -logp[np.arange(n), y].mean()

print(f"ln(10) con logits casi nulos   {entropia_cruzada(np.zeros((n, clases))):.4f}")   # -> 2.3026
print(f"logits ~ N(0, 0.01)            {entropia_cruzada(rng.normal(0, .01, (n, clases))):.4f}")  # -> 2.3031
print(f"logits ~ N(0, 4.0)             {entropia_cruzada(rng.normal(0, 4.0, (n, clases))):.4f}")  # -> 6.5759
