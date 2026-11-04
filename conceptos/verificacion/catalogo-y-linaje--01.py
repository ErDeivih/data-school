# Linaje a nivel de tabla: cada nodo apunta a los que se construyen a partir de el.
linaje = {
    "raw_clientes": ["stg_clientes"],
    "stg_clientes": ["dim_cliente", "int_pedidos"],
    "raw_pedidos":  ["int_pedidos"],
    "int_pedidos":  ["fact_ventas"],
    "dim_cliente":  ["fact_ventas"],
    "fact_ventas":  ["informe_margen"],
}

def recorrer(inicio, grafo):
    """Nodos alcanzables desde 'inicio', sin repetir. Es el impacto o el origen."""
    vistos, pila = set(), [inicio]
    while pila:
        nodo = pila.pop()
        for siguiente in grafo.get(nodo, []):
            if siguiente not in vistos:
                vistos.add(siguiente)
                pila.append(siguiente)
    return vistos

# Hacia abajo: que se rompe si cambio raw_clientes.
print("impacto:", sorted(recorrer("raw_clientes", linaje)))
# -> impacto: ['dim_cliente', 'fact_ventas', 'informe_margen', 'int_pedidos', 'stg_clientes']
print("nodos afectados:", len(recorrer("raw_clientes", linaje)))   # -> nodos afectados: 5

# Hacia arriba: de donde sale el informe. Se recorre el grafo con las aristas invertidas.
inverso = {}
for origen, destinos in linaje.items():
    for destino in destinos:
        inverso.setdefault(destino, []).append(origen)
print("origenes:", sorted(recorrer("informe_margen", inverso)))
# -> origenes: ['dim_cliente', 'fact_ventas', 'int_pedidos', 'raw_clientes', 'raw_pedidos', 'stg_clientes']
