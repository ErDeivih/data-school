# Mayoria y fallos tolerados: los numeros pares no aportan nada.
for n in range(1, 8):
    # // es la division entera: 5 // 2 da 2, no 2.5. Con / el resultado seria un float.
    mayoria = n // 2 + 1
    # (n - 1) // 2 fallos: son los que puede perder el lado mayoritario sin dejar de serlo.
    tolera = (n - 1) // 2
    print(f"N={n}  mayoria={mayoria}  fallos tolerados={tolera}")
