# Cache: la misma URL no se pide dos veces, y el analisis se puede reejecutar sin red
import hashlib

def clave(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:12] + ".html"

def obtener(url, cache, peticiones):
    fichero = clave(url)
    if fichero in cache:
        return cache[fichero], peticiones
    peticiones += 1
    contenido = f"<html>contenido de {url} descargado en la peticion {peticiones}</html>"
    cache[fichero] = contenido          # en produccion: Path(fichero).write_text(contenido)
    return contenido, peticiones

cache, peticiones = {}, 0
urls = ["https://tienda.example/catalogo?p=1",
        "https://tienda.example/catalogo?p=2",
        "https://tienda.example/catalogo?p=1"]      # la tercera ya la tenemos

for u in urls:
    _, peticiones = obtener(u, cache, peticiones)

print("URL visitadas   :", len(urls))            # -> 3
print("peticiones reales:", peticiones)          # -> 2
print("clave de cache   :", clave(urls[0]))      # -> dd09c881bfa5.html
