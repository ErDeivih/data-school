# Parsear cabeceras HTTP sin red: el bloque de cabeceras, tal cual llegaria
from email.parser import Parser

cabeceras = (
    "Content-Type: application/json\r\n"
    "X-RateLimit-Limit: 60\r\n"
    "X-RateLimit-Remaining: 58\r\n"
    'Link: <https://api.ejemplo.com/v1/pedidos?page=3>; rel="next", '
    '<https://api.ejemplo.com/v1/pedidos?page=10>; rel="last"\r\n'
)
m = Parser().parsestr(cabeceras)
print("restantes       :", m["X-RateLimit-Remaining"], "de", m["X-RateLimit-Limit"])  # -> 58 de 60

# La cabecera Link es una lista de URL con su relacion entre <> y rel=""
partes = [p.strip() for p in m["Link"].split(",")]
rel = {p.split('rel="')[1].rstrip('"'): p.split(">")[0].lstrip("<") for p in partes}
print("pagina siguiente:", rel["next"])
print("ultima pagina   :", rel["last"])
