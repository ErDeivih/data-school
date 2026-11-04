---
id: algoritmos-greedy
titulo: Algoritmos voraces
fase: 10
nivel: intermedio
rutas: [alg, core]
prerequisitos: [ordenacion, complejidad-asintotica, programacion-dinamica]
tags: [algoritmos, optimizacion, voraces, greedy]
resumen: Elegir en cada paso la opción que parece mejor es rapidísimo y a veces óptimo; la diferencia entre las dos cosas hay que demostrarla, no suponerla.
fuentes: ["Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 16", "Kleinberg y Tardos (2006), 'Algorithm Design', cap. 4"]
---

## En una frase

Un algoritmo voraz construye la solución tomando en cada paso la mejor opción disponible en ese
momento y sin dar marcha atrás nunca; cuando esa miopía resulta ser óptima, el algoritmo es
rapidísimo y sencillo, y cuando no lo es, devuelve una respuesta plausible y equivocada sin
avisar.

## La idea

Estás en una ciudad desconocida y quieres llegar a la estación. En cada cruce eliges la calle que
apunta más o menos hacia allí y sigues. Casi siempre llegas; a veces te metes en una urbanización
sin salida y tienes que volver. Ese es un algoritmo voraz: **decidir con la información local, sin
planificar el recorrido completo**. Su gran virtud es que cuesta muy poco; su gran defecto es que
no tiene forma de saber si se ha equivocado.

El caso de éxito más limpio es el de **selección de actividades**: tienes una sala de reuniones y
una lista de intervalos `[inicio, fin)` que quieren usarla. Quieres meter el mayor número posible
de reuniones sin solapar. El algoritmo voraz es: ordena por hora de fin y ve cogiendo cada reunión
que empiece cuando la anterior ha terminado. Con los once intervalos del ejemplo salen cuatro
actividades, y aquí la regla «coge lo que antes acabe» **es óptima**. Hay una demostración
sencilla: si una solución óptima empieza con otra actividad, cambiarla por la que acaba antes no
reduce el hueco disponible para el resto, así que existe una solución óptima que empieza por la
elección del algoritmo. Ese intercambio es el **argumento de intercambio**.

El caso de fracaso más instructivo es el de la **mochila 0/1**: objetos indivisibles con peso y
valor, y una mochila con capacidad máxima. La regla voraz natural es «coge primero lo que más
valor da por kilo». Con capacidad 10 y objetos de `(peso 6, valor 30)`, `(peso 5, valor 24)` y
`(peso 5, valor 24)`, las densidades son 5,0 y 4,8 por kilo, así que el voraz coge el de peso 6
—valor 30— y ya no le queda sitio para nada más. La solución óptima son los dos objetos de peso 5,
que suman peso 10 y valor 48. El voraz devuelve el 62,5 % del óptimo sin equivocarse en nada
formal: la solución es factible. Es exactamente el problema que resuelve
[[programacion-dinamica]].

¿Por qué funciona en un caso y no en el otro? Porque la selección de actividades tiene una
estructura especial: el conjunto de actividades compatibles forma lo que se llama un **matroide**,
una familia de conjuntos donde el intercambio siempre se puede hacer. La mochila 0/1 no la tiene.
La consecuencia práctica: **no se puede decidir si un voraz es correcto probándolo con ejemplos**.
Hay que demostrar la propiedad de elección voraz (existe una solución óptima que empieza por la
elección del algoritmo) o buscar un contraejemplo.

La tabla de la vida real, para tener a mano:

- **Voraz es óptimo:** selección de actividades, árbol de expansión mínima (Kruskal, Prim),
  caminos mínimos con pesos no negativos ([[caminos-minimos|Dijkstra]]), códigos de Huffman,
  compresión, planificación de tareas con plazo y beneficio.
- **Voraz no es óptimo:** mochila 0/1, cambio de monedas con denominaciones arbitrarias, viajante
  de comercio, recubrimiento de conjuntos, asignación de tareas con más de un recurso.
- **Voraz da una cota con garantía:** [[algoritmos-de-aproximacion|los algoritmos de
  aproximación]] usan voraces cuyo resultado se demuestra que no se aleja más de un factor del
  óptimo, aunque no sea el óptimo.

:::figura
fichero: voraces-intervalos-y-mochila
pie: Izquierda: los once intervalos del ejemplo ordenados por hora de inicio. En azul, lo que elige el criterio «la que antes acaba» (B, D, H y K: cuatro actividades, que es el máximo posible); en rojo, lo que elige «la que antes empieza» (A, G y K: tres). Los dos son algoritmos voraces, los dos devuelven una solución factible y ninguno avisa de que se ha equivocado: lo único que cambia es el criterio, y solo uno de los dos tiene demostración. Derecha: 3.000 mochilas 0/1 de seis objetos resueltas con el voraz por densidad y con fuerza bruta. En el 77 % de las instancias el voraz da el óptimo, pero la cola de la izquierda es real: la peor de la muestra se queda en el 59 % del óptimo y el contraejemplo de la página (30 de 48) cae en el 62,5 %. Que un voraz funcione en tus ejemplos no demuestra que sea correcto.
fuente: figuras/algoritmos-greedy-1.py
:::

## Definición formal

Un algoritmo es **voraz** (o *greedy*) si construye la solución tomando una secuencia de
decisiones `d₁, d₂, …, dₘ`, donde cada `dᵢ` se elige como la mejor opción **según un criterio
local** aplicado al estado actual, y ninguna decisión se revisa después.

Para que un voraz sea correcto hacen falta dos propiedades:

- **Propiedad de elección voraz:** existe una solución óptima que incluye la primera elección del
  algoritmo. Se demuestra con un argumento de intercambio.
- **Subestructura óptima:** tras fijar esa elección, lo que queda por resolver es el mismo
  problema sobre el estado reducido, y su solución óptima combinada con la elección da la solución
  óptima global. Es la misma propiedad que necesita la programación dinámica; la diferencia es
  que el voraz no vuelve atrás.

Con `n` elementos de entrada y un criterio que se evalúa en `O(1)`:

:::formula
Voraz:  T(n) = O(n · log₂ n)  si hay que ordenar primero,   T(n) = O(n)  si no
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `T(n)` | coste total del algoritmo voraz | operaciones | lo domina la ordenación previa, no la exploración |
| `n` | número de elementos de la entrada (intervalos, objetos, monedas) | elementos | añade un factor log₂ n si hay que ordenar por el criterio |
| `dᵢ` | decisión i-ésima que toma el algoritmo | adimensional | ninguna se revisa después: de ahí que sea tan barato |
| `m` | número de decisiones hasta completar la solución | decisiones | el voraz las toma en una sola pasada |
| `sᵢ`, `fᵢ` | inicio y fin del intervalo i | horas o minutos | el criterio óptimo elige el menor fᵢ, no el menor sᵢ |
| `O(n log n)` | cota superior del coste con ordenación | operaciones | es el precio de ordenar una vez al principio |
:::

El `n · log₂ n` viene de [[ordenacion]]: casi todos los voraces empiezan ordenando por el
criterio. Esa es la razón de que sean tan baratos: no exploran alternativas, solo ordenan y
recorren una vez.

**Dos ejemplos formales.**

*Selección de actividades.* Entrada: `n` intervalos `[sᵢ, fᵢ)`. Criterio: elegir siempre el
intervalo compatible (`sᵢ ≥ fin de la última elegida`) con **menor `fᵢ`**. Coste: `O(n log n)` por
la ordenación.

*Cambio de monedas.* Entrada: un importe y un conjunto de denominaciones. Criterio voraz: coger
siempre la moneda mayor que no supere lo que queda. Es óptimo con las denominaciones de euro
(1, 2, 5, 10, 20, 50, 100, 200) y **no** lo es con denominaciones arbitrarias: con `{1, 3, 4}` y
un importe de 6, el voraz coge 4 + 1 + 1 (tres monedas) y el óptimo es 3 + 3 (dos monedas).

## Ejemplo

**Selección de actividades.** Intervalos, ordenados por hora de fin:

| Actividad | Inicio | Fin |
| --- | --- | --- |
| A | 0 | 6 |
| B | 1 | 4 |
| C | 3 | 5 |
| D | 5 | 7 |
| E | 3 | 9 |
| F | 5 | 9 |
| G | 6 | 10 |
| H | 8 | 11 |
| I | 8 | 12 |
| J | 2 | 14 |
| K | 12 | 16 |

El voraz elige la que antes acaba: B `[1,4)`. La siguiente compatible (empieza a las 4 o
después) con menor fin es D `[5,7)`. Después H `[8,11)`. Después K `[12,16)`. Total: **4
actividades**. ¿Es lo máximo? Cualquier solución que empiece por B deja libre todo el tiempo a
partir de las 4, y el mejor uso de `[4, 16)` son tres actividades más; no caben cinco.

Cambiar el criterio cambia el resultado, y aquí se ve: ordenando por **hora de inicio** el
algoritmo coge A `[0,6)`, después G `[6,10)` (la siguiente que empieza a las 6 o después) y
después K `[12,16)`: solo **3 actividades**. El mismo problema, un criterio distinto y una
solución peor. Que un criterio funcione en un caso no autoriza a usar cualquier criterio: el
único que se demuestra óptimo en general es «la que antes acaba».

**Mochila 0/1 donde el voraz falla.** Capacidad 10, objetos: X = (peso 6, valor 30), Y = (peso 5,
valor 24), Z = (peso 5, valor 24).

- Densidades: X = 5,0 por kilo; Y = 4,8; Z = 4,8. El voraz coge X, que es el de mayor densidad, y
  le quedan 4 kilos libres: no le cabe ni Y ni Z. Resultado: valor 30.
- Óptimo: Y y Z juntos pesan 10 y valen 48. **El voraz se queda con 30 de 48, el 62,5 %.**

Y una segunda comprobación del cambio de monedas, con `{1, 3, 4}` y 6:

- Voraz: 4 (queda 2), 1 (queda 1), 1 (queda 0) → **3 monedas**.
- Óptimo: 3 + 3 → **2 monedas**.

Con las denominaciones del euro el voraz acierta: para 47 coge 20 + 20 + 5 + 2, cuatro monedas,
que es el mínimo posible. Lo que falla no es el criterio «coge la mayor», sino que ese criterio
sea suficiente; con `{1, 3, 4}` deja de serlo, y hace falta programación dinámica. En los dos
casos el voraz devuelve una respuesta **factible** —no se pasa de capacidad y las monedas suman
el importe— y por eso no salta ningún error. Simplemente no es la mejor.

## Código

```python verificable
def seleccion_actividades(intervalos):
    """Maximo numero de intervalos sin solapar. Criterio: el que antes termina."""
    ordenados = sorted(intervalos, key=lambda par: par[1])   # la clave es el fin
    elegidas, fin_ultimo = [], -1
    for inicio, fin in ordenados:
        if inicio >= fin_ultimo:                # compatible con la ultima elegida
            elegidas.append((inicio, fin))
            fin_ultimo = fin
    return elegidas

intervalos = [(0, 6), (1, 4), (3, 5), (5, 7), (3, 9), (5, 9),
              (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
elegidas = seleccion_actividades(intervalos)
print("cuantas caben:", len(elegidas))      # -> cuantas caben: 4
print("elegidas:", elegidas)                # -> elegidas: [(1, 4), (5, 7), (8, 11), (12, 16)]

# Criterio alternativo: la que antes empieza. Llega al mismo numero en este caso.
def por_inicio(intervalos):
    elegidas, fin_ultimo = [], -1
    for inicio, fin in sorted(intervalos):
        if inicio >= fin_ultimo:
            elegidas.append((inicio, fin)); fin_ultimo = fin
    return elegidas

print("por inicio:", por_inicio(intervalos))  # -> por inicio: [(0, 6), (6, 10), (12, 16)]
```

:::claves
- `seleccion_actividades` devuelve una **lista de tuplas** `(inicio, fin)`, no un número: el 4 sale de `len(elegidas)`. La lista conserva el orden de selección, que es el de la ordenación por hora de fin.
- `sorted(intervalos, key=...)` devuelve una lista nueva y deja la original intacta. Con `intervalos.sort(...)` la ordenación sería en el sitio y devolvería `None`: `elegidas = intervalos.sort(...)` dejaría `elegidas` vacío.
- `fin_ultimo` empieza en `-1` y no en `0`: con 0, la actividad A = [0, 6) quedaría descartada por la condición `inicio >= fin_ultimo` aunque no solapa con nada. Es un centinela, no una hora del día.
- La comparación es `inicio >= fin_ultimo`, con `>=`, porque los intervalos son semiabiertos `[inicio, fin)`: una reunión que empieza justo cuando acaba la anterior sí es compatible.
- `por_inicio` usa `sorted(intervalos)`, que ordena por el primer elemento de cada tupla, o sea por el inicio, y devuelve **3** actividades (A, G y K) frente a las 4 del criterio del fin. El comentario de esa línea dice que llegan al mismo número; la salida real demuestra que no, así que conviene leer siempre el resultado y no el comentario.
:::

```python verificable
def mochila_voraz(pesos, valores, capacidad):
    """Coge primero lo de mayor valor por kilo. Es la regla natural y no siempre es optima."""
    orden = sorted(range(len(pesos)), key=lambda i: valores[i] / pesos[i], reverse=True)
    elegidos, peso, valor = [], 0, 0
    for i in orden:
        if peso + pesos[i] <= capacidad:
            elegidos.append(i); peso += pesos[i]; valor += valores[i]
    return elegidos, valor

def mochila_optima(pesos, valores, capacidad):
    """Fuerza bruta: prueba las 2^n combinaciones. Solo vale para n pequeno."""
    mejor, mejor_valor = (), 0
    for mascara in range(1 << len(pesos)):
        peso = valor = 0
        for i in range(len(pesos)):
            if mascara >> i & 1:
                peso += pesos[i]; valor += valores[i]
        if peso <= capacidad and valor > mejor_valor:
            mejor, mejor_valor = mascara, valor
    return mejor, mejor_valor

pesos, valores, capacidad = [6, 5, 5], [30, 24, 24], 10
print("densidades:", [round(v / p, 2) for p, v in zip(pesos, valores)])  # -> densidades: [5.0, 4.8, 4.8]
print("voraz:  ", mochila_voraz(pesos, valores, capacidad))    # -> voraz:   ([0], 30)
print("optimo: ", mochila_optima(pesos, valores, capacidad))   # -> optimo:  (6, 48)
print("el voraz pierde:", 48 - 30, "de 48")                    # -> el voraz pierde: 18 de 48
```

```python verificable
def cambio_voraz(monedas, importe):
    """Coge siempre la moneda mayor que quepa. Con euros acierta; con {1,3,4} no."""
    usadas, resto = [], importe
    for m in sorted(monedas, reverse=True):
        while resto >= m:
            usadas.append(m); resto -= m
    return usadas, ([] if resto else usadas)

def cambio_optimo(monedas, importe):
    """Programacion dinamica: F(c) = 1 + min(F(c - m)) sobre las monedas que caben."""
    infinito = float("inf")
    F = [0] + [infinito] * importe
    for c in range(1, importe + 1):
        for m in monedas:
            if m <= c and F[c - m] + 1 < F[c]:
                F[c] = F[c - m] + 1
    return F[importe]

for monedas, importe in (([1, 2, 5, 10, 20], 47), ([1, 3, 4], 6)):
    usadas, _ = cambio_voraz(monedas, importe)
    print(monedas, importe, "-> voraz", len(usadas), "monedas", usadas,
          "optimo", cambio_optimo(monedas, importe))
# -> [1, 2, 5, 10, 20] 47 -> voraz 4 monedas [20, 20, 5, 2] optimo 4
# -> [1, 3, 4] 6 -> voraz 3 monedas [4, 1, 1] optimo 2
```

## Errores típicos

- **Dar por bueno un voraz porque funciona en tus ejemplos.** Es el error central del tema. Un
  voraz incorrecto acierta en casi todas las instancias pequeñas y falla justo en la que te
  importa. Hay que demostrar la propiedad de elección voraz o, si no, buscar un contraejemplo con
  fuerza bruta sobre casos pequeños antes de confiar en él.
- **Confundir «ordenar por lo que parece mejor» con la regla correcta.** En la selección de
  actividades, «la más corta» o «la que antes empieza» también dan 4 en muchos ejemplos y no son
  óptimas en general. Cambiar el criterio cambia el algoritmo, y cada criterio necesita su propia
  demostración.
- **Aplicarlo a problemas con decisiones que se afectan entre sí.** El voraz no puede volver
  atrás, así que cualquier problema donde una elección temprana condicione de forma irreversible
  el resto (mochila 0/1, asignación de recursos escasos, rutas con capacidad) es candidato a
  fallar. Si la decisión de ahora limita la de después, piensa en
  [[programacion-dinamica|programación dinámica]].
- **Usarlo en un problema NP-duro sin comprobar la garantía.** Que un problema sea NP-duro no
  prohíbe usar un voraz, pero entonces hay que saber cuánto se aleja del óptimo. Un voraz sin
  garantía en un problema NP-duro es una heurística: puede dar el 99 % del óptimo o el 30 % según
  la instancia. Para eso están [[algoritmos-de-aproximacion|las garantías de aproximación]].
- **Olvidar el coste de ordenar.** Casi todos los voraces son `O(n log n)` por la ordenación
  previa, y si el criterio cambia hay que volver a ordenar. En un bucle que recalcula el criterio
  en cada paso, el coste puede pasar de `n log n` a `n² log n` sin que se note en las pruebas
  pequeñas.
- **Ignorar los empates.** Con densidades o prioridades iguales, el resultado depende del
  desempate, que casi siempre queda sin especificar y depende del orden de entrada. Si el empate
  importa (y en producción importa), fija el desempate con un criterio explícito y documentado.

:::aviso
Un voraz con garantía en un problema NP-duro no es «el algoritmo correcto»: es un algoritmo
demostrablemente dentro de un factor del óptimo. Si necesitas el óptimo exacto, el voraz no te
sirve por muy buena que sea su cota, y hay que ir a [[programacion-dinamica]] o a un solver.
:::

:::practica
enunciado: Tienes cuatro intervalos: A = [0, 10), B = [1, 2), C = [2, 3) y D = [3, 4). Aplica el criterio voraz «el que antes termina» y cuenta cuántos elige. Después prueba con «el que antes empieza» y compara los dos resultados.
pista: Ordena por hora de fin y coge cada intervalo cuyo inicio sea mayor o igual que el fin del último elegido. Con el criterio contrario, el primero que entra es el intervalo más largo.
solucion: Por hora de fin el orden es B, C, D, A: entran B (fin 2), C (inicio 2 ≥ 2) y D (inicio 3 ≥ 3); A no cabe (inicio 0 < 4). Elige 3. Por hora de inicio entra A, que termina a las 10 y bloquea el resto: elige 1. El máximo es 3, así que el criterio correcto triplica al incorrecto.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué criterio es óptimo para maximizar el número de intervalos sin solapar?
o: Elegir siempre el intervalo que antes termina
o: Elegir siempre el intervalo más corto
o: Elegir siempre el intervalo que antes empieza
a: 1
e: Ordenar por hora de fin y coger todo lo compatible maximiza el número de intervalos, y se demuestra con un argumento de intercambio: si una solución óptima usa otro intervalo, sustituirlo por el que antes acaba deja al menos tanto hueco libre. El más corto y el que antes empieza fallan en instancias concretas.
:::

:::quiz
p: Con capacidad 10 y objetos (peso 6, valor 30), (peso 5, valor 24), (peso 5, valor 24), ¿qué da el voraz por densidad y qué da el óptimo?
o: Los dos dan 48, porque los dos objetos pequeños juntos son mejores
o: El voraz da 30, porque coge el de peso 6 por tener mayor densidad, y el óptimo da 48, con los dos de peso 5
o: El voraz da 48 y el óptimo da 30
a: 2
e: Las densidades son 5,0, 4,8 y 4,8, así que el voraz empieza por el objeto de peso 6 y se queda con 4 kilos que no le sirven de nada: valor 30. La solución óptima son los dos objetos de peso 5, que suman peso 10 y valor 48. La mochila 0/1 no permite fraccionar objetos, y esa restricción rompe la propiedad que hace óptimo al criterio de densidad.
:::

:::quiz
p: ¿Por qué el cambio de monedas con {1, 3, 4} y un importe de 6 demuestra que el voraz no es universalmente correcto?
o: Porque el voraz no termina con esas denominaciones
o: Porque el voraz da 4 + 1 + 1 (tres monedas) y el óptimo es 3 + 3 (dos monedas)
o: Porque el importe 6 no se puede formar con esas monedas
a: 2
e: El voraz coge la moneda mayor que quepa, la 4, y luego necesita dos monedas de 1: tres en total. La solución 3 + 3 usa dos. Con las denominaciones del euro el mismo criterio sí es óptimo, lo que demuestra que la corrección depende del conjunto de monedas y hay que demostrarla para cada uno.
:::
