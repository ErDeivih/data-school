import math

def bits(longitud, alfabeto):
    """Entropia de un secreto generado al azar: H = L * log2(A)."""
    return longitud * math.log2(alfabeto)      # log2: en bits, no en neperios ni en base 10

MINUSCULAS, ALFANUMERICO = 26, 62              # el alfabeto decide: 26 letras o 62 simbolos
for n in (8, 16, 32, 64):
    # :>3 alinea a la derecha en 3 caracteres, para que la tabla salga recta
    print(f"{n:>3} caracteres  minusculas {bits(n, MINUSCULAS):6.1f} bits"
          f"   alfanumerico {bits(n, ALFANUMERICO):6.1f} bits")

print(f"un token de 32 caracteres alfanumericos: {bits(32, ALFANUMERICO):.1f} bits")   # -> 190.5 bits

espacio = MINUSCULAS ** 8                      # 2^H combinaciones posibles
print("combinaciones de 8 minusculas:", espacio)                                    # -> 208827064576
# El tiempo medio es la mitad del espacio entre los intentos por segundo (2^H / (2 r)).
print(f"a mil millones de intentos por segundo: {espacio / 1e9:.0f} s")             # -> 209 s
