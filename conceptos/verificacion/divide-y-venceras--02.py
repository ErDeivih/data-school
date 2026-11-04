def karatsuba(x, y):
    """Multiplicacion de enteros por divide y venceras: 3 productos de n/2 cifras."""
    if x < 10 or y < 10:
        return x * y                      # caso base: una cifra
    n = max(len(str(x)), len(str(y)))
    mitad = n // 2
    potencia = 10 ** mitad
    a, b = divmod(x, potencia)
    c, d = divmod(y, potencia)
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    cruzado = karatsuba(a + b, c + d) - ac - bd     # aqui esta el ahorro: un producto menos
    return ac * potencia * potencia + cruzado * potencia + bd

print("1234 * 5678  =", karatsuba(1234, 5678))    # -> 1234 * 5678  = 7006652
print("coincide con *:", karatsuba(1234, 5678) == 1234 * 5678)   # -> coincide con *: True
print("987654 * 3210 =", karatsuba(987654, 3210))  # -> 987654 * 3210 = 3170369340
