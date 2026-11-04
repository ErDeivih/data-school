import numpy as np

# El rango de la correccion esta acotado por r: comprobamos los valores singulares.
rng = np.random.default_rng(0)
d, k, r, alpha = 8, 8, 2, 16
A = rng.normal(size=(r, k))
B = rng.normal(size=(d, r))
delta = (alpha / r) * (B @ A)                 # la actualizacion que aprende LoRA
s = np.linalg.svd(delta, compute_uv=False)

print("valores singulares de delta W:", np.round(s, 4))
# -> valores singulares de delta W: [50.1984 26.6556  0.      0.      0.      0.      0.      0.    ]
print("valores singulares no nulos:", int((s > 1e-10).sum()), "de", d)
# -> valores singulares no nulos: 2 de 8
print(f"norma de Frobenius con alpha/r={alpha / r:.1f}: {np.linalg.norm(delta):.4f}")
# -> norma de Frobenius con alpha/r=8.0: 56.8366
