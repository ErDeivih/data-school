---
id: regex-y-limpieza-de-texto
titulo: Expresiones regulares
fase: 3
nivel: intermedio
rutas: [de, ds]
prerequisitos: [tipos-y-estructuras-python, ficheros-y-encoding]
tags: [regex, texto, limpieza, patrones]
resumen: Patrones para validar, extraer y sustituir texto; por qué casi siempre «funciona», dónde está la trampa del anclaje y cuándo no hay que usar una expresión regular.
fuentes: ["Friedl (2006), 'Mastering Regular Expressions'"]
---

## En una frase

Una expresión regular es un patrón que describe un conjunto de cadenas, y sirve para tres cosas
—validar un formato, extraer un trozo y sustituir— con la advertencia de que casi siempre
«funciona» con los ejemplos que se te han ocurrido probar.

## La idea

Piensa en una plantilla de cartón con una forma recortada. Si la pones sobre un texto, solo pasa
lo que encaja en el hueco. Una expresión regular es eso: describes la forma (`\d{4}-\d{2}-\d{2}`)
y el motor busca o comprueba qué trozos encajan.

El problema es que la plantilla no entiende de significado. El patrón `\d{2}/\d{2}/\d{4}` da por
buena la cadena `99/99/9999`: la **forma** es correcta y la fecha es imposible. Una expresión
regular valida el formato, nunca el valor. Por eso después de la regex suele hacer falta una
conversión de verdad (`datetime.strptime`), que es la que rechaza el 32 de febrero.

Tres reglas evitan la mayoría de los disgustos:

1. **Ancla siempre.** `re.search` encuentra el patrón en cualquier posición y `re.match` solo al
   principio; ninguna de las dos valida la cadena completa. Para validar se usa `re.fullmatch` (o
   el patrón envuelto en `^…$`). Sin anclaje, `abc@def.com y basura` pasa como correo válido.
2. **Normaliza antes de comparar.** Espacios de más, mayúsculas y acentos hacen que el mismo valor
   de negocio sea varias cadenas distintas. Si normalizas al final, escribes el patrón dos veces y
   las categorías duplicadas reaparecen.
3. **Escribe el patrón contra ejemplos, incluidos los que NO deben pasar.** El caso vacío, el
   valor con un espacio detrás y el texto basura son las tres pruebas que descubren casi todos los
   fallos.

Dos comportamientos que hay que interiorizar:

- **Codicioso frente a perezoso.** `.*` intenta abarcar lo máximo posible y `.*?` lo mínimo. Con
  `<b>.*</b>` sobre `a <b>uno</b> y <b>dos</b>`, el codicioso devuelve desde el primer `<b>` hasta
  el último `</b>` —las dos etiquetas y lo de en medio—, y el perezoso devuelve solo `<b>uno</b>`.
  (El ejemplo sirve para ver el mecanismo; para leer HTML de verdad se usa un analizador, no una
  regex.)
- **Los grupos con nombre se leen.** `m['anio']` dice qué es; `m.group(3)` obliga a contar y se
  rompe en cuanto alguien añade un grupo delante.

Y lo que **no** hay que hacer con una expresión regular: analizar HTML, JSON o XML (un atributo
nuevo o una comilla escapada rompen el patrón y no te enteras); validar correos «de verdad» (el
formato completo es enorme y aun así no dice si el buzón existe); y categorizar texto libre sin
mirar antes cuántos valores distintos hay, cosa que resuelve el
[[perfilado-de-datos|perfilado]].

Un detalle de Python 3: `\w` incluye letras acentuadas y de otros alfabetos, y `[a-z]` no incluye
la `ñ`. Si el patrón tiene que ser estrictamente ASCII, dilo con `re.ASCII` o con una clase como
`[a-zA-Z0-9]`. Y si el patrón es fijo y se usa en un bucle, compílalo una vez con `re.compile`
fuera del bucle.

Por último, el coste: algunos patrones con cuantificadores anidados, como `(a+)+$`, hacen que el
motor pruebe un número exponencial de combinaciones ante una cadena que casi encaja. Es la
retrocedida catastrófica, y puede colgar el proceso con 40 caracteres.

## Definición formal

Piezas del lenguaje, con lo que significa cada una:

- **Literales y clases:** `abc` busca esa secuencia; `.` cualquier carácter salvo salto de línea
  (por defecto); `[abc]` uno de esos tres; `[^abc]` cualquiera menos esos; `[a-z]` un rango;
  `\d` un dígito; `\w` una letra, dígito o guion bajo; `\s` un espacio en blanco.
- **Cuantificadores:** `*` cero o más, `+` uno o más, `?` cero o uno, `{m,n}` entre `m` y `n`
  repeticiones, `{m,}` al menos `m`. Añadiendo `?` se vuelven perezosos (`*?`, `+?`).
- **Anclas y fronteras:** `^` principio de la cadena (o de línea con `re.MULTILINE`), `$` final,
  `\b` frontera de palabra.
- **Grupos:** `(...)` captura; `(?:...)` agrupa sin capturar; `(?P<nombre>...)` captura con nombre;
  `\1` o `(?P=nombre)` repiten lo capturado antes.
- **Alternancia:** la barra vertical separa dos alternativas, y `a|b` significa «a o b». Se combina
  con grupos para no comerse el resto del patrón: `(?:lunes|martes)`.
- **Lookaround:** `(?=...)` exige que lo que sigue encaje sin consumirlo; `(?!...)` exige que no
  encaje; `(?<=...)` y `(?<!...)` miran hacia atrás (en la mayoría de motores, con longitud fija).
- **Funciones:** `re.search` busca en cualquier posición; `re.match` ancla al principio;
  `re.fullmatch` exige que el patrón cubra la cadena entera; `re.findall` y `re.finditer`
  devuelven todas las coincidencias; `re.sub` sustituye (todas por defecto, o `count` veces);
  `re.split` parte por el patrón; `re.escape` convierte un texto literal en un patrón seguro.

Un objeto de coincidencia ofrece `group(0)` (la coincidencia completa), `group(n)` (el grupo `n`),
`groups()` (la tupla de grupos), y `start()` y `end()` (posiciones de inicio y fin).

## Ejemplo

Limpieza de un nombre y validación de un correo:

- `  juan   pérez ` → se colapsan los espacios, se recortan los extremos y se quitan las tildes:
  **`Juan Perez`**.
- `ANA@X.COM` → minúsculas: `ana@x.com`; `ana@x` **no** pasa el patrón porque le falta el dominio
  con punto; `no-es-un-email` tampoco; `ana@x.com ` pasa **solo** si se recortan los espacios
  antes de validar.

Extracción de fechas de un texto real: `Pedido 2024-03-05 entregado, factura 2024-04-12
pendiente`. Con el patrón `(?P<anio>\d{4})-(?P<mes>\d{2})-(?P<dia>\d{2})` salen dos coincidencias
y se reordenan a `05/03/2024` y `12/04/2024`. Y la advertencia del principio en números: ese mismo
patrón acepta `2024-13-45`, así que comprobar que la fecha existe se delega a `datetime`.

Codicioso frente a perezoso, con la misma entrada `a <b>uno</b> y <b>dos</b>`: `<b>.*</b>` devuelve
`<b>uno</b> y <b>dos</b>` y `<b>.*?</b>` devuelve `<b>uno</b>`. La única diferencia entre los dos
patrones es el signo de interrogación.

## Código

```python verificable
import re
import unicodedata

def normalizar(nombre):
    """Recorta espacios, quita tildes y deja una mayuscula inicial por palabra."""
    limpio = re.sub(r"\s+", " ", nombre).strip()
    sin_tildes = "".join(c for c in unicodedata.normalize("NFD", limpio)
                         if unicodedata.category(c) != "Mn")
    return sin_tildes.title()

sucios = ["  juan   pérez ", "MARIA gomez", " marta  ruiz-", "luis"]
print([normalizar(s) for s in sucios])
# -> ['Juan Perez', 'Maria Gomez', 'Marta Ruiz-', 'Luis']

# fullmatch exige que el patron cubra TODA la cadena; search habria dejado pasar basura.
CORREO = re.compile(r"[^@\s]+@[^@\s]+\.[a-z]{2,}")
candidatos = ["ana@x.com", "ANA@X.COM", "ana@x", "no-es-un-email", "ana@x.com "]
print([(c.strip().lower(), bool(CORREO.fullmatch(c.strip().lower()))) for c in candidatos])
# -> [('ana@x.com', True), ('ana@x.com', True), ('ana@x', False), ('no-es-un-email', False), ('ana@x.com', True)]
```

```python verificable
import re

texto = "Pedido 2024-03-05 entregado, factura 2024-04-12 pendiente"

# Grupos con nombre: se leen por su significado y no por su posicion.
FECHA = re.compile(r"(?P<anio>\d{4})-(?P<mes>\d{2})-(?P<dia>\d{2})")
print(" ".join(f"{m['dia']}/{m['mes']}/{m['anio']}" for m in FECHA.finditer(texto)))
# -> 05/03/2024 12/04/2024

# El asterisco es codicioso: se estira hasta el ultimo cierre. Con el interrogante, no.
print(re.search(r"<b>.*</b>", "a <b>uno</b> y <b>dos</b>").group(0))
# -> <b>uno</b> y <b>dos</b>
print(re.search(r"<b>.*?</b>", "a <b>uno</b> y <b>dos</b>").group(0))
# -> <b>uno</b>

# Lookahead: exigir un digito en cualquier posicion sin consumir caracteres.
print(bool(re.fullmatch(r"(?=.*\d)[A-Za-z0-9]{6,}", "abc123")))   # -> True
print(bool(re.fullmatch(r"(?=.*\d)[A-Za-z0-9]{6,}", "abcdef")))   # -> False
```

## Errores típicos

- **No anclar el patrón.** `re.match(r"\d+", "12 meses")` es verdadero y no has validado nada.
  Para comprobar que **toda** la cadena cumple el formato, `re.fullmatch` o anclas en los dos
  extremos. Es el error número uno porque el código «pasa las pruebas» con datos limpios.
- **Olvidar escapar el punto.** `\d+.\d+` acepta `12x34`, porque el punto sin escapar es cualquier
  carácter. Escribe `\.` o construye el patrón con `re.escape` cuando insertes texto del usuario.
- **Usar `.*` cuando querías lo mínimo.** En textos con varios pares de delimitadores, el
  codicioso se lleva todo el tramo. Cambia a `.*?` o, mejor, sustituye el patrón por una búsqueda
  estructura a estructura.
- **Analizar HTML, JSON o XML con expresiones regulares.** Funciona hasta que aparece un atributo
  nuevo, una comilla escapada o un salto de línea dentro de una etiqueta. Usa un analizador
  (`json`, `html.parser`, `lxml`); el texto estructurado se parsea, ver
  [[ficheros-y-encoding|ficheros y codificaciones]].
- **Suponer que `\w` es `[a-zA-Z]`.** En Python 3 `\w` incluye acentos y otros alfabetos. Un
  patrón de usuario que use `\w+` para un nombre de usuario acepta caracteres que tu base de datos
  puede no admitir. Sé explícito con la clase que quieres.
- **Escribir un patrón con anidamiento de cuantificadores.** `(a+)+` o `(\w+\s?)*` pueden provocar
  retrocedida exponencial: la misma expresión tarda milisegundos con una entrada y minutos con
  otra casi igual. Reescribe el patrón o limita la longitud de la entrada.

:::practica
enunciado: Escribe un patrón que valide códigos postales españoles: exactamente cinco dígitos y prefijo entre 01 y 52. Con re.fullmatch, cuenta cuántos pasan de ["46001","48001","99999","4600","4600a","01000"] y explica qué cambia si quitas el grupo de la alternancia.
pista: Ancla con fullmatch y agrupa el prefijo: sin los paréntesis, la alternancia se reparte el resto del patrón y deja alternativas sin los tres dígitos finales.
solucion: patron = re.compile(r"(?:0[1-9]|[1-4]\d|5[0-2])\d{3}"). Pasan "46001", "48001" y "01000": 3 de 6. Fallan "99999" (el prefijo 99 no está entre 01 y 52), "4600" (cuatro dígitos) y "4600a" (la letra final no encaja en \d). Sin el grupo, 0[1-9]|[1-4]\d|5[0-2]\d{3} solo exige los cinco dígitos en la última alternativa, así que rechazaría un código válido como "01000".
:::

## Comprueba que lo sabes

:::quiz
p: El patrón \d{2}/\d{2}/\d{4} acepta la cadena 99/99/9999. ¿Qué demuestra eso?
o: Que la expresión regular está mal escrita y que se puede arreglar para que la rechace
o: Que la expresión regular valida la forma, no el valor: comprobar que la fecha existe necesita un conversor
o: Que el patrón solo funciona con fechas anteriores a 1999
a: 2
e: El patrón describe el formato (dos dígitos, barra, dos dígitos, barra, cuatro dígitos) y 99/99/9999 encaja en él. Ninguna expresión regular razonable sabe cuántos días tiene febrero: eso lo resuelve datetime.strptime al convertir. El patrón no está mal escrito para lo que hace y no tiene nada que ver con el año: `\d{4}` acepta 2024 igual que 1999.
:::

:::quiz
p: ¿Qué diferencia hay entre <b>.*</b> y <b>.*?</b> sobre el texto a <b>uno</b> y <b>dos</b>?
o: Ninguna: el interrogante solo afecta a los grupos de captura
o: El primero es codicioso y llega hasta el último cierre; el segundo es perezoso y para en el primer cierre
o: El segundo patrón es inválido porque el interrogante no puede seguir a un asterisco
a: 2
e: El asterisco intenta abarcar lo máximo posible y el interrogante añadido lo vuelve perezoso, así que se detiene en la primera coincidencia del cierre. La sintaxis *? es perfectamente válida y es una de las combinaciones más usadas.
:::

:::quiz
p: Validar que un campo contiene un correo electrónico. ¿Cuál es la comprobación imprescindible que falta en re.match(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", valor)?
o: Usar fullmatch (o anclas) para exigir que el patrón cubra toda la cadena
o: Añadir el modificador re.IGNORECASE
o: Cambiar \s por un espacio literal
o: Quitar el cuantificador {2,} para que el patrón sea más corto
a: 1
e: re.match solo ancla al principio, así que una cadena que empiece por un correo válido y siga con cualquier cosa pasa el filtro. fullmatch exige que coincida la cadena entera. El modificador de mayúsculas es útil si el patrón tuviera letras, y \s es correcto para excluir espacios en cualquier posición. Quitar el cuantificador del dominio (que exige al menos dos letras detrás del punto) solo haría el patrón más permisivo, no más estricto.
:::

:::truco
Antes de escribir un patrón, junta la lista de ejemplos: cinco que deban pasar y cinco que no,
incluido el vacío, el que lleva un espacio al final y el que tiene el formato parecido pero
incorrecto. Con esa lista delante, el patrón casi se escribe solo y sabes cuándo has terminado.
Sin ella, el patrón crece hasta que «parece que funciona».
:::
