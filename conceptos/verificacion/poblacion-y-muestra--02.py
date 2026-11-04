import numpy as np

rng = np.random.default_rng(0)

# Sueldos por departamento: dentro de cada grupo son parecidos, pero los grupos
# tienen medias muy distintas. 6 tecnicos y 4 directivos.
tecnicos = np.array([1800.0, 1900, 1850, 1950, 1820, 1880])
directivos = np.array([4100.0, 4200, 4150, 4250])
poblacion = np.concatenate([tecnicos, directivos])
print(f"media poblacional      {poblacion.mean():.0f}")  # -> 2790

# Muestreo aleatorio simple: 5 personas de las 10 al azar
simple = np.array([rng.choice(poblacion, size=5, replace=False).mean()
                   for _ in range(2000)])

# Muestreo estratificado: 3 tecnicos y 2 directivos (la mitad de cada grupo)
estrat = np.array([0.6 * rng.choice(tecnicos, size=3, replace=False).mean()
                   + 0.4 * rng.choice(directivos, size=2, replace=False).mean()
                   for _ in range(2000)])

print(f"media del estratificado        {estrat.mean():.0f}")  # -> 2790
print(f"desviacion del muestreo simple {simple.std():.0f}")  # -> 376
print(f"desviacion del estratificado   {estrat.std():.0f}")  # -> 19
