import numpy as np

# La misma estrategia con dos ventanas: el Calmar cambia porque la caida cambia.
r = np.array([0.05, 0.04, -0.12, -0.08, 0.06, 0.05, 0.03, 0.04, 0.02, 0.03, 0.04, 0.03,
              0.005, 0.01, -0.015, 0.005, 0.01, 0.005, 0.005, 0.00, 0.01, 0.005, 0.005, 0.005])


def calmar(x):
    capital = np.cumprod(1 + x)       # arranca en 1: es el factor de crecimiento
    picos = np.maximum.accumulate(capital)
    mdd = float(((picos - capital) / picos).max())
    anual = float(capital[-1] ** (12 / x.size) - 1)
    return anual, mdd, anual / mdd


for etiqueta, tramo in (("24 meses", r), ("ultimos 12", r[-12:])):
    anual, mdd, ratio = calmar(tramo)
    print(f"{etiqueta:<12} anual {anual:+.2%}  caida {mdd:.2%}  Calmar {ratio:.2f}")
# -> 24 meses     anual +11.65%  caida 19.04%  Calmar 0.61
# -> ultimos 12   anual +5.09%  caida 1.50%  Calmar 3.39
