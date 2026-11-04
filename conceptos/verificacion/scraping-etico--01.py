# Decidir si una URL se puede pedir: la parte que casi todo el mundo se salta
from urllib.robotparser import RobotFileParser

robots = """User-agent: *
Disallow: /privado/
Crawl-delay: 2

User-agent: AgenteAmable
Disallow: /admin/
Crawl-delay: 10
"""

rp = RobotFileParser()
rp.parse(robots.splitlines())          # en produccion: rp.set_url(...); rp.read()

casos = [
    ("AgenteAmable", "https://tienda.example/admin/panel"),
    ("AgenteAmable", "https://tienda.example/catalogo"),
    ("OtroBot", "https://tienda.example/catalogo"),
    ("OtroBot", "https://tienda.example/privado/"),
]
for agente, url in casos:
    veredicto = "permitido" if rp.can_fetch(agente, url) else "PROHIBIDO"
    print(f"{agente:>12}  {url:42}  {veredicto}")

print("espera pedida al agente :", rp.crawl_delay("AgenteAmable"), "segundos")   # -> 10
print("espera pedida al resto  :", rp.crawl_delay("OtroBot"), "segundos")        # -> 2
