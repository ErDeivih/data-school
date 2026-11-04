import numpy as np

# Diez p-valores de diez metricas medidas sobre el mismo experimento.
p = np.array([0.001, 0.009, 0.011, 0.019, 0.031, 0.048, 0.120, 0.340, 0.510, 0.880])
m, alfa = p.size, 0.05

ordenados = np.sort(p)
umbral_bh = np.arange(1, m + 1) / m * alfa          # k * alfa / m
pasa = ordenados <= umbral_bh
k = int(np.max(np.where(pasa)[0]) + 1) if pasa.any() else 0

print(f"Bonferroni sobreviven {int((p <= alfa / m).sum())} con umbral {alfa / m:.4f}")
# -> Bonferroni sobreviven 1 con umbral 0.0050
print(f"BH sobreviven {k} con umbral {umbral_bh[k - 1]:.4f}")
# -> BH sobreviven 4 con umbral 0.0200
