---
id: tick-data-y-ohlcv
titulo: Datos de transacción y velas
fase: 9
nivel: básico
rutas: [quant, de]
prerequisitos: [que-es-un-mercado]
tags: [datos, velas, agregación, series-temporales]
resumen: Del tick a la vela: cada agregación resume el mercado y borra parte de la historia; saber qué se pierde evita backtests que solo funcionan en papel.
fuentes: ["López de Prado (2018), 'Advances in Financial Machine Learning', cap. 2"]
---

## En una frase

El *tick* es cada operación con su hora, su precio y su volumen; una vela (OHLCV) es el resumen
de todas las operaciones de un periodo, y al resumir se gana legibilidad pero se pierde el orden,
el número de operaciones y el camino que recorrió el precio.

## La idea

Imagina que quieres contar un partido de fútbol. Puedes grabar los 90 minutos completos, o
apuntar cada minuto el marcador. La segunda opción ocupa una hoja de papel y sirve para casi
todo, pero si un gol se anuló, si hubo dos goles en el mismo minuto o si el equipo dominó sin
marcar, esa hoja no te lo dice. La vela es el acta por minutos; el tick es el vídeo.

Los datos de transacción (ticks o *trades*) son la lista de operaciones ejecutadas: instante con
precisión de milisegundos o microsegundos, precio, cantidad y, en algunos mercados, si el
comprador o el vendedor fue el agresor. Con eso puedes reconstruir exactamente qué pasó y en qué
orden. El problema es el tamaño: un día de un valor líquido puede generar cientos de miles de
operaciones, y años de historia de varios valores ocupan cientos de gigabytes.

La vela es una agregación a un intervalo fijo (1 minuto, 5 minutos, 1 día). De cada intervalo
guarda **cinco números**: apertura, máximo, mínimo, cierre y volumen. Con eso se contesta lo
habitual: ¿subió o bajó?, ¿con cuánta amplitud?, ¿con cuánta participación? Y ocupa mil veces
menos.

Lo que la vela **no** dice, y conviene tener presente:

- **El orden de las operaciones dentro del intervalo.** Una vela con apertura 100, mínimo 99 y
  cierre 100,50 se ve igual si el precio bajó primero y luego subió o al revés. Para una
  estrategia de intradía, ese orden es justo lo que importa.
- **Cuántas operaciones hubo.** Una vela de 1.040 acciones puede ser una sola orden institucional
  o 200 operaciones pequeñas. La segunda implica mucha más participación y un mercado más sano.
- **El tamaño de cada operación.** Sin eso no puedes estimar el impacto ni detectar bloques.
- **El camino exacto del precio.** El máximo y el mínimo te dicen el rango, no si el precio pasó
  por el nivel de tu stop antes o después de tocar tu objetivo. Esto decide si una simulación de
  stop y objetivo es realista o es una fantasía.
- **De qué lado vino la presión.** Saber si las compras fueron agresivas (al *ask*) o pasivas
  distingue una subida con dinero de un simple hueco de apertura.

La conclusión práctica no es «usa siempre ticks». Tienes 15 años de historia diaria en un fichero
de 200 MB y tres meses de ticks en 40 GB. La conclusión es: **elige la agregación según lo que
tu estrategia necesita saber, y sé consciente de lo que has borrado.**

:::nota
La primera vela del día y la última no son comparables con las de en medio: en la subasta de
apertura se acumulan órdenes de toda la noche y en el cierre se concentra el volumen de los
fondos que siguen un índice. Son las dos barras con más información y las dos más engañosas.
:::

:::figura
fichero: tick-a-vela-que-se-pierde
pie: A la izquierda, las operaciones de los primeros minutos como puntos cuyo tamaño es su volumen, con la vela de cada minuto encima: el primer minuto abre y cierra casi al mismo precio, pero dentro se mueve un 0,16 %, y eso la vela no lo cuenta. A la derecha, los mismos datos agregados por tiempo (una barra por minuto) y por volumen (una barra cada 1.000 títulos): la desviación de las variaciones sale 0,0693 en un caso y 0,0417 en el otro, sin que el mercado haya cambiado. Conclusión: `V` se suma y se conserva, pero el camino y el tamaño de cada operación se pierden, y hasta la volatilidad que mides depende del criterio de agregación que elijas.
fuente: figuras/tick-data-y-ohlcv-1.py
:::

## Definición formal

Un conjunto de ticks es una secuencia de operaciones con su instante, y una vela es el resumen
de un intervalo:

:::formula
op_i = ( t_i , p_i , q_i )          vela_k = ( T_k , O_k , H_k , L_k , C_k , V_k )
:::

- `t_i` — instante de la operación i. **No es equidistante**: hay segundos con veinte operaciones
  y minutos con ninguna.
- `p_i`, `q_i` — precio y cantidad de la operación i.
- `T_k` — instante que etiqueta la vela k (normalmente el inicio del intervalo).
- `O_k`, `C_k` — precio de la primera y de la última operación dentro del intervalo.
- `H_k`, `L_k` — precio máximo y mínimo dentro del intervalo.
- `V_k` — suma de `q_i` de todas las operaciones del intervalo.

La agregación se define entonces como una partición del tiempo y una reducción por grupo:

:::formula
O_k = p_{min i en grupo}     C_k = p_{max i en grupo}     H_k = max p_i     L_k = min p_i     V_k = suma q_i
:::

- **grupo** — el conjunto de índices `i` cuya marca de tiempo cae dentro del intervalo k.
- **partición** — los intervalos no se solapan y cubren todo el periodo; si un intervalo no
  tiene ninguna operación, **no hay vela**. Ese hueco importa: un gráfico con huecos no es un
  gráfico con precios repetidos.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `t_i` | El instante de la operación `i` | marca de tiempo (ms, s) | No se elige y **no es equidistante**: los ticks llegan en ráfagas. Si la resolución es de segundos, dos operaciones dentro del mismo segundo quedan indistinguibles y el orden se pierde |
| `p_i`, `q_i` | El precio y la cantidad de la operación `i` | EUR y títulos | La cantidad no aparece en ninguna vela: solo se suma. Sin `q_i` no puedes estimar el impacto ni distinguir un bloque de 1.040 títulos de doscientas operaciones pequeñas |
| `T_k` | El instante que etiqueta la vela `k`, normalmente el inicio del intervalo | marca de tiempo | El tamaño del intervalo decide cuánto se borra: velas de un minuto conservan más camino que las diarias, y las de un día se comen la sesión entera. Y ojo con la etiqueta: el cierre de la vela marcada como 09:00 no estaba disponible a las 09:00 |
| `O_k`, `C_k` | El primer y el último precio del intervalo | EUR | Su diferencia es lo que casi todo el mundo mira, y es justo lo que **no** cambia si el camino se recorre en orden contrario. Una vela con `O = C` y un rango amplio es el caso más engañoso |
| `H_k`, `L_k` | El precio máximo y el mínimo del intervalo | EUR | Definen el rango, no la ruta: no te dicen si tu stop se tocó antes o después de tu objetivo dentro de la misma barra. Si ambos niveles caen dentro de `[L_k, H_k]`, el resultado de la simulación es ambiguo, no favorable |
| `V_k` | La suma de las cantidades del intervalo | títulos | Es la única información de actividad que sobrevive, y es aditiva: el volumen total de la sesión no se pierde al agregar. El **número** de operaciones y el tamaño medio, en cambio, se pierden para siempre |
| `n` (tamaño de barra) | Cuántos ticks o cuánto tiempo entra en cada vela | ticks o segundos | Con barras más grandes ganas legibilidad y pierdes detalle. El número de barras cambia, y con él la desviación de las variaciones: comparar volatilidades calculadas sobre frecuencias distintas no tiene sentido sin declararlo |
:::

## Ejemplo

Nueve operaciones de un valor, con hora al segundo:

```text
hora       precio   volumen
09:00:01   100,00   120
09:00:03   100,02   340
09:00:12    99,98    80
09:00:45   100,01   500
09:01:05   100,05   220
09:01:41   100,03    75
09:02:00   100,07   640
09:02:19   100,04    90
09:02:55   100,09   310
```

Agregando por minuto:

| Minuto | Apertura | Máximo | Mínimo | Cierre | Volumen |
| --- | --- | --- | --- | --- | --- |
| 09:00 | 100,00 | 100,02 | 99,98 | 100,01 | 1.040 |
| 09:01 | 100,05 | 100,05 | 100,03 | 100,03 | 295 |
| 09:02 | 100,07 | 100,09 | 100,04 | 100,09 | 1.040 |

Lectura de lo que se ha perdido:

- La vela de 09:00 tiene apertura 100,00 y cierre 100,01, casi plana. Pero dentro bajó a 99,98 y
  volvió: hubo un recorrido del 0,04 % en 44 segundos que la vela no destaca.
- Las velas de 09:00 y 09:02 tienen **el mismo volumen**, 1.040, pero la primera se formó con 4
  operaciones y la segunda con 3. El volumen medio por operación es distinto (260 frente a 346,7):
  son mercados distintos con la misma cifra.
- El número total de operaciones (9) no aparece en ninguna vela. Si solo tienes OHLCV, esa
  información es irrecuperable.
- La vela de 09:01 es la más estrecha (rango de 0,02) y la de menos volumen (295): un minuto sin
  actividad. Si tu estrategia dispara con cualquier movimiento, ese minuto es ruido puro.

Ahora la comparación que de verdad importa. Con las tres velas, la variación entre cierres es
100,01 -> 100,03 -> 100,09: dos subidas de 0,02 y 0,06, con una variación media de **+0,04** y una
desviación de esas variaciones de **0,0283**. Ese número, calculado sobre barras de distinta
duración y participación, es el que alimentará tu modelo de volatilidad. Si cambias el criterio
de agregación (por ejemplo, barras de volumen constante), el mismo mercado produce otro número.

## Código

```python verificable
# Nueve operaciones con su hora, precio y volumen: los datos de partida.
horas = ["09:00:01", "09:00:03", "09:00:12", "09:00:45", "09:01:05",
         "09:01:41", "09:02:00", "09:02:19", "09:02:55"]
precios = [100.00, 100.02, 99.98, 100.01, 100.05, 100.03, 100.07, 100.04, 100.09]
volumenes = [120, 340, 80, 500, 220, 75, 640, 90, 310]

# Agregar por minuto: el primero y el ultimo precio dan apertura y cierre,
# y el numero de operaciones se pierde al sumar.
velas = {}
for hora, precio, volumen in zip(horas, precios, volumenes):
    minuto = hora[:5]
    v = velas.setdefault(minuto, {"apertura": precio, "maximo": precio,
                                  "minimo": precio, "cierre": precio,
                                  "volumen": 0, "operaciones": 0})
    v["maximo"] = max(v["maximo"], precio)
    v["minimo"] = min(v["minimo"], precio)
    v["cierre"] = precio
    v["volumen"] += volumen
    v["operaciones"] += 1

print("minuto  apertura  maximo  minimo  cierre  volumen")
for minuto in sorted(velas):
    v = velas[minuto]
    print(f"{minuto}  {v['apertura']:8.2f}  {v['maximo']:6.2f}  "
          f"{v['minimo']:6.2f}  {v['cierre']:6.2f}  {v['volumen']:7d}")
# -> 09:00    100.00  100.02   99.98  100.01     1040
# -> 09:01    100.05  100.05  100.03  100.03      295
# -> 09:02    100.07  100.09  100.04  100.09     1040
print("operaciones agregadas:", len(horas),
      "volumen total:", sum(v["volumen"] for v in velas.values()))
# -> operaciones agregadas: 9 volumen total: 2375
```

:::claves
- `minuto = hora[:5]` corta la cadena **por posición** y se queda con «09:00». Funciona porque las horas están en formato estricto; con `"9:00:01"` (sin el cero de delante) el corte daría `"9:00:"` y las velas saldrían mal **sin dar ningún error**. Para fechas de verdad se convierte a `datetime` y se agrupa con su resolución, no con trozos de texto.
- `velas.setdefault(minuto, {...})` crea el diccionario del minuto la primera vez y lo devuelve las siguientes. Es el patrón habitual para agrupar, pero el diccionario inicial se construye **siempre**, aunque ya exista la clave: con millones de ticks eso es trabajo tirado. Y `v["apertura"]` se fija en la primera pasada porque la primera operación que llega es la que abre; si el fichero no estuviera ordenado por hora, la apertura sería cualquier cosa.
- El orden de las líneas importa: `v["maximo"] = max(v["maximo"], precio)` y `v["cierre"] = precio` se ejecutan en cada operación, así que el cierre acaba siendo el precio de la última del grupo. Mover la línea del cierre antes del `max` no cambia el resultado, pero moverla fuera del bucle sí: te quedarías con el cierre del primer tick de cada minuto.
- `v["operaciones"] += 1` cuenta las filas y `v["volumen"] += volumen` suma las cantidades. Las dos columnas se calculan igual de fácil **aquí**, con los ticks delante; si mañana solo tienes el OHLCV, la de operaciones ya no se puede reconstruir. Por eso el ejemplo las escribe: son las dos únicas del resumen que después se pierden.
- `print(f"{v['apertura']:8.2f}")` fija el ancho y los decimales, pero no redondea el número guardado. Y las comillas cruzadas son obligatorias: dentro de una f-string con comillas dobles, las claves del diccionario van con comillas simples, o el intérprete cierra la cadena antes de tiempo.
- `sorted(velas)` recorre las claves del diccionario **en orden alfabético**, que coincide con el cronológico porque el formato es «HH:MM» con ceros a la izquierda. Con un formato como «9:00» el orden alfabético pondría las 10:00 antes que las 9:00 y el gráfico saldría desordenado sin que nada fallara.
:::

```python verificable
import numpy as np

# Barras de tiempo frente a barras de volumen: la misma serie, dos criterios.
rng = np.random.default_rng(0)
precios = 100 + np.cumsum(rng.normal(0, 0.05, size=600))
volumen = rng.integers(10, 200, size=600).tolist()

def barras_por_tiempo(p, tam):
    return p[::tam]

def barras_por_volumen(p, v, objetivo):
    cierres, acumulado = [], 0
    for i, precio in enumerate(p):
        acumulado += v[i]
        if acumulado >= objetivo:            # se cierra la barra y se reinicia el contador
            cierres.append(precio)
            acumulado = 0
    return np.array(cierres)

por_tiempo = np.diff(barras_por_tiempo(precios, 20).astype(float))
por_volumen = np.diff(barras_por_volumen(precios.tolist(), volumen, 1000))

print("barras por tiempo :", por_tiempo.size)                # -> 29
print("barras por volumen:", por_volumen.size)               # -> 59
print("desv. por tiempo  :", round(por_tiempo.std(ddof=1), 4))     # -> 0.2245
print("desv. por volumen :", round(por_volumen.std(ddof=1), 4))    # -> 0.1475
```

## Errores típicos

- **Tratar los ticks como una serie regular.** Los ticks llegan cuando alguien opera: hay
  ráfagas y silencios. Cualquier cálculo que suponga un dato por segundo está inventando datos
  que no existen. Si necesitas regularidad, agrega y acepta lo que pierdes.
- **Etiquetar la vela con el final del intervalo y operar con el inicio, o al revés.** Si tu vela
  se llama 09:00 y contiene las operaciones de 09:00:00 a 09:00:59, el cierre de esa vela **no**
  estaba disponible a las 09:00. Mezclar la etiqueta con el instante real de disponibilidad es la
  forma más silenciosa de mirar al futuro.
- **Olvidar los ajustes por dividendos y ampliaciones.** Un precio de 25 EUR antes de un split
  2:1 y de 12,50 después parece una caída del 50 % que nunca ocurrió. Trabaja siempre con series
  ajustadas o, mejor, con retornos calculados dentro de cada tramo homogéneo.
- **Ignorar zonas horarias y cambios de horario.** Las velas de una misma estrategia comparadas
  entre países, o el cambio de hora de verano, desplazan una hora entera de actividad. En datos
  intradiarios, ese desplazamiento arruina cualquier cálculo de estacionalidad.
- **Usar la vela en curso.** La vela del día actual, a media sesión, tiene un cierre que todavía
  no es un cierre. Un backtest que la usa está operando con información que no tendría.
- **Promediar o comparar series agregadas a frecuencias distintas.** Una volatilidad diaria y una
  volatilidad de un minuto no son la misma magnitud. Si mezclas frecuencias sin declararlo, los
  números no son comparables.

:::practica
enunciado: Cuatro operaciones del minuto 10:00: 50,10 con 300 títulos, 50,06 con 150, 50,14 con 900 y 50,04 con 250. Construye la vela (apertura, máximo, mínimo, cierre y volumen), el volumen medio por operación y el rango en porcentaje sobre la apertura.
pista: La apertura es el primer precio del intervalo y el cierre el último, aunque el cierre coincida con el mínimo del minuto.
solucion: Apertura 50,10, máximo 50,14, mínimo 50,04, cierre 50,04 (la última operación) y volumen 300 + 150 + 900 + 250 = 1.600 títulos. Con cuatro operaciones, el volumen medio es 1.600 / 4 = 400 títulos. El rango es 50,14 − 50,04 = 0,10 EUR, un 0,20 % sobre la apertura. La vela cierra en el mínimo y parece débil, pero no sabes si fue una sola orden de 900 la que marcó el máximo.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Que información se pierde al pasar de ticks a velas de un minuto y no se puede recuperar?
o: El volumen total negociado en el minuto
o: El orden de las operaciones dentro del minuto y cuántas hubo
o: El precio máximo y mínimo del minuto
a: 2
e: La vela conserva apertura, máximo, mínimo, cierre y volumen agregado. Lo que desaparece es la secuencia interna: si el precio subió o bajó primero, y con cuántas operaciones se formó. Dos velas idénticas pueden proceder de mercados muy distintos.
:::

:::quiz
p: Una vela de 1.040 acciones y otra de 1.040 acciones, ¿son el mismo fenomeno de mercado?
o: Si, porque el volumen agregado es identico
o: No necesariamente: una puede ser una sola orden grande y la otra 200 operaciones pequeñas
o: Si, siempre que tengan el mismo rango entre máximo y mínimo
a: 2
e: El volumen es una suma y no distingue tamaños. Una única orden de 1.040 acciones es un bloque que puede haber movido el precio; 200 operaciones de tamaño pequeño indican participación amplia y un mercado más profundo. Para distinguirlo hacen falta los ticks o, al menos, el número de operaciones por barra.
:::

:::trampa
Un backtest intradia construido solo con OHLCV no puede saber si tu stop se toco antes o después
de tu objetivo dentro de la misma vela. Cualquier simulación que decida ese orden «a favor» está
regalandose resultado. Si el máximo y el mínimo de una barra contienen ambos niveles, el dato
honesto es que el resultado es ambiguo.
:::
