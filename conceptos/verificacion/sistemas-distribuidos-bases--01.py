# Si una peticion espera al mas lento de n servidores, la cola se multiplica con el abanico.
def afectadas(n):
    # 0.99 es la probabilidad de que UN servidor responda dentro de su tiempo; elevarlo a n
    # supone que los n son independientes. El complemento da "al menos uno lento".
    return 1 - 0.99 ** n

for n in (1, 10, 100, 1000):
    # :>5 reserva cinco caracteres alineados a la derecha: las columnas no bailan.
    print(f"abanico {n:>5} servidores -> {100 * afectadas(n):6.1f} % de peticiones afectadas")

print(f"con 100 servicios: {100 * afectadas(100):.1f} %")   # -> 63.4 %
