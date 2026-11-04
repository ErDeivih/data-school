---
id: preentrenamiento-y-escalado
titulo: Preentrenamiento y escalado
fase: 8
nivel: avanzado
rutas: [ds]
prerequisitos: [como-funciona-un-llm, funciones-de-perdida, transformers]
tags: [llm, escalado, coste, corpus]
resumen: Como se construye un corpus, que se optimiza durante el preentrenamiento y por qué el tamaño de un modelo se decide con leyes de escalado y no por intuición.
fuentes: ["Kaplan et al. (2020), 'Scaling Laws for Neural Language Models'", "Hoffmann et al. (2022), 'Training Compute-Optimal Large Language Models'"]
---

## En una frase

Preentrenar es hacer descender la entropía cruzada de «predecir el siguiente token» sobre un
corpus enorme; las leyes de escalado describen cómo baja esa pérdida al subir parámetros,
tokens y cómputo, y sirven para decidir el reparto antes de gastar el dinero.

## La idea

Hay tres cantidades que gobiernan todo lo demás, y conviene tenerlas separadas en la cabeza:

- `N`: **parámetros** del modelo, los números que se aprenden.
- `D`: **tokens** de texto que el modelo llega a leer durante el entrenamiento.
- `C`: **cómputo**, medido en operaciones en coma flotante (FLOPs). Es el presupuesto.

El error de principiante es pensar que un modelo es solo `N`. No lo es: un modelo de 10.000
millones de parámetros entrenado con 20.000 millones de tokens ha visto muy poco texto para su
tamaño, y uno de 1.000 millones entrenado con 200.000 millones de tokens suele rendir mejor.
Los tres números van juntos.

**El corpus.** Antes de entrenar hay una fase de ingeniería que ocupa más tiempo que el
entrenamiento y decide más que la arquitectura. Se recoge texto (páginas web, libros, código,
artículos), se filtra (se quitan plantillas, menús de navegación, texto generado, contenido
ofensivo o ilegal), se **deduplica** y se mezcla por dominios con unas proporciones elegidas a
mano. La deduplicación no es cosmética: si el mismo texto aparece treinta veces, el modelo lo
memoriza, la pérdida de entrenamiento mejora artificialmente y el modelo generaliza peor. El
filtrado de calidad tiene el efecto contrario al que sugiere la intuición: quitar el 90 % del
texto y quedarse con el 10 % mejor suele dar un modelo mejor que entrenar con todo.

**El objetivo.** Casi todos los modelos actuales usan la predicción del siguiente token sobre
texto sin etiquetar. Es autosupervisado: la etiqueta de cada posición es el token siguiente, así
que no hace falta anotar nada. Algunos modelos usan objetivos con huecos (enmascarar fragmentos
y reconstruirlos), pero la familia dominante es la autorregresiva porque es la que permite
generar texto de forma natural.

**Las leyes de escalado.** Lo sorprendente, y lo que las hace útiles, es que la pérdida baja de
forma suave y predecible al subir `N`, `D` y `C`: en escala logarítmica, una recta. No hay
escalones mágicos. Eso permite hacer algo muy poco habitual en machine learning:
**extrapolar**. Entrenas modelos pequeños, ajustas la curva y estimas cuánto vas a mejorar (y
cuánto vas a gastar) con un modelo diez veces mayor, antes de construirlo.

La consecuencia práctica más importante es el reparto. Durante un tiempo se entrenaron modelos
enormes con relativamente pocos tokens; los trabajos sobre reparto óptimo de cómputo mostraron
que, para un presupuesto fijo, conviene un modelo más pequeño y más tokens. La regla de trabajo
que salió de ahí es que los tokens deben ser del orden de veinte veces los parámetros. La cifra
exacta depende del ajuste y del corpus, pero el orden de magnitud cambió la industria.

**Dónde se rompe.** Dos límites reales:

1. **Te quedas sin datos.** Cuando has agotado el texto disponible de calidad, repetir el corpus
   varias veces aporta cada vez menos. Entras en el régimen limitado por datos, donde escalar
   `N` ya no ayuda: ayuda la calidad, la mezcla y el uso del cómputo en pasos de entrenamiento
   mejor aprovechados.
2. **La pérdida no lo es todo.** Un modelo con mejor pérdida de preentrenamiento puede ser peor
   en la tarea que te importa. La pérdida mide verosimilitud media sobre texto cualquiera, no
   corrección factual, ni seguimiento de instrucciones, ni seguridad. Lo que convierte el
   modelo preentrenado en asistente es la fase siguiente
   ([[instruccion-y-alineamiento|instrucción y alineamiento]]).

Y una advertencia sobre el coste que casi nadie hace al principio: **el entrenamiento se paga
una vez; la inferencia se paga siempre**. Entrenar cuesta del orden de `6·N·D` FLOPs; servir
una petición cuesta del orden de `2·N` FLOPs por token generado. Con millones de peticiones al
día, la factura de servir supera con holgura la de entrenar, y por eso los modelos pequeños y
destilados son un negocio, no una moda.

## Definición formal

**Cómputo de entrenamiento.** Para un transformer con `N` parámetros entrenado sobre `D` tokens:

:::formula
C_train ≈ 6 · N · D
:::

- `N` — número de parámetros entrenables.
- `D` — número de tokens procesados (no de tokens distintos: si repites el corpus, cuentan las
  repeticiones).
- El 6 sale de sumar el paso hacia delante (`2·N·D`) y el paso hacia atrás (`4·N·D`): la
  retropropagación cuesta aproximadamente el doble que la inferencia.
- **Inferencia:** `C_inf ≈ 2 · N` FLOPs por token generado, porque solo hay paso hacia delante.

**Tiempo de entrenamiento.** Con una máquina que sostiene `F` FLOPs por segundo de forma
efectiva:

:::formula
t ≈ C_train / F
:::

- `F` — rendimiento efectivo, no el pico teórico del acelerador. La diferencia entre el pico y
  lo que se sostiene de verdad es grande (comunicación entre dispositivos, esperas de datos,
  capas poco eficientes), así que en cualquier plan serio se mide en el propio sistema.

**Ley de potencia de la pérdida.** La forma que se ajusta a los datos es:

:::formula
L(N) = L∞ + a · N^(−α)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `N` | Parámetros entrenables del modelo | número de escalares | La pérdida baja, pero cada multiplicación por 10 baja menos que la anterior |
| `D` | Tokens procesados, repeticiones incluidas | tokens | Con `N` fijo, la pérdida baja hasta que el modelo empieza a memorizar el corpus |
| `C` | Cómputo de entrenamiento, `≈ 6·N·D` | FLOPs | Es el presupuesto: reparte entre `N` y `D`, no los elige por ti |
| `F` | Rendimiento efectivo del hardware | FLOP/s sostenidos | El tiempo baja en proporción directa: doblar `F` es la mitad de horas |
| `L∞` | Pérdida irreducible: el suelo de la curva | neperios (nats) | No baja con `N`: marca el límite de todo el escalado |
| `a` | Constante de escala de la ley | neperios (nats) | Depende del corpus y del tokenizador, no del tamaño del modelo |
| `α` | Exponente de la ley de potencia | adimensional | Cuanto menor es, más plano es el retorno: hace falta más `N` para lo mismo |
| `N*`, `D*` | Reparto óptimo para un presupuesto dado | parámetros y tokens | Con `D ≈ 20·N`, crecen como la raíz del presupuesto |
:::

- `L∞` — la pérdida irreducible: el suelo al que tiende la curva al crecer `N` indefinidamente.
- `a` — constante de escala, dependiente de la tokenización y del corpus.
- `α` — el exponente de la ley de potencia. Cuanto menor es, más plano es el retorno.
- Lo importante es la forma: cada multiplicación de `N` por 10 baja la pérdida una cantidad
  **cada vez menor**. Lo que se gana en el primer salto no se recupera en el décimo.

**Reparto óptimo con presupuesto fijo.** Con `C` fijo y `C = 6·N·D`, si se impone que los
tokens sean unas 20 veces los parámetros (`D ≈ 20·N`), entonces `C ≈ 120·N²`, y despejando:

:::figura
fichero: preentrenamiento-suelo-y-retorno-decreciente
pie: A la izquierda, la pérdida frente al tamaño del modelo en escala logarítmica. La banda azul es lo que aporta tener más parámetros y la línea roja discontinua es el suelo irreducible: por mucho que crezcas, la curva no baja de ahí, y a partir de cierto punto la mejora es invisible. A la derecha, lo que baja la pérdida en cada salto de multiplicar por diez: 0,3050, 0,2719 y 0,2423. Ese descenso es la razón de que las decisiones de escalado se tomen con una curva ajustada y no con la esperanza de que «más grande será mucho mejor».
fuente: figuras/preentrenamiento-y-escalado-1.py
:::

:::formula
N* ≈ √(C / 120)      D* ≈ 20 · N*
:::

Los dos números salen del mismo presupuesto: no se eligen por separado.

## Ejemplo

**Cuánto cuesta.** Un modelo de 1.000 millones de parámetros (`N = 1e9`) entrenado con 20.000
millones de tokens (`D = 2e10`):

```
FLOPs totales      1.200e+20
horas en una GPU   111.1
horas en 64 GPUs   1.74
```

El cómputo es `6 · 1e9 · 2e10 = 1,2e20` FLOPs. Con un supuesto explícito de `3e14` FLOPs por
segundo efectivos en un solo acelerador, son 111 horas; repartido entre 64, menos de dos horas.
Sube `D` a 200.000 millones de tokens (el reparto recomendado para ese tamaño) y el cómputo se
multiplica por diez: 1,2e21 FLOPs.

**Cuánto repartir.** Con un presupuesto de `1e20` FLOPs:

```
para 1e+20 FLOPs -> N = 9.129e+08 parametros, D = 1.826e+10 tokens
```

Es decir, unos 913 millones de parámetros y 18.300 millones de tokens. Compara esa decisión con
la de entrenar 10.000 millones de parámetros con esos mismos tokens: aunque el modelo quepa en
memoria, el presupuesto no da para ver suficiente texto y el resultado es peor.

**Cuánto se gana al escalar.** Con una ley de potencia de juguete `L(N) = 2,5·(N/1e9)^(−0,05) + 1,6`
(los exponentes son de ejemplo, lo que importa es la forma):

```
1e+08 -> 1e+09: baja 0.3050
1e+09 -> 1e+10: baja 0.2719
1e+10 -> 1e+11: baja 0.2423
```

Cada multiplicación por diez de parámetros da menos que la anterior. Si además multiplicas por
diez el cómputo para conseguir el salto, el rendimiento por FLOP cae todavía más rápido. Esa es
la razón por la que las decisiones de escalado se toman con una curva ajustada y no con la
esperanza de que «más grande será mucho mejor».

## Código

```python verificable
# Coste de un preentrenamiento: C ~ 6 * N * D (N parametros, D tokens)
N = 1.0e9        # parametros
D = 2.0e10       # tokens
C = 6 * N * D    # FLOPs totales

# Supuesto explicito: 3.0e14 FLOP/s utiles sostenidos por GPU (no es un benchmark medido)
flops_por_segundo = 3.0e14
horas = C / flops_por_segundo / 3600    # de segundos a horas: 3600 s por hora

print(f"FLOPs totales      {C:.3e}")          # -> 1.200e+20
print(f"horas en una GPU   {horas:.1f}")      # -> 111.1
print(f"horas en 64 GPUs   {horas / 64:.2f}") # -> 1.74

# Con la regla de ~20 tokens por parametro, el reparto para un presupuesto dado:
presupuesto = 1.0e20
n_opt = (presupuesto / (6 * 20)) ** 0.5    # despeja N de C = 6 * N * (20 * N) = 120 * N^2
print(f"para {presupuesto:.0e} FLOPs -> N = {n_opt:.3e} parametros, D = {20 * n_opt:.3e} tokens")
# -> N = 9.129e+08 parametros, D = 1.826e+10 tokens
```

:::claves
- `1.0e9` es un `float`, no un entero: por eso la división `C / flops_por_segundo` sale exacta y `{C:.3e}` se imprime en notación científica. Si escribieras `N = 10**9` el resultado sería el mismo número, pero un `int` de Python, que no admite `.3e` con la misma facilidad.
- La división entre `3600` es solo un cambio de unidad (segundos a horas). Olvidarla da un número 3.600 veces mayor y el error pasa desapercibido porque sigue siendo «un número grande».
- `(6 * 20) ** 0.5` sale de despejar `N` en `C = 120·N²`: la raíz convierte el presupuesto en parámetros. La línea siguiente multiplica ese `N` por 20 para dar los tokens, así que **`D` no es una decisión independiente**: sale del mismo presupuesto.
- `.0e` en `f"{presupuesto:.0e}"` imprime `1e+20` con un solo dígito de exponente. Si en vez de `presupuesto` pasaras una lista o un texto, el `print` fallaría con `ValueError`.
- En el segundo bloque, `(n / 1e9) ** -0.05` con exponente **negativo** hace que la pérdida baje al crecer `n`. Con `n = 0` la operación daría división entre cero: la ley solo tiene sentido para tamaños positivos.
- El bucle `for n in (1e8, 1e9, 1e10, 1e11)` recorre una **tupla de floats**, no un `range`: la variable `n` vale 100 000 000 y no 0, 1, 2, 3. Confundir los dos es el error clásico al leer este tipo de bucles.
- La resta `perdida(n) - perdida(10 * n)` mide lo que se gana en un salto de diez. Da positivo siempre porque la función es decreciente; lo interesante es que el tercer salto ya baja menos que el primero, y eso no se ve mirando solo la pérdida final.
:::

```python verificable
import numpy as np

# Ley de potencia de juguete: L(N) = 2.5 * (N/1e9)^-0.05 + 1.6
# Los exponentes son de ejemplo; lo que se ve es la forma de la curva, no un resultado medido.
def perdida(n):
    return 2.5 * (n / 1e9) ** -0.05 + 1.6

for n in (1e8, 1e9, 1e10, 1e11):
    print(f"parametros {n:.0e}  perdida {perdida(n):.4f}")
# -> una linea por tamano; lo que importa es como se aplana la columna de perdidas

# Cuanto se gana al multiplicar por 10 los parametros en cada salto
for n in (1e8, 1e9, 1e10):
    print(f"{n:.0e} -> {10 * n:.0e}: baja {perdida(n) - perdida(10 * n):.4f}")
# -> los tres saltos bajan: 0.3050, 0.2719, 0.2423
```

## Errores típicos

- **Comparar modelos por su número de parámetros.** Dos modelos del mismo tamaño pueden diferir
  mucho según cuántos tokens hayan visto y con qué calidad. Un modelo pequeño bien entrenado
  gana a uno grande mal alimentado; la comparación honesta incluye `N`, `D` y el corpus.
- **Creer que las leyes de escalado se extrapolan sin fin.** Son ajustes empíricos sobre un
  rango concreto de tamaños. Fuera de ese rango se topan con la pérdida irreducible, con la
  falta de datos de calidad y con el hecho de que mejorar la pérdida media no garantiza mejorar
  la tarea que te importa.
- **Entrenar desde cero lo que se resuelve con ajuste fino.** Si tu problema es concreto (un
  dominio, un formato, una tarea), casi nunca necesitas preentrenar: necesitas partir de un
  modelo ya preentrenado y adaptarlo ([[fine-tuning-y-lora|ajuste fino y LoRA]]). El
  preentrenamiento desde cero se justifica cuando tienes un corpus muy distinto, mucho
  presupuesto y un equipo que sabe medir.
- **Saltarse la deduplicación.** El texto repetido infla la métrica de entrenamiento, favorece
  la memorización literal y desperdicia el presupuesto en ejemplos que ya has visto. Es la
  mejora más barata de todo el proceso.
- **Medir con datos contaminados por el corpus.** Si tu conjunto de evaluación aparece, aunque
  sea parcialmente, en el texto de entrenamiento, el resultado no mide generalización: mide
  recuerdo. Hay que buscar coincidencias exactas y aproximadas entre evaluación y corpus antes
  de publicar nada.
- **Confundir el coste de entrenar con el de servir.** El entrenamiento es un gasto puntual; la
  inferencia crece con cada usuario y cada token. Un modelo con un 2 % mejor de pérdida puede
  ser económicamente inviable si cuesta el triple por petición
  ([[coste-y-latencia|coste y latencia]]).

## Comprueba que lo sabes

:::quiz
p: Tienes un presupuesto fijo de cómputo y dudas entre un modelo muy grande con pocos tokens o uno más pequeño con muchos más tokens. ¿Qué dice el reparto óptimo?
o: Siempre el modelo más grande, porque la capacidad manda
o: Conviene un modelo más pequeño con más tokens, del orden de veinte tokens por parámetro
o: Da igual: con el mismo cómputo se obtiene la misma pérdida
a: 2
e: Con cómputo fijo, `C = 6·N·D`: crecer `N` sin crecer `D` deja el modelo con muy poco texto visto. Los ajustes publicados sobre reparto óptimo apuntan a que los tokens deben ser aproximadamente veinte veces los parámetros, no a maximizar el tamaño del modelo.
:::

:::quiz
p: ¿Por qué es útil que la pérdida siga una ley de potencia en `N`?
o: Porque garantiza que el modelo será correcto en la tarea final
o: Porque permite extrapolar desde modelos pequeños y decidir el presupuesto antes de entrenar el grande
o: Porque entonces la pérdida llega a cero con parámetros suficientes
a: 2
e: Una relación suave y predecible en escala logarítmica permite ajustar la curva con ejecuciones pequeñas y estimar coste y ganancia de una ejecución grande. No garantiza nada sobre la tarea final, y la asíntota de la curva no es cero, sino la pérdida irreducible.
:::

:::quiz
p: ¿En qué se diferencia el coste de entrenar del de servir el modelo?
o: El entrenamiento cuesta `6·N·D` FLOPs una vez; la inferencia cuesta del orden de `2·N` FLOPs por token generado y se paga en cada petición
o: Son el mismo cálculo, solo cambia la unidad de medida
o: La inferencia es más cara por token porque tiene que retropropagar
a: 1
e: El entrenamiento incluye paso hacia delante y hacia atrás (unas seis veces `N·D`), y ocurre una sola vez. La inferencia solo hace paso hacia delante, unas dos veces `N` por token, pero se repite con cada usuario indefinidamente.
:::

:::aviso
Escalar no arregla un corpus malo. Si el texto está duplicado, tiene plantillas repetidas o
está contaminado con la evaluación, gastar diez veces más cómputo hace que el problema sea diez
veces más caro, no que desaparezca. La deduplicación y el filtrado de calidad son las primeras
horas mejor invertidas de todo el proyecto.
:::
