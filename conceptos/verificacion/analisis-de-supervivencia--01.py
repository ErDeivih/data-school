import numpy as np

# Tiempo observado en meses y si el evento ocurrio (1) o la observacion se censuro (0)
tiempo = np.array([1, 2, 3, 3, 5, 6, 7, 8, 10, 12, 4, 9, 11, 13, 15], dtype=float)
evento = np.array([1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0])

# Kaplan-Meier: en cada tiempo con evento, S se multiplica por (1 - d/n)
S, pasos = 1.0, []
for t in np.unique(tiempo[evento == 1]):
    en_riesgo = int((tiempo >= t).sum())                 # siguen en observacion en t
    casos = int(((tiempo == t) & (evento == 1)).sum())   # eventos en t
    S *= 1 - casos / en_riesgo
    pasos.append((t, en_riesgo, casos, S))

print("  ".join("t=%.0f n=%d d=%d S=%.4f" % p for p in pasos))
# -> t=1 n=15 d=1 S=0.9333  t=2 n=14 d=1 S=0.8667  t=3 n=13 d=1 S=0.8000  t=5 n=10 d=1 S=0.7200  t=6 n=9 d=1 S=0.6400  t=7 n=8 d=1 S=0.5600  t=10 n=5 d=1 S=0.4480  t=12 n=3 d=1 S=0.2987
print("supervivencia al final %.4f" % S)                     # -> supervivencia al final 0.2987
print("1 - eventos/total %.4f" % (1 - evento.sum() / evento.size))   # -> 1 - eventos/total 0.4667
print("mediana %.0f" % next(t for t, _, _, s in pasos if s <= 0.5))  # -> mediana 10
