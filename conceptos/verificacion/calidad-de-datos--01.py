# Cuatro dimensiones, cada una una proporcion sobre el total de filas.
id_ = [1, 2, 3, 4, 5, 5, 6, 7]
email = ["ana@x.com", "luis@x.com", None, "marta@x.com", "pau@x.com",
         "pau@x.com", "eva@x.com", "no-es-un-email"]
edad = [34, 41, 29, 150, 38, 38, 45, None]
provincia = ["Valencia", "Bilbao", "Valencia", "Bilbao", "Sevilla",
             "Sevilla", "Madrid", "Madrid"]
cp = ["46001", "48001", "46002", "48002", "41001", "41001", "28001", "99999"]
n = len(id_)

completitud = sum(1 for e in email if e is not None) / n
unicidad = 1 - (n - len(set(id_))) / n
validez = sum(1 for e in edad if e is not None and 0 <= e <= 120) / n

# Coherencia: el prefijo del codigo postal tiene que cuadrar con la provincia.
prefijo = {"Valencia": "46", "Bilbao": "48", "Sevilla": "41", "Madrid": "28"}
coherencia = sum(1 for p, c in zip(provincia, cp) if c[:2] == prefijo[p]) / n

print(f"filas {n}  completitud {completitud:.0%}  unicidad {unicidad:.0%}  "
      f"validez {validez:.0%}  coherencia {coherencia:.0%}")
# -> filas 8  completitud 88%  unicidad 88%  validez 75%  coherencia 88%
