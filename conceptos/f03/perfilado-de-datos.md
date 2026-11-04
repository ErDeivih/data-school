---
id: perfilado-de-datos
titulo: Perfilado y EDA automático
fase: 3
nivel: intermedio
rutas: [de, ds]
prerequisitos: [calidad-de-datos, pandas-fundamentos]
tags: [perfilado, eda, cardinalidad, exploracion]
resumen: Describir una tabla desconocida con números -tipo real, nulos, cardinalidad, rangos y valores frecuentes- antes de escribir una sola transformación.
fuentes: ["Tukey (1977), 'Exploratory Data Analysis'", "Kimball y Ross (2013), 'The Data Warehouse Toolkit'"]
---

## En una frase

Perfilar es pasar una batería de medidas estándar sobre una tabla que no conoces —cuántas filas
tiene, qué tipos hay de verdad, cuántos nulos, cuántos valores distintos y cuáles se repiten— para
decidir con datos qué mirar después.

## La idea

Llegas a un proyecto nuevo y te encuentras cuarenta tablas con nombres como `tbl_gen_f1`,
`maestro_v2` y `stg_pedidos_bis`. Antes de escribir una transformación necesitas responder
preguntas muy concretas, y ninguna se contesta mirando las primeras veinte filas:

- ¿Cuál es el **grano**? ¿Una fila por pedido o por línea de pedido? Si te equivocas en esto,
  todos los totales salen mal por un factor que nadie ve.
- ¿Qué columna identifica una fila? ¿Hay duplicados?
- ¿Qué columnas son **constantes** y por tanto inútiles (o peor: un filtro escondido)?
- ¿La columna que se llama `fecha_alta` es una fecha o es texto? ¿Y el `importe` es número o
  lleva la coma decimal dentro de una cadena?
- ¿Qué valores raros se repiten? Un `1900-01-01` que aparece miles de veces, un `-1`, un `9999`.
- ¿Cómo se distribuyen las columnas numéricas y qué hay en las colas?

Perfilar es eso: una analítica de sangre antes de decidir qué estudiar a fondo. Es una batería de
medidas baratas, automáticas y comparables, que se guarda como línea base. Y esa última parte es
la que casi todo el mundo olvida: un perfil que no se guarda no sirve para detectar que el mes
que viene los datos han cambiado.

Tres límites que conviene tener claros para no pedirle al perfilado lo que no da:

1. **No dice si el dato es correcto.** Un perfil puede decirte que la provincia tiene 52 valores
   distintos y una frecuencia razonable; no puede decirte si el cliente vive donde dice. Eso es
   exactitud y se audita contra el mundo, no contra la tabla (ver [[calidad-de-datos]]).
2. **No conoce las reglas de negocio.** Que `fecha_fin` sea anterior a `fecha_inicio` en 300 filas
   es una incoherencia, pero solo la detecta una regla que alguien escriba a mano.
3. **No sustituye al EDA.** El perfilado mira columna a columna y no ve relaciones. Las preguntas
   de verdad —«¿por qué este segmento factura el triple?»— se contestan después, con
   [[eda-pasos|el método del análisis exploratorio]] y con gráficos.

El enemigo silencioso del perfilado es la **normalización pendiente**. `Madrid`, `madrid` y
` Sevilla` son tres valores distintos para el motor y uno solo para el negocio. Si mides
cardinalidad sin normalizar, cuentas tres categorías donde hay una, y si construyes un modelo
sobre esa cuenta, creas tres grupos.

Y una advertencia sobre las muestras: perfilar 1.000 filas de 20 millones es rápido y suficiente
para ver tipos, nulos y distribuciones gruesas; no sirve para encontrar el caso raro que rompe el
proceso de carga, porque el 0,001 % de 1.000 filas no aparece. Para los centinelas y los formatos
raros hay que perfilar la columna entera o aceptar explícitamente que no los vas a ver.

## Definición formal

El **perfil de una columna** es una tupla de medidas calculadas sobre todas sus filas:

- **Tipo declarado y tipo inferido.** El primero lo dice el motor; el segundo, los datos.
- `n_filas`: el denominador de todo lo demás.
- `n_nulos` y `ratio_nulos = n_nulos / n_filas`.
- `n_distintos` (sin contar nulos) y **ratio de cardinalidad** `= n_distintos / n_filas`.
- `min` y `max` para números y fechas; longitud mínima, media y máxima para texto.
- **Top-k de valores** con su frecuencia absoluta y relativa.
- **Patrón dominante** para texto (por ejemplo, todos los valores encajan en `AAA-9999`).

Las reglas heurísticas que se aplican después, y que hay que leer como pistas y no como verdades:

- `n_distintos = 1` → columna constante. Si no es un filtro deliberado, sobra.
- `ratio = 1` y `n_nulos = 0` → candidata a clave primaria. Compruébalo, no lo asumas.
- `ratio < 0,05` → probable columna categórica, buen candidato a codificación por categorías.
- `ratio > 0,9` con texto → probable identificador, nombre propio o texto libre. Tratarla como
  categórica crea miles de columnas en un `one-hot`.
- `n_nulos > 0` → hay que decidir qué significa el hueco y qué se hace con él, caso por caso.

**El orden importa.** Primero el número de filas y el grano; después los tipos reales; después
nulos y cardinalidad; y solo al final distribuciones y valores extremos. Un perfil de una tabla
cuyo grano has entendido mal mide la columna equivocada con toda la precisión del mundo.

## Ejemplo

Seis filas de una tabla que parece inocente:

| pedido_id | país | ciudad | importe | alta |
| --- | --- | --- | --- | --- |
| 1 | ES | Madrid | 120,50 | 2024-01-05 |
| 2 | ES | Barcelona | 80,00 | 2024-01-05 |
| 3 | ES | madrid | 45,25 | 2024-01-06 |
| 4 | ES | Valencia | (nulo) | 2024-01-07 |
| 5 | ES | Barcelona | 999999,00 | 1900-01-01 |
| 6 | ES | « Sevilla» | 60,00 | 2024-01-08 |

El perfil devuelve:

| columna | nulos | distintos | ratio de cardinalidad |
| --- | --- | --- | --- |
| pedido_id | 0 | 6 | 1,00 |
| país | 0 | 1 | 0,17 |
| ciudad | 0 | 5 | 0,83 |
| importe | 1 | 5 | 0,83 |
| alta | 0 | 5 | 0,83 |

Lo que dicen esos cinco números:

- `pedido_id` tiene 6 valores distintos en 6 filas y ningún nulo: es la clave candidata.
- `pais` tiene un único valor: columna constante. No aporta nada hoy, y si mañana aparece `PT` es
  que algo ha cambiado en el origen.
- `ciudad` tiene 5 valores distintos, pero **son 4 de verdad**: `Madrid` y `madrid` son la misma,
  y ` Sevilla` lleva un espacio delante. Normalizar antes de contar no es cosmética: es la
  diferencia entre cuatro categorías y cinco.
- `importe` tiene 1 nulo y un máximo de 999999,00. Ese valor no es un importe: es la forma que
  tiene el sistema de origen de decir «no lo sé» o un error de captura. Un perfil lo saca a la
  luz; una media lo esconde.
- `alta` tiene forma de fecha, pero es texto, y una de las filas es `1900-01-01`, otro centinela.

## Código

```python verificable
# Perfil minimo: para cada columna, cuantos huecos hay y cuantos valores distintos.
crudo = {
    "pedido_id": [1, 2, 3, 4, 5, 6],
    "pais":      ["ES", "ES", "ES", "ES", "ES", "ES"],
    "ciudad":    ["Madrid", "Barcelona", "madrid", "Valencia", "Barcelona", " Sevilla"],
    "importe":   [120.5, 80.0, 45.25, None, 999999.0, 60.0],
    "alta":      ["2024-01-05", "2024-01-05", "2024-01-06",
                  "2024-01-07", "1900-01-01", "2024-01-08"],
}
filas = len(next(iter(crudo.values())))

print(f"{'columna':<10}{'nulos':>7}{'distintos':>11}{'cardinalidad':>14}")
for nombre, valores in crudo.items():
    nulos = sum(1 for v in valores if v is None)
    distintos = len({v for v in valores if v is not None})
    print(f"{nombre:<10}{nulos:>7}{distintos:>11}{distintos / filas:>14.2f}")

# La cardinalidad depende de haber normalizado antes: 5 valores son 4 categorias.
normalizadas = {c.strip().lower() for c in crudo["ciudad"]}
print("ciudad distintos sin normalizar", len(set(crudo["ciudad"])),
      " normalizando", len(normalizadas))
# -> ciudad distintos sin normalizar 5  normalizando 4
```

```text
columna     nulos  distintos  cardinalidad
pedido_id       0          6          1.00
pais            0          1          0.17
ciudad          0          5          0.83
importe         1          5          0.83
alta            0          5          0.83
```

```python verificable
# Buscar la clave candidata y los centinelas: las dos comprobaciones que evitan sorpresas.
columnas = {
    "pedido_id": [1, 2, 3, 4, 5, 6],
    "importe":   [120.5, 80.0, 45.25, None, 999999.0, 60.0],
    "alta":      ["2024-01-05", "2024-01-05", "2024-01-06",
                  "2024-01-07", "1900-01-01", "2024-01-08"],
}

# Candidata a clave: tantos valores distintos como filas y ningun hueco.
clave = [c for c, v in columnas.items() if len(set(v)) == len(v) and None not in v]
print("candidatas a clave:", clave)   # -> candidatas a clave: ['pedido_id']

# Un valor que se repite y no tiene sentido de negocio es un centinela disfrazado.
print("fecha 1900-01-01 repetida:", columnas["alta"].count("1900-01-01"))
# -> fecha 1900-01-01 repetida: 1

# Los huecos hay que quitarlos a mano: Python no compara None con un numero.
presentes = [v for v in columnas["importe"] if v is not None]
print("importe maximo:", max(presentes))   # -> importe maximo: 999999.0
```

## Errores típicos

- **Llamar perfilado a `describe()`.** Ese método solo mira columnas numéricas, ignora los nulos y
  no dice nada del texto ni de las fechas guardadas como cadena. El perfil tiene que cubrir todas
  las columnas y contar los huecos.
- **Perfilar sin normalizar.** `Madrid`, `madrid` y ` Sevilla` cuentan como tres valores. Antes de
  medir cardinalidad, recorta espacios, unifica mayúsculas y revisa acentos: si no, el informe
  pide crear categorías que no existen.
- **Confundir cardinalidad alta con buena calidad.** Un identificador único tiene un ratio de
  cardinalidad de 1; una provincia, con 52 valores en un millón de filas, tiene 0,000052. Ninguna
  de las dos es «mejor»: son tipos de columna distintos, y «cardinalidad 1» significa aquí
  *distintos = filas*, no *un solo valor* (eso era una columna constante). Y en un `one-hot`,
  tratar como categórica una columna de ratio 0,9 genera miles de columnas.
- **Perfilar una muestra diminuta y dar el resultado por bueno.** Con 500 filas no vas a ver el
  centinela que aparece una vez entre un millón. Los tipos y los nulos se ven con cualquier
  muestra; los casos raros, no.
- **Fiarse del nombre o del tipo declarado.** `fecha_alta` puede ser texto con formato
  `dd/mm/aaaa`, e `importe` puede ser una cadena con la coma decimal dentro. Comprueba el tipo
  real con `info()` o con el perfil, no con el nombre.
- **No guardar el perfil.** Sin línea base, una subida del 30 % en los nulos o un cambio en el
  top-5 de valores de una categórica pasan desapercibidos. Guarda el perfil y compáralo cada vez
  que cargues datos (ver [[monitorizacion-de-drift|deriva de datos y de concepto]]).

:::practica
enunciado: Una tabla de 6 filas tiene matricula = ["1234ABC","5678DEF","9012GHI","3456JKL","6789MNO","1234ABC"], kms = [12000, 45000, nulo, 90000, 999999, 3000] e itv = ["2024-05-01","2023-11-02","1900-01-01","1900-01-01","2024-03-03","2022-07-09"]. Calcula nulos, valores distintos y ratio de cardinalidad de cada columna, di si alguna es candidata a clave y qué valor huele a centinela.
pista: El ratio es valores distintos / filas, sin contar nulos; una candidata a clave tiene ratio 1 y ningún hueco.
solucion: matricula: 0 nulos, 5 distintos, 5/6 = 0,83, porque 1234ABC se repite. kms: 1 nulo, 5 distintos, 0,83. itv: 0 nulos, 5 distintos, 0,83. Ninguna llega a ratio 1, así que ninguna es candidata a clave. El 999999 de kms y el 1900-01-01 repetido dos veces en itv no son datos: son la forma que tiene el origen de decir «no lo sé», y se detectan contando valores repetidos y extremos.
:::

## Comprueba que lo sabes

:::quiz
p: En la tabla del ejemplo, la columna ciudad tiene 5 valores distintos. ¿Cuál es la cifra útil?
o: 5, porque son los valores que hay en la columna tal cual
o: 4, porque Madrid y madrid son la misma categoría y un valor lleva un espacio delante
o: 1, porque todas son ciudades y la columna es una sola
a: 2
e: La cardinalidad se mide sobre el valor normalizado. Sin recortar espacios ni unificar mayúsculas, el motor ve cinco valores y el negocio cuatro; construir un modelo sobre la cifra sin normalizar crea grupos duplicados. La opción 3 confunde el número de columnas con su cardinalidad.
:::

:::quiz
p: Una columna de importes tiene un máximo de 999999,00 y un 12 % de valores exactamente iguales a esa cifra. ¿Qué sospecha es razonable?
o: Que los clientes de ese segmento compran mucho
o: Que 999999 es un valor centinela con el que el sistema de origen indica «desconocido»
o: Que el máximo siempre es un error y hay que borrar la columna
a: 2
e: Un valor redondo y repetido hasta el 12 % no es una coincidencia de negocio: es la convención de un sistema para decir que no sabe. El perfil lo saca a la luz porque mide frecuencias y no solo medias. Descartar la columna entera por un valor extremo es la reacción contraria y también equivocada.
:::

:::truco
Antes de creerte un perfil, cuenta las filas. Si el resultado no cuadra con lo que esperabas
(10.000 en lugar de 100.000, o el doble), el problema no es de tipos ni de nulos: has leído dos
veces el fichero, has cruzado una tabla con un `JOIN` que multiplica filas o te falta un filtro.
Es la primera cifra que hay que mirar y la que más errores de interpretación evita.
:::
