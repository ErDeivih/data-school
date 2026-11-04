---
id: missing-data
titulo: Datos ausentes
fase: 2
nivel: intermedio
prerequisitos: [poblacion-y-muestra, medidas-de-centralidad, probabilidad-condicional]
rutas: [ds, de, core]
tags: [nulos, sesgo, imputacion]
resumen: MCAR, MAR y MNAR describen por qué falta cada dato, y ese mecanismo —no el porcentaje de nulos— decide si borrar filas sesga el resultado.
fuentes: ["Rubin (1976), 'Inference and Missing Data'", "Little y Rubin (2019), 'Statistical Analysis with Missing Data'"]
---

## En una frase

Un valor ausente nunca es solo un hueco: es el resultado de un mecanismo, y si ese mecanismo tiene
que ver con el valor que falta, el análisis de casos completos estima la media de los que
responden, no la de la población.

## La idea

Estás estimando el salario medio de una empresa y ocho de cada diez personas contestan la encuesta.
Los dos que no contestan son el director general y el comercial que cobra por comisiones. La media
de los ocho que responden es perfectamente calculable y está equivocada: has medido «el salario
medio de quien contesta encuestas de salario», que es una población distinta.

Ese es el problema, y la forma de razonarlo tiene tres casos:

- **MCAR** (*missing completely at random*): la probabilidad de que falte un dato no depende de
  nada, ni de lo observado ni de lo que falta. Es el sensor que se estropea al azar, el cuestionario
  que se pierde en el correo. Si borras filas, la estimación sigue siendo insesgada para la media,
  pero pierdes muestra y precisión. Es cómodo de suponer y raro en la práctica.
- **MAR** (*missing at random*): la probabilidad de que falte depende de **cosas que sí observas**,
  pero no del valor que falta. Los hombres contestan menos la pregunta de ingresos que las mujeres:
  el sexo lo observas, así que dentro de cada sexo el hueco es aleatorio y puedes corregirlo con un
  modelo. Ojo con el nombre: MAR no significa «falta al azar», significa «falta al azar **dado lo
  observado**». Es el supuesto que necesitan la imputación múltiple y los métodos de
  verosimilitud.
- **MNAR** (*missing not at random*): la probabilidad de que falte depende del propio valor que
  falta. Los que más ganan no dicen cuánto ganan; los pacientes más graves no vuelven a la revisión.
  Aquí ningún método estándar lo arregla, porque la información que necesitas es exactamente la que
  no tienes. Solo puedes hacer análisis de sensibilidad: «si los ausentes ganaran entre un 20 % y un
  60 % más que los observados, el efecto estaría entre X e Y».

La segunda idea es que **borrar filas no es neutral, es un filtro**. Al hacer análisis de casos
completos estás condicionando en «este dato está observado», y si eso correlaciona con el resultado,
cambias la población de la que hablas. Por eso el primer diagnóstico no es contar nulos, sino
comparar: ¿los registros con nulos se parecen a los completos en el resto de variables? Si el
porcentaje de bajas voluntarias es del 30 % entre los que tienen el ingreso ausente y del 8 % entre
los que lo tienen, tienes un problema de mecanismo, no de cantidad.

La tercera idea es que **imputar por la media es peor que borrar** en cuanto te importe algo más que
la media. Al sustituir todos los huecos por el mismo valor, la varianza se encoge artificialmente,
las correlaciones se atenúan hacia cero (los valores imputados no covarían con nada) y los
intervalos de confianza salen demasiado estrechos. Ganas tamaño de muestra en apariencia y pierdes
la estructura de los datos. Como referencia: el análisis de casos completos sesga; la imputación
simple por la media sesga **y** miente sobre la incertidumbre.

Lo que sí funciona: distinguir «no aplica» de «no lo sé», guardar el indicador de ausencia como una
variable más (a veces la ausencia es informativa), imputar con modelos que usen el resto de
variables y repetirlo varias veces para reflejar la incertidumbre ([[imputacion-de-datos]]), o
modelar directamente por máxima verosimilitud con todos los datos disponibles. Y documentar el
porcentaje y el motivo, porque un análisis sin esa información no es reproducible.

## Definición formal

Sea `Y` la variable que puede faltar y `R` el indicador de observación: `R = 1` si `Y` está
observado y `R = 0` si falta. Sea `X` el conjunto de variables observadas (que puede incluir otras
columnas y, en parte, la propia `Y`). Los tres mecanismos se definen por la distribución de `R`:

:::formula
MCAR:  P( R = 1 | Y, X ) = P( R = 1 )
:::

:::formula
MAR:   P( R = 1 | Y, X ) = P( R = 1 | X )
:::

:::formula
MNAR:  P( R = 1 | Y, X )  depende también de los valores no observados de Y
:::

Símbolos: `P(R = 1 | ·)` es la probabilidad de que el dato esté presente dado lo que se sabe; en MAR
el condicionante `X` incluye todo lo observado, no solo las variables del modelo.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `Y` | La variable que puede faltar: el salario, el peso, la fecha de baja | las de la variable | No es una cantidad que se mueva; lo que decide el problema es si su propio valor influye en que falte (eso separa MAR de MNAR) |
| `R` | Indicador de observación: 1 si el dato está, 0 si falta | 0 o 1 | Cuantos más ceros, menos datos y más ancho el intervalo; pero el **sesgo** no depende de cuántos faltan sino de quiénes faltan |
| `X` | Todo lo observado, no solo las variables del modelo | — | Cuantas más variables entren en `X`, más probable es que el mecanismo sea MAR y más creíble la corrección; con un `X` pobre, MAR es un acto de fe |
| `P(R = 1)` | Probabilidad de que el dato esté presente, la misma para todas las filas (MCAR) | probabilidad | Si baja, se pierde muestra y precisión, y la media sigue insesgada: MCAR es incómodo, no peligroso |
| `n` | Número de filas totales | filas | Con `n` pequeño, cualquier mecanismo no aleatorio pesa más en el resultado; no cambia el sesgo, cambia cuánto se nota |
| `n_obs` | Cuántas de esas filas tienen el dato observado | filas | `n_obs / n` es exactamente el factor que aplasta la varianza al imputar por la media: cuanto menor, más falsa precisión |
| `Var_observada` | Varianza calculada solo con los que responden | al cuadrado, las de `Y` | Sube con la dispersión real, pero al rellenar con la media queda multiplicada por `n_obs / n` y el intervalo sale demasiado estrecho |
:::

El sesgo del análisis de casos completos es la diferencia entre la media de los observados y la
media de todos:

:::formula
Sesgo = E[ Y | R = 1 ] − E[ Y ]
:::

Y el efecto de imputar por la media, con `n` observaciones totales y `n_obs` observadas, es
aproximadamente este:

:::formula
Var_imputada ≈ ( n_obs / n ) · Var_observada
:::

Cada hueco rellenado con la media no aporta dispersión, así que diluye la varianza en la proporción
de datos que faltan. La misma aritmética explica por qué las correlaciones se van hacia cero: el
valor imputado es constante y no puede covariar con nada.

Dos advertencias formales:

1. **MAR y MNAR no se distinguen con los datos.** La definición de MNAR involucra valores que no
   observas, así que no existe un test que separe ambos casos. Se decide con conocimiento del
   dominio (¿quién no contesta y por qué?) y se acompaña de análisis de sensibilidad.
2. **El orden importa.** La imputación se ajusta **solo con el conjunto de entrenamiento** y se
   aplica después a validación y test. Imputar antes de dividir filtra información del test y es una
   forma de [[fuga-de-datos]].

## Ejemplo

Diez personas, salario mensual en euros. Las dos últimas no contestaron, y son precisamente las que
más ganan:

```
1800  1900  2000  2100  2200  2400  2500  2600  9000  12000
```

- Media real (si conocieras todo): 38.500 / 10 = **3.850 €**.
- Media de los ocho que responden: 17.500 / 8 = **2.187,5 €**.
- Sesgo: 2.187,5 − 3.850 = **−1.662,5 €**, un 43 % por debajo de la realidad.

Y ahora el efecto de rellenar los dos huecos con la media de los observados, 2.187,5 €:

- Desviación típica real: **3.400,7 €**.
- Desviación típica con los dos huecos imputados por la media: **242,6 €**.

Las dos imputaciones no aportan ni un gramo de dispersión y la variabilidad se desploma de 3.400 a
243. Cualquier contraste o intervalo calculado sobre esa columna será falsamente preciso.

Compara los dos errores: borrar filas te da una media sesgada pero honesta en su dispersión;
imputar por la media te da la misma media sesgada y además una falsa sensación de precisión.

:::figura
fichero: nulos-sesgo-y-varianza
pie: Izquierda: si los que más ganan no contestan, la media de los que responden no es la de la plantilla y ningún cálculo posterior lo arregla, porque el hueco no está repartido al azar. Derecha: rellenar los huecos con esa media deja un pico en el centro y hunde la desviación de 1.265 € a 559 €; la media sigue sesgada y encima el resultado parece mucho más preciso de lo que es.
fuente: figuras/missing-data-1.py
:::

## Código

```python verificable
import pandas as pd

# Simulacion con la verdad conocida, para poder medir el sesgo
completo = pd.Series([1800, 1900, 2000, 2100, 2200, 2400, 2500, 2600, 9000, 12000], dtype=float)
observado = completo.mask(completo.index >= 8)      # los dos que mas ganan no responden

print(f"media real                {completo.mean():.1f}")   # -> 3850.0
print(f"media de casos completos  {observado.mean():.1f}")  # -> 2187.5
print(f"desv real                 {completo.std(ddof=0):.1f}")  # -> 3400.7
print(f"desv imputando la media   {observado.fillna(observado.mean()).std(ddof=0):.1f}")  # -> 242.6
print(f"nulos                     {int(observado.isna().sum())}")  # -> 2
```

:::claves
- `completo.mask(condicion)` pone `NaN` donde la condición es **verdadera**; `where()` hace justo lo contrario (conserva donde es verdadera). Cambiar `mask` por `where` deja observados precisamente los dos sueldos que se querían esconder, y el bloque sigue ejecutándose sin quejarse.
- `observado.mean()` devuelve 2.187,5 y no `NaN` porque pandas **se salta los nulos** por defecto. El matiz muerde: `.mean()`, `.std()` y `.min()` ignoran los huecos, pero `.sum()` de una columna entera de nulos da `0`, no `NaN`, y el `.count()` cuenta los que **sí** están (daría 8). NumPy no se salta nada: `np.mean` de un array con un `nan` devuelve `nan`.
- El `ddof=0` de `.std()` tiene que ir con nombre. El primer argumento posicional de `std` es `axis`, no `ddof`, así que `observado.std(0)` **no** cambia el divisor: sigue usando `ddof=1` y da 0,707 en vez de 0,5 con dos valores (el 0 y el 1). Es una línea que parece correcta y no hace nada.
- `observado.fillna(observado.mean())` devuelve una **copia**: después de esa línea `observado` sigue teniendo sus dos `NaN`. Si más abajo se vuelve a usar `observado` en vez del resultado, se está calculando sobre los huecos otra vez.
- `observado.isna().sum()` funciona porque al sumar `True` vale 1 y `False` vale 0; el resultado es un `np.int64` y el `int(...)` de fuera solo sirve para que el texto salga limpio. `count()` es lo contrario: cuenta los no nulos.
- Al enmascarar, el **índice no se renumera**: los dos huecos siguen siendo las posiciones 8 y 9, y por eso `.fillna()` y las operaciones posteriores siguen alineando las filas correctas. Si esa columna se convierte a lista o a array de NumPy, esa alineación se pierde y el hueco pasa a ser un valor más.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(0)
n = 5000
y = rng.normal(50, 10, size=n)

# MCAR: falta por un fallo del sensor, independiente del valor
mcar = y[rng.random(n) > 0.30]

# MNAR: faltan sistematicamente los valores mas altos (los que mas ganan no contestan)
mnar = y[y < np.quantile(y, 0.70)]

print(f"media completa  {y.mean():.2f}")     # -> 49.95
print(f"media con MCAR  {mcar.mean():.2f}")  # -> 49.78
print(f"media con MNAR  {mnar.mean():.2f}")  # -> 44.96
```

## Errores típicos

- **Decidir por el porcentaje y no por el mecanismo.** «Solo falta un 2 %» no dice nada: si ese 2 %
  son los diez clientes más grandes, el análisis está roto. Un 40 % MCAR en cambio es un problema de
  precisión, no de sesgo.
- **Borrar filas sin comparar los grupos.** Antes de decidir, compara los registros con nulos y sin
  nulos en el resto de variables. Si difieren en algo que afecta al resultado, el mecanismo no es
  MCAR y borrar sesga.
- **Imputar por la media y seguir como si los datos fueran reales.** Encoge la varianza, atenúa las
  correlaciones y hace que los intervalos de confianza sean demasiado estrechos. Si la media te vale
  como estimador puntual, no la uses para nada que dependa de la dispersión.
- **Confundir ausente con cero o con «no aplica».** Un ingreso de 0 y un ingreso desconocido son
  cosas distintas, y una fecha de baja vacía porque el cliente sigue activo no es un nulo: es un
  valor estructural. Trátalos por separado ([[calidad-de-datos]]).
- **Imputar con la variable objetivo o con datos del futuro.** Rellenar el gasto de un mes con el
  promedio de todo el año, incluidos los meses siguientes, mete información imposible en el modelo y
  es una forma clásica de fuga ([[fuga-de-datos]]).
- **Suponer que MAR es comprobable.** No existe un test que separe MAR de MNAR, porque la diferencia
  está en datos que no tienes. Asume el mecanismo con argumentos del dominio y haz análisis de
  sensibilidad cambiando el supuesto.

:::practica
enunciado: Diez clientes declaran su gasto mensual: 20, 25, 30, 35, 40, 45, 50, 55, 60 y 90 euros. Los tres que más gastan (55, 60 y 90) no contestan. Calcula la media de casos completos, el sesgo respecto a la media real y la desviación que tendría la columna si rellenaras los tres huecos con esa media.
pista: La media de los siete observados es el punto de partida, y cada hueco rellenado con la media no aporta ninguna dispersión.
solucion: Media real: 450/10 = 45,0. Media de los siete observados: 245/7 = 35,0, así que el sesgo es 35,0 − 45,0 = −10,0 euros (−22 %). La varianza de los siete es 100, con desviación 10,0. Imputando la media queda aproximadamente (7/10)·100 = 70, es decir una desviación de 8,37 frente a los 19,36 reales: la media sigue sesgada y encima cualquier intervalo saldrá falsamente estrecho.
:::

## Comprueba que lo sabes

:::quiz
p: En una encuesta, los que más ganan son los que menos contestan la pregunta de ingresos. ¿Qué mecanismo es y qué implica?
o: MCAR, así que borrar esas filas da una estimación insesgada de la media
o: MNAR, porque la ausencia depende del propio valor que falta, y ningún método estándar lo corrige sin supuestos adicionales
o: MAR, porque el salario se puede estimar a partir de las demás variables
a: 2
e: La ausencia depende del valor no observado del ingreso, que es la definición de MNAR. MCAR exigiría independencia total y MAR permitiría corregir si la ausencia dependiera solo de variables observadas. Con MNAR se hace análisis de sensibilidad, no una corrección estándar.
:::

:::quiz
p: Imputas el 30 % de los valores de una variable por su media. ¿Qué le pasa a la varianza y a las correlaciones de esa variable?
o: La varianza se mantiene porque la media no cambia, y las correlaciones también
o: La varianza se reduce aproximadamente en la proporción de valores imputados y las correlaciones se atenúan hacia cero
o: La varianza aumenta porque se añaden observaciones
a: 2
e: Cada valor imputado es la misma constante, así que no aporta dispersión: la varianza queda multiplicada aproximadamente por la fracción observada. Y como esa constante es igual para todos los huecos, no covaría con ninguna otra variable y las correlaciones se acercan a cero.
:::

:::quiz
p: ¿Por qué no basta con mirar el porcentaje de valores ausentes para decidir si un análisis es fiable?
o: Porque el porcentaje siempre se calcula mal
o: Porque lo que sesga el resultado es el mecanismo de ausencia, no su cantidad: un 2 % de ausencias concentrado en los casos extremos rompe la estimación
o: Porque los nulos solo importan en las variables categóricas
a: 2
e: Un 2 % de ausencias entre los clientes más grandes cambia la media y cualquier conclusión de negocio, mientras que un 30 % MCAR solo reduce la precisión. El porcentaje informa de cuánta información pierdes; el mecanismo, de si esa pérdida es sesgada.
:::
