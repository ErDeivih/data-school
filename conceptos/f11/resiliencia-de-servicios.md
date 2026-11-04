---
id: resiliencia-de-servicios
titulo: Resiliencia de servicios: cortacircuitos y degradación
fase: 11
nivel: avanzado
rutas: [alg, de]
prerequisitos: [apis-rest, idempotencia-en-apis, cache-y-redis, metricas-y-alertas]
tags: [resiliencia, cortacircuitos, timeouts, degradacion, disponibilidad]
resumen: Qué hacer cuando una dependencia se pone lenta: timeouts medidos, reintentos con espera creciente y azar, cortacircuitos, cupos y degradación en vez de caída total.
fuentes: ["Nygard (2018), 'Release It! Design and Deploy Production-Ready Software'", "Beyer y otros (2016), 'Site Reliability Engineering'", "Kleppmann (2017), 'Designing Data-Intensive Applications'"]
---

## En una frase

Un servicio es resiliente cuando sigue haciendo lo importante mientras una de sus dependencias
falla: se le pone un tope al tiempo de espera, un tope a los reintentos, un tope al tráfico y,
cuando la dependencia ya está rota, se deja de llamarla y se sirve una versión peor del producto.

## La idea

Piensa en el cuadro de luz de una casa. Los automáticos no evitan el cortocircuito: evitan que el
cortocircuito queme la casa. Actúan solos, en milisegundos, y dejan el resto de la casa con luz.
Un servicio sin cortacircuitos es una casa sin plomos: cualquier aparato estropeado se lleva por
delante la instalación entera.

**Un servicio lento es peor que un servicio caído**, y esta observación sostiene todo lo demás. Si
la dependencia rechaza la conexión, el llamante lo sabe en un milisegundo, libera el recurso y
decide. Si contesta a los 30 segundos, durante esos 30 segundos cada petición tiene un hilo, una
conexión, un búfer y una entrada en una cola. El mismo tráfico consume cientos de veces más
recursos. Y como los recursos son finitos, el llamante se agota: deja de atender también las
peticiones que no dependían de nada. Ese es el **fallo en cascada**: la dependencia no se cae sola,
se lleva por delante a quien la llama y a quien llama a ese.

Son tres límites que conviene poner por separado, porque cada uno arregla una cosa distinta:

- **Al tiempo (timeout).** Una llamada no puede esperar más de lo que el conjunto se puede
  permitir. Elegir ese tope es decidir producto: marca cuánto puede tardar el peor caso que
  aceptas. Si no lo pones tú, lo pone la librería, y suele poner «espera indefinidamente».
- **A la cantidad (reintentos, concurrencia y cupos).** Reintentar es la forma más rápida de
  convertir un bache en una caída: la dependencia que ya va mal recibe más carga justo cuando
  menos puede. Los reintentos necesitan un máximo, una espera que crezca y azar para que no
  lleguen todos a la vez.
- **A la verdad (el cortacircuitos).** Cuando la tasa de fallos pasa de un umbral, el sistema deja
  de llamar. Con eso le ahorras trabajo inútil a la dependencia y devuelves el error en un
  milisegundo en vez de a los 30 segundos, que es lo que acaba protegiendo a quien llama.

**Degradar es una decisión de producto, y se toma en frío.** Un comercio electrónico tiene
catálogo, buscador, carrito, recomendaciones, cobro y correo de confirmación. El día que el motor
de recomendaciones se cae, en la ficha de producto conviene enseñar los más vendidos de la
categoría en lugar de un error 500: es peor recomendación y suficiente. El catálogo de
funciones ordenado por lo que no se puede perder, cada una con su modo degradado escrito, es parte
de la arquitectura y no del manual de guardia. Y la degradación tiene que ser **visible**: si el
usuario no nota que falta algo, nadie se entera de que el sistema lleva tres días en modo barato
([[metricas-y-alertas]]).

**Compartimentos (bulkheads).** El nombre viene de los barcos: con el casco dividido en
compartimentos estancos, una vía de agua no hunde el barco. En un servicio se traduce en recursos
separados: un grupo de conexiones por dependencia, un grupo de hilos por tipo de trabajo y cupos
de tráfico por cliente. Si el buscador y el cobro comparten el mismo grupo de conexiones, un
buscador lento deja sin conexiones al cobro, y el cobro es intocable.

**Lo que no es resiliencia.** Duplicar un servicio no lo hace resistente si el camino de reserva
nunca se ha probado: una réplica que no recibe tráfico está sin estrenar. Tener un plan escrito
que nadie ha ejecutado tampoco sirve. Y reintentar con más ganas es empujar más fuerte contra
algo que se está rompiendo. La única prueba de que un sistema aguanta es haberlo
roto a propósito, en un entorno controlado, y haber visto la degradación funcionar
([[incidentes-y-postmortem]]).

## Definición formal

**Tiempo de espera.** El timeout no se elige por gusto: sale de la distribución de latencia que ya
has medido, más un margen para el día malo.

:::formula
timeout = p99,9(latencia observada) + margen
:::

El margen cubre la varianza (una o dos desviaciones típicas de esa latencia). Y hay una segunda
condición que se olvida siempre: el timeout tiene que caber dentro del presupuesto de latencia de
quien te llama. Si prometes un p95 por debajo de 400 ms y gastas un timeout de 2 s en una
dependencia, esa promesa es imposible de cumplir.

**Cuántos recursos hacen falta.** La ley de Little relaciona las tres magnitudes de cualquier
sistema con cola. Es la cuenta que explica por qué una dependencia lenta agota el servicio:

:::formula
L = λ · W
:::

**Reintentos.** Con `R` intentos máximos y `p` la probabilidad de que un intento salga bien, la
carga que recibe la dependencia por cada petición original es:

:::formula
carga(R, p) = 1 + (1 − p) + (1 − p)² + … + (1 − p)^(R−1)
:::

**Espera creciente con azar.** Con `n` el número del intento (el primero es 0), `base` la espera
inicial y `tope` el máximo:

:::formula
espera_n = aleatorio(0, min(tope, base · 2^n))
:::

El `aleatorio` cumple una función concreta. Sin él, mil clientes que fallan a la vez reintentan a la vez y
convierten un pico en una onda que se repite; con él, el mismo tráfico se reparte por la ventana
de espera.

**El cortacircuitos.** Sobre una ventana deslizante de las últimas peticiones:

:::formula
abre si  fallos_en_ventana / total_en_ventana ≥ umbral   y   total_en_ventana ≥ minimo_muestras
:::

**Composición.** La disponibilidad de un camino se calcula encadenando componentes:

:::formula
en serie:  A = A₁ · A₂ · … · A_n        en paralelo:  A = 1 − (1 − A₁)(1 − A₂) · … · (1 − A_n)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `timeout` | Tiempo máximo que se espera una respuesta antes de abandonar | milisegundos o segundos | Al subir, cada petición retiene recursos más tiempo: menos peticiones por segundo y el servicio se agota antes. Un timeout corto de más corta llamadas que iban a salir bien y dispara reintentos |
| `λ` | Peticiones que llegan por segundo a esa dependencia | peticiones/s | Al subir, sube `L` en línea recta. Un pico de tráfico es exactamente esto: el mismo `W` con más `λ` |
| `W` | Tiempo que cada petición ocupa su recurso, incluida la espera en cola | segundos | Al subir, sube `L` en línea recta. Es la palanca que más duele: duplicar `W` duplica los recursos necesarios aunque el tráfico no cambie |
| `L` | Peticiones en vuelo a la vez: hilos, conexiones o memoria ocupada | peticiones | Si supera el tamaño del grupo de conexiones, las demás esperan en cola. La cola crece, la espera crece y el timeout mata trabajo que ya estaba hecho |
| `R` | Número máximo de intentos por petición, incluido el primero | intentos | La carga sube siempre y solo baja el error si el fallo es transitorio. Con la dependencia caída, la carga es `R` veces la original |
| `p` | Probabilidad de que un intento salga bien | tanto por uno | Al bajar, la carga sube rápido: con `R = 3`, de 1,11 llamadas con `p = 0,9` a 2,44 con `p = 0,2`. El reintento castiga más cuanto peor va la dependencia |
| `base` y `tope` | Espera inicial del reintento y espera máxima | milisegundos | `base` marca el primer respiro que le das a la dependencia; `tope` evita que la espera crezca sin límite. Si el tope supera el presupuesto de latencia del usuario, el reintento es decorativo |
| `umbral` | Proporción de fallos que abre el cortacircuitos | tanto por uno | Al bajarlo, abre antes y protege más, pero corta más veces un servicio sano |
| `minimo_muestras` | Peticiones que hacen falta en la ventana para decidir | peticiones | Al subirlo, el cortacircuitos tarda más en abrir. Con poco tráfico hay que subirlo o el aparato se abre con cuatro errores de usuario y no con una avería |
| `t_espera` | Tiempo que el cortacircuitos permanece abierto antes de probar | segundos | Al subirlo, más respiro para la dependencia y más tiempo sirviendo el modo degradado. Si es demasiado corto, el sistema vuelve a martillear una dependencia que no se ha recuperado |
| `A` | Disponibilidad de un componente o camino | tanto por uno | En serie multiplica: tres dependencias del 99,9 %, 99,9 % y 99 % dan 98,8 %. En paralelo mejora, pero solo si el fallo es independiente y hay capacidad para el que queda |
:::

## Ejemplo

Un servicio de pago que atiende 200 peticiones por segundo y depende de tres servicios en serie:
pagos (99,9 %), catálogo (99,9 %) y antifraude (99,0 %).

- La disponibilidad del camino completo es 0,999 · 0,999 · 0,99 = **0,98802**. En un mes de 720
  horas eso son **8,6 horas** en las que el pago no funciona, y el culpable no es la suma de los
  fallos de cada pieza: es la multiplicación.
- El antifraude responde en 50 ms y el grupo de conexiones tiene 50. Por la ley de Little, en
  vuelo hay 200 · 0,05 = **10 conexiones**: sobra sitio.
- El antifraude se degrada y pasa a responder en 2 s. Ahora en vuelo hacen falta 200 · 2 = **400
  conexiones**. Solo hay 50, así que se atienden 50 / 2 = **25 peticiones por segundo** y las
  otras 175 se acumulan en la cola. En 5 minutos (300 s) la cola tiene 175 · 300 = **52.500
  peticiones**, y la última de ellas esperará 52.500 / 25 = **2.100 segundos**: 35 minutos. Con un
  timeout de 1 s, las 52.500 se descartan sin llegar a usarse. El trabajo perdido no es de la
  dependencia: es tuyo, y has gastado 50 conexiones en producirlo.
- Si además cada petición reintenta 3 veces, la llegada al antifraude pasa de 200 a **600
  peticiones por segundo** y la demanda de conexiones a 600 · 2 = **1.200**. La cuenta que había
  que hacer era la de la carga, no la del número de intentos.
- El cortacircuitos se configura con umbral del 50 %, mínimo 20 muestras, ventana de 10 s y 30 s
  abierto. A 200 peticiones por segundo, las 20 muestras llegan en 0,1 s: abre casi al instante y
  durante los 30 s siguientes evita 200 · 30 = **6.000 llamadas condenadas**, que se convierten en
  6.000 errores devueltos en un milisegundo. Con la misma configuración en un servicio de 0,2
  peticiones por segundo, las 20 muestras tardan 100 s: el aparato tarda en enterarse, y eso es lo
  correcto, porque con cuatro peticiones no hay evidencia de nada.

**Degradar sale casi siempre más barato que caer.** Si el motor de recomendaciones se cae y se
sirve la lista de más vendidos con datos de hace 10 minutos, la ficha de producto sigue
funcionando. Supón que el modo degradado conserva el 40 % de la conversión del modo normal: una
hora degradada cuesta el equivalente a 0,6 horas de conversión perdida, frente a la hora entera
que cuesta un error. La diferencia entre las dos cifras es el valor del catálogo de degradación, y
se calcula antes del incidente, no durante.

:::figura
fichero: resiliencia-cortacircuitos-y-pool
pie: Izquierda, la carga que llega a una dependencia que solo aguanta 150 peticiones por segundo: con tres reintentos por petición y sin cortacircuitos se la martillea a 300 por segundo justo cuando está caída, mientras que el cortacircuitos corta en seco, deja pasar unas pocas llamadas de prueba y solo devuelve el tráfico normal cuando la dependencia responde. Derecha, la ley de Little con 200 peticiones por segundo y un grupo de 50 conexiones: por debajo de 250 ms de latencia sobra sitio y a partir de ahí se encola todo, que es exactamente lo que un timeout demasiado generoso convierte en trabajo perdido.
fuente: figuras/resiliencia-de-servicios-1.py
:::

## Código

```python verificable
# Un cortacircuitos, con el reloj inyectado para no tener que esperar de verdad.
class Cortacircuitos:
    def __init__(self, umbral_fallos=5, espera_s=2.0):
        self.umbral_fallos = umbral_fallos  # fallos consecutivos que lo abren
        self.espera_s = espera_s            # segundos que permanece abierto
        self.fallos = 0
        self.estado = "cerrado"
        self.abierto_hasta = 0.0

    def permite(self, ahora):
        # Al cumplirse la espera pasa a semiabierto: deja pasar UNA llamada de prueba.
        if self.estado == "abierto" and ahora >= self.abierto_hasta:
            self.estado = "semiabierto"
        return self.estado != "abierto"

    def registra(self, ok, ahora):
        if self.estado == "semiabierto":
            self.estado = "cerrado" if ok else "abierto"
            self.fallos = 0 if ok else self.umbral_fallos
            self.abierto_hasta = ahora + self.espera_s
            return
        if ok:
            self.fallos = 0
        else:
            self.fallos += 1
            if self.fallos >= self.umbral_fallos:
                self.estado = "abierto"
                self.abierto_hasta = ahora + self.espera_s

cb = Cortacircuitos()
for t in range(0, 9):
    if not cb.permite(t):
        print("t=%d  %-11s peticion rechazada sin llamar" % (t, cb.estado))
        continue
    ok = t >= 5                          # la dependencia se recupera en t=5
    cb.registra(ok, t)
    print("t=%d  %-11s llamada -> %s" % (t, cb.estado, "ok" if ok else "fallo"))
# -> t=4  abierto     llamada -> fallo
# -> t=5  abierto     peticion rechazada sin llamar
# -> t=6  cerrado     llamada -> ok
```

:::claves
- El reloj entra como argumento (`ahora`) en vez de leerlo con `time.time()`: así el ejemplo se
  ejecuta en un milisegundo y, sobre todo, se puede probar la transición de estados sin esperar.
  Un cortacircuitos que llama al reloj por dentro no se puede probar sin dormir el proceso.
- `permite()` cambia el estado a `semiabierto` como efecto secundario de preguntar. Es cómodo y es
  peligroso: si el código pregunta dos veces antes de llamar, deja pasar dos pruebas. En una
  versión real, la transición va con un cerrojo para que solo una petición la haga.
- En `semiabierto` una sola llamada decide: si sale bien, cierra; si sale mal, vuelve a abrir. Con
  tráfico alto conviene exigir varias pruebas seguidas, porque una única llamada que caiga en el
  momento malo reabre el circuito y el sistema se pasa el día degradado.
- El umbral está en **fallos consecutivos** para que se lea fácil, pero en producción se usa la
  proporción de fallos de una ventana deslizante con un mínimo de muestras: con el contador
  consecutivo, un servicio sano que falla una de cada tres peticiones nunca abre.
:::

```python verificable
# Reintentar no es gratis: la carga que ve la dependencia crece con cada intento.
def intentos_esperados(p_exito, reintentos):
    """1 + (1-p) + (1-p)^2 + ... : los que fallan vuelven a intentarlo."""
    return sum((1 - p_exito) ** k for k in range(reintentos))

for p in (0.99, 0.9, 0.5, 0.2, 0.0):
    print("exito %.2f -> %.2f llamadas por peticion con 3 intentos"
          % (p, intentos_esperados(p, 3)))
# -> exito 0.90 -> 1.11 llamadas por peticion con 3 intentos
# -> exito 0.20 -> 2.44 llamadas por peticion con 3 intentos
# -> exito 0.00 -> 3.00 llamadas por peticion con 3 intentos

# Ley de Little: peticiones en vuelo = llegadas por segundo * tiempo de servicio.
LLEGADAS, POOL = 200, 50
for latencia in (0.05, 0.25, 0.5, 2.0):
    en_vuelo = LLEGADAS * latencia
    print("latencia %4.2f s -> %6.1f en vuelo (pool %d): %s"
          % (latencia, en_vuelo, POOL,
             "cabe" if en_vuelo <= POOL else "AGOTADO: se encolan y el timeout los mata"))
# -> latencia 0.25 s ->   50.0 en vuelo (pool 50): cabe
# -> latencia 2.00 s ->  400.0 en vuelo (pool 50): AGOTADO: se encolan y el timeout los mata
```

```python verificable
# La disponibilidad se compone: en serie se multiplica, en paralelo se mejora.
disponibilidades = [0.999, 0.999, 0.99]      # pagos, catalogo, antifraude
en_serie = 1.0
for a in disponibilidades:
    en_serie *= a
print("tres dependencias en serie: %.5f" % en_serie)            # -> 0.98802
print("horas de degradacion al mes: %.1f" % ((1 - en_serie) * 720))  # -> 8.6

# Replicas en paralelo: solo mejora si el fallo es independiente y hay capacidad.
for n in (1, 2, 3):
    print("%d replica(s) al 99 %%: %.6f" % (n, 1 - (1 - 0.99) ** n))
# -> 2 replica(s) al 99 %: 0.999900
# -> 3 replica(s) al 99 %: 0.999999
```

:::claves
- La composición en paralelo funciona solo con fallos independientes. Si las tres réplicas están
  en la misma máquina, la misma red o el mismo proveedor, el fallo es común y la fórmula del
  paralelo es fantasía: la disponibilidad no sube, baja.
- El `1 - (1 - 0.99) ** 3` sale 0.999999 y no 0.9999990000000001 por cómo redondea la coma
  flotante. Con disponibilidades que se multiplican, nunca compares con `==`: redondea o usa una
  tolerancia ([[precision-y-error-numerico]]).
- Las tres fórmulas del bloque son de planificación, no de operación: sirven para decidir cuántas
  réplicas y qué timeout antes de escribir el código. Durante el incidente se miran los
  percentiles reales ([[cuantiles-y-percentiles]]).
:::

## Errores típicos

- **Reintentar sin espera ni tope.** Es la causa número uno de que un bache de dos minutos se
  convierta en una caída de dos horas: cuando la dependencia empieza a fallar, todos los clientes
  multiplican su tráfico a la vez. Espera creciente, azar y un máximo de intentos, siempre.
- **Reintentar en todas las capas.** Si la interfaz reintenta 3 veces, el servicio 3 veces y el
  cliente de la base de datos 3 veces, una petición se convierte en 27 llamadas. El reintento se
  decide en un solo sitio, normalmente en el borde, y las capas de dentro propagan el fallo.
- **Reintentar lo que no es idempotente.** Repetir una lectura es gratis; repetir un cobro es un
  cobro duplicado. Antes de reintentar hay que saber qué pasa al ejecutar dos veces, y eso se
  resuelve con claves de idempotencia ([[idempotencia-en-apis]]), no con fe.
- **Dejar el timeout por defecto.** Muchas librerías esperan indefinidamente y algunas usan 60
  segundos. Ese valor decide cuántas peticiones caben en vuelo, así que no puede quedar en manos
  del que escribió la librería: se mide el p99,9, se le suma margen y se comprueba que la suma
  cabe en la latencia que prometes.
- **Un cortacircuitos sin mínimo de muestras.** Con umbral del 50 % y tráfico bajo, dos errores
  seguidos de un usuario con mala conexión abren el circuito y el sistema se degrada sin que haya
  ninguna avería. El mínimo de muestras es la mitad del mecanismo.
- **Un cortacircuitos sin semiabierto.** Si solo sabe abrir y cerrar, o se queda abierto para
  siempre y el modo degradado se convierte en el modo normal, o vuelve a cerrar a ciegas y
  martillea una dependencia que sigue rota. La prueba controlada es lo que lo hace útil.
- **Compartir el grupo de conexiones entre dependencias.** El proveedor de recomendaciones lento
  consume las conexiones que necesita el cobro, y el cobro es lo que no se puede perder. Cada
  dependencia, su presupuesto de recursos ([[concurrencia-async-hilos-procesos]]).
- **Colas sin límite.** Aceptar todo el trabajo en una cola infinita convierte un pico de tráfico
  en una caída de cuatro horas, porque el trabajo viejo se ejecuta cuando ya no sirve. Cuando la
  cola supera su presupuesto, se rechaza: es más honesto un error rápido que una respuesta
  inútil ([[colas-y-mensajeria]]).
- **Degradar en silencio.** Servir datos viejos sin decirlo hace que el equipo crea que todo va
  bien y que el usuario desconfíe sin saber por qué. La degradación se mide, se registra y se
  enseña en el panel con su propia etiqueta.

## Comprueba que lo sabes

:::practica
enunciado: Un servicio recibe 300 peticiones por segundo y llama a una dependencia que responde en 80 ms, con un grupo de 40 conexiones y un timeout de 5 s. La dependencia se degrada y pasa a responder en 3 s. Calcula las conexiones en vuelo antes y después, cuántas peticiones por segundo se atienden, cuánto crece la cola en 2 minutos y qué cambiarías del timeout y de los reintentos.
pista: Aplica la ley de Little con las llegadas y el tiempo de servicio; el número de conexiones es el techo de peticiones simultáneas, no el de peticiones por segundo.
solucion: Antes: 300 · 0,08 = 24 conexiones en vuelo, cabe en las 40 (queda margen para el doble de tráfico). Después: 300 · 3 = 900 conexiones en vuelo, pero solo hay 40, así que se atienden 40 / 3 = 13,3 peticiones por segundo y las otras 286,7 se encolan: en 120 s la cola crece hasta unas 34.400 peticiones. Con un timeout de 5 s, cada petición encolada espera de media 34.400 / 13,3 = 2.586 s antes de ser atendida, así que muere por timeout muchísimo antes: el timeout de 5 s no protege nada, solo retrasa el error. Lo que hay que hacer: bajar el timeout a unos 200-300 ms (p99,9 medido más margen, dentro del presupuesto de latencia del usuario), no reintentar en el mismo camino mientras el cortacircuitos esté abierto, y separar el grupo de conexiones para que esta dependencia no consuma el del resto del servicio.
:::

:::quiz
p: Por qué un servicio lento es más peligroso que uno caído?
o: Porque los usuarios se quejan más y generan más tickets de soporte
o: Porque cada petición retiene recursos durante todo el tiempo de espera y agota al que llama
o: Porque un servicio caído siempre se recupera solo
a: 2
e: Una conexión rechazada se detecta en un milisegundo y libera el recurso al instante; una respuesta a los 30 segundos mantiene ocupados hilo, conexión y memoria durante 30 segundos por petición. Con llegadas constantes, el número de peticiones en vuelo crece en línea recta con el tiempo de servicio (ley de Little) hasta agotar el grupo de conexiones, y entonces el llamante deja de atender también lo que no dependía de esa dependencia. Que los usuarios se quejen no es el mecanismo del daño, y una caída no se arregla sola.
:::

:::quiz
p: Una dependencia falla el 80 % de las veces y cada petición la intenta 3 veces. ¿Qué carga recibe la dependencia por cada petición original?
o: 3 veces, porque hay 3 intentos
o: 1,2 veces, porque el 80 % de los reintentos no llega a hacerse
o: 2,44 veces: es la suma de las llegadas de cada intento, 1 + 0,8 + 0,64
a: 3
e: La carga esperada es la suma de la probabilidad de llegar a cada intento: el primero siempre (1), el segundo cuando falla el primero (0,8) y el tercero cuando fallan los dos (0,8 · 0,8 = 0,64). En total 2,44 llamadas por petición. Son 3 solo si la dependencia está caída del todo y ningún intento puede salir bien; y no es 1,2 porque los reintentos se hacen precisamente cuando el intento anterior ha fallado.
:::

:::quiz
p: Por qué la espera entre reintentos lleva azar (jitter) además de crecer?
o: Para que la suma de todas las esperas sea menor y el usuario espere menos
o: Para que los clientes que fallan a la vez no reintenten a la vez y no creen picos sincronizados
o: Para que el reintento parezca más lento y el usuario cancele
a: 2
e: Sin azar, mil clientes que empiezan a fallar en el mismo segundo reintentan en el mismo instante y crean una onda que se repite mientras dure el fallo: la dependencia recibe picos en vez de carga repartida. El azar no reduce la espera total ni cambia lo que ve el usuario; reparte la misma carga en el tiempo para que la dependencia pueda digerirla.
:::

:::trampa
Reintentar un error que no es transitorio. Un 400, un 401 o un 404 no se arreglan insistiendo: el
reintento solo añade carga y latencia a un fallo que va a seguir ahí. Solo se reintentan los
errores de los que cabe esperar que la siguiente vez salga bien: timeouts, cortes de conexión,
503 y errores de red. Y nunca se reintenta un 429 sin respetar la cabecera que dice cuándo volver.
:::

:::nota
El cortacircuitos protege a la dependencia, pero también te protege a ti: devolver un error en un
milisegundo libera recursos y mantiene el servicio principal en pie. Por eso se pone en el lado de
quien llama y no en el de quien falla; el que falla no está en condiciones de gestionar su propia
cola de admiradores.
:::
