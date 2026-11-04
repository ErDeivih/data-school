# Por que un solo caracter en un CSV cambia el objeto que guarda git:
# el identificador es el hash del CONTENIDO completo, no un diff.
import hashlib

def hash_fichero(contenido: str) -> str:
    return hashlib.sha256(contenido.encode("utf-8")).hexdigest()

a = "2024-01-05,1.50\n2024-01-06,2.00\n"
b = "2024-01-05,1.50\n2024-01-06,2.00\n"          # mismo contenido
c = "2024-01-05,1.50\n2024-01-06,2,00\n"          # una coma en vez de un punto

print("A y B iguales:", hash_fichero(a) == hash_fichero(b))
print("A y C iguales:", hash_fichero(a) == hash_fichero(c))
print("prefijo de A:", hash_fichero(a)[:12])
print("prefijo de C:", hash_fichero(c)[:12])
print("caracteres distintos:", sum(1 for x, y in zip(a, c) if x != y))
