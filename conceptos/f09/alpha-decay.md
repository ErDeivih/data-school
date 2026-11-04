---
id: alpha-decay
titulo: Decaimiento del alpha
fase: 9
nivel: avanzado
rutas: [quant, ds]
prerequisitos: [generacion-de-senales, data-snooping-y-multiple-testing, backtesting-vectorizado]
tags: [alpha, decaimiento, capacidad, monitorizacion]
resumen: Toda señal pierde fuerza: cómo medir la vida media del alpha, distinguirla del sobreajuste y decidir cuándo una estrategia ha dejado de existir.
fuentes: ["McLean y Pontiff (2016), 'Does Academic Research Destroy Stock Return Predictability?'", "Grinold y Kahn (1999), 'Active Portfolio Management'"]
---

## En una frase

El decaimiento del alpha es la pérdida de capacidad predictiva de una señal a lo largo del
tiempo, y se mide con la autocorrelación de la señal, el IC por horizonte y la diferencia
entre lo simulado y lo que pasa de verdad.

## La idea

Hay dos decaimientos distintos y confundirlos lleva a decisiones opuestas:

1. **El decaimiento dentro del horizonte.** Una señal no predice igual de bien el retorno de
   mañana que el de dentro de veinte días. Si la información caduca rápido, tienes que operar
   rápido y pagar mucho giro; si caduca despacio, puedes rebalancear menos y ahorrar costes.
   Este decaimiento no es un problema: es una propiedad que se mide y se presupuesta.
2. **El decaimiento secular.** La señal que funcionaba en 2005 rinde menos en 2025. Las causas
   son conocidas: más capital buscando lo mismo, mejor tecnología para encontrarlo, cambios
   regulatorios, o simplemente que el efecto era un error de valoración que el mercado ha
   corregido. Este decaimiento sí es un problema, porque no se arregla con más datos.

El segundo es el que cuenta la historia famosa: cuando un efecto se publica y se hace popular,
el capital acude y la rentabilidad cae. Que eso ocurra exactamente igual en todos los casos es
discutible, y depende de si el efecto era una prima de riesgo (que debería sobrevivir) o un
error de valoración (que debería desaparecer). Pero el patrón general —más atención, menos
alpha— es lo que hay que saber gestionar.

Y aquí está la trampa central de esta página: **no puedes distinguir el decaimiento del
sobreajuste mirando solo la curva de resultados**. Una estrategia que se cae puede ser:

- un efecto real que se ha llenado de capital,
- un efecto real que ha dejado de funcionar porque cambió el régimen,
- o un artefacto que nunca existió y que ahora, en datos nuevos, vuelve a la nada.

Las tres se ven igual en el gráfico. Lo que las distingue está fuera del gráfico: cuántas
variantes probaste antes de quedarte con esa, si el IC era estable en el tiempo o dependía de
tres meses concretos, y si el decaimiento es gradual (capital entrando) o abrupto (un cambio
estructural). Por eso el decaimiento se mide con estadísticos de la señal y no con el retorno
de la cartera.

## Definición formal

El IC por horizonte mide cuánto dura la capacidad predictiva de una señal:

:::formula
IC(h) = corr( rango(s_·,t) , rango( Σ (k = 1…h) r_·,t+k ) )
:::

- `s_·,t` — la señal de todos los activos en el instante `t`.
- `Σ r_·,t+k` — el retorno acumulado desde `t+1` hasta `t+h`. Para `h = 1` es el retorno del
  periodo siguiente.
- `IC(h)` — la correlación de rango entre ambos. Si la señal es buena, `IC(1)` es el mayor de
  la serie y va cayendo con `h`; si sube con `h`, la señal apunta a algo más lento de lo que
  pensabas y estás rebalanceando demasiado.

La velocidad de ese decaimiento se resume con la **vida media**:

:::formula
vida media = el menor h tal que IC(h) = IC(1) / 2
:::

Para una señal que se comporta aproximadamente como un proceso autorregresivo, la vida media
también sale de su autocorrelación:

:::formula
vida media = −ln(2) / ln(ρ)  ,  giro ≈ (1 − ρ) · exposición bruta por periodo
:::

- `ρ` — autocorrelación de la señal entre un periodo y el siguiente.
- `1 − ρ` — la fracción de la señal que se renueva cada periodo, y por tanto una estimación
  del giro necesario para mantener la cartera en su sitio.
- `−ln(2) / ln(ρ)` — los periodos que tarda la señal en perder la mitad de su información.

Y la condición de supervivencia frente a costes, que hay que escribir **antes** de mirar el
backtest:

:::formula
alpha neto = alpha bruto − giro · coste por unidad de giro
:::

Si el alpha bruto por periodo es menor que `giro · coste`, no hay decaimiento que estudiar: la
estrategia no era viable ni en su mejor momento. El cociente
`alpha bruto / giro` es el coste de equilibrio y se compara con tu coste real, exactamente
como en [[arbitraje-estadistico|el arbitraje estadístico]].

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `IC(h)` | Correlación de rango entre la señal de hoy y el retorno acumulado hasta `h` periodos | sin unidades, entre −1 y 1 | Si aguanta en positivo con `h` grande, la señal es lenta y puedes rebalancear menos; si se desploma, cada periodo que aguantas la posición es un periodo regalando información |
| `h` | Horizonte al que se mide el IC y ancho de la ventana de retorno | periodos | Alarga la vida de la señal pero mezcla más retornos futuros: un `h` mayor que tu frecuencia de rebalanceo mide algo que no vas a cobrar |
| `vida media` | El menor `h` con `IC(h) = IC(1) / 2`; con la autocorrelación, `−ln(2) / ln(ρ)` | periodos | Es el presupuesto de tu rebalanceo: cambiar los pesos más a menudo que la vida media solo paga coste |
| `ρ` | Autocorrelación de la señal entre un periodo y el siguiente | sin unidades | Alarga la vida media y **reduce** el giro (`giro ≈ (1 − ρ) · exposición`), pero también apunta a que la señal se renueva despacio: persistencia no es lo mismo que acierto |
| `giro` | Fracción de la exposición bruta que se renueva cada periodo | tanto por uno | Sube el coste de operar, que se resta del alpha bruto; con 5 puntos básicos por unidad y 252 periodos, un giro de 0,374 cuesta un 4,72 % anual |
| `alpha neto` | `alpha bruto − giro · coste por unidad de giro` | retorno por periodo | Si sale negativo, la señal no paga su propia operación, por muy bueno que sea su IC |
:::

:::figura
fichero: alpha-decay-horizonte-y-corte-secular
pie: Arriba a la izquierda, la autocorrelación de la señal del ejemplo medida a cada retardo: cae de 0,93 a 0,50 en diez periodos, que es la vida media que predice `−ln(2)/ln(0,93) = 9,58`. Arriba a la derecha, la vida media que sale de cada `ρ`: la misma señal con `ρ = 0,80` dura 3,1 periodos y obliga a girar la cartera tres veces más. Abajo, el decaimiento secular: el IC diario de una señal que se apaga en el periodo 700 pasa de +0,0514 a −0,0046, y mirando por tramos se ve lo que la media de todo el histórico esconde.
fuente: figuras/alpha-decay-1.py
:::

## Ejemplo

Una señal con autocorrelación `ρ = 0,930` medida sobre 2000 periodos y 100 activos:

- Vida media: −ln(2) / ln(0,930) = 0,6931 / 0,0726 = **9,58 periodos**. Es decir, la señal tarda
  casi diez periodos en perder la mitad de su información.
- Giro medio para mantener los pesos: **0,374** de la exposición bruta por periodo. Tiene
  sentido: si cada periodo se renueva aproximadamente `1 − 0,930 = 0,070` de la señal,
  `0,374` de giro parece mucho, porque los pesos se renormalizan cada periodo y las colas de la
  distribución se mueven más que la media.
- Coste con 5 puntos básicos por unidad de giro: 0,374 · 252 · 0,0005 = **4,72 % del capital al
  año**.

Ahí está la cuenta que decide: esta señal necesita un alpha bruto superior al 4,72 % anual solo
para pagar la operación. Es perfectamente posible tener razón sobre la dirección y perder
dinero por el camino.

Ahora el decaimiento secular. Con el mismo tipo de señal, pero con el alpha desapareciendo a
partir de dos tercios de la muestra:

```
IC medio antes del corte +0,0514
IC medio despues         -0,0046
IC medio ultimos 200     -0,0078
diferencia antes-despues +0,0560
```

La lectura útil no es «la estrategia ha muerto», sino «cuándo». El IC medio pasa de +0,0514 a
−0,0046, es decir, a cero con ruido alrededor: después del corte no hay información, ni buena
ni mala. Ese es el patrón de un alpha que se apaga, y no el de un mes malo, que se vería como
una caída temporal con recuperación.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(11)
T, N = 2000, 100
s = np.zeros((T, N))
s[0] = rng.normal(0, 1, N)
for t in range(1, T):
    s[t] = 0.93 * s[t - 1] + rng.normal(0, 0.37, N)     # senal AR(1)

w = s / np.abs(s).sum(axis=1, keepdims=True)            # pesos proporcionales a la senal

rho = np.corrcoef(s[:-1].ravel(), s[1:].ravel())[0, 1]
vida_media = -np.log(2) / np.log(rho)
giro = np.abs(np.diff(w, axis=0)).sum(axis=1).mean()

print("autocorr de la senal %.3f" % rho)
print("vida media           %.2f periodos" % vida_media)
print("giro medio           %.3f del bruto por periodo" % giro)
print("coste con 5 pb       %.2f%% al ano" % (100 * giro * 252 * 0.0005))
# -> autocorr de la senal 0.930
# -> vida media           9.58 periodos
# -> giro medio           0.374 del bruto por periodo
# -> coste con 5 pb       4.72% al ano
```

:::claves
- El bucle que rellena `s[t]` es un AR(1) escrito a mano: `s[t] = 0.93 * s[t-1] + ruido`. Con 2000 periodos y 100 activos, el bucle de Python tarda lo suficiente para notarse; vectorizar por periodos exigiría llevarse la recursión al eje del tiempo, así que aquí se acepta el bucle.
- `w = s / np.abs(s).sum(axis=1, keepdims=True)` normaliza **cada periodo** para que la exposición bruta sea 1. Sin el `keepdims`, la división se emite contra un vector mal orientado y NumPy no se queja si los tamaños cuadran por casualidad.
- `np.corrcoef(s[:-1].ravel(), s[1:].ravel())` aplana los dos desplazamientos y correlaciona todos los pares `(s_t, s_t+1)` de una vez. Es más rápido que correlacionar activo a activo y da prácticamente lo mismo cuando las series son homogéneas; `[0, 1]` es la posición de ese coeficiente en la matriz 2×2 que devuelve.
- `np.abs(np.diff(w, axis=0)).sum(axis=1).mean()` es giro, no variación de pesos con signo: se suma el valor absoluto de cada cambio porque comprar y vender cuestan lo mismo. Quitar el `np.abs` da un número pequeño y falso.
- `np.log(rho)` con `rho` negativo daría `nan`, y con `rho = 1` daría una división entre cero: la fórmula de la vida media solo tiene sentido con una señal persistente. Si tu `rho` sale por debajo de 0,3, la vida media es de un par de periodos y el problema no es la fórmula, es el giro.
- En el segundo bloque, `ic[:700]` y `ic[700:]` son **vistas**, no copias, así que `.mean()` sobre ellas no duplica los datos. La fecha del corte se elige antes de mirar el IC: si la eliges después, ya no estás midiendo el decaimiento, lo estás dibujando.
:::

La autocorrelación se mide sobre todos los pares `(s_t, s_t+1)` apilados, no sobre la media
de las correlaciones por activo. Es más rápido y, con series homogéneas, da prácticamente lo
mismo; con activos muy distintos conviene calcularla por activo y mirar la dispersión.

```python verificable
import numpy as np

rng = np.random.default_rng(12)
T, N = 1200, 60
s = rng.normal(0, 1, (T, N))
b = np.where(np.arange(T) < 700, 0.001, 0.0)[:, None]     # el alpha muere en t = 700
r = b * s + rng.normal(0, 0.02, (T, N))

def ic_por_dia(a, c):
    ra = np.argsort(np.argsort(a, axis=1), axis=1).astype(float)
    rc = np.argsort(np.argsort(c, axis=1), axis=1).astype(float)
    ra -= ra.mean(axis=1, keepdims=True)
    rc -= rc.mean(axis=1, keepdims=True)
    return (ra * rc).sum(axis=1) / np.sqrt((ra ** 2).sum(axis=1) * (rc ** 2).sum(axis=1))

# La senal se conoce al empezar el periodo y el retorno se cobra en ese mismo periodo
ic = ic_por_dia(s, r)
print("IC medio antes del corte %+.4f" % ic[:700].mean())
print("IC medio despues         %+.4f" % ic[700:].mean())
print("IC medio ultimos 200     %+.4f" % ic[-200:].mean())
print("diferencia antes-despues %+.4f" % (ic[:700].mean() - ic[700:].mean()))
# -> IC medio antes del corte +0.0514
# -> IC medio despues         -0.0046
# -> IC medio ultimos 200     -0.0078
# -> diferencia antes-despues +0.0560
```

Este segundo bloque es el diagnóstico que deberías correr cada trimestre sobre tus señales en
producción: IC por tramos, con la fecha de cada corte decidida de antemano. Si el IC del
último tramo es indistinguible de cero y el giro sigue siendo el mismo, la decisión no es
«aguantar», es apagar.

## Errores típicos

- **Confundir un mes malo con el final de la estrategia.** Una racha de pérdidas es compatible
  con un alpha intacto. El decaimiento se mide sobre el IC en ventanas largas, no sobre el
  retorno de las últimas semanas.
- **Medir el decaimiento en la muestra donde ajustaste la señal.** Si los parámetros se
  eligieron mirando todo el histórico, el IC de la primera mitad está inflado y el de la
  segunda, castigado: verás un decaimiento que en realidad es tu propio procedimiento.
- **Extrapolar la recta del IC hasta cero y anunciar la fecha de muerte.** El IC no cae en
  línea recta y no hay ninguna ley que garantice que siga cayendo igual. Sirve para decidir si
  hay que investigar, no para poner una fecha.
- **Ignorar la autocorrelación de la señal.** Una señal que decae en dos días exige un giro
  enorme, y ese giro es una condición de viabilidad, no un detalle de implementación. Mídela
  antes de construir la cartera.
- **Creer que un buen backtest es una licencia para seguir operando.** Un Sharpe alto en la
  simulación no dice nada de la capacidad: esta depende del universo, del tamaño de las
  posiciones frente al volumen negociado y del coste de impacto, y una estrategia excelente
  sobre microempresas puede admitir muy poco capital antes de destruirse a sí misma. Y el
  backtest es un documento histórico: si el IC en producción lleva tres trimestres en cero, lo
  que hay que revisar es la hipótesis, no la paciencia.
- **Atribuir todo el decaimiento al crowding.** A veces la causa es un cambio de régimen
  (volatilidad, tipos, correlaciones) que no tiene nada que ver con que haya más competencia.
  Distinguirlo importa: si fue el régimen, la señal puede volver; si fue la competencia, no.

:::trampa
El sesgo de selección hace que el decaimiento parezca siempre una sorpresa. Si probaste
doscientas señales y elegiste la mejor, el IC de esa señal en la muestra de selección está
inflado, y su caída posterior no es «el mercado volviéndose eficiente»: es la corrección
estadística de tu propio proceso. Antes de hablar de decaimiento, descuenta el número de
intentos con [[sharpe-deflactado|el Sharpe deflactado]].
:::

:::practica
enunciado: Una señal tiene una autocorrelación medida de 0,96 y su cartera necesita un giro de 0,18 de la exposición bruta por periodo. Calcula su vida media en periodos y el alpha bruto mínimo por periodo que hace falta para no perder dinero con un coste de 4 pb por unidad girada.
pista: La vida media es −ln(2) / ln(ρ), y el coste de equilibrio por periodo es el giro multiplicado por el coste unitario.
solucion: Vida media = −ln(2) / ln(0,96) = 0,6931 / 0,0408 = 16,98, unos 17 periodos: la señal tarda ese tiempo en perder la mitad de su información. El coste de equilibrio es 0,18 · 0,0004 = 0,000072, o sea 0,72 pb por periodo, que con 252 periodos son 1,81 % anual. Por debajo de ese alpha bruto la señal no paga ni su propia operación.
:::

## Comprueba que lo sabes

:::quiz
p: El IC de tu señal pasa de 0,05 en la primera mitad de la muestra a 0,00 en la segunda. ¿Qué conclusión es defendible?
o: Que el mercado se ha vuelto eficiente y la señal ya no puede funcionar nunca más
o: Que la capacidad predictiva medida en la segunda mitad es indistinguible de cero, y hay que decidir si fue decaimiento, cambio de régimen o sobreajuste en la selección
o: Que hay que bajar los costes para recuperar el IC
a: 2
e: El dato es que el IC de la segunda mitad es cero; la causa no se deduce de ese dato. Puede ser competencia (decaimiento real), un cambio de régimen que revertirá, o un sesgo de selección si elegiste la señal entre muchas. Los costes no afectan al IC, solo a la rentabilidad que queda después de pagarlos.
:::

:::quiz
p: Una señal tiene autocorrelación de 0,80. ¿Qué implica para la operativa?
o: Que la señal es demasiado rápida y hay que buscar otra
o: Que tiene una vida media de unos 3,1 periodos y que hay que contar con un giro considerable para mantener la cartera
o: Que el IC será necesariamente mayor que con una autocorrelación de 0,95
a: 2
e: La vida media es −ln(2) / ln(0,80) = 3,1 periodos: la información caduca rápido y los pesos cambian mucho de un periodo al siguiente, lo que se traduce en giro y en coste. La autocorrelación no dice nada sobre el nivel del IC: una señal puede ser muy persistente y no predecir nada.
:::

:::aviso
El coste de equilibrio (`alpha bruto por periodo` dividido entre `giro por periodo`) es la
primera cifra que deberías calcular de cualquier señal, antes incluso que su IC. Si el coste
de equilibrio es inferior a tu coste real de ejecución, no hay decaimiento que estudiar: no
había negocio.
:::
