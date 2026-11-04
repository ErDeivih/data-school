---
id: union-find
titulo: Conjuntos disjuntos (union-find)
fase: 10
nivel: avanzado
rutas: [alg]
prerequisitos: [grafos-representacion, analisis-amortizado, arboles-binarios]
tags: [grafos, particiones, kruskal, amortizado]
resumen: Mantiene una partición en grupos que se van fusionando, con dos optimizaciones que dejan cada operación en un coste prácticamente constante.
fuentes: ["Tarjan (1975), 'Efficiency of a good but not linear set union algorithm'", "Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 21"]
---

## En una frase

Union-find responde «¿están estos dos elementos en el mismo grupo?» y «fusiona estos dos
grupos» en un tiempo que, con compresión de caminos y unión por rango, es tan cercano a
constante que en la práctica se trata como O(1).

## La idea

Imagina que vas uniendo personas en pandillas. Al principio cada persona es su propia pandilla.
Cuando dos pandillas se alían, no hace falta llamar a todos sus miembros ni cambiarles el
carné: basta con que el jefe de una pase a responder ante el jefe de la otra. A partir de ese
momento, para saber si dos personas son de la misma pandilla, subes por la cadena de jefes de
cada una hasta llegar al jefe supremo; si llegas al mismo, son de la misma pandilla.

Eso es todo el algoritmo: un array `padre` donde `padre[i]` es «el jefe de `i`», y el jefe
supremo de un grupo es el que es su propio padre. Buscar el jefe supremo se llama **find**. Si
dos elementos tienen el mismo jefe supremo, están en el mismo conjunto.

Dos detalles convierten esta idea sencilla en una de las estructuras más eficientes que se
conocen:

1. **Unión por rango** (o por tamaño): al fusionar dos grupos, se cuelga el árbol más bajo del
   más alto. Si se hiciera al revés sin mirar, las cadenas se estirarían y un `find` tendría que
   recorrerlas enteras.
2. **Compresión de caminos**: cuando buscas el jefe supremo de un elemento, aprovechas para
   colgar directamente de él a todos los nodos por los que has pasado. La cadena se aplana y la
   siguiente consulta sobre esos mismos nodos es casi instantánea.

Cada una de las dos optimizaciones por separado ya da O(log n) amortizado. **Juntas** dan
O(α(n)), donde `α` es la función inversa de Ackermann: una función que crece tan despacio que
para cualquier `n` que quepa en el universo físico vale menos que 5. Ese resultado es el que
justifica tratar la estructura como si fuera O(1) en todo el código que la usa.

La aplicación que la hace famosa es **Kruskal**, para el árbol de expansión mínimo: se ordenan
las aristas de menor a mayor peso y se van añadiendo; una arista se descarta si sus dos extremos
ya están en el mismo conjunto, porque añadirla cerraría un ciclo. Sin union-find, comprobar «¿ya
están conectados?» costaría un recorrido por cada arista. Con union-find, el algoritmo entero
cuesta O(m log m), y ese logaritmo viene de ordenar, no de la estructura.

Otras aplicaciones: contar componentes conexas, detectar si añadir una arista crea un ciclo,
agrupar registros duplicados (el *record linkage*, donde cada fusión declara que dos registros
son la misma entidad), mantener las regiones de una imagen segmentada o el algoritmo de
percolación.

## Definición formal

Se mantiene una **partición** de un universo de `n` elementos en conjuntos disjuntos: cada
elemento pertenece exactamente a un conjunto, y ningún elemento está en dos. La estructura se
representa con un bosque:

- `padre[i]` — el índice del nodo padre de `i`. Si `padre[i] = i`, entonces `i` es una **raíz**
  y representa a su conjunto.
- `rango[i]` — una cota superior de la altura del subárbol que cuelga de `i`. Solo se usa para
  decidir quién cuelga de quién.
- `find(i)` — sigue la cadena de padres hasta la raíz. Es el **representante** del conjunto de
  `i`. Dos elementos están en el mismo conjunto si y solo si `find(x) = find(y)`.
- `union(x, y)` — sustituye los dos conjuntos que contienen a `x` y a `y` por su unión.

Las tres operaciones:

:::formula
find(x): mientras padre[x] ≠ x, x ← padre[x]; devuelve x
:::

:::formula
union(x, y): rx ← find(x); ry ← find(y); si rx = ry no se hace nada; si no, el de menor rango cuelga del de mayor
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `n` | Elementos del universo, numerados 0…n−1 | Elementos | Sin optimizaciones el peor caso crece en proporción; con las dos puestas, α(n) sigue valiendo menos que 5 para cualquier n real |
| `padre[i]` | Índice del padre de `i`; si vale `i`, entonces `i` es raíz de su conjunto | Índice de 0 a n−1 | El camino hasta la raíz se alarga y cada `find` cuesta más saltos; la compresión de caminos lo vuelve a acortar en la siguiente consulta |
| `rango[i]` | Cota superior de la altura del subárbol que cuelga de `i` | Niveles del árbol | Ese subárbol es más alto y al fusionar es más probable que sea él quien reciba al otro, que es justo lo que se busca |
| `α(n)` | Inversa de la función de Ackermann: el coste amortizado por operación con las dos optimizaciones | Operaciones (adimensional) | No sube en la práctica: para n = 10¹⁸ vale 4. Es el coste de una operación, no una magnitud del problema |
| `m` | Operaciones de unión que se encadenan, o aristas que procesa Kruskal | Operaciones o aristas | El coste total es O(m · α(n)) y crece de forma lineal; en Kruskal m es el número de aristas y el logaritmo del total viene de ordenarlas, no de la estructura |
:::

Costes:

| Variante | Coste por operación | Coste de n operaciones |
| --- | --- | --- |
| Sin optimizaciones | O(n) en el peor caso | O(n²) |
| Solo unión por rango | O(log n) | O(n log n) |
| Solo compresión de caminos | O(log n) amortizado | O(n log n) |
| Las dos juntas | O(α(n)) amortizado | O(n · α(n)), que es O(n) a efectos prácticos |

- `α(n)` — la inversa de la función de Ackermann. Para `n = 10¹⁸`, `α(n) = 4`. Nunca se acerca a
  5 en ningún problema real.
- El coste es **amortizado**: una operación concreta puede recorrer una cadena larga, pero las
  siguientes sobre los mismos nodos van casi directas porque la compresión ya aplanó el camino.
  Es el tipo de razonamiento de [[analisis-amortizado]].

Detalles que hay que respetar:

1. **Compresión en dos pasadas** (la más habitual): se sube hasta la raíz para encontrarla y
   luego se vuelve a bajar colgando cada nodo de ella. Hay una variante de una sola pasada que
   va colgando cada nodo de su abuelo: aplana algo menos pero hace menos escrituras.
2. **Unión por rango frente a unión por tamaño.** Por rango se compara la altura estimada; por
   tamaño, el número de elementos. Las dos dan la misma cota y el mismo efecto; mezclarlas en la
   misma estructura no tiene sentido porque los dos arrays dejan de ser correctos.
3. **La partición solo se fusiona, nunca se divide.** Union-find no soporta «separar» un
   conjunto sin reconstruirlo desde cero. Si necesitas deshacer uniones, esta estructura no es
   la adecuada.

## Ejemplo

Universo de 6 elementos, `0` a `5`. Al principio cada uno es su propio conjunto:
`padre = [0, 1, 2, 3, 4, 5]` y todos los rangos valen 0.

Aplicamos las operaciones de izquierda a derecha, anotando el representante de cada elemento
después de cada paso:

| Operación | Qué pasa | padre resultante | Representantes |
| --- | --- | --- | --- |
| estado inicial | 6 conjuntos de 1 | [0, 1, 2, 3, 4, 5] | 0 1 2 3 4 5 |
| union(0, 1) | rangos iguales: el 1 cuelga del 0 | [0, 0, 2, 3, 4, 5] | 0 0 2 3 4 5 |
| union(2, 3) | rangos iguales: el 3 cuelga del 2 | [0, 0, 2, 2, 4, 5] | 0 0 2 2 4 5 |
| union(1, 3) | raíces 0 y 2, misma altura: la 2 cuelga de la 0 | [0, 0, 0, 2, 4, 5] | 0 0 0 0 4 5 |
| union(4, 4) | misma raíz: no se hace nada | [0, 0, 0, 2, 4, 5] | 0 0 0 0 4 5 |

Al final hay tres conjuntos: `{0, 1, 2, 3}`, `{4}` y `{5}`. El representante de `{0,1,2,3}` es
el 0.

Los dos últimos pasos enseñan lo importante:

- En `union(1, 3)` el 3 ya no es raíz: su padre es el 2. Por eso la unión se hace entre las
  **raíces** 0 y 2, no entre el 1 y el 3.
- En `union(4, 4)` el `find` de los dos lados devuelve la misma raíz (el 4). Es un caso que hay
  que tratar explícitamente: si se colgara la raíz de sí misma, el array quedaría en un estado
  sin sentido.

Ahora el efecto de la compresión. Si buscamos `find(3)` en el estado actual, el camino es
3 → 2 → 0. Al terminar la compresión, el padre del 3 pasa a ser 0 directamente. La cadena
3 → 2 → 0 se convierte en 3 → 0 y el 2 también queda apuntando al 0. Cada consulta posterior
sobre esos nodos cuesta un solo salto.

:::figura
fichero: union-find-compresion-y-saltos
pie: A la izquierda, el conjunto {0, 1, 2, 3} antes y después de un solo find(3): la cadena 3 → 2 → 0 cuesta dos saltos y la consulta la aplana, dejando los tres nodos colgando de la raíz. El 4 y el 5 no aparecen porque son raíces de otros conjuntos y esa consulta no los toca. A la derecha, lo que ese aplanamiento significa en trabajo: 200 consultas de find(499) sobre una cadena degenerada de 500 nodos suman 99.800 saltos sin compresión y 698 con ella, porque la primera consulta paga la cadena entera y las 199 siguientes cuestan un salto cada una. Es la diferencia entre O(n) y O(α(n)) por operación, medida en saltos contados.
fuente: figuras/union-find-1.py
:::

## Código

```python verificable
class UnionFind:
    """Particion de 0..n-1 con union por rango y compresion de caminos."""

    def __init__(self, n):
        self.padre = list(range(n))       # al principio cada uno es su propia raiz
        self.rango = [0] * n              # cota de la altura del subarbol
        self.componentes = n

    def find(self, x):
        raiz = x
        while self.padre[raiz] != raiz:   # primera pasada: llegar a la raiz
            raiz = self.padre[raiz]
        while self.padre[x] != raiz:      # segunda pasada: colgar todos del camino de la raiz
            self.padre[x], x = raiz, self.padre[x]
        return raiz

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False                  # ya estaban juntos: no hay nada que fusionar
        if self.rango[rx] < self.rango[ry]:
            rx, ry = ry, rx               # el arbol mas bajo cuelga del mas alto
        self.padre[ry] = rx
        if self.rango[rx] == self.rango[ry]:
            self.rango[rx] += 1           # solo crece la altura cuando empataban
        self.componentes -= 1
        return True

uf = UnionFind(6)
print("representantes al inicio:", [uf.find(i) for i in range(6)])  # -> representantes al inicio: [0, 1, 2, 3, 4, 5]

uf.union(0, 1)
uf.union(2, 3)
print("tras 0-1 y 2-3:", uf.padre, "conjuntos", uf.componentes)     # -> tras 0-1 y 2-3: [0, 0, 2, 2, 4, 5] conjuntos 4

uf.union(1, 3)
print("tras unir 1 y 3:", uf.padre, "conjuntos", uf.componentes)     # -> tras unir 1 y 3: [0, 0, 0, 2, 4, 5] conjuntos 3
print("mismo grupo (0, 3):", uf.find(0) == uf.find(3))               # -> mismo grupo (0, 3): True
print("mismo grupo (0, 4):", uf.find(0) == uf.find(4))               # -> mismo grupo (0, 4): False

uf.find(3)                                                          # la compresion aplana el camino
print("padre tras find(3):", uf.padre)                              # -> padre tras find(3): [0, 0, 0, 0, 4, 5]
```

:::claves
- `find` tiene **dos bucles**: el primero sube hasta la raíz para encontrarla y el segundo vuelve a bajar colgando del camino. La variante de una pasada (`self.padre[x] = self.padre[self.padre[x]]`, la que usa el bloque siguiente) hace la mitad de escrituras y deja el árbol algo menos plano.
- `union` devuelve un booleano: `True` si fusionó y `False` si ya estaban en el mismo conjunto. No es decorativo: es exactamente el valor que usa Kruskal para decidir si descarta una arista.
- `self.padre[ry] = rx` cuelga la **raíz** `ry`, no el elemento `y`. Si se colgara `y` directamente se rompe el invariante del bosque y `find` empieza a devolver representantes que no son raíces de nada.
- `self.rango[rx] += 1` solo cuando los dos rangos eran iguales. Si se incrementara siempre, la cota de altura dejaría de ser cierta y la unión por rango perdería todo su efecto.
- `self.padre = list(range(n))` deja cada elemento como su propia raíz, que es la condición `padre[i] == i` con la que `find` sabe que ha llegado al final de la cadena.
- El representante de un conjunto **cambia** al fusionarse: `uf.find(3)` devuelve 2 después de `union(2, 3)` y 0 después de `union(1, 3)`. Guardarlo como clave en un diccionario es un error que se descubre tarde.
:::

```python verificable
# Kruskal: el arbol de expansion minimo. Union-find decide que aristas no cierran ciclo.
class UnionFind:
    def __init__(self, n):
        self.padre = list(range(n))
        self.rango = [0] * n

    def find(self, x):
        while self.padre[x] != x:
            self.padre[x] = self.padre[self.padre[x]]   # compresion en una pasada
            x = self.padre[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rango[rx] < self.rango[ry]:
            rx, ry = ry, rx
        self.padre[ry] = rx
        if self.rango[rx] == self.rango[ry]:
            self.rango[rx] += 1
        return True

n = 6
aristas = [(0, 1, 4), (0, 2, 4), (0, 3, 1), (1, 2, 2), (1, 4, 3),
           (2, 3, 5), (2, 5, 6), (3, 4, 1), (4, 5, 2)]

uf = UnionFind(n)
total, arbol = 0, []
for u, v, w in sorted(aristas, key=lambda a: a[2]):   # de menor a mayor peso
    if uf.union(u, v):                                # union devuelve False si ya estaban juntos
        arbol.append((u, v, w))
        total += w

print("aristas del arbol:", arbol)      # -> aristas del arbol: [(0, 3, 1), (3, 4, 1), (1, 2, 2), (4, 5, 2), (1, 4, 3)]
print("peso total:", total)             # -> peso total: 9
print("aristas descartadas:", len(aristas) - len(arbol))  # -> aristas descartadas: 4
```

```python verificable
# Por que la compresion importa: contar los saltos de muchos find repetidos.
class UnionFind:
    def __init__(self, n, comprimir=True):
        self.padre = list(range(n))
        self.rango = [0] * n
        self.comprimir = comprimir
        self.saltos = 0

    def find(self, x):
        raiz = x
        while self.padre[raiz] != raiz:
            raiz = self.padre[raiz]
            self.saltos += 1
        if self.comprimir:
            while self.padre[x] != raiz:
                self.padre[x], x = raiz, self.padre[x]
        return raiz

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rango[rx] < self.rango[ry]:
            rx, ry = ry, rx
        self.padre[ry] = rx
        if self.rango[rx] == self.rango[ry]:
            self.rango[rx] += 1

# Cadena degenerada a proposito: 0 <- 1 <- 2 <- ... <- n-1
def cadena(n, comprimir):
    uf = UnionFind(n, comprimir)
    for i in range(1, n):
        uf.padre[i] = i - 1        # se fuerza la cadena saltandose la union por rango
    uf.rango = [0] * n
    return uf

n = 500
for comprimir in (False, True):
    uf = cadena(n, comprimir)
    for _ in range(200):
        uf.find(n - 1)             # siempre el mismo extremo: el peor caso
    print("comprimir =", comprimir, "saltos totales:", uf.saltos)
    # -> comprimir = False saltos totales: 99800
    # -> comprimir = True saltos totales: 698
```

## Errores típicos

- **Unir los elementos en lugar de sus raíces.** `union(x, y)` tiene que operar sobre
  `find(x)` y `find(y)`. Si se cuelga `x` directamente de `y` sin buscar las raíces, se rompe el
  invariante del bosque y `find` empieza a devolver representantes incoherentes.
- **Olvidar el caso en que ya están en el mismo conjunto.** Si `find(x) = find(y)` y la unión
  sigue adelante, se puede colgar una raíz de sí misma y el array queda corrupto. Hay que
  devolver sin tocar nada.
- **Implementar `find` sin compresión y creer que da igual.** Sin compresión, una secuencia de
  uniones mal ordenada construye cadenas de longitud n y cada consulta cuesta O(n). La
  diferencia entre O(n²) y O(n·α(n)) en un millón de elementos es la diferencia entre minutos y
  milisegundos.
- **Incrementar el rango siempre.** El rango solo crece cuando las dos raíces tenían el **mismo**
  rango; si no, la altura del árbol resultante es la de la raíz más alta y no cambia. Si se
  incrementa siempre, la cota de altura deja de ser cierta y la unión por rango pierde su
  efecto.
- **Confundir el representante con un identificador estable.** El representante de un conjunto
  **cambia** al fusionarse: el 2 era representante y después pasa a serlo el 0. Si guardas
  representantes en otra estructura y los comparas más tarde, tienes que volver a llamar a
  `find`. Nunca uses el representante como clave persistente.
- **Querer separar un conjunto.** Union-find solo fusiona. Si el problema necesita deshacer
  uniones (por ejemplo, borrar aristas de un grafo y recalcular componentes), hay que rehacer la
  estructura desde cero o usar una variante con histórico, que es mucho más cara.

:::practica
enunciado: Con 6 elementos (0 a 5) aplica, en este orden, union(0,1), union(2,3), union(4,5), union(1,3) y union(5,1). Escribe el array padre final, cuántos conjuntos quedan y los saltos de find(3) antes y después de comprimir.
pista: Cada unión se hace entre las raíces, no entre los elementos; con rangos iguales cuelga la segunda raíz de la primera.
solucion: Tras las tres primeras uniones padre = [0, 0, 2, 2, 4, 4], con rangos 1. union(1,3) une las raíces 0 y 2, de rango 1 las dos: el 2 cuelga del 0 y padre = [0, 0, 0, 2, 4, 4]. union(5,1) une las raíces 4 (rango 1) y 0 (rango 2): el 4 cuelga del 0 y padre = [0, 0, 0, 2, 0, 4]. Queda 1 conjunto. find(3) sube 3 → 2 → 0, dos saltos; tras comprimir cuesta un salto.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué hace exactamente la compresión de caminos en un find?
o: Reordena los elementos del conjunto por orden alfabético
o: Cuelga directamente de la raíz todos los nodos que estaban en el camino recorrido, para que las próximas consultas cuesten menos
o: Reduce el rango de la raíz para que el árbol no crezca
a: 2
e: La compresión no cambia qué elementos están juntos, solo la forma del árbol: aplana las cadenas. La unión por rango es la que controla la altura durante las fusiones; la compresión se encarga de las consultas. Juntas dan el coste O(α(n)).
:::

:::quiz
p: En Kruskal, ¿para qué sirve union-find?
o: Para ordenar las aristas por peso
o: Para saber en tiempo casi constante si los dos extremos de una arista ya están conectados y, por tanto, añadirla cerraría un ciclo
o: Para calcular el peso total del árbol
a: 2
e: El orden lo da el propio algoritmo de ordenación, y el peso se acumula sumando. La decisión que hay que tomar m veces es «¿estos dos vértices ya están en el mismo componente?», y union-find la responde en O(α(n)). Sin ella, cada comprobación costaría un recorrido del grafo.
:::

:::quiz
p: Un código de union-find guarda el representante de cada registro para usarlo como clave en un diccionario. ¿Qué problema tiene?
o: Ninguno: el representante de un conjunto es estable mientras el conjunto exista
o: Que el representante cambia cuando el conjunto se fusiona con otro, así que la clave guardada deja de ser válida
o: Que el representante no es un número entero
a: 2
e: Al fusionar dos conjuntos, uno de los dos representantes desaparece y todos sus elementos pasan a tener el otro como raíz. Cualquier copia del representante viejo queda obsoleta. Lo correcto es guardar el elemento y llamar a find cada vez que necesites el representante actual.
:::
