from urllib.parse import urlparse

# El ejecutor de herramientas decide, no el prompt: lista blanca por host exacto.
PERMITIDOS = {"api.interna.example"}

def host_permitido(url):
    """Solo el host exacto cuenta: subdominios y parecidos quedan fuera."""
    # urlparse no hace ninguna peticion: solo parte la URL y hostname devuelve el host (sin puerto ni ruta).
    # El `or ""` tapa el caso de una URL sin host, donde hostname es None y .lower() reventaria.
    host = (urlparse(url).hostname or "").lower()
    # `in` sobre un conjunto compara la cadena ENTERA: api.interna.example.evil.test no es igual al permitido
    return host in PERMITIDOS

propuestas = [
    "https://api.interna.example/v1/tarifas",
    "https://api.interna.example.evil.test/roba",
    "https://file.interna.example/v1",
]

for url in propuestas:
    print(f"{str(host_permitido(url)):>5}  {url}")   # :>5 alinea el True/False en 5 caracteres
# ->  True  https://api.interna.example/v1/tarifas
# -> False  https://api.interna.example.evil.test/roba
# -> False  https://file.interna.example/v1
