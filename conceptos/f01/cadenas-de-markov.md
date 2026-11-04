---
id: cadenas-de-markov
titulo: Cadenas de Markov
fase: 1
nivel: intermedio
rutas: [core, ds, quant]
prerequisitos: [probabilidad-condicional, operaciones-matriciales]
tags: [markov, transiciones, credito]
resumen: Un sistema que salta entre estados sin memoria, y cómo su matriz de transición permite calcular a dónde irá y cuánto tardará en quedarse atrapado.
fuentes: ["Norris (1997), 'Markov Chains'", "Jarrow, Lando y Turnbull (1997), 'A Markov Model for the Term Structure of Credit Risk Spreads'"]
---

## En una frase

Una cadena de Markov es un proceso que en cada paso cambia de estado con probabilidades que solo
dependen del estado en el que está ahora, no de cómo llegó hasta él.

## La idea

Piensa en un préstamo. Cada mes está en uno de unos pocos estados: al día, 30 días de retraso, 60,
90 o impagado. La pregunta que interesa a un banco no es qué pasó con este préstamo en concreto,
sino qué fracción de los préstamos que están al día acabarán impagados, y cuánto tardarán.

La idea de Markov es tirar el historial y quedarse solo con el estado. Si un préstamo lleva 60
días de retraso, ¿importa si antes estuvo al día o ya estuvo en 90? Bajo el supuesto de Markov,
no: lo único que cuenta es que está en 60, y desde ahí las probabilidades de ir a cada estado son
las mismas para todos los préstamos que estén en 60. Es una simplificación fuerte, y es
precisamente lo que hace el modelo tratable.

Con esa renuncia se gana mucho. Toda la información del sistema cabe en una matriz: en la fila
`i`, las probabilidades de pasar del estado `i` a cada estado `j`. La diagonal dice la
probabilidad de quedarse donde está. Y como multiplicar matrices encadena transiciones, elevar la
matriz a `n` da las probabilidades a `n` pasos. No hace falta simular nada: el futuro está en una
potencia.

El detalle que cambia todo es el **estado absorbente**: una vez que un préstamo impaga, se queda
ahí para siempre. Su fila es `[0, 0, 1]`. Esos estados actúan como sumideros y son los que
permiten responder a la pregunta del principio: la probabilidad de acabar en el sumidero y el
tiempo esperado hasta llegar.

:::aviso
La cadena de Markov es un modelo, y su punto débil es el supuesto de homogeneidad: que las
probabilidades no cambian con el tiempo. En una crisis, la probabilidad de pasar de «al día» a
«30 días» no es la del año anterior. Estimar la matriz con una ventana que mezcla dos regímenes
produce una matriz que no describe ninguno de los dos.
:::

## Definición formal

Una cadena de Markov en tiempo discreto sobre un conjunto finito de estados `S` se define por su
matriz de transición `P`, con `p_ij = P(X_{t+1} = j | X_t = i)`, que cumple:

:::formula
p_ij ≥ 0        Σ_j p_ij = 1 para cada fila i
:::

Las probabilidades a `n` pasos salen de la ecuación de Chapman-Kolmogorov:

:::formula
P^(n) = P^n        P(X_{t+n} = j | X_t = i) = (P^n)_ij
:::

- `P` — matriz de transición de un paso; cada fila suma 1 porque desde un estado siempre se va a
  algún sitio.
- `n` — número de pasos; un paso puede ser un mes, un día o un año, según cómo esté construida.
- `P^(n)` — matriz de transición a `n` pasos.

El estimador de máxima verosimilitud es simplemente contar y normalizar:

:::formula
p̂_ij = n_ij / Σ_k n_ik
:::

donde `n_ij` es el número de transiciones observadas del estado `i` al `j`. La restricción de que
cada fila sume uno se cumple por construcción, así que el estimador es la frecuencia relativa.

**Estados absorbentes y tiempo esperado.** Si separas los estados transitorios (`Q`) de los
absorbentes, la matriz fundamental es `N = (I − Q)⁻¹`. La entrada `N_ij` es el número esperado de
pasos que se pasan en `j` antes de absorberse, empezando en `i`; sumando la fila se obtiene el
tiempo esperado hasta la absorción.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `P` | Matriz de transición de un paso | probabilidades por fila | Si la diagonal sube, los estados son más persistentes y todo tarda más en moverse |
| `n` | Número de pasos que se elevan | pasos | `P^n` se acerca al régimen estacionario o a la absorción, según la cadena |
| `Q` | Submatriz de transiciones entre estados transitorios | probabilidades | Si sus valores suben, cuesta más salir de la parte transitoria y el tiempo hasta absorción crece |
| `N` | Matriz fundamental `(I − Q)⁻¹` | pasos esperados | Su suma por filas es el tiempo esperado hasta absorberse: es la cifra que se lleva a una provisión |
:::

## Ejemplo

Tres estados: 0 (al día), 1 (30 días de retraso) y 2 (impagado, absorbente).

:::formula
P = [ 0,90  0,08  0,02 ;  0,20  0,60  0,20 ;  0  0  1 ]
:::

- Desde «al día»: 90 % sigue al día, 8 % pasa a 30 días, 2 % impaga directamente.
- Desde «30 días»: 20 % se recupera, 60 % sigue, 20 % impaga.
- Desde «impagado»: se queda impagado con probabilidad 1.

Al cabo de 12 meses, la primera fila de `P¹²` da 0,4545 de seguir al día y 0,4406 de haber
impagado. Y el tiempo esperado hasta el impago desde «al día» es `N` sumando la primera fila: 20
meses.

Una lectura útil para discutir con negocio: con estas transiciones, un préstamo al día tiene algo
menos de la mitad de probabilidad de acabar impagado en un año. Si ese número choca con la
intuición del equipo de riesgo, o la matriz está mal estimada o la intuición está calibrada con
otro ciclo.

## Código

```python verificable
import numpy as np

# Filas: estado de origen. Columnas: estado de destino. La ultima fila es absorbente.
P = np.array([[0.90, 0.08, 0.02],
              [0.20, 0.60, 0.20],
              [0.00, 0.00, 1.00]])

P12 = np.linalg.matrix_power(P, 12)
Q = P[:2, :2]                       # transiciones entre estados transitorios
N = np.linalg.inv(np.eye(2) - Q)    # matriz fundamental

print(f"al dia a 12 meses {P12[0, 0]:.4f}")        # -> al dia a 12 meses 0.4545
print(f"impago a 12 meses {P12[0, 2]:.4f}")        # -> impago a 12 meses 0.4406
print(f"meses hasta impago {N[0].sum():.2f}")      # -> meses hasta impago 20.00
print(f"filas suman {P.sum(axis=1)}")               # -> filas suman [1. 1. 1.]
```

La última línea no es decorativa: si una fila no suma uno, falta un estado o sobra probabilidad, y
todas las potencias que calcules después estarán mal sin avisar.

:::claves
- `np.linalg.matrix_power(P, 12)` multiplica la matriz por sí misma 12 veces, que es exactamente
  encadenar 12 transiciones. `P ** 12` eleva cada elemento al cuadrado doce veces y no significa
  nada.
- `P[:2, :2]` recorta los estados transitorios. Si incluyes el absorbente en `Q`, `I − Q` es
  singular y la inversa revienta con `LinAlgError`: es la forma en que el álgebra te avisa de que
  has metido un sumidero donde no toca.
- `N[0].sum()` suma la fila entera, no solo la diagonal. El tiempo esperado hasta absorberse es la
  suma de los pasos esperados en cada estado transitorio, no el paso esperado en el primero.
- `P.sum(axis=1)` comprueba que cada fila suma uno. Sin `axis=1` suma toda la matriz y da 3, que
  no dice nada sobre ninguna fila.
- Los elementos de `N` son **pasos**, no meses. Si la matriz es mensual, el tiempo sale en meses;
  si la construyes con datos anuales, en años. Cambiar la frecuencia sin reestimar la matriz es un
  error de escala.
:::

## Errores típicos

- **Estimar la matriz con cuatro transiciones.** Con pocas observaciones, muchas celdas salen a
  cero por falta de datos, no porque sean improbables. Una probabilidad de impago estimada con
  tres casos no es una probabilidad: es una anécdota.
- **Olvidar el estado absorbente.** Si no existe, la cadena puede vagar para siempre y la pregunta
  «¿cuándo acaba?» no tiene respuesta. En riesgo de crédito, el impago es absorbente por
  definición.
- **Suponer homogeneidad sin comprobarla.** La matriz estimada con 2019-2020 no describe 2022.
  Conviene estimar por ventanas y comparar; si las matrices difieren mucho, el modelo de un solo
  régimen es una ficción.
- **Confundir la probabilidad a un año con la de cinco.** `P¹²` y `P⁶⁰` no se obtienen
  multiplicando por cinco la primera. La absorción no es lineal: los que ya impagaron no vuelven.
- **Leer la diagonal como «estabilidad» sin mirar el resto.** Un 0,90 en la diagonal con un 0,08
  hacia el estado siguiente no es lo mismo que un 0,90 con un 0,02 de impago directo, y las dos
  filas suman uno.
- **Usar la cadena para predecir un préstamo concreto.** La cadena describe frecuencias de una
  población, no el destino de un caso. Para el caso individual, lo que hay es una probabilidad.

:::practica
enunciado: Con la matriz del ejemplo, calcula la probabilidad de que un préstamo que hoy está en 30 días de retraso esté impagado dentro de dos meses, y compárala con la de uno que hoy está al día.
pista: La segunda fila de P² da las probabilidades a dos pasos desde el estado 1.
solucion: P² en la fila 1 vale: a estado 0, 0,2·0,9 + 0,6·0,2 = 0,30; a estado 1, 0,2·0,08 + 0,6·0,6 = 0,376; a impago, 0,2·0,02 + 0,6·0,2 + 0,2 = 0,324. Desde «al día» el impago a dos meses es 0,9·0,02 + 0,08·0,2 + 0,02 = 0,054. La diferencia (32,4 % frente a 5,4 %) muestra por qué el estado actual pesa mucho más que el historial.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué significa que una fila de la matriz de transición no sume uno?
o: Que falta un estado de destino o que las probabilidades están mal estimadas
o: Que la cadena no es absorbente
o: Que el estado es transitorio
a: 1
e: Desde cualquier estado hay que ir a algún sitio, así que la suma de sus probabilidades de salida es uno. Si no suma uno, hay un destino que no has modelado o un error de estimación, y todas las potencias posteriores heredan el fallo.
:::

:::quiz
p: ¿Por qué no se puede estimar la probabilidad de impago a cinco años multiplicando por cinco la de un año?
o: Porque la absorción no es lineal: los que ya impagaron salen de la población y no vuelven a impagar
o: Porque las probabilidades no se pueden multiplicar nunca
o: Porque a cinco años siempre hay tipos distintos
a: 1
e: La probabilidad a cinco años es la entrada correspondiente de P⁶⁰, no cinco veces la de P¹². La diferencia es la misma que entre interés simple y compuesto: los que salen de la población dejan de contribuir.
:::
