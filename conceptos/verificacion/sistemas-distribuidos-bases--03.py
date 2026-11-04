import hashlib

def nodo_por_modulo(clave, n):
    # El reparto clasico: el nodo es el resto de dividir la clave. Cambia n y cambia casi todo.
    return clave % n

def anillo(nodos, replicas=100):
    """Cada nodo se representa con 100 puntos virtuales repartidos por el anillo."""
    puntos = []
    for nodo in nodos:
        for r in range(replicas):
            # El hash se calcula sobre el TEXTO "nodo#replica". [:8] se queda con los 8 primeros
            # caracteres hex (32 bits) y int(..., 16) los interpreta en base 16: un entero.
            h = int(hashlib.sha256(f"{nodo}#{r}".encode()).hexdigest()[:8], 16)
            puntos.append((h, nodo))
    # sorted() ordena por el hash y deja el anillo listo para buscar en el.
    return sorted(puntos)

def nodo_por_anillo(clave, puntos):
    # La clave se hashea igual que los nodos, para que ambos vivan en el mismo espacio.
    h = int(hashlib.sha256(str(clave).encode()).hexdigest()[:8], 16)
    for posicion, nodo in puntos:        # primer punto a la derecha de la clave
        if posicion >= h:
            return nodo
    return puntos[0][1]                  # la clave da la vuelta al anillo

claves = list(range(20_000))
# range(4) y range(5) son los nodos 0..3 y 0..4: el mismo clúster antes y despues de crecer.
puntos_4, puntos_5 = anillo(range(4)), anillo(range(5))

# sum() sobre un generador de booleanos cuenta los True: True vale 1 y False vale 0.
movidas_modulo = sum(nodo_por_modulo(k, 4) != nodo_por_modulo(k, 5) for k in claves)
movidas_anillo = sum(nodo_por_anillo(k, puntos_4) != nodo_por_anillo(k, puntos_5) for k in claves)

# El anillo se reconstruye entero al cambiar de nodos; en un sistema real solo se insertan
# los puntos del nodo nuevo, que es lo que hace barato el cambio.
print(f"hash modulo, de 4 a 5 nodos: {100 * movidas_modulo / len(claves):.0f} % de claves movidas")   # -> 80 %
print(f"anillo consistente:          {100 * movidas_anillo / len(claves):.0f} % de claves movidas")   # -> 20 %
