import pandas as pd

# Simulacion con la verdad conocida, para poder medir el sesgo
completo = pd.Series([1800, 1900, 2000, 2100, 2200, 2400, 2500, 2600, 9000, 12000], dtype=float)
observado = completo.mask(completo.index >= 8)      # los dos que mas ganan no responden

print(f"media real                {completo.mean():.1f}")   # -> 3850.0
print(f"media de casos completos  {observado.mean():.1f}")  # -> 2187.5
print(f"desv real                 {completo.std(ddof=0):.1f}")  # -> 3400.7
print(f"desv imputando la media   {observado.fillna(observado.mean()).std(ddof=0):.1f}")  # -> 242.6
print(f"nulos                     {int(observado.isna().sum())}")  # -> 2
