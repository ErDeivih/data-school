---
id: exportar-y-servir-modelos
titulo: Exportar y servir modelos
fase: 7
nivel: avanzado
rutas: [ds, de]
prerequisitos: [pytorch-fundamentos, gpu-y-rendimiento, cuantizacion-y-destilacion]
tags: [onnx, despliegue, torchscript, inferencia, batching]
resumen: Pasar un modelo entrenado a algo que corre fuera de tu portátil: ONNX, TorchScript, torch.compile y por qué el exportado da números parecidos pero no idénticos.
fuentes: ["PyTorch (2024), 'torch.export and ONNX documentation'", "ONNX (2024), 'ONNX Runtime: Execution Providers'"]
---

## En una frase

Exportar es convertir el `nn.Module` que entrenaste en un **artefacto que corre sin Python y sin
tu código**: un grafo con los pesos dentro; y el resultado da números **casi** idénticos, no
idénticos, porque el motor que lo ejecuta suma en otro orden y redondea de otra forma.

## La idea

Mientras entrenas, tu modelo vive dentro de un programa de Python: un `nn.Module` con sus capas,
un `forward` que se ejecuta paso a paso y un montón de decisiones que se toman en tiempo de
ejecución. Eso está muy bien para investigar y no sirve para servir. Cuando el modelo tiene que
atender peticiones, se necesitan tres cosas que Python puro no da:

- **Un formato que otro programa pueda leer.** Un servidor escrito en C++, Go o Rust no puede
  importar tu clase de Python. Necesita un fichero con la estructura del cálculo y los pesos
  dentro. De eso se encargan **ONNX** (el grafo como estándar abierto) y **TorchScript** (la
  versión serializada de PyTorch).
- **Que no haya Python en el camino caliente.** Cada petición que pasa por el intérprete paga el
  coste por operación: construir tensores, comprobar tipos, lanzar el kernel. Con el grafo ya
  compilado, el motor encadena los kernels sin volver a Python.
- **Rendimiento.** Hay dos vías y conviene no confundirlas. `torch.compile` **no exporta nada**:
  reescribe tu modelo en el sitio para que corra más rápido dentro de PyTorch, fusionando
  operaciones (una convolución, su normalización por lotes y su ReLU se convierten en un solo
  kernel). La exportación, en cambio, produce un artefacto que puedes copiar a otra máquina y
  ejecutar con otro motor.

Y aquí llega la parte que sorprende la primera vez: validas el exportado contra el original y los
números **no coinciden**. No es un error tuyo ni un fallo del motor, es la aritmética de coma
flotante. En float32 solo hay 24 bits de mantisa, así que cada suma redondea, y el resultado
depende del orden: si el motor nuevo agrupa los sumandos de otra forma, aterriza en un valor
ligeramente distinto. Con miles de millones de operaciones, esa diferencia llega a la quinta o
sexta cifra significativa y ya no se puede ignorar. De ahí salen tres consecuencias prácticas:

1. **Compara con tolerancia, nunca con igualdad.** `torch.equal` y `np.array_equal` van a fallar.
   La validación se escribe con `np.allclose(a, b, rtol=1e-4, atol=1e-5)` y con el margen que
   aguante tu métrica, no con el que te gustaría.
2. **Valida con datos de verdad**, no con un tensor de ceros: con todo a cero las dos versiones
   coinciden y la prueba no demuestra nada.
3. **Si la diferencia es grande, no es redondeo.** Un 1e-6 relativo es aritmética; un 5 % es un
   error de exportación (una capa fuera, un `training=True` colado, una operación no soportada
   sustituida por una aproximación).

## Definición formal

Sea `f` el modelo original y `g` el modelo exportado, con los **mismos pesos** `W`. La validación
de un export es la comprobación de que, para toda entrada `x` del dominio:

:::formula
‖ f(x) − g(x) ‖ ≤ atol + rtol · ‖ f(x) ‖        y        forma(g(x)) = forma(f(x))
:::

- `f(x)`, `g(x)` — las salidas del modelo original y del exportado, con los mismos pesos.
- `atol` — tolerancia absoluta: el error que aceptas cuando la salida vale casi cero.
- `rtol` — tolerancia relativa: el error que aceptas en proporción al tamaño de la salida.
- La segunda condición no es opcional: un export que devuelve la misma forma pero las
  probabilidades sin normalizar pasaría una comparación de formas y fallaría todas las métricas.

De dónde sale esa diferencia. El error de redondear en una suma de `n` términos en precisión `p`
crece, en el peor caso, como:

:::formula
error ≈ Σ ( n · u · Σ |x_i| )        con u = 2^(−p)        y u ≈ 1,19 · 10⁻⁷ en float32
:::

- `n` — número de sumandos de la reducción (la dimensión que se contrae en un producto escalar).
- `u` — la unidad de redondeo de la precisión: media unidad en el último bit. En float32 vale
  1,19 · 10⁻⁷ cerca de 1,0; en float16, 9,77 · 10⁻⁴; en bfloat16, 7,81 · 10⁻³.
- `Σ |x_i|` — la suma de los valores absolutos: los positivos y los negativos **no** se cancelan
  para este cálculo. Una reducción con valores grandes del signo contrario es donde más duele.
- El `n` de delante es el motivo de que un modelo profundo derive más que uno superficial: no es
  una suma, son cientos encadenadas.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `atol` | Tolerancia absoluta de la comparación | unidades de la salida | Al subir, más exports pasan la prueba y más errores reales se cuelan. Se elige mirando la escala de la salida: si tus logits van de −5 a 5, un `atol` de 1 no valida nada |
| `rtol` | Tolerancia relativa, en proporción a la salida | adimensional | Es la que manda en salidas grandes. Con `rtol=1e-4` aceptas hasta 1 parte en 10.000, que es lo razonable para float32 y lo que aguanta casi cualquier métrica |
| `u` | Unidad de redondeo de la precisión: media unidad del último bit | adimensional | Es la causa de todo. Pasar de float32 a float16 la multiplica por 8.000; de ahí que un export a media precisión necesite tolerancias mucho más anchas |
| `n` | Sumandos que se contraen en cada reducción | elementos | Es la dimensión de la capa (4.096 en el ejemplo) y crece con el tamaño del modelo. El error de la reducción es proporcional a `n·u`, así que duplicar la capa duplica el error de cada suma |
| `Σ abs(x_i)` | Suma de los valores absolutos que se están sumando | unidades del producto | Es el verdadero tamaño del problema: si tienes valores de +1.000 y −1.000 que casi se cancelan, el resultado es pequeño pero el error se calculó sobre los 1.000 |
| `p` | Bits de mantisa de la precisión usada | bits | Más bits es menos error: float32 tiene 24, float16 tiene 11 y bfloat16 tiene 8. Menos bits es menos memoria y menos tiempo, y esa es toda la negociación |
:::

## Ejemplo

Un clasificador con una primera capa lineal de 4.096 entradas y 64 salidas. La cuenta por cada una
de las 64 salidas es un producto escalar de 4.096 términos. Los pesos y la entrada están en
float32, así que cada producto y cada suma redondea a 24 bits de mantisa.

Ejecutando esa misma cuenta con dos órdenes de suma distintos (el script imprime los valores):

```
n=1024    secuencial=-83.3684998   por parejas=-83.3685760   error 9,1e-07
n=4096    secuencial= +2.0263340   por parejas= +2.0263424   error 4,1e-06
n=16384   secuencial=+40.7600327   por parejas=+40.7601547   error 3,0e-06
n=65536   secuencial=+154.4001923  por parejas=+154.4004517  error 1,7e-06
```

El error relativo se queda entre `10⁻⁷` y `10⁻⁶` en todos los tamaños: **no crece sin límite**, se
estabiliza en el orden de la unidad de redondeo acumulada de la reducción. Ese es el mismo orden
que vas a ver al comparar el modelo de PyTorch con el exportado, y es la razón por la que la
validación se escribe con `rtol=1e-4`: dos órdenes de magnitud de margen sobre lo que la
aritmética justifica.

El segundo efecto, y el que rompe despliegues, es el **batching**. Un servidor agrupa peticiones
para aprovechar la GPU, y agrupar no es solo una decisión de rendimiento: cambia los números. El
mismo producto escalar, calculado dentro de un lote de 64 filas o fila a fila, no da el mismo
resultado en float32, porque el motor elige otro algoritmo según el tamaño del problema:

```text
diferencia maxima entre el lote entero y fila a fila   1.19e-06
forma con lote 1   (1, 32)
forma con lote 64  (64, 32)
```

Ese `1,19 · 10⁻⁶` es **diez unidades de redondeo** de float32 cerca de 1,0: el propio lote es una
fuente de variación del mismo orden que el cambio de motor. Y la forma de la salida también
cambia, `(1, 32)` frente a `(64, 32)`: un servidor que dé por hecha la forma del lote 1 se rompe
con el primer lote de verdad. De ahí, dos reglas:

- **Valida con el mismo tamaño de lote que vas a servir.** Validar con lote 1 y servir con lote 64
  no es validar lo que sirves: es validar otro cálculo.
- **El batching es la palanca grande de la factura de inferencia**, muy por delante de optimizar
  el kernel: cada petición suelta paga un coste fijo de lanzamiento de kernel que no depende del
  tamaño. La curva se aplana al llegar al ancho de banda de memoria, que es el techo real.

:::figura
fichero: exportar-servir-acumulacion-y-precision
pie: Arriba, el error relativo de la misma suma en float32 al cambiar el orden: se queda entre 10⁻⁷ y 10⁻⁵, sin crecer con el número de sumandos más allá del orden de la unidad de redondeo. Ese es el tamaño real de la diferencia entre el modelo que entrenas y el que exportas, y por eso se valida con `rtol=1e-4` y no con igualdad. Abajo, el precio de bajar la precisión al guardar los pesos: float16 deja un error del 0,021 % sobre la desviación de los pesos, int8 sube al 1,04 % e int4 se dispara al 18,9 %; int3 llega al 44 %. La cuantización no es gratis: cada escalón que baja quita memoria y ancho de banda, y añade error que hay que compensar con escala por canal o con calibración.
fuente: figuras/exportar-y-servir-modelos-1.py
:::

## Código

```python verificable
import numpy as np

# Dos formas de calcular el MISMO producto escalar en float32: sumando en orden, uno a uno, o
# dejando que NumPy lo haga por parejas. Es lo que cambia entre dos motores de inferencia.
def suma_secuencial(x):
    total = np.float32(0.0)
    for v in x:
        total = np.float32(total + v)      # cada suma redondea a 24 bits de mantisa
    return float(total)

rng = np.random.default_rng(0)
for n in (1024, 4096, 16384):
    a = rng.normal(0, 1, n).astype(np.float32)
    b = rng.normal(0, 1, n).astype(np.float32)
    secuencial = suma_secuencial(a * b)
    por_parejas = float(np.dot(a, b))
    rel = abs(secuencial - por_parejas) / abs(por_parejas)
    print(f"n={n:6d}  secuencial={secuencial:+.7f}  numpy={por_parejas:+.7f}  error={rel:.2e}")
# -> n=  1024  secuencial=-83.3684998  numpy=-83.3685760  error=9.15e-07
# -> n=  4096  secuencial=+2.0263340  numpy=+2.0263424  error=4.12e-06
# -> n= 16384  secuencial=+40.7600327  numpy=+40.7601547  error=2.99e-06

# La unidad de redondeo NO es la misma en todo el rango: crece con el tamano del numero.
for v in (1.0, 1000.0, 1e6):
    print(v, float(np.spacing(np.float32(v))))
# -> 1.0 1.1920928955078125e-07
# -> 1000.0 6.103515625e-05
# -> 1000000.0 0.0625

# Validar un export: con igualdad falla, con tolerancia pasa.
referencia = rng.normal(0, 1, 5)
exportado = referencia + rng.normal(0, 1e-5, 5)
print(np.array_equal(referencia, exportado))                      # -> False
print(np.allclose(referencia, exportado, rtol=1e-4, atol=1e-5))   # -> True
```

:::claves
- `np.float32(total + v)` está escrito a propósito: sin envolver el resultado, NumPy promociona el acumulador a float64 y el ejemplo **deja de medir lo que dice medir**. La precisión del acumulador es la mitad del asunto.
- `np.spacing(x)` devuelve la distancia al siguiente número representable: el tamaño real de un paso. Cerca de 1,0 es `1,19e-07`, pero cerca de un millón es `0,0625`. Por eso el error de una reducción no depende solo de `n`, sino del **tamaño de los sumandos intermedios**: ahí es donde se pierden los bits.
- `np.dot` **no suma en orden**: NumPy usa suma por parejas (y BLAS debajo), que agrupa los términos en un árbol. El resultado es más preciso que la suma secuencial, y también distinto. Esa es exactamente la situación de un modelo exportado: mismo cálculo, otro orden.
- `np.array_equal` exige igualdad bit a bit y va a devolver `False` casi siempre. `np.allclose` combina las dos tolerancias: pasa si `abs(a−b) <= atol + rtol·abs(b)`. Con `atol` sola, las salidas grandes fallan; con `rtol` sola, las salidas cercanas a cero fallan.
- El error relativo **no crece con `n`** en estos números: se queda entre `10⁻⁷` y `10⁻⁶`. Es la firma del error de redondeo aleatorio, que crece como la raíz de `n`, y no del error sistemático, que crecería como `n`. Si tu diferencia crece de forma lineal con las capas, tienes un fallo de exportación, no aritmética.
- `rng.normal(0, 1e-5, 5)` simula el ruido de un export; con semilla fija el bloque es reproducible. Sin semilla, el `array_equal` seguiría dando `False` pero el `allclose` podría fallar por azar.
:::

```python verificable
import numpy as np

# Cuantizar al exportar: el mismo bloque de pesos guardado con menos bits.
rng = np.random.default_rng(0)
W = rng.normal(0.0, 0.05, size=(128, 128))


def reconstruir(W, bits):
    """Cuantizacion simetrica por tensor, como la de un export a int8 o int4."""
    qmax = 2 ** (bits - 1) - 1
    escala = np.abs(W).max() / qmax            # la escala la fija el peso mas extremo
    return np.clip(np.round(W / escala), -qmax - 1, qmax) * escala


def error_relativo(reconstruido):
    return float(np.sqrt(((W - reconstruido) ** 2).mean()) / W.std())


print(f"float32 sin tocar       {error_relativo(W.astype(np.float32).astype(np.float64)):.6f}")
# -> 0.000000
print(f"float16                 {error_relativo(W.astype(np.float16).astype(np.float64)):.6f}")
# -> 0.000208
print(f"int8                    {error_relativo(reconstruir(W, 8)):.6f}")   # -> 0.009173
print(f"int4                    {error_relativo(reconstruir(W, 4)):.6f}")   # -> 0.166905
print(f"int3                    {error_relativo(reconstruir(W, 3)):.6f}")   # -> 0.390986

# El tamano del fichero si es lo unico que miras: 131 KB en float64, 65 KB en float32.
print(W.nbytes)                                # -> 131072
print(W.astype(np.float32).nbytes)             # -> 65536
```

:::claves
- La primera línea imprime el error de convertir a float32 y volver, que es **cero**: float32 tiene 24 bits de mantisa y los pesos del ejemplo vienen de un `float64` que cabe exactamente. Sirve de control: si esa línea no diera 0, el problema estaría en la conversión, no en la cuantización.
- `W.astype(np.float16).astype(np.float64)` vuelve a float64 para poder medir el error: si restas un array float16 de uno float64, NumPy promociona y el resultado sale igual, pero el `dtype` del intermedio es lo que quieres controlar.
- El error de int8 (0,9 % aquí, 1,04 % en la figura) es **menor** que el de int4 (16,7 % y 18,9 %) por una razón aritmética, no de gusto: los niveles positivos pasan de 127 a 7, así que la escala se multiplica por 18 y con ella el error de cada peso. Es la misma cuenta que en [[cuantizacion-y-destilacion|cuantización]]. Los dos números no coinciden exactamente porque el generador aleatorio se ha llamado antes en el script de la figura y los pesos salen distintos: el orden de magnitud es lo que se retiene, no la tercera cifra.
- `W.nbytes` cuenta **bytes de memoria**, no caracteres del fichero: pasar de float64 a float32 divide el peso por dos, y a int8 por ocho. Es la palanca que decide si el modelo cabe en la GPU que tienes, mucho antes que cualquier optimización de kernel.
- El error se divide entre `W.std()` para que sea comparable entre capas: una capa con pesos grandes tendría un error absoluto grande sin ser peor. Un 16,7 % aquí significa «el error pesa un 16,7 % de lo que se desvían los pesos», no «el modelo falla el 17 % de las veces».
- Esta cuantización es **solo de pesos** y sin calibrar. Cuantizar también las activaciones exige un conjunto de datos representativo que fije los rangos, y ahí sí que aparece una pérdida de precisión medible en la métrica.
- Fíjate en que `reconstruir` no toca `W`: devuelve un array nuevo. `np.round` y la multiplicación crean copias, así que puedes medir el error después sin haber perdido los pesos originales.
:::

```python ilustrativo
# El esqueleto de un export real. Necesita torch, onnx y onnxruntime instalados, y por eso va
# como ilustrativo: aqui no se ejecuta.
import numpy as np
import torch
import torch.nn as nn

modelo = nn.Sequential(nn.Linear(64, 128), nn.ReLU(), nn.Linear(128, 3)).eval()

# 1) Un tensor de ejemplo con la FORMA correcta. Los nombres de las dimensiones dinamicas
#    (batch) se declaran aparte: si los fijas, el modelo exportado solo acepta ese lote.
ejemplo = torch.randn(1, 64)

# 2) Exportar a ONNX. dynamic_axes es lo que permite servir lotes de distinto tamano.
torch.onnx.export(
    modelo, ejemplo, "modelo.onnx",
    input_names=["entrada"], output_names=["logits"],
    dynamic_axes={"entrada": {0: "lote"}, "logits": {0: "lote"}},
    opset_version=17,
)

# 3) Servir y VALIDAR con tolerancia, no con igualdad.
import onnxruntime as ort

sesion = ort.InferenceSession("modelo.onnx", providers=["CUDAExecutionProvider"])
x = np.random.default_rng(0).normal(0, 1, (4, 64)).astype(np.float32)

with torch.no_grad():
    referencia = modelo(torch.from_numpy(x)).numpy()
exportado = sesion.run(None, {"entrada": x})[0]

# rtol y atol se eligen por la metrica que aguante el negocio, no por lo que te gustaria.
assert np.allclose(referencia, exportado, rtol=1e-4, atol=1e-5)
print(np.abs(referencia - exportado).max())      # tipicamente 1e-6 o menos

# 4) torch.compile NO exporta: acelera el mismo modelo dentro de PyTorch.
rapido = torch.compile(modelo)
with torch.no_grad():
    print(torch.allclose(modelo(torch.from_numpy(x)), rapido(torch.from_numpy(x)),
                         rtol=1e-4, atol=1e-5))
```

:::claves
- `modelo.eval()` no es decorativo: en modo entrenamiento, `Dropout` apaga neuronas al azar y `BatchNorm` usa las estadísticas del lote. Un export hecho sin `.eval()` produce un grafo **estocástico**, y la validación fallará de forma intermitente, que es el peor fallo posible de diagnosticar.
- `dynamic_axes` con la dimensión 0 como `"lote"` es lo que permite pasar lotes de distinto tamaño. Sin eso, el grafo queda clavado al lote del ejemplo (1) y en producción rechazará cualquier otro tamaño.
- `torch.no_grad()` no cambia los números: cambia la memoria. Sin él, PyTorch construye el grafo de gradientes para una pasada que no va a retropropagar nada, y con un lote grande eso es el doble de memoria para nada.
- `onnxruntime` no es el único motor y la elección importa: `CUDAExecutionProvider` ejecuta en GPU y `CPUExecutionProvider` en CPU. Los dos dan resultados ligeramente distintos entre sí, y los dos distintos de PyTorch. Valida contra **el que vas a usar en producción**, no contra el que tengas a mano.
- `assert np.allclose(...)` es una prueba, y con `python -O` los `assert` se desactivan: en un pipeline de despliegue de verdad esto va con `if not np.allclose(...): raise`, no con `assert`.
- `torch.compile(modelo)` devuelve un modelo **nuevo** y deja `modelo` intacto, pero comparte los pesos. Por eso los dos dan lo mismo con tolerancia: son el mismo modelo con dos planes de ejecución, no dos entrenamientos.
:::

## Errores típicos

- **Validar con igualdad.** `torch.equal(referencia, exportado)` devuelve `False` casi siempre, y
  no porque el export esté mal. Si tu modelo es un clasificador, lo que importa es que la clase
  ganadora no cambie, no que el logit coincida en la décima cifra.
- **Exportar sin `.eval()`.** En modo entrenamiento el grafo lleva `Dropout` y `BatchNorm` de
  entrenamiento, así que las salidas cambian entre pasadas. El fallo aparece como una validación
  que unas veces pasa y otras no, y se persigue durante días.
- **Probar solo con un lote de tamaño 1.** En producción el servidor agrupa peticiones: si
  validaste con lote 1 y sirves con lote 64, no has validado nada.
- **Dar por hecho que cuantizar es gratis.** El int4 del ejemplo tiene un error del 16,7 % sobre
  la desviación de los pesos. Hay modelos que aguantan y modelos que se degradan de golpe en la
  primera capa: cuantiza, mide y compara en el mismo conjunto de evaluación.
- **Confundir `torch.compile` con exportar.** `torch.compile` acelera el modelo **dentro** de
  PyTorch y sigue necesitando tu código: no produce ningún artefacto que puedas copiar a otro
  contenedor. Si no quieres el intérprete en el camino, necesitas ONNX o TorchScript.
- **Ignorar el arranque.** El primer `run()` de una sesión de ONNX Runtime compila kernels y
  reserva memoria: puede tardar segundos. En una función sin servidor eso se paga en cada arranque
  en frío y aparece como la latencia del primer usuario. Mide el *cold start* aparte.
- **Elegir la precisión por el tamaño del fichero.** Que el `.onnx` ocupe la mitad no significa que
  vaya el doble de rápido: si el hardware no tiene instrucciones nativas para ese formato, el
  motor descomprime antes de operar. Mide latencia en el hardware de destino.

:::trampa
El error de una comparación con `atol` mal elegido es asimétrico: si pones `atol=1e-2` en un
modelo cuyos logits van de −5 a 5, estás aceptando un 0,2 % de error... y también cualquier bug de
exportación que mueva la salida menos que eso. La tolerancia no es una red de seguridad: es un
contrato, y se elige mirando la sensibilidad de la métrica final, no la comodidad del test.
:::

## Comprueba que lo sabes

:::quiz
p: Validas el export y `np.allclose` devuelve `False` con una diferencia máxima de 3 · 10⁻⁷ en un logit de valor 2,0. ¿Qué conclusiones son razonables?
o: Que el export está roto y hay que volver a convertirlo
o: Que es el redondeo normal de float32 al cambiar el orden de las sumas, y hay que validar con tolerancia relativa
o: Que hay que reentrenar el modelo porque los pesos se han corrompido
a: 2
e: La unidad de redondeo de float32 cerca de 1,0 es 1,19 · 10⁻⁷, así que un error de 3 · 10⁻⁷ es de ese orden y no indica nada roto. El export conmuta operaciones y agrupa las reducciones de otra forma; el resultado es distinto en las últimas cifras por aritmética, no por un fallo. Se valida con `rtol` y `atol`, y se comprueba además que la clase ganadora o la métrica final no cambien.
:::

:::quiz
p: Sirves con lotes de 64 peticiones y validaste con lotes de 1. ¿Qué es lo más grave que puede pasar?
o: Nada: el resultado de cada petición es independiente del lote
o: Que no has validado la ruta real: el lote cambia cómo se organizan las reducciones y, si el export tiene un error de forma o de dimensión dinámica, solo aparece con lotes grandes
o: Que el modelo va más lento
a: 2
e: Dos motivos distintos. El aritmético: con lote 64 las reducciones se agrupan de otra forma, así que la salida no es bit a bit la del lote 1. El de ingeniería: un `dynamic_axes` mal declarado o una operación que no admite la dimensión dinámica solo falla con lotes que no sean el del ejemplo. La validación tiene que usar el mismo camino que producción.
:::

:::quiz
p: Pasas los pesos de float32 a int8 y el fichero ocupa la cuarta parte. ¿Qué NO puedes concluir?
o: Que el error de reconstrucción de los pesos es medible y hay que comprobarlo contra el original
o: Que la inferencia va a ser cuatro veces más rápida
o: Que hay que volver a evaluar la métrica del modelo
a: 2
e: El tamaño en disco no se traduce directamente en tiempo: el cuello de botella de la inferencia suele ser el ancho de banda de memoria, que sí mejora, pero si el hardware no tiene instrucciones para ese formato el motor descomprime antes de operar. Además, cuantizar cambia los números, así que la métrica se mide otra vez. El ahorro de memoria es lo único que está garantizado.
:::

:::practica
enunciado: Exportas un modelo y comparas 10.000 salidas. La diferencia máxima es 8 · 10⁻⁵, la salida típica vale 1,5 y solo 3 de las 10.000 cambian de clase ganadora, en casos donde el margen entre la primera y la segunda clase era menor que 10⁻³. ¿Aceptas el export? Razona la respuesta y decide qué tolerancias usarías.
pista: Compara el error con la unidad de redondeo de la precisión y con el margen que necesita la decisión, no con cero.
solucion: El error relativo es 8 · 10⁻⁵ / 1,5 ≈ 5 · 10⁻⁵, es decir unas 400 unidades de redondeo de float32 (1,19 · 10⁻⁷): está dentro de lo que justifica la aritmética al reordenar sumas, así que el export funciona. Las 3 discrepancias se dan en casos con margen menor que 10⁻³, y el error máximo (8 · 10⁻⁵) es diez veces menor que ese margen: no son empates que el ruido haya decidido, son casos que ya estaban al filo. La tolerancia razonable es `rtol=1e-4` y `atol=1e-5`, que cubre el error observado con dos órdenes de margen. Y lo que hay que comprobar de verdad no es el logit, sino la métrica del negocio: si esas 3 de 10.000 cambian la precisión global en menos de lo que importa, el export se acepta.
:::

:::nota
Este concepto cierra la fase de redes neuronales por el lado del despliegue, y conecta con
[[gpu-y-rendimiento|GPU y rendimiento]] por un lado —el cuello de botella suele ser memoria, no
cómputo— y con [[mlops-y-cicd-de-modelos|MLOps]] por el otro: el artefacto exportado es lo que se
versiona y se despliega, no el fichero de pesos del entrenamiento. En la fase 8, la misma cuenta
de utilización y coste reaparece con nombre propio en
[[economia-de-la-inferencia-propia|la economía de la inferencia propia]].
:::
