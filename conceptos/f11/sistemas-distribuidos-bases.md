---
id: sistemas-distribuidos-bases
titulo: "Sistemas distribuidos: bases"
fase: 11
nivel: avanzado
rutas: [de, alg]
prerequisitos: [colas-y-mensajeria, cache-y-redis, particionado-y-clustering]
tags: [distribuidos, replicacion, particionado, latencia]
resumen: Que cambia cuando el sistema vive en varias máquinas: particiones, réplicas, relojes que no coinciden y fallos que solo afectan a una parte.
fuentes: ["Kleppmann (2017), 'Designing Data-Intensive Applications'", "Lamport (1978), 'Time, Clocks, and the Ordering of Events in a Distributed System'"]
---

## En una frase

Un sistema distribuido es un conjunto de máquinas que se coordinan por red para parecer una
sola, y su rasgo definitorio es el **fallo parcial**: una parte funciona, otra no, y desde
fuera no siempre puedes saber cuál es cuál.

## La idea

Una máquina sola tiene una propiedad cómoda: o funciona o no funciona. Un sistema distribuido
pierde esa comodidad. Puede estar medio roto, y el síntoma que ves —una petición que tarda—
tiene varias causas incompatibles entre sí:

- La otra máquina está caída.
- Está viva pero sobrecargada y responde tarde.
- La red por el camino está perdiendo paquetes.
- Tu petición no llegó nunca.
- Llegó, se aplicó, y se perdió la respuesta.

**Un tiempo de espera agotado no distingue esos casos.** Esa incertidumbre no es un defecto de
la herramienta que uses: es intrínseca. De ahí sale la primera regla de diseño: como no puedes
saber si la operación se aplicó, haz que aplicarla dos veces sea inofensivo
([[idempotencia-y-reintentos]]).

Se reparte por tres motivos, y conviene saber cuál es el tuyo porque las técnicas son distintas:

- **Volumen:** los datos o el cálculo no caben en una máquina.
- **Disponibilidad:** quieres sobrevivir a que una máquina se muera.
- **Latencia o cercanía:** los usuarios están repartidos por el mundo y la física no se negocia.

**Particionar** (repartir) trocea los datos por una clave: cada trozo vive en un nodo. Es la
respuesta al volumen y también la que más se estropea, porque la calidad de la clave lo decide
todo. Una clave que reparte bien da nodos equilibrados; una clave con un valor popular concentra
el tráfico en un nodo (el problema de la celebridad) y una clave basada en la fecha pone todo el
trabajo del día en la partición de hoy. Y cuando añades un nodo, ¿cuántos datos se mueven? Si
repartes con el resto de la división, casi todos; con un anillo de hashing consistente, sobre
uno de cada `N`.

**Replicar** es copiar los datos en varios nodos. La forma más común es líder y seguidores: las
escrituras van al líder y las lecturas se reparten entre las copias. Eso trae un fenómeno con
nombre propio, el **retraso de replicación**: durante unos milisegundos (o segundos, si hay
carga) una copia sirve datos viejos. Un usuario que guarda su perfil, recarga la página y no ve
su cambio, está viendo ese retraso. Tres garantías de sesión lo arreglan: leer tus propias
escrituras, no retroceder en el tiempo (lecturas monótonas) y no ver el futuro
(lecturas consistentes con el prefijo).

**Los relojes no sirven para ordenar.** Dos máquinas sincronizadas por red siguen teniendo
desfases distintos, y un desfase de 100 partes por millón son casi nueve segundos al día. Si
ordenas eventos por la marca de tiempo de cada máquina, puedes decidir que un suceso ocurrió
antes que su propia causa. Para ordenar de verdad se usan relojes lógicos: contadores que
avanzan con las comunicaciones y que, como mucho, detectan la concurrencia (no dicen cuál de
dos sucesos simultáneos es primero, dicen que son simultáneos).

**Y el detalle que decide la experiencia del usuario: la cola de la distribución.** Cuando una
petición se reparte entre cien servidores y espera al más lento, la probabilidad de toparse con
uno que esté en su percentil 99 no es del 1 %: es del 63 %. La cola se multiplica con el
abanico. Por eso el percentil 99 de un sistema no es el de sus piezas.

## Definición formal

**Latencia y percentiles.** Con la latencia de cada petición ordenada de menor a mayor, `p_k` es
el valor por debajo del cual queda el `k` % de las peticiones.

- **p50 (mediana)** — el caso típico.
- **p99** — una de cada cien peticiones tarda más que esto.
- **p999** — una de cada mil.

Los usuarios no experimentan el promedio: experimentan la cola, porque los casos lentos son los
que se recuerdan y los que rompen los tiempos de espera.

**Amplificación de la cola.** Si una petición necesita que `n` servidores independientes
respondan, y la probabilidad de que uno esté en su cola sea `p`:

:::formula
P(al menos uno lento) = 1 − (1 − p)ⁿ
:::

- `n` — número de servidores a los que se consulta (el abanico).
- `p` — probabilidad de que un servidor concreto esté lento (por ejemplo, 0,01 para el p99).

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `P(al menos uno lento)` | Probabilidad de que la petición global tenga que esperar a un servidor en su cola | tanto por uno | Es la que sufre el usuario: crece muy rápido al principio y luego se satura cerca de 1 |
| `n` | Servidores que hay que consultar para completar la petición (el abanico) | servidores | Sube la probabilidad de toparse con una cola: con `p = 0,01`, de 1 servidor al 1 % a 100 servidores al 63,4 % |
| `p` | Probabilidad de que un servidor concreto esté lento en ese momento | tanto por uno | Es el percentil que eliges como «lento»: `p = 0,01` es el p99 y `p = 0,001` el p999. Bajarlo es la palanca más eficaz |
:::

**El suelo de la física.** La luz en fibra óptica viaja alrededor de doscientos mil kilómetros
por segundo. Un viaje de ida y vuelta de `d` kilómetros no puede bajar de:

:::formula
RTT_mínimo ≈ 2 · d / 200 000    (en segundos, con d en kilómetros)
:::

Para 6.000 km, eso son unos 60 ms. Ninguna optimización de software baja de ahí: si necesitas
menos, hay que acercar los datos al usuario, no reescribir la consulta.

**Desfase de reloj.** Con un error de `δ` partes por millón durante un tiempo `t`:

:::formula
desfase = δ · 10⁻⁶ · t
:::

**Reparto de claves.** Al pasar de `N` a `N+1` nodos:

- Con `hash mod N`, la fracción de claves que cambia de nodo es `N / (N + 1)`.
- Con hashing consistente, alrededor de `1 / (N + 1)`.

**Disponibilidad en serie y en paralelo.** Si una petición necesita `k` componentes en serie y
cada uno tiene disponibilidad `a`:

:::formula
A_serie = aᵏ          A_paralelo = 1 − (1 − a)ᵐ
:::

- `a` — fracción de tiempo que un componente responde (0,999 para «tres nueves»).
- `k` — componentes que deben responder todos, uno detrás de otro.
- `m` — copias redundantes de las que basta con que conteste una.

Con tres nueves por componente, tres componentes en serie dan 99,7 %; la redundancia en
paralelo recupera el terreno perdido.

**Cotas de la replicación.** Con replicación asíncrona, ante la caída del líder se pueden perder
las últimas escrituras; con replicación síncrona no se pierde ninguna, pero una réplica lenta
frena todas las escrituras. La elección se expresa como dos números: cuánto tiempo puedes estar
sin escribir y cuántos datos puedes permitirte perder.

## Ejemplo

**El abanico.** Una página que consulta a 1 servidor tiene un 1 % de peticiones lentas (las que
caen en el p99 de ese servidor). La misma página repartida entre 10 servicios sube al 9,6 %, y
entre 100 servicios al **63,4 %**. La página no se ha vuelto lenta por su código: se ha vuelto
lenta por la aritmética del abanico.

**Los relojes.** Un servidor con un desfase de 100 partes por millón se separa 0,36 segundos en
una hora, 8,64 segundos en un día y 60,48 segundos en una semana. Por eso una marca de tiempo
de otra máquina no puede usarse para decidir qué escritura es la última: la que parece más
nueva puede ser la más vieja. La sincronización periódica reduce el desfase (cada 64 segundos,
el error esperado baja a unos 6,4 milisegundos), pero no lo elimina ni te avisa cuando falla.

**Repartir.** Un clúster de 4 nodos que reparte por `hash mod 4` y crece a 5: se mueven el 80 %
de las claves, es decir, casi todo el conjunto de datos por la red. El mismo crecimiento con un
anillo de hashing consistente mueve alrededor del 20 %: solo lo que le tocaba al nodo nuevo.
Multiplica por terabytes y verás por qué este detalle decide si añadir una máquina es una
operación rutinaria o un fin de semana perdido.

:::figura
fichero: sistemas-distribuidos-abanico-y-reparto
pie: Izquierda, la curva que arruina las páginas que reparten trabajo: con el p99 de cada servidor en el 1 %, la probabilidad de que al menos uno esté lento pasa del 1 % con un servidor al 9,6 % con diez y al 63,4 % con cien. La línea roja marca el 50 %: a partir de unos 70 servicios, la mayoría de las peticiones espera a alguien. Derecha, lo que cuesta añadir un nodo: repartir con el resto de la división mueve el 80 % de las claves de sitio al pasar de 4 a 5 nodos, y un anillo de hashing consistente mueve el 20 %, solo el tramo del nodo nuevo.
fuente: figuras/sistemas-distribuidos-bases-1.py
:::

## Código

```python verificable
# Si una peticion espera al mas lento de n servidores, la cola se multiplica con el abanico.
def afectadas(n):
    # 0.99 es la probabilidad de que UN servidor responda dentro de su tiempo; elevarlo a n
    # supone que los n son independientes. El complemento da "al menos uno lento".
    return 1 - 0.99 ** n

for n in (1, 10, 100, 1000):
    # :>5 reserva cinco caracteres alineados a la derecha: las columnas no bailan.
    print(f"abanico {n:>5} servidores -> {100 * afectadas(n):6.1f} % de peticiones afectadas")

print(f"con 100 servicios: {100 * afectadas(100):.1f} %")   # -> 63.4 %
```

:::claves
- La cuenta **no suma probabilidades**: multiplica las de que ninguno esté lento y resta de 1.
  Con 100 servicios, `0.99 ** 100` es 0,366, así que el 63,4 % de las peticiones espera a alguno.
- El resultado se queda en el **63 %**, no en el 100 %: la cola se amplifica, pero nunca se
  vuelve certeza. Con 1.000 servicios sube al 99,996 %.
- `0.99 ** n` con `n` grande pierde precisión por redondeo del punto flotante: para 1.000
  servicios el resultado sigue siendo fiable, pero para millones conviene calcularlo con
  logaritmos o con `math.expm1`.
- La función supone que los servidores son **independientes**. Si comparten base de datos o
  pasan por el mismo conmutador, sus colas se dan a la vez y el número real es peor.
- Cambiar el `0.99` por `0.999` (percentil 99,9 en vez de 99) baja el abanico de 100 del 63,4 %
  al 9,5 %: la cola de cada pieza pesa más que el número de piezas.
:::

```python verificable
# Los relojes de dos maquinas no avanzan igual: el desfase crece mientras nadie sincronice.
desfase_ppm = 100                      # 100 partes por millon
for horas in (1, 24, 24 * 7):
    # ppm son millonésimas: 100 ppm son 100 microsegundos por segundo, o 0,36 s por hora.
    print(f"{horas:>4} h -> {desfase_ppm * horas * 3600 / 1e6:7.2f} s de desfase")

print(f"en un dia: {desfase_ppm * 24 * 3600 / 1e6:.2f} s")   # -> 8.64 s
sincronizado = desfase_ppm * 64 / 1e6 * 1000     # resincronizando cada 64 s
# El * 1000 final convierte los segundos en milisegundos: sin el, la cifra no se lee.
print(f"resincronizando cada 64 s: {sincronizado:.1f} ms de desfase esperado")   # -> 6.4 ms
```

```python verificable
import hashlib

def nodo_por_modulo(clave, n):
    # El reparto clasico: el nodo es el resto de dividir la clave. Cambia n y cambia casi todo.
    return clave % n

def anillo(nodos, replicas=100):
    """Cada nodo se representa con 100 puntos virtuales repartidos por el anillo."""
    puntos = []
    for nodo in nodos:
        for r in range(replicas):
            # El hash se calcula sobre el TEXTO "nodo#replica". [:8] se queda con los 8 primeros
            # caracteres hex (32 bits) y int(..., 16) los interpreta en base 16: un entero.
            h = int(hashlib.sha256(f"{nodo}#{r}".encode()).hexdigest()[:8], 16)
            puntos.append((h, nodo))
    # sorted() ordena por el hash y deja el anillo listo para buscar en el.
    return sorted(puntos)

def nodo_por_anillo(clave, puntos):
    # La clave se hashea igual que los nodos, para que ambos vivan en el mismo espacio.
    h = int(hashlib.sha256(str(clave).encode()).hexdigest()[:8], 16)
    for posicion, nodo in puntos:        # primer punto a la derecha de la clave
        if posicion >= h:
            return nodo
    return puntos[0][1]                  # la clave da la vuelta al anillo

claves = list(range(20_000))
# range(4) y range(5) son los nodos 0..3 y 0..4: el mismo clúster antes y despues de crecer.
puntos_4, puntos_5 = anillo(range(4)), anillo(range(5))

# sum() sobre un generador de booleanos cuenta los True: True vale 1 y False vale 0.
movidas_modulo = sum(nodo_por_modulo(k, 4) != nodo_por_modulo(k, 5) for k in claves)
movidas_anillo = sum(nodo_por_anillo(k, puntos_4) != nodo_por_anillo(k, puntos_5) for k in claves)

# El anillo se reconstruye entero al cambiar de nodos; en un sistema real solo se insertan
# los puntos del nodo nuevo, que es lo que hace barato el cambio.
print(f"hash modulo, de 4 a 5 nodos: {100 * movidas_modulo / len(claves):.0f} % de claves movidas")   # -> 80 %
print(f"anillo consistente:          {100 * movidas_anillo / len(claves):.0f} % de claves movidas")   # -> 20 %
```

## Errores típicos

- **Reintentar sin pensar en duplicados.** Un tiempo de espera agotado no significa que la
  operación no se aplicara. Sin clave de idempotencia, cada reintento es un cobro más
  ([[idempotencia-y-reintentos]]).
- **Reintentar todos a la vez y sin espera.** Si mil clientes reintentan al mismo tiempo, el
  servicio que se estaba recuperando recibe el doble de carga. Espera creciente y un poco de
  aleatoriedad en el intervalo.
- **Interpretar un tiempo de espera como «está caído».** Un nodo lento y un nodo muerto se ven
  igual desde fuera. Si expulsas del clúster a cualquier nodo que tarde, pasarás el día
  moviendo datos por un problema de red de hace diez segundos.
- **Ordenar por marca de tiempo de cada máquina.** Los desfases hacen que el orden sea falso, y
  el «el último gana» descarta escrituras sin avisar. Usa relojes lógicos o un nodo que asigne
  el orden.
- **Repartir con `hash mod N`.** Cada cambio en el número de nodos mueve casi todos los datos.
  Usa hashing consistente o un mapa de particiones explícito.
- **Elegir una clave de reparto que concentra.** Un valor popular (la cuenta de la empresa más
  grande, la fecha de hoy) manda todo el tráfico a un nodo. Comprueba la distribución antes de
  poner el sistema en producción y prepara una clave compuesta para los casos calientes.
- **Replicación síncrona en todas partes por miedo a perder datos.** Una réplica lenta bloquea
  todas las escrituras: has cambiado «puedo perder los últimos milisegundos» por «no puedo
  escribir si la réplica estornuda». Decide qué necesitas de verdad por operación.
- **Usar una cola sin límite para absorber picos.** La cola convierte un problema de latencia en
  un problema de memoria, y cuando se llena se pierden mensajes en lugar de rechazarlos. Es
  mejor rechazar pronto (y avisar) que acumular tarde.

## Comprueba que lo sabes

:::quiz
p: Una página consulta a 100 servicios en paralelo y necesita la respuesta de todos. Cada servicio está en su percentil 99 el 1 % del tiempo. ¿Qué porcentaje de peticiones de la página será lento?
o: El 1 %, porque cada servicio solo está lento el 1 % del tiempo
o: Alrededor del 63 %, porque basta con que un servicio esté lento
o: El 100 %, porque los fallos se suman
a: 2
e: La probabilidad de que ninguno esté lento es 0,99 elevado a 100, un 36,6 %. El resto, el 63,4 %, tiene al menos un servicio en su cola y espera a que termine. La cola se amplifica con el abanico: es la razón de que los sistemas grandes midan percentiles altos y no medias.
:::

:::quiz
p: Haces una petición de escritura y se agota el tiempo de espera sin respuesta. ¿Qué sabes con certeza?
o: Que la escritura no se ha aplicado
o: Que no sabes si se aplicó, así que el reintento debe ser idempotente
o: Que la otra máquina está caída
a: 2
e: El tiempo agotado solo significa que no llegó la respuesta: la petición pudo no llegar, llegar y aplicarse, o aplicarse y perderse la respuesta. Como no puedes distinguirlo desde el cliente, la operación debe poder repetirse sin efectos adicionales, con una clave de idempotencia.
:::

:::quiz
p: ¿Por qué el hashing consistente mueve muchos menos datos al añadir un nodo?
o: Porque comprime las claves antes de repartirlas
o: Porque las claves se asignan al siguiente punto del anillo, así que al añadir un nodo solo cambian las que ahora caen en su tramo
o: Porque replica cada clave en todos los nodos
a: 2
e: Con el resto de la división, cambiar el divisor cambia el resultado de casi todas las claves: de 4 a 5 nodos se mueven el 80 %. Con un anillo, añadir un nodo inserta puntos nuevos y solo las claves de esos tramos cambian de dueño, alrededor de una de cada cinco.
:::

:::practica
enunciado: Un servicio necesita responder en 300 ms. Depende de tres componentes en serie, cada uno con disponibilidad del 99,9 % y una latencia p99 de 60, 90 y 40 ms. Estima la disponibilidad conjunta y la latencia p99 del conjunto, y di qué harías primero.
pista: En serie, las disponibilidades se multiplican y los tiempos se suman; el p99 del conjunto no es la suma de los p99 de cada pieza.
solucion: Disponibilidad conjunta = 0,999³ = 0,997, es decir 99,7 %: con tres nueves por pieza se pierden dos décimas. La suma de las latencias típicas es 190 ms y el presupuesto es 300 ms, así que hay margen, pero el p99 del conjunto es peor que la suma de los p99 individuales porque basta con que una pieza se ponga en su cola. Lo primero no es optimizar: es medir cuál de las tres domina la cola (con trazas) y decidir si alguna se puede cachear, paralelizar o convertir en opcional.
:::

:::aviso
La disponibilidad de un sistema nunca es mayor que la del componente que está en serie con
todo lo demás. Antes de añadir réplicas y reintentos, busca el punto único: la base de datos
sin conmutación, el servicio de identidad, la pieza que todos necesitan y que nadie replica.
:::
