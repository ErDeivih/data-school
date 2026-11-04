import numpy as np

# Meter el mismo valor en todos los huecos encoge la varianza: no aportan dispersion.
datos = np.array([10.0, 12.0, 14.0, 16.0, 18.0, np.nan, np.nan])
relleno = np.where(np.isnan(datos), np.nanmean(datos), datos)

# ddof=1 porque estimamos la media a partir de la propia muestra.
print(f"varianza de los completos {np.nanvar(datos, ddof=1):.2f}")  # -> 10.00
print(f"varianza tras imputar     {relleno.var(ddof=1):.2f}")      # -> 6.67
print(f"desviacion tras imputar   {relleno.std(ddof=1):.2f}")      # -> 2.58
