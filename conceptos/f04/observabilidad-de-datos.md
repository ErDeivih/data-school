---
id: observabilidad-de-datos
titulo: Observabilidad de datos
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [calidad-y-slas, contratos-de-datos]
tags: [monitorizacion, anomalias, volumen, alertas]
resumen: Medir frescura, volumen, esquema y distribución contra la historia del propio dato detecta lo que ningún test escrito de antemano iba a encontrar.
fuentes: ["Moses, Gavish & Vorwerck (2022), 'Data Quality Fundamentals'", "Kleppmann (2017), 'Designing Data-Intensive Applications'"]
---

## En una frase

La observabilidad de datos es medir cómo se comporta el dato —frescura, volumen, esquema,
distribución— y compararlo con su propio comportamiento pasado, para detectar lo que no
esperabas y no sólo para comprobar lo que ya sabías que podía fallar.

## La idea

Un test dice «esto cumple la regla que escribí». La observabilidad dice «esto se comporta como
siempre… o no». La diferencia parece filosófica y es muy práctica: los tests cubren lo conocido,
y los incidentes que duelen son los desconocidos.

El ejemplo que mejor lo enseña: el número de filas de la tabla de eventos cae un 40 % un martes.
Ningún test falla. No hay nulos, las claves son únicas, los tipos cuadran, todas las columnas
obligatorias están. El pipeline ha funcionado perfectamente y el negocio está midiendo la mitad
de la realidad. Un test no lo detecta porque nadie escribió «comprobar que hoy hay 1,2 millones
de filas»; una serie temporal sí, porque sabe cuántas había los martes anteriores.

Los cinco ejes que se vigilan en la práctica, y qué detecta cada uno:

1. **Frescura.** `ahora − max(fecha_evento)`. Detecta el pipeline parado o atascado.
2. **Volumen.** Filas por partición. Detecta la pérdida parcial, que es más peligrosa que la
   caída total porque no hace ruido.
3. **Esquema.** Columnas nuevas, eliminadas, tipos cambiados, nulabilidad. Detecta el cambio
   silencioso del productor.
4. **Distribución.** Media, mediana, percentiles, proporción de nulos, cardinalidad de las
   categóricas. Detecta que el dato ha cambiado de significado sin cambiar de forma.
5. **Linaje.** Qué está afectado y qué se ha roto aguas abajo (ver [[catalogo-y-linaje]]).

El error de método que convierte la observabilidad en ruido inservible es **comparar con un
umbral fijo**. Los datos tienen estacionalidad fuerte: los domingos hay un 45 % menos de pedidos,
el primer día de mes se multiplican las facturas, en una campaña de rebajas el volumen se dispara.
Un umbral plano produce los dos tipos de fallo a la vez:

- **Falsos positivos:** alerta todos los domingos, y a la tercera semana nadie la mira.
- **Falsos negativos:** un domingo con un 30 % menos de lo normal (que ya es anómalo) pasa el
  umbral sin problema.

La solución es comparar cada partición con **la misma partición de periodos anteriores** —los
lags de 7, 14, 21 y 28 días capturan la semana y el mes— y usar un estadístico robusto, porque
una sola partición rara en la historia no debe estropear la referencia. La mediana y el MAD
(mediana de las desviaciones absolutas) hacen ese trabajo: un valor extremo no los mueve.

:::trampa
«El dato ha llegado, luego está bien». La frescura es el indicador más fácil de medir y el que
menos información da. Un pipeline puede entregar a tiempo una tabla con la mitad de las filas, con
una columna nueva sin documentar o con el 90 % de los valores a nulo. Sin volumen, esquema y
distribución, la frescura sola da una falsa sensación de control.
:::

## Definición formal

Para una serie de particiones del mismo tipo (por ejemplo, todos los lunes), el estadístico que
se usa es el **z-score robusto**:

:::formula
z = 0,6745 · (x − mediana) ÷ MAD
:::

:::formula
MAD = mediana( /xᵢ − mediana(x)/ )
:::

Símbolos:

- `x` — el valor de la partición que se está evaluando (filas, suma, porcentaje de nulos).
- `mediana(x)` — la mediana de los valores de las particiones de referencia del mismo tipo
  (los cuatro lunes anteriores, por ejemplo).
- `xᵢ` — cada uno de esos valores de referencia.
- `MAD` — la mediana de las desviaciones absolutas respecto a la mediana. Es una medida de
  dispersión que, a diferencia de la desviación típica, no se dispara con un valor extremo.
- `0,6745` — la constante que hace que `z` se lea igual que un z-score clásico
  ([[z-score-y-estandarizacion]]) cuando los datos son normales.

El umbral habitual es `z > 3,5` en valor absoluto, más alto que el 3 clásico precisamente porque
la mediana y el MAD ya son robustos y un umbral bajo dispararía en cada cola normal.

Para el **esquema y el dominio**, la comprobación no es estadística sino de conjuntos:

:::formula
categorías nuevas = conjunto de hoy − conjunto de referencia
:::

Si ese conjunto no está vacío y su proporción no es despreciable, hay un cambio de significado
aguas arriba.

## Ejemplo

Volumen de pedidos de los cinco lunes anteriores y del lunes de hoy:

```text
1.180.000   1.240.000   1.210.000   1.195.000   1.225.000   |   hoy: 430.000
```

- Mediana de referencia: **1.210.000**.
- Desviaciones absolutas: 30.000, 30.000, 0, 15.000, 15.000. Ordenadas: 0, 15.000, 15.000,
  30.000, 30.000. La mediana de esas desviaciones es el **MAD = 15.000**.
- z robusto: 0,6745 · (430.000 − 1.210.000) ÷ 15.000 = 0,6745 · (−52) = **−35,1**.

Con un umbral de 3,5 en valor absoluto, esto no es una alerta: es un incendio. Y fíjate en la
sensibilidad del método: una caída «sólo» del 5 % daría `x = 1.149.500`, un z de **−2,72**, que
no dispara. El estadístico distingue lo que es variación normal de lo que es una caída real, que
es exactamente lo que un umbral fijo no sabe hacer.

Segundo caso, el cambio de significado. La columna `pais` lleva meses con tres valores:

```text
antes:  ES 90,0 %   PT 8,0 %   FR 2,0 %
hoy:    ES 40,0 %   PT 5,0 %   FR 2,0 %   ?? 53,0 %
```

Aparece una categoría nueva `??` en más de la mitad de las filas. Ningún test de nulos falla, el
tipo sigue siendo texto y la frescura es perfecta. Si esa columna alimenta un modelo, acaba de
quedarse sin señal en la mitad de los casos, y nadie se enterará hasta que la métrica de negocio
caiga.

## Código

```python verificable
import numpy as np

# Volumen de pedidos de los cinco lunes anteriores y del lunes de hoy.
lunes_previos = np.array([1_180_000, 1_240_000, 1_210_000, 1_195_000, 1_225_000])
hoy = 430_000

mediana = np.median(lunes_previos)
mad = np.median(np.abs(lunes_previos - mediana))       # robusto: un extremo no lo mueve
z = 0.6745 * (hoy - mediana) / mad

print(f"mediana   {mediana:,.0f}")        # -> mediana   1,210,000
print(f"MAD       {mad:,.0f}")            # -> MAD       15,000
print(f"z robusto {z:.1f}")               # -> z robusto -35.1

# La misma formula con una caida del 5 %: no deberia disparar.
z_suave = 0.6745 * (0.95 * mediana - mediana) / mad
print(f"caida del 5 % -> z {z_suave:.2f}")   # -> caida del 5 % -> z -2.72
```

```python verificable
import pandas as pd

# Deriva de dominio: la columna 'pais' era estable y hoy llega distinta.
antes = pd.Series(["ES"] * 900 + ["PT"] * 80 + ["FR"] * 20)
hoy = pd.Series(["ES"] * 400 + ["PT"] * 50 + ["FR"] * 20 + ["??"] * 530)

print("categorias antes/hoy:", antes.nunique(), hoy.nunique())          # -> categorias antes/hoy: 3 4
print("proporcion ES antes/hoy:",
      f"{(antes == 'ES').mean():.1%}", f"{(hoy == 'ES').mean():.1%}")
# -> proporcion ES antes/hoy: 90.0% 40.0%
print("categoria nueva:", sorted(set(hoy) - set(antes)))                # -> categoria nueva: ['??']
```

## Errores típicos

- **Umbrales fijos sin estacionalidad.** Cualquier tabla con tráfico humano tiene ciclo semanal y
  mensual. Compara siempre contra el mismo día de la semana y contra el mismo punto del mes.
- **Vigilar sólo la frescura.** Es el indicador más fácil y el que menos cubre. Volumen, esquema
  y distribución detectan los incidentes silenciosos, que son la mayoría.
- **Alertar de todo.** Cuarenta alertas al día equivalen a cero alertas: el equipo las silencia y
  con ellas se va la que importaba. Cada alerta debe ser accionable, tener dueño y ser como mucho
  una por tabla y día.
- **No guardar la historia de las métricas.** Sin línea base no hay anomalía, sólo hay «hoy me
  parece raro». Las métricas de observabilidad se guardan en una tabla con la misma disciplina que
  los datos de negocio.
- **Confundir la causa con el síntoma.** Ver treinta tests rojos en la capa intermedia y no ver
  que la tabla final está vacía. El consumidor necesita el síntoma; el ingeniero, la causa. Se
  muestran los dos, pero se alerta por el síntoma.
- **Instrumentar sólo el final del pipeline.** Cuando un número sale mal, el problema suele estar
  tres capas más arriba. Hay que medir en cada frontera —origen a ingesta, ingesta a
  transformación, transformación a consumo— para poder acotar dónde se rompió.

## Comprueba que lo sabes

:::quiz
p: ¿Por qué se usa la mediana y el MAD en lugar de la media y la desviación típica para detectar anomalías de volumen?
o: Porque la mediana y el MAD se calculan más rápido
o: Porque un valor extremo en la historia de referencia desplazaría la media y la desviación, y ocultaría la anomalía siguiente
o: Porque la media no se puede calcular con datos diarios
a: 2
e: Si una de las particiones de referencia fue un día de caída, la media baja y la desviación sube, así que el umbral se ensancha y la próxima caída pasa desapercibida. La mediana y el MAD apenas se mueven ante un valor raro, y por eso el estadístico sigue siendo sensible.
:::

:::quiz
p: La tabla de eventos tiene hoy un 40 % menos de filas y todos los tests pasan. ¿Qué conclusión es correcta?
o: Que no hay ningún problema, porque los tests son la red de seguridad
o: Que el incidente es del tipo que sólo detecta la observabilidad: ningún test comprobaba el volumen contra la historia
o: Que hay que añadir un test con el umbral fijo de filas esperadas
a: 2
e: Los tests verifican reglas que alguien escribió de antemano; nadie había escrito «hoy deben llegar unas 1,2 millones de filas». La respuesta correcta no es fijar ese número a mano, porque en un domingo sería falso: es comparar contra la misma partición de semanas anteriores.
:::

:::aviso
La observabilidad genera datos sobre los datos. Esa tabla de métricas crece todos los días y
necesita su propio gobierno: retención, agregados y coste. Si la plataforma de observabilidad
cuesta más que el almacén que vigila, algo se ha hecho mal.
:::
