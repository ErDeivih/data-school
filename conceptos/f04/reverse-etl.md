---
id: reverse-etl
titulo: Reverse ETL
fase: 4
nivel: intermedio
rutas: [de]
prerequisitos: [data-warehouse, contratos-de-datos, idempotencia-y-reintentos]
tags: [reverse-etl, crm, sincronizacion, pii]
resumen: Devolver al CRM, al soporte y a los anuncios lo que el almacén ya sabe del cliente: escritura por clave, campos con un solo dueño y respeto a los límites de la API.
fuentes: ["Reis & Housley (2022), 'Fundamentals of Data Engineering'", "Kimball & Ross (2013), 'The Data Warehouse Toolkit'"]
---

## En una frase

El reverse ETL cierra el círculo: coge lo que el almacén ya sabe del cliente y lo escribe en las
herramientas donde trabaja el negocio —CRM, soporte, publicidad— sin que nadie suba un fichero a
mano.

## La idea

Imagina que el almacén es la cabeza de la empresa y que el CRM, el sistema de soporte y el gestor de
anuncios son las manos. Todo el conocimiento está en la cabeza y las manos no lo ven: el comercial
llama a un cliente que lleva tres meses sin comprar porque no sabe que está a punto de irse, soporte
no ve que ese pedido va con retraso, y la publicidad sigue pujando por alguien que ya compró.

Durante años el puente entre las dos partes fue un fichero: el analista exporta un CSV, alguien lo
sube a mano, se equivoca de columna, la mitad de los contactos se duplican y nadie sabe qué se
envió ni cuándo. El reverse ETL automatiza ese puente con tres piezas: una consulta al almacén, un
mapeo de columnas a campos de la herramienta y una escritura por API.

Suena sencillo y tiene cuatro dificultades reales:

1. **Identidad.** El almacén guarda `email`; el CRM guarda `contact_id`. Hace falta una tabla que
   relacione las dos cosas, y la clave tiene que ser **estable**: el correo cambia, admite
   mayúsculas y dos personas pueden compartirlo. Un identificador propio no.
2. **Propiedad del campo.** Cada campo tiene un dueño. Si el comercial edita `teléfono` en el CRM,
   el almacén no puede reescribirlo cada noche con el valor viejo de hace un año. Solo se
   sincronizan los campos cuyo dueño es el almacén; los demás se leen y no se tocan.
3. **Idempotencia y límites.** Las APIs fallan, el proceso se reintenta y, si la escritura no es
   idempotente, duplica contactos. Además las APIs imponen un número máximo de llamadas por segundo
   y por día ([[idempotencia-y-reintentos]]).
4. **El bucle.** Si escribes un campo en el CRM, ese campo vuelve al almacén en la siguiente ingesta
   y alimenta el cálculo que decide el próximo valor, el campo oscila entre dos valores y nadie
   entiende por qué. La regla que lo evita: cada campo tiene **un solo escritor**.

:::aviso
Escribir en la herramienta de negocio no es solo escribir en una base de datos. Un cambio de campo
puede disparar una regla automática: un correo al cliente, una tarea para el comercial, una
puntuación recalculada. Una carga completa nocturna que reescribe 480.000 contactos puede lanzar
480.000 automatizaciones. Antes de sincronizar, revisa qué reglas hay activadas en el destino.
:::

## Definición formal

Una sincronización es una función de las filas del almacén a operaciones sobre objetos de la
herramienta de destino:

:::formula
S : W → T      S(fila) = upsert( k(fila), campos_que_posee_el_almacen )
:::

Y cuánto tarda depende del lote y del límite de la API:

:::formula
duración = ⌈ N / L ⌉ / R
:::

Símbolos:

- `W` — el conjunto de filas del almacén que se van a sincronizar.
- `T` — los objetos del destino: contactos, cuentas, tickets, audiencias.
- `k` — la clave de identidad que relaciona una fila con un objeto. Es la pieza que decide si hay
  duplicados o no.
- `upsert` — escribir de forma que si el objeto no existe se cree y si existe se actualice. Es lo
  que hace que reintentar no duplique.
- `campos_que_posee_el_almacen` — el subconjunto de campos del destino que el almacén tiene derecho
  a sobrescribir. El resto son del negocio.
- `N` — filas distintas que hay que escribir en esta ejecución.
- `L` — registros que acepta la API en una sola llamada, el tamaño del lote.
- `R` — llamadas por segundo que permite la API del destino.
- `⌈ ⌉` — redondeo hacia arriba: la última llamada va medio vacía, pero se paga entera.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `N` | Filas que hay que escribir en esta ejecución | registros | La duración crece en línea recta; filtrar por fecha de cambio es lo que mantiene `N` pequeño |
| `L` | Registros por llamada | registros/llamada | Menos llamadas y menos tiempo; el límite lo pone la API, que rechaza lotes grandes |
| `R` | Llamadas por segundo permitidas | llamadas/s | La duración baja en proporción inversa; si te pasas, la API responde con error y hay que reintentar |
| `k` | Clave de identidad usada en el upsert | identificador | Si no es estable ni única, aparecen duplicados: dos objetos para el mismo cliente |
| `campos` | Campos que el almacén puede sobrescribir | recuento | Más campos son más riesgo de pisar lo que edita el negocio, y más automatizaciones disparadas |
:::

:::figura
fichero: reverse-etl-lote-y-cambio
pie: A la izquierda, la duración de la sincronización frente a los registros que hay que escribir, con dos tamaños de lote y el mismo límite de cinco llamadas por segundo. Las dos verticales marcan los escenarios del ejemplo: 3.200 registros cambiados en un día y 480.000 en una carga completa. Separar las dos curvas cuesta multiplicar el lote por cinco; separar los dos puntos es cuestión del filtro, y son 150 veces. A la derecha, las llamadas que necesita cada estrategia: el ahorro viene de no enviar lo que no ha cambiado, no de apretar el tamaño del lote.
fuente: figuras/reverse-etl-1.py
:::

## Ejemplo

Un almacén con **480.000 contactos** en el CRM, de los cuales cada día cambian **3.200** (alta,
baja, segmento nuevo). Lotes de `L = 200` registros y un límite de `R = 5` llamadas por segundo.

| Estrategia | Llamadas | Duración |
| --- | --- | --- |
| Carga completa | ⌈480.000 / 200⌉ = 2.400 | 2.400 / 5 = 480 s, 8 minutos |
| Solo lo que cambió | ⌈3.200 / 200⌉ = 16 | 16 / 5 = 3,2 segundos |

La diferencia no viene del tamaño del lote, viene del filtro: multiplicar el lote por cinco (de 200
a 1.000) baja la carga completa de 2.400 llamadas a 480, es decir de 480 segundos a 96, mientras
que filtrar por fecha la deja en 3,2. Y hay
un límite diario que conviene mirar antes de celebrar: si la API acepta 100.000 llamadas al día, las
2.400 de la carga completa caben de sobra y el problema no es el cupo, son las 480.000 escrituras
que disparan automatizaciones en el CRM.

El detalle que se aprende a golpes: la ejecución que se corta a mitad y se reintenta. Con `upsert`
por `crm_id`, reintentar es inofensivo; con un `insert` a secas, el reintento duplica los contactos
que ya se habían escrito y alguien tiene que limpiarlos a mano.

## Código

```python verificable
import math

contactos = 480_000          # objetos en el destino
cambiados_dia = 3_200        # los que de verdad cambiaron hoy
lote = 200                   # registros por llamada
ritmo = 5                    # llamadas por segundo que permite la API

def sincronizar(filas, lote, ritmo):
    """Devuelve (llamadas, segundos) para escribir esas filas."""
    llamadas = math.ceil(filas / lote)
    return llamadas, llamadas / ritmo

for nombre, filas in (("carga completa", contactos), ("solo cambiados", cambiados_dia)):
    llamadas, segundos = sincronizar(filas, lote, ritmo)
    print(f"{nombre:>15}: {llamadas:5d} llamadas, {segundos:8.1f} s")
# ->  carga completa:  2400 llamadas,    480.0 s
# ->  solo cambiados:    16 llamadas,      3.2 s
print("factor:", contactos // cambiados_dia)   # -> 150
```

:::claves
- `math.ceil` redondea hacia arriba y devuelve un **entero**, no un decimal: `math.ceil(3200/200)` es
  `16`. La última llamada puede ir casi vacía, pero cuenta igual.
- Si dividieras con `//` (división entera) casi siempre saldría lo mismo, pero con un solo registro
  pendiente daría 0 llamadas: el registro no se enviaría nunca. Para contar lotes se usa `ceil`.
- `480_000` y `3_200` llevan guion bajo como separador de millares; Python los lee igual que
  `480000`. No cambian el valor, solo la lectura.
- `sincronizar` devuelve una **tupla** de dos valores. Se puede desempaquetar en dos variables
  (`llamadas, segundos = ...`) porque el orden es el de la tupla, no el de los nombres que uses.
- `{nombre:>15}` alinea a la derecha en 15 caracteres y `{segundos:8.1f}` en 8 con un decimal: son
  formatos de salida. Ojo, que `f"{x}"` no redondea el valor guardado, solo lo que se imprime.
- `contactos // cambiados_dia` es división entera: 150 exacto. Con `480_001` daría 150 también, y ahí
  está la trampa: el factor sirve para comunicar, no para calcular.
:::

```sql ilustrativo
-- Lo que se sincroniza: solo lo que cambio desde la ultima marca de agua.
SELECT c.crm_id, c.email, s.segmento, s.riesgo_baja
FROM oro.dim_cliente AS c
JOIN oro.cliente_puntuacion AS s ON s.cliente_id = c.cliente_id
WHERE s.actualizado_en > (
    SELECT max(sincronizado_hasta) FROM control.sincronizaciones WHERE destino = 'crm'
);
```

## Errores típicos

- **Usar el correo como clave de identidad.** Es la causa número uno de contactos duplicados: el
  correo se escribe con otra caja, cambia cuando alguien se va de la empresa y a veces lo comparten
  dos personas. La clave tiene que ser un identificador estable que exista en los dos lados.
- **Sobrescribir campos que edita el negocio.** El comercial cambia el teléfono por la mañana y tu
  sincronización lo revierte por la noche. Empieza por escribir en la herramienta una tabla de
  propiedad de campos y sincroniza solo los que son tuyos.
- **Hacer la carga completa cada noche.** Además del tiempo y del cupo de la API, reescribir todo
  dispara las reglas automáticas del destino. Filtra por fecha de modificación y sube solo lo que
  cambió ([[ingesta-incremental-y-cdc]]).
- **Ignorar los automatismos de la herramienta.** Un `update` no es inocuo: puede enviar un correo,
  crear una tarea o cambiar una puntuación. Prueba la sincronización en una cuenta de prueba con las
  automatizaciones activadas antes de tocar producción.
- **Mandar datos personales a un tercero sin base ni límite.** Copiar el correo y el teléfono a una
  plataforma de publicidad es una cesión de datos: necesita base legal, un contrato con el
  proveedor y un límite de uso ([[gobierno-y-privacidad]]). Que el almacén los tenga no autoriza a
  moverlos.
- **No dejar rastro de lo que se envió.** Sin un registro de escrituras —qué campo, qué valor, qué
  día y en qué ejecución— la primera pregunta del negocio («¿por qué este contacto tiene este
  segmento?») no tiene respuesta ([[observabilidad-de-datos]]).

## Comprueba que lo sabes

:::practica
enunciado: Tienes 120.000 suscriptores en una herramienta de correo y cada día cambian 800. La API acepta lotes de 100 registros y 10 llamadas por segundo. Calcula cuántas llamadas y cuánto tarda la sincronización diaria, y compáralo con una carga completa.
pista: Divide el número de filas entre el lote y redondea hacia arriba; después divide entre el ritmo.
solucion: Sincronización diaria: ⌈800 / 100⌉ = 8 llamadas, y 8 / 10 = 0,8 segundos. Carga completa: ⌈120.000 / 100⌉ = 1.200 llamadas, y 1.200 / 10 = 120 segundos, dos minutos. La diferencia de 150 veces sale solo de filtrar por la fecha de modificación, no de tocar el tamaño del lote: subirlo a 1.000 dejaría la carga completa en 120 llamadas y doce segundos, pero la API rara vez acepta lotes tan grandes.
:::

:::quiz
p: El equipo comercial edita a mano el campo `teléfono` en el CRM. ¿Qué debe hacer tu sincronización con ese campo?
o: Escribirlo cada noche con el valor del almacén, que es la fuente de la verdad
o: No escribirlo nunca: ese campo pertenece al CRM y el almacén solo lo lee
o: Escribirlo solo cuando el valor del almacén sea distinto del que hay en el CRM
a: 2
e: La propiedad del campo es lo que evita bucles y pérdida de trabajo. Si el negocio edita un campo en la herramienta, ese campo tiene su dueño allí; si el almacén lo sobrescribe, el comercial corrige y la sincronización vuelve a pisarlo. La tercera opción parece razonable, pero sigue borrando la corrección: el problema no es si el valor coincide, es quién manda.
:::

:::quiz
p: Hay 480.000 contactos, lotes de 200 registros y un límite de 5 llamadas por segundo. ¿Qué supone una carga completa?
o: 16 llamadas y 3,2 segundos
o: 2.400 llamadas y 8 minutos
o: 480.000 llamadas y más de 26 horas
a: 2
e: Con lotes de 200 hacen falta 480.000 / 200 = 2.400 llamadas, y a 5 por segundo son 480 segundos, ocho minutos. Las otras dos cifras corresponden a la sincronización incremental (16 llamadas) y a escribir de uno en uno, que es exactamente lo que evita el tamaño de lote.
:::

:::quiz
p: La API devuelve un timeout a mitad de la sincronización y el proceso se reintenta desde el principio. ¿Qué evita que aparezcan contactos duplicados?
o: Escribir con un upsert sobre una clave de identidad estable en cada reintento
o: Filtrar los duplicados por correo al terminar
o: Reintentar solo por la mañana, cuando la API va más rápida
a: 1
e: Un `upsert` por clave es idempotente: escribir dos veces el mismo objeto con los mismos datos deja el mismo resultado, así que el reintento es inofensivo. Filtrar por correo después es una limpieza manual que no siempre acierta, y reintentar más tarde no cambia nada: el timeout volverá a pasar.
:::
