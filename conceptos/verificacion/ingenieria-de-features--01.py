import pandas as pd

# Ventas diarias: la ventana de 3 dias debe mirar solo al pasado.
ventas = pd.Series([100, 120, 90, 140, 160, 130, 110], dtype=float)

sin_shift = ventas.rolling(3).mean()           # incluye el dia actual: no sirve como variable
con_shift = ventas.shift(1).rolling(3).mean()  # solo los 3 dias anteriores

print(f"dia 5: ventas {ventas[4]:.0f}, media sin shift {sin_shift[4]:.1f}, "
      f"con shift {con_shift[4]:.1f}")
# -> dia 5: ventas 160, media sin shift 130.0, con shift 116.7
