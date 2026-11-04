import numpy as np

rng = np.random.default_rng(0)

# Tiempos de espera con un valor extremo: la media no es robusta, la mediana si
datos = np.array([12.0, 14.5, 13.2, 15.1, 12.8, 14.0, 13.7, 96.0])
print(f"media    {datos.mean():.1f}")            # -> 23.9
print(f"mediana  {np.median(datos):.1f}")        # -> 13.8

# Bootstrap: remuestreamos con reemplazo 4000 veces para ver la incertidumbre
remuestras = rng.choice(datos, size=(4000, datos.size), replace=True)
medianas = np.median(remuestras, axis=1)

# El 96 aparece en dos tercios de las remuestras: es parte del problema, no un error
print(f"proporcion de remuestras con el 96    {(remuestras == 96.0).any(axis=1).mean():.2f}")  # -> 0.65
print(f"error tipico bootstrap de la mediana  {medianas.std(ddof=1):.2f}")  # -> 4.50
print(f"IC 95 % percentil  [{np.percentile(medianas, 2.5):.2f}, {np.percentile(medianas, 97.5):.2f}]")  # -> [12.80, 15.10]
