import hashlib

# Kafka garantiza el orden DENTRO de cada particion, no en el tema entero.
def particion(clave, n):
    # Kafka usa murmur2; aqui md5 solo para ilustrar una asignacion determinista.
    return int(hashlib.md5(clave.encode()).hexdigest(), 16) % n

N = 6
pedidos = [("A", 1), ("A", 2), ("B", 1), ("C", 1), ("D", 1), ("A", 3), ("B", 2), ("C", 2)]

por_particion = {}
for clave, numero in pedidos:
    por_particion.setdefault(particion(clave, N), []).append(f"{clave}{numero}")

for p in sorted(por_particion):
    print(f"particion {p}: {' '.join(por_particion[p])}")

# Todos los pedidos de un mismo cliente caen siempre en la misma particion.
particiones_de_a = {particion(c, N) for c, _ in pedidos if c == "A"}
print("particiones de la clave A:", len(particiones_de_a))   # -> particiones de la clave A: 1
print("particiones usadas:", len(por_particion))            # -> particiones usadas: 2
