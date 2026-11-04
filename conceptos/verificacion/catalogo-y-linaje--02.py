# Auditoria del catalogo: un listado sin dueno ni descripcion no responde a nada.
catalogo = [
    {"tabla": "fact_ventas", "dueno": "equipo-ventas", "descripcion": True,  "pii": False},
    {"tabla": "dim_cliente", "dueno": "equipo-crm",    "descripcion": True,  "pii": True},
    {"tabla": "tmp_extract", "dueno": None,            "descripcion": False, "pii": True},
    {"tabla": "int_pedidos", "dueno": "equipo-ventas", "descripcion": False, "pii": False},
]

print("sin dueno:", [t["tabla"] for t in catalogo if not t["dueno"]])
# -> sin dueno: ['tmp_extract']
print("sin descripcion:", [t["tabla"] for t in catalogo if not t["descripcion"]])
# -> sin descripcion: ['tmp_extract', 'int_pedidos']
print("con datos personales y sin dueno:", [t["tabla"] for t in catalogo if t["pii"] and not t["dueno"]])
# -> con datos personales y sin dueno: ['tmp_extract']
