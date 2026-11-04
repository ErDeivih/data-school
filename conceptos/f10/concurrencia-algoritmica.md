---
id: concurrencia-algoritmica
titulo: Concurrencia y paralelismo
fase: 10
nivel: avanzado
rutas: [alg]
prerequisitos: [complejidad-asintotica, tablas-hash, analisis-amortizado]
tags: [concurrencia, paralelismo, bloqueos, atomicidad]
resumen: Varias tareas en curso a la vez: por qué dos operaciones correctas se estropean al intercalarse y qué garantiza de verdad un candado.
fuentes: ["Herlihy y Shavit (2012), 'The Art of Multiprocessor Programming'", "Amdahl (1967), 'Validity of the single processor approach to achieving large scale computing capabilities'", "Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 27"]
---

## En una frase

Dos operaciones que por separado son correctas pueden dar un resultado incorrecto si se
intercalan mal: la concurrencia consiste en decidir qué combinaciones de pasos están prohibidas
y en construir un mecanismo que las impida.

## La idea

Dos personas sacan dinero de la misma cuenta, cada una con su libreta. Ambas leen el saldo:
100 €. Ambas restan 30 y escriben 70. Han sacado 60 € y la cuenta solo ha bajado 30. La
operación «restar 30» no es un paso, son tres: leer, calcular, escribir. Y el intercalado
—leer, leer, calcular, calcular, escribir, escribir— rompe una invariante que nadie puso por
escrito: el saldo tiene que bajar exactamente lo que se saca.

Eso es una **condición de carrera**: el resultado depende del orden en que el planificador
reparta los pasos. Lo grave no es que falle a menudo, es que falla de vez en cuando: un test que
pasa mil veces no demuestra nada, y el fallo aparece el día que hay carga en el servidor.

Hay dos motivos distintos para meter concurrencia en un programa, y conviene no confundirlos:

1. **Solapar esperas.** Mientras un hilo espera al disco o a la red, otro puede avanzar. No se
   hace más trabajo por segundo, se deja de estar parado. Es lo que resuelve la asincronía.
2. **Repartir cálculo.** Dos núcleos ejecutan a la vez dos mitades del problema. Aquí sí hay más
   trabajo por segundo, pero solo si las mitades no necesitan hablarse a cada paso.

El segundo caso tiene un techo incómodo: la parte que no se puede paralelizar manda. Si el 20 %
del tiempo de un programa es estrictamente secuencial, ningún número de núcleos baja de ese
20 %, así que la aceleración nunca pasa de 5 veces. Y ese techo se alcanza rápido: pasar de 4 a
64 núcleos compra muy poco cuando la mitad del trabajo es serie.

Compartir memoria trae además un problema de modelo mental: el hardware no ejecuta las cosas en
el orden en que las escribiste. Un compilador puede reordenar instrucciones y una CPU puede
tener dos escrituras en vuelo. Por eso los lenguajes ofrecen primitivas con garantías
explícitas —candados, variables atómicas, barreras de memoria— y por eso «casi siempre
funciona» no es un criterio válido.

## Definición formal

Notación: un programa concurrente son `n` hilos `T₁ … Tₙ`; cada hilo ejecuta una secuencia de
**acciones** (leer una variable, escribirla, adquirir un candado).

- **Entrelazado (interleaving):** una secuencia que contiene todas las acciones de todos los
  hilos respetando el orden interno de cada hilo. La semántica habitual de memoria compartida es
  que el resultado es el de *algún* entrelazado: si existe uno que rompe la propiedad, el
  programa es incorrecto, aunque otro entrelazado dé la respuesta buena.
- **Número de entrelazados:** con `n` hilos de `k` acciones cada uno hay

:::formula
entrelazados = (n · k)! / (k!)ⁿ
:::

  porque se permutan `n · k` acciones y se divide por las `k!` reordenaciones internas de cada
  hilo, que no son válidas. Con 2 hilos y 3 acciones: 6! / (3! · 3!) = 20.
- **Atómica:** una acción es atómica si ningún otro hilo puede observar un estado intermedio
  suyo. `contador += 1` no lo es: son una lectura, una suma y una escritura.
- **Sección crítica:** fragmento de código que toca estado compartido y que debe ejecutarse en
  exclusión mutua. El candado debe rodear la sección *completa*, no cada acceso por separado.
- **Invariante:** propiedad que debe cumplirse en todo momento observable. En la cuenta, «saldo
  = saldo inicial − suma de reintegros». Es lo que hay que proteger, no la variable suelta.
- **Candado (mutex):** par de operaciones `adquirir` / `liberar` con la garantía de que a lo sumo
  un hilo está dentro a la vez. `with candado:` libera al salir, incluso si hay excepción.
- **Interbloqueo (deadlock):** situación en la que cada hilo espera un candado que tiene otro y
  ninguno avanza. Condición necesaria: dos candados adquiridos en órdenes distintos.
- **Inanición (starvation):** un hilo no logra entrar nunca porque otros siempre se le cuelan.
- **Grano del candado:** cuánto abarca. Grueso (uno para todo) serializa; fino (uno por
  elemento) multiplica el coste de gestión y abre la puerta a interbloqueos.

**Aceleración (ley de Amdahl).** Si una fracción `p` del trabajo es paralelizable y hay `n`
trabajadores:

:::formula
S(n) = 1 / ((1 − p) + p / n)
:::

Con `p = 0,9` y `n = 4`: `S = 1 / (0,1 + 0,225) = 3,08`. Con `n = 64`: `S ≈ 7,7`. El muro no es
el número de núcleos, es el `0,1` que no se puede repartir.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Número de hilos del programa (o de núcleos, en la parte de Amdahl) | hilos o núcleos | Más hilos son más entrelazados que comprobar: el número de combinaciones crece de forma explosiva, y por eso un test que pasa mil veces no demuestra que el programa esté bien. En Amdahl, más núcleos ayudan cada vez menos |
| `k` | Acciones que ejecuta cada hilo; en el ejemplo de la cuenta, 3 (leer, sumar, escribir) | acciones | Cada acción nueva multiplica los entrelazados posibles por un factor que crece con `n`: pasar de 3 a 6 acciones por hilo no duplica el problema, lo eleva al cuadrado |
| `entrelazados` | Número de entrelazados válidos, `(n · k)! / (k!)ⁿ`: todas las acciones mezcladas sin romper el orden interno de cada hilo | entrelazados | Es el espacio de estados que habría que cubrir en un test exhaustivo. Con 2 hilos y 3 acciones son 20; con 4 hilos, 369.600 |
| `p` | Fracción del trabajo total que se puede repartir entre trabajadores | adimensional, entre 0 y 1 | La aceleración máxima sube: el techo es `1 / (1 − p)`. Con `p = 0,8` es 5 veces y con `p = 0,95`, 20; con `p = 0,5`, ni con 64 núcleos se pasa de 2 |
| `S(n)` | Aceleración: cuántas veces más rápido con `n` trabajadores que con uno | veces | Se acerca a su techo `1 / (1 − p)` y se estanca ahí. Duplicar los núcleos cuando `n` ya es grande compra muy poco: de 8 a 64 núcleos con `p = 0,8` solo se pasa de 3,33 a 4,71 |
:::

## Ejemplo

Una cuenta con 100 € y tres pasos por hilo: `L` (leer), `S` (sumar −30), `E` (escribir). Dos
hilos hacen `L₁ S₁ E₁` y `L₂ S₂ E₂`. Hay 20 entrelazados válidos, y en 18 de ellos las dos
lecturas caen antes de las dos escrituras: los dos hilos leen 100, los dos escriben 70 y el
saldo final es **70** con 60 € retirados. En los 2 entrelazados restantes la secuencia queda
`L₁ S₁ E₁ L₂ S₂ E₂` o `L₂ S₂ E₂ L₁ S₁ E₁`, y el saldo es **40**, que es lo correcto.

Con un candado alrededor de `L S E` completo, el número de entrelazados se reduce a dos
—`[L₁ S₁ E₁][L₂ S₂ E₂]` o `[L₂ S₂ E₂][L₁ S₁ E₁]`— y el saldo es siempre 40.

Y para la parte de aceleración: un proceso que tarda 10 s, de los cuales 8 s son de cálculo
repartible y 2 s de lectura de un fichero que nadie más puede tocar, tiene `p = 0,8`. Con 2
núcleos: `S = 1 / (0,2 + 0,4) = 1,67` → 6 s. Con 8 núcleos: `S = 1 / (0,2 + 0,1) = 3,33` → 3 s.
Multiplicar por cuatro los núcleos baja el tiempo de 6 a 3: el techo lo pone el fichero, no la
CPU.

:::figura
fichero: amdahl-y-entrelazados
pie: Izquierda: la aceleración que promete Amdahl para cuatro fracciones paralelizables, con el techo de cada una en línea de puntos. Con la mitad del trabajo en serie (p = 50 %) no se pasa de 2 veces por muchos núcleos que se pongan, y con p = 80 % el techo es 5: de 8 a 64 núcleos solo se sube de 3,33 a 4,71. La parte que no se reparte es la que manda, y se nota antes de lo que parece. Derecha: cuántos entrelazados admite un programa de n hilos con tres acciones cada uno (leer, sumar, escribir) y cuántos de ellos acaban con el resultado correcto. Con 2 hilos hay 20 y solo 2 salen bien: los otros 18 pierden una actualización, que es el 90 % de las veces. Con 4 hilos son 369.600 entrelazados y 24 buenos, uno de cada 15.400. Esa es la razón de que un test que pasa mil veces no demuestre nada: casi todos los entrelazados posibles están mal, y basta con que el planificador elija uno de ellos.
fuente: figuras/concurrencia-algoritmica-1.py
:::

## Código

```python verificable
import threading

# Intercalado forzado con eventos: el "lost update" se reproduce siempre, no por suerte.
contador = [0]
ha_leido = threading.Event()
puede_escribir = threading.Event()

def hilo_a():
    valor = contador[0]           # A lee 0
    ha_leido.set()                # avisa de que ya ha leido
    puede_escribir.wait()         # y espera a que B escriba
    contador[0] = valor + 1       # A escribe 1: pisa el 1 que dejo B

def hilo_b():
    ha_leido.wait()
    contador[0] = contador[0] + 1     # B lee 0 y escribe 1
    puede_escribir.set()

a = threading.Thread(target=hilo_a)
b = threading.Thread(target=hilo_b)
a.start(); b.start(); a.join(); b.join()

print("incrementos pedidos:", 2)                        # -> 2
print("valor final:", contador[0])                      # -> 1
print("se ha perdido un incremento:", contador[0] != 2)  # -> True
```

:::claves
- `contador = [0]` es una **lista de un elemento**, no un número: dentro de la función hay que escribir `contador[0]` para mutar el objeto compartido. Con `contador = 0` y `contador += 1` dentro de `hilo_a`, Python crearía una variable local y lanzaría `UnboundLocalError` al leerla antes de asignarla; el de fuera no cambiaría en ningún caso.
- `hilo_a` guarda `valor = contador[0]` **antes** de `puede_escribir.wait()`: por eso pisa la escritura de B. Si volviera a leer después de la espera, el valor final sería 2 y el fallo desaparecería. Lo que rompe la invariante es leer pronto y escribir tarde, no el `Event`.
- `threading.Event` sirve para **forzar** el intercalado malo y que el fallo salga siempre. Es lo contrario de un candado: no impide la carrera, la provoca a propósito para poder verla.
- Sin los `a.join()` y `b.join()`, el `print` puede ejecutarse antes de que los hilos terminen y el valor impreso sería 0. `join()` espera a que el hilo acabe, y aun así el orden de los `print` no demuestra nada sobre el orden real de las acciones.
- En el bloque siguiente, `permutations(pasos)` genera **720** tuplas (6!), no 20: el filtro `valido` descarta las que rompen el orden interno de cada hilo. `orden.index("A1")` recorre la tupla en cada llamada, así que el filtro cuesta más que generar las permutaciones.
- `POR_HILO = 50_000` es el mismo número que `50000`: el guion bajo es solo para leerlo de un vistazo. Y `with candado:` libera el candado al salir **aunque haya una excepción**, que es la razón de usarlo en vez de `acquire()` y `release()` a mano.
:::

```python verificable
from itertools import permutations
from math import factorial

# Cuantos entrelazados admite un programa de 2 hilos con 3 acciones cada uno.
pasos = ["A1", "A2", "A3", "B1", "B2", "B3"]

def valido(orden):
    # Cada hilo conserva el orden de sus propias acciones.
    return (orden.index("A1") < orden.index("A2") < orden.index("A3")
            and orden.index("B1") < orden.index("B2") < orden.index("B3"))

validos = [o for o in permutations(pasos) if valido(o)]
print("entrelazados validos:", len(validos))                      # -> 20
print("formula 6!/(3!*3!):", factorial(6) // factorial(3) ** 2)   # -> 20

# Los que pierden una actualizacion: las dos lecturas antes de las dos escrituras.
malos = [o for o in validos
         if max(o.index("A1"), o.index("B1")) < min(o.index("A3"), o.index("B3"))]
print("pierden una actualizacion:", len(malos))                   # -> 18
```

```python verificable
import threading

# Con un candado, leer-modificar-escribir se vuelve una sola operacion para los demas.
CONTADOR = [0]
candado = threading.Lock()
POR_HILO = 50_000
N_HILOS = 4

def sumar(n):
    for _ in range(n):
        with candado:
            CONTADOR[0] += 1

hilos = [threading.Thread(target=sumar, args=(POR_HILO,)) for _ in range(N_HILOS)]
for h in hilos:
    h.start()
for h in hilos:
    h.join()

print("esperado:", N_HILOS * POR_HILO)                        # -> 200000
print("obtenido:", CONTADOR[0])                               # -> 200000
print("coincide:", CONTADOR[0] == N_HILOS * POR_HILO)         # -> True
```

## Errores típicos

- **Creer que una operación de alto nivel es atómica.** `contador += 1`, `lista.append(x)` y
  `diccionario[clave] = valor` no lo son en general: son varios pasos y el planificador puede
  cortar entre ellos. Lo que hay que hacer es rodear la secuencia completa con el candado, no
  cada acceso suelto.
- **Proteger la variable en vez de la invariante.** En una transferencia entre dos cuentas hay
  que mantener «la suma de los dos saldos es constante»; si bloqueas cada cuenta por separado,
  entre las dos operaciones el dinero se ha esfumado y un lector intermedio ve un total falso.
  Un solo candado para las dos cuentas, o un orden global fijo.
- **Adquirir dos candados en órdenes distintos.** El hilo 1 toma `A` y espera `B`; el hilo 2
  toma `B` y espera `A`. Interbloqueo, y el programa se queda colgado sin consumir CPU. La regla
  práctica: todo el código adquiere los candados en el mismo orden, y se documenta el orden.
- **Comprobar y actuar sin candado.** «Si no existe la clave, créala» es un patrón de carrera
  clásico: los dos hilos comprueban, los dos crean. Hay que hacer la comprobación y la acción
  dentro de la misma sección crítica, o usar una operación atómica del contenedor.
- **Confundir concurrencia con paralelismo y esperar aceleración.** Tener 8 hilos en un
  intérprete con GIL no reparte el cálculo entre 8 núcleos: los detalles de qué acelera cada
  modelo en Python están en [[concurrencia-async-hilos-procesos]]. Paralelizar sin medir suele
  dejar el tiempo igual y añadir fallos intermitentes.
- **Ignorar la parte serie.** Antes de repartir hay que medir cuánto del tiempo es
  estrictamente secuencial. Si el 40 % no se puede paralelizar, el techo es 2,5 veces y montar un
  clúster grande no lo supera.

## Comprueba que lo sabes

:::quiz
p: ¿Por qué dos hilos que ejecutan `saldo = saldo - 30` pueden dejar la cuenta en 70 € si se han retirado 60 €?
o: Porque la resta se calcula mal cuando la hacen dos hilos a la vez
o: Porque cada hilo lee 100, resta y escribe 70, y la segunda escritura pisa a la primera
o: Porque el sistema operativo sincroniza las escrituras y descarta una
a: 2
e: La operación son tres acciones (leer, restar, escribir) y el entrelazado deja que las dos lecturas ocurran antes de las dos escrituras: ambas parten de 100 y ambas escriben 70. La resta es correcta; lo que falta es exclusión mutua alrededor de la secuencia entera.
:::

:::quiz
p: Un programa tarda 10 s y el 20 % de ese tiempo es estrictamente secuencial. ¿Qué aceleración máxima permite la ley de Amdahl?
o: 5 veces, porque el 20 % secuencial pone el suelo en 2 s
o: 20 veces, una por cada 5 % de trabajo secuencial
o: No hay máximo: con suficientes núcleos la parte paralela se hace instantánea
a: 1
e: Con p = 0,8 el límite cuando n crece es 1 / (1 − p) = 5. La parte paralela sí se hace arbitrariamente rápida, pero el tiempo total nunca baja de los 2 s secuenciales, así que 10 / 2 = 5 es el techo.
:::

:::quiz
p: El hilo 1 adquiere el candado A y luego pide B; el hilo 2 adquiere B y luego pide A. ¿Qué ocurre?
o: Se produce un interbloqueo y ninguno de los dos avanza
o: El sistema operativo mata al hilo que llegó segundo y el otro continúa
o: Los dos avanzan igualmente porque cada candado es independiente
a: 1
e: Cada hilo retiene lo que el otro necesita y ambos esperan indefinidamente: es la condición clásica de interbloqueo, y no se resuelve sola. La solución es que todo el programa adquiera los candados en el mismo orden.
:::

:::practica
enunciado: Dos hilos ejecutan cada uno tres acciones (leer, sumar, escribir) sobre la misma variable. Calcula cuántos entrelazados válidos existen y cuántos de ellos pierden una actualización. ¿Cuántos quedan si se protege la secuencia completa con un candado?
pista: Se permutan las 6 acciones y se descartan las que rompen el orden interno de un hilo. Para contar los que pierden una actualización, mira en cuántos las dos lecturas preceden a las dos escrituras.
solucion: Entrelazados válidos = 6! / (3! · 3!) = 720 / 36 = 20. Pierden una actualización todos aquellos en que las dos lecturas caen antes de las dos escrituras: son 18, y en ellos los dos hilos escriben el mismo valor. Con un candado que rodea la secuencia completa, cada hilo entra entero, así que solo quedan 2 entrelazados posibles (primero uno, luego el otro) y ambos dan el resultado correcto.
:::
