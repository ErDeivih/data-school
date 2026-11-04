import numpy as np
from scipy import stats

rng = np.random.default_rng(0)

# Muestra de 20 alturas: media 166,7 y desviacion 6,62
muestra = np.array([160, 158, 171, 165, 175, 162, 168, 155, 180, 166,
                    164, 172, 159, 170, 167, 161, 173, 163, 169, 176], dtype=float)
print(f"media muestral  {muestra.mean():.1f}")   # -> 166.7
print(f"desv muestral   {muestra.std(ddof=1):.2f}")  # -> 6.62

# Repetimos el experimento 5000 veces: en cada uno cogemos 20 personas de una
# poblacion con media 170 y desviacion 8, y construimos el intervalo al 95 %.
media_real, desv_real, n, reps = 170.0, 8.0, 20, 5000
semiancho = stats.norm.ppf(0.975) * desv_real / np.sqrt(n)   # sigma conocida
cubren = 0
for _ in range(reps):
    x = rng.normal(media_real, desv_real, size=n)
    cubren += (x.mean() - semiancho <= media_real <= x.mean() + semiancho)

print(f"cobertura empirica {cubren / reps:.3f}")   # -> 0.948
print(f"anchura del intervalo {2 * semiancho:.2f}")  # -> 7.01
