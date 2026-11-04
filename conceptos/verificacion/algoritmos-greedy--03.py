def cambio_voraz(monedas, importe):
    """Coge siempre la moneda mayor que quepa. Con euros acierta; con {1,3,4} no."""
    usadas, resto = [], importe
    for m in sorted(monedas, reverse=True):
        while resto >= m:
            usadas.append(m); resto -= m
    return usadas, ([] if resto else usadas)

def cambio_optimo(monedas, importe):
    """Programacion dinamica: F(c) = 1 + min(F(c - m)) sobre las monedas que caben."""
    infinito = float("inf")
    F = [0] + [infinito] * importe
    for c in range(1, importe + 1):
        for m in monedas:
            if m <= c and F[c - m] + 1 < F[c]:
                F[c] = F[c - m] + 1
    return F[importe]

for monedas, importe in (([1, 2, 5, 10, 20], 47), ([1, 3, 4], 6)):
    usadas, _ = cambio_voraz(monedas, importe)
    print(monedas, importe, "-> voraz", len(usadas), "monedas", usadas,
          "optimo", cambio_optimo(monedas, importe))
# -> [1, 2, 5, 10, 20] 47 -> voraz 4 monedas [20, 20, 5, 2] optimo 4
# -> [1, 3, 4] 6 -> voraz 3 monedas [4, 1, 1] optimo 2
