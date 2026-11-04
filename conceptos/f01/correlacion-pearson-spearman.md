---
id: correlacion-pearson-spearman
titulo: Correlación de Pearson y Spearman
fase: 1
nivel: básico
rutas: [core, ds]
prerequisitos: [covarianza-y-correlacion, medidas-de-dispersion]
tags: [estadistica, correlacion, relaciones]
resumen: Pearson mide cuánto se pega la nube de puntos a una recta y Spearman solo el orden; un único valor atípico puede mover la primera y no la segunda.
fuentes: ["Spearman (1904), 'The Proof and Measurement of Association between Two Things'", "Anscombe (1973), 'Graphs in Statistical Analysis'"]
---

## En una frase

La correlación mide si dos variables se mueven juntas: Pearson mide la parte **lineal** de esa
relación y Spearman mide solo si el orden de una acompaña al orden de la otra, y ninguna de las
dos dice nada sobre causalidad.

## La idea

Dibuja dos variables como una nube de puntos: cada punto es un caso, con su valor de `x` y su
valor de `y`. La correlación de **Pearson** pregunta cuánto se parece esa nube a una línea recta.
Si los puntos están sobre una recta con pendiente positiva, vale 1; si están sobre una recta con
pendiente negativa, vale −1; si forman una bola sin dirección, vale aproximadamente 0.

La correlación de **Spearman** hace un truco distinto: sustituye cada valor por su **rango** (el
puesto que ocupa al ordenar la variable) y calcula Pearson sobre esos rangos. Al quedarse solo
con el orden, ignora por completo las distancias. Eso la hace inmune a los valores extremos: da
igual que el valor más alto sea 20 o 20 millones, su rango es el mismo. Y detecta cualquier
relación **monótona**, no solo la lineal: si al crecer `x` siempre crece `y`, aunque sea muy
despacio al principio y muy rápido al final, Spearman da 1 y Pearson da menos.

Esa diferencia es la que decide cuál usar. En una relación dosis-respuesta, en precios que
crecen de forma multiplicativa, o cuando hay valores atípicos que no quieres borrar, Spearman
responde mejor a la pregunta «¿van juntas en el mismo sentido?». Pearson responde a una pregunta
más estrecha y más exigente: «¿se mueven de forma proporcional?». Y hay casos en los que las dos
fallan a la vez: si la relación es una `U` perfecta (primero baja, luego sube), Pearson da 0 y
Spearman también, aunque `y` esté completamente determinada por `x`.

Tres advertencias que valen más que la fórmula. La primera: **correlación no es causalidad**; dos
series que crecen con el tiempo se correlacionan casi siempre, sin ninguna relación real
([[causalidad-vs-correlacion]]). La segunda: un solo punto puede cambiar el resultado, así que
nunca mires el número sin mirar el gráfico. La tercera: `r = 0,5` no es «el 50 % de relación»;
para eso está `r² = 0,25`, la fracción de varianza que una recta explica. Con series temporales,
esa primera advertencia se ve en números en el código de más abajo: dos series independientes que
solo suben dan una correlación de 0,93 en niveles y de 0,02 en cambios.

## Definición formal

Con `n` pares `(x₁, y₁), …, (xₙ, yₙ)`, sus medias `x̄` e `ȳ` y sus desviaciones típicas `s_x` y
`s_y`:

:::formula
r = cov(x, y) / (s_x · s_y) = Σᵢ (xᵢ − x̄)(yᵢ − ȳ) / √( Σᵢ (xᵢ − x̄)² · Σᵢ (yᵢ − ȳ)² )
:::

- `xᵢ`, `yᵢ` — los valores de las dos variables en el caso `i`.
- `x̄`, `ȳ` — sus medias.
- `cov(x, y)` — la covarianza muestral: cuánto varían juntas las dos variables.
- `s_x`, `s_y` — las desviaciones típicas de cada una. Al dividir entre ellas, `r` queda
  adimensional y acotado entre −1 y 1 ([[covarianza-y-correlacion]]).

La correlación de **Spearman** es el mismo cálculo sobre los rangos:

:::formula
ρ = r( R(x), R(y) )        ρ = 1 − 6 · Σᵢ dᵢ² / (n · (n² − 1))   si no hay empates
:::

- `R(xᵢ)` — el rango del valor `xᵢ`: su posición al ordenar la variable, de 1 a `n`. Con valores
  repetidos se usa el rango medio (si dos valores comparten las posiciones 3 y 4, los dos reciben
  3,5).
- `dᵢ = R(xᵢ) − R(yᵢ)` — la diferencia de rangos de cada caso.
- La segunda fórmula es un atajo válido solo si no hay empates; la primera funciona siempre.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `xᵢ`, `yᵢ` | Los dos valores del caso `i` | las de cada variable, que pueden ser distintas | Al subir uno solo de los valores, `r` cambia y `ρ` cambia solo si ese valor cruza a otro en el orden. Un punto que se dispara fuera de la recta es justo lo que baja `r` de 1 a 0,82 |
| `x̄`, `ȳ` | Las medias de cada variable | las de cada variable | Centran la nube. Sumar una constante a una variable no cambia ni `r` ni `ρ`: restar la media ya lo hace por ti |
| `s_x`, `s_y` | Las desviaciones típicas de cada variable | las de cada variable | Son el divisor de `r` y lo que lo hace adimensional. Si alguna vale 0 (variable constante), `r` no está definido, y NumPy devuelve `nan` con un aviso en lugar de un error |
| `cov(x, y)` | Covarianza muestral: cuánto varían juntas las dos variables | producto de las unidades de las dos | Al subir, la relación va en el mismo sentido (positiva) o al contrario (negativa), pero el tamaño bruto solo se compara entre datos en las mismas unidades: multiplicar una variable por 100 multiplica la covarianza por 100 y deja `r` igual |
| `r` | Correlación de Pearson: la parte **lineal** del acoplamiento | adimensional, entre −1 y 1 | Al subir, los puntos se pegan a una recta creciente. Vale 1 con una recta perfecta y 0 si la nube no tiene dirección lineal, y **no** dice qué fracción de relación hay: eso es `r²` |
| `ρ` | Correlación de Spearman: el mismo cálculo sobre los rangos | adimensional, entre −1 y 1 | Al subir, el orden de una variable acompaña al de la otra. Es 1 en cualquier relación monótona creciente, aunque no sea recta, y no se inmuta si el valor más alto pasa de 20 a 20 millones |
| `R(xᵢ)`, `R(yᵢ)` | El rango (el puesto) de cada valor dentro de su variable | número entero de 1 a `n`; con empates, el rango medio | Al subir, un valor adelanta a otros. Es lo único que usa Spearman: por eso dos valores muy distintos pero en la misma posición dan el mismo resultado |
| `dᵢ` | Diferencia de rangos de un caso, `R(xᵢ) − R(yᵢ)` | número entero (o medio entero con empates) | Al subir en valor absoluto, `ρ` baja. La fórmula `1 − 6·Σdᵢ²/(n(n² − 1))` solo vale si no hay empates, porque los rangos medios rompen esa suma |
| `n` | Número de pares `(x, y)` | ninguna (recuento) | No cambia el valor de `r` ni el de `ρ`, pero sí su fiabilidad: con `n = 8` es fácil ver 0,7 por puro azar, y hace falta mucha más muestra para sostener una correlación pequeña |
:::

Propiedades que conviene tener presentes:

- `r` y `ρ` son **simétricas**: da igual qué variable llames `x`.
- `r` no cambia si cambias las unidades de una variable con una transformación afín positiva:
  pasar de metros a centímetros o de euros a dólares deja `r` igual.
- `r` **sí** cambia con transformaciones no lineales (logaritmos, cuadrados); `ρ` no cambia con
  ninguna transformación estrictamente creciente.
- `ρ = 1` significa relación monótona creciente perfecta; `r = 1`, relación lineal perfecta. La
  segunda es un caso particular de la primera.
- `r²` es la fracción de la varianza de `y` que explica una recta ajustada por mínimos cuadrados.
- El coeficiente de **Kendall** (`τ`) es una tercera alternativa: cuenta parejas concordantes y
  discordantes. Con pocos datos y muchos empates se comporta mejor que `ρ`, y su valor suele ser
  algo menor en valor absoluto.

## Ejemplo

Ocho casos con `x = 1, 2, 3, 4, 5, 6, 7, 8` y tres versiones distintas de `y`:

```text
Lineal:      y = 1  2  3  4  5  6  7   8
Un atipico:  y = 1  2  3  4  5  6  7  20
Curva:       y = 1  4  9 16 25 36 49  64
```

| Caso | Pearson | Spearman |
| --- | --- | --- |
| Lineal | +1,0000 | +1,0000 |
| Un atípico | +0,8165 | +1,0000 |
| Curva | +0,9762 | +1,0000 |

- **Lineal:** las dos valen 1, porque una recta perfecta es también una relación monótona perfecta.
- **Un atípico:** un solo punto (el último) baja Pearson de 1,00 a 0,82. Spearman no se inmuta:
  el orden sigue siendo el mismo, el valor 20 sigue siendo el mayor.
- **Curva:** la relación es `y = x²`, monótona pero nada lineal. Spearman la ve perfecta (1,0000);
  Pearson la infravalora (0,9762) porque solo premia las rectas.

Y el caso en el que las dos fallan:

```text
x = -4 -3 -2 -1  0  1  2  3  4
y = 16  9  4  1  0  1  4  9 16
```

Aquí `y = x²` con valores negativos de `x`: la relación es determinista y perfecta (sabiendo `x`
sabes `y` con total exactitud), pero Pearson da 0,0000 porque la nube es simétrica respecto a la
vertical, y Spearman también da 0,0000 porque la relación no es monótona: baja hasta `x = 0` y
luego sube. Es el recordatorio de que ninguna correlación es un resumen completo: si no se mira
el gráfico, este patrón pasa por «no hay relación» cuando la hay total.

:::figura
fichero: correlacion-pearson-frente-a-spearman
pie: En los tres paneles se leen las dos correlaciones del mismo par de variables. Con una recta perfecta valen 1 las dos; con el último valor disparado a 20, Pearson cae a 0,8165 y Spearman se queda en 1,0000 porque el 20 sigue siendo el mayor de la lista; y con `y = x²`, monótona pero nada recta, Spearman ve 1,0000 y Pearson solo 0,9762. Si solo publicas una de las dos, estás decidiendo por el lector qué tipo de relación buscabas.
fuente: figuras/correlacion-pearson-spearman-1.py
:::

## Código

```python verificable
import numpy as np
from scipy import stats

x = np.arange(1, 9, dtype=float)
lineal = x.copy()                                   # y = x
con_atipico = np.array([1, 2, 3, 4, 5, 6, 7, 20], dtype=float)
curva = x ** 2                                      # monotona, pero no lineal

for nombre, y in (("lineal", lineal), ("atipico", con_atipico), ("curva", curva)):
    r = stats.pearsonr(x, y)[0]
    rho = stats.spearmanr(x, y)[0]
    print(f"{nombre:>8}  Pearson {r:+.4f}  Spearman {rho:+.4f}")
# ->   lineal  Pearson +1.0000  Spearman +1.0000
# ->  atipico  Pearson +0.8165  Spearman +1.0000
# ->    curva  Pearson +0.9762  Spearman +1.0000
```

:::claves
- `stats.pearsonr(x, y)` **no devuelve un número**: devuelve una tupla con el coeficiente y el p-valor. Con `r = stats.pearsonr(x, y)` te llevas los dos y luego `r[0]` es el coeficiente; el `[0]` del código no es un capricho.
- `stats.spearmanr(x, y)` tiene la misma firma por comodidad, pero con más de dos variables devuelve una **matriz** de correlaciones en lugar de un número: `stats.spearmanr(np.column_stack([a, b, c]))` da un resultado cuyo `[0]` tiene forma `(3, 3)`. Con dos variables, en cambio, `[0]` es el coeficiente. El tipo de objeto no cambia, así que el error se descubre al usar el número, no al llamar.
- `x ** 2` sobre un array de `float` eleva cada elemento, no la matriz: no hay que transponer ni usar `np.power`. La trampa es `x ** 2` con `x` entero y exponente negativo, que en Python 3 lanza un error de valor en vez de truncar a cero.
- Spearman se calcula en la práctica como Pearson sobre los rangos, y con empates scipy usa el rango medio. Comprobarlo es fácil: `stats.spearmanr(x, y)[0]` y `stats.pearsonr(stats.rankdata(x), stats.rankdata(y))[0]` coinciden hasta el último decimal; con empates, esa igualdad es la definición que vale.
- El bucle `for nombre, y in (("lineal", lineal), ...)` recorre una tupla de pares: cada iteración desempaqueta el nombre y el array. Ojo con la variable `y`, que se sobrescribe en cada vuelta; si la necesitaras después del bucle, tendrías la del último caso.
- En el bloque de series temporales, `np.diff(a)` devuelve un array con un elemento menos que `a`: 49 cambios a partir de 50 niveles. Es la diferencia entre correlacionar los niveles (0,93, espuria) y los cambios (0,02, lo que de verdad hay).
:::

```python verificable
import numpy as np
from scipy import stats

# Relacion determinista y perfecta que ninguna de las dos correlaciones detecta
x = np.arange(-4, 5, dtype=float)
y = x ** 2

print("Pearson ", round(float(stats.pearsonr(x, y)[0]), 4))    # -> 0.0
print("Spearman", round(float(stats.spearmanr(x, y)[0]), 4))   # -> 0.0
```

```python verificable
import numpy as np
from scipy import stats

# Dos series independientes que solo suben: correlacion alta sin ninguna relacion
rng = np.random.default_rng(0)
n = 50
t = np.arange(n)
a = 0.5 * t + rng.normal(0, 1, n)
b = 0.2 * t + rng.normal(0, 1, n)

print("en niveles", round(float(stats.pearsonr(a, b)[0]), 2))          # -> 0.93
print("en cambios", round(float(stats.pearsonr(np.diff(a), np.diff(b))[0]), 2))  # -> 0.02
```

## Errores típicos

- **Leer la correlación como un porcentaje o como una causa.** `r = 0,5` no significa «50 % de
  relación» ni que una variable provoque la otra. La fracción de varianza compartida es `r²`, o
  sea el 25 %, y la causalidad necesita un diseño, no un coeficiente.
- **Usar Pearson con relaciones monótonas no lineales.** Con precios, dosis o cualquier variable
  que crezca de forma multiplicativa, Pearson subestima la relación. Si la pregunta es «¿van en
  el mismo sentido?», usa Spearman.
- **Dejar que un valor atípico decida.** Un solo punto puede llevar `r` de 0,1 a 0,9 o al revés.
  Reportar una correlación sin el gráfico de dispersión es reportar un número sin saber qué mide.
- **Correlacionar series temporales en niveles.** Dos series que crecen con el tiempo tienden a
  correlacionarse aunque sean independientes, porque comparten la tendencia. Hay que quitar la
  tendencia o correlacionar los cambios ([[estacionariedad]]).
- **Restringir el rango y concluir que no hay relación.** Si calculas la correlación solo con los
  clientes que siguen activos, o solo con los aprobados, has recortado la parte de la variable
  donde estaba la señal: `r` baja y parece que no pasa nada ([[sesgo-de-supervivencia]]).
- **Sumar correlaciones de grupos distintos.** El coeficiente calculado sobre datos agregados
  puede tener el signo contrario al de cada grupo por separado (paradoja de Simpson). Antes de
  agregar, comprueba si los grupos se comportan igual.
- **Confundir la correlación con la pendiente.** `r` no dice cuánto cambia `y` cuando cambia `x`:
  eso depende de las unidades. `r` mide el acoplamiento, no el efecto.

:::trampa
`pandas.DataFrame.corr()` usa Pearson por defecto y **descarta las filas con nulos por parejas**,
así que cada celda de la matriz puede estar calculada con un subconjunto distinto de datos. Con
muchos nulos, dos celdas de la misma tabla no son comparables. Comprueba el recuento antes de
sacar conclusiones.
:::

:::practica
enunciado: Cinco alumnos estudian 1, 2, 3, 4 y 5 horas y sacan 3, 5, 4, 7 y 9 puntos. Calcula la correlación de Spearman con la fórmula de las diferencias de rangos y di qué pasaría con ρ si el último sacara 30 en vez de 9.
pista: Sustituye cada nota por su puesto (1 al menor) y usa ρ = 1 − 6·Σd²/(n·(n² − 1)).
solucion: Los rangos de las notas son 1, 3, 2, 4, 5, así que d = 0, −1, 1, 0, 0 y Σd² = 2. ρ = 1 − 6·2/(5·24) = 1 − 12/120 = 0,90. Con 30 puntos el orden no cambia: ρ sigue valiendo 0,90, mientras que Pearson subiría bastante. Spearman solo mira el orden, no las distancias.
:::

## Comprueba que lo sabes

:::quiz
p: Con x = 1…8 e y = 1, 2, 3, 4, 5, 6, 7, 20, ¿qué pasa con las dos correlaciones?
o: Las dos bajan de 1,00 a 0,82
o: Pearson baja a 0,8165 y Spearman se queda en 1,0000
o: Pearson se queda en 1,0000 y Spearman baja a 0,8165
o: Las dos siguen valiendo 1,0000 porque el orden no cambia
a: 2
e: Pearson usa los valores, así que un punto que se separa mucho de la recta reduce el ajuste a 0,8165. Spearman usa solo los rangos y el 20 sigue siendo el mayor: la relación de orden es perfecta y da 1,0000. Esa es justo la razón de calcular las dos.
:::

:::quiz
p: ¿Qué afirmación sobre la correlación de Spearman es correcta?
o: Mide la relación lineal y por eso es más precisa que Pearson
o: No cambia si aplicas a una variable una transformación estrictamente creciente
o: Solo se puede calcular si las dos variables son normales
o: Siempre es mayor que la de Pearson
a: 2
e: Spearman trabaja con rangos, y una transformación estrictamente creciente no altera el orden. No mide linealidad (eso es Pearson), no exige normalidad y no siempre es mayor: en una relación lineal con un valor atípico que rompe la monotonía puede quedar por debajo.
:::

:::quiz
p: Dos series anuales de dos países crecen las dos con el tiempo y su correlación en niveles es 0,93. ¿Qué conclusión es defendible?
o: Que una economía arrastra a la otra
o: Que hay una relación causa-efecto que hay que confirmar
o: Que comparten tendencia, y por eso hay que mirar los cambios o quitar la tendencia antes de interpretar nada
o: Que la correlación está mal calculada, porque con series temporales nunca puede ser alta
a: 3
e: Dos series con tendencia creciente comparten el orden temporal y correlacionan aunque sean independientes: es la regresión espuria. La solución es trabajar con cambios, con residuos o quitando la tendencia. La correlación no aporta ninguna evidencia causal.
:::
