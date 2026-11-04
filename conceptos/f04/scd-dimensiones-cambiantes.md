---
id: scd-dimensiones-cambiantes
titulo: Dimensiones que cambian (SCD)
fase: 4
nivel: avanzado
rutas: [de, ds]
prerequisitos: [hechos-y-dimensiones, modelado-dimensional, sql-joins]
tags: [modelado, historico, dimensiones, bi]
resumen: Como guardar la historia de un atributo que cambia sin reescribir el pasado: tipos 1, 2, 3 y 6, claves sustitutivas y fechas de validez.
fuentes: ["Kimball y Ross (2013), 'The Data Warehouse Toolkit'", "Inmon (2005), 'Building the Data Warehouse'"]
---

## En una frase

Una **dimensión que cambia** (SCD, del inglés *slowly changing dimensión*) es una tabla de
[[hechos-y-dimensiones|dimensión]] cuyo atributo varía con el tiempo, y la decisión de qué
hacer con el valor antiguo determina si tus informes históricos seguirán contando la verdad
dentro de dos años.

## La idea

Un comercial vende en la región Sur durante 2021 y en 2023 le cambian la cartera a la región
Norte. En marzo de 2023 el jefe de ventas pide dos cosas a la vez:

1. «¿Cuánto vendió la región Sur en 2021?» — y el nombre del comercial debe aparecer en Sur.
2. «¿Cuánto está vendiendo hoy la región Norte?» — y el mismo comercial debe aparecer en Norte.

Si al cambiarle la región has **pisado** el valor anterior, la primera pregunta ya no tiene
respuesta: los datos de 2021 dicen que vendió en Norte, y la región Sur pierde 400.000 euros
de historia. Si en cambio **añades una fila nueva** y marcas hasta cuándo valía la anterior,
las dos preguntas se responden con la misma tabla. Eso es todo el concepto: el pasado deja de
ser un residuo y se convierte en un dato más.

Piensa en la ficha académica de un alumno. Cada curso se abre una matrícula nueva; no se
tacha la del año pasado. Si tacharas, no podrías expedir un certificado de las asignaturas de
2021. La diferencia con la ficha de papel es que aquí el volumen obliga a decidirlo por
atributo, no por tabla: la fecha de nacimiento no cambia nunca, el teléfono cambia a menudo y
la dirección cambia a veces.

Kimball puso nombre a las estrategias con números, y en las entrevistas de trabajo se usan
como taquigrafía:

- **Tipo 0 — retener el original.** El atributo no se actualiza jamás (fecha de nacimiento, o
  el primer código de cliente asignado). Sirve para auditar, no para informar.
- **Tipo 1 — sobrescribir.** Se pisa el valor. No hay historia: es la opción correcta para
  corregir un error (un nombre mal escrito), y la equivocada para un cambio real.
- **Tipo 2 — nueva fila.** La versión anterior se cierra con fecha de fin y se abre una nueva
  fila. Es el patrón estándar de la analítica y el único que permite informar de cualquier
  pasado.
- **Tipo 3 — columna de valor anterior.** Se añade `region_anterior` junto a `region_actual`.
  Guarda un solo salto: un tercer cambio pierde el primero para siempre.
- **Tipo 6 — híbrido (1 + 2 + 3).** Fila nueva tipo 2 y, además, dos columnas: el valor actual
  replicado en todas las versiones y el valor original. Permite agrupar «como está hoy» y
  «como estaba entonces» sin cambiar la consulta.
- **Tipo 4 — histórico en tabla aparte.** La dimensión actual se queda pequeña y rápida y el
  historial vive en otra tabla. Útil con atributos enormes que cambian mucho.

El precio del tipo 2 es que la dimensión crece y que **los hechos tienen que apuntar a la
versión correcta**, no al cliente. Ese detalle, que parece menor, es el que rompe la mitad de
los cuadros de mando que he visto.

## Definición formal

Sea `D` una dimensión con:

- `nk` — **clave natural**: el identificador del negocio (el código de cliente del CRM). Único
  por entidad, pero **no** único por fila cuando hay historial.
- `sk` — **clave sustitutiva** (*surrogate key*): un entero sin significado, generado por el
  almacén, único por **fila**. Es lo que guardan los hechos.
- `a₁ … aₘ` — los atributos versionados (ciudad, región, segmento).
- `inicio`, `fin` — el intervalo de validez de cada versión.
- `actual` — indicador booleano de la versión vigente; opcional si se calcula con `fin`.

Con el convenio de intervalo semiabierto:

:::formula
versión v vigente en t ⟺ inicio(v) ≤ t < fin(v)
:::

y las tres invariantes que un SCD tipo 2 debe cumplir siempre:

1. **Una sola versión vigente por `nk`:** `count(*) where actual = true` agrupado por `nk`
   vale exactamente 1.
2. **Sin huecos ni solapes:** al cerrar una versión, `fin` de la vieja es exactamente `inicio`
   de la nueva. Usar `BETWEEN` con un extremo inclusivo hace que el día del cambio aparezca en
   las dos versiones y duplique las ventas de ese día.
3. **La `sk` no se reutiliza jamás.** Si reciclas claves, el histórico se cruza: la venta de
   2021 apuntará a una versión que describe 2024.

En el momento de la carga, la actualización es: para cada `nk` del origen, comparar el valor
de los atributos versionados con la versión vigente; si **ningún** atributo cambió, no hay
fila nueva (esto es lo que evita que la dimensión crezca sin sentido); si cambió alguno, cerrar
la vigente en la fecha del cambio y abrir una nueva.

## Ejemplo

Cliente 4471, que cambia de ciudad dos veces. Después de dos cargas, la dimensión queda así:

| sk | nk | ciudad | inicio | fin | actual |
| --- | --- | --- | --- | --- | --- |
| 9001 | 4471 | Madrid | 2019-01-01 | 2022-03-15 | no |
| 9002 | 4471 | Barcelona | 2022-03-15 | 2024-07-01 | no |
| 9003 | 4471 | Valencia | 2024-07-01 | 9999-12-31 | sí |
| 9004 | 8890 | Sevilla | 2021-06-01 | 9999-12-31 | sí |

Tres filas para un solo cliente: el precio de conservar la historia. La fecha centinela
`9999-12-31` marca «sin fin conocido» para no tener que usar nulos en las comparaciones.

Ahora una venta del 2 de mayo de 2023 que guardó `sk_cliente = 9002`:

- Informe histórico (agrupa por la versión del hecho): la venta cae en **Barcelona**. Correcto:
  en mayo de 2023 el cliente estaba en Barcelona.
- Si en vez de la `sk` el hecho hubiera guardado el `nk` 4471 y se uniera por él, la venta se
  multiplicaría por las 3 versiones: 3 filas y un total triplicado. Ese es el **abanico**
  (*fan-out*) clásico de las dimensiones tipo 2.

Un cliente que no cambió nada —el 8890— tiene una sola fila y ninguna versión extra: la carga
solo abre versión cuando hay cambio real.

## Código

```python verificable
import pandas as pd

CORTE = pd.Timestamp("2025-01-01")     # fecha del cambio que llega del sistema origen
FIN = pd.Timestamp("9999-12-31")       # centinela: version abierta

# Dimension tipo 2: una fila por version, sk unica por fila y nk repetida
dim = pd.DataFrame({
    "sk": [9001, 9002, 9003],
    "nk": [4471, 4471, 8890],
    "ciudad": ["Madrid", "Barcelona", "Sevilla"],
    "inicio": pd.to_datetime(["2019-01-01", "2022-03-15", "2021-06-01"]),
    "fin": pd.to_datetime(["2022-03-15", "9999-12-31", "9999-12-31"]),
    "actual": [False, True, True],
})
origen = pd.DataFrame({"nk": [4471, 8890], "ciudad": ["Valencia", "Sevilla"]})

nuevas, cierres = [], []
for _, o in origen.iterrows():
    vigente = dim[(dim.nk == o.nk) & dim.actual].iloc[0]
    if vigente.ciudad == o.ciudad:      # sin cambio real: no se abre version nueva
        continue
    cierres.append(vigente.sk)
    nuevas.append({"sk": 9000 + len(dim) + len(nuevas) + 1, "nk": o.nk,
                   "ciudad": o.ciudad, "inicio": CORTE, "fin": FIN, "actual": True})

for sk in cierres:                      # la version sustituida se cierra, no se borra
    dim.loc[dim.sk == sk, "fin"] = CORTE
    dim.loc[dim.sk == sk, "actual"] = False
dim = pd.concat([dim, pd.DataFrame(nuevas)], ignore_index=True)

print("filas totales:", len(dim))                                     # -> filas totales: 4
print("versiones del cliente 4471:", int((dim.nk == 4471).sum()))     # -> versiones del cliente 4471: 3
print("ciudad vigente hoy:", dim.loc[(dim.nk == 4471) & dim.actual, "ciudad"].item())  # -> ciudad vigente hoy: Valencia
print("fin de la version 9002:", str(dim.loc[dim.sk == 9002, "fin"].item().date()))    # -> fin de la version 9002: 2025-01-01
```

```sql verificable
-- Con la clave sustitutiva en los hechos, cada venta cae en su version historica
CREATE TABLE dim_cliente AS
SELECT * FROM (VALUES
    (9001, 4471, 'Madrid',    DATE '2019-01-01', DATE '2022-03-15', FALSE),
    (9002, 4471, 'Barcelona', DATE '2022-03-15', DATE '2024-07-01', FALSE),
    (9003, 4471, 'Valencia',  DATE '2024-07-01', DATE '9999-12-31', TRUE)
) AS t(sk, nk, ciudad, inicio, fin, actual);

CREATE TABLE hechos_ventas AS
SELECT * FROM (VALUES
    (DATE '2023-05-02', 9002, 120.50),
    (DATE '2025-02-10', 9003,  80.00)
) AS t(fecha, sk_cliente, importe);

-- Informe historico: Barcelona 120.50 y Valencia 80.00, dos filas y ningun doble conteo
SELECT d.ciudad, count(*) AS ventas, sum(f.importe) AS total
FROM hechos_ventas f
JOIN dim_cliente d ON d.sk = f.sk_cliente
GROUP BY d.ciudad
ORDER BY d.ciudad;
```

## Errores típicos

- **Sobrescribir un atributo que cambia de verdad (tipo 1) y luego pedir historia.** El informe
  de 2021 se recalcula con el valor de 2024 y nadie lo nota hasta que el negocio cuadra
  cifras. Regla: sobrescribe solo para corregir errores, nunca para reflejar cambios.
- **Guardar el `nk` en los hechos.** Al unir por clave natural, cada hecho se multiplica por
  todas las versiones del cliente. Los totales se inflan y el error es silencioso porque el
  número sigue siendo «plausible». Los hechos guardan la `sk` vigente en el momento del evento.
- **Cerrar con `BETWEEN` en lugar de intervalo semiabierto.** Si la versión vieja termina el
  15 de marzo y la nueva empieza el 15 de marzo, un `BETWEEN` inclusivo cuenta ese día dos
  veces. Usa `inicio <= t and t < fin`.
- **No comprobar el cambio antes de insertar.** Si abres una versión en cada carga aunque nada
  haya cambiado, una dimensión de 200.000 clientes con carga diaria acaba con millones de
  filas idénticas y los informes se vuelven lentos sin ganar ni un dato.
- **Reutilizar la clave sustitutiva.** Compactar `sk` para «ahorrar» espacio rompe la relación
  con los hechos históricos: la venta apuntará a la versión equivocada para siempre.
- **Usar el estado actual para informar del pasado.** «Ventas por ciudad de los clientes
  actuales» mezcla el estado de hoy con hechos de hace tres años, y reprocesar el año pasado con
  la dimensión de hoy reescribe la foto histórica. Si haces esa pregunta, dilo; el reproceso debe
  usar la versión que era vigente entonces.

## Comprueba que lo sabes

:::quiz
p: Un cliente cambia de ciudad el 15 de marzo. En un SCD tipo 2, ¿qué dos cosas ocurren ese día en la dimensión?
o: Se actualiza la ciudad en la fila existente y se guarda la anterior en una columna
o: Se cierra la versión vigente con fin igual al 15 de marzo y se abre una fila nueva con inicio ese día
o: Se borra la fila antigua y se inserta una nueva con la misma clave sustitutiva
a: 2
e: El tipo 2 conserva las dos versiones: cierra la anterior (fin = 15 de marzo) y abre otra con inicio ese mismo día, de modo que el intervalo semiabierto no duplica ni pierde el día del cambio. La primera opción describe el tipo 3 y la tercera destruye la historia y reutiliza la clave.
:::

:::quiz
p: ¿Por qué los hechos guardan la clave sustitutiva y no la clave natural del cliente?
o: Porque la clave sustitutiva ocupa menos bytes y acelera las uniones
o: Porque la clave natural se repite en varias filas de la dimensión y la unión multiplicaría cada hecho
o: Porque la clave natural cambia cuando el cliente cambia de ciudad
a: 2
e: Con historial tipo 2, un mismo cliente tiene varias filas. Unir por la clave natural devuelve todas las versiones y cada hecho se cuenta tantas veces como versiones exista. La sk identifica una versión concreta. Que sea un entero pequeño es una ventaja secundaria, no la razón.
:::

:::quiz
p: Llega una carga en la que ningún atributo versionado ha cambiado. ¿Qué debe hacer un proceso SCD tipo 2?
o: Insertar una versión nueva y cerrar la anterior, para dejar constancia de la carga
o: No tocar la dimensión: sin cambio no hay versión nueva
o: Actualizar la fecha de fin de la versión vigente a la fecha de la carga
a: 2
e: El historial se abre solo cuando cambia algo; lo contrario multiplica filas idénticas y degrada los informes sin aportar información. La fecha de la carga no es un atributo del negocio y no debe cerrar nada.
:::

:::trampa
Antes de cambiar una dimensión a tipo 2, revisa todas las consultas que la unen por clave
natural. Un `JOIN` por `nk` que hoy devuelve una fila pasará a devolver varias y duplicará los
importes de los informes que ya estaban validados.
:::
