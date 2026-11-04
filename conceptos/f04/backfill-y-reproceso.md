---
id: backfill-y-reproceso
titulo: Backfill y reproceso
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [idempotencia-y-reintentos, particionado-y-clustering, orquestacion-y-dag]
tags: [pipelines, historico, particiones, incidentes]
resumen: Rellenar las particiones que faltan y recalcular las que ya existen es rutina; el peligro es aplicar la lógica de hoy al pasado sin darse cuenta.
fuentes: ["Reis & Housley (2022), 'Fundamentals of Data Engineering'", "Kleppmann (2017), 'Designing Data-Intensive Applications'"]
---

## En una frase

El **backfill** rellena particiones que no existen (una tabla nueva, una columna nueva, tres días
de caída) y el **reproceso** vuelve a calcular particiones que ya existen porque la lógica o el
dato de origen han cambiado; los dos se ejecutan como el job normal, pero con fechas del pasado,
y ahí es donde rompen cosas.

## La idea

Un backfill no es un incidente: es una operación normal del ciclo de vida de un dato. Aparece
cuando estrenas una tabla y quieres darle dos años de historia, cuando añades una columna y hay
que rellenarla hacia atrás, o cuando el pipeline estuvo caído un fin de semana.

Un reproceso sí suele nacer de un problema: se descubre un bug, cambia la definición de una
métrica o el sistema de origen manda una corrección (un *restatement* de facturación, por
ejemplo). La lógica es la misma en los dos casos —volver a ejecutar la transformación sobre
fechas pasadas—, pero las consecuencias son distintas: el backfill **añade** donde no había
nada y el reproceso **cambia** cifras que alguien ya está mirando.

Lo que hace peligrosos a los dos son cuatro mecanismos concretos:

1. **La asunción de «ahora».** El job de producción puede permitirse leer `current_date`, «el
   último precio conocido» o «el atributo actual del cliente», porque cuando corre, el presente
   es la fecha de la partición. Un backfill de enero lanzado en julio mete el precio de julio en
   las ventas de enero y produce un histórico coherente y falso. La solución es parametrizar
   todo por la fecha de la partición y hacer los joins contra dimensiones versionadas
   ([[scd-dimensiones-cambiantes|SCD tipo 2]]) filtrando por intervalo de validez.
2. **Dos escritores sobre la misma partición.** Si el backfill toca la partición de ayer mientras
   el job diario también la escribe, el resultado depende de quién acabe último. La regla
   habitual: el backfill se limita al rango histórico y **excluye los últimos N días**, que son
   propiedad del job diario.
3. **Cascada de dependencias.** Reprocesar una tabla intermedia obliga a reprocesar todo lo que
   cuelga de ella. Si el bug estaba en `int_pedidos` y de ahí salen ocho tablas de consumo, el
   número de ejecuciones se multiplica por ocho —y el de horas, también.
4. **Pérdida de reproducibilidad.** Si no guardas la versión del código ni una copia de las
   fuentes del momento, dentro de seis meses no podrás volver a obtener el mismo número que
   publicaste. El reproceso da fe de que el pipeline es reproducible; si no lo es, el problema no
   es el reproceso.

:::trampa
El backfill perfecto es el que se puede lanzar dos veces y no cambia nada. Si tu script de
backfill hace `INSERT` en vez de reemplazar la partición, un fallo a mitad y un relanzamiento te
dejan la mitad de las fechas duplicadas. Antes de rellenar 700 días, asegúrate de que la tarea es
[[idempotencia-y-reintentos|idempotente]].
:::

## Definición formal

Sea `D` el conjunto de particiones (normalmente, una por día) de una tabla destino `T`, y sea
`T_p` el contenido que la transformación produce para la partición `p` a partir de tres cosas:

:::formula
T_p = F(p, c, s_p)
:::

Símbolos:

- `p` — la partición, identificada por su fecha (o su hora, o su región).
- `F` — la transformación, tal y como está escrita en el código.
- `c` — la versión del código con la que se ejecuta.
- `s_p` — el snapshot de las fuentes que corresponden a `p`. Para que `s_p` exista, el origen
  tiene que conservar el histórico o hay que guardar copias inmutables.

Con eso, las dos operaciones se definen así:

- **Backfill:** ejecutar `F` sobre `{ p ∈ D : T_p no existe }`. Sólo añade.
- **Reproceso:** ejecutar `F` sobre `{ p ∈ D : T_p existe y ha cambiado c o s_p }`, y
  **reemplazar** `T_p`. Añadir sin reemplazar deja el resultado viejo y el nuevo a la vez.

Dos invariantes que conviene poder comprobar después:

:::formula
filas(T) = filas(origen)   y   { p : T_p existe } es un rango de fechas contiguo
:::

El primero es la reconciliación. El segundo detecta huecos: es mucho más fácil ver que falta el
14 de marzo si esperas un rango contiguo que si revisas día a día.

## Ejemplo

Un bug en el cálculo del IVA se descubre el 12 de julio de 2024. Estuvo activo desde el 1 de
enero, así que todas las particiones calculadas en esa ventana están mal.

- Ventana afectada: del 1 de enero al 30 de junio de 2024. En un año bisiesto eso son
  **182 particiones**.
- Además, el pipeline estuvo caído del 1 al 3 de julio: **3 particiones** que no existen.
- Total de ejecuciones de la tabla base: 185.
- A 45 segundos por partición, en serie son 185 · 45 s = 8.325 s ≈ **2 h 19 min**. Con 8 workers
  en paralelo, la aritmética dice unos 17 minutos, pero comparten el mismo almacén y la misma
  cuota de lectura: en la práctica se parece más a 25 o 30 minutos. El paralelismo reparte el
  cómputo, no el ancho de banda.
- Y falta la tabla derivada `fact_ventas_diarias`, que depende de `int_pedidos`: otras 182
  particiones. Total real del incidente: **367 ejecuciones** repartidas en dos capas.

Ese número —367 y no 182— es el que hay que enseñar cuando alguien pregunta «¿cuánto tarda en
arreglarse?». El bug estaba en una capa; el daño estaba en dos.

## Código

```python verificable
from datetime import date, timedelta

# Un bug activo del 1 de enero al 30 de junio de 2024: lo ya calculado esta mal.
bug_desde, bug_hasta = date(2024, 1, 1), date(2024, 6, 30)
hoy = date(2024, 7, 12)

def rango(a, b):
    """Todas las fechas de a a b, ambas incluidas."""
    return {a + timedelta(days=i) for i in range((b - a).days + 1)}

# Particiones que no existen porque el pipeline estuvo caido del 1 al 3 de julio.
caidas = {date(2024, 7, d) for d in (1, 2, 3)}

reproceso = rango(bug_desde, bug_hasta)      # existen, pero estan mal: hay que reemplazarlas
backfill = {p for p in caidas if p <= hoy}   # no existen: hay que crearlas
particiones_totales = 185                    # dato del enunciado, no se deduce del conjunto
print(f"a reprocesar {len(reproceso)}")                            # -> a reprocesar 182
print(f"a rellenar  {len(backfill)}")                              # -> a rellenar  3
print(f"huecos tras el arreglo {len(reproceso | backfill) - particiones_totales}")  # -> 0

# Y la capa derivada obliga a repetir el trabajo entero otra vez.
print(f"ejecuciones totales {2 * len(reproceso) + len(backfill)}")  # -> 367
```

```sql verificable
-- Reproceso idempotente de UNA particion: se reconstruye entera y se reemplaza.
CREATE TABLE ventas AS
SELECT * FROM (VALUES
    (DATE '2024-01-01', 'P1', 100.0, 0.21),
    (DATE '2024-01-01', 'P2', 250.0, 0.10)
) AS t(fecha, pedido_id, base, iva);

-- Logica corregida: el IVA se calcula sobre la base de cada linea y se redondea a centimos
-- antes de agregar, que es como se factura.
CREATE OR REPLACE TABLE fact_ventas AS
SELECT fecha, sum(base) + sum(round(base * iva, 2)) AS total
FROM ventas WHERE fecha = DATE '2024-01-01' GROUP BY fecha;

-- El reproceso se relanza (o se lanza tres veces): el resultado no cambia.
CREATE OR REPLACE TABLE fact_ventas AS
SELECT fecha, sum(base) + sum(round(base * iva, 2)) AS total
FROM ventas WHERE fecha = DATE '2024-01-01' GROUP BY fecha;

SELECT * FROM fact_ventas;
```

```text
fecha | total
2024-01-01 | 396.00
```

## Errores típicos

- **Hacer el backfill con la dimensión de hoy.** Es el error número uno. Un `JOIN` con
  `dim_cliente` sin filtrar por fecha de validez mete el segmento actual del cliente en compras
  de hace dos años, y el histórico queda plausible pero incorrecto en todas las filas.
- **Reprocesar sin parar el job diario.** Dos escritores sobre la misma partición: el resultado
  depende del orden de llegada. Bloqueo por partición o ventana de mantenimiento, y una regla
  clara de quién es dueño de las últimas 48 horas.
- **Reprocesar sólo la tabla donde viste el bug.** Si el error está en una capa intermedia y no
  vuelves a calcular sus descendientes, las cifras publicadas siguen mal aunque la tabla
  intermedia ya esté bien.
- **Confundir reproceso con `full refresh`.** Borrar y recalcular tres años cuesta cien veces más
  que rehacer 182 particiones, y además destruye lo que estaba correcto. Si el destino tiene
  viaje en el tiempo ([[lakehouse-y-table-formats|formatos de tabla transaccionales]]), se puede
  comparar el antes y el después y volver atrás.
- **Reprocesar con `main` cambiando a la vez.** Si otro compañero despliega mientras corres el
  backfill, la mitad de las particiones salen con una versión del código y la otra mitad con
  otra. Etiqueta el commit, congela la rama y anota con qué versión se reprocesó.
- **No avisar de que las cifras cambian.** Un reproceso altera números que ya están en informes,
  extractos y modelos entrenados. Si no se comunica, el equipo de negocio descubre la diferencia
  por su cuenta y deja de fiarse de la tabla. Publica qué particiones han cambiado y en cuánto.

## Comprueba que lo sabes

:::quiz
p: ¿Qué diferencia hay entre un backfill y un reproceso?
o: El backfill rellena particiones que no existen y el reproceso vuelve a calcular particiones que ya existen porque algo ha cambiado
o: El backfill se hace en desarrollo y el reproceso en producción
o: Son sinónimos: los dos significan recalcular todo el histórico desde cero
a: 1
e: La diferencia está en si la partición existe. Rellenar un hueco no pisa nada; reprocesar sí cambia datos publicados, y por eso exige avisar y versionar. Ninguno de los dos implica recalcular todo: se trabaja sólo sobre el rango afectado, que es lo que lo hace viable.
:::

:::quiz
p: ¿Por qué un backfill de enero lanzado en julio puede producir un histórico incorrecto aunque el código sea el mismo del job diario?
o: Porque el código se ha degradado con el tiempo
o: Porque la tarea puede leer el estado actual del sistema (dimensión sin versionar, último precio, `current_date`) en lugar del estado que existía en enero
o: Porque los datos de enero ya no están en el origen
a: 2
e: El job diario funciona porque cuando corre, «ahora» coincide con su partición. Al ejecutarlo meses después, cualquier lectura del presente contamina el pasado. Se corrige parametrizando toda la lógica por la fecha de la partición y uniendo contra dimensiones con intervalo de validez.
:::

:::aviso
Un reproceso en cascada consume la cuota del almacén y puede competir con el job diario, que es
el que mantiene el negocio en marcha. Lánzalo con concurrencia limitada, fuera de la ventana
crítica y con un tope de coste. Si el reproceso tumba la producción, el incidente pasa a ser
peor que el bug.
:::
