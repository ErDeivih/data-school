---
id: seleccion-de-features
titulo: Selección de variables
fase: 5
nivel: avanzado
rutas: [ds, core]
prerequisitos: [correlacion-pearson-spearman, validacion-cruzada]
tags: [variables, seleccion, sobreajuste]
resumen: Quedarse con las variables que aportan y tirar el resto: filtros, envolventes y métodos embebidos, con la estabilidad como criterio y sin colar el futuro.
fuentes: ["Guyon y Elisseeff (2003), 'An Introduction to Variable and Feature Selection'", "Meinshausen y Bühlmann (2010), 'Stability Selection'"]
---

## En una frase

Seleccionar variables es decidir cuáles entran en el modelo y cuáles se quedan fuera, porque
añadir columnas que no aportan no da más información: da más varianza.

## La idea

Imagina un juicio con testigos. Tres testigos fiables que vieron lo mismo valen más que treinta
que pasaban por allí. Cada testigo que añades es una oportunidad más de que el jurado se fije en
un detalle irrelevante. Con las variables pasa igual: cada columna nueva es un parámetro más que
estimar, y con un número fijo de filas, más parámetros significa una estimación peor de todos
ellos, incluidos los buenos.

Eso tiene nombre: el [[sesgo-varianza|compromiso sesgo-varianza]]. Un modelo con 5 variables
relevantes y 500 filas puede estimar bien sus coeficientes. El mismo modelo con esas 5 más 45
columnas de ruido aleatorio tiene 50 parámetros para 500 filas, y el ruido se reparte por los
coeficientes: el ajuste en entrenamiento mejora y el error en datos nuevos empeora. Si encima
hay más columnas que filas, el modelo puede ajustar los datos **exactamente**, con error cero en
entrenamiento y nulo valor predictivo.

Hay tres familias de métodos y conviene saber qué hace cada una:

- **Filtros.** Puntúan cada variable por separado, sin usar el modelo: varianza, correlación con
  el objetivo, información mutua, chi-cuadrado. Son rapidísimos y se pueden aplicar a 10.000
  columnas. Su límite es que ignoran las interacciones: una variable inútil por sí sola puede
  ser oro en combinación con otra.
- **Envolventes.** Prueban subconjuntos entrenando el modelo: selección hacia delante (añadir la
  que más mejora), hacia atrás (quitar la que menos duele), eliminación recursiva. Son los más
  precisos y los más caros: cada prueba es un entrenamiento completo.
- **Métodos embebidos.** La selección ocurre dentro del entrenamiento. El caso canónico es
  [[regularizacion-l1-l2|la penalización L1 (lasso)]], que empuja coeficientes exactamente a
  cero, y los árboles con [[importancia-de-variables|importancia por impureza]] o por
  permutación.

El criterio que casi nadie usa y que es el más importante es la **estabilidad**. Si seleccionas
variables con 10 particiones distintas de los mismos datos y salen 10 listas diferentes, tu
selección es ruido. Una variable que aparece en las 10 listas es una variable de verdad; una que
aparece en 3, seguramente no.

## Definición formal

Con `X` la matriz de variables, `y` el objetivo y `S` el subconjunto de columnas que se conserva:

- **Umbral de varianza.** Se descarta la columna `j` si `Var(xⱼ) < θ`. Con `θ = 0` caen las
  constantes, que no pueden explicar nada. Es un filtro previo, no una selección.
- **Correlación.** Se descarta una de dos columnas con `|corr(xⱼ, xₖ)| > 0,95`. Aportan lo mismo
  y, en un modelo lineal, sus coeficientes se reparten de forma arbitraria entre ellas.
- **Información mutua.** `I(xⱼ; y)` mide cuánta incertidumbre sobre `y` se elimina al conocer
  `xⱼ`. A diferencia de la correlación, detecta relaciones no lineales.
- **Importancia por permutación.** Se mide cuánto empeora la métrica al barajar al azar una
  columna. Si barajar `xⱼ` no cambia nada, la columna no se usa.
- **Lasso.** Se minimiza `(1/2n) · Σᵢ (yᵢ − ŷᵢ)² + α · Σⱼ |βⱼ|`. El término `α · Σ |βⱼ|` castiga
  la suma de los valores absolutos y, para `α` suficientemente grande, muchos `βⱼ` quedan
  exactamente en cero.

:::formula
minimizar  (1/2n) · Σᵢ (yᵢ − ŷᵢ)²  +  α · Σⱼ |βⱼ|        (lasso: L1)
:::

donde `n` es el número de filas, `yᵢ` el valor observado, `ŷᵢ` la predicción, `βⱼ` el coeficiente
de la variable `j` y `α` la fuerza de la penalización. Con `α = 0` es una regresión normal; a
medida que `α` crece, más coeficientes se anulan.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Número de filas con las que se ajusta el modelo | filas | Al dividir entre más filas, el término de error pesa más frente a la penalización: con el mismo `α`, el modelo conserva más variables |
| `α` | Fuerza de la penalización L1 | adimensional (no tiene unidades) | Es el mando del modelo: a más `α`, más coeficientes caen a cero exacto y más sesgo. Con `α` demasiado alto anula también las variables que sí aportan; con `α = 0` es una regresión sin selección |
| `βⱼ` | Coeficiente de la variable `j` | unidades de `y` por unidad de `xⱼ` | Si crece, esa variable pesa más en la predicción; el término de penalización `α · Σⱼ abs(βⱼ)` lo empuja hacia cero, y por eso L1 apaga variables en lugar de dejarlas pequeñas |
| `yᵢ` | El valor observado en la fila `i` | las del objetivo | No es un parámetro que se elija: es el dato |
| `ŷᵢ` | La predicción del modelo en la fila `i` | las del objetivo | Al acercarse a `yᵢ` baja el error, pero también suele subir el tamaño de los coeficientes: es el intercambio que gobierna `α` |
| `Σⱼ abs(βⱼ)` | Suma de los valores absolutos de todos los coeficientes | las del objetivo entre las de las variables | Sustituir L1 por L2 castiga `βⱼ²` en vez de `abs(βⱼ)`, y entonces los coeficientes se quedan pequeños pero **no** llegan a cero: se pierde la selección |
| `θ` | Umbral de varianza del filtro previo | las de la variable, al cuadrado | Con `θ = 0` solo caen las constantes; subirlo descarta variables poco informativas, pero medir la varianza en crudo favorece a las columnas con escala grande salvo que las estandaricen antes |
| `abs(corr(xⱼ, xₖ))` | Parecido lineal entre dos variables, en valor absoluto | adimensional, entre 0 y 1 | Por encima de 0,95 una de las dos sobra, y en un modelo lineal sus coeficientes se reparten de forma arbitraria entre ellas según la muestra |
:::

:::figura
fichero: seleccion-de-features-lasso-y-ruido
pie: A la izquierda, el camino de lasso: al subir `α` los coeficientes de `x2`, `x3`, `x5` y `x6` caen a cero exacto mientras los de `x1` y `x4` se encogen pero sobreviven. A la derecha, el mismo modelo con 60 filas y 45 columnas de ruido añadido: el `R²` medio pasa de 0,78 a −3,54, muy por debajo del cero que significa «predecir siempre la media». Ninguna columna nueva aportaba información, y sin embargo bastaron para arruinar el modelo.
fuente: figuras/seleccion-de-features-1.py
:::

La regla de oro del procedimiento: **la selección es parte del modelo**. Si eliges variables
mirando la métrica sobre el conjunto de prueba, el conjunto de prueba ha dejado de serlo. La
selección va **dentro** de cada pliegue de [[validacion-cruzada|validación cruzada]], nunca antes.

## Ejemplo

**Filtro de varianza y correlación.** Cuatro columnas:

```
col1: 1  2  3  4
col2: 3  3  3  3
col3: 5  4  3  2
col4: 5  4  3  2
```

El umbral de varianza conserva las columnas 1, 3 y 4 y descarta la 2, que es constante. Las
columnas 3 y 4 son idénticas: su correlación es **1,00**, así que una de las dos sobra. Con el
filtro de varianza solo no basta.

**El coste de añadir ruido.** 60 filas, 5 variables reales de las que solo 3 tienen efecto, y 45
columnas de ruido puro. Con validación cruzada de 5 pliegues:

- Coeficiente de determinación `R²` con las 5 variables reales: **0,63**.
- `R²` con las 5 más las 45 de ruido: **−7,53**.

Un `R²` negativo significa que el modelo predice peor que decir siempre la media. Has pasado de
un modelo decente a uno inútil sin tocar nada más que el número de columnas. Con 50 variables y
60 filas, cualquier ruido sirve para ajustar el entrenamiento.

**Lasso.** Las mismas 6 columnas de las que solo la 1 y la 4 tienen efecto, con `α = 0,1`:

- Coeficientes: **[2,91, 0, 0, −1,81, 0, 0,02]**.
- Variables anuladas: **3 de 6**.

El método no solo predice: te dice qué variables sobran. Su punto débil es que, con columnas muy
correlacionadas, elige una u otra de forma casi arbitraria según la muestra.

## Código

```python verificable
import numpy as np
from sklearn.feature_selection import VarianceThreshold

# Cuatro columnas: una constante, dos identicas y una informativa.
X = np.array([[1.0, 3.0, 5.0, 5.0],
              [2.0, 3.0, 4.0, 4.0],
              [3.0, 3.0, 3.0, 3.0],
              [4.0, 3.0, 2.0, 2.0]])

# threshold=0.0 tira solo las constantes; no detecta la redundancia entre columnas.
sel = VarianceThreshold(threshold=0.0).fit(X)
print("conservadas:", sel.get_support().tolist())   # -> [True, False, True, True]
print(f"correlacion columnas 3 y 4 {np.corrcoef(X[:, 2], X[:, 3])[0, 1]:.2f}")   # -> 1.00
```

:::claves
- `VarianceThreshold(threshold=0.0).fit(X)` no devuelve las columnas: devuelve el **selector**. Las columnas se piden con `sel.transform(X)` o `X[:, sel.get_support()]`, y `sel.get_support()` es una máscara booleana de `True`/`False`, no una lista de índices.
- La varianza que mide `VarianceThreshold` es la poblacional (`ddof=0`), no la muestral. Con `[1, 2, 3, 4]` sale `1,25` y no `1,67`. En una columna con todos los valores iguales da exactamente `0`, y por eso `threshold=0.0` la descarta: la comparación es `>` estricta.
- `threshold=0.0` **no** detecta columnas duplicadas, y el propio código lo demuestra: la 3 y la 4 son idénticas y las dos sobreviven. Un filtro de varianza solo mira cada columna consigo misma.
- `np.corrcoef(X[:, 2], X[:, 3])` devuelve una **matriz** 2×2, no un número: de ahí el `[0, 1]`. Si le pasas las cuatro columnas de golpe (`np.corrcoef(X.T)`) obtienes la matriz 4×4 completa, y las columnas constantes producen `nan` en toda su fila porque su desviación típica es cero.
- `Lasso(alpha=0.1)` no lleva `random_state` porque su ajuste es determinista (descenso por coordenadas), pero `alpha` no tiene escala universal: su efecto depende de las unidades de `X` y de `y`. Estandariza las columnas antes de comparar `alpha` entre problemas.
- `lasso.coef_` es un `np.ndarray` alineado con las columnas de `X`, no una lista de pares nombre-valor: el nombre de la variable solo lo tienes tú. Con el descenso por coordenadas de scikit-learn los descartados salen como `0.0` exacto, pero `round(float(c), 2) if abs(c) > 0.005 else 0.0` del ejemplo usa una tolerancia porque otros solvers devuelven `1e-17` en su lugar: comparar con `== 0` no es de fiar.
- `cross_val_score(..., scoring="r2").mean()` puede salir negativo. `R²` se calcula en cada pliegue con la media de **su** conjunto de prueba, así que un modelo peor que esa media da negativo, y el promedio de cinco valores negativos lo mantiene. Cambiar `cv=5` por `cv=KFold(5, shuffle=True, random_state=0)` mueve el resultado, porque el reparto por defecto no baraja.
:::

```python verificable
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

rng = np.random.default_rng(0)
n = 60
X_real = rng.normal(size=(n, 5))
# Solo las 3 primeras tienen efecto; las otras 2 y las 45 de ruido no aportan nada.
y = X_real @ np.array([2.0, -1.0, 0.5, 0.0, 0.0]) + rng.normal(0, 1.0, n)
ruido = rng.normal(size=(n, 45))

solo_real = cross_val_score(LinearRegression(), X_real, y, cv=5, scoring="r2").mean()
con_ruido = cross_val_score(LinearRegression(), np.hstack([X_real, ruido]), y, cv=5, scoring="r2").mean()

print(f"R2 con 5 variables reales {solo_real:.2f}")   # -> 0.63
print(f"R2 con 45 ruido anadido   {con_ruido:.2f}")   # -> -7.53
```

```python verificable
import numpy as np
from sklearn.linear_model import Lasso

rng = np.random.default_rng(0)
X = rng.normal(size=(100, 6))
y = 3.0 * X[:, 0] - 2.0 * X[:, 3] + rng.normal(0, 0.5, 100)

# La penalizacion L1 lleva a cero las variables que no aportan: seleccion embebida.
lasso = Lasso(alpha=0.1).fit(X, y)
print("coeficientes:", [round(float(c), 2) if abs(c) > 0.005 else 0.0 for c in lasso.coef_])
# -> coeficientes: [2.91, 0.0, 0.0, -1.81, 0.0, 0.02]
print(f"variables anuladas {int((np.abs(lasso.coef_) < 0.005).sum())} de {lasso.coef_.size}")
# -> variables anuladas 3 de 6
```

## Errores típicos

- **Seleccionar variables con todos los datos y validar después.** Elegir las 10 mejores por su
  correlación con el objetivo usando el conjunto completo, y luego hacer validación cruzada, da
  una estimación optimista: el conjunto de prueba participó en la elección. Es
  [[fuga-de-datos|fuga de datos]] por selección, y se corrige metiendo la selección dentro de
  cada pliegue.
- **Tomar la importancia por impureza como verdad absoluta.** En los árboles, la importancia por
  impureza favorece a las variables con muchos valores distintos y se reparte al azar entre
  columnas correlacionadas. Usa importancia por permutación sobre datos no vistos y comprueba
  que la conclusión aguanta.
- **Seleccionar con un único reparto de datos.** La lista de variables elegidas cambia con la
  semilla. Repite la selección en 10 particiones y quédate con las que aparecen casi siempre;
  esa es la idea de la selección por estabilidad.
- **Confundir correlación con efecto causal.** Que una variable esté correlacionada con el
  objetivo no significa que lo cause ni que sea útil para predecir en otro contexto. Y al
  revés: una variable con correlación casi nula puede ser imprescindible por su interacción con
  otra.
- **Añadir variables sin volver a medir.** Cada bloque de columnas nuevas hay que justificarlo
  con la misma validación y, si has probado muchas combinaciones, con el ajuste por pruebas
  múltiples de [[data-snooping-y-multiple-testing|data snooping]].
- **Eliminar variables que no están disponibles en producción.** Un filtro impecable sobre el
  histórico no sirve de nada si esa columna se calcula con un proceso que tarda tres días.
  Antes de seleccionar, comprueba que cada variable se puede servir a tiempo.

:::practica
enunciado: Seleccionas variables con lasso en 10 particiones distintas de los mismos datos y anotas en cuántas aparece cada candidata: x1 en 10, x2 en 9, x3 en 5, x4 en 2 y x5 en 1. Fijas el umbral de estabilidad en aparecer en 8 de las 10 particiones. ¿Qué variables conservas y qué porcentaje de las candidatas descartas?
pista: Pasa cada recuento a proporción sobre 10 y compáralo con el umbral.
solucion: x1 aparece en el 10/10 = 1,00 y x2 en el 9/10 = 0,90: las dos superan el umbral de 0,80. x3 se queda en 0,50, x4 en 0,20 y x5 en 0,10, así que las tres caen. Conservas 2 de las 5 candidatas y descartas 3, el 60 %. Con 10 particiones y 5 candidatas, exigir 8 apariciones es lo que separa la señal del ruido de muestreo.
:::

## Comprueba que lo sabes

:::quiz
p: Un modelo con 5 variables da R² = 0,63 en validación cruzada. Añades 45 columnas de ruido aleatorio y el R² cae a −7,53. ¿Qué ha pasado?
o: Que 50 variables siempre son demasiadas y el algoritmo se bloquea
o: Que con 50 variables para 60 filas el modelo ajusta el ruido y predice peor que la media
o: Que el ruido aleatorio contiene valores extremos que rompen la regresión
a: 2
e: Un R² negativo significa que el modelo es peor que predecir la media. Con más columnas que filas útiles, la regresión dispone de parámetros suficientes para ajustar el ruido del entrenamiento, y ese ajuste no se traslada a los pliegues de prueba. No es un fallo del algoritmo: es el compromiso sesgo-varianza en acción.
:::

:::quiz
p: Seleccionas las 10 variables más correlacionadas con el objetivo usando toda la tabla y luego haces validación cruzada de 5 pliegues. ¿Cuál es el problema?
o: Ninguno: la correlación se calcula por variable y no usa el modelo
o: Que el conjunto de prueba participó en la selección, así que la métrica sale optimista
o: Que la correlación de Pearson no detecta relaciones no lineales
a: 2
e: Aunque el filtro no entrene ningún modelo, miró todas las filas, incluidas las de prueba, para decidir qué columnas entran. Para que la estimación sea honesta, la selección debe repetirse dentro de cada pliegue usando solo su entrenamiento. Que la correlación ignore lo no lineal es cierto, pero es otro problema distinto.
:::

:::aviso
Seleccionar variables es una decisión de modelo más, así que también cuenta para el ajuste por
pruebas múltiples. Si has probado 200 subconjuntos y te quedas con el mejor, la métrica de ese
subconjunto está sesgada al alza igual que si hubieras probado 200 modelos. Reserva un conjunto
final que no hayas tocado o aplica la corrección correspondiente.
:::
