---
id: concurrencia-async-hilos-procesos
titulo: Concurrencia, asincronía, hilos y procesos
fase: 11
nivel: avanzado
rutas: [alg, de]
prerequisitos: [concurrencia-algoritmica, gestion-de-memoria, apis-y-peticiones-http]
tags: [python, rendimiento, gil, paralelismo]
resumen: Esperar a la red, repartir CPU y compartir memoria: qué resuelve cada modelo en Python y cuándo el GIL te deja sin nada.
fuentes: ["Python, 'concurrent.futures' y 'asyncio' (documentación oficial)", "Python, 'Thread State and the Global Interpreter Lock' (documentación oficial)"]
---

## En una frase

La asincronía sirve para esperar muchas cosas a la vez en un solo hilo, los hilos sirven para
trabajos que esperan —no para calcular— y los procesos sirven para calcular de verdad a cambio
de copiar datos y arrancar despacio.

## La idea

Imagina una cafetería. Un solo camarero que toma el pedido, espera a que la máquina termine y
sirve, toma el siguiente y espera otra vez: eso es un programa secuencial. El mismo camarero
que pone cinco cafés a la vez y va atendiendo al que se va completando es **asincronía**: no
trabaja más rápido, deja de estar parado.

Ahora añade dos camareros. Si el trabajo es esperar a la máquina, van más rápido. Si el trabajo
es moler café a mano (puro cálculo) y solo hay un molinillo, el segundo camarero espera su
turno: eso es lo que hace el **GIL** de Python, un candado que solo deja que un hilo ejecute
bytecode a la vez. Con hilos la cafetería no muele el doble de grano.

La solución para moler en paralelo es tener **otra cafetería** (otro proceso): cada uno con su
molinillo y su memoria. Más caro de montar y el café hay que llevarlo de una a otra, pero muele
de verdad en paralelo.

De ahí la regla:

- **Espera de entrada/salida (red, disco, base de datos): asincronía.** Miles de conexiones en
  un proceso con muy poca memoria.
- **Cálculo puro y datos pequeños: procesos.** Cada núcleo con su intérprete.
- **Trabajo bloqueante sin más (una biblioteca que no es asíncrona): hilos**, aceptando que solo
  dan servicio concurrente, no velocidad de CPU.

Y una cuarta opción que se olvida: **a veces no hay que paralelizar nada**. Si tu programa pasa
el 80 % del tiempo esperando la base de datos, la solución es una consulta mejor o una caché,
no doce procesos.

## Definición formal

**Concurrencia** es tener varias tareas en curso a la vez; **paralelismo** es ejecutarlas
literalmente en el mismo instante en núcleos distintos. La concurrencia es una propiedad del
diseño; el paralelismo, del hardware.

**GIL (Global Interpreter Lock).** Candado global que garantiza que un solo hilo ejecuta
bytecode de Python en cada momento. Consecuencias exactas:

- Los hilos **sí** se solapan cuando la operación libera el candado: esperas de red y de disco,
  `time.sleep`, y las operaciones de NumPy o de compresión que van a código C.
- Los hilos **no** se solapan en bucles de Python puro: dos hilos tardan lo mismo que uno.
- El GIL no hace atómica una secuencia de operaciones. `valor = valor + 1` son varios pasos y
  dos hilos pueden intercalarse, así que **necesitas un candado explícito**.

**Cálculo del tiempo esperado.** Con `W` el tiempo de trabajo efectivo y `T` el tiempo total:

:::formula
ganancia máxima = T / max(W_paralelizable / nucleos + W_serie, W_serie)
:::

Es la ley de Amdahl en su forma práctica: si el 20 % del trabajo es serie, ningún número de
núcleos baja de ese 20 %. Si tu tarea tarda 10 segundos y 2 son de lectura de fichero
irreducible, el suelo son 2 segundos aunque pongas 64 procesos.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `T` | Tiempo total del trabajo en un solo hilo, la línea base | segundos | La ganancia sube en la misma proporción: el paralelismo multiplica, no suma |
| `W_paralelizable` | Parte del trabajo que se puede repartir entre núcleos (bucles, tareas independientes) | segundos | La ganancia sube, pero se acerca al techo que impone la parte serie: nunca pasa de T / W_serie |
| `W_serie` | Parte que no se puede repartir: leer un fichero, arrancar procesos, agregar resultados | segundos | La ganancia baja y el techo se endurece: con W_serie = 2 s sobre 10 s, ningún núcleo baja de 5× |
| `nucleos` | Núcleos (o procesos) que reparten la parte paralelizable | cuentas | Al principio casi todo mejora y llega un punto en que no aporta nada: `W_paralelizable / nucleos` se vuelve despreciable frente a `W_serie` |
:::

**Asincronía en Python.** Una función `async def` devuelve una corrutina; `await` cede el
control al bucle hasta que la espera termina. El bucle de eventos gestiona miles de corrutinas
en un solo hilo. **Nada de esto sirve si dentro de la corrutina llamas a código bloqueante**:
un `requests.get` o un `time.sleep` congelan el bucle entero y con él todas las tareas.

**Los tres ejecutores de `concurrent.futures`:**

- `ThreadPoolExecutor`: hilos. Adecuado para esperas y para bibliotecas sincrónicas.
- `ProcessPoolExecutor`: procesos. Adecuado para cálculo. Los argumentos y resultados se
  serializan (pickle) y cada proceso arranca de cero: en Windows eso significa reimportar el
  módulo, y por eso el punto de entrada necesita `if __name__ == "__main__":`.
- `asyncio`: no es un ejecutor, es el bucle. Se combina con `run_in_executor` para lo bloqueante.

:::figura
fichero: concurrencia-modelos-y-techo
pie: A la izquierda, las tres tareas del ejemplo: arriba una tras otra (300 + 200 + 100 = 600 ms, las barras no se solapan) y abajo las tres a la vez (300 ms, lo que tarda la más lenta). La concurrencia no acelera ninguna tarea: elimina la espera de las demás. A la derecha, la ley de Amdahl con los números de la página: 10 s de trabajo con 2 s que no se pueden repartir. Con 4 núcleos ya se está en 2,5× y el techo es 5×, así que pasar de 16 a 64 núcleos apenas mueve la curva. Antes de añadir procesos, mira cuánto de tu trabajo es irreducible.
fuente: figuras/concurrencia-async-hilos-procesos-1.py
:::

**Candados.** `threading.Lock` garantiza exclusión mutua; `with candado:` lo suelta al salir,
incluso si hay excepción. Sobre datos compartidos entre procesos no hay candados que valgan:
cada proceso tiene su propia memoria, y compartir exige `multiprocessing.shared_memory`, colas o
un servicio externo.

## Ejemplo

Tres peticiones de red que tardan 300, 200 y 100 ms:

- **Secuencial:** 300 + 200 + 100 = 600 ms.
- **Con asyncio y `gather`:** 300 ms, porque las tres esperan a la vez. La aceleración es el
  cociente entre la suma y el máximo: 600 / 300 = 2.
- **Con hilos:** también unos 300 ms, porque las tres esperas sueltan el GIL. La diferencia con
  asincronía es el coste por tarea: cada hilo reserva su pila (del orden de megabytes de
  memoria virtual) y el cambio de contexto lo gestiona el sistema operativo; una corrutina ocupa
  kilobytes. Con 50 conexiones da igual; con 20.000, no.

Y ahora el caso contrario: sumar dos millones de raíces cuadradas en dos hilos no tarda la
mitad, tarda lo mismo o un poco más, porque el GIL serializa el bucle. Con dos procesos sí baja
(aunque no exactamente a la mitad, por el arranque y la copia de datos).

## Código

```python verificable
import asyncio
import time

async def descarga(nombre, segundos):
    # sleep de asyncio, NO time.sleep: cede el control al bucle y deja correr las demas tareas
    await asyncio.sleep(segundos)      # simula la espera de red, sin bloquear
    return f"{nombre} listo"

async def secuencial():
    inicio = time.perf_counter()               # reloj de pared: lo que espera una persona
    for nombre, segundos in [("a", 0.30), ("b", 0.20), ("c", 0.10)]:
        await descarga(nombre, segundos)       # una detras de otra: aqui si se espera cada una
    return time.perf_counter() - inicio

async def en_paralelo():
    inicio = time.perf_counter()
    # gather lanza las tres corrutinas y devuelve una lista con los resultados EN EL ORDEN
    # en que se pasaron, no en el orden en que terminan; tarda lo que la mas lenta.
    await asyncio.gather(descarga("a", 0.30), descarga("b", 0.20), descarga("c", 0.10))
    return time.perf_counter() - inicio

t_sec = asyncio.run(secuencial())      # asyncio.run arranca el bucle, ejecuta y lo cierra
t_par = asyncio.run(en_paralelo())     # dos run seguidos: un bucle nuevo para cada uno
print(f"una tras otra {t_sec:.2f} s")     # -> 0.60 s (suma de las esperas)
print(f"con gather    {t_par:.2f} s")     # -> 0.30 s (la mas lenta)
print("aceleracion:", round(t_sec / t_par, 1), "x")
```

:::claves
- `asyncio.run()` **arranca un bucle de eventos nuevo y lo cierra al terminar**. Por eso no se
  puede llamar dos veces a la vez ni desde dentro de una corrutina: cada llamada es un mundo
  aparte. En un programa real el bucle se crea una vez y las corrutinas se lanzan dentro.
- `await asyncio.sleep(0.3)` no duerme el programa: **devuelve el control al bucle**. Esa es la
  diferencia entera con `time.sleep(0.3)`, que bloquea el hilo y con él las otras tres tareas
  («a», «b» y «c» tardarían 0,6 s igual, pero con el bucle congelado y sin poder atender nada más).
- `asyncio.gather` devuelve los resultados **en el orden en que se pasaron los argumentos**, no
  en el orden en que terminaron, y por defecto **propaga la primera excepción y no cancela las
  demás tareas**: las otras siguen corriendo por detrás hasta que el bucle se cierra.
- `threading.Thread.join()` espera a que el hilo termine, pero **hay que llamarlo**: sin él, el
  programa sigue y mide o imprime antes de que los hilos hayan acabado. Y `start()` solo se puede
  llamar una vez por hilo: un `Thread` no se reutiliza, se crea otro.
- `sys.setswitchinterval(1e-6)` cambia cada cuánto el intérprete cede el turno entre hilos; está
  ahí **solo para que la carrera se vea casi siempre**. Con el valor por defecto (5 ms) el fallo
  aparece de vez en cuando y parece que el código funciona: los errores de concurrencia son
  intermitentes por naturaleza.
- `pool.map` es **perezoso**: sin envolverlo en `list()` no se ejecuta nada y el tiempo medido
  saldría casi cero. Y los resultados llegan en el orden de entrada, no en el de finalización,
  así que no sirve para saber qué proceso acabó antes.
- El array de NumPy del último bloque **no se comparte con los hijos**: `pickle` lo serializa,
  viaja por una tubería y el hijo lo reconstruye entero. Medido con `tracemalloc`, el pico de la
  copia es de unos 19 MiB para un array de 8 MB: más del doble, porque el array vive dos veces
  (original y reconstruido) más los bytes serializados. Para no duplicar datos hacen falta
  `shared_memory`, `mmap` o dejar que el hijo lea el fichero por su cuenta.
:::

```python verificable
import sys
import threading
import time

sys.setswitchinterval(1e-6)     # cambios de hilo frecuentes: la carrera se ve antes

class Contador:
    def __init__(self):
        self.valor = 0
        self.lock = threading.Lock()

    def sin_bloqueo(self):
        actual = self.valor            # leer
        # sleep(0) no cambia el valor: solo pide al sistema que cambie de hilo, y ahi se cuela
        time.sleep(0)                  # el hilo puede perder el turno justo aqui
        self.valor = actual + 1        # escribir: la suma del otro hilo se ha perdido

    def con_bloqueo(self):
        with self.lock:                # el candado se suelta al salir, aunque salte una excepcion
            actual = self.valor
            time.sleep(0)              # dentro del candado, nadie mas puede leer a medias
            self.valor = actual + 1

def lanzar(metodo, veces=500):
    for _ in range(veces // 4):                                       # 125 tandas de 4 hilos
        hilos = [threading.Thread(target=metodo) for _ in range(4)]   # hilos nuevos cada vez
        for h in hilos:
            h.start()                   # start arranca; no espera a que el hilo acabe
        for h in hilos:
            h.join()                    # join si espera: sin el, se contarian hilos a medias

contador = Contador()
lanzar(contador.sin_bloqueo)
print("esperado 500, conseguido:", contador.valor, "(carrera: se pierden sumas)")

contador = Contador()
lanzar(contador.con_bloqueo)
print("con bloqueo, conseguido:", contador.valor)     # -> 500
```

```python verificable
import os
import time
from concurrent.futures import ProcessPoolExecutor

def carga_cpu(n):
    total = 0
    for i in range(n):
        total += (i * i) % 997          # bucle de Python puro: aqui el GIL no deja solapar nada
    return total

if __name__ == "__main__":              # obligatorio en Windows: los hijos reimportan el modulo
    TRABAJOS = [1_000_000] * 4          # cuatro tareas identicas, una por nucleo

    inicio = time.perf_counter()
    # map devuelve un iterador perezoso: sin list() no se ejecutaria nada y el tiempo saldria 0
    list(map(carga_cpu, TRABAJOS))
    t_serie = time.perf_counter() - inicio

    inicio = time.perf_counter()
    # max_workers reparte las tareas entre procesos; el pool se cierra solo al salir del with
    with ProcessPoolExecutor(max_workers=4) as pool:
        # los resultados vuelven en el mismo orden en que se enviaron, no en el de llegada
        resultados = list(pool.map(carga_cpu, TRABAJOS))
    t_procesos = time.perf_counter() - inicio

    print("nucleos disponibles:", os.cpu_count())
    print("resultados:")
    for r in resultados:
        print("  ", r)
    print(f"en serie    {t_serie * 1000:7.0f} ms")
    print(f"4 procesos  {t_procesos * 1000:7.0f} ms")
    print("cada proceso arranca de cero: el modulo se reimporta y los datos se copian")
```

```python verificable
import pickle
import tracemalloc

import numpy as np

datos = np.arange(1_000_000, dtype=np.float64)      # 8 MB

tracemalloc.start()
serializado = pickle.dumps(datos)                   # lo que viaja por la tuberia al hijo
copia = pickle.loads(serializado)                   # y lo que el hijo reconstruye en su memoria
actual, pico = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("bytes del array original:", datos.nbytes)                        # -> 8000000
print("bytes del array reconstruido:", copia.nbytes)                    # -> 8000000
print(f"pico medido durante la copia {pico / 1024 / 1024:.1f} MiB")
print("el hijo no ve el array del padre: lo reconstruye entero")
```

## Errores típicos

- **Meter una llamada bloqueante dentro de una corrutina.** Un `time.sleep`, un `requests.get` o
  un driver sincrónico dentro de `async def` detienen el bucle y con él todas las tareas. Si la
  biblioteca es sincrónica, o usas `def` normal con hilos o la lanzas con
  `loop.run_in_executor`.
- **Usar hilos para cálculo puro esperando aceleración.** Con el GIL, dos hilos no suman dos
  núcleos en un bucle de Python. Para eso, procesos; y aun así, comprueba que el reparto
  compensa el coste de arranque y de copia.
- **Tocar estado compartido sin candado.** El GIL no hace atómica una secuencia de lectura y
  escritura. Los fallos son intermitentes, dependen de la carga y aparecen justo en producción.
- **Olvidar el `if __name__ == "__main__":` con multiprocessing en Windows.** Cada hijo
  reimporta el módulo; sin la guarda, vuelve a arrancar procesos desde el propio hijo y el
  programa falla con errores confusos de arranque.
- **Crear un proceso por tarea.** Arrancar un proceso cuesta decenas o cientos de milisegundos y
  copia datos. Se usa un grupo con tamaño fijo, dimensionado al número de núcleos.
- **Pasar el DataFrame entero a cada tarea de un grupo de procesos.** Cada envío serializa y
  copia todo: con 8 procesos y 100 MB de datos son gigabytes de copia por vuelta. Manda solo
  índices o nombres de partición y deja que el hijo lea lo que necesita, o comparte memoria.
- **Mezclar asincronía y grupos de hilos sin control.** `asyncio.to_thread` y los ejecutores son
  útiles, pero un grupo sin límite con miles de tareas concurrentes agota la memoria y las
  conexiones del servicio de destino. Pon límites y controla la concurrencia.

## Comprueba que lo sabes

:::quiz
p: Tienes que hacer 5.000 peticiones HTTP y luego un cálculo pesado sobre las respuestas. ¿Qué reparto es sensato en Python?
o: Un hilo por petición y, para el cálculo, más hilos
o: Asincronía o un grupo de hilos acotado para las peticiones, y procesos para el cálculo
o: Procesos para las peticiones y asincronía para el cálculo
a: 2
e: Las peticiones esperan red, así que se solapan con concurrencia (asincronía o hilos acotados). El cálculo puro está limitado por el GIL, así que necesita procesos para usar varios núcleos. Al revés no funciona: los procesos son carísimos para esperar y la asincronía no acelera el cálculo.
:::

:::quiz
p: ¿Por qué dos hilos que recorren una lista en Python no tardan la mitad que uno?
o: Porque el GIL solo permite ejecutar bytecode de Python a un hilo cada vez
o: Porque el sistema operativo reparte mal los núcleos
o: Porque las listas no se pueden compartir entre hilos
a: 1
e: En código Python puro el GIL serializa la ejecución: los hilos se relevan, no se solapan. Sí se solapan cuando la operación suelta el candado, como una espera de red o una función de NumPy que ejecuta código C.
:::

:::quiz
p: ¿Qué hace falta para que un proceso hijo vea un array grande que ya tiene el padre?
o: Nada, todos los procesos comparten la misma memoria
o: Enviarlo serializado por una cola, porque cada proceso tiene su propio espacio de memoria
o: Declarar el array como global
a: 2
e: Cada proceso tiene memoria propia: al enviar el array se serializa y el hijo lo reconstruye, así que se duplica. Para evitar la copia se usan mecanismos de memoria compartida o se hace que el hijo lea los datos de un fichero por su cuenta.
:::

:::trampa
El error más caro de este tema es leer «concurrente» y entender «paralelo». Cambiar un bucle por
un `ThreadPoolExecutor` sin medir antes puede dejar el tiempo igual o peor, con la dificultad
añadida de depurar condiciones de carrera. Mide primero, y paraleliza solo lo que sea de verdad
el cuello de botella.
:::

:::nota
Hay proyectos de Python sin GIL y va camino de ser opcional, pero el código que escribas hoy
debe seguir funcionando en un intérprete con GIL: las reglas de qué acelera cada modelo no
cambian por eso. Y aunque desaparezca, la carrera de datos sigue siendo tu responsabilidad.
:::

:::truco
Si dudas de si el cuello de botella es espera o cálculo, mide la CPU consumida además del tiempo
de reloj. Mucha CPU por segundo de reloj significa cálculo; poca CPU con mucho tiempo significa
espera, y ahí los procesos no te van a ayudar.
:::
