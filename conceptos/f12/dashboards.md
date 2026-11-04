---
id: dashboards
titulo: Cuadros de mando
fase: 12
nivel: intermedio
rutas: [core]
prerequisitos: [visualizacion-honesta, storytelling-con-datos]
tags: [comunicacion, metricas, producto, alertas]
resumen: Un cuadro de mando no es una pared de gráficos, sino un puñado de métricas accionables con dueño, frecuencia de actualización y umbral de alerta.
fuentes: ["Few (2006), 'Information Dashboard Design'", "Knaflic (2015), 'Storytelling with Data'"]
---

## En una frase

Un cuadro de mando es la pantalla que alguien mira para decidir si hoy hace algo distinto:
cada número que aparece tiene un dueño, un umbral y una acción asociada, y todo lo que no
cambia ninguna decisión sobra.

## La idea

Piensa en el salpicadero de un coche. No trae cuarenta indicadores: trae velocidad,
revoluciones, temperatura, combustible y unos cuantos chivatos que se encienden cuando hay que
hacer algo. Ninguno está ahí «porque queda bien»; todos están porque existe una acción: frenar,
reducir, repostar, parar en el arcén. Un cuadro de mando que enseña treinta gráficos hace lo
contrario: no resume el trabajo, lo traslada a quien lo mira, que tiene que decidir por su
cuenta qué es normal y qué no.

La diferencia entre un panel útil y un cementerio de gráficos se reduce a cuatro preguntas por
métrica:

1. **¿Tiene dueño?** Una persona con nombre que responde cuando el número se tuerce. Si la
   respuesta es «el equipo», no tiene dueño.
2. **¿Tiene umbral?** Un valor a partir del cual alguien tiene que actuar, escrito en algún
   sitio. Sin umbral, el número es un adorno que hay que interpretar cada mañana.
3. **¿Existe la acción?** Si el indicador se dispara y no hay nada que hacer (o nadie sabe qué
   hacer), el indicador solo genera ansiedad.
4. **¿Alguien lo mira?** Un panel que nadie ha abierto en tres meses es coste de
   mantenimiento puro. La regla práctica: lo que no se ha mirado en un trimestre se retira.

De ahí sale la **jerarquía**, que es la parte de diseño que más se olvida. Un panel tiene un
número principal (el que resume el objetivo del equipo), tres a cinco de apoyo que explican por
qué el principal se mueve, y el detalle escondido detrás de un clic para cuando haga falta
investigar. Si todo está al mismo nivel visual, nada destaca y se vuelve a la lectura de treinta
gráficos. Los indicadores también se encadenan: el número principal suele ser **retardado**
(mide lo que ya pasó, como los ingresos del mes) y los de apoyo son **adelantados** (miden lo
que anticipa el resultado, como el número de pruebas gratis de esta semana). Un panel que solo
tiene indicadores retardados siempre avisa tarde.

La **frecuencia de actualización** se elige por la cadencia de la decisión, no por lo que
permita la tecnología. Si la decisión es mensual, refrescar cada minuto no aporta nada y llena
el panel de ruido; si la decisión es diaria, un panel que se actualiza los lunes llega tarde
cuatro días de cada cinco. Y hay una cifra que tiene que estar siempre visible junto al título:
**hasta cuándo llegan los datos**. Un panel sin esa marca se lee como si fuera de ahora mismo,
y el día que el proceso de carga falla, alguien decide con datos de la semana pasada sin
enterarse.

Por último, una métrica sin comparación no dice nada. Todo número del panel necesita su
término de comparación: el mismo día de la semana pasada, el mismo mes del año pasado o el
objetivo. Y para las métricas de latencia y tiempo de espera se publican percentiles, no medias:
un tiempo medio de respuesta de 200 ms con un p99 de 4 segundos describe un sistema que va
rápido de media y es insufrible para uno de cada cien usuarios ([[cuantiles-y-percentiles]]).

## Definición formal

Una métrica accionable es una tupla, no un número:

```
M = (nombre, definición, fuente, grano, dueño, umbral, acción)
```

- `nombre` — la etiqueta que se ve, sin ambigüedad: «pedidos pagados por día», no «pedidos».
- `definición` — la fórmula exacta y qué queda fuera (¿devoluciones? ¿pruebas internas?).
- `fuente` — la tabla o el conjunto de datos del que sale, para poder reproducirla.
- `grano` — la unidad de una fila: un pedido, un usuario y día, un país y mes.
- `dueño` — la persona que responde por el número.
- `umbral` — el valor a partir del cual hay que actuar.
- `acción` — lo que se hace cuando se cruza el umbral, escrita de antemano.

La alerta más simple compara el valor de hoy con lo que es normal para ese mismo día:

:::formula
z = (x − μ) / σ    ·    hay alerta si el valor absoluto de z supera 2
:::

- `x` — el valor observado hoy.
- `μ` — la media histórica del mismo día de la semana (o del mismo periodo comparable).
- `σ` — la desviación típica de esos mismos valores históricos.
- El `2` sale de que, en una distribución aproximadamente normal, apenas un 5 % de las
  observaciones cae fuera de dos desviaciones típicas.

Con tres o cuatro semanas de historia, `σ` se estima fatal y la regla dispara avisos falsos. En
la práctica se usan ventanas más largas (8 a 12 semanas del mismo día) o medidas robustas como
el MAD ([[outliers-y-deteccion]]), y se revisa el umbral cada trimestre.

Y una cifra que siempre acompaña al panel:

:::formula
retraso = ahora − max(fecha de la última fila cargada)
:::

Si ese retraso supera la frecuencia comprometida, el panel no está «un poco viejo»: está roto,
y hay que decirlo en la cabecera.

## Ejemplo

Visitas diarias de cuatro semanas, con el patrón semanal habitual (el fin de semana cae a la
mitad):

```
semana 1   1200  1150  1250  1300  1100   620   540
semana 2   1290  1180  1230  1330  1120   660   560
semana 3   1150  1200  1270  1290  1150   600   520
semana 4    980  1190  1250  1310  1130   640   550
```

Con las tres primeras semanas como referencia:

- Media por día de la semana: lunes 1213, martes 1177, miércoles 1250, jueves 1307, viernes
  1123, sábado 627, domingo 540.
- Media global de las 21 observaciones: **1034**.
- El lunes de la cuarta semana, 980 visitas: contra la media global queda a **z = −0,18**, es
  decir, invisible. Contra los lunes anteriores (1213 con `σ ≈ 71`), **z = −3,29**: ha caído un
  19 % y está fuera de banda.
- El resto de la semana vigilada se mueve entre z = 0,00 y z = 0,53: variación normal, ningún
  aviso.

Ese contraste es todo el concepto. Un panel que dibuja los valores en crudo con una única línea
de media falla en las dos direcciones a la vez: deja pasar la caída real del lunes (z = −0,18
contra la media global, invisible) y hace parecer un problema el domingo, que contra esa misma
media queda a z = −1,62 cuando contra los domingos anteriores está en z = 0,50, es decir, en lo
normal. Comparar con el mismo día de la semana quita el falso positivo del fin de semana y deja
ver el verdadero del lunes.

## Código

```python verificable
import numpy as np

# Visitas por dia de 4 semanas (filas = semanas, columnas = lunes a domingo).
visitas = np.array([[1200, 1150, 1250, 1300, 1100, 620, 540],
                    [1290, 1180, 1230, 1330, 1120, 660, 560],
                    [1150, 1200, 1270, 1290, 1150, 600, 520],
                    [ 980, 1190, 1250, 1310, 1130, 640, 550]])

referencia = visitas[:3]             # tres semanas de base
vigilada = visitas[3]                # la semana que se vigila
media_dia = referencia.mean(axis=0)  # una media por dia de la semana
sigma_dia = referencia.std(axis=0, ddof=1)

print("medias por dia (L a D):", media_dia.round(0).astype(int).tolist())
# -> [1213, 1177, 1250, 1307, 1123, 627, 540]
print("z de la semana vigilada:", ((vigilada - media_dia) / sigma_dia).round(2).tolist())
# -> [-3.29, 0.53, 0.0, 0.16, 0.26, 0.44, 0.5]
print("media global de las 21 observaciones:", round(referencia.mean()))
# -> 1034

# La misma caida del lunes, juzgada de dos formas: la media global la esconde.
z_lunes = (vigilada[0] - media_dia[0]) / sigma_dia[0]
z_global = (vigilada[0] - referencia.mean()) / referencia.std(ddof=1)
print(f"el lunes 980: z contra los lunes {z_lunes:.2f}, z contra todo {z_global:.2f}")
# -> el lunes 980: z contra los lunes -3.29, z contra todo -0.18
print("alerta solo con el mismo dia de la semana:", bool(abs(z_lunes) > 2))
# -> True
```

```sql verificable
-- Un panel no necesita una consulta por grafico: esta devuelve la metrica, su valor
-- anterior y la variacion, y solo de los ultimos dias.
CREATE TABLE pedidos (fecha DATE, pedidos INTEGER, cancelados INTEGER);

INSERT INTO pedidos VALUES
    ('2024-05-01', 420, 12), ('2024-05-02', 455, 9), ('2024-05-03', 480, 14),
    ('2024-05-04', 300, 6),  ('2024-05-05', 285, 5), ('2024-05-06', 501, 22),
    ('2024-05-07', 470, 11);

SELECT fecha,
       pedidos,
       ROUND(100.0 * cancelados / pedidos, 2) AS cancelacion_pct,
       pedidos - LAG(pedidos) OVER (ORDER BY fecha) AS delta_ayer
FROM pedidos
ORDER BY fecha DESC
LIMIT 3;
```

```text
fecha      | pedidos | cancelacion_pct | delta_ayer
2024-05-07 |     470 |            2.34 |        -31
2024-05-06 |     501 |            4.39 |        216
2024-05-05 |     285 |            1.75 |        -15
```

## Errores típicos

- **El cementerio de gráficos.** Treinta paneles porque «por si acaso». Nadie los mira, nadie
  los mantiene y cuando uno se rompe nadie se entera. Recorta a una pantalla, con un número
  principal y un puñado de apoyo, y retira lo que no se ha abierto en un trimestre.
- **No declarar hasta cuándo llegan los datos.** Sin esa marca, un panel con datos de anteayer
  se lee como si fuera de hace un minuto. Pon el retraso en la cabecera y que el panel avise
  cuando supere la frecuencia comprometida ([[calidad-y-slas]]).
- **Alertas sin dueño ni acción.** Un aviso que llega a un canal que nadie mira, o que dice
  «las visitas han bajado» sin decir qué hacer, se ignora en tres semanas. Con la primera
  alerta ignorada empieza la fatiga de alertas: a partir de ahí se ignoran todas, incluidas las
  buenas.
- **Publicar medias para latencia y tiempos de espera.** La media esconde la cola, y la cola es
  lo que sufre la gente. Publica p50, p95 y p99, y di sobre qué población se calculan.
- **Refrescar según el pipeline y no según la decisión.** Un panel que se recalcula cada minuto
  para una decisión mensual es coste sin valor; uno diario para una decisión en tiempo real
  llega tarde. La frecuencia la manda la cadencia con la que alguien puede actuar.
- **Medir lo que sube solo.** Registros, páginas vistas o tiempo en pantalla suben casi siempre
  y no dicen si el producto mejora. Cada métrica de vanidad necesita un denominador: conversión,
  retención, ingresos por usuario activo.

:::trampa
Cambiar la definición de una métrica sin avisar. Si «usuarios activos» pasa de contar sesiones
a contar personas, el número cambia de nivel de un día para otro y el equipo se pasa la reunión
discutiendo del gráfico en vez del negocio. Las definiciones se versionan y se documentan
([[contratos-de-datos]], [[catalogo-y-linaje]]).
:::

:::practica
enunciado: Un panel de soporte tiene «tickets abiertos» y «tiempo medio de resolución». El lunes hay 340 tickets abiertos y el tiempo medio es 9 horas, con un p99 de 71 horas. ¿Qué falta para que esas dos cifras se puedan accionar y qué cambiarías del panel?
pista: Piensa en dueño, umbral, acción, comparación y en qué mide cada estadístico de la distribución.
solucion: Falta lo mínimo para decidir: el mismo día de la semana anterior o la media de los últimos lunes como comparación, un umbral (por ejemplo, avisar si el p99 supera 48 horas) y una acción escrita (reforzar el turno, priorizar los tickets de más de 3 días). La media de 9 horas es un mal indicador: con un p99 de 71 horas, la media esconde que una de cada cien incidencias se queda tres días sin resolver. El panel debería enseñar el número de tickets que superan el objetivo de resolución y el tiempo mediano, no la media.
:::

## Comprueba que lo sabes

:::quiz
p: El lunes de la cuarta semana hay 980 visitas, frente a una media global de 1034 y una media de los lunes anteriores de 1213 con desviación 71. ¿Qué lectura es correcta?
o: No hay nada que mirar, porque 980 está solo un 5 % por debajo de la media global
o: El lunes ha caído un 19 % respecto a los lunes anteriores y está a más de tres desviaciones, así que merece un aviso
o: El lunes está dentro de lo normal porque los fines de semana también bajan
a: 2
e: La media global mezcla días con niveles muy distintos (los fines de semana caen a la mitad), así que comparar contra ella esconde la caída. La comparación correcta es contra el mismo día de la semana: 980 frente a 1213 con sigma 71 es z = -3,29. La tercera opción confunde la estacionalidad semanal con una explicación de la caída.
:::

:::quiz
p: ¿Cuál de estas cuatro condiciones convierte un número en una métrica accionable?
o: Que aparezca en la pantalla principal del panel
o: Que tenga dueño, umbral y una acción definida de antemano
o: Que se actualice cada minuto
a: 2
e: Lo que hace accionable una métrica es que alguien responda por ella, que exista un valor a partir del cual haya que actuar y que la acción esté decidida antes de que ocurra. La posición en la pantalla, la frecuencia y el color ayudan a leerla, pero no la hacen accionable.
:::

:::quiz
p: El proceso que carga los datos del panel falla el viernes y nadie lo nota hasta el martes. ¿Cuál es la medida preventiva más eficaz?
o: Añadir más gráficos al panel para que el fallo se note
o: Publicar en la cabecera hasta cuándo llegan los datos y alertar cuando el retraso supere la frecuencia comprometida
o: Cambiar el panel para que se actualice cada minuto
a: 2
e: Un panel con datos viejos y sin fecha visible miente con la misma cara que uno correcto. La marca de frescura y la alerta por retraso son lo que convierte un fallo silencioso en un aviso. Actualizar más a menudo no arregla la carga rota, y más gráficos no dicen nada sobre la frescura.
:::
