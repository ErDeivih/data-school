---
id: prueba-de-fondeo
titulo: Pruebas de fondeo
fase: 9
nivel: avanzado
rutas: [quant]
prerequisitos: [maximo-drawdown, riesgo-de-ruina, tamano-de-posicion, metricas-de-riesgo]
tags: [prop-firms, riesgo, evaluacion, drawdown]
resumen: Las reglas de una prueba de fondeo (objetivo, límite diario y drawdown máximo) convierten el trading en un problema de supervivencia donde manda el tamaño de posición.
fuentes: ["Van Tharp (2008), 'Trade Your Way to Financial Freedom'", "López de Prado (2018), 'Advances in Financial Machine Learning', cap. 15"]
---

## En una frase

Una prueba de fondeo es un examen con tres relojes a la vez: hay que llegar a un objetivo de
beneficio **antes** de tocar un límite de pérdida diaria y un drawdown máximo, y lo que decide
si apruebas no es tu idea sino el tamaño de cada operación.

## La idea

El planteamiento comercial es sencillo: pagas una cuota por operar una cuenta simulada de, por
ejemplo, 100.000 €. Si llegas a un objetivo de beneficio sin incumplir las reglas de pérdida, la
empresa te da una cuenta fondeada y reparte contigo los beneficios (el reparto habitual va del
70 % al 90 % según la empresa y el programa; algunos devuelven la cuota con el primer pago, otros
no). Los números exactos cambian de una empresa a otra y están en su reglamento, así que aquí
usamos un ejemplo concreto y razonamos con él: **objetivo del 6 %, límite de pérdida diaria del
3 %, drawdown máximo del 6 %** y un mínimo de días de operación.

Lo importante es la **asimetría**. El objetivo está a seis puntos por arriba y el suelo a seis
puntos por abajo, pero el reloj diario corta a tres. Y hay una regla que casi nadie lee con
atención: el drawdown suele ser **móvil** (*trailing*), es decir, el suelo sube con cada nuevo
máximo de la cuenta. Si vas ganando 4.000 € y luego pierdes 3.000 €, no estás a 1.000 € de
beneficio con 6.000 € de colchón: estás a 1.000 € de beneficio con el suelo a 6.000 € **por
debajo del máximo alcanzado**, así que solo te quedan 3.000 € de margen. Otra variante habitual
es que el límite diario se mida sobre el *equity* (incluyendo las posiciones abiertas) y no sobre
el beneficio cerrado: en ese caso, una pérdida flotante te puede sacar de la prueba sin que hayas
cerrado nada.

Con esas reglas, el problema deja de ser «ganar dinero» y pasa a ser **llegar antes de morir**.
Y aquí está el resultado que sorprende a casi todo el mundo: subir el riesgo por operación no
aumenta la probabilidad de aprobar. La primera mitad de la tabla de abajo lo consigue antes
(cuanto más riesgo, menos operaciones hacen falta para ganar 6.000 €), pero la segunda mitad se
muere por el camino: con un 1 % de riesgo, tres pérdidas en el mismo día agotan el límite diario
y la prueba se acaba. Con un 2 %, dos pérdidas seguidas en el mismo día bastan.

Por eso la pregunta correcta no es «¿cuánto puedo ganar?», sino «¿cuántas pérdidas seguidas
aguanto en un día, cuántas desde el máximo, y mi sistema produce rachas de esa longitud con
normalidad?». Eso conecta directamente con [[riesgo-de-ruina]] y con [[maximo-drawdown]]: las
rachas no son mala suerte, son la forma que tiene el azar de repartirse.

Dos advertencias antes de seguir. La primera: la prueba mide una muestra corta, así que aprobar
o suspender tiene mucho de azar; el error caro es repetir el intento cambiando de estrategia
cuando lo que estaba mal era el tamaño. La segunda: hay reglas de consistencia (por ejemplo, que
ningún día aporte más de cierto porcentaje del beneficio total) que impiden aprobar con dos
operaciones afortunadas, y reglas de conducta (noticias, alta frecuencia, operar en ciertos
horarios) que pueden invalidar el resultado aunque llegues al objetivo. Léelas antes de pagar.

## Definición formal

Sea `C` el capital nominal de la evaluación y `ρ` el riesgo por operación como fracción de `C`.

- `T = t · C` — objetivo de beneficio, con `t` la fracción objetivo (0,06 en el ejemplo).
- `L = ℓ · C` — límite de pérdida diaria, con `ℓ` la fracción diaria (0,03).
- `D = d · C` — pérdida máxima total, con `d` la fracción (0,06). Si el drawdown es móvil, se mide
  desde el máximo de equity alcanzado; si es estático, desde el capital inicial.
- `ρ · C` — pérdida si la operación sale mal; la ganancia es `R · ρ · C`, con `R` el ratio de
  beneficio/pérdida (2 en el ejemplo: se gana el doble de lo que se arriesga).
- `p` — proporción de operaciones ganadoras (0,45 en el ejemplo).
- **Esperanza por operación:** `E = ρ · C · (p · R − (1 − p))`. Con `p = 0,45` y `R = 2` queda
  `E = 0,35 · ρ · C`.
- **Operaciones esperadas hasta el objetivo:** `T / E`, suponiendo que las reglas de pérdida no
  actúan. Es la parte «cuánto tardo».
- **Pérdidas seguidas que caben en el límite diario:** `⌊L / (ρ · C)⌋`. La siguiente ya lo
  incumple. Es la parte «cuánto aguanto».
- **Pérdidas seguidas que caben desde el máximo:** `⌊D / (ρ · C)⌋`, con la misma lectura.
- **Probabilidad de aprobar:** la probabilidad de que la trayectoria de la cuenta alcance `+T`
  antes de tocar `−D` (desde el máximo) y sin sufrir un día peor que `−L`. No hay fórmula cerrada
  en general: se estima por simulación o resolviendo la cadena de Markov del proceso.

De ahí salen las dos cuentas que hay que mirar siempre juntas:

:::formula
E = ρ · C · (p · R − (1 − p))   y   operaciones al objetivo ≈ T / E
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `C` | Capital nominal de la evaluación | € (100.000 en el ejemplo) | Todo se mide en proporción a él: los límites en euros suben, el problema es el mismo |
| `ρ` | Riesgo por operación, como fracción de `C` | tanto por uno | Llegas antes al objetivo y aguantas menos pérdidas seguidas: es el intercambio que decide la prueba |
| `t` | Objetivo de beneficio, como fracción de `C` | tanto por uno (0,06) | Hacen falta más operaciones para aprobar, con el mismo riesgo de morir por el camino |
| `ℓ` | Límite de pérdida diaria, como fracción de `C` | tanto por uno (0,03) | Cabe una racha más larga dentro del mismo día antes de incumplir |
| `d` | Drawdown máximo, como fracción de `C` | tanto por uno (0,06) | Más margen desde el máximo, pero un beneficio no consolidado sigue sin ser tuyo si el suelo es móvil |
| `p` | Proporción de operaciones ganadoras | tanto por uno (0,45) | Sube la esperanza por operación y bajan las rachas de pérdidas |
| `R` | Ratio beneficio/pérdida de cada operación | adimensional (2) | Sube la esperanza y hace falta menos tiempo, sin tocar el riesgo |
| `E` | Esperanza de beneficio por operación | € por operación | Con `E` más alto, `T / E` baja: tardas menos, pero los límites no se mueven |
:::

La primera dice cuánto ganas de media por operación; la segunda, cuánto tardas en llegar al
objetivo si nada te para. Pero el riesgo por operación también fija cuántas pérdidas aguantas:
`⌊L / (ρ · C)⌋` en un día y `⌊D / (ρ · C)⌋` desde el máximo, y la siguiente pérdida de cada
cuenta ya rompe la regla. Subir `ρ` reduce las operaciones que necesitas para llegar y reduce
también, en la misma proporción, las pérdidas que puedes encadenar. Ese es el intercambio que
decide la prueba, y el riesgo tiene que ser **pequeño frente a los límites**, no frente al
objetivo.

:::figura
fichero: prueba-fondeo-riesgo-y-muerte
pie: A la izquierda, la probabilidad de cada final según el riesgo por operación, con 1.500 intentos simulados por punto y las reglas del ejemplo. Con un riesgo diminuto se aprueba casi siempre, pero hacen falta unas 60 operaciones; a partir del 1 % el límite diario se lleva por delante a más de la mitad de los intentos, y subir el riesgo ya no compra probabilidad de aprobar. Morir por el drawdown total solo ocurre con riesgo pequeño, porque con riesgo grande el reloj diario corta antes. A la derecha, quince intentos reales con un 1 % de riesgo, parados en el momento en que se deciden: en verde los que llegan al objetivo, en rojo los que mueren por tres pérdidas en el mismo día.
fuente: figuras/prueba-de-fondeo-1.py
:::

## Ejemplo

Con `C = 100.000 €`, `t = 6 %`, `ℓ = 3 %`, `d = 6 %`, `p = 0,45` y `R = 2`:

| Riesgo por operación | Pérdida por operación | Operaciones al objetivo | Pérdidas que caben en el día | Pérdidas que caben desde el máximo |
| --- | --- | --- | --- | --- |
| 0,5 % | 500 € | 34,3 | 6 | 12 |
| 1,0 % | 1.000 € | 17,1 | 3 | 6 |
| 2,0 % | 2.000 € | 8,6 | 1 | 3 |

La tercera columna invita a subir el riesgo: con un 2 % el objetivo está a menos de nueve
operaciones. Las dos últimas columnas explican por qué eso es una trampa. Y la simulación de
2.000 trayectorias con las mismas reglas (tres operaciones al día, sin costes, sin límite de
tiempo) lo confirma:

| Riesgo | Aprueba | Muere por el límite diario | Muere por el drawdown total | Operaciones hasta aprobar (mediana) |
| --- | --- | --- | --- | --- |
| 0,25 % | 99,7 % | 0,0 % | 0,4 % | 63 |
| 0,50 % | 94,3 % | 0,0 % | 5,7 % | 27 |
| 1,00 % | 56,5 % | 43,5 % | 0,0 % | 8 |
| 2,00 % | 55,4 % | 34,1 % | 10,5 % | 3 |
| 3,00 % | 45,6 % | 54,4 % | 0,0 % | 1 |

La lectura, en tres frases. Con riesgo muy pequeño casi todo el mundo aprueba, pero hace falta
tiempo: 63 operaciones de mediana, que con tres al día son unas tres semanas. Con riesgo alto la
prueba se decide en un puñado de operaciones y la mayoría de las veces se decide en contra: el
límite diario se lleva por delante a más de la mitad de los intentos. Y el óptimo no está en
ninguno de los extremos: está en el riesgo más alto que todavía deja margen para la racha que tu
sistema produce de forma habitual.

## Código

```python verificable
# La aritmetica de las reglas, antes de simular nada.
C = 100000.0
objetivo, limite_diario, perdida_max = 6000.0, 3000.0, 6000.0   # 6 %, 3 % y 6 %
p, R = 0.45, 2.0                                               # 45 % de acierto, gana el doble

for riesgo in (0.005, 0.01, 0.02):
    r = riesgo * C
    esperanza = r * (p * R - (1 - p))          # ganancia media por operacion
    print(f"riesgo {riesgo:.1%}: {r:>6.0f} EUR  esperanza {esperanza:>6.1f} EUR/op  "
          f"ops al objetivo {objetivo / esperanza:>5.1f}  "
          f"perdidas que caben al dia {limite_diario // r:.0f}  desde el maximo {perdida_max // r:.0f}")
```

:::claves
- `limite_diario // r` es una división **entera**: con 3.000 € de límite y 1.000 € por pérdida devuelve 3, que son las pérdidas que caben. Si usaras `/` tendrías 3,0 y no verías el caso importante: con 1.100 € por operación caben 2 (el `//` da 2, aunque 2,7 pérdidas parezcan caber).
- El formato `.1%` multiplica por 100 y añade el signo de porcentaje: `f"{0.005:.1%}"` imprime `0.5%`. No lo confundas con `.1f`, que imprimiría `0.0`. Y ojo al pasar esos números a la prosa del portal, donde se escriben «0,5 %»: la coma y el espacio son cosa del texto, no del código.
- El generador propio (`uniformes`) devuelve los mismos números siempre, pero **consume estado**: si llamas dos veces a `simular` sin reiniciarlo, la segunda simulación es distinta de la primera. Para reproducir hay que crear uno nuevo en cada llamada, como hace la función.
- `pico - cap >= perdida_max` se comprueba **antes** de actualizar `pico`, así que el máximo del día en curso no cuenta: es el orden del original y cambiar esas dos líneas de sitio cambia los resultados en el caso límite (una cuenta que sube y baja dentro de la misma operación).
- `ops_hoy == ops_dia` reinicia el día **después** de operar: el día 1 son las operaciones 1, 2 y 3. Si el contador se reiniciara antes, el límite diario se mediría desde un equity distinto y la tasa de muertes por el reloj diario cambiaría.
:::

```python verificable
# Simulacion de la prueba completa: objetivo, limite diario y drawdown movil.
def uniformes(semilla=987654321):
    x = semilla
    while True:                                # generador propio: deterministico y sin version
        x = (1103515245 * x + 12345) % (2 ** 31)
        yield x / 2 ** 31

def simular(riesgo, n_sim=2000, ops_dia=3, capital=100000.0,
            objetivo=6000.0, limite_diario=3000.0, perdida_max=6000.0, max_ops=400):
    azar = uniformes()
    aprueba = muere_dia = muere_total = 0
    ops_hasta = []
    for _ in range(n_sim):
        cap = pico = dia = capital
        ops = ops_hoy = 0
        while True:
            r = capital * riesgo
            cap += 2 * r if next(azar) < 0.45 else -r
            ops += 1
            ops_hoy += 1
            if cap - capital >= objetivo:              # exito
                aprueba += 1
                ops_hasta.append(ops)
                break
            if dia - cap >= limite_diario:             # el reloj diario corta
                muere_dia += 1
                break
            if pico - cap >= perdida_max:              # drawdown movil desde el maximo
                muere_total += 1
                break
            pico = max(pico, cap)
            if ops_hoy == ops_dia:                     # empieza un dia nuevo
                dia = cap
                ops_hoy = 0
            if ops >= max_ops:
                break
    mediana = sorted(ops_hasta)[len(ops_hasta) // 2]
    return aprueba / n_sim, muere_dia / n_sim, muere_total / n_sim, mediana

print("riesgo  aprueba  muere dia  muere total  mediana ops")
for riesgo in (0.0025, 0.005, 0.01, 0.02, 0.03):
    aprueba, dia, total, mediana = simular(riesgo)
    print(f"{riesgo:>6.2%}  {aprueba:>7.1%}  {dia:>9.1%}  {total:>11.1%}  {mediana:>11}")
```

## Errores típicos

- **Confundir el límite diario con el drawdown total.** Son dos relojes distintos: uno se
  reinicia cada día y el otro no. Muchos intentos mueren por el diario con la cuenta en positivo:
  tres pérdidas en una mañana y se acabó, aunque el total esté intacto.
- **Ignorar que el drawdown es móvil.** Si el suelo sube con cada nuevo máximo, un beneficio que
  no has «cerrado» no es tuyo: una corrección normal desde el máximo te saca. Calcula el margen
  desde el máximo alcanzado, no desde el capital inicial.
- **Subir el riesgo por operación para llegar antes al objetivo.** Los números de la tabla lo
  desmienten: con un 1 %, tres pérdidas seguidas en el día agotan el límite; con un 3 %, una
  sola pérdida deja la prueba al borde. El riesgo alto no compra probabilidad de aprobar, compra
  velocidad a cambio de supervivencia.
- **Dejar posiciones abiertas con pérdida flotante.** Si el reglamento mide el límite sobre el
  equity, el margen no lo decide tu beneficio cerrado sino el peor momento del día. Cerrar más
  tarde no te salva de haberlo incumplido.
- **Operar después de tocar el objetivo para «asegurar margen».** Casi todos los programas tienen
  reglas de consistencia y de días mínimos: un día demasiado bueno respecto al total puede
  invalidar el intento, y seguir operando solo añade riesgo de tocar el suelo.
- **Tratarlo como un problema de suerte y repetir el intento sin cambiar el tamaño.** Si tu
  sistema produce rachas de cinco pérdidas con normalidad y tu riesgo hace que cuatro te saquen,
  el problema no es la estrategia: es el dimensionado, que se estudia en [[tamano-de-posicion]],
  [[criterio-de-kelly]] y [[riesgo-de-ruina]].

:::practica
enunciado: Con una cuenta de 100.000 €, objetivo del 6 %, límite diario del 3 % y drawdown móvil del 6 %, se arriesgan 800 € por operación. La cuenta llegó a un máximo de 104.800 € y está en 101.600 €. Calcula el suelo, el margen, las pérdidas seguidas que caben y si dos pérdidas en un día tocan el límite diario.
pista: El suelo se mide desde el máximo alcanzado, no desde el capital inicial.
solucion: Suelo = 104.800 − 6.000 = 98.800 €; margen = 101.600 − 98.800 = 2.800 €. Con 800 € por pérdida caben 2.800 / 800 = 3 (2.400 €); la cuarta lo incumpliría. El límite diario es 3.000 €: dos pérdidas son 1.600 € y no lo tocan, cuatro lo romperían. Conclusión: quedan tres pérdidas de margen y el tamaño de posición es lo que decide.
:::

## Comprueba que lo sabes

:::quiz
p: Con una cuenta de 100.000 €, límite diario de 3.000 € y 1.000 € de riesgo por operación, ¿cuántas pérdidas seguidas en el mismo día hacen fracasar la prueba?
o: Tres, porque 3 · 1.000 = 3.000 y agota el límite
o: Seis, porque el límite diario es la mitad del drawdown total
o: Ninguna: el límite diario solo cuenta las operaciones cerradas en pérdida neta
a: 1
e: El límite diario es de 3.000 € y cada pérdida son 1.000 €, así que tres pérdidas seguidas en el mismo día lo agotan. Seis pérdidas es lo que cabe en el drawdown total del 6 %. El detalle de si cuenta el flotante o solo lo cerrado depende del reglamento, pero el límite no se mide en pérdida neta.
:::

:::quiz
p: ¿Por qué subir el riesgo por operación no aumenta necesariamente la probabilidad de aprobar una prueba de fondeo?
o: Porque los límites de pérdida (diario y total) se alcanzan antes cuando cada operación arriesga más, y la racha de pérdidas es inevitable
o: Porque las empresas penalizan el riesgo alto con comisiones mayores
o: Porque el objetivo de beneficio se recalcula cuando arriesgas más
a: 1
e: El objetivo se alcanza en menos operaciones, pero el número de pérdidas seguidas que caben en el límite diario baja de seis a tres y a una. Como las rachas son la forma normal en que se reparte el azar, la probabilidad de morir antes de llegar crece más deprisa que la de aprobar: en la simulación, pasar del 0,25 % al 3 % baja la tasa de aprobados del 99,7 % al 45,6 %.
:::

:::quiz
p: ¿Qué significa que el drawdown máximo sea móvil (trailing)?
o: Que se mide solo durante la sesión de negociación
o: Que el suelo de pérdida sube con cada nuevo máximo de la cuenta, así que el margen se calcula desde el máximo alcanzado
o: Que se recalcula una vez al mes con la volatilidad realizada
a: 2
e: Móvil significa que el suelo acompaña al máximo: si la cuenta sube 4.000 € y luego baja 3.000 €, el margen que queda es el drawdown menos la caída desde el máximo, no el beneficio acumulado. Con un suelo estático, en cambio, el margen siempre se mide desde el capital inicial.
:::

:::aviso
Los números de esta página son un ejemplo con reglas concretas (objetivo 6 %, límite diario 3 %,
drawdown 6 %, móvil) y una simulación con supuestos fuertes: operaciones independientes con un
45 % de acierto y un ratio 2:1, sin costes, sin deslizamiento y sin límite de tiempo. Cada
programa tiene su reglamento y sus condiciones, y el resultado de una prueba concreta depende de
mucho más que de estas cuentas. Úsalo para razonar sobre el tamaño de posición, no como promesa
de nada.
:::
