---
id: maldicion-de-la-dimensionalidad
titulo: Maldición de la dimensionalidad
fase: 6
nivel: avanzado
rutas: [ds, alg]
prerequisitos: [norma-y-distancias, knn]
tags: [dimensionalidad, distancias, vecinos, reduccion]
resumen: Al añadir dimensiones el espacio se vacía, las distancias se igualan y el vecino más cercano deja de serlo; qué hacer cuando tu modelo sufre esto.
fuentes: ["Bellman (1961), 'Adaptive Control Processes: A Guided Tour'", "Beyer et al. (1999), 'When Is Nearest Neighbor Meaningful?'", "Hastie, Tibshirani y Friedman (2009), 'The Elements of Statistical Learning', cap. 2"]
---

## En una frase

Cada dimensión que añades hace que los datos ocupen una porción cada vez más pequeña del espacio
disponible, con lo que las distancias entre puntos se parecen entre sí, los vecinos más cercanos
dejan de ser cercanos y cualquier método basado en distancias pierde el sentido.

## La idea

Imagina que tienes que encontrar a tu amigo en una aldea de 100 casas. Recorres dos calles y llamas a
la puerta correcta. Ahora búscalo en un país de 100 casas: puedes pasar meses. Mismo número de
casas, más territorio, y por tanto menos densidad. Eso es lo que pasa al añadir dimensiones: si
mantienes el número de puntos y añades variables, la densidad se desploma.

El caso más llamativo es el del vecindario. Para capturar el 10 % del volumen de un cubo de lado 1 en
una dimensión, un intervalo tiene que medir 0,1 (el 10 % del rango). En dos dimensiones, un cuadrado
tiene que medir 0,32 de lado. En diez dimensiones, el cubo tiene que medir 0,79: **casi todo el
rango en cada eje** para quedarte con una décima parte del volumen. En 100 dimensiones, 0,98. Es
decir, en alta dimensión «el 10 % de los datos más cercanos» es, en la práctica, «casi todos los
datos».

La segunda consecuencia es peor, porque afecta a la noción misma de parecido. Con coordenadas
independientes, al crecer la dimensión la distancia al punto más cercano y la distancia al más lejano
se van pareciendo: el cociente entre la mínima y la máxima tiende a 1. En el ejemplo de abajo pasa de
0,035 en dos dimensiones a 0,91 en 1000. Cuando todos los puntos están casi a la misma distancia de
todos, «el más cercano» es casi una elección al azar, y eso rompe [[knn]], el clustering por
densidad, la detección de anomalías por distancia y los índices de vecinos.

Tercera consecuencia, de ingeniería: los índices que aceleran la búsqueda de vecinos (k-d trees,
ball trees) dejan de funcionar. Están pensados para descartar ramas enteras del árbol comparando
cajas, y con 50 dimensiones casi todas las cajas se solapan con la esfera de consulta, así que la
búsqueda degenera en recorrer todos los puntos ([[complejidad-asintotica]]). De ahí que en alta
dimensión se usen índices aproximados (HNSW, IVF) que renuncian a la exactitud
([[bases-de-datos-vectoriales]]).

¿Significa esto que añadir variables siempre sea malo? No. Significa que el problema no es el número
de dimensiones, sino la relación entre tres cosas: cuántos datos tienes, cuánta información lleva
cada variable y cuánto ruido añade. Dos salvavidas muy usados: reducir la dimensión antes de medir
distancias ([[pca]], [[seleccion-de-features]], [[autoencoders-y-vae]]) o cambiar la métrica por una
que se comporte mejor, como el coseno, que ignora la magnitud y se centra en la dirección
([[producto-punto-y-similitud]], [[embeddings]]).

## Definición formal

En `R^d`, la bola de radio `r` centrada en el origen tiene volumen

:::formula
V_d(r) = π^{d/2} · r^d / Γ(d/2 + 1)
:::

- `d` — el número de dimensiones.
- `r` — el radio.
- `Γ(·)` — la función gamma, que extiende el factorial: `Γ(m + 1) = m!` para `m` entero. Aparece
  porque el volumen de la bola se calcula con integrales que dependen de la paridad de `d`.

Dividiendo ese volumen por el del cubo de lado 2 (que es `2^d`), la fracción del cubo ocupada por la
esfera inscrita cae a una velocidad brutal: 0,785 en dos dimensiones, 0,0025 en diez y `1,9 · 10⁻⁷⁰`
en cien. Prácticamente todo el volumen de un cubo de alta dimensión está en las esquinas, no en el
centro.

**Vecindario que cubre una fracción `p` del volumen.** Si el vecindario es un cubo de lado `s` y el
dominio es el cubo unidad, `s^d = p`, de donde:

:::formula
s = p^{1/d}
:::

Con `p = 0,1`: `s = 0,1` en una dimensión, `0,316` en dos, `0,794` en diez y `0,977` en cien. La
dimensión entra en el exponente, y por eso el efecto es tan rápido.

**Concentración de distancias.** Sean `X_1, …, X_n` puntos con coordenadas independientes e
idénticamente distribuidas, con media y varianza finitas. Con `D_min` y `D_max` las distancias al
vecino más cercano y al más lejano de un punto:

:::formula
( D_max − D_min ) / D_min  →  0   cuando d → ∞
:::

La diferencia absoluta entre distancias crece (las distancias crecen como `√d`), pero crece más
despacio que la distancia típica, así que el **contraste relativo** desaparece. Beyer y sus coautores
dan las condiciones precisas de este resultado; la intuición es que una distancia es una suma de `d`
términos y, por la ley de los grandes números, esa suma se concentra alrededor de su media.

**Vecinos en la práctica.** La distancia esperada al `k`-ésimo vecino más cercano escala como
`(k/n)^{1/d}`. Para que se mantenga constante al aumentar `d`, el número de puntos tiene que crecer
de forma exponencial: pasar de 10 a 100 dimensiones manteniendo la misma distancia media exige del
orden de `10^90` veces más datos. Ese es el sentido cuantitativo de «el espacio se vacía».

:::figura
fichero: maldicion-vecindario-y-distancias
pie: A la izquierda, el lado del cubo que hace falta para cubrir el 10 % del volumen: 0,316 con dos variables, 0,794 con diez y 0,977 con cien. El vecindario local acaba ocupando casi todo el rango de cada eje. A la derecha, el contraste entre la distancia al vecino más cercano y al más lejano, medido con 150 puntos uniformes: vale 0,05 con dos dimensiones, 0,35 con diez y sigue acercándose a 1 en alta dimensión (el cociente se mide con otro número de puntos que la tabla del ejemplo, y por eso los decimales no coinciden del todo). Conclusión: en alta dimensión «el más cercano» y «el más lejano» se parecen, así que cualquier método que dependa de elegir entre ellos decide sobre casi nada; toca reducir dimensión, seleccionar variables o cambiar de métrica.
fuente: figuras/maldicion-de-la-dimensionalidad-1.py
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `d` | El número de dimensiones (variables) | adimensional | El lado necesario sube como `p^(1/d)` y el contraste relativo se hunde. Es el parámetro que manda en todo el tema, y entra en el exponente |
| `p` | La fracción del volumen que quieres capturar | tanto por uno, entre 0 y 1 | Cuanto menor es `p`, más pequeño es el vecindario, pero la pérdida de contraste con `d` se mantiene: pedir el 1 % en vez del 10 % no arregla la alta dimensión |
| `s` | El lado del cubo que cubre esa fracción | fracción del rango, entre 0 y 1 | Es el resultado de `s = p^(1/d)`. Si sube, el vecindario es menos local; con `d = 100` vale 0,977, o sea casi todo el eje |
| `r` | El radio de la bola donde se buscan vecinos | las de las variables | El volumen de la bola crece como `r^d` y su porción del cubo se desploma: con 10 variables la esfera inscrita ya solo ocupa el 0,25 % del cubo |
| `D_min`, `D_max` | Distancia al vecino más cercano y al más lejano | las de las variables | Las dos crecen como `√d`, pero `D_min` crece menos: el cociente `D_min / D_max` tiende a 1, y esa es la pérdida de contraste |
| `n` | El número de puntos | adimensional | La distancia al k-ésimo vecino escala como `(k/n)^(1/d)`. Subir `n` reduce esa distancia, pero para mantenerla constante al doblar `d` hacen falta del orden de `10^d` veces más datos |
:::

## Ejemplo

Dos experimentos con números concretos.

**Cobertura.** ¿Qué lado tiene que tener un cubo para cubrir el 10 % del volumen?

```text
dimensiones   lado necesario
     1            0,100
     2            0,316
     3            0,464
    10            0,794
    50            0,955
   100            0,977
```

Con dos variables basta mirar un 32 % del rango de cada una; con 100 variables hay que mirar el 98 %
de cada rango para quedarse con una décima parte de los datos. El «vecindario local» ya no es local.

**Concentración de distancias.** 200 puntos uniformes en un cubo unidad, distancia euclídea:

```text
dimensiones   vecino más cercano   punto más lejano   cociente mínimo/máximo
     2              0,035               1,023                0,035
    10              0,633               1,841                0,344
   100              3,437               4,647                0,740
  1000             12,260              13,506                0,908
```

En dos dimensiones, el punto más lejano está 29 veces más lejos que el vecino más cercano: la noción
de «vecino» discrimina. En 1.000 dimensiones, el más lejano solo está un 10 % más lejos que el más
cercano, y cualquier algoritmo que dependa de elegir entre ellos está decidiendo sobre casi nada.

## Código

```python verificable
import numpy as np
from math import gamma, pi

# Lado del cubo necesario para cubrir el 10 % del volumen de un cubo unidad
for d in (1, 2, 3, 5, 10, 50, 100, 1000):
    print("d=%4d  lado para el 10 %% del volumen: %.4f" % (d, 0.1 ** (1 / d)))
# -> d=   1  lado para el 10 % del volumen: 0.1000
# -> d=  10  lado para el 10 % del volumen: 0.7943
# -> d=1000  lado para el 10 % del volumen: 0.9977

# Fraccion del cubo que ocupa la esfera inscrita: pi^(d/2) / (2^d * Gamma(d/2+1))
for d in (2, 3, 10, 100):
    print("d=%3d  esfera inscrita / cubo: %.3e" % (d, pi ** (d / 2) / (2 ** d * gamma(d / 2 + 1))))
# -> d=  2  esfera inscrita / cubo: 7.854e-01
# -> d= 10  esfera inscrita / cubo: 2.490e-03
# -> d=100  esfera inscrita / cubo: 1.868e-70
```

```python verificable
import numpy as np

# 200 puntos uniformes en un cubo de lado 1, para varias dimensiones
rng = np.random.default_rng(0)
for d in (2, 10, 100, 1000):
    P = rng.random((200, d))
    dist = np.sqrt(((P[:, None, :] - P[None, :, :]) ** 2).sum(axis=2))
    np.fill_diagonal(dist, np.nan)                  # fuera la distancia de cada punto a si mismo
    minima, maxima = np.nanmin(dist, axis=1), np.nanmax(dist, axis=1)
    print("d=%4d  cercano %.3f  lejano %.3f  cociente min/max %.4f"
          % (d, minima.mean(), maxima.mean(), (minima / maxima).mean()))
# -> d=   2  cercano 0.035  lejano 1.023  cociente min/max 0.0351
# -> d=  10  cercano 0.633  lejano 1.841  cociente min/max 0.3442
# -> d= 100  cercano 3.437  lejano 4.647  cociente min/max 0.7397
# -> d=1000  cercano 12.260  lejano 13.506  cociente min/max 0.9078
```

:::claves
- `0.1 ** (1 / d)` funciona con enteros, pero en Python 3 la división ya es real: no hace falta escribir `1.0`. En Python 2 esto valía 0 y el resultado era siempre 1.
- `P[:, None, :] - P[None, :, :]` crea una matriz de `n × n × d` diferencias. Con `n = 200` y `d = 1000` son 40 millones de números (320 MB): por eso el código de la página calcula una sola dimensión a la vez y no todas de golpe.
- `np.fill_diagonal(dist, np.nan)` es imprescindible: sin él, el vecino más cercano de cada punto es él mismo y `D_min` sale 0 en todas las dimensiones.
- `np.nanmin` y `np.nanmax` ignoran los `nan` de la diagonal; `np.min` devolvería `nan` y la tabla entera saldría vacía.
- La fracción esfera/cubo necesita `math.gamma`: con `d = 1000`, `gamma(501)` desborda y lanza `OverflowError`. En la página se para en `d = 100`, y el orden de magnitud (`10⁻⁷⁰`) es lo que importa.
- `np.sqrt(((P[:, None, :] - P[None, :, :]) ** 2).sum(axis=2))` gasta mucha memoria para nada: con `cuadrado[:, None] + cuadrado[None, :] - 2 * P @ P.T` sale lo mismo usando una matriz de `n × n`.
:::

## Errores típicos

- **Añadir variables «por si acaso».** Cada columna irrelevante añade ruido a todas las distancias y
  aleja a los vecinos que de verdad importan. Veinte variables de relleno pueden arruinar un k-NN que
  funcionaba con tres. Si no puedes justificar una variable, déjala fuera; y ojo con los sensores que
  miden lo mismo con ruido, porque son dimensiones de correlación alta que inflan la distancia sin
  aportar información.
- **Usar k-NN con distancia euclídea en cientos de dimensiones.** Con el contraste relativo cerca de
  cero, el vecino elegido es casi aleatorio y el modelo pierde. Reduce antes, selecciona variables o
  cambia a similitud de coseno.
- **Estandarizar sin pensar en alta dimensión.** Con la euclídea, la variable con más varianza domina
  la distancia. Normalizar es casi siempre obligatorio, pero también cambia qué significa «cerca»
  cuando una variable es ruido puro.
- **Confiar en k-d trees o ball trees con muchas variables.** Por encima de unas pocas decenas de
  dimensiones el índice degenera en un recorrido completo y encima pagas el coste de construirlo.
  Mide antes de darlo por bueno.
- **Interpretar distancias absolutas en una proyección.** t-SNE y UMAP conservan vecindades locales,
  no distancias globales: la distancia entre dos grupos en el gráfico no significa nada
  ([[tsne-y-umap]]).
- **Concluir que la reducción de dimensión siempre ayuda.** Si las variables extra son informativas y
  hay datos suficientes, tirar dimensiones tira señal. La decisión se toma midiendo el error de
  validación, no por principio ([[pca]], [[seleccion-de-features]]).

:::practica
enunciado: Con n puntos uniformes en el cubo unidad, la distancia al vecino más cercano escala como (1/n)^(1/d). Calcula el lado que cubre el 1 % del volumen con d = 2 y d = 20, y cuántas veces más datos hacen falta al pasar de 10 a 20 dimensiones.
pista: El lado sale de despejar s^d = p; el crecimiento de datos, de mantener (1/n)^(1/d) constante.
solucion: Con p = 0,01, s = p^(1/d): en d = 2 el lado es 0,01^(1/2) = 0,1, y en d = 20 es 0,01^(1/20) = 10^(−0,1) = 0,794, casi todo el rango de cada eje. Para que (1/n)^(1/d) siga valiendo 0,1 hace falta n = 0,1^(−d): de 10 a 20 dimensiones, n se multiplica por 0,1^(−10) = 10^10. Conclusión: duplicar las variables exige diez mil millones de veces más datos.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué en 100 dimensiones hace falta que un vecindario mida el 98 % del rango en cada eje para contener el 10 % del volumen?
o: Porque el volumen crece como la potencia d-ésima del lado, así que el lado necesario es 0,1 elevado a 1/d
o: Porque los datos se concentran en el centro del cubo al aumentar la dimensión
o: Porque la distancia euclídea crece con la raíz del número de dimensiones
a: 1
e: El volumen de un cubo de lado s en d dimensiones es s^d; para que valga 0,1 hay que tomar s = 0,1^(1/d), que con d = 100 es 0,977. Los datos uniformes no se concentran en el centro (justo lo contrario: casi todo el volumen está en las esquinas), y el crecimiento de la distancia con la raíz de d es otro fenómeno, el de la concentración de distancias.
:::

:::quiz
p: Tienes 500 clientes descritos con 300 variables y quieres agruparlos por similitud. Todas las distancias entre pares salen entre 24 y 26. ¿Qué está pasando y qué haces?
o: Nada, con distancias tan parecidas el clustering será muy estable
o: El contraste relativo ha desaparecido; conviene reducir dimensión o seleccionar variables antes de agrupar
o: Hay un error de cálculo, porque las distancias no pueden ser todas parecidas
a: 2
e: Es exactamente el síntoma de la concentración de distancias: si la distancia al vecino más cercano y al más lejano difieren en un 8 %, el criterio de cercanía es casi ruido. No hay error de cálculo ni estabilidad: reduce dimensión (PCA, selección de variables) o cambia la métrica, y vuelve a medir.
:::

:::quiz
p: Un k-d tree con 10 variables responde en milisegundos y con 200 variables tarda más que recorrer los 5 millones de puntos a mano. ¿Por qué?
o: Porque el árbol se construye mal cuando hay muchas variables
o: Porque con muchas dimensiones casi todas las cajas del árbol se solapan con la región de consulta y no se puede descartar ninguna rama
o: Porque la memoria del árbol crece de forma cuadrática con las variables
a: 2
e: El k-d tree acelera descartando ramas cuya caja está lejos del punto de consulta. El volumen de una caja crece muy rápido con la dimensión, así que en alta dimensión todas las cajas están «cerca» y hay que visitarlas: el índice degenera en un escaneo lineal, con el coste añadido de haber construido el árbol.
:::
