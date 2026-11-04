---
id: datos-agrupados-y-errores-tipicos
titulo: Datos agrupados y errores típicos
fase: 2
nivel: básico
rutas: [ds, core]
prerequisitos: [medidas-de-centralidad, medidas-de-dispersion, poblacion-y-muestra, varianza-y-desviacion]
tags: [estadistica, agrupacion, varianza, error-tipico]
resumen: Cómo calcular la media y el error típico cuando tus datos vienen ya agrupados en frecuencias, y por qué confundir grupos con observaciones infla el error por diez.
fuentes: ["Kendall y Stuart (1977), 'The Advanced Theory of Statistics, vol. 1', 4ª ed.", "NIST/SEMATECH, 'e-Handbook of Statistical Methods', sección 1.3.5.6", "Scott y Sheppard, corrección de agrupamiento descrita en Kendall y Stuart (1977)"]
---

## En una frase

Cuando los datos llegan ya contados por intervalos o por categorías, la media y la varianza se
calculan con el número real de observaciones, no con el número de grupos, porque cada observación
es la que aporta información.

## La idea

Lo normal es tener una fila por observación: 120 alumnos, 120 filas, cada una con su nota. A veces
no. A veces lo que te dan es un resumen: «en el intervalo 0–20 hay 8 alumnos, en 20–40 hay 14…».
Es la tabla de frecuencias de toda la vida, la que aparece en cualquier informe de gestión, en
los censos y en los cuadros de mando que traen los datos ya agregados.

Con esa tabla se puede calcular la media sin ningún problema: usas el punto medio de cada
intervalo, lo multiplicas por cuántas observaciones hay en él, sumas y divides entre el total de
observaciones. Eso es una media ponderada por frecuencias y da el resultado correcto siempre que
los datos estén más o menos repartidos dentro de cada intervalo.

El error típico es donde casi todo el mundo tropieza. El error típico de la media se calcula
como la desviación típica dividida entre la raíz del **número de observaciones**. Y aquí está la
trampa: cuando los datos vienen agrupados, la tentación es meter en la fórmula el número de
**filas** de la tabla, que es el número de grupos, como si cada fila fuera un dato. No lo es. En
la tabla hay cuántos alumnos hay en cada intervalo; cada alumno es una observación y aporta. El
número que va debajo de la raíz es la suma de las frecuencias, `Σf`, no el número de intervalos.

El efecto de equivocarse es enorme y va en la dirección peligrosa. Con 120 alumnos repartidos en
5 intervalos, usar 5 en lugar de 120 multiplica el error típico por `√(120/5) = √24 ≈ 4,9`. Si en
lugar de 5 intervalos hubiera 10, el factor sería `√12 ≈ 3,5`. Un error típico casi cinco veces
más grande convierte un intervalo de confianza estrecho en uno inútil, y en un contraste hace que
algo clarísimo parezca no significativo. Es un error que no salta a la vista en el resultado
porque el número sigue siendo un número; solo se detecta mirando cuántas observaciones has
declarado.

Hay un segundo detalle, más sutil. Si los datos vienen agrupados, la varianza que calculas con
los puntos medios es la varianza **entre** los intervalos, y se deja fuera la variación de las
observaciones **dentro** de cada intervalo.

La varianza total es la suma de las dos: la de
dentro más la de entre. Si los intervalos son anchos, la parte de dentro pesa, y la varianza
calculada con los puntos medios se queda corta. Con los puntos medios exactos y una tabla
completa, esa pérdida se corrige con la corrección de Sheppard, que suma el cuadrado de la
anchura del intervalo dividido entre 12. Para la media no hace falta ninguna corrección; para la
varianza, sí.

Una regla práctica para no liarse nunca: antes de calcular nada con datos agrupados, escribe en
una columna aparte la suma de las frecuencias y comprueba que coincide con el número de
observaciones que esperabas. Ese solo gesto evita el error de usar el número de filas.

## Definición formal

Sea una tabla de frecuencias con `k` intervalos o categorías. Para el intervalo `i`, `xᵢ` es su
punto medio (o el valor de la categoría) y `fᵢ` su frecuencia.

:::formula
n = Σᵢ fᵢ      x̄ = (Σᵢ fᵢ · xᵢ) / n
:::

- `k` — número de intervalos o categorías de la tabla, es decir, de filas.
- `fᵢ` — frecuencia del intervalo `i`: cuántas observaciones caen dentro. Adimensional, un
  recuento.
- `xᵢ` — marca de clase o punto medio del intervalo `i`. Unidades de la variable.
- `n = Σᵢ fᵢ` — número **total de observaciones**. Es el número que va debajo de la raíz en el
  error típico, no `k`. Unidades: observaciones.
- `x̄` — media ponderada por frecuencias. Unidades de la variable.

La varianza y el error típico, con las dos versiones que hay que distinguir:

:::formula
s² = ( Σᵢ fᵢ · (xᵢ − x̄)² ) / (n − 1)        y        EE(x̄) = s / √n
:::

- `s²` — varianza muestral **entre** intervalos, calculada con los puntos medios. Unidades: las
  de la variable al cuadrado. Divide entre `n − 1` porque estima una varianza poblacional.
- `s` — desviación típica entre intervalos, en unidades de la variable.
- `EE(x̄)` — error típico de la media. Es la desviación típica de la media si repitieras el
  muestreo. Unidades de la variable.
- `√n` — la raíz del número de observaciones. Aquí es donde se cuela el error: si pones `√k` en
  lugar de `√n`, el error típico sale multiplicado por `√(n/k)`.

Con la corrección de Sheppard, si los intervalos son de anchura constante `h`:

:::formula
s²_corregida = s²_entre + h² / 12
:::

- `h` — anchura del intervalo. Unidades de la variable.
- `h²/12` — varianza media de una observación dentro de un intervalo, si dentro se distribuye de
  forma aproximadamente uniforme. Su unidades son las de la variable al cuadrado. Con `h = 20`,
  es `400/12 = 33,3` de varianza que se recupera.

:::parametros
| Símbolo | Qué es | Unidades | Si sube |
| --- | --- | --- | --- |
| `k` | Número de intervalos o categorías de la tabla | intervalos | Añade filas a la tabla y afina la información que se conserva, pero **no** cambia el número de observaciones. Confundirlo con `n` es el error que esta página existe para evitar: el error típico se multiplica por la raíz de `n/k` |
| `fᵢ` | Frecuencia del intervalo i: cuántas observaciones caen dentro | observaciones | Sube `n` y con ello el peso de ese intervalo en la media. El efecto en el error típico va como `1/√n` sobre el total, no intervalo a intervalo |
| `xᵢ` | Punto medio (marca de clase) del intervalo i | las de la variable | Mueve la media de forma ponderada por `fᵢ`. Si los datos se concentran en un extremo del intervalo, el punto medio sesga la media: ese sesgo no se corrige con ninguna fórmula |
| `n` | Total de observaciones, `ΣÍ fᵢ` | observaciones | Es el divisor de la raíz. Cuadruplicarlo divide el error típico por 2. Es el número que hay que declarar siempre, y el que no aparece en la tabla si solo cuentas filas |
| `s²` | Varianza entre intervalos, calculada con los puntos medios | las de la variable al cuadrado | Crece con la dispersión de los puntos medios y con la anchura de los intervalos. Subestima la varianza total porque no ve la variación de dentro de cada intervalo |
| `h` | Anchura del intervalo, si todos miden lo mismo | las de la variable | Con la corrección de Sheppard suma `h²/12` a la varianza: cuanto más anchos son los intervalos, más varianza se recupera. Con intervalos de anchura variable la corrección no se aplica tal cual |
| `EE(x̄)` | Error típico de la media | las de la variable | Es lo que se usa para el intervalo de confianza y para cualquier contraste sobre la media. Depende de las dos cosas a la vez: de la dispersión (`s`) y del número de observaciones (`n`) |
:::

| Comparación | Fórmula | Con 120 alumnos en 5 intervalos |
| --- | --- | --- |
| Correcto | `EE = s / √n` con `n = Σ fᵢ` | `21,68 / √120 = 1,98` |
| Error frecuente | `EE = s / √k` con `k` = filas de la tabla | `21,68 / √5 = 9,70` |
| Factor de error | `√(n / k)` | `√24 = 4,90` veces más grande |

:::aviso
La segunda tabla es la que hay que memorizar: mismo `s`, mismo aspecto, y un error típico casi
cinco veces mayor por haber puesto `k` donde iba `n`. El intervalo de confianza del 95 % pasa de
`±3,9` a `±19,0`, y un contraste que era clarísimo deja de serlo.
:::

:::figura
fichero: agrupados-error-tipico-y-varianza-de-dentro
pie: A la izquierda, el error típico frente al número de intervalos de la tabla, con n = 120 fijo: cuanto más se trocea la tabla, más pequeño es el error que se declara por error, porque √k crece y √n no se mueve. La línea roja es el error correcto, 1,98, que no depende de cómo se trocee la tabla. A la derecha, la varianza estimada con una tabla de intervalos de anchura creciente: los puntos miden solo la dispersión de los puntos medios y la línea azul añade la variación de dentro de cada intervalo, h²/12.
fuente: figuras/datos-agrupados-y-errores-tipicos-1.py
:::

## Ejemplo

Notas de 120 alumnos agrupadas en cinco intervalos:

```text
intervalo      punto medio x_i    frecuencia f_i
 0 -  20            10                 8
20 -  40            30                14
40 -  60            50                42
60 -  80            70                38
80 - 100            90                18
                                   ------
                             n =     120
```

La media ponderada:

`x̄ = (8·10 + 14·30 + 42·50 + 38·70 + 18·90) / 120 = (80 + 420 + 2100 + 2660 + 1620) / 120
= 6880 / 120 = 57,33`.

La suma de cuadrados respecto a esa media y la varianza entre intervalos:

```text
Σ fᵢ·(xᵢ − x̄)² = 8·2240,11 + 14·747,11 + 42·53,78 + 38·160,44 + 18·1067,11
               = 17920,9 + 10459,6 + 2258,7 + 6096,9 + 19208,0 = 55944,1
s² = 55944,1 / 119 = 470,1            s = 21,68
```

Y las dos versiones del error típico, que es lo que hay que retener:

```text
EE correcto   = 21,68 / √120 = 1,98        (n = 120 observaciones)
EE con k = 5  = 21,68 / √5   = 9,70        (5 filas de la tabla)
factor        = √(120 / 5)    = 4,90
Sheppard      = 470,1 + 400/12 = 470,1 + 33,3 = 503,5   ->  s = 22,44  ->  EE = 2,05
```

Los 120 alumnos son 120 observaciones; los 5 intervalos son 5 filas de una tabla. Si en el
informe escribes `57,33 ± 19,0` estás diciendo que no tienes ni idea de la nota media cuando en
realidad la tienes bastante clavada: el intervalo del 95 % correcto es `57,33 ± 3,9`. Y fíjate en
que la corrección de Sheppard aquí solo añade un 7 % de varianza, porque los intervalos (20
puntos de ancho) son estrechos comparados con la dispersión de las notas (21,68). Con intervalos
más anchos, ese porcentaje sube.

## Código

```python verificable
import numpy as np

# Tabla de frecuencias: punto medio de cada intervalo y cuantas observaciones caen dentro.
x = np.array([10.0, 30.0, 50.0, 70.0, 90.0])       # marcas de clase
f = np.array([8, 14, 42, 38, 18])                  # frecuencias
n = f.sum()
k = f.size

media = (f * x).sum() / n
var_entre = (f * (x - media) ** 2).sum() / (n - 1)
s = np.sqrt(var_entre)

print(f"n {n}  k {k}  media {media:.2f}  s {s:.2f}  s2 {var_entre:.1f}")
# -> n 120  k 5  media 57.33  s 21.68  s2 470.1
print(f"EE correcto (raiz de n) {s / np.sqrt(n):.2f}   EE con raiz de k {s / np.sqrt(k):.2f}")
# -> EE correcto (raiz de n) 1.98   EE con raiz de k 9.70
print(f"factor del error {np.sqrt(n / k):.2f}  Sheppard suma {20.0 ** 2 / 12:.1f}")
# -> factor del error 4.90  Sheppard suma 33.3
```

:::claves
- `f.sum()` es `n`, el número de observaciones, y `f.size` es `k`, el número de intervalos. Son
  la misma variable solo si cada intervalo tiene exactamente una observación, que es justo el
  caso en el que el error no importa. Escribe `n = f.sum()` explícitamente: si dejas `len(f)`,
  obtienes `k` sin que nada proteste.
- `(f * x).sum()` es la media ponderada y `f * x` es un producto elemento a elemento, no un
  producto matricial. Funciona porque ambos son arrays 1D del mismo tamaño; si `f` llegara como
  una lista de Python, `f * x` multiplicaría la lista por un entero o daría una forma rara. Con
  pandas, esa trampa se llama `.mul` frente a `.dot`.
- El divisor es `n - 1`, no `n`: se estima la media a partir de los mismos datos y eso gasta un
  grado de libertad. Con `n = 120` la diferencia es del 0,8 % y no cambia nada; con `n = 6` sí.
  `np.var(f * x)` sin `ddof=1` daría otro número y encima no ponderaría.
- El error típico con la corrección de Sheppard usa la varianza corregida, no la de entre: hay
  que sumar `h²/12` **antes** de hacer la raíz. Encadenar `s + h**2/12` en lugar de
  `np.sqrt(s2 + h**2/12)` da una desviación típica con unidades mezcladas y un número que no
  significa nada.
- La corrección de Sheppard supone que dentro de cada intervalo los datos se reparten de forma
  aproximadamente uniforme y que todos los intervalos miden lo mismo. Con intervalos abiertos
  («más de 100») o de anchura variable, no se aplica tal cual: o se usa otro modelo para el
  interior del intervalo o se informa del sesgo.
:::

```python verificable
import numpy as np
import pandas as pd

# La misma tabla en pandas, que es como llega casi siempre: una fila por intervalo.
tabla = pd.DataFrame({"marca": [10.0, 30.0, 50.0, 70.0, 90.0], "frecuencia": [8, 14, 42, 38, 18]})
n = int(tabla["frecuencia"].sum())
media = np.average(tabla["marca"], weights=tabla["frecuencia"])
var_entre = np.average((tabla["marca"] - media) ** 2, weights=tabla["frecuencia"]) * n / (n - 1)

print(f"media {media:.2f}  varianza {var_entre:.1f}  error tipico {np.sqrt(var_entre / n):.2f}")
# -> media 57.33  varianza 470.1  error tipico 1.98
print(f"el error tipico equivocado seria {np.sqrt(var_entre / len(tabla)):.2f} con {len(tabla)} filas")
# -> el error tipico equivocado seria 9.70 con 5 filas
print(f"filas {len(tabla)}  observaciones {n}")
# -> filas 5  observaciones 120
```

Fíjate en el factor `n / (n - 1)`: `np.average(..., weights=...)` divide entre la suma de pesos,
que es la versión de `ddof = 0`, y hay que corregirla a mano para estimar la varianza poblacional.
En pandas no hay un `.var(ddof=1)` ponderado; o se hace así o se usan `statsmodels` o
`wquantiles`.

## Errores típicos

- **Dividir entre la raíz del número de filas.** Es el error central de esta página. El error
  típico es `s / √n` con `n = Σ fᵢ`, siempre. Si solo tienes la tabla, suma la columna de
  frecuencias antes de tocar la calculadora y anota ese número al lado del resultado.
- **Calcular el error típico de la media a partir de las medias de grupo.** Si tienes la media de
  cada grupo por separado y quieres la media general, la fórmula correcta es la media ponderada
  por el tamaño de cada grupo. La media de las medias sin ponderar solo coincide si todos los
  grupos tienen el mismo tamaño, y con grupos muy desiguales puede dar un resultado muy alejado.
- **Olvidar que la varianza de los puntos medios subestima.** La varianza entre intervalos no ve
  lo que pasa dentro. Con intervalos de 20 puntos de ancho la corrección de Sheppard añade
  `h²/12 = 33,3` de varianza, que sobre 470,1 es un 7 %; con intervalos de 300 puntos, los 7.500
  que añade son un 9 % sobre 81.350. Cuanto más anchos son los intervalos respecto a la
  dispersión de los datos, más pesa lo que la tabla se deja fuera.
- **Informar la media de datos agrupados con más decimales de los que permite la tabla.** Si el
  intervalo es de 20 puntos de ancho, el punto medio se separa de cada observación como mucho ±10,
  con desviación típica `h/√12 = 20/3,46 ≈ 5,8`; la media de 120 observaciones arrastra por eso un
  error típico de unos `5,8/√120 ≈ 0,53`. Y si el reparto dentro del intervalo no es simétrico, ese
  error deja de compensarse de una observación a otra y se convierte en un sesgo que no baja al
  aumentar `n` y que puede llegar a `±h/2 = ±10`. Dar «57,33» con dos decimales es fingir una
  precisión que la tabla no tiene.
- **Tratar intervalos abiertos («más de 100») con un punto medio inventado.** El punto medio de
  «más de 100» no existe. Hay que decidirlo con información externa, modelar la cola o informar
  de que la media es una cota. Si el 30 % de las observaciones está en el intervalo abierto, la
  media que calcules es una fantasía.
- **Comparar dos tablas agrupadas con distinto número de intervalos.** Un error típico calculado
  con 5 intervalos y otro con 20 no son comparables si en algún paso se ha usado `k` en lugar de
  `n`. Antes de comparar, asegúrate de que los dos usan el mismo criterio y de que las dos `n`
  están declaradas.

:::practica
enunciado: Una encuesta mide el gasto mensual de 200 hogares y llega ya agrupada: menos de 300 euros, 45 hogares; de 300 a 600, 80; de 600 a 900, 50; de 900 a 1200, 25. Calcula la media, la desviación típica entre intervalos y el error típico correcto de la media. Después decide si el intervalo abierto del primer grupo cambia algo.
pista: Usa 150, 450, 750 y 1050 como marcas de clase, ten en cuenta que son 200 hogares y no 4 filas, y aplica la corrección de Sheppard con h = 300.
solucion: n = 200 (45 + 80 + 50 + 25). Media = (45·150 + 80·450 + 50·750 + 25·1050) / 200 = (6750 + 36000 + 37500 + 26250) / 200 = 106500 / 200 = 532,5 euros. Suma de cuadrados = 45·(150−532,5)² + 80·(450−532,5)² + 50·(750−532,5)² + 25·(1050−532,5)² = 6.583.781 + 544.500 + 2.365.313 + 6.695.156 = 16.188.750; s² = 16.188.750 / 199 = 81.350,5 y s = 285,2 euros. Error típico correcto = 285,2 / √200 = 20,17 euros. Con la corrección de Sheppard (h = 300): s² = 81.350,5 + 90000/12 = 81.350,5 + 7.500 = 88.850,5, s = 298,1 y el error típico sube a 21,08. El primer intervalo es abierto («menos de 300») y le hemos puesto marca 150: si en realidad hay hogares con gasto casi cero, la media real es más baja y el sesgo puede ser de bastantes euros; si el mínimo real son 100, la marca correcta sería 200 y bajaría la media. Con casi una cuarta parte de la muestra en ese intervalo, conviene informar del sesgo posible en lugar de dar la media con dos decimales.
:::

## Comprueba que lo sabes

:::quiz
p: Una tabla de frecuencias tiene 6 intervalos y sus frecuencias suman 300. La desviación típica entre intervalos es 12. ¿Cuál es el error típico de la media?
o: 12 / √6 = 4,90
o: 12 / √300 = 0,69
o: 12 / 300 = 0,04
a: 2
e: El error típico es la desviación típica entre la raíz del número de OBSERVACIONES, que es la suma de frecuencias, 300. Usar 6 (el número de intervalos) multiplica el error por √50 ≈ 7,1. Dividir entre n sin raíz no es el error típico de la media: eso sería otra cosa, con otras unidades.
:::

:::quiz
p: ¿Por qué la varianza calculada con los puntos medios de los intervalos suele quedarse corta?
o: Porque los puntos medios están mal elegidos
o: Porque solo mide la dispersión de los puntos medios y no ve la variación de las observaciones dentro de cada intervalo
o: Porque divide entre n en vez de entre n − 1
a: 2
e: La varianza total es la de dentro de los intervalos más la de entre los intervalos, y la fórmula de puntos medios solo captura la segunda. La corrección de Sheppard recupera la parte de dentro suponiendo que los datos se reparten de forma uniforme: suma h²/12. El divisor n − 1 es otra cosa y afecta a cualquier varianza muestral, agrupada o no.
:::

:::quiz
p: Tienes dos grupos con medias 10 y 20, con 10 y 90 observaciones. ¿Cuál es la media del conjunto?
o: 15, porque es la media de las dos medias
o: 19, porque pondera por el tamaño de cada grupo
o: No se puede saber sin los datos originales
a: 2
e: La media general es (10·10 + 20·90) / 100 = 1900 / 100 = 19. La media simple de las medias daría 15 y trata los dos grupos como si tuvieran el mismo peso, lo que con 10 frente a 90 observaciones es un error grande. Sí se puede saber sin los datos originales: basta con las medias y los tamaños de cada grupo.
:::
