# Los numeros son caros: miden poco y gastan muchos tokens.
texto = "El modelo cuesta 1.234,56 euros y pesa 7.000 millones de parametros."
# split() sin argumentos parte por cualquier espacio y agrupa los repetidos.
palabras, caracteres = texto.split(), len(texto)
print("palabras:", len(palabras))                                        # -> 11
print("caracteres:", caracteres)                                         # -> 68
print("caracteres por palabra:", round(caracteres / len(palabras), 2))   # -> 6.18
# El generador produce True y False; sum los cuenta como 1 y 0.
print("digitos:", sum(c.isdigit() for c in texto), "de", caracteres)     # -> 10 de 68

# La misma cantidad escrita de otra forma no ocupa lo mismo. len() cuenta CARACTERES, que
# no es lo que cuenta el tokenizador: el numero de tokens hay que medirlo con el.
print("1.234,56 ->", len("1.234,56"), "caracteres")   # -> 8 caracteres
print("1234.56  ->", len("1234.56"), "caracteres")    # -> 7 caracteres
