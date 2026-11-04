---
id: encoding-de-categoricas
titulo: Codificación de categóricas
fase: 5
nivel: intermedio
rutas: [ds, de]
prerequisitos: [pandas-fundamentos, eda-pasos]
tags: [categoricas, preprocesamiento, fuga]
resumen: Convertir categorías en números sin inventar un orden y sin colar la variable objetivo: one-hot, ordinal, frecuencia y target encoding con su trampa.
fuentes: ["Micci-Barreca (2001), 'A Preprocessing Scheme for High-Cardinality Categorical Attributes'"]
---

## En una frase

Un modelo solo come números, así que cada categoría hay que convertirla en uno o varios
números, y la forma de hacerlo decide si el modelo aprende una relación real o una inventada.

## La idea

Tienes una columna «ciudad» con Madrid, Lugo y Sevilla. La tentación es asignar
Madrid = 1, Lugo = 2, Sevilla = 3 y seguir. Eso es **codificación ordinal**, y solo es legítima
si el orden existe de verdad. En este caso acabas de decirle al modelo que Sevilla es el triple
de Madrid, y una regresión se lo va a creer: calculará un coeficiente por unidad de «ciudad».

La alternativa clásica es **one-hot**: una columna por categoría, con un 1 en la que
corresponde y 0 en las demás. No inventa ninguna distancia y funciona bien en árboles. Su
problema es el tamaño: una columna «código postal» con 8.000 valores produce 8.000 columnas
nuevas, casi todas con un solo 1 en toda la tabla. Eso se llama **alta cardinalidad**, y es
donde el one-hot deja de ser una opción: la tabla se vuelve enorme, dispersa y fácil de
sobreajustar.

Para esos casos existe el **target encoding** (o codificación por media): se sustituye cada
categoría por la media de la variable objetivo en esa categoría. Es potentísimo y es la fuente
de fuga de datos más común en preparación de variables, por un motivo simple: la media se
calcula **con la propia fila dentro**. Si una categoría aparece una sola vez y esa fila es
positiva, su valor codificado es exactamente 1, y el modelo aprende la etiqueta en vez de
aprender el patrón.

La solución tiene dos piezas que van juntas:

1. **Calcular la codificación fuera de la fila.** O se deja la fila fuera de su propia media
   (leave-one-out), o mejor aún se calcula por pliegues sobre el entrenamiento (out-of-fold).
2. **Suavizar hacia la media global.** Una categoría con 3 observaciones tiene una media
   ruidosa; se mezcla con la media general ponderando por el número de observaciones,
   exactamente igual que un estimador bayesiano con un prior.

Entre medias hay opciones baratas que casi nadie recuerda: codificar por **frecuencia** (cuántas
veces aparece la categoría) o agrupar las categorías raras en una sola clase «otros». Ambas
conservan información útil sin crear 8.000 columnas.

:::figura
fichero: encoding-ordinal-onehot-y-target
pie: A la izquierda, las tres ciudades con las dos codificaciones. El ordinal las convierte en 1, 2 y 3, y con eso la regresión calcula un coeficiente por unidad de «ciudad»: acaba de aprender que Sevilla es el triple de Madrid. El one-hot pone un punto en su columna y ninguno más, así que todas las categorías quedan a la misma distancia. A la derecha, el target encoding crudo sobre seis filas: cada fila aporta su propia `y` a su valor (0,67 para la categoría A), y al dejar la fila fuera los valores cambian a 0,5 / 1,0 / 0,5. La última fila de B tiene `y = 1` y le toca un 0,00 con leave-one-out: con categorías de una sola fila esa codificación le dice al modelo justo lo contrario de lo que debe predecir.
fuente: figuras/encoding-de-categoricas-1.py
:::

## Definición formal

Sea `C` una variable categórica con `K` valores posibles `c₁, …, cₖ`, y `y` la variable objetivo.

- **Ordinal:** una función `f: C → ℤ` que asigna un entero a cada categoría. Solo es válida si
  existe un orden real (bajo, medio, alto) y el salto entre niveles consecutivos tiene sentido.
- **One-hot:** `K` columnas indicadoras `xᵢₖ = 1` si la fila `i` tiene la categoría `cₖ` y `0` en
  caso contrario. La suma de la fila es 1.
- **Trampa de las dummies:** si se incluyen las `K` columnas junto con un término constante, son
  linealmente dependientes (suman 1 en todas las filas) y la regresión no tiene solución única.
  Por eso se elimina una columna de referencia y quedan `K − 1`.
- **Frecuencia:** `xᵢ = n(cᵢ) / n`, la proporción de filas con esa categoría.
- **Target encoding con suavizado:**

:::formula
x̂(c) = ( n(c) · ȳ(c) + m · ȳ ) / ( n(c) + m )
:::

donde `n(c)` es el número de filas con la categoría `c`, `ȳ(c)` la media del objetivo en esas
filas, `ȳ` la media global del objetivo y `m` un parámetro de suavizado (típicamente entre 5 y
100) que dice cuántas filas «virtuales» de la media global se añaden. Con `m = 0` no hay
suavizado y gana el ruido; cuanto mayor es `m`, más se parece la codificación a la media global.

La versión **out-of-fold** sustituye `ȳ(c)` por la media calculada solo en los pliegues que no
contienen la fila `i`. Es la única forma de que el valor codificado de una fila no contenga su
propio objetivo.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `K` | Número de valores distintos de la categoría (su cardinalidad) | categorías | Con one-hot produce `K` columnas nuevas. Por encima de unas decenas la tabla se vuelve enorme y dispersa, y cada columna tiene tan pocas filas que el modelo memoriza |
| `C` | La variable categórica | texto o etiqueta | No se puede meter en un modelo tal cual: hay que convertirla, y la forma de hacerlo es justo lo que se decide en esta página |
| `c` | Una categoría concreta | etiqueta | Es la unidad que se codifica; su frecuencia y su media del objetivo deciden cuánto se puede fiar el modelo de ella |
| `n(c)` | Número de filas con la categoría `c` | filas | Más filas dan una media más fiable. Por debajo de 5 el valor es casi ruido y hay que suavizarlo o agrupar la categoría en «otros» |
| `xᵢₖ` | Indicador one-hot: 1 si la fila `i` es de la categoría `cₖ` | 0 o 1 | Siempre vale 0 o 1; estandarizarlo lo convierte en valores como −0,3 y destruye su lectura. La suma de la fila es 1 (o 0 si la categoría es nueva) |
| `K − 1` | Columnas que quedan al eliminar la de referencia | columnas | Es la opción correcta junto a un término constante: con las `K` columnas, todas suman 1 y la regresión no tiene solución única |
| `n(cᵢ) / n` | Codificación por frecuencia | tanto por uno, 0 a 1 | Sube con las categorías habituales. Conserva información útil sin crear columnas, pero confunde «frecuente» con «importante»: una categoría muy común y con media normal queda con un valor alto |
| `ȳ(c)` | Media del objetivo en las filas de la categoría `c` | las del objetivo | Es el corazón del target encoding y también su peligro: calculada con la fila dentro, cada fila aporta su propia etiqueta a su propio valor |
| `ȳ` | Media global del objetivo | las del objetivo | Es el prior hacia el que se arrastran las categorías raras; con `m` grande, la codificación se le parece cada vez más |
| `m` | Fuerza del suavizado: filas «virtuales» del prior | filas | Con `m = 0` no hay suavizado y gana el ruido de las categorías pequeñas; cuanto mayor es `m`, más se acerca todo a la media global. El rango habitual es 5 a 100 |
| `x̂(c)` | El valor codificado que recibe la categoría | las del objetivo | Es lo que ve el modelo en lugar de la etiqueta. Con `m = 10`, una categoría de 3 filas con media 1,00 se queda en 0,38: el suavizado le quita la falsa seguridad |
:::

## Ejemplo

**One-hot.** Cinco filas con tres ciudades (Madrid, Lugo, Sevilla):

```
Madrid, Lugo, Madrid, Sevilla, Lugo
```

Sin eliminar referencia salen 3 columnas (`ciudad_Lugo`, `ciudad_Madrid`, `ciudad_Sevilla`);
con `drop_first` salen 2 (`ciudad_Madrid`, `ciudad_Sevilla`). Con 3 categorías la diferencia es
cosmética; con 8.000, no.

**Target encoding y su fuga.** Seis filas, dos ciudades y un objetivo binario:

```
ciudad: A  A  A  B  B  B
y:      1  0  1  0  0  1
```

- Media global: 3/6 = **0,50**.
- Codificación cruda por ciudad: A → 2/3 = **0,67**, B → 1/3 = **0,33**. La fila 1 tiene `y = 1`
  y su valor codificado es 0,67, que ya contiene ese 1.
- Dejando fuera la propia fila: A → **0,5, 1,0, 0,5** y B → **0,5, 0,5, 0,0**. La tercera fila
  de B tiene `y = 1` y su codificación es 0,0, es decir, el modelo ve justo lo contrario de lo
  que debe predecir. Con categorías de una sola fila, el leave-one-out es una bomba: hay que
  usar out-of-fold y suavizado, no leave-one-out a pelo.

**Suavizado.** Una categoría frecuente (100 filas, media 0,60) y una rara (4 filas, media 0,75),
con media global 0,61 y `m = 10`:

- Frecuente: (100 · 0,60 + 10 · 0,61) / 110 = **0,60**.
- Rara: (4 · 0,75 + 10 · 0,61) / 14 = **0,65**.

El suavizado apenas toca a la categoría con datos y arrastra la rara hacia la media global:
el 0,75 de cuatro observaciones no es de fiar y se corrige solo.

## Código

```python verificable
import pandas as pd

ciudades = pd.DataFrame({"ciudad": ["Madrid", "Lugo", "Madrid", "Sevilla", "Lugo"]})

# Una columna por categoria; con drop_first se quita la referencia y se evita la colinealidad.
todas = pd.get_dummies(ciudades, columns=["ciudad"])
sin_una = pd.get_dummies(ciudades, columns=["ciudad"], drop_first=True)

print(f"columnas sin drop_first {todas.shape[1]}")    # -> 3
print(f"columnas con drop_first {sin_una.shape[1]}")  # -> 2
print("columnas:", list(sin_una.columns))            # -> ['ciudad_Madrid', 'ciudad_Sevilla']
```

:::claves
- `pd.get_dummies` **no toca** el DataFrame original: devuelve uno nuevo. Si quieres el resultado tienes que asignarlo, como hace el ejemplo. Comprueba que `ciudades` sigue teniendo una sola columna después de las dos llamadas.
- `columns=["ciudad"]` es la lista de columnas que se convierten. Si la omites, `get_dummies` convierte **todas** las columnas de texto del DataFrame y puede dejar el resultado irreconocible. Si pasas una columna que no existe, pandas lanza un `KeyError`; no lo ignora.
- `drop_first=True` elimina la primera categoría en orden alfabético, no la más frecuente. Por eso desaparece `ciudad_Lugo` y quedan `ciudad_Madrid` y `ciudad_Sevilla`: Lugo pasa a ser «todo cero». Es una referencia implícita, y saber cuál es importa para interpretar los coeficientes.
- `todas.shape[1]` da 3 y `sin_una.shape[1]` da 2, pero fíjate en que **ninguna** de las dos incluye la columna original: `get_dummies` la sustituye, no la duplica. Y `sin_una.columns` es un `Index`, no una lista; por eso el ejemplo lo envuelve en `list(...)` antes de imprimirlo.
- Los nombres de las columnas nuevas se construyen como `original_valor`. Si una categoría contiene un guion o un espacio, el nombre lo arrastra y luego hay que escribirlo igual en `df["ciudad_San Sebastián"]`. Con miles de categorías conviene normalizar los nombres antes o usar `prefix=` para controlar el prefijo.
- Lo que aquí es cosmético (3 columnas frente a 2) deja de serlo con 8.000 categorías, y el motivo no es solo el tamaño: cada columna tendría un único 1 en toda la tabla. Compara `todas.values.sum()` con el número de filas y verás que la matriz está casi vacía. Eso es la alta cardinalidad, y es la razón de que existan frecuencia y target encoding.
:::

```python verificable
import pandas as pd

# Target encoding crudo frente a dejar fuera la propia fila.
df = pd.DataFrame({
    "ciudad": ["A", "A", "A", "B", "B", "B"],
    "compro": [1, 0, 1, 0, 0, 1],
})

crudo = df.groupby("ciudad")["compro"].transform("mean")
suma = df.groupby("ciudad")["compro"].transform("sum")
cuenta = df.groupby("ciudad")["compro"].transform("count")
fuera = (suma - df["compro"]) / (cuenta - 1)   # media sin la propia fila

print(f"media global      {df['compro'].mean():.2f}")     # -> 0.50
print("encoding crudo   ", crudo.round(2).tolist())      # -> [0.67, 0.67, 0.67, 0.33, 0.33, 0.33]
print("dejando uno fuera", fuera.round(2).tolist())      # -> [0.5, 1.0, 0.5, 0.5, 0.5, 0.0]
```

```python verificable
import pandas as pd

# Categoria frecuente (100 filas) y categoria rara (4 filas).
df = pd.DataFrame({"cat": ["A"] * 100 + ["B"] * 4,
                   "y": [1] * 60 + [0] * 40 + [1, 1, 1, 0]})

prior = df["y"].mean()
g = df.groupby("cat")["y"].agg(["count", "mean"])
m = 10   # fuerza del suavizado: cuantas filas virtuales del prior se anaden

# El suavizado arrastra la categoria con pocos datos hacia la media global.
suave = (g["count"] * g["mean"] + m * prior) / (g["count"] + m)

print(f"media global (prior)  {prior:.2f}")                  # -> 0.61
print("medias crudas       ", g["mean"].round(2).to_dict())  # -> {'A': 0.6, 'B': 0.75}
print("medias suavizadas   ", suave.round(2).to_dict())      # -> {'A': 0.6, 'B': 0.65}
```

## Errores típicos

- **Codificar como ordinal algo que no tiene orden.** Ciudad, marca, sector o país con números
  1, 2, 3 meten distancias falsas en cualquier modelo que use distancias o coeficientes
  lineales. Si la categoría no tiene orden real, va one-hot o target encoding.
- **Target encoding calculado sobre todo el conjunto.** `df.groupby("cat")["y"].mean()` y
  `map` sobre toda la tabla es [[fuga-de-datos|fuga de datos]] garantizada: cada fila aporta su
  propio objetivo a su propia variable. Y si luego validas con
  [[validacion-cruzada|validación cruzada]], la puntuación sale espectacular y en producción se
  desmorona.
- **Target encoding sin suavizar en categorías raras.** Una categoría con 2 filas y media 1,0
  se codifica como 1,0, y el modelo la trata igual que una categoría con 10.000 filas y media
  1,0. Con `m` entre 5 y 100 la categoría rara se va a la media global, que es lo honesto.
- **One-hot con cardinalidad alta.** 8.000 códigos postales son 8.000 columnas, casi todas con
  un solo valor distinto de cero. La tabla se hincha, el entrenamiento se ralentiza y el
  sobreajuste aparece solo. Agrupa las categorías raras, usa frecuencia o pasa a target
  encoding.
- **Dejar fuera una categoría que sí aparece en producción.** Si el codificador solo conoce las
  categorías vistas en entrenamiento, una categoría nueva produce todo ceros (one-hot) o un
  error (ordinal). Deja una clase «otros» explícita y decide qué valor le das.
- **Estandarizar o escalar las columnas resultantes.** Un one-hot estandarizado deja de ser un
  0/1 legible y, si la categoría es rara, su desviación típica es casi cero y el valor se
  dispara. Las binarias no se tocan.

:::practica
enunciado: Una categoría tiene 5 filas con media del objetivo 0,80; otra tiene 200 filas con media 0,62; la media global es 0,60. Con suavizado m = 20, calcula las dos codificaciones y decide si la categoría rara se puede usar tal cual.
pista: La fórmula pondera la media de la categoría por su número de filas y la global por m: con pocas filas, manda la global.
solucion: Rara: (5 · 0,80 + 20 · 0,60) / 25 = (4 + 12) / 25 = 0,64. Frecuente: (200 · 0,62 + 20 · 0,60) / 220 = (124 + 12) / 220 = 0,618. El suavizado arrastra la rara de 0,80 a 0,64, casi hasta la frecuente (0,62), así que ya no se puede separar como si fuera una regla segura: con 5 filas, aquel 0,80 era ruido.
:::

## Comprueba que lo sabes

:::quiz
p: Codificas una columna de 8.000 códigos postales con one-hot y el modelo sobreajusta. ¿Cuál es la causa más directa?
o: Que el one-hot introduce un orden artificial entre códigos postales
o: Que cada categoría tiene muy pocas filas y el modelo puede memorizar cada código con su propia columna
o: Que el one-hot no admite más de 100 categorías
a: 2
e: Con 8.000 columnas y unas pocas filas por columna, el modelo dispone de un parámetro libre por código postal: memoriza en vez de generalizar. El one-hot no inventa orden (eso lo hace la codificación ordinal) y no tiene ningún límite de categorías.
:::

:::quiz
p: Una categoría aparece 3 veces en el entrenamiento con media del objetivo 1,00, y la media global es 0,20. ¿Qué hace el target encoding con suavizado `m = 10`?
o: La deja en 1,00, porque es la media real observada
o: La baja a (3 · 1,00 + 10 · 0,20) / 13 = 0,38, porque 3 observaciones no bastan para fiarse
o: La sube a 0,50 para no castigar a las categorías pequeñas
a: 2
e: El suavizado pondera la media de la categoría por su número de filas y la media global por `m`. Con 3 filas frente a 10 virtuales, manda la media global. Dejarla en 1,00 es precisamente lo que hace que un árbol separe esa categoría como si fuera una regla segura.
:::

:::trampa
El target encoding es tan potente que muchas competiciones se ganan con él y se pierden en
producción. Antes de darlo por bueno, comprueba que la variable codificada no predicta la
etiqueta por encima de lo razonable y repite la validación con la codificación calculada dentro
de cada pliegue.
:::
