---
id: etiquetas-y-techo-del-modelo
titulo: Calidad de las etiquetas y techo del modelo
fase: 6
nivel: avanzado
rutas: [ds]
prerequisitos: [metricas-de-clasificacion, train-val-test, sesgo-varianza]
tags: [etiquetas, ruido, calidad-de-datos, evaluacion, limites]
resumen: Cuánto rendimiento te está costando el ruido de las etiquetas y cómo estimar el techo real de un modelo antes de gastar otra semana entrenando.
fuentes: ["Frénay y Verleysen (2014), 'Classification in the Presence of Label Noise: A Survey'", "Northcutt, Athalye y Mueller (2021), 'Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks'", "Sculley et al. (2015), 'Hidden Technical Debt in Machine Learning Systems'"]
---

## En una frase

El ruido de las etiquetas fija un techo al rendimiento, y por debajo de ese techo ninguna
arquitectura, ningún hiperparámetro y ninguna GPU rescatan el modelo: lo único que sube la marca
es arreglar las etiquetas.

## La idea

Estudias con un solucionario en el que el 15 % de las respuestas están mal. Puedes memorizarlo
entero, sacar un diez en los ejercicios de ese solucionario y suspender el examen real, porque
una parte de lo que has aprendido con esfuerzo es el propio error. Un modelo entrenado con
etiquetas ruidosas hace lo mismo: con capacidad suficiente acaba memorizando el ruido, la
pérdida de entrenamiento cae hacia cero y la métrica sobre datos nuevos se queda clavada. Lo
peligroso es que ese estancamiento se parece muchísimo a «necesito un modelo mejor».

Hay dos clases de ruido y se comportan de forma opuesta:

- **Conflicto**: la etiqueta es genuinamente ambigua. Dos anotadores competentes ven el mismo
  ejemplo y no se ponen de acuerdo porque el criterio no lo determina. Es irreducible: si la
  etiqueta es una moneda al aire, ningún modelo acierta más de lo que acierta una moneda. Este
  ruido **baja el techo**.
- **Error**: el criterio está claro y la anotación es la equivocada. Si el error se reparte al
  azar entre las clases y no depende de las variables, no mueve la frontera de decisión: la
  clase más probable sigue siendo la misma, solo que ahora está escrita con menos frecuencia.
  Lo que rompe es la **medición**: tu métrica de validación deja de significar lo que crees.

La segunda parte es la que hace perder semanas. Un clasificador que acierta de verdad el 90 %
parece mediocre (0,74) si lo mides contra etiquetas con un 20 % de errores, y un modelo que
parece excelente puede estar ya pegado al techo. Sin saber dónde está el techo, no sabes si el
esfuerzo que queda sirve para algo.

El techo se estima, no se adivina:

1. **Audita una muestra a ciegas.** Coge 200 o 300 ejemplos de validación, quita la etiqueta y
   vuelve a anotarlos sin mirar la original. El porcentaje de discrepancias es una estimación
   directa del ruido, y de paso te dice si el problema son unas pocas clases.
2. **Mide el acuerdo entre anotadores** con varios anotadores sobre la misma muestra. El kappa
   descuenta el acuerdo que se produciría por puro azar; eso explica que dos anotadores que
   coinciden en el 82 % de un problema de cuatro clases no estén de acuerdo en el 82 % de nada.
3. **Mira la curva de aprendizaje.** Si la métrica sigue subiendo entre el 50 % y el 100 % de los
   datos, no estás en el techo y lo que falta son datos. Si está plana, más datos no van a
   moverla: el arreglo está en las etiquetas o en el planteamiento del problema.
4. **Entrena dos modelos de familia distinta.** Un árbol con boosting y una regresión logística
   no comparten sesgos. Cuando los dos aterrizan en el mismo número con una diferencia menor que
   la dispersión entre semillas, ese número es el techo.

Cuando el techo está por debajo de lo que el negocio necesita, el problema ya no es de machine
learning. Es la definición de la etiqueta, el proceso de captura o la propia pregunta: quizá la
clase «abandono» mezcla dos motivos distintos, o quizá el ejemplo concreto que nadie sabe
etiquetar tampoco tiene una respuesta correcta que aprender.

:::trampa
Cuando la métrica de validación se estanca, la reacción automática es añadir capas, subir
neuronas o probar otro optimizador. Si el techo lo pone el ruido de las etiquetas, eso no sube
la validación: solo abre la brecha entre entrenamiento y validación, porque el modelo emplea la
capacidad extra en memorizar las etiquetas malas.
:::

:::figura
fichero: etiquetas-techo-y-memorizacion
pie: A la izquierda, el techo que impone el conflicto: cada curva es la exactitud máxima que puede alcanzar cualquier modelo para un porcentaje dado de etiquetas ambiguas, y la línea vertical marca el 10 %. Con dos clases ese 10 % deja el techo en 0,95; con diez clases lo deja en 0,91, porque acertar al azar entre más clases es más difícil. Nada por encima de esas curvas es alcanzable, así que un modelo que ronda su curva ya no tiene margen y el esfuerzo debe ir a las etiquetas. A la derecha, lo que ocurre cuando se responde al estancamiento con más capacidad: el mismo árbol de decisión, entrenado sobre 5.600 ejemplos con un 15 % de etiquetas cambiadas por una moneda, acierta el 100 % de lo que se le pidió a profundidad ilimitada y solo el 68,7 % de los datos limpios. El máximo está en profundidad 4, no en la más grande.
fuente: figuras/etiquetas-y-techo-del-modelo-1.py
:::

## Definición formal

**Techo por conflicto.** Si una fracción `m` de los ejemplos tiene una etiqueta que es
equiprobable entre las `C` clases —porque el criterio es ambiguo o porque los anotadores no se
ponen de acuerdo—, el mejor clasificador posible acierta todos los ejemplos no ambiguos y una
fracción `1/C` de los ambiguos:

:::formula
techo = 1 − m + m / C
:::

**Exactitud medida con ruido simétrico.** Si el ruido cambia la etiqueta por otra clase
cualquiera con probabilidad `ρ`, sin depender de las variables de entrada, entonces la exactitud
que mides contra esas etiquetas y la que tendrías contra las etiquetas verdaderas se relacionan
así:

:::formula
acc_medida = (1 − ρ) · acc_real + ρ / C
acc_real = (acc_medida − ρ / C) / (1 − ρ)
:::

La corrección solo vale si el ruido es simétrico. Cuando los errores son asimétricos —los
anotadores confunden sistemáticamente la clase 3 con la 2 y casi nunca al contrario—, la
frontera de decisión sí se mueve y deshacer el sesgo exige modelar la matriz de transición
completa, no una resta.

**Acuerdo entre anotadores.** El kappa de Cohen mide el acuerdo una vez descontado el que se
daría por azar:

:::formula
κ = (p_o − p_e) / (1 − p_e)
:::

Con `p_o` el acuerdo observado y `p_e` el esperado por azar a partir de las frecuencias de cada
clase. La convención habitual en anotación considera 0,6 aceptable y 0,8 bueno; por debajo, el
conjunto de validación no es una referencia fiable y el techo que estás midiendo es en realidad
el ruido de tus propias etiquetas.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `m` | Fracción de ejemplos con etiqueta ambigua o en conflicto | tanto por uno | El techo baja de forma lineal: cada punto de conflicto cuesta entre medio punto de exactitud máxima (con 2 clases) y casi un punto (con muchas clases). Con 10 clases y `m = 0,10` el techo queda en 0,91; con 2 clases, el mismo `m` lo deja en 0,95. Es la única palanca que sube la marca cuando ya estás pegado al techo |
| `C` | Número de clases del problema | recuento | Con más clases, el mismo conflicto cuesta **más**, porque acertar al azar es más difícil: 0,10 de conflicto cuesta 0,05 con 2 clases y 0,09 con 10. No es una palanca que puedas tocar, pero explica por qué el mismo porcentaje de desacuerdo es más grave en un problema de muchas clases que en uno binario |
| `ρ` | Tasa de etiquetas cambiadas por otra clase al azar | tanto por uno | Deforma la exactitud que mides, no la que tienes. Con `ρ = 0,20` y 10 clases, un modelo que acierta el 90 % de verdad aparece como 0,74; al subir `ρ`, el número medido se comprime hacia `1/C` y las diferencias entre modelos parecen desaparecer |
| `acc_medida` | Exactitud calculada contra las etiquetas que tienes | tanto por uno | Es la que ves en el informe. Sube cuando el modelo mejora, pero también cuando bajan `ρ` o `C`, así que no es comparable entre conjuntos con distinto ruido |
| `acc_real` | Exactitud contra las etiquetas verdaderas | tanto por uno | Es la que importa y no se observa. Se estima con la corrección, y solo es fiable si el ruido es simétrico y tienes una estimación decente de `ρ` |
| `κ` | Kappa de Cohen: acuerdo entre anotadores más allá del azar | tanto por uno | Al subir, el conjunto es más fiable y el techo medido se parece más al de verdad. Por debajo de 0,6 la referencia es blanda: conviene reescribir las instrucciones de anotación antes de tocar el modelo |
| `p_o` | Acuerdo observado entre dos anotadores | tanto por uno | Sube cuando el criterio es más nítido. Es engañoso por sí solo: con clases muy desbalanceadas, dos anotadores que siempre dicen «no» coinciden en el 95 % sin haber anotado nada |
| `p_e` | Acuerdo esperado por azar según las frecuencias | tanto por uno | Sube con el desbalanceo de clases y con menos clases. Es el listón que `p_o` tiene que superar para que el acuerdo signifique algo |
:::

## Ejemplo

**1. El techo de un problema con conflicto.** 2.000 ejemplos, 4 clases y 120 ejemplos (un 6 %)
donde el criterio es ambiguo. El techo vale `1 − 0,06 + 0,06/4 = 0,955`. Un modelo que saca
0,952 está a tres milésimas del techo: no queda nada que rascar y cualquier hora extra de
entrenamiento es tiempo perdido. Un modelo que saca 0,85 sí tiene diez puntos de margen real, y
ahí la conversación es otra.

**2. La exactitud que mides no es la que tienes.** Clasificador de 10 clases que acierta el
90 %, evaluado contra etiquetas con un 20 % de cambios al azar:

```
exactitud real      0.9010
exactitud medida    0.7411
exactitud corregida 0.9014
```

El 0,74 no dice «el modelo es flojo»: dice que el 20 % de ruido comprime cualquier exactitud
hacia 0,10, que es lo que vale acertar al azar entre diez clases. La corrección recupera el
valor real con un error de tres milésimas, que es el margen que da mirar 200.000 ejemplos.

**3. Dónde está el techo cuando hay conflicto.** Un árbol de decisión entrenado sobre 5.600
ejemplos con un 15 % de etiquetas cambiadas, medido sobre un conjunto de prueba limpio:

```
profundidad    2  entrenamiento 0.7087  prueba 0.7400
profundidad    4  entrenamiento 0.7602  prueba 0.7863
profundidad    6  entrenamiento 0.7850  prueba 0.7804
profundidad   12  entrenamiento 0.9055  prueba 0.7250
profundidad None  entrenamiento 1.0000  prueba 0.6871
```

El árbol sin límite de profundidad acierta el 100 % de lo que se le pidió y solo el 68,7 % de lo
que importa: la diferencia entre esas dos cifras es el ruido memorizado, no conocimiento. El
techo aquí es el punto —entre profundidad 4 y
6— donde más capacidad empieza a restar, no una línea horizontal contra la que chocas. Si solo hubieras entrenado el modelo grande, habrías
concluido que el problema es difícil; la curva entera dice que el problema es que las etiquetas
mienten.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(0)
C, n = 10, 200_000
y = rng.integers(0, C, n)                                       # etiqueta verdadera
acierta = rng.random(n) < 0.90                                  # el modelo acierta el 90 %
y_pred = np.where(acierta, y, (y + rng.integers(1, C, n)) % C)  # cuando falla, cae en otra clase

rho = 0.20                                                      # 20 % de etiquetas cambiadas al azar
cambiada = rng.random(n) < rho
y_ruidosa = np.where(cambiada, rng.integers(0, C, n), y)

medida = (y_pred == y_ruidosa).mean()
real = (y_pred == y).mean()
corregida = (medida - rho / C) / (1 - rho)

print(f"exactitud real      {real:.4f}")       # -> 0.9010
print(f"exactitud medida    {medida:.4f}")     # -> 0.7411
print(f"exactitud corregida {corregida:.4f}")  # -> 0.9014
```

:::claves
- La corrección `(medida - rho / C) / (1 - rho)` sale de despejar la fórmula de la sección anterior. No es un truco de estilo: es la única forma de comparar dos modelos evaluados con distinto ruido, y falla en cuanto el ruido deja de ser simétrico.
- `(y + rng.integers(1, C, n)) % C` genera una clase **distinta** de la verdadera: `rng.integers(1, C, n)` devuelve valores entre 1 y `C-1`, y el módulo da la vuelta al pasar de `C-1`. Si usaras `rng.integers(0, C, n)` a secas, en uno de cada diez casos el «fallo» coincidiría con la etiqueta correcta y la exactitud real saldría inflada.
- `rng.integers(0, C, n)` **excluye** el límite superior: genera de 0 a `C-1`. Es el error clásico al pasar de `random.randint` de la biblioteca estándar, que sí incluye los dos extremos.
- `y_ruidosa = np.where(cambiada, rng.integers(0, C, n), y)` consume el generador en la rama del `where` aunque el valor se descarte en las posiciones no cambiadas. Importa si comparas dos ejecuciones: cambiar el orden de las llamadas al generador cambia todos los números siguientes.
- Las tres cifras salen de la **misma** `y` y la **misma** `y_pred`; lo único que cambia es contra qué se comparan. Por eso `real` y `corregida` coinciden: son la misma cantidad medida de dos formas.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(7)
n, C = 200_000, 2
y = rng.integers(0, C, n)
m = 0.05                                        # 5 % de ejemplos con etiqueta en conflicto
ambiguo = rng.random(n) < m
y_etiquetada = np.where(ambiguo, rng.integers(0, C, n), y)

techo = 1 - m + m / C                           # lo mejor que puede hacer cualquier modelo
empirico = ((~ambiguo).sum() + ambiguo.sum() / C) / n
acuerdo = (y_etiquetada == y).mean()

print(f"techo teorico   {techo:.4f}")           # -> 0.9750
print(f"techo empirico  {empirico:.4f}")        # -> 0.9752
print(f"acuerdo con la verdad  {acuerdo:.4f}")  # -> 0.9753
```

:::claves
- `empirico` se calcula sin simular ningún clasificador: cuenta los ejemplos no ambiguos y suma `1/C` por cada ambiguo. Es la accuracy **esperada** del oráculo, y por eso es determinista; si en lugar de eso simularas las monedas al aire, el número variaría en cada ejecución y no podrías escribir un `# ->` fijo.
- `techo` y `empirico` coinciden salvo por el muestreo de `ambiguo`: el segundo usa la fracción realizada en esta muestra (0,9752) y el primero la fracción teórica `m`. Con 200.000 ejemplos la diferencia está en la cuarta decimal.
- En este modelo concreto, `acuerdo` —cuántas veces la etiqueta que tienes coincide con la verdad— coincide con el techo. Es una coincidencia del ruido simétrico, no una ley: sirve para ver de un vistazo que cuando el 2,5 % de las etiquetas son monedas al aire, el techo baja exactamente esos 2,5 puntos.
- `(~ambiguo).sum()` invierte la máscara booleana y cuenta los no ambiguos. Sobre un array de `bool`, `~` es la negación lógica elemento a elemento, no el complemento a nivel de bits de un entero.
:::

```python verificable
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

rng = np.random.default_rng(1)
n = 8_000
X = rng.normal(0, 1, (n, 8))
senal = 1.2 * X[:, 0] + 0.8 * X[:, 1]
y = (senal + rng.normal(0, 1.0, n) > 0).astype(int)

# Se parte primero y se ensucia despues: la prueba queda limpia y el techo lo pone el ruido de entrenamiento
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)
ruido = rng.random(len(y_tr)) < 0.15
y_tr[ruido] = rng.integers(0, 2, len(y_tr))[ruido]

for prof in (2, 4, 6, 12, None):
    arbol = DecisionTreeClassifier(max_depth=prof, random_state=0).fit(X_tr, y_tr)
    print(f"profundidad {str(prof):>4}  entrenamiento {arbol.score(X_tr, y_tr):.4f}"
          f"  prueba {arbol.score(X_te, y_te):.4f}")
# -> profundidad    4  entrenamiento 0.7602  prueba 0.7863   (el mejor)
# -> profundidad None  entrenamiento 1.0000  prueba 0.6871   (memoriza el ruido)
```

:::claves
- El orden importa y es la mitad de la lección: se hace `train_test_split` **antes** de ensuciar. Si corrompes el conjunto entero y luego partes, la prueba también queda ruidosa y el techo se confunde con el error de medición.
- `y_tr[ruido] = rng.integers(0, 2, len(y_tr))[ruido]` solo toca las posiciones marcadas. Escribirlo como `y_tr = rng.integers(...)` machacaría todas las etiquetas y el problema dejaría de tener señal.
- `max_depth=None` deja al árbol crecer hasta que cada hoja es pura. Es lo que produce el `entrenamiento 1.0000`: no es un logro, es la definición de memorizar.
- `DecisionTreeClassifier(random_state=0)` fija el desempate entre divisiones igual de buenas. Sin él, dos ejecuciones dan árboles distintos y la comparación entre profundidades se llena de ruido.
- La exactitud de prueba **sube y luego baja**: el máximo está en profundidad 4, no en la más grande. Ese es el patrón que hay que buscar cuando se sospecha ruido en las etiquetas.
:::

## Errores típicos

- **Confundir «el modelo no da más» con «el problema no da más».** Son dos frases que suenan
  igual y llevan a sitios opuestos. La forma de distinguirlas es la curva de aprendizaje y el
  acuerdo entre anotadores, no la intuición.
- **Tratar todo el ruido como si fuera simétrico.** La corrección `(medida − ρ/C) / (1 − ρ)` es
  correcta bajo un supuesto fuerte. Si los anotadores confunden dos clases parecidas mucho más
  que las demás, aplicar la fórmula te deja creyendo que el modelo es mejor de lo que es.
- **Auditar el conjunto de entrenamiento y no el de prueba.** El error de etiquetado en el
  conjunto de prueba es el más caro, porque es el que decide qué modelo se publica, y da la
  casualidad de que es el que nadie revisa. Una métrica calculada sobre un test con un 5 % de errores
  ordena mal los modelos.
- **Subir la capacidad para superar el techo.** Con más parámetros el modelo memoriza las
  etiquetas malas más rápido. La pérdida de entrenamiento baja, la de validación no, y la
  diferencia entre ambas se abre: eso apunta al ruido entrando en los pesos, no a un sobreajuste
  que se arregle con regularización.
- **Reetiquetar con las predicciones del propio modelo.** El pseudoetiquetado cambia opiniones
  por etiquetas y refuerza los mismos errores que ya tenía. Si lo usas, mide el efecto
  sobre un conjunto auditado a mano, nunca sobre las etiquetas que acabas de generar.
- **Mirar solo la media del desacuerdo.** Un 8 % de conflicto repartido por igual entre clases
  es un problema; el mismo 8 % concentrado en dos clases que el negocio necesita distinguir es
  otro muy distinto. Desglosa el desacuerdo por clase antes de decidir.

:::practica
enunciado: Un problema de 4 clases con 5.000 ejemplos tiene 600 etiquetas en conflicto (el criterio no las determina). El modelo saca 0,905 de exactitud en validación. Además, en una segunda medición con 15 % de etiquetas cambiadas al azar el modelo aparece con 0,80 sobre 4 clases. ¿Está el modelo en el techo? ¿Cuál es su exactitud real?
pista: Calcula primero el techo con `1 − m + m/C` y la exactitud real despejando `acc_medida = (1 − ρ)·acc_real + ρ/C`.
solucion: El conflicto es m = 600/5.000 = 0,12 y C = 4, así que el techo vale 1 − 0,12 + 0,12/4 = 0,91. El modelo saca 0,905: está a media milésima del techo, no hay margen de mejora por la vía del modelo. La segunda medición es otra cosa: con ρ = 0,15 y C = 4, ρ/C = 0,0375 y acc_real = (0,80 − 0,0375)/0,85 = 0,897. Es decir, el modelo acierta de verdad cerca del 90 %, que es coherente con estar pegado al techo de 0,91. Lo que hay que arreglar son las 600 etiquetas ambiguas, no la arquitectura.
:::

## Comprueba que lo sabes

:::quiz
p: La métrica de validación se estanca en 0,86 y añades capas: la pérdida de entrenamiento baja a 0,01 y la de validación sigue en 0,86. ¿Qué es lo más probable?
o: Que el modelo necesita regularización, porque hay sobreajuste clásico
o: Que el techo lo pone la calidad de las etiquetas y la capacidad extra solo está memorizando el ruido
o: Que la tasa de aprendizaje es demasiado alta y el modelo no converge
a: 2
e: La brecha entre entrenamiento y validación puede ser sobreajuste, pero el dato decisivo es que la validación no se mueve mientras el entrenamiento se desploma hacia cero. Eso es el patrón de ruido en las etiquetas: el modelo aprende las etiquetas malas porque son las únicas que le quedan por ajustar. La regularización lo frenaría sin subir la marca.
:::

:::quiz
p: En un problema de 2 clases, una auditoría encuentra que el 10 % de las etiquetas son ambiguas. ¿Cuál es el techo de exactitud?
o: 0,90, porque se pierde exactamente el 10 % de los ejemplos
o: 0,95, porque de los ambiguos se acierta la mitad
o: 0,99, porque el conflicto solo afecta a unas pocas clases
a: 2
e: Con C = 2, el techo es 1 − m + m/C = 1 − 0,10 + 0,05 = 0,95. Se aciertan todos los ejemplos claros y la mitad de los ambiguos, no ninguno: por eso el techo es más alto que 0,90. En un problema binario cada punto de conflicto cuesta medio punto de exactitud.
:::

:::quiz
p: ¿Para qué sirve el kappa de Cohen al evaluar la calidad de las etiquetas?
o: Para medir el porcentaje de ejemplos en los que dos anotadores coinciden
o: Para estimar cuántos ejemplos habría que reetiquetar
o: Para medir el acuerdo entre anotadores descontando el que se produciría por azar
a: 3
e: El acuerdo bruto engaña: con clases muy desbalanceadas, dos anotadores que siempre eligen la clase mayoritaria coinciden mucho sin haber anotado nada. El kappa resta el acuerdo esperado por azar y deja solo el que aporta información sobre la nitidez del criterio.
:::

:::aviso
Si el techo está por debajo de lo que pide el negocio, la decisión correcta puede ser cambiar la
definición de la etiqueta o el problema, no el modelo. Es una conversación incómoda y hay que
llegar a ella con el número del techo medido, no con la impresión de que «los datos son malos».
:::
