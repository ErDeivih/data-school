# Una tarjeta con n ideas se acierta entera solo si se aciertan las n: P = p**n.
# Y como cada intento es independiente, los repasos hasta acertarla son 1/P.
p = 0.9
for n in (1, 2, 4, 8):
    print(f"{n} idea(s) en la tarjeta -> P = {p ** n:.3f}   repasos hasta acertar = {1 / p ** n:.2f}")
