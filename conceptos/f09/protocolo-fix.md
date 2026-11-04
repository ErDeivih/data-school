---
id: protocolo-fix
titulo: Protocolo FIX
fase: 9
nivel: experto
rutas: [quant]
prerequisitos: [microestructura-de-mercado, order-book-y-spread, latencia-y-ejecucion]
tags: [ejecucion, protocolos, infraestructura]
resumen: El estándar de mensajería de órdenes entre bancos, brókers y bolsas: campos numerados, byte separador y una sesión con secuencias que hay que mantener en orden.
fuentes: ["Harris (2003), 'Trading and Exchanges: Market Microstructure for Practitioners'", "Johnson (2010), 'Algorithmic Trading and DMA'"]
---

## En una frase

FIX es el idioma con el que un sistema habla con un bróker o una bolsa para mandar órdenes,
recibir ejecuciones y cancelar: mensajes de texto formados por campos numerados
`tag=valor` separados por un byte de control, dentro de una sesión con números de secuencia que
las dos partes vigilan.

## La idea

Cuando un fondo quiere comprar 200.000 acciones, no lo hace por una web. Su sistema de
ejecución envía un mensaje a la mesa del bróker y este lo enruta al mercado; las respuestas
—aceptada, parcialmente ejecutada, ejecutada, rechazada— vuelven por el mismo canal. FIX es el
formato que casi todo el mundo usa en esa conversación, y llevas usándolo sin saberlo cada vez
que tu bróker retail te muestra «orden enviada» detrás de una interfaz bonita.

El protocolo nació en 1992 impulsado por Fidelity y Salomon Brothers para conectar compradores
y vendedores sin tener que programar un formato distinto por cada contraparte, y desde
entonces lo mantiene la FIX Trading Community. Las versiones que más te vas a encontrar son
FIX 4.2 y FIX 4.4; FIX 5.0 separó la capa de sesión en un protocolo aparte (FIXT 1.1). Un
detalle que sorprende a quien llega nuevo: **el estándar no garantiza que una sesión funcione**.
Cada bolsa y cada bróker publica su propia especificación con el subconjunto de mensajes que
acepta, los valores válidos de cada campo y sus ampliaciones propietarias. «Compatible con FIX
4.4» significa poco más que «habla el idioma»; la integración de verdad se hace contra el
documento de esa contraparte.

La sintaxis es deliberadamente simple. Un mensaje es una secuencia de campos `número=valor`
separados por el byte `SOH` (0x01, el separador ASCII de cabecera), sin comillas y sin
longitudes por campo. El orden de los campos **no** es fijo, salvo el bloque de cabecera al
principio y el checksum al final: por eso todo el mundo busca por número de tag y nadie lee
por posición. Esta decisión de diseño es la que explica su éxito —se puede depurar con un
`cat` si cambias el SOH por un carácter visible— y también su límite: parsear texto es más
lento que parsear binario, y por eso en las estrategias que compiten en microsegundos se usan
protocolos binarios.

Tres capas conviene no mezclar:

1. **La capa de aplicación** son los mensajes de negocio: `35=D` para una orden nueva,
   `35=F` para cancelar, `35=G` para reemplazar y `35=8` para las ejecuciones (Execution
   Report). Cada orden vive un ciclo: nueva, aceptada, parcialmente ejecutada, ejecutada o
   cancelada, y posiblemente rechazada por el bróker o por el mercado.
2. **La capa de sesión** es la que mantiene viva la conexión: `35=A` (Logon), `35=0`
   (Heartbeat), `35=1` (TestRequest), `35=2` (ResendRequest), `35=4` (SequenceReset) y `35=5`
   (Logout). Aquí vive lo que de verdad rompe integraciones.
3. **El transporte** es lo de abajo: TCP, normalmente con TLS, a veces con un mensaje previo
   de autenticación por el mismo canal.

La parte que hay que entender bien es la de las **secuencias**, porque es la causa número uno
de sesiones caídas. Cada dirección de la conversación lleva su propio contador: los mensajes
que tú mandas van numerados 1, 2, 3… con el tag `34`, y los que recibes llevan la numeración
del otro lado. Si llega un mensaje con un número mayor que el que esperabas, hay un hueco y
debes pedir el reenvío con `35=2`; si llega un número menor, es un duplicado y hay que mirar el
tag `43` (PossDupFlag) antes de reprocesarlo, porque puedes estar ejecutando dos veces la misma
orden. Un Logon con una secuencia inesperada puede tumbar la sesión entera si tu motor no sabe
negociarlo. Y `ClOrdID` (`11`) es el identificador de negocio de **tu** orden: lo generas tú,
tiene que ser único durante toda la vida de la orden y es lo que te permite casar el
`ExecutionReport` con la orden que mandaste. Reutilizarlo es la forma más rápida de confundir
tus propias posiciones.

Una última advertencia sobre latencia, que conecta con lo que viste en
[[latencia-y-ejecucion|latencia y ejecución]]: FIX no es un protocolo de alto rendimiento por
ser un estándar. Es texto con delimitador, con campos de longitud variable, y su parsing cuesta
microsegundos que en la carrera de la cola cuentan. Los participantes que compiten en ese
terreno usan variantes binarias —SBE sobre FIX, o los protocolos propios de cada mercado— y
reservan FIX para la gestión de órdenes y la comunicación con el bróker. Para casi cualquier
otro uso, la decisión sensata es **no escribir tu propio motor**: hay implementaciones maduras
y probadas (QuickFIX y QuickFIX/n entre las libres, varias comerciales), y lo que aporta valor
es la lógica de negocio, no reinventar el parser.

## Definición formal

Un mensaje FIX es una cadena de bytes con tres partes: cabecera estándar, cuerpo y trailer. Con
`SOH` como separador:

:::formula
8=BeginString SOH 9=BodyLength SOH [35=MsgType SOH … cuerpo …] 10=CheckSum SOH
:::

- `8` (BeginString) — versión del protocolo, por ejemplo `FIX.4.4`. Va siempre el primero.
- `9` (BodyLength) — longitud en bytes del cuerpo, definida justo abajo. Va siempre el segundo.
- `35` (MsgType) — tipo de mensaje: `D`, `8`, `F`, `A`…
- `10` (CheckSum) — siempre el último campo del mensaje.

Y las dos cuentas que hay que implementar sin equivocarse:

:::formula
BodyLength = bytes desde el tag 35 hasta el SOH anterior al tag 10
:::

:::formula
CheckSum = ( Σ bytes del mensaje hasta el SOH anterior al tag 10 ) mod 256
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `8` (BeginString) | Versión del protocolo, por ejemplo `FIX.4.4` | texto | Cambia el dialecto entero: un motor que habla 4.2 no negocia 4.4 sin que se lo digan. Va siempre el primer campo |
| `9` (BodyLength) | Longitud del cuerpo, del tag 35 al SOH anterior al tag 10 | bytes, no caracteres | Uno de más o de menos y la contraparte rechaza el mensaje: no lo arregla, lo tira |
| `35` (MsgType) | Tipo de mensaje: `D` orden nueva, `8` ejecución, `F` cancelación, `A` Logon | código de una letra | Determina cómo se interpreta todo lo que viene detrás; con el tipo equivocado, los mismos tags significan otra cosa |
| `10` (CheckSum) | Suma de los bytes anteriores, módulo 256, en tres dígitos | entero 0-255 | Se escribe con ceros a la izquierda (`007`, no `7`). Si sumas el mensaje entero en vez de parar antes del tag 10, el número cambia y el mensaje se rechaza |
| `SOH` | Byte separador entre campos | 1 byte, valor 0x01 | No aparece dentro de ningún valor. Un SOH de más parte un campo en dos y todo el mensaje se lee desplazado |
| `34` (MsgSeqNum) | Número de secuencia de esa dirección de la conversación | entero creciente | Un salto hacia arriba abre un hueco y obliga a un ResendRequest; un número repetido exige mirar el flag de duplicado antes de reprocesar |
| `11` (ClOrdID) | Identificador de negocio de tu orden, generado por ti | texto único | Si se repite, dejas de poder casar los ExecutionReport con tus órdenes: es la forma más rápida de acabar con posiciones fantasma |
| `43` (PossDupFlag) | Marca de que el mensaje es un reenvío y puede estar duplicado | `Y` o `N` | Se consulta al reprocesar. Ignorarla es ejecutar dos veces la misma orden |
| `150` / `39` | ExecType y OrdStatus: qué ha pasado con la orden | códigos (`0` nueva, `F` ejecución, `1` parcial) | Ordenan la secuencia de estados; confundirlos hace que tu sistema crea que una orden parcial está completa |
| `14` / `151` | CumQty y LeavesQty: ejecutado acumulado y lo que queda | acciones o contratos | La suma de los dos es el tamaño original. Si tu contabilidad usa solo uno, o cuenta doble o pierde el resto |
:::

- `BodyLength` — número de bytes del cuerpo, **incluyendo** el `SOH` final del último campo
  del cuerpo. No entra el campo `10` ni su separador, y tampoco los campos `8` y `9`.
- `CheckSum` — suma aritmética de todos los bytes del mensaje (valores ASCII) desde el primer
  carácter del tag `8` hasta el `SOH` que precede al tag `10`, sin incluirlo, y luego módulo
  256. Se escribe siempre con tres dígitos, con ceros a la izquierda si hace falta.
- Si la suma tiene tres cifras, se escribe tal cual; si sale 7, se escribe `007`.

:::figura
fichero: protocolo-fix-sesion-y-hueco-de-secuencia
pie: Una sesión FIX en la que cada dirección lleva su propio contador: el cliente numera 6 y 7, el bróker 12 y 13, y los números conviven sin chocar. En el centro, el hueco: al bróker le llega el 13 cuando esperaba el 12, pide el reenvío con un `35=2` y recibe otra vez el 7, ahora marcado con `43=Y` (posible duplicado). Ese `43=Y` es lo que impide ejecutar dos veces la misma orden al reprocesar; ignorarlo es la forma más común de acabar con una posición duplicada.
fuente: figuras/protocolo-fix-1.py
:::

**Campos que hay que conocer de memoria** para leer un mensaje de orden: `11` ClOrdID,
`55` Symbol, `54` Side (1 = compra, 2 = venta), `38` OrderQty, `40` OrdType (1 = mercado,
2 = limitada), `44` Price, `59` TimeInForce (0 = día, 1 = hasta cancelación, 3 = inmediata o
cancela, 4 = todo o nada), `60` TransactTime. En las ejecuciones: `150` ExecType, `39`
OrdStatus, `14` CumQty (ejecutado acumulado), `151` LeavesQty (lo que queda), `6` AvgPx
(precio medio), `37` OrderID del mercado, `17` ExecID (identificador único de esa ejecución).

## Ejemplo

Un `NewOrderSingle` real, con el byte `SOH` escrito como `|` para que se pueda leer:

```text
8=FIX.4.4|9=78|35=D|49=CLIENTE|56=BOLSA|34=7|11=ORD-1|55=BBVA|54=1|38=1000|40=2|44=9.85|59=0|10=168|
```

Campo a campo:

| Tag | Nombre | En este mensaje |
| --- | --- | --- |
| 8 | BeginString | FIX.4.4, la versión del protocolo |
| 9 | BodyLength | 78 bytes de cuerpo |
| 35 | MsgType | D: orden nueva |
| 49 | SenderCompID | CLIENTE, quien envía |
| 56 | TargetCompID | BOLSA, quien recibe |
| 34 | MsgSeqNum | 7, séptimo mensaje de esta dirección |
| 11 | ClOrdID | ORD-1, identificador propio de la orden |
| 55 | Symbol | BBVA |
| 54 | Side | 1: compra (2 sería venta) |
| 38 | OrderQty | 1.000 acciones |
| 40 | OrdType | 2: limitada (1 sería a mercado) |
| 44 | Price | 9,85 |
| 59 | TimeInForce | 0: válida solo para esta sesión |
| 10 | CheckSum | 168 |

Comprobación de las dos cuentas. El cuerpo va desde `35=D` hasta el `SOH` que hay antes de
`10=168`, y sus bytes suman 78: 5 (`35=D`) + 11 (`49=CLIENTE`) + 9 (`56=BOLSA`) + 5 (`34=7`) +
9 (`11=ORD-1`) + 8 (`55=BBVA`) + 5 (`54=1`) + 8 (`38=1000`) + 5 (`40=2`) + 8 (`44=9.85`) +
5 (`59=0`). El mensaje completo ocupa 100 bytes: 10 de `8=FIX.4.4`, 5 de `9=78`, 78 de cuerpo
y 7 de `10=168`. Y la suma de los 93 bytes anteriores al campo `10` es 168 módulo 256.

La respuesta del mercado a esa orden sería un `ExecutionReport` (`35=8`) con `150=0`
(New, aceptada), `39=0` (New), `151=1000` (todo pendiente) y `37` con el identificador que le
asigne la bolsa. Cuando se ejecute la mitad, llegará otro `35=8` con `150=F`, `39=1`
(parcialmente ejecutada), `14=500`, `151=500` y `6` con el precio medio. Tu sistema tiene que
saber que esos dos mensajes se refieren a la misma orden buscando el `11` que tú enviaste.

## Código

```python verificable
SOH = "\x01"

def fix(campos):
    """Monta un mensaje FIX: longitud de cuerpo y checksum calculados de verdad."""
    cuerpo = "".join(f"{t}={v}{SOH}" for t, v in campos)
    sin_checksum = f"8=FIX.4.4{SOH}9={len(cuerpo)}{SOH}" + cuerpo
    checksum = sum(sin_checksum.encode("ascii")) % 256
    return sin_checksum + f"10={checksum:03d}{SOH}"

msg = fix([(35, "D"), (49, "CLIENTE"), (56, "BOLSA"), (34, 7), (11, "ORD-1"),
           (55, "BBVA"), (54, 1), (38, 1000), (40, 2), (44, "9.85"), (59, 0)])

print(f"bytes totales   {len(msg)}")             # -> 100
print(f"body length     {msg.split(SOH)[1]}")   # -> 9=78
print(f"checksum        {msg[-4:-1]}")          # -> 168
print(msg.replace(SOH, "|"))                     # -> 8=FIX.4.4|9=78|35=D|49=CLIENTE|56=BOLSA|34=7|11=ORD-1|55=BBVA|54=1|38=1000|40=2|44=9.85|59=0|10=168|
```

:::claves
- `SOH = "\x01"` parece un carácter raro y es solo un byte escrito en hexadecimal: vale 1 y no se ve por pantalla. Por eso el `print` final hace `msg.replace(SOH, "|")`: sin esa sustitución, la salida sale con un símbolo invisible pegado a cada valor.
- `len(cuerpo)` cuenta **caracteres de la cadena**, no bytes. Con texto ASCII coinciden; en cuanto un valor lleve una tilde o cualquier carácter no ASCII, el tag 9 dirá un número menor que los bytes reales y la contraparte rechazará el mensaje.
- El orden de las dos líneas importa: `sin_checksum` se calcula como cabecera más cuerpo y **después** se suma. El checksum no incluye el propio campo `10`, así que no se puede calcular al final y añadirlo después sin más: hay que saber dónde corta.
- `f"10={checksum:03d}"` rellena con ceros a la izquierda hasta tres dígitos. Si el checksum vale 7, escribe `007`; sin el `:03d` saldría `7` y el mensaje tendría un campo más corto del que espera el receptor.
- `sum(sin_checksum.encode("ascii"))` suma los **bytes**, y `.encode("ascii")` falla si algún valor lleva acentos. La alternativa tolerante sería `.encode("utf-8")`, pero entonces la suma se haría sobre bytes multibyte y el resultado no sería el que espera el protocolo.
- En el segundo bloque, `campo.split("=", 1)` parte solo por el **primer** igual: sin ese `1`, un valor que contenga `=` se rompería en trozos y el diccionario se quedaría con basura. Y `if campo` descarta el último elemento vacío que deja el SOH final.
:::

```python verificable
SOH = "\x01"
mensaje = ("8=FIX.4.4" + SOH + "9=78" + SOH + "35=D" + SOH + "49=CLIENTE" + SOH +
           "56=BOLSA" + SOH + "34=7" + SOH + "11=ORD-1" + SOH + "55=BBVA" + SOH +
           "54=1" + SOH + "38=1000" + SOH + "40=2" + SOH + "44=9.85" + SOH +
           "59=0" + SOH + "10=168" + SOH)

campos = dict(campo.split("=", 1) for campo in mensaje.split(SOH) if campo)

# Se busca por numero de tag, nunca por posicion: el orden no esta garantizado
print(f"tipo de mensaje  {campos['35']}")        # -> D
print(f"simbolo          {campos['55']}")        # -> BBVA
print(f"lado             {campos['54']}")        # -> 1
print(f"cantidad         {campos['38']}")        # -> 1000
print(f"precio           {campos['44']}")        # -> 9.85
print(f"tags presentes   {len(campos)}")         # -> 14

# Comprobacion del checksum del propio mensaje: 93 bytes, suma 168 modulo 256
antes_del_checksum = mensaje[:mensaje.rindex("10=")]
print(f"checksum recalculado {sum(antes_del_checksum.encode('ascii')) % 256:03d}")  # -> 168
```

## Errores típicos

- **Confundir `BodyLength` con el tamaño total del mensaje, o calcular mal el checksum.** El
  tag `9` cuenta solo desde el tag `35` hasta el `SOH` anterior a `10`: no incluye la cabecera
  ni el checksum; en el ejemplo el mensaje ocupa 100 bytes y `9` vale 78. Y la suma del
  checksum se hace hasta el `SOH` que precede al campo `10`, sin incluirlo: si sumas el mensaje
  entero, el número sale distinto y la contraparte rechaza el mensaje.
- **Reutilizar `ClOrdID`.** Es el identificador de negocio de tu orden: debe ser único durante
  toda su vida, incluidas las cancelaciones y los reemplazos. Si lo repites, no puedes casar
  los `ExecutionReport` con tus órdenes y acabas con posiciones fantasma.
- **Ignorar los números de secuencia o no responder a un `ResendRequest`.** Un hueco sin
  rellenar deja la sesión descuadrada y la contraparte puede rechazar el siguiente Logon.
  Además, al reprocesar mensajes reenviados hay que mirar el tag `43` (PossDupFlag): un
  duplicado reprocesado sin filtrar es una orden ejecutada dos veces.
- **Parsear por posición.** El orden de los campos del cuerpo no está garantizado; solo la
  cabecera va al principio y el checksum al final. Busca siempre por número de tag y trata los
  campos ausentes como ausentes, no como cadenas vacías.
- **Suponer que todos los mercados usan el mismo diccionario.** Cada bolsa y cada bróker
  publica su especificación: subconjunto de mensajes, valores válidos, tags propietarios y
  reglas de validación. Una sesión que funciona contra un bróker no se puede copiar tal cual a
  otro.
- **Creer que FIX es un protocolo de baja latencia.** Es texto con delimitador y de longitud
  variable: cómodo, ubicuo y más lento de parsear que un binario. Para competir en la cola se
  usan SBE o protocolos propios; FIX se queda como capa de gestión de órdenes.

:::practica
enunciado: Montas este NewOrderSingle, con SOH como separador: 35=D, 49=BUY, 56=SELL, 34=12, 11=X1, 55=SAN, 54=2, 38=200, 40=1. Calcula el tag 9 (BodyLength), los bytes totales del mensaje y el 34 del siguiente que envíes.
pista: Cada campo son sus caracteres más el separador; el cuerpo va del tag 35 al SOH anterior al tag 10.
solucion: El cuerpo suma 5 (35=D) + 7 (49=BUY) + 8 (56=SELL) + 6 (34=12) + 6 (11=X1) + 7 (55=SAN) + 5 (54=2) + 7 (38=200) + 5 (40=1) = 56, así que 9=56. La cabecera 8=FIX.4.4 ocupa 10 bytes con su separador, el 9=56 otros 5 y el trailer 10=xxx siete. Total: 10 + 5 + 56 + 7 = 78 bytes. Los contadores son por dirección: tu siguiente mensaje sale con 34=13.
:::

## Comprueba que lo sabes

:::quiz
p: En un mensaje FIX, ¿qué cuenta exactamente el campo 9 (BodyLength)?
o: El número total de bytes del mensaje, incluido el checksum
o: Los bytes desde el tag 35 hasta el SOH anterior al tag 10
o: El número de campos del mensaje
a: 2
e: BodyLength mide solo el cuerpo: desde el primer tag después de la cabecera estándar hasta el separador que precede al checksum. No incluye los tags 8 y 9 ni el propio 10, y no tiene nada que ver con el número de campos.
:::

:::quiz
p: ¿Por qué no se puede reutilizar el ClOrdID (tag 11) en dos órdenes distintas?
o: Porque el mercado lo usa como número de secuencia de la sesión
o: Porque es el identificador con el que casas cada ExecutionReport con tu orden, y repetirlo hace imposible saber a cuál se refiere
o: Porque el protocolo obliga a que sea un número entero creciente
a: 2
e: El ClOrdID lo genera el cliente y es la única forma de reconciliar las ejecuciones, cancelaciones y rechazos con la orden original. No es el número de secuencia (ese es el tag 34, que gestiona la sesión) y no tiene por qué ser numérico: puede ser cualquier cadena única.
:::

:::quiz
p: Llega un mensaje con MsgSeqNum mayor que el esperado. ¿Qué corresponde hacer?
o: Descartarlo y seguir, porque el hueco no afecta a las órdenes
o: Detectar el hueco y pedir el reenvío de los mensajes que faltan con un ResendRequest
o: Cerrar la sesión y volver a hacer Logon con la secuencia a cero
a: 2
e: Un hueco significa que hay mensajes que no has visto, y entre ellos puede estar la ejecución de una orden tuya. Se pide el reenvío y, al reprocesar, se comprueba el flag de posible duplicado para no ejecutar dos veces lo mismo. Cerrar la sesión no recupera los mensajes perdidos.
:::

:::aviso
Escribir tu propio motor FIX es un proyecto de meses con una depuración desagradable: casos
límite de secuencias, reenvíos, mensajes partidos entre lecturas de TCP, codificaciones de
caracteres y especificaciones particulares de cada contraparte. Salvo que tu producto sea
precisamente eso, usa una implementación probada y dedica el esfuerzo a la lógica de negocio y
a la gestión de rechazos.
:::
