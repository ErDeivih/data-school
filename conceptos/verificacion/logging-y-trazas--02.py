# Arbol de tramos de una peticion: (nombre, id, padre, inicio_ms, duracion_ms)
spans = [
    ("GET /checkout", "a", None, 0, 240),
    ("autenticar", "b", "a", 5, 30),
    ("leer carrito", "c", "a", 40, 180),
    ("consulta SQL", "d", "c", 45, 170),
    ("calcular total", "e", "a", 225, 10),
]

hijos = {}
for nombre, sid, padre, inicio, duracion in spans:
    # Desempaquetado de la tupla en el propio for. setdefault agrupa por NOMBRE del padre:
    # crea la lista vacia la primera vez y luego siempre devuelve la misma.
    hijos.setdefault(padre, []).append((nombre, inicio, duracion))

raiz_nombre, raiz_id, _, _, raiz_duracion = spans[0]
directos = hijos[raiz_id]                    # los que cuelgan de la raiz; aqui no se solapan
ocupado = sum(duracion for _, _, duracion in directos)
# max con key: se queda con la TUPLA entera del tramo mas lento, no con la duracion.
mas_lento = max(directos, key=lambda s: s[2])

print("duracion de la peticion:", raiz_duracion, "ms")      # -> 240 ms
print("tiempo en hijos directos:", ocupado, "ms")           # -> 220 ms
print("tiempo propio del padre:", raiz_duracion - ocupado, "ms")   # -> 20 ms
# mas_lento[0] es el nombre y mas_lento[2] la duracion: el indice sale del orden de la tupla.
print(f"hijo mas lento: {mas_lento[0]} con {mas_lento[2]} ms")      # -> leer carrito con 180 ms
