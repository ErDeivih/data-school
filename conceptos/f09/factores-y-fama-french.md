---
id: factores-y-fama-french
titulo: Factores y Fama-French
fase: 9
nivel: avanzado
rutas: [quant, ds]
prerequisitos: [alpha-y-beta, regresion-lineal, correlacion-pearson-spearman]
tags: [factores, capm, cartera, riesgo]
resumen: Más allá del mercado: tamaño, valor, momentum y calidad explican parte de lo que el CAPM deja fuera y hunden el alpha de casi cualquier backtest.
fuentes: ["Fama y French (1993), 'Common risk factors in the returns on stocks and bonds'", "Carhart (1997), 'On Persistence in Mutual Fund Performance'", "Fama y French (2015), 'A five-factor asset pricing model'"]
---

## En una frase

Un factor es una fuente de riesgo ya identificada que se paga sola: si tu estrategia gana
cuando gana el factor valor, no has descubierto nada nuevo, solo tienes una exposición
disfrazada de habilidad.

## La idea

Imagina que comparas dos tiendas de ropa y una vende el doble que la otra. Antes de
felicitar a su dueño, miras dónde están: la primera está en una calle peatonal con miles de
personas al día y la segunda en un polígono. La diferencia de ventas la pone la
calle, no la gestión. Y ese mismo razonamiento ordena toda la ficha: antes de atribuir mérito a una estrategia, mira qué factor la empujaba. En rentabilidad de activos pasa lo mismo: hay «calles» que empujan los
resultados de un grupo entero de acciones, y hasta que no las descuentas no sabes si el
gestor aporta algo.

La primera calle que se identificó fue **el mercado**: cuando la bolsa sube, casi todo sube.
Eso es el CAPM, con un solo factor, y durante décadas fue el modelo de referencia. El
problema es que explicaba mal la realidad: las acciones pequeñas rendían más de lo que
justificaba su beta, y las acciones «baratas» (mucho valor contable respecto al precio)
también. Fama y French añadieron esos dos factores al modelo en 1993: **tamaño** (SMB, small
minus big) y **valor** (HML, high minus low). Carhart añadió después **momentum** (MOM,
ganadoras menos perdedoras) y Fama y French completaron su modelo de cinco factores con
**rentabilidad** (RMW, robust minus weak) y **inversión** (CMA, conservative minus
aggressive).

Cada factor es una cartera larga-corta, sin coste neto de capital, que se reconstruye cada
mes. Su rentabilidad media es la **prima de riesgo** del factor. Hay dos explicaciones en
disputa y la distinción importa mucho: o son riesgo de verdad (la empresa pequeña y
endeudada es frágil, así que exijo más rentabilidad) o son errores de valoración
sistemáticos que el mercado acabará corrigiendo. Si es riesgo, la prima sobrevive; si es
error, desaparece cuando hay dinero detrás. Tu decisión de invertir en un factor depende de
en cuál de las dos creas.

Para ti, que estás haciendo un backtest, la consecuencia es directa: **una
estrategia con rentabilidad positiva puede ser una inclinación a un factor**. La regresión
contra factores es el control de calidad que separa «tengo alpha» de «tengo una cartera de
valor con otro nombre».

## Definición formal

El modelo de factores se estima con una regresión por mínimos cuadrados:

:::formula
R_i − Rf = α_i + β_mkt · (Rm − Rf) + β_smb · SMB + β_hml · HML + β_mom · MOM + ε_i
:::

- `R_i` — retorno del activo o de la estrategia `i` en el periodo (mensual, típicamente).
- `Rf` — retorno del activo libre de riesgo en ese mismo periodo.
- `Rm − Rf` — exceso de retorno del mercado; es el factor de mercado.
- `α_i` (alpha) — el retorno medio que **no** explican los factores. Es lo que quieres que
  sea distinto de cero.
- `β_mkt`, `β_smb`, `β_hml`, `β_mom` — las cargas: cuánto se mueve `i` por cada unidad de
  cada factor. Se estiman, no se eligen.
- `ε_i` — el residuo, la parte idiosincrásica.
- `SMB`, `HML`, `MOM` — retornos de carteras larga-corta construidas así:
  - **SMB** = media de las carteras de baja capitalización menos media de las de alta.
  - **HML** = alto valor contable sobre precio menos bajo (las «baratas» menos las «caras»).
  - **MOM** = ganadoras de los últimos doce meses (saltando el más reciente) menos
    perdedoras, que es el [[momentum]] de manual.
- En el modelo de cinco factores se añaden `RMW` (rentabilidad operativa alta menos baja) y
  `CMA` (inversión conservadora menos agresiva), y `HML` pierde protagonismo porque parte de
  su contenido lo recogen las dos nuevas.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `R_i` | Retorno del activo o de la estrategia en el periodo | tanto por uno por mes | Es la variable que se quiere explicar. Si en lugar del retorno usas el exceso, tienes que hacerlo también en el lado de los factores, o el término independiente se traga el tipo sin riesgo |
| `Rf` | Retorno del activo libre de riesgo del mismo periodo | tanto por uno por mes | Se resta en los dos lados. Con tipos que cambian mucho dentro de la muestra, olvidarlo introduce una tendencia en el alpha que no tiene nada que ver con la habilidad |
| `Rm − Rf` | El exceso de retorno del mercado: el primer factor | tanto por uno por mes | Es el factor dominante. Su prima media decide el alpha aparente de cualquier estrategia con beta de mercado distinta de cero: si el mercado subió mucho en la muestra, casi todo sale con alpha |
| `SMB` | Tamaño: media de las carteras de baja capitalización menos media de las de alta | tanto por uno por mes | Una prima positiva significa que las pequeñas rindieron más. Si tu estrategia carga en ese factor y no lo metes, parte de la prima se va al intercepto |
| `HML` | Valor: alto valor contable sobre precio menos bajo (baratas menos caras) | tanto por uno por mes | Es el que más mueve el alpha de los backtests de acciones. Ojo: se publica sin costes y las carteras incluyen microempresas con diferenciales amplios, así que parte de esa prima no es cobrable |
| `MOM` | Ganadoras de los últimos doce meses (saltando el más reciente) menos perdedoras | tanto por uno por mes | Añadirlo cambia mucho el resultado de estrategias que compran lo que sube. Es el [[momentum]] de manual, y una estrategia de momentum sin `MOM` en la regresión se atribuye su propia prima |
| `RMW`, `CMA` | Rentabilidad operativa alta menos baja, e inversión conservadora menos agresiva | tanto por uno por mes | En el modelo de cinco factores le quitan a `HML` parte de su contenido, así que el mismo `HML` estimado con uno u otro modelo no es el mismo número |
| `α_i` | El retorno medio que **no** explican los factores incluidos | tanto por uno por mes | Es lo que se quiere que sea distinto de cero, pero **depende de qué factores metas**: quitando el factor valor, la estrategia de la página pasa de alpha cero a un +0,23 % mensual que no existe. Un alpha solo significa algo acompañado de la lista de factores y de su `t` |
| `β_mkt`, `β_smb`, `β_hml`, `β_mom` | Las cargas: cuánto se mueve `i` por cada unidad del factor | adimensional | Son el multiplicador de cada prima. Beta 0,5 de valor con prima de 0,6 % mensual aporta 0,30 puntos al mes: si no lo descuentas, lo llamas habilidad. Cambian con la ventana y con el régimen, así que un solo número para veinte años no significa nada |
| `ε_i` | El residuo, la parte idiosincrásica | tanto por uno por mes | Su dispersión fija los errores típicos de todo lo demás. Si los residuos están correlacionados entre periodos o tienen colas gordas, los `t` calculados con la fórmula de mínimos cuadrados están inflados |
| `n` | Número de periodos de la regresión | meses | Con 240 meses el `t` empieza a ser interpretable; con 3 observaciones (el ejemplo a mano de la página) el error típico es tan grande que la aritmética es correcta y la conclusión nula |
| `k` | Número de parámetros del modelo, incluida la constante | parámetros | La varianza residual se divide entre `n − k`, no entre `n`: cada factor que añades gasta un grado de libertad. Con 240 meses y 5 factores el efecto es pequeño; con 24 meses y 5 factores, no |
:::

Dos consecuencias de la construcción que conviene tener presentes:

1. **Los factores son larga-corta y se publican sin costes.** Un `HML` de +2 % en un mes no
   significa que nadie pudiera ganar ese 2 %: las «baratas» incluyen microempresas con
   diferenciales amplios que se comen buena parte del premio.
2. **El alpha es mensual y no se anualiza multiplicando por 12** si quieres una rentabilidad
   compuesta. Multiplicar por 12 sirve para comparar órdenes de magnitud, no para prometer
   dinero.

:::figura
fichero: factores-alpha-que-era-una-carga
pie: La estrategia de la izquierda se construyó sin ninguna habilidad: su alpha verdadero es cero. Estimada solo con el mercado sale un +0,21 % mensual con `t` superior a 2, que es el sesgo por variable omitida: la prima del factor valor se ha ido al término independiente, porque no había ningún factor que la recogiera. Al meter el valor, el alpha vuelve a cero y el R² sube de 0,78 a 0,97. Las barras de la derecha enseñan lo que sí llevaba la estrategia: 0,8 de mercado y 0,5 de valor. Antes de escribir «alpha» en un informe, mira si el número sobrevive al factor que has omitido.
fuente: figuras/factores-y-fama-french-1.py
:::

## Ejemplo

Cinco meses de una estrategia, con datos a mano. El exceso de retorno del mercado es
0,02; −0,01; 0,03; 0,00; 0,01 y el exceso de la estrategia es 0,03; −0,02; 0,04; 0,01; 0,02
(en tanto por uno).

- Media del mercado: 0,05 / 5 = 0,01. Media de la estrategia: 0,08 / 5 = 0,016.
- Suma de productos de las desviaciones: 0,014; suma de cuadrados del mercado: 0,010.
- Covarianza muestral (dividiendo por n − 1 = 4): 0,0035. Varianza muestral del mercado: 0,0025.
- Beta = 0,0035 / 0,0025 = **1,40**.
- Alpha = 0,016 − 1,40 · 0,01 = **+0,002**, es decir +0,20 % mensual.

La lectura es incómoda y es la correcta: la estrategia gana un 1,6 % mensual de media, pero
una vez ajustada por su exposición al mercado el alpha que queda es de dos décimas. Se movió
más que el mercado (beta 1,40) y por eso ganó más; el resto hay que demostrarlo con el error
típico, y aquí no se puede.

Ahora el paso que cambia la conclusión. Añade un factor valor con retornos mensuales
0,01; −0,005; 0,01; 0,005; 0,00 (media 0,005) y supón que la carga estimada es `β_hml = 0,5`. La
parte explicada por el valor es 0,5 · 0,005 = 0,0025, que sumada a la del mercado (1,40 · 0,01 =
0,0140) da 0,0165. El alpha pasa a ser 0,016 − 0,0165 = **−0,0005**: la estrategia
no aporta y además se queda corta respecto a lo que predecían sus factores. Con cinco
observaciones nada de esto es concluyente (el error típico es enorme), pero la aritmética es
la que hace el código con veinte años de datos.

Y ese error típico, que es lo que decide, se calcula igual que en [[alpha-y-beta]]: la suma de
cuadrados de los residuos es 0,0016, la de la estrategia 0,0212, así que el R² es
1 − 0,0016 / 0,0212 = **92,5 %**; la desviación típica de los residuos vale
`√(0,0016 / 3) = 0,73` puntos porcentuales y el error típico del alpha,
`0,73 · √(1/5 + 0,01² / 0,010) = 0,40`, deja el estadístico en `t = 0,20 / 0,40 = 0,50`. Con
cinco meses, ese +0,20 % mensual es **indistinguible de cero**.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(0)
n = 240
mkt = rng.normal(0.006, 0.04, n)
hml = rng.normal(0.005, 0.03, n)
hml = hml - hml.mean() + 0.005          # fijamos la prima media del factor en la muestra

# Estrategia SIN habilidad: alpha cero, beta de mercado 0,8 y carga de valor 0,5
y = 0.8 * mkt + 0.5 * hml + rng.normal(0, 0.006, n)

coef_con, *_ = np.linalg.lstsq(np.column_stack([np.ones(n), mkt, hml]), y, rcond=None)
coef_sin, *_ = np.linalg.lstsq(np.column_stack([np.ones(n), mkt]), y, rcond=None)

print("con HML  alpha %+.4f  beta_mkt %.3f  beta_hml %.3f" % (coef_con[0], coef_con[1], coef_con[2]))
print("sin HML  alpha %+.4f  beta_mkt %.3f" % (coef_sin[0], coef_sin[1]))
# -> con HML  alpha +0.0000  beta_mkt 0.795  beta_hml 0.485
# -> sin HML  alpha +0.0023  beta_mkt 0.828
```

:::claves
- `np.linalg.lstsq` **no añade la constante por ti**: hay que meterla como una columna de unos con `np.column_stack([np.ones(n), mkt, hml])`. Compara las dos llamadas del bloque: `coef_con` tiene tres elementos y `coef_sin` dos, y el primero de cada uno es el término independiente solo porque la columna de unos va **en primera posición**. Si la pones al final, `coef[0]` pasa a ser la beta del mercado y el código sigue funcionando sin avisar.
- `np.linalg.lstsq` devuelve una tupla de cuatro cosas (solución, residuos, rango, valores singulares) y el código se queda con la primera usando `coef, *_ = ...`. El `rcond=None` no es opcional en la práctica: sin él NumPy avisa por consola y en versiones nuevas el comportamiento cambia, porque `rcond` decide qué valores singulares se consideran cero.
- El sesgo por variable omitida que enseña el ejemplo no es un fallo del método: `lstsq` está resolviendo bien los dos problemas. Lo que ocurre es que `y` se construyó con `0.5 * hml` dentro y el segundo modelo no tiene ninguna columna que recoja `hml`, así que el residuo del modelo corto **contiene** esa prima y el intercepto la absorbe. Es aritmética, no ruido: quitar la columna mueve el alpha de 0,0000 a +0,0023.
- `y = 0.8 * mkt + 0.5 * hml + rng.normal(0, 0.006, n)` fija el alpha verdadero en cero por construcción, así que el ejercicio sabe la respuesta de antemano. Eso es lo que permite decir que el +0,23 % es sesgo y no una estimación afortunada; con datos reales esa comprobación no existe y hay que conformarse con el `t` y con el intervalo.
- En el segundo bloque, `s2 = resid @ resid / (n - k)` divide entre `n − k` con `k = X.shape[1]`, es decir, **contando la constante**. Si usaras `n − 1` o `n`, los errores típicos saldrían más pequeños de lo que son y el `t` del alpha parecería más significativo. Y `np.linalg.inv(X.T @ X)` se rompe si dos factores están muy correlacionados entre sí: la matriz se vuelve casi singular y los errores típicos se disparan.
- `X = np.column_stack([np.ones(len(y)), X])` **reutiliza el nombre `X`** dentro de la función: la matriz original del llamante no se toca (es una variable local), pero dentro de la función, a partir de esa línea, `X` ya es la matriz ampliada. Si añadieras una línea después usando la `X` original, estarías usando la ampliada sin darte cuenta.
:::

La estrategia del ejemplo **no tiene habilidad**: se construyó con alpha cero. Sin embargo,
al omitir el factor valor el término independiente se traga la prima del factor y aparece un
alpha de +0,23 % mensual. Ese es el sesgo por variable omitida, y por eso un
backtest sin factores miente.

```python verificable
import numpy as np

def resumen(y, X):
    X = np.column_stack([np.ones(len(y)), X])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ coef
    n, k = X.shape
    s2 = resid @ resid / (n - k)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    r2 = 1 - (resid @ resid) / ((y - y.mean()) @ (y - y.mean()))
    return coef, se, r2

rng = np.random.default_rng(0)
n = 240
mkt = rng.normal(0.006, 0.04, n)
hml = rng.normal(0.005, 0.03, n)
hml = hml - hml.mean() + 0.005
y = 0.8 * mkt + 0.5 * hml + rng.normal(0, 0.006, n)

coef_c, se_c, r2_c = resumen(y, np.column_stack([mkt, hml]))
coef_s, se_s, r2_s = resumen(y, mkt.reshape(-1, 1))

print("con HML  alpha %+.4f  t %+.2f  R2 %.3f" % (coef_c[0], coef_c[0] / se_c[0], r2_c))
print("sin HML  alpha %+.4f  t %+.2f  R2 %.3f" % (coef_s[0], coef_s[0] / se_s[0], r2_s))
# -> con HML  alpha +0.0000  t +0.10  R2 0.977
# -> sin HML  alpha +0.0023  t +2.21  R2 0.815
```

Este segundo bloque añade lo que de verdad decide: el estadístico `t` del alpha. Sin el
factor, el alpha parece casi significativo (t = 2,21) y el modelo explica menos (R² 0,815
frente a 0,977). Con el factor, el alpha es cero. La moraleja no es «usa siempre
cinco factores», sino «no declares alpha antes de haber controlado por lo que ya se sabe».

## Errores típicos

- **Llamar alpha a cualquier rentabilidad positiva.** Un backtest largo en acciones pequeñas
  de valor tendrá una rentabilidad media preciosa y un alpha de cero. Corre la regresión
  antes de escribir la palabra «alpha» en el informe.
- **Comparar alphas de estrategias con mandatos distintos.** Si la estrategia A solo puede
  comprar tecnología y la B solo utilities, el factor de mercado no las pone en igualdad de
  condiciones. Añade los factores que describen su universo o compara dentro del mismo.
- **Usar series de factores sin mirar cómo están construidas.** No es lo mismo un factor
  larga-corta igual ponderado que uno ponderado por capitalización, ni uno que excluye
  microempresas que uno que las incluye. Cambiar la definición cambia el alpha que mides.
- **Suponer que las cargas son constantes.** Una cartera que era de valor en 2015 puede ser
  de crecimiento en 2024. Estima las betas en ventanas móviles y mira si se mueven; si se
  mueven, un solo número para todo el periodo no significa nada.
- **Probar veinte factores hasta que el alpha desaparezca.** Eso no valida nada: con
  suficientes factores acabas explicando cualquier cosa y el alpha se va por construcción.
  Es la misma trampa que [[data-snooping-y-multiple-testing|el data snooping]] con otro
  disfraz.
- **Ignorar que las primas viven donde es caro operar.** El premio de tamaño se concentra en
  empresas con poca liquidez: si tu backtest no paga [[slippage-y-comisiones|diferencial ni
  impacto]], estás midiendo una cartera que no puedes montar.

:::trampa
Si al añadir factores el alpha se reduce a la mitad, la conclusión no es «me quedo con el
modelo que da más alpha». La conclusión es que la mitad de tu rentabilidad era una
exposición que puedes comprar más barata con un ETF de factores.
:::

:::practica
enunciado: Tu estrategia gana un 1,8 % mensual de exceso. Su regresión da β_mkt = 0,90, β_hml = 0,40 y β_mom = 0,30. Las primas medias del periodo fueron 1,0 % (mercado), 0,6 % (HML) y 0,8 % (MOM). Calcula el alpha y cuánto de la rentabilidad es habilidad.
pista: Cada factor aporta su beta multiplicada por su prima; el alpha es lo que queda después de restarlo todo.
solucion: Mercado: 0,90 · 1,0 = 0,90 %. HML: 0,40 · 0,6 = 0,24 %. MOM: 0,30 · 0,8 = 0,24 %. Explicado: 0,90 + 0,24 + 0,24 = 1,38 %. Alpha: 1,8 − 1,38 = +0,42 % mensual, que compuesto da (1,0042)¹² − 1 = 5,16 % anual. Solo 0,42 de los 1,8 puntos, el 23 %, no lo explican los factores: el resto es exposición que se compra con ETF de factores.
:::

## Comprueba que lo sabes

:::quiz
p: Tu estrategia tiene una rentabilidad media del 1,2 % mensual y un alpha de 0,1 % con t = 0,3. ¿Qué conclusión es correcta?
o: La estrategia aporta un 0,1 % mensual de habilidad, poco pero real
o: Casi toda la rentabilidad la explican los factores incluidos y el alpha no se distingue de cero
o: El modelo está mal, porque el alpha debería ser igual a la rentabilidad media
a: 2
e: Un t de 0,3 significa que el alpha estimado está dentro del ruido: con ese error típico, cero es perfectamente compatible con el dato. Lo que sí dice la regresión es que las cargas a los factores explican 1,1 de los 1,2 puntos. El alpha no tiene por qué igualar la rentabilidad media: esa igualdad solo se daría si todas las betas fueran cero.
:::

:::quiz
p: ¿Por qué una estrategia construida sin ninguna habilidad puede mostrar un alpha positivo al estimar solo con el factor de mercado?
o: Porque el término independiente recoge la prima media de los factores que has omitido
o: Porque el mercado tiene media positiva y eso infla siempre el alpha
o: Porque la regresión por mínimos cuadrados sesga el intercepto hacia arriba por construcción
a: 1
e: Si la estrategia tiene carga de valor y el factor valor tiene prima media positiva, esa prima no la recoge el mercado y se acumula en el intercepto: es el sesgo por variable omitida. Mínimos cuadrados es insesgado cuando el modelo está bien especificado, y el mercado puede tener media positiva o negativa sin que eso decida el signo del alpha.
:::

:::nota
Los factores de Fama-French, Carhart y los de calidad se publican de forma gratuita y
actualizada en el sitio del profesor Kenneth French, en la página de datos del Dartmouth
Tuck School of Business. Es la fuente estándar para reproducir estas regresiones.
:::
