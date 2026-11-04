---
id: fine-tuning-y-lora
titulo: Ajuste fino y LoRA
fase: 7
nivel: avanzado
rutas: [ds]
prerequisitos: [transfer-learning, operaciones-matriciales, optimizadores, tasas-de-aprendizaje-y-schedulers]
tags: [fine-tuning, lora, adaptadores, memoria]
resumen: Entrenar todos los pesos, solo una cabeza nueva o un par de matrices pequenas por capa: la diferencia esta en memoria, en estabilidad y en cuantos checkpoints guardas.
fuentes: ["Hu et al. (2021), 'LoRA: Low-Rank Adaptation of Large Language Models'", "Dettmers et al. (2023), 'QLoRA: Efficient Finetuning of Quantized LLMs'"]
---

## En una frase

El ajuste fino entrena los pesos del modelo preentrenado con tus datos; LoRA deja el modelo
original congelado y aprende, para cada matriz, una corrección de rango bajo que se puede
guardar aparte, sumar o descartar sin tocar los pesos originales.

## La idea

Adaptar un modelo grande a una tarea nueva es como corregir un manual técnico para tu empresa.
Puedes reescribir el libro entero (ajuste fino completo), puedes añadir un capítulo al final
(entrenar solo la cabeza) o puedes llenarlo de notas adhesivas en los márgenes (LoRA). Las
notas pesan casi nada, se quitan sin romper el libro y, para la mayoría de los ajustes, son
suficientes.

Lo que hace posible lo tercero es una observación empírica: **el cambio que necesita una matriz
de pesos para adaptarse a una tarea nueva suele tener rango bajo**. Una matriz de `768 × 768`
tiene 589.824 grados de libertad, pero la diferencia entre los pesos preentrenados y los
buenos para tu tarea se puede describir con dos matrices pequeñas de rango 8. Eso no es una
propiedad matemática universal, es lo que se observa; y es la apuesta central de LoRA.

Hay tres razones prácticas, y ninguna es «queda más elegante»:

1. **Memoria del optimizador.** Con Adam y compañía, cada parámetro entrenable arrastra dos
   momentos (media y varianza del gradiente) además de su gradiente. Entrenar en `float32` un
   modelo de 7.000 millones de parámetros exige almacenar pesos, gradientes y momentos: unos
   `7·10⁹ × 16 bytes ≈ 112 GB`. Si entrenas el 2 % de los parámetros, esa cuenta se divide por
   cincuenta. Es aritmética, no una opinión.
2. **Un adaptador por tarea.** Si entrenas todo, cada cliente o cada tarea necesita su copia
   completa del modelo. Con LoRA guardas megabytes por tarea y compartes una base.
3. **Menos olvido catastrófico.** Al no tocar los pesos originales, la tarea antigua se degrada
   menos. Y si el adaptador sale mal, se apaga y vuelves al modelo de partida.

El coste es que la capacidad de adaptación está limitada por el rango `r`, y que en inferencia
el adaptador añade un poco de latencia si no lo fusionas con la matriz base. Fusionarlo es
exactamente sumar `ΔW` a `W_0`, con la pérdida de precisión que eso implique si la base está
cuantizada.

:::figura
fichero: fine-tuning-y-lora-presupuesto-y-rango
pie: El panel izquierdo es la aritmética que hace atractivo a LoRA, en escala logarítmica porque si no las barras naranjas no se verían. En la capa de atención, el ajuste completo entrena 589.824 parámetros y el adaptador con `r = 8` solo 12.288: un 2,08 %. En la capa MLP la proporción baja a 1,30 %, y la razón está en el crecimiento: el adaptador cuesta `r·(d + k)`, que es lineal, mientras que la matriz completa cuesta `d·k`, que es cuadrático. Cuanto más grande es la capa, más barato sale LoRA en términos relativos. Esa diferencia se multiplica por los tres estados del optimizador (gradiente, media y varianza) y por los bytes por parámetro, que es de donde salen las decenas de gigabytes que se ahorran. El panel derecho explica el límite de la técnica, y es la parte que se olvida: `ΔW = (α/r)·B·A` es un producto de dos matrices de rango `r`, así que su rango no puede pasar de `r`. Con `r = 2` sobre una matriz de 8 × 8, solo 2 de los 8 valores singulares son distintos de cero: la corrección vive en un subespacio de dimensión 2 y el resto de direcciones no se pueden tocar. LoRA no puede producir cualquier ajuste, solo los que caben en ese subespacio. Ese es el supuesto del método: que el ajuste que necesita tu tarea tiene rango bajo.
fuente: figuras/fine-tuning-y-lora-1.py
:::

## Definición formal

Una capa lineal aplica `h = W_0·x`, con `W_0` de tamaño `d × k` (`d` salidas, `k` entradas). El
ajuste fino completo aprende una `W` nueva; LoRA deja `W_0` congelada y aprende dos matrices:

:::formula
h = W_0 · x + (α / r) · B · A · x
:::

- `W_0` — los pesos preentrenados, **congelados**; no reciben gradiente.
- `A` — matriz de `r × k`, inicializada con valores aleatorios pequeños.
- `B` — matriz de `d × r`, inicializada **a ceros**.
- `r` — el rango del adaptador; es el hiperparámetro que fija su capacidad. Típicamente 4, 8 o 16.
- `α` — constante de escala; el factor efectivo es `α / r`.
- `ΔW = (α / r)·B·A` — la corrección que se suma a la matriz original en inferencia.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `d` | Número de salidas de la capa (filas de `W_0`) | neuronas | La matriz completa crece como `d·k` y el adaptador como `r·(d + k)`: LoRA sale relativamente más barato |
| `k` | Número de entradas de la capa (columnas de `W_0`) | neuronas | Igual que `d`: el coste del adaptador crece linealmente y el del ajuste completo, cuadráticamente |
| `r` | Rango del adaptador: su capacidad | adimensional | Los parámetros entrenables suben de forma lineal, `r·(d + k)`, y con ellos la capacidad de adaptación. Con `r` grande el adaptador se comporta como un ajuste fino completo y vuelve el sobreajuste |
| `α` | Constante de escala del adaptador | adimensional | La corrección se multiplica por `α / r`: con `α` alto el adaptador mueve más los pesos con cada paso, así que suele pedir una tasa de aprendizaje menor |
| `α / r` | El factor de escala efectivo | adimensional | Es lo que de verdad escala la corrección. Si duplicas `r` y dejas `α` igual, el factor se reduce a la mitad y el adaptador aprende más despacio |
| `W_0` | Los pesos preentrenados, congelados | adimensionales | No se mueve y no recibe gradiente ni momentos del optimizador: es de donde viene todo el ahorro de memoria |
| `A`, `B` | Las dos matrices del adaptador: `A` es `r × k` y `B` es `d × r` | adimensionales | `B` se inicializa a ceros para que `ΔW = 0` al arrancar. El número de parámetros entrenables es `r·(k + d)` |
| `ΔW` | La corrección que se suma a la matriz base, `(α/r)·B·A` | adimensionales | Su rango está acotado por `r`: al subir `r` caben más direcciones de corrección y el ajuste es más expresivo |
:::

Tres consecuencias que conviene tener claras:

1. **`ΔW` empieza siendo cero.** Como `B = 0`, al iniciar el entrenamiento la capa se comporta
   exactamente como el modelo preentrenado: no hay salto en la pérdida en el primer paso.
2. **`rango(ΔW) ≤ r`.** Por definición de rango de un producto, la corrección vive en un
   subespacio de dimensión como mucho `r`. El número de parámetros entrenables de la capa pasa
   de `d·k` a `r·(d + k)`.
3. **`α` no significa nada sin `r`.** Si duplicas `r` y dejas `α` igual, el factor `α / r` se
   reduce a la mitad… y a la vez se duplica la capacidad. La práctica habitual es subir `α` con
   `r` para mantener
   más o menos constante la escala de la corrección.

La variante **QLoRA** cuantiza los pesos congelados a 4 bits (formato NF4: una cuantización
diseñada para distribuciones normales) y mantiene los adaptadores en `bfloat16`. El resultado
es que se puede ajustar un modelo que no cabría en memoria en precisión completa, con una
pérdida de calidad que hay que medir en tu tarea, no suponer.

:::nota
Ajustar el modelo completo con datos de instrucciones (lo que se llama SFT) es el paso previo
al alineamiento: véase [[instruccion-y-alineamiento]]. LoRA es una forma de hacer ese mismo
SFT gastando una fracción de la memoria.
:::

## Ejemplo

Presupuesto de parámetros entrenables para una capa de atención de `768 × 768` y una capa del
bloque MLP de `768 × 3072`, con tres rangos distintos:

```
atencion 768x768  r= 4  completo=  589824  LoRA=  6144  1.0417%
atencion 768x768  r= 8  completo=  589824  LoRA= 12288  2.0833%
atencion 768x768  r=16  completo=  589824  LoRA= 24576  4.1667%
     MLP 768x3072  r= 4  completo= 2359296  LoRA= 15360  0.6510%
     MLP 768x3072  r= 8  completo= 2359296  LoRA= 30720  1.3021%
     MLP 768x3072  r=16  completo= 2359296  LoRA= 61440  2.6042%
```

Con `r = 8` en la capa de atención: `8 · (768 + 768) = 12.288` parámetros frente a `589.824`,
un `2,08 %`. En la capa MLP el porcentaje baja a `1,30 %` porque la matriz original es más
grande y el coste del adaptador crece con `d + k`, no con `d · k`. Subir de `r = 4` a `r = 16`
cuadruplica el adaptador: el rango es la perilla que decide cuánto puedes aprender.

Segundo ejemplo: la corrección tiene rango acotado. Con `r = 2` sobre una matriz de `8 × 8`:

```
valores singulares de delta W: [50.1984 26.6556  0.      0.      0.      0.      0.      0.    ]
valores singulares no nulos: 2 de 8
norma de Frobenius con alpha/r=8.0: 56.8366
```

De los 8 valores singulares posibles, solo 2 son distintos de cero. Esa es la restricción de
LoRA en una frase: no puede producir cualquier corrección, solo las que caben en un subespacio
de dimensión `r`. Y la escala de la corrección depende de `α / r = 8`, no de `α` a secas.

## Código

```python verificable
# Presupuesto de parametros: W (d x k) frente a B (d x r) y A (r x k).
for d, k, nombre in ((768, 768, "atencion"), (768, 3072, "MLP")):
    completo = d * k
    for r in (4, 8, 16):
        lora = r * (d + k)              # B y A juntas
        print(f"{nombre:>8} {d}x{k}  r={r:>2}  completo={completo:>8}"
              f"  LoRA={lora:>6}  {lora / completo:.4%}")
# El formato :.4% multiplica por 100 y anade el signo de porcentaje; no es lo mismo que
# :.4f, que daria 0.0208 en vez de 2.0833%.
# -> atencion 768x768  r= 4  completo=  589824  LoRA=  6144  1.0417%
# -> atencion 768x768  r= 8  completo=  589824  LoRA= 12288  2.0833%
# -> atencion 768x768  r=16  completo=  589824  LoRA= 24576  4.1667%
# ->      MLP 768x3072  r= 4  completo= 2359296  LoRA= 15360  0.6510%
# ->      MLP 768x3072  r= 8  completo= 2359296  LoRA= 30720  1.3021%
# ->      MLP 768x3072  r=16  completo= 2359296  LoRA= 61440  2.6042%
```

```python verificable
import numpy as np

# El rango de la correccion esta acotado por r: comprobamos los valores singulares.
rng = np.random.default_rng(0)
d, k, r, alpha = 8, 8, 2, 16
A = rng.normal(size=(r, k))
B = rng.normal(size=(d, r))
delta = (alpha / r) * (B @ A)                 # la actualizacion que aprende LoRA
s = np.linalg.svd(delta, compute_uv=False)

print("valores singulares de delta W:", np.round(s, 4))
# -> valores singulares de delta W: [50.1984 26.6556  0.      0.      0.      0.      0.      0.    ]
print("valores singulares no nulos:", int((s > 1e-10).sum()), "de", d)
# -> valores singulares no nulos: 2 de 8
print(f"norma de Frobenius con alpha/r={alpha / r:.1f}: {np.linalg.norm(delta):.4f}")
# -> norma de Frobenius con alpha/r=8.0: 56.8366
```

```python ilustrativo
# Con la libreria peft, LoRA en cuatro lineas. No se ejecuta: necesita pesos descargados.
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

base = AutoModelForCausalLM.from_pretrained("ruta/al/modelo")

config = LoraConfig(
    r=8,                       # rango del adaptador
    lora_alpha=16,             # la escala que se divide por r
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],   # a que matrices se engancha el adaptador
    task_type="CAUSAL_LM",
)
modelo = get_peft_model(base, config)
modelo.print_trainable_parameters()   # imprime cuantos parametros se entrenan de verdad

# Al terminar, se guarda SOLO el adaptador (unos pocos MB) con modelo.save_pretrained(...)
# y se carga encima de la misma base en otra maquina.
```

## Errores típicos

- **Inicializar `B` con valores aleatorios.** Si `B` no empieza en cero, `ΔW ≠ 0` desde el
  primer paso y las predicciones del modelo cambian de golpe: la pérdida arranca alta y a veces
  ya no se recupera. La inicialización correcta es `A` aleatoria (normal pequeña) y `B = 0`, de
  modo que el modelo empieza siendo exactamente el preentrenado.
- **Subir `r` «para que aprenda más» sin mirar la validación.** `r` es la capacidad del
  adaptador: con `r` grande el adaptador se comporta como un ajuste fino completo y vuelve el
  sobreajuste que querías evitar. Además, con `α` fijo, cambiar `r` cambia el factor `α / r` y
  por tanto la escala efectiva del paso; sube `r` y `α` a la vez o ajusta la tasa.
- **Aplicar LoRA a las capas equivocadas.** Poner el adaptador solo en las consultas y no en los
  valores, u olvidar las capas MLP, deja fuera buena parte de la adaptación. `target_modules` se
  elige con un experimento comparativo, no por costumbre, y hay que comprobar que los nombres
  coinciden con los de tu arquitectura (cambian entre familias de modelos).
- **Comparar LoRA y ajuste fino completo con la misma tasa de aprendizaje.** No son el mismo
  problema de optimización: LoRA suele necesitar una tasa más alta (los adaptadores parten de
  cero) y menos épocas. Comparar con la misma configuración y concluir que «LoRA es peor» es un
  error de banco de pruebas.
- **Fusionar el adaptador en la base cuantizada y seguir entrenando.** Fusionar suma `ΔW` a
  pesos de 4 bits: se pierde precisión y ya no puedes separar el adaptador. Si vas a seguir
  entrenando o a cambiar de tarea, mantén el adaptador aparte y fusiona solo para servir.
- **Evaluar con los ejemplos del ajuste.** Con adaptadores pequeños es fácil que el modelo
  memorice unas decenas de ejemplos y parezca que ha aprendido la tarea. Reserva un conjunto de
  prueba que no haya tocado ni el preentrenamiento ni el ajuste.

:::practica
enunciado: Para una capa de 1.024 × 1.024 y para una del MLP de 1.024 × 4.096, calcula los parámetros entrenables de LoRA con r = 8 y el porcentaje que representa sobre el ajuste fino completo. ¿Por qué el porcentaje es menor en la segunda?
pista: El adaptador son dos matrices: r·k + d·r = r·(d + k).
solucion: Capa de atención: 8 · (1.024 + 1.024) = 16.384 frente a 1.024 · 1.024 = 1.048.576, es decir 16.384 / 1.048.576 = 1,5625 %. Capa MLP: 8 · (1.024 + 4.096) = 40.960 frente a 1.024 · 4.096 = 4.194.304, es decir 40.960 / 4.194.304 = 0,9766 %. El porcentaje baja porque el coste del adaptador crece con d + k, que es lineal, mientras que la matriz original crece con d · k: cuanto más grande es la capa, más barato sale LoRA en términos relativos.
:::

## Comprueba que lo sabes

:::quiz
p: Con r = 8 en una capa de 768 × 768, ¿cuántos parámetros entrena LoRA y cuántos tendría el ajuste completo?
o: 12.288 frente a 589.824, un 2,08 %
o: 6.144 frente a 589.824, un 1,04 %
o: 589.824 en los dos casos, porque la matriz base sigue existiendo
a: 1
e: El adaptador son dos matrices: r·k + d·r = 8·768 + 768·8 = 12.288. Los 589.824 de W_0 siguen ahí pero están congelados: no reciben gradiente ni momentos del optimizador, que es de donde viene el ahorro.
:::

:::quiz
p: ¿Por qué la matriz B se inicializa a ceros?
o: Para que la corrección ΔW sea cero al empezar y el modelo arranque siendo idéntico al preentrenado
o: Para que el rango de ΔW sea exactamente r en lugar de como mucho r
o: Para que el producto B·A sea simétrico
a: 1
e: Con B = 0, ΔW = 0 en el primer paso y la pérdida arranca en el valor del modelo preentrenado, sin salto. El rango sigue estando acotado por r independientemente de cómo se inicialice, y el producto de dos matrices rectangulares no tiene por qué ser simétrico.
:::

:::quiz
p: ¿Qué hace exactamente QLoRA respecto a LoRA?
o: Cuantiza los pesos congelados a 4 bits y mantiene los adaptadores en mayor precisión
o: Cuantiza también los adaptadores a 4 bits para ahorrar el doble
o: Sustituye el adaptador por una destilación del modelo grande a uno pequeño
a: 1
e: La base se guarda en 4 bits (formato NF4) porque no recibe gradientes, y los adaptadores, que sí se entrenan, se mantienen en bfloat16. La opción 2 destruiría el entrenamiento al cuantizar justo lo que se optimiza, y la 3 describe la destilación, que es otra técnica.
:::
