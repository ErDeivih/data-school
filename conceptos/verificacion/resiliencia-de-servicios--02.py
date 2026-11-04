# Reintentar no es gratis: la carga que ve la dependencia crece con cada intento.
def intentos_esperados(p_exito, reintentos):
    """1 + (1-p) + (1-p)^2 + ... : los que fallan vuelven a intentarlo."""
    return sum((1 - p_exito) ** k for k in range(reintentos))

for p in (0.99, 0.9, 0.5, 0.2, 0.0):
    print("exito %.2f -> %.2f llamadas por peticion con 3 intentos"
          % (p, intentos_esperados(p, 3)))
# -> exito 0.90 -> 1.11 llamadas por peticion con 3 intentos
# -> exito 0.20 -> 2.44 llamadas por peticion con 3 intentos
# -> exito 0.00 -> 3.00 llamadas por peticion con 3 intentos

# Ley de Little: peticiones en vuelo = llegadas por segundo * tiempo de servicio.
LLEGADAS, POOL = 200, 50
for latencia in (0.05, 0.25, 0.5, 2.0):
    en_vuelo = LLEGADAS * latencia
    print("latencia %4.2f s -> %6.1f en vuelo (pool %d): %s"
          % (latencia, en_vuelo, POOL,
             "cabe" if en_vuelo <= POOL else "AGOTADO: se encolan y el timeout los mata"))
# -> latencia 0.25 s ->   50.0 en vuelo (pool 50): cabe
# -> latencia 2.00 s ->  400.0 en vuelo (pool 50): AGOTADO: se encolan y el timeout los mata
