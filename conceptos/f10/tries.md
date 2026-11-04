---
id: tries
titulo: Árboles de prefijos (tries)
fase: 10
nivel: avanzado
rutas: [alg, de]
prerequisitos: [arboles-binarios, tablas-hash, complejidad-asintotica]
tags: [estructuras, cadenas, prefijos, autocompletado]
resumen: Un árbol con un carácter por arista que permite buscar, insertar y autocompletar por prefijo en tiempo proporcional a la longitud de la palabra, no al número de palabras.
fuentes: ["Fredkin (1960), 'Trie memory'", "Sedgewick y Wayne (2011), 'Algorithms', 4.ª ed., cap. 5"]
---

## En una frase

Un trie es un árbol en el que cada arista lleva un carácter y cada nodo representa el prefijo
formado por el camino desde la raíz, de modo que buscar una palabra cuesta tantos pasos como
letras tiene, y listar todo lo que empieza por un prefijo cuesta solo bajar hasta ese prefijo y
recorrer lo que cuelga de él.

## La idea

Piensa en un fichero de fichas de papel ordenadas alfabéticamente en cajones. Para saber si
«murciélago» está en el diccionario no comparas con todas las palabras: vas al cajón de la M,
dentro de él al de la MU, luego al de MUR, y en cuatro pasos sabes si está. La estructura no
guarda las palabras como bloques, guarda **caminos de letras** que comparten los primeros pasos.

Eso es un trie, y la propiedad que lo define es que **el tiempo de búsqueda no depende de cuántas
palabras haya en la estructura**, solo de la longitud de la palabra que buscas. En una tabla hash
([[tablas-hash|tabla hash]]) el coste medio también es constante, pero hay dos diferencias que
importan:

1. **El trie no necesita la palabra entera.** Con una tabla hash, para saber si existe alguna
   palabra que empiece por «mur» hay que recorrer las claves y comparar prefijos: `O(n · L)`, con
   `n` el número de claves y `L` la longitud máxima. En un trie, bajar hasta el nodo de «mur»
   cuesta 3 pasos y lo que cuelga de él es exactamente la respuesta.
2. **El trie comparte prefijos.** «casa», «caso» y «casar» ocupan un camino común de cuatro nodos
   (`c`, `a`, `s`, `a`) y luego se separan. Almacenar las tres palabras como cadenas independientes
   guarda la «casa» tres veces.

El coste de esas ventajas es la memoria, y no es pequeño. La implementación clásica reserva un
array de hijos por nodo: con un alfabeto de 26 letras y punteros de 8 bytes, cada nodo ocupa 208
bytes **aunque solo tenga un hijo**. Un diccionario de 100.000 palabras en español ocupa alrededor
de 500.000 caracteres como texto plano, pero como trie con arrays puede necesitar cientos de
megas. De ahí las variantes comprimidas: el **árbol Patricia** o **radix tree** fusiona las
cadenas de nodos con un solo hijo en una arista con una etiqueta de varios caracteres, y el
**DAWG** funde además los sufijos comunes.

El uso estrella es el **autocompletado**: cada vez que teclas una letra bajas un nivel del trie y
el nodo actual te da las continuaciones posibles. Eso es exactamente lo que hace un buscador al
sugerir mientras escribes. Otros usos donde el trie es la estructura natural: la corrección
ortográfica con distancia de edición sobre el trie (recorrerlo una vez en vez de comparar con
todas las palabras), el enrutado de prefijos de red (las tablas de rutas IP se guardan en tries
binarios de bits) y el filtrado de listas de bloqueo por palabra o dominio.

Y una limitación que se olvida: el trie está pensado para **prefijos**, no para sufijos ni para
búsquedas aproximadas. Para buscar «cualquier palabra que contenga esta subcadena» hace falta otra
estructura, como el árbol de sufijos, que es un trie construido sobre todos los sufijos de un
texto.

## Definición formal

Un **trie** sobre un alfabeto `Σ` es un árbol enraizado con estas propiedades:

- Cada arista lleva exactamente un símbolo de `Σ`.
- La raíz representa la cadena vacía.
- Cada nodo representa la cadena formada por los símbolos del camino desde la raíz hasta él.
- Si la cadena `w` está almacenada, existe un nodo que la representa y ese nodo está **marcado
  como fin de palabra**.
- Ningún nodo tiene dos aristas de salida con el mismo símbolo (por eso la representación de cada
  cadena es única).

Símbolos y costes, con `L` la longitud de la palabra consultada, `n` el número de palabras
almacenadas, `N` el número total de nodos, `/Σ/` el tamaño del alfabeto y `k` el número de
resultados de una consulta por prefijo:

| Operación | Coste | Comentario |
| --- | --- | --- |
| Buscar palabra `w` | O(L) | No depende de n |
| Insertar palabra `w` | O(L) | Creando nodos si hace falta |
| Buscar si existe un prefijo `p` | O(/p/) | Bajar y ver si el nodo existe |
| Listar palabras con prefijo `p` | O(/p/ + k) | Bajar y recorrer el subárbol |
| Borrar palabra | O(L) | Y podar los nodos que queden sin uso |
| Memoria | O(N · /Σ/) | El coste que duele |

La memoria merece la fórmula explícita: con un array de hijos por nodo, el espacio es
`O(N · /Σ/)`, y en el peor caso `N = n · L` (palabras sin ningún prefijo en común), así que la
memoria puede llegar a `O(n · L · /Σ/)`, que es peor que guardar las palabras. Con un diccionario
disperso de hijos (`{carácter: nodo}`) el espacio baja a `O(N)` y se cambia memoria por velocidad
de acceso; con aristas comprimidas, `N` se reduce a `O(n)`.

**Marcar el fin de palabra no es opcional.** «casa» y «casar» comparten camino hasta `c-a-s-a`;
si no se marca el nodo de «casa» como final, al buscar «casa» no hay forma de distinguir «está y
es una palabra» de «es solo un prefijo de otra». Es el error de implementación clásico de esta
estructura y produce falsos positivos silenciosos.

## Ejemplo

Insertamos, en este orden: «sol», «solo», «solar», «sal» y «sartén». El trie queda así (los
nodos con asterisco son fin de palabra):

```text
                raiz
                 |
                 s
               /   \
              o     a
              |    / \
              l   l   r
             (*) (*)  |
            /   \      t
           o     a     |
          (*)    |     e
                 r     |
                (*)    n
                      (*)
```

Detalles que se leen en el dibujo:

- El camino `s → o → l` es común a «sol», «solo» y «solar»: se almacena una sola vez.
- El nodo de `s-o-l` está marcado como final (es «sol») **y** tiene hijos: es prefijo de otras.
- «sal» y «sartén» comparten `s` y `a`, y ahí se separan: `l` por un lado, `r` por el otro.
- Número de nodos: 1 raíz + 12 = 13. Guardar las cinco palabras como cadenas cuesta 3 + 4 + 5 +
  3 + 6 = 21 caracteres, sin contar los separadores.

Búsquedas concretas:

- **«solo»**: bajar `s`, `o`, `l`, `o` → 4 pasos, nodo marcado → está. Con 5 palabras o con 5
  millones, 4 pasos.
- **«so»**: bajar `s`, `o` → nodo existe y no está marcado → **«so» es un prefijo pero no una
  palabra almacenada**. Ese matiz es justo el que permite distinguir autocompletado de búsqueda.
- **«sor»**: bajar `s`, `o`, y no hay arista con `r` → no está y no puede estar nada que empiece
  por «sor». Búsqueda negativa en 2 pasos.
- **Completar «sol»**: bajar 3 pasos y recorrer el subárbol → `sol`, `solo`, `solar`. Tres
  resultados en 3 + 3 pasos, sin mirar «sal» ni «sartén».

:::figura
fichero: tries-prefijos-y-consulta
pie: A la izquierda, el trie de las cinco palabras del ejemplo: 13 nodos, con el camino s-o-l compartido por «sol», «solo» y «solar», y el aro rojo marcando dónde termina una palabra almacenada. El nodo de «sol» está marcado y además tiene hijos: es palabra y prefijo a la vez, y esa distinción es la que separa una búsqueda exacta de un autocompletado. A la derecha, lo que cuesta saber si existe alguna palabra que empiece por «sol»: el trie baja los 3 caracteres del prefijo, con 5 palabras o con 5 millones, mientras que una tabla hash con las mismas claves tiene que mirarlas una por una, así que con un millón de palabras son un millón de comprobaciones como mínimo. De ahí que el autocompletado use tries.
fuente: figuras/tries-1.py
:::

## Código

```python verificable
class Trie:
    """Trie con hijos en diccionario: menos memoria que un array por alfabeto."""

    def __init__(self):
        self.hijos = {}          # caracter -> subtrie
        self.fin = False         # True si el camino hasta aqui es una palabra completa

    def insertar(self, palabra):
        nodo = self
        for c in palabra:
            nodo = nodo.hijos.setdefault(c, Trie())
        nodo.fin = True          # sin esta marca, "casa" y "casar" serian indistinguibles

    def contiene(self, palabra):
        nodo = self
        for c in palabra:
            if c not in nodo.hijos:
                return False
            nodo = nodo.hijos[c]
        return nodo.fin         # existe el camino, pero puede ser solo un prefijo

    def empieza_por(self, prefijo):
        nodo = self
        for c in prefijo:
            if c not in nodo.hijos:
                return False
            nodo = nodo.hijos[c]
        return True             # aqui si basta con que exista el nodo

t = Trie()
for palabra in ("sol", "solo", "solar", "sal", "sarten"):
    t.insertar(palabra)

print("contiene sol:", t.contiene("sol"))        # -> contiene sol: True
print("contiene so:", t.contiene("so"))          # -> contiene so: False
print("prefijo so:", t.empieza_por("so"))        # -> prefijo so: True
print("prefijo sor:", t.empieza_por("sor"))      # -> prefijo sor: False
print("contiene sar:", t.contiene("sar"))        # -> contiene sar: False
```

:::claves
- `nodo.hijos.setdefault(c, Trie())` crea el hijo **solo si falta** y devuelve el que hay en los dos casos, así que la inserción avanza sin comprobar nada. Ojo: `Trie()` se construye siempre, aunque la clave ya exista, porque el segundo argumento no es perezoso; con objetos caros conviene preguntar antes con `if c in nodo.hijos`.
- `contiene` termina en `return nodo.fin`, no en `return True`. Recorrer el camino solo demuestra que el prefijo existe: sin esa marca, `t.contiene("so")` devolvería `True` porque el camino s-o está en el trie.
- `empieza_por` sí devuelve `True` en cuanto encuentra el nodo, porque para un prefijo no hace falta que sea una palabra completa. Es la única diferencia entre los dos métodos, y explica por qué el autocompletado necesita el segundo.
- `self.hijos = {}` guarda un diccionario por nodo. Con un array de 26 posiciones cada nodo ocuparía lo mismo tenga un hijo o ninguno: 208 bytes con punteros de 8 bytes, y ese es el coste que aparece en el ejercicio de memoria.
- `setdefault` y `self.fin = True` solo se ejecutan al final de la inserción: insertar «solo» después de «sol» no vuelve a crear los nodos `s`, `o` y `l`, solo añade el último. Los prefijos se comparten entre palabras por construcción.
- Cambiar `for c in palabra` por `for c in palabra.lower()` hace el trie insensible a mayúsculas sin tocar la estructura, pero entonces lo que se guarda ya no es la palabra original: para devolverla habría que guardarla en el nodo de fin.
:::

```python verificable
class Trie:
    def __init__(self):
        self.hijos = {}
        self.fin = False

    def insertar(self, palabra):
        nodo = self
        for c in palabra:
            nodo = nodo.hijos.setdefault(c, Trie())
        nodo.fin = True

def completar(raiz, prefijo):
    """Devuelve todas las palabras almacenadas que empiezan por el prefijo."""
    nodo = raiz
    for c in prefijo:
        if c not in nodo.hijos:
            return []
        nodo = nodo.hijos[c]
    resultados = []

    def recorrer(n, acumulado):
        if n.fin:
            resultados.append(prefijo + acumulado)
        for c, hijo in sorted(n.hijos.items()):
            recorrer(hijo, acumulado + c)

    recorrer(nodo, "")
    return resultados

def contar_nodos(raiz):
    return 1 + sum(contar_nodos(h) for h in raiz.hijos.values())

palabras = ["sol", "solo", "solar", "sal", "sarten"]
t = Trie()
for p in palabras:
    t.insertar(p)

print("completar 'sol':", completar(t, "sol"))    # -> completar 'sol': ['sol', 'solar', 'solo']
print("completar 'sa':", completar(t, "sa"))      # -> completar 'sa': ['sal', 'sarten']
print("completar 's':", completar(t, "s"))        # -> completar 's': ['sal', 'sarten', 'sol', 'solar', 'solo']
print("nodos del trie:", contar_nodos(t))         # -> nodos del trie: 13
print("caracteres guardados:", sum(len(p) for p in palabras))   # -> caracteres guardados: 21
```

```python verificable
# Lo que un trie hace y una tabla hash no puede hacer barato: consultas por prefijo.
import time

class Trie:
    def __init__(self):
        self.hijos = {}
        self.fin = False

    def insertar(self, palabra):
        nodo = self
        for c in palabra:
            nodo = nodo.hijos.setdefault(c, Trie())
        nodo.fin = True

palabras = [f"palabra{i:05d}" for i in range(20000)]   # 20.000 claves con prefijo comun
t = Trie()
for p in palabras:
    t.insertar(p)
conjunto = set(palabras)

# Buscar un prefijo en el trie: bajar 7 caracteres, sin importar cuantas palabras haya.
inicio = time.perf_counter()
for _ in range(2000):
    nodo = t
    for c in "palabra0000":
        nodo = nodo.hijos[c]
micros_trie = (time.perf_counter() - inicio) / 2000 * 1e6

# Lo mismo con una tabla hash: hay que mirar todas las claves.
inicio = time.perf_counter()
for _ in range(2000):
    cuantas = [p for p in conjunto if p.startswith("palabra0000")]
micros_hash = (time.perf_counter() - inicio) / 2000 * 1e6

print(f"prefijo en trie: {micros_trie:7.1f} us")
print(f"prefijo en hash: {micros_hash:7.1f} us")
print("el trie es mas rapido:", micros_trie < micros_hash)   # -> el trie es mas rapido: True
print("cuantas palabras empiezan igual:", len(cuantas))      # -> cuantas palabras empiezan igual: 10
```

## Errores típicos

- **No marcar el fin de palabra.** El trie dirá que «ca» está porque existe el camino
  `c → a` de «casa». Sin el booleano de fin, no hay manera de distinguir un prefijo de una
  palabra completa. Es el error número uno de esta estructura.
- **Almacenar la palabra entera en cada nodo.** Guardar la cadena completa en cada nodo (o peor,
  una lista de todas las palabras que pasan por él) multiplica la memoria por la longitud. El nodo
  solo necesita sus hijos y la marca de fin; la palabra se reconstruye subiendo o llevando un
  acumulador durante el recorrido.
- **Usar un array de tamaño alfabeto para cada nodo sin pensar en la memoria.** Con caracteres
  Unicode, `Σ` puede tener más de 100.000 símbolos y un array por nodo es inviable. Decide entre
  array (rápido, mucha memoria), diccionario disperso (equilibrado) o aristas comprimidas (poca
  memoria, algo más de lógica) en función del alfabeto y del número de palabras.
- **Borrar una palabra sin podar.** Al borrar «solar» de un trie que también tiene «solo», hay que
  quitar la marca de fin y eliminar los nodos que se quedan sin hijos ni marca, subiendo desde el
  final. Si solo se quita la marca, el trie crece sin límite con palabras que ya no existen.
- **Creer que sirve para buscar subcadenas o hacer difusos.** El trie resuelve prefijos. Para
  «contiene» hace falta un árbol de sufijos; para tolerancia a errores de tecleo hace falta
  recorrer el trie con la distancia de edición como presupuesto, como se ve en
  [[programacion-dinamica|la distancia de edición]].
- **Sustituir una tabla hash por un trie sin medir.** Si solo necesitas «¿existe esta clave
  exacta?», la tabla hash es más simple, más rápida de media y más compacta. El trie se justifica
  cuando el prefijo es parte de la consulta o cuando compartir prefijos ahorra memoria de verdad.

:::nota
Los routers de internet guardan la tabla de rutas como un **trie binario** sobre los bits de la
dirección IP. La consulta es «la ruta más específica que encaje con este prefijo de bits», que es
exactamente una búsqueda por prefijo, y por eso un trie la responde en 32 pasos (los bits de una
IPv4) sin recorrer la tabla entera.
:::

:::practica
enunciado: Un diccionario tiene 100.000 palabras de 8 caracteres casi sin prefijos en común. Calcula cuántos nodos tendría su trie con un array de hijos por nodo y cuánta memoria pide con punteros de 8 bytes, y compáralo con guardar el texto.
pista: Cada nodo reserva un hueco por cada símbolo del alfabeto, tenga o no ese hijo: con 26 letras y 8 bytes por puntero son 208 bytes por nodo.
solucion: Al compartir poco los prefijos, los nodos son n · L = 100.000 · 8 = 800.000. Cada nodo ocupa 26 · 8 = 208 bytes, así que el trie pide 800.000 · 208 = 166.400.000 bytes, unos 166 MB. El texto son 800.000 caracteres, unos 0,8 MB, o 0,9 MB con separadores. Conclusión: el trie gasta unas 180 veces más; con un diccionario disperso de hijos el espacio baja a O(N).
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué un trie puede responder «¿hay alguna palabra que empiece por "sol"?» más rápido que una tabla hash con las mismas palabras?
o: Porque en el trie basta con bajar los 3 caracteres del prefijo y mirar el subárbol, mientras que en la tabla hay que revisar todas las claves
o: Porque el trie guarda las palabras ordenadas y la tabla no
o: Porque la tabla hash no admite cadenas como claves
a: 1
e: La consulta por prefijo en un trie cuesta O(longitud del prefijo) más el coste de listar los resultados, y no depende del número de palabras. En una tabla hash, las claves están dispersas: la única forma de saber quién empieza por «sol» es recorrerlas todas, O(n · L). La tabla sí admite cadenas y no guarda orden alguno; precisamente por eso no puede responder consultas por rango o prefijo.
:::

:::quiz
p: En un trie con «casa» y «casar» insertadas, ¿qué distingue que «casa» sea una palabra y no solo un prefijo?
o: Que el nodo de «casa» tenga hijos
o: Que el nodo de «casa» esté marcado como fin de palabra
o: Que la palabra «casa» sea más corta
a: 2
e: El camino c-a-s-a existe en los dos casos, porque «casar» pasa por él. Lo que marca que ahí termina una palabra almacenada es el booleano de fin de palabra, que puede ser verdadero y a la vez tener hijos. Sin esa marca, la consulta de «casa» devolvería un falso positivo por el simple hecho de existir el camino.
:::

:::quiz
p: ¿Cuál es el coste de memoria de un trie con un array de hijos por nodo, y por qué importa?
o: O(n), porque hay una entrada por palabra
o: O(N · /Σ/), con N el número de nodos y /Σ/ el tamaño del alfabeto, lo que puede superar el coste de guardar las palabras
o: O(L), porque solo se guardan las letras de cada palabra
a: 2
e: Cada nodo reserva espacio para todos los símbolos posibles del alfabeto, aunque tenga uno solo. Con 26 letras y 8 bytes por puntero, cada nodo ocupa 208 bytes, y el total es N · /Σ/, que con palabras de prefijos poco compartidos puede ser mayor que guardar las cadenas. De ahí las variantes con diccionario disperso o con aristas comprimidas.
:::
