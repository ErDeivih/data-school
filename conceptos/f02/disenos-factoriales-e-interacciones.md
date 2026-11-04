---
id: disenos-factoriales-e-interacciones
titulo: Diseños factoriales e interacciones
fase: 2
nivel: intermedio
rutas: [ds, core]
prerequisitos: [anova, test-t, contraste-de-hipotesis, errores-tipo-i-ii-y-potencia]
tags: [diseno, experimentos, interaccion, factores]
resumen: Varía varios factores a la vez para estimar cada efecto con todos los datos y para detectar la interacción, que es la mitad de la respuesta y casi siempre la pregunta.
fuentes: ["Fisher (1935), 'The Design of Experiments'", "Montgomery (2017), 'Design and Analysis of Experiments', 9ª ed.", "Box, Hunter y Hunter (2005), 'Statistics for Experimenters', 2ª ed."]
---

## En una frase

Un diseño factorial mueve todos los factores a la vez, en lugar de uno por uno, para medir cada
efecto con todos los datos y para descubrir si el efecto de un factor **depende** del otro: eso
es la interacción.

## La idea

Quieres saber si un fertilizante funciona y si el riego funciona. La forma intuitiva es probar el
fertilizante con el riego de siempre, y luego el riego con el fertilizante de siempre. Es el
método de «una variable cada vez», y tiene dos problemas que no se ven hasta que se ven.

El primero es que desaprovecha datos. Si tienes 40 parcelas, el diseño de uno en uno usa 20 para
el fertilizante y 20 para el riego. En un diseño factorial 2 × 2 con 10 parcelas en cada una de
las cuatro combinaciones, cada observación aporta información sobre el fertilizante **y** sobre
el riego, así que estimas los dos efectos con 40 datos en lugar de 20. Con la misma varianza, el
error típico de cada efecto baja.

El segundo problema es peor: el diseño de uno en uno no puede ver la interacción. Y la
interacción es, muy a menudo, la respuesta. Piensa en dos variedades de trigo y dos niveles de
abono. Puede pasar que el abono suba el rendimiento un 10 % en la variedad A y lo baje un 5 % en
la variedad B. Si solo pruebas el abono con la variedad A, concluirás «el abono funciona» y lo
recomendarás para las dos. El promedio de los dos efectos será positivo, el efecto principal
saldrá significativo y la recomendación será mala para la mitad del campo.

Una interacción, en el caso de dos factores con dos niveles, es simplemente la **diferencia de
las diferencias**. El efecto del abono en la variedad A es una diferencia entre dos medias; el
efecto del abono en la variedad B es otra; la interacción es cuánto difieren esas dos
diferencias. Si los dos efectos son iguales, la interacción es cero y se dice que los factores
son aditivos: cada uno aporta lo suyo y ya está. Si son distintos, el efecto de un factor cambia
según el nivel del otro, y entonces hablar de «el efecto del abono» sin decir en qué variedad es
una frase vacía.

Esto es lo que cambia la forma de leer el resultado. Cuando hay interacción, los efectos
principales se leen con pinzas: un efecto principal es un **promedio** de efectos que no son
iguales, y ese promedio puede ser significativo y no describir ninguna de las dos partes. La
regla es sencilla y se salta constantemente: si la interacción es relevante, se interpretan los
efectos simples dentro de cada nivel, no los efectos principales.

Dos vocabulario más, porque aparecen en todos los artículos. Un diseño es **factorial completo**
si se prueban todas las combinaciones de todos los niveles (2 factores con 2 niveles: 4 celdas;
2 factores con 3: 9 celdas). Y es un diseño **2^k**: `k` factores, cada uno con dos niveles, que
es el más frecuente en la industria porque con pocos experimentos cubre muchos factores, y
porque detecta tendencias e interacciones sin necesidad de muchos niveles por factor.

## Definición formal

Para dos factores, `A` con `a` niveles y `B` con `b` niveles, y `n` observaciones por celda, el
modelo de efectos es

:::formula
y_ijk = μ + τ_i + β_j + (τβ)_ij + ε_ijk
:::

- `y_ijk` — la observación `k` de la celda que combina el nivel `i` del factor `A` con el nivel
  `j` del factor `B`. Unidades: las de la variable respuesta (kilos, segundos, euros).
- `μ` — la media general de todas las observaciones.
- `τ_i` — efecto principal del nivel `i` del factor `A`: cuánto se separa la media de ese nivel
  de la media general. Media cero sobre los niveles.
- `β_j` — efecto principal del nivel `j` del factor `B`, igual.
- `(τβ)_ij` — **interacción**: la parte de la media de la celda que no explican `μ`, `τ_i` ni
  `β_j`. Media cero sobre cada índice.
- `ε_ijk` — error aleatorio, supuesto normal con media 0 y varianza común `σ²`, independiente
  entre observaciones.

La descomposición de la variabilidad total separa las tres señales del ruido:

:::formula
Σ (y_ijk − ȳ)² = SS_A + SS_B + SS_AB + SS_error
:::

- `SS_A` — suma de cuadrados del factor `A`: `b·n·Σᵢ (ȳ_i·· − ȳ)²`.
- `SS_B` — suma de cuadrados del factor `B`: `a·n·Σⱼ (ȳ_·j· − ȳ)²`.
- `SS_AB` — suma de cuadrados de la interacción: `n·Σᵢ Σⱼ (ȳ_ij· − ȳ_i·· − ȳ_·j· + ȳ)²`.
- `SS_error` — suma de cuadrados dentro de las celdas: lo que se dispersan las repeticiones
  alrededor de la media de su propia celda, con `a·b·(n − 1)` grados de libertad.

Cada suma se divide entre sus grados de libertad y se compara con el error, como en un
[[anova]]. El contraste de la interacción es

:::formula
F_AB = (SS_AB / ((a − 1)(b − 1))) / (SS_error / (a·b·(n − 1)))
:::

y bajo la hipótesis nula de que todas las interacciones son cero, `F_AB` sigue una distribución F
con `(a−1)(b−1)` y `a·b·(n−1)` grados de libertad.

Las medias de celda estimadas se escriben `ȳ_ij·`, y los efectos se estiman con las diferencias
correspondientes:

:::formula
interacción = (ȳ_11· − ȳ_12·) − (ȳ_21· − ȳ_22·)
:::

Con dos niveles en cada factor, esa única cantidad es la interacción: la diferencia de los dos
efectos simples.

:::parametros
| Símbolo | Qué es | Unidades | Si sube |
| --- | --- | --- | --- |
| `a`, `b` | Niveles del factor A y del factor B | niveles | Cada nivel extra añade celdas: el diseño completo pasa a `a · b` celdas y el número de observaciones necesarias se multiplica. A cambio, la interacción se estima con más grados de libertad y se pueden detectar respuestas no lineales |
| `n` | Repeticiones dentro de cada celda | observaciones | Es la palanca contra el ruido: el error típico de una media de celda baja como `1/√n`, así que para detectar una interacción la mitad de grande hace falta cuatro veces más `n` por celda. Sin repeticiones (`n = 1`) la interacción no se puede separar del error |
| `τ_i` | Efecto principal del nivel i de A | las de la respuesta | El efecto principal es un promedio de los efectos simples. Si hay interacción, subirlo en unos niveles y bajarlo en otros puede dejar el promedio casi intacto: el efecto principal deja de describir lo que pasa en ninguna celda |
| `(τβ)_ij` | Interacción de la celda (i, j) | las de la respuesta | Mide cuánto se desvía la celda de lo que predecirían los dos efectos por separado. Si es grande respecto al error, no se puede hablar del efecto de A sin decir el nivel de B |
| `SS_AB` | Suma de cuadrados de la interacción | las de la respuesta al cuadrado | Es la señal de la interacción. Sube cuando la diferencia entre niveles de A cambia al cambiar de nivel de B, es decir, cuando las rectas del gráfico de interacción se cruzan o se separan del paralelismo |
| `σ²` | Varianza del error dentro de cada celda | las de la respuesta al cuadrado | Es el ruido. Si sube, todo `F` baja y hacen falta más repeticiones. Se estima con `SS_error / (a·b·(n−1))` y es la referencia contra la que se juzgan los efectos |
| `k` | Número de factores en un diseño `2^k` | factores | El número de celdas crece como `2^k` y cada factor extra duplica el experimento. Con `k = 7` son 128 celdas: ahí se usan diseños fraccionarios, que confunden unas interacciones con otras a cambio de tamaño |
:::

:::figura
fichero: factoriales-interaccion-paralelas-y-cruzadas
pie: A la izquierda, dos factores sin interacción: subir la temperatura añade los mismos 8 puntos de rendimiento con el catalizador antiguo y con el nuevo, y las dos rectas son paralelas. A la derecha, una interacción fuerte: con el catalizador antiguo la temperatura alta mejora el rendimiento en 6 puntos, y con el nuevo lo empeora en 9. Las rectas se cruzan, y ahí el efecto principal de la temperatura es un promedio que no describe ninguna de las dos situaciones.
fuente: figuras/disenos-factoriales-e-interacciones-1.py
:::

## Ejemplo

Un experimento 2 × 2 con dos factores: temperatura (`baja`, `alta`) y catalizador (`antiguo`,
`nuevo`). Tres lotes por celda y el rendimiento en unidades:

```text
                       catalizador antiguo        catalizador nuevo
temperatura baja        52  54  50                 60  62  58
temperatura alta        58  60  56                 51  53  49
```

Medias de celda: `ȳ_baja,antiguo = 52`, `ȳ_baja,nuevo = 60`, `ȳ_alta,antiguo = 58`,
`ȳ_alta,nuevo = 51`. La media general es `(52 + 60 + 58 + 51) / 4 = 55,25`.

Efectos principales, que son las diferencias de las medias marginales:

- Temperatura: las dos celdas de temperatura baja promedian 56,0 y las dos de temperatura alta
  54,5, así que el efecto principal de subir la temperatura es **−1,5**.
- Catalizador: el antiguo promedia 55,0 y el nuevo 55,5, así que el efecto principal de cambiar
  de catalizador es **+0,5**.

Los dos efectos principales son minúsculos. Y sin embargo el experimento contiene un efecto
grandísimo, que aparece al mirar la interacción como diferencia de diferencias:

- Efecto de la temperatura con el catalizador antiguo: `58 − 52 = +6`.
- Efecto de la temperatura con el catalizador nuevo: `51 − 60 = −9`.
- Interacción: `(+6) − (−9) = +15`.

Subir la temperatura mejora 6 unidades con el catalizador antiguo y **empeora 9** con el nuevo.
El efecto principal de −1,5 sale de promediar un +6 y un −9, y no describe ninguna de las dos
situaciones: es el ejemplo de manual de por qué hay que mirar la interacción antes que los
efectos principales. Las sumas de cuadrados, con `n = 3` por celda, salen:

```text
SS_temperatura = 3 · 2 · ((56,0 − 55,25)² + (54,5 − 55,25)²) =  6,75   gl 1
SS_catalizador = 3 · 2 · ((55,0 − 55,25)² + (55,5 − 55,25)²) =  0,75   gl 1
SS_interaccion = 3 · (3,75² + 3,75² + 3,75² + 3,75²)         = 168,75   gl 1
SS_error       = 4 celdas con desviaciones ±2, 0, ±2          =  32,0   gl 8
```

`F` de la interacción: `(168,75 / 1) / (32,0 / 8) = 168,75 / 4,0 = 42,2`, con 1 y 8 grados de
libertad → **p = 0,00019**. Los efectos principales, en cambio, no llegan: `F = 1,69` para la
temperatura (p ≈ 0,23) y `F = 0,19` para el catalizador (p ≈ 0,68), ambos por debajo del valor
crítico 5,32. Si te hubieras quedado con los principales, habrías concluido que no pasa nada.

## Código

```python verificable
import numpy as np

# Las 12 observaciones del ejemplo: 4 celdas, 3 lotes cada una.
celdas = {("baja", "antiguo"): [52, 54, 50], ("baja", "nuevo"): [60, 62, 58],
          ("alta", "antiguo"): [58, 60, 56], ("alta", "nuevo"): [51, 53, 49]}
y = np.concatenate([np.array(v, dtype=float) for v in celdas.values()])
medias = {k: float(np.mean(v)) for k, v in celdas.items()}
general = y.mean()

ef_temp = np.mean([medias[("alta", "antiguo")], medias[("alta", "nuevo")]]) - \
          np.mean([medias[("baja", "antiguo")], medias[("baja", "nuevo")]])
ef_cat = np.mean([medias[("baja", "nuevo")], medias[("alta", "nuevo")]]) - \
         np.mean([medias[("baja", "antiguo")], medias[("alta", "antiguo")]])
inter = (medias[("alta", "antiguo")] - medias[("baja", "antiguo")]) - \
        (medias[("alta", "nuevo")] - medias[("baja", "nuevo")])

print(f"media general {general:.2f}  efecto temperatura {ef_temp:+.1f}  efecto catalizador {ef_cat:+.1f}")
# -> media general 55.25  efecto temperatura -1.5  efecto catalizador +0.5
print(f"interaccion (diferencia de diferencias) {inter:+.1f}")
# -> interaccion (diferencia de diferencias) +15.0
print(f"efecto de la temperatura con catalizador antiguo "
      f"{medias[('alta', 'antiguo')] - medias[('baja', 'antiguo')]:+.1f}  "
      f"con el nuevo {medias[('alta', 'nuevo')] - medias[('baja', 'nuevo')]:+.1f}")
# -> efecto de la temperatura con catalizador antiguo +6.0  con el nuevo -9.0
```

:::claves
- La interacción se calcula con **diferencias de medias de celda**, no con las marginales. Si la
  calculas restando efectos principales ya promediados, pierdes la información que buscas: el
  +15 del ejemplo no aparece en ninguna de las dos diferencias marginales.
- `medias[("alta", "antiguo")]` funciona porque la clave es una **tupla**, no una cadena. Si
  usas `medias["alta-ANTIGUO"]` como clave de texto, una errata en el nombre no da error de
  sintaxis: busca otra clave y lanza `KeyError`, o peor, devuelve `nan` si el diccionario tiene
  una clave parecida. Con tuplas el error se ve en la primera ejecución.
- `np.mean([a, b])` promedia las medias de celda **sin ponderar**, y aquí es correcto porque
  todas las celdas tienen 3 observaciones. Con celdas de tamaño distinto, ese promedio está mal:
  pesa cada media por su `n`. `np.mean` no avisa de nada.
- El signo de la interacción solo tiene sentido junto con el orden de los niveles. Aquí «+15»
  significa que el efecto de subir la temperatura es 15 unidades mayor con el catalizador
  antiguo que con el nuevo; con los niveles al revés, saldría −15. Cambiar el orden de un factor
  cambia el signo de todas las interacciones en las que participa, y no cambia los p-valores.
:::

```python verificable
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

datos = pd.DataFrame({
    "rendimiento": [52, 54, 50, 60, 62, 58, 58, 60, 56, 51, 53, 49],
    "temperatura": ["baja"] * 6 + ["alta"] * 6,
    "catalizador": ["antiguo", "antiguo", "antiguo", "nuevo", "nuevo", "nuevo"] * 2,
})
modelo = smf.ols("rendimiento ~ C(temperatura) * C(catalizador)", data=datos).fit()

# Con codificacion de tratamiento cada coeficiente es un salto respecto a la celda de referencia,
# asi que el signo depende de que nivel se tome como base. La interaccion es +15 con esta base.
print(modelo.params.round(2).to_dict())
# -> {'Intercept': 58.0, 'C(temperatura)[T.baja]': -6.0, 'C(catalizador)[T.nuevo]': -7.0,
#     'C(temperatura)[T.baja]:C(catalizador)[T.nuevo]': 15.0}

# Una ANOVA con el termino de interaccion da una fila por efecto; aqui la interaccion es la senal.
print(smf.ols("rendimiento ~ C(temperatura) * C(catalizador)", data=datos).fit().rsquared.round(3),
      len(modelo.resid), float((modelo.resid ** 2).sum()))
# -> 0.846 12 32.0
```

Fíjate en la última línea: la suma de residuos al cuadrado es 32,0, exactamente el `SS_error` que
sale de las desviaciones dentro de cada celda (±2, 0, ±2 en las cuatro celdas). Y el `R²` del
modelo es 0,846, no 0,99, y eso que la interacción es enorme: el ruido de dentro (32) pesa más
que los dos efectos principales (6,75 y 0,75) juntos. `R²` alto no es lo que hace bueno a un
diseño: lo que lo hace bueno es tener grados de libertad de error para contrastar la interacción.

## Errores típicos

- **Interpretar los efectos principales cuando hay interacción.** El caso del ejemplo es el
  patrón clásico: dos efectos principales que rozan cero y una interacción enorme. La regla:
  mira primero la fila de la interacción; si es relevante, informa de los efectos simples dentro
  de cada nivel y no vendas el promedio.
- **Cruzar «significativo» con «importante».** Con muchas repeticiones, una interacción de 0,3
  unidades sale significativa y no cambia ninguna decisión. Acompaña siempre el p-valor de la
  interacción con el tamaño del efecto en las unidades de la respuesta.
- **Diseños de una variable cada vez.** Además de gastar el doble de datos para la misma
  precisión, no pueden detectar la interacción: si los dos factores interactúan, el efecto que
  mides depende del nivel fijo que hayas elegido para el otro, y lo presentas como «el efecto».
- **Diseño factorial completo sin repeticiones.** Con `n = 1` por celda, los grados de libertad
  del error son cero si el modelo incluye la interacción: no hay forma de estimar `σ²` ni de
  contrastar nada. Se puede tirar de la interacción de orden más alto como estimador del error,
  pero es una hipótesis fuerte y hay que decirla.
- **Comparar celdas por parejas con t-tests en vez de mirar la interacción.** Con cuatro celdas
  hay seis pares, y con seis comparaciones la tasa de falso positivo se dispara: es el mismo
  problema que resuelve el [[anova]], y aquí se resuelve con la F de la interacción y, si hace
  falta, comparaciones post-hoc corregidas por [[multiplicidad-y-fdr]].
- **Confundir interacción con no aditividad de otra escala.** Una interacción en la escala
  original puede desaparecer al tomar logaritmos. Si el efecto del factor es multiplicativo, la
  interacción significativa en escala lineal es un artefacto de la escala. Decide la escala antes
  de mirar los datos, no después.
- **Ignorar el bloqueo y el orden aleatorio.** Si las 12 pruebas se hacen por tandas y las celdas
  se asignan por conveniencia (todas las de temperatura baja primero), el efecto de la tanda se
  cuela como interacción. Aleatoriza el orden dentro de cada bloque.

:::practica
enunciado: Un experimento 2 × 2 mide el tiempo de respuesta (en milisegundos) de dos interfaces (A y B) en dos tamaños de pantalla (pequeña y grande), con 10 usuarios por celda. Las medias son: A-pequeña 300, A-grande 340, B-pequeña 310, B-grande 400. Calcula los dos efectos principales y la interacción, y decide cómo hay que informar el resultado.
pista: Los efectos principales son diferencias de medias marginales (promediando las dos celdas) y la interacción es la diferencia de las diferencias.
solucion: Efecto de la interfaz: promediando tamaños, A da (300+340)/2 = 320 y B (310+400)/2 = 355, así que B tarda 35 ms más de media. Efecto del tamaño: promediando interfaces, pequeña (300+310)/2 = 305 y grande (340+400)/2 = 370, así que la pantalla grande tarda 65 ms más de media. Interacción: el efecto del tamaño con A es 340 − 300 = +40 y con B es 400 − 310 = +90, luego la interacción es 40 − 90 = −50 ms. Como la interacción es grande y del mismo orden que los efectos principales, informar «B tarda 35 ms más» es engañoso: con pantalla pequeña la diferencia es de solo 10 ms y con pantalla grande es de 60 ms. Lo correcto es informar los cuatro promedios (o los dos efectos simples del tamaño) y decir que la diferencia entre interfaces crece con el tamaño de pantalla.
:::

## Comprueba que lo sabes

:::quiz
p: Un experimento 2 × 2 da un efecto principal de la temperatura de −1,5 y una interacción de +15. ¿Qué conclusión es correcta?
o: Que la temperatura no influye, porque su efecto principal es casi cero
o: Que subir la temperatura mejora 6 unidades con el catalizador antiguo y empeora 9 con el nuevo, y el efecto principal es un promedio que no describe ninguna de las dos situaciones
o: Que hay un error en el cálculo, porque el efecto principal tiene que ser mayor que la interacción
a: 2
e: El efecto principal es el promedio de los dos efectos simples: (6 + (−9))/2 = −1,5. Que el promedio sea casi nulo no significa que el factor no haga nada, sino que hace cosas opuestas según el nivel del otro factor. Por eso, con interacción, se informan los efectos simples dentro de cada nivel.
:::

:::quiz
p: Tienes 4 factores para estudiar y presupuesto para 16 pruebas. ¿Qué diseño tiene más sentido?
o: Un factorial completo 2^4, que son exactamente 16 celdas
o: Cuatro experimentos de una variable cada vez, con 4 pruebas cada uno
o: Un factorial completo 4^2, con dos factores de cuatro niveles
a: 1
e: Un 2^4 son 16 combinaciones: cada prueba aporta información sobre los cuatro factores y sobre sus interacciones, con 16 celdas que cubren todo el espacio. El diseño de una variable cada vez no ve ninguna interacción y gasta los mismos recursos. Un 4^2 también son 16 celdas, pero solo estudia dos factores y deja los otros dos sin tocar.
:::

:::quiz
p: Un factorial 2 × 2 se ha ejecutado con una sola observación por celda. ¿Qué problema hay?
o: Ninguno, con 4 celdas ya se estiman los efectos
o: Que sin repeticiones no hay grados de libertad para estimar el error, así que no se puede contrastar la interacción ni calcular un p-valor honesto
o: Que hay que usar una prueba no paramétrica en lugar de ANOVA
a: 2
e: Con n = 1 por celda, el modelo saturado (media, dos efectos principales y la interacción) gasta los 4 grados de libertad totales: no queda ninguno para el error. Se puede suponer que la interacción de orden más alto es despreciable y usarla como error, pero es una hipótesis que hay que declarar y que no se puede comprobar. Con 3 repeticiones por celda hay 8 grados de libertad de error.
:::
