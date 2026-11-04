---
id: visualizacion-matplotlib
titulo: Visualización con Matplotlib
fase: 3
nivel: básico
rutas: [core, ds, de]
prerequisitos: [numpy-fundamentos, pandas-fundamentos]
tags: [matplotlib, graficos, visualizacion, figuras]
resumen: Figuras, ejes, escalas y anotaciones con Matplotlib, y las decisiones de ejes que hacen que un gráfico mienta sin querer.
fuentes: ["Hunter (2007), 'Matplotlib: A 2D graphics environment'", "Tufte (1983), 'The Visual Display of Quantitative Information'"]
---

## En una frase

Matplotlib es la librería con la que dibujas un gráfico a partir de arrays: tú decides qué va
en cada eje, con qué escala y desde dónde empieza el eje, y esas tres decisiones cambian más
la conclusión del lector que los propios datos.

## La idea

Tienes dos versiones del mismo producto y quieres contar que la nueva va mejor. La métrica es
la latencia media: 94,2 ms antes y 91,4 ms ahora. Una mejora del 3 %, real pero pequeña. Si
dibujas dos barras con el eje vertical empezando en 90, las alturas dibujadas son 4,2 y 1,4, así
que la barra de 94,2 se ve **tres veces más alta** que la de 91,4. Nadie ha mentido con los
números, y todo el mundo ha entendido mal la magnitud.

Ese es el problema que resuelve saber usar Matplotlib bien: **la escala y el recorte del eje
son parte del mensaje**. Hay dos reglas que evitan el 90 % de los gráficos engañosos:

1. En un **gráfico de barras** el eje de la magnitud **empieza siempre en cero**, porque lo
   que se compara es la longitud de las barras. Recortarlo exagera las diferencias.
2. En un **gráfico de líneas** el eje puede empezar donde quieras, porque lo que se compara
   es la pendiente, no la altura. Empezar en 90 para una serie que se mueve entre 91 y 95 es
   legítimo si lo dices.

Piensa en un electrocardiograma: el trazo no empieza en cero, y está bien, porque interesa la
forma. Pero si mides «cuánta agua hay en dos vasos» con dos barras que arrancan a media
altura, estás manipulando.

Matplotlib tiene dos interfaces. La moderna, orientada a objetos, trabaja con `fig` (la
figura, el lienzo entero) y `ax` (los ejes, un sistema de coordenadas dentro de la figura).
La antigua, `plt.plot(...)`, actúa sobre «los ejes actuales» de forma implícita y es la fuente
de la mitad de los bugs: acabas dibujando en el gráfico equivocado. Usa siempre
`fig, ax = plt.subplots()`.

## Definición formal

Los objetos de una figura, y para qué sirve cada uno:

- **Figure** (`fig`): el lienzo completo, con su tamaño en pulgadas (`figsize`) y su
  resolución en puntos por pulgada (`dpi`). No contiene datos.
- **Axes** (`ax`): un sistema de coordenadas con su rectángulo (los «ejes» en el sentido
  matemático). Una figura puede tener varios, uno al lado de otro con `plt.subplots(1, 2)`.
- **Axis** (sin la «s»): cada uno de los dos ejes de un `Axes`, con sus límites, sus marcas y
  sus etiquetas. Se controla con `ax.set_xlim()`, `ax.set_xlabel()`, `ax.set_xscale()`.
- **Artist**: todo lo que se dibuja dentro de un `Axes` (líneas, puntos, barras, texto).
  `ax.plot()` devuelve un `Line2D`, que es un artist.
- **Escala** (`set_xscale`): la transformación de dato a posición. `"linear"` (por defecto),
  `"log"` (multiplicativa), `"symlog"`. Elegir mal la escala oculta o inventa estructura.
- **Límites del eje**: `ax.set_ylim(0, 100)` fija el mínimo y el máximo. Es la decisión más
  consecuente de todo el gráfico.
- **Número de intervalos de un histograma**: con `n` observaciones y `IQR` el rango
  intercuartílico, la regla de Freedman-Diaconis da la anchura de cada intervalo.

:::formula
ancho = 2 · IQR / n^(1/3)  ,   intervalos ≈ (máx − mín) / ancho
:::

  Con 5.000 observaciones y un `IQR` de 20, el ancho sale 2 · 20 / 5000^(1/3) ≈ 2,3, así que
  unos 30 intervalos para un rango de 70. Es una regla de partida: si el histograma sale plano
  o con una sola barra, se ajusta a mano y se dice.

Dos funciones que conviene conocer de memoria, porque la confusión entre ellas es clásica:

- `ax.plot(x, y)` — primero la coordenada horizontal, después la vertical.
- `ax.scatter(x, y)` — la misma convención.
- `np.histogram(datos, bins=30)` devuelve `(frecuencias, bordes)`. **Ojo:** si dibujas con
  `ax.bar`, necesitas los bordes **izquierdos** (`bordes[:-1]`) y la **anchura** de cada
  intervalo (`np.diff(bordes)`), no los centros.

## Ejemplo

Dos campañas con las mismas visitas de media:

- Campaña A (estable): 98, 100, 99, 101, 102, 100 miles de visitas.
- Campaña B (a rachas): 40, 160, 55, 145, 60, 140 miles de visitas.

Las dos tienen media 100,0, y su desviación típica muestral es 1,4 y 53,8 respectivamente. El
resumen numérico (media y desviación) ya las distingue, pero solo el gráfico enseña que B alterna
picos y valles, y que A apenas se mueve. Con 40 y 160 en el mismo eje, cualquier barra de A es
invisible: eso es información, no un defecto del gráfico.

Con el eje recortado, el efecto sobre la percepción es puro cálculo:

- Barras de 94,2 y 91,4 con el eje de 90 a 95: las alturas dibujadas son 4,2 y 1,4, es decir
  la primera se ve 4,2 / 1,4 = 3 veces más alta.
- Las mismas barras con el eje de 0 a 100: 94,2 y 91,4, una diferencia visual del 3 %.

Mismo dato, dos mensajes opuestos. La regla no es «no recortes nunca»: es que **si recortas,
lo digas** (por ejemplo anotando el valor encima de cada barra).

## Código

```python verificable
import numpy as np
import matplotlib
matplotlib.use("Agg")          # sin ventana: solo calcular, no mostrar
import matplotlib.pyplot as plt

rng = np.random.default_rng(0)
fig, ax = plt.subplots()

# Histograma: hay que pasar los bordes IZQUIERDOS y la anchura, no los centros.
datos = rng.normal(100, 15, size=5000)
frec, bordes = np.histogram(datos, bins=30)
anchos = np.diff(bordes)
ax.bar(bordes[:-1], frec, width=anchos, align="edge")

print("intervalos:", len(frec))
print("borde mayor:", bordes[-1])
print("suma de frecuencias:", frec.sum())
```

```python verificable
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Los límites del eje y el número de marcas: el gráfico se puede leer de verdad.
fig, ax = plt.subplots()
ax.plot([0, 1, 2, 3], [10, 22, 19, 30], marker="o")

ax.set_ylim(0, 35)
ax.set_yticks([0, 10, 20, 30])

print("limites y:", ax.get_ylim())
print("marcas y :", ax.get_yticks().astype(int).tolist())
```

```python verificable
import numpy as np
import matplotlib.pyplot as plt

# Dos campanas con la MISMA media y desviaciones muy distintas:
# el resumen numerico no basta, hay que mirar la forma.
a = np.array([98, 100, 99, 101, 102, 100])
b = np.array([40, 160, 55, 145, 60, 140])

print(f"media A {a.mean():.1f}  desv A {a.std(ddof=1):.1f}")   # ddof=1: muestra, no poblacion
print(f"media B {b.mean():.1f}  desv B {b.std(ddof=1):.1f}")
print("rango A:", a.max() - a.min(), " rango B:", b.max() - b.min())

assert a.mean() == b.mean()          # la media no distingue nada: el grafico si
```

```python verificable
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Por que el recorte del eje enganna: las longitudes dibujadas cambian de proporcion.
antes, ahora = 94.2, 91.4

# Caso honesto: el eje empieza en cero.
fig1, ax1 = plt.subplots()
ax1.bar(["antes", "ahora"], [antes, ahora])
honesto = ax1.get_ylim()[1]
proporcion_cero = antes / ahora

# Caso engannoso: el eje recortado exagera la diferencia.
fig2, ax2 = plt.subplots()
ax2.bar(["antes", "ahora"], [antes, ahora])
ax2.set_ylim(90, 95)
proporcion_recortada = (antes - 90) / (ahora - 90)

print(f"altura dibujada  honesto {proporcion_cero:.2f}  recortado {proporcion_recortada:.2f}")
print("eje por defecto llega a", honesto)
```

## Errores típicos

- **Recortar el eje en un gráfico de barras.** Es el error número uno, y casi siempre
  involuntario: `ax.set_ylim(90, 95)` convierte una mejora del 3 % en una montaña rusa. En
  barras, el cero no es negociable. En líneas es aceptable si el rango es pequeño, pero
  anótalo.
- **Dibujar el histograma con los centros de los intervalos.** `np.histogram` devuelve los
  **bordes**, que son 31 valores para 30 intervalos. Si pasas los 31 a `ax.bar` obtienes una
  barra de más y todo desplazado medio intervalo. Se usan `bordes[:-1]` y `np.diff(bordes)`.
- **Gráfico de tarta con más de cinco categorías.** Un círculo con doce porciones no se
  compara a ojo: el ojo es malísimo estimando ángulos. Usa barras ordenadas de mayor a menor.
- **Línea para categorías sin orden.** Unir con una línea «Madrid, Barcelona, Valencia» sugiere
  una continuidad que no existe. Para categorías, barras; la línea es para magnitudes
  ordenadas, y casi siempre el tiempo.
- **Escala lineal con datos que abarcan varios órdenes de magnitud.** Si tus valores van de 1
  a 100.000, en escala lineal todas las barras pequeñas se ven iguales (pegadas al cero). En
  escala logarítmica se comparan cocientes; úsala y dilo en la etiqueta.
- **Dos ejes verticales para presumir de correlación.** Superponer dos series con ejes
  distintos siempre «muestra» que se mueven juntas: con libertad para escalar cada eje, puedes
  alinear cualquier par de series. Para relaciones, un diagrama de dispersión con un solo
  sistema de coordenadas.

:::trampa
El gráfico que enseña Matplotlib por defecto es el que sale de los datos, no el que cuenta lo
que quieres contar. Antes de exportar, comprueba tres cosas: desde dónde empieza el eje,
cuántas marcas tiene y si alguien puede leer las unidades. Un gráfico sin etiqueta en los ejes
no es un gráfico, es un dibujo.
:::

## Comprueba que lo sabes

:::quiz
p: Quieres comparar con barras una métrica que mejoró de 94,2 a 91,4 (un 3 %). ¿Qué haces con el eje vertical?
o: Empezarlo en 90 para que se aprecie la mejora
o: Empezarlo en cero, porque en barras lo que se compara es la longitud de las barras
o: Empezarlo en 91,4 para que la segunda barra quede pegada abajo
a: 2
e: En un gráfico de barras la magnitud se lee como longitud, así que el cero es obligatorio: con el eje de 90 a 95 la diferencia del 3 % se ve como una barra tres veces más alta. Si quieres destacar una mejora pequeña, anota los valores encima o usa una tabla, pero no recortes el eje. Recortar a 91,4 sería aún peor: la segunda barra desaparecería.
:::

:::quiz
p: ¿Por qué `ax.plot(x, y)` y `ax.hist` se comportan distinto con los bordes de un histograma?
o: Porque `ax.hist` calcula el histograma y lo dibuja, mientras que `ax.bar` necesita que le des tú las posiciones y la anchura de cada barra
o: Porque `ax.bar` solo admite números enteros
o: Porque `np.histogram` devuelve los centros de los intervalos
a: 1
e: `ax.hist` hace los dos trabajos: agrupa y dibuja. Si usas `np.histogram` para calcularlo tú, obtienes los bordes (31 valores para 30 intervalos) y tienes que quedarte con `bordes[:-1]` y calcular `np.diff(bordes)` para la anchura. No tiene nada que ver con enteros y `np.histogram` no devuelve centros.
:::

:::practica
enunciado: Tienes los ingresos anuales de 200 clientes: la mayoría entre 20.000 y 60.000 euros, y cuatro clientes por encima de 500.000. Quieres un solo gráfico que enseñe la distribución sin que los cuatro valores extremos aplasten al resto. ¿Qué dibujas y por qué?
pista: Piensa en qué escala hace comparables valores que se diferencian en un factor de 25.
solucion: Un histograma con el eje horizontal en escala logarítmica (`ax.set_xscale("log")`), con intervalos de anchura constante en escala logarítmica (por ejemplo 20 intervalos por década). En escala lineal, 196 clientes caen en los dos primeros intervalos y el histograma es una sola barra pegada a la izquierda. En logarítmica se ve la forma completa: el grueso entre 20.000 y 60.000 y una cola pequeña muy separada. La escala logarítmica compara cocientes, así que la distancia de 20.000 a 40.000 es la misma que de 40.000 a 80.000. Hay que decirlo en la etiqueta del eje: mucha gente lee un eje logarítmico como si fuera lineal y se cree que la cola es enorme. Si lo que quieres comunicar es «cuatro clientes se llevan una parte desproporcionada del total», es más claro un gráfico de barras ordenado o un diagrama de Pareto que un histograma.
:::

:::nota
En el ecosistema de visualización estadística, `[[visualizacion-estadistica|Seaborn]]` construye
sus gráficos **encima** de Matplotlib: acabas teniendo un `Figure` y un `Axes` de Matplotlib
igual que aquí, y por eso todo lo que aprendas de límites, escalas y etiquetas te sirve allí
tal cual. Matplotlib es la base, no una alternativa.
:::
