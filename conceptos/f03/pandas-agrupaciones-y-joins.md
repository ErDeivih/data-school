---
id: pandas-agrupaciones-y-joins
titulo: Pandas: agrupaciones y uniones
fase: 3
nivel: intermedio
rutas: [core, ds, de]
prerequisitos: [pandas-fundamentos, sql-agregaciones-y-group-by, sql-joins]
tags: [pandas, groupby, merge, pivot]
resumen: Agrupar y unir resuelven casi toda la transformación de tablas; el resto es saber cuándo apply es la respuesta equivocada y por qué una clave duplicada infla los totales.
fuentes: ["McKinney (2017), 'Python for Data Analysis'"]
---

## En una frase

Agrupar es partir la tabla por el valor de una clave, calcular algo en cada trozo y volver a
juntarlos; unir es pegar dos tablas por una clave común, y su trampa principal es que las claves
repetidas multiplican filas.

## La idea

Agrupar es lo que hace un cajero al cerrar: coge el montón de facturas, las reparte en pilas por
cliente, suma cada pila y apunta el total. Nadie suma las 4.000 facturas de una en una; el
trabajo se organiza en tres fases, y ese es exactamente el modelo de `groupby`:

1. **Partir** (*split*) — separar las filas según el valor de una o varias columnas.
2. **Aplicar** (*apply*) — calcular algo dentro de cada grupo: una suma, una media, un ranking,
   un porcentaje del total.
3. **Combinar** (*combine*) — juntar los resultados, que pueden ser **una fila por grupo** (una
   agregación) o **una fila por fila original** (una transformación).

Esa diferencia entre «una fila por grupo» y «una fila por fila» es la que decide si usas `agg` o
`transform`, y es la causa de la mitad de los errores de forma al añadir columnas calculadas. Si
quieres el total del grupo para compararlo con cada factura, necesitas `transform`: devuelve el
mismo número de filas que la tabla original.

Unir es distinto: es pegar dos tablas por una clave. La idea intuitiva («como un BUSCARV») es
correcta pero incompleta, porque oculta el detalle que arruina los informes: **si la clave se
repite en la tabla de la derecha, cada fila de la izquierda se empareja con todas sus
coincidencias**. Un pedido que se une con dos descuentos vigentes del mismo cliente produce dos
filas, y la suma de importes de la tabla resultante cuenta ese pedido dos veces. No hay error, no
hay aviso: hay un total inflado.

## Definición formal

**Agrupación.** Sea una tabla con `n` filas y una clave `g` que toma valores `1…k`. El resultado
de `df.groupby(g).agg(f)` tiene una fila por valor distinto de `g`, y en cada una el valor
`f` aplicado al subconjunto de filas con ese valor.

- `agg` — una fila por grupo. Admite varias funciones a la vez y nombres nuevos:
  `df.groupby("g").agg(total=("v", "sum"), media=("v", "mean"))`.
- `transform` — una fila por fila original, con el resultado del grupo repetido.
- `filter` — descarta grupos enteros según una condición sobre el grupo.
- `size()` — número de **filas** de cada grupo (cuenta los nulos). `count()` — número de valores
  **no nulos** de cada columna. No son lo mismo.
- Por defecto `groupby(dropna=True)` **descarta** las filas cuya clave es nula: esos grupos no
  aparecen en el resultado y los totales no cuadran con la tabla original.

**Unión.** Para una unión interna por la clave `k`, el número de filas del resultado es

:::formula
n_resultado = Σ_k n_izquierda(k) · n_derecha(k)
:::

donde `n_izquierda(k)` es cuántas filas de la tabla izquierda tienen la clave `k`. Si todas las
claves de la derecha son únicas, el resultado tiene exactamente las filas de la izquierda que
tienen pareja; si alguna se repite, las filas se multiplican. Herramientas para no caer en ello:

- `validate="one_to_one"`, `"one_to_many"`, `"many_to_one"` o `"many_to_many"` — Pandas lanza
  `MergeError` si la relación real no es la que declaras. Es la comprobación que hay que poner
  siempre que la clave no sea evidentemente única.
- `indicator=True` — añade una columna `_merge` que dice si cada fila vino de la izquierda, de la
  derecha o de las dos (`both`, `left_only`, `right_only`).
- `how` — `inner` (solo las claves presentes en las dos), `left` (todas las de la izquierda),
  `right`, `outer` (la unión de todas). Las claves sin pareja se rellenan con `NaN`.
- `pivot_table(index=…, columns=…, values=…, aggfunc=…)` — es un `groupby` de dos claves seguido
  de un `unstack`. `aggfunc` por defecto es `"mean"`, no `"sum"`.

## Ejemplo

Dos tablas diminutas. Pedidos, con el cliente:

```
pedido   cliente
     1         A
     2         A
     3         B
```

Y descuentos vigentes, también por cliente:

```
cliente   descuento
      A         0,10
      A         0,20
      B         0,30
```

La unión interna por `cliente` no da 3 filas, da **5**: `n(A) = 2 · 2 = 4` y `n(B) = 1 · 1 = 1`.
El pedido 1 aparece dos veces y el 2 también. Si después haces `resultado["importe"].sum()`,
cuentas dos veces los pedidos de A.

En la dirección contraria, si la derecha hubiera tenido una sola fila por cliente, el resultado
tendría 3 filas y el mismo número de filas que la izquierda. Esa es la señal que hay que
comprobar siempre: **¿cuántas filas tenía la izquierda y cuántas tiene el resultado?**

Un ejemplo de agrupación con números. Cinco ventas, tres en Sevilla:

```
ciudad     importe
Madrid        10,0
Madrid        30,0
Sevilla        5,0
Sevilla       15,0
Sevilla       25,0
```

- Total por ciudad: Madrid **40,0**, Sevilla **45,0**.
- Número de ventas: Madrid **2**, Sevilla **3**.
- Media de Sevilla: (5 + 15 + 25) / 3 = **15,0**, y con `transform("mean")` esa media aparece en
  las tres filas de Sevilla, para poder restarla y ver qué venta está por encima de su media.

## Código

```python verificable
import pandas as pd

ventas = pd.DataFrame({
    "ciudad": ["Madrid", "Madrid", "Sevilla", "Sevilla", "Sevilla"],
    "importe": [10.0, 30.0, 5.0, 15.0, 25.0],
})

print(ventas.groupby("ciudad")["importe"].sum().to_dict())    # -> {'Madrid': 40.0, 'Sevilla': 45.0}
print(ventas.groupby("ciudad")["importe"].size().to_dict())   # -> {'Madrid': 2, 'Sevilla': 3}

# transform devuelve una fila por fila original: sirve para comparar cada venta con su grupo
ventas["media_ciudad"] = ventas.groupby("ciudad")["importe"].transform("mean")
print(ventas["media_ciudad"].tolist())   # -> [20.0, 20.0, 15.0, 15.0, 15.0]
```

```python verificable
import pandas as pd

izq = pd.DataFrame({"pedido": [1, 2, 3], "cliente": ["A", "A", "B"]})
der = pd.DataFrame({"cliente": ["A", "A", "B"], "descuento": [0.1, 0.2, 0.3]})

print(len(izq), len(der))                          # -> 3 3
print(len(izq.merge(der, on="cliente")))           # -> 5   (2*2 + 1*1: la clave de la derecha se repite)

# validate convierte el error silencioso en una excepcion explicita
try:
    izq.merge(der, on="cliente", validate="many_to_one")
    print("sin error")
except Exception as e:
    print(type(e).__name__)                        # -> MergeError

# indicator dice de donde vino cada fila, sin adivinar
unida = izq.merge(der, on="cliente", how="outer", indicator=True)
print(int((unida["_merge"] == "both").sum()))      # -> 5
```

```python verificable
import pandas as pd

g = pd.DataFrame({"ciudad": ["M", "M", "S"], "importe": [10.0, None, 5.0]})
print(g.groupby("ciudad")["importe"].size().to_dict())    # -> {'M': 2, 'S': 1}  (filas)
print(g.groupby("ciudad")["importe"].count().to_dict())   # -> {'M': 1, 'S': 1}  (no nulos)

# Las claves nulas desaparecen del groupby salvo que lo pidas explicitamente
k = pd.DataFrame({"g": ["a", None, "a"], "v": [1.0, 2.0, 3.0]})
print(k.groupby("g")["v"].sum().to_dict())               # -> {'a': 4.0}
print(len(k.groupby("g", dropna=False)["v"].sum()))      # -> 2

piv = pd.DataFrame({"mes": ["ene", "ene", "ene", "feb"],
                    "ciudad": ["M", "M", "S", "M"],
                    "importe": [1.0, 2.0, 4.0, 8.0]})
print(piv.pivot_table(index="mes", columns="ciudad", values="importe", aggfunc="sum").to_numpy().tolist())
# -> [[3.0, 4.0], [8.0, nan]]
print(piv.pivot_table(index="mes", columns="ciudad", values="importe").to_numpy().tolist())
# -> [[1.5, 4.0], [8.0, nan]]  (sin aggfunc, pivot_table usa la media)
```

## Errores típicos

- **Unir sin comprobar la unicidad de la clave.** Es el error que más cifras erróneas produce en
  informes reales: el total sale más alto que la fuente y nadie sabe por qué. Compara
  `len(izq)` con `len(resultado)`, usa `validate=` y, si el resultado debe tener una fila por
  fila de la izquierda, no sigas hasta que lo tenga.
- **Confundir `count` con `size`.** Con nulos de por medio dan números distintos: `size` cuenta
  filas y `count` cuenta valores no nulos. Si tu media de «nº de operaciones por cliente» usa
  `count` sobre una columna con nulos, estás midiendo otra cosa.
- **Olvidar que `groupby` descarta las claves nulas.** Los grupos cuyo valor de clave es `NaN`
  no aparecen y su importe desaparece del total sin aviso. Usa `dropna=False` si quieres verlos.
- **Usar `apply` con una función de Python donde hay `agg`.** `groupby(...).apply(mi_funcion)`
  ejecuta Python por grupo y devuelve formas difíciles de predecir; `agg` y `transform` usan
  rutinas compiladas. Reserva `apply` para lo que no se puede expresar de otra forma.
- **Confundir `merge` con `concat`.** `merge` empareja por clave; `concat` pega por posición o
  por índice. Un `concat` donde querías un `merge` junta filas que no tienen nada que ver y
  produce una tabla con el doble de columnas y todos los valores desalineados.
- **Unir columnas con tipos distintos.** Pandas no convierte por ti: unir una clave de texto con
  una de entero lanza `ValueError: You are trying to merge on str and int64 columns`. Comprueba los
  dtypes de las dos claves antes de unir y conviértelos con `astype` de forma explícita, porque el
  error aparece al final del pipeline, cuando ya has escrito toda la transformación.

:::practica
enunciado: `pedidos` tiene tres filas (cliente A, A, B) con importes 2, 3, 6. `regiones` tiene dos filas (A norte, B sur). Escribe el código que calcula el total por cliente, lo une con las regiones y saca el total por región. Comprueba además con `validate` que la clave de regiones es única.
pista: Primero `groupby` con `agg`, después `merge`; el `validate` convierte en excepción el fan-out silencioso.
solucion: `pedidos.groupby("cliente")["importe"].sum()` da `{A: 5, B: 6}`. La unión `res.merge(regiones, on="cliente", validate="many_to_one")` funciona, da 2 filas (una por cliente) y con `groupby("region")["importe"].sum()` sale norte 5,0 y sur 6,0. Si la clave de la derecha se repitiera, `validate="many_to_one"` lanzaría `MergeError` en vez de devolver una tabla con más filas de las que tenía la izquierda.
:::

## Comprueba que lo sabes

:::quiz
p: La tabla de pedidos tiene 1.000 filas y la de descuentos 1.000 filas, todas con el mismo cliente. ¿Cuántas filas tiene la unión interna por cliente?
o: 1.000, porque el cliente es el mismo
o: 1.000.000, porque cada pedido se empareja con cada descuento
o: 2.000, porque se suman las dos tablas
a: 2
e: La cardinalidad de una unión interna es la suma de productos n_izq(k) · n_der(k) por clave: con una sola clave de 1.000 contra 1.000 son 1.000.000 de filas. Es el caso extremo del fan-out y la razón de usar `validate` antes de unir.
:::

:::quiz
p: Quieres añadir a cada fila de ventas la media de su ciudad, sin cambiar el número de filas. ¿Qué usas?
o: `groupby("ciudad")["importe"].agg("mean")`
o: `groupby("ciudad")["importe"].transform("mean")`
o: `groupby("ciudad")["importe"].size()`
a: 2
e: `transform` devuelve un resultado con la misma forma que la entrada, con el valor del grupo repetido en cada fila; `agg` devuelve una fila por grupo (y al asignarla al DataFrame daría un error de longitud o alinearía por índice), y `size` cuenta filas.
:::

:::quiz
p: `pivot_table(index="mes", columns="ciudad", values="importe")` sin `aggfunc` sobre importes 1,0 y 2,0 en la misma celda, ¿qué muestra?
o: 3,0, porque suma por defecto
o: 1,5, porque agrega con la media por defecto
o: Un error, porque falta `aggfunc`
a: 2
e: El valor por defecto de `aggfunc` en `pivot_table` es la media, así que la celda muestra 1,5. Si querías el total hay que escribir `aggfunc="sum"` de forma explícita, y esa diferencia explica muchos totales que no cuadran.
:::

:::aviso
Todo lo que se hace con `groupby` y `merge` se puede hacer con SQL, y casi siempre con menos
código: `GROUP BY` para agrupar (ver [[sql-agregaciones-y-group-by]]) y `JOIN` para unir (ver
[[sql-joins]]). La ventaja de Pandas es que el resultado queda en memoria para seguir trabajando;
la de SQL, que el motor optimiza el plan por ti.
:::
