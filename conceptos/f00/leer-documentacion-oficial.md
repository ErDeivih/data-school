---
id: leer-documentacion-oficial
titulo: Leer la documentación oficial
fase: 0
nivel: básico
rutas: [core]
prerequisitos: [como-estudiar]
tags: [documentacion, metodo, python, api]
resumen: La documentación oficial es el contrato de quien lo cumple: se lee buscando la firma exacta en la versión que tienes instalada, no de principio a fin como un libro.
fuentes: ["Procida (2017), 'Diátaxis: A systematic framework for technical documentation authoring'", "Python Software Foundation (2025), 'inspect — Inspect live objects'", "pandas development team (2025), 'pandas User Guide: Merge, join, concatenate and compare'"]
---

## En una frase

La documentación oficial es el sitio donde está escrito el contrato de una herramienta, con sus
valores por defecto y sus excepciones; se consulta buscando el nombre exacto de lo que usas y en la
versión que tienes instalada, no leyéndola entera como si fuera un libro.

## La idea

Cuando compras un electrodoméstico, el manual tiene tres partes muy distintas: la hoja de puesta en
marcha, las recetas de «cómo descongelar» y la tabla de especificaciones. Nadie lee la tabla de
especificaciones de principio a fin para aprender a usar el aparato, y nadie intenta averiguar el
consumo en vatios leyendo la receta. Con la documentación de software pasa lo mismo, y confundir las
partes es el error de base:

- **Tutorial** — te lleva de la mano por un camino que funciona. Sirve para la primera hora y
  miente por omisión: no lleva datos sucios, ni errores, ni casos raros.
- **Guía práctica** (how-to) — resuelve una tarea concreta («unir dos tablas», «leer por bloques»).
  Es el sitio al que ir cuando ya sabes qué quieres hacer.
- **Referencia** — el contrato: qué acepta cada función, qué devuelve, qué excepciones lanza y desde
  qué versión existe. Es la parte que se consulta a diario.
- **Explicación** — el porqué del diseño. Se lee cuando algo no te cuadra, no cuando tienes prisa.

Casi todo el tiempo que se pierde con una librería viene de buscar en la parte equivocada: intentar
aprender a usar algo leyendo la referencia, o buscar el valor por defecto de un parámetro en un
tutorial.

Lo segundo que hay que mirar es la **versión**. La documentación que sale por defecto suele describir
la última versión publicada, que puede no ser la tuya: un parámetro que existe en la versión
documentada puede no existir en la instalada, y uno que estaba por defecto puede haber cambiado de
comportamiento. Antes de copiar nada, comprueba qué versión tienes (`import pandas; pandas.__version__`)
y qué versión estás leyendo (el selector de versión de la propia web, o la ruta de la URL).

Y lo tercero: **la documentación es una herramienta de búsqueda, no de lectura**. Casi siempre llegas
con un nombre concreto —`DataFrame.merge`, `read_csv`, `json.loads`— y sales con cuatro datos: los
argumentos, los valores por defecto, el valor devuelto y las excepciones. Ese es el contrato. Si algo
no está ahí, el siguiente recurso es el registro de cambios, la guía de migración o el propio código
fuente; los foros y los asistentes van después, y se comprueban contra la referencia, nunca al revés.

:::aviso
Que la documentación oficial lo diga no significa que sea lo que tu versión hace. Los cambios de
comportamiento viven en las notas de la versión («What's new», el changelog), no siempre en la página
de la función. Si algo se comporta distinto de lo documentado, busca primero en ese registro.
:::

## Definición formal

Las cuatro clases de página, definidas por la pregunta que responden:

| Clase | Responde a | Se lee cuando | Qué no encontrarás |
| --- | --- | --- | --- |
| Tutorial | «¿Cómo empiezo y veo algo funcionar?» | La primera vez | Casos raros, errores, datos sucios |
| Guía práctica | «¿Cómo hago esta tarea concreta?» | Ya sabes el objetivo | El contrato completo de cada función |
| Referencia | «¿Qué acepta, qué devuelve, qué lanza?» | Siempre, mientras programas | Un camino de aprendizaje |
| Explicación | «¿Por qué está diseñado así?» | Cuando algo no te cuadra | Recetas ejecutables |

Y las piezas de una entrada de referencia, que es lo que se lee de verdad:

- **firma** — el nombre y la lista de parámetros, con el orden en que se pueden pasar y los que
  llevan valor por defecto: `merge(right, how='inner', on=None, ...)`.
- **parámetro obligatorio** — el que no tiene valor por defecto. Omitirlo no «falla un poco»: la
  llamada se rechaza antes de ejecutar nada.
- **valor por defecto** — qué hace la función si no le dices nada. Es el comportamiento «normal» que
  hay que conocer, porque es el que tendrás sin escribir una línea de más.
- **solo posicional y solo por nombre** — la barra `/` y el asterisco `*` dentro de la firma marcan
  los parámetros que no se pueden pasar de la otra forma. Un `*` en medio significa que todo lo que
  va detrás hay que escribirlo con su nombre.
- **valor devuelto** — no siempre es un objeto nuevo: muchas operaciones devuelven una **vista** de
  los datos originales, y modificar esa vista modifica el original. Es el mismo aviso que pide
  [[vistas-y-copias]].
- **excepciones** — los casos que el autor decidió rechazar en lugar de resolver en silencio.
- **notas de versión** — «Added in», «Changed in», «Deprecated in», «Removed in». Son cuatro líneas
  que ahorran una tarde de depuración.

El orden de confianza, de mayor a menor: el comportamiento observado en tu versión, la referencia de
tu versión, el registro de cambios, los ejemplos de la guía, y por último el foro o el asistente. Lo
que se lee en los dos últimos se comprueba contra los primeros antes de creérselo.

## Ejemplo

Objetivo: unir dos tablas y quedarte también con las claves que solo están en una de las dos. La
respuesta se saca en cuatro consultas, sin leer ningún tutorial:

1. Busca el nombre exacto del objeto: `DataFrame.merge`. No «cómo unir tablas en pandas».
2. Abre su referencia **en tu versión** y lee la firma: `how` acepta `left`, `right`, `outer`,
   `inner` y `cross`, y por defecto vale `inner`. En versiones recientes la lista ha crecido con
   `left_anti` y `right_anti`; esa diferencia es justo la que se pierde leyendo la documentación de
   otra versión.
3. Comprueba lo que significa cada valor con los datos delante. Con `izquierda` de identificadores
   1, 2 y 3 y `derecha` de identificadores 1, 2 y 4:

| Llamada | Filas que salen | Qué ha pasado |
| --- | --- | --- |
| `izquierda.merge(derecha, on="id")` | 2 | El `inner` que viene por defecto descarta los identificadores 3 y 4 |
| `izquierda.merge(derecha, on="id", how="outer")` | 4 | Aparecen el 3 y el 4, con dos huecos |

4. Lee la sección de notas: ahí es donde avisa de que con `how="outer"` las claves que faltan en un
   lado llegan como nulos, y de que un `many-to-many` duplica filas sin avisar.

Cuatro consultas, ninguna suposición y un resultado que puedes explicar. La alternativa —copiar un
ejemplo de un blog— también funciona el primer día, y falla el día que los identificadores se repiten.

## Código

```python verificable
import inspect
import pandas as pd

# La ayuda vive dentro del paquete instalado: es la de TU version y no necesita conexion.
firma = inspect.signature(pd.DataFrame.merge)
print("parametros  :", [p for p in firma.parameters if p != "self"])
print("por defecto :", firma.parameters["how"].default)
print("obligatorios:", [p.name for p in firma.parameters.values()
                        if p.name != "self" and p.default is inspect.Parameter.empty])
print("resumen     :", inspect.getdoc(pd.DataFrame.merge).splitlines()[0])

# No todo tiene firma inspeccionable: en las funciones escritas en C, la firma suele estar
# escrita a mano en la primera linea de la docstring.
try:
    inspect.signature(dict.update)
except ValueError as error:
    print("dict.update :", type(error).__name__)
    print("docstring   :", inspect.getdoc(dict.update).splitlines()[0])
```

```python verificable
import pandas as pd

# El valor por defecto viene en la firma: how="inner". Comprobarlo cuesta una linea y
# evita suponer lo que hace la funcion cuando la clave esta repetida o falta.
izquierda = pd.DataFrame({"id": [1, 2, 3], "importe": [10.0, 20.0, 30.0]})
derecha = pd.DataFrame({"id": [1, 2, 4], "pais": ["ES", "FR", "IT"]})

print("inner por defecto:", izquierda.merge(derecha, on="id").shape[0])                 # -> 2
print("outer explicito :", izquierda.merge(derecha, on="id", how="outer").shape[0])     # -> 4
print("nulos del outer :", int(izquierda.merge(derecha, on="id", how="outer").isna().sum().sum()))  # -> 2

# La firma es el contrato: si falta un argumento obligatorio, Python avisa antes de tocar datos.
try:
    izquierda.merge()
except TypeError as error:
    print("sin argumentos  :", error)
```

:::claves
- `inspect.signature` no ejecuta nada: lee la firma del objeto. Se puede usar con cualquier función
  cargada, aunque llamarla tuviera efectos.
- `firma.parameters` incluye `self`, que no se pasa nunca desde fuera: es la propia instancia. Por eso
  la lista que imprime el ejemplo empieza en `right`.
- Para saber si un parámetro es obligatorio no sirve mirar si su valor por defecto es `None`: hay que
  compararlo con `inspect.Parameter.empty`. Un `None` puede ser perfectamente el valor por defecto.
- `inspect.getdoc(objeto)` devuelve la docstring con la indentación limpiada; `objeto.__doc__` la da
  cruda, con los espacios del código fuente. Para leer texto, mejor `getdoc`.
- Con funciones escritas en C no siempre hay firma inspeccionable y `inspect.signature` lanza
  `ValueError`. En esos casos la firma suele estar escrita a mano en la primera línea de la docstring,
  como se ve con `dict.update`.
- El `TypeError` del último bloque lo lanza Python al comprobar la llamada, antes de entrar en la
  función: es la documentación ejecutándose. Si ves ese mensaje, no hay nada que depurar en tus datos.
- `merge` con `how="outer"` no rellena con ceros: rellena con nulos. Contar los nulos resultantes es
  la forma rápida de comprobar si una unión ha dejado huecos.
:::

:::truco
Cuando el mensaje de error no te diga nada, busca su texto literal junto al nombre de la función
(`ValueError read_csv pandas`). El mensaje es un identificador único y suele llevar a la página de la
referencia o a una nota de la versión, que es exactamente donde está la causa.
:::

## Errores típicos

- **Buscar la frase de tu tarea en vez del nombre del objeto.** «¿Cómo quito las filas duplicadas?»
  encuentra entradas de blog; `DataFrame.drop_duplicates` encuentra el contrato. La documentación
  está indexada por nombres, no por intenciones.
- **Leer la documentación de la última versión.** Si tienes una versión anterior, un parámetro que
  ahí aparece puede no existir en la tuya, y el error que recibirás no dirá «es de otra versión».
  Consulta el selector de versión de la web.
- **Quedarse en el tutorial.** El tutorial es un camino que funciona con datos limpios. No avisa de
  los nulos, ni de los duplicados, ni de las columnas que se llaman igual, que es donde te vas a
  chocar en el trabajo.
- **Copiar el ejemplo tal cual.** Los ejemplos definen su propio `df` dos líneas antes y no llevan
  control de errores. Si copias desde la mitad, estás usando variables que no existen y no te has
  enterado de qué datos suponía.
- **No leer la sección de notas.** Es donde se avisa de que un parámetro devuelve una vista, de que
  los nulos se ignoran al sumar o de que la operación duplica filas. Suele ser lo único de la página
  que no se deduce de la firma.
- **Fiarse de un foro o de un asistente sin comprobarlo.** La respuesta puede ser de otra versión o de
  otra librería, y sonar convincente. La documentación no es la única fuente, pero sí la única que se
  puede comprobar contra el comportamiento.
- **Buscar en la web lo que está en el propio paquete.** `help(objeto)` y las docstrings funcionan sin
  conexión, son de tu versión exacta y están siempre a una línea de distancia.

## Comprueba que lo sabes

:::quiz
p: Necesitas saber si `read_csv` puede leer un fichero por trozos. ¿Dónde lo buscas primero?
o: En el tutorial de introducción, que explica el uso básico
o: En la referencia de `read_csv`, mirando los parámetros y su valor por defecto
o: En un foro, preguntando si se puede
a: 2
e: La referencia es el contrato: si existe un parámetro para eso, aparece ahí con su nombre y su valor por defecto, junto al que ya conocías. El tutorial no cubre casos avanzados y un foro tarda más y puede hablar de otra versión.
:::

:::quiz
p: Copias un ejemplo de la documentación y al ejecutarlo sale un `NameError` con una variable que no has definido. ¿Qué ha pasado?
o: Que la documentación tiene un error y el ejemplo no funciona
o: Que has copiado un fragmento: el ejemplo define sus datos en las líneas de arriba, que no has traído
o: Que falta instalar una librería que el ejemplo usa
a: 2
e: Los ejemplos de la documentación son fragmentos mínimos pensados para leerse enteros, con sus datos definidos justo antes. Un NameError apunta a un nombre que no existe en tu programa, no a un fallo de la librería; y si faltara un módulo el error sería ModuleNotFoundError.
:::

:::quiz
p: ¿Qué miras de una firma antes de usar una función que no conoces?
o: Los parámetros obligatorios, los valores por defecto que te afectan, el tipo de valor devuelto y las excepciones
o: Solo el nombre de la función y el módulo del que viene
o: La fecha en la que se añadió la función al proyecto
a: 1
e: La firma es el contrato: sin los obligatorios la llamada no compila, los valores por defecto son el comportamiento que tendrás sin escribir nada, y saber qué devuelve y qué excepciones lanza es lo que evita depurar a ciegas. La fecha de alta solo importa si sospechas de un problema de versión.
:::

:::practica
enunciado: Quieres quedarte con las claves que están en una tabla o en la otra, pero no en las dos a la vez. Con `izquierda` con identificadores 1, 2 y 3 y `derecha` con 1, 2 y 4, describe qué consultas haces a la referencia, qué llamada escribes, qué resultado esperas y cómo lo compruebas.
pista: `how` acepta cuatro valores de unión, y ninguno de ellos es «solo las que no coinciden» por sí solo. Piensa en qué combinación de dos uniones da el resultado.
solucion: En la referencia de `DataFrame.merge` se ve que `how` acepta `left`, `right`, `outer`, `inner`, `cross` y, en versiones recientes, las uniones «anti» `left_anti` y `right_anti`. Con eso hay dos caminos. El primero, una unión completa filtrada: `izquierda.merge(derecha, on="id", how="outer", indicator=True)` devuelve 4 filas con la columna `_merge`; quedarse con las que no valen `both` deja el identificador 3 y el 4, es decir 2 filas. El segundo, dos uniones anti: `izquierda.merge(derecha, on="id", how="left_anti")` deja una fila (el 3), `right_anti` deja la otra (el 4) y la respuesta son 2 filas entre las dos. Se comprueba contando filas antes y después y mirando que no quede ningún `both`, que es más rápido que revisar la tabla entera a ojo.
:::

:::nota
Documentar lo que aprendes es la otra mitad de leer documentación: lo que te costó encontrar en la
referencia es exactamente lo que conviene anotar con tus palabras, porque la próxima vez lo buscarás
con las tuyas y no con las del autor.
:::
