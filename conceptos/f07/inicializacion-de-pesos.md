---
id: inicializacion-de-pesos
titulo: Inicialización de pesos
fase: 7
nivel: avanzado
rutas: [ds]
prerequisitos: [varianza-y-desviacion, funciones-de-activacion, retropropagacion]
tags: [inicializacion, entrenamiento, varianza, estabilidad]
resumen: Los pesos se sortean al azar antes de entrenar y la escala de ese sorteo decide si la señal sobrevive a diez capas o se apaga por el camino.
fuentes: ["Glorot y Bengio (2010), 'Understanding the Difficulty of Training Deep Feedforward Neural Networks'", "He et al. (2015), 'Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification'", "LeCun et al. (1998), 'Efficient BackProp'"]
---

## En una frase

Antes de entrenar, los pesos se sortean al azar; la **varianza** de ese sorteo decide si las
activaciones y los gradientes llegan vivos a las capas profundas o se desvanecen por el camino,
y por eso existe una fórmula distinta para cada activación.

## La idea

Supón una capa con tres neuronas y una inicialización en la que todos los pesos valen cero. Las
tres neuronas calculan exactamente lo mismo, reciben exactamente el mismo gradiente y se
actualizan igual. Da igual que la capa tenga tres neuronas o tres mil: se comporta como una
sola, porque nunca se rompe la simetría. Ese es el primer requisito de una buena
inicialización: tiene que ser **distinta para cada peso**. Una constante cualquiera (0, 0,01 o
lo que sea) tiene el mismo defecto.

El segundo requisito es la **escala**, y aquí está lo interesante. Piensa en el juego del
teléfono escacharrado: si cada persona repite el mensaje un 10 % más flojo, al final de la fila
no queda nada. En una red pasa lo mismo con las varianzas. Si una capa recibe `n_in` entradas,
la varianza de su salida antes de la activación es `n_in · Var(w)` veces la varianza de la
entrada: cada peso contribuye un poco y las contribuciones se suman. Si ese producto es menor
que 1, la señal se encoge en cada capa de forma geométrica: con 256 entradas y pesos de
desviación 0,01, el factor por capa es `256 · 0,01² = 0,0256` y en cinco capas la señal se ha
dividido por 10⁸. Si el producto es mayor que 1, la señal crece hasta desbordar. La
inicialización consiste en elegir la varianza de los pesos para que ese producto valga
aproximadamente 1.

Y hay un detalle que cambia el número: **ReLU apaga la mitad de las activaciones**. Al poner a
cero todo lo negativo, la varianza de la salida se reduce a la mitad, así que para compensar hay
que doblar la varianza de los pesos. De ahí que existan dos recetas: la de Xavier/Glorot,
calibrada para `tanh` y `sigmoide`, y la de He, calibrada para ReLU. Usar la de Xavier con ReLU
no rompe el entrenamiento, pero pierde la mitad de la señal en cada capa, y en una red
profunda eso se nota.

:::nota
En las redes modernas con conexiones residuales y [[normalizacion-por-lotes|normalización]], la
inicialización importa menos: la suma residual deja pasar la señal y la normalización reescala.
Aun así sigue importando lo suficiente como para que los [[transformers|transformers]] necesiten
un calentamiento de la tasa de aprendizaje: con una inicialización inadecuada, las primeras
actualizaciones son enormes.
:::

## Definición formal

Sea una capa con `n_in` entradas y `n_out` salidas, con pesos `w` independientes, de media cero
y varianza `Var(w)`, y entradas de media cero e independientes de los pesos. Entonces la
varianza de la preactivación `z = Σⱼ wⱼ · hⱼ` es:

:::formula
Var(z) = n_in · Var(w) · Var(h)
:::

- `n_in` — fan-in: número de entradas que recibe cada neurona de la capa.
- `Var(w)` — varianza de cada peso; lo que queremos elegir.
- `Var(h)` — varianza de las activaciones de la capa anterior.
- La igualdad usa que las covarianzas se anulan: los pesos son independientes entre sí y de las
  entradas.

Si la activación es `h = ReLU(z)`, con `z` simétrico y de media cero, `Var(h) = Var(z) / 2`. Para
que la varianza se mantenga constante capa a capa hay que imponer
`n_in · Var(w) · c = 1`, con `c = 1` para lineal o `tanh` y `c = 1/2` para ReLU:

:::formula
LeCun (lineal o tanh):   Var(w) = 1 / n_in
:::

:::formula
Xavier/Glorot:   Var(w) = 2 / (n_in + n_out)
:::

:::formula
He (ReLU):   Var(w) = 2 / n_in
:::

- `n_out` — fan-out: número de salidas que salen de cada neurona de la capa.
- Xavier usa la media armónica de `n_in` y `n_out` porque quiere conservar la varianza en los
  dos sentidos: en la ida el factor es `n_in`, y en la vuelta de los gradientes el factor que
  aparece es `n_out`. Repartir entre los dos da `2/(n_in + n_out)`.
- He solo mira el fan-in porque la no linealidad ya aporta el factor 2 que necesita.

Si prefieres muestrear de una uniforme en vez de una normal, usa `Var(U(−a, a)) = a²/3` para
despejar el límite:

:::formula
Xavier uniforme:  a = √( 6 / (n_in + n_out) )       He uniforme:  a = √( 6 / n_in )
:::

En PyTorch, `nn.init.kaiming_normal_(w, mode='fan_in', nonlinearity='relu')` implementa la
versión He normal con desviación típica `√(2 / n_in)`, y `nn.init.xavier_uniform_` la versión
uniforme de Glorot.

Los **sesgos** se inicializan a cero. No rompen ninguna simetría relevante (esa la rompen los
pesos) y un sesgo grande satura la activación desde el primer paso. La excepción conocida son
las puertas de olvido de una LSTM, donde poner el sesgo a 1 ayuda a que la memoria no se borre
al principio del entrenamiento.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n_in` | fan-in: entradas que recibe cada neurona de la capa | entradas | El factor de la varianza por capa es `n_in·Var(w)`: al subir el fan-in hace falta **menos** varianza por peso (`2/n_in`) para que el producto se quede en 1. Por eso un `σ` fijo no vale para capas de distinto tamaño |
| `n_out` | fan-out: salidas que salen de cada neurona | salidas | Solo entra en Xavier, que reparte entre ida y vuelta con `2/(n_in + n_out)`: al subir `n_out` baja la varianza que pide la fórmula |
| `Var(w)` | varianza de cada peso; es lo único que se elige al inicializar | las de `w²` | Es el mando del problema. Si `n_in·Var(w)·c` queda por debajo de 1, la señal se encoge geométricamente capa a capa; si queda por encima, crece y desborda |
| `Var(h)` | varianza de las activaciones de la capa anterior | las de `h²` | Entra multiplicando en `Var(z) = n_in·Var(w)·Var(h)`: si las activaciones llegan pequeñas, la preactivación siguiente también, y el efecto se acumula |
| `σ` | desviación típica de los pesos, `√Var(w)`; el número que se escribe en `normal(0, σ)` | las de `w` | Es la raíz del mando. Con ReLU, He pide `√(2/n_in)`; Xavier pide `√(2/(n_in+n_out))`, que con ReLU deja el factor en 0,5 y pierde la mitad de la señal en cada capa |
| `a` | límite de la uniforme `U(−a, a)`, la alternativa a la normal | las de `w` | Como `Var(U(−a, a)) = a²/3`, hay que tomar `a = √(3·Var(w))`: en Xavier uniforme queda `√(6/(n_in + n_out))`. Subir `a` es subir la varianza |
| `c` | factor que aporta la activación a la varianza: 1 en lineal o `tanh`, ½ en ReLU | adimensional | `ReLU` apaga la mitad de las activaciones, así que con `c = ½` hace falta el doble de varianza en los pesos para compensar. Esa es toda la diferencia entre Xavier y He |
| `fan_in` / `fan_out` / `fan_avg` | modos de `nn.init.kaiming_normal_` | — | Eligen qué dimensión entra en la fórmula. Confundirlos cambia la escala en un factor `n_out/n_in`, que en una capa de 1024 a 64 es 16: es la diferencia entre entrenar y no arrancar |
:::

## Ejemplo

Una red de 10 capas, 256 unidades por capa, activación ReLU, con una entrada de desviación
típica 1. Comparamos tres inicializaciones contando la desviación típica de las activaciones
tras las capas 1, 2, 5 y 10:

- **std 0,01:** `0,5 · 256 · 0,01² = 0,0128` es el factor de la **varianza** por capa, así que
  la desviación se multiplica por `√0,0128 = 0,113` y tras 10 capas queda `0,113¹⁰ ≈ 3,5·10⁻¹⁰`
  de la señal original. La simulación da `3,18·10⁻¹⁰`. La red está muerta: los gradientes que
  llegan a la primera capa son del orden de 10⁻¹⁰ veces los de la última.
- **Xavier:** el factor de varianza es `0,5 · 256 · (2/512) = 0,5`, o sea que la desviación cae
  un 29 % por capa. `0,707¹⁰ = 0,031`; la simulación acaba en `0,022`. La señal sobrevive diez
  capas, pero se ha dividido por 45.
- **He:** el factor es `0,5 · 256 · (2/256) = 1`, exactamente lo que hacía falta. Las
  desviaciones se quedan entre 0,64 y 0,85 en todas las capas: la señal no se apaga.

El error del primer caso no es que la red aprenda despacio, es que **no aprende**: el gradiente
que recibe la primera capa es proporcional al producto de los factores de todas las capas que
tiene por encima.

:::figura
fichero: inicializacion-senal-por-capa
pie: El panel izquierdo mide lo que de verdad pasa en una red ReLU de diez capas y 256 unidades: la desviación típica de las activaciones capa a capa, en escala logarítmica. Las tres curvas usan los mismos pesos aleatorios y solo cambia la escala del sorteo. Con `σ = 0,01` la recta cae en línea recta, que en esta escala significa que se multiplica por el mismo factor en cada capa (0,113) hasta quedar en 10⁻¹⁰: la red no es que aprenda despacio, es que no aprende. Xavier se queda en 0,5 de la varianza por capa y pierde un 29 % de la desviación en cada paso, así que tras diez capas queda un 2 % de la señal: por eso Xavier no es la receta de ReLU. He es la única que se mantiene cerca de 1 en todas las capas. El panel derecho explica cómo se elige esa escala: dibuja el factor que multiplica la varianza en cada capa frente al fan-in, y la línea de puntos marca el 1 que hay que conseguir. He vale exactamente 1 para cualquier tamaño de capa, Xavier se queda en 0,5 porque no cuenta con que ReLU apaga la mitad, y un valor fijo no puede acertar en todos los tamaños: con `σ = 0,01` acierta en una capa concreta y falla en el resto. Esa es la razón de que la fórmula dependa del fan-in y de la activación, en vez de ser un número.
fuente: figuras/inicializacion-de-pesos-1.py
:::

## Código

```python verificable
import numpy as np

# Propagacion de la varianza en una red ReLU de 10 capas y 256 unidades. Cada capa
# multiplica la varianza por 0.5 * 256 * Var(w): el 0.5 es el ReLU, que apaga la mitad.
rng = np.random.default_rng(0)
ancho = 256
entrada = rng.normal(size=ancho)          # activaciones de partida, desviacion 1

inicializaciones = [("std 0.01", 0.01),
                    ("Xavier", np.sqrt(2 / (ancho + ancho))),
                    ("He", np.sqrt(2 / ancho))]

print("inicializacion   capa 1   capa 2   capa 5  capa 10")
for nombre, escala in inicializaciones:
    x = entrada.copy()
    fila = []
    for capa in range(10):
        # normal(media, desviacion, forma): la escala es la DESVIACION, no la varianza
        w = rng.normal(0, escala, size=(ancho, ancho))
        x = np.maximum(0.0, w @ x)        # capa lineal + ReLU
        if capa in (0, 1, 4, 9):
            fila.append(f"{x.std():.2e}")
    print(f"{nombre:<14} " + "  ".join(fila))
# -> inicializacion   capa 1   capa 2   capa 5  capa 10
# -> std 0.01       9.66e-02  1.02e-02  1.66e-05  3.18e-10
# -> Xavier         5.64e-01  3.86e-01  1.42e-01  2.20e-02
# -> He             7.78e-01  8.47e-01  6.39e-01  7.22e-01
```

:::claves
- `rng` es un **generador**, no una función: el bucle pide números nuevos en cada capa y la
  secuencia avanza. Por eso las tres inicializaciones no usan los mismos pesos aleatorios (el
  generador ya ha consumido 256·256 números por cada capa anterior) y la comparación es entre
  tres redes distintas, no entre tres escalas de la misma red.
- `x = entrada.copy()` es obligatorio: sin el `copy()`, `x` y `entrada` serían el mismo array y
  cada inicialización arrastraría los valores de la anterior. `x = np.maximum(0.0, w @ x)` sí
  crea un array nuevo, así que solo hace falta copiar al principio.
- `rng.normal(0, escala, size=(ancho, ancho))` recibe la **desviación típica**, no la varianza.
  Las fórmulas del portal (`2/n_in`, `2/(n_in+n_out)`) están escritas como varianza, así que hay
  que pasarles la raíz: `np.sqrt(2 / ancho)`. Pasar el valor sin la raíz es un error de un factor
  `√2` que no rompe nada y cuesta rendimiento sin avisar.
- `x.std()` calcula la desviación con **`ddof = 0`** (divide entre `n`, no entre `n − 1`), que es
  la definición de numpy por defecto. Con 256 valores la diferencia es del 0,2 %, pero si
  comparas con `pandas.Series.std()` —que usa `ddof = 1`— los números no cuadran y parece un
  error de la simulación.
- `f"{nombre:<14}"` alinea el nombre a la izquierda en 14 caracteres y `f"{x.std():.2e}"` escribe
  en notación científica con dos decimales. Las columnas quedan rectas y la caída de la señal se
  lee de un vistazo; con notación normal, `0.0000000003` es ilegible al lado de `0.78`.
- En el segundo bloque, `np.sqrt(0.5 * n_in * 0.01 ** 2)` es el factor de la **desviación** por
  capa, no de la varianza: el 0,5 es lo que se lleva ReLU y el resultado se compara directamente
  con 1. Confundir factor de varianza con factor de desviación es lo que hace que la mitad de las
  cuentas a mano de este tema salgan mal.
- `nn.init.kaiming_normal_(capa.weight, mode="fan_in", nonlinearity="relu")` **modifica el tensor
  en el sitio** (el guion bajo final lo anuncia) y no devuelve nada. Es al revés que
  `nn.init.zeros_(capa.bias)`, que también modifica, pero cuyo nombre hace pensar en una
  creación.
- `nn.Linear(256, 256)` ya viene inicializada con `kaiming_uniform` al construirla. Reinicializar
  a mano solo tiene sentido cuando quieres una receta concreta; y si aplicas una inicialización
  sobre un modelo **preentrenado**, borras todo el entrenamiento anterior.
:::

```python verificable
import numpy as np

# El factor por capa depende del fan-in: el mismo std no vale para capas de distinto tamano.
for n_in in (64, 256, 1024):
    factor_std_0_01 = np.sqrt(0.5 * n_in * 0.01 ** 2)       # ReLU incluido
    # sqrt porque lo que se compara con 1 es el factor de la DESVIACION, no el de la varianza
    factor_he = np.sqrt(0.5 * n_in * (2 / n_in))
    # :>4 alinea n_in a la derecha en cuatro caracteres, para que las columnas no bailen
    print(f"n_in {n_in:>4}  std 0.01 -> {factor_std_0_01:.4f} por capa   He -> {factor_he:.4f}")
# -> n_in   64  std 0.01 -> 0.0566 por capa   He -> 1.0000
# -> n_in  256  std 0.01 -> 0.1131 por capa   He -> 1.0000
# -> n_in 1024  std 0.01 -> 0.2263 por capa   He -> 1.0000

# Xavier con ReLU: pierde la mitad de la varianza en cada capa
print(f"Xavier con ReLU, 10 capas: {np.sqrt(0.5) ** 10:.4f} de la senal inicial")
# -> Xavier con ReLU, 10 capas: 0.0313 de la senal inicial
```

```python ilustrativo
import torch
import torch.nn as nn

capa = nn.Linear(256, 256)

# PyTorch ya inicializa con kaiming_uniform (a=raiz de 5) al construir la capa.
print(capa.weight.std())                 # ~0.036

# He normal para ReLU, que es lo que pide la formula 2/n_in
# El guion bajo final avisa de que la funcion MODIFICA el tensor y no devuelve nada
nn.init.kaiming_normal_(capa.weight, mode="fan_in", nonlinearity="relu")
nn.init.zeros_(capa.bias)

otra = nn.Linear(256, 256)
nn.init.xavier_uniform_(otra.weight)     # para tanh, no para ReLU

# Cargar pesos preentrenados y sustituir la cabeza: solo se inicializa la cabeza
modelo = torchvision.models.resnet18(weights="DEFAULT")
modelo.fc = nn.Linear(modelo.fc.in_features, 10)      # capa nueva, inicializada
nn.init.kaiming_normal_(modelo.fc.weight, nonlinearity="relu")
```

## Errores típicos

- **Inicializar todo a cero (o a cualquier constante).** Todas las neuronas de una capa
  calculan lo mismo, reciben el mismo gradiente y se quedan idénticas para siempre: la capa
  pierde toda su capacidad. Lo mismo pasa con los sesgos, aunque ahí es inofensivo porque los
  que rompen la simetría son los pesos.
- **Usar `0,01` de desviación típica «porque es pequeño y seguro».** Es el error más común al
  escribir una red a mano. Con 256 entradas la señal se multiplica por 0,113 en cada capa y a
  la décima capa ya no queda nada. La escala tiene que depender del fan-in, no ser un número
  fijo.
- **Usar Xavier con ReLU.** Xavier está calibrado para funciones que valen aproximadamente
  `1 · z` cerca de cero. Con ReLU hace falta el factor 2 extra de He; sin él, la varianza se
  reduce a la mitad por capa y en 10 capas queda un 3 % de la señal.
- **Reinicializar los pesos de un modelo preentrenado.** Al cargar un `state_dict` y luego
  aplicar una inicialización sobre el modelo entero, borras el entrenamiento por el que habías
  pagado. Inicializa solo las capas nuevas; mira
  [[transfer-learning|aprendizaje por transferencia]] y [[fine-tuning-y-lora|ajuste fino]].
- **Confundir `fan_in` con `fan_out`.** En una capa de 1024 a 64, `2/1024` y `2/64` se
  diferencian en un factor 16. PyTorch permite `mode='fan_in'`, `'fan_out'` y `'fan_avg'`: elige
  el que corresponda a la fórmula y no el que salga por defecto.
- **Dar por hecho que el modelo lo aprenderá.** La inicialización no cambia el mínimo al que
  puedes llegar, pero sí si el entrenamiento arranca. Una red con la señal apagada tiene
  gradientes que no llegan a las primeras capas y se queda ahí para siempre.

:::practica
enunciado: Una capa con n_in = 400 entradas usa ReLU. ¿Qué desviación típica piden He y Xavier? Si inicializas a mano con desviación 0,05 en una red de ocho capas de ese tamaño, ¿qué factor multiplica a la desviación en cada capa y qué fracción de la señal inicial queda al final?
pista: El factor de varianza por capa es 0,5·n_in·Var(w); el 0,5 es lo que se lleva el recorte de ReLU.
solucion: He pide Var(w) = 2/400 = 0,005, desviación √0,005 = 0,0707; Xavier pide 2/(400+400) = 0,0025, desviación 0,05. Con 0,05 el factor de varianza es 0,5·400·0,0025 = 0,5, así que la desviación se multiplica por √0,5 = 0,7071 en cada capa. Tras ocho capas queda 0,7071⁸ = 0,0625: solo el 6,25 % de la señal, porque 0,05 es la receta de Xavier y no la de He.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué no se pueden inicializar todos los pesos de una capa a cero?
o: Porque la pérdida sería exactamente cero desde el principio
o: Porque todas las neuronas de la capa calculan lo mismo y reciben el mismo gradiente: la simetría nunca se rompe y la capa equivale a una sola neurona
o: Porque el optimizador no puede dividir por cero
a: 2
e: Con todos los pesos iguales, cada neurona de la capa produce la misma salida y el gradiente de sus pesos es idéntico; al actualizar, siguen siendo iguales y seguirán siéndolo en cada paso. La pérdida no es cero (el sesgo y la capa siguiente siguen dando valores), simplemente la capa no aporta nada que no aporte una única neurona.
:::

:::quiz
p: Una capa recibe 512 entradas y usa ReLU. ¿Qué varianza deberían tener sus pesos si sigues la receta de He?
o: 1/512 ≈ 0,00195
o: 2/512 ≈ 0,0039
o: 2/(512 + n_out)
a: 2
e: He usa 2/n_in para ReLU, porque la activación apaga la mitad de las contribuciones y hay que doblar la varianza para compensar. 1/n_in es la receta de LeCun para activaciones lineales o tanh, y 2/(n_in+n_out) es Xavier, que reparte entre ida y vuelta y no tiene en cuenta el recorte de ReLU.
:::

:::quiz
p: En la simulación, con pesos de desviación 0,01 la desviación de las activaciones es 3,18·10⁻¹⁰ tras 10 capas. ¿Qué consecuencia tiene sobre el entrenamiento?
o: El entrenamiento es más lento pero converge al mismo sitio
o: Los gradientes que llegan a las primeras capas son proporcionalmente diminutos y esas capas no se actualizan de forma apreciable
o: Los pesos se actualizan con pasos demasiado grandes y el modelo diverge
a: 2
e: En la retropropagación, la magnitud del gradiente se multiplica por los mismos factores que la señal en la ida. Si la señal se ha dividido por 10¹⁰, el gradiente que llega abajo es del mismo orden y las primeras capas apenas cambian. No es lentitud, es parálisis; y no hay divergencia porque lo que falta es gradiente, no lo que sobra.
:::

:::truco
Antes de entrenar, imprime la desviación típica de las activaciones de cada capa con un lote de
datos reales. Si cae un orden de magnitud entre la primera y la última capa, el problema es la
inicialización (o falta normalización), no la tasa de aprendizaje.
:::
