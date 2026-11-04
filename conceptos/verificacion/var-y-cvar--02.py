import numpy as np

p = 0.04                                   # probabilidad de impago de cada bono
perdida = 100.0                            # EUR que se pierden si impaga

def var_cvar(perdidas, probs, cola=0.05):
    """VaR y CVaR coherente: media del peor `cola` de la distribucion."""
    orden = np.argsort(-perdidas)
    pe, pr = perdidas[orden], probs[orden]
    var = pe[np.searchsorted(np.cumsum(pr), cola)]   # umbral del peor 5 %
    resto, cvar = cola, 0.0
    for perdida_i, peso in zip(pe, pr):              # masa parcial en el escalon
        toma = min(peso, resto)
        cvar += toma * perdida_i
        resto -= toma
    return var, cvar / cola

un_bono = var_cvar(np.array([0.0, perdida]), np.array([1 - p, p]))
dos_bonos = var_cvar(np.array([0.0, perdida, 2 * perdida]),
                     np.array([(1 - p) ** 2, 2 * p * (1 - p), p ** 2]))

print(f"VaR  95%  un bono {un_bono[0]:6.0f}  los dos {dos_bonos[0]:6.0f}")
# -> VaR  95%  un bono      0  los dos    100
print(f"CVaR 95%  un bono {un_bono[1]:6.2f}  los dos {dos_bonos[1]:6.2f}")
# -> CVaR 95%  un bono  80.00  los dos 103.20
print(f"suma de VaR  {2 * un_bono[0]:.0f} < {dos_bonos[0]:.0f} conjunto")
# -> suma de VaR  0 < 100 conjunto
print(f"suma de CVaR {2 * un_bono[1]:.2f} >= {dos_bonos[1]:.2f} conjunto")
# -> suma de CVaR 160.00 >= 103.20 conjunto
