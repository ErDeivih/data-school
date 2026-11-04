---
id: generacion-de-senales
titulo: Generación de señales
fase: 9
nivel: avanzado
rutas: [quant, ds]
prerequisitos: [ingenieria-de-features, validacion-temporal, fuga-de-datos]
tags: [senales, ic, horizonte, capacidad]
resumen: De la idea económica a una regla medible: universo, horizonte, IC, giro y capacidad, en ese orden y antes de escribir la primera línea de backtest.
fuentes: ["Grinold y Kahn (1999), 'Active Portfolio Management'", "Qian, Hua y Sorensen (2007), 'Quantitative Equity Portfolio Management'"]
---

## En una frase

Una señal es una función de la información disponible en un instante que ordena los activos
de mejor a peor, y generarlas bien consiste en decidir qué información, con qué horizonte y
con qué frecuencia de rebalanceo.

## La idea

«Las acciones baratas lo hacen mejor» no es una señal. Es una idea, y una idea no se puede
programar. Convertirla en señal obliga a decidir cuatro cosas que la frase esconde:

1. **El universo.** ¿Barata respecto a qué conjunto? No es lo mismo el S&P 500 que todas las
   acciones cotizadas del mundo. El universo decide qué se puede comprar, a qué coste y con
   cuánta capacidad.
2. **La variable.** ¿Barata es precio sobre valor contable, sobre beneficios, sobre ventas,
   sobre flujo de caja? Cada definición es un número distinto y da una señal distinta.
3. **El horizonte y el momento.** ¿Se mide el lunes con el dato del viernes? ¿Se rebalancea
   cada mes, cada semana? El horizonte de la señal tiene que ser coherente con la frecuencia de
   rebalanceo: una señal que predice un día no sirve si rebalanceas una vez al mes.
4. **La regla.** ¿Se compra el 10 % mejor, o se ponderan todos los activos por su puntuación?
   ¿La puntuación se usa tal cual o se convierte en un rango?

Todo lo demás —costes, capacidad, monitorización— viene después, pero se decide también antes
de mirar resultados, porque después ya no serás imparcial.

Hay una disciplina que separa a quien hace esto en serio del que hace backtests bonitos: **el
conjunto de información**. En el instante `t` en que decides, solo puedes usar lo que estaba
publicado y disponible en `t`. Eso incluye detalles que se olvidan: el dato fundamental de una
empresa se publica semanas después de que termine el trimestre, los precios de cierre se
conocen al cierre, y las cifras se reajustan retroactivamente. Un backtest que use el dato
definitivo en lugar del dato publicado en la fecha estará midiendo algo que nadie pudo hacer.

Y una idea que cambia la forma de trabajar: **muchas apuestas pequeñas ganan a una apuesta
grande**. Si tu señal acierta el 51 % de las veces, con diez apuestas al año el resultado es
ruido; con diez mil, la ventaja se acumula. Por eso el sector mide las señales con el IC y no
con la rentabilidad de una cartera concreta: el IC no depende de cómo ponderes, de cuánto
arriesgues ni de qué coste pagas.

## Definición formal

Una señal es una función del conjunto de información disponible:

:::formula
s_i,t = f(I_t) ,  sin usar ninguna información posterior a t
:::

- `s_i,t` — puntuación asignada al activo `i` en el instante `t`.
- `I_t` — toda la información publicada y disponible en `t`, y nada más.
- `f` — la transformación que aplicas: un ratio contable, un z-score, un rango, lo que sea.

La calidad predictiva se mide con el **coeficiente de información** (IC), que es la
correlación de rango entre la señal de hoy y el retorno del periodo siguiente:

:::formula
IC_t = corr( rango(s_·,t) , rango(r_·,t+1) )
:::

- `rango(·)` — la posición de cada activo dentro de la sección cruzada del momento. Se usan
  rangos y no valores para que un valor extremo no domine la correlación.
- `IC_t` — un número entre −1 y 1 por cada instante. Un IC medio de 0,03 ya es una señal
  aprovechable en un universo grande; un IC de 0,3 es casi siempre un error de cálculo.
- `t` del IC medio: `media(IC) / (desv(IC) / √T)`, con `T` el número de periodos. Es lo que
  distingue una señal de una casualidad.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `s_i,t` | Puntuación que la señal da al activo `i` en el instante `t` | la de tu transformación (un ratio, un z-score, un rango) | Si sube, el activo queda mejor colocado en la sección cruzada de ese día; lo que importa es el orden, no el valor |
| `IC_t` | Correlación de rango entre la señal de hoy y el retorno del periodo siguiente | sin unidades, entre −1 y 1 | Por encima de 0 predice en el sentido de la señal; por debajo, al revés. Un 0,03 sostenido ya es aprovechable |
| `IC medio` | Media del IC de todos los periodos | sin unidades | Sube con la calidad de la señal, pero también con el número de variantes que probaste y descartaste: es el estadístico más fácil de inflar sin querer |
| `t` del IC | `media(IC) / (desv(IC) / √T)`: cuántas desviaciones separan esa media de cero | desviaciones | Por debajo de 2, la señal es indistinguible del ruido; con 300 días y un IC de 0,034 sale 5,6 |
| `amplitud` | Número de apuestas independientes al año | apuestas | Cada apuesta aporta con su raíz cuadrada, así que para doblar el IR hay que cuadruplicarla. Con 80 activos y 252 días, 20 160 |
| `ρ` | Autocorrelación de la señal de un periodo al siguiente | sin unidades | Reduce la amplitud efectiva con el factor `(1 − ρ)/(1 + ρ)`: con ρ = 0,90 el IR de 4,26 cae a 0,98 |
| `giro` | Fracción de la exposición bruta que se renueva cada periodo | tanto por uno | Sube el coste de operar, que se resta del retorno bruto antes de comparar nada |
:::

:::figura
fichero: generacion-de-senales-ic-horizonte-y-coste
pie: Arriba a la izquierda, el IC de la misma señal de reversión medido a 1, 2, 3, 5, 8, 10, 15 y 20 días: empieza en +0,0344, que es un IC aprovechable, y a los quince días ya es +0,0039. Eso fija el rebalanceo: una señal que caduca en una semana no se puede operar una vez al mes. Arriba a la derecha, la ley fundamental: sin corregir promete un IR de 4,26, y con la autocorrelación real de una señal diaria se queda en 0,98. Abajo, el coste del giro (hasta un 3,78 % anual con un giro diario del 30 % del bruto) y el reparto del IC día a día, con un 62 % de días positivos y una cola de días en los que la señal apunta al revés.
fuente: figuras/generacion-de-senales-1.py
:::

La relación entre el IC y el resultado de la cartera la resume la ley fundamental de la
gestión activa:

:::formula
IR ≈ IC · √(amplitud) ,  amplitud = número de apuestas independientes al año
:::

- `IR` — ratio de información: exceso de retorno dividido entre su volatilidad. Es el
  [[ratio-de-sharpe|Sharpe]] medido contra el índice de referencia.
- `amplitud` — cuántas decisiones independientes tomas en un año. Con 80 activos y 252 días,
  la amplitud bruta sería 80 · 252 = 20 160.
- La raíz cuadrada es lo que hace que el número de apuestas importe tanto: para doblar el IR
  con el mismo IC hay que cuadruplicar la amplitud.
- Si la señal se repite de un periodo al siguiente (autocorrelación `ρ`), las apuestas no son
  independientes y la amplitud efectiva se corrige con el factor `(1 − ρ) / (1 + ρ)`.

La decisión de cómo convertir la señal en posiciones también es una fórmula, aunque sencilla:

:::formula
w_i ∝ desviación del rango respecto a su media, con exposición bruta normalizada
:::

Se resta la media para que la cartera sea neutra y se normaliza para que el riesgo no dependa
del número de activos del universo.

## Ejemplo

Una señal de reversión de corto plazo (el retorno de ayer con el signo cambiado) medida sobre
80 activos y 299 días, en un panel construido con una reversión del 4 %:

- IC medio: **+0,0344**.
- Estadístico `t` del IC medio: **+5,60**.
- Porcentaje de días con IC positivo: **62 %**.

Un IC de 0,0344 suena a nada, y por eso conviene ponerlo en contexto con la ley fundamental.
Con 80 activos y 252 días de negociación al año, la amplitud bruta es 20 160 y el IR teórico
sería:

```
IC 0,03 · √20160 = 0,03 · 142 = 4,26
```

Un IR de 4,26 es la señal de que algo va mal en el cálculo. Y lo que va mal es el supuesto de
independencia: las señales se repiten. Con una autocorrelación de la señal de 0,90 el factor de
corrección es (1 − 0,90)/(1 + 0,90) = 0,0526, la amplitud efectiva cae a 1061 y el IR baja a
**0,98**. Con 0,95 baja a **0,68**. Es decir: entre el número optimista y el realista hay un
factor de más de cuatro, y todo sale de una propiedad de la señal que se mide antes de
construir la cartera.

Falta la última cuenta, la que decide si la señal es un negocio. Un giro diario del 20 % de la
exposición bruta con un coste de 4 puntos básicos por unidad girada cuesta:

```
0,20 · 252 · 0,0004 = 0,0202, es decir, un 2,02 % del capital al año
```

Ese 2 % hay que restarlo del retorno bruto antes de comparar nada. Una señal con IC positivo y
un coste así puede ser perfectamente perdedora.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(3)
T, N = 300, 80
R = rng.normal(0, 0.02, (T, N))
R[1:] += -0.04 * R[:-1].copy()     # reversion de corto plazo

senal = -R[:-1]                    # lo que sabemos al decidir
futuro = R[1:]                     # retorno del dia siguiente

def ic_por_dia(a, c):
    ra = np.argsort(np.argsort(a, axis=1), axis=1).astype(float)
    rc = np.argsort(np.argsort(c, axis=1), axis=1).astype(float)
    ra -= ra.mean(axis=1, keepdims=True)
    rc -= rc.mean(axis=1, keepdims=True)
    return (ra * rc).sum(axis=1) / np.sqrt((ra ** 2).sum(axis=1) * (rc ** 2).sum(axis=1))

ic = ic_por_dia(senal, futuro)
print("IC medio         %+.4f" % ic.mean())
print("t-stat del IC    %+.2f" % (ic.mean() / (ic.std(ddof=1) / np.sqrt(ic.size))))
print("dias con IC > 0  %.0f%%" % (100 * (ic > 0).mean()))
# -> IC medio         +0.0344
# -> t-stat del IC    +5.60
# -> dias con IC > 0  62%
```

:::claves
- `np.argsort(np.argsort(a, axis=1), axis=1)` devuelve **posiciones**, no valores ordenados: es la forma de convertir cada fila en rangos sin ordenarla. El doble `argsort` es el truco, y el `axis=1` es lo que hace que los rangos se calculen dentro de cada día y no en toda la matriz.
- `ra -= ra.mean(axis=1, keepdims=True)` resta la media **de cada fila** y modifica `ra` en el sitio. Sin `keepdims=True`, NumPy aplastaría la dimensión y la resta saldría contra un vector de 80 elementos mal alineado; el resultado no daría error, daría otro número.
- `ic_por_dia` divide entre `np.sqrt((ra ** 2).sum(axis=1) * (rc ** 2).sum(axis=1))`, que es la covarianza ya normalizada: por eso el IC sale entre −1 y 1 sin restar medias otra vez. Con `np.corrcoef` por fila saldría casi lo mismo y mucho más lento.
- La alineación es la lección: la señal se construye con `R[:-1]` y se compara con `R[1:]`. Si cambias una de las dos por `R`, el IC sube a un valor bonito y el backtest deja de existir, porque estarías usando el retorno que intentas predecir.
- `ic.std(ddof=1)` divide entre `T − 1` porque la desviación se estima a partir de la media; NumPy usa `ddof=0` por defecto y pandas `1`. Con 299 días la diferencia es pequeña, pero el `t` que se publica cambia.
- En el segundo bloque, `np.sqrt(amplitud)` convierte `amplitud = 80 · 252 = 20160` en 142: la raíz es lo que hace que el número de apuestas importe tanto, y también lo que convierte un supuesto razonable en un IR de 4,26 imposible.
:::

La alineación de este bloque es la lección: la señal del día `t` se construye con `R[t]` (el
retorno ya cerrado) y se compara con `R[t+1]`. Así se define además el IC de rango: se
convierten ambos vectores a rangos antes de correlacionarlos, para que un valor extremo no
decida el resultado.

```python verificable
import numpy as np

# Ley fundamental: IR = IC * raiz(amplitud), con la amplitud = apuestas independientes al ano
ic, activos, dias = 0.03, 80, 252
amplitud = activos * dias
print("IC %.2f  amplitud %d  IR teorico %.2f" % (ic, amplitud, ic * np.sqrt(amplitud)))  # -> 4.26

# Si la senal se repite de un dia para otro, las apuestas no son independientes
for rho in (0.0, 0.5, 0.8, 0.9, 0.95):
    amplitud_ef = amplitud * (1 - rho) / (1 + rho)
    print("autocorr %4.2f  amplitud efectiva %8.0f  IR %.2f" % (rho, amplitud_ef, ic * np.sqrt(amplitud_ef)))

# El coste se come el IR: giro diario de 20 % del bruto y 4 pb por unidad de giro
giro_diario, coste_pb = 0.20, 4.0
coste_anual = giro_diario * dias * coste_pb / 1e4
print("coste anual estimado %.2f%% del capital bruto" % (100 * coste_anual))  # -> 2.02% del capital bruto
# -> IC 0.03  amplitud 20160  IR teorico 4.26
# -> autocorr 0.00  amplitud efectiva    20160  IR 4.26
# -> autocorr 0.50  amplitud efectiva     6720  IR 2.46
# -> autocorr 0.80  amplitud efectiva     2240  IR 1.42
# -> autocorr 0.90  amplitud efectiva     1061  IR 0.98
# -> autocorr 0.95  amplitud efectiva      517  IR 0.68
# -> coste anual estimado 2.02% del capital bruto
```

Fíjate en lo que hace ese bloque: empieza con un IR de 4,26 que invita a pedir un préstamo y
termina con un 0,68 y un 2 % de coste anual. Ninguno de los dos extremos es una medida de la
realidad; lo que importa es el ejercicio de poner las tres correcciones antes de ilusionarse.

## Errores típicos

- **Definir la señal con información que no existía en el momento de decidir.** El caso clásico
  son los datos fundamentales: usar el beneficio del trimestre en la fecha en que terminó el
  trimestre, cuando en realidad se publicó semanas después. Es
  [[sesgo-de-mirar-al-futuro|mirar al futuro]] y no se detecta mirando la curva.
- **Normalizar con estadísticos de toda la muestra.** Si el z-score de la señal usa la media y
  la desviación de todo el histórico, cada valor contiene el futuro. Usa estadísticos
  expandidos o móviles, calculados solo con lo anterior.
- **Confundir un IC alto con una estrategia rentable.** El IC no sabe nada de costes ni de
  capacidad. Una señal con IC de 0,05 sobre activos ilíquidos puede ser un negocio ruinoso, y
  una con IC de 0,02 sobre futuros líquidos puede ser excelente.
- **No medir el giro antes de construir la cartera, y encima aumentarlo discretizando.** El
  giro es lo que convierte una señal en factura: se calcula con la propia señal, antes de
  optimizar pesos, y es el primer filtro que debería eliminar ideas. Convertir la puntuación en
  «compro / no compro» tira información y suele subir el giro, porque los activos entran y
  salen del grupo por diferencias mínimas; es mejor ordenar y ponderar.
- **Ignorar la capacidad.** ¿Cuánto capital admite la señal antes de que tu propia operación
  mueva el precio? Si la respuesta es «dos millones», tienes un buen proyecto de investigación
  y un mal negocio.
- **Probar doscientas señales y quedarse con la mejor.** Con doscientas pruebas, la mejor sale
  bien por azar con una probabilidad nada despreciable. Ajusta por el número de intentos o
  reserva datos que no hayas mirado.

:::aviso
El IC que midas en la muestra donde elegiste los parámetros de la señal está sesgado al alza.
La secuencia correcta es: define la señal, mide el IC en una muestra de desarrollo, elige los
parámetros, y luego mide el IC en una muestra que no hayas tocado. Si el IC se cae a la mitad,
no ha fallado la muestra nueva: ha funcionado el filtro.
:::

:::practica
enunciado: Una señal tiene un IC medio de 0,03 sobre 120 activos con rebalanceo diario (252 días) y una autocorrelación de 0,75. Calcula la amplitud efectiva y el IR corregido, y el coste anual si el giro diario es del 15 % de la exposición bruta con 3 pb por unidad girada.
pista: La amplitud efectiva es activos · días · (1 − ρ)/(1 + ρ); el IR, el IC por la raíz de la amplitud.
solucion: Amplitud bruta = 120 · 252 = 30 240 y el factor de corrección es (1 − 0,75)/(1 + 0,75) = 0,1429. Amplitud efectiva = 30 240 · 0,1429 = 4 320, raíz 65,7, así que el IR baja del 0,03 · 173,9 = 5,22 a 0,03 · 65,7 = 1,97. El coste es 0,15 · 252 · 0,0003 = 0,0113, un 1,13 % anual que se resta antes de comparar.
:::

## Comprueba que lo sabes

:::quiz
p: Una señal tiene IC medio de 0,05 con 50 activos y rebalanceo diario. Aplicando la ley fundamental sin correcciones sale un IR de 5,6. ¿Qué hay que corregir antes de creérselo?
o: Nada, un IC de 0,05 es alto y el IR es coherente
o: La amplitud: hay que descontar la autocorrelación de la señal, y además restar los costes del giro diario
o: El IC, que hay que multiplicar por 252 para anualizarlo
a: 2
e: La amplitud bruta supone que cada apuesta es independiente, y una señal diaria está muy autocorrelacionada: la amplitud efectiva se reduce con el factor (1 − rho)/(1 + rho). Además, un rebalanceo diario implica un giro enorme cuyo coste hay que restar antes de comparar. El IC no se anualiza multiplicando: es una correlación por periodo, no un retorno.
:::

:::quiz
p: ¿Por qué se mide una señal con el IC en lugar de con la rentabilidad de una cartera concreta?
o: Porque el IC es más fácil de calcular
o: Porque el IC mide la capacidad predictiva sin depender de cómo se ponderen las posiciones, del riesgo asumido ni de los costes pagados
o: Porque la rentabilidad de una cartera no se puede medir sin mirar al futuro
a: 2
e: El IC es una propiedad de la señal frente a los retornos siguientes, y no cambia si decides ponderar por rango, por z-score o por optimización. La rentabilidad de una cartera mezcla la señal con las decisiones de construcción y con los costes, así que sirve para juzgar la estrategia completa, no la señal.
:::

:::nota
El IC de rango (Spearman) es más robusto que el IC de Pearson cuando la señal tiene valores
extremos o una distribución muy asimétrica, que es lo habitual. Si comparas IC publicados,
comprueba cuál de los dos se usó: no son intercambiables.
:::
