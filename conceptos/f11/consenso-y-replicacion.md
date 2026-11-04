---
id: consenso-y-replicacion
titulo: Consenso y replicación
fase: 11
nivel: experto
rutas: [de, alg]
prerequisitos: [sistemas-distribuidos-bases, cap-y-consistencia]
tags: [consenso, raft, paxos, quorum]
resumen: Cómo un clúster se pone de acuerdo en un valor y en su orden: mayorías, términos, elección de líder y por qué un número par de nodos no aporta nada.
fuentes: ["Lamport (1998), 'The Part-Time Parliament'", "Ongaro, Ousterhout (2014), 'In Search of an Understandable Consensus Algorithm'", "Fischer, Lynch, Paterson (1985), 'Impossibility of Distributed Consensus with One Faulty Process'"]
---

## En una frase

El consenso es conseguir que varias máquinas, con fallos y sin reloj común, acuerden el mismo
valor y el mismo orden de valores, de modo que todas lleguen al mismo estado aplicándolos en el
mismo orden.

## La idea

El problema que resuelve el consenso se llama **máquina de estados replicada**, y su lógica es
de una simplicidad engañosa: si todas las réplicas parten del mismo estado y aplican las mismas
órdenes en el mismo orden, terminan en el mismo estado. Por tanto, no hace falta replicar el
estado: hace falta replicar **una secuencia ordenada de órdenes**. De ahí que casi todos los
problemas de coordinación se reduzcan al mismo: acordar el contenido de una entrada de un
registro ([[cap-y-consistencia]]).

Esto es lo que hay debajo de un servicio de coordinación, del metadato de un clúster de
Kubernetes, de un bloqueo distribuido y de la elección de líder de un sistema de colas. Y es
también la razón de que sea caro: cada decisión cuesta una ida y vuelta a una mayoría.

**Qué tiene que cumplir un algoritmo de consenso.** Tres propiedades, y solo dos se pueden
garantizar siempre:

- **Acuerdo:** dos nodos correctos no deciden valores distintos.
- **Validez:** el valor decidido fue propuesto por alguien.
- **Terminación:** todo nodo correcto acaba decidiendo.

El resultado clásico de Fischer, Lynch y Paterson demuestra que en un modelo totalmente
asíncrono, con un solo proceso que pueda fallar, ningún algoritmo determinista garantiza las
tres. La salida no es rendirse, es cambiar el supuesto: se acepta que la red es **parcialmente
síncrona** (tarde o temprano los mensajes llegan en un tiempo acotado) y se usan tiempos de
espera para avanzar. Eso explica el comportamiento de los sistemas reales de consenso: pueden
**quedarse parados**, pero nunca contradecirse. Renuncian a la vivacidad, jamás a la seguridad.
Un clúster que pierde la mayoría deja de aceptar escrituras y sigue diciendo la verdad.

**La pieza que lo hace posible: la mayoría.** Cualquier conjunto mayoritario de `N` nodos se
cruza con cualquier otro: dos conjuntos de más de `N/2` elementos no caben sin solaparse. Ese
solapamiento es toda la seguridad del consenso: un valor aceptado por una mayoría no puede ser
borrado por otra mayoría, porque al menos un nodo está en las dos y no puede aceptar dos cosas
contradictorias en el mismo instante lógico.

**Paxos** fue la primera solución práctica y funciona en dos fases: un proponente pide permiso
con un número de ronda y los aceptadores prometen no aceptar nada más antiguo; después propone
un valor y, si una mayoría lo acepta, queda elegido. El detalle que lo hace correcto (y difícil
de ver) es que la promesa obliga al proponente a adoptar el valor aceptado de número más alto
que le hayan contado. La dificultad de Paxos no está en el algoritmo, sino en convertirlo en un
sistema: elegir un líder estable, rellenar huecos del registro, cambiar la composición del
clúster. De ahí nació **Raft**, diseñado explícitamente para ser entendible, con un líder fuerte,
términos que funcionan como reloj lógico y un registro que se repara por comparación de
posiciones.

**Cómo elige líder Raft, en cuatro pasos.** Los seguidores esperan latidos del líder; si no
llegan en un tiempo de espera (por ejemplo, entre 150 y 300 ms, sorteado al azar por cada
nodo), uno se convierte en candidato: incrementa el término, se vota a sí mismo y pide el voto
a los demás. Un nodo concede el voto si no ha votado ya en ese término y si el registro del
candidato está al menos tan actualizado como el suyo. Con la mayoría de los votos, el candidato
pasa a líder y empieza a mandar latidos. La aleatoriedad del tiempo de espera es lo que rompe
los empates: si todos esperasen lo mismo, todos se presentarían a la vez, el voto se repartiría
y el clúster se quedaría dando vueltas.

**Y una restricción que evita perder datos:** un nodo con el registro desactualizado no puede
ganar una elección, aunque consiga votos. Si pudiera, sería un líder sin las últimas entradas
confirmadas y las sobrescribiría.

## Definición formal

**Tamaño de la mayoría y fallos tolerados.** Con `N` nodos:

:::formula
Q = ⌊N/2⌋ + 1        f = ⌊(N − 1)/2⌋        2Q > N
:::

- `Q` — votos necesarios para decidir (mayoría).
- `f` — fallos que el clúster tolera sin dejar de decidir.
- `2Q > N` — la condición de intersección: dos mayorías cualesquiera comparten al menos un nodo.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `N` | Nodos con voto del clúster (los aprendices no cuentan) | nodos | Sube la tolerancia a fallos, pero cada decisión tiene que alcanzar a más nodos y la latencia depende del más lento de la mayoría |
| `Q` | Votos necesarios para decidir: la mayoría | votos | Es `⌊N/2⌋ + 1`, no la mitad: con 4 nodos son 3. Subir `Q` (por ejemplo, exigir la unanimidad) hace la decisión más lenta sin aportar seguridad nueva |
| `f` | Fallos que el clúster tolera y sigue decidiendo | nodos | Solo sube al pasar a un número impar mayor: de 3 a 4 nodos sigue siendo 1, y de 4 a 5 pasa a 2 |
| `2Q > N` | Condición de intersección entre dos mayorías cualesquiera | — | Si deja de cumplirse, dos grupos pueden decidir cosas distintas a la vez y el consenso pierde su garantía |
:::

**Seguridad del consenso.** Si un valor `v` se elige en el término `t`, cualquier valor elegido
en un término posterior es `v`. La seguridad no depende del tiempo ni de la red: es un
invariante.

**Propiedad de coincidencia del registro.** Si dos registros contienen una entrada con el mismo
índice y el mismo término, entonces son idénticos hasta ese índice inclusive. Es lo que permite
al líder reparar un seguidor comparando posiciones en vez de copiar el registro entero.

**Restricción de elección.** Un votante concede su voto si el registro del candidato está al
menos tan actualizado como el suyo, comparando primero el término de la última entrada y
después su longitud:

:::formula
(término_último_candidato, longitud_candidato) ≥ (término_último_votante, longitud_votante)
:::

La comparación es lexicográfica: primero el término, y solo si empatan, la longitud. Un registro
más largo con entradas de un término más antiguo no gana.

**Términos como reloj lógico.** El término es un entero que solo crece. Todo mensaje lleva el
término del emisor: quien recibe un término mayor se actualiza y vuelve a ser seguidor. Quien
recibe uno menor lo ignora. Así, sin relojes sincronizados, el clúster sabe qué decisiones son
más recientes.

**Regla de confirmación.** Una entrada del índice `i` y término `t` está confirmada cuando el
líder la tiene almacenada en una mayoría **y** `t` es el término actual del líder. Las entradas
de términos anteriores se confirman de forma indirecta, al confirmarse una del término actual:
un líder no puede dar por buena una entrada antigua solo porque esté en la mayoría (podría ser
sobrescrita por un líder futuro con un registro más actualizado).

**Latencia de una escritura.** Confirmar exige `Q` respuestas; el tiempo es el del orden
estadístico `Q`-ésimo de los tiempos de ida y vuelta:

:::formula
latencia ≈ RTT del nodo número Q entre los N (el más lento de la mayoría más rápida) + fsync
:::

De ahí que la latencia de consenso no la fije el software, sino dónde estén las máquinas. Un
viaje intercontinental de ida y vuelta ronda los 100 ms: cualquier escritura que necesite una
mayoría con otro continente pagará eso, como mínimo, en cada decisión.

**Almacenamiento estable.** `currentTerm` y `votedFor` deben persistir en disco antes de
responder a cualquier mensaje. Si un nodo vota, se reinicia y olvida su voto, puede votar dos
veces en el mismo término y elegir dos líderes: dos líderes significa perder datos.

## Ejemplo

**Cuántos nodos hacen falta.** La tabla de mayorías, que además enseña por qué los números
pares no aportan nada:

| Nodos | Mayoría | Fallos tolerados |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 2 | 1 |
| 4 | 3 | 1 |
| 5 | 3 | 2 |
| 6 | 4 | 2 |
| 7 | 4 | 3 |

Un clúster de 4 tolera exactamente lo mismo que uno de 3 y necesita una máquina más, con la
latencia y el coste que eso implica. Un clúster de 2 no tolera ningún fallo: si cae uno, no hay
mayoría y el sistema se para. Por eso los tamaños reales son 3 (tolerar un fallo) o 5 (tolerar
dos).

**Una elección, con reloj.** Cinco nodos, latidos cada 50 ms, tiempos de espera sorteados entre
150 y 300 ms:

- El líder muere en el instante 1000 ms. Nadie manda latidos.
- El nodo 3 sortea el tiempo más corto y expira en 1180 ms: incrementa el término de 7 a 8, se
  vota a sí mismo y pide el voto.
- Los otros cuatro están en el término 7 y no han votado en el 8: conceden el voto.
- Con 5 votos de 5 (le basta con 3), es líder en el instante 1182 ms, un viaje de ida y vuelta
  después.
- El clúster estuvo sin aceptar escrituras unos 180 ms: el tiempo de espera que hace falta para
  distinguir «el líder ha muerto» de «el líder va lento».

Si los cinco nodos tuvieran el tiempo de espera fijado en 200 ms, expirarían los cinco a la vez,
cada uno se votaría a sí mismo, ninguno llegaría a la mayoría y repetirían la ronda
indefinidamente: un clúster vivo, con todos sus nodos sanos, incapaz de decidir nada.

**El precio en latencia.** Dentro de un centro de datos, un viaje de ida y vuelta es del orden
de un milisegundo, así que cada decisión cuesta unos pocos milisegundos más el volcado a disco.
Con las réplicas repartidas entre continentes, la misma decisión cuesta unos 100 ms. Es la razón
de que los sistemas que necesitan consenso se desplieguen con la mayoría dentro de una región y
los demás nodos como observadores o aprendices, que no votan.

:::figura
fichero: consenso-mayorias-y-eleccion
pie: Arriba, por qué los números pares no sirven para nada: de 1 a 7 nodos, la tolerancia a fallos solo sube al pasar a un impar mayor (3 tolera 1, 5 tolera 2, 7 tolera 3), así que un clúster de 4 aguanta lo mismo que uno de 3 con una máquina más. Abajo, lo que cuesta la aleatoriedad del tiempo de espera en la elección de líder: con los temporizadores sorteados entre 150 y 300 ms, solo el 1,7 % de las rondas acaba en empate; con los 200 ms fijos para todos, el 100 % de las rondas empata y el clúster se queda dando vueltas sin elegir a nadie.
fuente: figuras/consenso-y-replicacion-1.py
:::

## Código

```python verificable
# Mayoria y fallos tolerados: los numeros pares no aportan nada.
for n in range(1, 8):
    # // es la division entera: 5 // 2 da 2, no 2.5. Con / el resultado seria un float.
    mayoria = n // 2 + 1
    # (n - 1) // 2 fallos: son los que puede perder el lado mayoritario sin dejar de serlo.
    tolera = (n - 1) // 2
    print(f"N={n}  mayoria={mayoria}  fallos tolerados={tolera}")
```

:::claves
- La mayoría se calcula con **`//` (división entera)**, no con `/`. `n // 2 + 1` da la mayoría
  estricta: con `N = 4` son 3 votos, y con `N = 5` también 3.
- `tolera = (n - 1) // 2` es el suelo de la mitad menos uno, y **coincide para pares e impares
  consecutivos**: `N = 3` y `N = 4` toleran los dos 1 fallo. Eso es exactamente lo que enseña la
  tabla: el nodo de más no compra tolerancia.
- El caso `N = 2` sale con mayoría 2 y 0 fallos tolerados: si cae uno, el clúster se queda sin
  mayoría y deja de decidir. No es «tolera un fallo», es «no tolera ninguno».
- `range(1, 8)` **no incluye el 8**: la tabla de la página llega hasta 7 porque es el último
  impar con un par comparable por encima.
- Un clúster puede tener **más nodos de los que votan**: los aprendices y observadores no cuentan
  para la mayoría, así que `N` aquí es el número de votantes, no el de máquinas.
:::

```python verificable
from itertools import combinations

# Dos mayorias cualesquiera se cruzan: eso es toda la seguridad del consenso.
for n in (3, 5, 7):
    mayoria = n // 2 + 1
    # combinations devuelve tuplas de tamano "mayoria": todos los grupos que podrian decidir.
    conjuntos = list(combinations(range(n), mayoria))
    # set(a) & set(b) es la interseccion; len() cuenta cuantos nodos comparten. El min sobre
    # todas las parejas da el peor caso, que es el que importa para la seguridad.
    cruce_minimo = min(len(set(a) & set(b)) for a in conjuntos for b in conjuntos)
    print(f"N={n}: {len(conjuntos)} mayorias de tamano {mayoria},"
          f" interseccion minima entre dos = {cruce_minimo}")
```

```python verificable
import numpy as np

rng = np.random.default_rng(7)
rondas = 20_000

def empate(timeouts):
    """Hay empate si mas de un nodo expira en el mismo instante minimo."""
    # timeouts.min() da el tiempo mas corto de la ronda; la comparacion produce un array de
    # booleanos y .sum() cuenta cuantos son True. Con mas de uno, hay empate en el minimo.
    return int((timeouts == timeouts.min()).sum()) > 1

# Temporizadores sorteados por cada nodo entre 150 y 300 ms
# size=(rondas, 5) crea una matriz de 20.000 rondas por 5 nodos; integers excluye el 301.
aleatorios = rng.integers(150, 301, size=(rondas, 5))
# Temporizadores iguales para todos: el error de configuracion clasico
iguales = np.full((rondas, 5), 200)

# map aplica empate() a cada fila de la matriz; sum() cuenta cuantas rondas empataron.
print(f"timeouts aleatorios: {100 * sum(map(empate, aleatorios)) / rondas:.1f} % de rondas con empate")   # -> 1.7 %
print(f"timeouts iguales:    {100 * sum(map(empate, iguales)) / rondas:.1f} % de rondas con empate")      # -> 100.0 %
```

## Errores típicos

- **Montar un clúster de 2 o de 4 nodos.** Un clúster de 2 no tolera ningún fallo, y uno de 4
  tolera lo mismo que uno de 3 con una máquina más. Los tamaños sensatos son impares: 3 o 5.
- **Creer que el líder decide.** El líder propone y ordena; quien decide es la mayoría. Si el
  líder se queda solo con su copia, sus escrituras no están confirmadas y se perderán cuando
  otro líder con un registro más actualizado tome el mando.
- **Leer de un seguidor y esperar consistencia fuerte.** Un seguidor puede ir retrasado. Las
  lecturas linealizables se hacen pasando por el registro, confirmando con una mayoría o con un
  arriendo de líder válido; y los arriendos dependen de que los relojes no se desvíen más de lo
  previsto.
- **Implementar tu propio consenso.** Un bloqueo distribuido «con tiempo de expiración» parece
  fácil y no lo es: sin una mayoría que lo respalde, dos procesos pueden creerse dueños del
  bloqueo a la vez. Usa un servicio probado y déjalo decidir.
- **No persistir el término y el voto antes de responder.** Si el nodo se reinicia y olvida su
  voto, puede votar dos veces en el mismo término y elegir dos líderes. Es la clase de fallo
  que aparece justo cuando crees que has probado todo.
- **Dejar que el registro crezca sin límite.** El registro es la historia completa y hay que
  compactarlo con instantáneas; sin eso, un clúster de años tarda más en arrancar que en
  servir.
- **Usar consenso para todo.** Cada decisión cuesta una ida y vuelta a una mayoría. El
  consenso es para el metadato y el orden de las órdenes, no para el volumen de datos: el
  estado se replica aparte, con el registro como fuente del orden
  ([[exactamente-una-vez]]).
- **Perder la mayoría y pensar que el sistema está roto.** Si un clúster de 5 se parte 2-3, el
  lado de 3 sigue decidiendo y el de 2 deja de aceptar escrituras. Es el comportamiento
  correcto: mejor parar que contradecir.

## Comprueba que lo sabes

:::quiz
p: ¿Por qué un clúster de 4 nodos es peor elección que uno de 3?
o: Porque con 4 nodos los términos se desincronizan más
o: Porque tolera el mismo número de fallos (1) y añade una máquina más que hay que consultar y mantener
o: Porque con 4 nodos no se puede alcanzar nunca la mayoría
a: 2
e: La mayoría de 4 es 3, así que tolera 1 fallo, igual que un clúster de 3 (mayoría 2, tolera 1). No se gana tolerancia y se paga una máquina más, más latencia y más probabilidad de que algo falle. Los tamaños útiles son impares: 3 para tolerar 1 fallo, 5 para tolerar 2.
:::

:::quiz
p: ¿Por qué Raft sortea al azar el tiempo de espera de la elección en lugar de usar un valor fijo?
o: Para repartir la carga entre los nodos
o: Para que en cada ronda sea improbable que dos nodos se presenten a la vez y el voto se reparta sin mayoría
o: Porque los relojes de las máquinas no son fiables
a: 2
e: Si todos los seguidores esperan lo mismo, expiran a la vez, cada uno se vota a sí mismo y ninguno alcanza la mayoría: el clúster repite la ronda indefinidamente sin que nada esté roto. El sorteo rompe esa simetría: con cinco nodos y 151 valores posibles, el empate en el mínimo ocurre en alrededor del 2 % de las rondas, y cuando ocurre, la ronda siguiente lo resuelve con otros tiempos.
:::

:::quiz
p: Un clúster de 5 nodos se parte en dos grupos, de 3 y de 2. ¿Qué pasa?
o: Los dos grupos siguen aceptando escrituras y luego se fusionan los cambios
o: El grupo de 3 sigue decidiendo y el de 2 deja de aceptar escrituras
o: Ninguno de los dos puede decidir hasta que se recomponga la red
a: 2
e: El lado con mayoría mantiene el líder y sigue confirmando entradas; el lado minoritario no puede elegir líder ni confirmar nada, así que rechaza las escrituras y, como mucho, sirve lecturas potencialmente obsoletas. Es el precio de la seguridad: se pierde disponibilidad en la minoría para que no existan dos versiones de la verdad.
:::

:::practica
enunciado: Necesitas un servicio de coordinación para 30 microservicios repartidos entre dos centros de datos. Decide el tamaño del clúster, dónde colocar cada nodo y qué pasa cuando se corta la comunicación entre los dos centros.
pista: La latencia de una decisión la fija el nodo más lento de la mayoría, y la mayoría define quién puede seguir decidiendo.
solucion: Cinco nodos con mayoría 3: tres en el centro principal y dos en el secundario. Tolerar dos fallos cualquiera y, sobre todo, que la mayoría viva en un solo centro: si se corta la comunicación entre centros, el lado de 3 sigue decidiendo (con latencia local, unos pocos milisegundos) y el lado de 2 deja de aceptar escrituras hasta que vuelva la red. Si se repartieran los nodos 2 y 3 al revés, la mayoría estaría en el centro secundario y el principal perdería la capacidad de escribir. Colocar los tres nodos de la mayoría juntos es deliberado: un reparto simétrico entre centros obligaría a cada decisión a pagar el viaje intercontinental de ida y vuelta, y además dejaría a los dos lados sin mayoría en caso de partición.
:::

:::aviso
El consenso garantiza el orden de las decisiones, no que las acciones externas se ejecuten una
sola vez. Un líder puede morir después de decidir un cobro y antes de confirmarlo al cliente,
y el nuevo líder puede reintentarlo. Para el mundo exterior hacen falta claves de idempotencia
y, en operaciones peligrosas, un testigo de cerca (un número de generación que el recurso
externo valida) que impida que un líder antiguo siga actuando ([[exactamente-una-vez]]).
:::
