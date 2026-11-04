---
id: covarianza-y-correlacion
titulo: Covarianza y correlación
fase: 1
nivel: básico
rutas: [core, ds, quant]
prerequisitos: [varianza-y-desviacion, valor-esperado]
tags: [probabilidad, dependencia, cartera]
resumen: Cuanto tienden dos variables a moverse juntas, la versión sin unidades de esa medida y las tres cosas que la correlación no dice.
fuentes: ["Casella y Berger (2002), 'Statistical Inference'", "DeGroot y Schervish (2012), 'Probability and Statistics'"]
---

## En una frase

La covarianza mide si dos variables tienden a moverse en la misma dirección, y la correlación
es la misma información sin unidades: un número entre −1 y 1.

## La idea

Piensa en dos tiendas en la misma calle: una vende paraguas y la otra helados. Los días de
lluvia la primera factura mucho y la segunda poco; los días de sol, al revés. Las dos series
se mueven en direcciones opuestas y eso es una buena noticia para quien sea dueño de las dos:
cuando una cae, la otra sube, y el ingreso total se estabiliza. Esa es la idea que hay detrás
de diversificar, y se mide con la covarianza.

La covarianza tiene un problema práctico: su magnitud depende de las unidades. Si mides las
ventas en euros, sale un número; si las mides en céntimos, sale cien veces mayor, con los
mismos datos y la misma relación. Para comparar relaciones de cosas distintas se divide por
las dos desviaciones típicas y aparece la **correlación**, que no tiene unidades y siempre
está entre −1 y 1.

La correlación es la métrica más malinterpretada de la estadística. Solo mide asociación
**lineal**, y eso deja fuera tres cosas importantes:

1. **Dependencias no lineales.** Toma `x = −3, −2, −1, 0, 1, 2, 3` e `y = x²`. `y` está
   perfectamente determinado por `x`: si sabes `x`, sabes `y` sin error. Su correlación es
   0,0000. Cero correlación no significa ninguna relación.
2. **Los extremos.** Dos activos pueden ir juntos en días tranquilos y desplomarse juntos en
   una crisis. La correlación media dice poco sobre la cola, que es justo donde te importa.
3. **La proporción de variación explicada.** Una correlación de 0,5 suena a «la mitad», pero
   el cuadrado (0,25) es la fracción de varianza compartida. La otra mitad no está explicada.

Y, por supuesto, correlación no es causalidad: el número de helados vendidos y el de
ahogamientos correlacionan porque ambos suben con el calor, no porque un helado provoque nada.

## Definición formal

Para dos variables `X` e `Y` con medias `μ_X` y `μ_Y`:

:::formula
Cov(X, Y) = E[(X − μ_X)·(Y − μ_Y)] = E[X·Y] − μ_X·μ_Y
:::

- `Cov(X, Y)` — covarianza: positiva si tienden a estar por encima (o por debajo) de su media
  a la vez; negativa si una sube cuando la otra baja.
- `E[·]` — valor esperado; `μ_X = E[X]` y `μ_Y = E[Y]` son las medias.

Dividiendo por las desviaciones típicas se obtiene la **correlación de Pearson**:

:::formula
ρ = Cov(X, Y) / (σ_X · σ_Y),  con −1 ≤ ρ ≤ 1
:::

- `ρ` (rho) — correlación poblacional; la versión muestral se escribe `r`.
- `σ_X = √Var(X)` — desviación típica de `X`, y `σ_Y` la de `Y`.

:::figura
fichero: correlacion-lineal-cero-y-cartera
pie: Arriba a la izquierda, seis alumnos: la nube se aprieta en una recta, la covarianza vale 3,10 y decir que las notas pasaran a escala 0-100 la convertiria en 310 sin tocar la correlación. Arriba a la derecha, y = x^2 con correlación 0,0000 y dependencia total: un cero no significa que no haya relación. Abajo, ocupando todo el ancho, la volatilidad de una cartera segun la correlación entre sus dos activos: con rho = -0,3 baja al 11,5 % y con rho = +0,3 sube al 13,7 %, siempre por debajo de la media ponderada (16 %).
fuente: figuras/covarianza-y-correlacion-1.py
:::

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `Cov(X, Y)` | Cuanto tienden a desviarse juntas dos variables | producto de las unidades de las dos | Es el resultado bruto y depende de la escala: multiplicar una variable por 100 multiplica la covarianza por 100. Su signo dice la dirección; su tamaño solo se compara con datos en las mismas unidades |
| `rho` | Correlación de Pearson: la covarianza sin unidades | adimensional, entre -1 y 1 | No cambia al multiplicar por constantes positivas. Con `rho = 1` los puntos caen en una recta creciente; con 0 no hay relación lineal, que no es lo mismo que no haber relación |
| `r` | La correlación calculada con datos (la estimación de `rho`) | adimensional, entre -1 y 1 | Con pocos datos salta mucho: con `n = 10` y `rho = 0` es fácil ver 0,3 por puro azar. Sin intervalo de confianza, una `r` aislada no es evidencia |
| `mu_X`, `mu_Y` | Las medias de cada variable | las de cada variable | Desplazar una variable no cambia la covarianza ni la correlación: `Cov(aX + b, cY + d) = a·c·Cov(X, Y)` |
| `sigma_X`, `sigma_Y` | Las desviaciones típicas de cada variable | las de cada variable | Son el divisor de `rho`. Si una es 0 (variable constante), la correlación no esta definida, no vale 0 |
| `a`, `c` | Factores de escala de cada variable | adimensionales | Multiplican la covarianza por `a·c`. Si `a·c` es negativo, la covarianza y la correlación cambian de signo; si ambos son positivos, `rho` no se mueve |
| `w1`, `w2` | Los pesos de cada activo en la cartera | fracción del total, suman 1 | La varianza de la cartera es cuadrática en los pesos: bajar `w1` reduce el termino `w1^2·Var1` pero también el termino cruzado. Pasarse de concentración sube el riesgo |
:::

**Propiedades.**

- `Cov(aX + b, cY + d) = a·c·Cov(X, Y)`. Los desplazamientos no cambian nada; los factores
  multiplican. Si `a·c` es negativo, la covarianza cambia de signo.
- `ρ` no cambia si multiplicas por constantes positivas ni si sumas constantes. Solo cambia de
  signo si uno de los factores es negativo.
- `ρ = 1` cuando `Y = aX + b` con `a > 0`; `ρ = −1` cuando la relación lineal es decreciente.
- `Var(X + Y) = Var(X) + Var(Y) + 2·Cov(X, Y)`. Con covarianza negativa el término cruzado
  resta, y la suma puede llegar a tener **menos** varianza que cada sumando por separado.
- `ρ = 0` significa «no correlacionadas», no «independientes». La implicación al revés sí vale:
  si son independientes, la covarianza es cero. La excepción que hace funcionar media
  estadística: si `X` e `Y` son conjuntamente normales, `ρ = 0` sí implica independencia.

## Ejemplo

**Horas de estudio y nota.** Seis alumnos, horas: 1, 2, 3, 4, 5, 6. Notas: 4,0 · 4,5 · 5,0 ·
6,0 · 7,0 · 8,5. La covarianza muestral es 3,1 y la correlación 0,9787: relación lineal fuerte
y positiva.

Ahora cambia la escala de las notas para publicarlas en una tabla con otra unidad:
`nota_nueva = 100 · nota + 5`. La covarianza pasa a 310 (cien veces mayor) y la correlación
sigue siendo 0,9787. Ese es exactamente el motivo de que la correlación exista.

**Dependencia sin correlación.** Con `x` de −3 a 3 e `y = x²`, `Cov(x, y) = 0` y `ρ = 0,0000`,
aunque `y` esté totalmente determinado por `x`. Con `y = −x`, `ρ = −1`.

**Por qué importa la covarianza.** Con dos activos de desviaciones típicas 20 % y 10 % y una
correlación de 0,3, una cartera al 60 % y 40 % tiene varianza
`0,36·0,04 + 0,16·0,01 + 2·0,6·0,4·0,3·0,02 = 0,01888`, es decir `σ = 13,7 %`. Menos que la
media ponderada de las volatilidades (16 %), porque la correlación no es 1. Si la correlación
fuera −0,3, la varianza bajaría a `0,0144 + 0,0016 − 0,00288 = 0,01312` y `σ = 11,5 %`.

## Código

```python verificable
import numpy as np

horas = np.array([1, 2, 3, 4, 5, 6], dtype=float)
notas = np.array([4.0, 4.5, 5.0, 6.0, 7.0, 8.5])

cov = np.cov(horas, notas, ddof=1)[0, 1]
print(f"covarianza  = {cov:.4f}")                          # -> 3.1000
print(f"correlacion = {np.corrcoef(horas, notas)[0, 1]:.4f}")  # -> 0.9787

# Cambiar de unidades multiplica la covarianza pero deja la correlacion intacta.
notas_nuevas = notas * 100 + 5
print(f"cov * 100   = {np.cov(horas, notas_nuevas, ddof=1)[0, 1]:.2f}")       # -> 310.00
print(f"corr igual  = {np.corrcoef(horas, notas_nuevas)[0, 1]:.4f}")         # -> 0.9787
```
:::claves
- `np.cov(horas, notas, ddof=1)` devuelve una **matriz de covarianzas 2x2**, no un número: `[0, 0]` es la varianza de las horas, `[1, 1]` la de las notas y las dos esquinas `[0, 1]` y `[1, 0]` son la covarianza. El `ddof=1` es el de la varianza muestral; `np.cov` ya lo usa por defecto, así que escribirlo es explicito pero no cambia nada.
- `np.corrcoef(horas, notas)[0, 1]` construye la misma matriz que `np.cov`, pero normalizada: cada covarianza se divide entre las dos desviaciones típicas, así que el resultado ya no depende de las unidades. Con dos arrays, el número que buscas es siempre la esquina `[0, 1]`.
- En el segundo bloque, `y = x ** 2` con `x = np.arange(-3, 4, dtype=float)` da correlación exactamente 0 por simetria. Si cambiaras el rango a `np.arange(0, 4)`, la simetria desaparece y la correlación daria claramente positiva: el cero de antes era un artefacto de los datos, no una propiedad de la relación.
- `np.corrcoef(np.arange(6.0), w)` con `w = -np.arange(6.0)` da -1,0000 exacto. La correlación se calcula dividiendo por las desviaciones típicas, y esas nunca son negativas: el signo solo puede venir del numerador, es decir, de la covarianza.
- El tercer panel no es una grafica de datos sino de una formula evaluada en 200 puntos de `rho`. Es útil precisamente porque ahi no hay nada que estimar: separa la relación matemática entre correlación y varianza de cartera de la incertidumbre de medirla con datos.
- Fijate en que `ingenua = (pesos * sigmas).sum()` es una línea fuera de la grafica: la media ponderada de volatilidades (16 %) no depende de `rho`. En cuanto una cartera tiene correlación por debajo de 1, la volatilidad real queda por debajo de ese 16 %, y esa brecha es todo el argumento de la diversificación.
:::


```python verificable
import numpy as np

# Dependencia perfecta y no lineal: x de -3 a 3, y = x^2.
x = np.arange(-3, 4, dtype=float)
y = x ** 2
print(f"covarianza(x, x^2)  = {np.cov(x, y, ddof=1)[0, 1]:.4f}")   # -> 0.0000
print(f"correlacion(x, x^2) = {np.corrcoef(x, y)[0, 1]:.4f}")      # -> 0.0000

# Relacion lineal decreciente: la correlacion llega al minimo posible.
w = -np.arange(6, dtype=float)
print(f"correlacion lineal negativa = {np.corrcoef(np.arange(6.0), w)[0, 1]:.4f}")  # -> -1.0000
```

## Errores típicos

- **Interpretar la covarianza como fuerza de la relación.** Con los mismos datos vale 3,1 o
  310 según las unidades. Para comparar relaciones, usa la correlación.
- **Concluir que no hay relación porque `ρ = 0`.** Con `y = x²` la correlación es 0 y la
  dependencia es total. Antes de dar por bueno un cero, mira el gráfico de dispersión.
- **Extrapolar la correlación a los extremos.** Una correlación de 0,2 en días normales puede
  ser 0,8 en una caída general: cuando más falta hace diversificar, menos diversifica la
  cartera. La correlación lineal media no describe la cola.
- **Leer `ρ = 0,5` como «el 50 %».** La fracción de varianza compartida es `ρ² = 0,25`. Si
  alguien dice «explica la mitad», está elevando al cuadrado con la intuición, no con la
  fórmula.
- **Aplicar Pearson a cualquier relación.** Pearson mide relación lineal. Con relaciones
  monótonas pero curvas (rangos, precios, dosis) la [[correlacion-pearson-spearman|correlación
  de Spearman]] describe mucho mejor lo que está pasando.
- **Fiarse de una correlación estimada con pocos datos.** El error típico de `r` es del orden
  de `(1 − ρ²)/√(n − 1)`: con 10 observaciones y `ρ = 0`, la estimación salta fácilmente a
  ±0,3 por puro azar. Sin intervalo de confianza, una correlación aislada no es evidencia.

:::practica
enunciado: Dos activos tienen volatilidades 18 % y 12 % (varianzas 0,0324 y 0,0144) y correlación 0,25. En una cartera al 50 % en cada uno, calcula Var(P) y sigma_P y compara con la media ponderada de volatilidades.
pista: Usa Var(P) = w1²·Var1 + w2²·Var2 + 2·w1·w2·rho·sigma1·sigma2, con la covarianza ya escrita por la correlación.
solucion: Var(P) = 0,25 · 0,0324 + 0,25 · 0,0144 + 2 · 0,5 · 0,5 · 0,25 · 0,18 · 0,12 = 0,0081 + 0,0036 + 0,0027 = 0,0144. sigma_P = raíz(0,0144) = 0,12, un 12 %. La media ponderada sería 15 %, así que diversificar ahorra 3 puntos de volatilidad.
:::

## Comprueba que lo sabes

:::quiz
p: Con los datos de horas de estudio y notas, la covarianza es 3,1. Si pasas las notas de la escala 0-10 a la escala 0-100 multiplicando por 10, ¿qué pasa?
o: La covarianza pasa a 31 y la correlación se multiplica por 10
o: La covarianza pasa a 31 y la correlación sigue igual
o: Las dos siguen igual, porque los datos no han cambiado
a: 2
e: La covarianza escala con las unidades: Cov(aX, Y) = a·Cov(X, Y), así que se multiplica por 10. La correlación se divide entre las dos desviaciones típicas, y el factor 10 se cancela, por eso es la medida adecuada para comparar relaciones de variables con escalas distintas.
:::

:::quiz
p: Dos variables tienen correlación exactamente 0. ¿Qué puedes concluir?
o: Que son independientes
o: Que no hay relación lineal entre ellas, pero puede haber una relación no lineal perfecta
o: Que una de las dos es constante
a: 2
e: La correlación de Pearson mide solo asociación lineal. Con y = x² la correlación es cero y la dependencia es total. La independencia implica covarianza cero, pero al revés solo se cumple con normalidad conjunta.
:::

:::quiz
p: ¿Por qué una covarianza negativa entre dos activos reduce el riesgo de una cartera?
o: Porque cuando uno baja, el otro tiende a subir, y la varianza de la suma resta el doble de la covarianza
o: Porque elimina la posibilidad de perder dinero
o: Porque con covarianza negativa las desviaciones típicas también son negativas
a: 1
e: Var(X + Y) = Var(X) + Var(Y) + 2·Cov(X, Y): con covarianza negativa, ese tercer término resta y la varianza conjunta baja. No elimina las pérdidas, solo reduce la dispersión del conjunto, y las desviaciones típicas nunca son negativas.
:::
