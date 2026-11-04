---
id: regularizacion-l1-l2
titulo: Regularización L1 y L2
fase: 6
nivel: intermedio
rutas: [ds, quant]
prerequisitos: [regresion-lineal, sesgo-varianza, escalado-y-transformacion]
tags: [regularizacion, ridge, lasso, seleccion]
resumen: Ridge encoge los coeficientes y Lasso lleva algunos a cero: cómo la penalización cambia el equilibrio sesgo-varianza y cuándo usar cada una.
fuentes: ["Hoerl y Kennard (1970), 'Ridge Regression: Biased Estimation for Nonorthogonal Problems'", "Tibshirani (1996), 'Regression Shrinkage and Selection via the Lasso'"]
---

## En una frase

Regularizar es añadir a la función de pérdida un castigo por tener coeficientes grandes: Ridge
los encoge todos un poco y Lasso lleva algunos exactamente a cero, cambiando un poco de sesgo
por bastante menos varianza.

## La idea

Mínimos cuadrados tiene un problema conocido cuando las variables se parecen entre sí: si dos
predictoras contienen casi la misma información, la fórmula reparte el efecto de forma
caprichosa. Un coeficiente se queda con +5 y el otro con −4,8, y ambos números cambian por
completo si añades una fila más. La predicción conjunta es estable, pero los coeficientes
individuales son basura interpretativa.

Piensa en dos testigos que vieron lo mismo. Si les preguntas por separado, uno te dirá que el
sospechoso era alto y el otro que era bajito, pero la media de sus respuestas acierta. Lo que
falta es una regla que reparta la información de forma sensata.

La regularización es esa regla. Se añade a la suma de errores al cuadrado un término que crece
con el tamaño de los coeficientes, y se busca el equilibrio: ajustar bien los datos, pero sin
permitir que ningún coeficiente se dispare. La fuerza del castigo es el hiperparámetro `λ`
(lambda): con `λ = 0` estás en mínimos cuadrados puros; con `λ` enorme, todos los coeficientes
caen a cero.

La diferencia entre L1 y L2 está en **cómo** castigan. L2 (`λ` por la suma de cuadrados) reparte
el castigo de forma suave y proporcional: los coeficientes grandes se reducen más y ninguno
llega a cero. L1 (`λ` por la suma de valores absolutos) castiga igual a un coeficiente grande
que a uno pequeño, así que empuja los pequeños hasta anularlos del todo. Por eso Lasso además
**selecciona variables**: devuelve modelos con ceros, y un cero es una variable fuera.

La forma de la restricción lo explica de un vistazo. Con dos coeficientes, la restricción L2 es
un círculo y la L1 un rombo. Las curvas de nivel del error son elipses alrededor del óptimo sin
penalizar. La solución es donde la elipse toca por primera vez la región permitida, y el rombo
tiene vértices sobre los ejes: la elipse suele tocar en un vértice, es decir, con un coeficiente
exactamente igual a cero. El círculo no tiene esquinas, así que casi nunca toca justo en un eje.

## Definición formal

Sea `RSS = Σᵢ (yᵢ − ŷᵢ)²` la suma de residuos al cuadrado del modelo lineal. Los tres objetivos
son:

:::formula
Ridge:      RSS + λ · Σⱼ βⱼ²
Lasso:      RSS + λ · Σⱼ |βⱼ|
Elastic Net: RSS + λ · ( α · Σⱼ |βⱼ| + (1 − α)/2 · Σⱼ βⱼ² )
:::

- `βⱼ` — coeficiente de la variable `j`, sin contar el intercepto.
- `λ` — fuerza de la penalización, mayor o igual que cero. Se elige por validación cruzada.
- `Σⱼ` — suma sobre las `p` variables.
- `α` — en Elastic Net, mezcla entre L1 y L2: `α = 1` es Lasso puro y `α = 0` es Ridge puro.
- El intercepto `β₀` **no se penaliza**: desplazar la predicción no es complicar el modelo.

Ridge tiene solución cerrada, muy parecida a la de mínimos cuadrados pero con `λ` sumado en la
diagonal:

:::formula
β_ridge = (XᵀX + λ · I)⁻¹ Xᵀ y
:::

- `X` — matriz de datos estandarizada, sin columna de unos (el intercepto se trata aparte).
- `I` — matriz identidad del tamaño de `XᵀX`.
- Sumar `λ` a la diagonal es lo que hace que la matriz sea invertible aunque las variables sean
  colineales: por eso Ridge también arregla los casos en los que mínimos cuadrados no tiene
  solución única.

Lasso no tiene fórmula cerrada porque el valor absoluto no es derivable en cero. Se resuelve con
descenso por coordenadas: se optimiza un coeficiente cada vez manteniendo el resto fijos, y el
resultado es una regla de umbral blando que devuelve ceros exactos.

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `λ` | Fuerza de la penalización | adimensional, en unidades de `XᵀX` | Todos los coeficientes se encogen; a partir de cierto valor, Lasso los pone a cero y el modelo se queda vacio |
| `α` | Mezcla entre L1 y L2 en Elastic Net | de 0 (Ridge puro) a 1 (Lasso puro) | Mas cerca de 1, mas coeficientes exactamente cero y menos estables cuando hay variables correlacionadas |
| `βⱼ` | Coeficiente de la variable `j`, sin el intercepto | unidades de `y` por unidad de `xⱼ` | Con la penalización activa no puede crecer libremente: el castigo lo frena |
| `RSS` | Suma de residuos al cuadrado | unidades de `y` al cuadrado | Si sube, el modelo ajusta peor; la penalización se suma a esto, no lo sustituye |
| `p` | Numero de variables | columnas | Con `p` mayor que `n`, Lasso selecciona como mucho `n` variables aunque haya mas relevantes |
| `I` | Matriz identidad del tamaño de `XᵀX` | adimensional | No es un parámetro que se mueva: es lo que permite sumar `λ` a la diagonal y que la matriz sea invertible |
:::

## Ejemplo

Cien observaciones con tres variables estandarizadas: `x1` con efecto real, `x2` casi idéntica a
`x1` (correlación altísima) y `x3` ruido puro. La respuesta se generó con `y = 3·x1` más ruido.
Sin penalización, el síntoma clásico de la colinealidad:

```
OLS    3.386 -0.530  0.012
Lasso  2.758  0.000  0.000
Ridge  2.102  0.739  0.007
```

Mínimos cuadrados reparte el efecto entre las dos variables gemelas con signos opuestos: `x1`
se lleva 3,386 y `x2` resta 0,530. La predicción conjunta es buena, pero los coeficientes no
hay quien los lea: el efecto real era 3,0 en una sola variable. Lasso se queda con `x1` y anula
las otras dos. Ridge reparte entre las dos primeras y deja la tercera casi en cero sin llegar a
serlo.

Para ver el encogimiento continuo, el mismo par de variables colineales solas, con la fórmula
cerrada a la izquierda y scikit-learn a la derecha:

```
lambda   0.0  manual [ 3.382 -0.527]  sklearn [ 3.382 -0.527]
lambda   1.0  manual [ 2.101  0.740]  sklearn [ 2.101  0.740]
lambda  10.0  manual [ 1.458  1.260]  sklearn [ 1.458  1.260]
lambda 100.0  manual [ 0.961  0.940]  sklearn [ 0.961  0.940]
```

Con `λ = 0` se recupera mínimos cuadrados, con sus dos coeficientes de signo contrario. Con
`λ = 10` el efecto se reparte (1,458 y 1,260) y con `λ = 100` los dos convergen hacia el mismo
valor. Ridge nunca pone un cero: encoge y reparte. Que la fórmula cerrada y la librería
coincidan dígito a dígito es una buena comprobación de que entiendes qué hace el `alpha` que le
pasas a `Ridge` cuando el intercepto ya está fuera del modelo.

:::figura
fichero: regularizacion-caminos-l1-l2
pie: Los dos primeros paneles son el mismo experimento con dos castigos distintos. En L1, la variable gemela y la de ruido llegan a cero exacto al subir α: la restricción es un rombo con vértices sobre los ejes y la elipse del error suele tocar ahí. En L2 nada toca el cero, solo se encogen: el círculo no tiene esquinas. El tercer panel compara los tres métodos con la misma escala: mínimos cuadrados reparte el efecto entre las dos variables gemelas con signos opuestos, Lasso se queda con una y anula las demás, y Ridge reparte sin anular. Más castigo no es siempre mejor: lo que decide es qué tipo de castigo usas.
fuente: figuras/regularizacion-l1-l2-1.py
:::

## Código

```python verificable
import numpy as np
from sklearn.linear_model import Lasso, LinearRegression, Ridge

rng = np.random.default_rng(0)
n = 100
x1 = rng.normal(size=n)
x2 = 0.95 * x1 + rng.normal(scale=0.1, size=n)   # casi colineal con x1
x3 = rng.normal(size=n)                          # ruido puro
X = np.column_stack([x1, x2, x3])
y = 3 * x1 + rng.normal(scale=0.5, size=n)

# Penalizar sin estandarizar castiga mas a la variable con menos escala.
X = (X - X.mean(axis=0)) / X.std(axis=0)   # axis=0: una media por columna, no por fila

for nombre, modelo in (("OLS  ", LinearRegression()),
                       ("Lasso", Lasso(alpha=0.1, max_iter=10000)),   # L1: anula coeficientes
                       ("Ridge", Ridge(alpha=1.0))):                  # L2: solo los encoge
    modelo.fit(X, y)
    coef = " ".join(f"{c:6.3f}" for c in modelo.coef_)   # coef_ es un array, no un numero
    print(f"{nombre} {coef}")
# -> OLS    3.386 -0.530  0.012
# -> Lasso  2.758  0.000  0.000
# -> Ridge  2.102  0.739  0.007
```

:::claves
- `X = (X - X.mean(axis=0)) / X.std(axis=0)` reasigna la variable `X` en el sitio: a partir de
  ahi `X` ya no son los datos crudos. Si necesitas los originales después, guardalos antes con
  una copia, porque la línea original se pierde.
- `axis=0` significa «una media por **columna**», que es lo que quieres para estandarizar
  variables. Con `axis=1` calcularia la media de cada fila, es decir, la media de las tres
  variables de un mismo alumno: un número sin sentido y un resultado que no falla, solo empeora.
- `X.std(axis=0)` usa `ddof=0` por defecto en NumPy (divide entre `n`), mientras que pandas usa
  `ddof=1`. Con `n = 100` la diferencia es del 0,5 %: no cambia ninguna conclusión, pero explica
  por qué los coeficientes no coinciden digito a digito con los de otro programa.
- `modelo.coef_` es un **array de NumPy**, y `f"{c:6.3f}"` lo formatea a seis caracteres con tres
  decimales. `Lasso` escribe `0.000`, no `0`: un cero de verdad y un número pequeño se imprimen
  igual, así que para comprobar la selección hay que mirar `coef_ == 0`, no el texto.
- `Ridge(alpha=lam, fit_intercept=False)` no es obligatorio en la comparación, pero deja el
  ajuste en la forma exacta de la fórmula cerrada. La `X` ya va centrada, así que el intercepto
  se lleva la media de `y` y no toca los coeficientes: con `fit_intercept=True` salen los mismos
  números en `coef_` y el intercepto se queda con la media de `y`.
- Cambia `Lasso(alpha=0.1)` por `alpha=0.5`: `x1` baja de 2,758 a 2,358 y las otras dos
  siguen en cero. Sube a `alpha=16` y los tres coeficientes son cero: la penalización se ha
  comido el modelo entero y la predicción es la media de `y`.
:::

```python verificable
import numpy as np
from sklearn.linear_model import Ridge

rng = np.random.default_rng(0)
n = 100
x1 = rng.normal(size=n)
x2 = 0.95 * x1 + rng.normal(scale=0.1, size=n)
x3 = rng.normal(size=n)
X = np.column_stack([x1, x2, x3])
y = 3 * x1 + rng.normal(scale=0.5, size=n)
X = (X - X.mean(axis=0)) / X.std(axis=0)      # centrada: el intercepto no se penaliza

X2 = X[:, :2]                                 # x1 y x2, las dos colineales
for lam in (0.0, 1.0, 10.0, 100.0):
    # Formula cerrada: sumar lam a la diagonal es lo unico que cambia respecto a OLS.
    manual = np.linalg.solve(X2.T @ X2 + lam * np.eye(2), X2.T @ y)
    # fit_intercept=False no cambia los coeficientes: la X ya esta centrada, asi que
    # sklearn obtendria el mismo resultado y solo sacaria aparte la media de y.
    sk = Ridge(alpha=lam, fit_intercept=False).fit(X2, y).coef_
    print(f"lambda {lam:>5.1f}  manual [{manual[0]:6.3f} {manual[1]:6.3f}]"
          f"  sklearn [{sk[0]:6.3f} {sk[1]:6.3f}]")
# -> lambda   0.0  manual [ 3.382 -0.527]  sklearn [ 3.382 -0.527]
# -> lambda   1.0  manual [ 2.101  0.740]  sklearn [ 2.101  0.740]
# -> lambda  10.0  manual [ 1.458  1.260]  sklearn [ 1.458  1.260]
# -> lambda 100.0  manual [ 0.961  0.940]  sklearn [ 0.961  0.940]
```

## Errores típicos

- **Penalizar sin estandarizar.** La penalización se aplica al tamaño del coeficiente, y ese
  tamaño depende de las unidades. Si una variable se mide en metros y otra en milímetros, la
  segunda tiene un coeficiente 1.000 veces menor y apenas se penaliza. Estandariza siempre
  antes ([[escalado-y-transformacion|escalado]]) y trata el intercepto aparte.
- **Interpretar los coeficientes de Lasso como importancia pura.** Con variables
  correlacionadas, Lasso elige una y anula las demás de forma casi arbitraria: si repites el
  ajuste con otra muestra, puede quedarse con la otra. Si quieres conservar grupos de variables
  relacionadas, usa Elastic Net con `α` intermedio.
- **Elegir `λ` con el mismo conjunto con el que evalúas.** Es una fuga clásica: la validación
  cruzada elige el `λ` que mejor puntúa, y luego reportas esa misma puntuación como rendimiento.
  Separa la elección del `λ` de la estimación final.
- **Creer que L1 selecciona siempre las variables «de verdad».** Con `p` mayor que `n`, Lasso
  selecciona como mucho `n` variables aunque haya más relevantes; es una limitación del
  procedimiento, no un hallazgo sobre tus datos.
- **Comparar un modelo regularizado con uno sin regularizar sin recordar el sesgo.** Ridge y
  Lasso son estimadores **sesgados a propósito**: su ventaja está en la varianza, y se nota en
  la predicción fuera de muestra, no en los coeficientes de la muestra de entrenamiento. Si
  comparas solo el error de entrenamiento, siempre ganará mínimos cuadrados.
- **Olvidar que un cero de Lasso es un cero numérico.** El umbral que devuelve cero depende de
  `λ` y de la escala. Un coeficiente de 0,0001 no es cero, y un cero no es una prueba de que la
  variable sea irrelevante: es una decisión del procedimiento para ese `λ`.

:::practica
enunciado: Una variable estandarizada y centrada cumple Σx² = 1 y Σxy = 0,8. Calcula su coeficiente Ridge con λ = 0, λ = 0,6 y λ = 1,4, y el λ que lo dejaría en 0,2.
pista: Con una sola variable, la fórmula cerrada (XᵀX + λI)⁻¹Xᵀy se reduce a dividir Xᵀy entre XᵀX más λ.
solucion: β = 0,8/(1 + λ). Con λ = 0, β = 0,8, que es mínimos cuadrados puros. Con λ = 0,6, β = 0,8/1,6 = 0,5: el castigo se lleva el 37,5 % del coeficiente. Con λ = 1,4, β = 0,8/2,4 = 0,333. Para bajarlo a 0,2 hace falta 1 + λ = 0,8/0,2 = 4, o sea λ = 3. Ridge encoge cada vez más, pero nunca llega a cero.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué Lasso devuelve coeficientes exactamente cero y Ridge no?
o: Porque Lasso usa la suma de valores absolutos, cuya región de restricción tiene vértices sobre los ejes donde las curvas de error suelen tocar primero
o: Porque Lasso elimina las variables antes de ajustar y Ridge no
o: Porque Ridge no penaliza los coeficientes pequeños
a: 1
e: La geometría es la clave: el rombo de la restricción L1 tiene esquinas en los ejes, y las elipses del error suelen alcanzarlo en una esquina (coeficiente cero). El círculo de L2 no tiene esquinas, así que encoge sin anular. Ninguno de los dos elimina variables «a mano».
:::

:::quiz
p: Con dos variables casi idénticas, ¿qué diferencia práctica ves entre Ridge y Lasso?
o: Ridge reparte el efecto entre las dos y Lasso se queda con una y anula la otra
o: Ridge anula las dos y Lasso las mantiene
o: Los dos dan exactamente el mismo resultado porque la penalización es la misma
a: 1
e: Ridge tiende a repartir el peso entre variables correlacionadas (en el ejemplo, 1,458 y 1,260), mientras que Lasso selecciona una y pone la otra a cero. Por eso Lasso es más interpretable pero menos estable cuando hay grupos de variables relacionadas.
:::

:::quiz
p: Estás penalizando un modelo y una variable binaria (0/1) sale con un coeficiente diminuto. ¿Cuál es la causa más probable?
o: Que la variable es irrelevante con seguridad
o: Que no estandarizaste y su escala es mucho mayor que la de las demás variables
o: Que Lasso no admite variables binarias
a: 2
e: La penalización actúa sobre la magnitud del coeficiente, que depende de la escala. Una variable con rango grande (por ejemplo ingresos en euros) tiene coeficientes pequeños por construcción y se penaliza poco o mucho según sus unidades. Estandarizar todas las predictoras pone el castigo en pie de igualdad.
:::
