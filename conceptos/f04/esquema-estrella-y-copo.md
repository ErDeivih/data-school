---
id: esquema-estrella-y-copo
titulo: Esquema en estrella y copo de nieve
fase: 4
nivel: intermedio
rutas: [de]
prerequisitos: [modelado-dimensional, sql-joins, normalizacion-vs-desnormalizacion]
tags: [modelado, estrella, copo-de-nieve, dwh, bi]
resumen: La estrella deja las dimensiones planas y el copo de nieve las normaliza; la primera gana casi siempre en analítica, y aquí se ve por qué y cuándo no.
fuentes: ["Kimball y Ross (2013), 'The Data Warehouse Toolkit', cap. 1", "Inmon (2005), 'Building the Data Warehouse'"]
---

## En una frase

Los dos esquemas tienen la misma tabla de hechos en el centro; la diferencia está en las
dimensiones: en la estrella son tablas planas y anchas, y en el copo de nieve están partidas en
varias tablas normalizadas.

## La idea

El nombre lo dice todo si miras un diagrama: en la **estrella**, la tabla de hechos está en el
centro y cada dimensión es un brazo directo. En el **copo de nieve**, algunas dimensiones se
ramifican en subdimensiones (producto apunta a categoría, categoría apunta a departamento) y el
dibujo se parece a un copo.

¿Por qué alguien partiría una dimensión? Por la misma razón por la que se normaliza una base
transaccional: **no repetir información**. Si 500.000 productos pertenecen a 40 categorías, en
la estrella el nombre de la categoría se repite en cada fila de producto; en el copo se guarda
una vez. En un mundo de discos caros, eso era dinero.

¿Y por qué la estrella ganó en analítica? Porque el coste dominante ya no es el espacio, sino
el **tiempo de la consulta y la simplicidad del modelo**:

- Cada tabla extra es una unión más en cada informe, y las uniones cuestan.
- Las herramientas de BI (arrastrar campos, construir filtros) funcionan mucho mejor con
  dimensiones planas: una lista de campos con nombres claros en lugar de una cadena de tablas
  que hay que atravesar.
- El almacenamiento columnar moderno comprime muy bien los textos repetidos. Repetir
  «periféricos» medio millón de veces cuesta, con diccionario, unos pocos kilobytes.
- Un modelo con menos tablas es más fácil de explicar, de documentar y de mantener.

Hay además un matiz que casi nadie menciona: en la práctica los dos esquemas **dan el mismo
resultado**. El consumidor obtiene la misma tabla agregada; lo que cambia es cuántas uniones
tiene que escribir (o generar la herramienta) para llegar. Cuando la discusión es «estrella o
copo», la pregunta correcta no es cuál es más elegante, sino cuánto cuesta cada unión y quién va
a escribir las consultas.

El copo tiene sus casos legítimos, y no son raros:

- **Dimensiones enormes y muy redundantes.** Un catálogo con millones de referencias y
  jerarquías de cinco niveles (departamento, familia, subfamilia, marca, gama).
- **Atributos compartidos por varias dimensiones.** Si producto, tienda y proveedor pertenecen
  al mismo árbol de sociedades, ese árbol puede ser una dimensión aparte.
- **Organizaciones con gobierno fuerte.** A veces el equipo de datos prefiere una fuente única
  para cada atributo y acepta el coste en uniones.

La recomendación de manual (Kimball) es clara: **empieza por la estrella**. Si una dimensión
crece hasta volverse inmanejable, se parte ese trozo concreto, no todo el modelo. Y si partes
una dimensión, documenta la unión resultante, porque el siguiente que llegue tendrá que
escribirla.

## Definición formal

Ambos esquemas comparten la tabla de hechos `F` de grano `G` con sus claves ajenas y medidas.
Lo que cambia es la forma de las dimensiones.

**Estrella:** cada dimensión `Dᵢ` es una sola tabla con clave sustituta y todos sus atributos,
incluidas las jerarquías, aplanadas:

```
F(fecha_id, producto_id, tienda_id, unidades, importe)
D_producto(producto_id, codigo, nombre, familia, departamento)
D_tienda(tienda_id, nombre, ciudad, provincia, comunidad)
D_fecha(fecha_id, fecha, anio, trimestre, mes, dia_semana, es_festivo)
```

**Copo de nieve:** alguna dimensión se descompone en `k` tablas encadenadas por claves ajenas:

```
F(fecha_id, producto_id, tienda_id, unidades, importe)
D_producto(producto_id, codigo, nombre, familia_id)
D_familia(familia_id, nombre, departamento_id)
D_departamento(departamento_id, nombre)
D_tienda(tienda_id, nombre, ciudad_id)
D_ciudad(ciudad_id, nombre, provincia_id, comunidad_id)
```

Consecuencias medibles de la diferencia:

- **Uniones por consulta**: la estrella necesita una unión por dimensión usada en el filtro o la
  agrupación. El copo necesita una unión por **cada nivel** de la jerarquía que se use. Un
  informe por departamento pasa de 2 uniones a 4.
- **Redundancia**: en la estrella, un atributo de nivel alto se repite en todas las filas de la
  dimensión. El espacio extra depende de la cardinalidad: con 2.000 productos y 40 familias, la
  dimensión aplanada en texto ocupa unos 137 KB frente a los 124 KB de la versión partida, es
  decir un 9 % más, que un formato columnar con diccionario reduce a un puñado de kilobytes.
- **Coste de mantenimiento**: en el copo, cambiar el nombre de un departamento es un `UPDATE` de
  una fila; en la estrella hay que actualizar todas las filas de la dimensión que lo mencionan
  (y si hay historia, decidir qué versiones se tocan).
- **Riesgo de inconsistencia**: en el copo, dos dimensiones pueden apuntar a jerarquías
  distintas si alguien no las conforma. En la estrella el atributo está en un solo sitio por
  fila y no hay ambigüedad.

## Ejemplo

Las mismas ventas, modeladas de las dos formas. Datos de partida: tres líneas de venta de tres
productos que pertenecen a dos familias y a dos departamentos.

**Estrella** (una dimensión plana):

`dim_producto`

| producto_id | nombre | familia | departamento |
| --- | --- | --- | --- |
| 1 | teclado | periféricos | accesorios |
| 2 | ratón | periféricos | accesorios |
| 3 | monitor | pantallas | imagen |

`hechos_ventas`

| producto_id | unidades | importe |
| --- | --- | --- |
| 1 | 2 | 59,90 |
| 2 | 1 | 12,50 |
| 3 | 3 | 179,00 |

Consulta de importe por departamento: **una unión**. Resultado: accesorios 72,40; imagen 179,00.

**Copo de nieve** (jerarquía partida):

`dim_producto`

| producto_id | nombre | familia_id |
| --- | --- | --- |
| 1 | teclado | 10 |
| 2 | ratón | 10 |
| 3 | monitor | 20 |

`dim_familia`

| familia_id | nombre | departamento_id |
| --- | --- | --- |
| 10 | periféricos | 100 |
| 20 | pantallas | 200 |

`dim_departamento`

| departamento_id | nombre |
| --- | --- |
| 100 | accesorios |
| 200 | imagen |

Consulta de importe por departamento: **tres uniones** (`hechos_ventas` con `dim_producto`,
`dim_producto` con `dim_familia` y `dim_familia` con `dim_departamento`), y el mismo resultado:
accesorios 72,40; imagen 179,00. Ahí se ve el patrón: cada nivel de jerarquía que añades al copo
se cobra una unión en cada consulta.

## Código

```python verificable
# Estrella (1 union) y copo (3 uniones): mismo resultado, distinto numero de saltos
DIM_ESTRELLA = {1: ("teclado", "perifericos", "accesorios"),
                2: ("raton", "perifericos", "accesorios"),
                3: ("monitor", "pantallas", "imagen")}

DIM_PRODUCTO = {1: ("teclado", 10), 2: ("raton", 10), 3: ("monitor", 20)}
DIM_FAMILIA = {10: ("perifericos", 100), 20: ("pantallas", 200)}
DIM_DEPARTAMENTO = {100: "accesorios", 200: "imagen"}

VENTAS = [(1, 59.90), (2, 12.50), (3, 179.00)]

estrella, copo = {}, {}
for producto, importe in VENTAS:
    departamento = DIM_ESTRELLA[producto][2]                        # 1 salto
    copo_dep = DIM_DEPARTAMENTO[DIM_FAMILIA[DIM_PRODUCTO[producto][1]][1]]   # 3 saltos
    estrella[departamento] = round(estrella.get(departamento, 0) + importe, 2)
    copo[copo_dep] = round(copo.get(copo_dep, 0) + importe, 2)

print("estrella (1 union)  :", estrella)     # -> {'accesorios': 72.4, 'imagen': 179.0}
print("copo     (3 uniones):", copo)         # -> {'accesorios': 72.4, 'imagen': 179.0}
print("mismo resultado     :", estrella == copo)   # -> True
```

```python verificable
# Cuanto ocupa la dimension plana frente a la partida, con 2000 productos y 40 familias
import json

FAMILIAS = [f"familia-{i:02d}" for i in range(40)]

estrella = [{"producto_id": i, "nombre": f"producto-{i:04d}", "familia": FAMILIAS[i % 40]}
            for i in range(2000)]
copo = ([{"producto_id": i, "nombre": f"producto-{i:04d}", "familia_id": i % 40}
         for i in range(2000)]
        + [{"familia_id": i, "nombre": FAMILIAS[i]} for i in range(40)])

bytes_estrella = len(json.dumps(estrella, separators=(",", ":")).encode())
bytes_copo = len(json.dumps(copo, separators=(",", ":")).encode())

print("dimension plana (estrella):", bytes_estrella, "bytes")   # -> 136891 bytes
print("dimension partida (copo)  :", bytes_copo, "bytes")       # -> 123981 bytes
print("el copo ahorra            :", bytes_estrella - bytes_copo, "bytes")   # -> 12910 bytes
```

```sql ilustrativo
-- La jerarquia aplanada permite agrupar por departamento con una sola union
SELECT p.departamento, sum(h.importe) AS importe
FROM hechos_ventas h
JOIN dim_producto p ON p.producto_id = h.producto_id
GROUP BY p.departamento;

-- En copo de nieve, el mismo informe necesita recorrer los tres niveles
SELECT d.nombre AS departamento, sum(h.importe) AS importe
FROM hechos_ventas h
JOIN dim_producto    p ON p.producto_id = h.producto_id
JOIN dim_familia     f ON f.familia_id = p.familia_id
JOIN dim_departamento d ON d.departamento_id = f.departamento_id
GROUP BY d.nombre;
```

## Errores típicos

- **Partir dimensiones «por elegancia» sin medir.** Cada nivel de jerarquía que separas es una
  unión más en cada consulta, para siempre, y a menudo el ahorro de espacio es irrelevante
  porque el formato columnar ya comprime el texto repetido.
- **Creer que el copo ahorra tiempo de consulta.** Ahorra espacio, no tiempo: las uniones
  cuestan. En un motor columnar, leer una dimensión ancha y plana suele ser más rápido que
  encadenar tres uniones.
- **Mezclar los dos estilos en el mismo modelo sin criterio.** Media docena de dimensiones
  aplanadas y dos en copo, sin documentar cuáles ni por qué. Quien consulta no sabe si tiene que
  unir una tabla o tres, y acaba copiando consultas ajenas sin entenderlas.
- **No aplanar las jerarquías en la dimensión.** Tener `dim_producto` con el nombre de la
  familia pero no el departamento obliga a unir con otra tabla precisamente para el informe más
  pedido. Si la jerarquía es estable, aplánala entera.
- **Olvidar las dimensiones conformadas.** Estrella o copo, la misma `dim_fecha` y la misma
  `dim_producto` deben servir a todos los hechos. Sin eso, las comparaciones entre procesos de
  negocio no son posibles.
- **Diseñar el modelo para el diagrama y no para las consultas.** Lo que decide es qué preguntas
  se hacen cada día. Si el 80 % de los informes filtra por tienda y familia, esos dos atributos
  tienen que estar a un salto de la tabla de hechos.
- **Suponer que el copo arregla los datos sucios.** Normalizar la estructura no normaliza el
  contenido: si hay dos formas de escribir «periféricos» en el origen, seguirá habiendo dos
  categorías distintas, en estrella y en copo.

## Comprueba que lo sabes

:::quiz
p: ¿Qué diferencia práctica hay entre una estrella y un copo de nieve para quien escribe la consulta?
o: El copo necesita más uniones porque cada nivel de la jerarquía está en una tabla distinta
o: El copo no permite agregar por atributos de la dimensión
o: La estrella solo admite una dimensión por tabla de hechos
a: 1
e: La tabla de hechos y las medidas son iguales en los dos; lo que cambia es cuántas tablas hay que atravesar para llegar a un atributo. Por eso el copo multiplica las uniones, sobre todo cuando el informe usa niveles altos de la jerarquía.
:::

:::quiz
p: Con 2.000 productos y 40 familias, ¿por qué la estrella no desperdicia tanto espacio como parece?
o: Porque los formatos columnares codifican como diccionario el texto repetido y solo guardan el valor una vez
o: Porque las bases de datos borran automáticamente los textos duplicados
o: Porque 2.000 filas es poco para cualquier motor
a: 1
e: En columnar, una columna con 40 valores distintos se comprime con diccionario: se guarda el valor una vez y referencias ligeras por fila. La redundancia lógica existe, pero el coste físico es mínimo, y a cambio te ahorras uniones en cada informe.
:::

:::quiz
p: ¿Cuándo tiene sentido partir una dimensión en un copo de nieve?
o: Siempre que la dimensión tenga más de diez atributos
o: Cuando la dimensión es enorme y muy redundante, o cuando una jerarquía es compartida por varias dimensiones
o: Nunca, porque el copo está obsoleto
a: 2
e: El copo es una herramienta, no un error: se justifica con dimensiones gigantes con jerarquías profundas o con atributos compartidos entre dimensiones. Lo que no se justifica es partir por costumbre, porque cada nivel añade una unión a todas las consultas.
:::

:::nota
Estrella y copo de nieve describen la **forma de las dimensiones**, no el motor ni el tamaño. Se
pueden tener las dos en el mismo sistema, y de hecho es lo habitual: casi todo aplanado y una o
dos dimensiones partidas donde de verdad hace falta.
:::
