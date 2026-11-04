---
id: transacciones-y-bloqueos
titulo: Transacciones, aislamiento y bloqueos
fase: 3
nivel: avanzado
rutas: [de, alg]
prerequisitos: [sql-select-y-filtros, sql-modelado-y-normalizacion]
tags: [sql, concurrencia, consistencia, bloqueos]
resumen: Agrupa varias escrituras en una unidad que se aplica entera o no se aplica, y decide qué ve la otra sesión mientras tanto para que dos procesos no se pisen el trabajo.
fuentes: ["Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 7", "Garcia-Molina, Ullman y Widom (2008), 'Database Systems: The Complete Book', caps. 18 y 19", "PostgreSQL Global Development Group, 'PostgreSQL Documentation: Concurrency Control'"]
---

## En una frase

Una transacción agrupa varias escrituras en una sola unidad —o se aplican todas o no se aplica
ninguna— y el nivel de aislamiento decide qué puede ver otra sesión mientras la primera trabaja.

## La idea

Dos cajeros cobran a la vez un ingreso en la misma cuenta. Cada uno hace lo más natural del
mundo: lee el saldo, le suma lo suyo en Python y escribe el resultado. Los dos leen 500 €. El
primero escribe 600 €; el segundo, que calculó sobre el 500 que leyó un instante antes, escribe
550 €. Los 100 € del primer ingreso **han desaparecido del sistema** y ningún programa ha dado
error. Eso es una **actualización perdida**, el fallo de concurrencia más común en cualquier
aplicación que escribe datos.

El problema no es la aritmética: es la ventana. Entre la lectura y la escritura hay un hueco en
el que cabe otra sesión, y ese hueco no se cierra con cuidado ni con buenas intenciones. La base
de datos ofrece dos herramientas distintas para cerrarlo, y confundirlas es la raíz de casi todos
los incidentes de este tema:

- **La transacción** convierte varias sentencias en una unidad atómica frente a los fallos: si el
  proceso muere a mitad, o el disco falla, o la tercera sentencia revienta, el motor deshace todo
  lo anterior. Sirve para la transferencia bancaria: restar de una cuenta y sumar a otra tienen
  que ocurrir juntos o no ocurrir.
- **El aislamiento y los bloqueos** deciden qué ve y qué puede tocar cada sesión mientras las
  demás trabajan. Sirve para la actualización perdida: dos escrituras sobre la misma fila no
  pueden basarse en la misma lectura vieja.

Son cosas independientes, y aquí está la trampa que se lleva por delante a todo el mundo: meter
el read-modify-write dentro de una transacción **no** evita la actualización perdida. Con el
nivel por defecto (READ COMMITTED en PostgreSQL y Oracle, REPEATABLE READ en MySQL InnoDB), cada
sentencia ve la última versión confirmada, pero tu lectura y tu escritura siguen siendo dos
sentencias separadas. Las dos sesiones leen antes de que la otra confirme, y la segunda escritura
pisa a la primera. La transacción te garantiza que no quede un cargo sin su abono; no te
garantiza que el número sea el correcto.

Las cuatro letras de ACID, en cristiano:

- **Atomicidad.** Todo o nada. Un `ROLLBACK` —explícito o provocado por un error— deja la base
  exactamente como estaba antes del `BEGIN`.
- **Consistencia.** Las restricciones declaradas (`NOT NULL`, `UNIQUE`, claves foráneas, `CHECK`)
  se cumplen al confirmar. Si no se cumplen, el motor rechaza el `COMMIT`.
- **Aislamiento.** El resultado de varias transacciones a la vez es equivalente a algún orden en
  serie. El nivel que elijas decide cuánto se acerca a ese ideal.
- **Durabilidad.** Lo confirmado sobrevive a un corte de luz. Se paga con escrituras en el
  registro de transacciones antes de dar el `COMMIT` por bueno.

Y una consecuencia práctica del aislamiento que conviene tener clara desde el principio: en los
motores modernos las **lecturas no bloquean a las escrituras** ni al contrario, porque el motor
guarda varias versiones de cada fila (control de concurrencia multiversión, MVCC). Un informe
largo que lee 40 millones de filas no impide que la caja siga cobrando: lee una foto del estado
tomada al empezar. Lo que sí se bloquea es **escritor contra escritor**: dos `UPDATE` sobre la
misma fila se ponen en cola, y si cada uno espera a un recurso que tiene el otro, el motor mata a
uno de los dos con un error de interbloqueo (*deadlock*) y deja seguir al otro.

:::trampa
Leer con `SELECT`, calcular en tu lenguaje y escribir con `UPDATE` es el patrón más peligroso que
existe y el que más se ve en código de producción. Arréglalo moviendo el cálculo dentro del
`UPDATE` (`SET saldo = saldo + 100`), que es una sola operación, o pidiendo el bloqueo de la fila
con `SELECT ... FOR UPDATE` si de verdad necesitas el valor en tu programa.
:::

:::nota
El nivel de aislamiento por defecto casi nunca es el que la gente cree. PostgreSQL y Oracle usan
READ COMMITTED; MySQL InnoDB, REPEATABLE READ. Y los niveles no son un botón mágico: subir a
SERIALIZABLE no elimina el problema, lo convierte en un error que el motor te devuelve y que tu
código tiene que reintentar.
:::

## Definición formal

Una **transacción** es una secuencia de operaciones que empieza con `BEGIN` y termina con
`COMMIT` (se aplica) o `ROLLBACK` (se deshace). Formalmente se exige que el historial de
operaciones sea **serializable**: que su efecto sea el mismo que el de ejecutar las transacciones
una detrás de otra en algún orden.

Dos operaciones de dos transacciones distintas **entran en conflicto** si tocan el mismo dato y
al menos una de las dos escribe. Con esas parejas se construye el grafo de conflictos, y el
criterio operativo es este:

:::formula
S es serializable  ⇔  el grafo de conflictos de S no tiene ciclos
:::

La actualización perdida es un ciclo de dos nodos: la sesión 1 escribe después de leer, la sesión
2 escribe después de leer, y ambas lecturas ocurrieron antes de la primera escritura. El
resultado pierde un incremento:

:::formula
saldo_final = saldo₀ + Δ₂   en lugar de   saldo₀ + Δ₁ + Δ₂
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `saldo₀` | Saldo de la cuenta justo antes de las dos operaciones | euros | El descuadre no cambia: lo que se pierde es el incremento, no el saldo |
| `Δ₁` | Incremento que aplica la sesión que escribe primero | euros | El descuadre crece exactamente en Δ₁: es el dinero que se evapora cuando la segunda escritura pisa la primera |
| `Δ₂` | Incremento que aplica la sesión que escribe al final, calculado sobre la lectura vieja | euros | El saldo final sube con él, y el descuadre no cambia: es el incremento que sobrevive |
| `S` | Historial: el orden real en que se ejecutaron las operaciones | no aplica | Cuantas más transacciones entrelazadas, más aristas tiene el grafo y más probable es el ciclo |
| arista del grafo | Pareja de operaciones en conflicto, con el orden observado | no aplica | Cada arista nueva es una restricción de orden que el motor debe respetar o romper |
:::

Lo que garantiza cada nivel de aislamiento, según el estándar SQL:

| Nivel | Lectura sucia | Lectura no repetible | Fila fantasma | Actualización perdida |
| --- | --- | --- | --- | --- |
| READ UNCOMMITTED | posible | posible | posible | posible |
| READ COMMITTED | no | posible | posible | posible |
| REPEATABLE READ | no | no | posible en el estándar | depende del motor |
| SERIALIZABLE | no | no | no | no |

Dos matices que la tabla no puede recoger. El primero: PostgreSQL trata READ UNCOMMITTED como
READ COMMITTED, así que la lectura sucia no existe en la práctica. El segundo: su REPEATABLE READ
va más allá del estándar y también evita las filas fantasma, a cambio de abortar la transacción
con un error de serialización cuando detecta el conflicto; ese error hay que reintentarlo, no
ignorarlo.

## Ejemplo

La cuenta `A` tiene 500,00 € y dos cajas ingresan a la vez, una 100,00 € y otra 50,00 €. Con el
patrón de leer-calcular-escribir y el nivel por defecto, el orden real es este:

1. Caja 1 lee `A` y ve 500,00. Caja 2 lee `A` y ve 500,00.
2. Caja 1 escribe 600,00 (`500,00 + 100,00`) y confirma.
3. Caja 2 escribe 550,00 (`500,00 + 50,00`) y confirma, porque calculó sobre el valor del paso 1.

El saldo final es 550,00 €, pero entre las dos cajas han entrado 150,00 €: la cuenta debería marcar
650,00 €, así que faltan 100,00 € que nadie podrá localizar mirando los movimientos, porque los dos
movimientos están registrados y los dos están mal aplicados. Da igual que las dos escrituras vayan
dentro de una transacción: el descuadre ocurre igual.

Con la suma dentro del `UPDATE` no hay hueco que aprovechar:

```
caja1: UPDATE cuentas SET saldo = saldo + 100 WHERE id = 'A';   -- 600,00
caja2: UPDATE cuentas SET saldo = saldo + 50  WHERE id = 'A';   -- 650,00
```

La segunda sentencia espera a que la primera confirme, y cuando le toca el turno lee el 600,00
que ya está escrito. Es el mismo caso de la transferencia entre cuentas, con una diferencia que
se lleva por delante un fin de semana entero: si el abono apunta a una cuenta que no existe,
`UPDATE cuentas SET saldo = saldo + 200 WHERE id = 'ZZ'` afecta a **cero filas y no da error**.
Sin transacción, el cargo ya se ha confirmado y los 200,00 € se quedan en el aire; con `BEGIN`
antes y `COMMIT` después, el mismo fallo silencioso se detecta —basta mirar cuántas filas se
escribieron— y se deshace todo con un `ROLLBACK`.

El interbloqueo aparece cuando cada sesión empieza por una fila distinta:

```
caja1: BEGIN; UPDATE cuentas SET saldo = saldo - 200 WHERE id = 'A';  -- bloquea A
caja2: BEGIN; UPDATE cuentas SET saldo = saldo - 100 WHERE id = 'B';  -- bloquea B
caja1: UPDATE cuentas SET saldo = saldo + 200 WHERE id = 'B';         -- espera a caja2
caja2: UPDATE cuentas SET saldo = saldo + 100 WHERE id = 'A';         -- espera a caja1
```

Ninguna puede avanzar y el motor no puede adivinar cuál tiene razón: mata una de las dos y
devuelve un error de interbloqueo. La otra continúa. Por eso una transacción de este tipo siempre
se envuelve en un bucle de reintentos, y por eso conviene que todas las sesiones toquen las filas
**en el mismo orden** (por ejemplo, siempre la cuenta con el identificador menor primero): con un
orden fijo, el ciclo no se puede formar.

:::figura
fichero: transacciones-lectura-perdida
pie: A la izquierda, las dos cajas leen 500 € antes de que ninguna escriba: el intercalado que produce la actualización perdida. A la derecha, lo que cuesta repetirlo: si cada día se pierde uno de los dos ingresos, el saldo que figura en la base y el dinero que de verdad ha entrado se separan 100 € al día, y esa distancia no se recupera sola. El error no está en la aritmética sino en el hueco entre la lectura y la escritura.
fuente: figuras/transacciones-y-bloqueos-1.py
:::

## Código

```sql verificable
CREATE TABLE cuentas (id VARCHAR, saldo DECIMAL(10,2));
INSERT INTO cuentas VALUES ('A', 500.00), ('B', 300.00);
CREATE TABLE registro (paso VARCHAR, saldo_a DECIMAL(10,2), saldo_b DECIMAL(10,2));

-- 1) Media transferencia que se aborta: el cargo queda deshecho.
BEGIN TRANSACTION;
UPDATE cuentas SET saldo = saldo - 200.00 WHERE id = 'A';
ROLLBACK;
INSERT INTO registro SELECT 'tras el rollback',
    (SELECT saldo FROM cuentas WHERE id = 'A'), (SELECT saldo FROM cuentas WHERE id = 'B');

-- 2) La transferencia entera: las dos escrituras se confirman juntas.
BEGIN TRANSACTION;
UPDATE cuentas SET saldo = saldo - 200.00 WHERE id = 'A';
UPDATE cuentas SET saldo = saldo + 200.00 WHERE id = 'B';
COMMIT;
INSERT INTO registro SELECT 'tras el commit',
    (SELECT saldo FROM cuentas WHERE id = 'A'), (SELECT saldo FROM cuentas WHERE id = 'B');

-- 3) Sin transaccion, el abono no encuentra destino y no avisa: 0 filas afectadas.
UPDATE cuentas SET saldo = saldo - 200.00 WHERE id = 'A';
UPDATE cuentas SET saldo = saldo + 200.00 WHERE id = 'ZZ';
INSERT INTO registro SELECT 'sin transaccion',
    (SELECT saldo FROM cuentas WHERE id = 'A'), (SELECT saldo FROM cuentas WHERE id = 'B');

SELECT * FROM registro;
```

```python verificable
import sqlite3

# Una sola base en memoria compartida y dos conexiones: las dos cajas del ejemplo.
uri = "file:cuentas?mode=memory&cache=shared"
c1 = sqlite3.connect(uri, uri=True, isolation_level=None, timeout=0.05)
c2 = sqlite3.connect(uri, uri=True, isolation_level=None, timeout=0.05)
c1.execute("CREATE TABLE cuentas (id TEXT PRIMARY KEY, saldo INTEGER)")
c1.execute("INSERT INTO cuentas VALUES ('A', 500)")

# Leer, calcular en Python y escribir: entre la lectura y la escritura cabe la otra sesion.
leido1 = c1.execute("SELECT saldo FROM cuentas WHERE id = 'A'").fetchone()[0]
leido2 = c2.execute("SELECT saldo FROM cuentas WHERE id = 'A'").fetchone()[0]
c1.execute("UPDATE cuentas SET saldo = ? WHERE id = 'A'", (leido1 + 100,))
c2.execute("UPDATE cuentas SET saldo = ? WHERE id = 'A'", (leido2 + 50,))
print("tras leer-modificar-escribir:", c1.execute("SELECT saldo FROM cuentas WHERE id = 'A'").fetchone()[0])
# -> 550

# El motor hace la suma: leer y escribir son una sola operacion, no hay hueco.
c1.execute("UPDATE cuentas SET saldo = saldo + 100 WHERE id = 'A'")
c2.execute("UPDATE cuentas SET saldo = saldo + 50 WHERE id = 'A'")
print("tras sumar dentro del UPDATE:", c1.execute("SELECT saldo FROM cuentas WHERE id = 'A'").fetchone()[0])
# -> 700

# Un escritor bloquea al otro en vez de dejar que lo pise: esa es la parte de los bloqueos.
c1.execute("BEGIN IMMEDIATE")
c1.execute("UPDATE cuentas SET saldo = saldo - 10 WHERE id = 'A'")
try:
    c2.execute("BEGIN IMMEDIATE")
except sqlite3.OperationalError as e:
    print("la segunda sesion no puede escribir:", type(e).__name__)
# -> OperationalError
c1.execute("ROLLBACK")
print("tras el rollback:", c1.execute("SELECT saldo FROM cuentas WHERE id = 'A'").fetchone()[0])
# -> 700
```

```python ilustrativo
import psycopg2

# Toda transaccion que puede chocar con otra se reintenta: el motor no negocia, aborta.
def transferir(dsn, origen, destino, importe, intentos=3):
    for intento in range(1, intentos + 1):
        try:
            with psycopg2.connect(dsn) as con:      # BEGIN implicito, COMMIT al salir
                with con.cursor() as cur:
                    # Bloqueamos las dos filas en un orden fijo para no formar ciclos.
                    cur.execute(
                        "SELECT id, saldo FROM cuentas WHERE id IN (%s, %s) "
                        "ORDER BY id FOR UPDATE",
                        (origen, destino),
                    )
                    cur.execute("UPDATE cuentas SET saldo = saldo - %s WHERE id = %s",
                                (importe, origen))
                    cur.execute("UPDATE cuentas SET saldo = saldo + %s WHERE id = %s",
                                (importe, destino))
                    if cur.rowcount != 1:           # un UPDATE vacio no es un error
                        raise RuntimeError("la cuenta destino no existe")
            return True
        except psycopg2.errors.SerializationFailure:
            continue                                # otro intento
        except psycopg2.errors.DeadlockDetected:
            continue
    return False
```

## Errores típicos

- **Creer que la transacción evita la actualización perdida.** Envuelve el read-modify-write en
  `BEGIN` y `COMMIT` y se queda tranquilo, y el descuadre sigue ahí. La transacción protege frente
  a fallos a medias, no frente a dos sesiones que leen lo mismo. Mueve la operación dentro del
  `UPDATE` o bloquea la fila con `SELECT ... FOR UPDATE`.
- **Dar por hecho que un `UPDATE` que no encuentra filas es un error.** No lo es: afecta a cero
  filas y devuelve éxito. Si el abono de la transferencia no encontró la cuenta, el cargo se ha
  hecho igual. Comprueba el número de filas afectadas (`cursor.rowcount`, `RETURNING id`) y aborta
  la transacción si no cuadra.
- **Olvidar el `COMMIT` o dejarlo en manos del cierre de la conexión.** El trabajo se pierde, o
  peor: se confirma en un momento impredecible. Algunos clientes abren transacción de forma
  implícita al primer `INSERT` y la mantienen abierta mientras el usuario piensa; en ese rato
  retienen bloqueos y engordan el registro de transacciones.
- **Transacciones largas.** Una transacción de veinte minutos bloquea las filas que tocó, impide
  que el recolector de versiones antiguas haga su trabajo y hace que el rendimiento caiga en todo
  el motor. Abre, escribe y confirma; deja las llamadas a la red y al usuario fuera.
- **No reintentar ante un interbloqueo o un fallo de serialización.** Son errores esperados, no
  fallos del programa: el motor te está diciendo «vuelve a intentarlo». Sin bucle de reintentos
  con unas pocas pasadas y una espera creciente, el usuario ve un error cada vez que dos procesos
  se cruzan.
- **Usar `SELECT ... FOR UPDATE` en todas partes para «ir sobre seguro».** Bloquea filas que
  nadie iba a modificar, serializa consultas que podrían ir en paralelo y multiplica los
  interbloqueos. Bloquea solo las filas que vas a escribir, en un orden fijo y durante el menor
  tiempo posible.

## Comprueba que lo sabes

:::quiz
p: Con el nivel por defecto, dos sesiones hacen SELECT del saldo y después UPDATE con el valor calculado. ¿Qué garantiza la transacción que las envuelve?
o: Que las dos escrituras se apliquen en el orden correcto y el saldo final sea el esperado
o: Que o se aplican las dos escrituras o no se aplica ninguna, pero una puede pisar a la otra
o: Que la segunda sesión falla con un error de conflicto y hay que reintentarla
a: 2
e: La atomicidad es frente a fallos, no frente a concurrencia: si el proceso muere a mitad, se deshace todo, pero las dos sesiones leyeron el mismo valor y la segunda escritura sobrescribe a la primera. El error de conflicto solo aparece con niveles de aislamiento que detectan el patrón (SERIALIZABLE, o REPEATABLE READ en PostgreSQL), no con el nivel por defecto.
:::

:::quiz
p: ¿Qué cambia si escribes UPDATE cuentas SET saldo = saldo + 100 en lugar de leer el saldo, sumarlo en Python y escribirlo?
o: Nada, las dos formas hacen lo mismo y dan el mismo resultado
o: La suma ocurre dentro del motor sobre la última versión de la fila, así que no hay ventana entre leer y escribir
o: Se evita el bloqueo de fila y las dos sesiones pueden escribir a la vez sin esperarse
a: 2
e: Con la suma dentro del UPDATE no existe el hueco donde cabía la otra sesión: el motor lee y escribe la misma fila en una sola operación. No evita el bloqueo —de hecho la segunda sentencia espera a que la primera confirme— y precisamente por eso el resultado es correcto.
:::

:::quiz
p: Una transacción recibe un error de interbloqueo. ¿Qué hace el motor y qué debe hacer tu código?
o: El motor elige una transacción, la aborta y deshace sus cambios; tu código debe reintentar la transacción completa
o: El motor espera a que se libere el bloqueo y reintenta la sentencia por su cuenta
o: El motor confirma la transacción que llevaba más tiempo y aborta la otra sin deshacer nada
a: 1
e: Ante un ciclo de esperas, el motor no puede decidir cuál tiene razón: mata una de las transacciones y deshace todo lo que había hecho, así que no queda trabajo a medias. La otra continúa. El error es esperado y la reacción correcta es reintentar desde el principio, con un orden fijo de acceso a las filas para que el ciclo no se forme.
:::
