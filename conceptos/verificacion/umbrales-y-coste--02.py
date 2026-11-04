import numpy as np

# Con probabilidades calibradas el minimo teorico es c_fp / (c_fp + c_fn).
# Lo comprobamos generando las etiquetas a partir de la propia probabilidad.
rng = np.random.default_rng(7)
p = np.linspace(0.0, 1.0, 2001)
# Cada caso sale positivo con probabilidad p: ese es el modelo perfectamente calibrado.
# .astype(float) deja las etiquetas en 0.0 y 1.0 para que las comparaciones sean numericas.
y = (rng.random(p.size) < p).astype(float)

c_fp, c_fn = 3.0, 200.0
umbrales = np.linspace(0.0, 0.60, 121)
costes = []
for t in umbrales:
    pred = p >= t
    fp = int((pred & (y == 0)).sum())
    fn = int((~pred & (y == 1)).sum())      # ~pred es la mascara contraria, no `not pred`
    costes.append(c_fp * fp + c_fn * fn)

print(f"umbral teorico  {c_fp / (c_fp + c_fn):.4f}")               # -> 0.0148
# argmin da la POSICION del minimo: hay que indexar umbrales con ella para ver el valor.
print(f"umbral empirico {float(umbrales[int(np.argmin(costes))]):.4f}")  # -> 0.0150
print(f"coste minimo    {min(costes):.0f} EUR")                   # -> 2862 EUR
