---
id: cap-y-consistencia
titulo: CAP y modelos de consistencia
fase: 11
nivel: experto
rutas: [de, alg]
prerequisitos: [sistemas-distribuidos-bases, cache-y-redis]
tags: [cap, consistencia, replicacion, quorum]
resumen: Que significan exactamente C, A y P, qué se puede y qué no cuando la red se parte, y cómo se paga la consistencia en latencia y disponibilidad.
fuentes: ["Gilbert, Lynch (2002), 'Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services'", "DeCandia y otros (2007), 'Dynamo: Amazon's Highly Available Key-value Store'"]
---

## En una frase

CAP no dice que haya que elegir dos de tres: dice que si la red se parte, cualquier nodo que
siga respondiendo tendrá que devolver datos que quizá ya no son los últimos; la pregunta útil no
es «¿consistencia o disponibilidad?» sino «¿qué le enseño al usuario mientras no puedo
coordinar?».

## La idea

El teorema nació de una conjetura de Brewer y de su demostración formal por Gilbert y Lynch, y
casi todos los resúmenes que circulan lo cuentan mal, así que conviene empezar por las tres
letras, con su significado técnico y no con el de andar por casa:

- **C, consistencia:** linealizabilidad. El sistema se comporta como si hubiera una sola copia
  del dato y cada operación surtiera efecto de forma atómica en algún instante entre su llamada
  y su respuesta. No significa «las réplicas acaban iguales» ni «todos los nodos ven lo mismo a
  la vez»: significa que nadie puede observar un orden que contradiga el tiempo real.
- **A, disponibilidad:** toda petición que llega a un nodo que no ha fallado recibe una
  respuesta que no es un error, **sin límite de tiempo**. No es «tener un 99,99 % de
  disponibilidad» ni «responder rápido»: un sistema que contesta «error, inténtalo luego» en un
  milisegundo no es disponible en el sentido de CAP.
- **P, tolerancia a particiones:** la red puede perder tantos mensajes como quiera entre grupos
  de nodos. Los nodos siguen vivos; lo que se rompe es la comunicación entre ellos.

El argumento de por qué no se pueden tener las tres es corto y merece la pena seguirlo. Imagina
que la red se parte en dos grupos. Un cliente escribe en el grupo A. Para ser linealizable, una
lectura posterior en el grupo B tiene que ver esa escritura, y para eso los dos grupos tienen
que hablarse: exactamente lo que la partición impide. Así que al grupo B solo le quedan dos
salidas: rechazar la lectura o devolver el valor antiguo. La primera pierde disponibilidad; la
segunda, consistencia. No hay una tercera.

De ahí salen tres matices que separan a quien ha entendido el teorema de quien lo repite:

1. **P no se elige.** Es una propiedad del mundo: las redes se parten, los cables se cortan y
   los conmutadores se reinician. Se elige qué hacer *cuando* pasa, no si pasa.
2. **La elección es por operación, no por sistema.** Un mismo servicio puede ser CP para el
   saldo de una cuenta (mejor un error que un saldo falso) y AP para el contador de «me gusta»
   (mejor un número desactualizado que una pantalla de error).
3. **El día a día no es CAP, es latencia.** Como las particiones son raras, el compromiso que
   se paga cada segundo es otro: si quieres más consistencia, tienes que esperar a más nodos,
   y esperar cuesta milisegundos. Eso es PACELC: ante una **P**artición eliges **A** o **C**;
   **E**n el caso normal (*else*) eliges **L**atencia o **C**onsistencia.

**Los modelos, de más fuerte a más débil.** Como «consistencia» no es una casilla que se marca,
conviene tener el catálogo ordenado, con lo que compra cada uno y lo que cuesta:

- **Linealizable:** cada lectura ve la última escritura confirmada. Exige coordinación por
  operación; si no se alcanza una mayoría, no se puede responder.
- **Secuencial:** existe un orden total de las operaciones igual para todos, pero puede no
  coincidir con el tiempo real.
- **Causal:** si un suceso precede a otro, todos los ven en ese orden; los sucesos simultáneos
  pueden verse en órdenes distintos. Es el punto dulce de muchos sistemas: preserva las
  conversaciones (una respuesta nunca aparece antes que el mensaje al que responde) sin exigir
  coordinación global.
- **Garantías de sesión:** «leo mis propias escrituras», «mis lecturas no retroceden en el
  tiempo». Son baratas y resuelven la mayoría de las quejas de usuario.
- **Consistencia eventual:** sin escrituras nuevas, las réplicas acaban coincidiendo. El
  «acaban» no tiene cota: una réplica apagada un mes sigue siendo eventualmente consistente.

**Cómo se implementa cada cosa.** La linealizabilidad se consigue con un líder que ordena las
escrituras y lecturas que confirman con una mayoría; los cuórums (`W + R > N`) consiguen algo
parecido sin líder fijo: como el conjunto que escribe y el que lee se cruzan en al menos un
nodo, la lectura puede reparar su copia con la versión más nueva. La consistencia causal se
implementa con relojes vectoriales, que detectan cuándo dos escrituras son simultáneas en vez
de fingir que una es posterior. Y la convergencia sin coordinación se consigue con estructuras
que se fusionan solas (contadores, conjuntos, registros), a cambio de limitar los tipos de datos
y arrastrar metadatos.

**El precio se paga en dos monedas.** Una es la disponibilidad: si no alcanzas una mayoría, un
sistema CP no responde. La otra es la latencia: una lectura local de una réplica cercana es
rapidísima, y una lectura que debe confirmarse con la mayoría tiene que alcanzar nodos que
pueden estar al otro lado del océano. La distancia no se negocia
([[sistemas-distribuidos-bases]]).

## Definición formal

**El teorema.** En un modelo de red asíncrona en el que los mensajes pueden perderse
indefinidamente (P), no existe ninguna implementación de un objeto de lectura y escritura que
sea a la vez linealizable (C) y disponible (A). La demostración es una reducción al absurdo:
se construye una ejecución con una partición, se escribe en un lado, se lee en el otro y se
llega a que el sistema debe violar C o rechazar la petición, violando A.

**Cuórums.** Con `N` réplicas, `W` confirmaciones exigidas a una escritura y `R` nodos
consultados en una lectura:

:::formula
W + R > N    ⟹    conjunto_escritura ∩ conjunto_lectura ≠ ∅
:::

- `N` — número de réplicas del dato.
- `W` — acuses que el cliente espera antes de dar la escritura por buena.
- `R` — réplicas que se consultan en una lectura.
- La intersección garantiza que al menos un nodo de la lectura tiene la última escritura, y la
  lectura se queda con la versión de número más alto (*read repair*).

Ojo con lo que **no** garantiza: si las escrituras no son atómicas en cada réplica, si el
conjunto de nodos cambia a mitad, o si una escritura se confirmó con `W` nodos y luego se
perdió en uno de ellos, la intersección no basta. `W + R > N` es una condición necesaria, no
una receta mágica.

**PACELC.** Se escribe como dos decisiones: `PA/EL` (disponible y de baja latencia, consistencia
eventual), `PC/EC` (consistente siempre, pagando latencia), y las combinaciones intermedias.
Nombrar un sistema con estas cuatro letras dice mucho más que decir «es AP».

**Consistencia eventual.** Para cada objeto y sin escrituras nuevas:

:::formula
lim(t → ∞) estado_réplica_i(t) = lim(t → ∞) estado_réplica_j(t)
:::

No hay cota de tiempo en la definición. Cualquier afirmación del tipo «converge en 50 ms»
depende de la implementación y de la carga, y no se deduce del modelo.

**Latencia de esperar a `W` de `N`.** Si la latencia de un nodo sigue una distribución `F` y
los nodos son independientes, la probabilidad de que la operación haya terminado en `x` es la
de que al menos `W` nodos hayan respondido antes de `x`:

:::formula
P(termina ≤ x) = Σ_{k=W}^{N} C(N, k) · F(x)ᵏ · (1 − F(x))^{N−k}
:::

- `F(x)` — probabilidad de que un nodo responda en menos de `x`.
- `C(N, k)` — combinaciones de `N` elementos tomados de `k` en `k`.
- Con `W = 1` la operación termina cuando responde el más rápido; con `W = N`, cuando responde
  el más lento.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `P(termina ≤ x)` | Probabilidad de que la operación haya terminado antes de `x` | tanto por uno | Es la curva que se lee: con `W = 1` se dispara al principio, con `W = N` se retrasa hasta el nodo más lento |
| `x` | Tiempo que llevas esperando la operación | ms | Va de 0 a 1: la probabilidad es monótona y nunca baja |
| `W` | Acuses que hay que reunir para dar la operación por buena | nodos | Sube la latencia y baja el riesgo: con `W = 1` esperas al más rápido, con `W = N` al más lento |
| `N` | Réplicas del dato | nodos | Más réplicas dan más margen de fallo, pero el orden estadístico que hay que esperar también es mayor |
| `F(x)` | Probabilidad de que **un** nodo responda en menos de `x` | tanto por uno | Es la latencia de una pieza: se mide, no se supone. Con cola, `F` crece despacio al final |
| `C(N, k)` | Combinaciones de `N` elementos tomados de `k` en `k` | número | Solo reparte el peso entre los casos de «exactamente `k` nodos rápidos» |
:::

**Anomalías de lectura obsoleta.** Con réplicas, tres clásicas:

- **Lectura sesgada:** ver la mitad de una transferencia y no la otra, un estado que nunca
  existió.
- **Actualización perdida:** dos procesos leen, modifican y escriben; la segunda escritura pisa
  la primera. Se arregla con comparar-y-escribir o con un bloqueo.
- **Escritura sesgada:** dos transacciones leen una instantánea coherente y escriben datos
  distintos que juntos rompen una invariante.

## Ejemplo

**Cuórums válidos.** Con `N = 3`, de las 9 combinaciones posibles de `W` y `R` solo 6 cumplen
`W + R > N`; con `N = 5`, 15 de 25. Las más baratas en número de respuestas son `W = 1, R = 3`
y `W = 3, R = 1`, pero no son simétricas en su significado: `W = 1` da la escritura por buena
con un solo acuse, así que si ese nodo muere antes de replicar, la escritura desaparece.
Escribe con mayoría, lee con mayoría (`W = R = 2` con `N = 3`) y tolera un fallo.

**La escritura que no se ve.** El líder confirma una escritura en el instante 100 ms y una
réplica va 400 ms por detrás. Una lectura en esa réplica a los 300 ms devuelve el valor
antiguo; a los 450 ms, también; solo a partir de los 500 ms ve el dato. Ese medio segundo es el
que produce la queja «lo he guardado y no está». La solución barata es una garantía de sesión:
el cliente recuerda la posición de su propia escritura y lee de una réplica que ya la ha
alcanzado (o del líder) durante unos segundos.

**Lo que cuesta esperar.** Con latencias de nodo que siguen una distribución con cola y mediana
de 10 ms: leer de una réplica al azar da 10,0 ms de mediana y 40,8 ms de percentil 99; esperar
a un cuórum de 3 de 5 deja la mediana igual (10,0 ms) y **mejora** la cola (21,1 ms), porque te
quedas con el tercero más rápido de cinco. Esperar al que conteste primero baja la mediana a
5,1 ms, y exigir que contesten los cinco la sube a 19,7 ms de mediana y 56,3 ms de percentil 99.
El coste real de un cuórum no está en la estadística de orden: está en que **si no alcanzas la
mayoría, no puedes responder**, y en que la mayoría puede estar lejos.

:::figura
fichero: cap-consistencia-coste-de-esperar
pie: Izquierda, las cuatro formas de leer con 5 réplicas cuyas latencias tienen cola (lognormal con mediana de 10 ms): leer de una réplica al azar deja la mediana en 10,0 ms y el p99 en 40,8 ms; esperar al más rápido baja la mediana a 5,1 ms; esperar a 3 de 5 deja la mediana igual y **mejora** la cola hasta 21,1 ms, porque te quedas con el tercero más rápido; y exigir los 5 sube la mediana a 19,7 ms y el p99 a 56,3 ms. El cuórum no se paga en la mediana, se paga en la cola y en que, si falta un nodo, no hay respuesta. Derecha, cuántas réplicas hay que consultar para que la lectura vea la última escritura: con `W + R > N` la intersección está garantizada; con `W + R ≤ N` hay parejas que no se cruzan y la lectura obsoleta deja de ser un accidente.
fuente: figuras/cap-y-consistencia-1.py
:::

## Código

```python verificable
# W + R > N hace que el conjunto que escribe y el que lee se crucen en algun nodo.
for n in (3, 5):
    # Lista por comprension con dos for anidados: recorre todas las parejas (w, r) y se queda
    # con las que cumplen la condicion. Se lee como "para cada w, para cada r, si w+r>n".
    validas = [(w, r) for w in range(1, n + 1) for r in range(1, n + 1) if w + r > n]
    print(f"N={n}: {len(validas)} combinaciones validas de {n * n}")
    # join con generador: une los textos con un espacio en vez de imprimir la lista con corchetes.
    print("  ", " ".join(f"W{w}R{r}" for w, r in validas))
    # key=lambda x: x[0] + x[1] ordena las parejas por su suma, no por el primer elemento.
    minimo = min(validas, key=lambda x: x[0] + x[1])
    print("   suma minima:", f"W{minimo[0]}R{minimo[1]}", "=", minimo[0] + minimo[1])
```

:::claves
- `min(validas, key=...)` **no** devuelve la suma: devuelve la **tupla** `(w, r)` que la minimiza,
  por eso hay que indexar `minimo[0]` y `minimo[1]` para reconstruir el texto.
- El orden de los dos `for` de la comprensión importa: el primero es el bucle externo. Si los
  cambias, la lista sale ordenada al revés (primero por `r`) aunque tenga las mismas parejas.
- `range(1, n + 1)` **no incluye** `n + 1`: sin el `+ 1` te dejarías fuera `W = N` y `R = N`, que
  son configuraciones reales (leer del líder o esperar a todos).
- `min` se queda con la **primera** pareja que alcanza la suma mínima; hay empates (con `N = 5`,
  `W1R5` y `W5R1` suman 6) y el que sale es el que aparece antes en la lista.
- Hay 6 parejas válidas con 3 réplicas, pero **no todas valen lo mismo**: `W = 1` da la escritura
  por buena con un solo acuse, así que la simetría de la suma esconde comportamientos distintos.
:::

```python verificable
# Lectura en una replica que va por detras del lider: la garantia de sesion lo evita.
escritura_ms, retraso_replica_ms = 100, 400

for t in (50, 150, 300, 450, 700):
    # La replica ha aplicado todo lo anterior a (t - retraso): la comparacion devuelve un bool.
    visible = t - retraso_replica_ms >= escritura_ms
    print(f"t={t:>4} ms  la replica ya ve la escritura: {visible}")

print("la escritura se ve a partir de:", escritura_ms + retraso_replica_ms, "ms")   # -> 500 ms
```

```python verificable
import numpy as np

rng = np.random.default_rng(0)
# Latencia de un nodo: lognormal con mediana 10 ms, una distribucion con cola como la real.
# size=(filas, columnas): cada FILA es una peticion y cada columna uno de los 5 nodos.
muestras = rng.lognormal(mean=np.log(10.0), sigma=0.6, size=(200_000, 5))
# sort con axis=1 ordena DENTRO de cada fila: asi la columna 0 es el nodo mas rapido de cada
# peticion y la 4 el mas lento. Sin axis, NumPy aplanaria la matriz y ordenaria todo junto.
ordenadas = np.sort(muestras, axis=1)

un_nodo = muestras[:, 0]         # leer de una sola replica, elegida al azar
mas_rapido = ordenadas[:, 0]     # W=1: termina cuando contesta el primero
tres_de_cinco = ordenadas[:, 2]  # cuorum: hay que esperar al tercero de cinco
los_cinco = ordenadas[:, 4]      # W=N: hay que esperar al mas lento

for nombre, serie in (("una replica al azar", un_nodo),
                      ("el mas rapido W=1 ", mas_rapido),
                      ("3 de 5 (cuorum)  ", tres_de_cinco),
                      ("los 5 (W=N)      ", los_cinco)):
    # np.median y np.percentile devuelven un escalar; el formato de la f-string lo redondea.
    print(f"{nombre}  mediana {np.median(serie):5.1f} ms   "
          f"p99 {np.percentile(serie, 99):6.1f} ms")
```

## Errores típicos

- **Leer CAP como «elige dos de tres».** P no es una casilla que se apaga; la elección es por
  operación y cambia con el tiempo. Decir «somos AP» sin decir qué pasa cuando la red se parte
  es no haber decidido nada.
- **Confundir la A de CAP con disponibilidad de servicio.** Un sistema que responde «error» no
  es disponible en el teorema, aunque su página de estado diga 99,99 %. Y al revés: cumplir la
  A de CAP no dice nada sobre la latencia.
- **Confundir la C de CAP con la C de ACID.** En ACID, la consistencia es que se respeten las
  invariantes de la base; en CAP es linealizabilidad, un orden global de las operaciones.
- **Creer que la consistencia eventual converge en milisegundos.** La definición no pone cota.
  Una réplica aislada puede volver con datos de hace días; el sistema es correcto según el
  modelo y el usuario ve datos falsos.
- **Usar «el último gana» con relojes de las máquinas.** Las marcas de tiempo tienen desfases
  de segundos: la escritura que parece más nueva puede ser la más vieja, y la otra se descarta
  en silencio. Si necesitas fusionar, usa relojes vectoriales o estructuras que combinen.
- **Configurar `W + R ≤ N` y creer que hay cuórum.** Sin intersección garantizada, una lectura
  puede caer entera en nodos que no tienen la última escritura: la lectura obsoleta deja de ser
  un accidente y pasa a ser lo normal.
- **Leer del líder y suponer que es linealizable.** Un líder depuesto puede seguir contestando
  durante un tiempo si no confirma su autoridad con una mayoría o con un arriendo válido. La
  linealizabilidad no viene de «preguntar al jefe», viene de la confirmación con la mayoría.
- **Poner una caché delante y olvidar que es una réplica más.** Una caché sin invalidación es
  una réplica con retraso infinito: el mismo problema de consistencia, con otro nombre.
  ([[cache-y-redis]])

## Comprueba que lo sabes

:::quiz
p: En el sentido del teorema CAP, ¿qué significa que un sistema sea «A», disponible?
o: Que responde en menos de 100 ms
o: Que toda petición a un nodo que no ha fallado recibe una respuesta que no es un error, sin límite de tiempo
o: Que tiene réplicas en tres centros de datos
a: 2
e: La disponibilidad de CAP es una propiedad de corrección, no de rendimiento: o respondes con un valor, o el sistema no es A. Un error rápido no cuenta como disponible, y la latencia no entra en la definición. Por eso decir «somos AP» y «tenemos 99,99 % de uptime» son dos afirmaciones distintas.
:::

:::quiz
p: Con N = 5 réplicas y W = R = 3, ¿qué garantiza la condición W + R > N y qué no?
o: Garantiza que la lectura y la escritura comparten al menos un nodo, pero no arregla que las escrituras no sean atómicas ni que los nodos cambien a mitad
o: Garantiza linealizabilidad en todos los casos
o: Garantiza que se pueden perder 3 nodos sin dejar de escribir
a: 1
e: La intersección no vacía es una condición necesaria: al menos un nodo de la lectura tiene la última versión, y la lectura se queda con la más alta. No es suficiente: hacen falta escrituras atómicas por réplica, pertenencia estable del conjunto y ausencia de fallos que rompan la intersección. Tampoco dice nada sobre cuántos nodos pueden caer: con N=5 y W=3 toleras 2 fallos en la escritura.
:::

:::quiz
p: Un sistema promete consistencia eventual. Un usuario guarda un cambio y al recargar no lo ve. ¿Qué ha fallado?
o: Nada: es el comportamiento prometido, porque la consistencia eventual no acota el tiempo de convergencia
o: El sistema incumple el teorema CAP
o: La escritura se perdió necesariamente
a: 1
e: «Eventual» significa que sin escrituras nuevas las réplicas acaban coincidiendo, sin cota de tiempo. Que la lectura caiga en una réplica retrasada es exactamente lo prometido. Lo que hay que añadir no es más consistencia global, sino una garantía de sesión: leer tus propias escrituras.
:::

:::practica
enunciado: Diseñas un servicio con dos operaciones: cobrar una suscripción y contar cuántas visitas ha tenido una página. El servicio corre en tres réplicas repartidas entre dos continentes. Decide el modelo de consistencia de cada operación, justifica el coste y di qué pasa cuando la red se parte.
pista: Pregúntate qué error es más grave: cobrar dos veces o mostrar un contador desactualizado.
solucion: El cobro necesita consistencia fuerte: una clave de idempotencia más una escritura confirmada por mayoría (W = 2 con N = 3) para que dos intentos simultáneos no generen dos cargos. Si no se alcanza la mayoría, la respuesta correcta es un error y que el cliente reintente con la misma clave: se elige C delante de A porque el daño de un cobro duplicado es peor que el de un reintento. El contador puede aceptar consistencia eventual: cada réplica acumula localmente y converge con un contador que se fusiona, de modo que ante una partición las dos partes siguen aceptando visitas y al reunirse suman. El coste: el cobro paga latencia (hay que alcanzar una mayoría, y una de las réplicas está al otro lado del océano) y el contador paga exactitud temporal, no disponibilidad.
:::

:::aviso
Las garantías de sesión («leo mis escrituras», «no retrocedo en el tiempo») resuelven la mayor
parte de las quejas reales de los usuarios sin exigir consistencia global y sin coordinación
entre continentes. Antes de subir el nivel de consistencia de todo el sistema, comprueba si el
problema se arregla recordando la posición de lectura de cada sesión.
:::
