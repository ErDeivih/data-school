---
id: arquitectura-medallion
titulo: Arquitectura medallion
fase: 4
nivel: intermedio
rutas: [de]
prerequisitos: [data-lake, etl-vs-elt, data-warehouse]
tags: [arquitectura, capas, calidad, lakehouse]
resumen: Bronce, plata y oro: tres capas con responsabilidades distintas que se reconstruyen en cadena para que la calidad del dato se pueda auditar.
fuentes: ["Databricks (2021), 'Medallion lakehouse architecture'"]
---

## En una frase

La arquitectura medallion organiza un lago de datos en tres capas —bronce con lo que llegó,
plata limpia y conforme, oro agregada para el negocio— de forma que cada capa tenga un
consumidor claro, una promesa distinta y se pueda reconstruir entera desde la anterior.

## La idea

Piensa en una planta potabilizadora. El agua entra del río tal cual, con barro, hojas y piedras.
Nadie bebe de ahí, pero tampoco se tira nada: se guarda una muestra de lo que entró, porque si
mañana aparece un problema habrá que saber qué llegó exactamente. Después pasa por la planta:
se filtra, se decanta, se analiza. Y al final sale embotellada, etiquetada y lista para el
consumidor, que no quiere saber nada de la planta, solo quiere abrir la botella.

Las tres capas son eso:

- **Bronce** es la toma del río. Guardas el dato tal como llegó, sin interpretarlo, en un
  formato abierto y añadiendo metadatos de ingesta (cuándo entró, de qué fichero o de qué
  sistema). No se borra nada, no se corrige nada, no se decide nada. Su promesa es una sola:
  *esto es exactamente lo que nos dio el origen, y se puede volver a leer*.
- **Plata** es la planta. Aquí sí se decide: se deduplica, se tipan las columnas, se unifican
  códigos, se resuelven las claves, se aplican reglas de negocio (un pedido cancelado no cuenta
  como venta). La promesa es: *una fila por entidad y evento, con tipos y reglas estables*.
- **Oro** es la botella. Tablas agregadas por pregunta de negocio, casi siempre con
  [[modelado-dimensional|modelado dimensional]], listas para que las consuma una herramienta de
  BI sin pensar. La promesa es: *esta tabla responde a esta pregunta y está pensada para leerla
  rápido*.

Lo que hace útil la arquitectura no son los nombres ni el color, es la **dirección de las
dependencias**. Los datos fluyen solo hacia abajo (bronce → plata → oro) y cada capa se
reconstruye por completo desde la anterior. Eso te da tres cosas:

1. **Reproceso honesto.** Cuando descubres que un importe estaba mal calculado, cambias la regla
   en plata y regeneras plata y oro desde bronce. No hay que pedirle los datos otra vez al
   sistema de origen, que probablemente ya los borró.
2. **Auditoría.** Si el número del informe no cuadra, puedes bajar por la cadena y encontrar en
   qué capa se torció: en un dato que llegó mal, en una regla de limpieza o en una agregación.
3. **Consumidores separados.** El científico de datos trabaja en plata, el analista de negocio
   en oro, y ninguno de los dos pisa el trabajo del otro.

Y hay un detalle que se olvida siempre: cada capa debe tener **dueño, contrato y recuento**. Si
nadie sabe cuántas filas debería tener plata, no hay forma de detectar que dejó de llegar un
día entero de datos. Medallion sin métricas por capa es solo una carpeta con tres
subcarpetas.

## Definición formal

Con `B`, `P` y `O` los conjuntos de tablas de bronce, plata y oro, y `T` una tabla cualquiera:

- **Bronce:** `T_b` es una copia append-only de la fuente, con esquema declarado como texto
  (todo lo que llega es «string hasta que se demuestre lo contrario») más columnas de linaje
  `_origen`, `_fichero`, `_ingerido_en`. No hay `UPDATE`, no hay `DELETE`, no hay reglas de
  negocio.
- **Plata:** `T_p = f(T_b)` con `f` una transformación determinista que aplica tipado,
  deduplicación por clave y reglas de negocio. La misma entrada debe producir la misma salida,
  siempre ([[idempotencia-y-reintentos|idempotencia]]).
- **Oro:** `T_o = g(T_p)` con `g` una agregación por grano de negocio. Nunca depende de `T_b`
  directamente.
- **Reconstruibilidad:** `g(f(B)) = O` para cualquier estado válido de bronce. Si para generar
  oro hace falta algo que no está en bronce, la cadena está rota.

:::formula
O = g(f(B))     y     f y g deterministas
recuento(capa) + reglas de calidad por capa = capa auditable
:::

## Ejemplo

Un día de pedidos en una tienda con cuatro países. Los números son estos:

| Capa | Filas | Qué se hizo |
| --- | --- | --- |
| Bronce | 1.000.000 | copia exacta del origen: 3.000 duplicados exactos y 12.000 filas sin importe |
| Plata | 997.000 | duplicados fuera por clave de pedido; las 12.000 sin importe se marcan, no se borran |
| Plata (válidas) | 985.000 | filas que entran en las métricas de venta |
| Oro | 124 | 31 días × 4 países, con pedidos y facturación |

Con un importe medio de 5,00 €, la facturación que publica oro es 985.000 × 5,00 € =
**4.925.000 €**, y ese total tiene que coincidir exactamente con la suma de la capa plata. Si no
coincide, el error está en la agregación, no en los datos.

Dos decisiones de diseño que se ven en esta tabla y conviene copiar:

- Los duplicados **se eliminan** en plata, porque son el mismo hecho repetido por la ingesta.
- Las filas sin importe **no se eliminan**: se marcan con una columna `importe_valido = false`.
  Borrarlas sería perder la prueba de que ese pedido existió, y el día que el origen se arregle
  ya no tendrías con qué recuperarlo. La regla general: se marca y se documenta; se borra solo
  cuando el dato es basura demostrable.

## Código

```python verificable
# El embudo de calidad de las tres capas, con los numeros del ejemplo.
crudas = 1_000_000
duplicadas = 3_000            # repeticiones exactas de la ingesta
sin_importe = 12_000          # filas que llegaron sin importe

plata = crudas - duplicadas
validas = plata - sin_importe
importe_medio = 5.00

print(f"bronce  {crudas:>10,} filas")
print(f"plata   {plata:>10,} filas   (-{duplicadas / crudas:.1%} duplicadas)")
print(f"validas {validas:>10,} filas   (-{sin_importe / crudas:.1%} sin importe)")
print(f"oro: facturado {validas * importe_medio:>12,.2f} EUR")
```

```sql verificable
-- Bronce guarda lo que llego; plata limpia y deduplica; oro agrega para el negocio.
WITH bronce(pedido_id, fecha, cliente, importe, pais) AS (
    VALUES
        (1, DATE '2024-01-02', 'ana',   10.5,  'ES'),
        (2, DATE '2024-01-02', 'luis',  20.0,  'ES'),
        (2, DATE '2024-01-02', 'luis',  20.0,  'ES'),   -- duplicado de la ingesta
        (3, DATE '2024-01-03', 'ana',   NULL,  'ES'),   -- importe que no llego
        (4, DATE '2024-01-03', 'marta', 5.25,  'FR')
),
plata AS (
    SELECT DISTINCT pedido_id, fecha, cliente, importe, pais
    FROM bronce
    WHERE importe IS NOT NULL
)
SELECT pais, count(*) AS pedidos, round(sum(importe), 2) AS facturado
FROM plata
GROUP BY pais
ORDER BY pais;
```

## Errores típicos

- **Meter reglas de negocio en bronce.** Si en la ingesta descartas los pedidos cancelados
  «porque no sirven», el día que negocio quiera analizar cancelaciones no tienes los datos: el
  sistema de origen ya los purgó. Bronce no interpreta.
- **Saltarse plata y construir oro directamente desde bronce.** Cada tabla de oro acaba
  repitiendo su propia limpieza, y a la tercera tabla las reglas ya no coinciden: dos informes
  con cifras distintas sobre el mismo mes. La limpieza va una sola vez, en plata.
- **Reprocesar solo la capa de oro.** Si corriges un dato en plata y regeneras únicamente oro, el
  histórico sigue mal en las capas anteriores y los recuentos dejan de cuadrar. Las capas se
  regeneran **en orden**, aguas abajo.
- **Confundir medallion con una herramienta.** No hace falta [[lakehouse-y-table-formats|Delta,
  Iceberg o Hudi]] para tener tres capas; ayudan (viaje en el tiempo, borrado por clave), pero la
  arquitectura es una decisión de responsabilidades, no una compra.
- **Dejar que bronce se convierta en un vertedero.** Sin política de retención, sin catálogo y
  sin dueño, en dos años tienes 400 TB de copias que nadie sabe si se pueden borrar. Ver
  [[gobierno-y-privacidad|gobierno y privacidad del dato]] y
  [[catalogo-y-linaje|catálogo y linaje]].
- **No medir cada capa.** Sin recuento, sin frescura y sin reglas de calidad por capa no puedes
  detectar que plata dejó de actualizarse; te enteras por el informe de dirección. Define
  [[calidad-y-slas|acuerdos de nivel de servicio]] por capa.

## Comprueba que lo sabes

:::quiz
p: Llegas por la mañana y el informe de ventas de oro está mal porque una regla de limpieza de plata era incorrecta. ¿Qué hay que hacer?
o: Corregir la regla en plata y regenerar plata y oro desde bronce, en orden
o: Corregir directamente las filas de oro, que es la capa que ve el negocio
o: Volver a pedir los datos al sistema de origen y recargar bronce entero
a: 1
e: Bronce conserva el dato original, así que se puede recalcular todo desde ahí. Corregir solo oro deja las capas anteriores incoherentes y no arregla los demás informes. Pedir de nuevo al origen es innecesario (y a veces imposible, porque ya no los tiene).
:::

:::quiz
p: ¿Por qué las 12.000 filas sin importe se marcan en plata en vez de borrarse?
o: Porque borrar filas en un lago de datos es técnicamente imposible
o: Porque son la prueba de que ese pedido existió y se podrán recuperar cuando el origen se corrija; borrarlas pierde información irrecuperable
o: Porque ocupan muy poco espacio y no compensa borrarlas
a: 2
e: La decisión no es de espacio ni de capacidad técnica: en un lago moderno se puede borrar. Se marcan porque son trazabilidad: el recuento de bronce a plata debe poder explicarse, y si el origen arregla el dato, la fila sigue ahí para reprocesarla.
:::

:::aviso
Medallion no dice **cuántas** capas necesita tu caso. Un pipeline pequeño puede vivir con dos
(bronce y oro) sin ningún problema. Las tres capas aparecen cuando hay varios consumidores con
necesidades distintas y quieres una única definición de «dato limpio» en medio. Añadir una capa
que nadie consulta solo añade un trabajo que puede fallar.
:::
