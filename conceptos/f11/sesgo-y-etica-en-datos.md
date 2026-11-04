---
id: sesgo-y-etica-en-datos
titulo: Sesgo y ética en datos
fase: 11
nivel: avanzado
rutas: [alg, ds]
prerequisitos: [exactamente-una-vez, metricas-de-clasificacion, train-val-test]
tags: [etica, sesgo, equidad, auditoria]
resumen: Un modelo aprende lo que hay en los datos, incluidas las injusticias que ya existían: como detectar sesgo, que mide cada métrica y por qué no se cumplen todas.
fuentes: ["Barocas, Hardt y Narayanan (2023), 'Fairness and Machine Learning: Limitations and Opportunities'", "Kleinberg, Mullainathan y Raghavan (2016), 'Inherent Trade-Offs in the Fair Determination of Risk Scores'"]
---

## En una frase

Un modelo no es neutral por ser matemático: aprende los patrones que ya estaban en los datos y
los aplica a escala, así que la pregunta no es si tu modelo tiene sesgo, sino de qué tipo, a
quién perjudica y qué vas a hacer al respecto.

## La idea

Un hospital quiere predecir qué pacientes necesitan atención adicional y entrena con el
historial de gasto sanitario. El modelo aprende bien su tarea, pero descubre algo incómodo:
predice peor la necesidad real de los grupos que históricamente han tenido menos acceso al
sistema, porque **para ellos el gasto no mide la enfermedad, mide el acceso**. El modelo no ha
inventado nada; ha heredado una etiqueta que ya era injusta. El mismo patrón aparece en
cualquier decisión automatizada que se apoye en un historial generado por personas.

De ahí sale la primera lección: **el sesgo casi nunca está en el algoritmo, está antes**. Las
fuentes típicas son cuatro:

1. **Sesgo histórico.** Los datos reflejan decisiones pasadas (a quién se contrató, a quién se
   concedió un crédito). Un modelo que aprende de ellos reproduce esas decisiones.
2. **Sesgo de representación.** Tu muestra no cubre a toda la población: recoges datos por
   aplicación móvil y te falta la gente mayor; mides en tres ciudades y generalizas al país.
3. **Sesgo de medición o de etiqueta (proxy).** La variable que usas como verdad no mide lo
   que crees: el gasto en lugar de la enfermedad, el número de detenciones en lugar de la
   delincuencia, la nota de un examen en lugar de la capacidad. Un **proxy** es una variable
   observada que sustituye a la que te interesa, y siempre arrastra lo que arrastraba el
   sistema que la generó.
4. **Sesgo de agregación.** Un modelo que funciona bien en promedio puede fallar en un
   subgrupo concreto, y las medias lo esconden: es el mismo fenómeno que hace que una media
   global oculte comportamientos opuestos por segmento.

La segunda lección es que «equidad» no es un solo número. Hay varias definiciones, todas
razonables, y **no se pueden satisfacer a la vez** cuando las tasas base difieren entre
grupos: eso es un teorema, no una opinión. Por eso una auditoría sería empieza eligiendo
explícitamente qué definición importa para ese caso y documentando el porqué, en lugar de
declarar «el modelo es justo» porque una métrica salió bien.

La tercera: **el umbral es una decisión de negocio, no un parámetro técnico**. Bajar el umbral
de selección de un grupo solo se puede hacer a propósito, con una razón escrita y con alguien
que lo apruebe. Es exactamente el mismo tipo de decisión que poner un precio, y merece el
mismo nivel de escrutinio.

## Definición formal

Con dos grupos `A` y `B`, sea `Ŷ = 1` la decisión positiva del modelo (conceder, seleccionar,
derivar), `Y = 1` el resultado real que te interesa, y agrupa:

- **Paridad demográfica.** `P(Ŷ = 1 | A) = P(Ŷ = 1 | B)`. Misma tasa de selección.
- **Igualdad de oportunidades.** `P(Ŷ = 1 | Y = 1, A) = P(Ŷ = 1 | Y = 1, B)`. Misma tasa de
  verdaderos positivos **entre quienes de verdad cumplen la condición**.
- **Paridad predictiva.** `P(Y = 1 | Ŷ = 1, A) = P(Y = 1 | Ŷ = 1, B)`. Misma precisión de la
  predicción positiva.
- **Impacto dispar (regla del 80 %).** Un criterio práctico de las guías de igualdad laboral
  estadounidenses: si la tasa del grupo menos favorecido dividida entre la del más favorecido
  es menor que `0,8`, hay indicios de impacto adverso y toca justificarlo.

:::formula
paridad demográfica: P(Ŷ = 1 / A) = P(Ŷ = 1 / B)  ·  impacto dispar: tasa_peor / tasa_mejor ≥ 0,8
:::

Símbolos: `Ŷ` es la predicción o decisión del modelo; `Y` es el resultado real (la etiqueta);
`A` y `B` son los dos grupos comparados; `P(· / ·)` es una probabilidad condicionada;
`tasa_peor` y `tasa_mejor` son las tasas de selección de cada grupo.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `Ŷ` | La decisión del modelo: 1 es seleccionado, concedido o derivado | 0 o 1 | Hay más decisiones positivas: suben todas las tasas a la vez y la brecha entre grupos puede quedarse igual |
| `Y` | El resultado real que te interesa, la etiqueta | 0 o 1 | Es la verdad contra la que se mide todo; si `Y` es un proxy mal elegido, ninguna métrica de equidad arregla el daño |
| `A` y `B` | Los dos grupos que se comparan | etiquetas | Cambiar la definición de los grupos (barrio, turno, tramo de edad) cambia el resultado de todas las métricas |
| `P(Ŷ = 1 / A)` | Probabilidad de ser seleccionado si estás en el grupo A | tanto por uno | Al separarse de `P(Ŷ = 1 / B)` aparece la brecha que mide la paridad demográfica |
| `tasa_peor` / `tasa_mejor` | Tasas de selección del grupo menos y del más favorecido | tanto por uno | El cociente de impacto dispar sube hacia 1; al bajar se aleja del listón de 0,8 y hay más que explicar |
| `0,8` | Umbral de la regla del 80 % | tanto por uno | Por debajo se considera indicio de impacto adverso y toca justificarlo |
:::

El resultado que hay que tener presente: si `P(Y = 1 / A) ≠ P(Y = 1 / B)` (las tasas base
difieren) entonces **no existe** un clasificador que cumpla a la vez igualdad de oportunidades
y paridad predictiva, salvo en el caso trivial de un modelo perfecto. Es el resultado de
Kleinberg, Mullainathan y Raghavan. Elegir una métrica es renunciar a otra, y esa renuncia se
documenta.

:::truco
Antes de discutir métricas, pregunta si hace falta puntuar. Muchas decisiones se pueden tomar
con reglas explícitas y auditables, o con revisión humana sobre una lista corta, y entonces el
problema de equidad se vuelve un problema de política visible en lugar de un número escondido
dentro de un modelo. La opción «no usar un modelo aquí» casi nunca está sobre la mesa y
debería estarlo.
:::

## Ejemplo

Dos grupos, un filtro automático y estas cifras:

```
grupo  candidatos  seleccionados  tasa
A            1000            420  0,42
B             400            120  0,30
```

- La tasa del grupo A es 420 / 1.000 = **0,42** (el 42 %).
- La tasa del grupo B es 120 / 400 = **0,30** (el 30 %).
- Impacto dispar: 0,30 / 0,42 = **0,71**, por debajo de 0,8.

No es una prueba de discriminación, pero sí es una señal que exige explicación: o hay una
razón legítima y documentada por la que B cumple menos el criterio, o el filtro está capturando
algo que no debería. Fíjate también en algo importante del cálculo: la diferencia absoluta es
de 12 puntos porcentuales, pero el **número** de personas afectadas es 1000 · (0,42 − 0,30) =
120 candidatos. Un porcentaje pequeño sobre mucha gente es mucha gente.

:::figura
fichero: sesgo-impacto-dispar
pie: A la izquierda, las tasas de selección del ejemplo: A selecciona el 42 % de sus candidatos y B el 30 %, y el listón del 80 % de la mejor tasa queda en 0,336, por debajo del cual se sitúa B. A la derecha, el cociente de impacto dispar (0,71) frente al umbral de 0,8; el grupo de referencia vale siempre 1,00 porque es el denominador. Estar por debajo no prueba discriminación, pero obliga a explicar por qué B cumple menos el criterio y a revisar las variables que entran al modelo.
fuente: figuras/sesgo-y-etica-en-datos-1.py
:::

## Código

```python verificable
import pandas as pd

# Seleccion por grupo: cuantos candidatos pasan el filtro de cada 100.
seleccion = pd.DataFrame({
    "grupo":         ["A", "B"],
    "candidatos":    [1000, 400],
    "seleccionados": [420, 120],
})
seleccion["tasa"] = seleccion.seleccionados / seleccion.candidatos   # division fila a fila

mejor = seleccion.tasa.max()
seleccion["impacto"] = seleccion.tasa / mejor          # regla del 80 %: el mejor grupo es la referencia

print(seleccion.to_string(index=False))                # quita la columna del indice, que aqui no aporta
print("impacto dispar minimo:", f"{seleccion.impacto.min():.2f}")   # .2f redondea solo lo que se imprime
print("regla del 80 %:", "se cumple" if seleccion.impacto.min() >= 0.8 else "NO se cumple")
print("personas de diferencia:", int(seleccion.candidatos[0] * (seleccion.tasa[0] - seleccion.tasa[1])))
```

:::claves
- `seleccion["tasa"] = ...` **sí** modifica el DataFrame: le añade una columna. La división es fila a fila entre dos columnas (y da `float`), no una operación escalar.
- `.max()` reduce toda la columna a un número y `seleccion.tasa / mejor` divide **cada** fila por ese mismo número. La fila del grupo A queda exactamente en 1,00 porque es el denominador: el mejor grupo se convierte en la referencia.
- `to_string(index=False)` quita la columna del índice; sin ese argumento pandas imprime además el índice (0 y 1) y puede abreviar columnas con `...` si no caben en el ancho de la consola.
- El `:.2f` redondea solo el texto que se imprime: en la columna sigue el valor con todos sus decimales, y la comparación `>= 0.8` usa el valor sin redondear. Un 0,795 se imprime como «0,80» y aun así no cumple.
- `seleccion.candidatos[0]` busca la **etiqueta** 0 del índice, no la posición: funciona porque el índice es 0 y 1. Si el DataFrame viniera filtrado, esa misma línea daría `KeyError`; `.iloc[0]` pide siempre la primera fila.
- `int(...)` **trunca** hacia cero, no redondea: un 119,9999999 por error de coma flotante se imprime como 119. Para contar personas conviene `round(...)` antes.
:::

```python ilustrativo
# Auditoria minima antes de poner un modelo en produccion: medir por subgrupo,
# no solo en el agregado. Con scikit-learn y un dataframe ya cargado.
from sklearn.metrics import confusion_matrix

for grupo in df["grupo"].unique():
    sub = df[df.grupo == grupo]          # mascara booleana: devuelve un DataFrame nuevo, no una vista
    vn, fp, fn, vp = confusion_matrix(sub["real"], sub["predicho"]).ravel()
    # ravel() aplana la matriz en el orden [[vn, fp], [fn, vp]]: si cambias el orden, las cuentas se cruzan.
    print(grupo,
          "tasa de seleccion", round((vp + fp) / len(sub), 3),
          "sensibilidad", round(vp / (vp + fn), 3),   # falla con ZeroDivisionError si el subgrupo no tiene positivos
          "falsos positivos", round(fp / (fp + vn), 3))
```

## Errores típicos

- **Quitar la variable protegida y creer que el problema está resuelto.** Si borras el código
  postal, el modelo encuentra el mismo patrón en otras variables correlacionadas (tipo de
  vivienda, centro de salud, idioma declarado). Eso son **variables proxy**, y funcionan igual
  de bien para discriminar. Medir el resultado por grupo es lo único que revela el problema.
- **Mirar solo la métrica agregada.** Un AUC de 0,85 global puede convivir con un rendimiento
  pésimo para un subgrupo que representa el 5 % de los datos. Desagrega siempre por los grupos
  que importan antes de dar un modelo por bueno.
- **Confundir «el modelo es preciso» con «el modelo es justo».** Son propiedades distintas.
  Un modelo puede ser exacto y aun así dañar a un grupo de forma sistemática, sobre todo cuando
  la etiqueta es un proxy de algo que no quieres medir.
- **Optimizar una métrica de equidad sin decidir antes cuál.** Cambiar de métrica cuando los
  resultados no gustan es elegir la conclusión primero. Decide y documenta la definición al
  principio, con quien responde de las consecuencias.
- **Ignorar que la etiqueta viene de un sistema humano.** Etiquetas como «impagado»,
  «reincidente» o «bajo rendimiento» las producen personas con sus propios sesgos. Antes de
  modelar, pregunta cómo se generó la etiqueta y a quién pudo perjudicar ese proceso.
- **Poner el modelo en producción sin plan de vigilancia.** El mundo cambia y la composición
  de los grupos también; una auditoría de hace dos años no dice nada del modelo de hoy.
  Vigila las tasas por grupo con la misma seriedad que la exactitud global
  ([[monitorizacion-de-drift]]).

:::trampa
Un modelo que predice «riesgo» y se usa para decidir sobre personas **crea** los datos que
luego lo confirman: si deniegas créditos a un barrio, ese barrio tendrá menos historial
crediticio y parecerá más arriesgado la próxima vez. Es un bucle de realimentación. La única
forma de romperlo es reservar una parte aleatoria de decisiones favorables y medir el
resultado real, en lugar de medir lo que el propio sistema decidió.
:::

## Comprueba que lo sabes

:::quiz
p: Un filtro selecciona el 42 % del grupo A y el 30 % del grupo B. ¿Qué se puede afirmar con rigor?
o: Que el filtro discrimina al grupo B, y hay que retirarlo
o: Que hay un indicio de impacto dispar (0,71, por debajo de 0,8) que exige explicación y revisión de las variables
o: Que el grupo B tiene menos candidatos válidos por naturaleza, así que no hay nada que revisar
a: 2
e: El cociente de tasas es una señal que obliga a investigar, no una prueba de discriminación: puede haber una razón legítima y documentada. La primera opción salta a la conclusión y la tercera la descarta sin mirar; las dos son formas de no auditar.
:::

:::quiz
p: ¿Por qué eliminar la variable de grupo del conjunto de entrenamiento no garantiza un modelo justo?
o: Porque el modelo pierde precisión sin esa variable
o: Porque otras variables correlacionadas actúan como proxy y el modelo reconstruye el mismo patrón
o: Porque las librerías de machine learning vuelven a añadirla de forma automática
a: 2
e: La información del grupo está repartida por el resto de variables: código postal, tipo de contrato, dispositivo, centro sanitario. El modelo no necesita el campo explícito para separar por grupo. Por eso la comprobación se hace midiendo resultados por grupo, no borrando columnas.
:::

:::quiz
p: Igualdad de oportunidades y paridad predictiva exigen lo mismo. ¿Es posible cumplir las dos a la vez?
o: Sí, con un modelo suficientemente preciso y datos suficientes
o: No, salvo en el caso trivial de un modelo perfecto, cuando las tasas base de los grupos difieren
o: Sí, basta con ajustar el umbral de decisión de cada grupo
a: 2
e: Es un resultado de imposibilidad: con tasas base distintas no existe un clasificador que iguale a la vez la tasa de verdaderos positivos y la precisión. Ajustar umbrales por grupo mueve el problema de una métrica a otra, no lo elimina; por eso hay que elegir y documentar qué se prioriza.
:::
