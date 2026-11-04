---
id: validacion-temporal
titulo: Validación temporal
fase: 5
nivel: avanzado
rutas: [ds, quant]
prerequisitos: [autocorrelacion-acf-pacf, estacionariedad, fuga-de-datos]
tags: [validacion, series-temporales, backtest]
resumen: Por qué el K-fold barajado miente con datos ordenados en el tiempo y cómo se evalúa de verdad, con ventanas hacia delante y sin fuga de información.
fuentes: ["Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice', cap. 5", "Bergmeir y Benítez (2012), 'On the use of cross-validation for time series predictor evaluation'"]
---

## En una frase

Validar un modelo temporal es responder a la pregunta «¿cómo le habría ido prediciendo el futuro
con lo que se sabía en cada momento?», y esa pregunta prohíbe barajar: las particiones tienen que
respetar el orden del tiempo y dejar un hueco entre el final del entrenamiento y el principio de la
prueba.

## La idea

Un modelo de machine learning normal se evalúa barajando las filas: saber el precio de la vivienda A
no te dice nada de la vivienda B, así que da igual qué filas caigan en entrenamiento y cuáles en
prueba. Con datos ordenados en el tiempo eso es falso, y no por un detalle técnico: **el K-fold
barajado responde a otra pregunta**.

Piensa en un examen. Si la mitad de las preguntas del examen están también en los apuntes con las
respuestas, aprobar es fácil y no demuestra nada. Eso es el K-fold barajado: cada punto de prueba
tiene vecinos temporales en el entrenamiento, y como la serie es suave, esos vecinos contienen casi
la respuesta. El modelo no extrapola, **interpola** entre puntos que ya ha visto.

En producción no hay vecinos: hay que predecir el mañana a partir del ayer. Esa es la extrapolación,
y es lo que mide el esquema hacia delante (*walk-forward*): se entrena con la primera parte de la
serie, se predice el bloque siguiente, se avanza el origen y se repite. La diferencia entre las dos
estimaciones no es un matiz del 5 %: en el ejemplo de abajo, un modelo de vecino más cercano obtiene
2,59 de error con K-fold barajado y 23,11 con walk-forward, sobre los mismos datos y el mismo modelo.

:::figura
fichero: validacion-temporal-barajar-frente-a-avanzar
pie: Los dos paneles usan los mismos 400 puntos, el mismo ruido y el mismo modelo de vecino más cercano, así que la única diferencia es **qué filas caen en prueba**. A la izquierda, los puntos de colores son los cinco pliegues barajados y cada punto de prueba tiene vecinos temporales a los lados: ahí el modelo interpola y el error sale 2,59. A la derecha, el esquema hacia delante empuja el bloque de prueba siempre por delante del entrenamiento, y el error sube a 23,11 porque pasado el último punto visto el vecino más cercano repite siempre 161,3 mientras la recta real ya vale 199,5. Conclusión: si tu partición permite interpolar, el número que obtienes no es el que tendrás en producción.
fuente: figuras/validacion-temporal-1.py
:::

Hay tres daños concretos del barajado, y conviene distinguirlos:

1. **Cambia la pregunta.** El barajado estima el error de interpolar; tú necesitas el de extrapolar.
   Cuanto más flexible sea el modelo (árboles, vecinos, redes), más grande es la diferencia.
2. **Subestima la incertidumbre.** Con autocorrelación, los errores de dos pliegues se parecen
   mucho entre sí: no son `k` medidas independientes, y la desviación entre pliegues que reportas
   como «error típico» se queda corta.
3. **Elige mal el modelo.** Si comparas una recta con un bosque usando pliegues barajados, gana el
   bosque casi siempre, porque interpolando es imbatible. En el esquema hacia delante, con tendencia,
   la recta gana.

## Definición formal

Sea una serie con instantes `t_1 < t_2 < … < t_N` y sea `h` el horizonte que quieres pronosticar.

- **Partición válida.** Una partición es válida si existe un hueco `g ≥ 0` tal que todo instante de
  prueba es posterior a todo instante de entrenamiento más el hueco:
  `min(t_prueba) ≥ max(t_entrena) + g`. Barajar rompe esa condición por construcción.
- **Gap o hueco `g`.** No es cero en la práctica. Si tus variables usan ventanas de 20 días o tu
  etiqueta tarda 10 días en cerrarse, hay información compartida entre el final del entrenamiento y
  el principio de la prueba. `g` debe cubrir esa memoria ([[purged-kfold|purga y embargo]]).
- **Ventana expansiva.** Para el origen `m_j`: entrenamiento `[t_1, t_{m_j}]` y prueba
  `[t_{m_j+1}, t_{m_j+h}]`. El entrenamiento crece con cada pliegue; es el esquema más parecido a
  «usar todo lo que sé».
- **Ventana móvil.** Entrenamiento `[t_{m_j−w+1}, t_{m_j}]`, con `w` el tamaño fijo de la ventana.
  Se usa cuando sospechas que el pasado lejano ya no representa el presente (cambio de régimen). A
  cambio, cada pliegue usa menos datos y la estimación es más ruidosa.
- **Origen único frente a varios orígenes.** Un solo corte da un solo número, y ese número depende
  del corte. Lo correcto es repetir con `J` orígenes y reportar la distribución:
  `error_medio = (1/J) · Σ_j error_j`, junto con la desviación entre pliegues.
- **Incertidumbre.** El error típico aparente es `desviación_entre_pliegues / √J`, pero es una cota
  inferior: los pliegues comparten casi todo el entrenamiento, así que sus errores están
  correlacionados. Con `J = 5` no esperes un intervalo estrecho.
- **Hiperparámetros dentro del pliegue.** Si eliges el modelo mirando el error de todos los
  pliegues y luego reportas ese mismo error, el número está sesgado al alza. La elección tiene que
  ocurrir dentro de cada pliegue y medirse en el trozo que ese pliegue no ha visto.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `N` | El número de observaciones de la serie | observaciones | Más historia permite más orígenes, pero no arregla el reparto: el error de extrapolación no baja solo por tener más filas. Con `N` pequeño, el último pliegue entrena con casi todo y apenas queda hueco para validar |
| `t_i` | El instante de la observación `i` | tiempo (días, meses) | No se elige: es el orden natural de los datos, y es justo lo que prohíbe barajar. Si los instantes no son equidistantes, el tamaño del bloque no es proporcional al tiempo que cubre |
| `h` | El horizonte que quieres pronosticar | pasos de tiempo | Bloques de prueba más largos miden de verdad la extrapolación, pero dejan menos orígenes. Con `h` muy pequeño, el error se parece al de un modelo ingenuo y todo empata |
| `g` | El hueco entre el final del entrenamiento y el principio de la prueba | pasos de tiempo | Un `g` mayor quita solapamiento de memoria, así que la estimación es más honesta y más pesimista. Si tus variables son medias móviles de 20 días y dejas `g = 0`, el modelo ve el futuro y el hueco no lo delata |
| `J` | El número de orígenes de validación que repites | orígenes (recuento) | Más orígenes dan una estimación menos dependiente de dónde cayó el corte, a cambio de más cómputo y de errores correlacionados entre sí. La incertidumbre **no** baja como `1/√J` |
| `m_j` | El instante en que arranca la prueba del origen `j`, es decir, el último punto de entrenamiento | índice de la observación | Al avanzarlo, el pliegue entrena con más datos (ventana expansiva) y prueba en un tramo distinto del mercado. Moverlo hasta que el resultado acompaña es p-hacking aplicado al tiempo |
| `w` | El tamaño de la ventana móvil, cuando no es expansiva | observaciones | Una `w` menor se adapta antes a un cambio de régimen, pero cada pliegue entrena con menos datos y el error es más ruidoso. Si `w` es tan pequeña como `h`, mides el ruido, no el modelo |
| `error_j` | El error del origen `j` sobre su bloque de prueba | las de la métrica (RMSE en euros, por ejemplo) | Es lo que se promedia. Un solo `error_j` no es una estimación: es una muestra del error y depende de dónde cayó el corte |
| `error_medio` | La media de los errores de todos los orígenes | las de la métrica | Al subir `J` se estabiliza, pero no se vuelve exacta: los orígenes comparten entrenamiento y sus errores están correlacionados. Es el número con el que se comparan modelos, nunca un solo pliegue |
| `desviación_entre_pliegues / √J` | El error típico aparente de esa media | las de la métrica | Es una cota **inferior** de la incertidumbre real. Se encoge al subir `J`, y ahí está la trampa: con J = 5 tenderías a un intervalo estrecho que los datos no justifican |
:::

El esquema de cuatro orígenes con ventana expansiva sobre 400 observaciones queda así:

```text
pliegue 1: entrena [  0,  80)   prueba [ 80, 160)
pliegue 2: entrena [  0, 160)   prueba [160, 240)
pliegue 3: entrena [  0, 240)   prueba [240, 320)
pliegue 4: entrena [  0, 320)   prueba [320, 400)
```

## Ejemplo

Cuatrocientos puntos de una recta `y = 0,5·t` con ruido de desviación 2. La desviación típica de la
serie es 57,88, así que la tendencia domina todo lo demás.

- **K-fold barajado, 5 pliegues, un modelo de vecino más cercano:** error cuadrático medio (RMSE) de
  **2,59**, con los pliegues entre 2,28 y 2,91. Un modelo casi perfecto, aparentemente.
- **Walk-forward, 4 orígenes, el mismo modelo:** RMSE de **23,11**, con los bloques entre 20,48 y
  25,94. Diez veces peor.
- ¿Por qué? Entrenado hasta `t = 319`, el vecino más cercano predice **161,3** tanto en `t = 320` como
  en `t = 399`: pasado el último punto de entrenamiento, repite siempre ese valor. La recta real en
  `t = 399` vale 199,5. El K-fold barajado no lo detecta porque nunca le pide extrapolar.

Con un modelo que sí extrapola, la comparación de esquemas de ventana es la decisión interesante:

- Recta con ventana expansiva: RMSE medio **1,96** (pliegues 2,13 · 1,87 · 1,92 · 1,90).
- Recta con ventana de 60 puntos: RMSE medio **2,28** (pliegues 2,63 · 1,93 · 2,65 · 1,90).
- Naive del último valor: **2,63**.

La ventana expansiva gana porque la relación es estable en toda la serie; si la pendiente hubiera
cambiado a mitad, la ventana móvil habría ganado. Eso no se decide por intuición, se mide.

## Código

```python verificable
import numpy as np

# Serie con tendencia lineal clara y ruido: y = 0.5*t + ruido
rng = np.random.default_rng(7)
n = 400
t = np.arange(n, dtype=float)
y = 0.5 * t + rng.normal(0, 2.0, n)
idx = np.arange(n)

def vecino_mas_cercano(entrena, prueba):
    """Predice con el valor del punto de entrenamiento mas cercano en el tiempo."""
    distancias = np.abs(t[prueba][:, None] - t[entrena][None, :])
    return y[entrena[distancias.argmin(axis=1)]]

def rmse(entrena, prueba):
    return float(np.sqrt(np.mean((y[prueba] - vecino_mas_cercano(entrena, prueba)) ** 2)))

# K-fold barajado: cada punto de prueba tiene vecinos temporales en el entrenamiento
azar = rng.permutation(idx)
err_azar = [rmse(np.setdiff1d(idx, p), p) for p in np.array_split(azar, 5)]

# Walk-forward: cada bloque se predice entrenando solo con lo anterior
err_wf = [rmse(idx[idx < b[0]], b) for b in np.array_split(idx, 5)[1:]]

print("K-fold barajado  RMSE %.2f  pliegues %s"
      % (np.mean(err_azar), " ".join("%.2f" % e for e in err_azar)))
# -> K-fold barajado  RMSE 2.59  pliegues 2.62 2.28 2.60 2.56 2.91
print("walk-forward     RMSE %.2f  bloques %s"
      % (np.mean(err_wf), " ".join("%.2f" % e for e in err_wf)))
# -> walk-forward     RMSE 23.11  bloques 20.48 24.32 25.94 21.70

# La causa: pasado el ultimo punto de entrenamiento, repite siempre ese mismo valor
entrena = idx[idx < 320]
print("predice en t=320 %.1f y en t=399 %.1f; la recta real en t=399 vale 199.5"
      % (vecino_mas_cercano(entrena, np.array([320]))[0],
         vecino_mas_cercano(entrena, np.array([399]))[0]))
# -> predice en t=320 161.3 y en t=399 161.3; la recta real en t=399 vale 199.5
```

:::claves
- `np.arange(n, dtype=float)` no es lo mismo que `np.arange(n)`: el primero es un array de decimales y el segundo, de enteros. En este bloque da igual, porque todo lo que se calcula después es decimal, pero el tipo de un array condiciona el de las operaciones que salen de él: míralo antes de dar por bueno un resultado raro.
- `rng.normal(0, 2.0, n)` recibe la **desviación típica**, no la varianza. Si le pasas 2 pensando en la varianza, el ruido real es de desviación 1,41 y toda la comparación de errores cambia.
- `t[prueba][:, None] - t[entrena][None, :]` construye una matriz de todas las distancias: `[:, None]` convierte la columna en `(len(prueba), 1)` y `[None, :]` la fila en `(1, len(entrena))`. Al restarlas, NumPy las «difunde» a `(len(prueba), len(entrena))`. Sin los corchetes nuevos, restaría elemento a elemento y saldría un vector de la longitud equivocada.
- `y[entrena[distancias.argmin(axis=1)]]` tiene tres indexaciones encadenadas: `argmin(axis=1)` devuelve **posiciones dentro del array de entrenamiento**, no índices originales. Por eso hay que traducirlas con `entrena[...]` antes de indexar `y`. Saltarse ese paso es el fallo que más veces se cuela aquí, y no da error: da predicciones de otro sitio.
- `np.setdiff1d(idx, p)` devuelve el complementario **ordenado**, y esa es justo la trampa del K-fold barajado: el conjunto de entrenamiento contiene puntos de antes y de después de cada punto de prueba. `np.array_split(azar, 5)` reparte una permutación, así que cada pliegue es una muestra dispersa en el tiempo.
- `np.array_split(idx, 5)[1:]` es el walk-forward: se toma el array **en orden** (sin permutar) y se descarta el primer bloque, que no tendría entrenamiento anterior. Cambiar `[1:]` por `[:4]` mide lo mismo pero desplazado; quitar el corte deja un pliegue sin datos de entrenamiento y `np.polyfit` falla.
- `np.polyfit(t, y, 1)` devuelve los coeficientes de mayor a menor grado, y `np.polyval(coef, t)` los evalúa. Ese orden es el contrario del que se escribe a mano en `a + b·x`: intercambiarlos no da error, da una recta casi vertical y un RMSE enorme que puedes confundir con el resultado del modelo.
- El RMSE del vecino más cercano se queda **clavado** en 161,3 para todo el bloque cuando el entrenamiento termina en `t = 319`: el vecino de cualquier instante futuro es siempre el último punto visto. Esa es la firma de la extrapolación con un modelo que no extrapola, y se ve en una línea: `np.unique(vecino_mas_cercano(entrena, np.arange(320, 400)))` devuelve un solo valor.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(7)
n = 400
t = np.arange(n, dtype=float)
y = 0.5 * t + rng.normal(0, 2.0, n)
idx = np.arange(n)

def walk_forward(ventana=None):
    """Error por bloque con ventana expansiva, o movil si se fija el tamano."""
    errores = []
    for bloque in np.array_split(idx, 5)[1:]:
        entrena = idx[idx < bloque[0]]
        if ventana:
            entrena = entrena[-ventana:]
        coef = np.polyfit(t[entrena], y[entrena], 1)   # minimos cuadrados con numpy
        pred = np.polyval(coef, t[bloque])
        errores.append(float(np.sqrt(np.mean((y[bloque] - pred) ** 2))))
    return np.array(errores)

expansiva, movil = walk_forward(), walk_forward(60)
print("expansiva  media %.2f  bloques %s"
      % (expansiva.mean(), " ".join("%.2f" % e for e in expansiva)))
# -> expansiva  media 1.96  bloques 2.13 1.87 1.92 1.90
print("movil 60   media %.2f  bloques %s"
      % (movil.mean(), " ".join("%.2f" % e for e in movil)))
# -> movil 60   media 2.28  bloques 2.63 1.93 2.65 1.90
print("naive del ultimo valor %.2f" % np.sqrt(np.mean((y[1:] - y[:-1]) ** 2)))
# -> naive del ultimo valor 2.63
```

## Errores típicos

- **Barajar antes de dividir.** `KFold(shuffle=True)` con una serie temporal mide interpolación. Si
  tu serie tiene autocorrelación (casi todas la tienen), el número que sale es un techo, no una
  estimación.
- **Meter futuro en el preprocesado o en la etiqueta.** Si la media, la imputación o una ventana de
  variables se calculan con datos posteriores al instante que predices, la fuga está dentro y el
  esquema de particiones no la ve ([[fuga-de-datos]], [[pipelines-de-ml]]).
- **Elegir los hiperparámetros con el mismo esquema que luego reportas.** Si pruebas 200
  configuraciones y publicas la mejor, ese número está sesgado al alza. La elección va dentro del
  pliegue (validación anidada) y el resultado se mide fuera.
- **Ignorar el hueco entre entrenamiento y prueba.** Si tus variables son medias móviles de 50 días o
  tu etiqueta tarda 10 días en resolverse, hay solapamiento aunque las fechas no se toquen
  ([[purged-kfold]], [[sample-weights]]).
- **Quedarte con un solo número.** Un origen es una sola muestra de la métrica, y reportar la media
  sin la dispersión entre pliegues oculta que el resultado depende del corte. Repite con varios
  orígenes y da la distribución completa ([[validacion-combinatoria-cpcv]]). Mover el origen hasta
  que el resultado acompañe es p-hacking aplicado al tiempo
  ([[data-snooping-y-multiple-testing]]).
- **Confundir validación con backtest.** La validación temporal estima el error de predicción; no
  modela comisiones, deslizamiento, liquidez ni capacidad. Una estrategia puede tener un error de
  pronóstico excelente y perder dinero al ejecutarla ([[backtesting-por-eventos]]).

:::practica
enunciado: Tienes 240 días para validar hacia delante con ventana expansiva y bloques de prueba de 30 días, con un mínimo de 60 días de entrenamiento inicial. ¿Cuántos orígenes caben y cuánto entrena el último? Si una variable es una media móvil de 20 días, ¿qué hueco hace falta?
pista: Cada origen entrena hasta donde empieza su bloque de prueba; el hueco g exige que el entrenamiento termine al menos g días antes.
solucion: Los orígenes son 60, 90, 120, 150, 180 y 210: seis. El último entrena [0, 210) y prueba [210, 240). Con una media móvil de 20 días hay memoria compartida, así que g debe ser 20 y el entrenamiento tiene que cerrarse en 190. Entonces el primer origen, m = 60, dejaría solo 40 días de entrenamiento, por debajo del mínimo: quedan cinco orígenes.
:::

## Comprueba que lo sabes

:::quiz
p: Sobre una serie con tendencia y ruido, un modelo de vecino más cercano obtiene RMSE 2,6 con K-fold barajado y 23,1 con walk-forward. ¿Cuál es la explicación?
o: El walk-forward entrena con menos datos, y por eso el error se multiplica por diez
o: El K-fold barajado deja vecinos temporales en el entrenamiento, así que el modelo interpola en vez de extrapolar
o: El modelo está mal configurado y el K-fold lo disimula con suerte
a: 2
e: La diferencia no viene del tamaño del entrenamiento: los pliegues barajados usan el 80 % de los datos y la ventana expansiva llega a usar el 80 % en el último bloque. La causa es que el barajado permite interpolar entre puntos cercanos, mientras que el walk-forward exige predecir fuera del rango visto, y ahí el vecino más cercano repite el último valor que conoce.
:::

:::quiz
p: ¿Qué mide exactamente la desviación entre pliegues dividida por la raíz del número de pliegues?
o: El error de generalización exacto del modelo
o: Una cota inferior de la incertidumbre de la estimación, porque los pliegues comparten datos de entrenamiento
o: La varianza del ruido de la serie
a: 2
e: La fórmula desviación / raíz de J solo vale para medidas independientes. En validación los pliegues comparten casi todo el entrenamiento y, con autocorrelación, también se parecen los errores, así que la incertidumbre real es mayor que esa cifra. No es el error de generalización ni tiene nada que ver con el ruido de la serie.
:::

:::quiz
p: Tienes 300 observaciones de una serie con una relación estable y usas 4 orígenes de validación hacia delante. ¿Qué ganas repitiendo el proceso con 20 orígenes solapados?
o: Nada, porque el esquema y los datos son los mismos
o: Una estimación con menos dependencia de dónde cayó el corte, a cambio de más cómputo y de errores correlacionados entre orígenes
o: Un error siempre menor, porque se aprovechan mejor los datos
a: 2
e: Con 4 orígenes el número depende mucho de dónde caen los cortes; con 20 la distribución se ve mejor y la media es más estable. No reduce el error del modelo ni convierte las medidas en independientes: los orígenes solapados comparten datos, así que la incertidumbre no baja como la raíz del número de orígenes.
:::

:::aviso
Si el modelo incluye variables construidas con ventanas largas o etiquetas que tardan en cerrarse,
el hueco entre entrenamiento y prueba tiene que cubrir esa memoria. Purgar y embargar es más barato
que descubrir en producción que el backtest estaba mirando el futuro.
:::
