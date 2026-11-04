---
id: etl-vs-elt
titulo: ETL frente a ELT
fase: 4
nivel: básico
rutas: [de]
prerequisitos: [ciclo-de-vida-del-dato, oltp-vs-olap]
tags: [etl, elt, pipelines, transformacion, carga]
resumen: Transformar antes o después de cargar los datos: la misma tubería con las etapas en otro orden, y una decisión que marca dónde vive tu lógica de negocio.
fuentes: ["Kimball & Ross (2013), 'The Data Warehouse Toolkit'", "Reis & Housley (2022), 'Fundamentals of Data Engineering'"]
---

## En una frase

ETL y ELT hacen el mismo trabajo —extraer de un sistema, cambiar los datos y dejarlos listos
para analizar— pero en orden distinto: ETL transforma en un servidor intermedio antes de cargar
nada en el almacén, y ELT carga primero el dato en crudo y transforma después, dentro del propio
almacén.

## La idea

Piensa en cómo guardas la compra. Puedes llegar a casa, lavar y trocear la verdura y congelarla
ya lista para la sartén (ETL). O puedes meterla entera en el congelador y trocearla el día que
cocinas (ELT). El trabajo total es el mismo; lo que cambia es **dónde** queda la verdura
troceada y **cuándo** has hecho el esfuerzo.

La industria eligió primero ETL por una razón de precio, no de elegancia. Hace años el almacén
de datos era un servidor caro y rígido, con licencia por procesador y capacidad justa: gastar
ese recurso en limpiar y unir tablas era tirar dinero. Así que se montaba una máquina intermedia
—un servidor de integración, un clúster— que hacía todo el trabajo sucio y dejaba al almacén
únicamente la tarea de servir consultas ya masticadas.

Lo que rompió el empate fue el abaratamiento del almacenamiento y la separación entre cómputo y
almacenamiento en los almacenes modernos. Si guardar un terabyte cuesta poco, el crudo ya no hay
que tirarlo; y si el motor que consulta es el mismo que transforma, resulta que el clúster de
transformación ya lo tenías pagado. A eso se suma que los formatos columnares comprimen mucho
mejor de lo que comprimía un CSV, y que el SQL lo entiende todo el mundo. Con esas tres piezas,
ELT pasó a ser lo normal.

Las consecuencias prácticas de cargar en crudo son tres, y son la verdadera lección de esta
página:

1. **Puedes reprocesar.** Si mañana cambia la definición de «cliente activo», con ETL tienes que
   volver a la fuente (que quizá ya no tenga el histórico) y rehacer la extracción. Con ELT
   relanzas la consulta sobre el crudo que ya tienes.
2. **La lógica se revisa.** Si la transformación es SQL versionado
   ([[dbt-y-transformacion]]), cualquier persona del equipo la lee y la discute. Un trabajo
   dibujado en una herramienta gráfica de integración, no.
3. **El crudo es un contrato.** Guardado en una capa de bronce ([[arquitectura-medallion]]) sirve
   de referencia cuando dos informes dan números distintos.

El precio no desaparece, solo cambia de sitio: en ELT pagas cómputo por cada consulta sobre el
crudo, guardas más bytes y necesitas gobierno desde el primer día, porque un lago sin gobierno se
convierte en un pantano ([[data-lake]]).

## Definición formal

Llamemos `O` al sistema de origen, `E` a la función de extracción, `T` a la transformación
(tipar, limpiar, deduplicar, unir con dimensiones, agregar) y `C` a la carga en el destino `A`.

- **ETL:** `A = C(T(E(O)))`. La transformación ocurre fuera del destino; al almacén solo llega el
  resultado.
- **ELT:** `A_crudo = C(E(O))` y después `A = T(A_crudo)`, con `T` ejecutándose **dentro** del
  destino.

Símbolos: `O` es la base transaccional o la API de la que lees ([[oltp-vs-olap]]); `E` decide qué
filas y columnas salen y con qué frecuencia; `T` es el conjunto de reglas de negocio; `C` es la
escritura física en el destino; `A` es lo que finalmente consultan las herramientas de análisis.

Tres propiedades que conviene medir en cualquiera de los dos órdenes:

- **Latencia:** tiempo entre el cambio en `O` y su disponibilidad en `A`. Un proceso nocturno
  tiene una latencia de hasta 24 horas; uno que corre cada 15 minutos, de hasta 15.
- **Idempotencia:** ejecutar la misma carga dos veces debe dejar `A` igual que ejecutarla una. Si
  no, cualquier reintento duplica ([[idempotencia-y-reintentos]]).
- **Linaje:** poder responder de qué tabla de origen sale cada columna de `A`. En ELT el linaje
  es más largo, porque hay más pasos intermedios, y por eso hace falta una herramienta que lo
  dibuje sola ([[catalogo-y-linaje]]).

| Criterio | ETL | ELT |
| --- | --- | --- |
| Dónde se transforma | En un servidor intermedio | Dentro del almacén |
| Dato crudo en el destino | No, solo el resultado | Sí, siempre |
| Reprocesar sin tocar el origen | Difícil | Trivial |
| Quién puede cambiar la lógica | Quien domine la herramienta de integración | Quien sepa SQL |
| Cuándo encaja | Hay que enmascarar datos personales antes de que salgan del perímetro, o el destino no tiene potencia | El destino es elástico, quieres auditar el crudo y las reglas cambian a menudo |

## Ejemplo

Un comercio tiene 6 pedidos en su base transaccional y la regla de negocio es «cuenta solo lo
pagado y con importe positivo»:

```
pedido  cliente  importe  estado
1       10        25,00   pagado
2       11        -3,00   pagado
3       10        40,00   devuelto
4       12        15,00   pagado
5       13         (nulo) pagado
6       12        60,00   pagado
```

- **ETL:** la transformación ocurre fuera. Se descartan el pedido 2 (importe negativo), el 3
  (devuelto) y el 5 (sin importe), y se agrega por cliente antes de cargar. Al almacén entran
  **2 filas**: cliente 10 con 25,00 y cliente 12 con 75,00. Total: 100,00.
- **ELT:** al almacén entran las **6 filas** en crudo. La misma regla se aplica después con una
  consulta, que produce las mismas 2 filas y el mismo total de 100,00.

Fíjate en que el resultado de negocio es idéntico y la diferencia está en cuántas filas cruzan la
frontera del almacén y en qué queda guardado. Si dentro de un mes alguien pregunta «¿cuántos
pedidos devueltos tuvimos?», en ELT la respuesta está en el crudo que ya cargaste; en ETL esos
pedidos nunca llegaron y hay que volver a la fuente.

## Código

```python verificable
import pandas as pd

# Los 6 pedidos tal como salen del sistema transaccional.
crudo = pd.DataFrame({
    "pedido_id": [1, 2, 3, 4, 5, 6],
    "cliente_id": [10, 11, 10, 12, 13, 12],
    "importe": [25.0, -3.0, 40.0, 15.0, None, 60.0],
    "estado": ["pagado", "pagado", "devuelto", "pagado", "pagado", "pagado"],
})

# La regla de negocio, escrita una sola vez.
valido = crudo[(crudo["estado"] == "pagado") & (crudo["importe"] > 0)]

# ETL: al almacen solo llega el agregado.
etl = valido.groupby("cliente_id")["importe"].sum()
print("ETL filas cargadas:", len(etl))                # -> ETL filas cargadas: 2
print("ETL total:", float(etl.sum()))                 # -> ETL total: 100.0

# ELT: al almacen llega todo el crudo y la regla se aplica despues.
print("ELT filas cargadas:", len(crudo))              # -> ELT filas cargadas: 6
print("ELT total:", float(valido["importe"].sum()))   # -> ELT total: 100.0
print("Filas descartadas:", len(crudo) - len(valido)) # -> Filas descartadas: 3
```

```sql verificable
-- La misma regla, en ELT: el crudo se carga entero y se transforma al consultar.
CREATE TABLE crudo AS
SELECT * FROM (VALUES
    (1, 10,  25.0, 'pagado'),
    (2, 11,  -3.0, 'pagado'),
    (3, 10,  40.0, 'devuelto'),
    (4, 12,  15.0, 'pagado'),
    (5, 13,  NULL, 'pagado'),
    (6, 12,  60.0, 'pagado')
) AS t(pedido_id, cliente_id, importe, estado);

SELECT cliente_id, SUM(importe) AS total
FROM crudo
WHERE estado = 'pagado' AND importe > 0
GROUP BY cliente_id
ORDER BY cliente_id;
```

El bloque SQL imprime dos filas: cliente 10 con total 25.0 y cliente 12 con total 75.0.

## Errores típicos

- **Creer que ELT significa «sin transformación».** Significa que la transformación se hace
  después y, normalmente, con SQL. Las reglas de negocio siguen existiendo y hay que escribirlas,
  probarlas y versionarlas; lo único que cambia es dónde se ejecutan.
- **Cargar en crudo y no gobernar nada.** Sin catálogo, sin dueño y sin pruebas de calidad, la
  capa de crudo se convierte en un vertedero del que nadie se fía y todos acaban reextrayendo
  desde el origen. El crudo solo sirve si está documentado.
- **Hacer ELT con datos personales sin enmascarar.** Si el nombre, el documento de identidad o el
  correo entran en crudo al almacén, multiplicas la superficie donde pueden filtrarse y complicas
  el borrado por derecho al olvido ([[gobierno-y-privacidad]]). Enmascara antes de cargar o cifra
  la columna.
- **Transformar dentro de la base de producción.** Una consulta con tres uniones y un `GROUP BY`
  sobre la base que usa la aplicación le roba procesador y bloqueos. Extrae primero a un destino
  aparte y transforma allí ([[oltp-vs-olap]]).
- **Confundir la capa de aterrizaje con un producto de datos.** Las tablas de staging son un
  detalle interno de la tubería. En cuanto tres informes las consultan directamente, ya no puedes
  cambiar su esquema nunca.
- **No guardar el crudo «para ahorrar espacio».** Es el ahorro más caro que existe: el día que
  cambia una regla de negocio no puedes reprocesar el pasado sin volver a molestar al sistema de
  origen ([[backfill-y-reproceso]]).

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es la diferencia esencial entre ETL y ELT?
o: ELT no transforma los datos, solo los copia
o: En ELT la transformación ocurre después de cargar, dentro del propio almacén
o: ETL solo funciona con ficheros planos y ELT solo con bases de datos
a: 2
e: El orden de las etapas es lo que cambia: en ETL se transforma antes de cargar y en ELT después. Las dos transforman y las dos pueden leer cualquier formato; lo que decide es dónde se ejecuta la lógica y si el dato en crudo queda guardado en el destino.
:::

:::quiz
p: Cambia la definición de «cliente activo» y hay que recalcular los tres últimos años. ¿En cuál de los dos órdenes te cuesta menos?
o: En ELT, porque el crudo ya está cargado y solo hay que relanzar la transformación
o: En ETL, porque el servidor intermedio guarda copias de todo
o: Da igual, en los dos casos hay que volver a extraer del origen
a: 1
e: La ventaja práctica de ELT es que el dato en crudo vive en el destino, así que un cambio de regla es una consulta nueva y no una extracción nueva. En ETL lo único que se guardó fue el resultado transformado, y el histórico del origen puede haber cambiado o ya no estar disponible.
:::

:::truco
Si dudas, carga en crudo y transforma después. Cargar de más es reversible: borras la tabla y
reprocesas. Haber tirado un dato que no guardaste, no.
:::
