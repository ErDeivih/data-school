---
id: train-val-test
titulo: Conjuntos de entrenamiento, validación y prueba
fase: 6
nivel: básico
rutas: [core, ds]
prerequisitos: []
tags: [evaluacion, particiones, generalizacion]
resumen: Tres particiones con tres papeles distintos: entrenar, decidir y medir una sola vez. Mirar el test más de la cuenta lo convierte en validación.
---

## En una frase

Los datos se parten en tres trozos separados —entrenamiento, validación y prueba— porque cada uno
tiene un papel distinto: con el primero se ajusta el modelo, con el segundo se decide cuál te quedas
y con el tercero se mide una sola vez lo que esperas obtener en el mundo real.

## La idea

Piensa en preparar una oposición. Estudias con los exámenes de años anteriores (entrenamiento),
haces simulacros para saber qué temario llevas flojo y qué estrategia te funciona (validación) y al
final haces el examen oficial (prueba). Si consigues ver el examen oficial antes, ya no mide lo que
sabes: mide lo que has memorizado de ese examen concreto. Y si lo miras diez veces, ajustando
respuestas cada vez, el resultado que obtengas no te dice nada sobre tu nivel real.

Ese es todo el concepto, pero tiene tres consecuencias prácticas que se olvidan a diario:

1. **El error sobre los datos de entrenamiento no sirve para decidir.** Un modelo más flexible
   siempre lo baja, hasta llegar a cero, y a partir de ahí solo está memorizando
   ([[sesgo-varianza]]). La validación existe precisamente para medir en datos que el ajuste no ha
   visto.
2. **La validación se puede tocar; la prueba no.** Puedes probar 20 configuraciones y quedarte con la
   mejor según validación: para eso está. Hacerlo con la prueba invalida el número. Y hay un matiz:
   incluso usando solo validación, el ganador está inflado, porque es el máximo de 20 estimaciones
   ruidosas (el ejemplo de abajo lo mide: 0,577 frente a 0,490 sobre datos sin señal).
3. **El tamaño de la prueba limita la precisión de tu conclusión.** Con 40 ejemplos, cada acierto
   mueve la exactitud 2,5 puntos: un 0,575 y un 0,525 son indistinguibles.

Como se parten los datos depende de la estructura del problema:

- **Estratificada.** Cada clase queda en la misma proporción en las tres particiones. Con clases raras
  no es un lujo: sin estratificar, una partición puede quedarse sin un solo positivo.
- **Por grupos.** Todas las filas de la misma entidad (cliente, paciente, máquina) van al mismo lado;
  si no, el modelo puede reconocer al cliente en vez de generalizar.
- **Temporal.** Se corta por fecha, y no se baraja nunca ([[validacion-temporal]]).

## Definición formal

Sea `D = {(x_i, y_i)}` una muestra de `n` observaciones. Una partición en tres conjuntos disjuntos
`D_train`, `D_val` y `D_test` cumple `D = D_train ∪ D_val ∪ D_test` y las intersecciones son vacías.

- **Tamaños habituales.** 60/20/20 o 70/15/15. Con muchas observaciones la proporción importa poco;
  con pocas, la validación y la prueba se quedan sin poder estadístico.
- **Error aparente.** El que se mide sobre `D_train`. Está sesgado a la baja, y el sesgo crece con la
  flexibilidad del modelo.
- **Error de validación.** El que se mide sobre `D_val`. Sirve para elegir modelo e hiperparámetros, y
  estima el rendimiento **del procedimiento de selección**, no del modelo elegido.
- **Error de prueba.** El que se mide sobre `D_test`, una sola vez y con el modelo ya congelado. Es la
  cifra que se reporta.
- **Incertidumbre.** Para una exactitud `p` medida sobre `n_test` ejemplos, el error típico es
  aproximadamente `√( p·(1 − p) / n_test )`. Con `p = 0,8` y `n_test = 200` vale 0,028, es decir
  ±2,8 puntos porcentuales. Dos modelos que difieran menos que eso no están separados por los datos.
- **Estratificación.** Se reparte de forma que la proporción de la clase `c` en cada partición `j`
  cumpla `n_j^c / n_j ≈ n^c / n`, para que ninguna se quede sin ejemplos de una clase rara.
- **Grupos.** Sea `g(i)` el grupo de la fila `i` (el cliente, el paciente, la máquina). La condición es
  `g(i) = g(j)` para todo `i, j` de la misma partición: ningún grupo se reparte entre dos conjuntos.
- **Cuándo no basta una sola partición.** Si `n` es pequeño, gastar un 20 % en validación deja el
  entrenamiento escaso y la estimación con mucha varianza ([[validacion-cruzada]]).

## Ejemplo

Cuatrocientos clientes de los que solo el 12 % se dio de baja, partidos 60/20/20:

```text
partición        positivos en validación     positivos en prueba
sin estratificar       3 de 40 (7,5 %)          2 de 40 (5,0 %)
estratificada          5 de 40 (12,5 %)         4 de 40 (10,0 %)
```

La partición sin estratificar deja la prueba con un 5 % de positivos cuando la población tiene un
12 %: la mitad de la tasa real. En un problema de fraude o de bajas, eso cambia por completo la
interpretación de la exactitud ([[desbalanceo-de-clases]]).

El segundo experimento mide el daño de elegir el mejor candidato por su nota en validación: 500 filas
de ruido puro (20 columnas sin relación con la etiqueta), partidas 50/25/25, con 20 árboles distintos
por ronda y 10 rondas:

- Exactitud media del elegido, medida en validación: **0,577**.
- Exactitud media de ese mismo elegido, medida en prueba: **0,490**.
- La verdad, conocida porque los datos son ruido: **0,500**.

El ganador parece bueno porque es el máximo de 20 estimaciones ruidosas, y esa ventaja desaparece al
cambiar de conjunto. Con 125 ejemplos de validación, el error típico de una exactitud del 50 % es
0,045; el máximo de 20 tiradas ronda 0,5 + 1,9 · 0,045 ≈ 0,59, y ahí está el 0,58 observado.

## Código

```python verificable
import numpy as np
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(0)
y = (rng.random(400) < 0.12).astype(int)      # solo el 12 % son bajas
X = rng.normal(size=(400, 5))

for nombre, est in (("sin estratificar", None), ("estratificada", y)):
    _, resto, _, y_resto = train_test_split(X, y, test_size=0.2, random_state=0, stratify=est)
    # Al estratificar, la segunda particion mantiene tambien la proporcion de clases
    _, _, y_val, y_test = train_test_split(
        resto, y_resto, test_size=0.5, random_state=0, stratify=None if est is None else y_resto)
    print("%s: validacion %d de %d (%.1f %%)  prueba %d de %d (%.1f %%)"
          % (nombre, y_val.sum(), y_val.size, 100 * y_val.mean(),
             y_test.sum(), y_test.size, 100 * y_test.mean()))
# -> sin estratificar: validacion 3 de 40 (7.5 %)  prueba 2 de 40 (5.0 %)
# -> estratificada: validacion 5 de 40 (12.5 %)  prueba 4 de 40 (10.0 %)
```

```python verificable
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

rng = np.random.default_rng(0)

# 500 filas de 20 columnas de ruido puro: ninguna senal, la exactitud real es 0.5
X = rng.normal(size=(500, 20))
y = rng.integers(0, 2, 500)

en_validacion, en_prueba = [], []
for ronda in range(10):
    Xtr, Xresto, ytr, yresto = train_test_split(X, y, test_size=0.5, random_state=ronda)
    Xva, Xte, yva, yte = train_test_split(Xresto, yresto, test_size=0.5, random_state=ronda)
    # 20 candidatos distintos: cada arbol mira 3 variables al azar en cada division
    modelos = [DecisionTreeClassifier(max_depth=5, max_features=3, random_state=s).fit(Xtr, ytr)
               for s in range(20)]
    notas = [m.score(Xva, yva) for m in modelos]
    elegido = modelos[int(np.argmax(notas))]     # el "mejor" segun validacion
    en_validacion.append(max(notas))
    en_prueba.append(elegido.score(Xte, yte))

print("elegido en validacion %.3f" % np.mean(en_validacion))   # -> elegido en validacion 0.577
print("el mismo en prueba    %.3f" % np.mean(en_prueba))       # -> el mismo en prueba    0.490
```

:::claves
- `train_test_split` devuelve una lista, no tuplas: el orden es el de los argumentos, y las cuatro variables de la segunda llamada son `X_va, X_te, y_va, y_te`. Cambiar dos de sitio no da error; da una partición mezclada.
- `test_size=0.5` se aplica **sobre lo que le pasas**: el segundo corte parte el 50 % restante por la mitad. Con `test_size=0.2` en la primera y `0.25` en la segunda sale un 60/20/20.
- `stratify=y` reparte manteniendo la proporción de clases, pero `stratify=y_resto` en la segunda llamada es obligatorio: estratificar solo en la primera deja la prueba descompensada.
- `m.score(X_va, y_va)` devuelve la exactitud del árbol, no el error. Es la media de aciertos, y por eso el azar vale 0,5 y no 0.
- `max_features=3` hace que cada árbol mire 3 de las 20 columnas en cada división: sin eso, los 20 árboles con `random_state` distinto serían idénticos y el máximo de las 20 notas sería siempre el mismo número.
- `np.argmax(notas)` devuelve la POSICIÓN del máximo, no el valor, y con empates se queda con la primera. El elegido es `modelos[posición]`: confundir el índice con la nota es un error silencioso.
- Cambia `range(20)` por `range(1)` en la lista de candidatos y el ganador deja de estar inflado: con un solo candidato no hay máximo que elegir, y su nota en validación se parece a la de prueba.
:::

:::figura
fichero: train-val-test-ganador-optimista
pie: A la izquierda, 20 candidatos por ronda sobre datos de ruido puro: cada punto azul es la nota de un árbol en validación y los rojos son el máximo de cada ronda, que es el que se elige. La línea de puntos marca la verdad (0,5) porque no hay señal que aprender. A la derecha, el mismo modelo elegido medido en los dos conjuntos: 0,576 de media en validación y 0,494 en prueba, con un margen de ±0,045 para 125 ejemplos. Conclusión: elegir el máximo de muchas estimaciones ruidosas regala unas décimas que no se repiten en datos nuevos, así que el número de la búsqueda se reporta con esa advertencia o se mide con validación anidada.
fuente: figuras/train-val-test-1.py
:::

## Errores típicos

- **Repetir el test más de una vez.** Si miras la prueba, cambias el modelo y vuelves a mirarla, la
  has convertido en validación y el número final es optimista. Elegir «la mejor de tres
  configuraciones» por su nota en prueba es exactamente el error que este concepto existe para
  evitar.
- **Escalar, imputar o seleccionar variables antes de partir.** Si calculas la media y la desviación
  con todos los datos y luego los partes, cada fila de entrenamiento lleva un poco de información de
  la prueba. Todo eso va dentro de un [[pipelines-de-ml|pipeline]] que se ajusta solo con
  entrenamiento ([[fuga-de-datos]]).
- **Elegir el umbral de decisión en la prueba.** Bajar el umbral de 0,5 a 0,3 para mejorar la
  exhaustividad es una decisión de modelo: se toma en validación, porque el umbral es un
  hiperparámetro más ([[umbrales-y-coste]]).
- **Partir por filas cuando hay entidades repetidas.** El mismo cliente en entrenamiento y en prueba
  hace que el modelo reconozca en vez de generalizar. Se parte por grupo, no por fila.
- **Ignorar el desbalanceo al partir.** Sin estratificar, la partición de prueba puede quedarse con
  dos positivos de 40, y cualquier métrica sobre esos dos es puro ruido
  ([[desbalanceo-de-clases]]).
- **Barajar una serie temporal.** El orden es información: si lo destruyes, la partición mide
  interpolación en vez de predicción ([[validacion-temporal]]). Y si la muestra es pequeña, gastar un
  20 % en validación deja el entrenamiento escaso: usa validación cruzada ([[validacion-cruzada]]).

:::practica
enunciado: 300 clientes con 5 filas cada uno (1.500 filas) partidos 70/15/15 por fila. Calcula cuántas filas de un cliente cualquiera caen de media en entrenamiento y en prueba, y cuántos clientes esperarías con filas a ambos lados.
pista: Cada fila cae por su cuenta, así que multiplica la probabilidad por las 5 filas del cliente.
solucion: Por fila, 0,7 · 5 = 3,5 filas caen en entrenamiento y 0,15 · 5 = 0,75 en prueba. La probabilidad de tener alguna fila en entrenamiento es 1 − 0,3^5 = 0,998 y de tener alguna en prueba 1 − 0,85^5 = 0,556; las dos cosas a la vez, 0,998 · 0,556 = 0,555, unos 167 de los 300 clientes. Partiendo por grupos cada cliente va entero a un solo lado y esa fuga desaparece.
:::

## Comprueba que lo sabes

:::quiz
p: Ajustas el umbral de decisión mirando qué valor da mejor exactitud sobre el conjunto de prueba. ¿Qué consecuencia tiene?
o: Ninguna, el conjunto de prueba es para eso
o: El error medido sobre la prueba deja de ser una estimación honesta del rendimiento futuro
o: Mejora el modelo, porque el umbral óptimo es una propiedad del modelo
a: 2
e: El umbral es una decisión de modelo y hay que tomarla con datos que el ajuste no haya visto. Si la tomas sobre la prueba, el resultado que reportes está sesgado al alza y en producción no se repetirá. La prueba se usa una sola vez, con todo congelado.
:::

:::quiz
p: En una ronda de selección con 20 candidatos sobre datos sin señal, el elegido saca 0,57 en validación y 0,49 en prueba. ¿Por qué?
o: Porque el modelo se ha sobreajustado al conjunto de entrenamiento
o: Porque el máximo de 20 estimaciones ruidosas es optimista y su ventaja no se repite en otro conjunto
o: Porque la partición de prueba es demasiado pequeña y está mal calculada
a: 2
e: El sobreajuste de entrenamiento no explica la caída: la caída ocurre al cambiar de conjunto de evaluación. Al elegir el máximo de 20 medidas con error típico 0,045, el ganador incorpora esa casualidad, y en la prueba vuelve a su nivel real, alrededor de 0,5.
:::

:::quiz
p: Tienes un modelo con exactitud 0,80 medida sobre 200 ejemplos de prueba. Otro saca 0,83. ¿Se puede concluir que el segundo es mejor?
o: Sí, porque 0,83 es mayor que 0,80
o: No necesariamente: el error típico de cada medida es de unos 0,028 y la diferencia está dentro de ese margen
o: Sí, siempre que los dos se hayan evaluado en el mismo conjunto de prueba
a: 2
e: Con n = 200, el error típico de una exactitud del 80 % es raíz de (0,8 · 0,2 / 200), unos 0,028. Una diferencia de 0,03 es del mismo orden que el ruido de muestreo, así que no basta para decidir. Evaluar en el mismo conjunto ayuda a que la comparación sea pareada, pero no elimina la incertidumbre.
:::
