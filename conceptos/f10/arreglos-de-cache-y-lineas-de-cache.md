---
id: arreglos-de-cache-y-lineas-de-cache
titulo: Jerarquía de memoria y localidad de caché
fase: 10
nivel: intermedio
rutas: [alg, de]
prerequisitos: [arrays-y-listas, complejidad-asintotica, rendimiento-y-perfilado]
tags: [memoria, cache, rendimiento, localidad]
resumen: Por qué dos programas con las mismas operaciones tardan mil veces distinto: la distancia entre el dato y el núcleo decide el tiempo, no el número de operaciones.
fuentes: ["Bryant y O'Hallaron (2015), 'Computer Systems: A Programmer's Perspective'", "Drepper (2007), 'What Every Programmer Should Know About Memory'", "Hennessy y Patterson (2017), 'Computer Architecture: A Quantitative Approach'"]
---

## En una frase

La memoria del ordenador es una escalera de niveles cada vez más grandes y más lentos, y tu
programa solo va rápido cuando los datos que toca están en el escalón de arriba.

## La idea

Un acceso a un registro del procesador tarda menos de una milmillonésima de segundo. El mismo
acceso, si el dato está en la memoria principal, tarda ochenta veces más. Y si está en disco,
cien mil veces más. Esa diferencia —que llega a ser de un factor de cinco órdenes de magnitud— explica por sí sola
que existan las cachés, y también que dos programas con las
mismas operaciones puedan tardar mil veces distinto.

La caché es una copia pequeña y rápida de los datos que acabas de usar, apoyada en una apuesta que
casi siempre se gana: si has tocado un dato, es muy probable que vuelvas a tocar ese dato o uno
cercano. La apuesta tiene dos formas, y conviene no mezclarlas:

- **Localidad temporal**: el mismo dato, otra vez. Un contador que se incrementa en un bucle vive
  en un registro o en L1, y no importa lo largo que sea el bucle.
- **Localidad espacial**: datos vecinos. Cuando pides un `float` de 8 bytes, el procesador no te
  trae 8 bytes: te trae una **línea de caché** entera, que en x86-64 son 64 bytes. Si el siguiente
  dato que vas a leer está dentro de esos 64 bytes, lo tienes gratis. Si está a 4096 bytes de
  distancia, esa línea te la traes para nada y el trabajo de traerla lo pagas igual.

Esa segunda forma es la que se olvida, y es la que decide el rendimiento de casi todo el código
que procesa colecciones de datos. Recorrer un array en orden es rápido porque cada línea que se
trae se aprovecha entera: 8 `float` de 8 bytes por línea. Recorrer una lista enlazada es lento
aunque tenga los mismos elementos, porque cada nodo está en una línea distinta y cada salto es un
viaje nuevo a memoria.

Y hay un nivel más que casi nadie tiene en cuenta al principio: el **planificador de páginas**. El
procesador no traduce cada dirección por su cuenta; guarda las traducciones recientes en la TLB
(*translation lookaside buffer*), que tiene unas pocas entradas. Si tu programa salta entre muchas
páginas de memoria distintas —por ejemplo, con un salto de 4096 bytes, justo el tamaño de página—,
la TLB se queda sin entradas y cada acceso cuesta una consulta más a las tablas de páginas. Ese es
el motivo de que un recorrido con salto de 65536 bytes sea decenas de veces más lento que uno
secuencial, y de que el número de operaciones no explique nada.

:::figura
fichero: cache-escalera-y-codo-de-localidad
pie: Arriba, la escalera de la jerarquía: cada nivel es más grande y más lento, y el salto de RAM a SSD no es un factor sino un cambio de escala. Abajo, el modelo de localidad: mientras el conjunto de trabajo cabe en un nivel, la fracción de accesos que atiende no cambia; al desbordarlo, la carga se muda entera al siguiente. Las líneas verticales marcan los tamaños donde está el codo.
fuente: figuras/arreglos-de-cache-y-lineas-de-cache-1.py
:::

## Definición formal

Una caché se describe con cuatro números, y cada uno se lleva su parte de los fallos:

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `B` | Tamaño de la línea de caché: la unidad mínima que se transfiere | bytes | Cada fallo cuesta más y la memoria se llena de datos que no usas; con líneas pequeñas, más etiquetas y más comprobaciones |
| `S` | Número de conjuntos en los que se organiza la caché | conjuntos | Bajan las colisiones entre direcciones distintas, pero hay más circuitería para decidir dónde va cada línea |
| `E` | Vías por conjunto (asociatividad) | líneas | Menos fallos por conflicto, a cambio de más comparaciones en paralelo y más tiempo por acceso |
| `N` | Tamaño total de la caché, `N = S · E · B` | bytes | Cabe más conjunto de trabajo sin fallos, y el codo de rendimiento se mueve a la derecha |
| `t_hit` | Latencia de un acierto | ciclos o ns | Es el suelo del tiempo de acceso: lo que tarda tu bucle como mínimo |
| `t_miss` | Latencia de un fallo, que incluye ir al nivel siguiente | ciclos o ns | Cada fallo duele más, así que la localidad importa más |
| `m` | Tasa de fallos: fallos divididos entre accesos | tanto por uno | Es la variable que de verdad gobierna el tiempo, y no se ve en el código: se mide |
| `AMAT` | Tiempo medio de acceso a memoria | ciclos o ns | Es el número que se optimiza; sube con `m` y con `t_miss`, y su suelo es `t_hit` |
| `W` | Conjunto de trabajo: cuánta memoria distinta toca el programa | bytes | Si supera `N`, la tasa de fallos deja de ser residual y pasa a dominar el tiempo |

:::

El tiempo medio de un acceso es la fórmula que explica todo lo demás:

:::formula
AMAT = t_hit + m · t_miss
:::

Con números reales de una caché L1 de un procesador actual: `t_hit` de 4 ciclos y `t_miss` de unos
200 ciclos hasta memoria. Con una tasa de fallos del 1 %, el acceso medio cuesta `4 + 0,01 · 200 =
6` ciclos: un 50 % más que el suelo. Con una tasa del 10 %, cuesta `4 + 20 = 24` ciclos: seis
veces el suelo. Fíjate en que la tasa de fallos no multiplica el tiempo total de forma lineal,
porque el término del fallo ya es 50 veces más grande que el acierto.

La dirección de memoria se parte en tres campos, y saber leerla explica los conflictos:

:::formula
dirección = etiqueta · (S · B) + conjunto · B + desplazamiento
:::

- `desplazamiento` — los bits bajos que dicen en qué byte dentro de la línea caes. Con `B = 64`
  son 6 bits, y por eso las direcciones 0 y 63 están en la misma línea.
- `conjunto` — los bits siguientes, que deciden en qué conjunto de la caché puede vivir la línea.
  Con `S = 64` conjuntos son 6 bits.
- `etiqueta` — el resto de la dirección, que se guarda junto a la línea para comprobar que el dato
  es el que crees y no otro que cayó en el mismo conjunto.

Eso deja dos consecuencias que muerden: dos direcciones separadas por un múltiplo de `S · B`
bytes van **al mismo conjunto** y compiten por sus `E` vías; y las líneas nunca se comparten, así
que leer 1 byte de cada 64 bytes usa el 100 % de la línea y leer 1 byte de cada 4096 usa el 1,6 %. Ese desperdicio no aparece por ningún lado en el código: solo se ve cuando cuentas fallos de caché por operación y los comparas con los accesos que hiciste.

## Ejemplo

Un array de un millón de enteros de 4 bytes ocupa 4 MB. Recorrerlo de principio a fin toca
`4.000.000 / 64 = 62.500` líneas, todas una sola vez. Con una L1 de 32 KB, cada línea se trae
desde el nivel siguiente, y el tiempo por elemento no depende del tamaño del array: la caché va
por delante del recorrido y va quedando sitio para la línea nueva.

Ahora el mismo array recorrido con un salto de 4096 bytes, que es el tamaño de una
página:

- Cada acceso cae en una **página distinta**: 1024 elementos por página, así que un recorrido de
  1.000 accesos visita 1.000 páginas.
- Cada página necesita su entrada en la TLB, y una TLB típica tiene unas 1.500 entradas para
  páginas de 4 KB. Al desbordarla, cada acceso paga una consulta a las tablas de páginas.
- Además, cada línea de 64 bytes se usa para 1 solo elemento de los 16 enteros que caben: el
  resto se descarga sin haberse tocado.

La tabla siguiente sale de medir sobre un buffer de 32 MB con accesos de tipo *gather* (un índice
calculado por acceso), que es el patrón que aparece al recombinar registros por una clave:

| Salto entre accesos | ns por acceso | Comentario |
| --- | --- | --- |
| 1 byte | 2,5 | Una línea sirve 64 accesos |
| 32 bytes | 4,5 | Dos accesos por línea |
| 64 bytes | 6,0 | Un acceso por línea: codo de la localidad espacial |
| 512 bytes | 8,5 | Sin reutilización, TLB aún holgada |
| 4096 bytes | 10,6 | Una página por acceso: la TLB empieza a fallar |
| 16384 bytes | 18,3 | TLB desbordada y precarga de páginas sin acertar |

De 2,5 a 18,3 ns por acceso: un factor de 7 con las mismas operaciones aritméticas.
Y en el caso del salto de 1 byte, la mitad del tiempo es el propio bucle de indexación de NumPy:
el acceso real a la memoria es bastante más barato de lo que dice la tabla.

Ese factor explica que estructurar los datos importe más que optimizar la aritmética. Un
ejemplo clásico: sumar una columna de una matriz guardada por filas cuesta un fallo por elemento
—cada elemento está en una línea distinta—, mientras que sumar la misma columna desde una copia
guardada por columnas cuesta un fallo cada 16 elementos.

## Código

```python verificable
# El mismo trabajo con la misma cuenta de operaciones: solo cambia el orden de los datos
import numpy as np

filas, columnas = 512, 512
m = np.arange(filas * columnas, dtype=np.float64).reshape(filas, columnas)
t = m.T                                   # vista traspuesta: NO copia nada

print("m es C-contigua:", m.flags["C_CONTIGUOUS"], "-> recorre memoria en orden")
# -> m es C-contigua: True -> recorre memoria en orden
print("t es C-contigua:", t.flags["C_CONTIGUOUS"], "-> salta de fila en fila")
# -> t es C-contigua: False -> salta de fila en fila
print("bytes de una fila:", m.strides[0], "bytes de la linea de cache tipica: 64")
# -> bytes de una fila: 4096 bytes de la linea de cache tipica: 64
```

:::claves
- `m.T` **no copia**: devuelve una vista con los mismos datos y los pasos de indexación
  intercambiados. Por eso el mismo array puede ser rápido por filas y lento por columnas sin que
  el tamaño cambie.
- `m.strides[0]` son los bytes que hay que saltar para pasar de una fila a la siguiente: 4096. Ese
  número es lo que decide si dos elementos consecutivos comparten línea de caché. Si es mayor que
  64, no la comparten.
- `m.flags["C_CONTIGUOUS"]` es `False` cuando los pasos no permiten recorrer el array en orden de
  memoria. Que el array sea contiguo no dice nada del resultado de tus sumas, pero lo dice todo
  del tiempo que tardan.
- Trasponer y sumar por columnas tiene la misma complejidad asintótica que sumar por filas
  —`O(filas · columnas)`— y puede ser varias veces más lento. La notación O esconde el coste de
  memoria: esa es la lección de la página.
- Si de verdad necesitas recorrer por columnas muchas veces, `np.ascontiguousarray(t)` paga una
  copia de 2 MB una vez y deja el recorrido rápido para siempre. Copiar para ordenar los datos
  suele salir a cuenta.
:::

```python verificable
# Cuantos bytes de memoria hay que traer por cada elemento, segun el salto
import numpy as np

LINEA = 64                        # bytes por linea de cache en x86-64

for salto in (1, 16, 64, 4096):
    # Un recorrido con paso fijo no repite linea: el numero de lineas distintas que se tocan
    # es como mucho el total del buffer, y el coste util de cada una depende de cuantos de sus
    # elementos se llegan a usar.
    elementos_por_linea = max(1, LINEA // salto)
    print(f"salto {salto:>5} B: {elementos_por_linea:>3} elementos por linea, "
          f"{LINEA / elementos_por_linea:>7.1f} bytes traidos por elemento")
# -> salto     1 B:  64 elementos por linea,     1.0 bytes traidos por elemento
# -> salto    16 B:   4 elementos por linea,    16.0 bytes traidos por elemento
# -> salto    64 B:   1 elementos por linea,    64.0 bytes traidos por elemento
# -> salto  4096 B:   1 elementos por linea,    64.0 bytes traidos por elemento
```

:::claves
- `LINEA // salto` es cuántos elementos consecutivos comparten línea en un buffer de bytes. Con
  salto 1 son 64; con salto 16, solo 4, y el resto de la línea se descarga sin haberse tocado. El
  `max(..., 1)` evita el cero: no se puede bajar de un elemento por línea.
- La última columna es la cuenta que importa. Con salto 16, cada byte que usas te cuesta 16 bytes
  traídos de memoria; con salto 64 o más, 64. Eso no se arregla escribiendo mejor el bucle: se
  arregla cambiando el orden de los datos, que es de lo que va la página.
- A partir de un salto igual a la línea (64), subir el salto ya no cambia los bytes por elemento:
  sigue siendo uno por línea. Lo que empeora entonces es otra cosa, la TLB, y por eso el tiempo
  sigue subiendo aunque estos números se queden quietos.
- El bucle **no** mide tiempo; cuenta bytes. Es determinista, no depende del procesador y se puede
  comprobar a mano. Los tiempos se miden aparte y con repeticiones.
:::

```python ilustrativo
# Cronometrar la misma suma sobre la vista traspuesta y sobre una copia contigua. Este bloque
# mide la maquina, no el algoritmo: los milisegundos cambian en cada ejecucion y la desigualdad
# puede invertirse, asi que no lleva comentarios `# ->` ni entra en la verificacion automatica.
import time

import numpy as np

m = np.arange(1024 * 1024, dtype=np.float64).reshape(1024, 1024)
vista = m.T                                   # no copia: los pasos siguen siendo de 8 KB
copia = np.ascontiguousarray(vista)           # copia: ahora el recorrido es en orden

def ms(operacion, repeticiones=20):
    """Milisegundos de la operacion, quedandose con el mejor de varios intentos."""
    mejor = float("inf")
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        operacion()
        mejor = min(mejor, time.perf_counter() - t0)
    return mejor * 1000

t_vista = ms(lambda: float(vista.sum()))
t_copia = ms(lambda: float(copia.sum()))
print(f"vista traspuesta: {t_vista:.2f} ms   copia contigua: {t_copia:.2f} ms")
print("la copia es mas rapida que la vista:", t_copia < t_vista)
```

:::claves
- Las dos sumas recorren los mismos 8 MB de números y hacen las mismas sumas. La única diferencia
  es que `vista` salta 8 KB entre elementos consecutivos y `copia` va en orden. Lo que se paga es
  la espera, no la aritmética.
- Se toma el **mínimo** de veinte intentos y se devuelve en milisegundos. La media de una medida
  tan corta la dominan las interrupciones del sistema; el mínimo se acerca al coste real.
- `np.ascontiguousarray(vista)` copia 8 MB una vez. Si el recorrido se va a hacer muchas veces,
  esa copia se amortiza; si se hace una sola vez, has pagado un trabajo de más. La decisión se
  toma contando cuántas pasadas vas a hacer, no por gusto.
- Ni el número ni la desigualdad son un resultado. Medido en este equipo, sumar el array entero
  tarda prácticamente lo mismo desde la vista que desde la copia, y hay ejecuciones en las que gana
  la vista: una reducción completa recorre la memoria en orden interno y el efecto de la
  trasposición se diluye. Con el array entero dentro de la caché (8 MB) la diferencia desaparece.
  Por eso este bloque va marcado `ilustrativo`: lo que se comprueba en la verificación es la cuenta
  de bytes del bloque anterior, que no depende de ninguna máquina.
- `float(vista.sum())` convierte el resultado a un `float` de Python para que NumPy no se guarde
  el cálculo como array; no cambia lo que se mide, pero deja claro que se usa el resultado.
:::

## Errores típicos

- **Contar operaciones y creer que eso es el tiempo.** Un recorrido de una lista enlazada y uno de
  un array tienen el mismo número de accesos y no tardan lo mismo ni de lejos. Cuando el tiempo no
  cuadra con la cuenta de operaciones, lo que falta es la jerarquía de memoria.
- **Creer que un array de NumPy es rápido siempre.** Un array con pasos raros (una vista
  traspuesta, un `[::3]`, una columna de una matriz por filas) es más lento que un bucle de
  Python bien escrito en algunos casos. La contigüidad es una propiedad del array, no del tipo.
- **Optimizar la aritmética antes que el acceso.** Multiplicar por la mitad de operaciones en un
  bucle que espera a memoria no se nota: el procesador ya estaba esperando. Primero se ordenan los
  datos, después se cuentan las operaciones.
- **Medir con `time` dentro del bucle.** Coger el reloj en cada iteración cuesta más que el acceso
  que pretendes medir. Se cronometra el bucle entero, se repite, y se divide.
- **Suponer que dos objetos independientes están separados.** En Python, un objeto y sus atributos
  pueden caer en la misma línea de 64 bytes, y entonces tocar un atributo trae los otros de
  regalo: por eso `__slots__` o guardar los datos en arrays paralelos puede ser más rápido que
  una lista de objetos, aunque el código parezca más feo.
- **Ignorar que la caché no es privada.** Hay un protocolo de coherencia entre núcleos: cuando un
  núcleo escribe una línea que otro tiene copiada, esa copia se invalida. Un contador compartido
  actualizado desde varios hilos mueve la misma línea de un núcleo a otro en cada iteración, y
  cada movimiento cuesta más que el incremento.
- **Asumir que el tamaño de la línea y de la página son iguales en todas las máquinas.** 64 bytes
  de línea es lo habitual en x86-64, pero no es universal, y el tamaño de página puede ser 4 KB o
  2 MB. Los números concretos se miden en la máquina donde vas a desplegar.

:::practica
enunciado: Una matriz de 10.000 por 10.000 números de 8 bytes está guardada por filas. Un programa la recorre entera sumando todos los elementos. ¿Cuántas líneas de caché distintas se tocan recorriendo por filas y cuántas si el acceso por algún motivo salta de 64 en 64 elementos?
pista: Cuenta cuántos elementos caben en una línea de 64 bytes y cuántas líneas usa cada elemento con cada patrón. Los bytes totales se calculan con filas por columnas por 8.
solucion: La matriz ocupa 10.000 · 10.000 · 8 = 800.000.000 bytes, unos 763 MB, es decir 12.500.000 líneas de 64 bytes. Recorriendo por filas, en orden, cada línea se usa entera y se tocan exactamente esas 12,5 millones de líneas. Con un salto de 64 elementos se toca un elemento por línea visitada, y cada línea se trae 64 bytes para usar 8: se acaban tocando las mismas líneas, pero ninguna reutilización sirve de nada y el orden de visita salta por toda la memoria. Si el salto hiciera que varias líneas se reutilizaran antes de ser desalojadas, el número de líneas tocadas no cambiaría, pero el número de fallos sí: la métrica que importa es la tasa de fallos, no el recuento de líneas.
:::

## Comprueba que lo sabes

:::quiz
p: Recorres un array de 8 millones de enteros de 4 bytes de principio a fin. ¿Cuántas líneas de caché tocas, como mínimo?
o: 8 millones, una por entero
o: 500.000, porque cada línea de 64 bytes lleva 16 enteros
o: 32 millones, cuatro por entero
a: 2
e: Una línea de caché son 64 bytes y cada entero ocupa 4, así que caben 16 enteros por línea y el total es 8.000.000 / 16 = 500.000 líneas. En un recorrido secuencial cada línea se trae una vez y se aprovecha entera; el número de accesos a memoria real es el de líneas, no el de elementos.
:::

:::quiz
p: Dos bucles hacen el mismo número de sumas y de comparaciones sobre los mismos datos. Uno tarda tres veces más. ¿Cuál es la explicación más probable?
o: El segundo usa una versión más lenta de la operación de suma
o: El patrón de acceso del segundo rompe la localidad espacial y paga más fallos de caché
o: El segundo tiene una complejidad asintótica peor
a: 2
e: Si las operaciones son las mismas, la complejidad asintótica es la misma y la suma tarda lo mismo: lo que cambia es cuántos fallos de caché y de TLB provoca cada patrón. Recorrer memoria en orden aprovecha líneas enteras; saltar de 4096 en 4096 usa 1 de cada 16 elementos de la línea y castiga la TLB.
:::

:::quiz
p: ¿Por qué trasponer una matriz con NumPy y sumar por columnas puede ser más lento que sumar por filas, si es la misma cantidad de datos?
o: Porque la traspuesta copia todos los datos a un array nuevo
o: Porque la traspuesta es una vista y el recorrido salta de fila en fila, con un fallo de caché casi por elemento
o: Porque NumPy no permite sumar matrices traspuestas
a: 2
e: `m.T` no copia nada: devuelve una vista con los pasos intercambiados. Al recorrerla, los elementos consecutivos están a 4096 bytes de distancia, es decir en líneas distintas, así que cada uno paga su propio acceso a memoria. Si el recorrido por columnas se repite muchas veces, copiar con `np.ascontiguousarray` una sola vez sale a cuenta.
:::
