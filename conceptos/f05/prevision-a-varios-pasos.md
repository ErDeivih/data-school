---
id: prevision-a-varios-pasos
titulo: Previsión a varios pasos
fase: 5
nivel: intermedio
rutas: [ds, quant]
prerequisitos: [series-temporales-componentes, autocorrelacion-acf-pacf, validacion-temporal]
tags: [series-temporales, pronostico, horizonte, error]
resumen: Predecir doce meses no es repetir doce veces la predicción de uno; la recursiva, la directa y la multi-salida se equivocan de forma distinta en cada horizonte.
fuentes: ["Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice', cap. 5", "Chevillon (2007), 'Direct multi-step estimation and forecasting'"]
---

## En una frase

Un modelo de un paso solo sabe predecir el paso siguiente, así que hay que decidir cómo
llegar hasta el horizonte doce: encadenando predicciones (recursiva), entrenando un modelo
para cada horizonte (directa) o entrenando un solo modelo que devuelve los doce valores de
golpe (multi-salida).

## La idea

Tienes un modelo que predice el consumo eléctrico de mañana a partir del de hoy. Te piden el
consumo de los doce meses que vienen. El modelo sabe hacer una cosa: dar un paso. El problema
de previsión a varios pasos es cómo convertir eso en doce números, y hay tres maneras.

La primera es **encadenar**: predices mañana, ese valor lo metes como si fuera un dato
observado, predices pasado mañana, y así doce veces. Se llama previsión recursiva, es lo que
hace todo el mundo por defecto, y tiene un rasgo que hay que entender antes de usarla: **el
único error que se propaga es el del modelo de un paso**. Si el modelo siempre se queda un
poco corto, el hueco se va sumando paso a paso y al horizonte doce el pronóstico está muy
lejos. Con un modelo autorregresivo estable, además, la predicción converge a la media de la
serie: cuanto más lejos miras, menos te crees el dato de hoy y más te crees el promedio
histórico. Eso no es un fallo, es la respuesta correcta del modelo; pero significa que a
largo plazo todos tus pronósticos se parecen entre sí.

La segunda es **entrenar un modelo por horizonte**. Para predecir a doce meses, ajustas
directamente la relación entre el dato de hoy y el dato de dentro de doce meses; para once,
otro. Cada modelo tiene su propia varianza del error, y ninguno arrastra error porque ninguno
usa predicciones. El precio es que cada horizonte se estima con menos historia: si tienes 60
observaciones y quieres el horizonte 12, ese modelo solo ve 48 pares, mientras que la
recursiva usa los 60 en un solo ajuste.

La tercera es **multi-salida**: un único modelo con doce salidas que se entrenan juntas, de
modo que el horizonte 12 aprende del 11 y del 10. La forma más honesta de describirlo es que
es una directa con información compartida entre horizontes, y solo aporta cuando esa
información compartida es real (por ejemplo, cuando la forma del error en el horizonte es
suave y se puede imponer como una recta). Si el modelo multi-salida es un ajuste por mínimos
cuadrados sin ninguna restricción que ate los horizontes, coincide numéricamente con la
directa: doce modelos de un solo parámetro o una matriz con doce columnas dan la misma
solución.

:::figura
fichero: prevision-varios-pasos-recursiva-frente-a-directa
pie: A la izquierda, la previsión recursiva para un proceso autorregresivo con coeficiente 0,396: el pronóstico cae de 2,64 a 1,91 en el primer paso, y luego se va pegando a la media de la serie (1,432) sin llegar nunca a ella, porque cada paso multiplica la distancia por 0,396. La línea naranja es la fórmula cerrada `media + φ^h · (y_T − media)`, que reproduce los puntos azules exactamente: no es una aproximación. A la derecha, la directa sobre los mismos datos y la misma ventana de entrenamiento, con un ajuste por horizonte: en la mitad de los horizontes gana a la recursiva y en la otra mitad pierde, y la diferencia entre las dos curvas es menor que la dispersión de los datos. Con datos estacionarios y 60 observaciones de entrenamiento, el error absoluto medio de la recursiva es 0,984 y el de la directa 1,001: la elección importa menos de lo que sugiere la teoría, hasta que el proceso tiene raíz unitaria o el modelo de un paso está mal.
fuente: figuras/prevision-a-varios-pasos-1.py
:::

## Definición formal

Sea `y_1, …, y_T` la serie observada, `h` el horizonte y `p` el número de retardos del modelo
de un paso.

:::formula
recursiva:  ŷ_{T+h} = f(ŷ_{T+h−1}, …, ŷ_{T+h−p})        directa:  ŷ_{T+h} = f_h(y_T, y_{T−1}, …)
:::

Para el caso autorregresivo de orden uno, `y_t = c + φ·y_{t−1} + ε_t`, la recursiva tiene
solución cerrada, que es lo que la hace tan fácil de diagnosticar:

:::formula
ŷ_{T+h} = μ + φ^h · (y_T − μ),  con  μ = c / (1 − φ)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube |
| --- | --- | --- | --- |
| `h` | Horizonte: cuántos pasos hacia delante se pronostica | pasos (meses, días) | Más pasos, más error en los tres métodos, pero el error de la recursiva crece de forma acotada: converge a la varianza de la serie |
| `y_T` | Último valor observado: el punto de partida | las de la serie | Es la única información que distingue un pronóstico de otro. Si `y_T` es un dato atípico, los doce pronósticos salen malos |
| `c` | Ordenada del modelo autorregresivo de un paso | las de la serie por paso | Sube el nivel hacia el que converge el pronóstico. Se estima con datos, no se elige |
| `φ` | Coeficiente autorregresivo: cuánto del valor de hoy pasa a mañana | adimensional | Por debajo de 1 en valor absoluto, el pronóstico se pega a la media y el error a largo plazo se estabiliza. Cerca de 1, el pronóstico se comporta como un paseo aleatorio y el error crece en línea recta con `h` |
| `μ` | Media de la serie implícita en el modelo: `c / (1 − φ)` | las de la serie | Es el destino de la recursiva. Cuanto más lejos esté `y_T` de `μ`, más grande es el recorrido y más se nota el método |
| `φ^h` | Cuánto sobrevive la desviación inicial después de `h` pasos | adimensional, entre 0 y 1 si `φ` está entre 0 y 1 | Sube si `φ` está más cerca de 1 y si `h` es pequeño. Es el factor que decide si el horizonte doce conserva algo del dato de hoy |
| `f_h` | El modelo entrenado específicamente para el horizonte `h` | — | No es un símbolo numérico: es un ajuste distinto por horizonte. Cada uno se estima con `T − h` pares de datos, así que los horizontes largos ven menos historia |
:::

Dos consecuencias prácticas de la fórmula cerrada: el pronóstico recursivo es **monótono**
hacia `μ` (no oscila), y la diferencia entre dos pasos consecutivos se multiplica por `φ`
cada vez, así que la secuencia converge de forma geométrica. Si eso no es lo que esperas de
tu serie, el modelo de un paso está mal especificado y la recursiva heredará el problema
doce veces.

## Ejemplo

Serie de 260 observaciones generada como `y_t = 0,5 + 0,6·y_{t−1} + ε_t`, con ruido de
desviación 1. Se ajusta un modelo de un paso con las últimas 60 observaciones del tramo de
entrenamiento (`y[:200][-60:]`, las observaciones 141 a 200) y sale `c = 0,8652` y `φ = 0,3957`,
o sea una media implícita `μ = 0,8652 / (1 − 0,3957) = 1,432`. El último dato de esa ventana es
`y_T = 2,637`; la serie sigue hasta `3,507` en la observación 260, que se reserva para los
orígenes de prueba.

- Desviación inicial: `y_T − μ = 1,205`.
- Horizonte 1: `1,432 + 0,3957 · 1,205 = 1,909`.
- Horizonte 2: `1,432 + 0,3957² · 1,205 = 1,621`. La diferencia con el paso anterior se ha
  multiplicado por 0,396.
- Horizonte 5: `1,432 + 0,3957⁵ · 1,205 = 1,443`.
- Horizonte 12: `1,432 + 0,3957¹² · 1,205 = 1,432`. Del dato de hoy solo queda una milésima.

Eso es la recursiva. La directa, sobre la misma ventana, da `1,909` en el horizonte 1,
`1,339` en el 2 y `1,490` en el 12: no se pega a la media, oscila con el ruido de cada
ajuste. Sobre 48 orígenes de prueba, el error absoluto medio por horizonte sale así:

| Horizonte | 1 | 2 | 4 | 8 | 12 | media |
| --- | --- | --- | --- | --- | --- | --- |
| Recursiva | 0,843 | 0,942 | 0,992 | 1,020 | 0,971 | 0,984 |
| Directa | 0,840 | 0,992 | 1,037 | 1,015 | 1,001 | 1,001 |
| Multi-salida | 1,022 | 1,027 | 1,014 | 1,038 | 0,967 | 1,021 |

La lectura importante no es quién gana: es que **la diferencia entre métodos es del 2 %**,
mientras que el error en el horizonte 1 es un 14 % menor que la media de los doce. El
horizonte pesa mucho más que el método. Donde el método sí decide es en el examen del
modelo: la recursiva te da una trayectoria que puedes comprobar contra la fórmula cerrada
(como en la figura), y la directa no te da ninguna garantía de forma.

## Código

```python verificable
import numpy as np

# Proceso autorregresivo estable: y_t = 0.5 + 0.6*y_{t-1} + ruido
azar = np.random.default_rng(4)
n = 260
y = np.empty(n)
y[0] = 10.0
for t in range(1, n):
    y[t] = 0.5 + 0.6 * y[t - 1] + azar.normal(0.0, 1.0)
ventana = y[:200][-60:]          # las 60 ultimas observaciones de entrenamiento
h = np.arange(1, 13)

i = np.arange(len(ventana) - 1)
A = np.column_stack([np.ones(len(i)), ventana[i]])
c, phi = np.linalg.lstsq(A, ventana[i + 1], rcond=None)[0]

# Recursiva: la prediccion vuelve a entrar como si fuera un dato observado
hist = [ventana[-1]]
recursiva = []
for _ in range(len(h)):
    v = c + phi * hist[-1]
    hist.append(v)
    recursiva.append(v)

# Directa: un modelo por horizonte, sin realimentar nada
directa = []
for k in h:
    j = np.arange(len(ventana) - k)
    Ak = np.column_stack([np.ones(len(j)), ventana[j]])
    ck = np.linalg.lstsq(Ak, ventana[j + k], rcond=None)[0]
    directa.append(ck[0] + ck[1] * ventana[-1])

media = c / (1 - phi)
print("c=%.4f phi=%.4f media implicita=%.3f" % (c, phi, media))
# -> c=0.8652 phi=0.3957 media implicita=1.432
print("recursiva h=1,2,12: %.3f %.3f %.3f" % (recursiva[0], recursiva[1], recursiva[11]))
# -> recursiva h=1,2,12: 1.909 1.620 1.432
print("formula cerrada h=1,2,12: %.3f %.3f %.3f"
      % (media + phi * (ventana[-1] - media), media + phi**2 * (ventana[-1] - media),
         media + phi**12 * (ventana[-1] - media)))
# -> formula cerrada h=1,2,12: 1.909 1.620 1.432
print("directa h=1,2,12: %.3f %.3f %.3f" % (directa[0], directa[1], directa[11]))
# -> directa h=1,2,12: 1.909 1.339 1.490
```

:::claves
- `np.linalg.lstsq(A, b, rcond=None)[0]` devuelve **la solución**, no un objeto con atributos: el `[0]` es el vector de coeficientes y el resto de la tupla son residuos, rango y valores singulares. Es el equivalente a `np.polyfit` pero admite varias variables.
- El diseño de la directa se construye con `j = np.arange(len(ventana) - k)`: el número de filas baja con el horizonte. Si copias el diseño de otro horizonte sin recalcularlo, `lstsq` lanza `Incompatible dimensions` o, peor, ajusta una relación que no es la que crees.
- El bucle de la recursiva mete en `hist` la predicción, no el valor real. Ese es todo el método: cambiar `v` por `ventana[...]` convertiría la recursiva en «evaluar con datos conocidos», que da un error artificialmente pequeño.
- `phi` se estima dentro de la función, así que `media = c / (1 - phi)` hereda su error. Si `phi` sale 0,98, la media implícita es 50 veces la ordenada `c` y cualquier imprecisión en `phi` mueve el destino del pronóstico.
- La directa del horizonte 12 usa `len(ventana) − 12 = 48` filas, no 60. Comparar su error con el de la recursiva sin decir esto es comparar dos cantidades entrenadas con distinta cantidad de datos.
- Con `phi` negativo (series que oscilan un paso sí y otro no), la recursiva también converge a la media, pero alternando de signo: `φ^h` cambia de signo en cada paso. No es un error del código.
:::

## Errores típicos

- **Encadenar sin mirar si el modelo de un paso tiene sesgo.** La recursiva multiplica el sesgo por cada paso: si el modelo se queda corto 0,2 de media, al horizonte 12 el pronóstico arrastra ese error doce veces. La comprobación es barata: grafica los residuos del modelo de un paso y mira si su media es distinta de cero.
- **Entrenar la directa con todo el histórico y compararla con un modelo de un paso.** Son cosas distintas: la directa del horizonte `h` solo usa `T − h` pares. Si no informas de la muestra efectiva, la comparación favorece a la recursiva sin motivo.
- **Elegir el método mirando el error del horizonte que interesa.** Probar recursiva y directa y quedarse con la que gana en el horizonte 12 es elegir después de ver el resultado. Si vas a comparar, fija el método antes, en [[validacion-temporal|validación temporal]] con varios orígenes, y reporta la curva de error entera.
- **Confundir multi-salida con «doce modelos que se hablan».** Un ajuste multi-salida sin restricción que ate las salidas da los mismos coeficientes que doce regresiones sobre el mismo diseño. El valor está en la restricción (compartir parámetros entre horizontes), no en el envoltorio de la API.
- **Ignorar la estacionalidad al agregar horizontes.** Si la serie tiene ciclo semanal y pronosticas 30 pasos, la recursiva con un solo retardo repite el error de no ver el ciclo en cada paso. Aquí hacen falta retardos estacionales ([[series-temporales-componentes]]) o un modelo específico ([[arima-sarima]]).
- **Reportar un único intervalo para todos los horizontes.** La incertidumbre del pronóstico crece con `h` de forma distinta en cada método, y con la recursiva se satura en la varianza de la serie. Un intervalo constante para los doce horizontes está mal por construcción ([[prediccion-con-incertidumbre]]).

:::practica
enunciado: Un modelo de un paso da `c = 0,4` y `φ = 0,9`, y el último dato observado es 10. Calcula el pronóstico recursivo en los horizontes 1, 5 y 10 y el factor que queda del dato de hoy en cada uno. ¿Qué horizonte necesitas para que al pronóstico le quede menos de un 10 % del desvío inicial?
pista: La fórmula cerrada es `ŷ = μ + φ^h · (y_T − μ)` con `μ = c / (1 − φ)`.
solucion: La media implícita es `μ = 0,4 / 0,1 = 4`. El desvío inicial es `10 − 4 = 6`. Horizonte 1: `4 + 0,9 · 6 = 9,4`. Horizonte 5: `4 + 0,59049 · 6 = 7,543`. Horizonte 10: `4 + 0,34868 · 6 = 6,092`. El factor que queda es `0,9^h`: para bajar del 10 % hace falta `0,9^h < 0,1`, o sea `h > log(0,1)/log(0,9) = 21,85`, así que a partir del horizonte 22. Con `φ = 0,9` el modelo tarda casi dos años de pasos en olvidar el dato de hoy, y eso es un aviso: una serie con tanta memoria necesita un horizonte de pronóstico corto o un modelo que capture algo más que su propio pasado.
:::

## Comprueba que lo sabes

:::quiz
p: Un modelo autorregresivo de un paso se aplica de forma recursiva con `φ = 0,4`. ¿Qué le pasa al pronóstico en el horizonte 12?
o: Se aleja cada vez más del último dato, porque el error se acumula sin límite
o: Se queda prácticamente en la media de la serie, porque el factor `φ^12` vale menos de una milésima
o: Oscila alrededor del último dato con amplitud constante
a: 2
e: La fórmula cerrada es `μ + φ^h · (y_T − μ)`, y con `φ = 0,4` el factor `0,4^12` vale 0,0000017: del desvío inicial no queda nada. El error se acumula, sí, pero de forma acotada: converge a la varianza de la serie, no crece sin límite. La oscilación aparecería con un `φ` negativo, que no es el caso.
:::

:::quiz
p: ¿Cuál es la diferencia esencial entre previsión recursiva y directa?
o: La recursiva usa predicciones como entradas; la directa entrena un modelo distinto por horizonte y no realimenta nada
o: La recursiva solo vale para series estacionarias y la directa para series con tendencia
o: La directa siempre da un error menor porque no acumula error
a: 1
e: La diferencia es la realimentación: la recursiva mete cada predicción en el modelo para dar el paso siguiente. La directa ajusta la relación entre el dato de hoy y el de dentro de `h` pasos, con `T − h` observaciones por horizonte. No hay garantía de que la directa gane: en el ejemplo de la página, la recursiva tiene error medio 0,984 y la directa 1,001, porque a cambio de no propagar error la directa estima con menos datos.
:::

:::quiz
p: En un proceso autorregresivo estable, ¿por qué el pronóstico recursivo se acerca a la media de la serie al crecer el horizonte?
o: Porque el modelo no tiene información sobre el futuro y la respuesta correcta es la esperanza condicional, que converge a la media incondicional
o: Porque el código arrastra un error de redondeo que se acumula
o: Porque la media de la serie se recalcula con cada paso y sustituye a la predicción anterior
a: 1
e: No es un artefacto numérico: es la solución matemática. En un proceso con `φ` menor que 1 en valor absoluto, la esperanza condicional a `h` pasos es `μ + φ^h · (y_T − μ)`, y `φ^h` tiende a cero. Lo que hace el modelo es olvidar el dato de hoy al ritmo que le marca `φ`, porque esa es la dinámica del proceso. Si el mundo real tiene memoria larga, el modelo es el que está mal, no el encadenamiento.
:::

:::aviso
La previsión a varios pasos no arregla un modelo de un paso malo: lo repite. Antes de elegir
entre recursiva y directa, comprueba los residuos del modelo de un paso
([[diagnostico-de-residuos]]) y asegúrate de que bates al [[pronosticos-de-referencia-y-mase|ingenuo]]
en el horizonte que te importa.
:::
