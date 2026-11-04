# La enye en dos codificaciones: mismo caracter, distinto numero de bytes
texto = "S" + "a" + "\u00f1" + "chez"

print("bytes de la enye:", texto.encode("utf-8")[2:4].hex())     # -> c3b1
print("longitud utf-8  :", len(texto.encode("utf-8")))          # -> 8
print("longitud latin1 :", len(texto.encode("latin-1")))        # -> 7

# Leer esos dos bytes como dos caracteres Latin-1 es el mojibake: U+00C3 y U+00B1
mal = texto.encode("utf-8").decode("latin-1")
print("caracteres distintos:", len(mal), "en vez de", len(texto))   # -> 8 en vez de 7
print("puntos de codigo:", " ".join(f"U+{ord(c):04X}" for c in mal))
