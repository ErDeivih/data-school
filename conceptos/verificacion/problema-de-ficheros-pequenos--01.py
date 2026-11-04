# Coste de metadatos: cuántas aperturas necesita una tabla con un tamano de fichero dado
total_mb = 100_000 * 10 / 1024          # 100.000 ficheros de 10 KB
objetivo_mb = 128

print(f"tamano total {total_mb / 1024:.2f} GB")                      # -> tamano total 0.95 GB
print(f"ficheros objetivo {total_mb / objetivo_mb:.0f}")             # -> ficheros objetivo 8
print(f"amplificacion {100_000 / (total_mb / objetivo_mb):.0f}")     # -> amplificacion 13107
print(f"bytes por fichero {10 * 1024}")                              # -> bytes por fichero 10240