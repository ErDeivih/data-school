import numpy as np

# Ley de potencia de juguete: L(N) = 2.5 * (N/1e9)^-0.05 + 1.6
# Los exponentes son de ejemplo; lo que se ve es la forma de la curva, no un resultado medido.
def perdida(n):
    return 2.5 * (n / 1e9) ** -0.05 + 1.6

for n in (1e8, 1e9, 1e10, 1e11):
    print(f"parametros {n:.0e}  perdida {perdida(n):.4f}")
# -> una linea por tamano; lo que importa es como se aplana la columna de perdidas

# Cuanto se gana al multiplicar por 10 los parametros en cada salto
for n in (1e8, 1e9, 1e10):
    print(f"{n:.0e} -> {10 * n:.0e}: baja {perdida(n) - perdida(10 * n):.4f}")
# -> los tres saltos bajan: 0.3050, 0.2719, 0.2423
