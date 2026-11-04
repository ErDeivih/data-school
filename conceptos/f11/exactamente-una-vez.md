---
id: exactamente-una-vez
titulo: Entrega exactamente una vez
fase: 11
nivel: experto
rutas: [alg, de]
prerequisitos: [colas-y-mensajeria, cap-y-consistencia, idempotencia-en-apis]
tags: [distribuidos, mensajeria, deduplicacion, fiabilidad]
resumen: Reintentar da al menos una vez y no reintentar da como mucho una vez; exactamente una vez se consigue deduplicando el efecto en el punto irreversible.
fuentes: ["Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 11", "Apache Software Foundation, 'Apache Kafka Documentation' (seccion Exactly Once Semantics)"]
---

## En una frase

«Exactamente una vez» no es una garantía de que un mensaje se entregue una sola vez, sino el
resultado de aceptar que se entregará muchas veces y conseguir que repetirlo no cambie nada:
se entrega al menos una vez y el efecto ocurre exactamente una vez.

## La idea

Imagina una transferencia bancaria. Envías la orden, el banco la recibe, y justo antes de
confirmarte la respuesta se cae la red. ¿Se ejecutó la transferencia o no? Tú no lo sabes. Si
la vuelves a enviar y ya se había ejecutado, has pagado dos veces; si no la envías y no se
había ejecutado, la factura se queda sin pagar. No hay ninguna opción que sea correcta en los
dos casos, porque la información que necesitas (¿llegó?) se perdió con la respuesta. Lo mismo pasa,
punto por punto, con un mensaje en una cola:

- **Al menos una vez** (*at-least-once*): el consumidor confirma el mensaje **después** de
  procesarlo. Si se cae entre procesar y confirmar, el bróker lo reenvía. No se pierde nada,
  pero algunos mensajes se procesan dos veces.
- **Como mucho una vez** (*at-most-once*): el consumidor confirma **antes** de procesarlo (o
  el bróker borra al enviar). Si se cae, el mensaje se perdió. No hay duplicados, pero hay
  huecos.

Fíjate en que las dos garantías son fáciles y las dos son incompletas. La razón es profunda:
confirmar y procesar son dos acciones separadas y **no existe forma de hacerlas atómicas de
forma distribuida** sin un protocolo de consenso que coordine a los dos participantes. Si el
bróker y el consumidor pudieran fallar en cualquier instante entre ambas, siempre hay una
ventana en la que una se hizo y la otra no.

Esta es la misma familia de problemas que estudia
[[cap-y-consistencia]]: no puedes tenerlo todo a la vez.

La salida está en hacer **inofensivos** los reintentos, no en eliminarlos. La idea se ve muy bien
con un ejemplo de la vida diaria: un ascensor con el botón de la planta 3. Puedes pulsarlo
una vez o veinte; el ascensor viene una vez. El botón no ordena «sube», ordena «quiero estar
en la planta 3», que es un estado, no un incremento. Un botón que dijera «sube un piso» sí
sería sensible a pulsaciones repetidas. La diferencia entre ambos es toda la diferencia entre
*exactly-once* y un desastre.

En sistemas de mensajería esa idea se materializa en una **clave de deduplicación**: cada
mensaje lógico lleva un identificador estable (no uno nuevo por entrega), y el consumidor
registra qué claves ya ha aplicado. Cuando llega una entrega cuya clave ya está registrada,
la ignora y confirma. Ese registro tiene que ser **atómico con el efecto**: si apuntas la
clave y luego haces el cobro, y te caes en medio, has perdido la protección. Por eso la clave
se guarda en la misma transacción que el efecto, normalmente como índice único de la tabla
donde escribes. La prueba de que la protección funciona es inyectar el mismo mensaje dos veces y
comprobar que el efecto se aplica una sola.

Dos matices importantes que casi nadie cuenta:

1. **Dentro de un solo sistema sí existe.** Kafka consigue exactamente-una-vez *dentro de su
   propio ámbito* combinando un productor idempotente (número de secuencia por partición, de
   modo que un reintento del productor no crea un mensaje nuevo) con transacciones que
   escriben en varios temas y desplazan las compensaciones de los consumidores en la misma
   operación. Eso cubre leer de Kafka, transformar y escribir en Kafka. En cuanto tu
   consumidor hace una llamada HTTP a un tercero o escribe en una base de datos que no
   participa en la transacción, la garantía se acaba ahí.
2. **Los efectos fuera del sistema no se pueden deshacer.** Un `INSERT` duplicado se ignora;
   un correo enviado, una transferencia ejecutada o un SMS ya no se pueden deduplicar hacia
   atrás. Por eso la clave tiene que actuar **antes** del efecto irreversible, no después.

De ahí el resumen honesto: *exactly-once* de extremo a extremo hay que **construirlo** en cada
punto donde algo se vuelve irreversible; no viene incluido en ninguna pieza que se compre.

## Definición formal

Sea `M` el conjunto de mensajes lógicos que un productor emite y `E(m)` el número de veces que
el sistema ejecuta el efecto asociado al mensaje `m`.

- **Al menos una vez:** para todo `m` con `m` emitido, `E(m) ≥ 1`. Nunca se pierde un efecto,
  pero puede haber `E(m) > 1`.
- **Como mucho una vez:** para todo `m` emitido, `E(m) ≤ 1`. Nunca se duplica un efecto, pero
  puede haber `E(m) = 0`.
- **Exactamente una vez (efecto):** para todo `m` emitido, `E(m) = 1`.

Y la pieza que hace posible lo tercero a partir de lo primero es la **deduplicación**. Si el
consumidor mantiene un conjunto `V` de claves vistas, y aplica el efecto solo cuando
`clave(m) ∉ V` y a la vez añade `clave(m)` a `V`, entonces:

- La actualización de `V` y el efecto se hacen en **una sola transacción atómica**, así que no
  existe un estado intermedio observable en el que la clave esté apuntada pero el efecto no se
  haya hecho (ni al revés).
- Un reintento con la misma `clave(m)` encuentra `clave(m) ∈ V` y no vuelve a aplicar el
  efecto: `E(m)` se queda en 1.

Símbolos: `M` es el conjunto de mensajes lógicos; `E(m)` es el número de aplicaciones del
efecto del mensaje `m`; `clave(m)` es un identificador estable del mensaje lógico, **igual en
todas sus entregas**; `V` es el conjunto de claves ya aplicadas; «atómico» significa que las
dos escrituras ocurren o no ocurren, sin término medio visible.

:::aviso
La deduplicación exige guardar `V` para siempre, o al menos durante más tiempo que el
reintento más tardío posible. Si expiras las claves a los 10 minutos y un consumidor
atascado reintenta a los 40, el duplicado vuelve a entrar.
:::

## Ejemplo

Un consumidor de pagos recibe cuatro entregas, pero solo hay tres pagos distintos: la entrega
3 es un reintento de la entrega 1 porque el consumidor cayó antes de confirmar.

```
entrega  clave   importe
      1  m-77      10,00 EUR
      2  m-31       5,00 EUR
      3  m-77      10,00 EUR   <- mismo mensaje logico, nueva entrega
      4  m-40       2,00 EUR
```

- Sumando todas las entregas: 10 + 5 + 10 + 2 = **27,00 EUR**.
- Deduplicando por `clave`: 10 + 5 + 2 = **17,00 EUR**.

El primer número es lo que cobra un sistema que confía en «at-least-once» sin deduplicar: ha
cobrado 10 euros de más. El segundo es el correcto. Observa que la entrega 3 no es un error
del bróker: es el precio, perfectamente razonable, de no perder mensajes.

El error está en el consumidor, que trató cada entrega como un mensaje nuevo. El bróker hizo
exactamente lo que promete la garantía: entregar.

:::figura
fichero: exactamente-una-vez-deduplicar
pie: Izquierda, las cuatro entregas del ejemplo con su clave: dos llevan `m-77` porque la tercera es un reintento de la primera. La suma de todas las entregas cobra 27,00 EUR; deduplicando por clave se cobran 17,00 EUR, y los 10,00 EUR de diferencia son el cobro duplicado que el usuario ve y nadie le devuelve. Derecha, el mecanismo: un contador de claves vistas por cada entrega. Las dos primeras entregas (`m-77` y `m-31`) encuentran el contador a cero y suman 10 + 5; la tercera ya ve dos claves apuntadas y no suma nada; la de `m-40` lo sube a 17. Lo que hace que esto funcione no es el contador, es que apuntar la clave y cobrar ocurran en la misma transacción.
fuente: figuras/exactamente-una-vez-1.py
:::

## Código

```python verificable
import pandas as pd

# Cada reintento lleva la misma clave: el consumidor la usa para no repetir el cobro.
# La clave es del mensaje ("m-77"), no de la entrega, que puede ocurrir varias veces.
entregas = pd.DataFrame({
    "entrega": [1, 2, 3, 4],
    "clave":   ["m-77", "m-31", "m-77", "m-40"],
    "importe": [10.0, 5.0, 10.0, 2.0],
})

ingenuo = entregas.importe.sum()                            # suma todas las entregas
# drop_duplicates("clave") deja la PRIMERA fila de cada clave y descarta las demas; por eso
# la entrega 3 (m-77) desaparece. Devuelve un DataFrame nuevo, no modifica "entregas".
dedup = entregas.drop_duplicates("clave").importe.sum()     # una por mensaje logico

print("entregas recibidas:", len(entregas))                 # len() cuenta FILAS, no columnas
print("mensajes distintos:", entregas.clave.nunique())      # nunique() cuenta valores unicos
print("suma sin deduplicar:", f"{ingenuo:.2f}")
print("suma correcta     :", f"{dedup:.2f}")
```

```python verificable
# La clave se comprueba y se apunta en la misma operacion atomica. Aqui lo simulamos
# con un conjunto, que es lo que en produccion seria un indice unico en la base de datos.
def procesar(estado, clave):
    if clave in estado["vistas"]:
        return False               # ya aplicado: confirmamos y no repetimos el efecto
    # El orden importa: primero se apunta la clave y despues se aplica el efecto, y en
    # produccion las dos escrituras van en la misma transaccion.
    estado["vistas"].add(clave)
    estado["cobros"] += 1
    return True

estado = {"vistas": set(), "cobros": 0}
for clave in ["m-77", "m-77", "m-31"]:
    nuevo = procesar(estado, clave)
    resultado = "procesada" if nuevo else "ignorada "
    # estado['cobros'] va entre comillas simples porque la f-string ya usa las dobles.
    print(f"clave {clave}: {resultado} cobros {estado['cobros']}")
```

:::claves
- `drop_duplicates("clave")` se queda con la **primera** aparición y conserva el índice
  original (`1, 2, 4`): el DataFrame resultante **no** está reindexado, así que si necesitas
  posiciones seguidas hay que encadenar `.reset_index(drop=True)`.
- Ni `drop_duplicates` ni `.sum()` **modifican** `entregas`: devuelven objetos nuevos. La suma
  ingenua (27,00) sigue disponible después de calcular la deduplicada (17,00).
- El criterio de igualdad es el valor de la clave, comparado tal cual: `"m-77"` y `"M-77"` son
  mensajes distintos, y por eso la clave tiene que ser un identificador estable y normalizado,
  no un texto que alguien escriba a mano.
- En el segundo bloque, `estado["vistas"]` es un **conjunto compartido**: el estado se pasa como
  argumento y se modifica dentro de la función, así que la protección no está en la función sino
  en que la comprobación y el apunte ocurren sin que nadie más se cuele en medio.
- La simulación **no es atómica de verdad**: entre el `if` y el `.add` otro hilo podría colarse.
  Lo que la hace segura en producción es la restricción de unicidad de la base de datos, que
  convierte el segundo `INSERT` en un error.
- Cambiar el orden de las dos líneas del cuerpo (aplicar el efecto antes de apuntar la clave) no
  cambia el resultado de este ejemplo, pero **sí** rompe la garantía: un fallo entre ambas deja
  el cobro hecho y la clave sin apuntar, y el reintento vuelve a cobrarlo.
:::

```text
clave m-77: procesada  cobros 1
clave m-77: ignorada   cobros 1
clave m-31: procesada  cobros 2
```

## Errores típicos

- **Confundir la garantía del bróker con la del efecto.** Que Kafka te prometa
  exactamente-una-vez significa exactamente-una-vez **dentro de Kafka**. Tu `INSERT` en
  PostgreSQL o tu `POST` a la pasarela de pago están fuera de esa transacción y pueden
  duplicarse. Si diseñas como si la garantía cubriera el efecto, el día que se cae el
  consumidor cobras dos veces.
- **Generar la clave en el consumidor.** Si el identificador se crea al recibir la entrega
  (`uuid4()` dentro del consumidor), cada reintento obtiene una clave distinta y la
  deduplicación no sirve para nada. La clave se genera **en el productor**, una vez por
  mensaje lógico, y viaja con él en todas sus entregas.
- **Guardar la clave y hacer el efecto en dos transacciones.** Apuntar la clave, cerrar la
  transacción y después ejecutar el pago deja una ventana en la que el proceso puede morir:
  la clave está anotada, el pago no se hizo, y el reintento se ignora. Ese es el peor fallo
  posible, porque pierde el efecto **y** lo esconde.
- **Aplicar incrementos en vez de estados.** Un consumidor que hace `saldo = saldo + 10` es
  sensible a los duplicados; uno que hace `INSERT ... ON CONFLICT DO NOTHING` sobre una clave
  única, no. Siempre que puedas, escribe operaciones idempotentes y déjate de contar entregas.
- **Expirar las claves demasiado pronto.** Las claves hay que conservarlas más tiempo que el
  reintento más tardío posible, incluidas las colas de mensajes muertos que alguien reinyecta
  a mano tres días después. Si expiras a las 24 horas y hay reinyección manual, tienes
  duplicados garantizados.
- **Creer que los duplicados son improbables y no medirlos.** Un reintento por cada mil
  mensajes, con un efecto duplicado cada uno, es un 0,1 % de errores visibles al usuario sin
  que ninguna alerta suene. Mide la tasa de deduplicación (claves ignoradas partido por
  entregas recibidas): si es cero, o tu sistema no reintenta nunca (imposible) o la
  deduplicación no está haciendo nada.

:::trampa
Un `SELECT` para ver si la clave existe, seguido de un `INSERT`, no es atómico. Dos entregas
del mismo mensaje pueden ejecutarse a la vez, las dos ver el `SELECT` vacío y las dos
insertar. La protección de verdad es la **restricción de unicidad en la base de datos**
(`PRIMARY KEY` o índice único): el segundo `INSERT` falla y tú lo interpretas como «ya estaba
hecho». Comprobar antes de escribir es una carrera, no una garantía.
:::

## Comprueba que lo sabes

:::quiz
p: Un consumidor confirma el mensaje después de procesarlo y la red falla justo entre procesar y confirmar. ¿Qué pasa y qué garantía tienes?
o: El mensaje se pierde y tienes como mucho una vez
o: El mensaje se reentrega y tienes al menos una vez, con un posible efecto duplicado
o: El bróker detecta el fallo y garantiza exactamente una vez
a: 2
e: Si la confirmación no llega, el bróker solo puede suponer que el mensaje no se procesó y reenviarlo. Eso da al menos una vez con duplicados posibles. La primera opción describe al-most-once (confirmar antes de procesar) y la tercera es imposible: el bróker no sabe nada de tu efecto.
:::

:::quiz
p: ¿Por qué la clave de deduplicación tiene que generarse en el productor y no en el consumidor?
o: Porque el consumidor no tiene acceso a un generador de identificadores
o: Porque cada entrega del mismo mensaje debe llevar la misma clave para que el consumidor la reconozca
o: Porque el productor procesa menos mensajes y genera claves más rápido
a: 2
e: El propósito de la clave es identificar el mensaje lógico, no la entrega. Si se genera al consumir, cada reintento produce una clave nueva y nunca coincide con la anterior. Las otras dos opciones son detalles de rendimiento irrelevantes: lo que falla es el concepto.
:::

:::quiz
p: Tienes 500.000 mensajes al día, un 0,3 % se reentrega y cada duplicado aplicado cuesta 0,05 EUR. ¿Cuál es el coste diario de no deduplicar?
o: 75 EUR
o: 7,50 EUR
o: 0,75 EUR
a: 1
e: 500.000 por 0,003 son 1.500 reentregas, y 1.500 por 0,05 son 75 EUR al día, unos 27.000 EUR al año. La segunda opción se equivoca en un factor 10 al aplicar el porcentaje y la tercera divide por 100 de más. El orden de magnitud es lo que decide si merece la pena montar la deduplicación.
:::
