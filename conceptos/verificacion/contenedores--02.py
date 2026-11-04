# Ocho servicios con la misma base: las capas compartidas se guardan una sola vez.
base_mb, capa_servicio_mb, servicios = 150, 250, 8

sin_dedup = servicios * (base_mb + capa_servicio_mb)      # suma de tamanos de imagen
con_dedup = base_mb + servicios * capa_servicio_mb        # lo que ocupa el disco de verdad

print("suma de tamanos de imagen:", sin_dedup, "MB")     # -> 3200 MB
print("bytes reales en disco:   ", con_dedup, "MB")      # -> 2150 MB
print(f"ahorro {100 * (1 - con_dedup / sin_dedup):.1f} %")   # -> 32.8 %
