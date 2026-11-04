---
id: paradigmas-de-aprendizaje
titulo: Paradigmas de aprendizaje
fase: 6
nivel: básico
rutas: [core, ds]
prerequisitos: []
tags: [machine-learning, paradigmas, etiquetas]
resumen: Supervisado, no supervisado, semisupervisado, autosupervisado y por refuerzo: lo que cambia entre ellos es de dónde sale la señal que el modelo usa para aprender.
---

## En una frase

Los cinco paradigmas del machine learning se distinguen por una sola cosa: de dónde sale la señal de
aprendizaje. Con etiquetas (supervisado), sin ninguna (no supervisado), con unas pocas (semi),
fabricándolas con la estructura de los datos (auto) o con recompensas que llegan tarde (refuerzo).

## La idea

Piensa en cinco formas de aprender a cocinar:

- **Con un profesor que prueba y corrige cada plato.** Tienes ejemplos resueltos y sabes cuál era la
  respuesta correcta. Es el **aprendizaje supervisado**, el que sostiene la mayoría de las
  aplicaciones: predecir si un cliente se dará de baja, si un pago es fraudulento o cuánto costará un
  siniestro.
- **Sin profesor, ordenando la despensa por parecido.** Nadie te dice los nombres de los grupos, pero
  tú los encuentras: los clientes se agrupan en perfiles, los productos en familias. Es el
  **aprendizaje no supervisado**, y como no hay respuesta correcta que copiar, tampoco hay una métrica
  mágica que diga si acertaste.
- **Con 200 recetas corregidas y 20.000 sin corregir.** Un profesor que solo corrige el 1 % de los
  platos. Es el **aprendizaje semisupervisado**: la esperanza es que la forma en que se agolpan los
  datos sin etiquetar informe dónde están las fronteras.
- **Tirando la mitad de cada receta y adivinándola.** Tapas un ingrediente del texto y aprendes a
  rellenarlo: la propia frase trae su respuesta. Es el **autosupervisado**, el motor de los modelos de
  lenguaje, que se preentrenan tapando la palabra siguiente ([[como-funciona-un-llm]],
  [[preentrenamiento-y-escalado]]).
- **Probando platos y viendo si el comensal vuelve.** Nadie te dice qué hiciste bien; solo recibes una
  señal agregada y retrasada. Es el **aprendizaje por refuerzo** ([[aprendizaje-por-refuerzo]]), donde
  el problema no es predecir, sino decidir una secuencia de acciones.

La confusión habitual es creer que el paradigma lo decide el algoritmo. No: lo decide el problema y,
sobre todo, **lo que tienes en la mano**. El mismo algoritmo puede servir a dos paradigmas: una red que
predice la palabra tapada es autosupervisada en el preentrenamiento y supervisada en el ajuste fino.

## Definición formal

Con `X` la matriz de entradas (una fila por ejemplo, una columna por variable) e `Y` las respuestas:

- **Supervisado.** Se dispone de `n` pares `(x_i, y_i)` muestreados de una distribución conjunta
  `P(X, Y)`. Se busca una función `f` que minimice el riesgo esperado `E[ L(Y, f(X)) ]`, con `L` la
  función de pérdida. Si `Y` es categórica, clasificación; si es numérica, regresión
  ([[metricas-de-regresion]], [[metricas-de-clasificacion]]).
- **No supervisado.** Solo se dispone de `{x_i}`. No hay `Y`, así que no hay pérdida contra la verdad:
  se optimiza un criterio interno. Ejemplos: agrupar minimizando la suma de distancias al centroide
  ([[k-means]]), estimar la densidad de `P(X)`, o proyectar a menos dimensiones conservando la
  varianza ([[pca]]).
- **Semisupervisado.** Se dispone de `l` pares etiquetados y `u` entradas sin etiquetar, con
  `u ≫ l`. Se añade un supuesto sobre la forma de los datos: el **supuesto de agrupamiento** (puntos
  del mismo cúmulo comparten etiqueta) o el **supuesto de variedad** (los datos viven cerca de una
  superficie de menos dimensiones). Sin él, las filas sin etiquetar no aportan nada
  ([[aprendizaje-semi-supervisado]]).
- **Autosupervisado.** Se construyen pares `(x, y)` a partir de los propios datos con una tarea
  auxiliar (*pretext task*): predecir la palabra siguiente, reconstruir una parte oculta, distinguir
  una muestra real de una alterada. El objetivo es formalmente supervisado, pero las etiquetas son
  gratis. Lo que se aprende es una representación que luego se reutiliza
  ([[embeddings]], [[transfer-learning]], [[fine-tuning-y-lora]]).
- **Por refuerzo.** Se formaliza como un proceso de decisión de Markov: estados `S`, acciones `A`,
  transiciones y una recompensa `r_t`. Se busca una política `π(a | s)` que maximice la recompensa
  acumulada descontada `E[ Σ_t γ^t · r_t ]`, con `γ ∈ [0, 1)` el factor de descuento. No hay ejemplos
  correctos: hay que explorar, y la señal puede llegar cientos de pasos después de la acción que la
  causó ([[q-learning-y-policy-gradient]]).

| Paradigma | Lo que necesitas | Lo que optimizas | Ejemplo típico |
| --- | --- | --- | --- |
| Supervisado | pares (entrada, respuesta) | error contra la respuesta | riesgo de impago |
| No supervisado | solo entradas | un criterio interno | segmentar clientes |
| Semisupervisado | pocas respuestas, muchas entradas | error y coherencia con la estructura | etiquetar 1 de cada 500 correos |
| Autosupervisado | datos en crudo y una tarea auxiliar | reconstruir o predecir una parte | preentrenar un modelo de lenguaje |
| Por refuerzo | un entorno donde actuar | recompensa acumulada | regular el caudal de un embalse |

## Ejemplo

Doce clientes con dos números cada uno: horas de uso al mes (`x`) y gasto mensual (`y`):

```
x:  1   2   3   4   5   6   7   8   9  10  11  12
y:  8  11  15  14  19  22  21  26  30  29  34  37
```

- **Supervisado.** Si `y` es lo que quieres predecir, ajustas una recta y obtienes
  `gasto = 5,71 + 2,53 · horas`, con un error cuadrático medio de 1,33 dentro de la muestra. Cada hora
  de uso se asocia a 2,53 euros más de gasto, y ese número se puede discutir con negocio.
- **No supervisado.** Si no tienes `y` y solo quieres ver si hay perfiles, aplicas K-means con dos
  grupos sobre los pares `(x, y)` y salen dos grupos de 7 y 5 clientes, con centroides en
  `(4,0 · 15,7)` y `(10,0 · 31,2)`. Nadie te ha dicho que existan dos grupos: con tres grupos saldrían
  otros, y «cliente intensivo» es una interpretación, no un dato.

Fíjate en la diferencia de estatus. El 2,53 de la regresión se puede comparar con la realidad y
fallar; el grupo de 7 clientes no se puede comparar con nada, porque no hay verdad que copiar.

## Código

```python verificable
import numpy as np

# Doce clientes: x = horas de uso al mes, y = gasto mensual
x = np.array([1.0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
y = np.array([8.0, 11, 15, 14, 19, 22, 21, 26, 30, 29, 34, 37])

# Supervisado: conocemos y y queremos predecirla con una recta (minimos cuadrados)
pendiente, intercepto = np.polyfit(x, y, 1)
print("recta: gasto = %.2f + %.2f * horas" % (intercepto, pendiente))
# -> recta: gasto = 5.71 + 2.53 * horas
print("RMSE en la muestra %.2f" % np.sqrt(np.mean((y - (pendiente * x + intercepto)) ** 2)))
# -> RMSE en la muestra 1.33

# No supervisado: dos grupos con K-means sobre los pares (x, y), sin etiquetas
datos = np.column_stack([x, y])
centros = np.array([datos[0], datos[-1]], dtype=float)   # arranque: el primero y el ultimo
for _ in range(20):                       # iterar hasta que los grupos se estabilicen
    distancias = np.sqrt(((datos[:, None, :] - centros[None, :, :]) ** 2).sum(axis=2))
    etiquetas = distancias.argmin(axis=1)
    centros = np.array([datos[etiquetas == k].mean(axis=0) for k in (0, 1)])
print("tamano de los grupos", np.bincount(etiquetas, minlength=2).tolist())
# -> tamano de los grupos [7, 5]
for cx, cy in centros:
    print("centroide: %.1f horas, %.1f euros" % (cx, cy))
# -> centroide: 4.0 horas, 15.7 euros
# -> centroide: 10.0 horas, 31.2 euros
```

:::claves
- `np.polyfit(x, y, 1)` devuelve los coeficientes **de mayor a menor grado**: `[2.53, 5.71]` es `2,53 · x + 5,71`. El bloque los desempaqueta en ese orden y por eso la recta se escribe `gasto = 5,71 + 2,53 · horas` sin darles la vuelta.
- `np.polyfit` no devuelve el error. El RMSE del ejemplo se calcula a mano con `np.sqrt(np.mean((y - (pendiente * x + intercepto)) ** 2))`, y ese 1,33 es **dentro de la muestra**: con datos nuevos sería mayor.
- `np.column_stack([x, y])` apila dos vectores como columnas y devuelve un `ndarray` de 12 filas y 2 columnas. `np.array([x, y])` daría 2 filas y 12 columnas, que es justo lo contrario de lo que el clustering necesita.
- `datos[:, None, :] - centros[None, :, :]` añade un eje a cada lado para que NumPy reste cada punto contra cada centroide a la vez (12 × 2 × 2). Sin esos `None`, las formas no encajan y la resta falla.
- `distancias.argmin(axis=1)` devuelve la **posición** del centroide más cercano (0 o 1), no la distancia. El eje importa: `axis=1` compara los dos centroides de cada fila; con `axis=0` compararía los 12 clientes de cada columna.
- `np.bincount(etiquetas, minlength=2)` cuenta cuántas veces aparece cada etiqueta y devuelve un array de NumPy; sin `minlength=2` fallaría si un grupo se queda vacío, y `.tolist()` está ahí para que la salida sea una lista de Python.
- `datos[etiquetas == k]` es una **máscara booleana**, no un índice: selecciona las filas donde la condición es cierta. Si un grupo se quedara sin clientes, `.mean(axis=0)` devolvería `nan` y el bucle siguiente arrastraría ese `nan`.
:::

## Errores típicos

- **Usar no supervisado donde tienes la etiqueta.** Si existe una variable objetivo, agrupar y luego
  ponerle nombre a los grupos es dar un rodeo: entrena el modelo supervisado y mide su error. El
  clustering se justifica cuando no hay respuesta, o como paso previo para crear variables.
- **Creer que las etiquetas del no supervisado son verdad.** Los grupos de K-means dependen del número
  de grupos que pidas, de la escala de las variables y de la distancia elegida. Cambia cualquiera de
  las tres y salen otros grupos igual de «válidos».
- **Pensar que el semisupervisado es «usar pocos datos».** Explota la estructura de los datos sin
  etiquetar y funciona cuando esa estructura coincide con las clases. Si las clases se solapan, el
  pseudoetiquetado amplifica el error en vez de reducirlo.
- **Suponer que el autosupervisado es gratis.** Ahorra etiquetas, no cómputo: preentrenar un modelo
  grande cuesta mucho más que etiquetar unos miles de ejemplos, y para tu tarea casi siempre hace
  falta una fase con etiquetas ([[fine-tuning-vs-rag]]).
- **Evaluar el refuerzo con métricas de supervisado.** La exactitud de la acción en cada paso no mide
  lo que importa, que es la recompensa acumulada: un agente puede acertar el 95 % de las decisiones
  inmediatas y arruinar el episodio por una sola acción mala en el momento equivocado.
- **Esperar que un agente de refuerzo aprenda de un fichero.** Sin entorno no hay recompensa ni
  exploración. Un dataset histórico solo permite imitación o evaluación fuera de línea, que es otro
  problema.

:::practica
enunciado: Un corpus tiene 10 millones de frases de 20 palabras. En el preentrenamiento autosupervisado se tapa el 15 % de las palabras y cada una tapada es una etiqueta. ¿Cuántas etiquetas genera cada época y cuántas veces más que las 5.000 etiquetas humanas disponibles?
pista: Multiplica frases por palabras para tener los tokens totales; la tarea auxiliar convierte cada palabra tapada en un par entrada-respuesta, sin anotación humana.
solucion: 10 millones de frases × 20 palabras = 200 millones de tokens; el 15 % son 30 millones de etiquetas por época, frente a 5.000 humanas: 30.000.000/5.000 = 6.000 veces más. Son gratis en anotación, no en cómputo, y solo enseñan a reconstruir texto: para la tarea concreta siguen haciendo falta las 5.000 etiquetas en el ajuste fino.
:::

## Comprueba que lo sabes

:::quiz
p: Quieres predecir qué clientes se darán de baja el mes que viene y tienes 3.000 bajas históricas etiquetadas. ¿Qué paradigma corresponde?
o: No supervisado, porque hay que descubrir los perfiles de cliente
o: Supervisado, porque tienes pares de entrada y respuesta correcta
o: Autosupervisado, porque la etiqueta se puede derivar del propio histórico
a: 2
e: Hay una variable objetivo observada (se dio de baja o no) y ejemplos históricos, así que es supervisado. El autosupervisado fabrica la etiqueta a partir de la estructura de los datos sin intervención humana, y aquí la etiqueta viene del negocio.
:::

:::quiz
p: ¿Qué necesita el aprendizaje semisupervisado para que las filas sin etiquetar aporten algo?
o: Que las filas sin etiquetar sean independientes de las etiquetadas
o: Un supuesto sobre la forma de los datos, por ejemplo que puntos del mismo grupo comparten etiqueta
o: Que haya más etiquetas que datos sin etiquetar
a: 2
e: Sin un supuesto de agrupamiento o de variedad, las entradas sin etiquetar no dicen nada sobre la frontera entre clases y pueden incluso empeorar el resultado. La cantidad no es el requisito: el requisito es que la estructura de los datos coincida con las clases.
:::

:::quiz
p: En una prueba de trading, un agente recibe +1 por cada operación ganadora y −1 por cada perdedora, y solo ve el resultado al cerrar el día. ¿Por qué encaja en aprendizaje por refuerzo y no en supervisado?
o: Porque la recompensa llega agregada y con retardo, así que hay que resolver a qué decisiones atribuirla
o: Porque no hay datos suficientes para entrenar un clasificador
o: Porque las operaciones ganadoras son la etiqueta y el problema es una clasificación binaria
a: 1
e: El problema de atribución temporal (crédito diferido) es lo propio del refuerzo: la recompensa no dice qué acción concreta fue la buena. Si tuvieras la etiqueta de cada operación por separado, sería un problema supervisado corriente.
:::
