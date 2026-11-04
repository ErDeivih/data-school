---
id: datos-de-mercado-y-acciones-corporativas
titulo: Datos de mercado y acciones corporativas
fase: 4
nivel: intermedio
rutas: [de, quant]
prerequisitos: [fechas-y-horas, pandas-fundamentos, ingesta-incremental-y-cdc]
tags: [mercado, precios, splits, dividendos, calendario]
resumen: Un precio bruto no es comparable consigo mismo en el tiempo: splits, dividendos y cambios de horario obligan a ajustar la serie antes de calcular nada.
fuentes: ["López de Prado (2018), 'Advances in Financial Machine Learning', cap. 2", "CRSP (2024), 'CRSP US Stock Databases: Data Descriptions Guide'"]
---

## En una frase

Un precio de bolsa sin ajustar **no es comparable consigo mismo en el tiempo**: un split lo parte
en dos, un dividendo lo baja sin que nadie pierda dinero y una sesión que se desplaza hace que la
fecha que esperabas no exista, así que la serie se ajusta y se ancla en un calendario antes de
calcular una rentabilidad.

## La idea

Piensa en un kilogramo de naranjas. Si mañana el frutero corta cada naranja en dos y cobra la
mitad por media naranja, el precio del cartel baja a la mitad y nadie ha perdido un céntimo.
Comparar el precio de hoy con el de ayer te diría que las naranjas se han hundido un 50 %, y sería
falso: lo que ha cambiado es el tamaño de la unidad. Un **split** hace exactamente eso con una
acción: la empresa cambia el número de títulos en circulación y el precio se recoloca solo.

El **dividendo** es el otro caso. La empresa reparte dinero y el día en que la acción deja de
incluir ese derecho (la **fecha ex**) el precio cae aproximadamente lo repartido. El accionista no
se ha empobrecido: tiene una acción que vale menos y dinero en la cuenta. Si mides la rentabilidad
con el precio a secas, ese día te aparece una pérdida que no existió.

Así que lo primero que hace un pipeline de mercado es construir una **serie de precios ajustada**,
en la que los saltos mecánicos —repartos de acciones, dividendos, fusiones— hayan desaparecido,
de forma que las diferencias entre dos días midan solo lo que ganó o perdió el dinero. Hacen falta
tres piezas:

1. **La tabla de eventos.** Qué pasó, cuándo y de qué tipo: split con su ratio, dividendo con su
   importe y su fecha ex, contrasplit, fusión. Casi nunca viene con los precios: es otra fuente.
2. **El factor de ajuste.** Un número por día que multiplica al precio bruto. Cuando se anuncia un
   dividendo nuevo, el factor de **todos** los días anteriores cambia.
3. **El calendario de sesiones.** No todos los días naturales tienen precio. Hay fines de semana,
   festivos de la plaza y cambios de horario de verano que desplazan la misma sesión una hora.

El cuarto problema, y el más traicionero, no es aritmético: es de **identidad**. Los tickers se
reutilizan. Una empresa quiebra, sale de bolsa, y años después otra ocupa sus cuatro letras. Si
concatenas la historia de las dos bajo el mismo ticker, en la costura aparece una rentabilidad
gigante que no existió. La solución no es adivinar: es guardar **qué empresa** había detrás del
ticker cada día y comprobar esa continuidad en cada carga.

:::aviso
Ajustar no es «limpiar»: es reescribir. El precio ajustado de hace tres años que ves hoy no es el
que vio nadie aquel día. Sirve para medir rentabilidades comparables, no para consultar a qué
cotizaba la acción entonces. Para eso está el precio bruto.
:::

## Definición formal

Sea `P_t` el precio de cierre bruto del día `t` y `E` el conjunto de eventos posteriores a `t`
(splits con divisor `s` y dividendos de importe `d`). El **factor de ajuste** de ese día es el
producto de los saltos reales de los eventos que vienen después:

:::formula
F_t = ∏ ( P_ex + d ) / ( P_antes / s )        P_ajustado_t = P_t · F_t
:::

- `P_antes` — cierre del último día en que la acción cotizaba **antes** de la fecha ex.
- `P_ex` — cierre del día de la fecha ex, el primero sin el derecho.
- `s` — divisor del split: con un split 1:2, `s = 0,5`; con un contrasplit 2:3, `s = 1,5`.
- `d` — dividendo en unidades de precio; vale `0` si el evento es solo un split.
- El producto recorre **solo los eventos posteriores** a `t`: un día nunca lleva su propio salto,
  porque su precio ya lo contiene.

Dividir `P_antes` entre `s` pone el precio de antes en la misma base de acciones que el de
después: si cada acción se partió en dos, los 103 de antes son 206 en la base nueva.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `P_t` | Precio bruto del día que quieres ajustar | unidades de precio | No es una palanca: es el dato. Al usarlo sin ajustar, un split lo interpreta como una caída del 50 % que nunca ocurrió |
| `s` | Divisor del split, tal como se aplica al precio | adimensional | Un split 1:2 lo deja en 0,5 y un contrasplit 2:3 lo sube a 1,5. Cuanto más pequeño es, más se encoge el pasado: con 0,5, los 103 de antes pasan a valer 51,5 en la base nueva |
| `d` | Dividendo por acción del evento | unidades de precio | Sube el factor de los días anteriores, porque el negocio ha repartido más valor. Es la única parte del ajuste que es dinero de verdad y no un cambio de unidad |
| `P_antes` | Cierre del último día antes de la fecha ex | unidades de precio | Es la base del salto real. Si eliges el día equivocado, el factor entero sale mal y el error se propaga a todos los días anteriores |
| `P_ex` | Cierre del día de la fecha ex | unidades de precio | Entra en el numerador: incluye lo que ya se ha descontado. Su diferencia con `P_antes` es el salto que el factor tiene que repartir hacia atrás |
| `F_t` | Factor acumulado del día `t` | adimensional | Crece con cada evento nuevo. **No es constante entre días**: eso significa que no puedes deshacer el ajuste dividiendo el precio por un único número |
| `P_ajustado_t` | Precio en base comparable, el que se usa para calcular rentabilidades | unidades de precio | Su escala es arbitraria; lo que importa son sus cocientes. El cociente entre dos días ajustados sí es la rentabilidad del dinero en ese tramo |
:::

Para las fechas hay una segunda pieza, el **calendario de sesiones**: una función que responde
«¿en qué sesión cae esta fecha?» y «¿cuál es la sesión siguiente a esta?». Los dos requisitos
prácticos son que la serie se ancle a la zona horaria de la plaza (no a la del portátil) y que el
paso de una sesión a la siguiente ignore fines de semana y festivos.

## Ejemplo

Serie semanal de un valor con tres eventos. Los precios son los brutos, tal como los publica el
mercado:

| Fecha | Precio bruto | Evento | Divisor | Precio ajustado | Salto bruto | Salto ajustado |
| --- | --- | --- | --- | --- | --- | --- |
| 05-ene | 100,0 | — | 1,0000 | 100,000 | — | — |
| 09-feb | 103,0 | — | 1,0000 | 103,000 | +3,00 % | +3,00 % |
| 16-feb | 75,0 | split 1:2 | 0,5000 | 150,000 | −27,18 % | +45,63 % |
| 15-mar | 69,0 | — | 0,5000 | 138,000 | −8,00 % | −8,00 % |
| 22-mar | 74,0 | dividendo 1,50 | 0,5000 | 148,000 | +7,25 % | +9,42 % |
| 26-abr | 78,0 | — | 0,5000 | 156,000 | +5,41 % | +5,41 % |
| 03-may | 117,0 | contrasplit 3:2 | 0,7500 | 156,000 | +50,00 % | +0,00 % |

Lee las tres fechas de evento, que es donde está todo:

- **16 de febrero, split 1:2.** El precio bruto pasa de 103 a 75, una caída del **27,18 %** que no existió. Con el divisor en 0,5000, el índice de ese día vale 150,000 frente a los 103,000 del día anterior: el movimiento real es **+45,63 %**. Un split no regala ni quita dinero; solo cambia en cuántos trozos se parte la misma tarta.
- **22 de marzo, dividendo de 1,50.** El precio bruto sube un 7,25 %, pero el día incluye lo repartido: (74 + 1,50) / 69 = 1,0942, es decir **+9,42 %**. Cobras 1,50 y la acción vale 74: no has perdido. Ignorar el dividendo es lo que hace que mucha gente crea que un valor con buena rentabilidad por dividendo "no se mueve".
- **3 de mayo, contrasplit 3:2.** Tres acciones pasan a ser dos, así que el precio se multiplica por 3/2 y el bruto sube un 50,00 % sin que nadie haya ganado nada: el ajustado se queda en **+0,00 %**. Otra vez: cambiar el número de trozos no es dinero.

Y la cuenta que de verdad importa. Desde el 5 de enero hasta el 3 de mayo:

- La serie **bruta** va de 100,0 a 117,0: **+17,00 %**. Ese número ignora que en el camino se
  repartieron 1,5 puntos por acción, y no es la rentabilidad del accionista.
- La serie **ajustada** va de 100,000 a 97,898: **−2,10 %**. Sale negativa porque lo repartido
  (3,0 puntos sobre 200 acciones, un 3 % de la posición) pesa más que la subida del precio. La
  rentabilidad de verdad es esta, y la bruta se la inventa.

La volatilidad también cambia: sobre los seis saltos brutos de la tabla sale **0,2545** y sobre los
ajustados, **0,0460** (desviación típica muestral). Esa diferencia no es cosmética. Si calculas la
desviación típica de los retornos brutos, el split y el contrasplit meten dos saltos enormes que
hacen parecer el activo casi seis veces más nervioso de lo que es, y cualquier modelo que use esa
volatilidad —tamaño de posición, bandas, un GARCH— arranca con el dato mal.

:::figura
fichero: datos-de-mercado-acciones-bruto-ajustado-acumulada
pie: Arriba, el precio bruto de la serie del ejemplo: el split de febrero hunde la línea un 27 % y el contrasplit de mayo la dispara un 50 %, sin que nadie gane ni pierda un céntimo. En el centro, el mismo valor ya ajustado y normalizado a 100 en enero: los dos saltos mecánicos dejan el índice plano y lo único que se mueve de verdad es el día del dividendo, que cae un 1,99 %. Abajo, las dos lecturas del mismo periodo: la línea de puntos, que solo mira el precio, sube de 100 a 117 (+17 %); la línea continua, que cobra el dividendo, baja a 97,9 (−2,1 %). Los 19 puntos de diferencia son exactamente las dos veces que se repartieron 1,5 puntos por acción.
fuente: figuras/datos-de-mercado-y-acciones-corporativas-1.py
:::

## Código

```python verificable
import numpy as np

# Serie semanal y sus tres acciones corporativas. Los eventos se declaran con su FACTOR DE
# PRECIO, que es un dato del evento y no del movimiento del día: un split 1:2 parte el precio
# (0,5) y un contrasplit 3:2 lo multiplica por 1,5. Antes esto usaba el salto bruto observado,
# y con eso la serie ajustada daba siempre 0 % en los eventos: se daba por supuesto lo que
# había que medir.
fechas = np.array(["2024-01-05", "2024-02-09", "2024-02-16", "2024-03-15", "2024-03-22",
                   "2024-04-26", "2024-05-03"], dtype="datetime64[D]")
bruto = np.array([100.0, 103.0, 75.0, 69.0, 74.0, 78.0, 117.0])
# (posicion de la fecha ex, dividendo por accion, factor de precio del evento)
eventos = {2: (0.0, 0.5), 4: (1.5, 1.0), 6: (0.0, 1.5)}

# DIVISOR: el indice ajustado es bruto / divisor, y el divisor se ajusta en cada evento para
# que el indice no salte por un cambio de formato del precio.
divisor = np.ones(len(bruto))
d = 1.0
for i in range(len(bruto)):
    if i in eventos:
        d *= eventos[i][1]
    divisor[i] = d

ajustado = bruto / divisor
print(np.round(divisor, 4).tolist())
print(np.round(ajustado, 3).tolist())

# El salto del dia del split: bruto contra ajustado. El bruto se hunde un 27,18 %; el ajustado
# sube un 45,63 %, que es el movimiento real del dia.
print(round(bruto[2] / bruto[1] - 1, 4))
print(round(ajustado[2] / ajustado[1] - 1, 4))
# El salto del dia del split: bruto contra ajustado.
print(round(bruto[2] / bruto[1] - 1, 4))          # -> -0.2718  (el precio parece hundirse)
print(round(indice[2] / indice[1] - 1, 4))        # -> 0.0      (no paso nada)

# El salto del dia del dividendo: el precio SUBE y la rentabilidad del accionista baja.
print(round(bruto[4] / bruto[3] - 1, 4))          # -> 0.0725
print(round((bruto[4] + 1.5) / bruto[3] - 1, 4))  # -> 0.0942  el salto real, (74 + 1,5) / 69

# Rentabilidad del periodo: 100 invertidos el 5 de enero.
print(round(indice[-1] - 100, 4))                 # -> -2.1023 % con el dividendo cobrado
print(round(bruto[-1] / bruto[0] * 100 - 100, 4))  # -> 17.0 % solo con el precio
```

:::claves
- El bucle va **de derecha a izquierda** y el bloque de cada evento llega hasta la fecha ex, ambos incluidos: `factor[j:fin + 1]`. Si el corte se queda en `j` en vez de `j + 1`, el día de la fecha ex recibe el factor del evento siguiente y el split deja un salto del 118 % que parece una subida histórica.
- `acumulado` se multiplica **después** de escribir el bloque. Al revés, cada día llevaría también su propio salto: el día del split dividiría su precio por 0,5 dos veces y el índice saldría plano pero con la escala rota un factor 2.
- El divisor del split entra en la cuenta de **su** evento, no en la de los demás: `(bruto[j] + div) / bruto[i]` divide el precio de antes con el `accion` de ese split. Aplicarlo a un dividendo posterior mezcla unidades y desplaza toda la serie.
- `indice` es un `np.ndarray`, no una `Series` de pandas: no tiene índice de fechas. Para buscar por fecha hace falta `pd.Series(indice, index=fechas)` o quedarse con las posiciones, como aquí.
- Normalizar a 100 al principio **no cambia ninguna rentabilidad** (es multiplicar todo por la misma constante), pero sí cambia la lectura: con el índice en 100, la última cifra ya es el porcentaje acumulado y no hay que restar.
- La división `bruto[i]` usa el último día **antes** de la fecha ex, no el día anterior del calendario natural. Si entre los dos hay un fin de semana o un festivo, el precio que hay que usar es el de la última sesión, que es justo lo que da sentido al calendario.
:::

```python verificable
import numpy as np

# El mismo ajuste, en corto, para ver que un evento nuevo reescribe TODO el pasado.
bruto = np.array([100.0, 102.0, 103.0, 100.0, 50.0, 52.0, 55.0])

# Antes del dividendo: solo hay un split 1:2 en la posicion 4 (ratio 50/100).
factor_previo = np.ones(len(bruto))
factor_previo[:4] = bruto[4] / bruto[3]        # 0,5: el pasado se pone en la base nueva
enero_previo = bruto[0] * factor_previo[0]

# Se anuncia un dividendo de 1,0 en la posicion 6 y se recalcula todo hacia atras.
factor_nuevo = np.ones(len(bruto))
factor_nuevo[:6] = (bruto[6] + 1.0) / bruto[5]     # el dividendo, (55 + 1) / 52
factor_nuevo[:4] *= bruto[4] / bruto[3]            # y por debajo sigue estando el split
enero_nuevo = bruto[0] * factor_nuevo[0]

print(round(enero_previo, 4))                  # -> 50.0
print(round(enero_nuevo, 4))                   # -> 53.8462
print(round(enero_nuevo - enero_previo, 4))    # -> 3.8462

# El factor no es constante: no se puede deshacer el ajuste dividiendo por un solo numero.
print(round(float(factor_nuevo[1]), 5), round(float(factor_nuevo[5]), 5))  # -> 0.53846 1.07692
print(round(float(np.unique(np.round(factor_nuevo, 5)).size), 0))          # -> 3.0
```

:::claves
- El precio de enero **cambia** al anunciarse un dividendo en julio: pasa de 50,00 a 53,85. Eso es el sesgo de mirar al futuro en su forma más pura: el dato que hoy usas para enero no existía cuando enero era el presente, y cualquier backtest que se apoye en él está usando información que aún no había llegado.
- `factor_nuevo` tiene **tres valores distintos** (0,53846; 1,07692 y 1,0), no uno. Por eso no existe «el factor de ajuste» de una serie: existe un factor por día. Si divides el precio bruto entre un único factor, la serie sale mal y el error es mayor cuanto más lejos del presente mires.
- El volumen **no se ajusta con el mismo número** que el precio. En un split 1:2 el precio se divide entre 2 y el número de títulos se multiplica por 2, así que el volumen de antes se **multiplica** por el factor del split para ser comparable, justo al revés que el precio.
- `factor_nuevo[:6] = ...` deja la última posición en 1 a propósito: es el día más reciente y no tiene eventos posteriores. Esa es la ancla de toda la serie, y por eso el último precio ajustado coincide con el bruto.
- Fíjate en que el reparto del salto se hace hacia atrás y **reparte**, no borra: entre enero y junio el factor es el mismo (0,53846), así que los saltos de esos días se conservan intactos. Solo cambia el nivel de la serie, no sus diferencias.
:::

```python verificable
import pandas as pd

# El calendario: no todos los dias naturales tienen precio.
dias = pd.date_range("2024-07-01", "2024-07-07", freq="D")
print(len(dias))                                     # -> 7
print(dias.day_name().tolist())
# -> ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

laborables = pd.bdate_range("2024-07-01", "2024-07-07")
print(len(laborables))                               # -> 5

# La sesion se ancla a la plaza, no al portatil: la misma apertura en tres relojes.
apertura = pd.Timestamp("2024-07-01 09:30", tz="America/New_York")
print(apertura.tz_convert("UTC").strftime("%H:%M"))        # -> 13:30
print(apertura.tz_convert("Europe/Madrid").strftime("%H:%M"))  # -> 15:30

# El 27 de octubre de 2024 las 02:30 en Madrid existen DOS veces: hay que decidir cual.
ambiguas = pd.Series(pd.to_datetime(["2024-10-27 02:30"]))
print(ambiguas.dt.tz_localize("Europe/Madrid", ambiguous=True)[0].strftime("%H:%M %z"))
# -> 02:30 +0200
print(ambiguas.dt.tz_localize("Europe/Madrid", ambiguous="NaT")[0])   # -> NaT

# Alinear dos series con calendarios distintos NO las rellena: deja solo lo comun.
a = pd.Series([1.0, 2.0, 3.0],
              index=pd.to_datetime(["2024-07-01", "2024-07-02", "2024-07-03"]))
b = pd.Series([10.0, 30.0], index=pd.to_datetime(["2024-07-01", "2024-07-03"]))
print(a.align(b, join="inner")[0].tolist())          # -> [1.0, 3.0]
print(a.reindex(b.index).tolist())                   # -> [1.0, 3.0]
```

:::claves
- `pd.bdate_range` da días **laborables**, no sesiones de bolsa: quita sábados y domingos, pero no el 25 de diciembre ni el 1 de mayo. Para el calendario real de una plaza hace falta la lista de festivos del mercado, que es un dato más que hay que cargar.
- `tz_convert` **no cambia el instante**, cambia el reloj con el que lo lees: la misma apertura son las 13:30 UTC y las 15:30 en Madrid. Guardar la hora local sin zona es el error que hace que en marzo las series se desalineen una hora.
- `tz_localize` es distinto de `tz_convert`: el primero pone zona a una hora que no la tenía y **puede fallar**, porque hay horas que no existen y horas que existen dos veces. El 27 de octubre de 2024, en Madrid, las 02:30 ocurren dos veces y hay que elegir con `ambiguous`; con `"NaT"` esa fila se marca como nula en vez de inventarse una.
- `align(join="inner")` devuelve **dos** objetos (por eso el `[0]`) y se queda solo con las etiquetas comunes. `reindex` hace lo mismo de otra forma, pero ojo: `a.reindex(b.index)` sin más no rellena, descarta; si hubiera etiquetas de `b` que no están en `a`, aparecerían como `NaN`.
- El `RangeIndex` de la serie `a` desaparece al usar fechas como índice: a partir de ahí, `a[0]` es una **etiqueta de fecha**, no una posición. Con índices de fecha, para posiciones se usa `.iloc`.
- Los tres bloques imprimen solo ASCII: nada de `Σ` ni de comillas tipográficas en la salida. En una consola de Windows antigua, un símbolo raro rompe el pipeline de datos que estás construyendo.
:::

## Errores típicos

- **Calcular rentabilidades con el precio bruto.** Es el error de partida. El día del split aparece
  una caída del 50 % y el día del dividendo una caída del 2 % que no existieron; la volatilidad
  sale inflada y el backtest, roto. Ajusta antes de calcular, siempre.
- **Creer que el factor de ajuste es una constante.** No lo es: hay uno por día, y es un producto
  que crece según te alejas del presente. Multiplicar toda la serie por un único número deja los
  eventos mal repartidos y produce saltos de cientos por ciento.
- **Ignorar que los ajustes se reescriben.** Cada dividendo o split nuevo cambia el pasado entero.
  Consecuencia práctica: el backtest de hace un año **no** da el mismo resultado hoy con los
  mismos datos, y si comparas dos backtests hechos con meses de diferencia, parte de la
  diferencia es de la serie, no de la estrategia. Fija la versión de los datos que usas.
- **Mezclar precio ajustado con otras columnas sin ajustar.** El volumen, el número de acciones en
  circulación y la capitalización bursátil no se ajustan con el factor del precio: en un split 1:2
  el precio se divide entre 2 y el volumen se multiplica por 2. Un gráfico de «precio ajustado
  contra volumen bruto» enseña una correlación que es un artefacto del split.
- **Confundir la fecha ex con la fecha de pago.** El precio se ajusta el día en que la acción deja
  de incluir el derecho, que es la **fecha ex**; el dinero llega a la cuenta semanas después. Si
  ajustas por la fecha de pago, mueves el salto de sitio y dejas el de verdad sin tocar.
- **Tomar la fecha ex por la fecha del anuncio.** El anuncio puede ser meses antes; el día en que
  el precio se descuenta es la fecha ex. Un pipeline que se dispare con el anuncio aplica el
  ajuste con semanas de adelanto.
- **Fiarse del ticker como identidad.** Los tickers se reutilizan. Si unes la historia de dos
  empresas distintas bajo las mismas cuatro letras, la costura mete una rentabilidad falsa enorme.
  Guarda el identificador de la empresa y verifica la continuidad de la serie en cada carga.
- **Reindexar a días naturales.** Rellenar los fines de semana con el precio del viernes inventa
  cuatro sesiones falsas por semana con rentabilidad cero, y hunde la volatilidad calculada. Si un
  día no es sesión, no tiene precio: no se rellena, se respeta el calendario.

:::trampa
Un `ffill()` sobre una serie de precios parece inofensivo y no lo es: convierte un festivo en una
sesión con rentabilidad cero. Repetido 250 veces al año, eso baja la volatilidad estimada y hace
que un modelo de riesgo parezca mejor de lo que es. Rellena solo dentro de la sesión —huecos de un
mismo día— y nunca a través de un día sin mercado.
:::

## Comprueba que lo sabes

:::quiz
p: El cierre bruto del último día antes de una fecha ex es 80,00 y el del día ex es 76,80, con un dividendo de 3,20 por acción. ¿Cuál es el factor de ajuste de los días anteriores?
o: 0,96, porque el precio bajó un 4 %
o: 1,00, porque el salto real es (76,80 + 3,20) / 80,00 = 1,00
o: 0,04, que es lo que se repartió
a: 2
e: El factor tiene que hacer que la rentabilidad del día ex sea cero cuando el precio baja exactamente lo repartido: (76,80 + 3,20) / 80,00 = 1,00. El 0,96 sería quedarse solo con el movimiento del precio e ignorar el dividendo, que es el error que la página entera trata de evitar.
:::

:::quiz
p: Una serie bruta sube un 17 % en cuatro meses y la ajustada del mismo periodo baja un 2,1 %. ¿Cómo puede ser?
o: Es un error de cálculo: la ajustada siempre es mayor que la bruta
o: Porque la serie bruta ignora los dividendos repartidos, que son dinero que el accionista cobró y que la bruta no cuenta
o: Porque el split cambió el número de acciones y alteró la rentabilidad
a: 2
e: El split no cambia nada (reparte acciones, no dinero): su efecto desaparece al ajustar. Lo que separa las dos cifras es el dividendo. En el ejemplo se repartieron 3,0 puntos por acción, más que la subida del precio, así que la rentabilidad de verdad del accionista es negativa aunque el precio termine más alto.
:::

:::quiz
p: Estás cargando precios con `pd.date_range(freq="D")` y sale un error al unir con la tabla de eventos. ¿Qué es lo más probable?
o: Que los precios tienen tres decimales y los eventos dos
o: Que estás mezclando días naturales con sesiones y las fechas no encajan
o: Que falta la zona horaria en la tabla de eventos
a: 2
e: Los mercados no cotizan todos los días: hay fines de semana y festivos, y cada plaza tiene los suyos. Si generas el calendario con días naturales aparecen sesiones que no existen y las uniones fallan o, peor, se rellenan con `NaN` en silencio. El calendario de sesiones es un dato del pipeline, no algo que se deduce del rango de fechas.
:::

:::practica
enunciado: El 15 de marzo una acción cierra a 200,0. El 12 de junio hay un split 3:1 y el 28 de junio un dividendo de 8,0 con cierre de 216,0. Calcula el precio ajustado del 15 de marzo en la base de junio y la rentabilidad de verdad del tramo, sabiendo que el precio sin ajustar sube un 8 %.
pista: Con un split 3:1, el precio de antes hay que pasarlo a la base nueva multiplicándolo por 3. Después, el dividendo descuenta (216 − 8) / 216 de todos los días anteriores.
solucion: El split multiplica el pasado por 3: 200,0 · 3 = 600,0. El dividendo descuenta (216,0 − 8,0) / 216,0 = 0,962963, así que el precio ajustado del 15 de marzo es 600,0 · 0,962963 = 577,78. Con eso, la rentabilidad de verdad del tramo es 216,0 · 3 / 577,78 − 1 = 0,1215, es decir +12,15 %. Sale más que el 8 % del precio porque hay que sumar el dividendo: el accionista cobra 8,0 (que sobre el precio de junio son 8/208 = 3,85 %) además de la subida. El split no aparece por ningún lado: reparte 3 acciones por cada una y baja el precio a un tercio, y las dos cosas se cancelan. Conclusión: el tramo gana un 12,15 % de verdad, no el 8 % del precio; la diferencia es lo repartido.
:::

:::nota
Este concepto es la puerta de entrada a todo lo que se calcula después en la ruta de finanzas
cuantitativas: una [[retornos-logaritmicos|rentabilidad]] sobre precios sin ajustar no significa
nada, y cualquier métrica construida encima hereda el error. Si vienes de ingeniería de datos, la
parte que te toca es la de siempre: [[ingesta-incremental-y-cdc|ingerir]] la tabla de eventos con
su histórico, versionarla y comprobar en cada carga que no ha cambiado sin avisar. Los precios son
la mitad del problema; la otra mitad es saber qué ha pasado con la empresa.
:::
