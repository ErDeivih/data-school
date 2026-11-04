---
id: capa-semantica-y-metricas
titulo: Capa semántica y métricas
fase: 4
nivel: avanzado
rutas: [de, ds]
prerequisitos: [dbt-y-transformacion, arquitectura-medallion, catalogo-y-linaje]
tags: [metricas, semantica, dbt, gobierno]
resumen: Definir cada métrica una sola vez, con su medida, su agregación, su grano y sus filtros, para que el cuadro, la API y el modelo devuelvan el mismo número.
fuentes: ["Reis & Housley (2022), 'Fundamentals of Data Engineering'", "Kimball & Ross (2013), 'The Data Warehouse Toolkit'"]
---

## En una frase

Una capa semántica es el único sitio donde se define qué significa una métrica —su medida, su
agregación, su grano y sus filtros—, y todo lo demás la consume: cuadros de mando, portátiles de
análisis, APIs y modelos.

## La idea

Todo el mundo conoce la escena: en el cuadro de ventas, «ingresos» es la suma de los pedidos
facturados con impuestos; en el de finanzas, la misma palabra es lo facturado menos devoluciones y
sin impuestos; en el cuaderno del analista, solo pedidos completados. Tres cifras, tres reuniones y
una discusión que no va de datos sino de definiciones. Nadie está equivocado: cada uno escribió su
fórmula en su herramienta.

Piensa en el plano del metro. Cada línea tiene su color, sus paradas y sus transbordos; si cada
oficina dibujara su propio plano, planificar un trayecto sería imposible. La capa semántica es el
plano oficial. No transporta a nadie —no guarda datos ni ejecuta nada por sí sola—, pero todos leen
el mismo dibujo.

Contiene tres cosas:

1. **Modelos semánticos.** Qué tabla es la fuente, cuál es su clave o entidad, cuáles son sus
   dimensiones (fecha, canal, país) y cuáles sus medidas (importe, pedidos, clientes). Es la
   traducción de tu [[modelado-dimensional|modelo dimensional]] a algo que la herramienta entiende.
2. **Métricas.** La medida más la agregación, el grano, las dimensiones permitidas y los filtros.
   «Ingresos netos» no es una columna de ninguna tabla: es la suma de `importe − devoluciones`
   filtrando los pedidos no cancelados. Esa frase, escrita una vez, es la métrica.
3. **El grafo de uniones.** Con qué claves se puede unir cada modelo y en qué grano, para que la
   herramienta agregue **antes** de unir y no cuente doble.

Encima de eso hay una interfaz: quien pregunta escribe el nombre de la métrica y las dimensiones,
nunca la fórmula. La herramienta compila el SQL y lo devuelve con el mismo resultado venga la
pregunta de un cuadro, de una API o de un agente. Las implementaciones que verás son el Semantic
Layer de dbt con MetricFlow, Cube y LookML de Looker; las tres hacen lo mismo con vocabulario
distinto, y las tres comparten la propiedad que importa: cambiar la definición en un sitio cambia
todos los consumidores a la vez.

Dos consecuencias prácticas:

- La pregunta deja de ser «¿de qué tabla saco esto?» y pasa a ser «¿qué métrica es esto?».
- La discusión se mueve a donde se puede resolver: la definición, con dueño, revisión y pruebas.

:::nota
La capa semántica no es el catálogo. El catálogo dice qué datos existen, quién es el dueño y cómo se
llaman las columnas ([[catalogo-y-linaje]]); la capa semántica dice cómo se calcula un número a
partir de ellos. Se complementan, pero una no sustituye a la otra.
:::

## Definición formal

Una métrica es una tupla, y cada pieza tiene que estar declarada:

:::formula
métrica = ( medida, agregación, grano, dimensiones, filtros )
:::

Símbolos:

- `medida` — la columna numérica que se va a agregar: `importe`, `pedidos`, `visitas`.
- `agregación` — cómo se colapsan las filas de esa medida: suma, recuento, recuento distinto,
  mínimo o máximo. La media solo se declara sobre una medida aditiva; un cociente se declara como
  métrica derivada de otras dos.
- `grano` — qué representa una fila de la fuente: un pedido, una línea de pedido, un día y canal.
- `dimensiones` — los cortes por los que se puede preguntar sin redefinir nada: fecha, canal, país.
- `filtros` — las filas que entran en el cálculo: pedidos no cancelados, clientes con consentimiento.
- `numerador`, `denominador` — las dos medidas que forman un ratio, como pedidos y visitas.
- `grupos` — las partes en que se trocea la pregunta (días, canales) cuando alguien promedia un
  ratio ya calculado en vez de dividir los totales.

Y la regla que más veces se rompe en producción:

:::formula
ratio del total = Σ numerador / Σ denominador   ≠   media de los ratios por grupo
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `medida` | La columna numérica que se agrega | las de la columna | Si es aditiva, la métrica escala con ella; si no lo es, sumarla da un número sin sentido |
| `agregación` | Cómo se colapsan las filas | categoría | Cambiarla cambia la métrica entera: `sum` y `count distinct` no son intercambiables |
| `grano` | Qué representa una fila de la fuente | categoría | Un grano más fino multiplica filas; agregar después de unir duplica el total |
| `dimensiones` | Cortes por los que se puede preguntar | categoría | Añadir una dimensión no cambia el total si cubre todas las filas; si deja filas fuera, el total baja |
| `filtros` | Filas que entran en el cálculo | condición | Cada fila extra mueve el numerador y el denominador a la vez |
| `numerador` | Parte de arriba del ratio | las de la medida | El ratio sube en proporción directa |
| `denominador` | Parte de abajo del ratio | las de la medida | El ratio baja; con denominadores pequeños el ratio se dispara |
| `grupos` | Cuántos grupos promedias si te equivocas | recuento | Cuanto más desiguales son los tamaños, más se aleja la media de ratios del ratio real |
:::

Dos reglas que hay que poder comprobar en cualquier capa semántica:

:::formula
toda medida tiene un grano declarado   ·   toda métrica tiene un dueño
:::

## Ejemplo

La tasa de conversión de tres días, con visitas y pedidos:

| Día | Visitas | Pedidos | Conversión |
| --- | --- | --- | --- |
| Lunes | 50 | 12 | 24,0 % |
| Martes | 400 | 20 | 5,0 % |
| Miércoles | 250 | 25 | 10,0 % |
| Total | 700 | 57 | 8,14 % |

La media de las conversiones diarias es (24,0 + 5,0 + 10,0) / 3 = **13,0 %**, y el ratio del total es
57 / 700 = **8,14 %**. La primera cifra es un 60 % más alta que la segunda y es la que sale de
cualquier cuadro que guarde una columna `conversion` por día y luego la promedio. El error no está en
el cálculo: está en promediar ratios en vez de dividir los totales.

:::figura
fichero: capa-semantica-y-metricas-media-de-ratios
pie: A la izquierda, la conversión de cada día en barras y las dos líneas que compiten por resumirlas: la discontinua naranja es la media de los ratios (13,0 %) y la roja continua es el ratio del total (8,14 %). La media queda por encima porque da el mismo peso al lunes que al martes. A la derecha está la información que esa media ignora, el tráfico de cada día: el de conversión más baja, el 5 %, es el que más visitas tuvo, 400, y por eso debe pesar más en el total. Cuando definas una métrica de ratio, guárdala como numerador y denominador, nunca como un porcentaje ya calculado.
fuente: figuras/capa-semantica-y-metricas-1.py
:::

El segundo caso es el de la unión. Una tabla de pedidos con dos filas (100 € y 50 €) unida a su
detalle de tres líneas devuelve tres filas, y la suma de `total` pasa de 150 € a 250 €. La medida
`total` vive en la tabla de pedidos, en un grano, y hay que agregarla **antes** de unir el detalle.
En cuanto la capa semántica declara el grano y el camino de unión, la herramienta hace ese orden por
ti, y el fan-out deja de ser un accidente.

El tercer caso es el de la medida no aditiva: `clientes_activos` cuenta 1.000 cada día y sumar los 30
días da 30.000, pero los clientes distintos del mes pueden ser 4.200. La métrica se declara con
recuento distinto y se prohíbe sumarla sobre el tiempo. La misma trampa aparece con saldos e
inventario: sumar el saldo de cada día no es el saldo del mes.

## Código

```python verificable
import numpy as np

visitas = np.array([50, 400, 250])
pedidos = np.array([12, 20, 25])

# Correcto: se agregan las componentes y se divide una sola vez
total = pedidos.sum() / visitas.sum() * 100
# Incorrecto: se promedian ratios ya calculados. Cada dia pesa igual, tenga 50 o 400 visitas
media = (pedidos / visitas).mean() * 100

print(f"ratio del total   {total:.2f} %")    # -> 8.14
print(f"media de ratios   {media:.2f} %")    # -> 13.00
print(f"sobreestima       {media / total:.2f} veces")   # -> 1.60
```

:::claves
- `pedidos / visitas` divide **elemento a elemento** y devuelve un array de la misma forma que las
  entradas. Sobre ese array, `.mean()` es la media de ratios que hay que evitar; no es un promedio
  ponderado por visitas.
- `pedidos.sum()` es un escalar de NumPy. La división de dos escalares da un `float64` de doble
  precisión: `0.08142857142857142`, no un decimal exacto. Redondear es trabajo del `print`.
- El `.2f` de la f-string redondea **al imprimir**, no al calcular: `total` sigue guardando todos los
  decimales, y una cadena de cálculos hecha a partir de la cadena impresa arrastraría otro número.
- `ddof` no aparece aquí, pero vuelve en cuanto calcules varianzas: NumPy usa `ddof=0` y pandas `1`, así
  que la misma columna da dos desviaciones distintas según la librería.
- `visitas` y `pedidos` son `int64`; al dividir, NumPy asciende a coma flotante. Si los hubieras
  pasado por `//`, obtendrías enteros truncados y el ratio saldría mal sin avisar.
- Si tus datos vinieran en un DataFrame con una columna `conversion` ya calculada, no hay forma de
  recuperar el ratio del total sumando esa columna: hay que volver a las componentes. Por eso la capa
  semántica guarda medidas y no ratios.
:::

```python verificable
import pandas as pd

pedidos = pd.DataFrame({"pedido_id": [1, 2], "total": [100.0, 50.0]})
lineas = pd.DataFrame({"pedido_id": [1, 1, 2], "importe": [60.0, 40.0, 50.0]})

# La medida 'total' vive en pedidos: su valor correcto es la suma sin unir
correcto = pedidos["total"].sum()
# Al unir el detalle, cada pedido se repite una vez por linea y su total se cuenta de mas
unido = pedidos.merge(lineas, on="pedido_id")
print("filas antes", len(pedidos), "filas despues", len(unido))
print(f"suma correcta {correcto:.1f}")
print(f"suma tras unir {unido['total'].sum():.1f}")
# -> filas antes 2 filas despues 3
# -> suma correcta 150.0
# -> suma tras unir 250.0
```

```yaml
# Definicion de la metrica en un Semantic Layer tipo MetricFlow: medida, agregacion y ratio.
semantic_models:
  - name: pedidos
    model: ref('fact_pedidos')
    entities:
      - name: pedido
        type: primary
      - name: cliente
        type: foreign
    dimensions:
      - name: fecha_pedido
        type: time
        type_params:
          time_granularity: day
    measures:
      - name: importe_neto
        agg: sum
        expr: importe - devoluciones

metrics:
  - name: ingresos_netos
    type: simple
    type_params:
      measure: importe_neto
  - name: ticket_medio
    type: ratio
    type_params:
      numerator: ingresos_netos
      denominator: pedidos
```

## Errores típicos

- **Dejar que cada cuadro escriba su fórmula.** Es el origen del problema: dos números distintos para
  la misma palabra. La métrica se declara una vez y se consume; si un cuadro necesita otra cosa, es
  otra métrica, con su nombre y su dueño.
- **Promediar ratios.** La media de conversiones diarias dio 13,0 % cuando el ratio real era 8,14 %.
  Los ratios se calculan dividiendo totales, no promediando divisiones, porque cada grupo tiene un
  tamaño distinto.
- **Sumar medidas no aditivas.** Clientes distintos, saldos, inventario y usuarios activos no se
  suman sobre el tiempo. Necesitan recuento distinto o la última foto del periodo, y eso se declara
  en la métrica, no se decide en el cuadro.
- **Unir antes de agregar.** El fan-out del ejemplo convirtió 150 € en 250 € sin ningún error de
  sintaxis. La agregación va antes de la unión, en el grano que la medida declara.
- **Definir la métrica sin grano ni filtro.** «Ingresos» sin decir si son brutos o netos, ni si son
  del día o acumulados del mes, no es una métrica: es una palabra. El grano y el filtro son parte de
  la definición, igual que la agregación.
- **Esperar que la capa semántica limpie los datos.** Agrega de forma consistente y evita fan-outs,
  pero si en el origen hay pedidos duplicados, el resultado será un total duplicado y perfectamente
  coherente. La calidad se arregla aguas arriba ([[calidad-y-slas]]); la semántica arregla la
  coherencia.

## Comprueba que lo sabes

:::practica
enunciado: Tienes visitas y pedidos de tres días: 80 visitas y 16 pedidos, 600 visitas y 30 pedidos, 320 visitas y 40 pedidos. Calcula el ratio del total y la media de los ratios diarios, y explica cuál de los dos debe publicarse como tasa de conversión.
pista: Suma primero los pedidos y las visitas por separado; después compara con la media de las tres conversiones diarias.
solucion: Los totales son 16 + 30 + 40 = 86 pedidos y 80 + 600 + 320 = 1.000 visitas, así que el ratio del total es 86 / 1.000 = 8,6 %. Las conversiones diarias son 20,0 %, 5,0 % y 12,5 %, y su media es 12,5 %, un 45 % más alta. Se publica el 8,6 %: la media de ratios da el mismo peso a un día de 80 visitas que a uno de 600, y no responde a la pregunta «de cada 100 visitas, cuántas acaban en pedido».
:::

:::quiz
p: Un cuadro guarda una columna `conversion` por día y hace la media del mes. ¿Qué obtiene?
o: La conversión del mes, porque la media de las conversiones diarias es el promedio
o: Un valor más alto que la conversión real, porque cada día pesa igual aunque tenga muy pocas visitas
o: Un valor más bajo, porque los días malos se compensan con los buenos
a: 2
e: La media de ratios pondera igual todos los grupos: un día con 50 visitas y un 24 % pesa lo mismo que uno con 400 visitas y un 5 %. En el ejemplo la media daba 13,0 % frente al 8,14 % real. El ratio del mes se calcula sumando pedidos y visitas por separado y dividiendo al final.
:::

:::quiz
p: Una tabla de pedidos con dos filas (100 € y 50 €) se une a su detalle de líneas y después se suma la columna `total`. ¿Qué pasa?
o: Sale 150 €, porque la suma ignora las filas repetidas
o: Sale 250 €, porque el pedido de 100 € aparece una vez por cada línea de su detalle
o: La consulta falla con un error de clave duplicada
a: 2
e: Es el fan-out: al unir en un grano más fino, cada fila de la izquierda se repite tantas veces como coincidencias tenga. La solución no es un `distinct` a posteriori, sino declarar el grano de la medida y agregar antes de unir; la capa semántica hace ese reordenado por ti. Unir dos tablas con claves repetidas nunca da error por sí solo.
:::

:::quiz
p: Quieres publicar «clientes activos del mes» a partir de un recuento diario de 1.000 clientes. ¿Cómo se define la métrica?
o: Sumando los 1.000 clientes de cada día del mes
o: Con un recuento distinto de cliente sobre todo el mes, porque sumar días cuenta al mismo cliente muchas veces
o: Con el máximo diario del mes, que siempre es el valor correcto
a: 2
e: Sumar recuentos diarios cuenta 30 veces al cliente que compró todos los días: 30.000 en vez de los 4.200 distintos del ejemplo. Es una medida no aditiva en el tiempo y se declara con recuento distinto; el máximo diario tampoco sirve, porque la actividad se reparte entre días y perderías clientes.
:::
