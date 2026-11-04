# Reconciliacion lote contra flujo: los totales cuadran, los dias no.
import numpy as np

rng = np.random.default_rng(0)
dias = 30
ocurridos = rng.poisson(33_333, size=dias)      # eventos que ocurrieron cada dia
tarde = rng.binomial(ocurridos, 0.004)          # 4 por mil llegan con retraso
tarde[-1] = 0        # los del ultimo dia todavia no han llegado al cerrar

flujo = ocurridos - tarde
flujo[1:] += tarde[:-1]                         # cada tardio se cuenta al dia siguiente

dif = np.abs(flujo - ocurridos)
print(f"total en lote  {ocurridos.sum():,}")
print(f"total en flujo {flujo.sum():,}")
print(f"dias con diferencia   {(dif > 0).sum()} de {dias}")
print(f"error relativo maximo {dif.max() / ocurridos.min():.2%}")
