---
id: reproducibilidad-del-entrenamiento
titulo: Reproducibilidad del entrenamiento
fase: 7
nivel: intermedio
rutas: [ds, alg]
prerequisitos: [pytorch-fundamentos, inicializacion-de-pesos]
tags: [reproducibilidad, semillas, determinismo, entrenamiento, mlops]
resumen: Por qué dos ejecuciones con el mismo código no dan el mismo número, qué fuentes de azar hay que fijar y qué parte del determinismo no se puede recuperar.
fuentes: ["Pineau et al. (2021), 'Improving Reproducibility in Machine Learning Research'", "Bouthillier et al. (2019), 'Unreproducible Research is Reproducible'", "PyTorch (2024), 'Reproducibility' (documentación oficial)"]
---

## En una frase

Reproducir un entrenamiento no es que salga un número parecido: es poder volver a obtener el
mismo número, o saber exactamente por qué no puedes.

## La idea

Dos cocineros con la misma receta y la misma cocina sacan platos casi idénticos. Con la misma
receta y otra cocina, parecidos pero no iguales. Y si la receta dice «sal al gusto» y «fuego
medio», no hay forma de repetir nada. Entrenar una red tiene las tres cosas: receta
(hiperparámetros), cocina (hardware y versiones) y una lista larga de «al gusto» (semillas).

Merece la pena separar tres niveles, porque se piden en momentos distintos:

- **Bit a bit.** Dos ejecuciones producen exactamente los mismos pesos. Exige el mismo hardware,
  las mismas versiones, algoritmos deterministas y todas las semillas fijadas. Es lento, frágil,
  y solo hace falta para una cosa: depurar.
- **Estadística.** Las ejecuciones caen en la misma distribución. Es lo que necesitas para
  afirmar que una configuración es mejor que otra, y lo que se reporta en un informe.
- **De la conclusión.** El resultado cualitativo se sostiene aunque los números cambien. Es lo
  único que sobrevive cuando alguien reproduce tu trabajo en otra máquina.

El malentendido que arruina las tres es creer que `manual_seed(0)` lo fija todo. **La semilla no
es el estado: es el origen de una secuencia.** Lo que determina el resultado es cuántas veces y
en qué orden se consume esa secuencia. Si añades una capa de `dropout`, o cambias el
`DataLoader` de 0 a 4 workers, o introduces un aumento de datos, todas las extracciones
posteriores salen distintas aunque la semilla sea la misma. Dos ejecuciones con la misma semilla
y el mismo código pueden diferir en todo; lo que las iguala es la misma secuencia de consumo.

Las fuentes de azar que hay que tener localizadas:

1. **Inicialización de los pesos.** Es la que más mueve el resultado final.
2. **Barajado de los datos** y el orden de los lotes.
3. **Regularización estocástica**: `dropout`, ruido gaussiano, aumento de datos.
4. **Los workers del `DataLoader`.** Cada uno recibe un generador derivado del principal; con
   `num_workers=0` y con `num_workers=4` el orden de los lotes no es el mismo.
5. **Kernels no deterministas de GPU.** Cuando varios hilos suman en la misma posición, el orden
   de las sumas cambia entre ejecuciones y, como la suma en coma flotante no es asociativa, el
   resultado cambia en los últimos bits.
6. **`cudnn.benchmark`**, que elige el algoritmo más rápido midiendo tiempos en la primera
   ejecución: dos ejecuciones pueden escoger algoritmos distintos.
7. **Precisión mixta y TF32**, que redondean en sitios distintos según el camino que tome el
   kernel.
8. **Versiones de librerías, modelo de GPU y número de núcleos.** Cambiar de máquina cambia las
   reducciones y, con ellas, los últimos decimales.
9. **El orden de iteración de un `set`**, que depende del hash de sus elementos y, con cadenas de
   texto, de `PYTHONHASHSEED`. Un barajado hecho recorriendo un conjunto puede dar dos órdenes
   distintos en dos procesos. Un `dict`, en cambio, conserva el orden de inserción desde Python
   3.7: ahí el riesgo está en cómo se construyó, no en el hash.

El punto 8 explica por qué «misma semilla» no implica «mismos bits» entre dos máquinas: no hay
semilla que arregle que las sumas se hagan en otro orden. Se puede forzar el orden con
`torch.use_deterministic_algorithms(True)`, a cambio de que algunas operaciones —las sumas
dispersas en las que varios índices escriben en la misma posición— dejen de tener implementación
y lancen un error en vez de dar un resultado variable. Es un intercambio consciente: precisión
reproducible a cambio de velocidad y de algunas operaciones menos.

La regla práctica: fija todo lo que puedas, **registra el entorno junto con la semilla**, y no
persigas el bit a bit más allá de la depuración. Cuando dos ejecuciones del mismo código con la
misma semilla difieren, no es el azar: es un bug o un worker de más.

:::trampa
Fijar la semilla global al principio del script y dar por hecho que todo queda determinista. El
`DataLoader` con workers, el aumento de datos y los kernels de GPU tienen su propio generador o
ninguno. El síntoma es una pérdida que coincide durante dos épocas y luego se separa sin que
hayas tocado nada.
:::

:::figura
fichero: reproducibilidad-semillas-e-intervalos
pie: A la izquierda, treinta entrenamientos de la misma configuración en los que lo único que cambia es la semilla. El punto rojo es el resultado de la semilla 1, que es el número que aparecería en el informe si solo hubieras lanzado una ejecución, y la banda azul es donde cae el 95 % de los entrenamientos. La conclusión que se puede defender con un solo punto es prácticamente ninguna. A la derecha, la diferencia entre las dos preguntas: en azul, la amplitud del intervalo de confianza de la media, que se estrecha como la raíz del número de semillas; en rojo, la amplitud del intervalo de predicción de una ejecución nueva, que baja al principio y se queda pegada a dos desviaciones típicas. Más semillas afinan la media, pero no hacen que la próxima ejecución sea más predecible.
fuente: figuras/reproducibilidad-del-entrenamiento-1.py
:::

## Definición formal

Un entrenamiento es una función de tres entradas más el entorno:

:::formula
θ_T = F(θ₀, D, ξ)          ξ = (ξ_pesos, ξ_lotes, ξ_dropout, ξ_aumento)
:::

Decimos que el entrenamiento es determinista bit a bit cuando dos ejecuciones con el mismo
`θ₀`, el mismo `D`, la misma `ξ` y el mismo entorno producen exactamente el mismo `θ_T`. Y es
reproducible a nivel estadístico cuando la distribución de `M(θ_T)` es la misma, aunque los
pesos no coincidan.

**La semilla no determina `ξ`.** Fijar la semilla fija el origen de cada flujo, pero `ξ` depende
del número de extracciones: si entre el paso `t` y el paso `t+1` el programa consume una
extracción más, a partir de ahí todos los valores del flujo se desplazan una posición. La
consecuencia formal es que la reproducibilidad bit a bit es una propiedad **del programa**, no
de la semilla.

**Qué esperar de una ejecución nueva.** Con `k` semillas de la misma configuración, media `R̄` y
desviación típica `s`, el valor de una ejecución adicional cae, con la convención de dos errores
típicos, en:

:::formula
R_nueva ∈ R̄ ± 2 · s · √(1 + 1/k)
:::

El `1 + 1/k` es lo que distingue este intervalo del de la media: el término `1/k` viene de la
incertidumbre sobre `R̄` y desaparece cuando `k` crece, pero el `1` se queda. Por mucho que
entrenes, una ejecución nueva sigue teniendo la dispersión completa del problema.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `θ₀` | Pesos iniciales | las de cada parámetro | Es la fuente de azar que más mueve el resultado. Cambiar la semilla de inicialización puede mover la exactitud final más que cambiar la tasa de aprendizaje, y por eso una sola ejecución no es evidencia de nada |
| `D` | Conjunto de datos y su partición | — | Si cambia, cambia el problema: dos ejecuciones con particiones distintas no son comparables ni con la misma semilla. Su identidad se registra con un hash y con el identificador de la partición |
| `ξ` | Toda la aleatoriedad del entrenamiento | — | No se fija con una sola semilla, sino con la semilla **y** la secuencia de consumo. Añadir una extracción lo desplaza todo; es la razón de que el mismo `manual_seed(0)` dé resultados distintos tras tocar el modelo |
| `entorno` | Versiones de librerías, modelo de GPU, número de núcleos, precisión | — | Al cambiar, cambia el orden de las sumas en coma flotante. Es la parte que no se puede fijar desde el código y la que rompe la reproducibilidad entre máquinas: hay que registrarla, no esconderla |
| `R̄` | Media de la métrica `M` sobre `k` semillas | las de `M` | Es la estimación del valor esperado de la configuración. Su precisión mejora con `k`, pero no dice nada sobre cuánto puede desviarse una ejecución concreta |
| `s` | Desviación típica entre semillas | las de `M` | Sube con la capacidad del modelo y con menos datos. Es la cifra que hay que reportar junto a toda media, y la que decide cuántas semillas hacen falta |
| `k` | Número de semillas ejecutadas | recuento | Estrecha la estimación de `R̄` como `1/√k`, pero deja intacta la dispersión de una ejecución nueva: el intervalo de predicción tiende a `± 2s` por mucho que subas `k` |
| `R_nueva` | Métrica de una ejecución que todavía no has lanzado | las de `M` | Es lo que de verdad quieres predecir, y es más ancho que el intervalo de la media. Confundir los dos es la causa de prometer resultados que no se repiten |
:::

## Ejemplo

**1. La misma semilla no basta.** Un entrenamiento de juguete con tres parámetros, ejecutado dos
veces con la semilla 0: los pesos salen idénticos. Se inserta **una sola** extracción del
generador y todo lo que viene después se desplaza:

```
misma semilla, mismo codigo:   True
misma semilla, una tirada mas: False
distancia entre los dos pesos: 0.0725
```

Una llamada de más separa los pesos 0,0725 en un modelo de tres parámetros. En una red real esa
separación se amplifica época tras época: no es que los resultados «se parezcan menos», es que
dejan de estar relacionados.

**2. Lo que cabe esperar de la próxima ejecución.** Cuatro semillas de la misma configuración,
misma partición, mismo número de épocas:

```
media de las 4 ejecuciones  0.8413
dispersion entre semillas   0.0082
la proxima caera entre      0.8229 y 0.8597
amplitud del intervalo      0.0368
```

El intervalo mide 0,0368, casi cuatro puntos de exactitud. Cualquier mejora que pretendas
defender y que sea menor que eso es indistinguible del efecto de la semilla: la ejecución número
cinco puede caer en cualquier punto de esa banda sin que hayas cambiado nada.

## Código

```python verificable
import numpy as np


def entrena(semilla, tirada_extra=False):
    rng = np.random.default_rng(semilla)
    w = rng.normal(0, 0.1, 3)
    if tirada_extra:
        rng.random()                       # una sola tirada de mas...
    return w + rng.normal(0, 0.05, 3)      # ...desplaza todo lo que viene despues


a = entrena(0)
b = entrena(0)
c = entrena(0, tirada_extra=True)

print("misma semilla, mismo codigo:  ", bool(np.allclose(a, b)))      # -> True
print("misma semilla, una tirada mas:", bool(np.allclose(a, c)))      # -> False
print(f"distancia entre los dos pesos: {np.linalg.norm(a - c):.4f}")  # -> 0.0725
```

:::claves
- `np.random.default_rng(semilla)` crea un generador **nuevo e independiente** en cada llamada. Ese es el patrón correcto: un generador por componente (pesos, lotes, aumento) en lugar de uno global compartido, porque así el orden en que se consuman no altera a los demás.
- `rng.random()` no se guarda en ninguna variable y aun así cambia el resultado: consume un número de la secuencia. Es la demostración de que la semilla fija el **origen** de la secuencia, no los valores que se usan.
- `np.allclose` compara con tolerancia, no con igualdad exacta. Para decir «son la misma ejecución» es lo que quieres; para depurar un problema de determinismo bit a bit necesitarías `np.array_equal`, que distingue el último bit.
- `bool(...)` convierte el `np.bool_` que devuelve `allclose` en un `bool` de Python, para que el `print` diga `True` y no una representación con el tipo.
- Compara los dos `print` primeros: la única diferencia entre `a` y `c` es una línea dentro de la función. En un entrenamiento real esa línea la añade el tiempo: una capa nueva, un aumento de datos, un `dropout` que antes no estaba.
:::

```python verificable
import numpy as np

# Cuatro ejecuciones del mismo codigo con la misma configuracion: solo cambia la semilla
acc = np.array([0.8450, 0.8312, 0.8503, 0.8388])
k = acc.size
media, s = acc.mean(), acc.std(ddof=1)
margen = 2 * s * np.sqrt(1 + 1 / k)          # intervalo de prediccion para UNA ejecucion nueva

print(f"media de las {k} ejecuciones  {media:.4f}")                      # -> 0.8413
print(f"dispersion entre semillas    {s:.4f}")                          # -> 0.0082
print(f"la proxima caera entre       {media - margen:.4f} y {media + margen:.4f}")   # -> 0.8229 y 0.8597
print(f"amplitud del intervalo       {2 * margen:.4f}")                 # -> 0.0368
```

:::claves
- `np.sqrt(1 + 1 / k)` y no `np.sqrt(1 / k)`: el intervalo de **predicción** de una ejecución nueva suma la varianza de la media (`s²/k`) y la varianza propia de una ejecución (`s²`). Si usaras solo `1/k` estarías calculando el intervalo de confianza de la media, que es más estrecho y no responde a la pregunta «¿qué sacará la próxima vez?».
- Con `k = 4` el factor vale `√1,25 = 1,118`, así que el margen es apenas un 12 % más ancho que `2s`. Es incómodo a propósito: con pocas semillas, la incertidumbre sobre dónde está la media es pequeña comparada con la dispersión propia del problema.
- `acc.std(ddof=1)` divide entre `k − 1`. Con cuatro valores, usar `ddof=0` daría una desviación un 15 % menor y un intervalo engañosamente estrecho.
- Los cuatro números están escritos a mano para que la salida sea siempre la misma. En un entrenamiento real salen de cuatro ejecuciones, y lo importante es que las cuatro compartan partición, época de parada y métrica.
- Fíjate en que la amplitud del intervalo, 0,0368, es mayor que la diferencia entre las semillas 2 y 3 (0,0115). Ahí está la razón de que reportar la mejor semilla sea una forma de mentir sin querer.
:::

```python ilustrativo
import os
import random

import numpy as np
import torch

# Fijar las tres fuentes de azar que dependen del codigo
semilla = 0
random.seed(semilla)
np.random.seed(semilla)
torch.manual_seed(semilla)
torch.cuda.manual_seed_all(semilla)

# CuDNN deja de elegir el algoritmo midiendo tiempos (que es lo que lo hace no determinista)
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True
# Ordena las reducciones en CUDA; algunas operaciones dejaran de estar disponibles
torch.use_deterministic_algorithms(True)
os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"

# El DataLoader necesita SU generador, y una semilla por worker
generador = torch.Generator()
generador.manual_seed(semilla)


def semilla_worker(worker_id):
    np.random.seed(semilla + worker_id)


cargador = torch.utils.data.DataLoader(
    conjunto, batch_size=64, shuffle=True, num_workers=4,
    generator=generador, worker_init_fn=semilla_worker,
)
```

:::claves
- `torch.manual_seed` fija el generador de la CPU **y** el de la GPU actual, pero no los de los workers del `DataLoader`: cada worker es un proceso nuevo y arranca con su propio estado. De ahí `worker_init_fn`.
- `generator=generador` y `shuffle=True` van juntos: si pasas un `generator` pero `shuffle=False`, el barajado no ocurre y el generador no se usa. Y si no pasas ninguno, el `DataLoader` usa el generador global, que ya se ha consumido un número impredecible de veces.
- `worker_init_fn` recibe el identificador del worker, no la semilla. Hay que derivar una semilla distinta por worker (`semilla + worker_id`); si todos usaran la misma, dos workers producirían el mismo aumento de datos para ejemplos distintos.
- `torch.use_deterministic_algorithms(True)` no es gratis: lanza un error cuando una operación no tiene implementación determinista. Es preferible a que dé un resultado distinto cada vez, pero obliga a revisar el modelo.
- `CUBLAS_WORKSPACE_CONFIG` hay que fijarlo **antes** de la primera operación de cuBLAS; cambiarlo a mitad de ejecución no tiene efecto.
- Fíjate en que `os.environ` se toca en el mismo bloque que las semillas: el entorno es parte del estado reproducible. Si no lo registras junto al número de ejecución, la próxima vez no sabrás qué combinación produjo el resultado.
:::

## Errores típicos

- **Creer que `manual_seed(0)` lo fija todo.** Fija el origen de los flujos de CPU y de la GPU
  actual. Los workers del `DataLoader`, el aumento de datos y los kernels no deterministas se
  quedan fuera.
- **Comparar ejecuciones con distinto número de workers o distinta GPU.** No son la misma
  ejecución, aunque el registro diga lo mismo. Si el entorno forma parte del resultado, tiene que
  formar parte de la ficha.
- **Fijar la semilla y no anotarla.** Una ejecución sin su semilla es irrepetible por definición,
  y la semilla es un campo más barato de guardar que cualquier otra cosa del registro.
- **Confundir reproducible con determinista.** Reproducible es que dos ejecuciones cuenten la
  misma historia; determinista es que den los mismos bits. Se puede ser reproducible a nivel
  estadístico sin ser determinista, y es lo normal.
- **Reportar una sola semilla.** El número es correcto y la conclusión es falsa: con la
  dispersión habitual entre semillas, la mitad de las mejoras que se anuncian caben dentro del
  ruido.
- **Perseguir el bit a bit en producción.** Fijar todo el determinismo cuesta velocidad y
  restringe operaciones. Sirve para depurar y para comparar dos versiones del código en la misma
  máquina, no para cada entrenamiento del día a día.

:::practica
enunciado: Entrenas la misma configuración con 5 semillas y obtienes una exactitud media de 0,912 con una desviación típica entre semillas de 0,011. ¿Qué rango esperas para la sexta ejecución? ¿Y si en vez de predecir una ejecución nueva quisieras dar el intervalo de confianza de la media al 95 %?
pista: El intervalo de predicción de una ejecución nueva usa `2 · s · √(1 + 1/k)`; el de la media usa `2 · s / √k`.
solucion: Para una ejecución nueva, el margen es 2 · 0,011 · √(1 + 1/5) = 0,022 · 1,0954 = 0,0241, así que la sexta caerá entre 0,8879 y 0,9361. Para la media, el margen es 2 · 0,011 / √5 = 0,0098, es decir la media está entre 0,9022 y 0,9218. La diferencia entre los dos intervalos es la lección: la media se conoce bastante bien con cinco semillas, pero lo que sacará la próxima ejecución sigue siendo incierto casi cuatro veces más. Un informe que dé solo la media está prometiendo una precisión que la próxima ejecución no va a cumplir.
:::

## Comprueba que lo sabes

:::quiz
p: Dos ejecuciones con el mismo código dan pérdidas idénticas durante las dos primeras épocas y luego se separan. ¿Cuál es el sospechoso más probable?
o: Que la GPU se ha calentado y ha bajado la frecuencia
o: Que algo consume números del generador de forma distinta, como un `DataLoader` con workers o un aumento de datos
o: Que la función de pérdida es numéricamente inestable
a: 2
e: Que coincidan al principio y diverjan después es la firma de un flujo aleatorio desplazado: al inicio se consumen las mismas extracciones y, en cuanto entra el componente que consume de más, todo lo que viene después cambia. Una frecuencia de GPU distinta cambiaría los últimos bits desde el primer paso, no la trayectoria.
:::

:::quiz
p: ¿Qué diferencia hay entre el intervalo de confianza de la media y el intervalo de predicción de una ejecución nueva?
o: Ninguna, los dos miden lo mismo con nombres distintos
o: El de predicción solo sirve si el modelo es determinista
o: El de la media se estrecha con más semillas como `1/√k`; el de una ejecución nueva tiende a la dispersión completa del problema
a: 3
e: El intervalo de la media estima dónde está el valor esperado y se estrecha al repetir. El de una ejecución nueva incluye además la variabilidad propia de esa ejecución, así que se queda en torno a dos desviaciones típicas por mucho que aumentes el número de semillas.
:::

:::quiz
p: ¿Para qué sirve activar `torch.use_deterministic_algorithms(True)`?
o: Para que el entrenamiento sea más rápido al elegir siempre el mismo algoritmo
o: Para que las operaciones usen implementaciones de orden fijo, a cambio de que algunas no estén disponibles y lancen un error
o: Para fijar automáticamente todas las semillas del programa
a: 2
e: La bandera obliga a que las reducciones se hagan en un orden reproducible. Como contrapartida, las operaciones que no admiten un orden fijo dejan de ejecutarse y avisan, y algunas pierden velocidad. No fija ninguna semilla: eso hay que hacerlo aparte.
:::

:::aviso
Antes de dar por bueno un resultado, comprueba que puedes repetirlo. La prueba más barata es
relanzar la misma configuración con la misma semilla en la misma máquina y ver si los pesos
coinciden; si no coinciden, hay azar que no has localizado y cualquier comparación posterior
arrastra ese ruido.
:::
