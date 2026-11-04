---
id: gan
titulo: Redes generativas adversarias
fase: 7
nivel: experto
rutas: [ds]
prerequisitos: [perceptron-y-mlp, funciones-de-perdida, retropropagacion, entropia-e-informacion]
tags: [generativo, adversarial, deep-learning, entrenamiento]
resumen: Dos redes que compiten: una fabrica muestras y la otra intenta distinguirlas. El equilibrio existe en teoria y es fragil en la practica.
fuentes: ["Goodfellow et al. (2014), 'Generative Adversarial Networks'", "Arjovsky y Bottou (2017), 'Towards Principled Methods for Training Generative Adversarial Networks'"]
---

## En una frase

Una red (el generador) transforma ruido en muestras falsas y otra (el discriminador) intenta
decir cuáles son reales; las dos se entrenan a la vez y con objetivos opuestos, y en el
equilibrio ideal el generador reproduce la distribución de los datos.

## La idea

Piensa en un falsificador de billetes y en un policía. El falsificador empieza haciendo
chapuzas; el policía las detecta con facilidad y le explica, sin querer, en qué se nota que
son falsas. El falsificador corrige esos detalles, el policía vuelve a mirar con más
atención, y así sucesivamente. Cuando el juego termina, los billetes falsos son
indistinguibles de los buenos. Eso es una GAN: **no hay una función de pérdida que diga
«esta imagen es buena»**, hay un rival que se encarga de decirlo.

Esto es lo que la hace distinta de todo lo anterior. Un [[autoencoders-y-vae|autoencoder
variacional]] aprende una densidad explícita y optimiza una cota de la verosimilitud; una GAN
nunca escribe la densidad de los datos. Solo necesita poder *muestrear*: coge un vector `z` de
ruido, lo pasa por el generador y ya tiene una muestra sintética. A cambio, no tiene una
función de pérdida que puedas mirar y decir «va bien»: el número que baja en el generador
sube en el discriminador, y viceversa. Esa es la primera cosa que sorprende a quien llega
desde la clasificación.

El segundo choque es que el entrenamiento es un **juego, no una minimización**. En descenso
de gradiente buscas un punto bajo; aquí buscas un punto de silla: un punto que es mínimo para
el generador y máximo para el discriminador a la vez. Los métodos de primer orden que usamos
para entrenar redes no están diseñados para eso, y de ahí salen las oscilaciones, el colapso
de modos y los entrenamientos que se van al garete en la iteración 40.000.

La teoría dice que el juego tiene solución: si el discriminador es óptimo para un generador
dado, la cantidad que el generador minimiza es la divergencia de Jensen-Shannon entre datos y
generador, que vale cero solo cuando ambas distribuciones coinciden. La práctica dice que esa
solución se alcanza pocas veces, porque el discriminador óptimo es justo el escenario donde el
gradiente del generador se apaga. Todo el truco del oficio consiste en no llegar nunca a ese
escenario.

:::figura
fichero: gan-gradiente-y-colapso
pie: El panel izquierdo explica el error que hubo que corregir en el propio artículo original. Con la pérdida saturada, la señal que llega al generador es la derivada de la sigmoide, `D(1−D)`, y su máximo es 0,25 en `D = 0,5`: por cada paso se pierde al menos el 75 % del gradiente. Peor aún, cuando el discriminador rechaza bien lo falso (`D ≈ 0,001`) la señal vale 0,001 y el generador se queda parado justo cuando más necesita corregir. La pérdida no saturada `−log D(G(z))` tiene la misma solución de equilibrio pero su gradiente es `1 − D`, que vale 0,999 en ese mismo punto: ahí está toda la diferencia entre aprender y no aprender. El panel derecho es el otro modo de fallo, el colapso de modos. Los datos reales tienen dos modos y el generador naranja cubre solo uno: reparte su masa en una zona segura y repite variaciones de lo mismo. La razón está en la asimetría de la KL, no en la capacidad del modelo. `KL(p_g‖p_d)` vale 0,693 y solo castiga poner masa donde no hay datos, así que al generador no le cuesta nada ignorar el segundo modo; en el sentido contrario la misma situación vale 12,175. Un modelo que minimice el primer sentido prefiere concentrarse antes que arriesgarse a caer en zona vacía, y eso es exactamente lo que ves en el dibujo.
fuente: figuras/gan-1.py
:::

## Definición formal

El juego minimax original:

:::formula
min_G max_D  E_{x∼p_d}[log D(x)] + E_{z∼p_z}[log(1 − D(G(z)))]
:::

- `G` — el generador: recibe un vector de ruido `z` y produce una muestra `G(z)`.
- `D` — el discriminador: devuelve `D(x) ∈ (0, 1)`, la probabilidad que asigna a que `x` sea real.
- `p_d` — la distribución de los datos reales.
- `p_z` — la distribución del ruido de entrada (una normal estándar, típicamente).
- `E[·]` — esperanza matemática sobre muestras de la distribución indicada.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `G(z)` | La muestra falsa que produce el generador a partir del ruido `z` | las de los datos | No es un número que se mueva: es la salida del generador. Se entrena para que la distribución de `G(z)` se parezca a la de los datos |
| `D(x)` | Probabilidad que el discriminador asigna a que `x` sea real | adimensional, entre 0 y 1 | El objetivo del discriminador es maximizarla en los reales y minimizarla en las falsas. Si sube en las falsas, el generador recibe menos señal |
| `z` | Vector de ruido del que parte el generador | adimensional | Más dimensiones dan al generador más grados de libertad para cubrir los datos; demasiadas, con pocos datos, facilitan memorizar |
| `p_d` | Distribución de los datos reales | densidad | No se toca: es el objetivo. El juego termina cuando `p_g = p_d` |
| `p_g` | Distribución que induce el generador | densidad | Es lo que se mueve durante el entrenamiento. Cuanto más se acerca a `p_d`, menor es la divergencia de Jensen-Shannon y mejor el resultado |
| `D*` | Discriminador óptimo para un generador fijo, `p_d / (p_d + p_g)` | adimensional, entre 0 y 1 | Es el escenario que hay que evitar: cuando `D*` es exacto, el gradiente del generador se apaga y la GAN deja de aprender |
| `L_G` | Pérdida del generador en la versión no saturada, `−E[log D(G(z))]` | adimensional (nats) | Se minimiza. Cuanto más baja, mejor engaña el generador; pero este número **no** es comparable entre carreras ni entre iteraciones |
:::

Si fijas `G` y optimizas `D` punto a punto, el discriminador óptimo es

:::formula
D*(x) = p_d(x) / (p_d(x) + p_g(x))
:::

donde `p_g` es la densidad que induce el generador. Sustituyendo `D*` en el objetivo, el valor
del juego para el generador resulta `2·JSD(p_d, p_g) − 2·log 2`, con `JSD` la divergencia de
Jensen-Shannon (una medida de parecido entre distribuciones, simétrica y acotada). El mínimo
global vale `−log 4 ≈ −1,386` y se alcanza cuando `p_g = p_d`.

El problema práctico está en la pérdida del generador. Con la formulación original,
`log(1 − D(G(z)))` es **saturada**: cuando el discriminador rechaza bien las muestras falsas,
`D(G(z)) ≈ 0`. Como `D` es una sigmoide de un logit `a`, la derivada `dD/da = D·(1 − D)` se
hace diminuta, y esa derivada es la que tiene que atravesar el generador para llegar a sus
pesos ([[retropropagacion|regla de la cadena]]). La solución estándar es entrenar el generador
con la pérdida **no saturada**:

:::formula
L_G = − E_z[log D(G(z))]
:::

Mismo punto de equilibrio, gradientes muy distintos cuando el generador va perdiendo.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `L_G` | Pérdida del generador con la formulación no saturada | adimensional (nats) | Se minimiza. Si baja, el generador engaña más al discriminador; el número en sí no mide calidad de las muestras y no se compara entre carreras |
| `D(G(z))` | Probabilidad que el discriminador da a una muestra falsa | adimensional, entre 0 y 1 | Con la pérdida no saturada, la señal del generador es `1 − D`: cuanto más sube `D` (el discriminador acierta), menos señal recibe el generador |
| `D·(1 − D)` | Derivada de la sigmoide respecto al logit, la que atraviesa el generador en la versión saturada | adimensional | Su máximo es 0,25 en `D = 0,5` y se hunde en los extremos: es la razón de que la pérdida saturada deje de aprender cuando el discriminador gana |
| `p_d`, `p_g` | Densidad de los datos y densidad que induce el generador | densidad | No se mueven a mano. Cuando `p_g` se acerca a `p_d`, la divergencia de Jensen-Shannon baja y el valor del juego se acerca a su mínimo, `−log 4` |
| `JSD(p_d, p_g)` | Divergencia de Jensen-Shannon entre datos y generador | adimensional | Es simétrica y está acotada: al subir, las dos distribuciones se parecen menos y el generador está peor |
:::

## Ejemplo

Primera columna: el valor de `D*` en cinco zonas del espacio, con las densidades de datos y de
generador escritas a mano. Las otras dos columnas son la señal de gradiente que llega al
generador: `D·(1 − D)` con la pérdida saturada y `1 − D` con la no saturada.

```
zona   p_d    p_g     D*    saturada D(1-D)   no saturada 1-D
0      0.001  0.90    0.001      0.00111           0.99889
1      0.02   0.50    0.038      0.03698           0.96154
2      0.30   0.30    0.500      0.25000           0.50000
3      0.50   0.02    0.962      0.03698           0.03846
4      0.90   0.001   0.999      0.00111           0.00111
```

Mira la zona 0: el generador está poniendo masa donde no hay datos (`p_g` es 900 veces
`p_d`) y el discriminador lo sabe. Con la pérdida saturada la señal que llega al generador es
de `0,00111`; con la no saturada, de `0,99889`. Son casi mil veces más. Esa es toda la
diferencia entre aprender algo y quedarse parado.

Segundo ejemplo, el **colapso de modos**. Los datos son una mezcla de dos gaussianas
centradas en −2 y +2. El generador no puede cubrir las dos y prueba dos alternativas: cubrir
un solo modo o repartirse ancha por el centro:

```
generador          KL(p_g||p_d)   KL(p_d||p_g)
un solo modo           0.693          12.175
ancha y centrada       1.909           0.800
```

Un generador que solo cubre un modo tiene una divergencia `KL(p_g‖p_d)` de `0,693` (el log 2
de haber ignorado la mitad de la masa, más un poco) y sin embargo es penalizado con `12,175`
si se mide en el sentido contrario. La razón es que `KL(p_g‖p_d)` solo castiga poner masa
donde no hay datos, y le da igual dejar datos sin cubrir. Un modelo que minimice ese sentido
prefiere concentrarse en un modo seguro antes que arriesgarse a caer en zona vacía: eso es
exactamente el colapso de modos, y explica por qué aparece tanto en GAN y tan poco en modelos
de verosimilitud.

## Código

```python verificable
import numpy as np

# Discriminador optimo: D*(x) = p_d(x) / (p_d(x) + p_g(x)).
# La senal que llega al generador incluye dD/da = D*(1 - D*).
p_d = np.array([0.001, 0.02, 0.30, 0.50, 0.90])
p_g = np.array([0.90, 0.50, 0.30, 0.02, 0.001])
# La division va elemento a elemento: son dos arrays de la misma forma, no matrices.
D = p_d / (p_d + p_g)

print("zona      D*   minimax D(1-D)   no saturada 1-D")
for i, d in enumerate(D):
    print(f"{i:>4}  {d:6.3f}  {d * (1 - d):14.5f}  {1 - d:14.5f}")
# -> zona      D*   minimax D(1-D)   no saturada 1-D
# ->    0   0.001         0.00111         0.99889
# ->    1   0.038         0.03698         0.96154
# ->    2   0.500         0.25000         0.50000
# ->    3   0.962         0.03698         0.03846
# ->    4   0.999         0.00111         0.00111
```

```python verificable
import numpy as np

# Por que aparece el colapso de modos: la KL no es simetrica.
x = np.linspace(-8, 8, 4001)
dx = x[1] - x[0]        # paso de la rejilla: la integral de Riemann es una suma por dx


def normal(x, mu, s):
    return np.exp(-0.5 * ((x - mu) / s) ** 2) / (s * np.sqrt(2 * np.pi))


p_d = 0.5 * normal(x, -2, 0.5) + 0.5 * normal(x, 2, 0.5)   # datos bimodales
p_d = p_d / (p_d.sum() * dx)      # se renormaliza: la suma de la rejilla no da 1 exacto

candidatos = {"un solo modo": normal(x, -2, 0.5), "ancha y centrada": normal(x, 0.0, 1.6)}
for nombre, p_g in candidatos.items():
    p_g = p_g / (p_g.sum() * dx)      # normalizamos para que integre 1
    kl_pg_pd = np.sum(p_g * np.log(p_g / np.maximum(p_d, 1e-12))) * dx
    # np.maximum(y, 1e-12) evita el log(0) cuando una densidad es practicamente nula;
    # sin esa proteccion saldria -inf o nan y la comparacion no diria nada.
    kl_pd_pg = np.sum(p_d * np.log(np.maximum(p_d, 1e-12) / np.maximum(p_g, 1e-12))) * dx
    print(f"{nombre:>16}  KL(p_g||p_d)={kl_pg_pd:6.3f}  KL(p_d||p_g)={kl_pd_pg:8.3f}")
# ->     un solo modo  KL(p_g||p_d)= 0.693  KL(p_d||p_g)=  12.175
# -> ancha y centrada  KL(p_g||p_d)= 1.909  KL(p_d||p_g)=   0.800
```

:::claves
- `p_d / (p_d + p_g)` con dos arrays de la misma forma divide **elemento a elemento**: no es
  álgebra matricial ni el cociente de dos escalares. Si los tamaños no coinciden, NumPy avisa o
  emite un error de emisión (*broadcasting*), nunca hace lo que uno espera a ojo.
- `D * (1 - D)` sale directamente de la derivada de la sigmoide. `D` aquí ya es la probabilidad,
  no el logit; si te dan el logit `a`, la derivada es `sigmoid(a) · (1 − sigmoid(a))` y hay que
  aplicar la sigmoide antes.
- `(x - mu) / s` con `s` escalar funciona por *broadcasting*: se resta el mismo `mu` a las 4001
  posiciones. Si `mu` fuera una lista de dos valores, el resultado tendría dos filas y el `p_d`
  bimodal habría que sumarlo con cuidado.
- `dx = x[1] - x[0]`: la densidad es una función continua, no una probabilidad. Para sumarla y
  comparar hace falta multiplicar por el paso de la rejilla; sin el `* dx` los valores salen
  proporcionales al número de puntos que hayas puesto, no a la divergencia real.
- `.detach()` sobre las muestras falsas en el paso del discriminador es la línea que evita que el
  gradiente del discriminador llegue al generador. Quitarlo no da error, pero entrena las dos
  redes a la vez y estropea el juego.
- Los dos optimizadores (`opt_D`, `opt_G`) se construyen **antes** del bucle y se vacían con
  `zero_grad()` en cada paso. Reutilizar el mismo optimizador para las dos redes acumularía los
  gradientes de una en la otra.
:::

```python ilustrativo
# Esqueleto del bucle de entrenamiento: dos optimizadores y dos pasos por lote.
# Necesita GPU y un juego de imagenes real, por eso no se ejecuta aqui.
import torch
from torch import nn

G = Generador(z_dim=128)          # ruido -> imagen
D = Discriminador()               # imagen -> probabilidad de ser real
opt_G = torch.optim.Adam(G.parameters(), lr=2e-4, betas=(0.5, 0.999))
opt_D = torch.optim.Adam(D.parameters(), lr=2e-4, betas=(0.5, 0.999))
bce = nn.BCEWithLogitsLoss()

for reales in cargador_de_datos:                      # reales: (lote, C, H, W)
    z = torch.randn(reales.size(0), 128, device=reales.device)
    falsas = G(z)

    # Paso del discriminador: reales a 1, falsas a 0 (etiquetas suavizadas a 0.9)
    opt_D.zero_grad()
    perdida_D = bce(D(reales), torch.full((reales.size(0), 1), 0.9)) \
        + bce(D(falsas.detach()), torch.zeros(reales.size(0), 1))
    perdida_D.backward()
    opt_D.step()

    # Paso del generador con la perdida NO saturada: -log D(G(z))
    opt_G.zero_grad()
    perdida_G = bce(D(falsas), torch.ones(reales.size(0), 1))
    perdida_G.backward()
    opt_G.step()
```

## Errores típicos

- **Mirar la pérdida del discriminador para decidir si el generador mejora.** Si `D` aprende
  rápido, su pérdida baja y la del generador sube; eso no significa que el generador empeore,
  significa que el rival es más fuerte. La pérdida de una GAN **no es comparable entre
  carreras ni entre iteraciones** y no mide calidad de muestras. Para juzgar necesitas
  inspección visual, métricas de distancia entre distribuciones de características o
  evaluadores externos, y siempre con varias semillas.
- **Usar la pérdida saturada `log(1 − D)` cuando el discriminador va ganando.** Es el error que
  hizo falta corregir en el propio artículo original: el gradiente que llega al generador se
  multiplica por `D·(1 − D)` y, con `D(G(z)) = 0,001`, vale `0,00111` en vez de `0,99889`.
  Entrena el generador con `−log D(G(z))`.
- **Dejar que el discriminador se entrene hasta la perfección.** Un `D` óptimo es
  precisamente el punto donde el generador no tiene señal. En la práctica se usan menos pasos
  de `D` que de `G`, o un `D` con menos capacidad, o ruido en las etiquetas. Si tu `D` acierta
  el 100 % del lote, no estás entrenando un generador: estás entrenando un clasificador.
- **Confundir colapso de modos con sobreajuste.** El colapso no es que el generador memorice
  el conjunto de entrenamiento; es que reparte su masa en una región pequeña y segura y
  repite variaciones de lo mismo. La tabla de la divergencia lo enseña: la KL en el sentido
  `KL(p_g‖p_d)` premia la estrategia conservadora. Se combate con arquitectura, con más
  diversidad en el lote y, en el caso de imágenes, con discriminadores que miran varias
  escalas.
- **Comparar dos GAN por una única muestra o una única semilla.** El resultado de una carrera
  depende de la semilla de inicialización del generador y del orden de los lotes. Un cambio
  que parece una mejora puede ser ruido de una sola semilla. Fija las semillas, repite al
  menos tres veces y compara distribuciones de resultados, no capturas sueltas.
- **Dar por hecho que la GAN es la opción por defecto para generar.** Sin densidad explícita
  no tienes verosimilitud, el entrenamiento es inestable y la evaluación es difusa. Los
  [[modelos-de-difusion|modelos de difusión]] cambiaron el panorama precisamente porque
  entrenan con una pérdida de regresión estable, a cambio de un muestreo más lento. Si tu
  problema tolera muchas pasadas de red por muestra, empieza por ahí.

:::practica
enunciado: En una zona del espacio la densidad real es p_d = 0,001 y la del generador p_g = 0,90: el generador pone masa donde no hay datos. Calcula el discriminador óptimo D* y compara la señal de gradiente que le llega al generador con la pérdida saturada D(1−D) y con la no saturada 1−D.
pista: Con un discriminador óptimo, D* es el cociente entre p_d y la suma de las dos densidades.
solucion: D* = 0,001 / (0,001 + 0,90) = 0,001 / 0,901 = 0,00111. Saturada: D(1−D) = 0,00111 · 0,99889 = 0,00111. No saturada: 1 − D = 0,99889. La segunda es unas 900 veces mayor. Conclusión: donde el generador va perdiendo, la pérdida no saturada es la única que le da señal para corregir.
:::

## Comprueba que lo sabes

:::quiz
p: Con un generador fijo, ¿cuál es el discriminador óptimo según la teoría del juego?
o: D*(x) = p_d(x) / (p_d(x) + p_g(x)), la probabilidad de que x venga de los datos
o: D*(x) = 1 para todas las muestras reales y 0 para todas las falsas
o: D*(x) = p_g(x) / p_d(x), el cociente de verosimilitudes
a: 1
e: Optimizando el objetivo del discriminador punto a punto sale el cociente entre la densidad de datos y la suma de ambas densidades. La opción 2 describe un clasificador perfecto, que es el caso límite que apaga el gradiente del generador. La opción 3 es el cociente al revés y además no está acotado entre 0 y 1.
:::

:::quiz
p: ¿Por qué se entrena el generador con la pérdida no saturada −log D(G(z)) y no con log(1 − D(G(z)))?
o: Porque la pérdida no saturada es la que aparece en la demostración del equilibrio
o: Porque cuando el discriminador rechaza bien las muestras falsas, el gradiente de la versión saturada se multiplica por D(1−D) y se apaga
o: Porque log(1 − D) exige calcular una exponencial que es numéricamente inestable
a: 2
e: Las dos pérdidas comparten el mismo punto de equilibrio, así que la demostración no distingue. La diferencia está en el gradiente: la derivada de la sigmoide, D(1−D), es diminuta cuando el discriminador está seguro, y con D = 0,001 la señal cae de 0,999 a 0,001.
:::

:::quiz
p: El generador cubre solo uno de los dos modos de la distribución de datos. ¿Qué mide cada sentido de la divergencia de Kullback-Leibler?
o: KL(p_g‖p_d) penaliza poner masa donde no hay datos y vale poco; KL(p_d‖p_g) penaliza dejar datos sin cubrir y vale mucho
o: Las dos valen lo mismo porque la divergencia es simétrica
o: KL(p_g‖p_d) vale mucho y KL(p_d‖p_g) vale poco, y por eso el colapso es imposible
a: 1
e: La KL no es simétrica. En el ejemplo numérico, cubrir un solo modo da 0,693 en un sentido y 12,175 en el otro: el generador que minimiza el primer sentido no siente ninguna presión por cubrir el modo que ignora, y ahí está el colapso de modos.
:::
