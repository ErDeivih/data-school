---
id: metricas-de-producto
titulo: Métricas de producto
fase: 12
nivel: intermedio
rutas: [core, ds]
prerequisitos: [dashboards, ab-testing, cuantiles-y-percentiles]
tags: [producto, metricas, retencion, cohortes, experimentos]
resumen: Qué medir para saber si el producto mejora de verdad: métrica norte, guardarraíles, retención por cohortes y estado estacionario en vez de números que suben solos.
fuentes: ["Kohavi, Tang y Xu (2020), 'Trustworthy Online Controlled Experiments'", "Croll y Yoskovitz (2013), 'Lean Analytics'", "Ries (2011), 'The Lean Startup'"]
---

## En una frase

Una métrica de producto se elige por la decisión que mueve: una métrica norte que represente el
valor que recibe quien usa el producto, unos pocos guardarraíles que no pueden empeorar y la
retención mirada por cohortes, que es el único sitio donde se ve si el producto mejora de verdad.

## La idea

Casi todos los paneles de producto tienen el mismo problema: enseñan números que solo pueden subir.
Registros, visitas, usuarios totales, tiempo en pantalla. Son las **métricas de vanidad**, y su
defecto está en que no se pueden accionar, no en que sean falsas: cuando una sube, nadie sabe qué hizo
bien, y cuando baja, nadie sabe qué arreglar. La prueba es siempre la misma pregunta: **si este
número se tuerce, ¿qué hago mañana distinto?** Si no hay respuesta, el número sobra.

Una métrica de producto sirve cuando está pegada al valor que recibe el usuario. Para un mercado
de segunda mano, «transacciones completadas por comprador activo» vale; «usuarios registrados» no,
porque un registro es una promesa y una transacción es un hecho.

Conviene añadir un
**denominador**: los ingresos suben solos si también sube el número de usuarios, así que lo que se
mira es el ingreso por usuario activo, la conversión por visita o la retención de quien ya probó
el producto.

**Métrica norte y métrica de entrada.** La norte es el resultado que le importa al negocio y suele
moverse despacio (retención a 90 días, ingreso por usuario). Las de entrada son las que el equipo
controla en el día a día y que mueven a la norte con retraso (tiempo hasta el primer valor, tasa de
fallo del flujo de compra, porcentaje de búsquedas sin resultado). Trabajar solo con la norte
frustra, porque no se puede tocar; trabajar solo con las de entrada hace perder de vista para qué
estaban.

**Guardarraíles.** Cuando eliges una métrica, el sistema se organiza para moverla, y ahí aparece el
daño colateral. Subir la conversión es fácil si se ocultan los gastos de envío hasta el final;
subir el tiempo en pantalla es fácil si el usuario no encuentra lo que busca. Los guardarraíles son
dos o tres métricas que **no pueden empeorar** mientras se persigue la norte: latencia, tasa de
error, contactos con soporte, cancelaciones, devoluciones, accesibilidad. Se eligen antes del
experimento y con su umbral escrito, porque después siempre hay una explicación para el daño
([[ab-testing]]).

**Cohortes: la única forma de ver si algo mejora.** Una cohorte es un grupo de usuarios que
comparten el momento de entrada (los que se registraron en enero) y se sigue su comportamiento
semana a semana. La alternativa —mirar la retención agregada de todo el producto— mezcla usuarios
de edades distintas y produce paradojas: con una base que crece mucho, la métrica agregada
«activos de este mes sobre activos del mes pasado» puede dar 120 % mientras cada cohorte pierde el
80 % de su gente. La curva de una cohorte tiene una forma reconocible: cae rápido las primeras
semanas y luego se aplana en un **suelo** de usuarios habituales. Ese suelo, y no el primer día, es
lo que dice si el producto sirve: una curva que se aplana alto tiene usuarios que vuelven solos;
una que baja hasta cero tenía una novedad, no un producto.

**La retención es la palanca de crecimiento, por blanda que parezca la palabra.** Con altas constantes, la
base de usuarios no crece sin fin: converge a un estado estacionario que es el cociente entre las
altas y la tasa de abandono. Con 4.000 altas al mes y un abandono del 6 % mensual, la base se
estabiliza en 66.667 usuarios, por muchas campañas que se hagan. Un punto menos de abandono la
lleva a 80.000: el mismo efecto que subir las altas un 20 %. Y como el valor de un usuario es el
margen que deja cada mes multiplicado por los meses que se queda, la retención entra dos veces: en
cuántos usuarios hay y en cuánto vale cada uno.

**Definición antes que número.** Toda métrica necesita su ficha: qué evento cuenta, qué población
entra, en qué ventana y qué queda excluido. «Usuarios activos» es una pregunta, no una métrica:
¿activos por abrir la aplicación o por completar una acción con valor? Dos equipos con definiciones
distintas se pasan la reunión discutiendo del gráfico en vez del negocio, y la solución es la capa
semántica y los contratos de datos, no la buena voluntad ([[capa-semantica-y-metricas]]).

## Definición formal

**Curva de retención de una cohorte.** Para una cohorte de tamaño `N`:

:::formula
R(t) = usuarios_activos_en_t / N
:::

**Estado estacionario.** Con `A` altas por periodo y `c` la tasa de abandono por periodo, la
recurrencia y su punto fijo son:

:::formula
U_{t+1} = U_t · (1 − c) + A          U* = A / c
:::

**Valor de vida.** Si cada usuario deja un margen `m` por periodo y la probabilidad de seguir ahí
tras `k` periodos es `(1 − c)^k`, la esperanza de vida es `1 / c` periodos:

:::formula
LTV = m / c
:::

**Quick ratio.** Cuánta gente entra por cada una que se va:

:::formula
quick_ratio = (altas + recuperados) / bajas
:::

**Descomposición de los ingresos.** La norte casi siempre se puede escribir como producto de
factores que un equipo puede tocar por separado:

:::formula
ingresos = usuarios_activos · frecuencia_de_uso · conversión · ticket_medio
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `R(t)` | Proporción de una cohorte que sigue activa en el periodo `t` | tanto por uno | Es la curva que hay que mirar. Si cae más rápido en las cohortes nuevas que en las viejas, el producto empeora aunque la base crezca |
| `N` | Tamaño inicial de la cohorte | usuarios | Al subir, la curva es más estable (menos ruido) y también más lenta de leer: una cohorte de 200 usuarios da saltos del 0,5 % con un solo usuario |
| `c` | Tasa de abandono por periodo | tanto por uno | Al subir, baja el estado estacionario y baja el valor de vida. Es la métrica más pequeña con el efecto más grande: dos puntos de más hunden la base un 25 % |
| `A` | Altas nuevas por periodo | usuarios | Al subir, sube el estado estacionario en la misma proporción. Es la palanca que se puede comprar con dinero, y por eso es la que menos se debe mirar sola |
| `U*` | Usuarios activos en equilibrio | usuarios | Es el techo al que tiende la base con la retención actual. Se alcanza en unos `3 / c` periodos: con un 6 % mensual, unos cuatro años |
| `m` | Margen que deja un usuario por periodo | euros | Al subir, sube el valor de vida en la misma proporción. Si `m` es negativo, retener más solo acelera la pérdida: primero hay que arreglar el margen |
| `LTV` | Valor de vida de un usuario | euros | Al subir, se puede pagar más por adquirir. Comparado con el coste de adquisición dice si el crecimiento se puede permitir |
| `quick_ratio` | Entradas por cada salida | adimensional | Por encima de 1 la base crece; por debajo, se encoge aunque las altas parezcan buenas. Por encima de 2 se considera crecimiento sano, pero solo como referencia de cada negocio |
| Guardarraíl | Métrica que no puede empeorar mientras se persigue la norte | según la métrica | Al subir el número de guardarraíles, la decisión se vuelve imposible: con diez, ninguno se cumple nunca y el equipo aprende a ignorarlos. Dos o tres, con umbral escrito |
:::

## Ejemplo

Cuatro cohortes de usuarios nuevos, con su actividad en las semanas siguientes (semana 0 es el
alta):

```
cohorte    N      S0    S1    S2    S3    S4
2024-01  1000   100%   42%   30%   25%   23%
2024-02  1200   100%   38%   26%   18%    -
2024-03  1400   100%   34%   22%    -     -
2024-04  1600   100%   31%    -     -     -
```

La lectura honesta: la retención de la semana 2 va de 30 % a 22 % y la de la semana 1 de 42 % a
31 %. Cada cohorte nueva retiene menos que la anterior, así que algo se rompió a finales de enero
y el producto empeora, no mejora.

La lectura tramposa: sumar todo y decir «tenemos 1.224 usuarios activos en la semana 2, un 23,5 %
de nuestra base». Ese 23,5 % no mide la retención de nadie: es una mezcla de cohortes de edades
distintas, y sube o baja según cuánta gente nueva entre, no según lo bien que retenga el producto.
Peor todavía es la métrica agregada clásica: con 10.000 activos, 10.000 altas en el mes y solo el
20 % de los activos anteriores que vuelve, los activos del mes son 0,2 · 10.000 + 10.000 = 12.000,
y 12.000 / 10.000 = **120 % de retención**. El número es correcto y la lectura es falsa: cada
cohorte ha perdido el 80 % de su gente.

Del mismo producto, con 4.000 altas al mes y un margen de 4 euros por usuario y mes:

- Abandono del 8 %: estado estacionario 4.000 / 0,08 = **50.000 usuarios**, valor de vida 4 / 0,08
  = **50 euros**.
- Abandono del 6 %: **66.667 usuarios** y **67 euros**.
- Abandono del 5 %: **80.000 usuarios** y **80 euros**.

Comparación que decide prioridades: bajar el abandono del 6 % al 5 % da 80.000 usuarios estables, y
subir las altas un 20 % con el abandono intacto da los mismos 80.000. La diferencia es
que las altas se compran (con dinero y de forma indefinida) y la retención se construye una vez.

:::figura
fichero: metricas-retencion-y-estado-estacionario
pie: Izquierda, dos curvas de retención por cohortes: caen rápido las primeras semanas y luego se aplana el suelo de usuarios habituales, que es lo que de verdad dice si el producto sirve. La cohorte que empieza más alta pero se desploma acaba por debajo de la que empieza más baja y se aplana, y por eso la retención se lee por cohortes y nunca en agregado. Derecha, el estado estacionario: la base de usuarios converge al cociente entre altas y abandono, y un punto menos de abandono mueve la meseta tanto como subir las altas un 20 %.
fuente: figuras/metricas-de-producto-1.py
:::

## Código

```python verificable
import pandas as pd

# Cuatro cohortes de usuarios nuevos y su actividad en las semanas siguientes.
# Cada fila es una cohorte; cada columna, una semana desde el alta (0 = el alta).
retencion = pd.DataFrame(
    [[1000, 420, 300, 250, 230],
     [1200, 456, 312, 210, None],
     [1400, 476, 308, None, None],
     [1600, 496, None, None, None]],
    index=["2024-01", "2024-02", "2024-03", "2024-04"],
    columns=[0, 1, 2, 3, 4])

# Curva de retencion: activos de la semana t sobre el tamano inicial de esa cohorte.
curva = retencion.div(retencion[0], axis=0)
print((100 * curva).round(1))
print("semana 2 por cohorte:", [round(100 * float(v), 1) for v in curva[2].dropna()])
# -> semana 2 por cohorte: [30.0, 26.0, 22.0]

# El agregado engana: juntar todas las cohortes mezcla usuarios de edades distintas.
usuarios = int(retencion[0].sum())
print("activos sobre el total por semana:",
      [round(100 * float(retencion[s].sum()) / usuarios, 1) for s in retencion.columns])
# -> activos sobre el total por semana: [100.0, 35.5, 17.7, 8.8, 4.4]
```

:::claves
- `retencion.div(retencion[0], axis=0)` divide **cada fila** por el tamaño inicial de su cohorte,
  que es lo que convierte el recuento de activos en una curva comparable entre cohortes de tamaños
  distintos. Sin `axis=0`, pandas intenta alinear por columnas y el resultado no tiene sentido.
- Los huecos van como `None`, que pandas convierte en `NaN`: una cohorte de marzo no puede tener
  dato de la semana 4 porque esa semana todavía no ha ocurrido. Rellenarlos con ceros es el error
  clásico y hace que las cohortes nuevas parezcan mucho peores de lo que son.
- `dropna()` sobre la columna 2 descarta las cohortes sin dato en esa semana. La alternativa,
  `fillna(0)`, mezcla «no lo sé todavía» con «cero usuarios» y estropea la curva.
- `float(...)` en los `round` no es decoración: `retencion[s].sum()` devuelve un escalar de NumPy,
  y su representación al imprimir una lista sale como `np.float64(35.5)` en vez de `35.5`.
:::

```python verificable
# Con altas constantes la base no crece sin fin: converge a altas / churn.
def base_estable(altas_mes, churn):
    return altas_mes / churn

altas, margen_mensual = 4000, 4.0
for churn in (0.08, 0.06, 0.05):
    print("churn %.0f %% -> base estable %.0f usuarios, LTV %.0f EUR"
          % (100 * churn, base_estable(altas, churn), margen_mensual / churn))
# -> churn 6 % -> base estable 66667 usuarios, LTV 67 EUR
# -> churn 5 % -> base estable 80000 usuarios, LTV 80 EUR

# Un punto de churn vale lo mismo que subir las altas un 20 %.
print("subir altas un 20 %:", round(base_estable(altas * 1.2, 0.06)))  # -> 80000
print("bajar el churn a 5 %:", round(base_estable(altas, 0.05)))       # -> 80000

# Quick ratio: cuanto entra por cada uno que se va. Por debajo de 1, la base se encoge.
for nuevos, recuperados, bajas in ((4000, 800, 2000), (3000, 300, 3300)):
    print("quick ratio %.2f" % ((nuevos + recuperados) / bajas))
# -> quick ratio 2.40
# -> quick ratio 1.00
```

:::claves
- `LTV = m / c` solo vale con abandono constante, que es falso casi siempre: los usuarios que
  aguantan son los que menos se van, así que el churn real de la base que queda baja con el tiempo
  y el valor de vida es mayor que esta cuenta. Sirve para comparar, no para prometer.
- El estado estacionario `A / c` no se alcanza nunca del todo: se llega al 95 % en unos `3 / c`
  periodos. Con un abandono del 6 % mensual son unos 50 meses, y por eso una mejora de retención
  tarda años en verse en la base total y meses en verse en la cohorte ([[series-temporales-componentes]]).
- El `quick_ratio` mezcla dos cosas distintas en el numerador: usuarios nuevos y usuarios que
  vuelven después de haberse ido. Conviene mirarlos separados, porque recuperar a alguien que ya
  conoce el producto es mucho más barato que traer a alguien nuevo, y el ratio agregado lo esconde.
- Si `m` es el margen por usuario y `base_estable` da usuarios, el LTV sale en euros por usuario.
  Mezclar margen mensual con margen anual multiplica o divide el resultado por doce: el error de
  unidades más frecuente de estas cuentas.
:::

```python verificable
import pandas as pd

# Cada metrica declara hacia donde mejora y si es la norte o un guardarrail.
# Sin fijar esa direccion, un efecto positivo se lee como bueno aunque sea la latencia.
medidas = pd.DataFrame({
    "metrica": ["retencion_semana_4", "ingreso_por_usuario", "latencia_p95", "tickets_soporte"],
    "efecto": [0.018, 0.002, 0.150, 0.060],
    "limite_inferior": [0.004, -0.011, 0.040, 0.010],
    "limite_superior": [0.032, 0.015, 0.200, 0.110],
    "direccion": ["sube", "sube", "baja", "baja"],
    "norte": [True, False, False, False],
})

# Se orienta todo a "bueno" antes de leer: en las de direccion "baja" se cambia el signo.
signo = medidas.direccion.map({"sube": 1, "baja": -1})
inferior, superior = medidas.limite_inferior * signo, medidas.limite_superior * signo
medidas["lectura"] = "sin cambio"
medidas.loc[inferior > 0, "lectura"] = "mejora"
medidas.loc[superior < 0, "lectura"] = "empeora"
print(medidas[["metrica", "efecto", "direccion", "lectura"]].to_string(index=False))

norte_mejora = bool((medidas.loc[medidas.norte, "lectura"] == "mejora").all())
guardarrailes_ok = bool((medidas.loc[~medidas.norte, "lectura"] != "empeora").all())
print("la metrica norte mejora:", norte_mejora)               # -> True
print("los guardarrailes aguantan:", guardarrailes_ok)         # -> False
print("decision:", "lanzar" if norte_mejora and guardarrailes_ok
      else "no lanzar: la latencia se come la mejora")
```

## Errores típicos

- **Métricas de vanidad sin denominador.** Usuarios registrados, páginas vistas y descargas solo
  suben, y suben más cuando más se gasta en publicidad. Lo que se mira es la proporción: ingreso
  por usuario activo, conversión por visita, retención de quien ya usó el producto.
- **Mirar el agregado en vez de la cohorte.** La retención global mezcla usuarios de edades
  distintas y su valor depende de cuánta gente nueva entre. La métrica agregada puede marcar 120 %
  mientras cada cohorte pierde cuatro de cada cinco usuarios. La cohorte es la única lectura que
  responde a «¿esto va a mejor?».
- **Rellenar con ceros las cohortes que aún no tienen dato.** Una cohorte de la semana pasada no
  puede tener retención a 90 días: poner un cero la hunde y hace creer que el producto se ha
  roto. El hueco se deja vacío y se espera.
- **Cambiar la definición de una métrica sin versionarla.** Si «usuario activo» pasa de contar
  sesiones a contar personas, el número salta de nivel y el equipo discute del gráfico en vez del
  negocio. Las definiciones van escritas, versionadas y con su dueño ([[contratos-de-datos]]).
- **Convertir la métrica en objetivo.** Cuando un número se convierte en la meta, se empieza a
  optimizar el número y no el problema: el tiempo en pantalla sube si el usuario no encuentra lo
  que busca, y la conversión sube si se esconden los gastos de envío. Los guardarraíles existen
  para eso, y hay que mirarlos antes de cantar la victoria.
- **Elegir los guardarraíles después del experimento.** Si los eliges cuando ya ves el resultado,
  siempre habrá una razón para quedarse con el que conviene. Se fijan antes, con su umbral, y se
  aceptan aunque la norte haya mejorado.
- **Decidir con un experimento sin potencia.** Un efecto del 1 % medido con 400 usuarios no es un
  efecto: es ruido con un intervalo de confianza que cruza el cero por los dos lados. Si el
  intervalo contiene el cero, la respuesta honesta es «no lo sé» ([[tamano-muestral]]).
- **Promediar segmentos que se mueven en direcciones opuestas.** La conversión media sube porque
  entra mucho tráfico de un país con conversión altísima, mientras la conversión baja en todos los
  demás. Es la paradoja de Simpson, y se evita mirando el desglose antes que la media.

## Comprueba que lo sabes

:::practica
enunciado: Un producto tiene 10.000 usuarios activos al mes, recibe 10.000 altas nuevas cada mes y solo el 20 % de los usuarios activos de un mes sigue activo al siguiente. Calcula la métrica agregada «activos de este mes sobre activos del mes pasado», el estado estacionario y qué pasa con la base si el abandono mejora al 15 %. Explica por qué la primera cifra engaña.
pista: La base del mes siguiente es los que repiten más las altas nuevas. El estado estacionario es altas entre abandono.
solucion: Activos del mes siguiente = 0,20 · 10.000 + 10.000 = 12.000, así que la métrica agregada es 12.000 / 10.000 = 120 %: parece que la retención es buenísima. Engaña porque el 80 % que se fue queda tapado por las 10.000 altas nuevas, que no tienen nada que ver con retener. El abandono real es del 80 % mensual, y el estado estacionario es 10.000 / 0,8 = 12.500 usuarios: la base no crecerá de ahí por muchas altas que se compren. Con un abandono del 15 %, el estado estacionario pasa a 10.000 / 0,15 = 66.667 usuarios, más de cinco veces la base actual. La conclusión práctica es que la palanca está en la retención: subir las altas un 20 % mueve la meseta un 20 %, y bajar el abandono del 80 % al 15 % la multiplica por cinco.
:::

:::quiz
p: El panel de producto enseña «activos este mes sobre activos del mes pasado» y marca 120 %. ¿Qué significa?
o: Que el producto retiene al 120 % de sus usuarios, lo cual es excelente
o: Que la base creció un 20 %, pero no dice nada de la retención: las altas nuevas tapan a los que se van
o: Que hay un error de cálculo, porque la retención nunca puede pasar del 100 %
a: 2
e: El cociente entre los activos de dos meses consecutivos es una medida de crecimiento de la base, no de retención: mezcla a los que repiten con los que acaban de llegar. Puede pasar del 100 % sin ninguna contradicción, y también puede quedarse en el 95 % mientras la retención por cohortes mejora. La retención de verdad se mide dentro de una cohorte, sobre los usuarios que entraron juntos.
:::

:::quiz
p: Con 4.000 altas al mes, ¿qué mueve más la base de usuarios estables: subir las altas un 20 % o bajar el abandono del 6 % al 5 %?
o: Subir las altas, porque actúa desde el primer mes
o: Las dos cosas dan la misma base estable, 80.000 usuarios, pero la retención se construye una vez y las altas se pagan todos los meses
o: Bajar el abandono, porque da 66.667 usuarios frente a 50.000
a: 2
e: El estado estacionario es altas entre abandono: 4.800 / 0,06 = 80.000 y 4.000 / 0,05 = 80.000. Las dos llegan al mismo sitio, con la diferencia de que las altas hay que comprarlas cada mes de forma indefinida y la mejora de retención se mantiene. La tercera opción confunde las cifras: 66.667 es la base con el abandono del 6 % sin tocar nada.
:::

:::quiz
p: Un experimento mejora la retención a 4 semanas con un intervalo de confianza de +0,4 a +3,2 puntos, pero la latencia del flujo de compra empeora un 15 % con un intervalo de +4 % a +20 %. ¿Qué se hace?
o: Lanzar, porque la métrica norte mejora y el intervalo no cruza el cero
o: No lanzar todavía: la mejora es real, pero el guardarraíl de latencia empeora y su intervalo tampoco cruza el cero
o: Lanzar y vigilar la latencia durante una semana
a: 2
e: Una mejora clara en la norte no compensa automáticamente un daño claro en un guardarraíl: los guardarraíles se fijan antes precisamente para que esa decisión no se negocie con el resultado delante. Aquí los dos intervalos excluyen el cero, así que ambos efectos son reales, y lo que toca es arreglar la latencia y volver a medir. Lanzar «y vigilar» es la forma habitual de quedarse con el daño.
:::

:::trampa
Optimizar la métrica en vez del problema. En cuanto un número se convierte en el objetivo del
equipo, alguien encuentra la forma de subirlo sin resolver nada: la conversión sube si se esconden
los gastos de envío hasta el último paso, el tiempo en pantalla sube si el usuario no encuentra lo
que busca, y la retención sube si se cuenta como activo abrir la aplicación. Mira siempre la
métrica con su guardarraíl y con el desglose por segmento antes de celebrar nada.
:::

:::nota
No hace falta medir todo. Un equipo con una métrica norte, dos o tres de entrada y dos
guardarraíles tiene una conversación mucho mejor que uno con cuarenta números en un panel: no
porque tenga menos información, sino porque sabe cuál mira cuando tiene que decidir
([[dashboards]]).
:::
