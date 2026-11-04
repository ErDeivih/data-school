import numpy as np

rng = np.random.default_rng(0)

# Verdadera varianza poblacional: 4. Se mira que estimador se acerca mas de media.
verdadera_var, repeticiones, tam = 4.0, 20000, 10
sesgados, insesgados = [], []
for _ in range(repeticiones):
    x = rng.normal(0, np.sqrt(verdadera_var), size=tam)
    sesgados.append(x.var())            # divide por n
    insesgados.append(x.var(ddof=1))    # divide por n-1

print(f"dividir por n    media {np.mean(sesgados):.3f}  error {np.mean(sesgados) - verdadera_var:+.3f}")
print(f"dividir por n-1  media {np.mean(insesgados):.3f}  error {np.mean(insesgados) - verdadera_var:+.3f}")

# La correccion de Bessel no sale de la nada: el sesgo exacto es -sigma^2 / n.
print(f"sesgo teorico    {-verdadera_var / tam:.3f}")
