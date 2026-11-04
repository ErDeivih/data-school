# Cuanto se desperdicia mandando el objeto entero cuando solo hace falta un campo.
consulta_rest = {                  # /pedidos/42 trae todo, aunque solo quieras el total
    "id": 42, "fecha": "2026-01-05", "estado": "enviado", "total": 412.5,
    "cliente": {"id": 7, "nombre": "Ana", "email": "ana@ejemplo.com", "direccion": "Calle Mayor 3"},
    "lineas": [{"producto": "A", "cantidad": 2, "precio": 12.5},
               {"producto": "B", "cantidad": 1, "precio": 30.0}],
}

def tamano(objeto):
    if isinstance(objeto, dict):
        # suma recursiva de claves y valores; no cuenta llaves, comas ni dos puntos
        return sum(tamano(k) + tamano(v) for k, v in objeto.items())
    if isinstance(objeto, list):
        return sum(tamano(x) for x in objeto)     # en una lista no hay claves, solo valores
    return len(str(objeto))                       # una hoja se mide por su texto: 412.5 son 5

pedido_graphql = {"total": 412.5}   # la consulta pide exactamente un campo

print("tamano REST:", tamano(consulta_rest), "caracteres")      # -> 165 caracteres
print("tamano GraphQL:", tamano(pedido_graphql), "caracteres")  # -> 10 caracteres
print("sobra:", round(tamano(consulta_rest) / tamano(pedido_graphql), 1), "veces mas datos")
# la division con / siempre devuelve float; round lo deja en un decimal para leerlo
