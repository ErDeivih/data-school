# Como codifica protobuf un entero: tag en los bits bajos, varint para el valor.
def varint(n):
    bytes_salida = []
    while True:
        byte = n & 0x7F            # los 7 bits bajos del numero
        n >>= 7                    # el resto se desplaza: sera el byte siguiente del varint
        bytes_salida.append(byte | (0x80 if n else 0))   # 0x80 = "hay mas bytes"; el ultimo va sin el
        if not n:
            return bytes_salida    # devuelve una lista de enteros, no bytes

for campo, valor in [(1, 42), (2, 40000), (3, 9000000)]:
    tag = (campo << 3)              # 3 bits de tipo (0 = varint) + n. de campo
    codificado = varint(tag) + varint(valor)    # concatenar listas: primero el tag, luego el valor
    print(f"campo {campo} valor {valor:>7} -> {len(codificado)} bytes: {codificado}")
print("el mismo numero en JSON ocupa tambien el nombre del campo y las comillas")
