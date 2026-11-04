# Postings comprimidos: diferencias entre identificadores consecutivos + varint.
def varint(n):
    """Entero no negativo en 7 bits por byte; el bit alto indica que hay continuacion."""
    salida = bytearray()
    while True:
        byte = n & 0x7F
        n >>= 7
        if n:
            salida.append(byte | 0x80)
        else:
            salida.append(byte)
            return bytes(salida)


postings = [1, 3, 4, 7, 11, 12, 800, 801]
deltas = [postings[0]] + [b - a for a, b in zip(postings, postings[1:])]
comprimido = b"".join(varint(d) for d in deltas)

print("postings:", postings)
print("deltas:", deltas)                                # -> [1, 2, 1, 3, 4, 1, 788, 1]
print("bytes sin comprimir (4 por doc):", 4 * len(postings))   # -> 32
print("bytes con delta + varint:", len(comprimido))            # -> 9
