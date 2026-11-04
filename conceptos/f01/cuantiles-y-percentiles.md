---
id: cuantiles-y-percentiles
titulo: Cuantiles y percentiles
fase: 1
nivel: básico
rutas: [core, ds]
prerequisitos: [medidas-de-centralidad, notacion-matematica]
tags: [estadistica, descriptiva, percentiles]
resumen: El percentil 95 de latencia es el tiempo que solo superan 5 de cada 100 peticiones; los cuantiles resumen sin suponer ninguna forma concreta.
fuentes: ["Tukey (1977), 'Exploratory Data Analysis'"]
---

## En una frase

Un cuantil de orden `q` es el valor que deja una fracción `q` de los datos por debajo: el
percentil 95 de latencia es el tiempo que solo superan 5 de cada 100 peticiones, sin suponer
que los tiempos sigan ninguna distribución concreta.

## La idea

Imagina 100 peticiones ordenadas de la más rápida a la más lenta. El percentil 90 es el tiempo
de la petición que ocupa la posición 90 de esa lista. No te dice cuánto tarda la más lenta: te
dice dónde está el corte que deja al 90 % por debajo. Eso es todo lo que hace un cuantil,
colocar una marca en una posición de la lista ordenada.

La media contesta a otra pregunta: cuánto suman todos los tiempos repartidos entre todos. Si
unas pocas peticiones tardan muchísimo, la suma se la llevan ellas y la media deja de describir
a nadie ([[medidas-de-centralidad]]). Los percentiles no suman: cuentan. Por eso aguantan los
valores extremos: si la petición más lenta tarda un segundo o una hora, el percentil 50 se
mueve exactamente cero.

La contrapartida es que tiran la magnitud. El p99 te dice dónde está el corte del 1 % más
lento, pero no cuánto tardan esos. Y hay un límite que casi nadie respeta: un cuantil solo es
robusto mientras la fracción de datos raros sea menor que la cola que estás mirando. Con 100
observaciones, el p99 lo decide prácticamente el valor máximo, así que no es una medida de la
cola: es el máximo con otro nombre.

:::figura
fichero: percentiles-que-aguantan-y-que-no
pie: Arriba, la escalera acumulada de diez latencias: el p90 deja exactamente al 90 % por debajo y el p95 al 95 %, y entre los dos solo hay una petición. Abajo, los mismos percentiles calculados con la serie limpia y con la última petición en 1.000 ms: p50 y p75 no se mueven, pero el p95 y el p99 pasan de 100 a 1.000 ms. Un cuantil solo es robusto mientras la fracción de valores raros sea menor que la cola que estás mirando.
fuente: figuras/cuantiles-y-percentiles-1.py
:::

Dos propiedades lo hacen muy cómodo en la práctica. La primera: los cuantiles solo dependen del
orden, así que cualquier transformación estrictamente creciente los transforma igual. Si pasas
los tiempos de respuesta a logaritmo, el cuantil del logaritmo es el logaritmo del cuantil; la
media no tiene esa propiedad (el logaritmo de la media no es la media de los logaritmos). La
segunda: no hace falta normalidad, ni simetría, ni siquiera varianza finita. Con datos de cola
muy gruesa, donde la media es inestable, los cuantiles siguen diciendo algo.

Los cuartiles son los cuantiles 0,25, 0,50 y 0,75, y su diferencia (el rango intercuartílico) es
la medida de dispersión robusta de [[medidas-de-dispersion]].

## Definición formal

Con `n` observaciones ordenadas de menor a mayor, `x₍₁₎ ≤ x₍₂₎ ≤ … ≤ x₍ₙ₎`, y un orden `q` entre
0 y 1:

- El **cuantil** `Q(q)` es el valor que deja una fracción `q` de los datos por debajo.
- El **percentil** `p` es el cuantil de orden `q = p/100`: el percentil 95 es `Q(0,95)`.
- Los **cuartiles** son `Q(0,25)`, `Q(0,50)` y `Q(0,75)`; `Q(0,50)` es la mediana.
- El **rango intercuartílico** es `IQR = Q(0,75) − Q(0,25)`.

Con `n` pequeño esa definición todavía no fija un número: hay que elegir cómo interpolar. Las
dos convenciones que más te vas a encontrar:

- **Rango más cercano** (nearest rank): `Q(q) = x₍⌈q·n⌉₎`, el primer valor que deja al menos el
  `q·100 %` de los datos por debajo.
- **Interpolación lineal** entre estadísticos de orden, la que usa NumPy por defecto: con
  `h = (n − 1)·q` y `k = ⌊h⌋`,
  `Q(q) = x₍ₖ₊₁₎ + (h − k)·(x₍ₖ₊₂₎ − x₍ₖ₊₁₎)`.

Símbolos: `n` es el número de observaciones; `q` es el orden del cuantil, entre 0 y 1; `x₍ᵢ₎` es
el valor que ocupa la posición `i` una vez ordenados; `⌈·⌉` es el redondeo hacia arriba (techo) y
`⌊·⌋` el redondeo hacia abajo (suelo). Con las dos convenciones salen números distintos, y con
pocos datos la diferencia es grande.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `q` | El orden del cuantil, la fracción de datos que quieres dejar por debajo | número puro entre 0 y 1 | Al subir `q` el corte se mueve hacia la derecha, pero no en proporción: con pocos datos das saltos de un valor entero. Con `q` cerca de 1 dependes del máximo y el cuantil deja de ser robusto |
| `p` | El percentil: el mismo corte expresado de 0 a 100, con `q = p/100` | número puro entre 0 y 100 | `p` y `q` son el mismo parámetro con otra escala: el p95 es el cuantil 0,95. Con `p` muy alto (99, 99,9) y muestras pequeñas, el valor lo decide uno o dos datos |
| `n` | Número de observaciones ordenadas | ninguna (recuento) | No cambia el valor del cuantil, pero cambia cuánta cola puedes mirar: con `n = 10` el p95 y el p99 son el mismo dato, y solo a partir de unos cientos de observaciones un p99 significa algo |
| `x₍ᵢ₎` | El valor que ocupa la posición `i` una vez ordenados | las de la variable | Es la materia prima: el cuantil siempre sale de aquí. Si el valor más alto se dispara, todos los cuantiles por encima de la fracción que ocupa ese dato se mueven con él |
| `x₍ₖ₊₁₎`, `x₍ₖ₊₂₎` | Los dos valores ordenados que rodean la posición buscada | las de la variable | Son los que se interpolan. Cuanto más separados estén (cola larga), más depende el resultado del método que elijas |
| `h` | La posición exacta que ocupa el cuantil: `h = (n − 1) · q` | número puro, entre 0 y `n − 1` | Al subir `q`, `h` sube y el cuantil se interpola entre dos valores más altos. `h` entero significa que el cuantil cae justo sobre un dato y no hay que interpolar nada |
| `k` | La parte entera de `h`, `k = ⌊h⌋` | índice (desde 0) | Marca entre qué dos valores se interpola. Con `h = 8,55` se interpola entre el noveno y el décimo valor, no entre el octavo y el noveno |
| `⌈·⌉`, `⌊·⌋` | Redondeo hacia arriba (techo) y hacia abajo (suelo) | — | El techo es lo que usa el rango más cercano y por eso devuelve siempre un valor observado; el suelo es lo que usa la interpolación lineal. Cambiar de uno a otro cambia el número con los mismos datos |
| `IQR` | El rango intercuartílico, `Q(0,75) − Q(0,25)` | las de la variable | Al subir, los datos se reparten más: es la anchura del 50 % central, así que un solo valor extremo no lo mueve. Se usa como unidad de la valla de Tukey |
:::

:::formula
Si g es estrictamente creciente: Q(g(X), q) = g(Q(X, q))
:::

Es decir: los cuantiles son equivariantes ante transformaciones monótonas; la media no lo es.

## Ejemplo

Diez tiempos de respuesta, en milisegundos:

```text
10  20  30  40  50  60  70  80  90  100
```

Con interpolación lineal:

- `Q(0,50)`: `h = 9 · 0,5 = 4,5` → entre el quinto valor (50) y el sexto (60) → **55 ms**.
- `Q(0,90)`: `h = 9 · 0,9 = 8,1` → `90 + 0,1 · (100 − 90)` = **91 ms**.
- `Q(0,95)`: `h = 9 · 0,95 = 8,55` → `90 + 0,55 · 10` = **95,5 ms**.
- `Q(0,25) = 32,5` y `Q(0,75) = 77,5`, así que `IQR = 45 ms`.

Con la convención del rango más cercano, el percentil 95 es `x₍⌈9,5⌉₎ = x₍₁₀₎ = 100 ms`. El mismo
conjunto de datos da 95,5 o 100 según el método: cuando compares percentiles, di con qué método
los has calculado.

Ahora supón que la última petición no tardó 100 ms sino 1.000 ms. Ese único valor es el 10 % de
los datos. La media pasa de 55 a 145 ms, el p90 de 91 a 181 ms y el p95 de 95,5 a 590,5 ms. El
p50 no se mueve: sigue en 55 ms. La lección: un cuantil es inmune a los valores extremos que
caen por encima de su propia cola. Como un solo valor raro de cada diez contamina todo lo que
esté por encima del percentil 90, el p90 y el p95 dejan de ser robustos en cuanto la proporción
de valores raros iguala o supera el 10 %: el ejemplo de arriba lo consigue con un solo valor raro
de cada diez.

## Código

```python verificable
import numpy as np

latencia = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# NumPy interpola entre los dos valores ordenados que rodean la posicion buscada
print("p50        ", np.percentile(latencia, 50))                        # -> 55.0
print("p90        ", np.percentile(latencia, 90))                        # -> 91.0
print("p95        ", round(float(np.percentile(latencia, 95)), 1))       # -> 95.5

# El rango mas cercano no interpola: devuelve un valor observado
print("p95 nearest", np.percentile(latencia, 95, method="nearest"))      # -> 100

# Los cuartiles son los percentiles 25 y 75; su diferencia es el IQR
q1, q3 = np.percentile(latencia, [25, 75])
print("IQR        ", q3 - q1)                                           # -> 45.0
```

:::claves
- `np.percentile(latencia, 50)` devuelve un `float` suelto, pero `np.percentile(latencia, [25, 75])` devuelve un array de dos elementos; de ahí que `q1, q3 = ...` funcione. Si pides un solo percentil con una lista de uno, te llevas un array, no un número.
- El argumento se llama `method` en NumPy 2 y `interpolation` en NumPy 1.22 y anteriores. Si copias código antiguo y no cambia nada al pasar `method="nearest"`, comprueba la versión: en la vieja el parámetro se llamaba distinto.
- Ojo con el redondeo de los `print`: `np.percentile(latencia, 95)` vale 95,5 exacto, pero sin `round(..., 1)` se imprime `95.5` y con la interpolación de otro método puede salir `95.49999999999999`. Para publicar un percentil, redondea tú.
- `np.percentile` **no** modifica `latencia` ni la ordena: trabaja sobre una copia. Puedes calcular diez percentiles seguidos y el array sigue igual.
- El `method` por defecto es `"linear"` (`h = (n − 1)·q` interpolando). No es el único que existe en el mundo: `quantile_disc` en SQL y el rango más cercano devuelven otro número con los mismos datos, y esa diferencia es la que hace que dos informes «contradictorios» sean los dos correctos.
- `q3 - q1` sale en milisegundos, como los datos, y no en «porcentaje»: el IQR es una anchura, no una fracción. Si quisieras una fracción comparable entre escalas tendrías que dividir entre la mediana, que ya es otra cosa.
:::

```python verificable
import numpy as np

# La misma serie, pero la ultima peticion tarda 1 segundo en vez de 100 ms
latencia = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 1000])
q1, q3 = np.percentile(latencia, [25, 75])

print("media", latencia.mean())                                        # -> 145.0
print("p50  ", np.percentile(latencia, 50))                            # -> 55.0
print("p90  ", round(float(np.percentile(latencia, 90)), 1))           # -> 181.0
print("p95  ", round(float(np.percentile(latencia, 95)), 1))           # -> 590.5

# La valla de Tukey marca como atipico todo lo que supere Q3 + 1,5 * IQR
print("valla", q3 + 1.5 * (q3 - q1))                                   # -> 145.0
```

```sql verificable
CREATE TABLE latencias (ms INTEGER);
INSERT INTO latencias VALUES (10),(20),(30),(40),(50),(60),(70),(80),(90),(100);

-- quantile_cont interpola entre valores; quantile_disc solo devuelve valores observados
SELECT count(*)               AS n,
       round(avg(ms), 1)      AS media,
       quantile_cont(ms, 0.5) AS p50,
       quantile_cont(ms, 0.95) AS p95,
       quantile_disc(ms, 0.95) AS p95_orden
FROM latencias;
```

## Errores típicos

- **Confundir el percentil con el porcentaje.** «El p95 es 95 ms» no significa que el 95 % de
  las peticiones tarde exactamente 95 ms: significa que el 95 % tarda 95 ms o menos, y que el 5 %
  restante tarda eso o más.
- **Comparar percentiles calculados con métodos distintos.** NumPy, el rango más cercano, Excel
  (`PERCENTIL.INC` y `PERCENTIL.EXC` son dos funciones diferentes) y `pandas` dan números
  distintos, sobre todo con pocos datos. Si publicas un p99, di cómo lo has calculado.
- **Sacar conclusiones de un p99 con pocos datos.** Con 100 observaciones el p99 lo determina el
  segundo valor más alto; con 20, es directamente el máximo. Un p99 calculado con 50 datos es una
  anécdota, no una medida de cola.
- **Promediar percentiles de varios grupos.** La media de los p95 de tres servidores no es el p95
  del conjunto, salvo que los tres tengan el mismo número de peticiones y la misma distribución.
  Para el p95 global hacen falta los datos en crudo.
- **Calcular cuantiles de variables sin orden.** Sobre categorías (color, provincia, tipo de
  incidencia) no hay percentiles posibles: hace falta la moda o una frecuencia acumulada sobre un
  orden que tenga sentido.
- **Creer que el p95 acota el peor caso.** El p95 dice dónde está el corte, no cuánto duele lo
  que queda por encima: ese 5 % puede ser diez veces peor. Para eso está el valor esperado de la
  cola, que es lo que mide [[var-y-cvar]].

:::trampa
Un «p95 de 200 ms» puede convivir con una media de 80 ms si pocas peticiones son lentísimas, y
también con una media de 190 ms si casi todas van lentas. Los cuantiles no sustituyen a la
media: la complementan. Publica siempre un par (p50 y p95) en vez de un solo número.
:::

:::practica
enunciado: Ocho latencias ordenadas, en milisegundos: 12, 18, 25, 31, 44, 58, 73 y 96. Calcula Q1, Q3 y el rango intercuartílico con interpolación lineal y decide si 96 ms es atípico según la valla de Tukey.
pista: Con n = 8 la posición es h = (n − 1) · q; interpola entre los dos valores que la rodean. La valla de Tukey es Q3 + 1,5 · IQR.
solucion: Q1: h = 7 · 0,25 = 1,75, entre 18 y 25, luego 18 + 0,75 · 7 = 23,25 ms. Q3: h = 7 · 0,75 = 5,25, entre 58 y 73, luego 58 + 0,25 · 15 = 61,75 ms. IQR = 61,75 − 23,25 = 38,5 ms. Valla = 61,75 + 1,5 · 38,5 = 119,5 ms. Conclusión: como 96 < 119,5, ningún valor es atípico y la cola no distorsiona el resumen.
:::

## Comprueba que lo sabes

:::quiz
p: Con las latencias 10, 20, 30, 40, 50, 60, 70, 80, 90 y 100 ms, ¿cuál es el p95 si interpolas linealmente?
o: 90 ms, porque es el valor que deja nueve por debajo
o: 95,5 ms, porque la posición 8,55 cae entre 90 y 100
o: 100 ms, porque el percentil 95 siempre es el valor más alto
o: 99,5 ms, porque el p95 es la media del p90 y el máximo
a: 2
e: Con n = 10, la posición es h = 9 · 0,95 = 8,55: el 55 % del camino entre 90 y 100, o sea 95,5. La opción 90 es lo que devuelve el método `lower` (y `quantile_disc` si pides el percentil 90), y 100 lo que devuelven `quantile_disc` en el 0,95 y el rango más cercano; ninguno de los dos es la interpolación lineal.
:::

:::quiz
p: Cambias la última petición de la serie (100 ms) por una que tardó 1.000 ms. ¿Qué medida se queda igual?
o: La media, porque el cambio es de un solo dato
o: El p50, porque está por debajo de la zona contaminada
o: El p95, porque los percentiles ignoran los valores extremos
o: El rango, porque solo cambia el máximo
a: 2
e: Un valor raro de cada diez contamina todos los cuantiles cuya cola sea menor o igual al 10 %: el p90 y el p95 se disparan. El p50 no, porque para calcularlo solo se usan los valores centrales. La media sí cambia (de 55 a 145) y el rango también.
:::

:::quiz
p: ¿Qué significa exactamente que el p99 de latencia de una API sea 800 ms?
o: El 99 % de las peticiones tarda exactamente 800 ms
o: El 99 % de las peticiones tarda 800 ms o menos
o: La petición más lenta ha tardado 800 ms
o: La media de las 100 peticiones más lentas es 800 ms
a: 2
e: Un cuantil es un corte: el 99 % de los datos queda por debajo de él. No dice cuánto tarda el 1 % peor (podría tardar 5 segundos), ni es el máximo, ni es un promedio de la cola: eso último sería el CVaR.
:::
