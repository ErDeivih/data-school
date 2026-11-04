---
id: registros-rechazados-y-cuarentena
titulo: Registros rechazados, cuarentena y parada del pipeline
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [calidad-de-datos, contratos-de-datos]
tags: [pipeline, calidad, errores, cuarentena]
resumen: Qué hacer con la fila que no cumple las reglas: apartarla con su motivo, reprocesarla después o parar el lote entero cuando la tasa de rechazo deja de ser ruido.
fuentes: ["Reis & Housley (2022), 'Fundamentals of Data Engineering', cap. 8", "Moses, Gavish y Vorwerck (2022), 'Data Quality Fundamentals'", "Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 11"]
---

## En una frase

Un registro rechazado es una fila que no cumple las reglas de la tabla de destino, y lo que decidas
hacer con ella —apartarla, reintentarla o parar el pipeline entero— decide si el problema acaba
siendo un dato que falta o un dato equivocado.

## La idea

El 11 de marzo el proveedor cambia la unidad del campo `precio`: de euros a céntimos. El proceso
nocturno carga los pedidos como siempre y en el cuarto lote, de 470 filas, 140 traen un precio cien
veces mayor. Hay dos formas de reaccionar y las dos son malas:

- **Escribirlo todo.** La tabla acaba con 330 precios en euros y 140 en céntimos. Con 140 valores
  cien veces mayores, el total del lote sale unas 30 veces más alto: mezclado en un cuadro que
  agrega países y semanas, la cifra pasa desapercibida y el error se descubre tres meses después.
  Un dato equivocado es peor que un dato que falta: el que falta se nota, el equivocado se usa
  para decidir.
- **Parar al primer registro malo.** El pipeline aborta en la fila 12 y no carga nada. Durante
  semanas, un teléfono con un guion raro o un acento mal codificado bloquea los pedidos de todo el
  país. El negocio deja de recibir datos por un problema que cabía en una fila.

El camino de en medio tiene tres piezas, y las tres hacen falta:

1. **Validar en la frontera y separar en dos flujos.** El mismo predicado que decide que una fila
   es buena decide que es mala. Las buenas van a la tabla; las malas, a una tabla de cuarentena
   con el motivo. Nunca las dos, nunca ninguna.
2. **Decidir por tasa, no por caso.** Un rechazo suelto es ruido; el 30 % de un lote es una señal
   de que el origen ha cambiado. Si la tasa de rechazo supera un umbral, **no se escribe nada** y
   el lote entero se queda fuera hasta que alguien mire. Los buenos también: escribir la parte
   buena de un lote sospechoso deja la tabla a medias y sin rastro de lo que falta.
3. **Guardar el rechazo de forma que se pueda reprocesar.** La cuarentena es una tabla con el
   registro en crudo, el motivo, el lote, el instante y la localización de origen. No es un
   fichero de log: los logs rotan, nadie los lee y no se pueden consultar por «cuántos rechazos de
   este proveedor llevamos este mes».

La distinción que más cuesta interiorizar es la de **rechazo de fila** y **rechazo de lote**. Una
fila con unidades negativas o un correo sin arroba es un rechazo de fila: se aparta y el resto
sigue. Un fichero que no se puede abrir, una columna obligatoria que ya no viene, un checksum que
no cuadra o un esquema distinto del contratado son rechazos de **lote**: no hay nada que rescatar,
y meter medio millón de filas en cuarentena no ayuda a nadie. En ese caso se aparta el lote
completo —el fichero, la partición, lo que sea— y se avisa; lo que no se hace es escribir la mitad
de un lote que no se entiende.

La cuarentena tiene un requisito que se olvida y que la convierte en un agujero negro: **alguien
tiene que reprocesarla**. Un proceso que la vacía periódicamente, un informe de su tamaño y una
alerta cuando crece. Si nadie mira, el dato rechazado es una pérdida silenciosa que se descubre
seis meses después, cuando ya no se puede reconstruir. Y para reprocesar hace falta que la
escritura sea idempotente: reinsertar sin duplicar depende de una clave de destino, no de la suerte
(es el mismo problema que resuelve [[idempotencia-y-reintentos]]).

:::trampa
El umbral no es una constante universal. Con lotes de tamaños distintos, el mismo número absoluto
de rechazos da tasas muy distintas: 10 rechazos son el 10 % de un lote de 100 y el 0,001 % de uno
de un millón. Y un umbral fijo se queda corto cuando el volumen crece: lo que de verdad avisa es
la **desviación respecto a la línea base reciente**, no el valor absoluto. Si el mes pasado la
tasa era del 0,2 % y hoy es del 2 %, hay un problema aunque el umbral sea del 5 %.
:::

## Definición formal

Sea `N` el número de registros que entran en un lote y `R` los que no cumplen alguna regla. La tasa
de rechazo del lote es:

:::formula
tasa_rechazo = R / N
:::

Y la decisión del pipeline se escribe así:

:::formula
si R / N > umbral  ⇒  0 filas escritas, lote apartado y salida con código distinto de cero;  si no  ⇒  N − R a la tabla y R a cuarentena
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `N` | Registros que entran en el lote | filas | El umbral se vuelve menos sensible: el mismo número absoluto de rechazos pesa menos y el pipeline tolera más defecto real |
| `R` | Registros que no cumplen ninguna regla y se apartan | filas | Más filas en cuarentena y la tasa sube; si cruza el umbral, no se escribe nada, ni siquiera las buenas |
| `N − R` | Registros que sí se escriben en la tabla de destino | filas | Es el dato que se publica: si la validación es laxa, crece a costa de la calidad |
| `umbral` | Tasa a partir de la cual se considera que el origen ha cambiado y se para | tanto por uno (o %) | Si subes el umbral, hay menos paradas y más basura publicada; si lo bajas, más falsas alarmas y más lotes retenidos |
| `tasa_rechazo` | Proporción del lote que se rechaza | tanto por uno (o %) | Al acercarse al umbral, cualquier variación del origen decide entre cargar o parar |
| línea base | Tasa mediana de los últimos lotes correctos | tanto por uno (o %) | Si crece, el sistema se ha acostumbrado a un origen peor: la alerta debe ser la desviación, no el valor |
:::

Tres propiedades que hacen que la regla sea de fiar:

- **Exclusión mutua.** Cada registro acaba exactamente en un sitio. La validación se escribe **una
  vez** y de ella salen las dos ramas; con dos condiciones distintas —una para «bueno» y otra para
  «malo»— siempre hay un caso que se cuela por la grieta o que aparece en las dos tablas.
- **Atomicidad del lote.** La escritura de las filas buenas y de las filas de cuarentena se
  confirma en la misma unidad. Si el proceso muere a mitad, no queda medio lote cargado sin su
  cuarentena (mira [[transacciones-y-bloqueos]]).
- **Reversibilidad.** El registro de cuarentena guarda el dato original, no solo su identificador,
  para poder reprocesarlo sin volver al origen. Si el origen ya no está disponible, un identificador
  suelto no sirve de nada.

## Ejemplo

Un lote de ocho pedidos entra en la validación con tres reglas: unidades positivas, precio positivo
y no nulo, y correo con arroba.

| pedido | unidades | precio | correo | resultado |
| --- | --- | --- | --- | --- |
| P1 | 2 | 10,00 | a@x.es | entra |
| P2 | 1 | 5,00 | b@x.es | entra |
| P3 | −3 | 20,00 | c@x.es | rechazado: unidades no positivas |
| P4 | 4 | nulo | d@x.es | rechazado: precio vacío |
| P5 | 0 | 8,00 | sin-arroba | rechazado: dos motivos |
| P6 | 7 | 12,00 | f@x.es | entra |
| P7 | 2 | 9,00 | g@x.es | entra |
| P8 | 5 | 0,00 | h@x.es | rechazado: precio no positivo |

Cuatro rechazos de ocho: **50 %**. Con un umbral del 20 %, el lote no se escribe: ni las cuatro
filas buenas ni las cuatro malas. El pipeline para y avisa. Si el mismo proceso recibe un lote
sano con un solo precio vacío, la tasa es del **12,5 %**, por debajo del umbral: se escriben siete
filas y la rechazada va a cuarentena con su motivo, que es lo que permite arreglarla y
reprocesarla al día siguiente.

El caso del proveedor que cambia de unidad es el mismo cálculo a escala de un día. Cinco lotes de
tamaño parecido y un umbral del 5 %:

```
lote 1:   1 rechazado de 500   ->  0,2 %   pasa
lote 2:   3 rechazados de 480  ->  0,6 %   pasa
lote 3:   2 rechazados de 510  ->  0,4 %   pasa
lote 4: 140 rechazados de 470  -> 29,8 %   NO pasa: no se escribe nada
lote 5:   1 rechazado de 490   ->  0,2 %   pasa
```

La tasa del lote 4 no se parece a nada de lo que venía pasando, y ese salto es la señal. Con un
umbral del 30 % el lote habría pasado: las 330 filas buenas con precios en euros se habrían
mezclado con las 140 en céntimos y el error habría entrado en producción sin hacer ruido. Ese es
el compromiso real de un umbral: cada punto que lo subes compra menos paradas y vende más
descuadres silenciosos.

:::figura
fichero: rechazos-cuarentena-y-umbral
pie: A la izquierda, el bifurcador: la misma validación manda cada registro a la tabla buena o a la cuarentena con su motivo, y una rama aparte para el lote cuando la tasa supera el umbral. A la derecha, la tasa de rechazo de los cinco lotes del día: cuatro están por debajo del umbral y el cuarto lo cruza con un 29,8 %, así que se para y no se escriben ni sus 330 filas buenas. Lo que distingue una avería del ruido normal no es el número de rechazos, es el salto de la tasa.
fuente: figuras/registros-rechazados-y-cuarentena-1.py
:::

## Código

```python verificable
import pandas as pd

UMBRAL = 0.20        # mas alla de esto, el lote no se escribe

def revisar(lote):
    """Devuelve (buenos, rechazados) con el motivo de cada rechazo."""
    motivos = []
    for _, f in lote.iterrows():
        fallos = []
        if not f["unidades"] > 0:
            fallos.append("unidades no positivas")
        if pd.isna(f["precio"]) or f["precio"] <= 0:
            fallos.append("precio vacio o no positivo")
        if "@" not in str(f["email"]):
            fallos.append("email sin arroba")
        motivos.append("; ".join(fallos))
    lote = lote.assign(motivo=motivos)
    return lote[lote["motivo"] == ""], lote[lote["motivo"] != ""]

def procesar(nombre, lote):
    buenos, malos = revisar(lote)
    tasa = len(malos) / len(lote)
    print(f"{nombre}: {len(malos)} rechazados de {len(lote)} ({tasa:.1%})")
    if tasa > UMBRAL:
        print("  -> por encima del umbral: 0 filas escritas y el pipeline se para")
    else:
        print("  -> por debajo del umbral:", len(buenos), "filas a la tabla y", len(malos), "a cuarentena")
    return buenos, malos

sucio = pd.DataFrame({
    "pedido_id": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"],
    "unidades": [2, 1, -3, 4, 0, 7, 2, 5],
    "precio": [10.0, 5.0, 20.0, None, 8.0, 12.0, 9.0, 0.0],
    "email": ["a@x.es", "b@x.es", "c@x.es", "d@x.es", "sin-arroba", "f@x.es", "g@x.es", "h@x.es"],
})
normal = pd.DataFrame({
    "pedido_id": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"],
    "unidades": [2, 1, 3, 4, 1, 7, 2, 5],
    "precio": [10.0, 5.0, 20.0, None, 8.0, 12.0, 9.0, 1.0],
    "email": ["a@x.es", "b@x.es", "c@x.es", "d@x.es", "e@x.es", "f@x.es", "g@x.es", "h@x.es"],
})

procesar("tanda sucia", sucio)
print()
buenos, malos = procesar("tanda normal", normal)
print(malos[["pedido_id", "motivo"]].to_string(index=False))
```

```python verificable
import pandas as pd

# Cuarentena: el registro en crudo, el motivo y la tanda. Con eso se puede reprocesar.
cuarentena = pd.DataFrame({
    "pedido_id": ["P3", "P4", "P5"],
    "unidades": [-3, 4, 0],
    "motivo": ["unidades no positivas", "precio vacio", "unidades no positivas"],
})
tabla = pd.DataFrame({"pedido_id": ["P1", "P2", "P6"], "unidades": [2, 1, 7]})

# Arreglada la causa, se reprocesa la cuarentena y la clave de destino evita duplicar.
arreglados = cuarentena.assign(unidades=[3, 4, 1])[["pedido_id", "unidades"]]
tabla = pd.concat([tabla, arreglados]).drop_duplicates(subset="pedido_id", keep="last")
print(tabla.sort_values("pedido_id").to_string(index=False))
print("filas tras el reproceso:", len(tabla))
# -> 6
```

```sql ilustrativo
-- Una sola expresion define que es bueno y que es malo, para que ningun registro
-- pueda acabar en las dos tablas ni quedarse fuera.
WITH revisados AS (
    SELECT *,
           CASE WHEN unidades <= 0               THEN 'unidades no positivas'
                WHEN precio IS NULL OR precio <= 0 THEN 'precio vacio o no positivo'
                WHEN email NOT LIKE '%@%'         THEN 'email sin arroba'
           END AS motivo
    FROM staging.pedidos_crudos
    WHERE tanda = :tanda
)
INSERT INTO cuarentena (pedido_id, registro_crudo, motivo, tanda, detectado_en)
SELECT pedido_id, to_jsonb(revisados), motivo, :tanda, now()
FROM revisados
WHERE motivo IS NOT NULL;

-- Pero antes de escribir nada hay que decidir: si la tasa supera el umbral, no se
-- inserta ni una fila (ni aqui ni en la tabla buena) y el proceso sale con error.
SELECT COUNT(*) FILTER (WHERE motivo IS NOT NULL)::numeric
       / NULLIF(COUNT(*), 0) AS tasa_rechazo
FROM revisados;
```

## Errores típicos

- **Validar solo en la tabla de destino y esperar que el motor lo arregle.** Una restricción
  `CHECK` o un `NOT NULL` rechaza la fila, aborta la transacción del lote y te deja sin saber qué
  fila era ni por qué. Valida antes de escribir y guarda el motivo; deja las restricciones del
  motor como última red, no como estrategia.
- **Escribir las filas buenas de un lote sospechoso.** Cinco filas malas de un millón se apartan
  sin más; el 30 % de un lote no es suciedad, es un cambio de origen. Si la tasa supera el umbral,
  no se escribe ninguna fila: una tabla a medias es peor que una tabla que no avanzó, porque el
  consumidor no sabe que falta la otra mitad.
- **Tratar el rechazo de lote como rechazo de fila.** Si no se puede abrir el fichero o falta la
  columna de la clave, no hay filas que apartar: hay un lote entero que no se entiende. Apártalo
  completo, avisa y no escribas nada; volcarlo a cuarentena fila a fila solo llena una tabla de
  ruido.
- **Guardar la cuarentena en un log.** Un fichero de log rota, se comprime y desaparece, y no se
  puede consultar por proveedor, por motivo o por antigüedad. La cuarentena es una tabla con
  columnas, con su retención y con dueño.
- **No reprocesar nunca.** Una cuarentena que solo crece es una pérdida de datos progresiva y
  silenciosa. Hace falta un proceso que la vacíe, un informe de su tamaño y una alerta cuando
  lleva días subiendo; y para reinsertar sin duplicar, una clave de destino y escritura
  idempotente.
- **Fijar el umbral una vez y no volver a mirarlo.** El umbral correcto depende del volumen, de
  la estacionalidad y de lo que cuesta cada error. Un umbral del 5 % en un origen que
  históricamente rechaza el 4 % está avisando todos los días, y una alerta que suena siempre deja
  de ser una alerta ([[calidad-y-slas]] y [[observabilidad-de-datos]] tratan esa parte).

## Comprueba que lo sabes

:::quiz
p: Un lote de 500 registros llega con 3 rechazados y el umbral del pipeline es el 2 %. ¿Qué hace el pipeline?
o: Escribe los 497 buenos y manda los 3 a cuarentena con su motivo
o: No escribe nada, porque cualquier rechazo invalida el lote
o: Escribe los 500 y anota los 3 en el log
a: 1
e: La tasa es 3/500 = 0,6 %, por debajo del umbral: se cargan los buenos y los rechazados van a cuarentena para poder arreglarlos y reprocesarlos. No escribir nada por tres filas malas convertiría cualquier teléfono raro en una parada del negocio, y escribir las 500 mete en la tabla tres filas que no cumplen las reglas.
:::

:::quiz
p: La tasa de rechazo de un lote se dispara al 30 % cuando llevaba meses en el 0,3 %. ¿Por qué se para el pipeline en vez de cargar la parte buena?
o: Porque una tasa muy por encima de lo normal suele significar que el origen ha cambiado, y entonces lo que está mal es la interpretación de los datos, no unas pocas filas
o: Porque cargar pocas filas tarda más que no cargar ninguna
o: Porque el 30 % de rechazos supera el límite legal de errores de un pipeline
a: 1
e: Un salto así no es suciedad puntual: es un esquema nuevo, una unidad distinta, un encoding roto o un fichero que no es el que se esperaba. En ese escenario las filas «buenas» también están mal interpretadas, así que cargarlas es publicar un dato equivocado. Un rechazo suelto se aparta; una tasa que se multiplica se investiga.
:::

:::quiz
p: ¿Qué tiene que llevar la tabla de cuarentena para que sirva de algo?
o: Solo el identificador del registro y la fecha, para no duplicar información
o: El registro original completo, el motivo, el lote y la localización de origen, para poder reprocesarlo sin volver al origen
o: El mensaje de error del motor y el nombre de la tabla de destino
a: 2
e: Con solo el identificador no se puede reprocesar si el origen ya no está o si cambió; y con solo el mensaje de error no se sabe qué dato era. Guardar el registro en crudo, el motivo, la tanda y de dónde salió permite arreglar la causa y reinsertar. Además hace falta un proceso que la vacíe y una alerta cuando crece, porque una cuarentena que nadie mira es una pérdida silenciosa.
:::
