import heapq

# heapq mantiene un MIN-heap: el menor siempre en la posicion 0.
datos = [50, 30, 70, 20, 40, 60, 80]
heapq.heapify(datos)                     # O(n): reordena in situ, sin crear otra lista
print("heap tras heapify:", datos)        # -> heap tras heapify: [20, 30, 60, 50, 40, 70, 80]
print("minimo:", datos[0])                # -> minimo: 20
print("no esta ordenado:", datos[1:])     # -> no esta ordenado: [30, 60, 50, 40, 70, 80]

print("los tres menores, extraidos uno a uno:", [heapq.heappop(datos) for _ in range(3)])  # -> los tres menores, extraidos uno a uno: [20, 30, 40]
print("lo que queda:", datos)             # -> lo que queda: [50, 70, 60, 80]
