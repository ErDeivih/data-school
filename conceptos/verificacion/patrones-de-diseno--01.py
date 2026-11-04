# Estrategia: el algoritmo se inyecta y el contexto no sabe cual es.
# Las tres funciones tienen la misma firma (un peso, un numero): por eso son intercambiables.
def envio_estandar(peso): return 3.50 + 0.80 * peso    # cuota fija + precio por kilo
def envio_express(peso):  return 9.00 + 2.00 * peso    # misma forma, otros numeros
def envio_gratis(peso):   return 0.0                   # ignora el argumento: misma firma igual

# Fabrica: un solo sitio traduce la clave externa a la estrategia concreta.
# Ojo: el diccionario guarda FUNCIONES (sin parentesis), no el resultado de llamarlas.
TARIFAS = {"estandar": envio_estandar, "express": envio_express, "gratis": envio_gratis}

def tarifa(nombre):
    # Devuelve la funcion, no el precio: comprobar antes evita un KeyError poco claro.
    if nombre not in TARIFAS:
        raise ValueError(f"tarifa desconocida: {nombre}")
    return TARIFAS[nombre]

def coste_envio(peso, nombre):
    # Doble llamada: tarifa(nombre) da la funcion y (peso) la ejecuta con el peso.
    return round(tarifa(nombre)(peso), 2)

print("estandar 2.5 kg:", coste_envio(2.5, "estandar"))   # -> 5.5
print("express  2.5 kg:", coste_envio(2.5, "express"))    # -> 14.0
print("gratis   2.5 kg:", coste_envio(2.5, "gratis"))     # -> 0.0
