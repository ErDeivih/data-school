---
id: dropout-y-regularizacion
titulo: Dropout y regularización
fase: 7
nivel: intermedio
rutas: [ds]
prerequisitos: [regularizacion-l1-l2, sesgo-varianza, sobreajuste-en-redes]
tags: [regularizacion, sobreajuste, dropout, aumentos]
resumen: Apagar neuronas al azar, encoger los pesos, parar a tiempo o inventar datos que no cambian la etiqueta: cuatro formas de encarecer la memorización.
fuentes: ["Srivastava et al. (2014), 'Dropout: A Simple Way to Prevent Neural Networks from Overfitting'", "Li et al. (2018), 'Understanding the Disharmony between Dropout and Batch Normalization by Variance Shift'", "Goodfellow, Bengio y Courville (2016), 'Deep Learning', cap. 7"]
---

## En una frase

Regularizar es modificar el entrenamiento para que memorizar los datos de entrenamiento salga
más caro que aprender el patrón: el **dropout** apaga neuronas al azar en cada paso, el
decaimiento de pesos las encoge, la parada temprana corta el entrenamiento en el mejor momento
y el aumento de datos multiplica los ejemplos que el modelo ve.

## La idea

Cuando una red es mucho más grande que los datos que tiene, acaba memorizándolos: la pérdida de
entrenamiento sigue bajando mientras la de validación empieza a subir. El modelo ha aprendido
el ruido del conjunto concreto que le diste, no la regla que hay detrás. Eso es el
[[sesgo-varianza|compromiso sesgo-varianza]] en acción, y hay cuatro formas de pelearse con él.

La primera es **ver más datos**. Cada ejemplo nuevo es una restricción más y el ruido concreto
de cada uno importa menos. Es la solución más eficaz, y por eso el aumento de datos —recortes,
giros, ruido, mezclas, deformaciones del tiempo— suele dar más rendimiento que cualquier truco
de arquitectura. Con una condición: la transformación tiene que conservar la etiqueta. Girar
una foto de un gato sigue siendo un gato; girar un 6 lo convierte en un 9 y le estás enseñando
mentiras al modelo.

La segunda es el **dropout**. En cada paso de entrenamiento, cada activación se apaga con
probabilidad `p` y las que sobreviven se dividen entre `1 − p`. Atendiendo a un solo paso,
parece una mutilación: en una capa de 1000 unidades, con `p = 0,5` se apagan unas 500. Hay dos
lecturas de por qué funciona. La primera es que estás entrenando, a la vez y compartiendo pesos,
un conjunto enorme de subredes distintas, y en inferencia promedias todas (el reescalado
`1/(1 − p)` es justo lo que hace que la esperanza no cambie). La segunda, más terrenal: impide
que una neurona se apoye en otra concreta para corregir su error. Si su compañera desaparece la
mitad de las veces, aprende a ser útil por sí misma. Se llama evitar la **coadaptación**, y es
la razón de que el dropout se ponga sobre todo en capas ocultas grandes.

La tercera es el **decaimiento de pesos**: sumar a la pérdida una penalización proporcional a la
suma de los cuadrados de los pesos. Con SGD puro eso equivale a multiplicar cada peso por
`(1 − η·λ)` en cada paso, de ahí el nombre. Leído como estadística bayesiana, es poner una
distribución previa gaussiana centrada en cero sobre los pesos: ver
[[estimacion-bayesiana-map|estimación bayesiana y MAP]]. La cuarta es la **parada temprana**:
mirar la métrica de validación y quedarte con el modelo del mejor momento. Es la regularización
más barata que existe y la que más veces se olvida.

:::nota
Si tu modelo **no** sobreajusta, regularizar empeora las cosas: la pérdida de entrenamiento
sube, la de validación también y has añadido un hiperparámetro que no necesitabas. El orden
razonable es: más datos y aumentos, luego decaimiento de pesos, luego parada temprana, y el
dropout cuando las capas ocultas son grandes y aun así memoriza.
:::

## Definición formal

En entrenamiento, con `p` la probabilidad de apagar cada unidad:

:::formula
mᵢ ~ Bernoulli(1 − p)          h'ᵢ = mᵢ · hᵢ / (1 − p)
:::

- `p` — probabilidad de apagar una unidad; los valores habituales van de 0,1 a 0,5.
- `mᵢ` — máscara aleatoria: vale 1 con probabilidad `1 − p` y 0 con probabilidad `p`,
  independiente por unidad y por paso.
- `1/(1 − p)` — factor de reescalado. Mantiene la esperanza: `E[h'] = (1 − p) · h/(1 − p) = h`.
- En inferencia se usa `h' = h`: ni máscara ni reescalado. Este esquema se llama dropout
  invertido y es el que implementa PyTorch.

La penalización L2, con `λ` el coeficiente y `w` los pesos:

:::formula
L_total = L + (λ/2) · Σⱼ wⱼ²          w ← w · (1 − η·λ) − η·∇L
:::

- `λ` — cuánto pesa la penalización frente a la pérdida de los datos. El `½` es la convención que
  hace que el gradiente de la penalización sea `λ·w` a secas, y de ahí el factor `(1 − η·λ)` de la
  derecha; con `L + λ·Σw²` el factor sería `(1 − 2·η·λ)`.
- `Σⱼ wⱼ²` — suma de los cuadrados de todos los pesos; normalmente se excluyen sesgos y
  parámetros de normalización.
- `η` — tasa de aprendizaje. La segunda forma solo es exactamente equivalente con SGD puro; con
  Adam la penalización entra en el gradiente y se divide por `√v̂`, así que se usa `AdamW`.

El etiquetado suave cambia los objetivos en vez de los pesos, con `K` clases y `ε` el suavizado:

:::formula
y_suave = (1 − ε) · y + ε / K
:::

- `ε` — suavizado típico de 0,1; reparte un poco de probabilidad entre todas las clases.
- Evita que el modelo aprenda a dar probabilidad 1 a todo, lo que además estropea la
  [[calibracion|calibración]].

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `p` | probabilidad de apagar cada unidad en cada paso | adimensional, entre 0 y 1 | Más unidades apagadas y más reescalado: sube la regularización y baja la capacidad efectiva. Con `p = 0,5` desaparece la mitad de la capa; en la capa de entrada o en la de salida se usa 0 o valores muy bajos |
| `mᵢ` | máscara aleatoria de esa unidad: 1 con probabilidad `1 − p`, 0 con probabilidad `p` | adimensional, 0 o 1 | No se ajusta: se sortea en cada paso. Su media es `1 − p`, y por eso el reescalado la compensa |
| `1/(1 − p)` | factor que multiplica a las unidades que sobreviven | adimensional | Mantiene la esperanza. Cuando `p` se acerca a 1 el factor se dispara: quedan pocas unidades multiplicadas por mucho y la varianza de cada sorteo se vuelve enorme |
| `h` | activación de la capa antes del dropout | las de la activación | Es la señal que se apaga y se reescala. Su esperanza no cambia, pero un sorteo concreto sí |
| `λ` | coeficiente de la penalización L2 | 1 partido por las de `w` al cuadrado | Con SGD el peso se multiplica por `(1 − η·λ)` en cada paso: al subir, encoge más. Un factor 10 pasa de «encoger un poco» (0,368 tras 1000 pasos) a «borrar el peso» |
| `w` | peso del modelo | adimensional | Al crecer crece también `λ·w²`: la penalización castiga más a los pesos que ya son grandes, que es justo lo que se busca |
| `η` | tasa de aprendizaje | las de `w` partido por las de `g` | Multiplica el efecto del decaimiento, porque lo que encoge el peso en cada paso es el producto `η·λ`: al subir `η` regularizas más aunque no toques `λ` |
| `K` | número de clases del problema | clases | Reparte el suavizado entre todas: con muchas clases cada una recibe muy poco y el efecto del etiquetado suave se diluye |
| `ε` | suavizado del etiquetado (0,1 en el uso habitual) | adimensional, entre 0 y 1 | Reparte probabilidad entre todas las clases: al subir, el modelo deja de dar probabilidad 1 a todo, la calibración mejora y la pérdida ya no puede llegar a cero |
| `y_suave` | objetivo suavizado que entra en la pérdida | probabilidad por clase | Es lo que de verdad se optimiza con etiquetado suave; sus componentes siguen sumando 1, así que no cambia la escala de la pérdida |
:::

## Ejemplo

**Dropout.** Una capa con activaciones `h = [2, −1, 0,5, 3]` y `p = 0,5`. Sale la máscara
`[1, 1, 1, 0]`: se apaga la última unidad y las demás se dividen entre 0,5, es decir, se
duplican. El resultado es `[4, −2, 1, 0]`. La media de ese sorteo concreto es
`(4 − 2 + 1 + 0)/4 = 0,75`, bastante por debajo de la media original, `1,125`. Eso no es un
error: es que con cuatro unidades una máscara concreta cambia mucho. Si repites el sorteo 20 000
veces, la media de las medias sale 1,1227, prácticamente la original. La esperanza se conserva;
la varianza de un sorteo concreto, no.

**Decaimiento de pesos.** Un peso que vale 1, con `η = 0,1` y `λ = 0,01`, se multiplica por
`(1 − 0,1 · 0,01) = 0,999` en cada paso. Tras 1000 pasos vale `0,999¹⁰⁰⁰ = 0,368`: ha perdido el
63 % de su valor sin que ningún gradiente se lo haya pedido. Con `λ = 0,1` el factor es 0,99 y
tras 1000 pasos el peso vale 0,99¹⁰⁰⁰ = 4,3·10⁻⁵, que con tres decimales se imprime como 0,000. Un
factor 10 en `λ` pasa de «encoger un poco» a «borrar el
peso»: por eso `λ` se ajusta en escala logarítmica y con cuidado.

**Parada temprana.** Si la pérdida de validación por época es 0,42 → 0,39 → 0,40 → 0,45
mientras la de entrenamiento sigue bajando (0,30 → 0,22 → 0,18 → 0,15), el modelo bueno es el de
la segunda época. Guardar el mejor `state_dict` según validación cuesta tres líneas y evita
semanas de mirar curvas.

:::figura
fichero: dropout-y-regularizacion-esperanza-y-encogimiento
pie: El panel izquierdo enumera los 16 sorteos posibles de la máscara sobre una capa de cuatro unidades con p = 0,5. Ninguno tiene por qué dar la media de la capa (1,125) —el del ejemplo de arriba da 0,75— pero el promedio de los 16 cae exactamente en 1,125: eso, y no otra cosa, es lo que arregla el reescalado 1/(1−p). La consecuencia práctica es doble: la pérdida de un lote concreto es ruidosa aunque el método sea insesgado, y con pocas unidades por capa ese ruido pesa mucho más. El panel derecho mide el decaimiento de pesos con un peso que no recibe gradiente ninguno. Las dos rectas son el factor (1 − η·λ) elevado al número de pasos, y en escala logarítmica un decaimiento exponencial es una recta, así que su pendiente lee directamente la fuerza de la regularización. Con λ = 0,01 el peso acaba en 0,368 tras mil pasos; con λ = 0,1, en 4·10⁻⁵. Un factor 10 en λ separa «encoger un poco» de «borrar el peso», y de ahí que λ se ajuste en escala logarítmica y que no se aplique a sesgos ni a los parámetros de normalización.
fuente: figuras/dropout-y-regularizacion-1.py
:::

## Código

```python verificable
import numpy as np

h = np.array([2.0, -1.0, 0.5, 3.0])
p = 0.5
rng = np.random.default_rng(7)

mascara = (rng.random(h.size) >= p).astype(float)
# >= p deja la mascara a 1 con probabilidad 1-p; astype(float) la convierte en 0.0 y 1.0
print(f"mascara {mascara}")                              # -> mascara [1. 1. 1. 0.]
print(f"salida  {np.round(h * mascara / (1 - p), 2)}")   # -> salida  [ 4. -2.  1.  0.]

# La esperanza se conserva aunque cada sorteo concreto la mueva.
medias = []
for _ in range(20000):
    m = (rng.random(h.size) >= p).astype(float)
    medias.append((h * m / (1 - p)).mean())
print(f"media teorica {h.mean():.4f}  media simulada {np.mean(medias):.4f}")
# -> media teorica 1.1250  media simulada 1.1227
```

:::claves
- El **signo** de la comparación decide qué fracción sobrevive: `rng.random(...) >= p` pone la
  máscara a 1 con probabilidad `1 − p`, que es lo que dice la fórmula. Con `< p` sobreviviría solo
  la fracción `p` y el reescalado `1/(1 − p)` estaría compensando justo lo contrario.
- `.astype(float)` no es cosmético. Sin él, `h * mascara` también funciona (el `True` vale 1),
  pero el `print` muestra `[ True  True  True False]` y la división deja de leerse como la
  fórmula. Convertir la máscara a número antes de multiplicar evita ese lío.
- `np.random.default_rng(7)` crea un generador **propio** y no toca el estado global. Con
  `np.random.seed(7)` cualquier otra parte del programa comparte ese estado y la secuencia deja
  de ser reproducible en cuanto alguien más sortea. Además, `default_rng(7)` **no** produce los
  mismos números que `np.random.seed(7)`: son dos generadores distintos.
- `rng.random(h.size)` pide un vector de 4 números. Si se te olvida el `h.size`, devuelve **un
  escalar** y la máscara deja de ser un vector; el fallo aparece más tarde, al multiplicar.
- `medias` es una lista de Python, no un array: `np.mean(medias)` la recorre y la convierte por
  dentro. Para 20 000 elementos es lo legible; en un bucle de verdad conviene preasignar un array
  y escribir por índice, porque añadir a una lista tiene su coste.
- `h.mean()` (1,1250) es la media **teórica** de la salida, no la de `h` reescalada: como
  `E[m] = 1 − p` y el factor divide por `1 − p`, la esperanza vuelve a ser `h`. La simulación da
  1,1227 porque son 20 000 sorteos, no infinitos; con otra semilla saldría otro decimal parecido.
:::

```python verificable
import numpy as np

# Decaimiento de pesos: sin gradiente, solo el factor (1 - eta*lambda) por paso.
eta = 0.1
for lam in (0.01, 0.1):
    # {lam:<5} alinea a la izquierda en 5 caracteres: sin eso las dos lineas salen desalineadas
    print(f"lambda {lam:<5} factor por paso {1 - eta * lam:.4f}  tras 1000 pasos {(1 - eta * lam) ** 1000:.3f}")
# -> lambda 0.01  factor por paso 0.9990  tras 1000 pasos 0.368
# -> lambda 0.1   factor por paso 0.9900  tras 1000 pasos 0.000
```

```python ilustrativo
import torch
import torch.nn as nn

class Red(nn.Module):
    def __init__(self):
        super().__init__()
        self.capa = nn.Linear(256, 256)
        self.drop = nn.Dropout(p=0.3)        # 30 % de las activaciones, cada paso
        self.salida = nn.Linear(256, 10)

    def forward(self, x):
        return self.salida(self.drop(torch.relu(self.capa(x))))

modelo = Red()
modelo.train()                  # con dropout activo
modelo.eval()                   # imprescindible al evaluar: dropout desactivado

# El decaimiento de pesos se configura en el optimizador, no en la capa
optimizador = torch.optim.AdamW(modelo.parameters(), lr=3e-4, weight_decay=0.01)

# Parada temprana: guardar el mejor estado segun validacion
mejor = float("inf")
for epoca in range(50):
    entrenar_una_epoca(modelo, optimizador)
    perdida_val = evaluar(modelo, val)
    if perdida_val < mejor:
        mejor = perdida_val
        torch.save(modelo.state_dict(), "mejor.pt")
```

## Errores típicos

- **Olvidar `model.eval()` al evaluar.** Con dropout activo, cada predicción se calcula con una
  máscara aleatoria distinta: la misma imagen da clases diferentes en dos ejecuciones y la
  métrica de validación se hunde sin que el modelo tenga nada malo. Es el fallo más común de
  todos los que se cometen con regularización.
- **Añadir dropout para arreglar un modelo que no aprende.** El dropout quita capacidad: si la
  pérdida de entrenamiento ya es alta, apagar neuronas la sube más. El dropout es para cuando
  hay mucha diferencia entre entrenamiento y validación, no antes.
- **Poner `p = 0,5` en la capa de entrada o en la de salida.** En la entrada destruyes
  información del propio dato (con `p = 0,5` la mitad de las características desaparecen), y en
  la salida no tiene sentido porque es la que produce la predicción. En esas posiciones se usa
  0 o valores muy bajos.
- **Reescalar a mano además de lo que ya hace la librería.** Si aplicas tu propia división por
  `1 − p` y usas `nn.Dropout`, escalas dos veces: las activaciones en entrenamiento salen el
  doble de grandes que en inferencia y el modelo aprende con la escala equivocada.
- **Poner decaimiento de pesos a todo por igual.** Los sesgos y los parámetros `γ` y `β` de las
  capas de [[normalizacion-por-lotes|normalización]] no deben encogerse: limitan la capacidad
  del modelo sin aportar regularización útil. Sepáralos en un grupo sin decaimiento.
- **Usar el decaimiento L2 dentro de Adam y creer que es lo mismo que en SGD.** El término
  entra en el gradiente y se normaliza con `√v̂`, así que los parámetros con gradientes grandes
  reciben menos encogimiento efectivo del que has configurado. Usa `AdamW` si quieres
  decaimiento de pesos de verdad.

:::practica
enunciado: Una capa tiene las activaciones h = [3, −2, 4, 1, 0,5, 5] y dropout con p = 1/3. La máscara de este paso apaga la tercera y la quinta unidad. Escribe la salida con su reescalado, calcula la media de h y la de la salida, y explica por qué no coinciden.
pista: Las unidades que sobreviven se dividen entre 1 − p = 2/3, es decir se multiplican por 1,5; las apagadas quedan en cero.
solucion: La máscara es (1, 1, 0, 1, 0, 1) y la salida es (4,5; −3; 0; 1,5; 0; 7,5). La media de h es 11,5/6 = 1,917 y la de la salida es 10,5/6 = 1,75: un sorteo concreto mueve la media porque solo hay seis unidades. El factor 1,5 no arregla cada máscara, arregla la esperanza: promediando muchos sorteos, la media vuelve a 1,917.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué las activaciones que sobreviven al dropout se dividen entre `1 − p`?
o: Para que la salida de la capa tenga varianza 1
o: Para que la esperanza de la activación sea la misma en entrenamiento y en inferencia
o: Para compensar el efecto de la regularización L2
a: 2
e: Sin el reescalado, en entrenamiento las activaciones valdrían de media (1 − p)·h y en inferencia h: el modelo estaría calibrado para una escala que ya no existe. Dividir entre 1 − p devuelve la esperanza a h. No tiene nada que ver con la varianza (que sí cambia en cada sorteo) ni con la penalización L2, que es otro mecanismo distinto.
:::

:::quiz
p: Entrenas con dropout y en validación obtienes una exactitud mucho peor que en entrenamiento, con la misma métrica y los mismos datos. ¿Qué es lo primero que revisas?
o: Si has llamado a `model.eval()` antes de evaluar
o: Si la tasa de aprendizaje es demasiado alta
o: Si el conjunto de validación está mal etiquetado
a: 1
e: En modo entrenamiento el dropout sigue activo y cada evaluación usa máscaras nuevas: el resultado es ruidoso y peor. `model.eval()` desactiva dropout (y hace que la normalización use sus estadísticas acumuladas). Una tasa de aprendizaje alta también da malas métricas, pero el síntoma típico del modo equivocado es una diferencia grande y ruidosa entre entrenamiento y validación.
:::

:::quiz
p: Un peso vale 1 y no recibe gradiente nunca. Con `η = 0,1` y `λ = 0,01`, ¿cuánto vale tras 1000 pasos y por qué?
o: 1, porque sin gradiente no hay actualización
o: 0,368, porque el decaimiento de pesos lo multiplica por 0,999 en cada paso
o: 0, porque el decaimiento lo borra siempre
a: 2
e: En SGD, la penalización L2 es exactamente un factor multiplicativo (1 − η·λ) por paso, así que actúa aunque el gradiente de los datos sea cero: 0,999¹⁰⁰⁰ = 0,368. No llega a cero con ese λ; con λ = 0,1 el factor es 0,99 y sí queda prácticamente en cero, que es la señal de que el coeficiente es demasiado alto.
:::

:::trampa
El aumento de datos solo es regularización si **conserva la etiqueta** en tu problema. Girar o
recortar funciona en fotos de objetos y falla en dígitos escritos, en textos (cambiar una
palabra cambia el significado) y en series temporales (desplazar la ventana cambia el futuro).
Revisa siempre la transformación con ejemplos reales antes de darla por buena.
:::
