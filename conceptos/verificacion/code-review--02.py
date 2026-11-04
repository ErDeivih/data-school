# Medir el diff antes de pedir revision: un cambio enorme no se lee, se aprueba.
diffs = {"src/pagos.py": 320, "tests/test_pagos.py": 140, "CHANGELOG.md": 12}
LIMITE = 400                    # en mayusculas por convencion: es una constante, no un dato

total = sum(diffs.values())     # values(), no el diccionario: sumar las claves daria un error
for fichero, lineas in diffs.items():
    print(f"{fichero:<22} {lineas:>4} lineas")

print("lineas cambiadas:", total)                 # -> 472
print("dentro del limite:", total <= LIMITE)      # -> False
# max con key: compara por el valor (las lineas) y devuelve la clave (el nombre del fichero).
print("mayor bloque:", max(diffs, key=diffs.get)) # -> src/pagos.py
