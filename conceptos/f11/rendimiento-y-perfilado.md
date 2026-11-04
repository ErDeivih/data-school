---
id: rendimiento-y-perfilado
titulo: Rendimiento y perfilado
fase: 11
nivel: avanzado
rutas: [alg, de]
prerequisitos: [concurrencia-async-hilos-procesos, gestion-de-memoria, numpy-fundamentos]
tags: [rendimiento, profiling, memoria, optimizacion]
resumen: Medir antes de optimizar: dónde se va el tiempo, cuánta memoria ocupa cada objeto y qué cuello de botella atacar primero.
fuentes: ["Gregg (2020), 'Systems Performance: Enterprise and the Cloud'", "Python, 'The Python Profilers' (documentación oficial)"]
---

## En una frase

Perfilar es averiguar con números dónde se va el tiempo y la memoria antes de tocar nada,
porque el cuello de botella casi nunca está donde la intuición dice.

## La idea

Todo el mundo sabe cuál es la línea lenta de su programa, y casi todo el mundo se equivoca. La
intuición se fija en lo que se entiende —una función con bucles anidados, un cálculo con
logaritmos— y el tiempo de verdad se va en la llamada que se hace un millón de veces, en la
consulta que se repite por cada fila o en el formateo de un `print` dentro del bucle.

La regla es sencilla de enunciar y difícil de cumplir: **primero se mide, después se optimiza**.
Y se mide en dos ejes distintos, porque un programa puede ser lento por dos motivos que se
arreglan de formas opuestas:

- **Está limitado por CPU:** pasa el tiempo calculando. Se arregla con un algoritmo mejor,
  vectorización o más núcleos.
- **Está limitado por entrada/salida:** pasa el tiempo esperando disco o red. Se arregla con
  menos llamadas, más concurrencia o caché, y añadir núcleos no sirve de nada.

Antes de medir hay que saber cuál de los dos es, y eso se ve comparando el tiempo de reloj con
la CPU consumida: mucha CPU por segundo de reloj es cálculo; tiempo de reloj alto con poca CPU
es espera.

Después está la memoria, que es el otro recurso que se agota. En Python cada objeto lleva
sobrecoste: un entero dentro de un diccionario ocupa más de lo que parece y un `DataFrame` de
Pandas ocupa varias veces lo que ocuparían los mismos números en memoria continua. Cuando un
proceso muere por falta de memoria, la pregunta correcta no es «cuántas filas tengo» sino
«cuántos bytes por fila estoy guardando, y cuántas copias de esa tabla existen a la vez».

Y una advertencia que ahorra días: **el perfilador cambia lo que mide**. Instrumentar cada
llamada tiene un coste fijo por llamada, así que las funciones cortas y muy repetidas aparecen
infladas, y el código que pasa mucho tiempo en C puede no reflejarse igual. El perfil no es la
verdad absoluta; es una pista que se confirma midiendo el antes y el después del cambio.

## Definición formal

**Perfiladores deterministas frente a estadísticos.**

- **`cProfile`** (determinista): instrumenta cada llamada y cuenta llamadas, tiempo total y
  tiempo propio. Coste alto por llamada, cifras exactas de recuento.
- **`line_profiler`**: tiempo por línea dentro de una función. Es lo que quieres cuando ya sabes
  qué función es el problema.
- **`py-spy`** (estadístico): muestrea la pila del proceso en ejecución, sin modificarlo ni
  frenarlo. Sirve para producción y para código que no puedes reiniciar.
- **`tracemalloc`**: asigna y libera memoria rastreada, con el punto del código donde se
  reservó. Es el perfilador de memoria de la biblioteca estándar.

**Las dos cifras que hay que saber leer.**

- **`tottime`** — tiempo propio: el que se pasó en la función sin contar lo que llamó dentro.
  Es la que señala al culpable real.
- **`cumtime`** — tiempo acumulado: el de la función más todo lo que llamó. Una función con
  `cumtime` alto y `tottime` bajo no es el problema; lo es algo que está más abajo.

**Complejidad algorítmica frente a constante.** Cambiar un recorrido lineal por una búsqueda en
conjunto cambia el orden de crecimiento; cambiar un bucle por una operación vectorizada cambia
la constante. Ambas cosas se miden igual, pero la primera gana siempre en cuanto los datos
crecen y la segunda puede ser irrelevante a pequeña escala.

**Regla de la medida honesta.** Un experimento de rendimiento necesita: datos del tamaño real,
varias repeticiones, mediana en lugar de una sola medida, y la misma máquina para las dos
versiones. Comparar dos tiempos medidos en máquinas o cargas distintas no es una medida, es una
anécdota.

## Ejemplo

Un proceso que analiza 500.000 filas con Pandas. La intuición dice que lo caro es el cálculo
estadístico. La medición dice otra cosa:

- Lectura del fichero CSV: 3,1 s.
- Cálculo de la media por grupo: 0,4 s.
- Validación fila a fila con `iterrows()`: 18,7 s.
- Escritura del resultado: 0,6 s.

Total: 22,8 s, de los que el 82 % está en una validación escrita como bucle sobre filas. La
solución no es tocar la estadística: es reescribir la validación de forma vectorizada. Y de paso,
cambiar el CSV por Parquet baja la lectura de 3,1 s a unas décimas.

Ahora el mismo programa contado en memoria: 500.000 filas con cinco columnas numéricas de 8
bytes son 20 MB en memoria continua, pero el `DataFrame` de Pandas con tipos por defecto puede
ocupar dos o tres veces eso, porque cada columna arrastra su índice y sus metadatos. Si además
hay una copia por una operación sobre una vista, tienes dos veces la tabla. Con 50 millones de
filas esa diferencia decide si el proceso cabe o no.

:::figura
fichero: rendimiento-perfil-y-memoria
pie: Izquierda, el perfil del ejemplo ordenado por tiempo: la validación fila a fila con `iterrows()` se lleva 18,7 de los 22,8 segundos, el 82 %, mientras que la estadística que la intuición señalaba son 0,4 s. Ese es el resultado que se busca al perfilar: no el que esperabas, el que está. Derecha, por qué el mismo dato puede ocupar cuatro veces y media más: una lista de enteros guarda un objeto por número (28 bytes de cabecera más 8 del puntero), y un array de 64 bits guarda 8 bytes planos. Antes de reescribir el algoritmo, cambia la representación.
fuente: figuras/rendimiento-y-perfilado-1.py
:::

## Código

```python verificable
import time

datos = list(range(1_000_000))          # sin numpy: queremos un recorrido lineal de verdad
valores = list(range(0, 1_000_000, 20_000))   # 50 consultas

inicio = time.perf_counter()
# `v in datos` sobre una lista recorre posiciones hasta encontrar v: O(n) por consulta.
en_lista = sum(1 for v in valores if v in datos)
t_lista = time.perf_counter() - inicio

# Convertir a conjunto cuesta un recorrido completo (O(n))... una vez.
conjunto = set(datos)
inicio = time.perf_counter()
# ...que se paga con creces: la pertenencia en un conjunto es O(1) por consulta.
en_conjunto = sum(1 for v in valores if v in conjunto)
t_conjunto = time.perf_counter() - inicio

print("encontrados:", en_lista, "y", en_conjunto)     # -> 50 y 50 (las dos formas coinciden)
print(f"buscar en la lista   {t_lista * 1000:8.1f} ms")
print(f"buscar en el conjunto {t_conjunto * 1000:7.3f} ms")
# max() evita dividir entre cero: con una lista diminuta el conjunto puede tardar 0.0 ms.
print("mejora:", round(t_lista / max(t_conjunto, 1e-9)), "x  (O(n) frente a O(1))")
```

:::claves
- `time.perf_counter()` es el reloj correcto para medir: es monótono (nunca retrocede si el
  sistema ajusta la hora) y tiene la mayor resolución disponible. `time.time()` mide hora de
  calendario y puede dar tiempos negativos.
- `t_lista` y `t_conjunto` se miden con **dos llamadas diferentes** a `perf_counter()`, cada una
  alrededor de su bucle. Si las restas al revés, el resultado sale negativo: el orden importa.
- `set(datos)` cuesta un recorrido completo de la lista y, además, **memoria**: un conjunto
  ocupa bastante más que la lista de la que sale. Aquí compensa porque se consulta 50 veces;
  con dos consultas, convertir sería más lento que buscar en la lista.
- `tracemalloc` solo ve **lo que pasa por el asignador de Python**. Un array de NumPy o un
  buffer de Arrow no aparecen: para esos hay que mirar el RSS del proceso (el monitor del
  sistema), no el perfilador.
- `tracemalloc.start()` no es gratis y **cambia el rendimiento** del programa que mide. Se
  enciende para medir y se apaga con `stop()`; dejar el rastreo encendido en producción falsea
  los tiempos y consume memoria propia.
- `estadisticas.stats` es un diccionario cuya clave es la tupla `(fichero, línea, nombre)` y
  cuyo valor empieza por el número de llamadas. Por eso `llamadas_a` busca por `k[2]` (el
  nombre) y coge `v[0]`: si dos funciones se llaman igual en ficheros distintos, `next()`
  devuelve la primera que encuentre, sin avisar.
- El diccionario de 200.000 entradas del segundo bloque guarda **200.000 referencias a un único
  objeto `str`**, no 200.000 cadenas: el sobrecoste por entrada que imprime es el del hueco del
  diccionario más el entero de la clave, no el del texto.
:::

```python verificable
import tracemalloc

# Para medir memoria hay que medirla, no adivinarla: cada objeto de Python tiene sobrecoste.
tracemalloc.start()
tabla = {}
for i in range(200_000):
    # El diccionario guarda 200.000 referencias AL MISMO objeto str, no 200.000 copias.
    tabla[i] = "x"                       # clave int, valor str
actual, pico = tracemalloc.get_traced_memory()   # pico = maximo alcanzado desde el start
tracemalloc.stop()

print("entradas:", len(tabla))                                # -> 200000
print(f"memoria actual {actual / 1024 / 1024:.1f} MiB")
print(f"pico {pico / 1024 / 1024:.1f} MiB")
# Dividir por el numero de entradas da el coste real de una entrada, metadatos incluidos.
print(f"sobrecoste por entrada {actual / len(tabla):.0f} bytes")
```

```python verificable
import cProfile
import pstats
from io import StringIO

def transformar(filas):
    return [fila for fila in filas if fila % 3 == 0]   # comprension: se llama una sola vez

def recorrer(filas):
    total = 0
    for fila in filas:              # recorrer una lista grande es lo caro
        total += fila
    return total

def trabajo():
    for _ in range(30):             # 30 llamadas: el perfil contara exactamente eso
        recorrer(range(20_000))     # range no crea la lista de 20.000 numeros
    transformar(list(range(20_000)))   # aqui si: list() materializa los 20.000

perfil = cProfile.Profile()
perfil.enable()          # a partir de aqui, cada llamada queda instrumentada y cronometrada
trabajo()
perfil.disable()

flujo = StringIO()       # print_stats vuelca cientos de lineas: se guardan en memoria, no en pantalla
estadisticas = pstats.Stats(perfil, stream=flujo).sort_stats("tottime")
estadisticas.print_stats()
informe = flujo.getvalue()

# stats guarda una fila por funcion: (fichero, linea, nombre) -> (llamadas, ...)
def llamadas_a(funcion):
    # v[0] es el numero de llamadas: se busca la fila cuyo nombre de funcion coincide.
    return next(v[0] for k, v in estadisticas.stats.items() if k[2] == funcion.__name__)

print("llamadas a recorrer:", llamadas_a(recorrer))            # -> 30
print("llamadas a transformar:", llamadas_a(transformar))      # -> 1
print("lineas del informe:", len(informe.splitlines()))
print("el informe ordena por tiempo propio: recorrer encabeza la lista")
```

## Errores típicos

- **Optimizar por intuición sin medir.** Se reescribe la función que parece lenta y el programa
  sigue tardando lo mismo, porque el tiempo estaba en otra parte. Perfila primero y anota el
  antes y el después de cada cambio.
- **Confundir tiempo propio con acumulado.** Una función con `cumtime` alto y `tottime` bajo no
  es la culpable: lo es algo que llamó. Si te fijas en la columna equivocada, optimizas el sitio
  que no era.
- **Medir una sola vez y con datos diminutos.** Un ejemplo con cien filas no dice nada del
  comportamiento con cien millones, y una única medida está dominada por el ruido del sistema.
  Repite, usa la mediana y datos del tamaño real.
- **Olvidar el coste de serializar y copiar.** `apply` fila a fila, `iterrows`, pasar el
  `DataFrame` a cada proceso o hacer `copy()` por comodidad cuestan más que el cálculo que
  intentas acelerar. La operación más rápida es la que no se hace.
- **Cambiar de algoritmo antes de mirar la constante.** Vectorizar o paralelizar un recorrido
  sigue siendo O(n). Si necesitas búsquedas repetidas, el conjunto o el índice valen más que
  cualquier microoptimización (de segundos a milisegundos, no de un 10 % a un 15 %).
- **Optimizar lo que nadie usa.** Bajar de 4 ms a 2 ms una función que se llama diez veces al
  día no cambia nada; reducir de 20 a 2 segundos una consulta que corre en cada petición, sí.
  Ordena por impacto total, no por porcentaje de mejora.
- **Dejar el perfilador encendido en producción.** Instrumentar cada llamada multiplica el coste
  y puede cambiar el comportamiento. En producción se muestrea con una herramienta externa o se
  activa el perfil de forma temporal y acotada.
- **Optimizar memoria y tiempo a la vez sin medir ambos.** Un cambio puede bajar el tiempo y
  multiplicar la memoria (caches, copias, materializar). Mide las dos cosas o acabarás
  cambiando un problema por otro.

## Comprueba que lo sabes

:::quiz
p: El informe de cProfile muestra una función con cumtime alto y tottime casi nulo. ¿Qué conclusión es correcta?
o: Que la función es la culpable y hay que optimizarla
o: Que el tiempo se va en las funciones que llama, no en ella misma
o: Que el perfilador está mal configurado
a: 2
e: El tiempo propio bajo dice que la función casi no ejecuta código por su cuenta: su tiempo es la suma de sus llamadas. El culpable está más abajo en el árbol. Optimizar esa función solo, sin mirar lo que llama, no cambia nada.
:::

:::quiz
p: Tu proceso tarda 40 segundos y la CPU consumida es de 3 segundos. ¿Qué tipo de cuello de botella tienes?
o: Limitado por CPU, así que conviene paralelizar con procesos
o: Limitado por entrada/salida, así que conviene reducir llamadas o usar concurrencia
o: No se puede saber con esos datos
a: 2
e: Tres segundos de CPU en cuarenta de reloj significa que el proceso pasa la mayor parte del tiempo esperando: red, disco o una base de datos. Paralelizar con procesos multiplicaría los que esperan sin reducir la espera; lo que hace falta es menos idas y venidas o concurrencia.
:::

:::quiz
p: ¿Por qué un cambio de lista a conjunto acelera tanto una búsqueda repetida?
o: Porque el conjunto guarda los elementos ordenados y usa búsqueda binaria
o: Porque la lista exige recorrer los elementos hasta encontrar el buscado, y el conjunto tiene acceso directo por hash
o: Porque el conjunto ocupa menos memoria que la lista
a: 2
e: En una lista cada consulta recorre hasta encontrar el valor, así que el coste crece con el tamaño. Un conjunto (y un diccionario) localiza por función hash casi en tiempo constante. No está ordenado ni usa búsqueda binaria, y de hecho suele ocupar más memoria que la lista.
:::

:::practica
enunciado: Un script tarda 6 minutos en procesar un CSV de 2 GB: 4 minutos leyendo por trozos con Pandas, 1 minuto calculando agregados y 1 minuto escribiendo a un CSV. Propón tres cambios ordenados por impacto y justifica cómo comprobarías cada uno.
pista: Reparte el tiempo entre entrada/salida y cálculo antes de decidir nada.
solucion: El 83 % del tiempo es entrada/salida (lectura más escritura), así que el cálculo no es el objetivo. Primero, cambiar el formato: leer y escribir Parquet en vez de CSV suele reducir mucho el tiempo porque es columnar y comprimido, y además permite leer solo las columnas necesarias. Segundo, leer solo las columnas que se usan y filtrar en la lectura, para tocar menos bytes. Tercero, evitar materializar el fichero entero si solo hace falta agregar: procesar por particiones o usar un motor que agregue sin cargar todo en memoria. Comprobación: cronometrar cada fase por separado antes y después con `time.perf_counter`, con el mismo fichero y varias repeticiones, y vigilar el pico de memoria con `tracemalloc` o el monitor del sistema, porque un cambio puede bajar el tiempo y disparar la memoria.
:::

:::trampa
El perfilador tiene coste por llamada. Una función corta llamada un millón de veces aparece
inflada en `cProfile` y puede parecer el cuello de botella cuando solo es víctima de la
instrumentación. Si sospechas eso, confirma con un perfilador estadístico como `py-spy`, que
muestrea sin instrumentar.
:::

:::truco
Antes de optimizar, mide el techo: cuánto tardaría una versión ideal que no hiciera el trabajo.
Si tu script tarda 6 minutos y el tiempo mínimo teórico de leer esos datos es 5, no busques
optimizaciones de cálculo, busca otro formato o menos datos que leer.
:::
