---
id: funciones-de-activacion
titulo: Funciones de activación
fase: 7
nivel: intermedio
rutas: [ds]
prerequisitos: [perceptron-y-mlp, regla-de-la-cadena, derivadas-y-reglas]
tags: [redes-neuronales, no-linealidad, gradientes, saturacion]
resumen: Sigmoide, tanh, ReLU y GELU: por qué sin no linealidad una red de veinte capas equivale a una regresión lineal
fuentes: ["Glorot y Bengio (2010), 'Understanding the difficulty of training deep feedforward neural networks'", "Hendrycks y Gimpel (2016), 'Gaussian Error Linear Units (GELUs)'"]
---

## En una frase

La función de activación es la no linealidad que se aplica después de cada combinación lineal
de una neurona, y es lo único que impide que una red de veinte capas sea matemáticamente
idéntica a una regresión lineal.

## La idea

Una capa calcula `W·h + b`, que es una transformación lineal. Si la red encadena tres capas
lineales, el resultado es `W₃·(W₂·(W₁·x + b₁) + b₂) + b₃`, y eso se puede reescribir como
`W'·x + b'` con una sola matriz `W' = W₃·W₂·W₁`. Toda la profundidad se colapsa en una capa. La
no linealidad es lo que rompe esa igualdad: sin ella, no hay red.

La elección de activación cambia tres cosas a la vez, y por eso importa tanto:

1. **Cuánta señal deja pasar en cada zona.** La sigmoide aplasta todo a `(0, 1)`: en los
   extremos, un cambio grande en la entrada produce un cambio diminuto en la salida. Eso
   significa que el gradiente que llega a las capas anteriores se hace casi cero, y el
   entrenamiento se atasca. Se llama saturación, y es la razón por la que la sigmoide se
   abandonó en las capas internas.
2. **Si el gradiente muere o no.** `tanh` está centrada en cero (va de −1 a 1), lo que hace
   que las activaciones no estén todas sesgadas hacia arriba y el descenso de gradiente
   converja mejor que con la sigmoide. Pero también se satura. `ReLU`, en cambio, tiene
   derivada exactamente 1 en la zona positiva: no satura por arriba. Su problema es el otro
   lado: en la zona negativa su derivada es 0, y una neurona que cae ahí deja de recibir
   gradiente y puede no recuperarse nunca (neurona muerta).
3. **El coste de cálculo.** `ReLU` es una comparación con cero. La sigmoide y `tanh` necesitan
   una exponencial. En un modelo con miles de millones de operaciones, esa diferencia se nota.

`GELU` es el compromiso dominante en los transformers. En vez de cortar a cero de golpe,
multiplica la entrada por la probabilidad de que una normal estándar sea menor que ella: los
valores muy negativos se apagan suavemente y los cercanos a cero se atenúan sin cortarse. Esa
suavidad ayuda al gradiente cerca de cero y, en la práctica, entrena algo mejor en redes muy
profundas; a cambio, es más caro de calcular que `ReLU`.

En la capa de salida la activación no se elige por gusto, sino por el problema: `softmax`
cuando hay que repartir probabilidad entre clases excluyentes, sigmoide para varias etiquetas
independientes, y ninguna (identidad) para regresión.

## Definición formal

Las cuatro activaciones habituales en capas internas, con `z` la preactivación de la neurona:

:::formula
σ(z) = 1 / (1 + e^(−z))      tanh(z) = (e^z − e^(−z)) / (e^z + e^(−z))
:::

:::formula
ReLU(z) = max(0, z)          GELU(z) ≈ 0,5·z·(1 + tanh(√(2/π)·(z + 0,044715·z³)))
:::

- `z` — la preactivación, `w·x + b`; puede ser cualquier número real.
- `σ` — la sigmoide; su salida está en `(0, 1)` y su derivada es `σ(z)·(1 − σ(z))`.
- `tanh` — la tangente hiperbólica; su salida está en `(−1, 1)` y su derivada es
  `1 − tanh(z)²`.
- `ReLU` — unidad lineal rectificada; vale `z` si `z > 0` y `0` si `z ≤ 0`. Su derivada es 1 o
  0, y en `z = 0` no está definida (en la práctica se toma 0).
- `GELU` — la aproximación con `tanh` de la definición exacta `z·Φ(z)`, donde `Φ` es la función
  de distribución de la normal estándar.
- `√(2/π)` — constante, aproximadamente 0,7979. No hay que memorizarla: importa entender que
  la curva es suave y que es no monótona en un entorno pequeño de cero.

En la capa de salida, con `K` clases y `z₁, …, z_K` las preactivaciones finales:

:::formula
softmax(z)_k = e^(z_k) / Σ_{j=1..K} e^(z_j)
:::

- `z_k` — la preactivación de la neurona de salida de la clase `k`.
- El denominador normaliza para que las `K` salidas sumen 1: son probabilidades excluyentes.
- Para varias etiquetas a la vez (no excluyentes) se aplica una sigmoide por salida, no un
  `softmax`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `z` | preactivación de la neurona: `w·x + b`, antes de la activación | las de la combinación lineal | Al alejarse de cero en cualquier dirección, la sigmoide y `tanh` se saturan y su derivada cae hacia cero: el gradiente que vuelve por esa neurona se apaga |
| `σ(z)` | sigmoide; su salida está en `(0, 1)` | adimensional | Nunca pasa de 1 ni baja de 0: aplasta cualquier entrada. Al subir `z`, la salida se acerca a 1 y su derivada a 0, así que la neurona deja de aprender |
| `tanh(z)` | tangente hiperbólica; su salida está en `(−1, 1)` | adimensional | Igual que la sigmoide pero centrada en cero: la salida tiende a 1 y la derivada a 0. Estar centrada es lo que la hizo preferible en capas internas |
| `ReLU(z)` | `max(0, z)` | las de `z` | En la zona positiva la salida crece sin límite y la derivada se queda en 1: no satura por arriba. En la negativa la salida y la derivada son 0, y ahí la neurona muere |
| `GELU(z)` | `z·Φ(z)`, aproximada con `tanh` | las de `z` | En la zona positiva grande se comporta como `ReLU`; cerca de cero es suave y en la negativa deja pasar algo de gradiente, así que no apaga la neurona del todo |
| `Φ` | función de distribución de la normal estándar | adimensional | Es la probabilidad de que una normal estándar sea menor que `z`: al subir `z` pasa de 0 a 1 y con ella el factor que multiplica a la entrada |
| `softmax(z)_k` | probabilidad de la clase `k` | adimensional, entre 0 y 1 | Al crecer la preactivación de una clase respecto de las demás, su probabilidad se acerca a 1 y las otras a 0. Lo que decide es la **diferencia** entre logits, no su tamaño |
| `K` | número de clases de la salida | clases | Las mismas diferencias se reparten entre más salidas: con un logit claramente ganador, cada probabilidad se acerca más a `1/K` y el `softmax` se vuelve menos decidido |
:::

## Ejemplo

Valores de las cuatro activaciones en cinco entradas:

```
z          -6,000   -2,000    0,000    2,000    6,000
sigmoide    0,0025   0,1192   0,5000   0,8808   0,9975
tanh       -1,0000  -0,9640   0,0000   0,9640   1,0000
ReLU        0,0000   0,0000   0,0000   2,0000   6,0000
GELU       -0,0000  -0,0454   0,0000   1,9546   6,0000
```

Fíjate en tres cosas concretas:

- **En `z = −6` la sigmoide vale 0,0025 y su derivada también (el máximo de `s·(1−s)` es
  0,25, en `z = 0`).** Un gradiente de 0,0025 es prácticamente cero: la señal se apaga. En
  `z = 0`, la derivada es 0,25. La diferencia entre esos dos puntos es un factor de 100 en la
  velocidad de aprendizaje de esa neurona. Con `tanh` el efecto es aún más brusco: su derivada
  en `z = −6` es 0,0000 redondeado a cuatro decimales.
- **`ReLU` y `GELU` coinciden en la zona positiva** (2 y 6 dan 2 y 6) y solo se diferencian
  cerca de cero: en `z = −2`, `ReLU` da 0 exacto y `GELU` da −0,0454, una pequeña fuga que
  mantiene vivo un poco de gradiente en la zona negativa.
- **`tanh` está centrada**: en `z = −2` da −0,964, mientras que la sigmoide en el mismo punto
  da 0,119. Esa diferencia de centrado es lo que hizo que `tanh` sustituyera a la sigmoide
  durante años.

:::figura
fichero: activaciones-curvas-y-derivadas
pie: El panel izquierdo son las cuatro curvas y el derecho sus derivadas, que es el panel que importa: la derivada es el factor que multiplica al gradiente cuando vuelve hacia atrás. Se ven tres cosas a la vez. Primera, la sigmoide y `tanh` se pegan a sus techos en los extremos, y ahí su derivada vale prácticamente cero: una neurona que trabaja en esa zona deja de recibir señal, y encadenar diez capas así desvanece el gradiente. Segunda, el máximo de la derivada de la sigmoide es 0,25 en `z = 0`, así que por cada neurona de este tipo se pierde al menos el 75 % del gradiente. Tercera, `ReLU` vale exactamente 1 en toda la zona positiva (no satura) pero exactamente 0 en la negativa: una neurona que cae ahí para todos los ejemplos se queda muerta, sin gradiente que la rescate. `GELU` es la versión suave de ese compromiso, y por eso se dobla por debajo de cero en lugar de cortar.
fuente: figuras/funciones-de-activacion-1.py
:::

## Código

```python verificable
import numpy as np

def sigmoide(x):
    return 1.0 / (1.0 + np.exp(-x))

def relu(x):
    # np.maximum compara elemento a elemento; el max() de Python no sabe hacerlo con un array
    return np.maximum(0.0, x)

# La aproximacion tanh de GELU, la que usan la mayoria de las implementaciones
def gelu(x):
    return 0.5 * x * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (x + 0.044715 * x**3)))

x = np.array([-6.0, -2.0, 0.0, 2.0, 6.0])
print("entradas ", x)                          # -> [-6. -2.  0.  2.  6.]
print("sigmoide ", np.round(sigmoide(x), 4))   # -> [0.0025 0.1192 0.5    0.8808 0.9975]
print("tanh     ", np.round(np.tanh(x), 4))    # -> [-1.    -0.964  0.     0.964  1.   ]
print("relu     ", np.round(relu(x), 4))       # -> [0. 0. 0. 2. 6.]
print("gelu     ", np.round(gelu(x), 4))       # -> [-0.     -0.0454  0.      1.9546  6.    ]
```

:::claves
- `np.maximum(0.0, x)` es la versión **vectorizada** de `max`: compara elemento a elemento y
  devuelve un array nuevo. El `max(0.0, x)` de Python no sirve aquí, porque no sabe comparar un
  número con un array.
- En numpy, `*` es producto **elemento a elemento** y `@` es el producto matricial. En `gelu`,
  `0.5 * x * (...)` multiplica posición a posición, y `x**3` eleva cada elemento al cubo.
  Confundir `*` con `@` es el error más caro y casi nunca da error de formas, solo resultados
  absurdos.
- Las funciones no modifican la entrada: `np.exp(-x)` devuelve otro array y `x` sigue igual
  después de la llamada. Lo mismo con `np.round`, que devuelve una copia redondeada y deja `s`
  con todos sus decimales.
- `(z > 0).astype(float)` es la derivada de `ReLU`: la comparación produce un array de `bool` y
  `astype(float)` lo convierte en 0,0 y 1,0. Sin el `astype`, numpy deja sumar booleanos pero no
  multiplicarlos por un gradiente con decimales.
- `z - z.max(axis=-1, keepdims=True)` no cambia el resultado del `softmax` (numerador y
  denominador quedan multiplicados por lo mismo) y evita que `np.exp` desborde con logits
  grandes. `keepdims=True` conserva la dimensión para que la resta se emita contra la matriz
  original en vez de contra un vector plano.
- `np.sqrt(2.0 / np.pi)` es la constante 0,7979 de la aproximación de `GELU`. La definición
  exacta es `z·Φ(z)`, con `Φ` la normal estándar acumulada: esta versión con `tanh` se desvía
  menos de una milésima y es bastante más barata de calcular.
:::

```python verificable
import numpy as np

# La derivada decide si la senal sobrevive: es el factor que multiplica al gradiente
z = np.array([-6.0, -2.0, 0.0, 2.0, 6.0])
s = 1.0 / (1.0 + np.exp(-z))
print("derivada sigmoide:", np.round(s * (1 - s), 4))
# -> [0.0025 0.105  0.25   0.105  0.0025]

print("derivada tanh    :", np.round(1 - np.tanh(z) ** 2, 4))
# -> [0.     0.0707 1.     0.0707 0.    ]

# ReLU no satura por arriba: pendiente 1 en toda la zona positiva
# (z > 0) da booleanos y astype(float) los convierte en 0.0 y 1.0
print("derivada relu    :", (z > 0).astype(float))
# -> [0. 0. 0. 1. 1.]

# El producto de las derivadas mide cuanto sobrevive el gradiente al atravesar la pila
# De 0,0025 a 0,105 hay un factor 42: la sigmoide cerca de 0 deja pasar mucho mas
print("minimo de la derivada sigmoide:", round(float((s * (1 - s)).min()), 4))   # -> 0.0025
print("maximo de la derivada sigmoide:", round(float((s * (1 - s)).max()), 4))   # -> 0.25
```

```python ilustrativo
# Softmax: reparte probabilidad entre clases excluyentes, con su version estable
import numpy as np

def softmax(z):
    z = z - z.max(axis=-1, keepdims=True)   # restar el maximo evita el desbordamiento de exp
    e = np.exp(z)
    # axis=-1 normaliza por la ultima dimension (las clases) y no por las filas del lote
    return e / e.sum(axis=-1, keepdims=True)

print(softmax(np.array([2.0, 1.0, 0.1])))   # -> [0.659 0.242 0.099]

# Ojo: softmax y sigmoide no son intercambiables
# softmax   -> las clases compiten, las salidas suman 1
# sigmoide  -> cada etiqueta es independiente, las salidas no suman 1
```

## Errores típicos

- **Poner una activación lineal en una capa interna.** Si `φ` es la identidad, la red entera
  colapsa a un modelo lineal con independencia del número de capas. Es un error silencioso: el
  modelo entrena y da resultados, solo que nunca podrá aprender una frontera curva.
- **Usar sigmoide en capas internas profundas.** Con 10 capas, el gradiente que vuelve se
  multiplica por derivadas menores que 0,25 en cada paso, y se desvanece. Es la razón histórica
  de que las redes profundas no se pudieran entrenar hasta la llegada de `ReLU` y de las
  inicializaciones adecuadas.
- **Poner `softmax` y usar una pérdida que ya lo incluye.** En PyTorch, `CrossEntropyLoss`
  aplica `log_softmax` internamente. Si además pones un `softmax` en la última capa, estás
  calculando el logaritmo de una probabilidad ya normalizada: la pérdida se comporta mal y el
  entrenamiento se degrada sin avisar.
- **Confundir `ReLU` con «no hace nada».** `ReLU` sí es no lineal (su gráfica tiene un codo), y
  ese codo es lo que da capacidad a la red. Lo que no hace es acotar la salida: con entradas
  grandes, las activaciones crecen sin límite y hay que controlar la escala con la
  inicialización o con normalización.
- **Ignorar las neuronas muertas.** Si una neurona cae en la zona negativa y su gradiente es 0
  para todos los ejemplos, se queda muerta para siempre. Se detecta contando cuántas
  activaciones son exactamente cero en un lote; si es una fracción grande, baja la tasa de
  aprendizaje o prueba una variante con fuga (`LeakyReLU`, `GELU`).
- **Elegir la activación sin mirar la capa de salida.** En regresión hay que dejar la salida
  sin activación (o con la que imponga el rango: `sigmoid` si el objetivo está en `[0,1]`,
  `softplus` si es positivo). Aplicar `softmax` a una regresión destruye la escala del
  objetivo.

:::practica
enunciado: Una red de cuatro capas usa sigmoide y en un lote todas las preactivaciones valen z = −2, donde la derivada de la sigmoide es 0,105. ¿Qué factor multiplica al gradiente al atravesar las cuatro capas? Compara con el caso z = 0, donde la derivada es 0,25, y di cuántas veces llega más pequeño.
pista: El gradiente que vuelve se multiplica por la derivada de la activación en cada capa: cuatro capas son cuatro factores encadenados.
solucion: Con z = −2 el factor por capa es 0,105, así que en cuatro capas el gradiente se multiplica por 0,105⁴ = 0,000122. Con z = 0 es 0,25⁴ = 0,003906. El cociente es 0,003906 / 0,000122 = 32. Conclusión: por trabajar en la zona saturada, a la primera capa le llega un gradiente unas 32 veces más pequeño.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué pasa si eliminas la función de activación de todas las capas de una red de 10 capas?
o: La red se vuelve más rápida pero aprende lo mismo
o: La red entera equivale a una única transformación lineal, sin importar la profundidad
o: La red deja de poder calcular la salida y da error
a: 2
e: La composición de funciones lineales es otra función lineal, así que las 10 capas se pueden colapsar en una sola matriz. La red funciona, entrena y da resultados, pero su capacidad es la de una regresión lineal: no puede representar fronteras curvas.
:::

:::quiz
p: En z = −6, la sigmoide vale 0,0025 y su derivada también. ¿Qué implica eso para el entrenamiento?
o: Que esa neurona aprende 400 veces más rápido que en z = 0
o: Que el gradiente que atraviesa esa neurona es casi cero y la señal se apaga al propagarse hacia atrás
o: Que la salida de esa neurona es negativa
a: 2
e: El máximo de la derivada de la sigmoide es 0,25, en z = 0. En los extremos la curva es plana y el factor que multiplica al gradiente se hace diminuto. Encadenar varias capas así hace que el gradiente se desvanezca. La salida en z = −6 es positiva (0,0025), no negativa.
:::

:::trampa
`ReLU` no satura por arriba pero sí puede matar neuronas por abajo: si la preactivación es
negativa para todos los ejemplos de todos los lotes, su gradiente es cero y esa neurona nunca
se recupera. Antes de cambiar de arquitectura, mira qué fracción de activaciones son
exactamente cero en un lote: si es más de la mitad, el problema es la tasa de aprendizaje o la
inicialización, no el tamaño de la red.
:::
