# Por que construir un monticulo es O(n) y no O(n log n): contar comparaciones.
def sift_down(a, i, n, cont):
    while True:
        izq, der = 2 * i + 1, 2 * i + 2
        menor = i
        if izq < n:
            cont[0] += 1
            if a[izq] < a[menor]:
                menor = izq
        if der < n:
            cont[0] += 1
            if a[der] < a[menor]:
                menor = der
        if menor == i:
            return
        a[i], a[menor] = a[menor], a[i]
        i = menor

def construir_heap(valores):
    cont = [0]
    a = list(valores)
    for i in range(len(a) // 2 - 1, -1, -1):   # de abajo hacia arriba, solo nodos internos
        sift_down(a, i, len(a), cont)
    return cont[0]

def insertar_uno_a_uno(valores):
    h, cont = [], [0]
    for x in valores:
        h.append(x)
        i = len(h) - 1
        while i > 0:                            # sift-up: sube hasta que el padre es menor
            padre = (i - 1) // 2
            cont[0] += 1
            if h[padre] <= h[i]:
                break
            h[padre], h[i] = h[i], h[padre]
            i = padre
    return cont[0]

valores = list(range(1000, 0, -1))              # descendente: el peor caso para sift-up
print("n =", len(valores))                                        # -> n = 1000
print("comparaciones con build-heap:", construir_heap(valores))    # -> comparaciones con build-heap: 1982
print("comparaciones insertando uno a uno:", insertar_uno_a_uno(valores))  # -> comparaciones insertando uno a uno: 7987
