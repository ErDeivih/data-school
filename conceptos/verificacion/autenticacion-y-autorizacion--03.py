import hashlib
import time

sal = b"sal-aleatoria-por-usuario"
contrasena = b"correcta-caballo-bateria-grapadora"

inicio = time.perf_counter()          # reloj de pared con la mayor resolucion disponible
for _ in range(20_000):               # 20.000 vueltas para que sha256 sea medible
    hashlib.sha256(sal + contrasena).hexdigest()    # concatena sal y contrasena; devuelve texto hex
t_sha = time.perf_counter() - inicio  # segundos con decimales

inicio = time.perf_counter()
hashlib.scrypt(contrasena, salt=sal, n=2**14, r=8, p=1, dklen=32)
# n marca el coste (memoria y CPU) y dklen la longitud del hash; scrypt basta con un intento
t_scrypt = time.perf_counter() - inicio

print(f"sha256, 20000 intentos: {t_sha * 1000:7.1f} ms  ({t_sha / 20000 * 1000:.3f} ms por intento)")
# las dos cuentas son el mismo paso de segundos a milisegundos, una total y otra por intento
print(f"scrypt, 1 intento:      {t_scrypt * 1000:7.1f} ms  ({t_scrypt * 1000:.1f} ms por intento)")
print(f"un atacante prueba {t_scrypt / (t_sha / 20000):.0f} veces mas rapido con sha256")
# el cociente entre lo que cuesta un intento lento y uno rapido: esa es toda la defensa
