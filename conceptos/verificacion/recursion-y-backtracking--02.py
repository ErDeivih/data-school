def resolver_n_reinas(n):
    """Devuelve todas las soluciones y cuantos nodos del arbol ha explorado."""
    soluciones, nodos = [], 0

    def viable(fila, col, colocadas):
        # Solo hay que comprobar contra las reinas ya puestas: misma columna o misma diagonal.
        for f, c in colocadas:
            if c == col or abs(f - fila) == abs(c - col):
                return False
        return True

    def explorar(fila, colocadas):
        nonlocal nodos
        nodos += 1
        if fila == n:
            soluciones.append(list(colocadas))
            return
        for col in range(n):
            if viable(fila, col, colocadas):     # poda antes de seguir
                colocadas.append((fila, col))
                explorar(fila + 1, colocadas)
                colocadas.pop()                  # deshacer: el paso clave del backtracking

    explorar(0, [])
    return soluciones, nodos

for n in (4, 6):
    soluciones, nodos = resolver_n_reinas(n)
    print(f"n={n}: soluciones={len(soluciones):>3}  nodos explorados={nodos:>6}  hojas sin poda={n**n}")
# -> n=4: soluciones=  2  nodos explorados=    17  hojas sin poda=256
# -> n=6: soluciones=  4  nodos explorados=   153  hojas sin poda=46656

tablero = resolver_n_reinas(6)[0][0]
for fila, col in tablero:
    print("." * col + "R" + "." * (6 - col - 1))
# -> .R....
# -> ...R..
# -> .....R
# -> R.....
# -> ..R...
# -> ....R.
