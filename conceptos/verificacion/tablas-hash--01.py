# Tabla hash con encadenamiento, el mecanismo que hay dentro de un dict.
def dispersion_java(s, m):
    """Hash de cadenas estilo Java, reducido modulo m."""
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) % m   # el modulo en cada paso evita numeros gigantes
    return h

m = 8
palabras = ["sol", "luna", "mar", "rio", "cielo", "nube"]
cubos = [[] for _ in range(m)]

for p in palabras:
    cubos[dispersion_java(p, m)].append(p)

print("ocupacion por cubo:", [len(c) for c in cubos])   # -> [2, 0, 2, 0, 1, 0, 1, 0]
print("factor de carga:", round(len(palabras) / m, 2))  # -> 0.75

# Buscar 'mar': el cubo 6 tiene un solo elemento, asi que basta una comparacion
cubo = cubos[dispersion_java("mar", m)]
print("cadena del cubo", dispersion_java("mar", m), ":", cubo)  # -> cadena del cubo 6 : ['mar']
print("comparaciones:", cubo.index("mar") + 1)                  # -> 1
