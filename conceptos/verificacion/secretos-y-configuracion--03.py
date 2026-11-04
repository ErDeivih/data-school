import re

# Contenido de dos commits: el que introduce el secreto y el que lo elimina.
historial = [
    ("a1b2c3", '+API_KEY = "sk-fake-NO-ES-UN-SECRETO-REAL"'),
    ("d4e5f6", '-API_KEY = "sk-fake-NO-ES-UN-SECRETO-REAL"'),
]
patron = re.compile(r"sk-fake-[A-Za-z0-9-]+")

# El patron busca en la LINEA entera, y el prefijo + o - del diff no estorba: da igual si el
# secreto se anadio o se quito, en los dos casos el valor esta escrito ahi.
afectados = [sha for sha, linea in historial if patron.search(linea)]
print("commits cuyo diff contiene el secreto:", len(afectados), afectados)   # -> 2 ['a1b2c3', 'd4e5f6']
# all() sobre un generador: False en cuanto encuentra una linea con el patron.
print("el historial esta limpio:", all(not patron.search(l) for _, l in historial))   # -> False
