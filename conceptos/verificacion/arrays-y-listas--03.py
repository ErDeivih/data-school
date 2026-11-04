# Insertar al principio contra anadir al final: el mismo numero de elementos, otro coste.
def desplazamientos_al_principio(n):
    total = 0
    for tam in range(n):          # insertamos n elementos, cada uno delante del anterior
        total += tam              # al insertar el numero tam hay que mover los tam previos
    return total

def desplazamientos_al_final(n):
    capacidad, tam, total = 1, 0, 0
    for _ in range(n):
        if tam == capacidad:      # se llena: se duplica y se copia lo que habia
            total += tam
            capacidad *= 2
        tam += 1
    return total

print("1000 al principio:", desplazamientos_al_principio(1000))          # -> 1000 al principio: 499500
print("100000 al principio:", desplazamientos_al_principio(100000))      # -> 100000 al principio: 4999950000
print("100000 al final:", desplazamientos_al_final(100000))              # -> 100000 al final: 131071
