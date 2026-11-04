---
id: entrenamiento-frente-a-inferencia
titulo: Coherencia entre entrenamiento e inferencia
fase: 6
nivel: avanzado
rutas: [ds, de]
prerequisitos: [train-val-test, pipelines-de-ml, fuga-de-datos, monitorizacion-de-drift]
tags: [mlops, produccion, pipeline, features]
resumen: Un modelo acierta en producción solo si el dato llega transformado igual que en el entrenamiento; la mitad de los fallos son de escala, no de algoritmo.
fuentes: ["Sculley et al. (2015), 'Hidden Technical Debt in Machine Learning Systems'", "Breck et al. (2017), 'The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction'", "Polyzotis et al. (2018), 'Data Lifecycle Challenges in Production Machine Learning'"]
---

## En una frase

Entrenar e inferir son dos caminos que tienen que producir **exactamente la misma
transformación** del dato bruto, y casi todos los fallos que se achacan al modelo son
diferencias entre esos dos caminos: otra media, otra escala, otra ventana, otro valor por
defecto o una variable que en producción no existe.

## La idea

Un modelo no ve la tabla: ve números ya transformados. Si entrenas con la superficie
estandarizada y sirves con la superficie en metros cuadrados, el modelo recibe valores en
torno a 120 donde esperaba valores en torno a 0, y responde una barbaridad. No ha dejado de
funcionar: le estás hablando otro idioma. Y al revés es igual de grave: con una sola petición
no hay desviación que calcular, así que la transformación ni siquiera existe.

Eso es el *training-serving skew*, y tiene una forma muy reconocible: **el modelo acierta en
la validación y se equivoca en producción siempre en la misma dirección**, como si estuviera
desplazado. En el ejemplo de esta página, ese desplazamiento vale 6,16 miles de euros por
piso: el nivel al que apunta el modelo se mueve porque la media que usa para centrar la
variable no es la del entrenamiento, sino la del lote que acaba de llegar.

La causa raíz es que el mismo cálculo vive en dos sitios:

- **En el entrenamiento** es un `fit_transform` dentro de un *notebook* o de un script, con
  todos los datos delante.
- **En producción** es una función que se ejecuta con un solo registro, o con un lote de 20,
  y que muchas veces se reescribió a mano «para que fuera rápido».

Cada detalle que se reescribe es una oportunidad de discrepancia. Los cinco más frecuentes:

1. **Media y desviación recalculadas con el lote actual.** Es el error del ejemplo. Si el
   lote es de un solo registro, la desviación es cero y la transformación deja de existir.
2. **Estadísticos escritos a mano.** Alguien copia `media = 100` de un cuaderno porque «era
   más o menos eso». Con una media real de 119,77, el modelo se desplaza 23,8 unidades en
   precio.
3. **Variables calculadas con el futuro.** Una media móvil centrada, un `groupby` del día
   completo o una imputación con la media del mes: en entrenamiento se pueden calcular porque
   el mes ya pasó; al servir, no existen. El modelo aprende una variable que en producción vale
   otra cosa ([[fuga-de-datos]]).
4. **Valores por defecto distintos.** En el entrenamiento, un nulo en la categoría de producto
   se rellena con `"desconocido"`; en producción, el servicio devuelve `null` y el modelo
   recibe un cero. La misma fila, dos entradas distintas.
5. **Universos distintos.** El entrenamiento se hizo con clientes de 2024 y el servicio atiende
   a los de 2026. Esto ya no es un fallo de coherencia sino de deriva, y se detecta de otra
   forma ([[monitorizacion-de-drift]]), pero se manifiesta igual: el modelo se equivoca.

La buena noticia es que la coherencia se puede **verificar**, no solo desear. Se comprueba
igual que se comprueba el código: con una prueba que toma un conjunto de filas conocidas,
calcula la transformación por los dos caminos y compara. Si los dos números no coinciden al
bit, el problema no está en el modelo.

:::figura
fichero: entrenamiento-inferencia-lote-y-escala
pie: La misma variable (superficie en metros cuadrados) transformada de dos formas. En azul, con la media y la desviación aprendidas en el entrenamiento; en naranja, recalculando esos estadísticos con el lote de peticiones que llega. La forma de las dos series es la misma porque la variable no ha cambiado: lo que cambia es la escala, y el modelo recibe otro número para la misma entrada. A la derecha, el desvío medio de la predicción según el tamaño del lote, en escala logarítmica: con lotes de 2 el desvío medio es 63,6 (y el máximo 242), con lotes de 100 baja a 13,5 y con 300 se queda en 6,2. Nunca llega a cero: quedarse en «casi» no es coherencia.
fuente: figuras/entrenamiento-frente-a-inferencia-1.py
:::

## Definición formal

Sea `x` una fila de datos brutos y `T` la transformación que se aplica antes del modelo.
Entrenamiento e inferencia son coherentes si existe una única `T` tal que:

:::formula
T_entrenamiento(x) = T_inferencia(x)    para toda fila x
:::

En la práctica, `T` casi nunca se escribe una sola vez. Se escribe como una cadena de pasos, y
la coherencia hay que exigirla paso a paso:

:::formula
z = (x − μ_entrena) / σ_entrena        con μ_entrena y σ_entrena fijos, calculados una vez
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube |
| --- | --- | --- | --- |
| `x` | El valor bruto de la variable tal como llega | las de la variable (m², euros) | Es el dato. Si su unidad cambia entre sistemas (metros frente a pies), la coherencia se rompe sin que nada falle |
| `μ_entrena` | Media de la variable calculada **solo con el conjunto de entrenamiento** | las de la variable | Centra la variable. Si en producción se recalcula con el lote, un lote cuya media esté más alta desplaza todas las predicciones en `β · (μ_lote − μ_entrena)` |
| `σ_entrena` | Desviación típica de la variable en el entrenamiento | las de la variable | Es la escala. Un `σ` mal puesto multiplica o divide todas las entradas: con `σ` un 20 % mayor, el modelo ve valores un 20 % más pequeños y responde como si la vivienda fuera más pequeña |
| `z` | El valor transformado que recibe el modelo | adimensional | Es lo que de verdad entra en el modelo. Comparar `z` en entrenamiento y en producción es la comprobación directa de coherencia |
| `n_lote` | Número de peticiones que se procesan juntas si se recalculan los estadísticos | recuento | Con `n_lote = 1`, `σ = 0` y la transformación se rompe. A medida que sube, el error baja como `1/√n_lote`, pero nunca desaparece |
| `β` | Coeficiente del modelo para esa variable | unidades del objetivo por unidad de la variable | Amplifica cualquier desplazamiento de la entrada. Un `β` grande convierte una discrepancia pequeña de escala en un error grande de predicción |
| `Δ` | Diferencia entre el valor transformado en producción y en entrenamiento para la misma fila | adimensional | Es la métrica de coherencia: debería ser 0 exacto. Se mide en un conjunto de control y se alerta si crece, igual que con cualquier otra métrica ([[calibracion]]) |
:::

Dos propiedades que conviene tener claras:

- **La coherencia no depende del modelo.** Se puede comprobar antes de entrenar nada: pasas
  un conjunto de filas de control por los dos caminos y comparas. Es una prueba de ingeniería,
  no de estadística.
- **Coherencia no es corrección.** Un modelo perfectamente coherente y mal entrenado seguirá
  equivocándose, pero siempre de la misma forma y con un error que puedes medir. La
  incoherencia, en cambio, hace que el error en producción no se parezca al de validación, y
  entonces no puedes diagnosticar nada.

## Ejemplo

Mil viviendas con superficie generada como lognormal y precio `1,2 · superficie + ruido` de
desviación 8. Se entrenan los primeros 700 registros y se sirven los 300 últimos. Los
estadísticos del entrenamiento son `μ = 119,7723` y `σ = 69,7077`, y el modelo lineal
aprende `precio = 144,2564 + 83,8899 · z`, donde `z` es la superficie estandarizada.

Servido con los estadísticos guardados, el error absoluto medio sobre las 300 viviendas nuevas
es de **6,646** miles de euros, en línea con el ruido del 8 que se inyectó.

Ahora el error clásico, el mismo modelo pero centrando con la media del lote que llega. La
media de esas 300 viviendas es 114,6565, así que:

- Desplazamiento del centro: `(114,6565 − 119,7723) / 69,7077 = −0,0734` desviaciones.
- Desplazamiento de la predicción: `83,8899 · (−0,0734) = −6,16` miles de euros. Todas las
  predicciones se van 6,16 miles por debajo, y el error absoluto medio sube de 6,646 a 9,264.
- Para la misma vivienda de 100 m², el modelo entrenado predice `144,2564 + 83,8899 · (100 −
  119,7723) / 69,7077 = 120,46`, que es una predicción razonable (la relación real da 120,00).
  Con los estadísticos del lote, esa misma vivienda entra como `(100 − 114,6565) / σ_lote`, un
  número distinto: la entrada ha cambiado, no el modelo.

Y no es un problema de tener pocos datos: el desvío se encoge con el tamaño del lote, pero no
se anula.

| Tamaño del lote | Desvío medio de la predicción | Desvío máximo |
| --- | --- | --- |
| 2 | 63,62 | 242,17 |
| 5 | 37,32 | 119,38 |
| 20 | 19,30 | 31,52 |
| 100 | 13,50 | 19,52 |
| 300 | 6,16 | 6,16 |

Léelo al revés: incluso con lotes de 300, sigues sirviendo predicciones que dependen de qué
otras viviendas cayeron en el mismo lote. Dos peticiones idénticas pueden recibir respuestas
distintas según con quién viajen, y eso es imposible de explicar a quien usa el modelo. La
caída no es monótona (con 150 el desvío medio es 9,18 y con 200 sube a 13,42) porque el
número de lotes completos que caben en la muestra cambia con el tamaño: es ruido de muestreo,
no una propiedad del método.

## Código

```python verificable
import numpy as np

# 1000 viviendas: superficie lognormal y precio = 1.2 * superficie + ruido
azar = np.random.default_rng(3)
n = 1000
area = azar.lognormal(4.6, 0.55, n)
precio = 1.2 * area + azar.normal(0.0, 8.0, n)
corte = 700

# Los estadisticos se calculan SOLO con el entrenamiento y se guardan con el modelo
media, desviacion = area[:corte].mean(), area[:corte].std()
z = (area - media) / desviacion

# El modelo se entrena sobre la variable ya estandarizada
ejes = np.column_stack([np.ones(corte), z[:corte]])
pesos = np.linalg.lstsq(ejes, precio[:corte], rcond=None)[0]
print("pesos: %.4f y %.4f" % (pesos[0], pesos[1]))
# -> pesos: 144.2564 y 83.8899
print("media del entrenamiento %.4f  desviacion %.4f" % (media, desviacion))
# -> media del entrenamiento 119.7723  desviacion 69.7077

# --- Camino correcto: al servir se usan los estadisticos guardados ------------
z_ok = z[corte:]
pred_ok = pesos[0] + pesos[1] * z_ok
print("MAE con los estadisticos del entrenamiento %.3f"
      % np.mean(np.abs(precio[corte:] - pred_ok)))
# -> MAE con los estadisticos del entrenamiento 6.646

# --- El error: al servir se recalculan con el lote que llega ------------------
media_lote = area[corte:].mean()
print("media del lote %.4f  desplazamiento %.2f desviaciones  %.2f de precio"
      % (media_lote, (media_lote - media) / desviacion,
         pesos[1] * (media_lote - media) / desviacion))
# -> media del lote 114.6565  desplazamiento -0.07 desviaciones  -6.16 de precio
z_mal = (area[corte:] - media_lote) / area[corte:].std()
pred_mal = pesos[0] + pesos[1] * z_mal
print("MAE con los estadisticos del lote %.3f" % np.mean(np.abs(precio[corte:] - pred_mal)))
# -> MAE con los estadisticos del lote 9.264
```

:::claves
- `area[:corte].mean()` y `area[corte:].mean()` son **estadísticos distintos**, y esa diferencia es todo el problema. La regla que lo evita: el `fit` de cualquier transformación se hace una sola vez, con datos de entrenamiento, y lo que se guarda con el modelo es el objeto ajustado, no los datos.
- `np.linalg.lstsq` sin estandarizar da **las mismas predicciones** que con la variable estandarizada: los coeficientes cambian por completo (`144,2564` y `83,8899` frente a `0,1228` y `1,2035`), pero la recta es la misma. Por eso el ordenador no detecta el error de escala: el modelo es correcto, la entrada no.
- La estandarización no es obligatoria para un modelo lineal, pero sí para casi todo lo demás: regularización, K-vecinos, redes y k-medias miden distancias, y sin la misma escala en producción las distancias cambian de significado ([[escalado-y-transformacion]]).
- `precio[:corte]` solo aparece en el ajuste y `precio[corte:]` solo en la evaluación. Si mezclas los dos en el mismo `fit`, la métrica deja de medir lo que crees ([[train-val-test]]).
- El desplazamiento de nivel `β · (μ_lote − μ_entrena)` tiene signo: aquí el lote es más barato que el entrenamiento, así que el modelo se queda corto. En un lote con viviendas más grandes, el error cambia de signo y las dos métricas que compares pueden parecer mejores sin serlo.
:::

```python verificable
import numpy as np

# Comparar el mismo dato transformado por los dos caminos: la prueba de coherencia
media, desviacion = 119.7723, 69.7077        # guardados con el modelo
control = np.array([80.0, 100.0, 119.7723, 150.0, 220.0])
z_entrenamiento = (control - media) / desviacion
z_produccion = (control - media) / desviacion       # misma funcion, mismos numeros
print("diferencia maxima %.2e" % np.max(np.abs(z_entrenamiento - z_produccion)))
# -> diferencia maxima 0.00e+00

# La version que falla: la constante escrita a mano en el servicio
otra_media = 100.0
z_mal = (control - otra_media) / desviacion
print("desplazamiento por variable %.4f" % np.max(np.abs(z_entrenamiento - z_mal)))
# -> desplazamiento por variable 0.2836
print("z correcto de 100 m2 %.4f   z con la media a mano %.4f"
      % (z_entrenamiento[1], z_mal[1]))
# -> z correcto de 100 m2 -0.2836   z con la media a mano 0.0000
```

:::claves
- Una prueba de coherencia **no necesita datos reales**: basta con un vector de valores de control que cubra el rango, incluidos los extremos y el cero. Si la diferencia no es exactamente 0, tienes un fallo antes de tocar el modelo.
- La media a mano (100) hace que la vivienda de 100 m² se transforme a `z = 0`, justo el valor neutro. Es el tipo de error que **mejora** las predicciones para las viviendas que están cerca de la constante equivocada y las destroza para el resto: por eso sobrevive tanto tiempo sin que nadie lo note.
- `np.max(np.abs(...))` da el peor caso; para vigilar en producción interesa más la media y el percentil 99 de `Δ` a lo largo del tiempo. Una diferencia que no es 0 pero se mantiene estable se puede tolerar; una que crece, no.
- Esta prueba cabe en el arranque del servicio: si el vector de control no reproduce los valores guardados, el despliegue se rechaza. Es más barato que descubrirlo con las predicciones ya servidas ([[ci-cd]]).
:::

## Errores típicos

- **Recalcular los estadísticos con el lote de producción.** Es el fallo central de esta
  página. Con una petición por lote, la desviación es cero; con lotes pequeños, la predicción
  depende de qué otras peticiones viajaron juntas. La transformación se ajusta una vez y se
  guarda con el modelo.
- **Reescribir la transformación en el servicio.** Dos implementaciones de lo mismo acaban
  divergiendo: una redondea, la otra no; una rellena los nulos con 0, la otra con la mediana.
  Si no se puede compartir el código, comparte al menos las constantes y añade una prueba que
  compare los dos caminos con un vector de control ([[pipelines-de-ml]]).
- **Entrenar con variables que en producción no existen.** Agregados del día, medias móviles
  centradas, variables calculadas después del cierre: en el entrenamiento se calculan sin
  esfuerzo porque el periodo ya terminó. En producción hay que calcularlas con lo que se sabe
  en ese instante, y suelen valer otra cosa ([[fuga-de-datos]], [[ingenieria-de-features]]).
- **Confundir coherencia con rendimiento.** Un modelo coherente puede tener un error enorme si
  el mundo cambió. La deriva se mide con la distribución de las variables y de los residuos;
  la coherencia, con la diferencia entre las dos transformaciones. Son dos alarmas distintas y
  se disparan por motivos distintos ([[monitorizacion-de-drift]]).
- **Dar por hecho que el mismo dato significa lo mismo en los dos sitios.** La variable
  «importe» puede estar en euros con IVA en el entrenamiento y en euros sin IVA en el
  servicio. La transformación es idéntica; el dato, no. La coherencia incluye las unidades y
  las definiciones.
- **No versionar la transformación.** Si guardas solo los coeficientes del modelo y recalculas
  la media cada vez que arranca el servicio, estás entrenando y sirviendo con dos
  transformaciones aunque el código sea el mismo ([[mlops-y-cicd-de-modelos]]).
- **Validar con el mismo camino que el entrenamiento.** Una validación dentro del *notebook*
  usa la misma función que el `fit`, así que no puede detectar la discrepancia. Hay que probar
  el camino de producción, con su código, aunque sea incómodo ([[pipelines-de-ml]]).

:::practica
enunciado: Un modelo de riesgo se entrenó estandarizando el ingreso mensual con media 2.400 y desviación 900. En producción, el servicio calcula la media del lote de solicitudes del día: hoy son 20 solicitudes con media 3.150. El coeficiente del ingreso estandarizado es 0,42 (en unidades de probabilidad logarítmica). Calcula el desplazamiento del nivel y decide si la predicción de hoy es comparable con la de ayer.
pista: El desplazamiento es `β · (μ_lote − μ_entrena) / σ_entrena`, porque la variable que entra en el modelo ya está estandarizada.
solucion: El desplazamiento es `0,42 · (3.150 − 2.400) / 900 = 0,42 · 0,8333 = 0,35`. En escala logarítmica, 0,35 equivale a multiplicar las probabilidades por `e^0,35 = 1,42` y a sumar unos 8,7 puntos porcentuales en una probabilidad base del 50 %. Las predicciones de hoy no son comparables con las de ayer: no porque el riesgo haya cambiado, sino porque el lote de hoy tiene ingresos más altos y el servicio usó esa media como referencia. La corrección es guardar con el modelo la media 2.400 y la desviación 900 y no recalcularlas nunca; si se sospecha que la población cambió, eso se mide aparte, con la distribución de los ingresos y no dentro de la transformación.
:::

## Comprueba que lo sabes

:::quiz
p: Un modelo acierta en validación y en producción se equivoca siempre en la misma dirección. Se comprueba que las variables de entrada son las mismas que en el entrenamiento. ¿Cuál es la causa más probable?
o: El modelo está sobreajustado y hay que regularizar más
o: La transformación aplicada en producción no es la misma: suele ser un estadístico recalculado con el lote o una constante escrita a mano
o: El conjunto de validación estaba mal separado y el error real es mayor
a: 2
e: Un error sistemático en la misma dirección apunta a un desplazamiento de la entrada, no a varianza del modelo. Si la media o la desviación que se usan para centrar y escalar se recalculan en producción, todas las predicciones se mueven en bloque con un desplazamiento `β · (μ_producción − μ_entrenamiento)`. El sobreajuste produce errores grandes en casos raros, no un sesgo constante en todos.
:::

:::quiz
p: ¿Por qué es mala idea normalizar cada petición con su propia media y desviación?
o: Porque el modelo recibe valores distintos según con qué otras peticiones se agrupe, y con una sola petición la desviación es cero
o: Porque es más lento que usar estadísticos guardados
o: Porque el modelo deja de ser lineal
a: 1
e: La coherencia exige que la misma entrada produzca la misma transformación, y eso no se cumple si los estadísticos vienen del lote. Con un lote de un solo registro, la desviación es cero y la transformación no está definida. El problema no es de velocidad ni de linealidad: es que dos peticiones idénticas pueden recibir predicciones distintas.
:::

:::quiz
p: Un modelo usa como variable el promedio del gasto del cliente en el último mes. En entrenamiento, el mes ya había terminado cuando se construyó la variable. ¿Qué riesgo tiene al servir?
o: Ninguno, si la transformación es idéntica en los dos caminos
o: Que en producción solo se puede calcular con el gasto transcurrido hasta hoy, así que la variable vale otra cosa y el modelo recibe una entrada distinta
o: Que el gasto se mide en otra unidad en producción
a: 2
e: La coherencia de la transformación no basta si la variable no se puede reproducir en el momento de servir. El promedio del último mes es un dato del futuro en mitad del mes; en producción hay que usar el gasto acumulado hasta el instante de la predicción, que es una variable distinta. Esto es una fuga de datos que se manifiesta como una caída de rendimiento al desplegar.
:::

:::aviso
La coherencia se puede automatizar casi por completo: guarda el objeto de transformación
ajustado junto al modelo (no los datos), expón una única función de transformación para
entrenamiento y servicio, y añade una prueba con un vector de control que falle el despliegue
si las dos rutas no dan el mismo número. Es trabajo de una tarde y elimina la familia de
fallos más difícil de diagnosticar, porque cuando el modelo recibe otra escala no hay ningún
error, solo predicciones malas.
:::
