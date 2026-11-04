---
id: visualizacion-estadistica
titulo: Visualización estadística
fase: 3
nivel: intermedio
rutas: [ds, core]
prerequisitos: [visualizacion-matplotlib, medidas-de-centralidad, cuantiles-y-percentiles, medidas-de-dispersion]
tags: [seaborn, plotly, distribuciones, correlacion, eda]
resumen: Boxplots, violines, densidades y matrices de correlación: cómo enseñar una distribución entera en vez de un solo número que la esconde.
fuentes: ["Waskom (2021), 'seaborn: statistical data visualization'", "Tukey (1977), 'Exploratory Data Analysis'"]
---

## En una frase

La visualización estadística dibuja la **distribución completa** de una variable y sus
relaciones, en lugar de un resumen de una sola cifra: un boxplot, un violín o un diagrama de
dispersión enseñan lo que una media tapa.

## La idea

Dos grupos de usuarios han probado tu aplicación. El grupo A tarda de media 1,8 segundos en
completar la tarea; el grupo B, 1,8 segundos. Con eso, informas de que «no hay diferencias».
Vuelves a mirar los datos crudos: en el grupo A los tiempos son 1,7 y 1,9 casi siempre, y en
el grupo B la mitad tarda 0,9 segundos y la otra mitad 2,7. Es la misma media y no se parecen
en nada. Esta es exactamente la lección del cuarteto de Anscombe, cuatro conjuntos de datos con
la misma media, la misma varianza y la misma correlación, y cuatro formas completamente
distintas al dibujarlos. **El resumen numérico no es la distribución.**

La visualización estadística es la caja de herramientas para eso:

- Para **una variable**: histograma, densidad, boxplot, violín, gráfico de puntos con temblor
  (jitter), función de distribución acumulada empírica.
- Para **dos variables**: diagrama de dispersión, hexágono o mapa de densidad cuando hay
  demasiados puntos, y matriz de correlación.
- Para **una variable numérica por categorías**: boxplot o violín por grupo, que es el gráfico
  que responde a «¿de verdad son distintos estos grupos?».
- Para **una variable a lo largo del tiempo**: línea con banda de intervalo, y nunca barras
  sueltas sin continuidad.

La regla práctica que resume todo: **si vas a agregar, enseña también la dispersión**. Un
gráfico de barras con la media por grupo es una mentira por omisión: dos grupos con la misma
media y desviaciones de 0,1 y 5 se ven idénticos. Añade el error (intervalo de confianza o
desviación típica) y di qué has dibujado, porque la barra de error no significa lo mismo en
cada caso.

Y una decisión que casi nadie explicita: **cuántos datos hay por grupo**. Un violín estimado
con 8 observaciones es una forma inventada; un boxplot con 8 puntos también, aunque sea más
discreto. Con menos de 30 valores por grupo, dibuja los puntos.

## Definición formal

Las piezas de los gráficos estadísticos, con su definición precisa:

- **Cuartiles.** Con los datos ordenados, `Q1` es el valor que deja el 25 % por debajo, `Q2` la
  mediana (el 50 %) y `Q3` el 75 %.
- **IQR (rango intercuartílico):** `IQR = Q3 − Q1`. Mide la dispersión del 50 % central y no
  la arrastran los extremos, igual que la mediana.
- **Bigotes del boxplot:** se extienden hasta el dato más alejado que aún cumple estar dentro de
  `Q1 − 1,5 · IQR` y `Q3 + 1,5 · IQR`. Lo que queda fuera se dibuja como punto suelto. **Un
  punto fuera de los bigotes no es un error de medición**: la regla 1,5 · IQR marca rareza
  estadística, no invalidez.
- **Densidad (KDE):** una estimación suavizada de la función de densidad, que se obtiene
  sumando una curva pequeña centrada en cada observación. Su forma depende de un **ancho de
  banda** que hay que elegir; con pocos datos, la curva es más una opinión que un dato.
- **Violín:** un boxplot con la densidad dibujada a los lados. Aporta la forma (bimodalidad,
  asimetría) a cambio de exigir más datos para no mentir.
- **Coeficiente de correlación de Pearson:** `r = cov(x, y) / (σx · σy)`, con `cov(x, y)` la
  covarianza muestral y `σx`, `σy` las desviaciones típicas muestrales. Vale entre −1 y 1 y
  mide **relación lineal**. `r = 0` no significa «sin relación», significa «sin relación
  lineal»: una parábola perfecta tiene `r ≈ 0`.

:::formula
r = cov(x, y) / (σx · σy)  ,   −1 ≤ r ≤ 1
:::

- **Fila de la matriz de correlación:** cada celda es el `r` entre dos columnas. Es simétrica y
  su diagonal vale 1. Ordenar las columnas por similitud (agrupamiento jerárquico) hace
  visible la estructura que un orden alfabético esconde.

## Ejemplo

Los tiempos de respuesta de un servicio, en milisegundos, ordenados:

```
42  48  51  55  61  66  70  74  81  95  110  140  190  320  900
```

Son 15 mediciones. Hecho a mano, con el convenio de que el cuartil es el valor que deja el 25 %
de los datos por debajo (posición `0,25 · (15 + 1) = 4` y `0,75 · (15 + 1) = 12`):

- `Q1` = 55 (posición 4), `Q2` (mediana) = 74 (posición 8), `Q3` = 140 (posición 12).
- `IQR` = 140 − 55 = 85.
- Bigote superior: `Q3 + 1,5 · IQR` = 140 + 127,5 = 267,5. El bigote llega hasta 190 (el mayor
  valor por debajo de 267,5) y **320 y 900** se dibujan como puntos sueltos.
- Media = 153,5 ms; mediana = 74 ms. La media está **por encima de 12 de las 15 mediciones**:
  solo 190, 320 y 900 la superan.

:::aviso
Ese `Q1 = 55` y ese `Q3 = 140` son los del cálculo a mano. NumPy y la mayoría de las
herramientas usan **interpolación lineal** entre los dos valores que rodean la posición, y con
estos mismos datos devuelven `Q1 = 58,0` y `Q3 = 125,0`. No es que uno esté mal: son dos
convenios distintos de percentil, y el mismo dato da un IQR de 85 o de 67 según cuál se use. El
boxplot del bloque de código usa el convenio de NumPy, así que su límite superior es 225,5 en vez
de 267,5: la caja cambia de tamaño y los bigotes se calculan con otro número, aunque con estos
datos los puntos sueltos salgan los mismos (320 y 900) con los dos convenios. Si publicas un
boxplot, di con qué herramienta lo has hecho, porque dos gráficos del mismo dato pueden salir
distintos.
:::

Ese es el motivo de que en latencia se publique `p50`, `p95` y `p99` y no la media: con una cola
larga, la media describe a un usuario que no existe. Un histograma o un boxplot de estos datos
enseña en dos segundos lo que la tabla de percentiles cuenta con esfuerzo: el grueso por debajo
de 100 ms y una cola de dos casos lentísimos.

## Código

```python verificable
import numpy as np
import matplotlib.pyplot as plt

# Boxplot sin Seaborn: mismos cuartiles, mismos bigotes, todo explicito.
ms = np.array([42, 48, 51, 55, 61, 66, 70, 74, 81, 95, 110, 140, 190, 320, 900], dtype=float)

q1, mediana, q3 = np.percentile(ms, [25, 50, 75])
iqr = q3 - q1
bigote = q3 + 1.5 * iqr
atipicos = ms[ms > bigote]

fig, ax = plt.subplots()
ax.boxplot(ms, orientation="horizontal")
ax.set_xlabel("ms")
print("Q1, mediana, Q3:", q1, mediana, q3)
print("IQR:", iqr)
print("limite del bigote:", bigote)
print("atipicos:", atipicos.tolist())
print("media:", round(ms.mean(), 1))
```

```python verificable
import numpy as np

# La media miente con cola a la derecha; los percentiles aguantan.
ms = np.array([42, 48, 51, 55, 61, 66, 70, 74, 81, 95, 110, 140, 190, 320, 900], dtype=float)

print(f"media  {ms.mean():.1f}")
print(f"p50    {np.percentile(ms, 50):.0f}")
print(f"p95    {np.percentile(ms, 95):.0f}")
print("mediciones por debajo de la media:", int((ms < ms.mean()).sum()), "de", ms.size)
```

```python verificable
import numpy as np

# Correlacion de Pearson: una parabola perfecta tiene r casi cero.
x = np.linspace(-3, 3, 41)
y = x**2

r = np.corrcoef(x, y)[0, 1]
print("r de x con x^2:", round(r, 3))

# ...y sin embargo la relacion es exacta y determinista.
print("y siempre vale x^2:", bool(np.allclose(y, x**2)))
```

```python verificable
import numpy as np

# Matriz de correlacion: covarianza estandarizada, diagonal 1 y simetrica.
rng = np.random.default_rng(7)
altura = rng.normal(170, 9, size=400)
peso = 0.8 * altura + rng.normal(20, 4, size=400)   # correlacion fuerte y positiva
horas_sueno = rng.normal(7, 1.2, size=400)          # independiente de las otras dos

datos = np.column_stack([altura, peso, horas_sueno])
r = np.corrcoef(datos, rowvar=False)

print("forma de la matriz:", r.shape)
print("simetrica:", bool(np.allclose(r, r.T)))
print("diagonal:", np.round(np.diag(r), 6).tolist())
print("r(altura, peso):", round(r[0, 1], 3))
print("r(altura, sueno):", round(r[0, 2], 3))
```

```python ilustrativo
import seaborn as sns
import matplotlib.pyplot as plt

# Seaborn calcula la estimacion por ti (KDE, cuartiles, intervalos) y devuelve
# objetos de Matplotlib: sigue siendo fig y ax, con las mismas reglas de ejes.
df = sns.load_dataset("tips")      # necesita la red la primera vez
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Distribucion del gasto por dia: la forma importa mas que la media.
sns.violinplot(data=df, x="day", y="total_bill", inner="quart", cut=0, ax=ax1)

# Relacion entre dos variables numericas, con una recta de regresion.
sns.regplot(data=df, x="total_bill", y="tip", ax=ax2)

# Matriz de correlacion: cada celda es un coeficiente de Pearson.
sns.heatmap(df[["total_bill", "tip", "size"]].corr(), vmin=-1, vmax=1, annot=True)
plt.show()
```

```python ilustrativo
import plotly.express as px

# Plotly genera HTML interactivo: util para explorar, pesado para publicar.
# El hover y el zoom hacen que no tengas que agregar los datos para que se lean.
fig = px.scatter(
    df, x="total_bill", y="tip", color="day", trendline="ols",
    hover_data=["size", "time"],
    labels={"total_bill": "cuenta (USD)", "tip": "propina (USD)"},
)
fig.update_layout(title="Propina frente a cuenta, por dia de la semana")
fig.show()
```

## Errores típicos

- **Enseñar solo la media.** La barra de la media por grupo esconde la dispersión: dos grupos
  con la misma media pueden ser idénticos o no tener nada que ver. Acompaña siempre con la
  dispersión (boxplot, puntos o banda) y di qué representa la barra de error: el error típico
  es más pequeño que la desviación típica, y mucha gente los confunde.
- **Violín con pocos datos.** La densidad es una estimación con un ancho de banda elegido a
  mano: con 8 valores, la forma del violín la decide el ancho de banda, no los datos. Por
  debajo de unas 30 observaciones por grupo, dibuja los puntos.
- **Diagrama de dispersión con 200.000 puntos.** Todo se convierte en una mancha sólida y las
  zonas densas se ven igual que las raras. Para eso están la transparencia, el muestreo
  aleatorio o los gráficos de densidad hexagonal y 2D.
- **Leer la matriz de correlación como causalidad.** `r = 0,9` entre dos variables no dice cuál
  mueve a cuál; puede haber una tercera variable detrás. Mira
  [[causalidad-vs-correlacion|causalidad y correlación]] antes de escribir la conclusión.
- **Olvidar que Pearson solo mide lo lineal.** Un `r` de 0,02 con una relación en forma de U es
  perfectamente compatible. Antes de fiarte del número, mira el gráfico. Si la relación es
  monótona pero no lineal, [[correlacion-pearson-spearman|Spearman]] es la medida adecuada.
- **Recortar el eje del boxplot.** Aunque el bigote se defina con el IQR, cambiar el límite del
  eje para «acercar» la caja hace que los atípicos desaparezcan del dibujo. Si los quitas,
  dilo; si los tapas con `set_ylim`, estás escondiendo justo lo que había que enseñar.

:::practica
enunciado: Notas ordenadas de 11 alumnos: 2, 3, 4, 5, 5, 6, 7, 7, 8, 9, 10. Con el convenio `0,25 · (n + 1)`, calcula Q1, Q3, el IQR, los límites de los bigotes y di si hay puntos sueltos.
pista: Con n = 11 las posiciones son 3 y 9; los bigotes llegan al dato más lejano dentro de Q1 − 1,5 · IQR y Q3 + 1,5 · IQR.
solucion: Q1 cae en la posición 0,25 · 12 = 3, es decir 4; Q3 en la 0,75 · 12 = 9, es decir 8. IQR = 8 − 4 = 4. Límite superior 8 + 6 = 14; inferior 4 − 6 = −2. Los datos van de 2 a 10, todos dentro, así que el boxplot no dibuja ningún punto suelto.
:::

## Comprueba que lo sabes

:::quiz
p: Un boxplot de 20 mediciones muestra dos puntos fuera de los bigotes. ¿Qué significa?
o: Que esas dos mediciones son errores y hay que borrarlas
o: Que están fuera del rango Q1 − 1,5·IQR y Q3 + 1,5·IQR, es decir que son raras según ese criterio, no necesariamente erróneas
o: Que la distribución es normal y esos puntos son imposibles
a: 2
e: La regla de 1,5 · IQR es una convención para marcar valores alejados del 50 % central; no es un test de error. En datos con colas gordas (latencia, ingresos, tráfico) hay puntos fuera de los bigotes constantemente y son parte del fenómeno. Se investigan uno a uno antes de decidir si se corrigen.
:::

:::quiz
p: Dos variables tienen un coeficiente de Pearson de 0,03. ¿Qué concluyes?
o: Que no hay ninguna relación entre ellas
o: Que no hay relación lineal, pero puede haber una relación no lineal fuerte
o: Que el cálculo está mal, porque un valor tan bajo es imposible
a: 2
e: Pearson mide solo la componente lineal. Una relación simétrica en forma de U da un coeficiente cercano a cero y una relación perfecta. Para descartar relación hay que mirar el gráfico de dispersión o usar medidas que capturen monotonía, como Spearman.
:::

:::trampa
Un violín `cut=0` recorta la densidad a los límites de los datos observados; con el valor por
defecto, Seaborn **extiende** la curva más allá del mínimo y el máximo reales. Eso es
interpolación, no dato: si tu variable no puede ser negativa, un violín que baja de cero está
dibujando algo imposible. Comprueba siempre los extremos del dibujo contra los de los datos.
:::

:::nota
Si solo puedes usar una herramienta, aprende [[visualizacion-matplotlib|Matplotlib]] a fondo:
Seaborn y Plotly devuelven objetos de Matplotlib o construyen figuras por encima de él, así que
los límites, las escalas y las etiquetas se controlan igual. La diferencia es el trabajo que
te ahorran, no el vocabulario.
:::
