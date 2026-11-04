import numpy as np

# Ingresos de 9 personas: 3 sin declarar (NaN) y un valor extremo de 9.500.
ingresos = np.array([1200.0, 1350.0, 1500.0, 1600.0, 1800.0,
                     np.nan, np.nan, np.nan, 9500.0])

media, mediana = np.nanmean(ingresos), np.nanmedian(ingresos)
print(f"media de los que responden   {media:>7.0f}")    # -> 2825
print(f"mediana de los que responden {mediana:>7.0f}")  # -> 1550

# Rellenar por la media deja la media intacta pero inventa 3 ingresos altos.
relleno_media = np.where(np.isnan(ingresos), media, ingresos)
relleno_mediana = np.where(np.isnan(ingresos), mediana, ingresos)
print(f"media tras imputar con media   {relleno_media.mean():.0f}")    # -> 2825
print(f"media tras imputar con mediana {relleno_mediana.mean():.0f}")  # -> 2400
