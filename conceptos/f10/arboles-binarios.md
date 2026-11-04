---
id: arboles-binarios
titulo: Árboles binarios y de búsqueda
fase: 10
nivel: intermedio
rutas: [alg]
prerequisitos: [complejidad-asintotica, recursion-y-backtracking]
tags: [estructuras, arboles, busqueda, orden]
resumen: Jerarquías de nodos con dos hijos por nodo; ordenados como BST dan búsqueda logarítmica y, sobre todo, recorrido en orden y consultas por rango.
fuentes: ["Sedgewick y Wayne (2011), 'Algorithms', 4.ª ed., cap. 3", "Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 12"]
---

## En una frase

Un árbol binario es una jerarquía en la que cada nodo tiene como mucho dos hijos, y si además
se cumple que todo lo de la izquierda es menor que el nodo y todo lo de la derecha es mayor,
buscar cuesta proporcional a la altura del árbol y recorrerlo en orden devuelve los datos ya
ordenados sin ordenar nada.

## La idea

Imagina una guía telefónica en papel que en cada página te dijera: «si el apellido que buscas
va antes alfabéticamente que el de esta página, pasa a la mitad izquierda; si va después, a la
derecha». Abres por la mitad, descartas media guía, y repites. Con un millón de entradas
localizas cualquiera en unas 20 decisiones, porque cada paso divide el problema por dos. Eso es
un **árbol binario de búsqueda** (BST, del inglés *binary search tree*): una estructura donde
cada comparación descarta una rama entera.

Un árbol binario sin más es solo una forma de organizar datos jerárquicos: un organigrama, el
árbol de un DOM, la descomposición de una expresión matemática. Cada nodo tiene hasta dos
hijos, y eso es todo. El nodo del que cuelga todo se llama **raíz**; los nodos sin hijos,
**hojas**. La **altura** es el número de aristas del camino más largo de la raíz a una hoja, y
es la variable que manda: todas las operaciones cuestan O(altura).

Lo que convierte un árbol binario en una herramienta de búsqueda es la **propiedad de orden
BST**: para cualquier nodo, todas las claves de su subárbol izquierdo son menores que la suya y
todas las de su derecho son mayores. Con esa regla, buscar es repetir «menor: izquierda,
mayor: derecha», y el árbol se comporta como la [[busqueda-binaria]] pero permitiendo
inserciones y borrados sin recolocar un array entero.

Ahora la comparación incómoda con [[tablas-hash]]. Una tabla hash busca en O(1) de media y un
BST en O(log n): la tabla gana. Pero la tabla no sabe nada del orden de sus claves. Un BST te
da tres cosas que ninguna tabla hash da:

1. **Recorrido en orden**, que devuelve las claves ordenadas en O(n) sin llamar a ningún
   algoritmo de [[ordenacion]].
2. **Consultas por rango**: «dame todas las claves entre 40 y 60» es bajar por el árbol y
   podar las ramas que quedan fuera, sin recorrer lo que no hace falta.
3. **Vecinos ordenados**: el menor, el mayor, el siguiente y el anterior a una clave, en
   O(log n).

El precio de un BST sin más es su peor caso. Si insertas claves ya ordenadas (1, 2, 3, 4, 5…)
siempre a la derecha, el árbol se convierte en una lista: altura n, búsqueda O(n). Esa
degeneración es la razón de que existan los [[arboles-balanceados]], que garantizan altura
O(log n) a cambio de recolocar nodos en cada operación.

## Definición formal

Un árbol binario es una estructura recursiva: o está vacío, o es un nodo con una clave y dos
subárboles binarios, llamados izquierdo y derecho.

- `n` — número de nodos.
- `h` — altura: número de aristas del camino más largo de la raíz a una hoja. Un árbol con un
  solo nodo tiene h = 0.
- `raíz` — el único nodo sin padre.
- `hoja` — un nodo sin hijos.
- `subárbol izquierdo de x` — el árbol que cuelga del hijo izquierdo de `x`.

**Propiedad de orden BST.** Para todo nodo `x` con clave `k`: toda clave del subárbol izquierdo
de `x` es menor que `k`, y toda clave del subárbol derecho es mayor que `k`. Si se admiten
claves repetidas hay que fijar una convención (por ejemplo, **menores o iguales** a la
izquierda) y respetarla en todo el código, porque la definición estricta no dice dónde van las
iguales.

Costes en función de la altura `h`:

| Operación | Coste |
| --- | --- |
| Buscar | O(h) |
| Insertar | O(h) |
| Borrar | O(h) |
| Mínimo y máximo | O(h) |
| Sucesor y precesor | O(h) |
| Recorrido en orden | O(n) |
| Consulta por rango [a, b] | O(h + k), con k claves devueltas |

Cota de la altura:

- **Mejor caso (árbol completo):** h = ⌊log₂ n⌋, y entonces buscar es O(log n).
- **Peor caso (árbol degenerado):** h = n − 1, y buscar es O(n).
- Con n nodos, un árbol binario cualquiera siempre cumple h ≥ ⌊log₂ n⌋.

**Recorridos.** Los tres recorridos en profundidad se distinguen por cuándo se visita el nodo
respecto a sus subárboles:

- **Preorden** (nodo, izquierda, derecha) — sirve para copiar o serializar el árbol.
- **En orden** (izquierda, nodo, derecha) — en un BST devuelve las claves ordenadas.
- **Postorden** (izquierda, derecha, nodo) — sirve para liberar memoria o evaluar expresiones.

Añadiendo un recorrido **por niveles** (primero la raíz, luego toda su generación, luego la
siguiente) se completa la familia; ese es el que usa [[bfs-y-dfs]].

:::figura
fichero: arboles-binarios-forma-y-coste
pie: A la izquierda, comparaciones hasta encontrar la clave en un árbol equilibrado (unos log₂ n, veinte con un millón de claves) y en uno degenerado (media lista, quinientas mil): 25.000 veces de diferencia. A la derecha, los dos árboles dibujados con las mismas siete claves; uno mide 3 niveles y el otro 6, y buscar la última cuesta siete comparaciones. El recorrido in-order devuelve las claves ordenadas en los dos casos: lo que cambia con el orden de inserción es la forma y el coste, no el orden.
fuente: figuras/arboles-binarios-1.py
:::

## Ejemplo

Insertamos en este orden las claves 50, 30, 70, 20, 40, 60, 80. Como cada nueva clave cae
siempre en una hoja, el árbol queda completo y con 3 niveles:

```
            50
          /    \
        30      70
       /  \    /  \
     20    40 60    80
```

- Altura: h = 2. Con n = 7 nodos, el mínimo posible es ⌊log₂ 7⌋ = 2, así que este árbol es
  óptimo en altura.
- Buscar 40: 40 < 50 → izquierda; 40 > 30 → derecha; 40 = 40 → encontrado. **2 comparaciones**
  más la de la raíz, es decir 3.
- Mínimo: bajar siempre a la izquierda → 20. Máximo: siempre a la derecha → 80.
- Recorrido en orden: 20, 30, 40, 50, 60, 70, 80. Ordenado, y no hemos ordenado nada.

Ahora insertamos las mismas claves ya ordenadas: 20, 30, 40, 50, 60, 70, 80. Cada una es mayor
que la anterior, así que todas bajan por la derecha:

```
20
  \
   30
     \
      40
        \
         50
           \
            60
              \
               70
                 \
                  80
```

Altura h = 6 con n = 7 nodos: es una lista disfrazada. Buscar 80 cuesta 7 comparaciones, y
buscar una clave que no está cuesta 7 para descubrir que no está. El mismo conjunto de claves,
dos formas de insertarlo, y costes que pasan de O(log n) a O(n). Guardar el árbol «equilibrado»
es exactamente el trabajo de los [[arboles-balanceados]].

## Código

```python verificable
class Nodo:
    __slots__ = ("clave", "izq", "der")

    def __init__(self, clave):
        self.clave, self.izq, self.der = clave, None, None

def insertar(raiz, clave):
    """Inserta respetando la propiedad BST y devuelve la raiz del subarbol."""
    if raiz is None:
        return Nodo(clave)
    if clave < raiz.clave:
        raiz.izq = insertar(raiz.izq, clave)
    elif clave > raiz.clave:
        raiz.der = insertar(raiz.der, clave)
    return raiz   # clave duplicada: se ignora a proposito

def en_orden(raiz):
    """Izquierda, nodo, derecha: en un BST sale ordenado."""
    if raiz is None:
        return []
    return en_orden(raiz.izq) + [raiz.clave] + en_orden(raiz.der)

def altura(raiz):
    if raiz is None:
        return -1                      # el arbol vacio tiene altura -1 por convenio
    return 1 + max(altura(raiz.izq), altura(raiz.der))

raiz = None
for k in (50, 30, 70, 20, 40, 60, 80):
    raiz = insertar(raiz, k)

print("en orden:", en_orden(raiz))   # -> en orden: [20, 30, 40, 50, 60, 70, 80]
print("altura:", altura(raiz))       # -> altura: 2
```

:::claves
- `altura(None)` devuelve **−1**, no 0, y por eso un árbol de un solo nodo mide 0. Ese convenio es el que hace que `1 + max(...)` funcione sin casos especiales. Con el árbol vacío devolviendo 0, todo mediría un nivel de más.
- `__slots__` en la clase `Nodo` evita el diccionario interno de cada objeto: con un millón de nodos, eso es menos memoria y menos saltos. Cambiar `__slots__` por atributos normales no rompe el código, solo lo engorda.
- La inserción es **recursiva y devuelve la raíz del subárbol**: `raiz.izq = insertar(raiz.izq, clave)`. Si te olvidas de reasignar, el árbol se construye en el aire y `raiz` sigue teniendo `None` en los hijos.
- Con clave duplicada, `insertar` la ignora **en silencio** (no hay rama para `==`). Si necesitas contar repeticiones, la convención va en el `else` y hay que respetarla en todo el código.
- `en_orden` concatena listas con `+` en cada nivel: es O(n) en total pero crea listas intermedias. Con un acumulador pasado por parámetro o un generador se evita esa memoria extra.
- `comparaciones` es el nombre que tendría el contador si lo llevaras en la función
  `comparaciones` del bloque anterior: cuenta **una comparación por nodo visitado**, incluida la
  última que acierta. Buscar el 80 en el árbol equilibrado cuesta 3 y en el degenerado 7: la
  diferencia no está en el algoritmo, está en la forma.
:::

```python verificable
class Nodo:
    __slots__ = ("clave", "izq", "der")

    def __init__(self, clave):
        self.clave, self.izq, self.der = clave, None, None

def insertar(raiz, clave):
    if raiz is None:
        return Nodo(clave)
    if clave < raiz.clave:
        raiz.izq = insertar(raiz.izq, clave)
    elif clave > raiz.clave:
        raiz.der = insertar(raiz.der, clave)
    return raiz

def altura(raiz):
    if raiz is None:
        return -1
    return 1 + max(altura(raiz.izq), altura(raiz.der))

def comparaciones(raiz, objetivo):
    """Cuenta las comparaciones hasta encontrar la clave (o agotar el camino)."""
    n, actual = 0, raiz
    while actual is not None:
        n += 1
        if objetivo == actual.clave:
            return n
        actual = actual.izq if objetivo < actual.clave else actual.der
    return n

# Mismo conjunto de claves, dos ordenes de insercion
equilibrado = None
for k in (50, 30, 70, 20, 40, 60, 80):
    equilibrado = insertar(equilibrado, k)

degenerado = None
for k in (20, 30, 40, 50, 60, 70, 80):   # ya ordenadas: todas caen a la derecha
    degenerado = insertar(degenerado, k)

print("altura equilibrado:", altura(equilibrado))                  # -> altura equilibrado: 2
print("altura degenerado:", altura(degenerado))                    # -> altura degenerado: 6
print("comparaciones para el 80:", comparaciones(equilibrado, 80),
      comparaciones(degenerado, 80))                               # -> comparaciones para el 80: 3 7
```

```python verificable
# Consulta por rango: lo que un BST hace y una tabla hash no puede hacer sin ordenar antes.
class Nodo:
    __slots__ = ("clave", "izq", "der")

    def __init__(self, clave):
        self.clave, self.izq, self.der = clave, None, None

def insertar(raiz, clave):
    if raiz is None:
        return Nodo(clave)
    if clave < raiz.clave:
        raiz.izq = insertar(raiz.izq, clave)
    elif clave > raiz.clave:
        raiz.der = insertar(raiz.der, clave)
    return raiz

def rango(raiz, a, b, visitados=None):
    """Devuelve las claves en [a, b] podando las ramas que quedan fuera."""
    visitados = [0] if visitados is None else visitados
    if raiz is None:
        return []
    visitados[0] += 1
    if raiz.clave < a:                       # todo el subarbol izquierdo es menor que a
        return rango(raiz.der, a, b, visitados)
    if raiz.clave > b:                       # todo el subarbol derecho es mayor que b
        return rango(raiz.izq, a, b, visitados)
    return rango(raiz.izq, a, b, visitados) + [raiz.clave] + rango(raiz.der, a, b, visitados)

claves = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 90]
raiz = None
for k in claves:
    raiz = insertar(raiz, k)

recorridos = [0]
print("claves entre 30 y 60:", rango(raiz, 30, 60, recorridos))  # -> claves entre 30 y 60: [30, 35, 40, 45, 50, 55, 60]
print("nodos visitados:", recorridos[0], "de", len(claves))     # -> nodos visitados: 11 de 15
```

## Errores típicos

- **Confundir árbol binario con árbol binario de búsqueda.** Un árbol binario cualquiera no
  tiene por qué estar ordenado, y buscar en él exige recorrerlo entero. La propiedad BST es una
  condición adicional, no un sinónimo.
- **Insertar claves ya ordenadas y dar por hecho que el árbol está bien.** Es el error más
  caro: las operaciones empiezan a costar O(n) sin que nada falle. Si los datos llegan
  ordenados con frecuencia (identificadores autoincrementales, fechas, series temporales), un
  BST desnudo es la estructura equivocada.
- **Creer que el recorrido en orden sirve para cualquier árbol.** Solo devuelve las claves
  ordenadas si se cumple la propiedad BST. En un árbol binario sin orden, el recorrido en orden
  es un orden arbitrario.
- **Borrar un nodo con dos hijos sustituyéndolo por un hijo cualquiera.** Eso rompe la
  propiedad de orden. El borrado correcto usa el **sucesor en orden** (el menor del subárbol
  derecho) o el predecesor, lo pone en el lugar del nodo y borra el original de su posición
  nueva.
- **Usar la recursión sin pensar en la profundidad.** Los recorridos recursivos consumen un
  marco de pila por nivel. Con un árbol degenerado de un millón de nodos, la recursión revienta
  con un desbordamiento de pila antes de terminar; hay que pasar a una versión iterativa con
  pila explícita, como se ve en [[bfs-y-dfs]].
- **Elegir un BST cuando bastaba una tabla hash.** Si solo necesitas «dado este identificador,
  dame su valor» y nunca vas a preguntar por rangos ni por orden, [[tablas-hash]] es más simple
  y más rápida de media.

:::practica
enunciado: Inserta en un BST vacío las claves 8, 4, 12, 2, 6, 10 y 14. Indica la altura del árbol, las comparaciones para buscar el 6 y el resultado del recorrido en orden. ¿Cuántas claves devuelve una consulta por rango [5, 11]?
pista: Cada clave menor baja por la izquierda y cada mayor por la derecha; en orden es izquierda, nodo, derecha, y el rango poda lo que queda fuera.
solucion: El árbol queda con 8 en la raíz (sus hijos 4 y 12), y en el tercer nivel 2 y 6 a la izquierda, 10 y 14 a la derecha: 7 nodos y los 6 llegan al mismo nivel, así que está lleno salvo por los nietos del 2, que no existen. Altura 2, el mínimo para 7 nodos. Buscar 6: 6 < 8 → izquierda, 6 > 4 → derecha, 6 = 6: tres comparaciones. El recorrido en orden da 2, 4, 6, 8, 10, 12, 14, y el rango [5, 11] devuelve 6, 8 y 10. Conclusión: con las claves insertadas ya ordenadas la altura subiría a 6.
:::

## Comprueba que lo sabes

:::quiz
p: Insertas las claves 1, 2, 3, 4, 5 en un BST vacío, en ese orden. ¿Qué altura tiene el árbol y cuánto cuesta buscar el 5?
o: Altura 4; buscar el 5 cuesta 5 comparaciones
o: Altura 2; buscar el 5 cuesta 3 comparaciones
o: Altura 4; buscar el 5 cuesta 3 comparaciones
a: 1
e: Cada clave es mayor que la anterior, así que todas bajan por la derecha y el árbol es una cadena de 5 nodos con 4 aristas: altura 4. Recorrer esa cadena hasta el 5 son 5 comparaciones, el peor caso de un BST. Un árbol equilibrado con esas claves tendría altura 2.
:::

:::quiz
p: ¿Qué te da un BST que no te da una tabla hash con las mismas claves?
o: Búsquedas más rápidas en el caso medio
o: El recorrido en orden, las consultas por rango y el sucesor o precesor de una clave
o: Menos memoria ocupada por elemento
a: 2
e: La tabla hash gana en velocidad media (O(1) frente a O(log n)) y suele ganar también en memoria. Lo que no puede dar es orden: para responder «claves entre 40 y 60» tendría que extraer y ordenar todo, O(n log n), mientras que el BST poda ramas y responde en O(log n + k).
:::
