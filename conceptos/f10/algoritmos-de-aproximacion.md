---
id: algoritmos-de-aproximacion
titulo: Algoritmos de aproximación
fase: 10
nivel: experto
rutas: [alg, quant]
prerequisitos: [np-completitud, algoritmos-greedy, complejidad-asintotica]
tags: [aproximacion, np-duro, garantias, optimizacion]
resumen: Cuando el óptimo es inalcanzable en tiempo razonable, se renuncia a él a cambio de una garantía demostrable sobre cuánto se aleja la solución.
fuentes: ["Vazirani (2001), 'Approximation Algorithms'", "Motwani y Raghavan (1995), 'Randomized Algorithms'", "Feige (1998), 'A threshold of ln n for approximating set cover'"]
---

## En una frase

Un algoritmo de aproximación resuelve en tiempo polinómico un problema NP-duro y devuelve una
solución acompañada de una **garantía demostrada**: «esta solución nunca costará más del doble
que la mejor posible», o «nunca cubrirá menos de dos tercios de lo máximo cubrible».

## La idea

Estás reformando un piso y pides presupuesto. Un contratista te dice «lo hago y ya veremos»: eso
es una **heurística**, y no sabes si la factura será el doble o cien veces más. Otro te dice «te
garantizo que no pagarás más del doble de lo mínimo que costaría esto, y lo demuestro». Eso es un
**algoritmo de aproximación**. Los dos pueden acabar cobrándote lo mismo; la diferencia es que
con el segundo sabes de antemano cuál es el peor escenario y puedes decidir si te vale.

Formalmente: para un problema de **minimización** como el recubrimiento de vértices, un algoritmo
es **ρ-aproximado** si para toda instancia `I` devuelve una solución factible cuyo coste es como
mucho `ρ` veces el óptimo. Para un problema de **maximización**, la desigualdad va al revés y `ρ`
es mayor que 1 si se expresa como cociente entre el óptimo y lo obtenido.

Tres cosas que hay que entender bien, porque son las que se malinterpretan:

1. **La garantía es del peor caso, no de tu caso.** El recubrimiento de vértices con
   emparejamiento maximal garantiza «como mucho el doble del óptimo», y en muchas instancias da
   el óptimo exacto. Lo que la garantía te dice es que *ninguna* instancia puede hacerlo peor,
   no que tu instancia vaya a salir mal.
2. **La garantía se demuestra, no se mide.** Comparar tu algoritmo con un óptimo calculado por
   fuerza bruta en 20 instancias pequeñas no demuestra nada sobre las grandes. La demostración
   usa una **cota inferior** del óptimo, típicamente un objeto que cualquier solución debe pagar
   (un emparejamiento disjunto, la suma de los elementos menos cubiertos).
3. **No todos los problemas admiten lo mismo.** Algunos tienen esquemas de aproximación que se
   acercan al óptimo tanto como quieras (la mochila); otros tienen un umbral por debajo del cual
   aproximar es tan difícil como resolver el problema exacto (el recubrimiento de conjuntos).

La segunda mitad del tema es la parte incómoda y es lo que lo hace interesante: la **dificultad
de aproximación**. El teorema PCP implica que para ciertos problemas existe un umbral `ρ*` tal
que aproximar mejor que `ρ*` es NP-duro. Es decir, a veces el mejor algoritmo posible ya se
conoce, no porque se haya encontrado, sino porque se ha demostrado que no puede existir otro
mejor salvo que P = NP.

## Definición formal

Sea `I` una instancia y `OPT(I)` el valor de la solución óptima.

- **Minimización:** un algoritmo `A` es **ρ-aproximado** (con `ρ ≥ 1`) si para toda instancia
  devuelve una solución factible con:

:::formula
A(I) ≤ ρ · OPT(I)
:::

- **Maximización:** `A` es **ρ-aproximado** si `A(I) ≥ OPT(I) / ρ`, es decir, obtiene al menos
  una fracción `1/ρ` del óptimo.
- `ρ` puede depender del tamaño de la entrada `n`; entonces se escribe `ρ(n)`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `I` | Una instancia concreta del problema (un grafo, una mochila, unos conjuntos) | el problema | No es una palanca: es el caso que te ha tocado |
| `OPT(I)` | El valor de la mejor solución posible de esa instancia | las del objetivo (vértices, conjuntos, distancia) | Solo cambia con la instancia, no con el algoritmo |
| `A(I)` | El valor de la solución que devuelve el algoritmo | las del objetivo | Es lo que se mide; `OPT(I) / A(I)` es el cociente real |
| `ρ` | El factor garantizado del peor caso | adimensional, `ρ ≥ 1` | Cuanto mayor, más floja es la garantía; con `ρ = 1` sería exacto |
| `n` | Tamaño de la entrada (vértices, elementos, objetos) | unidades | Alarga el tiempo y puede empeorar `ρ(n)`: el voraz de conjuntos garantiza `H_n ≈ ln n` |
| `ε` | Margen de error que aceptas en un PTAS o FPTAS | fracción del óptimo | El tiempo de cómputo se desploma, pero la solución se aleja del óptimo: la tabla del FPTAS crece como `1/ε` |
:::

:::figura
fichero: algoritmos-de-aproximacion-precio-y-optimo
pie: A la izquierda, lo que cuesta afinar el error: con ε = 0,1 el FPTAS tiene que resolver unos 3.000 valores distintos, y con ε = 0,0001 son más de tres millones, porque la escala de valores crece como 1/ε. A la derecha está la parte incómoda: 200 grafos pequeños con el recubrimiento de vértices óptimo calculado por fuerza bruta. En azul, todas las instancias del FPTAS caen en el 1,00 (y su garantía, 1,10, no se toca). En naranja, el algoritmo 2-aproximado del emparejamiento maximal se queda de mediana en 1,56 y llega hasta el 2,00 exacto: la garantía no es un adorno, hay instancias que la alcanzan. Ahí está la lección: la cota es una promesa sobre el peor caso, no una predicción de lo que pasará con la instancia que tienes delante.
fuente: figuras/algoritmos-de-aproximacion-1.py
:::

**Esquemas de aproximación.** Un **PTAS** (esquema de aproximación polinómico) es una familia de
algoritmos que, para cada `ε > 0`, da una `(1 + ε)`-aproximación en tiempo polinómico en `n`
(pero puede ser exponencial en `1/ε`, por ejemplo `O(n^{1/ε})`). Un **FPTAS** es más fuerte:
polinómico en `n` **y** en `1/ε`. La mochila 0/1 tiene FPTAS; el viajante **euclídeo** tiene
PTAS (Arora, 1998), mientras que el métrico general no lo tiene salvo que P = NP; y el
recubrimiento de conjuntos, como se ve abajo, está todavía más lejos.

**Cinco resultados que conviene tener a mano:**

1. **Recubrimiento de vértices, factor 2.** Se calcula un emparejamiento **maximal** `M`
   (conjunto de aristas disjuntas al que no se le puede añadir ninguna más) y se toma como
   recubrimiento **los dos extremos de cada arista de `M`**. Es factible porque toda arista del
   grafo toca a alguna arista de `M` (si no, `M` no sería maximal). Y es 2-aproximado porque
   cualquier recubrimiento debe incluir al menos un extremo de cada arista de `M`, y esas aristas
   son disjuntas: `OPT ≥ |M|`, mientras que la solución tiene `2|M|` vértices.
2. **Recubrimiento de conjuntos, factor `H_n`.** El algoritmo voraz elige en cada paso el
   conjunto que cubre más elementos aún no cubiertos. Su garantía es el **número armónico**
   `H_n ≈ ln n + 0,5772`, donde `n` es el número de elementos del universo y `0,5772` es la
   constante de Euler-Mascheroni. Es decir, un factor logarítmico, no constante.
3. **Viajante métrico, factor 2 (y 3/2 con Christofides).** Si las distancias cumplen la
   desigualdad triangular, construir el árbol de expansión mínima y recorrerlo en preorden da un
   tour de coste como mucho el doble del óptimo. El algoritmo de Christofides (1976) baja el
   factor a `3/2` y fue el mejor conocido durante décadas.
4. **MAX-3SAT, factor 8/7.** Asignar cada variable a cara o cruz satisface en espera `7/8` de
   las cláusulas, y la aleatoriedad se puede eliminar con el método de las expectativas
   condicionales, obteniendo un algoritmo determinista con la misma garantía. Además, mejorar
   `7/8 + ε` es NP-duro (Håstad, 1997): el algoritmo trivial es óptimo en el peor caso.
5. **Umbral del recubrimiento de conjuntos.** No existe un algoritmo
   `(1 − o(1)) · ln n`-aproximado salvo que P = NP (Feige, 1998). El `ln n` del algoritmo voraz
   no es una debilidad de ese algoritmo: es lo mejor que se puede hacer.

## Ejemplo

**Recubrimiento de conjuntos.** Universo `U = {1, 2, 3, 4, 5, 6}` y tres conjuntos:
`A = {1, 2, 3, 4}`, `B = {1, 2, 5}`, `C = {3, 4, 6}`.

- Voraz: `A` cubre 4 elementos nuevos (el máximo), quedan `{5, 6}`. Después `B` cubre 1 nuevo
  (`5`) y `C` cubre 1 nuevo (`6`, porque el 3 y el 4 ya están). Da igual cuál se elija: hacen
  falta **3 conjuntos**.
- Óptimo: `B ∪ C = {1, 2, 3, 4, 5, 6}`, es decir **2 conjuntos**.

El cociente es `3 / 2 = 1,5`, muy por debajo de la garantía `H₆ = 1 + 1/2 + 1/3 + 1/4 + 1/5 +
1/6 = 2,45`. Con `n = 6`, el logaritmo natural es 1,79 y la garantía del voraz es 2,45; la
diferencia entre ambos crece despacio con `n`.

**Recubrimiento de vértices.** Grafo con aristas `(1,2)`, `(1,3)`, `(2,4)`, `(5,6)`, `(6,7)`. Un
emparejamiento maximal es `{(1,2), (5,6)}`: las aristas `(1,3)`, `(2,4)` y `(6,7)` ya tocan
vértices elegidos. El recubrimiento resultante es `{1, 2, 5, 6}`, con 4 vértices. La cota
inferior es `|M| = 2`, así que el óptimo está entre 2 y 4. Aquí el factor 2 se alcanza
exactamente: `4 = 2 · 2`.

**Cobertura máxima.** Universo `{1, …, 6}`, conjuntos `A = {1,2,3}`, `B = {1,4,5}` y
`C = {2,3,6}`, y hay que elegir `k = 2`. El voraz coge `A` (3 elementos) y luego `B` (2 nuevos,
frente a 1 de `C`), cubriendo 5. El óptimo es `B ∪ C = {1, 2, 3, 4, 5, 6}`, que cubre 6. El
cociente es `5/6 ≈ 0,833`, por encima de la garantía `1 − 1/e ≈ 0,632`. La cobertura máxima es
submodular y monótona, y para ese tipo de funciones el voraz siempre logra al menos `1 − 1/e`
del óptimo.

## Código

```python verificable
# Recubrimiento de conjuntos voraz: cada paso, el conjunto con mas elementos nuevos.
universo = set(range(1, 7))
conjuntos = {"A": {1, 2, 3, 4}, "B": {1, 2, 5}, "C": {3, 4, 6}}


def voraz(universo, conjuntos):
    pendiente, elegidos = set(universo), []
    while pendiente:
        mejor = max(conjuntos, key=lambda s: len(conjuntos[s] & pendiente))
        if not (conjuntos[mejor] & pendiente):
            break                      # ningun conjunto cubre lo que queda
        elegidos.append(mejor)
        pendiente -= conjuntos[mejor]
    return elegidos


eleccion = voraz(universo, conjuntos)
print("voraz:", eleccion, "->", len(eleccion), "conjuntos")   # -> 3
print("optimo: B y C -> 2 conjuntos")
print("cociente observado: {:.2f}".format(len(eleccion) / 2))  # -> 1.50
print("cota teorica H(6) = {:.2f}".format(sum(1 / i for i in range(1, 7))))  # -> 2.45
```

:::claves
- `set` no conserva el orden de inserción y `max(conjuntos, key=...)` recorre las claves en ese orden interno. Cuando dos conjuntos cubren los mismos elementos nuevos, el elegido puede cambiar de una ejecución a otra: con Python 3.7 o superior el desempate es el orden de inserción del diccionario, pero no lo uses como criterio.
- `pendiente -= conjuntos[mejor]` modifica el conjunto `pendiente` en el sitio, no devuelve uno nuevo. Si escribes `pendiente = pendiente - conjuntos[mejor]` también funciona, porque `-` crea un `set` nuevo; `-=` no.
- `set` está implementado con una tabla hash, así que `conjuntos[s] & pendiente` (la intersección) tarda lo que el conjunto más pequeño, no lo que el universo. Por eso el voraz es rápido incluso con millones de elementos.
- `max()` sobre un diccionario devuelve una **clave**, no un valor: en `max(conjuntos, key=...)` la `key` es una función que se aplica a cada clave y cuyo resultado se compara. Sin `key`, `max` compararía las cadenas `"A"`, `"B"`, `"C"` entre sí.
- `len(set().union(*[...]))` de la tercera línea del último bloque une los conjuntos elegidos: el `*` desempaqueta la lista y `union` acepta varios argumentos a la vez. Con una lista vacía `union()` no recibe nada y devuelve el conjunto vacío, sin error.
- `itertools.combinations(conjuntos, k)` elige combinaciones **sin repetir** y en el orden del iterable: para 3 conjuntos y `k = 2` produce `AB`, `AC` y `BC`, no `AA` ni `BA`. El número de combinaciones crece como `C(n, k)`, y por eso la fuerza bruta solo sirve para instancias pequeñas.
:::

```python verificable
# Vertex cover 2-aproximado: emparejamiento maximal y a tomar los dos extremos.
aristas = [(1, 2), (1, 3), (2, 4), (5, 6), (6, 7)]
emparejamiento, cubiertos = [], set()
for u, v in aristas:
    if u not in cubiertos and v not in cubiertos:
        emparejamiento.append((u, v))
        cubiertos |= {u, v}

print("emparejamiento maximal:", emparejamiento)
print("vertex cover:", sorted(cubiertos), "->", len(cubiertos), "vertices")
print("cota inferior (tamano del emparejamiento):", len(emparejamiento))
# el cociente es 4 / 2 = 2, justo el factor garantizado
```

```python verificable
import itertools
import numpy as np

# Cobertura maxima: elegir k conjuntos para cubrir el maximo de elementos.
universo = {1, 2, 3, 4, 5, 6}
conjuntos = {"A": {1, 2, 3}, "B": {1, 4, 5}, "C": {2, 3, 6}}
k = 2

cubierto, elegidos = set(), []
for _ in range(k):
    mejor = max(conjuntos, key=lambda s: len(conjuntos[s] - cubierto))
    elegidos.append(mejor)
    cubierto |= conjuntos[mejor]

optimo = max(len(set().union(*[conjuntos[s] for s in combo]))
             for combo in itertools.combinations(conjuntos, k))

print("voraz:", elegidos, "cubre", len(cubierto))       # -> cubre 5
print("optimo con 2 conjuntos:", optimo)                # -> 6
print("cociente: {:.3f}".format(len(cubierto) / optimo))          # -> 0.833
print("cota 1 - 1/e: {:.3f}".format(1 - 1 / np.e))                # -> 0.632
```

## Errores típicos

- **Llamar «aproximación» a una heurística.** Un algoritmo genético, un recocido o una regla de
  tres no tienen garantía. Si no puedes escribir «`A(I) ≤ ρ · OPT(I)` para todo `I`» con una
  demostración detrás, lo que tienes es una heurística, y hay que reportarlo como tal.
- **Leer la garantía como una predicción de tu instancia.** El factor es una cota del peor caso
  sobre todas las instancias posibles. En los ejemplos de arriba, el set cover salió a 1,5
  frente al 2,45 garantizado (mejor de lo prometido) y el vertex cover salió a 2,0 clavado (el
  peor caso permitido). Nunca uses `ρ` para afirmar cuánto se ha desviado la solución que tienes
  delante.
- **Confundir emparejamiento maximal con máximo.** El algoritmo voraz produce un emparejamiento
  **maximal** (no se le puede añadir otra arista) en tiempo lineal. El **máximo** es más grande y
  más caro de calcular. La demostración del factor 2 funciona con el maximal, y usar el máximo no
  mejora la garantía; lo que rompe el razonamiento es creer que son lo mismo.
- **Aplicar la garantía del viajante métrico a un problema no métrico.** El factor 2 y el 3/2
  dependen de la desigualdad triangular. Sin ella, el problema del viajante **no admite ninguna
  aproximación con factor constante** salvo que P = NP: basta con codificar un problema NP-duro
  en las distancias.
- **Reportar el mejor resultado de tu heurística como si fuera el óptimo.** Si usas el voraz para
  establecer la referencia y luego mides tu método contra el voraz, el cociente «1,0» solo dice
  que has empatado con el voraz. El óptimo hay que calcularlo aparte (fuerza bruta en instancias
  pequeñas, o un solver exacto con límite de tiempo) y hay que decir cuál de las dos cosas es.
- **Redondear la solución de una relajación lineal sin comprobar la factibilidad.** La vía de la
  relajación más redondeo es una técnica legítima, pero el redondeo hay que diseñarlo para que la
  solución siga siendo factible; si no, el resultado no es una aproximación, es una solución
  inválida con un cociente bonito.

:::nota
La garantía se define sobre el cociente, no sobre el error absoluto: un algoritmo 1,01-aproximado
para un problema cuyo óptimo vale un millón puede equivocarse en 10.000 unidades, y un algoritmo
2-aproximado para un óptimo de 10 se equivoca como mucho en 10. Al elegir un algoritmo de
aproximación, mira las dos cosas.
:::

:::practica
enunciado: Grafo con las aristas (1,2), (2,3), (3,4), (4,5) y (5,1), en ese orden. Ejecuta el algoritmo 2-aproximado del recubrimiento de vértices, da el recubrimiento obtenido, calcula el óptimo a mano y compara el cociente con la garantía.
pista: El emparejamiento maximal se construye recorriendo las aristas y tomando la primera que no toque ningún vértice ya cubierto; el recubrimiento son los dos extremos de cada arista elegida.
solucion: Entra (1,2) y cubre {1, 2}; (2,3) toca el 2 y se salta; entra (3,4) y cubre {1, 2, 3, 4}; (4,5) y (5,1) se saltan. Recubrimiento: 4 vértices, con un emparejamiento de 2 aristas. El óptimo es 3, con {1, 3, 5}. Cociente 4/3 ≈ 1,33, por debajo del 2 garantizado.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es la diferencia esencial entre una heurística y un algoritmo de aproximación?
o: El de aproximación es más rápido y la heurística más precisa
o: El de aproximación tiene demostrado un factor ρ que acota el cociente con el óptimo para toda instancia; la heurística no tiene esa garantía
o: La heurística solo se aplica a problemas de maximización
a: 2
e: Ambos renuncian al óptimo, pero solo el segundo viene con una demostración de que nunca se aleja más de ρ veces del óptimo. Una heurística puede funcionar mejor en la práctica y no dar ninguna garantía, y eso cambia por completo cómo se puede usar el resultado en una decisión.
:::

:::quiz
p: En el recubrimiento de vértices con emparejamiento maximal, ¿por qué la solución tiene como mucho el doble de vértices que el óptimo?
o: Porque el emparejamiento maximal siempre tiene la mitad de aristas que vértices tiene el grafo
o: Porque la solución toma 2 vértices por cada arista del emparejamiento y cualquier recubrimiento necesita al menos 1 por arista, y esas aristas no comparten vértices
o: Porque el grafo es bipartito y en los bipartitos el recubrimiento mínimo se calcula en tiempo polinómico
a: 2
e: Las aristas del emparejamiento son disjuntas, así que cualquier recubrimiento debe incluir al menos un extremo distinto de cada una: OPT es al menos el tamaño del emparejamiento. La solución construida usa exactamente dos extremos por arista, de ahí el factor 2. La tercera opción es cierta para grafos bipartitos, pero no es la razón de la garantía.
:::

:::aviso
Que un problema sea NP-duro no significa que haya que renunciar a resolverlo exactamente. Los
solvers de programación entera resuelven a diario instancias industriales enormes: la teoría
habla del peor caso y la práctica encuentra estructura. Antes de conformarte con una
aproximación, mide cuánto tarda un solver exacto en tus datos reales. La aproximación es el plan
B, no el plan A.
:::
