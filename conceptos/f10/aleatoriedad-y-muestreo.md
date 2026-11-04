---
id: aleatoriedad-y-muestreo
titulo: Aleatoriedad y muestreo
fase: 10
nivel: intermedio
rutas: [alg, ds]
prerequisitos: [probabilidad-axiomas, variable-aleatoria, poblacion-y-muestra]
tags: [aleatoriedad, muestreo, simulacion, sesgo]
resumen: Generadores pseudoaleatorios, semillas, muestreo uniforme y ponderado, y los sesgos que convierten una muestra en una conclusión falsa.
fuentes: ["Knuth (1997), 'The Art of Computer Programming, vol. 2'", "Cochran (1977), 'Sampling Techniques'"]
---

## En una frase

Tu programa no lanza dados: usa una fórmula determinista que, a partir de una **semilla**,
produce una secuencia que *parece* aleatoria; el muestreo consiste en elegir qué elementos de
la población entran en la muestra usando esos números, y hacerlo mal es la forma más silenciosa
de sesgar un resultado.

## La idea

Imagina que quieres saber la altura media de los 40.000 habitantes de tu pueblo. No puedes
medirlos a todos, así que mides a 400. Si eliges a los 400 que pasan por delante del
ambulatorio un martes por la mañana, tu muestra estará llena de personas mayores y enfermas.
No has medido mal: has medido a otra población. Eso es el **sesgo de muestreo**, y no se
arregla con más datos, solo con otra forma de elegir.

La forma de elegir que no favorece a nadie es el **muestreo aleatorio simple**: cada habitante
tiene la misma probabilidad de salir. Y para eso necesitas números aleatorios, que es
justo lo que un ordenador no tiene.

Lo que tiene es un **generador pseudoaleatorio** (PRNG): una función determinista que, dado un
estado inicial, produce una secuencia larguísima de números que supera los tests estadísticos
habituales. Determinista significa que la misma semilla da exactamente la misma secuencia, y
eso no es un defecto: es lo que te permite repetir un experimento y obtener el mismo resultado.
La semilla forma parte del experimento, igual que los datos.

Tres ideas que se confunden todo el tiempo:

1. **Aleatorio no es uniforme.** Un PRNG devuelve números uniformes en `[0, 1)`. Si necesitas
   que el elemento *i* salga con probabilidad proporcional a un peso `wᵢ`, tienes que hacer tú
   la transformación; no sale sola.
2. **Uniforme no es representativo.** Puedes sortear perfectamente a los 400 habitantes y
   aun así olvidarte de una aldea que no está en tu lista. La uniformidad se define sobre la
   población que le das; si la lista está incompleta, el sorteo es impecable y la conclusión
   falsa.
3. **La reproducibilidad no es gratis.** `random.random()` sin semilla, `hash()` de Python o
   un `ORDER BY` sin criterio de desempate dan resultados distintos en cada ejecución y te
   dejan sin poder reproducir un hallazgo.

## Definición formal

**Generador congruencial lineal.** La familia más antigua de PRNG:

:::formula
xₙ₊₁ = (a · xₙ + c) mod m
:::

- `xₙ` — el estado actual, un entero entre 0 y `m − 1`.
- `a` — el multiplicador.
- `c` — el incremento (si `c = 0` se llama multiplicativo).
- `m` — el módulo; el estado solo puede tomar `m` valores distintos.
- `mod` — el resto de la división entera.

La secuencia de salida es determinista y **periódica**: como mucho recorre `m` valores antes de
repetirse. Se dice que tiene **periodo completo** cuando recorre los `m` sin repetir ninguno.
Los PRNG modernos (Mersenne Twister, PCG64) tienen periodos astronómicos, pero siguen siendo
deterministas: `np.random.default_rng(0)` da siempre la misma secuencia.

**Muestreo uniforme sin reemplazo.** De una población de `n` elementos se extrae una muestra de
tamaño `k < n` sin repetir ninguno. Cualquier subconjunto concreto de `k` elementos tiene
probabilidad `1 / C(n, k)`, donde `C(n, k)` es el número de subconjuntos distintos de tamaño `k`
que se pueden formar con `n` elementos. El algoritmo habitual es **Fisher-Yates**: recorrer el
array de atrás hacia delante e intercambiar cada posición con una elegida al azar entre las
anteriores, incluida ella misma.

**Muestreo ponderado.** Cada elemento `i` tiene un peso `wᵢ > 0` y su probabilidad es
`pᵢ = wᵢ / Σⱼ wⱼ`, donde `Σⱼ` significa «suma sobre todos los elementos». Con **transformada
inversa**: se calculan las sumas acumuladas `Pᵢ = p₁ + … + pᵢ`, se sortea `u` uniforme en
`[0, 1)` y se elige el primer `i` con `u < Pᵢ`.

**Estimador y error.** La media muestral `x̄ = (1/n) · Σᵢ xᵢ` es un estimador **insesgado** de
la media poblacional `μ` cuando el muestreo es uniforme sin reemplazo: su valor esperado es
`μ`. Su error típico es aproximadamente `σ / √n`, con `σ` la desviación típica de la población.
Ese `√n` es la mala noticia del oficio: para reducir el error a la mitad hay que cuadruplicar la
muestra.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `a`, `c`, `m` | Multiplicador, incremento y módulo del generador congruencial | enteros | Cambian la secuencia y su periodo; con `a = 1` el generador degenera en una cuenta y con `c = 0` (multiplicativo) el estado nunca pasa por el cero |
| `x₀` | Semilla: el estado inicial | entero entre 0 y `m − 1` | Cambia toda la secuencia, pero no su calidad: los mismos vicios, los mismos patrones, en otro orden |
| `n` | Tamaño de la muestra | elementos | El error típico baja como `σ/√n`: cuatro veces más muestra para la mitad de error |
| `k` | Tamaño de la muestra sin reemplazo del muestreo uniforme, o huecos del reservoir | elementos | Más grande, más información y menos error; nunca puede pasar de `n` |
| `wᵢ` | Peso del elemento `i` en el muestreo ponderado | positivo, sin unidades fijas | Solo importan los cocientes: multiplicar todos los pesos por 2 no cambia ninguna probabilidad |
| `σ` | Desviación típica de la población | las de la variable | Es el suelo del error: con la misma `n`, una población más dispersa da estimaciones más ruidosas |
| `pᵢ` | Probabilidad de elegir el elemento `i` | entre 0 y 1, y suman 1 | Si se elige por algo correlacionado con lo que mides, aparece el sesgo de selección, y ese no baja con `n` |
:::

:::figura
fichero: aleatoriedad-y-muestreo-error-y-sesgo
pie: A la izquierda, cuánto se equivoca la media de una muestra al crecer la muestra, en escala doble logarítmica. Los puntos azules (muestreo aleatorio simple) se pegan a la recta gris de la teoría, σ/√n; la línea verde es el mismo presupuesto repartido por estratos, y se queda sistemáticamente por debajo. A la derecha, la distribución de la media estimada con 5.000 muestras de tamaño 200 tomadas con probabilidad proporcional al valor: la línea roja es la media real de la población y la verde discontinua, la media de las estimaciones, un 169 % por encima. Esa separación no se cierra aumentando el tamaño de la muestra: más datos estrechan la campana, no la centran. Para arreglarlo hay que cambiar el procedimiento (ponderar por la probabilidad de selección, o estratificar), no el tamaño.
fuente: figuras/aleatoriedad-y-muestreo-1.py
:::

## Ejemplo

**Un congruencial lineal con periodo completo.** Con `a = 5`, `c = 3`, `m = 16` y semilla
`x₀ = 1`, la fórmula produce:

```
8  11  10  5  12  15  14  9  0  3  2  13  4  7  6  1
```

Son los 16 valores de `0` a `15`, cada uno exactamente una vez: periodo completo. La secuencia
«parece» desordenada, pero el valor 17 es otra vez 8 y todo se repite. Y ojo: los 16 valores
salidos de `mod 16` no son un buen generador de verdad, porque los bits bajos van alternando
patrones; sirven para ver el mecanismo, no para simular.

**Muestreo ponderado a mano.** Pesos `0,5`, `0,3` y `0,2` para tres anuncios. Sumas acumuladas:
`0,5`, `0,8` y `1,0`. Si el sorteo da `u = 0,62`, el primer acumulado mayor que `0,62` es
`0,8`, así que sale el segundo anuncio. Con `u = 0,05` sale el primero y con `u = 0,99` sale el
tercero.

**Comprobar el generador.** Con 10.000 sorteos ponderados salen frecuencias de `0,499`,
`0,299` y `0,202` frente a las esperadas `0,5`, `0,3` y `0,2`. Las diferencias de una o dos
milésimas son ruido de muestreo, no un fallo del generador: con 10.000 tiradas, el error típico
de una proporción del 30 % es `√(0,3 · 0,7 / 10000) ≈ 0,005`, es decir medio punto porcentual.

## Código

```python verificable
# Generador congruencial lineal: x_{n+1} = (a * x_n + c) mod m
a, c, m = 5, 3, 16
x = 1
secuencia = []
for _ in range(16):
    x = (a * x + c) % m
    secuencia.append(x)

print("secuencia:", secuencia)
print("valores distintos:", len(set(secuencia)))          # -> 16
print("el ultimo vuelve a la semilla:", secuencia[-1] == 1)  # -> True
```

:::claves
- El generador devuelve `x` **después** de actualizarlo: el primer valor de la secuencia es 8, no la semilla 1. Por eso `secuencia[-1] == 1` es verdadero y la semilla original no está en la lista hasta el final del ciclo.
- `set(secuencia)` sirve para contar valores distintos, pero **destruye el orden**. Para ver el periodo hay que mirar la lista, no el conjunto: `len(set(secuencia)) == 16` con `m = 16` indica periodo completo, y es la única comprobación que hace este bloque.
- `x = (a * x + c) % m` con enteros de Python nunca desborda. El mismo cálculo con `np.int32` daría la vuelta al llegar a 2³¹ y la secuencia quedaría rota sin ningún aviso.
- En el segundo bloque, `np.cumsum(pesos)` devuelve `[0.5, 0.8, 1.0]` y `np.searchsorted` busca el primer índice cuyo acumulado **no es menor** que el sorteo. Como el acumulado llega a 1.0, ningún `u` de `[0, 1)` se queda fuera; con pesos que no sumaran 1 habría sorteos sin destino y `searchsorted` devolvería un índice fuera del array.
- `rng.random(10_000)` genera los 10.000 sorteos de golpe, no uno a uno. Es mucho más rápido y, al venir del mismo generador con semilla, el resultado se repite exactamente igual en cada ejecución.
- `np.bincount(elegido, minlength=3)` cuenta cuántas veces sale cada índice y `minlength=3` fuerza que el array tenga tres posiciones aunque el valor 2 no hubiera salido nunca. Sin esa opción, el array tendría la longitud del mayor índice observado y la comparación con los pesos esperados se descuadraría.
:::

```python verificable
import numpy as np

# Muestreo ponderado por transformada inversa: las sumas acumuladas reparten [0, 1).
pesos = np.array([0.5, 0.3, 0.2])
acumulada = np.cumsum(pesos)                # [0.5, 0.8, 1.0]

rng = np.random.default_rng(0)              # semilla fija: el resultado se repite igual
sorteos = rng.random(10_000)
elegido = np.searchsorted(acumulada, sorteos)

print("frecuencias observadas:", np.round(np.bincount(elegido, minlength=3) / sorteos.size, 3))
print("frecuencias esperadas: ", pesos)
# la salida es, respectivamente, [0.499 0.299 0.202] y [0.5 0.3 0.2]
```

## Errores típicos

- **No fijar la semilla.** Un análisis que usa `np.random` sin semilla no se puede repetir, y
  el día que alguien lo audite obtendrá otro número. Fija la semilla en un solo sitio del
  programa y anótala junto a los resultados.
- **Reutilizar la misma semilla en procesos paralelos.** Si lanzas 8 workers con
  `default_rng(0)` cada uno, los 8 generan la misma secuencia y muestrean los mismos registros.
  Usa una semilla derivada por worker (`default_rng(semilla_base + worker)`) o
  `SeedSequence.spawn()` de NumPy.
- **Confundir `random.random()` con uniforme en un rango.** `random.random()` da `[0, 1)`;
  `random.randint(a, b)` da un entero en `[a, b]` **ambos inclusive**, y `np.random.randint(a, b)`
  da `[a, b)`. Ese intervalo abierto o cerrado es fuente de off-by-one clásico en remuestreos.
- **Sortear con `ORDER BY RANDOM()` en una tabla grande.** Es cómodo y funciona, pero obliga a
  ordenar la tabla entera: `O(n log n)` para extraer 1.000 filas. Un muestreo por
  `WHERE hash(id) % 100 < 1` es `O(n)` y además reproducible entre ejecuciones.
- **Sesgo de supervivencia.** Muestrear solo los casos que llegaron al final (fondos que
  siguen abiertos, usuarios que no se dieron de baja, máquinas que no fallaron) y sacar
  conclusiones sobre todos. Es el sesgo que más veces ha hundido una conclusión en finanzas,
  y tiene su propia página: [[sesgo-de-supervivencia]].
- **Ignorar la corrección por población finita.** Al muestrear sin reemplazo una fracción
  apreciable de una población pequeña (más del 5 %, por ejemplo), el error típico real es menor
  que `σ / √n`; el factor de corrección es `√((N − n) / (N − 1))`. Ignorarlo no te equivoca,
  pero te hace conservador: con n = 400 sobre una población de N = 1.000 el factor vale
  `√(600 / 999) = 0,775`, así que el error típico es un 22,5 % menor de lo que dice `σ / √n`, y
  estás dejando esa precisión sobre la mesa.

:::practica
enunciado: Para estimar la altura media del pueblo mides 400 habitantes y la desviación típica de la muestra es 12 cm. Calcula el error típico de la media y cuántas mediciones harían falta para dejarlo en 0,3 cm.
pista: El error típico es σ/√n y va con la raíz del tamaño: para partirlo por la mitad hay que cuadruplicar la muestra.
solucion: Con n = 400, √400 = 20, así que el error típico es 12/20 = 0,6 cm. Para bajarlo a 0,3 cm hace falta √n = 12/0,3 = 40, es decir n = 1.600 mediciones. Cuatro veces más muestra para la mitad de error; y si el marco de muestreo sigue sesgado, medir más no corrige nada.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué es útil que un generador pseudoaleatorio sea determinista?
o: Porque así los números son de verdad aleatorios y no predecibles
o: Porque la misma semilla reproduce la misma secuencia y el experimento se puede repetir
o: Porque consume menos memoria que un generador físico
a: 2
e: La utilidad práctica del determinismo es la reproducibilidad: mismo código, misma semilla, mismos resultados, y el fallo se puede depurar. Precisamente por ser determinista la secuencia es predecible si conoces el estado, que es lo contrario de la primera opción.
:::

:::quiz
p: Tienes tres anuncios con pesos 0,5, 0,3 y 0,2 y el sorteo da u = 0,62. ¿Cuál se muestra?
o: El primero, porque 0,62 es menor que la suma total 1,0
o: El segundo, porque las sumas acumuladas son 0,5, 0,8 y 1,0 y 0,62 cae entre 0,5 y 0,8
o: El tercero, porque 0,62 está en la mitad superior del intervalo
a: 2
e: Con la transformada inversa se busca el primer acumulado mayor que u. Como 0,62 supera 0,5 pero no 0,8, el elegido es el segundo, que es el que tiene asignado el tramo [0,5, 0,8) de anchura 0,3, justo su peso.
:::

:::trampa
Un muestreo aleatorio impecable sobre una lista incompleta sigue siendo un mal muestreo. Antes
de mirar el tamaño de la muestra, mira cómo se construyó el marco: si la lista excluye a un
grupo entero, ningún sorteo lo va a recuperar.
:::
