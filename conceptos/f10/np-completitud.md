---
id: np-completitud
titulo: NP-completitud
fase: 10
nivel: experto
rutas: [alg, core]
prerequisitos: [complejidad-asintotica, programacion-dinamica, algoritmos-greedy, grafos-representacion]
tags: [complejidad, np, reducciones, teoria]
resumen: La frontera entre lo que se puede resolver rápido y lo que solo se puede comprobar rápido, y por qué una reducción convierte un problema en otro.
fuentes: ["Cook (1971), 'The complexity of theorem-proving procedures'", "Karp (1972), 'Reducibility among combinatorial problems'", "Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 34", "Garey y Johnson (1979), 'Computers and Intractability'"]
---

## En una frase

Un problema es NP-completo si pertenece a NP —sus soluciones se comprueban rápido— y cualquier
otro problema de NP se puede transformar en él en tiempo polinómico, de modo que resolverlo
rápido resolvería todos los demás; nadie ha encontrado ese algoritmo y hay razones para pensar
que no existe.

## La idea

Hay una diferencia que cuesta ver hasta que se ve, y es esta: **comprobar una solución es mucho
más fácil que encontrarla**.

- Te doy un tablero de sudoku resuelto: en un par de minutos compruebas si las reglas se cumplen.
  Encontrarlo desde cero te puede costar una tarde.
- Te doy cinco números y te digo que tres de ellos suman exactamente 100, y me dices cuáles: lo
  compruebas en tres sumas. Encontrar esos tres entre veinte números ya cuesta, y entre cien es
  inabordable a mano.
- Te doy una ruta que pasa por 40 ciudades: comprobar su longitud es una suma. Encontrar la más
  corta es el problema del viajante, y con 40 ciudades hay más rutas posibles que átomos en el
  universo observable.

Esa asimetría es el corazón de NP. **P** es la clase de los problemas que se **resuelven** en
tiempo polinómico (ordenar, buscar, caminos mínimos, programación lineal). **NP** es la clase de
los problemas cuyas soluciones se **comprueban** en tiempo polinómico, sin exigir que se
encuentren rápido. Todo lo de P está en NP (si sabes resolverlo rápido, sabes comprobar la
solución), pero la pregunta de si P = NP está abierta desde 1971 y es uno de los problemas del
milenio.

Lo que sí se ha demostrado es que **dentro de NP hay problemas que son los más difíciles de
todos**: si existiera un algoritmo polinómico para uno cualquiera de ellos, existiría para todos.
Son los **NP-completos**. La herramienta que lo demuestra es la **reducción**: transformar una
instancia de un problema `A` en una instancia de un problema `B`, de forma que resolver `B`
resuelva `A`. Si esa transformación cuesta tiempo polinómico, entonces «`B` es al menos tan
difícil como `A`». Encadenando reducciones desde un problema inicial, Cook demostró en 1971 que
el problema de satisfacibilidad booleana (SAT) es NP-completo, y Karp añadió 21 problemas más en
1972.

La consecuencia práctica es lo que importa en el día a día: cuando te enfrentas a un problema
NP-duro (la versión de optimización, al menos tan difícil como el NP-completo de decisión), no
pierdas semanas buscando el algoritmo exacto y eficiente. Las salidas honestas son:

- **Instancias pequeñas o con estructura especial.** El viajante con 15 ciudades se resuelve por
  programación dinámica en `O(n² · 2ⁿ)`: 15 · 32768, perfectamente abordable. Con 40, no.
- **Aproximar con garantía.** [[algoritmos-de-aproximacion|Los algoritmos de aproximación]]
  renuncian al óptimo a cambio de una cota demostrada.
- **Resolver de forma exacta con un solver.** Los solvers de programación entera y SAT resuelven
  en la práctica instancias reales mucho más grandes de lo que su peor caso sugiere. La teoría
  dice que el peor caso es malo; no dice que tu caso lo sea.

:::figura
fichero: np-completitud-verificar-y-buscar
pie: Izquierda: la asimetría del tema, en operaciones y con el eje vertical en escala logarítmica. Buscar un subconjunto que sume el objetivo cuesta 2ⁿ intentos (rojo) y comprobar un candidato cuesta n sumas (azul): con 30 números son 1.073.741.824 intentos frente a 30 sumas, y con 60 las asignaciones posibles (1,15 · 10¹⁸) superan los segundos que ha vivido el universo, marcados con la línea morada. Lo que hay que mirar es la forma de cada curva: la azul no se hace difícil al crecer la instancia, la roja sí. Derecha: el mapa de las clases, con las inclusiones demostradas (P dentro de NP y NP dentro de PSPACE) y la franja de los NP-completos, que quedaría fuera de P si la conjetura P ≠ NP es cierta. Cada región lleva un ejemplo y una cifra; fuera del óvalo grande queda lo indecidible, como la parada de una máquina de Turing, que no tiene algoritmo ninguno.
fuente: figuras/np-completitud-1.py
:::

## Definición formal

Un **problema de decisión** es aquel cuya respuesta es sí o no. Se formaliza como un lenguaje
`L ⊆ {0,1}*`: el conjunto de codificaciones de instancias con respuesta sí.

- **P:** `L ∈ P` si existe un algoritmo que decide si `x ∈ L` en tiempo `O(n^k)` para alguna
  constante `k`, con `n` el tamaño de `x` en bits.
- **NP:** `L ∈ NP` si existe un algoritmo verificador `V` y una constante `k` tales que
  `x ∈ L` si y solo si existe un **certificado** `y` con longitud `O(n^k)` y `V(x, y)` termina en
  tiempo `O(n^k)`. Al certificado se le llama también testigo: es la solución candidata.
- **Reducción polinómica:** `A ≤ₚ B` si existe una función `f` computable en tiempo polinómico
  tal que `x ∈ A` si y solo si `f(x) ∈ B`. Es decir: `B` resuelve `A` a través de `f`.
- **NP-duro:** `L` es NP-duro si para todo `A ∈ NP` se cumple `A ≤ₚ L`. No se exige que `L`
  esté en NP; puede ser incluso indecidible.
- **NP-completo:** `L` es NP-completo si `L ∈ NP` y `L` es NP-duro. Es la intersección de las
  dos condiciones, y las dos hay que demostrarlas.

La relación entre las clases, hoy:

:::formula
P ⊆ NP ⊆ PSPACE,   y se conjetura P ≠ NP
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `L` | lenguaje: el conjunto de instancias cuya respuesta es sí | conjunto de cadenas | define el problema de decisión, no la versión de optimización |
| `x` | instancia concreta del problema | una cadena de bits | su tamaño n es lo que se mide |
| `n` | tamaño de la instancia en bits | bits | el coste se mide en función de n, no del valor de los números |
| `y` | certificado o testigo: la solución candidata | una cadena de bits | su longitud está acotada por O(n^k) |
| `V(x, y)` | verificador polinómico: dice si y prueba que x ∈ L | verdadero o falso | su coste es O(n^k) y no depende de lo difícil que sea encontrar y |
| `k` | exponente constante del polinomio que acota el coste | adimensional | separa las clases: P, NP y PSPACE se definen con uno |
| `A ≤ₚ B` | reducción polinómica: B resuelve A a través de f | adimensional | si A ≤ₚ B, entonces B es al menos tan difícil como A |
| `W` | capacidad de la mochila, en la versión de decisión | unidades de capacidad | entra como valor: por eso el algoritmo Θ(n · W) es pseudopolinómico |
:::

donde `PSPACE` es la clase de los problemas resolubles con memoria polinómica. Lo único que se
sabe con certeza es la inclusión; la desigualdad es una conjetura, aunque el hecho de que
décadas de esfuerzo no hayan producido un algoritmo polinómico para ningún NP-completo es la
evidencia informal más citada a su favor.

**Los tres ingredientes de una demostración de NP-completitud:**

1. **Pertenencia a NP.** Describir el certificado y el verificador polinómico. Sin este paso,
   como mucho se demuestra que el problema es NP-duro.
2. **Elección del problema base.** Un problema ya conocido como NP-completo (SAT, 3-SAT,
   clique, recubrimiento de vértices, mochila de decisión, viajante de decisión, coloración de
   grafos…).
3. **La reducción.** Construir `f` del problema base al tuyo, en tiempo polinómico, y demostrar
   las dos direcciones: si la instancia base tiene solución, la transformada también; y si la
   transformada tiene solución, se puede recuperar una de la base.

Una reducción mal hecha falla casi siempre en la segunda dirección y el error pasa inadvertido,
porque la primera suele ser la fácil de escribir.

## Ejemplo

**Subset sum (suma de subconjuntos).** Dados `{3, 34, 4, 12, 5, 2}` y un objetivo 9, ¿hay un
subconjunto que sume exactamente 9? La respuesta es sí: 4 + 5 = 9, y también 3 + 4 + 2 = 9.

- **Comprobar** la solución `{4, 5}` cuesta dos sumas: es polinómico, así que el problema está en
  NP.
- **Encontrarla** probando todos los subconjuntos cuesta `2⁶ = 64` comprobaciones con 6 números.
  Con 30 números son `2³⁰ = 1.073.741.824`, más de mil millones; con 60, más que segundos ha
  vivido el universo. La comprobación, en cambio, sigue costando 30 sumas.

Esa es la asimetría en números: **30 sumas para verificar frente a mil millones de intentos para
encontrar**.

**Reducción de 3-SAT a clique (esbozo).** Una fórmula en 3-SAT es una conjunción de cláusulas de
tres literales cada una; el problema pregunta si existe una asignación de verdad que la haga
cierta. La construcción clásica crea un vértice por cada literal de cada cláusula (3 vértices por
cláusula), une dos vértices si están en cláusulas distintas y no son literales complementarios
(`x` y `¬x`), y pregunta si hay un clique de tamaño igual al número de cláusulas. Un clique así
elige un literal por cláusula sin contradicciones, y eso es exactamente una asignación
satisfactoria. La transformación es lineal en el tamaño de la fórmula, y la equivalencia va en
las dos direcciones: ese es el patrón de toda reducción.

**Dónde cae cada problema.** Tener el mapa a mano ahorra semanas de trabajo:

| Problema | Clase | Qué significa en la práctica |
| --- | --- | --- |
| Ordenar, buscar | P | Hay algoritmos n log n y nadie busca más |
| Camino más corto (pesos no negativos) | P | Dijkstra resuelve |
| Programación lineal | P | Solvers de interior point y símplex |
| Mochila 0/1 (decisión) | NP-completo | Solo hay pseudopolinómico en W |
| Viajante de comercio (decisión) | NP-completo | Instancias reales se atacan con solvers |
| Satisfacibilidad (SAT) | NP-completo | Primer problema demostrado, base de todo |
| Clique, recubrimiento de vértices | NP-completo | Reducciones de SAT y entre ellos |
| Parada de una máquina de Turing | Indecidible | No es que sea difícil: no existe algoritmo |

La última fila recuerda algo importante: NP-completo no es lo peor que existe. Los problemas
indecidibles no tienen algoritmo **ninguno**, ni lento ni rápido.

## Código

```python verificable
from itertools import combinations

def subset_sum_verificar(numeros, objetivo, certificado):
    """Verificar es polinomico: basta sumar el candidato y comprobar."""
    return sum(certificado) == objetivo and set(certificado) <= set(numeros)

def subset_sum_buscar(numeros, objetivo):
    """Buscar es exponencial: hay que probar subconjuntos de todos los tamanos."""
    intentos = 0
    for tam in range(len(numeros) + 1):
        for candidato in combinations(numeros, tam):
            intentos += 1
            if sum(candidato) == objetivo:
                return list(candidato), intentos
    return None, intentos

numeros = [3, 34, 4, 12, 5, 2]
solucion, intentos = subset_sum_buscar(numeros, 9)
print("solucion:", solucion)                    # -> solucion: [4, 5]
print("intentos de busqueda:", intentos)        # -> intentos de busqueda: 18
print("verificacion:", subset_sum_verificar(numeros, 9, solucion))   # -> verificacion: True
print("subconjuntos posibles con n=6:", 2 ** 6)  # -> subconjuntos posibles con n=6: 64
```

:::claves
- `subset_sum_verificar` devuelve un `bool` de Python y evalúa las dos condiciones en **cortocircuito**: si la suma no cuadra, ni siquiera mira la contención. Verificar es sumar y comparar, nada más.
- `set(certificado) <= set(numeros)` es contención de **conjuntos**, no una comparación numérica. Y como los conjuntos no guardan repeticiones, un certificado `[5, 5]` pasaría la comprobación aunque el 5 aparezca una sola vez en `numeros`: el verificador acepta soluciones que no existen.
- `sum([])` vale 0, así que el subconjunto vacío es un candidato válido: con objetivo 0, `subset_sum_buscar` devuelve `[]` como solución y gasta un solo intento.
- `subset_sum_buscar` recorre los subconjuntos **por tamaño creciente** y devuelve el primero que encuentra: con `{3, 34, 4, 12, 5, 2}` y objetivo 9 sale `[4, 5]` después de 18 intentos, y no la otra solución 3 + 4 + 2, que también existe.
- `intentos` cuenta los subconjuntos probados, incluido el que acierta y los de tamaño 0 y 1: 18 de los 64 posibles con n = 6. No es una estimación teórica, es el coste real de encontrar.
- `2 ** 6` es exacto porque son enteros de Python. Con un entero de 64 bits, `2 ** 63` ya desbordaría: en un ejemplo que trata de contar combinaciones, el tipo de dato forma parte del argumento.
:::

```python verificable
from itertools import product

def evaluar(clausulas, asignacion):
    """Una clausula es una tupla de literales; el literal i>0 es x_i y i<0 es not x_i."""
    for clausula in clausulas:
        if not any((asignacion[abs(lit) - 1] if lit > 0 else not asignacion[abs(lit) - 1])
                   for lit in clausula):
            return False
    return True

def sat_bruto(clausulas, n_variables):
    """Busca la asignacion satisfactoria probando las 2^n posibilidades."""
    probadas = 0
    for bits in product([False, True], repeat=n_variables):
        probadas += 1
        if evaluar(clausulas, bits):
            return bits, probadas
    return None, probadas

# (x1 or x2 or x3) and (not x1 or not x2 or x3)
clausulas = [(1, 2, 3), (-1, -2, 3)]
asignacion, probadas = sat_bruto(clausulas, 3)
print("asignacion:", asignacion)              # -> asignacion: (False, False, True)
print("probadas:", probadas, "de", 2 ** 3)    # -> probadas: 2 de 8
print("todas ciertas:", evaluar(clausulas, asignacion))   # -> todas ciertas: True
```

```python verificable
import time

# La verificacion no crece con el problema; la busqueda si. Mismo problema, dos costes.
def verificar_subconjunto(numeros, objetivo, elegidos):
    return sum(numeros[i] for i in elegidos) == objetivo

def contar_subconjuntos_posibles(n):
    return 2 ** n

for n in (10, 20, 30):
    print(f"n={n:>2}  combinaciones={contar_subconjuntos_posibles(n):>12,}  "
          f"sumas para verificar={n:>3}")
# -> n=10  combinaciones=       1,024  sumas para verificar= 10
# -> n=20  combinaciones=   1,048,576  sumas para verificar= 20
# -> n=30  combinaciones=1,073,741,824  sumas para verificar= 30

inicio = time.perf_counter()
comprobado = verificar_subconjunto(list(range(30)), 15, [0, 1, 2, 3, 4, 5])
micros = (time.perf_counter() - inicio) * 1e6
print("verificacion de 6 indices:", comprobado, f"en {micros:.1f} us")
print("es polinomica:", micros < 1000)       # -> es polinomica: True
```

## Errores típicos

- **Decir «NP» cuando quieres decir «no polinómico».** NP significa *nondeterministic
  polynomial*: problemas cuyas soluciones se verifican en tiempo polinómico. Ordenar está en P y
  también en NP. La frase «este problema es NP, luego no se puede resolver rápido» es falsa por
  partida doble: NP incluye problemas fáciles y no se sabe si P ≠ NP.
- **Confundir NP-duro con NP-completo.** NP-duro no exige pertenecer a NP, así que hay problemas
  NP-duros que ni siquiera son decidibles. NP-completo es NP-duro **y** estar en NP. Si solo
  demuestras la reducción desde un problema NP-completo, has demostrado NP-duro, no
  NP-completo.
- **Olvidar demostrar que el problema está en NP.** Es el paso que se salta todo el mundo. Sin
  él, la demostración está a medias: podrías haber probado que un problema indecidible es
  NP-duro, lo cual es cierto y no dice nada útil sobre su dificultad relativa a NP.
- **Hacer la reducción en la dirección equivocada.** Para demostrar que tu problema `B` es
  NP-duro hay que reducir **desde** un problema NP-completo conocido `A` **hacia** `B`
  (`A ≤ₚ B`). Reducir tu problema al problema conocido demuestra lo contrario: que el conocido es
  al menos tan difícil, que ya se sabía.
- **Reducciones que no son polinómicas.** Si la transformación tarda tiempo exponencial, no
  demuestra nada: cualquier problema se reduce a cualquier otro con tiempo suficiente. La
  reducción tiene que construir la instancia nueva en tiempo polinómico en el tamaño de la
  original.
- **Creer que un problema NP-duro es intratable en la práctica.** La NP-dureza es un enunciado
  sobre el peor caso y sobre familias de instancias. Los solvers de SAT y de programación entera
  resuelven a diario instancias industriales enormes porque tienen estructura. Antes de rendirte,
  mide en tus datos.

:::aviso
La mochila 0/1 tiene un algoritmo `Θ(n · W)` y es NP-completa. No hay contradicción: `W` entra
como valor, no como número de bits, y por eso se dice pseudopolinómico. Si `W` se escribe con
`b` bits, el coste es exponencial en `b`. Este matiz es el que separa a quien ha entendido la
teoría de complejidad de quien ha memorizado una tabla.
:::

:::practica
enunciado: Con los números {2, 5, 9, 12, 17, 20, 33, 41} y objetivo 46, ¿cuántos subconjuntos hay que probar en el peor caso y cuántas sumas cuesta verificar el certificado {5, 9, 12, 20}? Encuentra además otro subconjunto que también sume 46.
pista: Buscar recorre los 2ⁿ subconjuntos; verificar solo suma el candidato y lo compara con el objetivo. Los dos costes viven en escalas distintas.
solucion: Con n = 8 hay 2⁸ = 256 subconjuntos que probar. Verificar {5, 9, 12, 20} cuesta 3 sumas parciales y una comparación: 5 + 9 + 12 + 20 = 46, correcto. Otro subconjunto válido es {9, 17, 20}, que también suma 46. La asimetría del tema, en números: 256 intentos frente a 3 sumas.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué significa exactamente que un problema esté en NP?
o: Que no se puede resolver en tiempo polinómico
o: Que sus soluciones se pueden comprobar en tiempo polinómico
o: Que su mejor algoritmo es exponencial
a: 2
e: NP se define por la existencia de un verificador polinómico que, dado un certificado, decide si la instancia tiene respuesta sí. P está contenido en NP, así que hay problemas de NP que se resuelven rápido. Que el mejor algoritmo conocido sea exponencial no entra en la definición, y para muchos problemas no se sabe si existe uno polinómico.
:::

:::quiz
p: Quieres demostrar que tu problema B es NP-completo. ¿Qué dos cosas necesitas?
o: Demostrar que B está en NP y reducir un problema NP-completo conocido A a B en tiempo polinómico
o: Demostrar que B no tiene algoritmo polinómico y reducir B a SAT
o: Encontrar un algoritmo exponencial para B y compararlo con otro problema difícil
a: 1
e: La pertenencia a NP se justifica con el certificado y el verificador; la dureza, con una reducción A ≤ₚ B desde un problema ya NP-completo. Reducir B a SAT demuestra lo contrario de lo que se necesita, y un algoritmo exponencial no demuestra nada sobre la dificultad intrínseca: siempre puede aparecer uno mejor.
:::

:::quiz
p: La mochila 0/1 es NP-completa y a la vez tiene un algoritmo Θ(n · W). ¿Cómo se explica?
o: La complejidad NP solo se aplica a problemas sin solución algorítmica
o: W entra como valor, no como número de bits, así que el algoritmo es pseudopolinómico y no polinómico en el tamaño de la entrada
o: Θ(n · W) es en realidad exponencial, y por eso no hay contradicción
a: 2
e: El tamaño de la entrada se mide en bits. Escribir W necesita log₂ W bits, y duplicar ese número de bits multiplica W por una potencia enorme: el coste crece exponencialmente respecto al tamaño real de la entrada. La NP-completitud es un enunciado sobre el tamaño en bits, y por eso el algoritmo de la tabla no la contradice.
:::
