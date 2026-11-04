---
id: ingenieria-de-features
titulo: Ingeniería de variables
fase: 5
nivel: avanzado
rutas: [ds, de, quant]
prerequisitos: [pandas-fundamentos, pandas-agrupaciones-y-joins, series-temporales-componentes]
tags: [variables, ventanas, ratios, dominio]
resumen: Construir variables que resumen lo que sabes del problema: cocientes, diferencias, ventanas pasadas y agregados por grupo, siempre mirando solo hacia atrás.
fuentes: ["Zheng y Casari (2018), 'Feature Engineering for Machine Learning'", "Kuhn y Johnson (2019), 'Feature Engineering and Selection'"]
---

## En una frase

La ingeniería de variables es escribir a mano, en forma de columna, el conocimiento que tienes
del problema, para que el modelo no tenga que adivinarlo a partir de los datos crudos.

## La idea

Un modelo no ve el mundo: ve la tabla que le das. Si le pasas «ingresos» y «deuda» por separado,
una regresión lineal solo puede sumarlas con pesos. Pero la pregunta que de verdad importa suele
ser si la deuda es sostenible **en relación con los ingresos**, y eso es un cociente, no una
suma. Un árbol, por su parte, solo puede cortar por umbrales: con «visitas» y «compras» jamás
va a descubrir por sí solo la tasa de conversión, porque la tasa no está en ninguna de las dos
columnas.

Piénsalo como cocinar. Los datos crudos son los ingredientes: harina, huevos, azúcar. El modelo
es el horno, y el horno no bate. Si le metes los ingredientes sin batir, sale una cosa; si bates
antes, sale otra. Batir es ingeniería de variables, y el conocimiento del negocio es la receta.

Las familias que más rendimiento dan, por orden de utilidad práctica:

- **Agregados por grupo.** «Gasto medio de este cliente en los últimos 90 días», «número de
  pedidos de esta tienda». Es lo que convierte una tabla de eventos en una tabla de entidades.
  La clave es que el agregado se calcule **solo con lo anterior** al instante que estás
  prediciendo.
- **Ventanas móviles hacia atrás.** Media, máximo, mínimo, desviación de los últimos `k`
  periodos. Capturan nivel y volatilidad reciente.
- **Cocientes, diferencias y variaciones.** Deuda/ingresos, precio/beneficio, variación
  porcentual respecto a hace un mes. Suelen ser mucho más estables entre mercados y escalas que
  los valores absolutos.
- **Interacciones.** El producto de dos variables, o su división. Sirven para dar a un modelo
  lineal la capacidad de capturar un efecto conjunto sin partir los datos en trozos.
- **Variables de calendario y de ciclo de vida.** Día de la semana, mes, días desde el alta del
  cliente, días desde la última compra. Baratas y sorprendentemente potentes.
- **Rezagos.** El valor de ayer, el de hace una semana. En series con
  [[autocorrelacion-acf-pacf|autocorrelación]] son la primera variable que hay que probar.

La regla que gobierna todo esto es la **dirección de la mirada**: cada variable debe poder
calcularse con la información disponible en el momento de la predicción, y con nada más. Una
media móvil centrada, un máximo de todo el histórico o un agregado calculado con la tabla
completa son formas distintas de mirar al futuro, y todas inflan las métricas de validación.

## Definición formal

Con una serie temporal `x₁, x₂, …, xT` y un horizonte de ventana `k`:

- **Rezago:** `Lₖ(t) = x_{t−k}`. El valor de `k` periodos antes.
- **Media móvil hacia atrás:** `MAₖ(t) = (1/k) · Σ_{i=1..k} x_{t−i}`. Fíjate en el sumatorio:
  va de `t−1` a `t−k`, **nunca incluye `x_t`**. Ese detalle es la diferencia entre una variable
  útil y una fuga.
- **Desviación móvil:** `SDₖ(t) = √( (1/(k−1)) · Σ_{i=1..k} (x_{t−i} − MAₖ(t))² )`.
- **Cociente:** `r(t) = a(t) / b(t)`. Solo tiene sentido si `b(t)` está lejos de cero; si puede
  serlo, usa `(a − b)/(a + b)` o añade una constante.
- **Media acumulada por grupo:** para cada entidad `g`, `E(t) = (1/n) · Σ x_s`, sumando los
  periodos `s < t` de esa entidad, y con `n` el número de esos periodos anteriores. Es la media
  de todo lo anterior de ese cliente, no de todo el histórico completo.

:::formula
MAₖ(t) = (1/k) · Σ_{i=1..k} x_{t−i}       ventana = pasado, nunca incluye x_t
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `x_t` | El valor observado en el instante `t` | las de la serie | Con una ventana fija, cada valor nuevo pesa `1/k` en la media: una sola cifra disparatada mueve menos el resultado |
| `k` | El número de periodos que entran en la ventana | periodos (días, meses) | La variable se vuelve más suave y más lenta: reacciona menos a lo reciente. Con `k` muy grande la media deja de describir el presente; con `k = 1` la variable es el valor de ayer y no resume nada |
| `MAₖ(t)` | La media de los `k` periodos anteriores a `t` | las de la serie | — (es el resultado) |
| `Σ_{i=1..k}` | La suma de los `k` valores anteriores, de `t−1` a `t−k` | las de la serie | Si el sumatorio llegara hasta `i = 0` incluiría `x_t` y la variable pasaría a contener la respuesta: eso es fuga, no información |
| `Lₖ(t)` | El rezago `k`: el valor de hace `k` periodos | las de la serie | Con más `k` la variable es más antigua y suele predecir peor, salvo que la serie tenga memoria muy larga |
| `r(t)` | El cociente `a(t) / b(t)` | adimensional | Es el resultado; su valor no cambia si multiplicas `a` y `b` por la misma constante, y por eso aguanta mejor los cambios de escala |
| `a(t)`, `b(t)` | Numerador y denominador del cociente | las de cada magnitud | Si `b(t)` se acerca a cero, `r` se dispara hacia el infinito y arrastra medias y escalados; comprueba el mínimo de `b` antes de dividir |
| `n` | Número de periodos anteriores de la entidad, en la media acumulada | periodos | Con `n` pequeño (cliente nuevo) la media es inestable: promedia dos o tres compras |
:::

:::figura
fichero: ingenieria-de-features-ventana-y-cociente
pie: A la izquierda, la media de 3 días del día 5 vale 130,0 si la ventana incluye el propio día 5 y 116,7 si solo mira atrás: la primera columna contiene la respuesta que quieres predecir, así que en producción no existiría. A la derecha, visitas y compras se solapan entre las dos clases, pero el cociente las separa sin un solo error: la información estaba en la relación, no en ninguna de las dos columnas.
fuente: figuras/ingenieria-de-features-1.py
:::

Tres propiedades que hay que comprobar antes de dar una variable por buena:

1. **Disponibilidad.** ¿Existiría este número en producción, en el instante exacto de la
   predicción, con la latencia real del sistema de origen? En finanzas, un dato que se publica
   con dos días de retraso no estaba disponible el día de la operación, por mucho que en la
   tabla tenga esa fecha.
2. **Estabilidad.** La distribución de la variable en entrenamiento y en producción debe
   parecerse. Una variable que se dispara cuando cambia un sistema de origen es una bomba de
   relojería; se vigila con [[monitorizacion-de-drift|la monitorización de deriva]].
3. **Aportación.** Una variable nueva que no mejora nada medible es coste puro: más columnas,
   más overfitting y más cosas que mantener. La criba se hace con
   [[seleccion-de-features|selección de variables]].

## Ejemplo

**Ventana con y sin desplazamiento.** Siete días de ventas:

```
100  120  90  140  160  130  110
```

El día 5 (índice 4) vendió 160. Para predecir ese día hay dos formas de calcular la media de 3
días, y solo una sirve:

- **Ventana sin desplazar**, `rolling(3)` en la fila 4: promedia los índices 2, 3 y 4, es decir
  (90 + 140 + 160) / 3 = **130,0**. Incluye el propio 160 que quieres predecir.
- **Ventana desplazada**, `shift(1)` antes del `rolling(3)`, en la fila 4: promedia los índices
  1, 2 y 3, es decir (120 + 90 + 140) / 3 = **116,7**. Solo pasado.

El mismo cálculo, dos columnas distintas, y solo la segunda es legítima. Ese desplazamiento de
una posición es la diferencia entre predecir y copiar.

**Cociente que ninguna columna tiene.** Ocho filas con visitas y compras:

```
visitas:  10  20  30  40   12  24  36  48
compras:   2   4   6   8    6  12  18  24
clase:     0   0   0   0    1   1   1   1
```

- Visitas medias: **25,0** en la clase 0 y **30,0** en la clase 1. Se solapan: hay filas de la
  clase 0 con 40 visitas y filas de la clase 1 con 12.
- Compras medias: **5,0** frente a **15,0**. También se solapan.
- Tasa de conversión (compras / visitas): **0,20** frente a **0,50**. Separa las dos clases sin
  un solo error.

Ninguna de las dos columnas originales contiene esa información; el cociente sí, porque es la
relación la que define el fenómeno.

**Agregado acumulado por cliente.** Para los importes de un cliente, la media de todo lo
anterior se calcula con `shift()` y `expanding()`: el primer registro no tiene pasado (queda
vacío) y a partir de ahí cada fila usa solo lo ya visto.

## Código

```python verificable
import pandas as pd

# Ventas diarias: la ventana de 3 dias debe mirar solo al pasado.
ventas = pd.Series([100, 120, 90, 140, 160, 130, 110], dtype=float)

sin_shift = ventas.rolling(3).mean()           # incluye el dia actual: no sirve como variable
con_shift = ventas.shift(1).rolling(3).mean()  # solo los 3 dias anteriores

print(f"dia 5: ventas {ventas[4]:.0f}, media sin shift {sin_shift[4]:.1f}, "
      f"con shift {con_shift[4]:.1f}")
# -> dia 5: ventas 160, media sin shift 130.0, con shift 116.7
```

:::claves
- `ventas.shift(1)` no desplaza el índice ni pierde la primera fila: la deja con `NaN` en la posición 0. Por eso el `rolling(3)` que va detrás tampoco da valor hasta la fila 3, y `con_shift[2]` sale nulo. Si rellenas esos `NaN` con 0, estás inventando un pasado que no existía.
- El orden de los dos métodos importa y no es intercambiable: `shift(1).rolling(3)` promedia las filas 1, 2 y 3 en la fila 4, pero `rolling(3).shift(1)` promedia las filas 2, 3 y 4 y **después** lo coloca en la fila 5. La primera es la que quieres; la segunda desplaza el resultado un día y usa el día que quieres predecir.
- `rolling(3).mean()` devuelve una `Series` nueva (con el mismo índice que `ventas`), no modifica el original. Si en vez de asignarla a una variable escribes `ventas.rolling(3).mean()` a secas, no pasa nada: el cálculo se tira.
- La ventana es de **filas**, no de tiempo. Con fechas desordenadas o con días que faltan, `rolling(3)` promedia las tres filas anteriores aunque entre ellas haya un salto de un mes. Para ventanas por tiempo hace falta `rolling("3D")` sobre un índice de fechas.
- `nan` se propaga: cualquier media que toque una fila vacía sale vacía. Compara cuántos nulos tiene `sin_shift` (2) y `con_shift` (3): esa fila de diferencia es la que el modelo no puede usar.
- El segundo bloque usa `df.groupby("convierte")[["visitas", "tasa"]].mean()`. Fíjate en el doble corchete: con `["visitas"]` el resultado tiene dos índices (`convierte` y la columna) y `g.loc[0, "visitas"]` funciona; con `"visitas"` a secas, `g` es una `Series` con un solo índice y la misma línea falla.
:::

```python verificable
import pandas as pd

# Ninguna columna separa las clases por si sola; el cociente si.
df = pd.DataFrame({
    "visitas": [10, 20, 30, 40, 12, 24, 36, 48],
    "compras": [2, 4, 6, 8, 6, 12, 18, 24],
    "convierte": [0, 0, 0, 0, 1, 1, 1, 1],
})
df["tasa"] = df["compras"] / df["visitas"]
g = df.groupby("convierte")[["visitas", "tasa"]].mean()

print(f"visitas medias clase 0 {g.loc[0, 'visitas']:.1f}  clase 1 {g.loc[1, 'visitas']:.1f}")
# -> visitas medias clase 0 25.0  clase 1 30.0
print(f"tasa media     clase 0 {g.loc[0, 'tasa']:.2f}  clase 1 {g.loc[1, 'tasa']:.2f}")
# -> tasa media     clase 0 0.20  clase 1 0.50
```

```python verificable
import pandas as pd

# Agregado historico por cliente: cada fila usa solo lo anterior de ese cliente.
df = pd.DataFrame({
    "cliente": ["A", "A", "A", "B", "B", "B"],
    "importe": [10, 30, 20, 5, 5, 45],
})
df["media_previa"] = df.groupby("cliente")["importe"].transform(lambda s: s.shift().expanding().mean())

# La primera fila de cada cliente no tiene pasado: queda a nulo, y eso es correcto.
print([None if pd.isna(v) else round(float(v), 1) for v in df["media_previa"]])
# -> [None, 10.0, 20.0, None, 5.0, 5.0]
```

## Errores típicos

- **Calcular la ventana incluyendo el instante actual.** `rolling(7).mean()` sin `shift(1)` usa
  el valor que quieres predecir. La puntuación sube y en producción no existe esa columna. Es
  [[fuga-de-datos|fuga de datos]] en su forma más común.
- **Usar agregados de todo el histórico en vez de acumulados.** «Número total de pedidos del
  cliente» calculado sobre la tabla entera incluye pedidos posteriores a la fila. Hay que usar
  `expanding()` o `cumcount()`, que solo miran hacia atrás, o fijar una ventana temporal
  explícita.
- **Construir variables con la variable objetivo.** «Media del objetivo en este segmento»,
  «número de impagos de este cliente» cuando predices impago: el modelo aprende la etiqueta.
  Si el agregado usa el objetivo, va con validación temporal y codificación fuera de pliegue,
  como en [[encoding-de-categoricas|la codificación de categóricas]].
- **Dividir por un denominador que puede ser cero.** Un cociente con denominador 0 produce
  infinito, y con denominadores pequeños produce valores enormes que desestabilizan medias y
  escalados. Comprueba el mínimo del denominador y decide qué hacer con esos casos.
- **Añadir cien variables porque «por si acaso».** Cada variable de más es una oportunidad de
  sobreajuste y un problema de mantenimiento. Con muchas columnas y pocas filas aparece
  [[maldicion-de-la-dimensionalidad|la maldición de la dimensionalidad]] y el rendimiento cae.
  Mide lo que aporta cada bloque antes de sumar el siguiente.
- **Recalcular las variables de forma distinta en producción.** Si el `rolling` de producción
  usa 5 días y el del entrenamiento 7, o si en producción el agregado se calcula con la tabla
  completa, las variables no significan lo mismo. Ese es exactamente el problema que resuelve
  un [[feature-store|almacén de variables]].

:::practica
enunciado: Ventas de cinco días: 80, 90, 100, 70, 120. Para predecir el día 5 (120), calcula la media de 3 días con y sin desplazamiento y decide cuál de las dos columnas es la variable válida.
pista: Sin desplazar, la ventana de la fila del día 5 incluye el propio día 5; con shift(1) la ventana termina el día 4.
solucion: Sin desplazar, la ventana de 3 en el día 5 promedia los días 3, 4 y 5: (100 + 70 + 120) / 3 = 96,7. Con shift(1), promedia los días 2, 3 y 4: (90 + 100 + 70) / 3 = 86,7. Solo la segunda sirve: la primera contiene la respuesta que quieres predecir, así que infla la validación y en producción no existiría.
:::

## Comprueba que lo sabes

:::quiz
p: Calculas `ventas.rolling(7).mean()` y lo usas como variable para predecir las ventas del mismo día. ¿Qué está mal?
o: Nada, la media móvil de 7 días es una variable estándar
o: Que la ventana incluye el día que quieres predecir, así que la variable contiene la respuesta
o: Que la media móvil solo vale para 30 días o más
a: 2
e: `rolling(7)` en la fila `t` promedia las filas `t−6` a `t`, incluida `t`. Para predecir el día `t` hay que usar `shift(1)` antes del `rolling`, de forma que la ventana termine en `t−1`. Sin ese desplazamiento la validación se infla y en producción la variable no existe.
:::

:::quiz
p: Tienes visitas y compras por sesión, pero las dos columnas se solapan entre las dos clases. ¿Qué variable construyes?
o: La suma de visitas y compras, para tener una sola señal
o: El cociente entre compras y visitas
o: La diferencia entre visitas y compras
a: 2
e: El fenómeno es una tasa de conversión, y una tasa es un cociente. La suma y la diferencia dependen de la escala: una sesión con 40 visitas y 8 compras da una diferencia de 32, mayor que otra con 12 visitas y 6 compras y diferencia 6, aunque la segunda convierta mucho mejor.
:::

:::trampa
La ingeniería de variables es donde más se cuela el futuro, porque es donde más decisiones
tomas con la vista puesta en el resultado. Si construyes una variable y de repente tu AUC sube
de 0,62 a 0,91, no celebres: busca el momento exacto en que conoces ese dato en producción. Casi
siempre no lo conoces.
:::
