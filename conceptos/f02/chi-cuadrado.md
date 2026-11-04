---
id: chi-cuadrado
titulo: Test chi-cuadrado
fase: 2
nivel: intermedio
rutas: [ds, core]
prerequisitos: [contraste-de-hipotesis, p-valor, distribuciones-discretas, test-t]
tags: [inferencia, categoricas, tablas, independencia]
resumen: Contrastar si dos variables categóricas se relacionan o si unas frecuencias observadas encajan con las esperadas, y medir cuánto.
fuentes: ["Pearson (1900), 'On the Criterion that a Given System of Deviations from the Probable in the Case of a Correlated System of Variables is such that it can be Reasonably Supposed to have Arisen from Random Sampling'", "Agresti (2002), 'Categorical Data Analysis'"]
---

## En una frase

El test chi-cuadrado compara las frecuencias que has observado con las que esperarías si las dos
variables fueran independientes (o si se cumpliera una distribución teórica), y resume la
diferencia en un solo número.

## La idea

Tienes una tabla con dos formas de clasificar lo mismo: por dispositivo (móvil o escritorio) y
por si el usuario convirtió o no. Quieres saber si el dispositivo tiene algo que ver con
convertir, o si las diferencias que ves son las que aparecerían por azar al repartir 400
usuarios al azar en esas cuatro casillas.

La lógica es la de siempre en un contraste de hipótesis: construyes el escenario «no pasa nada»
—las dos variables son independientes, así que la tasa de conversión es la misma en los dos
dispositivos— calculas cuántos usuarios caerían en cada casilla en ese escenario y mides cuánto
se aleja tu tabla de esa tabla teórica. Si el alejamiento es grande respecto a lo que cabría
esperar por azar, rechazas la independencia.

La medida del alejamiento es la suma de las diferencias al cuadrado, dividida cada una entre lo
que se esperaba en esa casilla. Se eleva al cuadrado para que las diferencias positivas y
negativas no se cancelen, y se divide entre lo esperado para que una desviación de 10 usuarios
en una casilla de 20 pese mucho más que la misma desviación en una casilla de 2.000.

Dos usos distintos con la misma matemática:

- **Independencia (o homogeneidad)**: una tabla de contingencia de dos variables categóricas
  (dispositivo y conversión, tratamiento y efecto adverso, turno y error).
- **Bondad de ajuste**: una sola variable categórica y unas proporciones teóricas (¿están los
  pedidos repartidos de forma uniforme entre las cuatro franjas horarias?).

Y una advertencia que se salta casi todo el mundo: un chi-cuadrado significativo **no te dice
dónde está la diferencia ni si es importante**. Para lo primero, mira los residuos; para lo
segundo, mira la V de Cramér o la diferencia de proporciones, que es un
[[tamano-del-efecto|tamaño del efecto]].

## Definición formal

Con `Oᵢⱼ` el recuento observado en la casilla de la fila `i` y la columna `j`, y `Eᵢⱼ` el
recuento esperado bajo independencia:

:::formula
χ² = Σᵢⱼ (Oᵢⱼ − Eᵢⱼ)² / Eᵢⱼ ,   Eᵢⱼ = (total fila i · total columna j) / N
:::

- `χ²` — estadístico chi-cuadrado; la letra griega chi, `χ`, es solo el nombre del estadístico.
- `Oᵢⱼ` — lo que has contado en esa casilla.
- `Eᵢⱼ` — lo que contarías si las dos variables fueran independientes.
- `N` — total de observaciones de la tabla.
- Los grados de libertad son `(filas − 1) · (columnas − 1)`. Para una tabla 2×2, 1.

:::figura
fichero: chi-cuadrado-residuos-y-cola
pie: A la izquierda, cada casilla lleva su recuento y su residuo: móvil convierte 40 veces cuando esperaba 50, y escritorio 60 cuando esperaba 50, así que las cuatro desviaciones se suman en el mismo χ² = 5,33 (2,00 + 0,67 + 2,00 + 0,67). A la derecha, ese 5,33 se sitúa sobre la distribución que tendría el estadístico si no hubiera asociación: el área a su derecha es el p-valor de 0,0209. La consecuencia es que un χ² grande no te dice dónde está la diferencia, solo cuánta hay en total.
fuente: figuras/chi-cuadrado-1.py
:::

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `chi2` | Suma de las desviaciones al cuadrado, ponderadas por lo esperado | adimensional | Es el resultado de la formula. Crece cuando alguna casilla se aleja de lo esperado, y crece mas si la casilla que se aleja es pequeña: la misma desviación de 10 pesa el triple en una casilla de 50 que en una de 150 |
| `O_ij` | Recuento observado en la casilla (fila i, columna j) | observaciones (recuentos, nunca porcentajes) | Es el dato. Si le pasas proporciones o medias en vez de recuentos, el estadístico y los grados de libertad salen mal y el p-valor no significa nada |
| `E_ij` | Recuento que se esperaría si las dos variables fueran independientes | observaciones | No es un parámetro que muevas: sale de los marginales. Si alguna casilla baja de 5, la aproximación chi-cuadrado deja de ser fiable y toca el test exacto de Fisher |
| `N` | Total de observaciones de la tabla | observaciones | Multiplica la tabla entera sin cambiar las proporciones: `chi2` se multiplica por ese factor y el p-valor baja. Con N enorme, una asociación irrelevante sale significativa |
| `gl` | Grados de libertad, `(filas - 1)·(columnas - 1)` | grados de libertad | No mueve `chi2`, mueve la distribución con la que se compara. Con más gl, el mismo estadístico da un p-valor mayor: no es lo mismo 5,33 con 1 gl que con 6 |
| `V` | V de Cramér, el tamaño del efecto: `raiz(chi2 / (N · (min(r,c) - 1)))` | adimensional, de 0 a 1 | Es el número que hay que mirar además del p. Con V por debajo de 0,1 el efecto es pequeño aunque el p sea diminuto; con N grande, V pequeña y p minusculo conviven sin contradicción |
| `p` | Probabilidad de que el azar produzca un `chi2` igual o mayor | probabilidad, de 0 a 1 | Baja cuando `chi2` sube o cuando N sube. Ojo: la corrección de Yates para tablas 2×2 lo sube de 0,0209 a 0,0282 con los mismos datos |
:::

Para bondad de ajuste, `Eᵢ = N · pᵢ` con `pᵢ` las proporciones teóricas, y los grados de libertad
son `categorías − 1` (menos uno más por cada parámetro estimado de los datos).

**El tamaño del efecto** para una tabla de `r` filas y `c` columnas es la V de Cramér:

:::formula
V = √( χ² / (N · (min(r, c) − 1)) )
:::

Va de 0 (independencia perfecta) a 1. Para una tabla 2×2, `0,1` es un efecto pequeño, `0,3`
medio y `0,5` grande; son convenciones, no leyes.

**Condición práctica:** la aproximación chi-cuadrado necesita frecuencias esperadas razonables,
en la práctica **5 o más en todas las casillas**. Si no se cumple —típico en tablas 2×2 con
muestras pequeñas o con sucesos raros— usa el test exacto de Fisher, que calcula el p-valor
exactamente sin depender de la aproximación.

## Ejemplo

Conversión por dispositivo, con 200 usuarios en cada grupo:

```text
                    convierte   no convierte   total
movil                     40            160      200
escritorio                60            140      200
total                    100            300      400
```

La tasa global de conversión es 100 / 400 = 0,25. Si el dispositivo no influyera, cada uno de los
dos grupos de 200 tendría 0,25 · 200 = 50 conversiones:

```text
esperado            convierte   no convierte
movil                     50            150
escritorio                50            150
```

- Móvil: (40 − 50)² / 50 = 2,00 y (160 − 150)² / 150 = 0,67.
- Escritorio: (60 − 50)² / 50 = 2,00 y (140 − 150)² / 150 = 0,67.
- `χ²` = 2,00 + 0,67 + 2,00 + 0,67 = **5,33**, con 1 grado de libertad → **p ≈ 0,021**.
- V de Cramér = √(5,33 / 400) = **0,115**.

Hay evidencia de asociación, pero es pequeña: la diferencia de conversión es de 10 puntos
porcentuales (20 % frente a 30 %) sobre una base del 25 %. Con 400 usuarios, esa diferencia es
detectable; con 40, no lo sería.

## Código

```python verificable
import numpy as np
from scipy import stats

# Filas movil/escritorio, columnas convierte/no convierte.
tabla = np.array([[40, 160],
                  [60, 140]])
chi2, p, gl, esperado = stats.chi2_contingency(tabla, correction=False)

print(esperado.astype(int).tolist())                      # -> [[50, 150], [50, 150]]
print(f"chi2 {chi2:.3f}  gl {gl}  p {p:.4f}")             # -> chi2 5.333  gl 1  p 0.0209
print(f"V de Cramer {np.sqrt(chi2 / tabla.sum()):.3f}")   # -> V de Cramer 0.115
```

:::claves
- `stats.chi2_contingency` devuelve **cuatro** cosas y en este orden: `chi2, p, gl, esperado`. Si escribes `chi2, p = stats.chi2_contingency(tabla)` te llevas un error de desempaquetado; lo que casi nadie espera es que el **cuarto** valor, la tabla esperada, es un `np.array` de `float64`, no de enteros.
- `esperado` sale con decimales (50.0, 150.0) aunque los recuentos sean enteros, porque se calcula como `total_fila * total_columna / N`. El `.astype(int)` de la primera línea no es decorativo: **trunca**, no redondea. Con un esperado de 49,7 imprimirías 49 y creerías que la tabla cuadra cuando no cuadra.
- El `correction=False` del ejemplo es una decisión, no un detalle: SciPy pone `correction=True` por defecto en tablas 2×2. Con `correction=True`, Yates baja el estadístico de 5,333 a 4,813 y **sube** el p-valor de 0,0209 a 0,0282. La página compara los dos números justamente por eso: cambia la conclusión práctica.
- `(tabla - esperado) / np.sqrt(esperado)` funciona porque `tabla` es (2, 2) y `esperado` también; NumPy resta elemento a elemento. El `np.sqrt` es sobre la **tabla esperada**, no sobre la diferencia: si lo pusieras como `np.sqrt(tabla - esperado)` te arriesgas a una raíz de un número negativo cuando la casilla observada queda por debajo de la esperada.
- `tabla.sum()` sin `axis` suma **todo** el array y devuelve un único número: por eso `chi2 / tabla.sum()` da la V de Cramér de una tabla 2×2, donde `min(r, c) − 1 = 1`. Con una tabla en la que los dos lados tengan tres o más categorías ese `1` pasa a ser 2 y esa misma línea daría una V mal calculada.
- Si cambias el `40` por `45` (y el `160` por `155`), `chi2` cae de 5,33 a 2,91 y el p-valor sube a 0,088, por encima del umbral del 5 %: la asociación deja de ser significativa. Se comprueba ejecutando el bloque dos veces y comparando los `print`, que es exactamente lo que hace el verificador con la salida comentada.
:::

```python verificable
import numpy as np
from scipy import stats

# Residuos estandarizados: donde esta la diferencia que el p-valor global no senala.
tabla = np.array([[40, 160], [60, 140]])
chi2, p, gl, esperado = stats.chi2_contingency(tabla, correction=False)
residuos = (tabla - esperado) / np.sqrt(esperado)

print(f"movil       {residuos[0, 0]:+.2f}")   # -> movil       -1.41
print(f"escritorio  {residuos[1, 0]:+.2f}")   # -> escritorio  +1.41
print(f"Yates:      {stats.chi2_contingency(tabla, correction=True)[1]:.4f}")  # -> Yates:      0.0282
```

```python verificable
import numpy as np
from scipy import stats

# Bondad de ajuste: 200 pedidos en 4 franjas horarias, hipotesis de reparto uniforme.
observado = np.array([40, 60, 70, 30])
esperado = np.array([50, 50, 50, 50])
chi2, p = stats.chisquare(observado, esperado)

print(f"chi2 {chi2:.1f}  gl {observado.size - 1}  p {p:.4f}")
# -> chi2 20.0  gl 3  p 0.0002
```

## Errores típicos

- **Pasar porcentajes o medias a la tabla.** El chi-cuadrado necesita **recuentos**. Si tienes
  «el 20 % de 200», el recuento es 40. Con porcentajes, el estadístico y los grados de libertad
  salen mal.
- **Ignorar la regla de las frecuencias esperadas.** Si alguna `Eᵢⱼ` baja de 5, la aproximación
  chi-cuadrado no es fiable y el p-valor puede estar muy equivocado. Usa el test exacto de
  Fisher (`stats.fisher_exact`), sobre todo en tablas 2×2 con pocos datos.
- **Concluir causalidad.** El chi-cuadrado detecta asociación, no dirección ni causa. Que el
  dispositivo se asocie con convertir no significa que el dispositivo lo provoque. Eso es
  [[causalidad-vs-correlacion]].
- **Quedarse con el p global.** Un `χ²` significativo en una tabla de 4×3 no te dice qué celda
  se desvía. Mira los residuos estandarizados: los que pasan de ±2 en valor absoluto son los que
  están tirando del estadístico.
- **Presumir de p diminuto con V minúscula.** Con 2 millones de filas, una asociación con
  V = 0,01 sale con p < 0,001. Es real y es irrelevante. Informa siempre de las dos cosas.
- **Aplicar o no aplicar la corrección de Yates sin darte cuenta.** En tablas 2×2, la corrección
  de continuidad cambia el p-valor (0,0209 frente a 0,0282 en el ejemplo). En SciPy el valor por
  defecto de `chi2_contingency` es `correction=True`; decide y dilo.
- **Confundir independencia con homogeneidad.** Son la misma matemática con diseños distintos
  (una muestra clasificada por dos variables, frente a varias muestras comparadas en una
  variable). El nombre del test no cambia, pero la interpretación del diseño sí.

:::practica
enunciado: Una tienda compara la conversión de 300 usuarios según el dispositivo: 30 de 100 en tablet y 45 de 200 en escritorio. La tasa global es 75/300 = 0,25. Con el valor crítico de χ² con 1 grado de libertad al 5 % (3,84), calcula el estadístico, la V de Cramér y decide.
pista: Bajo independencia cada grupo convierte al 25 %, así que cada recuento esperado es total de fila por total de columna partido entre 300.
solucion: Esperados: tablet 25 y 75; escritorio 50 y 150. χ² = (30−25)²/25 + (70−75)²/75 + (45−50)²/50 + (155−150)²/150 = 1,00 + 0,33 + 0,50 + 0,17 = 2,00. V = √(2,00/300) = 0,082. Como 2,00 < 3,84, no se rechaza la independencia: la diferencia de conversión (30 % frente a 22,5 %) es compatible con el azar, y el efecto sería pequeño.
:::

## Comprueba que lo sabes

:::quiz
p: En el ejemplo, la conversión es 20 % en móvil y 30 % en escritorio, con 200 usuarios por grupo, y chi2 = 5,33. ¿Qué se puede concluir?
o: Que usar el móvil reduce la conversión diez puntos porcentuales
o: Que hay evidencia de asociación entre dispositivo y conversión, con un tamaño de efecto pequeño (V = 0,115)
o: Que no hay relación, porque V = 0,115 es menor que 0,3
a: 2
e: El test rechaza la independencia (p = 0,021) pero no dice nada sobre la dirección ni la causa, y el tamaño del efecto es pequeño. Un efecto pequeño puede ser real y detectable con muestra suficiente; no es lo mismo «no hay relación» que «la relación es modesta».
:::

:::quiz
p: Vas a hacer un chi-cuadrado de independencia sobre una tabla 2x2 con 18 observaciones en total. ¿Qué comprobación es imprescindible?
o: Que las frecuencias esperadas de las cuatro casillas lleguen a 5; si no, usa el test exacto de Fisher
o: Que las frecuencias observadas sean todas iguales
o: Que la variable tenga distribución normal
a: 1
e: La aproximación chi-cuadrado reparte una cantidad discreta con una distribución continua, y con esperados por debajo de 5 el error es grande. Con 18 observaciones en una tabla 2x2 los esperados suelen quedarse en 4 o 5, así que lo razonable es Fisher. La normalidad no tiene nada que ver aquí: son datos de recuento.
:::

:::quiz
p: Un chi-cuadrado de bondad de ajuste sobre cuatro categorías da chi2 = 20,0. ¿Cuántos grados de libertad tiene?
o: 3, porque son las categorías menos uno
o: 4, porque hay cuatro categorías
o: 1, porque la suma de los recuentos está fijada
a: 1
e: Con cuatro categorías y el total fijado, solo tres desviaciones son libres. Si además estimas parámetros a partir de los datos (por ejemplo, una media), se resta uno más por cada parámetro estimado.
:::

:::trampa
Un chi-cuadrado significativo en una tabla grande se cita muchas veces como «las variables están
relacionadas» sin mirar dónde. Abre la tabla: a veces toda la señal viene de una casilla con
pocos casos y el resto es homogéneo. Los residuos estandarizados te lo dicen en un segundo.
:::
