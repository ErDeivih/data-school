---
id: anomalias-en-series-temporales
titulo: Anomalías en series temporales
fase: 5
nivel: intermedio
rutas: [ds, de]
prerequisitos: [series-temporales-componentes, outliers-y-deteccion, estacionariedad]
tags: [series-temporales, anomalias, deteccion, robustez]
resumen: En una serie con deriva y ciclo, el z-score global no marca nada; hay que detectar sobre el residuo, con una escala robusta y contando los ecos.
fuentes: ["Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice', cap. 12", "Iglewicz y Hoaglin (1993), 'How to Detect and Handle Outliers'", "Ahmad et al. (2017), 'Unsupervised real-time anomaly detection for streaming data'"]
---

## En una frase

Detectar anomalías en una serie temporal no es buscar valores raros, sino valores que no
encajan **con lo que se esperaba en ese instante**, y esa expectativa casi nunca es la media
de toda la serie: es la tendencia, el ciclo y el nivel reciente, medidos en una escala
robusta.

## La idea

Un termómetro industrial mide la temperatura de un horno cada cinco minutos. El horno arranca
frío por la mañana y se calienta hasta la tarde; los lunes no hay producción, así que la
temperatura sigue un ciclo semanal. Ahora imagina que un sensor se descalibra y marca 30
grados de más durante media hora. La pregunta «¿es 320 una temperatura anómala?» no tiene
respuesta sin decir cuándo: a las tres de la madrugada del lunes, 320 es un disparate; a las
cinco de la tarde del miércoles, es lo normal.

Ese es el problema entero. El [[outliers-y-deteccion|z-score]] clásico compara cada valor con
la media y la desviación de **toda** la serie, y en una serie temporal esa desviación no mide
el ruido: mide la deriva y el ciclo. En el ejemplo de esta página, la desviación típica de la
serie es 39,5 mientras que el ruido real es de 2,6, así que el umbral de cuatro desviaciones
cae 158 unidades por encima de la media y **ninguna de las ocho anomalías inyectadas llega a
cruzarlo**. La regla no es conservadora: está ciega.

Hay tres formas de arreglarlo, y las tres se usan juntas en la práctica:

1. **Quitar de en medio la estructura.** Convierte la serie en algo estacionario: resta la
   tendencia, toma diferencias, o compara cada punto con el mismo punto del ciclo anterior
   (diferencia estacional). Lo que queda es el residuo, y ahí ya tiene sentido preguntar por
   un valor raro.
2. **Medir la escala con algo robusto.** La desviación típica se infla con la propia anomalía
   que intentas detectar. La mediana de las desviaciones absolutas respecto a la mediana
   (MAD) no: aguanta hasta que casi la mitad de los datos son raros. Multiplicada por 1,4826
   estima la desviación típica de una distribución normal, así que los umbrales de siempre
   (3, 3,5, 4) se siguen leyendo igual.
3. **Elegir el umbral por el coste, no por la estadística.** Si cada falsa alarma despierta a
   un operario a las tres de la mañana, el umbral sube; si una anomalía no detectada rompe
   una máquina de 200.000 euros, el umbral baja. La estadística te dice cuántas marcas
   esperas por azar; el negocio decide cuántas tolera.

Y hay una consecuencia de la que casi nadie habla: **una diferencia estacional marca cada
anomalía dos veces**. Si el día 41 el valor sube 22, la diferencia respecto al día 34 sube 22;
y cuando la anomalía sale de la ventana, el día 48 vuelve a compararse con el día 41 y la
diferencia baja 22. La anomalía ha dejado un eco a siete días vista. En el experimento de
abajo, la regla detecta 7 de las 8 anomalías reales y produce 8 marcas adicionales en los
ecos: cada una cae exactamente siete días después de una anomalía, y la del día 50 es el eco de
la del día 43, justo la única que se escapó. Interpretar eso como «15 anomalías» es el
error más común al pasar de la detección al informe.

:::figura
fichero: anomalias-deriva-z-global-frente-a-diferencia-estacional
pie: La serie tiene 300 días con deriva de 0,45 al día, un ciclo semanal de amplitud 9, ruido de desviación 2,6 y ocho anomalías inyectadas (tres de ellas seguidas, en los días 41 a 43). A la izquierda, el z-score global: la desviación de toda la serie vale 39,5, la banda de cuatro desviaciones (línea roja de puntos) cae fuera del gráfico y los ocho puntos rojos pasan completamente desapercibidos, con un z máximo de 2,23. A la derecha, la diferencia respecto al mismo día de la semana anterior y un z-score con mediana y MAD en ventana de 29 días: siete de las ocho anomalías reales salen por encima del umbral (los puntos rojos) y los cuadrados naranjas son los ecos a siete días, cuando la anomalía sale de la ventana de comparación. En total 15 marcas para 8 anomalías: recuperación del 88 % y precisión del 47 % si cuentas cada marca por separado; agrupando marcas próximas, las quince marcas se reducen a ocho incidentes.
fuente: figuras/anomalias-en-series-temporales-1.py
:::

## Definición formal

Con la serie `y_1, …, y_T` y un horizonte estacional `m` (7 en datos diarios con ciclo
semanal, 1 si no hay ciclo), la detección se plantea siempre en dos pasos: calcular un
residuo y tipificarlo con una escala robusta.

:::formula
r_t = y_t − ŷ_t        z_t = (r_t − mediana(r)) / (1,4826 · MAD(r))
:::

:::formula
MAD(r) = mediana( |r_i − mediana(r)| )
:::

El residuo `ŷ_t` puede venir de tres sitios, y cada uno detecta un tipo de anomalía distinto:

- **Diferencia estacional:** `r_t = y_t − y_{t−m}`. Elimina el ciclo y, si la serie es un
  paseo, también la deriva. Detecta saltos puntuales y cambios de nivel, y deja ecos.
- **Mediana de una ventana centrada** de ancho `w`, sin contar el punto que se evalúa:
  `r_t = y_t − mediana(y_{t−w/2} … y_{t+w/2})`. Adapta el nivel a la deriva, pero necesita
  `w/2` puntos de futuro: **no sirve para detectar en tiempo real**, solo para revisar.
- **Predicción de un modelo** (suavizado exponencial, ARIMA, un modelo de machine learning):
  `r_t = y_t − ŷ_t` con `ŷ_t` calculado solo con información anterior. Es el único de los
  tres que funciona en producción sin mirar al futuro ([[suavizado-exponencial]],
  [[prediccion-con-incertidumbre]]).

:::parametros
| Símbolo | Qué es | Unidades | Si sube |
| --- | --- | --- | --- |
| `y_t` | El valor observado en el instante `t` | las de la serie | Es el dato. Un solo valor extremo contamina la media y la desviación, pero apenas mueve la mediana |
| `ŷ_t` | Lo que se esperaba en `t` según el residuo elegido | las de la serie | Si `ŷ_t` es demasiado suave, el residuo arrastra el ciclo y el detector marca cada lunes. Si es demasiado flexible, se come la anomalía |
| `r_t` | Residuo: lo que el dato se aparta de lo esperado | las de la serie | Es donde se busca la anomalía. Su media debería estar cerca de cero; si no, el nivel esperado está sesgado |
| `m` | Periodo estacional de la comparación | pasos (entero) | Con `m` mal puesto (un 30 en vez de 7) el residuo mantiene el ciclo y el detector se llena de falsos positivos cada semana |
| `w` | Ancho de la ventana del residuo por mediana centrada | pasos | Una ventana mayor es más estable y tarda más en adaptarse a un cambio de nivel; con `w` pequeño el detector confunde ruido con anomalía |
| `MAD(r)` | Mediana de las desviaciones absolutas respecto a la mediana del residuo | las de la serie | Es la escala robusta. Sube si el ruido crece, y entonces el umbral efectivo sube con él: menos marcas |
| `1,4826` | Factor que convierte el MAD en una estimación de la desviación típica normal | adimensional | No se elige: es la constante que hace que `1,4826 · MAD` sea insesgado para una normal |
| `z_t` | Puntuación tipificada del residuo | desviaciones típicas robustas | Es lo que se compara con el umbral. Dos series con ruido muy distinto producen `z_t` comparables, y ahí es donde está la utilidad |
| `k` | Umbral de decisión, típicamente entre 3 y 4 | desviaciones típicas robustas | Cada unidad que bajas multiplica los falsos positivos. En una normal, `k = 3` marca un 0,27 % de los puntos por puro azar: en 10.000 observaciones son 27 marcas aunque no pase nada |
:::

Una comprobación que conviene hacer siempre: si `MAD(r) = 0` (serie constante o residuo
discreto), la fórmula divide entre cero. En la práctica se pone un suelo, o se cambia a un
criterio de cuantiles del residuo.

## Ejemplo

300 días con `y_t = 120 + 0,45·t + 9·sen(2πt/7) + ruido` de desviación 2,6, más ocho anomalías
inyectadas en los días 41, 42, 43 (racha de tres), 118, 171, 229, 230 y 275, con magnitudes
entre 19 y 26 en valor absoluto. La desviación típica de la serie completa es **39,48**; el
ruido real es 2,6. Resultados por regla:

| Regla | Umbral | Marcas correctas | Marcas falsas | Precisión | Recuperación |
| --- | --- | --- | --- | --- | --- |
| z-score global (media y desviación de todo) | 4,0 | 0 de 8 | 0 | — | 0,00 |
| z-score robusto global (mediana y MAD de todo) | 4,0 | 0 de 8 | 0 | — | 0,00 |
| z-score robusto en ventana centrada de 29 días sobre la serie | 3,5 | 3 de 8 | 0 | 1,00 | 0,38 |
| Diferencia estacional `y_t − y_{t−7}` y z-score robusto en ventana | 4,0 | 7 de 8 | 8 | 0,47 | 0,88 |

Léelo como tres lecciones distintas:

- Las dos reglas globales obtienen **recuperación cero**. Su `z` máximo es 2,23: no es que el
  umbral sea exigente, es que la escala está midiendo la tendencia. Cambiar la media por la
  mediana no arregla nada mientras sigas midiendo la escala sobre la serie entera.
- La ventana centrada es la mejor en precisión: cuando marca, acierta. Pero recupera solo 3
  de 8, y son precisamente las anomalías del día 118, 229 y 275: los puntos sueltos. La racha
  de tres días consecutivos se le escapa porque tres valores raros inflan la mediana y el MAD
  de su propia ventana: es el **efecto de enmascaramiento**, y empeora cuanto más dura la
  anomalía.
- La diferencia estacional recupera casi todo, incluida la racha, y paga el precio de los
  ecos: ocho de sus quince marcas caen exactamente siete días después de una anomalía. La
  única anomalía que se le escapa es la tercera de la racha, la del día 43, porque su
  comparación (`y_43 − y_36`) cae justo en el umbral. Si agrupas las marcas por proximidad
  antes de contar, las quince marcas se convierten en ocho incidentes: siete que contienen una
  anomalía real y uno que agrupa los tres ecos del día 48.

Con datos diarios, `m = 7` y umbral `k = 4`, la tasa esperada de falsos positivos por azar es
diminuta, así que casi todas las marcas falsas del ejemplo son estructurales (ecos y cambios
de nivel), no ruido.

## Código

```python verificable
import numpy as np

# Serie con deriva, ciclo semanal y ruido; ocho anomalias encima (dias 41, 42, 43...)
azar = np.random.default_rng(9)
n = 300
t = np.arange(n)
y = 120 + 0.45 * t + 9.0 * np.sin(2 * np.pi * t / 7) + azar.normal(0.0, 2.6, n)
pos = np.array([41, 42, 43, 118, 171, 229, 230, 275])
y[pos] += np.array([22.0, 25.0, 21.0, -23.0, 19.0, -26.0, -21.0, 24.0])
real = np.zeros(n, dtype=bool)
real[pos] = True


def z_robusto(r, k, w=29):
    """Tipifica el residuo con mediana y MAD de una ventana centrada."""
    mad = np.empty(n)
    for i in range(n):
        a = max(0, i - w // 2)
        vecinos = np.delete(r[a:min(n, i + w // 2 + 1)], i - a)
        mad[i] = np.median(np.abs(vecinos - np.median(vecinos)))
    return np.abs(r - np.median(r)) / (1.4826 * mad + 1e-9) > k


d7 = np.zeros(n)
d7[7:] = y[7:] - y[:-7]                     # misma comparacion que el dia 7 anterior
marca = z_robusto(d7, k=4.0)
zeker = np.abs((y - y.mean()) / y.std()) > 4.0     # la regla ciega, para comparar

print("desviacion de la serie %.2f  desviacion del ruido %.2f" % (y.std(), 2.6))
# -> desviacion de la serie 39.48  desviacion del ruido 2.60
print("z global maximo %.2f  marcas %d" % (np.abs((y - y.mean()) / y.std()).max(), zeker.sum()))
# -> z global maximo 2.23  marcas 0
print("diferencia estacional: aciertos %d de %d  marcas totales %d"
      % (int((marca & real).sum()), int(real.sum()), int(marca.sum())))
# -> diferencia estacional: aciertos 7 de 8  marcas totales 15
print("dias marcados:", np.where(marca)[0].tolist())
# -> dias marcados: [41, 42, 48, 49, 50, 118, 125, 171, 178, 229, 230, 236, 237, 275, 282]
```

:::claves
- `np.delete(r[a:b], i - a)` quita el punto que estás evaluando de su propia ventana. Sin ese `delete`, el valor raro entra en el cálculo del MAD, lo infla y se autoexculpa: el detector deja de ver justo lo que busca.
- La multiplicación por 1,4826 no es un adorno. El MAD mide la mediana de las distancias a la mediana; para una normal, esa cantidad vale 0,6745 desviaciones típicas. Dividir entre 0,6745 es multiplicar por 1,4826, y por eso el umbral se sigue leyendo en «desviaciones típicas».
- `d7[0:7] = 0` por construcción: los siete primeros días no tienen con quién compararse. Esos ceros son residuos artificiales, no datos, y si el umbral fuera más bajo marcarían el día 0.
- El `+ 1e-9` del denominador evita la división entre cero cuando el residuo es constante. Enmascara el problema en lugar de resolverlo: una serie con `MAD = 0` necesita otra regla, no un épsilon.
- `z_robusto` recorre los 300 puntos con un bucle y crea una ventana nueva por punto: es legible y es lento. Sobre una serie de un millón de puntos esto tarda minutos; con `scipy.ndimage.median_filter` o pandas rodante baja a segundos.
- El conjunto `pos` y el array `real` existen solo para poder medir precisión y recuperación. En un problema real no tendrás esa etiqueta, y sin ella **no puedes calcular ninguna de las dos**: es el punto que trata la sección de errores típicos.
:::

## Errores típicos

- **Tipificar contra la media y la desviación de toda la serie.** Es el error de partida y el
  más caro, porque la regla parece razonable y no marca nada. En el ejemplo, la escala sale 15
  veces más grande que el ruido. Si tu serie tiene tendencia, la media global no describe
  ninguna parte de la serie ([[estacionariedad]]).
- **Usar la desviación típica en lugar del MAD.** Un solo valor extremo infla la desviación y
  con ella el umbral: el detector se apaga justo cuando más lo necesitas. La mediana y el MAD
  solo se rompen cuando la mitad de los datos son raros.
- **Contar los ecos como anomalías distintas.** Cada anomalía deja una marca cuando entra y
  otra cuando sale de la ventana de comparación. Sin agrupar marcas cercanas, tu informe
  duplica el número de incidentes y el equipo de guardia desconfía del detector.
- **Mirar al futuro sin decirlo.** Una mediana centrada, un suavizado que usa los dos lados o
  un `diff` mal alineado usan información que en producción todavía no existe. La detección
  retrospectiva (revisar el mes pasado) puede permitírselo; la detección en vivo, no
  ([[fuga-de-datos]]).
- **Fijar el umbral por la estadística y olvidar el coste.** El umbral se elige con el coste
  de cada tipo de error: una falsa alarma que despierta a alguien y una anomalía perdida que
  rompe una máquina no valen lo mismo ([[umbrales-y-coste]]).
- **Suponer que la anomalía es siempre un error.** Un pico puede ser un fallo de sensor o el
  día que se lanzó una promoción. Distinguir error de fenómeno real exige contexto de negocio
  y, muchas veces, hablar con quien opera el sistema ([[calidad-de-datos]]).
- **Evaluar el detector con las anomalías que ya conocías.** Si marcas como «anomalías
  reales» solo los eventos que un analista etiquetó después de verlos, la recuperación sale
  alta por construcción. La única evaluación honesta usa anomalías inyectadas con
  localización conocida, como en el ejemplo.

:::practica
enunciado: Una métrica se mide cada hora y tiene ciclo diario. El equipo quiere un detector en vivo y otro para revisar el mes pasado. Propón el residuo de cada uno, la escala, el umbral y qué tasa de falsos positivos esperas por azar.
pista: Uno de los dos puede usar información del futuro y el otro no. El ciclo diario son 24 horas.
solucion: Para revisar el mes pasado, el residuo puede ser la mediana de una ventana centrada de 25 horas sin contar el punto, y la escala el MAD del residuo en la misma ventana: detecta cambios de nivel y no necesita modelo. Para el detector en vivo, ese residuo está prohibido porque usa 12 horas de futuro. En su lugar, la expectativa es el valor de la misma hora del día anterior (residuo estacional con m = 24) o la predicción de un suavizado exponencial estacional ajustado solo con datos anteriores, y la escala es el MAD del residuo calculado sobre las últimas 168 horas (una semana). Con umbral k = 4 en una normal, la tasa esperada de marcas por puro azar es de unas 6 por cada 100.000 puntos, o sea prácticamente ninguna en un mes de 720 horas; en la práctica verás más por los cambios de nivel y los días atípicos, que no son ruido. Con k = 3 la tasa sube a 27 por cada 10.000, unas dos marcas al mes solo por azar: aceptable si nadie se despierta por ellas.
:::

## Comprueba que lo sabes

:::quiz
p: Una serie diaria con tendencia y ciclo semanal tiene desviación típica de 39,5. Aplicas un z-score clásico con umbral 3 y no marca nada. ¿Por qué?
o: Porque el umbral 3 es demasiado alto para series diarias
o: Porque la desviación típica mide la tendencia y el ciclo, no el ruido, así que la banda de decisión queda fuera del rango de la serie
o: Porque el z-score solo funciona con distribuciones normales y esta serie no lo es
a: 2
e: La escala está contaminada por la estructura: el ruido real es de 2,6 y la desviación de la serie es de 39,5, quince veces mayor. La banda de tres o cuatro desviaciones cae fuera del gráfico y ninguna anomalía la alcanza. El problema no es la normalidad ni el umbral, y bajar el umbral marcaría el ciclo entero, no las anomalías.
:::

:::quiz
p: ¿Por qué se usa el MAD multiplicado por 1,4826 en lugar de la desviación típica?
o: Porque el MAD es más rápido de calcular que la desviación típica
o: Porque el MAD es robusto: una minoría de valores extremos no lo infla, y el factor 1,4826 lo devuelve a la escala de una desviación típica normal
o: Porque el MAD está acotado entre 0 y 1
a: 2
e: La robustez es la razón: con la desviación típica, la misma anomalía que quieres detectar engorda el umbral que debería detectarla. El factor 1,4826 es la constante que hace que el MAD estime la desviación típica de una distribución normal, y por eso los umbrales de 3 o 4 se interpretan igual. El MAD no es más rápido que la desviación típica ni está acotado entre 0 y 1.
:::

:::quiz
p: Detectas anomalías con la diferencia respecto al mismo día de la semana anterior y obtienes 7 aciertos y 7 marcas extra. ¿Qué son esas marcas extra?
o: Ruido del sensor, que hay que filtrar subiendo el umbral
o: Ecos: la anomalía vuelve a aparecer cuando sale de la ventana de comparación, siete días después
o: Anomalías reales que el detector anterior no había visto
a: 2
e: Son la misma anomalía vista dos veces: al entrar en la comparación y al salir de ella, porque la diferencia `y_t − y_{t−7}` se descompensa en los dos extremos. Subir el umbral las eliminaría junto con las detecciones buenas. Lo correcto es agrupar marcas próximas antes de contar incidentes, y anotar que un cambio de nivel permanente solo deja la marca de entrada.
:::

:::aviso
Sin etiquetas no hay precisión ni recuperación. Puedes medir cuántas marcas produce tu regla y
a qué tasa (eso sí es verificable con datos reales), pero afirmar que aciertas el 90 % exige
un conjunto con anomalías localizadas. Si no lo tienes, invierte el esfuerzo en inyectar
anomalías sintéticas sobre tus propias series antes que en afinar el umbral.
:::
