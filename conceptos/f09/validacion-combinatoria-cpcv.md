---
id: validacion-combinatoria-cpcv
titulo: Validación combinatoria (CPCV)
fase: 9
nivel: experto
rutas: [quant, ds]
prerequisitos: [purged-kfold, validacion-cruzada, ratio-de-sharpe]
tags: [validacion, backtest, lopez-de-prado, sobreajuste]
resumen: Reparte el histórico en bloques y prueba todas las combinaciones posibles: obtienes la distribución de resultados de la estrategia en vez de un único número.
fuentes: ["López de Prado (2018), 'Advances in Financial Machine Learning', cap. 12", "Bailey, Borwein, López de Prado y Zhu (2016), 'The Probability of Backtest Overfitting'"]
---

## En una frase

En vez de un solo camino de prueba, se parte el histórico en `N` bloques, se toman todas las
combinaciones de `k` bloques como conjunto de prueba y se entrena con el resto (purgando y
embargando): el resultado no es un número, es una distribución de resultados.

## La idea

Tienes una estrategia con un [[ratio-de-sharpe|Sharpe]] de 1,4 en tu backtest. ¿Es buena? La
pregunta honesta no es si 1,4 es alto, sino **cuánto de ese 1,4 depende de dónde has cortado los
datos**. Con una única partición de entrenamiento y prueba, no puedes saberlo: has hecho un
experimento y tienes un resultado. Si mueves la fecha de corte tres meses, el número cambia, y no
tienes forma de saber cuánto.

La validación combinatoria responde a eso cambiando un experimento por muchos. En lugar de
decidir «los primeros años entrenan, los últimos prueban», se divide el histórico en `N` bloques
del mismo tamaño, se eligen `k` bloques como prueba y se entrena con los otros `N − k`. Como hay
`C(N, k)` formas de elegir esos `k` bloques, se hacen todas. Cada combinación produce un camino de
prueba, y cada camino produce su propia métrica. Con `N = 6` y `k = 2` son 15 caminos; con
`N = 10` y `k = 2`, 45.

Lo que ganas es lo que faltaba: la **dispersión**. Si los 45 caminos te dan un Sharpe entre 0,2 y
2,1, sabes que tu 1,4 es frágil y depende del corte. Si te dan entre 1,2 y 1,6, la estimación es
mucho más sólida aunque el número sea el mismo. Esa información no sale de ninguna otra partición
única.

Hay una diferencia conceptual con [[validacion-temporal|walk-forward]] que conviene tener clara:
en walk-forward el entrenamiento siempre está **antes** que la prueba, porque simula lo que harías
en la realidad. En CPCV no: una combinación puede entrenar con datos posteriores al bloque de
prueba. Para estimar el rendimiento eso es una ventaja (usas toda la información en las dos
direcciones y reduces la varianza de la estimación), pero **no es una simulación de la operativa
real**. CPCV sirve para medir incertidumbre y para detectar sobreajuste; el camino que enseñarías
como «lo que habría pasado» es el de walk-forward.

:::aviso
Los caminos no son independientes entre sí: cada bloque aparece como prueba en muchas
combinaciones y como entrenamiento en todas las demás. La dispersión que observas es una
subestimación de la incertidumbre real, porque los caminos comparten datos. No calcules el error
típico de la media de caminos como si fueran `C(N, k)` experimentos independientes.
:::

## Definición formal

Sea el histórico dividido en `N` bloques consecutivos de igual tamaño y sea `k` el número de
bloques que se apartan como prueba en cada ronda:

:::formula
J = C(N, k) = N! / ( k! · (N − k)! )        prueba = k / N del total
:::

- `N` — número de bloques. Deben ser mayores que el horizonte de la etiqueta; si un bloque dura
  menos que una operación, la purga se come el bloque entero.
- `k` — bloques de prueba por ronda. `k = 2` es lo habitual: con `k = 1` el conjunto de prueba es
  muy pequeño y cada métrica es ruidosa.
- `J` — número de caminos y también de entrenamientos distintos (el complementario de cada
  combinación es único).
- `θ_j` — la métrica agregada del camino `j` (por ejemplo, el Sharpe calculado sobre la
  concatenación de los `k` bloques de prueba).

Para cada camino se aplica [[purged-kfold|purga y embargo]]: del entrenamiento se eliminan las
observaciones cuyas etiquetas solapan con los bloques de prueba y las que caen en el hueco
inmediatamente posterior.

Con los `J` valores `θ_j` se resume la distribución: media, desviación típica y percentiles. Y se
puede estimar la **probabilidad de sobreajuste del backtest** (PBO), que es la frecuencia con la
que la configuración elegida como mejor dentro del entrenamiento queda por debajo de la mediana
fuera de la muestra:

:::formula
PBO = (1 / J) · Σ_j 1{ r_j < 0,5 }
:::

- `r_j` — el rango normalizado entre 0 y 1 que ocupa, dentro de la muestra de prueba del camino
  `j`, la configuración que fue la mejor en el entrenamiento de ese camino.
- `1{·}` — indicador: vale 1 si la condición se cumple.
- Un PBO cercano a 0,5 significa que «el mejor en entrenamiento» acaba siendo mediocre en prueba,
  que es la definición operativa de haber sobreajustado el backtest.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `N` | El número de bloques consecutivos en que se parte el histórico | bloques | Cada bloque dura menos y se acerca al horizonte de la etiqueta: cuando un bloque dura menos que una operación, la purga se lo come entero |
| `k` | Los bloques que se apartan como prueba en cada ronda | bloques | `k = 2` es lo habitual; con `k = 1` el conjunto de prueba es muy pequeño y cada métrica es ruidosa, y con `k` alto la prueba ocupa media muestra y se solapa consigo misma |
| `J` | El número de caminos, `C(N, k)` | caminos | Crece muy deprisa (6 y 2 son 15; 10 y 2, 45) y con él el coste de calcularlos; estimar un PBO con 15 casos tiene un error enorme |
| `k / N` | La fracción del histórico que se prueba en cada camino | fracción | Sube con `k`; el resto entrena, menos lo que se lleve la purga |
| `θ_j` | La métrica agregada del camino `j` | la de la métrica (Sharpe, por ejemplo) | No se elige: se mide. Lo que se reporta es su distribución, no el camino que más brilla |
| `r_j` | El rango normalizado, entre 0 y 1, que ocupa la configuración ganadora del entrenamiento en la prueba de ese camino | entre 0 y 1 | Por debajo de 0,5 quiere decir que la mejor del entrenamiento quedó en la mitad floja fuera de muestra |
| `PBO` | La probabilidad de sobreajuste del backtest | entre 0 y 1 | Un valor cercano a 0,5 es la definición operativa de haber sobreajustado; con pocos caminos el propio PBO es ruidoso |
:::

:::figura
fichero: cpcv-caminos-y-dispersion
pie: Arriba, las 15 formas de repartir 6 bloques tomando 2 como prueba: no se elige una, se prueban todas. Abajo, el Sharpe de esos 15 caminos sobre una estrategia idéntica en todo el periodo: van de −0,60 a 1,47 y la serie completa da 0,49. Lo único que cambia entre caminos es qué bloques se usan para probar, así que ese recorrido de 2,07 puntos mide la fragilidad de la estimación, no la habilidad. Lo que se reporta es la distribución, nunca el mejor camino.
fuente: figuras/validacion-combinatoria-cpcv-1.py
:::

## Ejemplo

600 observaciones repartidas en `N = 6` bloques de 100, con `k = 2` y etiquetas que duran 10
barras:

- Número de caminos: `C(6, 2) = 15`. Los primeros son `(0,1)`, `(0,2)`, `(0,3)`, `(0,4)`.
- Cada camino prueba 200 de las 600 observaciones (un 33 %) y entrena con las otras 400.
- Purga: cada bloque de prueba invalida las etiquetas vecinas que solapan. En el camino `(0,1)`,
  los dos bloques son contiguos y solo se pierden 9 observaciones por el borde derecho; en el
  camino `(2,5)`, con los dos bloques separados, se pierden 36. La media es 24 observaciones
  purgadas por camino.

Ahora la parte interesante. Sobre una serie sintética de 720 retornos con una estrategia fija (la
misma en todo el periodo, con Sharpe de la serie completa igual a 0,49), los 15 caminos dan:

```
camino mas flojo     -0,60
percentil 5          -0,43
mediana               0,43
media                 0,50
percentil 95          1,45
camino mas fuerte     1,47
```

La estrategia es exactamente la misma en los 15 casos; lo único que cambia es qué bloques se usan
para probar. Y el resultado va de −0,60 a 1,47: un recorrido de 2,07 puntos de Sharpe que no tiene
nada que ver con la habilidad, solo con el reparto. Enseñar el 1,47 como «el Sharpe de la
estrategia» es elegir el camino que te gusta; enseñar el −0,60 también. Lo que se reporta es la
distribución, y con ella la pregunta «¿cuánto de esto es el corte?» deja de ser retórica.

## Código

```python verificable
import numpy as np
from itertools import combinations

n_grupos, k, por_grupo = 6, 2, 100
combos = list(combinations(range(n_grupos), k))
print(f"N={n_grupos}, k={k}: {len(combos)} caminos de prueba")     # -> 15
print(f"cada camino prueba {k * por_grupo} de {n_grupos * por_grupo} observaciones")  # -> 200

# Purga: cada bloque de prueba invalida las etiquetas vecinas que solapan con el.
largo = 10
purgadas = []
for combo in combos:
    prueba = np.zeros(n_grupos * por_grupo, dtype=bool)
    bandas = np.zeros(n_grupos * por_grupo, dtype=bool)
    for g in combo:
        prueba[g * por_grupo:(g + 1) * por_grupo] = True
        bandas[max(0, g * por_grupo - largo + 1):(g + 1) * por_grupo + largo - 1] = True
    purgadas.append(int((bandas & ~prueba).sum()))
print(f"purgadas por camino: min {min(purgadas)}  max {max(purgadas)}  "
      f"media {np.mean(purgadas):.1f}")        # -> min 9  max 36  media 24.0
```

:::claves
- `combinations(range(n_grupos), k)` da las combinaciones **sin orden y sin repetición**: `(0, 1)` y `(1, 0)` son la misma, y por eso hay 15 caminos y no 30. Es un iterador perezoso: si no se envuelve en `list(...)` solo se puede recorrer una vez y la segunda vuelta sale vacía sin dar error.
- Cada `combo` es una **tupla**, inmutable: `g in combo` pregunta si el bloque pertenece a la combinación y `combo[0] = 3` lanzaría un error. Escribir `(0, 1)` y `(1, 0)` daría dos caminos distintos si se usara `permutations` en lugar de `combinations`, y el conteo se doblaría.
- `np.zeros(..., dtype=bool)` crea las máscaras en tipo booleano y los operadores `&`, `~` y `|` se leen como Y, NO y O elemento a elemento. Con listas de Python en vez de arrays, `&` y `~` no funcionarían.
- `prueba[g * por_grupo:(g + 1) * por_grupo] = True` escribe sobre una **vista**: el corte de un array comparte memoria con el original, así que la asignación marca `prueba` de verdad. Y `max(0, g * por_grupo - largo + 1)` no es decorativo: sin él, en el primer bloque el índice sería negativo, Python contaría desde el final del array y marcaría una banda en el otro extremo sin avisar.
- `(bandas & ~prueba).sum()` cuenta las posiciones que están en la banda pero no en la prueba; hay que quitar la prueba porque `bandas` incluye los propios bloques de prueba. `purgadas` es una lista de Python, así que `np.mean(purgadas)` la convierte por dentro en un array.
- `prueba` y `bandas` se crean **dentro** del bucle: si se crearan fuera, cada combinación arrastraría las bandas de las anteriores y el número de purgadas crecería sin sentido. Es la línea que conviene mover para comprobar que se entiende el bucle.
:::

```python verificable
import numpy as np
from itertools import combinations

rng = np.random.default_rng(0)
n_grupos, k, T = 6, 2, 120
ret = rng.normal(0.0005, 0.01, size=n_grupos * T)   # una sola estrategia, sin cambios
bloques = [ret[g * T:(g + 1) * T] for g in range(n_grupos)]

def sharpe_anual(x):
    return x.mean() / x.std(ddof=1) * np.sqrt(252)

# Cada camino es la concatenacion de los k bloques de prueba de esa combinacion.
srs = np.array([sharpe_anual(np.concatenate([bloques[g] for g in c]))
                for c in combinations(range(n_grupos), k)])
print(f"serie completa: Sharpe {sharpe_anual(ret):.2f}")      # -> 0.49
print(f"caminos {srs.size}  media {srs.mean():.2f}")          # -> 0.50
print(f"minimo {srs.min():.2f}  maximo {srs.max():.2f}")      # -> -0.60 y 1.47
print(f"p5 {np.percentile(srs, 5):.2f}  p95 {np.percentile(srs, 95):.2f}")  # -> -0.43 y 1.45
```

## Errores típicos

- **Quedarte con el mejor camino.** Si haces 45 caminos y publicas el de Sharpe 2,1, has hecho
  45 experimentos y has informado del máximo: eso es
  [[data-snooping-y-multiple-testing|selección sobre ruido]], y encima con la misma muestra. El
  resultado es la distribución completa, con su mediana y sus percentiles.
- **Tratar los caminos como independientes.** Comparten bloques, así que su dispersión está
  subestimada y su media tiene menos precisión de la que sugiere `J`. Sirve para comparar dos
  estrategias hechas con el mismo esquema, no para calcular un intervalo de confianza clásico.
- **No purgar entre bloques.** Un bloque de prueba contamina a sus vecinos de entrenamiento por
  el solapamiento de etiquetas y por las ventanas de las variables. Sin purga ni embargo, la
  dispersión entre caminos se estrecha y la validación deja de valer.
- **Bloques más cortos que el horizonte de la etiqueta.** Si cada bloque dura 20 barras y las
  etiquetas duran 30, la purga se lleva todo el bloque y no queda entrenamiento. Regla práctica:
  bloques de al menos cinco o diez veces el horizonte.
- **Confundir CPCV con una simulación de la operativa.** Entrenar con datos posteriores a la
  prueba da una estimación mejor del rendimiento, pero no es lo que harías en producción. Para
  «qué habría pasado» se usa walk-forward; para «cuánto depende esto del corte», CPCV.
- **Calcular el PBO con pocas combinaciones.** Con `N = 6` y `k = 2` hay 15 caminos, y una
  frecuencia estimada sobre 15 casos tiene un error enorme. Si el PBO es la conclusión que
  persigues, necesitas `N` y `k` que generen bastantes más caminos.

:::practica
enunciado: Divides 720 observaciones en N = 8 bloques de 90 y tomas k = 3 bloques como prueba en cada ronda. Calcula cuántos caminos produce CPCV, qué fracción del histórico se prueba en cada uno y el PBO si en 21 caminos la mejor configuración del entrenamiento queda por debajo de la mediana fuera de muestra.
pista: Cada camino es una combinación sin orden de k bloques, C(8, 3); el PBO es la frecuencia de esos 21 casos sobre el total.
solucion: C(8, 3) = 8 · 7 · 6 / 6 = 56 caminos. Cada uno prueba 3/8 = 37,5 % del histórico y entrena con los 5 bloques restantes (450) menos lo que se lleve la purga. PBO = 21/56 = 0,375: en casi dos de cada cinco caminos la mejor del entrenamiento cae en la mitad floja. Su error es grande con solo 56 casos.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es la diferencia esencial entre walk-forward y la validación combinatoria?
o: En walk-forward el entrenamiento siempre es anterior a la prueba; en CPCV hay combinaciones que entrenan con datos posteriores al bloque de prueba
o: En walk-forward se usa purga y en CPCV no hace falta
o: CPCV usa menos datos que walk-forward en todos los casos
a: 1
e: Walk-forward respeta el orden temporal porque simula la operativa real: solo sabes lo que había pasado. CPCV rompe ese orden a propósito para poder estimar el rendimiento con todas las direcciones del tiempo y obtener una distribución. Las dos cosas son útiles, pero responden a preguntas distintas. La purga hace falta en las dos.
:::

:::quiz
p: Con N = 10 bloques y k = 2 bloques de prueba, ¿cuántos caminos se generan y qué fracción del histórico se prueba en cada uno?
o: 20 caminos y un 20 % del histórico
o: 45 caminos y un 20 % del histórico
o: 45 caminos y un 50 % del histórico
a: 2
e: El número de combinaciones es C(10, 2) = 45 y cada camino prueba k/N = 2/10 = 20 % de las observaciones. El otro 80 % se usa para entrenar, menos lo que se lleve la purga. Con k = 5 y N = 10 serían 252 caminos probando la mitad de los datos en cada uno.
:::

:::quiz
p: Los 15 caminos de una misma estrategia dan Sharpes entre −0,60 y 1,47. ¿Qué conclusión es correcta?
o: La estrategia no sirve, porque hay caminos negativos
o: El recorrido mide cuánto depende el resultado del reparto de bloques, así que hay que reportar la distribución y no un único camino
o: Hay que mejorar la estrategia hasta que todos los caminos sean positivos
a: 2
e: La estrategia es idéntica en los 15 caminos: lo único que cambia es qué bloques se usan para probar. Un recorrido amplio indica una estimación frágil y dependiente del corte. Exigir que todos los caminos sean positivos es otra forma de seleccionar sobre la muestra.
:::
