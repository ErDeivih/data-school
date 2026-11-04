---
id: vectorizacion
titulo: Vectorización
fase: 3
nivel: intermedio
rutas: [core, de, ds]
prerequisitos: [numpy-fundamentos, numpy-broadcasting]
tags: [rendimiento, numpy, pandas]
resumen: Sustituir los bucles por operaciones sobre el array entero: máscaras booleanas, where y agregaciones por grupo, sin recorrer fila a fila en Python.
fuentes: ["Harris et al. (2020), 'Array programming with NumPy', Nature", "McKinney (2017), 'Python for Data Analysis'"]
---

## En una frase

Vectorizar es escribir la operación sobre la columna entera en vez de sobre cada fila, de modo
que el bucle se ejecute en código compilado: el bucle no desaparece, cambia de idioma.

## La idea

Imagina un supermercado con dos formas de cobrar. En la primera, el cajero saca un producto de
la cesta, mira el precio en el catálogo, lo suma a mano en un papel y repite. En la segunda, pasa
todos los productos por el lector y el sistema calcula el total. El número de operaciones
aritméticas es el mismo, pero en la segunda nadie está tomando decisiones producto a producto.

En Python, un bucle paga un peaje por cada elemento: crear un objeto, comprobar tipos, llamar a
métodos, actualizar contadores de referencia. Ese peaje domina el tiempo total. Cuando escribes
`precios * 1.21`, NumPy hace un bucle en C sobre posiciones de memoria consecutivas: mismo
cálculo, sin peaje.

Vectorizar no es solo «usar NumPy». Es una forma de traducir la lógica:

- Un `if` dentro del bucle se convierte en una **máscara booleana** o en `np.where`.
- Un contador se convierte en `.sum()` sobre una comparación, porque `True` vale 1.
- Un `for` que acumula por grupos se convierte en `np.bincount` o en un `groupby` de Pandas.
- Un `for` con dos ramas se convierte en `np.select` (o en un `merge` con una tabla de reglas).

El límite está en la memoria: cada operación intermedia crea un array del tamaño de la entrada.
Una cadena de cinco operaciones sobre 10 millones de `float64` puede reservar medio giga antes de
llegar al resultado. Cuando eso importa, se escribe en el sitio (`x += 1`, `out=`) o se trocea.

Y hay un segundo límite, más importante: **solo se vectoriza lo que cabe en memoria**. Si tus
datos no caben, la herramienta no es un truco de NumPy, es [[polars]] o un motor que procese por
bloques (ver [[duckdb-y-analitica-local]]).

## Definición formal

Sea `x = (x₁, …, xₙ)` un array y `m` una **máscara booleana** de la misma forma, donde `mᵢ` es
`True` o `False`:

- **Recuento:** el número de elementos que cumplen la condición es `Σᵢ mᵢ`, porque en la
  aritmética de NumPy `True` es 1 y `False` es 0. Se escribe `(x > 0).sum()`.
- **Media condicional:** la media de los elementos seleccionados es
  `Σᵢ xᵢ · mᵢ / Σᵢ mᵢ`, que se escribe `x[m].mean()`.
- **Selección:** `x[m]` devuelve un array **nuevo** con los elementos donde la máscara es
  verdadera.
- **Elección elemento a elemento:** `np.where(m, a, b)` devuelve `aᵢ` si `mᵢ` y `bᵢ` si no.
  Es una expresión, no un flujo: las dos ramas se calculan enteras.
- **Agregación por grupo:** con las etiquetas de grupo `g` codificadas como enteros `0…k−1`,
  `np.bincount(g, weights=x)` calcula de una vez

:::formula
y_t = Σ_i x_i · [g_i = t]          para t = 0, 1, …, k−1
:::

donde `[g_i = t]` vale 1 si la observación `i` pertenece al grupo `t` y 0 en caso contrario.
Vocabulario que aparece en el código:

- **Máscara** — array de `bool` de la misma forma que los datos.
- **`np.select(condiciones, opciones, default=…)`** — el `if`/`elif`/`else` de varios niveles
  en versión array: recorre las condiciones en orden y aplica la primera que se cumple.
- **`np.clip(x, mínimo, máximo)`** — recorta los valores fuera de rango, sin bucles.
- **Temporal** — cada array intermedio que se crea y se descarta dentro de una expresión.

## Ejemplo

Cinco precios de cierre: `100, 102, 98, 105, 103`. Los retornos simples entre un día y el
siguiente son la diferencia de precios dividida por el precio anterior, y eso es exactamente lo
que hace `np.diff`:

```
precios      = [100, 102,  98, 105, 103]
diferencias  = [     2,   -4,   7,  -2]
divisor      = [100, 102,  98, 105]        (el precio anterior, precios[:-1])
retornos     = [0,02, -0,0392, 0,0714, -0,019]
```

De ahí salen las cuentas sin un solo `if`:

- Días con subida: `(retornos > 0).sum()` = **2** de 4. La media de esos dos retornos positivos
  es (0,02 + 0,0714) / 2 = **0,0457**.
- Señal de entrada: `np.where(retornos > 0, 1, −1)` da `[1, −1, 1, −1]`.

El mismo patrón con grupos. Con seis facturas repartidas en tres clientes codificados como
`0, 0, 1, 1, 1, 2` y estos importes:

```
grupos   = [0, 0, 1, 1, 1, 2]
importes = [1, 2, 3, 4, 5, 6]
```

`np.bincount(grupos, weights=importes)` da `[3, 12, 6]`: 1 + 2 para el cliente 0, 3 + 4 + 5 para
el 1 y 6 para el 2. Y `np.bincount(grupos)` da `[2, 3, 1]`, el número de facturas de cada uno.
Dos líneas en lugar de un diccionario y un bucle con `setdefault`.

## Código

```python verificable
import numpy as np

precios = np.array([100.0, 102.0, 98.0, 105.0, 103.0])
retornos = np.diff(precios) / precios[:-1]     # el bucle real ocurre en C

print(np.round(retornos, 4).tolist())          # -> [0.02, -0.0392, 0.0714, -0.019]
print(int((retornos > 0).sum()), "subidas de", retornos.size)   # -> 2 subidas de 4
print(np.round(retornos[retornos > 0].mean(), 4))               # -> 0.0457

senal = np.where(retornos > 0, 1, -1)          # sin if dentro de un bucle
print(senal.tolist())                          # -> [1, -1, 1, -1]
```

```python verificable
import numpy as np

grupos = np.array([0, 0, 1, 1, 1, 2])          # cliente codificado como entero 0..2
importes = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

# Suma por grupo en una sola pasada: el equivalente vectorizado de un bucle con diccionario
print(np.bincount(grupos, weights=importes).tolist())   # -> [3.0, 12.0, 6.0]
print(np.bincount(grupos).tolist())                     # -> [2, 3, 1]
```

```python verificable
import numpy as np

x = np.array([-5.0, -0.5, 0.5, 5.0])

# Varias condiciones en orden: la primera que se cumple manda
etiquetas = np.select([x < -1, x < 1], ["bajada fuerte", "plana"], default="subida fuerte")
print(etiquetas.tolist())   # -> ['bajada fuerte', 'plana', 'plana', 'subida fuerte']

# Recortar valores extremos sin bucles
print(np.clip(x, -1.0, 1.0).tolist())   # -> [-1.0, -0.5, 0.5, 1.0]
```

## Errores típicos

- **`df.apply(..., axis=1)` para hacer aritmética entre columnas.** Recorrer filas construye un
  objeto Series por fila: es la forma más habitual de que un análisis de 200.000 filas tarde
  minutos en lugar de segundos. Si la operación se puede escribir con columnas enteras
  (`df["a"] * df["b"]`), escríbela así; `axis=1` solo para lógica que de verdad necesita la fila
  completa, y mejor aún con `np.select`.
- **`iterrows()` o `for i in range(len(df))`.** Además de lento, `iterrows()` convierte cada fila
  a un objeto con un dtype común, así que un entero puede aparecer como `1.0`. Usa las columnas o
  `itertuples()` si no hay más remedio.
- **Acumular con `np.append` o `pd.concat` dentro de un bucle.** Cada iteración copia todo lo
  anterior. El coste pasa de O(n) a O(n²) y con 100.000 filas se nota en minutos.
- **Creer que `np.where` solo evalúa la rama que toca.** Evalúa las dos completas. En
  `np.where(x != 0, 1 / x, 0)` la división se calcula (y avisa con un `RuntimeWarning`) antes de
  elegir. La alternativa es `np.divide(1, x, out=np.zeros_like(x), where=x != 0)`.
- **Llamar a `np.vectorize` pensando que acelera.** No es una vectorización: es un bucle de
  Python con otro nombre. Sirve para escribir una línea más corta, no para ganar velocidad.
- **Vectorizar sin mirar la memoria.** Una cadena de operaciones crea un temporal por paso. Con
  arrays grandes, suma en el sitio (`x += 1`), usa `out=` o procesa por trozos; si no, el
  programa muere por memoria justo cuando iba rápido.

:::practica
enunciado: Con `precios = [50, 55, 52, 58]`, escribe el código que calcula los tres retornos simples, los retornos negativos, cuántos días suben y una señal que valga 1 si el retorno supera el 5 % y -1 en caso contrario. Todo sin bucles.
pista: La diferencia y el divisor salen de `np.diff` y `precios[:-1]`; la máscara booleana sirve a la vez para seleccionar y para contar.
solucion: `ret = np.diff(p) / p[:-1]` da `[0.1, -0.0545, 0.1154]` redondeado a 4 decimales. La máscara `ret < 0` selecciona `-0.0545` y `ret[ret < 0]` devuelve ese único valor. Hay 2 días que suben: `(ret > 0).sum()` vale 2. Con `np.where(ret > 0.05, 1, -1)` la señal es `[1, -1, 1]`, porque solo dos retornos pasan del 5 %.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cómo cuentas cuántos elementos de un array `precios` superan 100 sin escribir un bucle?
o: `precios.sum() > 100`
o: `(precios > 100).sum()`
o: `len(precios > 100)`
a: 2
e: `precios > 100` devuelve una máscara booleana y sumarla cuenta los `True`, porque valen 1. `precios.sum() > 100` suma los precios, y `len` de un array booleano daría el total de elementos, no los que cumplen la condición.
:::

:::quiz
p: `np.bincount([0, 1, 1, 2], weights=[5, 1, 2, 3])` devuelve `[5, 3, 3]`. ¿Qué representa cada posición?
o: El valor máximo de cada grupo
o: La suma de los pesos de las observaciones de cada grupo, y 0 si el grupo no aparece
o: La media de los pesos de cada grupo
a: 2
e: La posición `t` del resultado acumula los pesos de todas las observaciones con etiqueta `t`: en 0 solo el 5, en 1 el 1 + 2 y en 2 el 3. Sin `weights`, contendría el número de observaciones de cada grupo.
:::

:::quiz
p: ¿Por qué `np.where(x > 0, np.log(x), 0)` puede dar un aviso aunque el resultado final sea correcto?
o: Porque `np.where` evalúa las dos ramas completas antes de elegir, así que `np.log` se aplica también a los valores no positivos
o: Porque `np.log` no acepta arrays
o: Porque `np.where` solo admite dos argumentos
a: 1
e: `np.where` es una expresión, no un `if`: calcula las dos ramas enteras y luego escoge elemento a elemento. Para evitar el cálculo inútil se usa `np.log(x, out=np.zeros_like(x), where=x > 0)`.
:::

:::truco
Antes de optimizar, mide. Si un `apply` tarda 4 segundos y la versión con columnas tarda 40
milisegundos, la discusión está resuelta; si el programa pasa el 90 % del tiempo leyendo un
CSV, vectorizar la aritmética no te va a salvar (ver [[rendimiento-y-perfilado]]).
:::
