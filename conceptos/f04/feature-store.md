---
id: feature-store
titulo: Feature store
fase: 4
nivel: experto
rutas: [de, ds]
prerequisitos: [ingenieria-de-features, fuga-de-datos, pipelines-de-ml]
tags: [mlops, variables, entrenamiento, produccion]
resumen: Un feature store garantiza que la variable que el modelo vio al entrenar es la misma que verá al predecir, con el valor que existía en ese instante y no con el de hoy.
fuentes: ["Sculley et al. (2015), 'Hidden Technical Debt in Machine Learning Systems'", "Breck et al. (2017), 'The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction'"]
---

## En una frase

Un feature store es la capa que garantiza dos cosas: que la variable que usa el modelo al
predecir se calcula **igual** que la que se usó al entrenar, y que en el entrenamiento se usó el
valor que existía **en el momento del evento**, no el de hoy.

## La idea

El problema que resuelve tiene dos caras, y la segunda es la que casi nadie ve venir.

**Cara uno: el sesgo entre entrenamiento y servicio.** El científico de datos calcula el ticket
medio de los últimos 30 días con un `GROUP BY` en el almacén, entrena y obtiene un AUC
estupendo. El ingeniero, para servir el modelo en producción con latencia de milisegundos, lo
recalcula en el servicio contando los pedidos que le llegan. Y resulta que el primero contaba
sólo los pedidos completados, el segundo cuenta todos; que el primero corta a medianoche y el
segundo a la hora de la petición; que el primero imputa los nulos con cero y el segundo con la
media. Dos implementaciones de «la misma» variable que no coinciden. El modelo rinde peor en
producción y nadie sabe por qué. Ese fenómeno se llama *training-serving skew*, y la única forma
de eliminarlo es no tener dos implementaciones.

**Cara dos: la corrección temporal (*point-in-time correctness*).** Si para predecir la compra
del 10 de marzo unes la variable con su valor del 20 de marzo, estás usando información que en
producción no existía. Es [[fuga-de-datos|fuga de datos]] pura, y hace que el modelo parezca
bueno en validación y fracase en real. La regla es tajante: para cada evento, la variable es
**el último valor conocido en ese instante o antes**.

Un feature store es, en la práctica, cuatro piezas:

1. **Almacén offline.** El histórico completo, en el almacén o en Parquet. Se usa para construir
   el conjunto de entrenamiento con uniones `as-of` ([[pandas-agrupaciones-y-joins|merge_asof]])
   y para el análisis.
2. **Almacén online.** Una base clave-valor de baja latencia (Redis, DynamoDB, Bigtable) que
   guarda **el último valor por entidad**. Es lo que consulta el servicio antes de predecir;
   el objetivo habitual son menos de 10 ms.
3. **Pipeline de materialización.** Empuja los valores del offline al online de forma periódica
   o en streaming, y define la **frescura** de la variable: si materializa cada hora, el servicio
   puede estar sirviendo un valor de hace 59 minutos.
4. **Registro de variables.** Nombre, entidad, tipo, dueño, transformación y versión. Sin esto,
   dos equipos definen `cliente_activo` de dos maneras y nadie lo descubre hasta que los números
   no cuadran.

:::trampa
Un feature store no arregla una fuga de datos. Si la variable se calcula con información
posterior al evento —por ejemplo, «número de devoluciones del pedido» para predecir si ese pedido
se va a devolver—, el almacén la servirá encantado de la vida, en el offline y en el online, con
toda la corrección temporal del mundo. La línea temporal hay que diseñarla antes; la
infraestructura sólo la respeta.
:::

## Definición formal

Sea `e` una entidad (un cliente, un producto, una sesión) y `f` una variable. El almacén offline
contiene una serie de observaciones `(e, f, t_v, valor)`: el valor de `f` para `e` en el instante
`t_v` en que se calculó. El almacén online contiene, para cada par `(e, f)`, el valor con el `t_v`
más reciente.

Para un evento `i` de la entidad `eᵢ` ocurrido en `tᵢ`, la variable correcta para entrenar es:

:::formula
x[i, f] = valor(f, eᵢ, t')   con   t' = max{ t_v ≤ tᵢ }
:::

Símbolos:

- `tᵢ` — el instante del evento que quieres predecir. Todo lo que se use tiene que ser anterior.
- `t_v` — el instante en que se calculó cada valor de la variable.
- `t'` — el instante del último valor conocido **en o antes** del evento. Es lo que hace el
  `direction="backward"` de una unión `as-of`.
- `x[i, f]` — lo que acabará en la fila `i` y la columna `f` de la matriz de entrenamiento.

El sesgo entre las dos implementaciones se mide con la desviación relativa, fila a fila:

:::formula
desviación = /x_offline − x_online/ ÷ max(/x_online/, ε)
:::

donde `x_offline` es el valor que se usó para entrenar, `x_online` el que sirvió el servicio para
el mismo evento y la misma entidad, y el denominador es ese mismo valor servido: es la referencia
contra la que se mide el sesgo. `ε` es un número muy pequeño que evita dividir por cero.
Un umbral razonable de alarma: más del 1 % de las filas con una desviación superior al 5 %.

## Ejemplo

Un cliente con una compra el 10 de marzo. El almacén de variables guarda tres valores de
`saldo_medio_30d`:

| Fecha del valor | saldo_medio_30d |
| --- | --- |
| 2024-03-01 | 700 |
| 2024-03-10 | 850 |
| 2024-03-20 | 900 |

- **Unión correcta** (último valor en o antes del 10 de marzo): **850 €**.
- **Unión incorrecta** (el valor más reciente de la tabla, 900 €): el modelo aprende que un saldo
  de 900 precede a una compra.
- La diferencia es de 50 €, un **5,9 %**. No parece mucho, pero si la variable entra en un modelo
  lineal con coeficiente 0,002, cada euro son 0,002 puntos de probabilidad: 50 € son 0,1 puntos,
  suficiente para cruzar un umbral de decisión de 0,5 en las predicciones que están cerca del
  corte. Y el sesgo es sistemático: no es ruido que se promedie, es una dirección concreta en
  todas las filas donde el valor subió después del evento.

En un caso real, este error se comete con variables que sólo existen hacia delante: el total
facturado del mes (que incluye el resto del mes), el estado final del pedido, el número de
devoluciones. Son las variables más predictivas del mundo… porque contienen la respuesta.

## Código

```python verificable
import pandas as pd

# Eventos a predecir: compra (1) o no compra (0) de un cliente.
eventos = pd.DataFrame({
    "cliente": [1, 1],
    "t_evento": pd.to_datetime(["2024-03-10", "2024-03-25"]),
    "objetivo": [1, 0],
})

# Historial de la variable, con el instante en que cada valor era el vigente.
snapshots = pd.DataFrame({
    "cliente": [1, 1, 1],
    "t_valor": pd.to_datetime(["2024-03-01", "2024-03-10", "2024-03-20"]),
    "saldo_30d": [700.0, 850.0, 900.0],
})

# Union as-of: para cada evento, el ultimo valor conocido en o antes de su fecha.
pit = pd.merge_asof(eventos.sort_values("t_evento"), snapshots.sort_values("t_valor"),
                    left_on="t_evento", right_on="t_valor", by="cliente",
                    direction="backward")
print("point-in-time", pit["saldo_30d"].tolist())     # -> point-in-time [850.0, 900.0]

# Lo que hace una union normal: coge el valor mas reciente para TODOS los eventos.
naive = eventos.merge(snapshots.sort_values("t_valor").groupby("cliente").tail(1), on="cliente")
print("union ingenua ", naive["saldo_30d"].tolist())  # -> union ingenua  [900.0, 900.0]
```

```python verificable
import pandas as pd

# La misma variable calculada por dos caminos: es el sesgo que busca el feature store.
pedidos = pd.DataFrame({
    "cliente": [1, 1, 1, 2, 2, 2, 3],
    "importe": [20.0, 40.0, 100.0, 10.0, 50.0, 90.0, 15.0],
    "estado":  ["ok", "ok", "devuelto", "ok", "ok", "ok", "ok"],
})

# Offline (dbt, para entrenar): media de todos los pedidos, devueltos incluidos.
offline = pedidos.groupby("cliente")["importe"].mean()
# Online (el servicio): filtra los devueltos, que es lo que hace el negocio.
online = pedidos[pedidos["estado"] == "ok"].groupby("cliente")["importe"].mean()

comparacion = pd.DataFrame({"offline": offline, "online": online})
# El denominador es el valor servido, en valor absoluto y con un suelo para no dividir por cero:
# es la misma formula que la definicion de arriba.
comparacion["desviacion"] = ((comparacion["offline"] - comparacion["online"]).abs()
                             / comparacion["online"].abs().clip(lower=1e-9))
print("clientes con desviacion > 1 %:", int((comparacion["desviacion"] > 0.01).sum()))  # -> 1
print(f"desviacion del cliente 1: {comparacion.loc[1, 'desviacion']:.1%}")              # -> 77.8%
```

## Errores típicos

- **Construir el conjunto de entrenamiento con la dimensión actual.** Un `JOIN` normal con
  `dim_cliente` trae el atributo de hoy para un evento de hace dos años. Tiene que ser una unión
  `as-of` o contra una dimensión versionada. Es el mismo fallo que en
  [[backfill-y-reproceso|el backfill]], pero aquí se cuela en el modelo en vez de en el informe.
- **Mantener dos implementaciones de la misma variable.** Una en SQL para entrenar y otra en
  Python dentro del servicio. Divergen el día que alguien arregla un caso límite en una sola.
  Si de verdad hay dos (batch y streaming), necesitan una comparación automática que las
  confronte sobre los mismos eventos.
- **Ignorar el TTL del almacén online.** Si los valores caducan a las 24 horas y el modelo se
  sirve los lunes por la mañana, las variables del viernes ya no están y llegan nulos. El modelo
  no falla: predice mal, que es peor.
- **Guardar las variables a nivel de fila en lugar de a nivel de entidad.** El almacén online se
  indexa por entidad. Si la variable sólo existe por pedido, para predecir necesitas la clave del
  pedido antes de predecir, y eso suele ser circular.
- **Confundir frescura con corrección temporal.** Materializar cada minuto no arregla que la
  variable esté mal calculada. La frescura dice *cuándo*, la corrección temporal dice *con qué
  información*.
- **No medir el sesgo nunca.** Sin una comparación periódica entre el valor offline y el valor
  que sirvió el servicio para los mismos eventos, el sesgo es invisible hasta que alguien compara
  una métrica de negocio con la del modelo. Se mide, se grafica y se alerta.

## Comprueba que lo sabes

:::quiz
p: Para predecir una compra ocurrida el 10 de marzo, ¿qué valor de la variable hay que usar en el conjunto de entrenamiento?
o: El valor más reciente disponible en la tabla, porque es el más informativo
o: El último valor calculado en o antes del 10 de marzo
o: La media de todos los valores de esa variable para ese cliente
a: 2
e: Cualquier valor posterior al evento contiene información que en producción no existía: eso es fuga de datos y hace que la validación mienta. La media de toda la serie también incluye el futuro. La regla es el último valor conocido en el instante del evento o antes.
:::

:::quiz
p: El modelo rinde bien en validación y mal en producción. La variable se calcula en un `dbt` para entrenar y en el servicio en Python para predecir. ¿Cuál es la causa más probable?
o: Que el modelo está sobreajustado y hay que regularizar más
o: Que las dos implementaciones de la variable no coinciden y el modelo ve en producción una distribución distinta a la del entrenamiento
o: Que el servidor de producción es más lento y las peticiones expiran
a: 2
e: Es el sesgo entrenamiento-servicio. Dos implementaciones de la misma variable divergen en los casos límite (qué filas entran, cómo se tratan los nulos, dónde se corta la ventana). Si la latencia fuera el problema, verías timeouts y errores, no predicciones peores. Un feature store lo resuelve porque hay una sola definición y dos materializaciones de la misma.
:::

:::aviso
Montar un feature store es caro: un almacén online con 400 variables y 50 millones de entidades
cuesta dinero todos los meses. Si tienes tres modelos y dos equipos, un `dbt` con las
definiciones centralizadas y una tabla de entrenamiento bien construida resuelve el 90 % del
problema. El feature store compensa cuando hay muchos modelos, latencia de milisegundos y varios
equipos pisándose.
:::
