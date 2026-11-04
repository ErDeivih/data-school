---
id: anova
titulo: ANOVA
fase: 2
nivel: intermedio
rutas: [ds, core]
prerequisitos: [test-t, contraste-de-hipotesis, varianza-y-desviacion, distribuciones-continuas]
tags: [inferencia, medias, varianza, comparaciones]
resumen: Comparar las medias de tres o más grupos con un solo contraste, descomponiendo la variabilidad total en la de dentro y la de entre grupos.
fuentes: ["Fisher (1925), 'Statistical Methods for Research Workers'", "Tukey (1949), 'Comparing Individual Means in the Analysis of Variance'"]
---

## En una frase

El análisis de la varianza compara las medias de tres o más grupos preguntándose si la
variabilidad *entre* los grupos es grande comparada con la variabilidad *dentro* de cada grupo,
y así evita el problema de hacer muchas comparaciones por parejas.

## La idea

Con dos grupos, un [[test-t]] resuelve el problema. Con cuatro grupos, la tentación es hacer
todos los pares: 6 tests t. Y ahí está la trampa. Cada test tiene un 5 % de probabilidad de dar
un falso positivo cuando no hay nada. Con 6 tests, esa probabilidad ya no es del 5 %: sube por
encima del 25 %. Si pruebas 10 pares, ronda el 40 %. Estás buscando diferencias hasta
encontrarlas.

El ANOVA resuelve esto con **un único contraste** para toda la familia de grupos. La idea es
comparar dos formas de medir la variabilidad:

- **Dentro de cada grupo**: cuánto se parecen entre sí las observaciones del mismo grupo. Es el
  ruido de fondo, la variabilidad que no tiene nada que ver con el grupo al que perteneces.
- **Entre grupos**: cuánto se separan las medias de los grupos de la media general. Si los
  grupos de verdad son distintos, sus medias estarán lejos unas de otras y esta cantidad será
  grande.

El estadístico F es simplemente el cociente entre las dos, corregido por los grados de libertad
de cada una. Si el cociente es cercano a 1, las diferencias entre medias son del tamaño del
ruido y no hay nada que contar. Si es mucho mayor que 1, las medias se separan más de lo que el
ruido de dentro explica.

Dos cosas que el ANOVA **no** hace y que se le piden constantemente:

1. No dice *qué* grupo es distinto de cuál. Para eso está un contraste post-hoc (Tukey HSD es el
   más común), que sí controla la multiplicidad.
2. No dice si la diferencia es grande. F puede ser enorme con diferencias minúsculas si tienes
   muchísimos datos. El tamaño del efecto aquí es eta cuadrado (`η²`), que es la proporción de la
   variabilidad total que explica el grupo.

## Definición formal

Con `k` grupos, `nᵢ` observaciones en el grupo `i`, `N` el total y `x̄` la media general:

:::formula
F = (SS_entre / (k − 1)) / (SS_dentro / (N − k))
:::

donde las dos sumas de cuadrados son:

:::formula
SS_entre = Σᵢ nᵢ · (x̄ᵢ − x̄)² ,   SS_dentro = Σᵢ Σⱼ (xᵢⱼ − x̄ᵢ)²
:::

- `k` — número de grupos comparados.
- `N` — número total de observaciones, `Σᵢ nᵢ`.
- `x̄ᵢ` — media del grupo `i`; `x̄` — media de todas las observaciones juntas.
- `xᵢⱼ` — observación `j` del grupo `i`.
- `SS_entre` — suma de cuadrados entre grupos: cuánto se separan las medias.
- `SS_dentro` — suma de cuadrados dentro de los grupos: cuánto se dispersan las observaciones
  alrededor de la media de su propio grupo.
- `k − 1` y `N − k` — grados de libertad; `SS/(gl)` es el cuadrado medio.
- Bajo la hipótesis nula de que todas las medias son iguales, `F` sigue una distribución F de
  Fisher con `k − 1` y `N − k` grados de libertad.

El tamaño del efecto más directo es eta cuadrado:

:::formula
η² = SS_entre / (SS_entre + SS_dentro)
:::

Es la proporción de la variabilidad total que se explica por la pertenencia al grupo. Como eta
cuadrado está sesgado al alza con muestras pequeñas, existe omega cuadrado (`ω²`), que lo
corrige; para un uso descriptivo, eta cuadrado basta si dices cuántos datos tienes.

:::figura
fichero: anova-entre-dentro-y-precio-de-los-pares
pie: En el panel izquierdo, las flechas rojas miden lo que se separan las medias del centro (SS_entre = 43,3) y las líneas grises lo que se dispersa cada grupo por dentro (SS_dentro = 30,0): F = 8,67 sale de dividir 43,3/2 entre 30,0/12, es decir de comparar las dos variabilidades. En el derecho, 12.000 experimentos simulados sin ninguna diferencia real: mirar los tres pares da un falso positivo el 12,7 % de las veces, mientras que el ANOVA se queda en el 5 % que promete el umbral.
fuente: figuras/anova-1.py
:::

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `F` | Cociente entre el cuadrado medio de entre grupos y el de dentro | adimensional | Es el resultado de la formula. Cerca de 1 significa que las diferencias entre medias son del tamaño del ruido; grande, que las medias se separan mas de lo que el ruido de dentro explica. No es una diferencia de medias: es un cociente de variabilidades |
| `k` | Numero de grupos que comparas | grupos | Sube el numerador `k - 1`, que es bueno (mas señal), pero cada grupo extra añade su propio ruido y baja `N - k`, que es malo. Tambien sube la tentación de mirar los pares, que es lo que el ANOVA evita |
| `N` | Total de observaciones, `suma de n_i` | observaciones | Con las medias y las varianzas fijas, mas datos bajan `SS_dentro` en proporción y `F` sube: detecta diferencias cada vez mas pequeñas. Con `N` enorme, una diferencia irrelevante sale significativa |
| `n_i` | Observaciones de cada grupo | observaciones | Si los grupos no tienen el mismo tamaño, `SS_entre` pesa cada media por su `n_i`: un grupo con muchos datos tira mas de la media general. Con tamaños muy desiguales y varianzas distintas, la F clasica se desvia y toca la versión de Welch |
| `SS_entre` | Suma de cuadrados entre grupos: `suma n_i (media_i - media_general)^2` | las de la variable al cuadrado | Es la señal. Sube cuando las medias de grupo se alejan de la general, y su `gl` es `k - 1` |
| `SS_dentro` | Suma de cuadrados dentro de los grupos: `suma (x_ij - media_i)^2` | las de la variable al cuadrado | Es el ruido. No cambia al mover una media de grupo, solo cuando los datos se dispersan mas alrededor de la suya. Sus `gl` son `N - k` |
| `eta2` | Proporción de la variabilidad total que explica el grupo: `SS_entre / (SS_entre + SS_dentro)` | adimensional, de 0 a 1 | Es el tamaño del efecto que hay que mirar junto al p. Esta sesgado al alza con muestras pequeñas; con muchas observaciones y `eta2` de 0,01 el p puede ser minusculo e irrelevante |
| `alpha` | Riesgo de falso positivo que aceptas | probabilidad | Es el liston del p-valor, no del estadístico. Bajarlo reduce los falsos positivos y sube los falsos negativos: con el mismo `N`, detectas menos |
:::

**Supuestos:** independencia entre observaciones, normalidad dentro de cada grupo y varianzas
similares (homocedasticidad). Con varianzas muy distintas, usa el ANOVA de Welch, que no supone
igualdad de varianzas y es el equivalente del [[test-t]] de Welch. En SciPy, `f_oneway` calcula
la versión clásica.

## Ejemplo

Tres métodos de empaquetado, cinco medidas de tiempo cada uno (en segundos):

```text
metodo A:  12  14  13  15  16     media 14,0
metodo B:  10  11  12   9  13     media 11,0
metodo C:  14  16  15  13  17     media 15,0
```

Media general: (70 + 55 + 75) / 15 = 200 / 15 = **13,33**.

- `SS_entre` = 5·(14 − 13,33)² + 5·(11 − 13,33)² + 5·(15 − 13,33)²
  = 5·(0,44 + 5,44 + 2,78) = **43,33**.
- `SS_dentro`: en cada grupo las desviaciones respecto a su propia media son −2, −1, 0, 1, 2 (en
  A), −1, −2, −1, 0, 2... y sus cuadrados suman 10 en cada grupo. Total **30,00**.
- Cuadrados medios: 43,33 / 2 = 21,67 y 30,00 / 12 = 2,50.
- `F` = 21,67 / 2,50 = **8,67**, con 2 y 12 grados de libertad → **p ≈ 0,0047**.
- `η²` = 43,33 / (43,33 + 30,00) = **0,59**: el método explica el 59 % de la variabilidad.

Rechazas la igualdad de las tres medias. Y como hay tres grupos, toca post-hoc: con Tukey HSD, B
se separa de A (diferencia −3,0 s, p ajustado 0,028) y de C (−4,0 s, p ajustado 0,005), mientras
que la diferencia entre A y C (1,0 s) no es distinguible del ruido (p ajustado 0,59).

## Código

```python verificable
import numpy as np
from scipy import stats

a = np.array([12, 14, 13, 15, 16])
b = np.array([10, 11, 12,  9, 13])
c = np.array([14, 16, 15, 13, 17])
grupos = [a, b, c]
todos = np.concatenate(grupos)

gl_entre, gl_dentro = len(grupos) - 1, todos.size - len(grupos)
ss_entre = sum(g.size * (g.mean() - todos.mean())**2 for g in grupos)
ss_dentro = sum(((g - g.mean())**2).sum() for g in grupos)

print(f"SS entre {ss_entre:.2f}  SS dentro {ss_dentro:.2f}")
# -> SS entre 43.33  SS dentro 30.00
print(f"F {ss_entre / gl_entre / (ss_dentro / gl_dentro):.3f}  "
      f"p {1 - stats.f.cdf(ss_entre / gl_entre / (ss_dentro / gl_dentro), gl_entre, gl_dentro):.4f}")
# -> F 8.667  p 0.0047
print(f"eta2 {ss_entre / (ss_entre + ss_dentro):.3f}")
# -> eta2 0.591
```

:::claves
- `np.concatenate(grupos)` recibe la **lista** de arrays y devuelve un array nuevo de 15 elementos. No comprueba que los grupos tengan el mismo tamaño: con grupos de 5, 5 y 6, `todos.size` sería 16 y `gl_dentro` saldría bien igual, pero `SS_entre` con `g.size` por grupo seguiría siendo correcto. Lo que **no** funciona es `sum(grupos)`: eso suma los arrays elemento a elemento y con longitudes distintas da error.
- `g.size` es el número de elementos del array y `len(g)` también vale aquí; pero con un array de dos dimensiones `len(g)` devuelve las filas y `g.size` el total. En esta página son 1D y coinciden, en cuanto llegues a matrices dejan de coincidir.
- `g.mean()` y `todos.mean()` son `np.float64`, no `float` de Python: al imprimirlos con `:.2f` da igual, pero si los usas como clave de un diccionario o los serializas a JSON te vas a encontrar con un tipo que no esperabas.
- La F se calcula **dos veces** en la línea del `print`: una para el valor y otra dentro de `1 - stats.f.cdf(...)`. Quien empieza suele escribir `1 - stats.f.cdf(F, ...)` con la `F` de antes, que es correcto, o `stats.f.sf(F, ...)`, que es lo mismo pero sin restar de 1 y da más precisión en la cola derecha. Copia mal la línea y el p-valor sale distinto sin avisar.
- `stats.f.cdf(F, gl_entre, gl_dentro)` da la probabilidad **acumulada a la izquierda**. El p-valor de un ANOVA es la cola derecha, por eso se resta de 1. Es el error de novato más frecuente: al revés sale un p-valor casi 1 y uno se cree que «no hay nada».
- En el segundo bloque, `x = rng.normal(0, 1, (reps, 3, n))` crea un array de forma (20000, 3, 20) y `media, var = x.mean(axis=2), x.var(axis=2, ddof=1)` los reduce a (20000, 3): `axis=2` es el eje de los sujetos, que es justo el que quieres promediar. `ddof=1` divide entre `n - 1`; NumPy usa `ddof=0` por defecto, y con `n = 20` esa decisión cambia la tasa de falso positivo medida del 0,124 al 0,137. Es el mismo tipo de detalle que hace que el número de la página no cuadre si copias el bloque a medias.
:::

```python verificable
import numpy as np
from scipy import stats

# Tres grupos SIN ninguna diferencia real: cuantas veces "sale algo" haciendo 3 t-tests.
rng = np.random.default_rng(1)
reps, n = 20000, 20
x = rng.normal(0, 1, (reps, 3, n))
media, var = x.mean(axis=2), x.var(axis=2, ddof=1)

def p_valor(i, j):
    ee2 = var[:, i] / n + var[:, j] / n                     # version de Welch
    t = (media[:, i] - media[:, j]) / np.sqrt(ee2)
    gl = ee2**2 / ((var[:, i] / n)**2 / (n - 1) + (var[:, j] / n)**2 / (n - 1))
    return 2 * stats.t.sf(np.abs(t), gl)

pares = [p_valor(0, 1), p_valor(0, 2), p_valor(1, 2)]
print(f"falso positivo con 3 t-tests: {(np.minimum.reduce(pares) < 0.05).mean():.3f}")
# -> falso positivo con 3 t-tests: 0.124
print(f"cota si los tests fueran independientes: {1 - 0.95**3:.3f}")
# -> cota si los tests fueran independientes: 0.143
```

Fíjate en que la tasa observada (0,124) queda por debajo de la cota teórica del 14,3 %: esa cota
supone que los tres tests son independientes, y no lo son, porque comparten grupos. Aun así, más
que duplica el 5 % nominal.

## Errores típicos

- **Hacer t-tests por parejas en vez de ANOVA.** Con tres grupos, la tasa de falso positivo pasa
  del 5 % al 12 %; con cinco grupos, a más del 25 %. Si comparas varios grupos a la vez, usa
  ANOVA (o corrige por [[multiplicidad-y-fdr]]).
- **Interpretar una F significativa como «todos los grupos son distintos».** F solo dice que no
  todas las medias son iguales. Con tres grupos, puede haber un único grupo que se separa. Hace
  falta un post-hoc que controle la multiplicidad.
- **Mirar el p-valor y no el tamaño del efecto.** Un `η²` = 0,01 con 100.000 filas da p < 0,001 y
  no significa nada práctico. Informa de `η²` o de las diferencias de medias con su intervalo.
- **Ignorar la heterocedasticidad.** Con varianzas muy dispares y tamaños de grupo distintos, la
  F clásica se desvía. Usa el ANOVA de Welch (`statsmodels` lo tiene como `anova_oneway`).
- **Aplicar ANOVA de una vía a medidas repetidas.** Si los mismos sujetos pasan por las tres
  condiciones, las observaciones no son independientes: necesitas un ANOVA de medidas repetidas
  o un modelo mixto.
- **Ignorar la agrupación por conglomerados.** Si las observaciones vienen en grupos naturales
  (aulas, tiendas, máquinas), los errores típicos están mal calculados y el p-valor sale
  demasiado pequeño. Modelos mixtos o errores agrupados.
- **Quitar un grupo para que la F salga significativa.** Es p-hacking con otro nombre. Si el
  grupo sobraba, se decide antes de ver los datos.

:::practica
enunciado: Tres máquinas producen piezas y mides el tiempo de ciclo en cuatro lotes de cada una: A = 4, 6, 5, 5; B = 8, 9, 7, 8; C = 6, 5, 7, 6. Calcula SS_entre, SS_dentro, F y eta cuadrado, y decide si las medias difieren.
pista: La media general es 76/12 = 6,33; SS_entre pesa cada media de grupo por 4 y SS_dentro usa las desviaciones respecto a la media del propio grupo.
solucion: Medias 5, 8 y 6. SS_entre = 4·(5−6,33)² + 4·(8−6,33)² + 4·(6−6,33)² = 7,11 + 11,11 + 0,44 = 18,67. SS_dentro = 2 + 2 + 2 = 6,00. F = (18,67/2)/(6,00/9) = 9,33/0,67 = 14,0 con 2 y 9 grados de libertad, muy por encima del valor crítico 4,26: se rechaza la igualdad. η² = 18,67/24,67 = 0,76, la máquina explica el 76 % de la variabilidad.
:::

## Comprueba que lo sabes

:::quiz
p: Con cuatro grupos, ¿por qué es peor hacer las 6 comparaciones por parejas que un ANOVA?
o: Porque el ANOVA siempre da un p-valor menor
o: Porque cada comparación añade un 5 % de probabilidad de falso positivo y la tasa de al menos uno sube muy por encima del 5 %
o: Porque el test t no se puede aplicar a más de dos grupos
a: 2
e: La probabilidad de al menos un falso positivo crece con el número de comparaciones. El ANOVA hace un solo contraste global y mantiene la tasa de error en familia en el 5 %. No es que dé p-valores menores: de hecho suele dar un p mayor que la comparación por parejas más favorable, precisamente porque es honesto con la multiplicidad.
:::

:::quiz
p: Tres grupos dan SS_entre = 43,33 y SS_dentro = 30,00, con 2 y 12 grados de libertad. ¿Cuánto vale F?
o: 43,33 / 30,00 = 1,44
o: (43,33/2) / (30,00/12) = 8,67
o: (30,00/12) / (43,33/2) = 0,12
a: 2
e: F compara los cuadrados medios, no las sumas de cuadrados: hay que dividir cada suma entre sus grados de libertad antes del cociente. Ese paso es imprescindible; si no, el número de grupos y el tamaño de muestra se cuelan en el estadístico.
:::

:::quiz
p: Un ANOVA da p = 0,0047 con eta cuadrado = 0,59. ¿Qué puedes afirmar?
o: Que las tres medias no son todas iguales y que el grupo explica una parte importante de la variabilidad
o: Que los tres grupos difieren entre sí dos a dos
o: Que el grupo explica el 59 % de la probabilidad de que la hipótesis nula sea cierta
a: 1
e: La F rechaza la igualdad global y eta cuadrado cuantifica cuánta variabilidad explica el grupo. No dice nada de comparaciones dos a dos: eso requiere un post-hoc. Y eta cuadrado es una proporción de varianza explicada, no una probabilidad sobre hipótesis.
:::

:::aviso
El ANOVA clásico supone varianzas parecidas. Compruébalo antes con un test de Levene o de
Bartlett y, si sale mal, usa la versión de Welch. Es un cambio de dos líneas que evita un
p-valor equivocado.
:::
