---
id: visualizacion-honesta
titulo: Visualización honesta
fase: 12
nivel: intermedio
rutas: [core, ds]
prerequisitos: [medidas-de-centralidad, storytelling-con-datos]
tags: [graficos, ejes, agregacion, comunicacion]
resumen: Un gráfico puede decir la verdad y mentir a la vez: ejes truncados, escalas mal elegidas, agregaciones que invierten la conclusión y colores que engañan sin querer.
fuentes: ["Tufte (2001), 'The Visual Display of Quantitative Information'", "Cairo (2019), 'How Charts Lie: Getting Smarter about Visual Information'"]
---

## En una frase

Elegir qué se ve y qué no se ve es una decisión con consecuencias: truncar un eje, cambiar la
escala, agregar por el campo equivocado o usar un color que parece otra cosa puede llevar a tu
lector a una conclusión opuesta a la que sostienen los datos.

## La idea

Piensa en una báscula de baño mal calibrada. Si empieza en 70 kg en lugar de 0, cada kilo que
ganas parece enorme. Nadie aceptaría esa báscula, y sin embargo el equivalente gráfico —un eje
que no empieza en cero— está en miles de informes. La diferencia es que en el gráfico nadie ve
dónde está el cero: la línea del eje se dibuja igual.

Hay tres formas de mentir sin decir una sola cifra falsa:

1. **Manipular el marco visual.** Un eje truncado exagera diferencias pequeñas; un gráfico con
   proporciones raras (muy alto y estrecho) exagera las pendientes; un gráfico 3D deforma las
   áreas porque las partes de delante parecen mayores. En barras, la regla es clara: **la
   longitud de la barra codifica la magnitud, así que el eje tiene que empezar en cero**. En
   líneas, truncar es más defendible (lo que importa es la forma de la tendencia), pero hay que
   avisar. En áreas y volúmenes, casi nunca: si duplicas el lado de un cuadrado, el área se
   multiplica por cuatro y el ojo lee esa multiplicación.
2. **Agregar por el campo equivocado.** Un mismo conjunto de datos puede dar dos conclusiones
   opuestas según el nivel al que se agrupe. Eso se llama **paradoja de Simpson**, y no es un
   truco retórico: es la razón de que «la media general» pueda ser la peor cifra del informe.
3. **Usar el canal equivocado.** El color es buenísimo para categorías y malísimo para
   magnitudes continuas, porque nuestro ojo no ordena tonos: un mapa de calor con el arcoíris
   crea fronteras que no existen en los datos. Para magnitudes se usan escalas secuenciales
   (claro a oscuro) o divergentes centradas en el valor neutro.

A esto se suma un cuarto problema más silencioso: **el gráfico bonito que no se puede usar**.
Sin título que diga el mensaje, sin unidades, sin fuente de los datos, con dos ejes verticales
que se cruzan donde conviene, con colores que no distinguen las series a quien tiene daltonismo
([[accesibilidad]]). Un gráfico que necesita cinco minutos de explicación para entenderse no
está comunicando: está decorando.

La regla que resume todo: **el gráfico tiene que hacer fácil la comparación que quieres que se
haga, y difícil la que no se sostiene**. Si tu gráfico hace que 3 puntos porcentuales parezcan
una revolución, no es un gráfico persuasivo, es un gráfico que miente sobre su propia escala.

## Definición formal

Dos medidas concretas para auditar un gráfico antes de publicarlo.

**1. Fracción del eje ocupada por la diferencia.** Sea `v_min` y `v_max` los valores
representados y `y_min` el límite inferior del eje. La diferencia relativa que ve el lector no
es `(v_max − v_min) / v_max`, sino la fracción del eje que ocupa esa diferencia:

:::formula
fraccion_visual = (v_max − v_min) / (v_max − y_min)
:::

Símbolos: `v_max` y `v_min` son el mayor y el menor de los valores dibujados; `y_min` es el
límite inferior del eje (`0` si el eje empieza en cero). Con el eje desde cero y valores entre
100 y 110, la diferencia ocupa `10/110 ≈ 9 %` de la altura. Con el eje empezando en 100, ocupa
`10/10 = 100 %` de la altura: la misma diferencia parece diez veces mayor.

**2. Agregado frente a desagregado.** Sea `S_g` la tasa del grupo `g` y `n_g` su tamaño. La
tasa agregada es una media ponderada por tamaño:

:::formula
S = Σ_g (n_g · S_g) / Σ_g n_g
:::

Si los pesos `n_g` son muy distintos entre los grupos que comparas, el agregado puede invertir
la conclusión: un grupo con mejor tasa en todos los segmentos puede perder en el total solo
porque la mayoría de sus casos están en el segmento difícil.

## Ejemplo

**Eje truncado.** Cuatro valores: 102, 105, 103, 107, dibujados en un lienzo de 200 píxeles de
alto.

- Con el eje desde **cero** (hasta 117,7, el máximo más un 10 % de margen), las barras miden
  173, 178, 175 y 182 píxeles: la primera alcanza el **95 %** de la última y se ven casi
  iguales, que es la verdad.
- Con el eje entre **100 y 107,5**, las mismas barras miden 53, 133, 80 y 187 píxeles: la
  primera parece el **28 %** de la última. La diferencia real (5 unidades) no ha cambiado; ha
  cambiado el marco, y con él la conclusión que saca el ojo.

**Paradoja de Simpson.** Dos tratamientos, evaluados por separado en casos leves y graves:

```
gravedad  tratamiento  casos  exitos  tasa
leve      A              10       9   0,90
leve      B             100      80   0,80
grave     A              40      20   0,50
grave     B              10       4   0,40
```

- En casos **leves**, A gana: 90 % frente a 80 %.
- En casos **graves**, A también gana: 50 % frente a 40 %.
- Pero agregando: A tiene 29 / 50 = **58,0 %** y B tiene 84 / 110 = **76,4 %**. A gana en los
  dos segmentos y pierde en el total.

El agregado no miente por aritmética, sino por mezcla: A se aplicó sobre todo a los casos graves
(40 de sus 50) y B sobre todo a los leves (100 de sus 110), así que el total pondera poblaciones
distintas y da la vuelta a la conclusión. El gráfico honesto es el de tasas por gravedad, no el
agregado.

## Código

```python verificable
import pandas as pd

# El mismo dato agregado y desagregado: dos historias distintas.
datos = pd.DataFrame({
    "gravedad":    ["leve", "leve", "grave", "grave"],
    "tratamiento": ["A", "B", "A", "B"],
    "casos":       [10, 100, 40, 10],
    "exitos":      [9, 80, 20, 4],
})
datos["tasa"] = datos.exitos / datos.casos

global_ = datos.groupby("tratamiento")[["exitos", "casos"]].sum()
global_["tasa"] = global_.exitos / global_.casos

print(datos[["gravedad", "tratamiento", "tasa"]].to_string(index=False))
print()
print("agregado:")
print(global_.to_string())
```

```python verificable
# Cuanto exagera un eje truncado, medido en pixeles.
def altura_px(valor, y_min, y_max, alto=200):
    return (valor - y_min) / (y_max - y_min) * alto

valores = [102, 105, 103, 107]
for etiqueta, y_min in [("desde 0  ", 0), ("desde 100", 100)]:
    alturas = [round(altura_px(v, y_min, max(valores) * 1.1 if y_min == 0 else 107.5)) for v in valores]
    print(f"eje {etiqueta}: alturas en px {alturas}  primera/ultima {alturas[0]/alturas[-1]:.2f}")
```

```python ilustrativo
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

valores = [102, 105, 103, 107]
fig, (izq, der) = plt.subplots(1, 2, figsize=(8, 3), sharey=False)

izq.bar(range(4), valores)                 # eje truncado: exagera la diferencia
izq.set_ylim(100, 108)
izq.set_title("Truncado (engana)")

der.bar(range(4), valores)                 # eje desde cero: la diferencia real
der.set_ylim(0, 110)
der.set_title("Desde cero (honesto)")
```

## Errores típicos

- **Truncar el eje de un gráfico de barras.** Es el error número uno, y el más eficaz para
  exagerar. En barras la longitud es la codificación, así que el cero es obligatorio. En líneas
  truncar es aceptable si lo dices y si el eje no induce a error sobre la magnitud del cambio.
- **Usar dos ejes verticales para dos series.** Elegir las escalas de forma que las dos líneas
  se crucen donde interesa es una fábrica de correlaciones falsas: puedes hacer que dos series
  cualesquiera parezcan ir juntas. Si necesitas dos magnitudes, usa dos gráficos apilados con
  el mismo eje horizontal.
- **Gráficos de tarta con muchas categorías.** Un ojo humano compara mal ángulos, y con seis o
  siete porciones es imposible ordenarlas. Para partes de un todo, barras horizontales
  ordenadas de mayor a menor; la tarta solo se defiende con dos o tres categorías muy
  distintas.
- **Volumen y 3D.** El efecto 3D deforma áreas y las porciones de delante parecen mayores. No
  aporta información y quita precisión: es decoración que miente.
- **Escalas de color arcoíris para magnitudes.** El arcoíris no tiene orden perceptivo (¿el
  amarillo es más que el verde?), crea bandas que no existen en los datos y es ilegible para
  daltonismo. Usa una escala secuencial de un solo tono y, si hay un centro con significado
  (cero, media), una divergente.
- **Publicar el agregado sin mirar los segmentos.** El total puede estar dominado por un
  segmento grande y ocultar que en el segmento que te importa la cosa va al revés. Antes de
  publicar un total, desagrega por las dos o tres dimensiones que podrían cambiarlo.
- **No decir las unidades ni el periodo.** «Ingresos: 1,2» no dice nada: ¿millones? ¿euros?
  ¿meses? El título, las unidades, el periodo y la fuente son parte del gráfico, no adornos.
- **Esconder la incertidumbre.** Una proyección dibujada como una línea limpia sugiere una
  precisión que no tienes. Añade la banda del intervalo o, si no puedes, dilo en el texto.

:::trampa
Una media móvil o un suavizado con la ventana equivocada puede convertir una serie plana en una
tendencia y al revés. Y un gráfico con puntos cada 7 días puede hacer desaparecer un patrón
semanal que sí existe. Antes de suavizar o de agregar por semana o mes, comprueba que la
decisión no es la que crea el efecto que estás contando: dibuja la serie diaria, aunque sea
fea, y decide después.
:::

## Comprueba que lo sabes

:::quiz
p: Cuatro barras con valores 102, 105, 103 y 107, con el eje vertical empezando en 100. ¿Qué efecto tiene?
o: Ninguno: los valores son los mismos y las barras son proporcionales a ellos
o: Que la diferencia real (5 unidades) ocupa casi toda la altura del eje y parece enorme
o: Que las barras se dibujan al revés
a: 2
e: Con el eje entre 100 y 107,5, la primera barra mide 53 píxeles y la última 187: parece un 28 % de la última, cuando desde cero alcanza el 95 %. Las barras siguen siendo proporcionales a su valor, pero el marco visual decide cómo se percibe la diferencia, y eso es exactamente lo que la truncadura manipula.
:::

:::quiz
p: Un tratamiento gana en casos leves y también en casos graves, pero pierde en el total. ¿Cómo se explica?
o: Es un error de cálculo: si gana en los dos segmentos, tiene que ganar en el total
o: Es la paradoja de Simpson: los segmentos tienen tamaños muy distintos y el agregado pondera por tamaño
o: Es porque las tasas no se pueden agregar nunca
a: 2
e: La tasa agregada es una media ponderada por el número de casos: si el grupo que gana aplica casi todos sus casos al segmento difícil, su total baja aunque gane en cada segmento. No es un error, es la consecuencia de agregar poblaciones distintas. Las tasas sí se pueden agregar, pero solo ponderando y sabiendo qué estás mezclando.
:::

:::quiz
p: ¿Por qué el eje vertical es obligatorio desde cero en un gráfico de barras y no tanto en uno de líneas?
o: Porque las barras son más bonitas con el cero incluido
o: Porque la longitud de la barra codifica la magnitud, mientras que en una línea lo que se lee es la forma de la tendencia
o: Porque los datos cambian de valor si el eje no empieza en cero
a: 2
e: En barras, el ojo compara longitudes y una barra que empieza en 100 mide una longitud que no corresponde al valor. En una línea, el lector interpreta pendientes y forma, y truncar puede ser aceptable si se avisa y no se exagera la magnitud del cambio. Las otras dos opciones son falsas: el eje no cambia los datos.
:::
