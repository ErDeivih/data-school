# Dimensiones conformadas: la misma dim_tienda sirve para ventas y para devoluciones
PRODUCTO = {1: ("TEC-01", "teclado", "perifericos"), 2: ("RAT-02", "raton", "perifericos")}
TIENDA = {10: ("Centro", "Madrid"), 20: ("Norte", "Bilbao")}

VENTAS = [(1, 10, 59.90), (2, 10, 12.50), (1, 20, 89.85)]
DEVOLUCIONES = [(2, 10, 12.50), (2, 20, 9.99)]

def por_ciudad(filas):
    acumulado = {}
    for producto, tienda, importe in filas:
        ciudad = TIENDA[tienda][1]
        acumulado[ciudad] = round(acumulado.get(ciudad, 0) + importe, 2)
    return acumulado

ventas_ciudad = por_ciudad(VENTAS)
devoluciones_ciudad = por_ciudad(DEVOLUCIONES)

print("ventas por ciudad      :", ventas_ciudad)          # -> {'Madrid': 72.4, 'Bilbao': 89.85}
print("devoluciones por ciudad:", devoluciones_ciudad)    # -> {'Madrid': 12.5, 'Bilbao': 9.99}
print("tasa de devolucion     :", round(sum(devoluciones_ciudad.values())
                                         / sum(ventas_ciudad.values()), 4))   # -> 0.1386
