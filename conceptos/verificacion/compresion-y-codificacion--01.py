# 1.000.000 de filas con 20 ciudades distintas de 9 caracteres cada una
n = 1_000_000
ciudades = [f"ciudad_{i:02d}" for i in range(20)]

crudo = len(ciudades[0]) * n                    # cada fila guarda el texto completo
bits_indice = 5                                 # 2**5 = 32, suficiente para 20 valores
diccionario = sum(len(c) for c in ciudades) + n * bits_indice // 8

print("bytes sin codificar:", crudo)                                # -> bytes sin codificar: 9000000
print("bytes con diccionario:", diccionario)                        # -> bytes con diccionario: 625180
print("ratio de la codificacion:", round(crudo / diccionario, 1))   # -> ratio de la codificacion: 14.4
print("bits por valor:", round(8 * diccionario / n, 3))             # -> bits por valor: 5.001
