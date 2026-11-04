---
id: tablas-hash
titulo: Tablas hash
fase: 10
nivel: intermedio
rutas: [alg, de]
prerequisitos: [complejidad-asintotica, arrays-y-listas, analisis-amortizado]
tags: [estructuras, diccionarios, dispersion, coste]
resumen: Convierten una clave en una posición de un array para responder en O(1) de media, a cambio de aceptar colisiones y vigilar el factor de carga.
fuentes: ["Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 11", "Knuth (1998), 'The Art of Computer Programming, vol. 3'"]
---

## En una frase

Una tabla hash guarda cada par clave-valor en la posición de un array que le dice una función
de dispersión, de forma que buscar no requiere recorrer nada: en promedio cuesta un número
constante de operaciones, con independencia de cuántos elementos haya guardados.

## La idea

Piensa en un archivador con cajones numerados. Si cada persona tuviera asignado un cajón
distinto, encontrar su expediente sería abrir un cajón y ya está. El problema es doble: harían
falta tantos cajones como personas posibles, y las claves con las que trabajas (nombres,
correos, identificadores de sesión) no son números consecutivos del 0 al n.

La solución es una **función de dispersión** (en inglés, *hash*): una función que convierte
cualquier clave en un número de cajón. Con eso, guardar y buscar pasan a ser «calcula el número
y abre ese cajón». Aparecen entonces los dos problemas que definen toda la estructura:

1. **Colisiones.** Dos claves distintas pueden dar el mismo número. No es un fallo de la
   función: es inevitable, porque hay infinitas claves posibles y un número finito de cajones.
   La pregunta no es cómo evitarlas, sino qué hacer cuando ocurren. La respuesta más común es
   el **encadenamiento**: cada cajón guarda una lista de los pares que cayeron en él.
2. **Factor de carga.** Si metes 10.000 claves en 100 cajones, cada cajón acaba con 100 pares
   de media y buscar vuelve a ser lento. La solución es **redimensionar**: cuando la ocupación
   pasa de cierto umbral (típicamente 0,75), se crea un array del doble de tamaño y se
   reinsertan las claves. Cada inserción individual sigue costando O(1) de media; ese es
   justo el argumento de [[analisis-amortizado]]: el redimensionamiento ocasional es caro,
   pero repartido entre todas las inserciones sale a constante.

La diferencia práctica se ve con números. Buscar un identificador en una lista de un millón de
elementos comparando uno a uno cuesta, de media, 500.000 comparaciones; cada comparación de
cadenas puede tocar varios caracteres. Una tabla hash bien dimensionada resuelve la misma
búsqueda con un cálculo y una o dos comparaciones. Es la razón de que los diccionarios y los
conjuntos sean la estructura que más se usa en el día a día, y también de que el coste O(1) sea
el más malinterpretado de todos: es un coste **promedio bajo un supuesto de dispersión
uniforme**, no una garantía.

## Definición formal

Una tabla hash es una estructura con `m` posiciones (los *cubos* o *buckets*) y una función
`h` que asigna a cada clave un índice en `[0, m)`. Las tres operaciones son `insertar(k, v)`,
`buscar(k)` y `borrar(k)`.

- `k` — la clave que identifica al par. Debe ser un valor **inmutable** y con una relación de
  igualdad bien definida.
- `m` — el número de cubos.
- `h(k)` — la función de dispersión: recibe la clave y devuelve un entero; el índice final es
  `h(k) mod m`.
- `n` — el número de pares guardados.
- **Factor de carga** `α = n / m`. Es el número medio de pares por cubo y la variable que hay
  que vigilar.
- **Colisión** — dos claves `k₁ ≠ k₂` con `h(k₁) mod m = h(k₂) mod m`.

Costes con encadenamiento, suponiendo que `h` reparte las claves de forma aproximadamente
uniforme (supuesto de *hashing uniforme simple*):

- `buscar`, `insertar` y `borrar`: O(1 + α) de media. Con `α` acotado por una constante (por
  ejemplo 0,75) eso es O(1).
- **Peor caso:** O(n), cuando todas las claves caen en el mismo cubo. Ese caso no es
  teórico: es la base de los ataques por colisiones, en los que un atacante elige claves que
  dispersan al mismo cubo para degradar un servicio a propósito.
- **Espacio:** O(n + m).

Propiedades que conviene tener claras:

1. Una tabla hash **no mantiene ningún orden**. Recorrerla no da las claves ordenadas ni en el
   orden de inserción. Si necesitas orden, la estructura es [[arboles-binarios]] o una lista
   ordenada con [[busqueda-binaria]].
2. El coste O(1) se paga con **memoria y con una función de dispersión decente**. Una función
   mala convierte la tabla en una lista enlazada con pasos extra.
3. Para que la estructura funcione, dos claves iguales **tienen que producir el mismo hash**.
   Esa es la única obligación matemática: `k₁ = k₂` implica `h(k₁) = h(k₂)`. Lo contrario no se
   exige (dos claves distintas pueden compartir hash).

:::figura
fichero: tablas-hash-carga-y-colisiones
pie: A la izquierda, las sondas medias por búsqueda frente al factor de carga α = n/m. Con encadenamiento el coste sube en línea recta (1 + α/2) y nunca estalla; con direccionamiento abierto y sondeo lineal se dispara al acercarse a 1, y por eso se redimensiona en torno a α = 0,75. A la derecha, el reparto real de 1.000 claves entre 1.024 cubetas al azar: 390 cubetas quedan vacías y la cadena más larga llega a 5 claves, así que la búsqueda de esa clave no es O(1) sino O(5). El O(1) es un coste medio, no una promesa.
fuente: figuras/tablas-hash-1.py
:::

## Ejemplo

Queremos guardar 6 palabras en una tabla de `m = 8` cubos con encadenamiento. Usamos la
función de dispersión de Java para cadenas, que es una suma ponderada de los caracteres y que
va reduciendo el resultado en cada paso para que los números no crezcan:

```
h ← 0
para cada carácter ch de la cadena:  h ← (h · 31 + código(ch)) mod m
```

donde `código(ch)` es el código del carácter (ASCII). El índice final es `h`, ya reducido a un
valor entre 0 y m−1: el residuo no cambia por aplicarlo en cada paso o solo al final, pero
hacerlo en cada paso evita enteros gigantes. Las palabras son: `sol`, `luna`, `mar`, `rio`,
`cielo`, `nube`.

Los códigos ASCII son `'a'` = 97, `'c'` = 99, `'e'` = 101, `'i'` = 105, `'l'` = 108, `'m'` = 109,
`'n'` = 110, `'o'` = 111, `'r'` = 114, `'s'` = 115, `'u'` = 117. Calculamos `mar` paso a paso,
con `m = 8`:

- h empieza en 0.
- `'m'` = 109 → h = 0 · 31 + 109 = 109; 109 mod 8 = 5.
- `'a'` = 97 → h = 5 · 31 + 97 = 252; 252 mod 8 = 4.
- `'r'` = 114 → h = 4 · 31 + 114 = 238; 238 mod 8 = 6.
- Resultado: h = 6 → **cubo 6**.

Repitiendo con las demás:

| Palabra | h mod 8 (cubo) |
| --- | --- |
| sol | 0 |
| luna | 4 |
| mar | 6 |
| rio | 0 |
| cielo | 2 |
| nube | 2 |

Seis claves en 8 cubos: los cubos 0, 2, 4 y 6 quedan ocupados, los impares vacíos, y hay **dos
colisiones**: `sol` con `rio` en el cubo 0, y `cielo` con `nube` en el cubo 2. El factor de
carga es α = 6 / 8 = 0,75, justo en el umbral en el que una implementación real
redimensionaría.

Las colisiones no dependen de que las palabras se parezcan: `cielo` y `nube` no tienen nada en
común y aun así comparten cubo, porque la posición la decide el resto de dividir entre 8, y
solo hay 8 restos posibles.

Buscar `mar` cuesta una operación: calcular h, ir al cubo 6 y comparar con el único par que
hay. El coste medio, en cambio, lo marcan los cubos con dos elementos: buscar `nube` cuesta dos
pasos, cubo 2, comparar con `cielo` (no coincide) y comparar con `nube` (sí). Ese «1 + longitud
de la cadena» es exactamente el coste O(1 + α).

## Código

```python verificable
# Tabla hash con encadenamiento, el mecanismo que hay dentro de un dict.
def dispersion_java(s, m):
    """Hash de cadenas estilo Java, reducido modulo m."""
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) % m   # el modulo en cada paso evita numeros gigantes
    return h

m = 8
palabras = ["sol", "luna", "mar", "rio", "cielo", "nube"]
cubos = [[] for _ in range(m)]

for p in palabras:
    cubos[dispersion_java(p, m)].append(p)

print("ocupacion por cubo:", [len(c) for c in cubos])   # -> [2, 0, 2, 0, 1, 0, 1, 0]
print("factor de carga:", round(len(palabras) / m, 2))  # -> 0.75

# Buscar 'mar': el cubo 6 tiene un solo elemento, asi que basta una comparacion
cubo = cubos[dispersion_java("mar", m)]
print("cadena del cubo", dispersion_java("mar", m), ":", cubo)  # -> cadena del cubo 6 : ['mar']
print("comparaciones:", cubo.index("mar") + 1)                  # -> 1
```

:::claves
- `h = (h * 31 + ord(ch)) % m` aplica el módulo **en cada paso**, no al final. El residuo es el mismo, pero los números no crecen sin límite y la operación se mantiene barata. Quitar ese `% m` no cambia el cubo final y sí cambia el coste.
- `[[] for _ in range(m)]` crea **m listas distintas**; `[[]] * m` crea una sola lista repetida m veces y todas las claves acabarían en el mismo cubo. Es el error clásico con listas mutables.
- `cubo.index("mar") + 1` cuenta las comparaciones reales: `index` recorre la cadena desde el principio, así que un elemento al final de una cadena larga cuesta más. Ese es exactamente el O(1 + α) de la teoría.
- `sum(c - 1 for c in cuenta.values() if c > 1)` cuenta **claves de más**, no cubos ocupados: un cubo con 3 claves aporta 2. Si lo que quieres es cuántos cubos están ocupados, es `len(cuenta)`.
- `del d["clave"]` libera el hueco, pero la tabla no se reordena: ese hueco queda como **tumba**
  y el diccionario solo reaprovecha el espacio en una reconstrucción posterior (al insertar con
  suficientes huecos liberados, o cuando reduce el tamaño). Borrar e insertar mucho sin parar
  pasa por ese estado intermedio sin que nada falle.
- Dos claves iguales **tienen que dar el mismo hash**, pero el contrario no se exige. Definir `__eq__` sin `__hash__` deja `__hash__` en `None` y el objeto deja de poder ser clave: Python lo bloquea a propósito.
:::

```python verificable
# Modulo primo frente a potencia de 2: la misma familia de claves, dos repartos.
claves = [1024, 2048, 3072, 4096, 5120, 6144]   # todas multiplos de 1024

def colisiones(valores, m):
    """Cuantos valores comparten cubo con otro: 0 seria un reparto perfecto."""
    cuenta = {}
    for v in valores:
        cuenta[v % m] = cuenta.get(v % m, 0) + 1
    return sum(c - 1 for c in cuenta.values() if c > 1)

print("modulo 1024, potencia de 2  colisiones:", colisiones(claves, 1024))  # -> 5
print("modulo 1009, primo         colisiones:", colisiones(claves, 1009))  # -> 0
print("cubos ocupados con 1024:", len({k % 1024 for k in claves}))         # -> 1
print("cubos ocupados con 1009:", len({k % 1009 for k in claves}))         # -> 6
```

El ejemplo no depende de que Python mezcle los enteros con `hash`: el sesgo está en el módulo.
Cuando las claves comparten un factor con el tamaño de la tabla, el resto solo puede tomar los
valores de ese factor y el reparto se hunde. Por eso las tablas de tamaño primo son más
tolerantes con claves «redondas», y por eso las que usan potencias de 2 compensan con una
función de mezcla que rompa esos patrones.

```python ilustrativo
d = {}
d["clave"] = 1
d["clave"]            # lectura: O(1) de media
del d["clave"]        # borrado: O(1) de media
"clave" in d          # pertenencia: O(1) de media, sin recorrer el diccionario
```

## Errores típicos

- **Usar objetos mutables como clave.** Una lista o un diccionario no pueden ser clave en
  Python porque su contenido cambia y el hash dejaría de ser válido. Si necesitas una clave
  compuesta, usa una tupla.
- **Mutar la clave después de insertarla.** El par queda guardado en el cubo que le tocó con
  el valor viejo del hash. Al buscar con la clave ya modificada, la función da otro cubo, no
  se encuentra nada y el objeto aparece como «perdido» dentro de la tabla. Es un fallo
  silencioso: no lanza error, simplemente devuelve que no está.
- **Romper el contrato entre igualdad y hash.** Si defines `__eq__` para tus objetos y no
  defines `__hash__` acorde, dos objetos iguales pueden acabar en cubos distintos y la tabla
  guarda duplicados. La regla: si `a == b`, entonces `hash(a) == hash(b)`.
- **Contar con O(1) garantizado.** El O(1) es promedio. Con una función de dispersión mala, o
  con claves elegidas por un atacante para colisionar, el coste real es O(n). Si aceptas claves
  de fuera, no uses una función de dispersión tuya y trivial.
- **Esperar un orden.** Recorrer un diccionario o un conjunto no da las claves ordenadas. En
  Python los diccionarios conservan el orden de inserción, pero eso es una propiedad del
  diccionario, no de las tablas hash en general, y un `set` no la ofrece.
- **Elegir el tamaño como potencia de 2 con claves que comparten factores.** Si `m = 1024` y
  todas tus claves terminan en `000`, el módulo devuelve siempre los mismos pocos cubos. Con
  potencias de 2 hace falta una buena función de mezcla; con un primo, el módulo ya reparte
  mejor.

:::practica
enunciado: Una tabla hash con encadenamiento tiene 1.000 cubos y 850 pares, y redimensiona al superar un factor de carga de 0,75. Calcula el factor actual, decide si redimensiona y calcula el nuevo factor si duplica a 2.000 cubos. ¿Cuántos pares tiene la cadena media en cada caso?
pista: El factor de carga es pares dividido entre cubos, y la cadena media mide exactamente eso.
solucion: α = 850 / 1.000 = 0,85, por encima del umbral 0,75, así que se redimensiona a 2.000 cubos y se reinsertan los 850 pares. El nuevo factor es α = 850 / 2.000 = 0,425: la cadena media baja de 0,85 a 0,425 pares. La búsqueda sigue siendo O(1 + α) de media, con la reubicación pagada una sola vez. Conclusión: redimensionar compra margen, no una garantía, porque el peor caso sigue siendo O(n).
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué ocurre si insertas una clave en un diccionario y después modificas el objeto que usaste como clave?
o: El diccionario redimensiona automáticamente y recoloca la entrada
o: La entrada queda en el cubo antiguo y buscarla con el nuevo hash no la encuentra
o: El diccionario lanza un error de clave duplicada
a: 2
e: La posición se calculó con el hash del valor en el momento de insertar. Al cambiar el objeto cambia el hash, la búsqueda mira en otro cubo y no encuentra nada, aunque la entrada siga ocupando memoria. Por eso las claves deben ser inmutables.
:::

:::quiz
p: Una tabla tiene 600 elementos y 1.000 cubos con encadenamiento. ¿Qué se puede afirmar del coste de búsqueda?
o: Es O(1) en el peor caso porque el factor de carga es menor que 1
o: Es O(1 + α) de media, con α = 0,6, pero puede degradarse a O(n) si todas las claves caen en el mismo cubo
o: Es O(log n) porque el encadenamiento mantiene cada cubo ordenado
a: 2
e: Con α = 600 / 1000 = 0,6, el cubo medio tiene menos de un par y la búsqueda es constante de media. El peor caso no lo fija el factor de carga, sino la distribución: si las 600 claves colisionan, se recorre una lista de 600. Y el encadenamiento no ordena nada.
:::

:::trampa
Los conjuntos y diccionarios de Python solo adoptaron la aleatorización del hash de cadenas
(PYTHONHASHSEED) para frenar ataques por colisiones: sin ella, quien elija las claves puede
forzar que todas caigan en el mismo cubo y convertir una operación constante en lineal. Si
escribes una estructura propia que recibe claves de fuera, no repitas el error.
:::
