import numpy as np

# Ingresos con cola larga: el z-score clasico se queda corto porque sigma esta inflada
rng = np.random.default_rng(0)
ingresos = rng.lognormal(mean=10.0, sigma=0.6, size=5000)
valor = 100_000.0

z_clasico = (valor - ingresos.mean()) / ingresos.std()
mad = np.median(np.abs(ingresos - np.median(ingresos)))
z_robusto = (valor - np.median(ingresos)) / (1.4826 * mad)

print("media   ", round(float(ingresos.mean())))        # -> 26254
print("sd      ", round(float(ingresos.std())))         # -> 16934
print("mediana ", round(float(np.median(ingresos))))    # -> 21664
print("MAD     ", round(float(mad)))                    # -> 8464
print("z clasico", round(float(z_clasico), 2))          # -> 4.35
print("z robusto", round(float(z_robusto), 2))          # -> 6.24
