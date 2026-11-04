---
id: mlops-y-cicd-de-modelos
titulo: MLOps y CI/CD de modelos
fase: 4
nivel: avanzado
rutas: [ds, de]
prerequisitos: [train-val-test, pipelines-de-ml]
tags: [mlops, despliegue, versionado, cicd]
resumen: Versionar código, datos, entorno y semilla; validar los datos antes de entrenar y promover un modelo solo si su mejora supera el ruido de la medición.
fuentes: ["Sculley et al. (2015), 'Hidden Technical Debt in Machine Learning Systems'", "Breck et al. (2017), 'The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction'"]
---

## En una frase

MLOps es aplicar a los modelos lo que la ingeniería de software ya hace con el código —versionar,
probar, desplegar de forma gradual y poder revertir— sabiendo que aquí hay **cuatro** cosas que
versionar, no una: el código, los datos, el entorno y la semilla.

## La idea

Una cadena de restaurantes tiene un problema cuando un cliente se intoxica: hay que saber **qué
receta** se usó, **qué lote de ingredientes** entró en la cocina, **qué horno** y con **qué
ajustes**. Si la respuesta es «la receta de siempre, con ingredientes normales», no puedes
arreglar nada ni evitar que vuelva a pasar.

Un modelo en producción es igual. Cuando un modelo empieza a dar predicciones malas, la pregunta
es siempre la misma y tiene cuatro respuestas posibles:

1. **El código cambió.** Alguien tocó el preprocesado y ya no es el mismo pipeline.
2. **Los datos cambiaron.** El mundo se movió: ver [[monitorizacion-de-drift|deriva de datos y
   de concepto]].
3. **El entorno cambió.** Otra versión de la librería (una versión nueva de la misma librería de
   árboles puede dar resultados distintos con los mismos datos y la misma semilla).
4. **La semilla cambió.** La partición de entrenamiento y prueba se generó con otra semilla, y
   el modelo aprendió con datos distintos.

Sin versionar las cuatro, no puedes distinguir «el modelo ha empeorado» de «he medido otra
cosa». Y esa confusión es la causa número uno de discusiones interminables en equipos de datos.

Sobre esa base se montan las dos mitades:

**Integración continua (CI).** Cada cambio en el repositorio pasa por: pruebas de código,
**validación de datos** (esquema, rangos, nulos, cardinalidad, distribución frente al histórico),
un entrenamiento de humo con una muestra pequeña y una **puerta de evaluación**: el modelo
candidato se compara con el que está en producción y solo pasa si mejora lo suficiente. Si no
hay datos disponibles en CI, se usan datos sintéticos o una muestra versionada; lo que no se
puede hacer es no probar.

**Despliegue continuo (CD).** El artefacto que sale de CI es inmutable y va al **registro de
modelos** con su versión, sus métricas y la huella de todo lo que lo produjo. Desde ahí se
despliega, y el despliegue no es un salto al vacío: **sombra** (el modelo nuevo predice en
paralelo sin afectar a nadie), **canario** (un porcentaje pequeño de tráfico real), **azul-verde**
(dos versiones completas y un conmutador). Y siempre con una **vuelta atrás** probada: revertir
significa volver a la versión anterior, que tiene que seguir existiendo y siendo compatible con
las variables que se calculan en producción.

Hay una parte que se salta casi siempre y que es la que más devuelve el tiempo invertido:
**definir la puerta de promoción antes de medir**. Si primero entrenas, ves el resultado y luego
decides si merecía la pena, no tienes un criterio: tienes una justificación.

## Definición formal

- **Artefacto reproducible:** `modelo = entrenar(código, datos, entorno, semilla)`. Cualquiera de
  los cuatro puede cambiar la salida; los cuatro llevan versión y huella.
- **Huella del modelo:** resumen criptográfico de la terna `(hash de datos, hiperparámetros,
  hash del código)` que identifica de forma única una ejecución de entrenamiento.
- **Puerta de promoción:** condición medible que el candidato debe cumplir para pasar a
  producción. Por ejemplo: `métrica(candidato) < métrica(producción) − δ`, con `δ` mayor que el
  ruido de la medición.
- **Ruido de la medición:** dispersión de la métrica debida a la partición de datos, a la
  semilla y al muestreo. Se estima repitiendo la evaluación con varias semillas y tomando la
  desviación típica entre ejecuciones.
- **Canario:** fracción `p` del tráfico (típicamente 1-5 %) que recibe la versión nueva mientras
  el resto sigue con la anterior. Se compara la métrica de negocio de ambos grupos antes de
  subir `p`.

:::formula
modelo = f(código, datos, entorno, semilla)
promover si  métrica(candidato) < métrica(producción) − ruido
huella = hash(hash_datos + hiperparámetros + hash_código)
:::

## Ejemplo

Un modelo de regresión con 300 filas y 6 variables. El mismo código, los mismos datos y el mismo
hiperparámetro; lo único que cambia es la **semilla de la partición** entrenamiento/prueba:

| Semilla | MAE en prueba |
| --- | --- |
| 0 | 13,86 |
| 1 | 13,43 |
| 2 | 12,23 |

La diferencia entre la mejor y la peor es de **1,63**, y solo por haber barajado las filas de
otra manera. La conclusión práctica es inmediata: si tu candidato mejora el MAE en **0,4** y lo
promueves, no has mejorado el modelo, has elegido una semilla afortunada. Ese 0,4 desaparece en
la siguiente ejecución.

La regla que sale de este ejemplo: **mide el ruido antes de fijar la puerta**. Repite la
evaluación con 5 semillas, mira la dispersión y pon el umbral `δ` por encima. Si el ruido es
1,6, necesitas una mejora bastante mayor que 1,6 para creerte algo — y si ninguna mejora llega
a ese tamaño, el problema probablemente no se resuelve con otro modelo, sino con mejores
variables o mejores datos.

El otro ejemplo es la huella. Dos ejecuciones con los mismos datos y el mismo código pero con
`alpha = 1,0` y `alpha = 1,1` producen huellas **ad1c8b5578dcdc98** y **befc8d3137384312**: dos
artefactos distintos, dos entradas distintas en el registro, dos cosas que se pueden comparar y
volver a producir. Sin la huella, «el modelo de la semana pasada» no significa nada.

## Código

```python verificable
# El ruido de la medicion: mismo codigo, mismos datos, distinta semilla de particion.
from sklearn.datasets import make_regression
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

X, y = make_regression(n_samples=300, n_features=6, noise=15.0, random_state=7)

for semilla in (0, 1, 2):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=semilla)
    mae = mean_absolute_error(y_te, Ridge(alpha=1.0).fit(X_tr, y_tr).predict(X_te))
    print(f"semilla {semilla}: MAE {mae:.2f}")
# -> semilla 0: MAE 13.86
# -> semilla 1: MAE 13.43
# -> semilla 2: MAE 12.23
```

```python verificable
# La huella del modelo: datos + hiperparametros + codigo identifican una ejecucion.
import hashlib, json

def huella(hash_datos, params, hash_codigo):
    carga = json.dumps({"datos": hash_datos, "params": params, "codigo": hash_codigo}, sort_keys=True)
    return hashlib.sha256(carga.encode()).hexdigest()[:16]

base = {"alpha": 1.0, "fit_intercept": True}
print("huella alpha 1.0:", huella("a1b2", base, "c3d4"))                    # -> huella alpha 1.0: ad1c8b5578dcdc98
print("huella alpha 1.1:", huella("a1b2", {**base, "alpha": 1.1}, "c3d4"))  # -> huella alpha 1.1: befc8d3137384312
```

## Errores típicos

- **Versionar el código y no los datos ni la semilla.** Es el fallo más común y el más caro: el
  mismo `git checkout` no reproduce el modelo porque los datos de entrenamiento ya no son los
  mismos. Versiona la partición (o al menos su hash) junto al modelo.
- **Promover por una mejora más pequeña que el ruido.** Un 0,4 de mejora cuando la semilla mueve
  la métrica 1,6 no es una mejora: es azar. Fija el umbral después de medir la dispersión.
- **No conservar el modelo anterior.** Sin la versión previa y su entorno, la vuelta atrás es una
  promesa, no un plan. Revertir tiene que ser un despliegue, no una reconstrucción.
- **Entrenar con un pipeline de variables y servir con otro.** La misma variable calculada de dos
  formas (una ventana de 7 días en entrenamiento, de 30 en producción) hunde el modelo sin lanzar
  ningún error. Se resuelve con un [[feature-store|almacén de variables]] o, como mínimo,
  reutilizando literalmente el mismo código de transformación en los dos lados.
- **Probar el código y no los datos.** Los tests verifican que la función suma bien, pero nadie
  comprueba que la columna `importe` llegó con el 40 % de nulos. La validación de datos en CI es
  parte del pipeline, no un extra; ver [[calidad-de-datos|calidad de datos]].
- **Dejar las dependencias sin fijar.** Un `requirements.txt` con versiones abiertas convierte el
  entorno en una variable no controlada: la reconstrucción de mañana puede no ser la de hoy. Fija
  versiones exactas y reconstruye la imagen ([[docker-para-datos|Docker]]) en cada despliegue.

## Comprueba que lo sabes

:::quiz
p: Tu candidato mejora el MAE de 14,2 a 13,8 (0,4 de mejora). Repitiendo el entrenamiento con otras semillas, el MAE oscila entre 12,2 y 13,9. ¿Qué haces?
o: Promoverlo, porque 0,4 es una mejora medible
o: No promoverlo con ese criterio: la mejora es menor que el ruido de la partición, así que hay que exigir un umbral mayor o mejorar los datos o las variables
o: Promoverlo solo si el modelo nuevo es más complejo que el anterior
a: 2
e: La dispersión por semilla (1,7) es mayor que la mejora (0,4): el resultado es indistinguible de haber elegido una partición afortunada. La puerta de promoción debe fijarse por encima del ruido medido, y si ninguna mejora lo supera, el problema no está en el algoritmo.
:::

:::quiz
p: ¿Por qué no basta con versionar el código del modelo?
o: Porque el modelo también cambia si cambian los datos de entrenamiento, la versión de las librerías o la semilla de la partición
o: Porque el código de un modelo nunca se puede reproducir
o: Porque las métricas del modelo no dependen del código
a: 1
e: El modelo es la salida de cuatro entradas: código, datos, entorno y semilla. Cambiar cualquiera de ellas cambia el artefacto. Versionar solo el código deja tres variables libres y hace imposible explicar por qué el modelo de hoy no se comporta como el de ayer.
:::

:::aviso
La mayoría del código de un sistema de machine learning no es el modelo. Alrededor del núcleo de
entrenamiento hay validación de datos, ingeniería de variables, configuración, monitorización,
automatización y herramientas de operación, y esa es la parte que se lleva el mantenimiento. Si
solo has probado y versionado el entrenamiento, has cubierto la parte pequeña del problema.
:::
