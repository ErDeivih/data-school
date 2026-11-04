---
id: tomar-notas-tecnicas
titulo: Tomar notas técnicas
fase: 0
nivel: básico
rutas: [core]
prerequisitos: [como-estudiar]
tags: [notas, metodo, documentacion, memoria]
resumen: Una nota técnica es un mensaje a tu yo de dentro de seis meses: qué pasaba, qué decidiste, por qué y con qué versiones, en texto plano que se pueda buscar.
fuentes: ["Ahrens (2017), 'How to Take Smart Notes'", "Forte (2022), 'Building a Second Brain'", "Python Software Foundation (2025), 'doctest — Test interactive Python examples'"]
---

## En una frase

Una nota técnica es un mensaje a tu yo de dentro de seis meses: el síntoma con las palabras con las
que lo buscarás, la decisión que tomaste, el motivo y las versiones exactas, guardada en texto plano
que se pueda encontrar con una búsqueda.

## La idea

Imagina que el mes que viene vuelves a ver el mismo error de hoy. Tienes dos escenarios. En el
primero, recuerdas vagamente que «esto ya lo arreglé» y vuelves a empezar de cero: dos horas. En el
segundo, abres un fichero, buscas tres palabras y lees seis líneas que dicen qué era, qué hiciste y
por qué, con la fecha y la versión. Dos minutos. La diferencia entre los dos escenarios no es tu
memoria: es si escribiste la nota el día que resolviste el problema.

Lo primero que hay que entender es que **el valor de una nota no está en escribirla, está en
reencontrarla**. Por eso el formato importa más que la prosa: texto plano, un fichero por idea, un
título que describa el síntoma y no la solución («bom-en-la-primera-columna» se encuentra;
«arreglos-csv» no) y las palabras que usarás al buscar dentro del propio texto. Una nota en una
captura de pantalla, en un chat o en una aplicación que no exporta es una nota que no vas a
encontrar, y entonces su valor es cero.

Lo segundo es **qué lleva una nota**, y son cinco campos, no un diario:

1. **Contexto.** Qué estabas haciendo, con qué herramienta y en qué versión. Sin esto, no sabrás
   dentro de un año si la nota sigue siendo cierta.
2. **Síntoma.** El mensaje de error literal, copiado como texto, y lo que esperabas. Es el campo por
   el que vas a buscar.
3. **Decisión.** Qué hiciste, en una línea, con el código mínimo que lo resuelve.
4. **Por qué.** El motivo. Es el campo que todo el mundo se salta y el único que te permite saber si
   la decisión sigue valiendo cuando cambie el entorno.
5. **Descartes y preguntas abiertas.** Qué probaste y no era, y qué quedó sin responder. Los
   descartes ahorran la mitad del tiempo la próxima vez.

Lo tercero: **escribe con tus palabras**. Copiar un párrafo de la documentación no consolida nada
—es la misma trampa que leer y subrayar de [[como-estudiar]]— y dentro de un año ese párrafo habrá
cambiado en la web y tú no sabrás si lo entendiste. Parafrasear obliga a decidir qué es lo esencial,
y esa decisión es la que se queda.

Y lo cuarto, que es lo que separa un cuaderno útil de un cementerio: **las notas se podan y se
explotan**. Cuando una nota te ha ahorrado tiempo tres veces, esa es una tarjeta de repaso y debería
estar en tu mazo, no escondida en una carpeta. Cuando una nota se queda obsoleta, se corrige o se
borra. Un cuaderno que solo crece acaba siendo un vertedero donde ya no buscas nada.

:::aviso
Una nota sin fecha ni versiones es una trampa con retardo. El mismo comando se comporta de otra
forma tres versiones después, y la nota seguirá sonando igual de convincente. Fecha y versión en
cada nota, aunque parezca obvio el día que la escribes.
:::

## Definición formal

El valor esperado de una nota, en minutos:

:::formula
valor = P(reencontrar) · utilidad − coste
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `P(reencontrar)` | Probabilidad de dar con la nota cuando la necesites | entre 0 y 1 | La nota rinde más: se encuentra y se usa. Sube con el texto plano, el título con el síntoma y la búsqueda por palabras |
| `utilidad` | Tiempo que te ahorra cada vez que la usas | minutos | Merece la pena escribir notas más largas y detalladas, porque se van a amortizar |
| `coste` | Tiempo de escribirla y mantenerla | minutos | Si pasa de lo que ahorra, la nota es un hobby, no una herramienta |
| `valor` | Minutos esperados de ganancia | minutos | Si sale negativo, esa nota no había que escribirla: es el caso de la captura de pantalla que nunca volverás a mirar |
:::

Las cinco partes de una nota técnica, como definición operativa: **contexto** (dónde estabas),
**síntoma** (qué pasaba, con el texto del error), **decisión** (qué hiciste), **motivo** (por qué
funciona) y **descartes** (qué no era). Una nota a la que le falta el motivo sirve una vez; una a la
que le faltan los descartes sirve media.

Dos reglas de forma que no son estética, son recuperación: **un fichero por idea** y **el título con
el síntoma**. La primera evita el fichero de 400 líneas en el que todo está mezclado; la segunda
evita el título «notas varias», que es lo mismo que no tener título.

:::truco
Si el motivo de una nota se puede comprobar, escríbelo como ejemplo ejecutable con el formato de
`doctest` (`>>>` y el resultado esperado debajo). Así la nota se comprueba sola cuando el
comportamiento cambie, y deja de ser un texto en el que hay que confiar. Es la misma idea que
sostiene los bloques verificables de este portal.
:::

## Ejemplo

Dos notas sobre el mismo problema. La primera es lo que se escribe con prisa:

```text
notas.txt

he tenido un problema con el csv de importes, al final era el encoding
usar utf-8-sig y ya esta. tambien probe con latin-1 y no iba bien.
```

La segunda es la misma información, con los cinco campos y un título que se puede buscar:

```text
2026-10-14  bom-en-la-primera-columna

CONTEXTO  Exportación de importes a CSV que el usuario abre y vuelve a guardar en Excel.
SÍNTOMA   La primera columna del CSV se llama 'importe' y el script no la encuentra:
          el nombre lleva un BOM delante y no es la misma cadena.
DECISIÓN  Abrir con encoding="utf-8-sig". El BOM se consume y los nombres salen limpios.
MOTIVO    El BOM es un carácter invisible al principio del fichero; utf-8-sig lo descarta
          al leer, y el resto del texto se decodifica igual que con utf-8.
DESCARTE  latin-1: no quita el BOM (sigue delante del nombre, ahora como tres caracteres
          raros) y además rompe los acentos del resto del fichero.
          Quitar el BOM con un script aparte: un paso más que mantener, para nada.
VERSIONES Python 3.12.10 · pandas 3.0.6 · Windows 11
ABIERTA   ¿qué otros programas escriben BOM? (Excel y algunos exportadores, dicen)
```

La misma verdad, dos resultados distintos, y la diferencia se ve con la fórmula. Supón que el
problema tarda 30 minutos en resolverse desde cero y que escribir una nota cuesta 8 minutos:

| Nota | P(reencontrar) | Utilidad | Coste | Valor esperado |
| --- | --- | --- | --- | --- |
| El bloque suelto en `notas.txt` | 0,05 | 30 min | 8 min | −6,5 min |
| La nota con título y cinco campos | 0,60 | 30 min | 8 min | +10 min |

La primera se escribió para quitársela de encima: vive en un fichero sin títulos, no dice qué
herramienta era ni con qué versión, y nadie busca «encoding» para encontrar un problema de BOM. Su
probabilidad de reencuentro es casi nula, así que sus ocho minutos de escritura se han perdido. La
segunda se encuentra buscando «importe», «bom» o «utf-8-sig», y a la tercera vez que te ahorre media
hora habrá pagado su coste muchas veces.

## Código

```python verificable
# Buscar en texto plano es lo unico que encuentra una nota que no recuerdas haber escrito.
# Fijate en la segunda busqueda: la nota existe, pero con otras palabras, y no aparece.
notas = [
    ("bom-en-la-primera-columna",
     "El nombre de la primera columna sale con caracteres raros: el CSV empieza con BOM. Abrir con utf-8-sig."),
    ("leer-400-csv-tarda-9-minutos",
     "Leer 400 CSV tardaba 9 minutos; el mismo dato en Parquet, 12 segundos."),
    ("nulos-en-el-join",
     "LEFT JOIN en SQL: los nulos del lado derecho no son ceros al sumar."),
]

def buscar(notas, consulta):
    c = consulta.lower()
    return [titulo for titulo, texto in notas if c in texto.lower() or c in titulo]

print("buscar 'bom'      :", buscar(notas, "bom"))
print("buscar 'va lento' :", buscar(notas, "va lento"))
print("buscar 'tarda'    :", buscar(notas, "tarda"))
```

```python verificable
import doctest

# Una nota con el ejemplo en formato doctest se comprueba sola: si el resultado del ejemplo
# cambia, `python -m doctest nota.md` avisa antes de que te fies de ella.
nota = """>>> import json
>>> json.loads('{"filas": 3}')["filas"]
3"""

prueba = doctest.DocTestParser().get_doctest(nota, {}, "nota", "nota.md", 0)
resultado = doctest.DocTestRunner(verbose=False).run(prueba)
print("comprobaciones:", resultado.attempted, "  fallos:", resultado.failed)
```

:::claves
- `buscar` recorre las notas con una comparación de cadenas: es literalmente lo que hace `grep` o la
  búsqueda de tu editor. No hace falta una base de datos para encontrar tus notas; hace falta que
  sean texto.
- La comparación es en minúsculas por los dos lados. Sin eso, «BOM» y «bom» serían notas distintas, y
  tú no escribes siempre igual.
- La segunda búsqueda no encuentra nada y **no es un fallo del programa**: es el resultado real de
  buscar una palabra que no está en ninguna nota. Ese hueco es el que hay que evitar al escribirla.
- En la nota de ejemplo, `doctest` cuenta dos comprobaciones porque el bloque tiene dos sentencias
  `>>>`; la segunda es la que lleva la salida esperada y la que se compara línea a línea.
- `DocTestParser().get_doctest(texto, {}, "nota", "nota.md", 0)` convierte un texto cualquiera en una
  prueba. No hace falta que el fichero sea un módulo de Python: vale un `.md`.
- La salida de un doctest fallido se escribe en la salida estándar con las líneas `Expected` y `Got`.
  Ese informe es la nota diciéndote que se ha quedado desfasada.
- Los tres títulos de la lista usan las palabras del síntoma; ninguno se llama «csv» a secas. Un
  título genérico es invisible en una búsqueda, por muy buena que sea la nota.
:::

## Errores típicos

- **Apuntar la decisión y no el motivo.** «Usar `utf-8-sig`» sin el porqué no te deja decidir si
  sigue valiendo cuando leas datos que no vienen de Excel. El motivo es lo que se reutiliza.
- **Copiar y pegar documentación o respuestas de un asistente.** No has decidido qué era esencial, así
  que no lo has entendido, y en tres meses no podrás defenderlo. Es el riesgo que describe
  [[usar-ia-para-aprender]]: el atajo se nota al explicarlo.
- **Guardar la nota donde no la vas a buscar.** Capturas de pantalla, mensajes a ti mismo y
  aplicaciones sin exportar son el mismo agujero: el contenido existe, la búsqueda no.
- **El fichero único que crece sin parar.** Cuatrocientas líneas con veinte temas dentro. Un fichero
  por idea, con el nombre del síntoma, y una carpeta que se pueda recorrer de un vistazo.
- **Notas sin fecha ni versiones.** Sin esos dos datos no puedes saber si la nota sigue siendo cierta,
  y una nota obsoleta en la que confías es peor que no tenerla.
- **Apuntar solo lo que funcionó.** La lista de descartes («probé latin-1 y rompía los acentos») es lo
  que evita repetir el camino largo la próxima vez.
- **Escribir notas y no volver a mirarlas nunca.** Sin poda ni conversión en tarjetas, el cuaderno se
  convierte en un archivo muerto: para que una nota rinda, tiene que acabar en el repaso.

## Comprueba que lo sabes

:::quiz
p: ¿Cuál de estos títulos de nota encontrarás dentro de un año buscando el problema?
o: `arreglos-varios.csv`
o: `bom-en-la-primera-columna`
o: `nota-2026-10-14`
a: 2
e: El título tiene que llevar las palabras del síntoma, que son las que te van a venir a la cabeza cuando vuelvas a verlo. «Arreglos varios» no dice nada y la fecha tampoco: la fecha va dentro, como dato, no como nombre.
:::

:::quiz
p: ¿Por qué el campo del motivo es el que más se olvida y el que más importa?
o: Porque ocupa más espacio que los demás
o: Porque sin él no puedes saber si la decisión sigue siendo válida cuando cambie el entorno o la versión
o: Porque es el único campo que se puede copiar de la documentación
a: 2
e: La decisión te sirve una vez; el motivo te permite volver a decidir. Con el porqué delante, un cambio de versión o de fuente de datos te deja reevaluar la nota en lugar de aplicarla a ciegas.
:::

:::quiz
p: Una nota que te ha ahorrado media hora tres veces vive en tu cuaderno. ¿Qué haces con ella?
o: Dejarla donde está, que ya funciona
o: Convertirla en una o dos tarjetas de repaso y podar el resto
o: Copiarla entera en el fichero de notas generales por si acaso
a: 2
e: Si el contenido se ha usado tres veces es que es un conocimiento que quieres tener disponible sin buscarlo, y eso es exactamente una tarjeta de repaso. Copiarla al fichero general la vuelve a enterrar.
:::

:::practica
enunciado: Escribe la nota técnica de este episodio, con sus cinco campos y un título que se pueda buscar: «Hoy intenté subir un CSV a la base de datos y el proceso falló a mitad. Al final era que una fecha venía como 31/02/2026 y la base no la acepta. Lo arreglé filtrando las fechas imposibles antes de cargar, después de probar a cambiar el formato de fecha a ISO y de subir el fichero por trozos. Uso PostgreSQL 16 y Python 3.12 con pandas 3.0.6.»
pista: El síntoma es el mensaje de la base, no la conclusión. Y el descarte («cambiar a ISO») tiene un motivo que conviene escribir.
solucion: «2026-10-14 fechas-imposibles-rompen-la-carga. CONTEXTO: carga nocturna de un CSV de pedidos a PostgreSQL 16. SÍNTOMA: la carga falla a mitad con `invalid input syntax for type date: "31/02/2026"`; esperaba 12.400 filas cargadas y se quedó en 8.100. DECISIÓN: convertir con `pd.to_datetime(serie, format="%d/%m/%Y", errors="coerce")` y revisar cuántos nulos salen antes de cargar; cargar solo las filas con fecha válida y contar las descartadas. MOTIVO: la columna llega como texto y hay fechas que no existen en el calendario (31/02, 30/02), así que la base las rechaza aunque el formato sea correcto; pasarlas por `to_datetime` con `coerce` las convierte en nulas y las deja fuera antes de tocar la base. DESCARTE: pasar todo a ISO antes de cargar (`31/02` seguía siendo inválido, solo cambiaba el mensaje); subir por trozos (la fila mala seguía dentro y el fallo se repetía más tarde, con medio trabajo hecho). ABIERTA: ¿de dónde salen las fechas imposibles, del formulario o del exportador? VERSIONES: Python 3.12, pandas 3.0.6, PostgreSQL 16.» El título lleva el síntoma, el síntoma lleva el mensaje literal con el que se buscará, y cada descarte explica por qué el atajo no servía.
:::

:::nota
Una nota no es documentación para otros: es tu memoria externa. No hace falta que sea bonita ni
completa, hace falta que la encuentres y que te creas lo que dice. La prueba es sencilla: dentro de
un mes, busca el problema con tres palabras y mira si aparece.
:::
