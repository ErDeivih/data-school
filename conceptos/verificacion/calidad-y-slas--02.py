# Completitud por canal: el total puede cuadrar y el desglose no.
esperadas = {"web": 610_000, "app": 300_000, "marketplace": 110_000}
cargadas = {"web": 610_000, "app": 300_000, "marketplace": 74_000}

for canal in esperadas:
    print(canal, cargadas[canal], "de", esperadas[canal],
          f"{cargadas[canal] / esperadas[canal]:.1%}")
# -> web 610000 de 610000 100.0%
# -> app 300000 de 300000 100.0%
# -> marketplace 74000 de 110000 67.3%

total_cargado, total_esperado = sum(cargadas.values()), sum(esperadas.values())
print("total", total_cargado, "de", total_esperado, f"{total_cargado / total_esperado:.1%}")
# -> total 984000 de 1020000 96.5%
