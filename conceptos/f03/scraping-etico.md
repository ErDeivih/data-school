---
id: scraping-etico
titulo: Web scraping responsable
fase: 3
nivel: intermedio
rutas: [de, ds]
prerequisitos: [apis-y-peticiones-http, regex-y-limpieza-de-texto]
tags: [scraping, robots, etica, cache, html]
resumen: Antes de rascar una web hay que leer robots.txt, limitar el ritmo, cachear lo descargado y comprobar si existe una API o un fichero que ya lo ofrece.
fuentes: ["RFC 9309, 'Robots Exclusion Protocol'", "Documentación de Python: urllib.robotparser"]
---

## En una frase

El scraping responsable es pedir permiso (leer `robots.txt` y los términos de uso), pedir poco
(un ritmo lento y una caché que evite repetir), identificarte y saber retirarte cuando la web
dice que no.

## La idea

Rascar una web no es técnicamente difícil: se pide una página y se extrae lo que interesa. Lo
difícil es hacerlo sin ser un mal vecino y sin construir un sistema que se rompa cada semana.

Piensa en la web del otro como en una tienda. Entrar y mirar el escaparate es razonable.
Mandar a cincuenta personas a recorrer cada pasillo a la vez, no. Y copiar el catálogo entero
para revenderlo ya es otra conversación, que no se resuelve con código.

Hay tres puertas que hay que llamar antes de rascar:

1. **`robots.txt`**: fichero en la raíz del dominio (`https://ejemplo.com/robots.txt`) donde el
   dueño dice qué puede recorrer cada robot. Es un estándar de facto, documentado hoy en la
   RFC 9309. Bloquea rutas por agente: `User-agent: *` para todos, `Disallow: /privado/` para
   prohibir una ruta, `Crawl-delay` para pedir una pausa mínima entre peticiones.
2. **Los términos de uso de la web**: pueden prohibir la extracción automatizada aunque
   `robots.txt` no diga nada. `robots.txt` es una convención técnica, no un permiso legal.
3. **La ley de protección de datos y la propiedad intelectual**: si lo que rascas incluye
   datos personales (nombres, correos, perfiles), estás tratando datos personales y te aplica
   el RGPD, con sus bases jurídicas y sus plazos de conservación. Y los textos, fotos y bases de
   datos originales tienen derechos de autor o de creador de bases de datos. En caso de duda,
   hay una respuesta que casi siempre es la correcta y no es «rascar más»: pedir una API, pedir
   un volcado al dueño, o usar datos abiertos con licencia.

Después está la ingeniería, que tiene su propia lista de problemas:

- **Ritmo.** Un servidor web no distingue «un investigador» de «un ataque» salvo por la
  frecuencia. Respeta `Crawl-delay`, deja un margen entre peticiones, y usa un solo hilo por
  dominio mientras no tengas permiso explícito para más.
- **Caché.** Guarda cada página descargada en disco con su URL y su fecha. Volver a pedir algo
  que ya tienes duplica la carga del servidor y hace tu análisis irrepetible. Con caché, además,
  puedes reejecutar tu script sin red.
- **Identificación.** Un `User-Agent` que diga quién eres y cómo contactarte es lo mínimo. Un
  `User-Agent` falseado (haciéndote pasar por un navegador que no eres) es lo que convierte un
  scraping educado en un engaño.
- **Fragilidad.** El HTML es para humanos: cambia el diseño y tu selector deja de encontrar
  nada. Y no siempre falla ruidosamente: a veces la tabla sigue existiendo pero vacía. Si el
  dato es importante, valida lo extraído (número de filas, rangos de valor) y alerta.
- **Alternativas mejores.** Antes de rascar, busca: ¿hay API? ¿hay un fichero CSV descargable?
  ¿hay un conjunto de datos abierto (portal de datos abiertos, catálogo público)? ¿hay un
  `sitemap.xml` con las URLs en condiciones? Una parte enorme de los scrapers que se escriben
  no hacían ninguna falta.

## Definición formal

**`robots.txt`** es un fichero de texto con grupos separados por líneas en blanco:

```
User-agent: <agente>
Disallow: <prefijo de ruta>      ruta o prefijo prohibido
Allow:    <prefijo de ruta>      excepción dentro de lo prohibido
Crawl-delay: <segundos>          espera mínima entre peticiones
Sitemap:  <URL del sitemap>      no es una regla, es un aviso
```

Reglas que conviene tener claras:

- El espaciado y las mayúsculas de `User-agent` y `Disallow` no importan; las rutas **sí**
  distinguen mayúsculas de minúsculas.
- `Disallow:` vacío significa «puede recorrerlo todo». `Disallow: /` significa «no recorra
  nada».
- Un robot debe aplicar **su** grupo si existe (el que coincide con su `User-agent`), y el
  grupo `*` en caso contrario. Los grupos no se mezclan: si tienes grupo propio, se aplica el
  tuyo.
- La ruta de la consulta cuenta: `Disallow: /buscar?` prohíbe `/buscar?q=algo`.

Un cliente que cumple esto en Python es `urllib.robotparser.RobotFileParser`: se le pasa el
contenido del `robots.txt` con `parse()`, y a partir de ahí `can_fetch(agente, url)` responde
sí o no y `crawl_delay(agente)` devuelve la pausa pedida.

## Ejemplo

`robots.txt` de `https://tienda.example/robots.txt`:

```
User-agent: *
Disallow: /privado/
Crawl-delay: 2

User-agent: AgenteAmable
Disallow: /admin/
Crawl-delay: 10
```

Que significa para cada robot:

- `AgenteAmable` tiene su propio grupo, así que se le aplica **solo** ese: no puede tocar
  `/admin/` y debe esperar 10 segundos entre peticiones. Puede recorrer `/catalogo` igual que
  cualquier otro, porque su grupo no lo menciona.
- Cualquier otro robot usa el grupo `*`: no puede tocar `/privado/` y debe esperar 2 segundos.

Con cuatro rutas, la decisión de pedir es:

| Agente | URL | Decisión | Motivo |
| --- | --- | --- | --- |
| AgenteAmable | /admin/panel | Prohibido | Regla propia del agente |
| AgenteAmable | /catalogo | Permitido | No hay regla que lo bloquee |
| OtroBot | /catalogo | Permitido | El grupo `*` no lo menciona |
| OtroBot | /privado/ | Prohibido | `Disallow: /privado/` del grupo `*` |

## Código

```python verificable
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
```

```python verificable
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
```

```python ilustrativo
# El scraper educado: permiso, cache y ritmo, en el orden correcto
import time
from pathlib import Path
from urllib.robotparser import RobotFileParser

import requests

AGENTE = "AgenteAmable/1.0 (+https://misitio.example/contacto)"
CACHE = Path("cache")

rp = RobotFileParser("https://tienda.example/robots.txt")   # 1. permiso
rp.read()
espera = rp.crawl_delay(AGENTE) or 2

for pagina in range(1, 500):
    url = f"https://tienda.example/catalogo?p={pagina}"
    destino = CACHE / f"catalogo-{pagina}.html"
    if destino.exists():                                    # 2. cache
        continue
    if not rp.can_fetch(AGENTE, url):
        break
    r = requests.get(url, headers={"User-Agent": AGENTE}, timeout=15)
    r.raise_for_status()
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(r.text, encoding="utf-8")
    time.sleep(espera)                                      # 3. ritmo
```

## Errores típicos

- **Ignorar `robots.txt` «porque es solo una convención».** Lo es, y precisamente por eso
  ignorarlo dice mucho de ti: es la forma que tiene el dueño de decir que no sin cerrar la
  puerta. Si te piden rascar algo prohibido, la respuesta correcta es pedir permiso por
  escrito, no cambiar el `User-Agent`.
- **Falsear el `User-Agent` para parecer un navegador.** Conseguirás la página hoy y un bloqueo
  por IP mañana, además de incumplir los términos de uso. Identifícate con un agente propio y
  una URL de contacto.
- **Rascar sin caché.** Cada prueba de tu script vuelve a golpear el sitio entero. Con caché en
  disco, el desarrollo es más rápido, el análisis es reproducible y el servidor apenas se
  entera.
- **Rascar sin límite de ritmo.** Un `for` sin `sleep` genera decenas de peticiones por segundo.
  Ni siquiera necesitas mala intención: basta un script eficiente. Respeta el `Crawl-delay` y,
  si no lo hay, empieza por 1 o 2 segundos por petición.
- **Escribir selectores contra un HTML que cambia.** El scraping basado en rutas de etiquetas se
  rompe en el siguiente rediseño. Extrae con reglas que dependan del significado (cabeceras de
  tabla, atributos estables) y **valida** el resultado: si esperabas 200 filas y hay 3, es un
  fallo, no un dato.
- **Rascar datos personales sin base jurídica.** Un listado de nombres con teléfonos o correos
  es datos personales: hace falta una base jurídica, informar y limitar la conservación. Y
  aunque no haya personas, copiar una base de datos ajena puede vulnerar derechos del creador.
- **No mirar si hay algo mejor.** Muchas webs publican un CSV, un `sitemap.xml` o una API
  pública. Dos minutos de búsqueda ahorran una semana de mantenimiento del scraper y todos los
  problemas anteriores.

:::practica
enunciado: El robots.txt de tienda.example tiene un solo grupo "*" con Disallow: /privado/, Allow: /privado/prensa/ y Crawl-delay: 2. Quieres descargar 600 páginas de /catalogo/ y 40 de /privado/prensa/. ¿Cuántas puede pedir tu bot, cuánto tarda respetando la espera y qué pasa si repites el proceso con caché en disco?
pista: El Allow abre una excepción dentro de lo prohibido. El tiempo son las peticiones menos una, multiplicado por la espera entre ellas.
solucion: El bot puede pedir las 600 de /catalogo/ y las 40 de /privado/prensa/, porque el Allow gana sobre el Disallow del prefijo; /privado/pedidos quedaría prohibido. Son 640 peticiones y 639 intervalos de 2 segundos: 1278 segundos, unos 21 minutos. Con caché en disco, la segunda ejecución no hace ninguna petición: lee las 640 páginas guardadas y no vuelve a cargar el servidor.
:::

## Comprueba que lo sabes

:::quiz
p: Un `robots.txt` tiene un grupo `User-agent: *` con `Disallow: /privado/` y otro `User-agent: MiBot` con `Disallow: /admin/`. ¿Qué puede recorrer MiBot?
o: Solo lo que no esté ni en /privado/ ni en /admin/, porque los grupos se suman
o: Puede recorrer /privado/, porque su grupo propio sustituye al grupo general
o: No puede recorrer nada, porque hay dos grupos y eso es un error de sintaxis
a: 2
e: Los grupos no se combinan: si el robot tiene su propio grupo, se aplica ese y solo ese. MiBot queda limitado por su Disallow: /admin/, mientras el grupo * solo afecta a los robots que no tienen grupo propio. Mucha gente cree que las reglas se acumulan, y no.
:::

:::quiz
p: ¿Por qué es importante cachear en disco las páginas descargadas?
o: Porque así el HTML se guarda comprimido y ocupa menos
o: Porque evita repetir peticiones al servidor y hace que el análisis se pueda reejecutar sin red
o: Porque sin caché el navegador no permite abrir las páginas
a: 2
e: La caché cumple dos funciones: reduce la carga del sitio (no pido dos veces lo mismo) y hace el trabajo reproducible, porque puedo repetir la extracción sin depender de que la web siga igual o esté disponible. La compresión es otra cosa y no tiene nada que ver.
:::

:::quiz
p: Has encontrado un listado público con nombres, teléfonos y correos que quieres rascar. ¿Qué falta comprobar antes?
o: Nada, si la página es pública los datos son libres
o: Si hay base jurídica para tratar datos personales, qué dicen los términos de uso y si existe una vía mejor (API o datos abiertos)
o: Solo si el HTML tiene una etiqueta que prohíba el scraping
a: 2
e: Que un dato sea públicamente accesible no lo convierte en libre: los datos personales siguen protegidos por el RGPD y exigen base jurídica, información y límite de conservación. Además hay que mirar los términos de uso y la propiedad intelectual, y buscar alternativas licenciadas.
:::

:::trampa
Un scraper que funciona hoy puede devolver cero filas mañana sin lanzar ningún error, porque la
página existe pero ya no tiene la tabla donde estaba. Valida siempre el número de filas y el
rango de los valores extraídos, y haz que el pipeline falle cuando no cuadren.
:::
