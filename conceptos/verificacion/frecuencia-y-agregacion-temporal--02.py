import numpy as np
import pandas as pd

# --- Flujo frente a nivel ------------------------------------------------------
flujo = pd.Series([10.0, 20.0, 15.0])        # lo que pasa en cada hora
nivel = flujo.cumsum()                       # lo que marca el contador al cierre
print("flujo total %.0f   suma de las fotos del contador %.0f   ultimo nivel %.0f"
      % (flujo.sum(), nivel.sum(), nivel.iloc[-1]))
# -> flujo total 45   suma de las fotos del contador 85   ultimo nivel 45

# --- Media de medias sin ponderar ---------------------------------------------
febrero = np.full(28, 10.0)                  # 28 dias a 10 grados
marzo = np.full(8, 20.0)                     # solo 8 dias medidos en marzo
print("media de las medias %.3f   media ponderada %.3f"
      % ((febrero.mean() + marzo.mean()) / 2,
         np.concatenate([febrero, marzo]).mean()))
# -> media de las medias 15.000   media ponderada 12.222

# --- Promedio de ratios frente a ratio de totales -----------------------------
visitas = pd.Series([1000.0, 100.0])
compras = pd.Series([10.0, 20.0])
print("media de los ratios %.4f   ratio de los totales %.4f"
      % ((compras / visitas).mean(), compras.sum() / visitas.sum()))
# -> media de los ratios 0.1050   ratio de los totales 0.0273
