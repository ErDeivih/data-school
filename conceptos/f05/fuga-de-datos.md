---
id: fuga-de-datos
titulo: Fuga de datos (data leakage)
fase: 5
nivel: avanzado
rutas: [ds, de, quant]
prerequisitos: [validacion-cruzada, train-val-test]
tags: [fuga, validacion, errores]
resumen: Información que el modelo ve al entrenar y no existirá al predecir: el error que hace que un modelo parezca perfecto en el portátil y falle el primer día en producción.
fuentes: ["Kaufman et al. (2012), 'Leakage in Data Mining: Formulation, Detection, and Avoidance'", "López de Prado (2018), 'Advances in Financial Machine Learning'"]
---

## En una frase

Hay fuga de datos cuando en el entrenamiento entra información que en el momento de predecir no
estará disponible, y el síntoma es siempre el mismo: métricas demasiado buenas para ser verdad.

## La idea

Imagina un examen en el que el profesor, sin darse cuenta, te da el enunciado con la respuesta
impresa detrás. Sacas un 10 y no has aprendido nada. La nota no mide lo que crees que mide.
Eso es exactamente la fuga de datos: el modelo acierta porque la respuesta estaba en la entrada,
no porque haya aprendido el patrón.

Lo traicionero es que casi nunca es un error de libro. Son detalles pequeños:

- Una columna que se genera **después** del evento. Un dataset de impagos con la columna
  «llamadas del departamento de cobros»: las llamadas ocurren *porque* el cliente no pagó, así
  que la columna es consecuencia de la etiqueta. En producción no la tendrías el día de la
  concesión del crédito.
- Un preprocesamiento calculado con todas las filas. La media, la desviación, el IQR o la
  codificación por objetivo mirados con el conjunto entero.
- Un reparto aleatorio en un problema con tiempo o con grupos. Si barajas, filas del mismo
  paciente, del mismo cliente o de la misma semana caen en entrenamiento y prueba a la vez.
- Un dato con retraso de publicación. En finanzas, el resultado de una empresa se publica semanas
  después del cierre del trimestre; usar la fecha del cierre es mirar al futuro.
- Duplicados. La misma fila, con un identificador distinto, en los dos conjuntos.

La buena noticia es que la fuga deja **huellas medibles**, y hay tres que se comprueban siempre:

1. **Un salto brusco de métrica.** Pasar de un AUC de 0,62 a 0,91 al añadir una variable no es
   un buen día: es un síntoma.
2. **Importancias raras.** Si una sola variable concentra casi toda la importancia del modelo, o
   si una columna que debería ser irrelevante aparece la primera, mira de dónde sale ese dato.
3. **Diferencia entre validación y producción.** Si el modelo funciona en el portátil y falla en
   el servidor, casi siempre es porque alguna variable no tiene el mismo valor (o no existe) en
   el momento real de la predicción.

## Definición formal

Sea `D` el conjunto de datos, `tᵢ` el instante en que se predice la fila `i` y `xᵢⱼ` el valor de
la variable `j` en esa fila. Decimos que **no hay fuga** si para toda fila `i` y toda variable
`j`:

:::formula
xᵢⱼ = fⱼ( D_{< tᵢ} )        y        θ̂ = g( D_entrenamiento )
:::

Es decir: cada variable se calcula **solo** con información disponible estrictamente antes del
instante de predicción `tᵢ`, y todos los parámetros aprendidos (medias de imputación, escalados,
codificaciones, coeficientes, hiperparámetros) se estiman **solo** con el conjunto de
entrenamiento. `fⱼ` es la función que construye la variable `j` a partir del pasado `D_{< tᵢ}`.

De ahí salen las tres condiciones que se comprueban en una auditoría:

- **Condición temporal.** `xᵢⱼ` no puede depender de nada ocurrido en `t ≥ tᵢ`.
- **Condición de separación.** Ningún parámetro ajustado puede haber visto las filas de prueba,
  ni directa ni indirectamente (medias, cuantiles, selección de variables, elección de
  hiperparámetros).
- **Condición de independencia.** Entrenamiento y prueba no pueden compartir entidad, paciente,
  cliente, sensor ni duplicado. Si comparten grupo, hay que partir por grupo
  (`GroupKFold`) o por tiempo ([[validacion-temporal|validación temporal]]).

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `tᵢ` | El instante en que se predice la fila `i` | tiempo (fecha, día, trimestre) | Cuanto más tarde se predice, más información existe en el mundo; el error es usar la de después. Lo que decide no es la fecha del hecho, sino la fecha en que el dato se conoce |
| `xᵢⱼ` | El valor de la variable `j` en la fila `i` | las de esa variable | Si solo puede calcularse mirando a `t ≥ tᵢ`, la variable entra en el modelo con la respuesta dentro |
| `D` | El conjunto de datos completo | filas × columnas | Es la tentación: cualquier estadístico calculado sobre `D` entero (media, cuantil, IQR) ya ha visto la prueba |
| `D_{< tᵢ}` | Todo lo conocido estrictamente antes de `tᵢ` | filas | Es el único material con el que se puede construir `xᵢⱼ`. Encogerlo es lo correcto; ampliarlo hasta `D` es la fuga |
| `fⱼ` | La función que construye la variable `j` a partir del pasado | — | Si `fⱼ` es un `rolling` sin `shift`, `fⱼ(D_{< tᵢ})` incluye en realidad `tᵢ` y la condición temporal se rompe sin que se note |
| `θ̂` | Todo parámetro aprendido: medias de imputación, escalados, codificaciones, coeficientes, hiperparámetros | las del parámetro | Un `θ̂` estimado con `D` entero en lugar de con `D_entrenamiento` transmite a las variables un resumen de la prueba, aunque el modelo no vea nunca una fila de prueba |
| `D_entrenamiento` | El subconjunto con el que se ajusta todo | filas | Cuanto más pequeño, más se nota la fuga: con 60 filas, una media calculada con las 60 mueve mucho la escala de las 12 de prueba |
| `AUC`, `accuracy`, `R²` | La métrica con la que te crees el modelo | adimensional (AUC, accuracy) o sin unidades (`R²`) | Un salto grande y sin explicación es el síntoma. En `R²`, bajar de 0 ya significa que el modelo es peor que predecir la media |
:::

:::figura
fichero: fuga-de-datos-cuatro-huellas
pie: Las cuatro huellas de la fuga, una por panel. Una columna calculada después del evento lleva la exactitud al 1,00 frente al 0,52 de la única señal legítima. Esa misma columna se lleva casi todo el peso del modelo y deja la señal real en 0,01. El valor 998 llega al modelo como 2,0 o como 444,1 según si el escalador se ajustó con las cinco filas o solo con las cuatro de entrenamiento: la fuga no solo infla la métrica, cambia lo que significa el dato. Y con un reparto barajado, cada punto de prueba queda rodeado de días que el modelo ya vio, así que acierta interpolando en lugar de extrapolar.
fuente: figuras/fuga-de-datos-1.py
:::

## Ejemplo

**Una variable calculada después del evento.** 500 filas, una variable legítima y otra que se
construye como `y` más un poco de ruido (como haría un proceso que se ejecuta después):

- Accuracy en prueba con la variable con fuga: **1,00**.
- Accuracy en prueba usando solo la variable legítima: **0,53**.

La segunda cifra es la verdadera capacidad predictiva: el 0,53 está a la altura del azar porque
esa variable no tenía relación con el objetivo. El 1,00 era la respuesta impresa detrás del
enunciado.

**Un escalado ajustado con todo el conjunto.** Cinco valores, uno de ellos extremo:

```
2   4   6   8   998
```

- Si el escalador se ajusta con los cinco, la media usada es **204** y el 998 se transforma en un
  z-score de **2,00**: parece un valor casi normal.
- Si se ajusta solo con los cuatro primeros (entrenamiento), la media es **5** y ese mismo 998
  se transforma en **444,08**.

El modelo entrenado con el primer escalado nunca vio un valor extremo: le llegó ya domesticado.
Y en producción, con el escalador correcto, ese mismo dato llegará como 444,08 y el modelo no
sabrá qué hacer. La fuga no solo infla la métrica: cambia el significado de la variable.

**Un reparto aleatorio en una serie temporal.** 300 días de una señal periódica, predicha con
KNN sobre el propio índice temporal:

- Con `KFold(shuffle=True)`: `R²` = **0,81**.
- Con cortes temporales consecutivos: `R²` = **−1,54**.

El primero es mentira: los días vecinos en el tiempo caen repartidos entre pliegues, así que el
modelo *interpola* entre puntos que ya ha visto. El segundo es la situación real, en la que hay
que *extrapolar* hacia delante, y ahí el modelo es peor que decir la media.

## Código

```python verificable
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(0)
n = 500
y = rng.integers(0, 2, n)                     # etiqueta binaria
senal = rng.normal(0, 1, n)                   # variable legitima, sin relacion con y
fuga = y + rng.normal(0, 0.1, n)              # calculada DESPUES de conocer y

X = np.column_stack([senal, fuga])
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)

con_fuga = LogisticRegression().fit(X_tr, y_tr)
sin_fuga = LogisticRegression().fit(X_tr[:, :1], y_tr)

print(f"accuracy con la variable con fuga   {accuracy_score(y_te, con_fuga.predict(X_te)):.2f}")   # -> 1.00
print(f"accuracy con la senal legitima sola {accuracy_score(y_te, sin_fuga.predict(X_te[:, :1])):.2f}")   # -> 0.53
```

:::claves
- `train_test_split(X, y, test_size=0.3, random_state=0)` devuelve cuatro objetos en el orden `X_train, X_test, y_train, y_test`. Si cambias el orden de las variables a la izquierda, el modelo se entrena con las etiquetas de prueba y no da error: da una métrica absurda. El `random_state` fija el reparto para que el 1,00 y el 0,53 sean siempre los mismos.
- `X_tr[:, :1]` es una **matriz** de una columna, no un vector. `X_tr[:, 0]` sería un vector de forma `(350,)`, y scikit-learn lo rechaza en el `fit` con «Expected 2D array, got 1D array instead»: hay que pasar siempre una matriz de dos dimensiones. El `:1` es lo que conserva esa segunda dimensión.
- `fuga = y + rng.normal(0, 0.1, n)` no es una variable: es la etiqueta con un poco de ruido. Por eso la exactitud sale 1,00. El detalle que engaña es que `fuga` **no es constante** y su coeficiente (unos 6,6) parece razonable si no miras de dónde sale.
- La comparación entre los dos modelos no es del todo justa y conviene saberlo: al modelo con fuga le pasas 2 columnas y al otro 1. La conclusión que aguanta es que la segunda columna es la que produce todo el acierto, no que un modelo con más columnas sea mejor.
- `accuracy_score(y_te, con_fuga.predict(X_te))` usa el umbral 0,5 por defecto sobre la probabilidad. Cambiar el umbral mueve la exactitud, así que dos modelos solo se comparan con el mismo umbral; y en un problema desbalanceado la exactitud por sí sola no dice nada (un modelo que siempre diga «no» acierta el 95 % si el 95 % de las filas son «no»).
- `LogisticRegression` tiene `penalty="l2"` y `C=1.0` por defecto, así que no ajusta por máxima verosimilitud pura: la penalización evita que los coeficientes se disparen con datos separables. `from sklearn.linear_model import LogisticRegression` tarda un par de segundos y el bloque entero se queda cerca del límite de 15 segundos en frío; si lo amplías, cuida ese margen.
- En el segundo bloque, `StandardScaler().fit(datos)` guarda `mean_` y `scale_`. Reutilizar ese mismo escalador ajustado en el entrenamiento para transformar la prueba es exactamente la fuga: `mal.transform(prueba)` da 2,00 y `bien.transform(prueba)` da 444,08 para el mismo 998. El número no cambió; cambió el modelo de referencia.
:::

```python verificable
import numpy as np
from sklearn.preprocessing import StandardScaler

# Escalar antes de dividir contamina: la media y la desviacion incluyen la prueba.
datos = np.array([[2.0], [4.0], [6.0], [8.0], [998.0]])
entrenamiento, prueba = datos[:4], datos[4:]

mal = StandardScaler().fit(datos)            # vio la fila de prueba
bien = StandardScaler().fit(entrenamiento)   # solo el entrenamiento

print(f"media usada con fuga {mal.mean_[0]:.0f}")    # -> 204
print(f"media usada sin fuga {bien.mean_[0]:.0f}")   # -> 5
print(f"prueba con fuga {mal.transform(prueba)[0, 0]:.2f}")    # -> 2.00
print(f"prueba sin fuga {bien.transform(prueba)[0, 0]:.2f}")   # -> 444.08
```

```python verificable
import numpy as np
from sklearn.model_selection import KFold, cross_val_score
from sklearn.neighbors import KNeighborsRegressor

rng = np.random.default_rng(0)
n = 300
t = np.arange(n).reshape(-1, 1)
y = np.sin(2 * np.pi * np.arange(n) / 50) + rng.normal(0, 0.3, n)

# Con KFold barajado, el vecino mas cercano en el tiempo cae casi siempre en el mismo pliego.
barajado = cross_val_score(KNeighborsRegressor(n_neighbors=5), t, y,
                           cv=KFold(5, shuffle=True, random_state=0)).mean()

# Con cortes consecutivos hay que extrapolar hacia delante, que es lo que pasa de verdad.
bloques = np.array_split(np.arange(n), 5)
temporal = np.mean([
    KNeighborsRegressor(n_neighbors=5).fit(t[:b[0]], y[:b[0]]).score(t[b[0]:], y[b[0]:])
    for b in bloques[1:]
])

print(f"R2 con KFold barajado    {barajado:.2f}")   # -> 0.81
print(f"R2 con cortes temporales {temporal:.2f}")   # -> -1.54
```

## Errores típicos

- **Ajustar cualquier preprocesamiento con todos los datos.** Medias de imputación, escalados,
  codificación por objetivo, selección de variables y también la elección de hiperparámetros.
  Todo eso se ajusta **dentro** de cada pliegue. Un [[pipelines-de-ml|pipeline]] con
  `fit`/`transform` bien puestos evita el 90 % de estos casos.
- **Usar variables que son consecuencia del objetivo.** «Número de reclamaciones», «días hasta
  la baja», «importe recuperado por el juzgado». Pregúntate siempre: el día que tengo que
  predecir, ¿este número ya existe? Si la respuesta es «existe porque ya pasó lo que quiero
  predecir», fuera.
- **Barajar en un problema con tiempo.** La validación cruzada normal mezcla pasado y futuro. En
  cuanto las filas están ordenadas en el tiempo o tienen [[autocorrelacion-acf-pacf|autocorrelación]],
  usa [[validacion-temporal|validación temporal]] o, si las etiquetas se solapan, un esquema con
  purga como [[purged-kfold|el k-fold con purga y embargo]].
- **Partir al azar cuando hay grupos.** El mismo paciente con 12 visitas repartidas entre
  entrenamiento y prueba hace que el modelo reconozca al paciente, no la enfermedad. Parte por
  paciente, por cliente o por dispositivo, nunca por fila.
- **Ignorar los duplicados.** Muchos datasets reales tienen la misma entidad repetida con otro
  identificador. Un `drop_duplicates` antes de dividir, o una comprobación de solapamiento por
  clave, es más barato que descubrirlo en producción.
- **Olvidar el retraso de publicación de los datos.** El dato existe en la fecha del hecho, pero
  se conoce más tarde. En finanzas y en sensores esto es sistemático: hay que desplazar cada
  variable al momento en que de verdad era conocida, no al momento en que ocurrió.
- **Usar el conjunto de prueba para decidir cuándo parar.** Mirar la métrica de prueba en cada
  iteración y quedarte con la mejor convierte el conjunto de prueba en un conjunto de validación
  encubierto. Guarda un conjunto final que solo mires una vez.

:::practica
enunciado: Tienes 1.000 filas, de las que 200 forman 100 pares de duplicados exactos. Repartes al azar el 70 % para entrenamiento y el 30 % para prueba. ¿Cuántos pares esperas que queden partidos entre los dos conjuntos y qué porcentaje de las 300 filas de prueba tendrá a su gemela exacta en entrenamiento?
pista: Cada par se parte cuando una fila cae en entrenamiento y la otra en prueba; hay dos órdenes posibles.
solucion: La probabilidad de que las dos filas del par caigan en lados distintos es 2 · 0,7 · 0,3 = 0,42. Con 100 pares, esperas 42 pares partidos, es decir 42 filas de prueba con su copia exacta en entrenamiento: el 42/300 = 14 % de la prueba. Esas filas se aciertan casi seguro y la métrica sale inflada. La solución es deduplicar antes de dividir o partir por clave.
:::

## Comprueba que lo sabes

:::quiz
p: Un modelo de impago incluye la columna «número de llamadas del departamento de cobros» y da un AUC de 0,95 en validación. ¿Qué sospecha primero?
o: Que el modelo es muy bueno y hay que desplegarlo cuanto antes
o: Que esa columna es consecuencia del impago y en el momento de conceder el crédito no existe
o: Que el AUC no sirve para problemas de impago
a: 2
e: Las llamadas de cobros ocurren porque el cliente no ha pagado, así que la variable contiene la respuesta. El día de la decisión de crédito vale cero para todo el mundo. Es fuga de datos por una variable construida después del evento, no un modelo excelente.
:::

:::quiz
p: Escalas las variables con todo el dataset y después haces una validación cruzada de 5 pliegues. ¿Por qué la métrica sale optimista?
o: Porque la media y la desviación usadas en cada pliegue contienen información de las filas de prueba
o: Porque la validación cruzada de 5 pliegues siempre exagera los resultados
o: Porque el escalado destruye la información de las variables
a: 1
e: Los estadísticos del escalador son parámetros aprendidos de los datos. Si se calculan antes de dividir, las filas de prueba participan en su estimación y el modelo dispone de un resumen del conjunto que se supone que no ha visto. La solución es ajustar el escalador solo con el entrenamiento de cada pliegue, que es lo que hace un pipeline bien montado.
:::

:::trampa
Si tu modelo va demasiado bien, el problema casi nunca es que hayas encontrado algo. Repasa por
este orden: variables calculadas después del evento, preprocesamiento ajustado con todo el
dataset, reparto aleatorio con tiempo o grupos, duplicados entre conjuntos. Cuatro comprobaciones
resuelven la mayoría de los casos.
:::
