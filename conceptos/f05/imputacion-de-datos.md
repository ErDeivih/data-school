---
id: imputacion-de-datos
titulo: Imputación de datos
fase: 5
nivel: intermedio
rutas: [ds, de]
prerequisitos: [missing-data, pandas-fundamentos]
tags: [nulos, preprocesamiento, pandas]
resumen: Rellenar los huecos con media, mediana, modelo o KNN cambia la distribución; casi siempre hay que dejar además una marca de que el dato faltaba.
fuentes: ["Little y Rubin (2019), 'Statistical Analysis with Missing Data'", "van Buuren (2018), 'Flexible Imputation of Missing Data'"]
---

## En una frase

Imputar es rellenar los valores que faltan con una estimación, y toda estimación es una
suposición: elegir el método según por qué falta el dato y dejar constancia de que faltaba es
la mitad del trabajo.

## La idea

Imagina una clase de 10 alumnos y el día del examen faltan 3. Ponerles la nota media de los
otros 7 es defendible, pero tiene consecuencias: nadie saca un 3 y la clase parece más
homogénea de lo que era. Ponerles la mediana es más prudente si las notas están sesgadas.
Y dejar la casilla vacía también cuesta: cualquier media posterior se calcula sobre 7 en vez
de sobre 10, y si los que faltaron son justo los que peor lo llevaban, el resultado está
sesgado sin que nadie lo note.

Ese es el punto central: **imputar no es limpiar, es modelar**. Cuando rellenas un hueco estás
afirmando algo sobre esa fila, y esa afirmación puede ser falsa. Por eso el primer paso nunca
es elegir el método, sino entender **por qué falta**. La distinción clásica tiene tres casos:

- **Falta completamente al azar (MCAR).** El hueco no depende de nada: se rompió un sensor al
  azar. Borrar las filas afectadas no sesga nada, solo pierdes potencia estadística.
- **Falta al azar (MAR).** El hueco depende de otras columnas que sí observas: los ingresos
  faltan más entre los autónomos, y tú sabes quién es autónomo. Aquí un modelo que use esas
  columnas puede reconstruir el valor razonablemente.
- **Falta no al azar (MNAR).** El hueco depende del propio valor que falta: la gente con
  ingresos muy altos no los declara. Ningún método puede arreglar esto desde dentro de los
  datos; hay que decirlo y acotar el sesgo.

Con eso claro, los métodos se ordenan de menos a más esfuerzo: borrar filas o columnas,
rellenar con un estadístico (media, mediana, moda), rellenar con un vecino parecido (KNN),
rellenar con un modelo entrenado con el resto de columnas (regresión, imputación múltiple).

:::figura
fichero: imputacion-que-cambia-el-relleno
pie: Los tres paneles enseñan lo que ninguna fórmula dice a primera vista. Arriba, rellenar los tres huecos de ingresos con la media (2.825 €) inventa tres sueldos que solo uno de los nueve observados alcanza, el de 9.500 €, porque los otros cinco están por debajo; con la mediana (1.550 €) el relleno es más creíble. Abajo a la izquierda, la varianza muestral cae de 10,00 a 6,67 solo por meter el mismo número dos veces: se pierde un tercio de la dispersión sin borrar ni un dato real. A la derecha, KNN copia de los vecinos parecidos (con `k = 1` da 12,0 y con `k = 2` da 11,0), no de la media de la columna, que es 51,8 y no se parece a ninguna fila del grupo. Ninguna de las tres cosas se ve en el resultado final: hay que mirarlas antes de dar la tabla por buena.
fuente: figuras/imputacion-de-datos-1.py
:::

Hay una pieza que casi todo el mundo olvida: la **marca de ausencia**. Si los ingresos
faltan sobre todo en un segmento concreto, saber *que* faltan es información predictiva de
primera. Añadir una columna binaria «este valor estaba vacío» es gratis y muchas veces mejora
el modelo más que la propia imputación.

## Definición formal

Sea una tabla de `n` filas y `p` columnas, con `xᵢⱼ` el valor de la fila `i` en la columna
`j`. Definimos el indicador de observación `rᵢⱼ = 1` si el valor está presente y `rᵢⱼ = 0` si
falta. La **marca de ausencia** es su complementario, `1 − rᵢⱼ`.

Los estimadores más habituales, escrito `x̂ᵢⱼ` el valor imputado:

- **Media:** `x̂ᵢⱼ = x̄ⱼ`, la media de los valores observados de esa columna.
- **Mediana:** `x̂ᵢⱼ = mediana(xⱼ | rᵢⱼ = 1)`. Robusta frente a valores extremos, y por eso es
  la opción por defecto en variables con cola larga como ingresos o tiempos de espera.
- **Moda:** el valor más frecuente. Es la única opción sensata en una columna categórica.
- **Regresión:** `x̂ᵢⱼ = β̂₀ + Σₖ β̂ₖ · zᵢₖ`, donde `zᵢₖ` son las otras columnas de la fila `i`
  y `β̂` se estima solo con las filas donde `xᵢⱼ` está observado.
- **KNN:** la media de los `k` vecinos más cercanos medidos en las columnas que sí están
  completas en ambas filas.

:::formula
x̂ᵢⱼ = x̄ⱼ  (media de los observados)   ·   x̂ᵢⱼ = β̂₀ + Σₖ β̂ₖ · zᵢₖ  (modelo)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `n` | Número de filas de la tabla | filas | No cambia el valor imputado, pero con `n` pequeño la media y la mediana son estimaciones ruidosas y el hueco se rellena peor |
| `p` | Número de columnas | columnas | Más columnas dan más información al modelo de imputación, pero también más huecos por fila: con un 5 % de nulos en 20 columnas puedes perder la mitad de las filas si borras |
| `xᵢⱼ` | El valor de la fila `i` en la columna `j` | las de la columna | Es la incógnita cuando `rᵢⱼ = 0`; el objetivo de todo el método es estimarla |
| `rᵢⱼ` | Indicador de observación: vale 1 si el dato está y 0 si falta | 0 o 1 | Sube la proporción de datos disponibles; si baja mucho, cualquier estadístico se calcula sobre muy pocos casos |
| `1 − rᵢⱼ` | La marca de ausencia que se añade como columna | 0 o 1 | Es gratis y muchas veces mejora el modelo más que la imputación: sin ella el modelo no distingue «vale 1.550 porque lo tiene» de «vale 1.550 porque lo he inventado» |
| `x̂ᵢⱼ` | El valor imputado y puesto en el hueco | las de la columna | Con la media queda siempre igual a `x̄ⱼ`; con la mediana, en el centro de la columna. Los dos son deterministas: el mismo hueco recibe siempre el mismo número |
| `x̄ⱼ` | Media de los valores observados de la columna `j` | las de la columna | Se arrastra hacia los extremos, así que en columnas sesgadas rellena con un valor que casi nadie tiene |
| `k` | Número de vecinos que usa KNN | vecinos | Con `k = 1` el hueco copia al vecino más cercano (en el ejemplo, 12,0); con `k = 2` es la media de los dos (11,0). Subirlo alarga el cálculo y suaviza, pero con `k` muy grande acaba pareciéndose a la media global |
| `m` | Número de juegos completos de la imputación múltiple (MICE) | juegos | Sube el coste y también la honestidad: con `m = 1` finges que el valor imputado es exacto, y la varianza final sale demasiado pequeña |
:::

Dos propiedades que conviene tener escritas, porque explican casi todas las trampas:

1. **La imputación por media no cambia la media y reduce la varianza.** Como metes el mismo
   número en todos los huecos, esos valores no aportan dispersión. La varianza muestral baja,
   y la correlación con otras columnas también se diluye.
2. **La imputación por media es determinista, así que subestima la incertidumbre.** Si
   repitieras el estudio con otra muestra, los huecos se habrían rellenado con otro número.
   La imputación múltiple (MICE) genera `m` juegos de datos completos con algo de ruido y
   combina los resultados, precisamente para no fingir que el valor imputado es exacto.

## Ejemplo

Nueve personas declaran sus ingresos mensuales; tres no contestan y una es un valor extremo:

```
1200  1350  1500  1600  1800  (falta)  (falta)  (falta)  9500
```

- Media de los seis que responden: 16.950 / 6 = **2.825 €**.
- Mediana de los seis: (1.500 + 1.600) / 2 = **1.550 €**.

Si imputas por la media, cada uno de los tres huecos se rellena con 2.825 €, una cifra mayor
que la de cinco de los nueve. La media global se queda igual (2.825), que es justo el problema:
parece que no has tocado nada, pero acabas de inventar tres ingresos altos. Si imputas por la
mediana, la media final baja a 2.400 € y los valores inventados son más creíbles.

El segundo efecto se ve en la varianza. Con una columna de cinco valores completos
(10, 12, 14, 16, 18) y dos huecos:

- Varianza de los cinco completos: **10,00**.
- Varianza tras imputar los dos huecos con la media (14): **6,67**.

Has perdido un tercio de la dispersión sin tocar un solo dato real. Cualquier modelo que
dependa de la escala de esa variable notará esa compresión.

## Código

```python verificable
import numpy as np

# Ingresos de 9 personas: 3 sin declarar (NaN) y un valor extremo de 9.500.
ingresos = np.array([1200.0, 1350.0, 1500.0, 1600.0, 1800.0,
                     np.nan, np.nan, np.nan, 9500.0])

media, mediana = np.nanmean(ingresos), np.nanmedian(ingresos)
print(f"media de los que responden   {media:>7.0f}")    # -> 2825
print(f"mediana de los que responden {mediana:>7.0f}")  # -> 1550

# Rellenar por la media deja la media intacta pero inventa 3 ingresos altos.
relleno_media = np.where(np.isnan(ingresos), media, ingresos)
relleno_mediana = np.where(np.isnan(ingresos), mediana, ingresos)
print(f"media tras imputar con media   {relleno_media.mean():.0f}")    # -> 2825
print(f"media tras imputar con mediana {relleno_mediana.mean():.0f}")  # -> 2400
```

:::claves
- `np.nanmean` y `np.nanmedian` **saltan** los `NaN` (`nan` = «not a number», el hueco). Sus primas sin `nan` (`np.mean`, `np.median`) devuelven `nan` en cuanto hay un solo hueco, y ese `nan` se propaga silenciosamente a todo lo que se calcule después. Si ves un resultado `nan` sin explicación, busca el hueco.
- `np.where(condicion, valor_si_verdadero, valor_si_falso)` devuelve un array **nuevo**; no modifica `ingresos`. Comprueba que `ingresos` sigue teniendo sus tres `nan` después de la línea. Para escribir encima hace falta `ingresos[faltan] = media`, que sí cambia el original y no devuelve nada.
- Ojo con el orden de los argumentos: `np.where(cond, a, b)` recibe **las dos** ramas ya calculadas. Con `media` y `mediana` es igual, pero con una función cara o con una división que pueda dar error, la rama que no se usa también se calcula. La versión perezosa es pasar la máscara a la propia operación: `np.divide(1, x, out=salida, where=cond)` solo calcula donde la condición se cumple. `np.copyto(destino, 1 / x, where=cond)` no sirve para eso: el `1 / x` se calcula igual, en todos los elementos.
- `np.isnan(ingresos)` devuelve un array de booleanos de la misma longitud, y por eso se puede usar como máscara. No sirve para comparar: `ingresos == np.nan` siempre da `False`, porque `nan` no es igual a nada, ni siquiera a sí mismo. Ese es el motivo de que exista `np.isnan` y de que `df["col"] == np.nan` no filtre nada en pandas.
- La media no cambia al imputar con la media (sigue en 2.825) y eso es justo el problema: parece que no has tocado nada, pero acabas de inventar tres ingresos altos. La mediana sí cambia la media final (baja a 2.400), y ese cambio es la señal de que has metido valores nuevos donde no había.
- `f"{media:>7.0f}"` formatea solo el texto que se imprime: el `>7` rellena por la izquierda hasta siete caracteres y el `.0f` redondea a cero decimales. El número que sigue en `media` no ha cambiado, así que no uses la cifra impresa para volver a calcular. Si necesitas el valor redondeado de verdad, usa `float(round(media, 0))`: `round` con decimales sobre un `np.float64` sigue devolviendo `np.float64`, y solo `round(x)` sin segundo argumento devuelve un `int` de Python.
:::

```python verificable
import numpy as np

# Meter el mismo valor en todos los huecos encoge la varianza: no aportan dispersion.
datos = np.array([10.0, 12.0, 14.0, 16.0, 18.0, np.nan, np.nan])
relleno = np.where(np.isnan(datos), np.nanmean(datos), datos)

# ddof=1 porque estimamos la media a partir de la propia muestra.
print(f"varianza de los completos {np.nanvar(datos, ddof=1):.2f}")  # -> 10.00
print(f"varianza tras imputar     {relleno.var(ddof=1):.2f}")      # -> 6.67
print(f"desviacion tras imputar   {relleno.std(ddof=1):.2f}")      # -> 2.58
```

```python verificable
import numpy as np
from sklearn.impute import KNNImputer

# Dos grupos de valores muy separados; la fila con el hueco esta en el grupo bajo.
X = np.array([[1.0, 10.0], [2.0, 12.0], [3.0, np.nan], [8.0, 90.0], [9.0, 95.0]])

# KNN usa los dos vecinos mas parecidos (10 y 12), no la media de toda la columna.
imputado = KNNImputer(n_neighbors=2).fit_transform(X)[2, 1]
print(f"imputado por KNN {imputado:.1f}")            # -> 11.0
print(f"media global     {np.nanmean(X[:, 1]):.1f}")  # -> 51.8
```

## Errores típicos

- **Imputar con la media en variables sesgadas.** Ingresos, precios, tiempos de espera y
  visitas tienen cola larga: la media está por encima de la mayoría y rellena los huecos con
  un valor que casi nadie tiene. Usa la mediana, o mejor un modelo que use el resto de
  columnas.
- **Imputar y no dejar la marca de ausencia.** Si el hueco no es MCAR, que el dato falte es
  información. Sin la columna indicadora, el modelo no puede distinguir «ingresos = 1.550
  porque los tiene» de «ingresos = 1.550 porque lo he inventado». Añade siempre `1 − rᵢⱼ` como
  variable, sobre todo si la ausencia supera el 5 % de la columna.
- **Imputar antes de dividir en entrenamiento y prueba.** Si calculas la media con todo el
  conjunto y luego divides, la media contiene información del conjunto de prueba. Es
  [[fuga-de-datos|fuga de datos]] en estado puro y hay que ajustar el imputador solo con
  entrenamiento. Cualquier [[pipelines-de-ml|pipeline]] razonable lo hace por ti.
- **Confundir «cero» con «falta».** Un 0 en el número de compras es un dato, no un hueco.
  Rellenar con 0 cuando el 0 no existe en el dominio (peso, altura, facturación) inventa un
  valor imposible y suele ser peor que cualquier media.
- **Usar la variable objetivo para imputar variables de entrada.** Rellenar el gasto que falta
  con una función de si el cliente se dio de baja es fuga directa: en producción no tendrás esa
  etiqueta para las filas nuevas.
- **Aplicar KNN sin escalar.** La distancia euclídea la domina la columna de mayor rango: si
  una variable va de 0 a 100.000 y otra de 0 a 1, los vecinos se eligen solo con la primera.
  Escala antes con [[escalado-y-transformacion|escalado]] y comprueba que los vecinos tienen
  sentido de negocio.

:::practica
enunciado: Una columna tiene seis valores completos: 20, 24, 28, 32, 36, 40. Hay dos huecos y los rellenas con la media. Calcula la varianza muestral antes y después y decide qué has perdido.
pista: Calcula la varianza con los seis observados y luego con los ocho valores, sabiendo que los dos imputados valen exactamente la media.
solucion: Media = 180 / 6 = 30. Desviaciones: −10, −6, −2, 2, 6, 10; suma de cuadrados 280; varianza = 280 / 5 = 56. Con los dos huecos imputados a 30: n = 8 y varianza = 280 / 7 = 40. Pierdes 16 puntos, el 28,6 % de la dispersión, sin tocar un dato real, y los dos valores nuevos son iguales a la media: deja además la marca de ausencia.
:::

## Comprueba que lo sabes

:::quiz
p: Una columna de ingresos tiene un 20 % de huecos y una cola larga con valores muy altos. ¿Qué imputación simple es la menos mala?
o: La media, porque usa todos los datos disponibles
o: La mediana, porque no la arrastran los valores extremos
o: Cero, para que el modelo sepa que no hay dato
a: 2
e: Con cola larga la media está por encima de la mayoría, así que rellena los huecos con un valor que casi nadie tiene. La mediana está en el centro real de la distribución. El cero no es un valor del dominio de los ingresos: introduce una observación imposible.
:::

:::quiz
p: ¿Por qué imputar por la media reduce la varianza de la columna?
o: Porque los valores imputados son todos iguales y no aportan dispersión
o: Porque la media siempre es menor que la desviación típica
o: Porque se eliminan las filas con valores extremos
a: 1
e: Al repetir el mismo número en cada hueco, esos valores no se separan de la media y la suma de cuadrados apenas crece mientras `n` aumenta. La varianza muestral baja. No se borra ninguna fila ni tiene nada que ver con el tamaño de la media.
:::

:::trampa
Borrar todas las filas con algún hueco es también una imputación, y la más peligrosa porque no
deja rastro. Si los huecos no son MCAR, borrar elimina sistemáticamente un tipo de caso: con
un 5 % de nulos repartidos en 20 columnas puedes perder la mitad de la tabla.
:::
