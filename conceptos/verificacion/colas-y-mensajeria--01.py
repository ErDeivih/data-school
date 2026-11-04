# Tres formas de entregar el mismo mensaje y lo que pasa cuando el consumidor falla.
def intento_entrega(exito):
    return exito                    # el parametro simula el resultado: True funciona, False falla

def at_most_once(exito):
    intento_entrega(exito)          # se envia una vez y se olvida
    return "perdido" if not exito else "procesado"
    # expresion condicional: primero el valor de la izquierda, que es el de la condicion cierta

def at_least_once(exito, max_reintentos=3):
    for _ in range(max_reintentos):     # _ es la variable de usar y tirar: no se lee la vuelta
        if intento_entrega(exito):
            return "procesado"          # sale en el primer intento que funcione
    return "a la cola de muertos"       # agoto los reintentos: el mensaje es veneno

print("at-most-once, fallo  ->", at_most_once(False))            # -> perdido
print("at-least-once, fallo ->", at_least_once(False))           # -> a la cola de muertos
print("at-least-once, exito ->", at_least_once(True))            # -> procesado

# Backoff exponencial con tope: el reintento 3 espera 4 s y del 6 en adelante, 30 s.
for intento in range(1, 8):
    espera = min(30, 2 ** (intento - 1))     # el tope es lo que aplana la curva
    print(f"reintento {intento}: espera {espera:>2} s")     # :>2 alinea los numeros de dos cifras
