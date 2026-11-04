---
id: remuestreo-y-permutacion
titulo: Tests de permutación
fase: 2
nivel: avanzado
rutas: [ds, core]
prerequisitos: [contraste-de-hipotesis, p-valor, distribuciones-continuas, bootstrap]
tags: [permutacion, remuestreo, no-parametrico]
resumen: Construir la distribución nula barajando las etiquetas del propio experimento: un contraste exacto, sin supuestos de distribución y válido para casi cualquier estadístico.
fuentes: ["Fisher (1935), 'The Design of Experiments'", "Phipson y Smyth (2010), 'Permutation P-values Should Never Be Zero'", "Efron y Tibshirani (1993), 'An Introduction to the Bootstrap'"]
---

## En una frase

Un test de permutación construye la distribución nula barajando las etiquetas de los grupos en tus
propios datos: si las etiquetas no aportaran nada, cualquier reparto de valores entre los grupos
habría sido igual de plausible, así que el p-valor es la proporción de repartos que dan un resultado
al menos tan extremo como el observado.

## La idea

Tienes seis personas, tres en un grupo y tres en otro, y seis valores. La pregunta es si los grupos
son distintos. Un test de permutación razona así: si el grupo al que pertenece cada persona fuera
irrelevante, daría exactamente lo mismo haber repartido esos seis valores de cualquier otra forma.
Así que enumera **todos** los repartos posibles, calcula la diferencia de medias en cada uno y mira
en qué lugar cae el reparto que observaste. Si tu reparto es de los más extremos, es que algo pasa
con las etiquetas.

Este razonamiento tiene tres virtudes que ningún test de fórmula ofrece:

1. **No supone ninguna distribución.** No hay normalidad, ni igualdad de varianzas, ni tamaño
   mínimo. El único supuesto es la intercambiabilidad: bajo la nula, las etiquetas no aportan
   información.
2. **Vale para cualquier estadístico.** Diferencia de medias, de medianas, de varianzas, de
   percentiles, un AUC, un R², el coeficiente de una regresión, el número de veces que un grupo
   supera al otro. Si sabes calcularlo, sabes permutarlo. Eso lo hace especialmente útil en
   problemas donde la distribución del estadístico no se conoce en forma cerrada
   ([[tests-no-parametricos]]).
3. **Es exacto, no asintótico.** El nivel del test es exactamente `α` (hasta la granularidad de los
   repartos posibles) con cualquier tamaño de muestra, no «aproximadamente para `n` grande».

El precio es que hay que pensar en qué se baraja. Barajar etiquetas supone que los datos son
intercambiables bajo la nula, y eso se rompe en cuanto hay estructura:

- **Datos emparejados.** Si cada persona se mide dos veces (antes y después), las dos medidas de la
  misma persona no son intercambiables entre sí. La permutación correcta es **dentro de cada par**:
  cambiar el signo de la diferencia, elegido al azar. Es el test de los signos, y es el equivalente
  permutacional del test t de muestras relacionadas.
- **Bloques.** Si tienes varios hospitales o varios días, se permuta **dentro de cada bloque**, no
  entre bloques, para no destruir la estructura.
- **Series temporales.** Barajar el orden temporal destruye la autocorrelación y produce p-valores
  falsamente pequeños. Hay que permutar bloques de tiempo o no permutar.
- **Varianzas muy distintas.** Si un grupo tiene varianza diez veces mayor, permutar etiquetas deja
  de contrastar «mismas medias» y pasa a contrastar «misma distribución», y el test se vuelve
  sensible a la diferencia de varianzas. Con datos muy desiguales, usa un estadístico
  estudentizado.

Conviene no confundir este método con el [[bootstrap]], que es su pariente y responde a otra
pregunta. El bootstrap remuestrea **con reemplazo** de la muestra observada para aproximar la
distribución del estimador: sirve para poner un intervalo de confianza. La permutación reordena
etiquetas para aproximar la distribución del estadístico **bajo la nula**: sirve para contrastar. El
primero pregunta «¿cuánto varía mi estimación?»; el segundo, «¿es compatible lo que veo con que no
haya nada?».

## Definición formal

Tenemos `n` observaciones con un valor `xᵢ` y una etiqueta de grupo `zᵢ ∈ {A, B}`, con `n_A` en el
grupo A y `n_B = n − n_A` en el B. Sea `T(x, z)` el estadístico que mide la diferencia entre grupos.

- `T_obs = T(x, z)` — el valor observado del estadístico.
- `π` — una permutación de las etiquetas: reasigna los `zᵢ` entre las observaciones.
- `π(z)` — las etiquetas barajadas; los valores `xᵢ` no se tocan nunca.
- `B` — número de permutaciones de Monte Carlo generadas (por ejemplo 10.000).
- `b` — cuántas de esas `B` permutaciones dan un estadístico al menos tan extremo como el observado.
- `H₀` — hipótesis de intercambiabilidad: la distribución conjunta de `(x, z)` es invariante frente a
  cualquier reordenación de las etiquetas.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `T_obs` | El valor del estadístico en los datos, tal como se recogieron | las del estadístico | Es la referencia: cuanto más lejos cae de la nula, menos barajados lo alcanzan y más pequeño es el p-valor |
| `T(x, z)` | El estadístico elegido: diferencia de medias, de medianas, un AUC, un R² | las del estadístico | Se decide **antes** de mirar las permutaciones. Cambiarlo después de ver cuál gana es p-hacking: el p-valor deja de ser válido |
| `π(z)` | Las etiquetas barajadas. Los valores `x` no se tocan nunca | — | Es lo único que se mueve. Barajar los valores en vez de las etiquetas mide otra cosa y no lo que se cree |
| `B` | Número de permutaciones de Monte Carlo generadas | permutaciones | Sube la resolución: el p-valor mínimo alcanzable es `1/(B+1)` y el error de Monte Carlo baja como `1/√B` |
| `b` | Cuántas de esas `B` permutaciones dan un estadístico al menos tan extremo como el observado | permutaciones | Es el numerador del p-valor. Con `b = 0` no se informa 0, se informa `1/(B+1)`: subir `B` da resolución, redondear no |
| `p = (1+b)/(1+B)` | Proporción de repartos al menos tan extremos como el observado | probabilidad, entre 0 y 1 | Los dos `+1` cuentan el reparto observado como una permutación más; sin ellos, con `B = 200` y ningún extremo saldría `p = 0`, que una muestra finita no puede demostrar |
| `n_A`, `n_B` | Cuántas observaciones caen en cada grupo | observaciones | Fijan cuántos repartos existen, `C(n, n_A)`: con 3 contra 3 solo hay 20 y el p-valor más pequeño posible es `2/20 = 0,10` |
:::

El p-valor de Monte Carlo es:

:::formula
p = ( 1 + b ) / ( 1 + B )
:::

El `+1` no es un adorno. El reparto observado es uno de los repartos posibles, así que cuenta como
una permutación más (la identidad). Sin esa corrección, con `B = 200` y ningún reparto más extremo
que el observado saldría `p = 0`, es decir «imposible bajo la nula», algo que una muestra finita no
puede demostrar. Con la corrección, el p-valor mínimo alcanzable es `1/(B+1)`: con 10.000
permutaciones, `0,0001`.

Cuando `n` es pequeño se pueden enumerar **todas** las permutaciones y el test es exacto:

:::formula
Número de repartos distintos = C(n, n_A) = n! / ( n_A! · n_B! )
:::

donde `C(n, n_A)` es el número de formas de elegir qué `n_A` de las `n` posiciones llevan la etiqueta
A. Si `n = 6` y `n_A = 3`, son 20 repartos; con 5 por grupo y 10 observaciones en total, 252; con 10
por grupo y 20 en total, 184.756, cantidad ya incómoda para enumerar pero trivial para muestrear.

Dos consecuencias directas de la fórmula:

1. **La granularidad importa.** Con 20 repartos posibles, los p-valores solo pueden ser múltiplos de
   `1/20 = 0,05`. Con 3 contra 3, el p-valor bilateral más pequeño posible es `2/20 = 0,10`: ni con
   una separación perfecta puedes bajar de ahí. Un test de permutación con muestras diminutas no es
   «más potente» por ser exacto, simplemente no tiene resolución.
2. **El error de Monte Carlo se controla con `B`.** La desviación típica de la estimación de `p` es
   aproximadamente `√(p(1−p)/B)`. Con `B = 1.000` y `p = 0,05` ronda 0,007; para reportar tres
   decimales con comodidad hacen falta 10.000 permutaciones o más.

:::figura
fichero: permutacion-nula-y-granularidad
pie: Izquierda: la distribución nula no sale de una fórmula, sale de barajar las etiquetas 5.000 veces; el p-valor es la parte de esos barajados que cae en la zona roja, tan lejos como el valor observado. Derecha: con 3 piezas por grupo solo existen 20 repartos, así que los p-valores posibles son múltiplos de 0,05 y ni con una separación perfecta se baja de 0,10. La exactitud del método no crea resolución.
fuente: figuras/remuestreo-y-permutacion-1.py
:::

## Ejemplo

Tres piezas de un proveedor y tres de otro, con su resistencia medida:

```
proveedor A:  12  14  16
proveedor B:  20  22  24
```

Las medias son 14 y 22, así que `T_obs = 14 − 22 = −8`.

Solo hay `C(6,3) = 20` formas de repartir esos seis valores en dos grupos de tres. Puedo
enumerarlas a mano con un truco: la diferencia de medias depende solo de la suma del grupo A,
`T = (2·suma_A − 108) / 3`. Para que `/T/ ≥ 8` hace falta `suma_A ≤ 42` o `suma_A ≥ 66`.

- `suma_A = 12 + 14 + 16 = 42` → diferencia −8. Cuenta.
- `suma_A = 20 + 22 + 24 = 66` → diferencia +8. Cuenta.
- Cualquier otra combinación intermedia (46, 48, 50, 54, 58…) da una diferencia menor en valor
  absoluto.

Son 2 repartos de 20, así que `p = 2/20 = 0,10`. Con `α = 0,05` **no se rechaza** la igualdad, y no
porque los grupos no estén separados —están perfectamente separados— sino porque con tres
observaciones por grupo el test no puede dar un p-valor menor. Esa es la lección más útil de este
ejemplo: la exactitud del método no compensa la falta de datos.

## Código

```python verificable
import itertools
import numpy as np

a = np.array([12, 14, 16])
b = np.array([20, 22, 24])
todos = np.concatenate([a, b])
observado = a.mean() - b.mean()

# Enumeramos las C(6,3) = 20 formas de repartir los seis valores en grupos de tres
extremos = 0
for indice in itertools.combinations(range(6), 3):
    grupo = todos[list(indice)]
    resto = np.delete(todos, list(indice))
    if abs(grupo.mean() - resto.mean()) >= abs(observado) - 1e-9:
        extremos += 1

print(f"diferencia observada  {observado:.1f}")            # -> -8.0
print(f"repartos extremos     {extremos} de 20")           # -> 2 de 20
print(f"p-valor exacto        {extremos / 20:.2f}")        # -> 0.10
```

:::claves
- `itertools.combinations(range(6), 3)` genera cada grupo **una sola vez**: `(12, 14, 16)` sí y `(16, 14, 12)` no, porque el orden no importa. De ahí salen 20 grupos y no 120; si hicieran falta las dos ordenaciones, la función sería `permutations`.
- `todos[list(indice)]` es indexación con una lista y devuelve una **copia**; `np.delete(todos, list(indice))` también devuelve un array nuevo y más corto sin tocar `todos`. En cambio un corte como `todos[0:3]` sería una **vista** del mismo bloque de memoria: escribir dentro cambiaría `todos` sin avisar.
- El `- 1e-9` de la comparación es una tolerancia para la coma flotante. Sin ella, un reparto con exactamente la misma diferencia podría no contarse por un error de redondeo de 1e-16, y el p-valor saldría 0,05 en lugar de 0,10: el resultado cambiaría por un detalle invisible.
- Aquí **no** se aplica la fórmula `(b+1)/(B+1)` de la página: se enumeran los 20 repartos posibles, así que el observado ya está entre ellos y el cociente directo `2/20` es exacto. El `+1` hace falta cuando se muestrea, no cuando se enumera todo.
- `indice` es una **tupla**, no un número, aunque el nombre lo sugiera: `todos[list(indice)]` funciona porque NumPy acepta una lista de posiciones. Con la tupla directamente también funcionaría, pero `todos[0]` sería un único valor, no un grupo.
- `extremos / 20` es una división real (0,1) aunque los dos operandos sean enteros, y `:.2f` la escribe con dos decimales. Por eso la salida del programa dice `0.10` y el texto de la página dice `0,10`: el mismo número con otra convención.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(0)
grupo_a = rng.normal(0.30, 1.0, size=120)     # efecto real pequeno
grupo_b = rng.normal(0.00, 1.0, size=120)
todos = np.concatenate([grupo_a, grupo_b])
etiquetas = np.array([1] * 120 + [0] * 120)
observado = grupo_a.mean() - grupo_b.mean()

# Barajamos las etiquetas B veces: asi se genera la distribucion nula
B = 5000
extremos = 0
for _ in range(B):
    rng.shuffle(etiquetas)
    diferencia = todos[etiquetas == 1].mean() - todos[etiquetas == 0].mean()
    extremos += abs(diferencia) >= abs(observado)

# El +1 en numerador y denominador incluye el reparto observado: nunca da cero
print(f"diferencia observada  {observado:.4f}")              # -> 0.5073
print(f"permutaciones extremas {extremos} de {B}")          # -> 0 de 5000
print(f"p-valor Monte Carlo   {(extremos + 1) / (B + 1):.4f}")  # -> 0.0002
```

## Errores típicos

- **Permutar observaciones emparejadas como si fueran independientes.** Con medidas antes-después de
  las mismas personas, barajar todas las etiquetas rompe el emparejamiento y da p-valores
  equivocados. Hay que permutar dentro de cada par, cambiando el signo de la diferencia.
- **Aplicarlo a series temporales sin bloques.** El orden temporal no es intercambiable: barajarlo
  destruye la autocorrelación y produce p-valores demasiado pequeños. Permuta bloques contiguos o
  cambia de método ([[autocorrelacion-acf-pacf]]).
- **Reportar `p = 0`.** Ocurre cuando ninguna permutación supera al estadístico observado. El valor
  correcto es `(b + 1)/(B + 1)`, nunca cero, y si necesitas más resolución, sube `B` en lugar de
  redondear.
- **Usarlo con varianzas muy dispares creyendo que contrasta medias.** Con un grupo mucho más
  disperso, el test se vuelve sensible a esa diferencia de varianza. Si eso importa, usa un
  estadístico estudentizado o un test de Welch.
- **Confundirlo con el bootstrap.** Son cosas distintas: el bootstrap estima incertidumbre
  remuestreando con reemplazo, la permutación contrasta barajando etiquetas. Usar bootstrap para
  calcular un p-valor bajo la nula es un error conceptual frecuente.
- **Elegir el estadístico después de ver qué permutación gana.** El estadístico se decide antes,
  igual que la hipótesis. Probar diferencia de medias, de medianas y de percentil 90 y quedarse con
  el que da el p-valor más pequeño es p-hacking con otro nombre.

:::practica
enunciado: Barajas las etiquetas de un experimento con 400 observaciones 2.500 veces. En 120 de esas permutaciones la diferencia de medias es al menos tan extrema como la observada. Calcula el p-valor, su error de Monte Carlo con √(p(1−p)/B) y decide si puedes afirmar que estás por debajo de 0,05.
pista: El reparto observado cuenta como una permutación más, en el numerador y en el denominador, así que ni 120/2500 ni un p de cero son la respuesta.
solucion: p = (120 + 1) / (2500 + 1) = 121/2501 = 0,0484. El error de Monte Carlo es √(0,0484 · 0,9516 / 2500) = √0,0000184 = 0,0043, así que el p-valor real ronda el intervalo 0,044 a 0,053. Con esta resolución no puedes afirmar que esté por debajo de 0,05: sube B a 20.000 o informa del intervalo. El mínimo alcanzable es 1/2501 = 0,0004.
:::

## Comprueba que lo sabes

:::quiz
p: Con 3 observaciones por grupo y una separación perfecta entre los dos grupos, el test de permutación exacto da p = 0,10. ¿Por qué no da un p-valor menor?
o: Porque el test de permutación es menos potente que el test t
o: Porque solo hay C(6,3) = 20 repartos posibles y únicamente 2 son tan extremos como el observado, así que 2/20 es el mínimo alcanzable
o: Porque los grupos tienen distinta varianza
a: 2
e: La exactitud del método no crea resolución: con 20 repartos, los p-valores posibles son múltiplos de 0,05 y el mínimo bilateral es 2/20. No es una cuestión de potencia frente al test t ni de varianzas, es la granularidad de un espacio de permutaciones diminuto.
:::

:::quiz
p: ¿Por qué se usa la fórmula (b + 1) / (B + 1) en lugar de b / B?
o: Porque el reparto observado es una de las permutaciones posibles y contarlo evita reportar p = 0, que una muestra finita no puede demostrar
o: Porque así el p-valor siempre sale mayor que 0,05
o: Porque corrige por comparaciones múltiples
a: 1
e: El reparto observado es una configuración más de las etiquetas, así que forma parte de la distribución nula, y sin contarlo puede salir p = 0. El mínimo alcanzable pasa a ser 1/(B+1). No tiene nada que ver con el umbral del 5 % ni con la multiplicidad.
:::

:::quiz
p: Quieres contrastar el efecto de un fármaco midiendo a cada paciente antes y después. ¿Cómo se permuta?
o: Barajando todas las etiquetas antes-después entre todos los pacientes
o: Permutando dentro de cada paciente, es decir, decidiendo al azar si se cambia el signo de su diferencia
o: No se puede usar permutación con datos emparejados
a: 2
e: Las dos medidas de un mismo paciente no son intercambiables entre sí, pero sí lo son las dos etiquetas dentro del par, porque bajo la nula el orden es irrelevante. Eso da el test de los signos. Barajar entre pacientes destruye el emparejamiento y sí se puede usar permutación con datos emparejados.
:::
