# Comprobacion minima de compatibilidad hacia atras: el lector NUEVO lee datos VIEJOS
def compatible(viejo, nuevo):
    # None en el valor significa que el campo lleva valor por defecto
    quitados = [c for c in viejo if c not in nuevo]
    anadidos = [c for c in nuevo if c not in viejo]
    return len(quitados) == 0 and all(nuevo[c] is None for c in anadidos)

v1 = {"pedido_id": "str", "importe": "double"}
v2 = {"pedido_id": "str", "importe": "double", "moneda": "str"}
v3 = {"pedido_id": "str", "importe": "double", "moneda": None}
v4 = {"pedido_id": "str"}

print(f"v1 a v2 {compatible(v1, v2)}")   # -> v1 a v2 False
print(f"v1 a v3 {compatible(v1, v3)}")   # -> v1 a v3 True
print(f"v1 a v4 {compatible(v1, v4)}")   # -> v1 a v4 False