import numpy as np

# Con cuantos datos se estima cada parametro: tres anos de retornos mensuales.
sigma_anual, mu_anual, meses = 0.15, 0.08, 36
sigma_mes = sigma_anual / np.sqrt(12)

# La media se anualiza sumando 12 meses; la volatilidad, multiplicando por sqrt(12).
error_media = 12 * sigma_mes / np.sqrt(meses)
error_vol = sigma_anual / np.sqrt(2 * meses)

print(f"error tipico de la media {error_media:.2%} sobre una media de {mu_anual:.0%}")
# -> error tipico de la media 8.66% sobre una media de 8%
print(f"error tipico de la volatilidad {error_vol:.2%} sobre {sigma_anual:.0%}")
# -> error tipico de la volatilidad 1.77% sobre 15%
print(f"error relativo de la media {error_media / mu_anual:.0%}")          # -> 108%
print(f"error relativo de la volatilidad {error_vol / sigma_anual:.0%}")  # -> 12%
