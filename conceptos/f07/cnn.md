---
id: cnn
titulo: Redes convolucionales
fase: 7
nivel: avanzado
rutas: [ds]
prerequisitos: [perceptron-y-mlp, funciones-de-activacion, operaciones-matriciales]
tags: [vision, convolucion, imagenes, pesos-compartidos]
resumen: Deslizar el mismo filtro diminuto por toda la imagen y compartir los pesos permite ver bordes, texturas y objetos con muy pocos parámetros.
fuentes: ["LeCun et al. (1998), 'Gradient-Based Learning Applied to Document Recognition'", "Goodfellow, Bengio y Courville (2016), 'Deep Learning', cap. 9"]
---

## En una frase

Una convolución aplica el mismo filtro pequeño en cada posición de la imagen; como los pesos se
comparten, la red aprende a detectar un patrón una sola vez y lo reconoce esté donde esté,
gastando una fracción de los parámetros que necesitaría una capa densa.

## La idea

Coge una foto de 32×32 píxeles en color: 3.072 números. Si la conectas a una capa densa de solo
16 neuronas, necesitas 49.168 pesos. Y hay un problema peor que el tamaño: esa capa tiene que
aprender por separado «un gato en la esquina superior izquierda» y «un gato en el centro»,
porque cada píxel llega a una neurona distinta.

Ahora piensa en cómo miras tú una foto. No analizas la posición absoluta de cada píxel: buscas
un patrón (un borde, una curva, un ojo) y lo buscas **en todas partes**. Si encuentras un ojo
arriba a la izquierda, sabes reconocer el mismo ojo abajo a la derecha. Eso es exactamente una
convolución: un filtro diminuto (3×3, 5×5) que se desliza por toda la imagen y produce un mapa
que dice «aquí he visto este patrón» con más o menos fuerza.

De ahí salen las tres propiedades que hacen funcionar a las CNN:

1. **Localidad.** Cada neurona mira solo una ventana pequeña. Tiene sentido: en una imagen, un
   píxel se relaciona con sus vecinos, no con el que está a 200 píxeles.
2. **Pesos compartidos.** El mismo filtro se usa en las 900 posiciones de una imagen de 32×32.
   Por eso una capa convolucional tiene cientos de parámetros y no decenas de miles.
3. **Equivarianza a la traslación.** Si mueves el patrón, la respuesta del filtro se mueve
   igual, no desaparece. La invarianza (que dé igual dónde esté) la aporta después la
   agrupación o el promedio global.

La arquitectura clásica es una alternancia: convolución, no linealidad, agrupación, y otra vez.
Las primeras capas detectan bordes y colores; las siguientes, combinaciones de bordes
(texturas, esquinas); las últimas, partes de objetos. Ese apilamiento es lo que hace que
aprender de arriba abajo funcione: nadie programa el detector de bordes, sale del descenso de
gradiente sobre [[retropropagacion|la retropropagación]].

## Definición formal

La operación que hacen de verdad las librerías es la **correlación cruzada** en dos
dimensiones. Para una imagen `I` (una matriz de alturas por anchuras) y un filtro `K` de lado
`F`:

:::formula
(I ⋆ K)[i, j] = Σ_{m=0}^{F−1} Σ_{n=0}^{F−1} I[i+m, j+n] · K[m, n]
:::

- `I` — la entrada de esa capa, con forma `H × W × C_in` (alto, ancho, canales de entrada).
- `K` — el filtro o *kernel*, de forma `F × F × C_in`. Cada uno de sus números es un peso
  aprendido.
- `F` — el lado del filtro (3 significa 3×3). También se llama tamaño de ventana.
- `i, j` — la posición de la salida.
- `C_in` — número de canales de entrada (3 en una imagen en color, 64 en una capa intermedia).
- `C_out` — número de filtros distintos; cada uno produce un canal de salida.

**Forma de la salida.** Con relleno `P` (ceros añadidos alrededor) y paso `S` (cuántas
posiciones se desplaza el filtro cada vez):

:::formula
H_out = ⌊(H + 2P − F) / S⌋ + 1
:::

- `P` — *padding*, el número de ceros que se añaden por cada lado. Con `P = (F−1)/2` y `S = 1`
  la salida mide lo mismo que la entrada («mismo» relleno).
- `S` — *stride*, el paso. Con `S = 2` la salida mide aproximadamente la mitad.
- `⌊·⌋` — redondear hacia abajo.

**Parámetros de una capa convolucional:** `F² · C_in · C_out + C_out`. El último término son los
sesgos, uno por filtro.

**Campo receptivo.** Es la región de la entrada original que influye en una neurona de una capa
`l`. Crece así, donde `S_k` es el paso de la capa `k`:

:::formula
r_l = r_{l−1} + (F_l − 1) · Π_{k<l} S_k
:::

**Agrupación** (*pooling*). La más común es el máximo: se parte el mapa en ventanas de `F × F`
y se conserva el valor más alto de cada una. No tiene parámetros y reduce la resolución
espacial a la mitad con `F = 2, S = 2`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `H`, `W` | alto y anchura de la entrada de la capa | píxeles | La salida crece en la misma proporción y el coste también: cada píxel de más es otra ventana que multiplicar. El número de parámetros no cambia |
| `F` | lado del filtro (3 significa 3×3) | píxeles | Los pesos de cada filtro pasan de `F²` a más y el filtro ve una zona mayor: sube la capacidad y los parámetros con `F²`, y la salida se encoge `F − 1` píxeles si no añades relleno |
| `P` | relleno de ceros alrededor de la entrada | píxeles | La salida crece; con `P = (F−1)/2` y `S = 1` mide lo mismo que la entrada. No añade parámetros, pero los ceros del borde diluyen la respuesta en las orillas |
| `S` | paso: cuántas posiciones se desplaza el filtro | píxeles | La salida se reduce más o menos en la misma proporción y el coste baja igual, pero se pierde resolución: un paso mayor que 1 puede saltarse justo el patrón que buscabas |
| `C_in` | canales de entrada (3 en color, 64 en una capa intermedia) | canales | Cada filtro necesita `F² · C_in` pesos en vez de `F²`: parámetros y coste suben en línea recta con los canales de entrada |
| `C_out` | número de filtros distintos; cada uno produce un canal | filtros | Es la palanca más directa: multiplica los parámetros y los canales de salida, y con ellos todo el coste de las capas siguientes |
| `I` | la entrada de la capa: `H × W` números por canal | adimensional (píxeles ya normalizados) | No es un ajuste, pero muerde: si dejas los píxeles de 0 a 255 en vez de 0 a 1, los productos punto son 255 veces mayores y la primera capa satura sus activaciones |
| `K` | el filtro: los `F² · C_in` pesos que se aprenden | adimensional | Es lo único que se aprende aquí. Valores grandes dan respuestas grandes y gradientes grandes; por eso se inicializan pequeños (He o Xavier) |
| `r_l` | campo receptivo: la zona de la imagen que ve una neurona de la capa `l` | píxeles | Crece con la profundidad, y mucho más deprisa si hay pasos mayores. Si es menor que el objeto que buscas, esa neurona no puede verlo entero por muy bien que se entrene |
:::

## Ejemplo

Entrada de 32×32 píxeles con 3 canales, una convolución de 3×3 con 16 filtros, relleno 1 y paso 1.

- Forma de salida: (32 + 2·1 − 3)/1 + 1 = **32×32×16**. La misma altura y anchura, 16 canales.
- Parámetros: 3² · 3 · 16 + 16 = 432 + 16 = **448**.
- La capa densa equivalente (3.072 entradas, 16 salidas): 3.072 · 16 + 16 = **49.168**.
- La convolución usa **110 veces menos parámetros** y además reconoce el patrón en cualquier
  posición.

Con paso 2 y el mismo relleno: (32 + 2 − 3)/2 + 1 = 16, es decir **16×16×16**: la mitad de lado,
un cuarto de posiciones.

Campo receptivo de dos convoluciones 3×3 con paso 1 encadenadas: 1 + (3−1) + (3−1) = **5**. Cada
neurona de la segunda capa ve una ventana de 5×5 de la imagen original. Con una agrupación de
2×2 en medio, el campo receptivo crece más deprisa porque `S` pasa a valer 2.

:::figura
fichero: cnn-ventana-y-respuesta
pie: Los cuatro paneles cuentan dos veces la misma historia. Arriba, el filtro de 3×3 lee una ventana de la imagen y la multiplica por sus nueve pesos: un valor alto significa «aquí hay un borde que va de oscuro a claro». La respuesta sale con dos picos enfrentados, uno positivo (azul) donde la intensidad sube y uno negativo (rojo) donde baja. Fíjate en lo que eso implica: el filtro no devuelve una etiqueta ni un «sí o no», devuelve cuánto se parece cada una de las posiciones al patrón que lleva dentro, y lo hace con los mismos nueve números en todas ellas. Abajo se repite todo con la barra desplazada cuatro píxeles: la respuesta es el mismo dibujo, movido, y los pesos del filtro no han cambiado. Eso es la equivarianza a la traslación, y es exactamente la razón de que una capa convolucional necesite 448 parámetros donde la capa densa equivalente necesitaría 49.168: el detector de bordes se aprende una vez y sirve en todas las posiciones. Y ahora lo que la figura NO dice, que es donde se falla: la convolución no es invariante, la salida se mueve cuando se mueve la entrada; y solo es equivariante a traslaciones, así que una rotación o un cambio de escala no desplazan la respuesta, la destruyen.
fuente: figuras/cnn-1.py
:::

## Código

```python verificable
import numpy as np

# Correlacion cruzada 2D a mano: es lo que hacen las librerias (sin girar el filtro).
imagen = np.array([[0, 0, 0, 0, 0],
                   [0, 1, 1, 1, 0],
                   [0, 1, 1, 1, 0],
                   [0, 1, 1, 1, 0],
                   [0, 0, 0, 0, 0]], dtype=float)
# Filtro que detecta un borde vertical: negativo a la izquierda, positivo a la derecha.
filtro = np.array([[-1, 0, 1],
                   [-1, 0, 1],
                   [-1, 0, 1]], dtype=float)

salida = np.zeros((3, 3))          # float64 por defecto: con dtype=int cada suma se truncaria
for i in range(3):                 # range(3) porque 5 - 3 + 1 = 3 posiciones validas
    for j in range(3):
        # imagen[i:i+3, j:j+3] es una VISTA, no una copia: no gasta memoria y escribir en
        # ella modificaria la imagen original. El * es elemento a elemento, no matricial.
        salida[i, j] = (imagen[i:i+3, j:j+3] * filtro).sum()

# astype devuelve una COPIA convertida a entero y tolist() la pasa a listas de Python: sin
# los dos se imprimiria un array de numpy, con un formato que cambia segun la version.
print(salida.astype(int).tolist())   # -> [[2, 0, -2], [3, 0, -3], [2, 0, -2]]
```

:::claves
- `imagen[i:i+3, j:j+3]` es una **vista**, no una copia: el recorte no reserva memoria nueva y
  apunta a los mismos números. Leerlo y multiplicarlo no cambia nada, pero si escribieras
  dentro (`ventana[0, 0] = 9`) estarías modificando `imagen`. Con indexación avanzada
  (`imagen[[0, 2]]`) sí hay copia, y ahí el mismo código se comportaría distinto.
- El `*` de `(ventana * filtro)` es producto **elemento a elemento**; `@` sería matricial y
  daría otra cosa. Los dos funcionan sin dar error cuando las formas encajan, así que este es
  un error que no avisa.
- `np.zeros((3, 3))` crea una matriz de `float64`. Si le pones `dtype=int`, cada suma se
  trunca: con este filtro los resultados son enteros y no se nota, pero con un filtro
  normalizado (pesos de 1/9) todas las posiciones saldrían 0 y parecería que no hay bordes.
- El `range(3)` está calculado a mano para una entrada de 5 y un filtro de 3: `5 − 3 + 1 = 3`.
  Si cambias el filtro a 5×5, `range(3)` sigue siendo válido y el bucle lee ventanas que ya no
  caben. Lo correcto es escribirlo como `H - F + 1`.
- `salida.astype(int)` **no** modifica `salida`: devuelve una copia convertida. Y `.tolist()` es
  lo que hace que la salida se imprima como `[[2, 0, -2], …]` y no como
  `array([[ 2, 0, -2], …])`, que es lo que sale de un array de numpy.
- En la segunda pieza de código, `(32 + 2 * 1 - 3) // 2 + 1` usa división entera a propósito:
  con `/` daría 16.5 y la forma de salida estaría mal. La fórmula lleva `⌊·⌋` justamente por
  eso, y es el origen del error clásico de dimensiones con paso 2.
:::

```python verificable
# Parametros de una convolucion frente a una capa densa sobre la misma entrada.
C_in, C_out, F = 3, 16, 3
conv = F * F * C_in * C_out + C_out
densa = (32 * 32 * C_in) * C_out + C_out
print("parametros conv :", conv)                 # -> 448
print("parametros densa:", densa)                # -> 49168
print("veces menos     :", round(densa / conv))  # -> 110

# Forma de salida con H=32, F=3, P=1 y dos pasos distintos.
print("S=1 ->", (32 + 2 * 1 - 3) // 1 + 1)   # -> 32
print("S=2 ->", (32 + 2 * 1 - 3) // 2 + 1)   # -> 16

# Campo receptivo de dos convoluciones 3x3 con paso 1: r = 1 + 2 + 2.
print("campo receptivo:", 1 + (3 - 1) + (3 - 1))   # -> 5
```

```python ilustrativo
import torch.nn as nn

# Un bloque convolucional tipico: convolucion, no linealidad y agrupacion.
bloque = nn.Sequential(
    nn.Conv2d(3, 32, kernel_size=3, padding=1),   # 32x32x3 -> 32x32x32
    nn.BatchNorm2d(32),
    nn.ReLU(inplace=True),
    nn.MaxPool2d(2),                              # -> 16x16x32
    nn.Conv2d(32, 64, kernel_size=3, padding=1),  # -> 16x16x64
    nn.ReLU(inplace=True),
    nn.AdaptiveAvgPool2d(1),                      # un valor por canal: 64 numeros
    nn.Flatten(),
    nn.Linear(64, 10),
)
# Una convolution 1x1 no mezcla vecinos: solo combina canales y sirve para adelgazar.
cuello = nn.Conv2d(256, 64, kernel_size=1)
```

## Errores típicos

- **Confundir convolución con correlación cruzada.** La convolución matemática gira el filtro
  180 grados; los frameworks de deep learning no lo giran. Para una red da igual (el filtro se
  aprende igual), pero si copias una fórmula de un libro de procesamiento de señal y comparas
  números, te saldrán distintos y no has hecho nada mal.
- **Calcular mal las dimensiones.** Con `S = 2` y relleno «mismo» la salida no es la mitad
  exacta cuando `H` es impar, y encadenar capas con formas mal contadas revienta en la primera
  capa densa. Escribe la fórmula y comprueba la forma con un tensor de prueba antes de entrenar.
- **Empezar con una capa densa sobre los píxeles.** Es el error que la convolución existe para
  evitar: pierdes el sesgo inductivo de localidad y disparas el número de parámetros. Si la
  entrada es una imagen, empieza con convoluciones.
- **Confundir equivarianza con invarianza, y esperar más de lo que da.** Una convolución es
  equivariante: mueves la entrada y la respuesta se mueve. La invarianza (que dé igual dónde
  esté) la consigues con agrupación, con promedio global o con aumento de datos. Y es
  equivariante **solo a traslaciones**: una rotación o un cambio de escala no desplazan la
  respuesta, la destruyen. Si tu modelo falla con el objeto girado o más pequeño, no es un fallo
  de la convolución: te faltan datos aumentados o una arquitectura preparada para eso.
- **Apilar profundidad sin conexiones residuales ni normalización.** Una CNN muy profunda sin
  atajos empeora en entrenamiento antes que en prueba, y no por sobreajuste: el gradiente se
  degrada al atravesar tantas capas. Añade conexiones residuales y
  [[normalizacion-por-lotes|normalización]].
- **Ignorar el coste de memoria.** Las activaciones intermedias de una CNN son grandes porque
  se guardan mapas de `H × W × C` por capa para la pasada hacia atrás. Es una de las razones
  por las que el lote no cabe, y el motivo por el que existe la [[gpu-y-rendimiento|precisión
  mixta]].

:::practica
enunciado: Entrada de 28×28×1. Una convolución de 5×5 con 8 filtros, relleno 2 y paso 1, seguida de una agrupación de máximo 2×2 con paso 2. ¿Qué forma sale de cada paso y cuántos parámetros tiene la convolución?
pista: Aplica H_out = ⌊(H + 2P − F)/S⌋ + 1; la agrupación 2×2 con paso 2 parte el lado por la mitad y no tiene parámetros.
solucion: Convolución: (28 + 4 − 5) / 1 + 1 = 28, luego 28×28×8, y sus parámetros son 5² · 1 · 8 + 8 = 200 + 8 = 208. La agrupación deja 14×14×8, con cero parámetros. La etapa entera aprende 208 pesos porque el mismo filtro se reutiliza en las 784 posiciones.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué una convolución 3×3 con 16 filtros sobre una entrada de 3 canales tiene 448 parámetros y la capa densa equivalente casi 50.000?
o: Porque la convolución descarta parte de los píxeles de la entrada
o: Porque cada filtro tiene 3·3·3 = 27 pesos más un sesgo, y son 16 filtros: 448. La densa necesita un peso por cada pareja entrada-salida
o: Porque la convolución usa menos bits por peso que la capa densa
a: 2
e: La convolución comparte los 27 pesos de cada filtro en todas las posiciones y usa 16 filtros. La capa densa conecta cada una de las 3.072 entradas con cada una de las 16 salidas, así que necesita 49.168 pesos. La convolución no descarta píxeles: los recorre todos.
:::

:::quiz
p: Tienes dos convoluciones 3×3 con paso 1 encadenadas, sin agrupación. ¿Qué tamaño tiene el campo receptivo de una neurona de la segunda capa?
o: 3×3, porque cada filtro es de 3×3
o: 5×5, porque la segunda capa combina tres posiciones y cada una ya veía tres
o: 9×9, porque los filtros se multiplican
a: 2
e: r = 1 + (3−1) + (3−1) = 5. Cada neurona de la segunda capa mira tres posiciones de la primera, y cada una de esas posiciones mira tres píxeles, con solapamiento: el total es 5, no 9. El campo receptivo crece linealmente con la profundidad mientras el paso sea 1, y mucho más deprisa si hay pasos mayores.
:::

:::nota
Dos variantes que conviene reconocer: la **convolución 1×1** no mezcla vecinos, solo combina
canales, y sirve para reducir o aumentar el número de canales barato. La **convolución
separable en profundidad** aplica un filtro por canal y luego combina con 1×1, y reduce el
coste en un factor cercano a `F²` a cambio de algo menos de capacidad.
:::
