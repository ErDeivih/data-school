import numpy as np

# Numeros de ejemplo (inventados) para la cuenta que hay que hacer al leer
# cualquier tabla de resultados con semillas.
propuesto = np.array([0.911, 0.918, 0.905, 0.915, 0.909])
baseline = np.array([0.906, 0.902, 0.911, 0.899, 0.908])

def error_tipico(a):
    return a.std(ddof=1) / np.sqrt(a.size)      # incertidumbre de la media

diferencia = propuesto.mean() - baseline.mean()
ee = np.sqrt(error_tipico(propuesto) ** 2 + error_tipico(baseline) ** 2)

print(f"medias       {propuesto.mean():.4f} vs {baseline.mean():.4f}")
print(f"diferencia   {diferencia:+.4f}")
print(f"en errores tipicos {diferencia / ee:.2f}")   # -> 2.05: prometedor, no concluyente
