---
id: tipos-y-estructuras-python
titulo: Tipos y estructuras de Python
fase: 3
nivel: básico
rutas: [de, ds, core]
prerequisitos: [entorno-python]
tags: [python, estructuras, coste]
resumen: Listas, tuplas, diccionarios y conjuntos guardan varios valores; elegir mal no rompe el programa, lo hace lento o lo llena de errores silenciosos.
fuentes: ["Ramalho (2022), 'Fluent Python', 2.ª edición"]
---

## En una frase

Una lista es una secuencia que puedes cambiar, una tupla es una secuencia que no, un diccionario
asocia cada clave con un valor y un conjunto guarda valores únicos sin orden; la diferencia
práctica está en que buscar dentro de una lista recorre todos los elementos y buscar en un
diccionario o un conjunto es casi instantáneo.

## La idea

Piensa en cuatro formas de organizar lo mismo. Una **lista** es una fila de cajas numeradas: el
orden importa, puedes añadir una caja al final, cambiar lo que hay dentro y acceder a la caja 37 sin
tocar las demás. Una **tupla** es la misma fila pero con las cajas selladas: se usa para registros
que no deben cambiar, como una coordenada `(40.4168, -3.7038)` o una fila de una consulta.

Un **diccionario** no guarda posiciones, guarda etiquetas: le das una clave y te devuelve su valor.
«Busca el precio del producto A-1042» es una operación de diccionario. Desde Python 3.7 los
diccionarios además recuerdan el orden en que se insertaron las claves, pero eso es una comodidad
para leerlos, no su propósito: no están ordenados alfabéticamente ni por valor.

Un **conjunto** es un diccionario sin valores: solo claves, todas distintas y sin orden. Su utilidad
es doble: eliminar duplicados y responder «¿está esto aquí?» muy rápido.

Y esa es la idea que conviene interiorizar desde el principio, porque es la que decide si tu script
tarda un segundo o diez minutos. Cuando escribes `x in mi_lista`, Python compara `x` con el primer
elemento, luego con el segundo y así hasta encontrarlo o llegar al final: si la lista tiene un
millón de elementos y `x` no está, son un millón de comparaciones. Cuando escribes `x in mi_set`,
Python calcula un número a partir de `x` (su *hash*) y va directamente a la casilla donde debería
estar. Es la diferencia entre buscar un libro hojeando la biblioteca entera y buscarlo por su
signatura.

La otra idea es la **mutabilidad**, y aquí está el error que más tiempo hace perder a quien empieza:
en Python, asignar no copia. Si escribes `b = a`, `b` y `a` son dos nombres para la misma lista;
cambiar una cambia la otra. Para tener una lista independiente hay que copiarla (`a[:]`,
`list(a)`, `a.copy()`), y esa copia es **superficial**: si la lista contiene listas, la copia
comparte esas listas interiores. El detalle completo está en [[vistas-y-copias]], pero la regla
mental es: `=` comparte, `[:]` copia un nivel, `copy.deepcopy` copia todo.

Una consecuencia de la mutabilidad es que no todo puede ser clave de diccionario. Las claves deben
ser **hashables**, es decir, no pueden cambiar después de insertarse: valen números, cadenas y
tuplas de cosas inmutables; no valen listas ni diccionarios. Por eso `{("madrid", "norte"): 120}`
funciona y `{[1, 2]: 120}` lanza un error inmediato y muy explicativo.

Por último, cuándo usar cada una: si el orden importa y vas a añadir o quitar elementos, lista; si
es un registro fijo de campos, tupla; si vas a buscar por una etiqueta, diccionario; si te importa
la pertenencia o no quieres repetidos, conjunto.

## Definición formal

- **Secuencia** — colección ordenada con acceso por posición (índice entero, desde 0).
- **Mutable** — el objeto se puede modificar después de creado. Las listas, los diccionarios y los
  conjuntos lo son; las tuplas y las cadenas no.
- **Hashable** — objeto que tiene un valor de dispersión estable y puede usarse como clave de
  diccionario o elemento de conjunto.
- **`O(·)`** — cota asintótica del coste: `O(n)` significa que el número de operaciones crece
  proporcionalmente al tamaño, `O(1)` que no depende de él ([[complejidad-asintotica]]).

| Estructura | Orden | Se modifica | Clave de diccionario | Acceso por posición | Pertenencia |
| --- | --- | --- | --- | --- | --- |
| `list` | sí, el de inserción | sí | no | `O(1)` | `O(n)` |
| `tuple` | sí, el de inserción | no | sí, si sus elementos lo son | `O(1)` | `O(n)` |
| `dict` | orden de inserción de claves | sí | es el contenedor de claves | por clave, `O(1)` de media | `O(1)` de media |
| `set` | no definido | sí | no | no hay | `O(1)` de media |

El contrato que hace posible esa velocidad, para dos objetos cualesquiera `a` y `b`, es este:

:::formula
a == b   ⟹   hash(a) == hash(b)
:::

La implicación va en un solo sentido: dos objetos distintos pueden compartir hash (una *colisión*,
que el diccionario resuelve comparando). Lo que no puede pasar es que dos objetos iguales tengan
hashes distintos, porque entonces el diccionario los buscaría en casillas diferentes y no los
encontraría. De ahí que las claves tengan que ser inmutables: si una clave cambiara, su hash
cambiaría y el valor quedaría perdido dentro de la tabla.

## Ejemplo

Una lista de identificadores con repeticiones:

```
7  3  7  9  3  7  12  9
```

- Tamaño de la lista: 8 elementos.
- Como conjunto: `{3, 7, 9, 12}`, cuatro valores distintos. El conjunto elimina las cuatro
  repeticiones sin que tengas que escribir nada.
- Frecuencias contadas con un diccionario: el 7 aparece 3 veces, el 3 dos veces, el 9 dos veces y el
  12 una vez. La suma de frecuencias es 8, como el tamaño de la lista.
- Pertenencia del 12: en la lista hay que recorrer 8 posiciones hasta encontrarlo al final; en el
  conjunto, un cálculo de hash y una comparación.

Con 8 elementos la diferencia es ridícula. Con un millón, comprobar la pertenencia de 10.000
elementos pasa de 10.000 millones de comparaciones a 10.000 operaciones: el mismo programa, escrito
con `set` en lugar de `list`, termina en segundos en vez de en horas.

## Código

```python verificable
# b = a NO copia: los dos nombres apuntan a la misma lista
a = [1, 2, 3]
b = a
b.append(4)
print("a tras b.append(4):", a)   # -> a tras b.append(4): [1, 2, 3, 4]

# [:] si crea una lista nueva (copia superficial, un solo nivel)
c = a[:]
c.append(5)
print("a tras c.append(5):", a)   # -> a tras c.append(5): [1, 2, 3, 4]
print("c:", c)                    # -> c: [1, 2, 3, 4, 5]
```

```python verificable
ids = [7, 3, 7, 9, 3, 7, 12, 9]

print("elementos en la lista:", len(ids))       # -> elementos en la lista: 8
print("ids distintos:", sorted(set(ids)))       # -> ids distintos: [3, 7, 9, 12]

conteo = {}
for i in ids:
    conteo[i] = conteo.get(i, 0) + 1
print("frecuencias:", dict(sorted(conteo.items())))   # -> frecuencias: {3: 2, 7: 3, 9: 2, 12: 1}

# Una tupla de valores inmutables si puede ser clave de diccionario
stock = {("madrid", "norte"): 120, ("madrid", "sur"): 80}
print("stock madrid norte:", stock[("madrid", "norte")])   # -> stock madrid norte: 120

# El argumento por defecto se crea UNA sola vez y se comparte entre llamadas
def anade(x, acumulado=[]):
    acumulado.append(x)
    return acumulado

print("primera llamada:", anade(1))   # -> primera llamada: [1]
print("segunda llamada:", anade(2))   # -> segunda llamada: [1, 2]

# La solucion: valor por defecto None y la lista se crea dentro de la funcion
def anade_bien(x, acumulado=None):
    acumulado = [] if acumulado is None else acumulado
    acumulado.append(x)
    return acumulado

print("con None:", anade_bien(1), anade_bien(2))   # -> con None: [1] [2]
```

```python ilustrativo
# Por que importa la estructura: coste de comprobar pertenencia
#   lista de 1.000.000 de ids -> hasta 1.000.000 de comparaciones
#   set   de 1.000.000 de ids -> 1 calculo de hash y 1 comparacion
# Regla practica: si vas a preguntar "esta esto?" muchas veces, construye
# un set al principio y no una lista que recorres en cada iteracion.
```

## Errores típicos

- **Creer que `b = a` copia.** No copia: comparte. Cambiar `b` cambia `a` y el error aparece lejos
  de su causa. Usa `a[:]` o `a.copy()` para una copia de un nivel, y `copy.deepcopy` para
  estructuras anidadas ([[vistas-y-copias]]).
- **Usar una lista para buscar una y otra vez.** `if x in lista` dentro de un bucle es la receta
  clásica del programa que tarda horas. Convierte la lista en `set` o en `dict` y la búsqueda pasa a
  ser prácticamente gratis.
- **Intentar meter una lista como clave de diccionario.** Lanza `TypeError: unhashable type: 'list'`.
  Si necesitas una clave compuesta, usa una tupla de elementos inmutables.
- **Modificar una lista mientras la recorres.** Al borrar elementos durante el `for` te saltas
  posiciones, y en un diccionario Python lanza `RuntimeError`. Recorre una copia o construye la
  lista nueva con una comprensión.
- **Usar un valor mutable como argumento por defecto.** `def f(x, acumulado=[])` comparte la misma
  lista entre todas las llamadas, como se ve en el bloque de arriba. El valor por defecto debe ser
  `None` y crear la lista dentro de la función.
- **Confundir `is` con `==`.** `==` compara valores; `is` compara identidad, es decir, si son el
  mismo objeto en memoria. Que `a is b` sea verdadero para dos enteros pequeños es un detalle de
  implementación, no algo con lo que puedas contar.

:::practica
enunciado: Dada `ids = [11, 4, 11, 7, 4, 11, 30]`, escribe el código que imprime cuántos elementos tiene la lista, los distintos ordenados, la frecuencia de cada uno y la pertenencia de 30 y de 99. Usa la estructura adecuada para cada cosa y di qué coste tiene cada búsqueda.
pista: El conjunto quita duplicados y responde a la pertenencia; el diccionario acumula el conteo.
solucion: `print(len(ids))` da 7. `sorted(set(ids))` da `[4, 7, 11, 30]`. El conteo con `conteo[i] = conteo.get(i, 0) + 1` da `{4: 2, 7: 1, 11: 3, 30: 1}`. Con `s = set(ids)`, `30 in s` es `True` y `99 in s` es `False`. Buscar el 99 en la lista recorre sus 7 posiciones; en el conjunto son un cálculo de hash y una comparación.
:::

## Comprueba que lo sabes

:::quiz
p: Tienes una lista de un millón de identificadores y necesitas comprobar 10.000 veces si un id está presente. ¿Qué haces?
o: Recorrer la lista con un bucle y comparar uno a uno
o: Convertirla a un set y comprobar la pertenencia, porque la búsqueda pasa de O(n) a O(1) de media
o: Ordenar la lista antes de cada comprobación
a: 2
e: La pertenencia en una lista recorre los elementos hasta encontrarlo, así que 10.000 comprobaciones sobre un millón de elementos son del orden de 10.000 millones de comparaciones. Un set usa el hash y resuelve cada comprobación en tiempo constante. Ordenar no ayuda si lo haces en cada consulta.
:::

:::quiz
p: Ejecutas a = [1, 2, 3]; b = a; b.append(4). ¿Qué vale a?
o: [1, 2, 3], porque la asignación copia la lista
o: [1, 2, 3, 4], porque a y b son dos nombres del mismo objeto
o: Da un error porque la lista está en uso
a: 2
e: La asignación en Python no copia: liga un segundo nombre al mismo objeto. Para tener una lista independiente hay que copiarla con a[:] o a.copy(), y esa copia es superficial: los elementos mutables que contenga seguirán compartidos.
:::

:::quiz
p: ¿Por qué una lista no puede ser clave de un diccionario pero una tupla sí?
o: Porque las tuplas ocupan menos memoria
o: Porque las claves deben ser hashables y una lista, al poder cambiar, no puede tener un hash estable
o: Porque el diccionario ordena las claves alfabéticamente y las listas no se pueden ordenar
a: 2
e: El diccionario localiza una clave por su hash; si la clave cambiara después de insertarla, su hash cambiaría y el valor quedaría inencontrable. Las tuplas de elementos inmutables son hashables y sirven como clave compuesta. El tamaño y el orden no tienen nada que ver.
:::
