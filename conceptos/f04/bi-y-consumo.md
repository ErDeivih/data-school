---
id: bi-y-consumo
titulo: BI y capa de consumo
fase: 4
nivel: básico
rutas: [de, core]
prerequisitos: [oltp-vs-olap, modelado-dimensional]
tags: [bi, dashboards, coste, gobierno]
resumen: Cuadros de mando sobre tablas curadas: cuándo consultar en vivo, cuándo servir un extracto más barato y qué se publica con dueño y fecha de caducidad.
fuentes: ["Kimball & Ross (2013), 'The Data Warehouse Toolkit'", "Few (2013), 'Information Dashboard Design'"]
---

## En una frase

La capa de consumo es lo que el negocio abre cada mañana: cuadros de mando y listados que leen de
tablas ya curadas. Decidir si se sirven en vivo o como extracto, y quién responde de cada uno, es
la última decisión de un pipeline.

## La idea

Imagina un restaurante. La cocina es el almacén: allí están los ingredientes limpios y las recetas.
El mostrador es la capa de consumo: los platos ya emplatados que se llevan al cliente. Nadie entra
en la cocina a cortarse, y el que cocina no atiende la mesa.

Hay dos formas de servir el mismo plato:

- **Consulta viva.** Cada vez que alguien abre el cuadro se lanza una consulta contra el almacén
  ([[data-warehouse]]). El número es el de este segundo, y el precio lo pagas en cada apertura:
  cómputo, bytes escaneados y cola compartida con los demás trabajos.
- **Extracto.** El cuadro lee una copia que vive en el motor de la herramienta de BI y que se
  refresca por horario. Abrirlo es instantáneo y no toca el almacén, pero el número tiene una edad:
  la del último refresco terminado.

La elección no es de gusto, es aritmética. Un cuadro que se abre 6.000 veces al mes y escanea 2 GB
por apertura mueve 12 TB; el mismo cuadro extraído son 60 GB copiados 30 veces, 1,8 TB. Y el extracto
**no siempre gana**: con 120 consultas al mes de 2 GB, 0,24 TB, sale más barato no copiar nada. Si el
cuadro decide qué puja de publicidad se ajusta en diez minutos, la frescura vale más que el ahorro y
se consulta en vivo.

El tercer ingrediente es el gobierno, y es el que más se olvida. Un cuadro es un producto: tiene
dueño, responde a una pregunta concreta y tiene fecha de revisión. De ahí salen tres reglas:

1. **La fuente está curada.** El cuadro lee tablas de consumo, no la base de la aplicación
   ([[oltp-vs-olap]]), que es la que sostiene la facturación.
2. **La métrica está definida una sola vez.** «Ingresos netos» sale de la capa semántica
   ([[capa-semantica-y-metricas]]) o de un modelo con contrato ([[contratos-de-datos]]), nunca de
   una fórmula escrita a mano dentro de la herramienta: cuando la definición vive dentro del cuadro
   aparecen dos cifras para la misma pregunta.
3. **Lo publicado tiene responsable.** El catálogo y el linaje dicen de dónde sale cada número
   ([[catalogo-y-linaje]]); el dueño dice a quién se le pregunta cuando está mal.

:::trampa
Un cuadro que nadie abre sigue costando: se refresca, escanea, ocupa espacio y alguien lo mantiene
cuando cambia un esquema. Antes de publicar uno nuevo, mira cuántas veces se abrió el último
informe parecido. La mayoría de las organizaciones tiene cientos de cuadros y docenas de usuarios.
:::

## Definición formal

El coste mensual de servir un cuadro de las dos maneras:

:::formula
C_viva = n · b · p          C_extracto = f · B · p
:::

Símbolos:

- `n` — consultas que recibe el cuadro en un mes.
- `b` — bytes que escanea cada consulta. Sin poda de partición es la tabla entera
  ([[particionado-y-clustering]]).
- `p` — precio del almacén por TB escaneado.
- `f` — refrescos del extracto en un mes.
- `B` — bytes que copia cada refresco: la tabla completa del extracto.
- `C_viva`, `C_extracto` — coste mensual de cada opción, en euros.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Consultas que recibe el cuadro en un mes | consultas/mes | La consulta viva se encarece en línea recta; pasado el cruce, el extracto gana |
| `b` | Bytes que escanea cada consulta | TB | Igual que `n`: se paga por cada apertura, así que podar la partición es el mayor ahorro |
| `p` | Precio del almacén por TB escaneado | €/TB | Suben las dos opciones por igual: no mueve el cruce, solo la factura |
| `f` | Refrescos del extracto en un mes | refrescos/mes | El extracto se encarece y el cruce sube: menos casos en los que compensa |
| `B` | Bytes que copia cada refresco | TB | Igual que `f`: pagas la tabla entera en cada vuelta |
| `periodo` | Cada cuánto se refresca el extracto | horas | El dato envejece; por encima de lo que aguanta la decisión, el ahorro no vale nada |
| `duracion` | Lo que tarda un refresco en terminar | minutos | Suma a la edad del dato y, si supera al periodo, los refrescos se solapan |
:::

De ahí sale la regla de decisión: el extracto conviene cuando `f · B < n · b`, es decir, cuando el
cuadro se lee más de lo que se refresca. El punto de cruce, las consultas al mes a partir de las
cuales el extracto es más barato, es `n* = f · B / b`.

Y el precio del extracto no se paga en euros, se paga en tiempo:

:::formula
edad máxima del dato = periodo de refresco + duración del refresco
:::

- `periodo de refresco` — cada cuánto se lanza la copia: cada hora, cada noche.
- `duración del refresco` — lo que tarda en terminar. Con periodo nocturno y una duración de 40
  minutos, el dato de las 9:00 de la mañana ya tiene siete horas.
- `edad máxima del dato` — lo que puede tener de viejo el número que ve el usuario. Si la decisión
  que se toma con él es mensual, siete horas dan igual; si es una puja en tiempo real, no.

:::figura
fichero: bi-y-consumo-coste-viva-y-extracto
pie: A la izquierda, las dos rectas de coste: la consulta viva arranca en cero y sube con cada apertura, el extracto es una línea plana porque se paga una vez al mes. El corte a 900 consultas es la frontera entre las dos estrategias, y a 6.000 aperturas el extracto cuesta casi siete veces menos. A la derecha, el mismo cruce calculado para distintos valores de bytes escaneados por consulta: podar la partición baja `b` de 2 GB a 0,02 GB y mueve el cruce de 900 a 90.000 consultas, con lo que la consulta viva pasa a ser la opción barata. La decisión no la toma el número de usuarios, la toma cuánto lee cada consulta.
fuente: figuras/bi-y-consumo-1.py
:::

## Ejemplo

Un cuadro de ventas por canal, con estos números:

- Se abre 6.000 veces al mes y cada apertura escanea 2 GB.
- La tabla que copiaría el extracto ocupa 60 GB y se refrescaría cada noche, 30 veces al mes.
- El almacén cobra 5 € por TB escaneado, contando 1 TB como 1.000 GB.

| Opción | Cálculo | Coste al mes |
| --- | --- | --- |
| Consulta viva | 6.000 × 2 GB = 12 TB, a 5 € el TB | 60 € |
| Extracto | 30 × 60 GB = 1,8 TB, a 5 € el TB | 9 € |

El cruce está en `n* = 30 · 60 / 2 = 900` consultas al mes. Con 6.000 aperturas, el extracto sale
6,7 veces más barato, y el precio que pagas es que el número puede tener hasta 24 horas.

El detalle que le da la vuelta: si el cuadro filtra por la fecha de hoy y la tabla está particionada
por día, cada consulta escanea 0,02 GB en vez de 2 GB. El cruce pasa a `30 · 60 / 0,02 = 90.000`
consultas al mes y la consulta viva cuesta 0,6 € frente a los 9 € del extracto: la misma tabla y la
conclusión contraria. Lo que decide es cuántos bytes lee cada consulta.

## Código

```python verificable
# Coste mensual de servir el mismo cuadro de las dos maneras.
consultas_mes = 6000
gb_por_consulta = 2.0      # lo que escanea una consulta sin podar la particion
gb_tabla = 60.0            # lo que ocupa la tabla que copia el extracto
refrescos_mes = 30
precio_tb = 5.0            # tarifa de ejemplo: euros por TB escaneado
gb_por_tb = 1000.0

viva = consultas_mes * gb_por_consulta / gb_por_tb * precio_tb
extracto = refrescos_mes * gb_tabla / gb_por_tb * precio_tb
# Cruce: consultas al mes que igualan el coste del extracto (aqui se cancela precio_tb)
cruce = refrescos_mes * gb_tabla / gb_por_consulta

print(f"consulta viva {viva:7.2f} EUR/mes")             # -> 60.00
print(f"extracto      {extracto:7.2f} EUR/mes")         # -> 9.00
print(f"cruce en {cruce:.0f} consultas/mes")            # -> 900
```

:::claves
- `gb_por_tb = 1000.0` es una decisión tuya, no una constante física: parte de las facturas de nube
  usan TiB (1.024 GiB) y redondean a su manera. Cambiar ese número altera los dos costes, pero **no**
  el cruce, porque se cancela en la división.
- El cruce se calcula con `gb_tabla` y `gb_por_consulta` en las **mismas** unidades. Si metieras uno
  en TB y el otro en GB, el resultado saldría 1.000 veces mayor y decidirías lo contrario.
- Los `print` con `f"..."` no calculan nada: `7.2f` solo alinea en siete caracteres y redondea a dos
  decimales al escribir. La variable sigue teniendo todos sus decimales.
- Una división en Python 3 siempre devuelve `float`: `cruce` es `900.0`, y `{cruce:.0f}` lo imprime
  sin decimales. Si esperabas un entero, no lo es.
- El extracto de este cálculo solo paga el escaneo del refresco. Falta el cómputo, el almacenamiento
  de la copia y el trabajo de mantenerla: súmalos y el cruce se desplaza a la izquierda, es decir,
  hacen falta más consultas para que compense.
:::

```sql ilustrativo
-- El cuadro no lee la tabla de la aplicacion: lee una vista curada y podada por fecha.
CREATE OR REPLACE VIEW consumo.ventas_dia AS
SELECT fecha, canal, sum(importe) AS importe
FROM oro.fact_ventas
WHERE fecha >= DATE '2024-01-01'   -- el filtro es lo que permite podar la particion
GROUP BY fecha, canal;
```

## Errores típicos

- **Decidir por costumbre y no por números.** «En esta empresa los cuadros siempre han sido
  extractos» no es un argumento. Calcula `n · b` y `f · B` con las cifras reales de un mes; son dos
  multiplicaciones.
- **Publicar sin dueño ni fecha de revisión.** Un cuadro sin dueño es un cuadro que nadie arregla, y
  uno sin fecha de caducidad es un cuadro que sigue vivo cinco años después de que se fuera el
  equipo que lo pidió.
- **Escribir la fórmula dentro del cuadro.** En cuanto dos cuadros calculan «margen» con dos
  fórmulas, dejas de tener una métrica y empiezas a tener un debate. La definición va en la capa
  semántica ([[capa-semantica-y-metricas]]) y el cuadro la consume.
- **Extraer la tabla entera para mirar un mes.** Un extracto de 60 GB que solo se usa para el mes en
  curso es 59 GB de coste puro. Extrae lo que se consulta, con el grano que se consulta.
- **Copiar los datos sin copiar los permisos.** El extracto es una copia: si en el almacén había
  control de acceso por fila, en el fichero del motor de BI no hay nada salvo que lo montes. Un
  extracto con datos personales y sin control de acceso es una fuga esperando a que alguien comparta
  el enlace.
- **No declarar el grano del extracto.** Si el extracto agrega por día y alguien suma su columna
  `pedidos` después de unirlo con otra tabla, cuenta doble. El grano va en la documentación y en la
  prueba, no en la cabeza del que lo montó.

## Comprueba que lo sabes

:::practica
enunciado: Un cuadro escanea 0,5 GB por apertura y lo abren 500 veces al día durante 20 días laborables. La tabla del extracto ocupa 200 GB y se refresca cada 2 horas (12 veces al día) durante esos 20 días. ¿Cuál de las dos opciones es más barata?
pista: Pasa las dos opciones a TB al mes y compáralas con el cruce `n* = f · B / b`.
solucion: La consulta viva son 500 × 20 = 10.000 aperturas y 10.000 × 0,5 GB = 5 TB al mes. El extracto son 12 × 20 = 240 refrescos de 200 GB = 48 TB al mes, casi diez veces más. El cruce está en 240 × 200 / 0,5 = 96.000 consultas al mes, muy por encima de las 10.000 reales, así que gana la consulta viva. Con un refresco nocturno (20 refrescos, 4 TB, 20 € frente a los 25 € de la consulta viva) el extracto ya gana: el cruce baja a 20 × 200 / 0,5 = 8.000 consultas al mes, por debajo de las 10.000 reales, y el precio es un dato de hasta 24 horas más lo que tarde el refresco.
:::

:::quiz
p: Un cuadro se abre 6.000 veces al mes, cada apertura escanea 2 GB y el extracto completo son 60 GB que se copian cada noche. ¿Qué opción sale más barata?
o: La consulta viva, porque siempre devuelve el dato del momento
o: El extracto, porque a partir de unas 900 consultas al mes copiar sale más barato que consultar
o: Las dos cuestan lo mismo, porque el almacén cobra por almacenamiento y no por consulta
a: 2
e: La consulta viva mueve 12 TB (60 €) y el extracto 1,8 TB (9 €): el cruce está en 900 consultas al mes y se está muy por encima. Que la consulta viva sea más fresca no la hace más barata, y el almacén sí cobra por bytes escaneados en los motores analíticos habituales.
:::

:::quiz
p: La tabla del cuadro está particionada por día y el cuadro filtra por la fecha de hoy. ¿Qué efecto tiene?
o: Ninguno: el motor escanea la tabla completa en cualquier caso
o: Cada consulta lee solo su partición, el cruce sube a 90.000 consultas al mes y la consulta viva pasa a ser la opción barata
o: El extracto deja de ser necesario porque el motor cachea el resultado
a: 2
e: Si el filtro es sobre la columna de partición, el motor solo lee la partición del día: 0,02 GB en vez de 2 GB. Con `b` cien veces menor, el cruce se multiplica por cien (`n* = f · B / b`) y el extracto deja de compensar. Por eso el filtro y el particionado son decisiones de coste, no solo de estilo.
:::

:::quiz
p: Dos cuadros del mismo mes dan cifras distintas de «ventas». ¿Cuál es la causa más probable?
o: Que uno de los dos tiene mal el orden de las columnas
o: Que cada cuadro lleva su propia fórmula en vez de leer la misma métrica definida una vez
o: Que el almacén devuelve resultados distintos según la hora de la consulta
a: 2
e: Cuando la definición vive dentro de la herramienta de BI, cada autor decide si incluye devoluciones, impuestos o pedidos cancelados, y las dos cifras son «correctas» según su fórmula. La solución es definir la métrica una sola vez en la capa semántica y que los dos cuadros la consuman; el problema no es de rendimiento ni de horario.
:::
