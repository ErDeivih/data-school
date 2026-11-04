from numbers import Real

PASOS_MAX = 4

def sumar(a, b): return a + b
def multiplicar(a, b): return a * b
def dividir(a, b):
    # la herramienta decide lo que es un error de negocio y lo lanza como excepcion
    if b == 0: raise ValueError("division por cero")
    return a / b

ESQUEMAS = {
    "sumar": {"a": Real, "b": Real},
    "multiplicar": {"a": Real, "b": Real},
    "dividir": {"a": Real, "b": Real},
}
# el diccionario de funciones permite llamar por nombre, sin if/elif por herramienta
FUNCIONES = {"sumar": sumar, "multiplicar": multiplicar, "dividir": dividir}

def validar(nombre, argumentos):
    esquema = ESQUEMAS.get(nombre)
    if esquema is None: return False, "herramienta desconocida: " + str(nombre)
    # comparar los conjuntos de claves detecta a la vez el campo que falta y el que sobra
    if set(argumentos) != set(esquema): return False, "los argumentos no coinciden con el esquema"
    for clave, tipo in esquema.items():
        # bool es subclase de int: True pasaria como numero valido
        if not isinstance(argumentos[clave], tipo):
            return False, clave + " tiene un tipo que no toca"
    return True, argumentos

def ejecutar(nombre, argumentos):
    # se valida ANTES de tocar la funcion real: si falla, no hay efecto ninguno
    ok, aviso = validar(nombre, argumentos)
    if not ok: return None, aviso                    # nunca se llama a la funcion real
    try:
        # **argumentos reparte el diccionario como argumentos con nombre
        return FUNCIONES[nombre](**argumentos), "ok"
    except ValueError as error:
        # el error de la herramienta vuelve al modelo como texto, no rompe el bucle
        return None, "error de la herramienta: " + str(error)

def bucle_agente(politica):
    observaciones = []
    for paso, (nombre, argumentos) in enumerate(politica, 1):
        if paso > PASOS_MAX:
            print(f"  paso {paso}: presupuesto agotado, se corta el bucle")
            break
        resultado, estado = ejecutar(nombre, argumentos)
        observaciones.append(resultado)          # un fallo deja None en la lista
        print(f"  paso {paso}: {nombre}({argumentos}) -> {estado} {resultado}")
    return observaciones

print("agente A:")
obs_a = bucle_agente([("multiplicar", {"a": 3, "b": 4}), ("sumar", {"a": 12, "b": 5})])
print("  observaciones:", obs_a, "-> responde 17")
print("agente B:")
obs_b = bucle_agente([("multiplicar", {"a": 3, "b": 4}), ("sumar", {"a": "doce", "b": 5}),
                      ("multiplicar", {"a": 3, "b": 4}), ("sumar", {"a": 12, "b": 5})])
print("  observaciones:", obs_b, "-> responde 17 con un paso perdido")
