---
id: frecuencia-y-agregacion-temporal
titulo: Frecuencia, granularidad y agregación
fase: 5
nivel: intermedio
rutas: [de, ds]
prerequisitos: [series-temporales-componentes, pandas-agrupaciones-y-joins, fechas-y-horas]
tags: [series-temporales, remuestreo, granularidad, agregacion]
resumen: Bajar de frecuencia no es resumir: promediar borra los picos, sumar un nivel da un número sin sentido y un ratio mal agregado miente.
fuentes: ["Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice', cap. 11", "McKinney (2022), 'Python for Data Analysis', cap. 11", "Pandas development team (2024), 'pandas.DataFrame.resample'"]
---

## En una frase

La frecuencia es cada cuánto está medido un dato, la granularidad es el tamaño del intervalo
que representa, y agregar es decir qué pasa con una magnitud cuando juntas varios intervalos:
la respuesta correcta depende de si esa magnitud es un flujo, un nivel o un cociente.

## La idea

Un sensor de una máquina mide cada cinco minutos y genera 288 valores al día. El analista
quiere una serie diaria. Lo natural es `resample("1D").mean()` y seguir. Ese día el equipo
pierde una anomalía: la máquina se sobrecalentó durante media hora, y esa media hora, metida
en el promedio de un día, deja de existir.

Hagámoslo con números. El sensor mide 50 de media con ruido de desviación 0,8, y un pico de
30 minutos suma 12 unidades. Al agregar:

| Granularidad | Valores al día | Subida que deja el pico | Cuánto pesa frente al ruido del nivel |
| --- | --- | --- | --- |
| Cada 5 minutos | 288 | 12,00 | 2,80 desviaciones |
| Cada hora | 24 | 6,00 | 1,42 desviaciones |
| Cada día | 1 | 0,25 | el pico se queda en la quinta parte de la variación normal entre días, que en la serie de la figura es de 1,38 |

La anomalía no se ha atenuado un poco: ha desaparecido. Un promedio diario **promedia la
señal y el ruido**, y la contribución del pico se reparte entre los 288 intervalos del día: sus
seis intervalos aportan una cuarentayochoava parte. La desviación del ruido también baja al
promediar, pero baja igual en todos los días, así que la comparación **entre** días no mejora;
y la variación diaria de la señal (el ciclo, la deriva) no baja nada. La regla que sale de aquí
es la que decide toda la fase: **agrega pensando en la anomalía más corta que te importa**. Si
necesitas ver un pico de media hora, tu frecuencia mínima es la hora, y el día es demasiado
grueso.

Y agregar no siempre es promediar. Depende del tipo de magnitud, y confundirlas produce
números que no significan nada:

- **Flujo** (lo que pasa en un intervalo: ventas del día, peticiones por minuto, litros). Se
  **suma**. Agregar de minuto a hora es sumar 60 valores, y el total del día cuadra.
- **Nivel** (lo que vale algo en un instante: inventario, saldo de una cuenta, temperatura,
  usuarios activos). Se toma el **último** valor del intervalo, o el máximo si buscas el pico,
  pero nunca la suma. Sumar el saldo de una cuenta al cierre de cada hora y llamarlo «dinero
  movido en el día» es un error de interpretación, no de cálculo.
- **Cociente o tasa** (conversión, precio medio, porcentaje de error). No se promedia ni se
  suma: se **recalcula a partir del numerador y el denominador agregados**. Promediar ratios
  pondera todos los intervalos por igual, y normalmente no quieres eso.
- **Percentil** (p95 de latencia, mediana de duración). No es agregable en absoluto: el p95 de
  los p95 de cada hora no es el p95 del día. O guardas el histograma, o recalculas desde los
  datos en crudo.

:::figura
fichero: frecuencia-agregacion-pico-y-ruido
pie: A la izquierda, 36 horas de la serie de ejemplo a tres escalas: la línea gris son los valores cada 5 minutos, con un pico de media hora en la hora 25. La línea azul es la media por hora y ya lo reduce a la mitad; agregado a día, el pico entero cabe dentro de la variación normal del nivel. A la derecha, la misma anomalía a cuatro granularidades: la amplitud del pico medida sobre el nivel cae de 16,8 a 2,0, mientras el ruido del nivel apenas baja de 1,7 a 1,4. Y si el pico se mide descontando el ciclo diario, a escala diaria se queda en 0,25. La señal se diluye mucho antes que el ruido, y por eso la anomalía deja de ser detectable.
fuente: figuras/frecuencia-y-agregacion-temporal-1.py
:::

## Definición formal

Sea `y` una serie medida con paso `Δ` (5 minutos, un día) y sea `Δ' = k · Δ` el paso al que
quieres agregarla. Con `n = k` valores dentro de cada bloque nuevo:

:::formula
flujo:   Y = Σ_{i=1}^{n} y_i            nivel:   Y = y_n (o máx y_i)
:::

:::formula
var(ȳ) = σ² / n        (varianza del promedio)        sd(ȳ) = σ / √n
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube |
| --- | --- | --- | --- |
| `Δ` | Paso temporal original: cada cuánto está medido el dato | tiempo (minutos, días) | Un paso mayor significa que ya has perdido lo que pasaba entre dos medidas, y no hay forma de recuperarlo |
| `Δ'` | Paso al que quieres agregar | tiempo | Cuanto más grande, menos filas y menos resolución. La elección se hace por la magnitud más corta que necesitas detectar, no por comodidad |
| `k` | Número de valores originales dentro de cada bloque nuevo: `Δ' / Δ` | adimensional (entero) | Sube el factor de dilución: una anomalía de duración `d` aporta a la media una fracción `d / Δ'`. Con `Δ' = 288 · Δ`, un pico de 30 minutos aporta una cuarentayochoava parte |
| `n` | Número de valores que se promedian en cada bloque | recuento | Reduce la varianza del promedio como `1/n`, pero no reduce el sesgo: si el bloque contiene una anomalía, el promedio se desplaza |
| `σ` | Desviación típica de los valores originales dentro del bloque | las de la serie | Es el ruido que se promedia. Se mide con los datos, no con la teoría: en una serie con ciclos, `σ` incluye el ciclo |
| `sd(ȳ)` | Desviación típica del promedio agregado | las de la serie | Baja con la raíz de `n`. Es la razón por la que una serie diaria parece más suave que una de 5 minutos: no es que el mundo se haya calmado, es que has promediado |
| `d` | Duración de la anomalía que te importa | tiempo | Es el parámetro que manda. Si `d < Δ'`, la anomalía no desaparece del todo, pero su contribución se vuelve comparable al ruido |
:::

Dos aclaraciones que evitan el error más común:

- **`sd(ȳ) = σ / √n` es la desviación del promedio, no la desviación de la serie agregada.**
  Si agregas 5 minutos a día y luego calculas la desviación de la serie diaria, esa desviación
  NO baja con `√n`: mide variación entre días, que es otra cosa. Confundir las dos hace que
  alguien «demuestre» que su sistema se ha estabilizado después de agregar.
- **Un ratio agregado no es el promedio de los ratios.** Si en una hora hay 1.000 visitas y 10
  compras (1 %) y en la siguiente 100 visitas y 20 compras (20 %), el promedio de los dos
  ratios da 10,5 %, mientras que el ratio de los totales da 30/1.100 = 2,7 %. El primero
  pondera las dos horas igual; el segundo pondera por tráfico.

## Ejemplo

Un sensor mide cada 5 minutos durante cinco días con una onda diaria suave y ruido de
desviación 0,8. En el intervalo 300 (minuto 1.500, es decir, la 1:00 del segundo día) se
inyecta un pico de 12 unidades que dura 30 minutos:

- **A 5 minutos:** los seis valores del pico suben 12, o sea 2,80 desviaciones del nivel. Se ve
  a simple vista.
- **A 1 hora:** el pico cae en una sola hora y sube su promedio 6 unidades (12 · 6/12). Eso es
  1,42 desviaciones: se ve, pero hay que mirar.
- **A 1 día:** los seis intervalos de 30 minutos son 6 de 288 del día, así que el promedio
  diario sube `12 · 6/288 = 0,25`. En una serie con variación semanal, como la de la figura, la
  desviación típica de los promedios diarios es 1,38: el pico es una quinta parte de la
  variación normal entre días. Nadie lo va a ver.

Y un segundo ejemplo, sobre la trampa de la media de medias. Febrero tiene 28 días a 10 °C de
media y marzo 8 días medidos a 20 °C (solo hay lecturas de la primera semana):

- Media de las medias: `(10 + 20) / 2 = 15,0`.
- Media correcta, ponderando por días: `(28 · 10 + 8 · 20) / 36 = 12,22`.
- Error: **2,78 °C**, por promediar dos agregados que representan distinta cantidad de días.

## Código

```python verificable
import numpy as np
import pandas as pd

# Cinco dias medidos cada 5 minutos: onda diaria suave y ruido de desviacion 0.8
azar = np.random.default_rng(0)
minutos = pd.date_range("2026-01-05", periods=5 * 24 * 12, freq="5min")
t = np.arange(len(minutos))
base = 50 + 6 * np.sin(2 * np.pi * t / 288) + azar.normal(0.0, 0.8, len(t))
sin_pico = pd.Series(base, index=minutos)
con_pico = sin_pico.copy()
con_pico.iloc[300:306] += 12.0        # media hora de sobrecalentamiento

for etiqueta, regla in [("5 min", "5min"), ("1 hora", "1h"), ("1 dia", "1D")]:
    a = sin_pico.resample(regla).mean()
    b = con_pico.resample(regla).mean()
    print("%-7s n=%5d  subida del pico=%6.2f  desviacion del nivel=%.2f"
          % (etiqueta, len(a), (b - a).abs().max(), a.std()))
# -> 5 min   n= 1440  subida del pico= 12.00  desviacion del nivel=4.29
# -> 1 hora  n=  120  subida del pico=  6.00  desviacion del nivel=4.22
# -> 1 dia   n=    5  subida del pico=  0.25  desviacion del nivel=0.05
print("la serie de 5 minutos tiene desviacion %.3f" % sin_pico.std())
# -> la serie de 5 minutos tiene desviacion 4.287
```

:::claves
- `resample("1D").mean()` agrupa por día natural y **promedia dentro de cada grupo**. Si la magnitud es un flujo (ventas, peticiones), lo que quieres es `.sum()`; si es un nivel (inventario, saldo), `.last()` o `.max()`. Elegir mal no da error: da un número plausible y falso.
- `resample` es distinto de `groupby`: `groupby` agrupa por el valor de una columna, `resample` agrupa **por el índice de tiempo** y decide las etiquetas de los bloques. Si tu fecha está en una columna y no en el índice, `resample` lanza `TypeError`.
- Las etiquetas de `resample("1D")` apuntan al **inicio del intervalo** por defecto (`label="left"`). Al agregar a mes, la etiqueta es el primer día del mes, no el último. Si unes esa serie con otra que usa el cierre del periodo, todo se desplaza.
- `closed`: para «1D» con datos que caen exactamente a medianoche, `closed="left"` (por defecto) mete la medianoche en el día que empieza y `closed="right"` la mete en el que acaba. Cambiar esto mueve los valores de frontera entre bloques y cambia la serie sin avisar.
- La desviación del nivel diario sale 0,05 porque esta serie sintética solo tiene estructura diaria: quitar el ciclo dentro de cada día deja los promedios casi idénticos. Con una serie real, esa cifra es la variación entre días (en el ejemplo de la figura, 1,38), y es la que hay que comparar con la subida de 0,25 para ver que el pico ya no se distingue.
- `con_pico.iloc[300:306] += 12.0` suma **en el sitio** y no devuelve nada útil: escribir `con_pico = con_pico.iloc[300:306] + 12.0` crearía una copia del trozo y dejaría el resto de la serie intacto, que no es lo que quieres.
:::

```python verificable
import numpy as np
import pandas as pd

# --- Flujo frente a nivel ------------------------------------------------------
flujo = pd.Series([10.0, 20.0, 15.0])        # lo que pasa en cada hora
nivel = flujo.cumsum()                       # lo que marca el contador al cierre
print("flujo total %.0f   suma de las fotos del contador %.0f   ultimo nivel %.0f"
      % (flujo.sum(), nivel.sum(), nivel.iloc[-1]))
# -> flujo total 45   suma de las fotos del contador 85   ultimo nivel 45

# --- Media de medias sin ponderar ---------------------------------------------
febrero = np.full(28, 10.0)                  # 28 dias a 10 grados
marzo = np.full(8, 20.0)                     # solo 8 dias medidos en marzo
print("media de las medias %.3f   media ponderada %.3f"
      % ((febrero.mean() + marzo.mean()) / 2,
         np.concatenate([febrero, marzo]).mean()))
# -> media de las medias 15.000   media ponderada 12.222

# --- Promedio de ratios frente a ratio de totales -----------------------------
visitas = pd.Series([1000.0, 100.0])
compras = pd.Series([10.0, 20.0])
print("media de los ratios %.4f   ratio de los totales %.4f"
      % ((compras / visitas).mean(), compras.sum() / visitas.sum()))
# -> media de los ratios 0.1050   ratio de los totales 0.0273
```

:::claves
- `flujo.cumsum()` convierte un flujo en un nivel. La suma del nivel (85) no es el total del periodo (45): es el **área bajo la escalera**, que solo tiene sentido si la serie fuera continua. La firma del error es que el resultado crece con el número de fotos que tomas.
- `np.full(28, 10.0)` crea 28 valores iguales; sirve para hacer visible que la media de las medias solo coincide con la media correcta si los dos grupos tienen el mismo tamaño. Si febrero tuviera 28 días y marzo 28, las dos cifras darían 15,0.
- `(compras / visitas).mean()` pondera las dos horas por igual; `compras.sum() / visitas.sum()` pondera por tráfico. La diferencia entre 10,5 % y 2,7 % no es un matiz de precisión: son dos métricas de negocio distintas con el mismo nombre.
- Los dos `Series` del ejemplo de ratios **comparten índice** por construcción. Si vinieran de tablas distintas con índices diferentes, la división alinearía por etiqueta y produciría `NaN` en los huecos en lugar de un error; comprueba siempre el número de filas antes de dividir.
:::

## Errores típicos

- **Agregar con `mean` cualquier cosa.** El promedio es correcto para magnitudes intensivas (temperatura, precio por unidad en el mismo instante), pero para flujos hay que sumar y para niveles hay que tomar el último. Un panel de ventas diarias construido con `mean` sobre ventas por hora da la venta media por hora, no la del día, y el número es 24 veces menor.
- **Subir de frecuencia para rellenar huecos.** Llevar una serie mensual a diaria por interpolación inventa 29 valores por mes. Es legítimo para un gráfico, y es una fuga de información si esos valores entran en un modelo ([[fuga-de-datos]], [[imputacion-de-datos]]).
- **Muestrear sin comprobar el aliasing.** Si mides un ciclo de 12 horas cada 24, todas las medidas caen en la misma fase y la onda parece una constante. Antes de bajar la frecuencia de una señal periódica, comprueba que el nuevo paso no es múltiplo del periodo ([[series-temporales-componentes]]).
- **Ignorar los bloques incompletos.** El primer y el último periodo casi nunca están completos: el día que empieza a medianoche y corta a las 10, o el mes en curso. Un flujo agregado sobre un bloque parcial es menor que los demás y arruina cualquier comparación o detector de anomalías ([[calidad-de-datos]]).
- **Mezclar zonas horarias al agregar.** Agrupar por día natural en UTC y compararlo con informes en hora local desplaza las ventas de la tarde al día siguiente. Fija la zona antes de agregar y no la cambies a mitad del análisis ([[fechas-y-horas]]).
- **Comparar métricas calculadas a distinta granularidad.** Un modelo evaluado sobre datos diarios y otro sobre datos de 5 minutos no son comparables, ni siquiera con la misma métrica. Fija la granularidad de evaluación antes de modelar, y evalúa todos los candidatos en ella ([[metricas-de-regresion]], [[pronosticos-de-referencia-y-mase]]).
- **Creer que agregar reduce el ruido del sistema.** Reduce la varianza del promedio dentro de cada bloque, no la variabilidad entre bloques. La pregunta «¿mi sistema es más estable los martes?» solo se responde con la variación entre martes.

:::practica
enunciado: Tienes latencias medidas cada minuto durante una hora: la mayoría entre 40 y 60 ms, con un pico de 900 ms que dura 3 minutos. Quieres una serie de 6 bloques de 10 minutos. ¿Con qué agregado no pierdes el pico, y qué pasa si usas la media? ¿Y si en vez de latencia fueran peticiones por minuto?
pista: El pico ocupa 3 de los 10 minutos de un bloque, así que su peso en la media es 3/10. Piensa qué magnitud estás agregando: un tiempo de respuesta es un nivel por intervalo, no un flujo.
solucion: Con la media, el bloque que contiene el pico sube `(3 · 900 + 7 · 50) / 10 = 305` ms, que se ve; los otros bloques quedan en 50. Pero el pico real era 900 y el promedio lo deja en 305: si el umbral de alerta está en 800, la media no lo dispara y el máximo sí. Para latencia usa `max` por bloque (o el p95, si el pico es más corto que el bloque), nunca la media, porque un pico de 3 minutos dentro de un bloque de 10 se diluye a un tercio. Si fueran peticiones por minuto, la magnitud es un flujo y la regla cambia: se suma, y el bloque con el pico da `3 · 900 + 7 · 50 = 3.050` peticiones, que es el total real del bloque.
:::

## Comprueba que lo sabes

:::quiz
p: Un sensor mide cada 5 minutos y hay un pico de 30 minutos. Pasas la serie a diaria con la media y el pico desaparece. ¿Cuál es la explicación correcta?
o: Porque la media diaria introduce un error de redondeo que elimina los valores altos
o: Porque el pico contribuye al promedio diario en proporción a su duración: 6 de 288 intervalos, o sea 12 · 6/288 = 0,25, por debajo de la variación normal entre días
o: Porque el pico estaba mal medido y a escala diaria se corrige
a: 2
e: Promediar es repartir la contribución del pico entre todos los intervalos del bloque. Seis intervalos de 288 aportan una cuarenta y ochoava parte de las 12 unidades: 0,25, frente a una desviación de 1,38 entre promedios diarios. No hay redondeo ni corrección: hay dilución. Si quieres conservar el pico, la solución es agregar con máximo o quedarte a una granularidad más fina.
:::

:::quiz
p: Agregas a diario una tabla con ventas por hora y usas `.mean()`. ¿Qué obtienes?
o: La venta total del día
o: La venta media por hora de ese día
o: La venta media diaria de todo el mes
a: 2
e: La media de las 24 horas del día es la venta de una hora típica de ese día, no el total. Para el total hay que usar `.sum()`, porque la venta por hora es un flujo: se acumula. La media diaria del mes saldría de promediar los totales diarios, que es un paso posterior.
:::

:::quiz
p: En una hora hay 1.000 visitas y 10 compras; en la siguiente, 100 visitas y 20 compras. ¿Cuál es la conversión del periodo de dos horas?
o: El 10,5 %, que es la media de los dos porcentajes
o: El 2,7 %, que es el total de compras entre el total de visitas
o: El 20 %, porque es la conversión de la hora con más compras
a: 2
e: El ratio correcto se recalcula con los totales: 30 compras entre 1.100 visitas, un 2,7 %. La media de los porcentajes (10,5 %) pondera las dos horas por igual y le da el mismo peso a una hora con 100 visitas que a una con 1.000. La tercera opción ni siquiera es un agregado: es elegir la hora que más te gusta.
:::

:::aviso
Antes de agregar, decide qué es cada columna: flujo, nivel, tasa, percentil o marca de tiempo.
Un `resample(...).mean()` aplicado a la columna equivocada no falla, no avisa y produce un
número creíble. Es el error de agregación más frecuente en un panel de métricas, y el más
difícil de detectar después, porque el resultado ya está publicado.
:::
