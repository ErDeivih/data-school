---
id: estacionariedad
titulo: Estacionariedad
fase: 5
nivel: intermedio
rutas: [ds, quant]
prerequisitos: [series-temporales-componentes, varianza-y-desviacion]
tags: [series-temporales, supuestos, pronostico]
resumen: Media, varianza y autocovarianza que no dependen del momento en que miras la serie; el supuesto que casi todo modelo temporal da por hecho.
fuentes: ["Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice', caps. 8 y 9", "Hamilton (1994), 'Time Series Analysis', cap. 3"]
---

## En una frase

Una serie es estacionaria cuando sus propiedades estadísticas no dependen de cuándo las mires:
la media, la varianza y la autocorrelación son las mismas hoy que hace tres años, así que lo que
aprendiste del pasado sigue siendo válido para el futuro.

## La idea

Imagina dos habitaciones. En la primera hay un termostato: mires cuando mires, la temperatura
ronda los 21 °C, unas veces 20,8 y otras 21,3, pero siempre alrededor del mismo valor. En la
segunda han encendido una estufa y no la apagan: a las nueve de la mañana hay 18 °C, a mediodía
22 y a las seis de la tarde 28. En la primera habitación puedes predecir la temperatura de
mañana con la media histórica; en la segunda, esa media no sirve para nada porque el sistema se
está moviendo.

Eso es exactamente la estacionariedad. Una serie temporal es estacionaria cuando el proceso que
la genera no cambia con el tiempo. Y es el requisito que aparece una y otra vez porque casi
todos los modelos clásicos de series temporales —[[arima-sarima|ARIMA]], [[suavizado-exponencial|el
suavizado]], las bandas de confianza de una [[autocorrelacion-acf-pacf|autocorrelación]]— suponen
que existe una media y una varianza estables a las que la serie vuelve. Si esa suposición es
falsa, el modelo no está mal programado: está respondiendo a otra pregunta.

Hay tres formas de romper la estacionariedad y conviene saber distinguirlas, porque se arreglan
de forma distinta:

1. **Tendencia.** La serie sube o baja de forma sostenida (facturación de una empresa que crece,
   precio de un índice de bolsa a muy largo plazo, población de un país). La media depende del
   tiempo. Se corrige con una **diferencia**: en vez de modelar el nivel, modelas el cambio
   `Δy_t = y_t − y_{t−1}`.
2. **Estacionalidad.** El patrón se repite cada `s` periodos (ventas de helados, consumo
   eléctrico, tráfico de un portal de empleo). La media también depende del tiempo, pero de forma
   predecible. Se corrige con una **diferencia estacional** `Δ_s y_t = y_t − y_{t−s}` o dejando
   que el modelo incluya el patrón.
3. **Varianza cambiante.** El nivel es estable, pero la amplitud de las oscilaciones cambia por
   tramos (periodos tranquilos y periodos agitados). Aquí la media no delata nada: hay que mirar
   la varianza. Se corrige con una transformación (logaritmo, raíz cuadrada) o modelando la
   varianza explícitamente con un [[garch-volatilidad|GARCH]].

Un detalle que sorprende a mucha gente: una serie puede tener **media y varianza constantes y
aun así no ser independiente**. El ruido blanco es el caso extremo (sin memoria
alguna), pero un AR(1) con coeficiente 0,8 es perfectamente estacionario y un valor alto hoy
anuncia un valor alto mañana. Estacionario no significa impredecible: significa que las reglas
del juego no cambian.

## Definición formal

Una serie `{y_t}` es **estacionaria en sentido débil** (o de covarianza) si cumple tres
condiciones para todo `t`:

:::formula
E[y_t] = μ   ·   Var(y_t) = σ² < ∞   ·   Cov(y_t, y_{t+k}) = γ_k
:::

:::parametros
| Símbolo | Qué es | Unidades | Qué pide la estacionariedad |
| --- | --- | --- | --- |
| `y_t` | El valor de la serie en el instante `t` (un mes, un día, un trimestre) | las de la serie | — |
| `E[y_t]` | La media de la serie en ese instante | las de la serie | Que no dependa de `t` |
| `μ` | Esa media, ya constante | las de la serie | Que exista y sea finita |
| `Var(y_t)` | La dispersión en ese instante | las de la serie, al cuadrado | Que sea la misma en todo `t` |
| `σ²` | Ese valor constante de la varianza | las de la serie, al cuadrado | Igual para todo `t` |
| `Cov(y_t, y_{t+k})` | Cuánto se parecen el valor de hoy y el de dentro de `k` pasos | al cuadrado | Que solo dependa de `k` |
| `γ_k` | Esa covarianza, llamada autocovarianza de orden `k` | al cuadrado | Función solo de `k` |
| `ρ_k` | `γ_k / γ_0`: la autocorrelación a distancia `k` | adimensional, entre −1 y 1 | Función solo de `k` |
| `ε_t` | El ruido blanco: lo que se añade en cada paso | las de la serie | Media 0, varianza constante, sin memoria |
:::

De ahí sale la **autocorrelación** `ρ_k = γ_k / γ_0`, con `γ_0 = σ²`. Es la versión
estandarizada de la covarianza y es lo que se dibuja en un correlograma.

La **estacionariedad estricta** es más exigente: pide que la distribución conjunta de cualquier
bloque de `k` valores consecutivos sea la misma esté donde esté ese bloque. La débil es la que se
usa en la práctica, porque solo habla de medias y varianzas, que son lo que se estima con datos.

Tres consecuencias que conviene tener a mano:

- Un **paseo aleatorio** `y_t = y_{t−1} + ε_t`, con `ε_t` ruido blanco de varianza `σ²_ε`, **no es
  estacionario**: partiendo de `y_0`, su varianza es `t · σ²_ε`, que crece sin límite. Su primera
  diferencia, en cambio, es `ε_t`, que sí lo es. Ese es el motivo de que casi todo se modele en
  diferencias.
- Una serie con **tendencia determinista** `y_t = a + b·t + ε_t` tampoco es estacionaria, porque
  `E[y_t]` depende de `t`; pero quitando la tendencia (por regresión o diferenciando) queda un
  ruido estacionario. Diferenciar aquí es opcional; en un paseo aleatorio es obligatorio.
- **Diferenciar una serie que ya era estacionaria la estropea.** La serie diferenciada de más
  arrastra una autocorrelación negativa artificial: introducir una raíz unitaria en el polinomio
  de medias móviles. Por eso se contrasta antes con [[test-adf-kpss|los tests de raíz unitaria]].

:::figura
fichero: estacionariedad-nivel-y-cambio
pie: Arriba, el nivel de una serie con deriva. La línea roja es su media de todo el periodo: no describe ninguna parte de la serie, y por eso un modelo que la use se equivoca. Abajo, la misma serie diferenciada una vez: la media ya es estable y la serie se puede modelar.
fuente: figuras/estacionariedad-1.py
:::

## Ejemplo

Doce trimestres de facturación (miles de euros) con una tendencia clara:

```
20  23  25  28  30  33  35  38  40  43  45  48
```

- Media de los seis primeros trimestres: **26,50**.
- Media de los seis últimos: **41,50**.

La media se ha movido 15 puntos: la serie no es estacionaria. Fíjate en un detalle importante:
la **varianza sí es constante** (22,70 en ambos tramos). Mirar solo la dispersión no habría
detectado el problema; hay que mirar la media.

Ahora la primera diferencia, trimestre a trimestre:

```
3  2  3  2  3  2  3  2  3  2  3
```

- Media de las diferencias: **2,55**.
- Varianza de las diferencias: **0,27**.

La tendencia desapareció: queda un patrón estable que ya se puede modelar. La serie diferenciada
es estacionaria (con la salvedad de que aquí es casi determinista, porque el ruido es mínimo).

Y el tercer caso, el más traicionero: una serie con media plana pero varianza creciente. Si el
logaritmo de una magnitud crece en proporción a su nivel (precios, facturación, número de
usuarios), la serie en crudo tiene una varianza que aumenta con el nivel aunque su media sea
estable. La solución es trabajar con retornos o con el logaritmo, no con el nivel.

## Código

```python verificable
import numpy as np

# Serie trimestral con tendencia clara: cada trimestre sube ~2,5 de media
serie = np.array([20, 23, 25, 28, 30, 33, 35, 38, 40, 43, 45, 48])

primera, segunda = serie[:6], serie[6:]
print(f"media 1a mitad {primera.mean():.2f}   media 2a mitad {segunda.mean():.2f}")  # -> 26.50 y 41.50
print(f"varianza 1a    {primera.var(ddof=1):.2f}   varianza 2a    {segunda.var(ddof=1):.2f}")  # -> 22.70 y 22.70

# La primera diferencia quita la tendencia: ahora la media es estable
dif = np.diff(serie)
print(f"diferencias     {dif}")                    # -> [3 2 3 2 3 2 3 2 3 2 3]
print(f"media dif       {dif.mean():.2f}   varianza dif   {dif.var(ddof=1):.2f}")  # -> 2.55 y 0.27
```

:::claves
- `np.array([...])` es el tipo de NumPy, no una lista de Python: guarda los números pegados en memoria y sin objetos de por medio (en la página de [[numpy-fundamentos|fundamentos de NumPy]] está el porqué). Un `.mean()` sobre `np.array` es una cuenta que se hace en C, no un bucle de Python.
- `serie[:6]` y `serie[6:]` no cortan la serie en dos mitades nuevas: son **vistas** sobre los mismos datos. Si escribieras dentro de una de ellas cambiarías la serie original. Para tener una copia de verdad hay que pedirla: `serie[:6].copy()` ([[vistas-y-copias]]).
- `ddof=1` en `.var()` divide entre `n − 1` en vez de entre `n`, que es lo correcto cuando la serie es una muestra y no la población entera. NumPy usa `ddof=0` por defecto y pandas `ddof=1`: por eso el mismo dato da varianzas ligeramente distintas según la librería.
- `np.diff(serie)` devuelve un array **una posición más corto** que la entrada: cada elemento es «el de ahora menos el de antes». Por eso la primera diferencia convierte `t` observaciones en `t − 1`.
- Los dos `print` con `f"..."` y `{valor:.2f}` son formato de texto, no cálculo: `.2f` significa «dos decimales».
:::

```python verificable
import numpy as np

# 2000 caminos de 400 pasos: comparamos como crece la dispersion con el tiempo
rng = np.random.default_rng(0)
n, m = 400, 2000
pasos = rng.normal(0, 1, (m, n))
paseo = np.cumsum(pasos, axis=1)            # y_t = y_{t-1} + eps_t: raiz unitaria
ar1 = np.zeros((m, n))                      # AR(1) con phi = 0.8: estacionario
for t in range(1, n):
    ar1[:, t] = 0.8 * ar1[:, t - 1] + pasos[:, t]

for nombre, x in (("paseo aleatorio", paseo), ("AR(1) phi=0.8", ar1)):
    print(f"{nombre:>16}  desv en t=50 {x[:, 49].std(ddof=1):5.2f}"
          f"   t=200 {x[:, 199].std(ddof=1):5.2f}   t=400 {x[:, 399].std(ddof=1):5.2f}")
# -> paseo aleatorio: 7.16, 14.15 y 20.20 (crece como la raiz de t)
# -> AR(1) phi=0.8:  1.65,  1.67 y  1.64 (constante: 1/sqrt(1-0.64) = 1.67)
```

## Errores típicos

- **Mirar solo el gráfico y concluir que es estacionaria porque la media está plana.** La
  varianza también cuenta. Una serie con media estable y volatilidad que se agrupa por tramos no
  es estacionaria: es un candidato a [[garch-volatilidad|GARCH]], no a ARIMA.
- **Confundir estacionaria con independiente.** Un AR(1) con coeficiente 0,9 es estacionario y
  tiene una autocorrelación altísima. La estacionariedad dice que las reglas no cambian, no que
  no haya memoria.
- **Diferenciar sin comprobar si hacía falta.** Si la serie ya era estacionaria, `np.diff` le
  mete una raíz unitaria artificial, infla la varianza y deja una autocorrelación negativa que te
  hará elegir un MA(1) con coeficiente cercano a −1. Contrástalo antes con [[test-adf-kpss]].
- **Usar la media histórica para pronosticar una serie no estacionaria.** Con tendencia, la media
  de todo el histórico siempre va por detrás de la realidad: subestima al alza y sobreestima a la
  baja. Es el error clásico al presupuestar con la media de los últimos años.
- **Aplicar la estacionariedad a los precios y no a los retornos.** Los precios de una acción se
  parecen a un paseo aleatorio; sus [[retornos-logaritmicos|retornos logarítmicos]] son mucho más
  manejables. Casi todo el análisis financiero se hace en retornos por este motivo.
- **Confundir la estacionalidad con una raíz unitaria.** Una serie con un patrón trimestral
  fuerte tiene una media que depende de `t` y no es estacionaria, pero el problema se resuelve con
  una diferencia estacional, no diferenciando mes a mes, que destruiría la señal.

:::practica
enunciado: Un paseo aleatorio parte de y = 50 y suma pasos de varianza 4, independientes entre sí. Calcula la media y la desviación típica de la serie en t = 100, y la desviación típica de su primera diferencia. Decide si la serie en niveles es estacionaria.
pista: En un paseo aleatorio la varianza se acumula: cada paso añade su varianza a la del anterior.
solucion: La media sigue siendo 50, porque los pasos tienen media cero. La varianza en t = 100 es 100 · 4 = 400, así que la desviación típica es √400 = 20. La primera diferencia es el propio paso, con varianza 4 y desviación típica 2. La varianza en niveles crece con t, luego la serie no es estacionaria; en diferencias, sí.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál de estas series NO es estacionaria en sentido débil?
o: Ruido blanco gaussiano con media 0 y varianza 1
o: Un paseo aleatorio que empieza en 100 y suma pasos de varianza 1
o: Un AR(1) con coeficiente 0,8 y ruido blanco de varianza 1
a: 2
e: En un paseo aleatorio la varianza en el instante t es t por la varianza del paso, así que crece sin límite y el segundo requisito falla. El ruido blanco y el AR(1) con coeficiente menor que 1 en valor absoluto tienen media y varianza constantes.
:::

:::quiz
p: La facturación trimestral de una empresa sube de 20 a 48 en doce trimestres. ¿Qué haces antes de ajustar un modelo?
o: Nada: con doce datos, cualquier modelo vale
o: Diferenciar la serie para trabajar con el cambio trimestral y comprobar que la diferencia es estable
o: Restar la media de toda la serie, que ya corrige la tendencia
a: 2
e: Restar la media global deja la tendencia intacta: la serie seguiría subiendo. La primera diferencia convierte el nivel en cambio y elimina la tendencia; después hay que verificar que la serie diferenciada es estable con un contraste como el de [[test-adf-kpss]].
:::

:::trampa
Una varianza constante en la muestra no demuestra que la varianza sea constante en el proceso. En
series financieras la volatilidad se agrupa: hay meses tranquilos y meses violentos. Si ajustas un
ARIMA a retornos diarios sin mirar la varianza, los intervalos de predicción serán demasiado
estrechos justo en los peores días, que es cuando más importan.
:::
