ids = [7, 3, 7, 9, 3, 7, 12, 9]

print("elementos en la lista:", len(ids))       # -> elementos en la lista: 8
print("ids distintos:", sorted(set(ids)))       # -> ids distintos: [3, 7, 9, 12]

conteo = {}
for i in ids:
    conteo[i] = conteo.get(i, 0) + 1
print("frecuencias:", dict(sorted(conteo.items())))   # -> frecuencias: {3: 2, 7: 3, 9: 2, 12: 1}

# Una tupla de valores inmutables si puede ser clave de diccionario
stock = {("madrid", "norte"): 120, ("madrid", "sur"): 80}
print("stock madrid norte:", stock[("madrid", "norte")])   # -> stock madrid norte: 120

# El argumento por defecto se crea UNA sola vez y se comparte entre llamadas
def anade(x, acumulado=[]):
    acumulado.append(x)
    return acumulado

print("primera llamada:", anade(1))   # -> primera llamada: [1]
print("segunda llamada:", anade(2))   # -> segunda llamada: [1, 2]

# La solucion: valor por defecto None y la lista se crea dentro de la funcion
def anade_bien(x, acumulado=None):
    acumulado = [] if acumulado is None else acumulado
    acumulado.append(x)
    return acumulado

print("con None:", anade_bien(1), anade_bien(2))   # -> con None: [1] [2]
