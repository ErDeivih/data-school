---
id: normalizacion-vs-desnormalizacion
titulo: Normalización frente a desnormalización
fase: 4
nivel: intermedio
rutas: [de, ds]
prerequisitos: [sql-modelado-y-normalizacion, sql-joins]
tags: [modelado, rendimiento, integridad, redundancia]
resumen: Repartir cada dato en un solo sitio para no contradecirte, o duplicarlo a propósito para leer más rápido: el compromiso que decide tu modelo.
fuentes: ["Kimball y Ross (2013), 'The Data Warehouse Toolkit'", "Codd (1970), 'A Relational Model of Data for Large Shared Data Banks'"]
---

## En una frase

**Normalizar** es guardar cada hecho una sola vez y reconstruir el resto con uniones;
**desnormalizar** es copiar datos a propósito para no tener que unirlos, a cambio de que cada
cambio haya que aplicarlo en varios sitios y de que las copias puedan contradecirse.

## La idea

Tienes una tienda con 50.000 clientes y 500.000 pedidos. En la tabla de pedidos hay una columna
`ciudad_cliente`. ¿Para qué repetir 500.000 veces una ciudad que ya está en la ficha del
cliente? Con un `JOIN` la obtienes cuando la necesites y, sobre todo, cuando un cliente se mude
solo tendrás que cambiar **una fila**.

Ese es el argumento de la normalización, y es un argumento de **integridad**, no de elegancia.
Si la ciudad está copiada en cada pedido, ¿qué pasa cuando el cliente se muda? Hay tres
respuestas posibles y las tres son malas:

- Actualizas los 500.000 pedidos históricos y reescribes el pasado: el informe de ventas de
  2021 por ciudad cambia sin que nadie haya vendido nada.
- Actualizas solo los pedidos nuevos y ahora el cliente tiene dos ciudades a la vez en la misma
  tabla. Un informe `GROUP BY ciudad` lo parte en dos.
- No actualizas nada y la ciudad se queda obsoleta en todos los pedidos.

En un modelo normalizado ninguna de esas tres cosas puede pasar: la ciudad vive en un sitio y
no hay forma de que se contradiga consigo misma. A esto se le llama evitar las **anomalías de
actualización**, y es la razón por la que el modelo normalizado se inventó.

Entonces, ¿por qué desnormalizar? Porque unir tablas cuesta. Cada `JOIN` es trabajo de mover y
comparar filas, y en los motores analíticos ese coste se paga en tiempo y en dinero. En un
[[data-warehouse|almacén analítico]], las consultas son de solo lectura, se ejecutan sobre
millones de filas y las escribe un proceso controlado, no 300 usuarios a la vez. En ese
contexto, copiar la ciudad en el hecho elimina un `JOIN` en cada consulta del cuadro de mando
y las tres anomalías de arriba se resuelven en el proceso de carga, que es el único que
escribe. Eso es exactamente lo que hacen el [[esquema-estrella-y-copo|esquema en estrella]] y
las dimensiones de un almacén.

La forma moderna de decidir no es «normalizado o no», sino **dónde**: normaliza donde se
escribe y se decide (el sistema de origen y el núcleo del almacén), desnormaliza donde se lee
(las tablas de hechos y las vistas que consumen las herramientas de BI). Y si dudas, la
respuesta por defecto es normalizar: desnormalizar es una optimización y toda optimización
debería tener una medida delante.

## Definición formal

Sobre una relación `R` con atributos `A₁ … Aₙ`, una **dependencia funcional** `X → Y` dice que
dos filas con los mismos valores en `X` tienen necesariamente los mismos valores en `Y`. Con
esa notación:

- **1FN (primera forma normal):** todos los atributos son atómicos. Nada de `telefonos` con
  `"600111222, 600333444"` dentro de una celda.
- **2FN:** está en 1FN y todo atributo no primo depende de la clave completa, no de una parte.
  Rompe las claves compuestas donde un atributo depende solo de un componente.
- **3FN:** está en 2FN y no existen dependencias transitivas, es decir, `X → Y → Z` con `Y` no
  clave. Un atributo *primo* es el que forma parte de alguna clave candidata.

:::formula
3FN ⟺ toda X → Y no trivial tiene X superclave o Y primo
:::

**Desnormalizar** es aceptar a propósito una violación de 3FN: se guarda `Y` junto a `X`
aunque `X → Y` ya exista en otra tabla. Los costes se pueden acotar:

- **Espacio:** `bytes_copia = bytes_atributo × filas_de_la_tabla_que_lo_copia`.
- **Escritura:** cada cambio del atributo toca `filas_que_lo_copian` filas en lugar de una.
- **Riesgo:** dos copias son dos verdades; sin un proceso de refresco idempotente y una
  comprobación de consistencia, divergen. La desnormalización no elimina el `JOIN`, lo mueve
  del momento de la consulta al momento de la carga.

## Ejemplo

50.000 clientes y 500.000 pedidos (10 por cliente). La ciudad tiene 6 a 9 caracteres, unos 7
de media.

- **Normalizado:** la ciudad ocupa `50.000 × 7 = 350.000` bytes. Cambiar la ciudad de un
  cliente es 1 fila.
- **Desnormalizado:** la ciudad ocupa `500.000 × 7 = 3.500.000` bytes, diez veces más. Cambiar
  la ciudad de un cliente toca sus 10 pedidos.
- Si cada año el 10 % de los clientes se muda (5.000 clientes), el modelo normalizado actualiza
  5.000 filas y el copiado 50.000. Diez veces más escrituras para ahorrar un `JOIN`.

Y el daño no es solo de rendimiento, es de corrección. Con la ciudad copiada, un cliente puede
acabar con dos ciudades:

| id_pedido | cliente | ciudad | importe |
| --- | --- | --- | --- |
| 1 | 4471 | Madrid | 120,00 |
| 2 | 4471 | Barcelona | 80,00 |
| 3 | 8890 | Sevilla | 50,00 |

El informe por ciudad dirá Madrid 120 y Barcelona 80, y el total del cliente 4471 son 200
euros repartidos entre dos ciudades. Ninguna de las dos filas es «el error»: el error es el
diseño, que permite que existan. En el modelo normalizado ese estado es imposible de
representar.

## Código

```python verificable
import pandas as pd

CIUDADES = ["Barcelona", "Madrid", "Sevilla", "Bilbao"]   # 9, 6, 7 y 6 caracteres
ciudad = pd.Series([CIUDADES[i % 4] for i in range(50_000)])

bytes_normalizado = int(ciudad.str.len().sum())            # ciudad solo en la ficha del cliente
bytes_copiado = bytes_normalizado * 10                     # 10 pedidos por cliente, en promedio
print("bytes de ciudad normalizado:", bytes_normalizado)        # -> bytes de ciudad normalizado: 350000
print("bytes de ciudad copiado:", bytes_copiado)                # -> bytes de ciudad copiado: 3500000
print("factor de duplicacion:", bytes_copiado // bytes_normalizado)  # -> factor de duplicacion: 10

mudanzas = 5_000        # el 10 % de los clientes cambia de ciudad en un ano
print("filas escritas al ano normalizado:", mudanzas)           # -> filas escritas al ano normalizado: 5000
print("filas escritas al ano copiado:", mudanzas * 10)          # -> filas escritas al ano copiado: 50000
```

```sql verificable
-- El modelo copiado permite que un cliente tenga dos ciudades a la vez
CREATE TABLE pedidos AS
SELECT * FROM (VALUES
    (1, 4471, 'Madrid',    120.00),
    (2, 4471, 'Barcelona',  80.00),
    (3, 8890, 'Sevilla',    50.00)
) AS t(id_pedido, nk_cliente, ciudad, importe);

-- El cliente 4471 aparece dos veces: 80.0 y 120.0 repartidos entre dos ciudades
SELECT nk_cliente, ciudad, sum(importe) AS total
FROM pedidos
GROUP BY nk_cliente, ciudad
ORDER BY nk_cliente, ciudad;
```

## Errores típicos

- **Desnormalizar antes de medir.** «Las uniones son lentas» es una intuición, no un dato. Mide
  el plan de ejecución y los bytes leídos ([[sql-indices-y-planes]]); muchas consultas lentas
  lo son por un filtro mal escrito, no por el `JOIN`.
- **Duplicar atributos que cambian mucho sin montar el refresco.** Si copias la ciudad en los
  pedidos, necesitas un proceso idempotente que la mantenga sincronizada, un dueño y una
  comprobación que avise cuando los totales no cuadren. Sin eso, la desnormalización es una bomba
  de relojería silenciosa.
- **Confundir desnormalizar con quitar claves y restricciones.** Se pueden copiar atributos y
  seguir teniendo claves primarias, foráneas y comprobaciones. La redundancia deliberada no
  justifica perder la integridad referencial.
- **Pensar que todo dato duplicado en un hecho es un error.** El precio unitario del producto
  en la línea de pedido **debe** copiarse: el precio de hoy no es el que se cobró. Eso no es
  desnormalizar por rendimiento, es guardar un hecho histórico. Pregúntate siempre si el
  atributo describe la entidad (se actualiza) o el evento (se congela).
- **Desnormalizar solo para ahorrar almacenamiento.** Es al revés: desnormalizar **gasta**
  almacenamiento. Si tu problema es el espacio, la solución es comprimir y particionar
  ([[compresion-y-codificacion]], [[particionado-y-clustering]]).
- **Aplicarlo en el sistema transaccional.** Desnormalizar en la base donde escriben las
  aplicaciones multiplica los bloqueos y las escrituras, justo lo contrario de lo que
  necesita un [[oltp-vs-olap|OLTP]].

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es el problema principal de copiar la ciudad del cliente en cada pedido?
o: Que ocupa más espacio en disco, que es el único coste relevante
o: Que un cambio de ciudad obliga a actualizar muchas filas y las copias pueden contradecirse entre sí
o: Que impide hacer un GROUP BY por ciudad
a: 2
e: El coste de espacio es real pero secundario. Lo grave es que el atributo pasa a tener varias verdades simultáneas: si actualizas solo parte de las filas, el mismo cliente aparece en dos ciudades. El GROUP BY sigue funcionando; lo que hace es devolver un resultado incoherente.
:::

:::quiz
p: En un almacén analítico de solo lectura, ¿por qué se acepta un esquema en estrella desnormalizado?
o: Porque la tercera forma normal no se aplica a los almacenes de datos
o: Porque elimina uniones en cada consulta y el único que escribe es el proceso de carga, que puede mantener las copias
o: Porque en analítica no importa la integridad de los datos
a: 2
e: La 3FN se aplica igual; lo que cambia es el reparto de responsabilidades: hay muchas lecturas y un solo escritor controlado, así que mover el coste del JOIN al proceso de carga sale a cuenta. Y la integridad importa más, no menos: por eso el refresco es idempotente y se comprueba.
:::

:::quiz
p: El precio unitario de un producto copiado en la línea de pedido, ¿es un error de normalización?
o: Sí, es redundancia: el precio ya está en la tabla de productos
o: No, es un hecho histórico: describe lo que se cobró ese día y no debe cambiar cuando cambie la tarifa
o: Solo es un error si el producto sube de precio
a: 2
e: La prueba es preguntar si el atributo describe la entidad o el evento. El precio actual del producto es un atributo del producto; el precio cobrado es un atributo de la venta y se congela. Si lo unieras por la tabla de productos, recalcularías el pasado cada vez que cambia una tarifa.
:::

:::trampa
Una tabla «desnormalizada para ir más rápido» que se refresca con un `INSERT` nocturno en vez
de un `MERGE` idempotente acaba con duplicados. Si no puedes ejecutar el proceso dos veces
seguidas con el mismo resultado, ese refresco romperá el cuadro de mando un martes cualquiera.
:::
