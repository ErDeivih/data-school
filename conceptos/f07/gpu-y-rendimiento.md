---
id: gpu-y-rendimiento
titulo: GPU y rendimiento
fase: 7
nivel: avanzado
rutas: [ds]
prerequisitos: [pytorch-fundamentos, operaciones-matriciales, retropropagacion]
tags: [gpu, rendimiento, memoria, entrenamiento]
resumen: Por qué una GPU entrena redes y cómo aprovecharla de verdad: memoria, precisión mixta, acumulación de gradiente y los cuellos de botella que sí importan.
fuentes: ["Patterson y Hennessy (2020), 'Computer Architecture: A Quantitative Approach'", "Williams et al. (2009), 'Roofline: An Insightful Visual Performance Model for Multicore Architectures'"]
---

## En una frase

Una GPU no es «un procesador más rápido»: es un procesador con miles de núcleos pequeños
diseñados para hacer la misma operación sobre muchísimos números a la vez, y solo gana cuando
el trabajo es abundante, uniforme y no depende de mover datos de un sitio a otro.

## La idea

Imagina una cocina. La CPU es un restaurante con ocho cocineros excelentes: cada uno puede
preparar un plato distinto, consultar la receta, improvisar si falta un ingrediente. La GPU es
una fábrica de conservas con diez mil puestos: cada puesto hace exactamente lo mismo que el de
al lado, cortar tomate, pero entre todos cortan toneladas. Si tu problema es «cortar diez mil
tomates iguales», la fábrica arrasa. Si es «inventar un plato nuevo con lo que hay en la
nevera», la fábrica es un estorbo.

Entrenar una red neuronal es, casi literalmente, cortar tomates. El 90 % del tiempo de cálculo
se va en multiplicaciones de matrices: la misma operación `a · b + c` repetida millones de
veces sobre elementos independientes. Eso es lo que hace una GPU: ejecuta esa operación sobre
miles de elementos en paralelo con una sola instrucción.

Pero hay una trampa que explica la mitad de los disgustos con GPU: **los núcleos no pueden
hacer nada mientras esperan datos**. La memoria de la GPU (VRAM) es rápida pero no infinita, y
el canal que la conecta con los núcleos tiene un ancho de banda finito. Si tu operación hace
mucho cálculo por cada byte que lee, el cálculo manda y la GPU vuela. Si hace poco cálculo por
byte, el cuello de botella es la memoria y tener más núcleos no sirve de nada. Esa relación
tiene nombre y es la herramienta mental más útil de esta página: la **intensidad aritmética**.

De ahí salen las tres palancas que de verdad mueven el rendimiento: **lotes más grandes**
(más cálculo por byte leído), **precisión más baja** (menos bytes por número, y encima más
rápido en los núcleos que lo soportan) y **acumulación de gradiente** (simular un lote grande
cuando no cabe en memoria, a cambio de más tiempo). Todo lo demás —número de capas, tipo de
optimizador— importa, pero no es lo que decide si la GPU está al 95 % o al 20 %.

## Definición formal

Llamamos **FLOP** a una operación de coma flotante (por ejemplo una multiplicación y una suma).
Los dos límites de una GPU son:

- **Pico de cálculo** `P`: FLOP por segundo que los núcleos pueden ejecutar en el mejor caso.
  Se mide en TFLOPS (10¹² FLOP/s).
- **Ancho de banda de memoria** `B`: bytes por segundo que se pueden leer o escribir en la
  VRAM. Se mide en GB/s.

Para un cálculo que mueve `W` bytes y hace `F` FLOP, la **intensidad aritmética** es
`I = F / W`, en FLOP por byte. El modelo *roofline* dice que el rendimiento alcanzable es:

:::formula
R ≤ min( P , I · B )
:::

- `R` — rendimiento efectivo, en FLOP/s.
- `P` — pico de cálculo del chip (TFLOPS).
- `I` — intensidad aritmética del cálculo (FLOP/byte).
- `B` — ancho de banda de memoria (bytes/s).
- `I · B` — techo impuesto por la memoria; si está por debajo de `P`, el cálculo está
  **limitado por memoria** (*memory bound*) y añadir núcleos no ayuda.

**Cuánta memoria ocupa un entrenamiento.** Con `N` parámetros y el optimizador Adam en
precisión simple (float32, 4 bytes por número), la regla de contabilidad es:

| Concepto | Bytes por parámetro |
| --- | --- |
| Pesos | 4 |
| Gradientes | 4 |
| Media móvil de Adam | 4 |
| Varianza móvil de Adam | 4 |
| Total | 16 |

A eso hay que sumar las **activaciones**: todo lo que la pasada hacia delante guarda para poder
calcular el gradiente en la pasada hacia atrás. Crecen con el tamaño del lote, así que son lo
primero que se queda sin sitio cuando subes el lote.

**Precisión.** Un número en coma flotante se guarda con un signo, un exponente y una mantisa.
Menos bits de mantisa significa menos precisión pero la mitad de bytes:

- **float32**: 1 bit de signo, 8 de exponente, 23 de mantisa. El estándar de referencia.
- **tf32**: 8 de exponente y 10 de mantisa. Formato interno de las matrices en GPUs recientes.
- **float16**: 5 de exponente, 10 de mantisa. Rápido, pero su rango es estrecho y desborda.
- **bfloat16**: 8 de exponente, 7 de mantisa. Mismo rango que float32, menos precisión fina.

**Acumulación de gradiente.** Si divides el lote en `k` micro-lotes y acumulas sus gradientes
antes de actualizar los pesos, el gradiente que aplicas es el del lote efectivo:

:::formula
g = (1/k) · Σᵢ gᵢ ,  lote_efectivo = k · lote_micro
:::

donde `gᵢ` es el gradiente calculado con el micro-lote `i`. El resultado matemático es el del
lote grande; el precio es que el paso se da `k` veces menos a menudo.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `R` | rendimiento efectivo que se consigue | FLOP/s (TFLOPS) | No es un mando, es el resultado: sale de `min(P, I·B)`. Si sube, es que has acercado la intensidad a la cresta o has reducido los bytes que hay que mover |
| `P` | pico de cálculo del chip | FLOP/s (TFLOPS) | Sube el tramo horizontal del roofline. Si el cálculo está limitado por memoria, más pico no cambia nada: la línea que manda es `I·B` |
| `B` | ancho de banda de la VRAM | bytes/s (GB/s) | Sube la pendiente del roofline: con la misma intensidad se alcanza más rendimiento. Es la palanca más directa para todo lo que está limitado por memoria |
| `I` | intensidad aritmética: FLOP por byte movido | FLOP/byte | Es la variable que de verdad se controla desde el código. Al subir (lote más grande, más cálculo por dato leído) el punto se acerca a la cresta y el rendimiento sube hasta `P`; al bajarlo, los núcleos esperan datos |
| `F` | FLOP del cálculo | FLOP | En una capa lineal es `2 · lote · entradas · salidas`, así que crece con el lote. Al subirlo sin mover más bytes, la intensidad mejora y con ella el rendimiento |
| `W` | bytes que hay que mover | bytes | Los pesos se leen enteros haga el lote que haga: al subir `W` sin subir `F`, la intensidad cae y el cálculo pasa a estar limitado por memoria. Bajar la precisión reduce `W` a la mitad |
| `N` | número de parámetros del modelo | parámetros | Con Adam en float32 cuesta 16 bytes por parámetro entre pesos, gradientes y los dos momentos. Al subir, el coste fijo de memoria crece linealmente antes de contar activaciones |
| `k` | número de micro-lotes de la acumulación de gradiente | micro-lotes | Sube el lote efectivo (`k · lote_micro`) sin subir la memoria, pero el paso se da `k` veces menos a menudo: al subir, cada época tarda más aunque el gradiente sea mejor |
| `gᵢ` | gradiente del micro-lote `i` | las de `g` | Se **suman** en `.grad` y luego se dividen entre `k`. Si te olvidas de dividir, el gradiente efectivo es `k` veces mayor y el paso del optimizador también |
| `lote_micro` | ejemplos de cada micro-lote | ejemplos | Al subirlo con `k` fijo, el lote efectivo crece. Es lo que se baja para que el micro-lote quepa en la VRAM, y lo que decide si el paso se da o revienta por memoria |
:::

## Ejemplo

Una capa lineal que recibe un lote de 64 vectores de 1024 números y produce 4096 salidas. Su
coste y su tráfico de memoria:

- FLOP: 2 · 64 · 1024 · 4096 = 536.870.912 ≈ **0,537 GFLOP** (el 2 es una multiplicación y
  una suma por cada elemento).
- Bytes de pesos: 1024 · 4096 · 4 = 16.777.216 bytes = **16 MiB** en float32.
- Intensidad: 536.870.912 / 16.777.216 = **32 FLOP por byte**.

Con esa intensidad el cálculo domina y la GPU se aprovecha. Ahora la misma capa con **lote de
1**: los FLOP bajan a 8.388.608 pero los pesos que hay que leer son exactamente los mismos
16 MiB, así que la intensidad cae a **0,5 FLOP/byte**. Si tu ancho de banda es de 1 TB/s y tu
pico de cálculo de 30 TFLOPS, el techo por memoria es 0,5 · 1000 = 500 GFLOP/s, es decir el
**1,7 %** del pico. Has pagado una GPU entera para usarla como si fuera un portátil.

Memoria, en el mismo ejemplo: un modelo de 1 millón de parámetros con Adam en float32 gasta
1.000.000 · 16 = **16 MB** solo en pesos, gradientes y estado del optimizador. Con 100 millones
de parámetros son **1,6 GB** antes de contar activaciones.

:::figura
fichero: gpu-y-rendimiento-roofline-y-memoria
pie: El panel izquierdo es el modelo roofline con los números del ejemplo: 30 TFLOPS de pico y 1 TB/s de ancho de banda. La línea morada es el techo alcanzable, min(P, I·B), y la cresta cae en I = P/B = 30 FLOP por byte. Los dos puntos son la misma capa del texto. Con lote de 1 la intensidad es 0,5 FLOP/byte, el techo lo pone la memoria y el chip entrega 500 GFLOP/s: el 1,7 % de lo que podría dar. Con lote de 64 la intensidad es 32 FLOP/byte, justo en la cresta, y el cálculo pasa a mandar. La lección es que el tamaño del lote no es una comodidad: mueve el punto de trabajo de la GPU por dos órdenes de magnitud sin tocar ni una capa del modelo. El panel derecho explica de qué se llena la memoria. La banda azul de abajo es el coste fijo —pesos, gradientes y los dos momentos de Adam, 16 bytes por parámetro, 1,6 GB para 100 millones de parámetros— y la naranja son las activaciones, que crecen de forma lineal con el lote. La línea roja marca los 12 GB de una GPU corriente: con esta cuenta el lote no pasa de 115. Y como el coste fijo no se puede bajar sin cambiar de optimizador o de precisión, la palanca real es el lote y la precisión, no el número de capas.
fuente: figuras/gpu-y-rendimiento-1.py
:::

## Código

```python verificable
# Cuentas de pizarra: el tamano del lote decide si el nucleo calcula o espera.
B, D_in, D_out = 64, 1024, 4096
flops = 2 * B * D_in * D_out
bytes_pesos = D_in * D_out * 4                # float32: 4 bytes por parametro

print(f"FLOPs           {flops / 1e9:.3f} GFLOP")            # -> 0.537 GFLOP
# 2**20 vale 1048576: esto son MiB (potencias de 1024) y no MB (potencias de 1000)
print(f"pesos          {bytes_pesos / 2**20:.1f} MiB")       # -> 16.0 MiB
print(f"intensidad     {flops / bytes_pesos:.1f} FLOP/byte")  # -> 32.0 FLOP/byte

# Con lote de 1 se leen los mismos pesos y se hace 64 veces menos calculo.
print(f"lote  1: {2 * 1 * D_in * D_out / bytes_pesos:.2f} FLOP/byte")   # -> 0.50 FLOP/byte
print(f"lote 64: {2 * 64 * D_in * D_out / bytes_pesos:.2f} FLOP/byte")  # -> 32.00 FLOP/byte
```

:::claves
- `bytes_pesos / 2**20` convierte a **MiB**, potencias de 1024: 16.777.216 bytes son 16,0 MiB y
  16,8 MB. En memorias y ficheros las dos unidades se mezclan todo el rato, y ese 5 % de
  diferencia decide si un lote cabe o no cabe.
- En la misma línea convive `flops / 1e9`, que sí es una potencia de 1000: los GFLOP se cuentan en
  base decimal y los MiB en base 1024. La mezcla es la convención del sector, no un descuido, pero
  conviene saber que está ahí.
- El `2` de `2 * B * D_in * D_out` es una multiplicación **y** una suma por cada elemento de la
  salida. Si se te olvida, la intensidad sale la mitad y la conclusión sobre el lote se invierte.
- `D_in * D_out * 4`: ese `4` son los bytes de un `float32`. En bfloat16 serían 2 y la intensidad
  se doblaría, así que si cambias la precisión tienes que cambiar también esta cuenta. Está
  escrito a mano y no lo deduce nadie por ti.
- Este bloque no importa NumPy: `D_in`, `D_out` y `B` son enteros de Python y las divisiones
  devuelven `float`. En Python 3 `/` siempre da `float` (para la división entera está `//`), así
  que `flops / 1e9` no pierde los decimales por el camino.
- La segunda parte repite la fórmula con `2 * 1 * ...` y `2 * 64 * ...` en lugar de llamar a una
  función. Está así a propósito: se ve de un vistazo que lo único que cambia es el lote y que los
  bytes leídos por los núcleos son exactamente los mismos en los dos casos.
:::

```python verificable
import numpy as np

# Acumular gradientes: la suma dividida entre los pasos da el gradiente del lote grande.
micro, acumulacion = 8, 4
print("lote efectivo:", micro * acumulacion)          # -> 32

deltas = [np.array([1.0, 3.0]), np.array([3.0, 5.0]),
          np.array([2.0, 2.0]), np.array([2.0, 2.0])]
# sum() arranca en el entero 0 y va sumando arrays uno a uno: el resultado es un array nuevo
medio = sum(deltas) / len(deltas)
print("gradiente medio:", medio.round(2).tolist())     # -> [2.0, 3.0]
print("suma sin dividir:", sum(deltas).round(2).tolist())  # -> [8.0, 12.0]
```

```python ilustrativo
import torch

modelo = Modelo().cuda()
optimizador = torch.optim.AdamW(modelo.parameters(), lr=3e-4)
# float16 tiene 10 bits de mantisa y desborda: hay que escalar la perdida para el backward.
escalador = torch.cuda.amp.GradScaler()

for x, y in cargador:                                  # cargador con pin_memory=True
    optimizador.zero_grad(set_to_none=True)
    with torch.cuda.amp.autocast(dtype=torch.float16):
        perdida = criterio(modelo(x.cuda(non_blocking=True)), y.cuda(non_blocking=True))
    escalador.scale(perdida).backward()
    escalador.step(optimizador)                        # solo actualiza si no hay inf/nan
    escalador.update()

torch.cuda.synchronize()   # obligatorio antes de medir: el lanzamiento es asincrono
```

## Errores típicos

- **Medir tiempos sin sincronizar.** Las llamadas a CUDA se encolan y devuelven el control al
  instante. Si cronometras alrededor de `modelo(x)` sin `torch.cuda.synchronize()`, estás
  midiendo lo que tarda en *encolar* el trabajo, no en hacerlo, y el resultado sale ridículo.
  Cronometra con eventos de CUDA o sincroniza antes de parar el reloj.
- **Subir el lote y no tocar la tasa de aprendizaje.** Con el doble de lote hay la mitad de
  pasos por época. La regla habitual es escalar la tasa con el lote, pero es una heurística:
  verifica que la pérdida de validación no empeora en vez de darla por buena.
- **Confundir acumulación de gradiente con un lote grande cuando hay normalización por lotes.**
  La matemática del gradiente es la misma, pero [[normalizacion-por-lotes|BatchNorm]] calcula
  sus estadísticas por micro-lote, así que ve lotes de 8 y no de 32. Usa LayerNorm/GroupNorm o
  sincroniza las estadísticas entre dispositivos.
- **Usar float16 sin escalado de pérdida.** Con 5 bits de exponente, los gradientes pequeños se
  van a cero y aparecen NaN a las pocas iteraciones. O escalas la pérdida (como en el ejemplo),
  o usas bfloat16, que tiene el rango de float32.
- **Culpar a la GPU cuando el cuello de botella es el cargador de datos.** Si el `DataLoader` no
  usa `num_workers` ni `pin_memory`, la GPU pasa el rato esperando lotes. Compruébalo midiendo
  la utilización: si está baja y la CPU al 100 %, el problema no es el modelo.
- **Ignorar la memoria de activaciones al elegir el lote.** Los pesos y el optimizador son un
  coste fijo, pero las activaciones crecen de forma lineal con el lote. Un lote que cabe con
  5 capas no cabe con 50.

:::practica
enunciado: Un modelo de 7 millones de parámetros se entrena con Adam en float32 y las activaciones de un lote ocupan 1,5 GB. ¿Cuánta memoria gastan pesos, gradientes y estado del optimizador, y cabe el entrenamiento en una GPU de 12 GB?
pista: Adam en float32 guarda 16 bytes por parámetro entre pesos, gradientes y sus dos momentos.
solucion: 7.000.000 · 16 = 112.000.000 bytes = 112 MB, unos 0,11 GB. Sumando 1,5 GB de activaciones, el total ronda 1,61 GB, muy por debajo de los 12 GB. El margen no lo decide el modelo sino el lote: pesos y optimizador son un coste fijo y las activaciones crecen con él.
:::

## Comprueba que lo sabes

:::quiz
p: Una capa hace 0,5 FLOP por byte y tu GPU tiene 30 TFLOPS de pico y 1 TB/s de ancho de banda. ¿Qué esperas?
o: Unos 30 TFLOPS, porque el pico de cálculo es el límite
o: Unos 0,5 TFLOPS, porque el techo lo pone la memoria que hay que leer
o: Depende solo del número de núcleos de la GPU
a: 2
e: El modelo roofline da min(P, I·B) = min(30, 0,5 · 1) = 0,5 TFLOPS. La intensidad es tan baja que cada byte leído solo alimenta media operación: los núcleos se pasan el tiempo esperando. Añadir núcleos no mueve ese techo; lo que lo mueve es aumentar el lote o reducir los bytes por número.
:::

:::quiz
p: ¿Qué consigues exactamente con acumulación de gradiente de 4 pasos y micro-lote de 8?
o: Que el modelo entrene cuatro veces más rápido
o: El gradiente de un lote efectivo de 32, dando un paso de actualización cada 4 micro-lotes
o: Cuatro actualizaciones de pesos por cada micro-lote
a: 2
e: Se suman los gradientes de los 4 micro-lotes y se dividen entre 4, así que el resultado es el gradiente medio de 32 ejemplos. El precio es que se actualizan los pesos 4 veces menos a menudo, no que vaya más rápido. Se usa cuando el lote de 32 no cabe en memoria.
:::

:::trampa
Si tu GPU está al 30 % de utilización, no compres otra: mide. Los tres sospechosos habituales
son el cargador de datos (poca CPU, sin `num_workers`), las operaciones diminutas encadenadas
(la latencia de lanzar cada núcleo domina) y las sincronizaciones escondidas (imprimir la
pérdida en cada paso, mover tensores a la CPU para mirarlos, `.item()` dentro del bucle).
:::
