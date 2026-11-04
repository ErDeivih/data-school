import numpy as np

# Por que aparece el colapso de modos: la KL no es simetrica.
x = np.linspace(-8, 8, 4001)
dx = x[1] - x[0]        # paso de la rejilla: la integral de Riemann es una suma por dx


def normal(x, mu, s):
    return np.exp(-0.5 * ((x - mu) / s) ** 2) / (s * np.sqrt(2 * np.pi))


p_d = 0.5 * normal(x, -2, 0.5) + 0.5 * normal(x, 2, 0.5)   # datos bimodales
p_d = p_d / (p_d.sum() * dx)      # se renormaliza: la suma de la rejilla no da 1 exacto

candidatos = {"un solo modo": normal(x, -2, 0.5), "ancha y centrada": normal(x, 0.0, 1.6)}
for nombre, p_g in candidatos.items():
    p_g = p_g / (p_g.sum() * dx)      # normalizamos para que integre 1
    kl_pg_pd = np.sum(p_g * np.log(p_g / np.maximum(p_d, 1e-12))) * dx
    # np.maximum(y, 1e-12) evita el log(0) cuando una densidad es practicamente nula;
    # sin esa proteccion saldria -inf o nan y la comparacion no diria nada.
    kl_pd_pg = np.sum(p_d * np.log(np.maximum(p_d, 1e-12) / np.maximum(p_g, 1e-12))) * dx
    print(f"{nombre:>16}  KL(p_g||p_d)={kl_pg_pd:6.3f}  KL(p_d||p_g)={kl_pd_pg:8.3f}")
# ->     un solo modo  KL(p_g||p_d)= 0.693  KL(p_d||p_g)=  12.175
# -> ancha y centrada  KL(p_g||p_d)= 1.909  KL(p_d||p_g)=   0.800
