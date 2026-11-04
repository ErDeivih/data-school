---
id: meta-labeling
titulo: Meta-etiquetado
fase: 9
nivel: experto
rutas: [quant, ds]
prerequisitos: [triple-barrera, metricas-de-clasificacion, umbrales-y-coste]
tags: [etiquetado, clasificacion, lopez-de-prado, tamano-de-posicion]
resumen: Un primer modelo decide la dirección de la apuesta y un segundo decide si merece dinero y cuánto: separa el lado del tamaño y sube la precisión.
fuentes: ["López de Prado (2018), 'Advances in Financial Machine Learning', cap. 3"]
---

## En una frase

El **modelo primario** decide el lado de la apuesta (comprar o vender) y el **modelo
secundario** decide si esa apuesta concreta merece dinero y cuánto: dos problemas distintos,
resueltos por dos modelos distintos.

## La idea

Imagina que tienes una regla que detecta bien los movimientos, pero que da muchas señales
falsas. Suena el 100 % de las veces que hay algo y también muchas veces que no hay nada. No
quieres tirarla: quieres un portero que, para cada señal, estime la probabilidad de que esa
señal concreta sea buena.

Eso es el meta-etiquetado. El primario puede ser cualquier cosa: una media móvil, un modelo de
gradiente boosting, una idea tuya, incluso un analista humano. El secundario es siempre lo
mismo: un clasificador binario que aprende a responder «¿acertó el primario esta vez?». La
etiqueta del secundario no es «¿sube o baja?», es «¿el primario tenía razón?».

Hay tres consecuencias prácticas que explican por qué merece la pena el trabajo extra:

1. **Sube la precisión sin tocar el primario.** Cada señal que el secundario rechaza es una
   operación que no pagas. En estrategias con costes, rechazar el 20 % de las operaciones malas
   suele valer más que mejorar el acierto del 60 % al 62 %.
2. **El tamaño de la posición sale gratis.** La probabilidad del secundario es una medida
   natural de confianza: puedes apostar más cuando dice 0,8 que cuando dice 0,55. Eso es
   [[tamano-de-posicion|dimensionar la posición]] por convicción, no por corazonada.
3. **Separas dos preguntas que se estorban.** Un solo modelo obligado a acertar dirección *y*
   momento tiene que repartir su capacidad entre las dos. Dos modelos especializados rinden más.

El precio a pagar es una condición que casi nadie respeta: **el primario y el secundario no
pueden compartir los datos con los que se ajustan**. Si entrenas el primario y luego generas las
etiquetas del secundario sobre esas mismas operaciones, el secundario aprende a confiar en un
primario que en esa muestra parece mucho mejor de lo que es. Aprenderá «si el primario dice
comprar con mucha seguridad, acierta», cuando esa seguridad es sobreajuste. En producción, esa
confianza se evapora y el secundario se queda sin nada que filtrar.

:::trampa
El meta-etiquetado no mejora la dirección: no convierte un primario malo en bueno. Si tu primario
tiene un área bajo la curva ROC de 0,5, el secundario aprenderá que la probabilidad de acierto es
la misma para todas las señales y filtrará al azar. Solo sirve cuando el primario tiene algo de
habilidad y su acierto depende de las condiciones.
:::

## Definición formal

Para cada evento `t`:

- `lado_t ∈ {−1, +1}` — lo que dice el primario: `+1` comprar, `−1` vender. Es una decisión
  conocida en el instante `t0` del evento.
- `y_t ∈ {−1, 0, +1}` — la etiqueta de [[triple-barrera|triple barrera]] del evento.
- `X_t` — las variables disponibles en `t0` (las mismas para los dos modelos).

La etiqueta del secundario y su modelo son:

:::formula
z_t = 1 si lado_t · y_t > 0, y 0 en caso contrario        p_t = P(z_t = 1 | X_t, lado_t)
:::

- `z_t` — la meta-etiqueta: 1 si el primario acertó, 0 si falló. Con `y_t = 0` (venció la
  barrera vertical) el producto vale 0 y la operación cuenta como fallo. Es la convención
  conservadora: no ganaste nada y ocupaste capital.
- `p_t` — la probabilidad estimada de acierto, salida del clasificador binario.
- `u` — el umbral de decisión: solo se opera si `p_t ≥ u`.
- `m_t` — el tamaño de la posición. La forma más simple es `m_t = lado_t · 1{p_t ≥ u}`;
  una versión más informada usa `m_t = lado_t · f(p_t)` con `f` creciente de 0 a 1.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `lado_t` | El lado que decide el primario en el evento `t`: `+1` comprar, `−1` vender | signo | No es un parámetro que se elija: lo fija el modelo primario |
| `y_t` | La etiqueta de triple barrera del evento: `+1`, `−1` o `0` si venció el plazo | signo | No se elige; sale de la regla de etiquetado |
| `X_t` | Las variables conocidas en `t0`, las mismas para los dos modelos | las de cada variable | Más variables dan al secundario más con qué separar, y más ocasiones de sobreajustar |
| `z_t` | La meta-etiqueta: `1` si el primario acertó, `0` si falló | 0 o 1 | No se elige; conviene mirar su media, porque si el primario acierta el 90 % la clase 0 es rara |
| `p_t` | La probabilidad de acierto que estima el clasificador secundario | entre 0 y 1 | Es una salida del modelo, no un mando: solo se puede calibrar |
| `u` | El umbral de decisión: solo se opera si `p_t ≥ u` | probabilidad | Sube la precisión y baja la cobertura; el valor esperado total tiene un máximo, y pasarse de `u` lo baja (en el ejemplo de la figura, de 322R a 121R) |
| `m_t` | El tamaño de la posición | contratos o fracción del capital | Con `m = lado · f(p)`, un `f` más agresivo concentra el riesgo en las pocas señales de `p` alta |
:::

La etiqueta `z` es **asimétrica**: no pregunta si el precio subió, pregunta si la apuesta del
primario funcionó. Un primario que siempre dice «comprar» tendrá `z = 1` justo cuando la etiqueta
de triple barrera sea `+1`, y el secundario aprenderá en qué condiciones eso pasa.

Dos métricas que hay que mirar juntas, porque una sola engaña:

- **Precisión**: de las operaciones que decides tomar, qué fracción acertó. Sube al subir `u`.
- **Cobertura** (o exhaustividad): qué fracción de todas las señales del primario tomas. Baja al
  subir `u`.

Elegir `u` es elegir un punto en esa curva, y la decisión correcta no es la que maximiza la
precisión sino la que maximiza el valor esperado, que depende de cuánto ganas cuando aciertas,
cuánto pierdes cuando fallas y cuánto cuesta operar. Ese razonamiento está en
[[umbrales-y-coste|elegir el umbral por coste]], no en la exactitud del clasificador.

:::figura
fichero: meta-etiquetado-precision-y-cobertura
pie: Arriba, las dos métricas del filtro: al subir el umbral la precisión (verde) sube y la cobertura (azul) baja, y ninguna de las dos decide sola. Abajo, el dinero total de esas mismas operaciones: tiene un máximo en el umbral 0,20 y desde ahí cae, así que el umbral que más acierta (0,80) no es el que más gana. Eliges el punto que maximiza el valor esperado, no el que maximiza la precisión.
fuente: figuras/meta-labeling-1.py
:::

## Ejemplo

Doce operaciones de un primario, con la etiqueta de triple barrera `y` y la probabilidad `p` del
secundario:

| # | lado | y | z | p |
| --- | --- | --- | --- | --- |
| 1 | +1 | +1 | 1 | 0,78 |
| 2 | +1 | −1 | 0 | 0,72 |
| 3 | −1 | −1 | 1 | 0,66 |
| 4 | +1 | +1 | 1 | 0,58 |
| 5 | −1 | +1 | 0 | 0,55 |
| 6 | −1 | −1 | 1 | 0,71 |

(y las seis restantes: filas 7 a 12 con `z` igual a 1, 0, 1, 1, 0, 1 y `p` igual a 0,83, 0,33,
0,62, 0,69, 0,44, 0,30.)

- El primario acierta 8 de 12: precisión 0,667.
- Con umbral `u = 0,5` el secundario toma 9 de las 12 señales (cobertura 0,75) y acierta 7 de
  ellas: precisión 0,778. Ha subido 11 puntos rechazando tres operaciones.
- Si cada acierto vale 1,6 veces lo que se pierde al fallar, el resultado sin filtro es
  8 · 1,6 − 4 · 1 = **8,8R** en 12 operaciones (0,733R por operación). Con el filtro:
  7 · 1,6 − 2 · 1 = **9,2R** en 9 operaciones (1,022R por operación). Ganas más dinero total
  operando menos veces, que es exactamente el objetivo.

Fíjate en el detalle que hace que esto funcione: las dos operaciones que el secundario rechaza
peor puntuadas (0,30 y 0,33) son fallos, y entre las que acepta está la número 2, que puntuaba
0,72 y falló. No hay ningún umbral que acierte con todas; se trata de mejorar la proporción, no
de acertar siempre.

## Código

```python verificable
import numpy as np

lado = np.array([1, 1, -1, 1, -1, -1, 1, 1, -1, 1, -1, -1])
y    = np.array([1, -1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1])
p    = np.array([0.78, 0.72, 0.66, 0.58, 0.55, 0.71, 0.83, 0.33, 0.62, 0.69, 0.44, 0.30])

z = ((lado * y) > 0).astype(int)      # etiqueta del secundario: acerto el primario?
toma = p >= 0.5                       # el secundario decide si se apuesta

print(f"primario: {z.sum()} aciertos de {z.size}  precision {z.mean():.3f}")   # -> 0.667
print(f"secundario: {toma.sum()} apuestas de {z.size}  precision {z[toma].mean():.3f}")  # -> 0.778
print(f"cobertura del filtro: {toma.mean():.3f}")   # -> 0.750
```

:::claves
- `lado * y` multiplica dos arrays elemento a elemento; `> 0` convierte el resultado en un array de booleanos y `.astype(int)` los pasa a 0 y 1. Es el idioma habitual para construir una etiqueta binaria, pero fíjate en que `False` es 0 y `True` es 1: si el producto vale 0 (venció la barrera vertical), la operación cuenta como fallo, que es la convención conservadora.
- `z.sum()` y `z.mean()` sobre un array de 0 y 1 dan el número de aciertos y la precisión, porque la media de unos y ceros **es** la proporción de unos. No hace falta contar a mano.
- `p >= 0.5` no devuelve índices ni filas: devuelve una **máscara** booleana de la misma longitud que `p`. Por eso `z[toma]` selecciona solo las posiciones donde la máscara es cierta, y lo que devuelve es una **copia** con esas posiciones, no una vista que comparta memoria con `z`.
- Ese filtrado tiene una trampa de tamaño: `r_multiple[toma].mean()` no divide entre las 12 operaciones, divide entre las que han pasado el filtro. Comparar la media filtrada con la no filtrada sin mirar `toma.sum()` es comparar dos muestras de tamaño distinto; el total (`r_multiple[toma].sum()`) es lo que responde a «¿gano más dinero?».
- El umbral `0.5` es una decisión de negocio, no una constante del problema: cambiarlo por `0.4` mete más operaciones y cambia las dos cifras. Se comprueba en una línea: `print(z[p >= 0.4].mean(), (p >= 0.4).mean())`.
- Las tres variables son arrays distintos alineados por posición: la operación 4 es la cuarta en `lado`, en `y` y en `p`. Si una de las tres listas se construye en otro orden (por ejemplo, ordenando las señales por probabilidad), las etiquetas dejan de corresponder a su operación y el resultado sale plausible y falso. La comprobación es que `lado.size == y.size == p.size` y que las seis filas de la tabla del ejemplo cuadren una a una.
:::

```python verificable
import numpy as np

lado = np.array([1, 1, -1, 1, -1, -1, 1, 1, -1, 1, -1, -1])
y    = np.array([1, -1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1])
p    = np.array([0.78, 0.72, 0.66, 0.58, 0.55, 0.71, 0.83, 0.33, 0.62, 0.69, 0.44, 0.30])

z = ((lado * y) > 0).astype(int)
toma = p >= 0.5

r_multiple = np.where(z == 1, 1.6, -1.0)     # 1,6R si acierta, -1R si falla
print(f"sin filtro  E[R] {r_multiple.mean():+.3f}  operaciones {z.size}")       # -> +0.733
print(f"sin filtro  total {r_multiple.sum():+.1f}R")                          # -> +8.8R
print(f"con filtro  E[R] {r_multiple[toma].mean():+.3f}  operaciones {toma.sum()}")  # -> +1.022
print(f"con filtro  total {r_multiple[toma].sum():+.1f}R")                    # -> +9.2R
```

## Errores típicos

- **Generar las meta-etiquetas con un primario entrenado en los mismos datos.** Es la fuga
  clásica de este método: el secundario aprende a calibrar el sobreajuste del primario, que no
  existe fuera de la muestra. El primario se ajusta en unos datos y las meta-etiquetas del
  secundario se generan con predicciones de otro tramo (o de un esquema con purga).
- **Etiquetar el meta con el signo del retorno a horizonte fijo.** Si el primario opera con stop
  y objetivo, el resultado que importa es el de la triple barrera. Mezclar una regla de salida
  con una etiqueta de otro tipo hace que el secundario aprenda a filtrar operaciones que no vas a
  hacer.
- **Confundir «mejor precisión» con «mejor modelo».** Filtrar siempre sube la precisión si subes
  el umbral: con `u = 0,95` a lo mejor tomas una operación y aciertas. Lo que hay que enseñar es
  la curva completa de precisión y cobertura, y el valor esperado por operación en cada punto.
- **Elegir el umbral en la misma muestra donde lo evalúas.** Probar 20 umbrales y quedarte con el
  mejor es [[data-snooping-y-multiple-testing|selección sobre ruido]]. Reserva un tramo para
  elegir el umbral y otro, que no hayas tocado, para reportar.
- **Olvidar que las operaciones del secundario siguen solapándose.** Las etiquetas vienen de
  operaciones que duran varios días; el secundario necesita
  [[sample-weights|pesos por unicidad]] y [[purged-kfold|purga en la validación]] igual que
  cualquier otro modelo de esta familia. El meta-etiquetado no exime de nada.
- **Ignorar que el secundario puede tener muy pocos positivos.** Si el primario acierta el 90 %
  de las veces, la clase 0 es rara y el clasificador aprende a decir 1 casi siempre. Ahí el
  problema no es filtrar, es dimensionar: usa la probabilidad para el tamaño y no para decidir.

:::practica
enunciado: Diez señales de un primario, con meta-etiqueta z = 1, 1, 0, 1, 0, 1, 0, 1, 0, 1 y probabilidad del secundario p = 0,75; 0,62; 0,68; 0,55; 0,81; 0,71; 0,45; 0,59; 0,52; 0,66. Cada acierto vale 1,5R y cada fallo −1R. Con umbral u = 0,70, calcula precisión, cobertura y total en R, y compáralo con no filtrar.
pista: Acepta solo las señales con p ≥ u y separa la precisión (aciertos entre las aceptadas) de la cobertura (aceptadas sobre el total).
solucion: Sin filtro acierta 6 de 10, precisión 0,60, y suma 6 · 1,5 − 4 · 1 = 5,0R. Con u = 0,70 acepta 3 señales (0,75; 0,81; 0,71), cobertura 0,30; dos aciertan, precisión 0,667, y el total cae a 2 · 1,5 − 1 = 2,0R. Sube el resultado por operación, de 0,50R a 0,667R, pero deja menos dinero total.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué aprende exactamente el modelo secundario del meta-etiquetado?
o: A predecir la dirección del precio, igual que el primario pero con más datos
o: A predecir si la apuesta concreta del primario va a resultar ganadora, dadas las variables y el lado elegido
o: A elegir entre las predicciones de varios modelos primarios
a: 2
e: El secundario no predice el mercado: predice el acierto del primario, que es una pregunta condicionada al lado que ya ha elegido el primario. Por eso su etiqueta se construye con lado multiplicado por la etiqueta de triple barrera, y por eso no mejora a un primario sin habilidad.
:::

:::quiz
p: Un primario se entrena con datos de 2015 a 2020 y las meta-etiquetas se generan prediciendo esos mismos años. ¿Qué pasa?
o: Nada, el secundario necesita ver todos los datos para calibrar bien
o: El secundario aprende a confiar en un primario que en esa muestra parece mejor de lo que es, y su probabilidad deja de ser válida fuera de la muestra
o: El secundario se vuelve más conservador y rechaza todas las señales
a: 2
e: Las predicciones dentro de la muestra están infladas por el sobreajuste. El secundario aprende la relación entre ese sobreajuste y el acierto, que es un artefacto de la muestra. La solución es generar las meta-etiquetas con predicciones de un tramo distinto, idealmente con validación purgada.
:::

:::quiz
p: El secundario rechaza 3 de cada 12 señales y la precisión pasa de 0,667 a 0,778. ¿Cómo se decide si merece la pena?
o: Solo con la precisión: si sube, siempre merece la pena
o: Comparando el valor esperado total con y sin filtro, que depende de cuánto se gana al acertar, cuánto se pierde al fallar y de los costes de operar
o: Con la exactitud del clasificador secundario
a: 2
e: La precisión puede subir rechazando operaciones que aportaban valor esperado positivo. Lo que decide es el total: en el ejemplo se pasa de 8,8R en 12 operaciones a 9,2R en 9. Filtrar de más reduce el número de operaciones por debajo del punto en que el total deja de crecer.
:::

:::aviso
El meta-etiquetado añade un modelo, un umbral, un esquema de validación y una decisión de tamaño.
Es más superficie donde equivocarse. Si el primario ya tiene una precisión alta y estable, el
filtro aportará poco y el riesgo de sobreajustar el umbral será alto.
:::
