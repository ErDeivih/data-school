# La logica de git bisect: busqueda binaria hasta el primer commit que rompio algo.
n_commits = 64
primer_malo = 41        # el bisect no conoce este dato: lo descubre probando

def esta_malo(commit):
    # Hace de suite de pruebas: dice si ese commit ya tiene el fallo.
    return commit >= primer_malo

izquierda, derecha = 0, n_commits - 1    # izquierda: se sabe bueno; derecha: se sabe malo
sondas = []
# Se para cuando quedan dos commits seguidos: el malo es el de la derecha.
while derecha - izquierda > 1:
    # // es division entera: trunca hacia abajo y siempre da un commit valido.
    medio = (izquierda + derecha) // 2
    sondas.append(medio)
    if esta_malo(medio):
        derecha = medio         # el fallo ya estaba: se descarta la mitad derecha
    else:
        izquierda = medio       # el fallo vino despues: se descarta la mitad izquierda

print("commits en el historial:", n_commits)           # -> 64
print("sondas realizadas:", len(sondas))               # -> 6
print("secuencia:", sondas)                            # -> [31, 47, 39, 43, 41, 40]
print("primer commit malo:", derecha)                  # -> 41
print("con busqueda lineal:", primer_malo + 1)         # -> 42
