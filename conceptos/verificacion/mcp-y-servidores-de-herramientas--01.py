# Un servidor MCP de juguete: recibe peticiones JSON-RPC y responde. Lo que se ilustra es la
# forma de la conversacion, no el transporte: aqui las peticiones son un diccionario de Python.
import json

CAPACIDADES_SERVIDOR = {"tools": {}, "resources": {}}

# El catalogo se declara UNA vez. El anfitrion lo descubre con tools/list y a partir de ahi
# puede ofrecerselo a cualquier modelo: esa es toda la ventaja del protocolo.
HERRAMIENTAS = [
    {"name": "buscar_pedido", "description": "Devuelve un pedido por su identificador",
     "inputSchema": {"type": "object", "properties": {"id_pedido": {"type": "string"}},
                     "required": ["id_pedido"]}},
    {"name": "estado_pedido", "description": "Estado actual de un pedido",
     "inputSchema": {"type": "object", "properties": {"id_pedido": {"type": "string"}},
                     "required": ["id_pedido"]}},
]

PEDIDOS = {"A-4471": {"cliente": "ACME", "importe": 1240.50, "estado": "en transito"}}


def ejecutar(nombre, argumentos):
    # La validacion es del servidor, no del modelo: si el esquema no se cumple, no se ejecuta.
    if nombre not in {h["name"] for h in HERRAMIENTAS}:
        return None, {"code": -32601, "message": "metodo no encontrado"}
    if nombre == "buscar_pedido":
        pedido = PEDIDOS.get(argumentos.get("id_pedido"))
        if pedido is None:
            return None, {"code": -32000, "message": "pedido inexistente"}
        return pedido, None
    if nombre == "estado_pedido":
        pedido = PEDIDOS.get(argumentos.get("id_pedido"))
        if pedido is None:
            return None, {"code": -32000, "message": "pedido inexistente"}
        return {"estado": pedido["estado"]}, None
    return None, {"code": -32601, "message": "metodo no encontrado"}


def responder(peticion):
    metodo = peticion["method"]
    if metodo == "initialize":
        # El servidor contesta con SU version y SUS capacidades: la sesion empieza por un acuerdo.
        return {"result": {"protocolVersion": peticion["params"]["protocolVersion"],
                           "capabilities": CAPACIDADES_SERVIDOR}}
    if metodo == "tools/list":
        return {"result": {"tools": HERRAMIENTAS}}
    if metodo == "tools/call":
        params = peticion["params"]
        resultado, error = ejecutar(params["name"], params.get("arguments", {}))
        # El error viaja como DATO con codigo, no como excepcion del transporte.
        return {"result": {"content": [resultado]}} if error is None else {"error": error}
    return {"error": {"code": -32601, "message": "metodo no encontrado"}}


sesion = [
    {"id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
    {"id": 2, "method": "tools/list", "params": {}},
    {"id": 3, "method": "tools/call",
     "params": {"name": "buscar_pedido", "arguments": {"id_pedido": "A-4471"}}},
    {"id": 4, "method": "tools/call",
     "params": {"name": "buscar_pedido", "arguments": {"id_pedido": "B-0000"}}},
]

for peticion in sesion:
    respuesta = responder(peticion)
    cuerpo = json.dumps(respuesta["result"] if "result" in respuesta else respuesta["error"])
    if len(cuerpo) > 74:
        cuerpo = cuerpo[:71] + "..."
    print(f"id {peticion['id']}  {peticion['method']:14s} -> {cuerpo}")
# -> id 1  initialize     -> {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}, "resour...
# -> id 2  tools/list     -> {"tools": [{"name": "buscar_pedido", "description": "Devuelve un pedido...
# -> id 3  tools/call     -> {"content": [{"cliente": "ACME", "importe": 1240.5, "estado": "en trans...
# -> id 4  tools/call     -> {"code": -32000, "message": "pedido inexistente"}
