---
id: correccion-point-in-time
titulo: Corrección point-in-time
fase: 4
nivel: avanzado
rutas: [de, quant]
prerequisitos: [sesgo-de-mirar-al-futuro, scd-dimensiones-cambiantes, datos-de-mercado-y-acciones-corporativas]
tags: [point-in-time, linaje, backtest]
resumen: Guardar cada dato con la fecha en que estuvo disponible y no con la del evento, la disciplina que separa un pipeline honesto de un backtest inflado.
fuentes: ["López de Prado (2018), 'Advances in Financial Machine Learning', cap. 4", "Kimball y Ross (2013), 'The Data Warehouse Toolkit'"]
---

## En una frase

Cada fila lleva dos fechas —cuándo ocurrió el hecho y cuándo se pudo saber— y toda consulta
histórica filtra por la segunda.

## La idea

Un resultado trimestral cierra el 31 de marzo y se publica el 24 de abril. Una revisión al alza
sale el 12 de junio. Tres fechas para un solo dato, y la mayoría de los almacenes guarda una.

Si tu tabla tiene solo la fecha de cierre, cualquiera que pregunte «qué se sabía el 15 de mayo»
obtendrá la cifra definitiva, que en ese momento no existía. No es un error de consulta: es un
error del modelo de datos, y es el mismo que el sesgo de mirar al futuro, pero a nivel de almacén.
El backtest sale mejor de lo que debería, el informe de riesgo enseña una foto que nadie tuvo, y
nadie sospecha porque los números cuadran.

La solución es incómoda y por eso se salta: guardar dos marcas de tiempo por fila y no sobrescribir
nunca. Cuando llega una corrección, se cierra la versión anterior y se abre una nueva. La tabla
crece, las consultas se complican un poco, y a cambio cada pregunta histórica tiene una respuesta
correcta.

:::trampa
Un `UPDATE` que corrige un importe a posteriori destruye el histórico para siempre. Si no tienes
una copia, ya no puedes reconstruir qué se sabía antes de la corrección. La disciplina de no
sobrescribir es más importante que cualquier índice.
:::

## Definición formal

Una tabla point-in-time tiene, como mínimo, dos atributos temporales por fila:

:::formula
valid_from  ≤  as_of        (el hecho existe antes de que se pueda conocer)
:::

:::formula
vigente(t, e) = la fila con mayor as_of tal que as_of ≤ t y valid_from ≤ e
:::

- `valid_from` — cuándo ocurrió el hecho: el cierre del trimestre, la fecha de la venta.
- `as_of` — cuándo estuvo disponible ese valor: la publicación, la carga en el almacén.
- `t` — el instante de la consulta: «qué se sabía el 15 de mayo».
- `e` — el instante del hecho: «el trimestre cerrado el 31 de marzo».

Cuando `as_of` y `valid_from` van en la misma columna, el modelo no distingue entre «lo que pasó»
y «lo que se supo», y toda consulta histórica miente por defecto.

**Dos formas de implementarlo.** La primera es una tabla bitemporal con `valid_from`, `valid_to`,
`as_of` y un cierre por versión. La segunda, más barata, es un `raw` inmutable con la fecha de
carga en la ruta (`raw/fecha_carga=2025-06-12/...`) y una vista que, para cada clave, se queda con
la última carga anterior al instante consultado. La primera es más consultable; la segunda es más
difícil de romper.

## Ejemplo

Una tabla de ingresos con dos versiones del mismo trimestre:

| cuenta | cierre | publicado | ingresos |
| --- | --- | --- | --- |
| A | 2025-03-31 | 2025-04-24 | 100,0 |
| A | 2025-03-31 | 2025-06-12 | 103,0 |
| B | 2025-03-31 | 2025-04-28 | 50,0 |

Consultando con `as_of ≤ 2025-05-15`, la cuenta A vale 100,0: la revisión de junio todavía no
existía. Con `as_of ≤ 2025-07-15`, vale 103,0. Y la cuenta B, que publicó el 28 de abril, ya
aparece en la primera consulta.

Sin la columna `publicado`, las dos consultas devolverían 103,0 y el informe de mayo habría usado
un dato de junio. Nadie lo notaría, porque 103 es un número razonable.

## Código

```python verificable
import pandas as pd

filas = [
    {"cuenta": "A", "cierre": "2025-03-31", "publicado": "2025-04-24", "ingresos": 100.0},
    {"cuenta": "A", "cierre": "2025-03-31", "publicado": "2025-06-12", "ingresos": 103.0},
    {"cuenta": "B", "cierre": "2025-03-31", "publicado": "2025-04-28", "ingresos": 50.0},
]
df = pd.DataFrame(filas)

def vigente(cuenta, fecha):
    v = df[(df["cuenta"] == cuenta) & (df["publicado"] <= fecha)]
    if v.empty:
        return float("nan")
    return float(v.sort_values("publicado").iloc[-1]["ingresos"])

print(f"A el 2025-05-15 {vigente('A', '2025-05-15'):.1f}")   # -> A el 2025-05-15 100.0
print(f"A el 2025-07-15 {vigente('A', '2025-07-15'):.1f}")   # -> A el 2025-07-15 103.0
print(f"B el 2025-04-10 {vigente('B', '2025-04-10')}")        # -> B el 2025-04-10 nan
print(f"B el 2025-05-15 {vigente('B', '2025-05-15'):.1f}")   # -> B el 2025-05-15 50.0
```

La tercera línea es tan importante como las otras: antes de la publicación, la cuenta B **no
tiene valor**, y devolver un cero sería peor que devolver un nulo. Un cero es una cifra; un nulo
es una pregunta abierta.

:::claves
- `df["publicado"] <= fecha` compara cadenas en formato ISO, que es el único formato de fecha en
  el que el orden alfabético es el orden cronológico. Con `24/04/2025` esta comparación miente.
- `sort_values("publicado").iloc[-1]` se queda con la versión más reciente **anterior** al corte,
  que es la definición de vigente. Un `groupby().last()` sin ordenar devuelve la última fila del
  fichero, que no tiene por qué ser la última publicada.
- `v.empty` protege el caso de consulta anterior a cualquier publicación. Sin esa guarda, `iloc`
  lanza un error y el pipeline se cae por un dato que legítimamente no existía.
- `float("nan")` es un nulo, no un cero. La diferencia importa en todos los promedios que se
  calculen después: un cero entra en la media, un nulo se puede excluir.
- Comparar fechas como texto funciona aquí porque están en ISO; con tipos `datetime` sería más
  robusto, pero entonces la comparación con una cadena falla en silencio en algunas versiones.
:::

## Errores típicos

- **Guardar solo la fecha del evento.** Es el error de origen: el almacén ya no puede responder
  «qué se sabía entonces» y ninguna capa posterior lo arregla.
- **Corregir con `UPDATE`.** Reescribe el pasado y elimina la prueba de que hubo una corrección.
  En un almacén serio, la corrección es una fila nueva con su `as_of`.
- **Filtrar por `valid_from` creyendo que es lo mismo.** Filtra por `as_of`. `valid_from` dice
  cuándo pasó; la pregunta histórica es cuándo se supo.
- **Olvidar que los datos macroeconómicos se revisan.** El PIB se publica tres veces y cambia. Un
  modelo que usa la cifra definitiva está usando información del futuro.
- **Rellenar con cero los datos que faltan.** Un cero es un valor y pasa los controles de tipo. Un
  nulo es la verdad: todavía no hay dato.
- **No probar el caso del hueco.** Si no hay una prueba con una fecha entre el cierre y la
  publicación, el filtro puede estar invertido y todo sigue en verde.

:::practica
enunciado: Una tabla de ventas guarda solo `fecha_venta`. Un informe de marzo se generó el 5 de abril y otro el 20 de abril, y el segundo muestra un 8 % más porque el sistema de origen cargó pedidos atrasados. ¿Qué dos columnas faltaban y qué consulta habría dado la cifra honesta para el informe del 5 de abril?
pista: La respuesta no es «filtrar por marzo»: es «filtrar por lo que se sabía el 5 de abril».
solucion: Faltaban `valid_from` (fecha del hecho, la venta) y `as_of` (fecha de disponibilidad, la carga). La consulta honesta filtra `as_of <= '2025-04-05'` y agrupa por `valid_from` dentro de marzo. El informe del 20 de abril no es una corrección del anterior: es otra foto, y las dos deben poder reproducirse.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué dos fechas necesita una fila para ser honesta en un almacén histórico?
o: La del hecho y la de su disponibilidad
o: La de creación y la de modificación del registro
o: La del evento y la del cierre contable
a: 1
e: La fecha del hecho dice cuándo ocurrió; la de disponibilidad, cuándo se pudo conocer. Las de creación y modificación del registro son de auditoría técnica y suelen ser posteriores a la publicación, así que no sirven para responder qué se sabía.
:::

:::quiz
p: Consultas el 15 de mayo un dato publicado el 24 de abril y revisado el 12 de junio. ¿Qué valor debe devolver una tabla point-in-time?
o: El de la publicación de abril, porque la revisión de junio aún no existía
o: El revisado de junio, porque es el valor correcto
o: La media de los dos, para no sesgar
a: 1
e: La pregunta es «qué se sabía el 15 de mayo», y ese día solo existía la cifra de abril. Devolver la revisada es usar información del futuro; promediar es inventar un dato que nunca existió.
:::
