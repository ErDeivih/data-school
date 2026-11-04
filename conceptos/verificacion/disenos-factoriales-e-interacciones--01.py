import numpy as np

# Las 12 observaciones del ejemplo: 4 celdas, 3 lotes cada una.
celdas = {("baja", "antiguo"): [52, 54, 50], ("baja", "nuevo"): [60, 62, 58],
          ("alta", "antiguo"): [58, 60, 56], ("alta", "nuevo"): [51, 53, 49]}
y = np.concatenate([np.array(v, dtype=float) for v in celdas.values()])
medias = {k: float(np.mean(v)) for k, v in celdas.items()}
general = y.mean()

ef_temp = np.mean([medias[("alta", "antiguo")], medias[("alta", "nuevo")]]) - \
          np.mean([medias[("baja", "antiguo")], medias[("baja", "nuevo")]])
ef_cat = np.mean([medias[("baja", "nuevo")], medias[("alta", "nuevo")]]) - \
         np.mean([medias[("baja", "antiguo")], medias[("alta", "antiguo")]])
inter = (medias[("alta", "antiguo")] - medias[("baja", "antiguo")]) - \
        (medias[("alta", "nuevo")] - medias[("baja", "nuevo")])

print(f"media general {general:.2f}  efecto temperatura {ef_temp:+.1f}  efecto catalizador {ef_cat:+.1f}")
# -> media general 55.25  efecto temperatura -1.5  efecto catalizador +0.5
print(f"interaccion (diferencia de diferencias) {inter:+.1f}")
# -> interaccion (diferencia de diferencias) +15.0
print(f"efecto de la temperatura con catalizador antiguo "
      f"{medias[('alta', 'antiguo')] - medias[('baja', 'antiguo')]:+.1f}  "
      f"con el nuevo {medias[('alta', 'nuevo')] - medias[('baja', 'nuevo')]:+.1f}")
# -> efecto de la temperatura con catalizador antiguo +6.0  con el nuevo -9.0
