---
id: ficheros-y-encoding
titulo: Ficheros y codificaciones
fase: 3
nivel: básico
rutas: [de, ds, core]
prerequisitos: [entorno-python, tipos-y-estructuras-python]
tags: [ficheros, csv, json, parquet, encoding]
resumen: El mismo dato cambia de significado según la codificación, el formato y el separador; aquí se aprende a no corromperlo ni a perderlo por el camino.
fuentes: ["RFC 4180, 'Common Format and MIME Type for CSV Files'", "Documentación de Apache Parquet"]
---

## En una frase

Un fichero de datos son solo bytes con un convenio encima, y casi todos los desastres
silenciosos de un análisis empiezan ahí: leer UTF-8 como Latin-1, tomar la coma decimal por
separador de columnas, o meter un CSV de dos millones de filas en Excel y perder las últimas.

## La idea

Abre un fichero con un editor de texto y verás letras. Ábrelo con un editor hexadecimal y verás
la verdad: números. Un fichero no guarda «Sánchez», guarda la secuencia de bytes
`53 E1 6E 63 68 65 7A` o `53 C3 A1 6E 63 68 65 7A` según cómo esté escrito. Para volver de esos
bytes a la palabra hacen falta dos acuerdos: cuántos bytes forman cada carácter (la
**codificación**) y cómo están separados los campos (el **formato**).

Cuando la codificación equivocada **acepta** los bytes, no hay excepción ni traza de error: hay
basura. Latin-1 no falla jamás (cualquier byte es un carácter válido) y Windows-1252 falla solo
con cinco, así que leer como Latin-1 un fichero UTF-8 no se queja nunca. Al revés sí: un fichero
guardado en cp1252 y leído como UTF-8 lanza `UnicodeDecodeError: 'utf-8' codec can't decode byte
0xe1 in position 1: invalid continuation byte`. La
letra `ñ` existe tanto en UTF-8 como en Latin-1, pero se escribe con **dos bytes** en la
primera (`C3 B1`) y con **uno solo** en la segunda (`F1`). Quien lea los dos bytes pensando que
cada byte es un carácter obtiene dos caracteres distintos, y el programa sigue tan contento.

El segundo acuerdo, el del formato, decide cosas que parecen detalles y no lo son. En un CSV
el separador de campos puede ser la coma, el punto y coma o el tabulador, y el separador
decimal puede ser el punto o la coma. **No puedes elegir los dos igual.** Con decimales
españoles («1.234,56») el separador tiene que ser el punto y coma, porque si usas la coma el
número se parte en tres columnas y el resultado no da error: da una tabla con más columnas y
valores absurdos que a veces no se notan hasta el informe final.

Los formatos que vas a usar cada día, y para qué sirve cada uno:

- **CSV**: texto plano, una fila por línea, campos separados por un carácter. Universal y
  legible, pero **no guarda tipos**: todo es texto y hay que volver a interpretarlo al leer.
  Para comas o saltos de línea dentro de un campo, ese campo va entre comillas dobles.
- **JSON y JSON Lines**: guarda estructura y tipos (números, texto, booleanos, nulos) y
  anidamiento. JSON Lines es un objeto por línea, que es lo que permite leerlo por partes.
- **Parquet**: binario y **columnar** (guarda los valores agrupados por columna, no por fila),
  con tipos, diccionarios y compresión. Es lo que se usa para datos que se leen enteros una y
  otra vez.
- **Excel**: un `.xlsx` es en realidad un ZIP con XML dentro. Cómodo para gente, malo como
  formato de intercambio: pesa más, es más lento de leer y arrastra formato, celdas combinadas
  y fórmulas.

Finalmente, los saltos de línea no son universales: Unix usa `\n`, Windows `\r\n` y el Mac
clásico usaba `\r`. Python traduce los tres al leer en modo texto, pero si escribes un fichero
en binario con `\n` y lo abres en el Bloc de notas antiguo verás todo en una sola línea.

## Definición formal

**Codificación:** una función inyectiva que asigna a cada punto de código Unicode (un número
entre 0 y 1.114.111, escrito `U+XXXX`) una secuencia de bytes.

- **UTF-8**: codificación de longitud variable, de 1 a 4 bytes por carácter. Propiedad clave:
  los 128 primeros puntos de código (ASCII: letras sin tilde, dígitos, puntuación básica) se
  codifican **igual que en ASCII, con un solo byte**. Por eso es compatible hacia atrás.
  - 1 byte: `U+0000`–`U+007F` (ASCII).
  - 2 bytes: `U+0080`–`U+07FF` (Latin-1 con tildes, griego, cirílico).
  - 3 bytes: `U+0800`–`U+FFFF` (chino, japonés, símbolos como `€` o `√`).
  - 4 bytes: `U+10000`–`U+10FFFF` (emoji, planos suplementarios).
- **Latin-1 (ISO-8859-1)** y **Windows-1252**: un byte por carácter, solo cubren idiomas
  occidentales. Si tratas bytes UTF-8 como Latin-1, cada carácter acentuado se convierte en
  dos caracteres basura (el fenómeno llamado *mojibake*).
- **BOM** (*byte order mark*): la secuencia `EF BB BF` al principio de un fichero. En UTF-8 no
  sirve para nada, pero algunas herramientas de Windows la escriben. Si no la quitas, tu
  primera columna se llamará `\ufeffid` y no `id`. En Python se resuelve leyendo con
  `encoding="utf-8-sig"`.
- **`n`**: número de líneas del fichero, contando también la última aunque no acabe en salto.

**Límites de Excel**, que son la causa de la mitad de los «faltan datos»: 1.048.576 filas y
16.384 columnas por hoja. La versión 97-2003 (`.xls`) se queda en 65.536 filas.

## Ejemplo

Fichero `ventas.csv` con separador punto y coma y decimales con coma, tres líneas:

```
producto;importe
teclado;29,95
raton;12,50
```

- Si lo lees con un lector que usa la coma como separador, la cabecera `producto;importe` queda en
  **una sola columna** y cada línea de datos se parte por la coma decimal: `teclado;29,95` se
  convierte en `['teclado;29', '95']`. El daño es peor de lo que parece: hay columnas de más, el
  separador se queda pegado al nombre y los importes acaban dentro de una cadena de texto, así que
  no se pueden sumar.
- Si lo lees con `sep=";"` y `decimal=","`, obtienes dos columnas y la columna `importe` como
  número: 29,95 y 12,50. La media es 21,225.

Con una tabla de 2.000 filas y dos columnas (un entero y un texto que se repite entre cuatro
valores), el CSV ocupa unos 22 KB. La misma tabla guardando el texto una sola vez y una clave
por fila baja a unos 12 KB, y un formato columnar real como Parquet, que además comprime, se
queda alrededor de 8,5 KB: **menos de la mitad**. La ventaja crece con más columnas y más
repetición, y a eso se suma no tener que volver a interpretar los tipos al leer. Esa es la
razón de que todos los lagos de datos hablen Parquet y no CSV.

## Código

```python verificable
import csv
import io

# Leer un CSV con el separador equivocado: no falla, devuelve una sola columna de texto
crudo = "producto;importe\nteclado;29,95\nraton;12,50\n"

mal = list(csv.reader(io.StringIO(crudo)))
print("columnas mal :", mal[0], "filas", len(mal) - 1)          # -> ['producto;importe'] filas 2
print("tipo mal     :", type(mal[1][1]).__name__, "en vez de float")   # -> str en vez de float

bien = list(csv.reader(io.StringIO(crudo), delimiter=";"))
print("columnas bien:", bien[0])                                 # -> ['producto', 'importe']
importe = [float(f[1].replace(",", ".")) for f in bien[1:]]
print("media        :", round(sum(importe) / len(importe), 3))   # -> 21.225
```

```python verificable
import csv
import io

# Por que un formato columnar ocupa menos: el texto repetido se guarda como codigos
nombres = ["Sanchez", "Nunez", "Gomez", "Ruiz"]
filas = [(f"{i:04d}", nombres[i % 4]) for i in range(2000)]

csv_buf = io.StringIO()
escritor = csv.writer(csv_buf, lineterminator="\n")
escritor.writerow(["pedido_id", "nombre"])
escritor.writerows(filas)
bytes_csv = len(csv_buf.getvalue().encode())

# Modelo de lo que hace un diccionario: cada texto una vez y una clave por fila
diccionario = {n: i for i, n in enumerate(nombres)}
bytes_codigos = sum(len(p) + 2 for p, _ in filas) + sum(len(n) + 1 for n in nombres)

print("csv                    :", bytes_csv, "bytes")             # -> 22517 bytes
print("misma tabla como codigos:", bytes_codigos, "bytes")        # -> 12025 bytes
print("factor                 :", round(bytes_csv / bytes_codigos, 1))   # -> 1.9
print("codigos de la columna nombre:", [diccionario[n] for _, n in filas[:4]])   # -> [0, 1, 2, 3]
```

```python verificable
# La enye en dos codificaciones: mismo caracter, distinto numero de bytes
texto = "S" + "a" + "\u00f1" + "chez"

print("bytes de la enye:", texto.encode("utf-8")[2:4].hex())     # -> c3b1
print("longitud utf-8  :", len(texto.encode("utf-8")))          # -> 8
print("longitud latin1 :", len(texto.encode("latin-1")))        # -> 7

# Leer esos dos bytes como dos caracteres Latin-1 es el mojibake: U+00C3 y U+00B1
mal = texto.encode("utf-8").decode("latin-1")
print("caracteres distintos:", len(mal), "en vez de", len(texto))   # -> 8 en vez de 7
print("puntos de codigo:", " ".join(f"U+{ord(c):04X}" for c in mal))
```

```python verificable
import csv
import io

# Un campo con el separador y comillas dentro: CSV lo resuelve doblando las comillas
linea = 'producto;importe;nota\n"teclado; inalambrico";29,95;"dice ""oferta"" y ; sigue"\n'
filas = list(csv.reader(io.StringIO(linea), delimiter=";"))

print("columnas por fila:", [len(f) for f in filas])   # -> [3, 3]
print("campo con ';'    :", filas[1][0])               # -> teclado; inalambrico
print("comillas dobladas:", filas[1][2])               # -> dice "oferta" y ; sigue
```

## Errores típicos

- **Leer sin decir la codificación.** En Python y en Windows, `open()` sin `encoding=` usa la
  codificación del sistema (en España, tradicionalmente `cp1252`), no UTF-8. En Linux suele ser
  UTF-8 y el código «funciona» hasta que se ejecuta en otra máquina. Escribe siempre
  `encoding="utf-8"` y, si el fichero trae BOM, `encoding="utf-8-sig"`.
- **Arreglar el mojibake con `errors="ignore"`.** Silenciar los caracteres problemáticos no los
  recupera: los borra. Si el daño pasó por dos codificaciones distintas ya no hay vuelta atrás.
  Y si un carácter no existe en la codificación de destino (un emoji con `encode("latin-1")`),
  Python lanza `UnicodeEncodeError`; míralo en vez de taparlo.
- **Abrir CSV sin decir el separador ni el decimal.** Los ficheros exportados desde Excel en
  España llevan punto y coma y coma decimal. Si no lo declaras, obtienes una columna de texto y
  ninguna queja. Comprueba el resultado después de leer: si una fila tiene un campo donde
  esperabas dos, ese es el síntoma.
- **Escribir JSON a mano.** Un `NaN` de pandas no es JSON válido (`NaN` no existe en el
  estándar) y las fechas tampoco. Usa `to_json` con `date_format="iso"` y un `na` explícito, o
  convierte los nulos a `null` antes de serializar.
- **Abrir un `.xlsx` como si fuera texto.** Es un ZIP: leerlo como CSV da un error o basura. Se
  lee con `pd.read_excel`, y para saber qué hojas tiene, `pd.ExcelFile(ruta).sheet_names`.
- **Usar Excel como tubería de datos.** Al abrir un CSV con más de 1.048.576 filas, Excel
  trunca sin avisar; además reinterpreta códigos como `007` y convierte números largos en
  notación científica, cambiando el valor. Excel sirve para mirar, no para pasar datos de un
  sistema a otro.

:::practica
enunciado: El fichero ventas.csv trae las líneas producto;importe, teclado;1.234,56, raton;12,50 y monitor;99,90. Léelo con csv.reader usando delimiter=";", convierte la coma decimal y calcula el total. ¿En cuántas columnas queda cada línea si no declaras el separador?
pista: La coma solo aparece dentro del número decimal, así que con el delimitador por defecto el lector no encuentra el separador de campos; cambia la coma por un punto antes de sumar.
solucion: Con delimiter=";" la cabecera es ['producto', 'importe'] y los importes 1234.56, 12.50 y 99.90 tras reemplazar la coma por el punto. El total es 1234,56 + 12,50 + 99,90 = 1346,96. Sin declarar el separador, "producto;importe" queda en 1 columna y "teclado;1.234,56" se parte en ['teclado;1.234', '56']: más columnas, importes en texto y ninguna suma posible.
:::

## Comprueba que lo sabes

:::quiz
p: Un CSV exportado en España trae `producto;importe` con valores como `29,95`. ¿Qué pasa si lo lees con la coma como separador por defecto?
o: Lanza un error porque la coma decimal no es válida en CSV
o: La cabecera queda en una columna y las líneas de datos se parten por la coma decimal, así que no hay dos columnas limpias y los importes acaban en texto
o: Lee bien las columnas pero convierte los importes a enteros
a: 2
e: El lector busca comas: en la cabecera no hay ninguna, así que queda entera en una columna, y en `teclado;29,95` la encuentra en el decimal y parte la línea en `teclado;29` y `95`. El resultado es una tabla con distinto número de campos por fila, el separador `;` pegado al nombre y los importes en texto. Hay que declarar `delimiter=";"` y `decimal=","` para obtener dos columnas y números de verdad.
:::

:::quiz
p: ¿Qué significa que UTF-8 sea compatible con ASCII?
o: Que cualquier fichero UTF-8 se puede leer como ASCII sin perder información
o: Que los 128 primeros caracteres se codifican con un solo byte idéntico a ASCII, y el resto ocupa 2, 3 o 4
o: Que UTF-8 solo puede representar caracteres ingleses
a: 2
e: La compatibilidad es hacia atrás y solo en ese rango: los puntos de código por debajo de U+0080 coinciden byte a byte con ASCII. Fuera de ese rango UTF-8 usa varios bytes, y leerlos como Latin-1 produce mojibake, no información correcta.
:::

:::quiz
p: ¿Por qué un formato columnar como Parquet ocupa bastante menos que el CSV con los mismos datos?
o: Porque agrupa los valores por columna, comprime mejor y guarda el texto repetido como códigos de diccionario
o: Porque elimina las filas duplicadas al guardar
o: Porque guarda solo una muestra de los datos
a: 1
e: Parquet es columnar: los valores de una misma columna se parecen entre sí, así que se comprimen mejor y el texto repetido se sustituye por una clave. No elimina filas ni muestrea: al leerlo recuperas exactamente las filas escritas, con sus tipos.
:::

:::aviso
Si lees con `errors="ignore"`, los bytes que no encajan desaparecen y obtienes filas a las que
les faltan caracteres, sin ninguna pista de cuáles. Cuenta cuántos se descartan antes de
decidir que el fichero «estaba bien».
:::
