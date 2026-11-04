# Cuanto cuesta en contexto el catalogo: la parte del protocolo que se paga en cada peticion.
import json

def tokens_aprox(objeto):
    # Regla de andar por casa: unos 4 caracteres por token en texto en ingles.
    return len(json.dumps(objeto, ensure_ascii=False)) / 4

def herramienta(nombre, campos):
    return {"name": nombre,
            "description": f"Consulta {nombre.replace('_', ' ')} en el sistema de pedidos",
            "inputSchema": {"type": "object",
                            "properties": {c: {"type": "string"} for c in campos},
                            "required": list(campos)}}

# Tres servidores realistas, con 2, 4 y 3 herramientas.
catalogo = ([herramienta("buscar_pedido", ["id_pedido"])] * 2
            + [herramienta(f"cliente_{i}", ["nombre", "pais"]) for i in range(4)]
            + [herramienta(f"factura_{i}", ["id_factura"]) for i in range(3)])
print("herramientas en el catalogo:", len(catalogo))
print("tokens del catalogo por peticion:", round(tokens_aprox(catalogo)))
# -> 9
# -> 476
# ojo: 476 tokens de prefijo por peticion, y el prefijo se repite en CADA llamada al modelo

# Con el catalogo como prefijo estable se paga a precio de cache la mayor parte.
P_ENTRADA, P_CACHE, PETICIONES_MES = 3.0, 0.30, 200_000
tokens_catalogo = tokens_aprox(catalogo)
sin_cache = tokens_catalogo * PETICIONES_MES * P_ENTRADA / 1e6
con_cache = tokens_catalogo * PETICIONES_MES * P_CACHE / 1e6
print(f"catalogo sin cache: {sin_cache:6.1f} EUR al mes")
print(f"catalogo con cache: {con_cache:6.1f} EUR al mes")
# -> catalogo sin cache:  285.9 EUR al mes
# -> catalogo con cache:   28.6 EUR al mes
# ojo: la diferencia es de diez veces, y solo por el orden del prefijo

# Y si se conectan treinta servidores "por si acaso", el catalogo crece con ellos.
for n_servidores in (3, 10, 30):
    grande = [h for i in range(n_servidores) for h in catalogo]
    print(f"{n_servidores:2d} servidores -> {len(grande):3d} herramientas y "
          f"{round(tokens_aprox(grande)):5d} tokens por peticion")
# ->  3 servidores ->  27 herramientas y  1430 tokens por peticion
# -> 10 servidores ->  90 herramientas y  4765 tokens por peticion
# -> 30 servidores -> 270 herramientas y 14295 tokens por peticion
