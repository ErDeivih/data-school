---
id: comprensiones-y-generadores
titulo: Comprensiones y generadores
fase: 3
nivel: básico
rutas: [core, de, ds]
prerequisitos: [funciones-y-modulos, tipos-y-estructuras-python]
tags: [python, comprensiones, generadores, perezoso]
resumen: Las comprensiones construyen listas y diccionarios en una línea; los generadores producen los valores de uno en uno y no gastan memoria aunque pidas millones.
fuentes: ["Ramalho (2022), 'Fluent Python', 2.ª edición, caps. 2 y 17"]
---

## En una frase

Una comprensión es un bucle que construye la colección entera de golpe; un generador es una función
que va soltando los valores de uno en uno con `yield`, así que puedes recorrer un millón de
elementos gastando la memoria de uno solo.

## La idea

Escribe el mismo trabajo de dos formas. La primera, con un bucle y un `append`: creas una lista
vacía, recorres los elementos, calculas, añades. Funciona, pero son cuatro líneas para decir una
idea. La segunda es una **comprensión** y dice lo mismo en una línea: `[x * x for x in range(10)]`.
Se lee casi como el español («el cuadrado de cada x, para las x de 0 a 9») y, de propina, se ejecuta
antes porque el bucle ocurre dentro del intérprete y no en tu bytecode.

La comprensión está construida con tres piezas: la **expresión** que se calcula (`x * x`), el
**bucle** que recorre (`for x in range(10)`) y el **filtro** opcional que descarta
(`if x % 2 == 0`). Cambiando los corchetes por llaves obtienes un diccionario (`{clave: valor for
...}`) o un conjunto (`{valor for ...}`), y el mismo patrón sirve para agrupar, contar o limpiar.

Con la memoria, la comprensión tiene un problema: construye **todo** antes de que puedas usar el
primer elemento. Si pides los cuadrados del 1 al millón, tienes un millón de enteros en memoria a la
vez. Y muchas veces no quieres los valores, quieres recorrerlos: sumarlos, escribirlos, contar
cuántos cumplen algo. Guardarlos es un desperdicio.

Ahí entra el **generador**. Un generador es una función que en vez de `return` usa `yield`: cuando
el bucle de fuera le pide el siguiente valor, la función se ejecuta hasta el `yield`, entrega ese
valor y **se queda congelada** con sus variables y el punto por donde iba. En la siguiente vuelta
continúa desde ahí. Esto se llama **evaluación perezosa**: nada se calcula hasta que alguien lo
pide. La diferencia de memoria es brutal y se puede medir: una lista con un millón de enteros ocupa
unos 8 megas; el generador equivalente, unos doscientos bytes, y no crece con el número de
elementos.

Y como es perezoso, puedes describir cosas infinitas. `(x for x in itertools.count())` es una
expresión que representa todos los números naturales sin calcular ninguno. El que consume decide
cuándo parar.

Dos pegas que conviene saber antes de enamorarse. La primera: **un generador se agota**. No es una
colección que puedas recorrer dos veces; cuando termina, `next` lanza `StopIteration` para siempre.
La segunda: la expresión generadora **fija su iterable en la línea donde se crea**, no cuando la
recorres. Si después reasignas esa variable a otra lista, el generador sigue con la antigua; si lo
que haces es modificarla en el sitio (añadir un elemento), el generador nuevo sí lo ve. La
comprensión, en cambio, materializa los valores en el momento y no le afecta nada de eso.

El tercer concepto, que hace que todo esto encaje, es el **iterador**: un objeto con `__next__` que
recuerda por dónde va y avisa del final con `StopIteration`. Comprensiones, generadores, ficheros y
listas producen iteradores, y el `for` de Python no es más que azúcar sobre `next()` repetido. Por
eso puedes recorrer un fichero de 10 GB línea a línea sin cargarlo en memoria: nunca tienes las
líneas a la vez, solo la corriente.

## Definición formal

Las dos sintaxis, una con memoria y otra sin ella:

:::formula
[ expresión for elemento in iterable if condición ]        ← lista, materializa todo
:::

:::formula
( expresión for elemento in iterable )      ← generador, produce uno a uno
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube / cambia… |
| --- | --- | --- | --- |
| `expresión` | Lo que se calcula para cada elemento: es lo que acaba en la colección | las del resultado | Más cálculo por elemento es tiempo que se paga en cada vuelta, también en el generador |
| `elemento` | El nombre que va tomando cada valor del iterable | las del dato | Solo vive dentro de la comprensión: no existe después, y no puede chocar con el de fuera |
| `iterable` | De dónde salen los elementos: lista, rango, fichero, generador | — | `range(n)` no reserva memoria; una lista de `n` sí |
| `condición` | Filtro opcional: solo pasan los elementos que lo cumplen | booleano | Cuanto más estricta, menos elementos llegan y menos trabajo posterior |
| `yield` | Devuelve un valor y congela la función hasta el siguiente `next` | — | Cada `yield` es un punto de pausa; `return` dentro de un generador lo termina |
| `n` | Número de elementos que pides | elementos | La lista ocupa memoria proporcional a `n`; el generador, constante |
| `StopIteration` | La excepción con la que un iterador avisa de que se acabó | — | El `for` la captura solo; si llamas a `next()` a mano, la ves tú |
| `itertools.islice` | Corta los primeros `k` valores de un iterador sin agotarlo del todo | elementos | Es la forma de consumir un generador infinito sin bloquear el programa |
:::

## Ejemplo

Para un millón de cuadrados, medido con `sys.getsizeof`:

```
lista      -> 8 448 728 bytes (8,1 MB)   y los tienes todos a la vez
generador  ->       200 bytes            y todavía no se ha calculado ninguno
```

El generador no ha calculado nada al crearse: el primer valor sale en el primer `next()`. Y de un
generador que representa todos los naturales, pedir los cinco primeros pares cuesta cinco vueltas:

```
list(islice((x for x in count() if x % 2 == 0), 5))  ->  [0, 2, 4, 6, 8]
```

La segunda llamada a `next` sobre el mismo generador no vuelve a dar 0: da 1. El generador recuerda
por dónde iba, y cuando se acaba, `next` lanza `StopIteration` para siempre.

:::figura
fichero: comprensiones-y-generadores-memoria
pie: El eje vertical está en escala logarítmica, así que cada salto es un factor de diez. La línea roja (la lista) crece en línea recta con el número de elementos; la verde (el generador) es plana: da igual pedir 200.000 que dos millones. La conclusión práctica: si solo vas a recorrer los valores una vez, no los guardes en una lista.
fuente: figuras/comprensiones-y-generadores-1.py
:::

## Código

```python verificable
import sys

# Lista por comprension: se calcula y se guarda todo de golpe
cuadrados_lista = [x * x for x in range(1_000_000)]
# Expresion generadora: NO calcula nada hasta que se lo pides
cuadrados_gen = (x * x for x in range(1_000_000))

print("lista:", sys.getsizeof(cuadrados_lista))          # -> lista: 8448728
print("generador:", sys.getsizeof(cuadrados_gen))        # -> generador: 200
print("primeros tres:", [next(cuadrados_gen) for _ in range(3)])   # -> primeros tres: [0, 1, 4]

# Diccionario por comprension: de nombre a lista de precios
filas = [("pan", 3.5), ("vino", 9.0), ("pan", 2.0)]
por_categoria = {c: [v for n, v in filas if n == c] for c in {n for n, _ in filas}}
print("categorias:", sorted(por_categoria))              # -> categorias: ['pan', 'vino']
print("pan:", por_categoria["pan"])                      # -> pan: [3.5, 2.0]
```

:::claves
- La lista y el generador se escriben casi igual, pero la lista ya ha hecho todo el trabajo al
  crearse y el generador no ha calculado nada todavía: el primer valor se paga en el primer
  `next()`. `sys.getsizeof` mide **el contenedor**, no lo que ocupan los elementos que apunta.
- `sys.getsizeof(cuadrados_lista)` da millones de bytes porque mide la lista de punteros; los
  enteros que contiene van aparte. Aun así la comparación vale: el generador no guarda ni punteros.
- El nombre `x` de la comprensión vive solo dentro de los corchetes. Escribir `[x * x for x in
  range(3)]` y después `print(x)` da `NameError` en Python 3 (en Python 2 se filtraba y era una
  fuente inagotable de errores).
- La expresión generadora **fija su iterable en el momento de crearla**, no al recorrerla: si la
  construyes sobre una variable y luego la reasignas, el generador sigue viendo la lista antigua.
  Lo que sí ve es una modificación en el sitio de esa misma lista (un `append`), porque el iterable
  es el mismo objeto. Con una comprensión de lista te quedas con los valores de entonces.
- Un generador **se agota**: la cuarta llamada a `next(cuadrados_gen)` seguiría dando 9, pero si
  recorres el generador entero y vuelves a pedir, sale `StopIteration`. No es una lista reutilizable.
- `sys.getsizeof` del generador puede variar unas decenas de bytes entre versiones de Python; lo que
  no varía nunca es que no depende del número de elementos que le pidas.
:::

```python verificable
# yield convierte la funcion en una fabrica de valores perezosa
def cuenta_atras(desde):
    print("empieza el generador")
    while desde > 0:
        yield desde
        desde -= 1
    print("se acabo")

generador = cuenta_atras(3)
print("creado, sin ejecutar nada")     # -> creado, sin ejecutar nada: nada se ha impreso del generador
print("primero:", next(generador))     # -> empieza el generador
                                       # -> primero: 3
print("resto:", list(generador))       # -> se acabo
                                       # -> resto: [2, 1]
```

```python verificable
import itertools

# Perezoso: el rango es infinito y no se materializa nada hasta que se pide
pares = (x for x in itertools.count() if x % 2 == 0)
print("cinco pares:", list(itertools.islice(pares, 5)))     # -> cinco pares: [0, 2, 4, 6, 8]

# Un fichero de texto tambien es un iterador: se recorre linea a linea
lineas = ["a,1", "b,2", "c,3"]
pares_clave_valor = {clave: int(valor) for clave, valor in (l.split(",") for l in lineas)}
print("leido:", pares_clave_valor)                          # -> leido: {'a': 1, 'b': 2, 'c': 3}

# Un generador agotado no se reinicia: la segunda vuelta devuelve una lista vacia
agotado = (n for n in range(3))
print("primera vuelta:", list(agotado))                     # -> primera vuelta: [0, 1, 2]
print("segunda vuelta:", list(agotado))                     # -> segunda vuelta: []
```

## Errores típicos

- **Recorrer un generador dos veces.** La segunda vez no da error: da una lista vacía, que es peor,
  porque el fallo se descubre tres pasos después. Si necesitas dos pasadas, materialízalo con
  `list(...)` o vuelve a crear el generador.
- **Poner un generador dentro de `len()` o indexarlo.** Un generador no tiene longitud ni
  posiciones: no sabe cuántos elementos quedan. `len(gen)` lanza `TypeError`; para contar hay que
  consumirlo (`sum(1 for _ in gen)`) y entonces ya no puedes recorrerlo otra vez.
- **Comprobaciones de pertenencia dentro de una comprensión sobre una lista.** `if x in lista`
  dentro del filtro convierte la comprensión en un bucle cuadrado: para cada elemento recorre la
  lista entera. Convierte la lista en un `set` antes y la comprobación pasa a ser casi instantánea
  ([[tipos-y-estructuras-python]]).
- **Comprensiones anidadas de tres niveles para aplanar matrices.** Se puede, pero se lee fatal. Si
  necesitas más de dos `for`, escribe el bucle: la comprensión es para cuando cabe en una línea
  legible.
- **Efectos secundarios dentro de una comprensión.** `[imprime(x) for x in datos]` funciona, pero
  engaña: estás usando una construcción que devuelve una lista para hacer algo que no construye
  nada. Usa un `for` normal, y si solo quieres el efecto, un generador consumido a propósito.
- **Creer que el generador ejecuta su código al llamarlo.** `g = mi_generador()` no ejecuta ni una
  línea; el cuerpo arranca en el primer `next`. Por eso un error dentro del generador aparece lejos
  de la línea que lo creó, y por eso el depurador de [[errores-y-depuracion]] parece saltarse líneas.
- **Pasar un generador a una función que lo recorre dos veces.** Muchas funciones de pandas o de
  validación lo consumen y luego intentan recorrerlo otra vez: la segunda pasada está vacía. Cuando
  el consumidor no sea tuyo, pasa una lista.

:::practica
enunciado: De la lista `ventas = [("norte", 120), ("sur", 80), ("norte", 200), ("este", 50)]` saca, con comprensiones y generadores: los importes mayores de 100, un diccionario de zona a total facturado y el total general sin construir ninguna lista intermedia. Explica qué has ganado en el tercer caso.
pista: Para el diccionario necesitas las zonas distintas primero; para el total, `sum()` acepta un generador directamente y no guarda nada.
solucion: `[v for _, v in ventas if v > 100]` da `[120, 200]`. Las zonas se obtienen con `{z for z, _ in ventas}` y el diccionario con `{z: sum(v for zz, v in ventas if zz == z) for z in zonas}`, que da `{'sur': 80, 'este': 50, 'norte': 320}`. El total es `sum(v for _, v in ventas)`, o sea 450. En el tercer caso `sum` va consumiendo el generador y descartando cada valor, así que la memoria no depende del número de filas; con una lista intermedia habrías guardado todas las ventas para sumarlas y tirarlas.
:::

## Comprueba que lo sabes

:::quiz
p: `g = (x * x for x in range(4))`. ¿Qué imprime `print(list(g))` seguido de `print(list(g))`?
o: `[0, 1, 4, 9]` y otra vez `[0, 1, 4, 9]`
o: `[0, 1, 4, 9]` y luego `[]`, porque el generador ya se agotó
o: Un `TypeError`, porque un generador no se puede convertir en lista
a: 2
e: Un generador es un iterador que se consume: la primera `list` lo recorre entero, la segunda lo encuentra terminado y devuelve una lista vacía sin lanzar error. Si necesitas dos pasadas, guarda `list(g)` en una variable.
:::

:::quiz
p: ¿Cuándo se ejecuta el código de una función que contiene `yield`?
o: Al llamar a la función, en la línea de la llamada
o: En el primer `next()` sobre el generador, y se pausa en cada `yield`
o: Al terminar el programa, cuando Python libera la memoria
a: 2
e: Llamar a la función solo crea el objeto generador; el cuerpo no se ejecuta hasta que alguien pide el primer valor con `next()` o con un `for`. A partir de ahí avanza de `yield` en `yield`, conservando las variables locales entre pausas.
:::

:::quiz
p: Tienes un fichero de 10 GB y quieres sumar una columna. ¿Por qué `sum(int(l.split(",")[2]) for l in open(ruta))` no se queda sin memoria?
o: Porque `open` carga el fichero en disco temporalmente
o: Porque el fichero se recorre línea a línea y el generador solo mantiene la línea actual
o: Porque `sum` comprime los datos antes de sumarlos
a: 2
e: Un fichero abierto es un iterador: entrega una línea cada vez y no guarda las anteriores. El generador convierte cada línea en un número y lo entrega a `sum`, que lo acumula y lo descarta. La memoria depende del tamaño de una línea, no del fichero. Lo que sí hay que hacer es cerrar el fichero, por ejemplo con un `with`.
:::
