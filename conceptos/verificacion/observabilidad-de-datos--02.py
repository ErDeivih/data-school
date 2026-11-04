import pandas as pd

# Deriva de dominio: la columna 'pais' era estable y hoy llega distinta.
antes = pd.Series(["ES"] * 900 + ["PT"] * 80 + ["FR"] * 20)
hoy = pd.Series(["ES"] * 400 + ["PT"] * 50 + ["FR"] * 20 + ["??"] * 530)

print("categorias antes/hoy:", antes.nunique(), hoy.nunique())          # -> categorias antes/hoy: 3 4
print("proporcion ES antes/hoy:",
      f"{(antes == 'ES').mean():.1%}", f"{(hoy == 'ES').mean():.1%}")
# -> proporcion ES antes/hoy: 90.0% 40.0%
print("categoria nueva:", sorted(set(hoy) - set(antes)))                # -> categoria nueva: ['??']
