---
id: confusores-y-dag
titulo: Confusores, mediadores y DAG
fase: 2
nivel: avanzado
rutas: [ds, core]
prerequisitos: [causalidad-vs-correlacion, correlacion-pearson-spearman]
tags: [causalidad, confusores, dag, ajuste]
resumen: Dibujar el grafo causal antes de tocar la regresión decide qué variables ajustar y, sobre todo, de cuáles no hay que tocar nada.
fuentes: ["Pearl (1995), 'Causal Diagrams for Empirical Research'", "Hernán, Hernández-Díaz y Robins (2004), 'A Structural Approach to Selection Bias'"]
---

## En una frase

Un DAG es un dibujo de las relaciones causales que crees que existen entre tus variables, y sirve
para una cosa muy concreta: decidir qué variables hay que ajustar en el análisis y cuáles hay que
dejar fuera, porque ajustar de más introduce tanto sesgo como ajustar de menos.

## La idea

La receta habitual cuando alguien quiere estimar un efecto causal es «mete todo lo que tengas en
la regresión y así controlas por todo». Es una mala receta, y lo es por partida doble. Primero,
porque solo controlas lo que has medido. Y segundo, y más importante, porque **ajustar por la
variable equivocada puede crear un sesgo que antes no existía**.

Para saber qué hacer con una tercera variable `Z`, hay que saber qué papel juega entre el
tratamiento `T` y el resultado `Y`. Hay tres papeles y cada uno pide una cosa distinta:

- **Confusor**: `Z` causa `T` y también causa `Y` (es una causa común). Es la definición de libro,
  y aquí **sí hay que ajustar**. Ejemplo: la edad influye en si haces un curso y en cuánto cobras.
  Si no la separas, el efecto del curso se mezcla con el efecto de la edad.
- **Mediador**: `Z` está en medio de la cadena, `T → Z → Y`. Aquí **no hay que ajustar** si lo que
  quieres es el efecto total. Si un máster mejora tu salario precisamente porque te da acceso a
  una red de contactos, esa red es parte del mecanismo: ajustar por ella responde a otra pregunta
  («el efecto del máster que no pasa por la red»), no a la que suele interesar.
- **Colisionador**: `Z` es consecuencia de `T` y de `Y` a la vez (`T → Z ← Y`). Aquí **no hay que
  ajustar nunca**, y hacerlo es el error más contraintuitivo de los tres. Separar por un efecto
  común de dos variables independientes las vuelve dependientes entre sí.

Ese último punto merece un ejemplo cotidiano. El talento y la suerte son independientes: hay
gente con talento con suerte, sin suerte, y gente sin talento con y sin suerte. Ahora filtra por
«proyectos que salieron bien», que es un colisionador (para tener éxito basta con talento **o**
con suerte). Entre los proyectos exitosos, la correlación entre talento y suerte aparece negativa:
si un proyecto exitoso no tuvo talento, es casi seguro que tuvo suerte; y si tuvo talento, ya no
necesitaba suerte. Nadie ha creado esa relación en el mundo: la ha creado el filtro.

De ahí sale la herramienta: **dibuja el grafo antes de estimar nada**. El DAG no sale de los
datos (ningún algoritmo deduce la dirección de las flechas de una tabla de correlaciones). Sale de
tu conocimiento del dominio y del orden temporal. Una vez dibujado, el criterio de la puerta
trasera te dice exactamente qué conjunto de variables ajustar.

:::figura
fichero: dag-tres-papeles-de-z
pie: El mismo tercer nodo, tres papeles distintos. En el confusor hay que ajustar porque su efecto se mezcla con el del tratamiento; en el mediador, ajustar bloquea parte del mecanismo que se quiere medir; en el colisionador, ajustar fabrica una relación que no existe en el mundo. La lista de columnas no decide: decide el dibujo.
fuente: figuras/confusores-y-dag-1.py
:::

## Definición formal

Un **DAG** (grafo dirigido acíclico) tiene un nodo por variable y una flecha por influencia causal
directa, sin ciclos. Un **camino** es cualquier secuencia de flechas que conecta `T` con `Y`, sin
importar la dirección de cada flecha. En un camino, un nodo intermedio puede ser:

- una **cadena** (`→ Z →`) o una **bifurcación** (`← Z →`), o
- un **colisionador** (`→ Z ←`).

**Bloqueo.** Un conjunto de variables `S` bloquea un camino si contiene algún nodo intermedio de
tipo cadena o bifurcación, o si **no** contiene ningún colisionador del camino ni descendiente de
él. La regla del colisionador se invierte respecto a la intuición: para bloquear un camino hay que
**dejar fuera** el colisionador.

**Criterio de la puerta trasera.** Un conjunto `S` sirve para estimar el efecto causal de `T`
sobre `Y` si:

1. bloquea **todos** los caminos de `T` a `Y` que empiezan con una flecha que entra en `T`
   (los «caminos traseros», que son los no causales), y
2. no contiene **ningún descendiente de `T`** (esto es lo que prohíbe ajustar por mediadores).

Si `S` cumple las dos condiciones, el efecto causal se calcula con la **fórmula de ajuste**:

:::formula
E[Y | do(T = t)] = Σ_c E[Y | T = t, C = c] · P(C = c)
:::

- `do(T = t)` — intervención que fija `T` en el valor `t` en toda la población.
- `C` — el conjunto de variables de ajuste; `c` recorre sus valores.
- `E[Y | T = t, C = c]` — la media de `Y` dentro del estrato, que sí se estima con datos.
- La suma pondera cada estrato por su frecuencia, que es lo que reconstruye la población completa.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `do(T = t)` | Intervención que fija el tratamiento en `t` en toda la población, en vez de observarlo | 0 o 1 si `T` es binario | No es una cantidad que suba: es lo que se quiere estimar. Si `T` toma varios valores, la fórmula se repite para cada uno |
| `C` | Conjunto de variables por las que se ajusta: las que bloquean los caminos traseros | lista de variables | Meter más variables no es más seguro: si entra un mediador se bloquea parte del efecto y si entra un colisionador se abre un camino que estaba cerrado |
| `c` | Un valor concreto de `C`, es decir, un estrato | las de `C` | Cuantos más estratos, menos datos en cada uno: la media del estrato se vuelve ruidosa y el promedio, inestable |
| `E[ Y dado T = t, C = c ]` | Media de `Y` dentro de un estrato, lo único que se calcula con datos | las de `Y` | Es la pieza estimable; si un estrato se queda sin observaciones no hay nada que promediar y el resultado sale `nan` |
| `P(C = c)` | Peso del estrato en la población | probabilidad, suman 1 | Si los pesos de la muestra no son los de la población, el promedio reconstruye otra población distinta |
| `E[Y dado do(T = t)]` | El efecto causal buscado | las de `Y` | La diferencia entre `t = 1` y `t = 0` es el efecto medio; solo vale si `C` cumple las dos condiciones |
| `T`, `Y`, `Z` | Tratamiento, resultado y la tercera variable de turno | — | El papel de `Z` (confusor, mediador o colisionador) decide si entra en `C`; su nombre o su correlación con `Y` no lo deciden |
:::

El efecto causal medio es la diferencia entre `t = 1` y `t = 0` de esa expresión. En la práctica se
calcula estandarizando: se estima el efecto dentro de cada estrato y se promedia ponderando por el
tamaño del estrato (o se ajusta por regresión con `C` como covariables, que es una versión
paramétrica de la misma suma).

Dos avisos técnicos que aparecen en cuanto se trabaja con esto de verdad:

- **Sesgo por M**: ajustar por una variable que es colisionadora de dos causas no observadas abre
  un camino que estaba cerrado. Ni todos los confusores hay que ajustarlos, ni todas las
  covariables son inocentes.
- **Sobreajuste**: incluir variables que solo predicen `Y` no sesga el efecto, pero gasta grados de
  libertad y, con muestras pequeñas, aumenta la varianza del estimador. Ajustar por costumbre no es
  gratis.

## Ejemplo

Quieres estimar el efecto de la formación (`T`) sobre el salario (`Y`), y tienes la edad (`Z`).
La edad influye en ambas cosas, así que es un confusor y hay que ajustar. Los datos agregados:

```text
grupo      formacion   salario medio   personas
joven      con             24.000         200
joven      sin             21.000         100
mayor      con             36.000         100
mayor      sin             33.000         300
```

**Sin ajustar** (comparación bruta):

- Con formación: (200 · 24.000 + 100 · 36.000) / 300 = **28.000 €**.
- Sin formación: (100 · 21.000 + 300 · 33.000) / 400 = **30.000 €**.
- Diferencia bruta: **−2.000 €**. La formación parece *reducir* el salario.

**Ajustando por edad** (dentro de cada estrato y promediando):

- Jóvenes: 24.000 − 21.000 = **+3.000 €** (300 personas).
- Mayores: 36.000 − 33.000 = **+3.000 €** (400 personas).
- Efecto ajustado: (300 · 3.000 + 400 · 3.000) / 700 = **+3.000 €**.

El signo se invierte. La explicación: los jóvenes se formaron mucho más (200 de 300) y cobran
menos que los mayores. La comparación bruta confunde «ser joven» con «estar formado». Una vez
separas por edad, la formación suma 3.000 € en los dos grupos, y el promedio ponderado da +3.000 €.

El segundo bloque de código ilustra el caso contrario, el del colisionador: talento y suerte son
independientes en toda la población (correlación −0,001) y aparecen con correlación −0,501 si te
quedas solo con los que tuvieron éxito. Ajustar por el éxito, aquí, inventaría una relación
negativa entre el talento y la suerte que no existe en ninguna parte.

## Código

```python verificable
import pandas as pd

# Formacion (T), salario (Y) y edad (Z). Z influye en las dos: es un confusor.
filas = [
    ("joven", "con", 24000, 200),
    ("joven", "sin", 21000, 100),
    ("mayor", "con", 36000, 100),
    ("mayor", "sin", 33000, 300),
]
df = pd.DataFrame(filas, columns=["edad", "formacion", "salario", "n"])

def media(d):
    return (d["salario"] * d["n"]).sum() / d["n"].sum()

bruto = media(df[df.formacion == "con"]) - media(df[df.formacion == "sin"])
print(f"diferencia bruta {bruto:+,.0f}")             # -> diferencia bruta -2,000

# Fórmula de ajuste: efecto dentro de cada estrato, ponderado por su tamaño.
estratos = []
for edad, grupo in df.groupby("edad"):
    dif = media(grupo[grupo.formacion == "con"]) - media(grupo[grupo.formacion == "sin"])
    estratos.append((dif, grupo["n"].sum()))

pesos = sum(n for _, n in estratos)
print(f"diferencia ajustada {sum(d * n for d, n in estratos) / pesos:+,.0f}")
# -> diferencia ajustada +3,000
```

:::claves
- `df[df.formacion == "con"]` no escribe nada en `df`: devuelve un DataFrame nuevo y filtrado. Si en vez de leerlo intentaras asignar sobre esa selección (`df[df.formacion == "con"]["salario"] = 0`), pandas avisaría de que estás escribiendo en una copia y el cambio se perdería.
- `df.groupby("edad")` no devuelve un DataFrame sino un objeto agrupado que hay que recorrer. En cada vuelta, `grupo` conserva los **índices originales** del `df` (0 y 1, 2 y 3), no 0 y 1: si luego se cruzan resultados por índice, las filas se emparejan mal.
- `media()` divide entre `d["n"].sum()`, así que es una media **ponderada** por personas. Con el `.mean()` de pandas cada fila pesaría lo mismo, y como cada fila es una combinación de edad y formación, daría otro número: la pregunta sería «qué diferencia media hay entre las cuatro casillas», no «cuánto suma la formación por persona».
- `sum(n for _, n in estratos)` recorre un generador, que se agota: si se guardara en una variable y se usara dos veces, la segunda valdría 0. El `_` es la diferencia que aquí no se usa; el nombre no tiene ningún efecto.
- Si a un estrato le faltara la fila «con» o la «sin», el filtro devolvería un DataFrame vacío y `media()` haría 0/0: pandas devuelve `NaN` sin lanzar error, el `print` imprime `nan` y el programa termina como si todo hubiera ido bien.
- `:+,.0f` pide tres cosas a la vez: signo siempre visible, separador de miles y ningún decimal. El separador que añade Python es la coma inglesa (`-2,000`), no el punto que se usa en el texto de la página.
:::

```python verificable
import numpy as np

# Talento y suerte son independientes; el exito ocurre si se da al menos uno.
# El exito es un colisionador (T -> E <- L) y condicionar en el crea la asociacion.
rng = np.random.default_rng(0)
talento = rng.integers(0, 2, 100_000)
suerte = rng.integers(0, 2, 100_000)
exito = (talento + suerte) >= 1

print(f"poblacion completa {np.corrcoef(talento, suerte)[0, 1]:+.3f}")
# -> poblacion completa -0.001
print(f"solo los exitosos  {np.corrcoef(talento[exito], suerte[exito])[0, 1]:+.3f}")
# -> solo los exitosos  -0.501
```

## Errores típicos

- **Ajustar por todo lo que tengas.** Es la práctica más extendida y la más peligrosa. Ajustar por
  mediadores cambia la pregunta (estimas el efecto directo, no el total) y ajustar por
  colisionadores abre caminos que estaban cerrados. El DAG decide, no la lista de columnas.
- **Confundir un confusor con una variable que predice el resultado.** Una variable que solo
  predice `Y` (por ejemplo, el código postal en un estudio de salarios) mejora la precisión del
  estimador, pero no corrige ningún sesgo. Llamarla confusor lleva a creer que sin ella el
  resultado está sesgado, y no es así.
- **Ajustar por un descendiente del tratamiento.** Meter en la regresión cualquier cosa medida
  después de la intervención es jugar a la ruleta: puede ser un mediador (bloqueas parte del
  efecto) o un colisionador (creas sesgo). La regla es mecánica: nada que venga después de `T`.
- **Deducir el DAG de los datos.** Ninguna tabla de correlaciones te dice la dirección de las
  flechas: `T → Y` e `Y → T` generan exactamente la misma matriz. Las flechas salen del
  conocimiento del dominio y del orden temporal.
- **Elegir el conjunto de ajuste probando combinaciones hasta que el resultado sea significativo.**
  Con suficientes combinaciones siempre hay una que da un p-valor bonito. Eso es
  [[multiplicidad-y-fdr|multiplicidad]] aplicada a la especificación del modelo.
- **Olvidar los confusores no medidos.** Si la causa común no está en los datos, ningún ajuste la
  arregla. El DAG sirve precisamente para verlo: si el grafo tiene una flecha desde una variable
  que no tienes, tu estimación no es causal, y la solución está en el diseño (aleatorizar, buscar
  un instrumento, usar un corte temporal), no en el modelo.
- **Leer los coeficientes de una regresión como causas por defecto.** Un coeficiente solo tiene
  lectura causal si el conjunto de ajuste cumple el criterio de la puerta trasera. Si no lo has
  argumentado, tienes una descripción condicional, no un efecto.
- **Confundir el criterio con «bloquear todos los caminos».** Hay que bloquear los traseros y
  **dejar abiertos** los delanteros: los caminos causales `T → … → Y` son exactamente lo que
  quieres medir.

## Comprueba que lo sabes

:::quiz
p: Quieres estimar el efecto de un máster sobre el salario y tienes una variable «acceso a red de contactos» que ocurre después del máster y que a su vez mejora el salario. ¿Qué haces con esa variable?
o: Ajustar por ella, porque predice el salario
o: No ajustar por ella si quieres el efecto total del máster, porque es un mediador
o: Ajustar por ella y también por todas las variables anteriores al máster
a: 2
e: La red de contactos es parte del mecanismo por el que el máster aumenta el salario (T -> M -> Y). Ajustar por un mediador bloquea el camino causal y estima solo el efecto directo, que es otra pregunta. Además el criterio de la puerta trasera prohíbe explícitamente incluir descendientes del tratamiento.
:::

:::quiz
p: En el ejemplo, la diferencia bruta es −2.000 € y la ajustada por edad es +3.000 €. ¿Qué ha pasado?
o: Que el ajuste por edad ha creado una relación que no existía
o: Que la edad es una causa común de la formación y del salario, y al no separarla se mezclaba el efecto de envejecer con el de formarse
o: Que la muestra es demasiado pequeña para decidir
a: 2
e: Los jóvenes se formaron mucho más y cobran menos: sin separar por edad, ese patrón se atribuye a la formación y hasta cambia el signo. Es la paradoja de Simpson vista como problema de confusión. Aquí la edad es confusor y ajustar es lo correcto.
:::

:::quiz
p: El bloque del colisionador da correlación −0,001 en toda la población y −0,501 entre los exitosos. ¿Qué significa?
o: Que el talento y la suerte están negativamente relacionados en la población
o: Que condicionar en un efecto común de dos variables independientes induce una asociación entre ellas
o: Que la simulación tiene un error, porque la correlación no debería cambiar
a: 2
e: El éxito ocurre si hay talento o suerte, así que es consecuencia de las dos. Al mirar solo los exitosos, la ausencia de una causa obliga a la presencia de la otra, y aparece una correlación negativa artificial. Es exactamente el sesgo que se introduce al ajustar por un colisionador o al analizar una muestra seleccionada.
:::

:::practica
enunciado: Quieres estimar el efecto de una campaña de precios (T) sobre la compra (Y). Tienes tres variables medidas: el histórico de compras del cliente (H, medido antes), el número de visitas a la web durante la campaña (V) y el canal de adquisición (C, medido antes). Dibuja el DAG y decide el conjunto de ajuste.
pista: Pregúntate para cada variable si es causa de T y de Y (confusor), si está en medio de la cadena T → … → Y (mediador) o si es consecuencia de T (descendiente).
solucion: El histórico H y el canal C se miden antes y razonablemente influyen tanto en recibir la campaña como en comprar: son confusores, hay que ajustar por los dos. Las visitas V ocurren después de la campaña y son parte del mecanismo (la campaña lleva tráfico y el tráfico compra): es un mediador, no se ajusta si quieres el efecto total, y desde luego es un descendiente de T, lo que lo excluye por el criterio de la puerta trasera. El conjunto de ajuste es {H, C}. Queda un supuesto sin comprobar: si existe una causa común de T y de Y que no has medido (por ejemplo, una promoción local que coincidió con la campaña), el estimador no será causal por mucho que ajustes.
:::

:::trampa
Una regresión con 30 covariables no es más causal que una con 3. Ajustar de más puede sesgar el
resultado, y el sesgo por colisionador no se detecta mirando el R² ni la significación: el modelo
se ve perfectamente sano y el coeficiente está mal.
:::
