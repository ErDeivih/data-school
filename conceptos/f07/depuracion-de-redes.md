---
id: depuracion-de-redes
titulo: Depurar el entrenamiento
fase: 7
nivel: avanzado
rutas: [ds]
prerequisitos: [sobreajuste-en-redes, retropropagacion, funciones-de-perdida, tasas-de-aprendizaje-y-schedulers]
tags: [deep-learning, depuracion, gradientes, entrenamiento]
resumen: Perdidas que no bajan, perdidas que son NaN y modelos que solo aprenden un lote: el método para aislar cada fallo con comprobaciones baratas.
fuentes: ["Goodfellow, Bengio y Courville (2016), 'Deep Learning', cap. 8", "Karpathy (2019), 'A Recipe for Training Neural Networks'"]
---

## En una frase

Depurar una red no es leer el código entero con lupa: es ir descartando sospechosos con
comprobaciones que cuestan segundos, empezando por la que más descarta, que es intentar
memorizar un lote de ocho ejemplos.

## La idea

Un fallo de entrenamiento tiene cientos de causas posibles: la tasa de aprendizaje, una capa
mal conectada, etiquetas desalineadas, un `log(0)`, una pérdida que no corresponde a la tarea,
un tensor en el dispositivo equivocado, datos sin escalar. Buscar a ciegas es desesperante
porque casi todas producen el mismo síntoma: «la pérdida no baja».

La forma de salir es **reducir el espacio de búsqueda con experimentos que sabes de antemano
cómo deben salir**. En lugar de preguntar «¿por qué no aprende?», preguntas «¿es capaz de
aprender algo trivial?». Si la respuesta es no, el problema está en el código. Si es sí, el
problema está en los datos o en el régimen de entrenamiento. Esa única pregunta parte el
problema en dos mitades.

La escalera de comprobaciones, de más barata y más informativa a más específica:

1. **Fija la semilla y reproduce el fallo.** Si el fallo aparece y desaparece entre
   ejecuciones, el problema es de inicialización o de datos, no de arquitectura. Y sin
   reproducibilidad no puedes comprobar si un cambio arregló algo.
2. **Comprueba la pérdida inicial.** Un clasificador de `C` clases balanceadas, con logits casi
   nulos, debe arrancar en `ln C`. Nueve clases: 2,20. Mil clases: 6,91. Si arranca en 0,05,
   las etiquetas se están filtrando por algún sitio. Si arranca en 30, la capa de salida está
   produciendo logits enormes.
3. **Intenta memorizar un lote diminuto.** Coge 8 o 16 ejemplos, quita toda la regularización,
   sube la tasa de aprendizaje y entrena 500 épocas. Con más parámetros que ejemplos, la
   pérdida debe quedar cerca de cero. Si no baja de `ln C`, tienes un error de código:
   gradientes que no llegan, pérdida mal emparejada con las etiquetas, datos y etiquetas
   desordenados entre sí.
4. **Añade una pieza cada vez.** Con el lote memorizado, pasa al conjunto completo y comprueba
   que la pérdida baja. Luego añade el aumento de datos, luego la regularización, luego la
   arquitectura. El primer paso que rompe el entrenamiento es el culpable.
5. **Solo entonces mira los datos.** Errores de etiquetado, clases desbalanceadas, variables sin
   escalar y duplicados se ven mucho mejor después de saber que el código está bien.

Para las pérdidas NaN hay un triaje propio, porque no es lo mismo un NaN desde el primer paso
que uno en la época 4.000:

- **NaN en el primer lote:** casi siempre `log(0)` o `sqrt` de un número negativo, división por
  una desviación de cero, o una pérdida que recibe logits en vez de probabilidades.
- **NaN tras unos cientos de pasos:** gradientes que explotan por una tasa de aprendizaje alta
  o por una pérdida mal normalizada (sumar en vez de promediar). Se diagnostica recortando la
  norma del gradiente y bajando la tasa un orden de magnitud.
- **NaN solo con precisión mixta:** desbordamiento en `float16` al calcular la pérdida. La
  pérdida se calcula siempre en `float32` y se compensa la escala.

La regla que resume todo: **si no puedes hacer que el modelo sobreajuste a un lote, no tienes un
problema de generalización; tienes un bug.**

:::figura
fichero: depuracion-memorizar-y-arranque
pie: A la izquierda, el test de memorización sobre 8 ejemplos: la pérdida arranca en ln 2 = 0,6931 (que es lo que vale no saber nada en un problema de dos clases) y baja dos órdenes de magnitud hasta 0,0088. Esa caída es la prueba de que el bucle de entrenamiento, los gradientes y el emparejamiento de datos y etiquetas funcionan; si la curva se quedara plana en 0,63, el fallo estaría en el código y no habría que tocar ni los datos ni los hiperparámetros. A la derecha, el otro valor de referencia: la pérdida del primer paso de un clasificador con `C` clases equiprobables es `ln C`, y crece muy despacio. Un arranque muy por debajo de esa línea delata etiquetas filtradas o mal emparejadas, y uno muy por encima (el punto rojo, 6,58 con 10 clases) delata una capa de salida mal escalada.
fuente: figuras/depuracion-de-redes-1.py
:::

## Definición formal

Sea `L(θ)` la pérdida media del modelo con parámetros `θ` y `g = ∇_θ L(θ)` su gradiente.

**Pérdida inicial de referencia.** Para un clasificador con `C` clases equiprobables y logits
nulos, la [[funciones-de-perdida|entropía cruzada]] media vale:

:::formula
L₀ = −(1/n) · Σᵢ ln(1/C) = ln C
:::

- `C` — número de clases.
- `n` — número de ejemplos del lote.
- `ln C` — el valor de referencia: 2,30 con 10 clases, 6,91 con 1.000.

Cualquier desviación grande de `ln C` en el primer paso tiene una causa concreta: si es mucho
menor, las etiquetas están correlacionadas con la salida (fuga, o has pasado probabilidades en
vez de logits); si es mucho mayor, los logits tienen una escala desproporcionada.

**Test de memorización.** Con `n` ejemplos y una red cuya capacidad efectiva supera `n`, existe
una configuración de parámetros con pérdida casi nula sobre ese lote. La comprobación es
empírica: entrena con regularización desactivada y observa si `L` cae por debajo de 0,01. Si no
cae, el fallo es de implementación.

**Recorte por norma del gradiente.** Se sustituye `g` por:

:::formula
g ← g · min(1, τ / ‖g‖₂)
:::

- `‖g‖₂` — la norma euclídea del gradiente, es decir `√(Σₖ gₖ²)` sobre todos los parámetros.
- `τ` — el umbral (típicamente 1 a 5). Si la norma ya es menor que `τ`, no se toca nada.
- La dirección del gradiente no cambia; solo su longitud. Por eso el recorte estabiliza sin
  alterar hacia dónde se mueve el modelo.

**Detección de valores no finitos.** Un `NaN` se propaga por toda la suma y por toda la
retropropagación: si `x ≠ x`, es `NaN`. La comprobación `np.isfinite(L)` sobre la pérdida es
más barata que cualquier depuración posterior, y lo correcto es abortar el paso antes de
aplicarlo a los pesos.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `C` | Número de clases del clasificador | recuento | Sube el listón de la pérdida inicial, pero muy despacio: `ln C` vale 2,30 con 10 clases, 4,61 con 100 y 6,91 con 1.000. La consecuencia práctica es que con muchas clases una pérdida inicial «baja» es más sospechosa todavía: con 0,04 solo puede pasar si ya hay fuga de información |
| `L₀` | Pérdida del primer paso con logits casi nulos | las de la pérdida | Es la referencia contra la que se compara, no una palanca. Al alejarte de ella, el diagnóstico está claro: por debajo, etiquetas correlacionadas con la salida o probabilidades pasadas donde se esperan logits; por encima, logits con escala desproporcionada |
| `n` | Número de ejemplos del lote que se intenta memorizar | recuento | Con `n` pequeño (8 o 16) el test es concluyente: la red tiene más parámetros que ejemplos y la pérdida debe acercarse a cero. Si subes `n` hasta acercarlo al número de parámetros, el test deja de discriminar y un fallo real puede pasar por dificultad del problema |
| `θ` | Todos los parámetros del modelo | las de cada peso | Es lo que se mueve. La comprobación `np.isfinite` sobre la pérdida se hace **antes** de aplicar el paso: si aplicas un paso con `NaN`, todos los pesos pasan a `NaN` y a partir de ahí no hay forma de saber en qué paso se originó |
| `g` | Gradiente de la pérdida respecto de los parámetros | las de la pérdida partido por las del parámetro | Es lo que mueve los pesos. Su norma es la que se recorta: con norma 335,54 y umbral 5, un paso de descenso sin recortar lleva los pesos a una zona donde la pérdida es arbitraria, y ese es el mecanismo habitual detrás del primer `NaN` tardío |
| `‖g‖₂` | Norma euclídea del gradiente: `√(Σ gₖ²)` | las de `g` | Al subir, el paso de descenso es más largo y el entrenamiento más inestable. Es el número que se vigila: una norma que crece época tras época anuncia el `NaN` antes de que llegue |
| `τ` | Umbral de recorte de la norma del gradiente | las de `‖g‖₂` | Si la norma ya es menor que `τ`, no se toca nada; si es mayor, el paso se acorta hasta `τ` conservando la dirección. Al subir `τ` el recorte actúa menos y el entrenamiento se parece al original; al bajarlo, estabiliza más pero frena el aprendizaje. Lo habitual es entre 1 y 5 |
| `L` | La pérdida del paso actual | las de la pérdida | Se comprueba con `np.isfinite(L)` en cada paso. Un `NaN` inmediato (primer lote) apunta a `log(0)`, `sqrt` de un negativo o una división por cero; uno tardío, a inestabilidad acumulada |
:::

## Ejemplo

Cuatro diagnósticos con números concretos.

**1. Pérdida inicial.** Clasificador de 10 clases con 256 etiquetas aleatorias (no hay nada que
aprender, así que la pérdida no puede bajar de `ln 10 = 2,3026`):

```
ln(10) con logits casi nulos   2.3026   <- correcto
logits ~ N(0, 0.01)            2.3031   <- correcto
logits ~ N(0, 4.0)             6.5759   <- la capa de salida esta mal escalada
```

La tercera fila no dice «el modelo es malo»: dice que la inicialización de la última capa
multiplica la señal por demasiado, y que la primera actualización va a ser gigantesca.

**2. Test de memorización.** 8 ejemplos, 2 variables, una capa oculta de 16 unidades, 600
épocas:

```
epoca   1  perdida 0.6347
epoca 200  perdida 0.0648
epoca 600  perdida 0.0088
```

Baja dos órdenes de magnitud: el bucle de entrenamiento funciona. Si estas tres cifras fueran
0,63 / 0,63 / 0,62, el problema estaría en el código y no habría que tocar ni los datos ni los
hiperparámetros.

**3. Gradiente que explota.** Un gradiente con norma 335,54 y umbral 5 se recorta a norma 5,00
conservando la dirección. Sin recorte, un paso de descenso con esa norma mueve los pesos a una
zona del espacio donde la pérdida es arbitraria: es el mecanismo habitual detrás del primer
`NaN`.

**4. Detección temprana.** `[0.693, 0.512, nan, 0.301]` contiene un `NaN` en el tercer paso. Si
aplicas ese paso, todos los pesos pasan a `NaN` y a partir de ahí la pérdida es `NaN` para
siempre: el fallo se puede localizar en el paso 3 o no localizarse nunca.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(0)
clases, n = 10, 256
y = rng.integers(0, clases, n)     # etiquetas al azar: no hay patron que aprender

def entropia_cruzada(logits):
    z = logits - logits.max(axis=1, keepdims=True)        # resta estable antes de exponenciar
    logp = z - np.log(np.exp(z).sum(axis=1, keepdims=True))
    return -logp[np.arange(n), y].mean()

print(f"ln(10) con logits casi nulos   {entropia_cruzada(np.zeros((n, clases))):.4f}")   # -> 2.3026
print(f"logits ~ N(0, 0.01)            {entropia_cruzada(rng.normal(0, .01, (n, clases))):.4f}")  # -> 2.3031
print(f"logits ~ N(0, 4.0)             {entropia_cruzada(rng.normal(0, 4.0, (n, clases))):.4f}")  # -> 6.5759
```

:::claves
- `logits - logits.max(axis=1, keepdims=True)` resta el máximo **por fila**, no el máximo global. `axis=1` recorre las columnas de cada ejemplo y `keepdims=True` conserva la forma `(n, 1)` para que la resta se emita contra las 10 columnas. Sin `keepdims` el resultado sería un vector de `n` elementos y la resta fallaría o daría algo distinto por emisión.
- `np.log(np.exp(z).sum(axis=1, keepdims=True))` es `logsumexp` escrito a mano. La versión numéricamente estable usa `z` (ya desplazado) y no `logits`; si usaras los logits originales, `np.exp(6.5759)` aún cabría pero con logits de 800 desbordaría a `inf` y la pérdida saldría `nan`.
- `-logp[np.arange(n), y].mean()` usa **indexado avanzado**: dos arrays de la misma longitud se emparejan posición a posición y devuelven los `n` valores de la clase correcta. Es la forma de decir «la probabilidad que el modelo dio a la etiqueta verdadera de cada fila» sin bucles.
- `entropia_cruzada` recalcula todo desde cero cada vez y **no toca** `rng` (el ruido se genera en la llamada, no dentro). Por eso las tres líneas son independientes aunque compartan la misma variable `y`: las etiquetas aleatorias son las mismas en las tres, lo único que cambia es la escala de los logits.
- El `n` que se usa dentro de la función es el `n = 256` del ámbito global, no un parámetro. Funciona, pero si reutilizaras esta función para otro tamaño de lote tendrías que pasar `n` como argumento o dividir entre `logp.shape[0]`: con `n` desacoplado del array, el `mean()` y el `n` podrían dejar de coincidir.
- Compara con el ejemplo de la sección anterior: `ln(10) = 2,3026`, y las tres cifras de esta tabla son eso mismo con logits nulos, eso mismo con ruido pequeño, y una cifra que no tiene nada que ver (6,5759) cuando la escala de los logits es 4. El diagnóstico no es «el modelo es malo», es «la última capa está mal escalada».
:::

```python verificable
import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(0, 1, (8, 2))                    # 8 ejemplos, 2 variables
y = np.array([0, 1, 0, 1, 0, 1, 0, 1])          # etiquetas casi arbitrarias

W1 = rng.normal(0, 0.5, (2, 16)); b1 = np.zeros(16)
W2 = rng.normal(0, 0.5, (16, 2)); b2 = np.zeros(2)
idx = np.arange(X.shape[0])

def perdida():
    h = np.tanh(X @ W1 + b1)
    z = h @ W2 + b2
    p = np.exp(z - z.max(1, keepdims=True)); p /= p.sum(1, keepdims=True)
    return -np.log(p[idx, y]).mean(), h, p

historial = {}
for epoca in range(1, 601):
    L, h, p = perdida()
    if epoca in (1, 200, 600):
        historial[epoca] = L
    g2 = p.copy(); g2[idx, y] -= 1; g2 /= X.shape[0]     # gradiente de la entropia cruzada + softmax
    g1 = (g2 @ W2.T) * (1 - h ** 2)
    W2 -= 0.5 * h.T @ g2; b2 -= 0.5 * g2.sum(0)
    W1 -= 0.5 * X.T @ g1; b1 -= 0.5 * g1.sum(0)

# Si la red no puede memorizar 8 ejemplos, el fallo esta en el codigo, no en los datos
print(f"epoca   1  perdida {historial[1]:.4f}")     # -> 0.6347
print(f"epoca 200  perdida {historial[200]:.4f}")   # -> 0.0648
print(f"epoca 600  perdida {historial[600]:.4f}")   # -> 0.0088
```

```python verificable
import numpy as np

# Gradiente con un valor enorme: sin recorte, un paso de SGD destruye los pesos
g = np.array([120.0, -310.0, 45.0, 8.0])
umbral = 5.0
norma = np.linalg.norm(g)
g_recortado = g * min(1.0, umbral / norma)

print(f"norma original   {norma:8.2f}")                       # -> 335.54
print(f"norma recortada  {np.linalg.norm(g_recortado):8.2f}")  # -> 5.00

# Una perdida NaN se detecta antes de que contamine los pesos
perdidas = np.array([0.693, 0.512, np.nan, 0.301])
print("hay NaN en la perdida:", bool((~np.isfinite(perdidas)).any()))   # -> True
```

:::claves
- `min(1.0, umbral / norma)` es un `float` de Python, no `np.minimum`: funciona porque `umbral / norma` ya es un escalar. Si `g` fuera una matriz y quisieras recortar **por fila**, necesitarías `np.minimum` con el eje bien elegido, y con el `min()` de Python daría error o un resultado silenciosamente equivocado por emisión.
- `g * min(...)` devuelve un array **nuevo**; `g` sigue siendo el gradiente original con norma 335,54. Es lo que se quiere aquí (se conserva el original para comparar), pero en un bucle de entrenamiento real se sustituye el gradiente antes del paso, y hacerlo con `g *= factor` modificaría el tensor en el sitio y rompería el grafo de autograd de PyTorch.
- `np.linalg.norm(g)` calcula la norma euclídea sin decir el eje, porque `g` es un vector plano. Para una matriz, `np.linalg.norm(M)` devuelve la **norma de Frobenius** (la raíz de la suma de todos los cuadrados), que no es el recorte por norma que se usa en la práctica: ahí lo que se recorta es la norma del gradiente entero tratado como un vector, que en Frobenius coincide, pero si recortaras por fila el resultado sería otro.
- `(~np.isfinite(perdidas)).any()` hace tres cosas: `np.isfinite` da `False` donde hay `nan` o `inf`, el `~` lo invierte y `.any()` responde si hay **al menos uno**. El `bool(...)` convierte el `np.bool_` en un `bool` de Python para que el `print` diga `True` y no `True` con un tipo raro.
- Recortar el gradiente **no** arregla el `NaN`: si la pérdida ya salió `NaN`, el gradiente también es `NaN` y `umbral / nan` es `nan`, así que `min(1.0, nan)` devuelve `nan` en Python. El recorte evita que la norma crezca hasta desbordar; la comprobación `np.isfinite` es la que aborta el paso cuando ya ha pasado.
- Fíjate en que este bloque no entrena nada: es una comprobación de dos líneas sobre valores escritos a mano. Ese es el punto de la página: las comprobaciones que descartan sospechosos cuestan segundos y se escriben antes de mirar el modelo entero.
:::

## Errores típicos

- **Depurar leyendo código en vez de hacer experimentos.** Pasar cuatro horas revisando el
  modelo capa por capa rinde menos que dos minutos de «memoriza 8 ejemplos». Cada comprobación
  debe tener un resultado esperado escrito de antemano; si no lo tiene, no es una comprobación,
  es una impresión.
- **Cambiar tres cosas a la vez.** Si tocas la tasa de aprendizaje, la inicialización y el
  número de capas en la misma iteración y la pérdida mejora, no sabes qué lo arregló ni qué
  romperá la próxima vez. Un cambio, una ejecución.
- **Culpar a los datos de un bug de código.** «Es que mis datos son muy difíciles» es la
  conclusión más cómoda y casi siempre la equivocada. El test de memorización la descarta en
  30 segundos.
- **Ignorar la pérdida del primer paso.** Arrancar en 0,02 cuando el valor de referencia es
  2,30 significa que las etiquetas están entrando por donde no deben, o que estás pasando
  probabilidades a una pérdida que espera logits. Es un error que se arrastra durante días.
- **Tapar los `NaN` con un `nan_to_num`.** Sustituir el `NaN` por cero deja el entrenamiento en
  marcha con pesos ya corrompidos y un modelo que parece entrenar sin aprender. Un `NaN` se
  investiga, no se maquilla.
- **Evaluar con el modelo en modo de entrenamiento.** Si al medir validación sigues con
  [[dropout-y-regularizacion|dropout]] activo y con [[normalizacion-por-lotes|BatchNorm]]
  actualizando sus estadísticas, tus métricas son ruidosas y peores de lo que deberían. Es el
  «bug» que más veces resulta no ser un bug.

:::practica
enunciado: Una red de 20 clases arranca con una pérdida de 0,10 y su gradiente en el primer paso es [9, −40, 12]. ¿Cuál era la pérdida inicial esperada y qué gradiente aplicas si recortas por norma con τ = 2?
pista: Con clases balanceadas y logits nulos la entropía cruzada vale ln C; el recorte conserva la dirección y solo acorta el vector.
solucion: El valor de referencia es ln 20 = 2,9957, así que arrancar en 0,10 delata un error de emparejamiento de etiquetas o de logits, no un problema de datos. La norma es √(81 + 1600 + 144) = √1825 = 42,72; el factor es 2 / 42,72 = 0,0468, y el gradiente recortado vale [0,421; −1,873; 0,562], con norma 2,00. Conclusión: recorta el paso y revisa cómo entran las etiquetas.
:::

## Comprueba que lo sabes

:::quiz
p: Tu red de 10 clases arranca con una pérdida de 0,04. ¿Qué miras primero?
o: La tasa de aprendizaje, porque es el hiperparámetro más importante
o: Como se construyen las etiquetas y qué espera exactamente la función de pérdida, porque el valor de referencia es ln 10 = 2,30
o: La inicialización de los pesos, porque una pérdida baja indica pesos demasiado grandes
a: 2
e: Con logits casi nulos y clases balanceadas, la entropía cruzada media vale ln C. Una pérdida inicial de 0,04 solo es posible si la salida ya está correlacionada con la etiqueta: fuga, emparejamiento incorrecto de filas, o probabilidades pasadas donde se esperan logits.
:::

:::quiz
p: ¿Para qué sirve intentar que la red memorice 8 ejemplos con la regularización desactivada?
o: Para medir la capacidad real que necesita el problema final
o: Para separar un error de implementación de un problema de datos o de régimen de entrenamiento
o: Para elegir la tasa de aprendizaje definitiva
a: 2
e: Si la red no puede con 8 ejemplos, ningún ajuste de hiperparámetros va a arreglarlo: el fallo está en el código. Si los memoriza, el bucle funciona y el problema está en los datos o en cómo se entrena con el conjunto completo.
:::

:::quiz
p: La pérdida se vuelve NaN en la época 4.000, después de haber bajado con normalidad. ¿Cuál es el primer sospechoso?
o: Un log(0) en la primera capa
o: Gradientes que explotan por una tasa de aprendizaje demasiado alta o una pérdida mal normalizada
o: Un error de codificación de caracteres en las etiquetas
a: 2
e: Un NaN inmediato apunta a una operación matemática imposible desde el principio; uno tardío apunta a inestabilidad numérica acumulada: norma del gradiente creciente, sumas en vez de medias, o pérdida calculada en precisión insuficiente. Se diagnostica recortando el gradiente y bajando la tasa.
:::

:::aviso
Antes de tocar hiperparámetros, comprueba tres cosas que no se ven en las curvas: que `x` e `y`
siguen emparejados después de barajar, que no hay `NaN` ni infinitos en las variables de
entrada, y que todas las variables están en la misma escala. Muchos «problemas de
entrenamiento» son un `StandardScaler` que se aplicó solo a una parte de los datos.
:::
