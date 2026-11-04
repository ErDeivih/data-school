---
id: modelos-de-difusion
titulo: Modelos de difusión
fase: 7
nivel: experto
rutas: [ds]
prerequisitos: [autoencoders-y-vae, retropropagacion, funciones-de-perdida, optimizadores]
tags: [generativo, difusion, muestreo, deep-learning]
resumen: Un proceso fijo que destruye los datos con ruido y una red que aprende a deshacer un paso cada vez: generación estable a cambio de muestreo lento.
fuentes: ["Ho et al. (2020), 'Denoising Diffusion Probabilistic Models'", "Song et al. (2021), 'Denoising Diffusion Implicit Models'"]
---

## En una frase

Se define un proceso que va añadiendo ruido a los datos hasta convertirlos en ruido puro, y
se entrena una red para que deshaga **un solo paso** de ese proceso; generar una muestra es
aplicar esa red muchas veces seguidas, desde ruido hasta una imagen.

## La idea

Echa una gota de tinta en un vaso de agua. Al principio la gota tiene forma; a los pocos
segundos está difusa; al final el color se reparte por todo el vaso y no queda ninguna
estructura reconocible. Ese proceso de difusión es **físico, conocido y no hay que
aprenderlo**: solo hay que decidir cuánta tinta se mezcla en cada instante. Lo difícil es lo
contrario, reconstruir la gota a partir del agua teñida.

La clave del método es no intentar el salto completo. Reconstruir la gota original desde el
agua completamente teñida es imposible; quitar un poquito de difusión, casi nada, es fácil.
Así que se parte el problema en mil micrómetros de nada: la red ve `x_t` (una versión de la
imagen con un poco más de ruido) y predice el ruido que se añadió en ese paso. Encadenando mil
predicciones diminutas aparece la imagen. **Es una cadena de problemas fáciles en lugar de un
problema imposible.**

Esto resuelve la enfermedad que arrastraba una [[gan|GAN]]: aquí no hay adversario, no hay
equilibrio que buscar y la pérdida es un error cuadrático medio corriente, con lo que el
entrenamiento es tan estable como el de una regresión. El precio se paga al generar: una GAN
produce una imagen con una pasada de red, un modelo de difusión típico necesita cientos o
miles. Por eso la difusión ganó primero donde la latencia no importaba y por eso los
algoritmos de muestreo rápido (menos pasos, más listos) ocupan una parte importante de la
literatura reciente.

Hay una segunda lectura, muy útil: el proceso de ida define una jerarquía de niveles de ruido,
y la red aprende a **quitar ruido a cualquier nivel**. Eso da un modelo que sirve para
restaurar imágenes, para superresolución y para edición guiada, no solo para generar desde
cero. Un [[autoencoders-y-vae|VAE]] también descomprime desde un espacio latente, pero su
decodificador hace el trabajo de golpe; la difusión lo reparte en una cadena.

:::figura
fichero: modelos-de-difusion-senal-y-error
pie: Los dos paneles describen el mismo proceso desde dos lados, y juntos explican por qué la red tiene que saber en qué paso está. A la izquierda, los pesos de la forma cerrada: el peso de la señal (azul) y el del ruido (rojo) no son independientes, sus cuadrados suman 1 en todo momento. Hacia el paso 500 el ruido ya pesa más que la señal, y en el 900 la señal original es menos del 0,03 % de la varianza: ahí no queda estructura que recuperar, solo una mancha con un esbozo. A la derecha, la consecuencia práctica. La relación señal-ruido (verde) cae varios órdenes de magnitud y el factor de amplificación (morado) sube: un error de una décima al predecir el ruido mueve la estimación de `x_0` en 0,034 unidades cuando `t = 100`, pero en 15,7 cuando `t = 999`. La conclusión que importa: los primeros pasos, con mucho ruido, fijan la estructura global y los últimos solo eligen detalles, y sin embargo la pérdida `‖ε − ε_θ‖²` trata todos los pasos por igual. De ahí salen las variantes con pesos por paso.
fuente: figuras/modelos-de-difusion-1.py
:::

## Definición formal

El proceso directo (el de ida) es una cadena de Markov gaussiana fija:

:::formula
q(x_t | x_{t−1}) = N( √(1 − β_t) · x_{t−1} ,  β_t · I )
:::

- `x_0` — el dato real (una imagen, un vector de características).
- `x_t` — la versión con ruido en el paso `t`, con `t` de 1 a `T` (típicamente `T = 1000`).
- `β_t` — la varianza de ruido añadida en el paso `t`; el conjunto `{β_t}` es el **calendario**.
- `I` — la matriz identidad, que indica ruido independiente en cada dimensión.
- `N(μ, Σ)` — una normal multivariante de media `μ` y covarianza `Σ`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `T` | Número de pasos del proceso directo (típicamente 1000) | pasos | Cada paso añade menos ruido, así que el proceso destruye la señal más despacio y hace falta más tiempo para generar. Es el intercambio entre fidelidad del calendario y coste |
| `β_t` | Varianza del ruido que se añade en el paso `t` | varianza | Con `β` más grande se destruye más señal en cada paso: `ᾱ_t` cae antes y el modelo tiene menos pasos útiles con estructura |
| `ᾱ_t` | Producto acumulado de `(1 − β_s)`; cuánta señal original queda | adimensional, de 0 a 1 | Es lo que baja a lo largo de la cadena. Cuanto más alto, más limpia está la imagen en ese paso |
| `x_t` | La versión ruidosa del dato en el paso `t` | las de `x_0` | No es un parámetro, es el estado. Su escala la fijan `√ᾱ_t` y `√(1 − ᾱ_t)` |
| `ε` | El ruido concreto que se ha añadido, `N(0, I)` | las de `x_0` | Es lo que la red intenta predecir. Un error constante de 0,1 en `ε` se multiplica por `√((1−ᾱ_t)/ᾱ_t)` al estimar `x_0` |
| `1 − ᾱ_t` | La parte de varianza que ya es ruido | adimensional, de 0 a 1 | Al subir, la señal original pesa menos y la tarea de la red cambia por completo: por eso recibe también `t` |
:::

Como cada paso es gaussiano, se puede saltar de `x_0` a cualquier `x_t` en forma cerrada:

:::formula
x_t = √(ᾱ_t) · x_0 + √(1 − ᾱ_t) · ε ,   con ᾱ_t = Π_{s=1..t} (1 − β_s)  y  ε ∼ N(0, I)
:::

- `ᾱ_t` — el producto acumulado de `(1 − β_s)`; mide **cuánta señal original queda**.
- `ε` — el ruido concreto que se ha añadido, un vector normal estándar.
- `√(ᾱ_t)` y `√(1 − ᾱ_t)` — los pesos de señal y de ruido; sus cuadrados suman 1.

Entrenar es predecir ese `ε` con una red `ε_θ(x_t, t)`:

:::formula
L(θ) = E_{t, x_0, ε} [ ‖ ε − ε_θ(x_t, t) ‖² ]
:::

`θ` son los pesos de la red y `‖·‖²` es la norma euclídea al cuadrado. La red recibe el paso
`t` porque la tarea es distinta en cada nivel de ruido: no es lo mismo limpiar una imagen casi
limpia que una casi destruida. La relación señal-ruido es `SNR(t) = ᾱ_t / (1 − ᾱ_t)` y cae
varios órdenes de magnitud a lo largo de la cadena.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `θ` | Pesos de la red que predice el ruido | adimensionales | Más capacidad para ajustar el ruido de cada paso: baja la pérdida de entrenamiento, pero también la garantía de generalizar a datos no vistos |
| `ε_θ(x_t, t)` | El ruido que la red predice para esa imagen y ese paso | las de `x_0` | Si predice mejor, baja `L`. Un error de 0,1 se traduce en `0,1·√((1−ᾱ_t)/ᾱ_t)` de error en la estimación de `x_0`, que en `t = 999` vale 15,7 |
| `L(θ)` | Error cuadrático medio entre el ruido real y el predicho | las de `x_0` al cuadrado | Es lo que se minimiza. Solo es comparable entre experimentos con el mismo calendario y la misma parametrización, porque un calendario más agresivo baja `L` sin mejorar el modelo |
| `SNR(t)` | Relación señal-ruido en el paso `t`, `ᾱ_t / (1 − ᾱ_t)` | adimensional | Al subir, queda más señal y la tarea es más fácil; al bajar por debajo de 1 el ruido domina y el paso solo matiza |
:::

Para generar, se parte de `x_T ∼ N(0, I)` y se aplica hacia atrás, paso a paso:

:::formula
x_{t−1} = (1 / √(1 − β_t)) · ( x_t − (β_t / √(1 − ᾱ_t)) · ε_θ(x_t, t) ) + σ_t · z
:::

- `σ_t` — la desviación típica del ruido que se vuelve a inyectar en cada paso (menos en el último).
- `z ∼ N(0, I)` — ruido nuevo; es lo que hace que cada muestra generada sea distinta.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `σ_t` | Desviación típica del ruido que se vuelve a inyectar en el paso `t` | las de `x_0` | Cada muestra sale más distinta de las demás, pero con más ruido visible. Con `σ_t = 0` el muestreo es determinista y todas las muestras de la misma semilla coinciden |
| `z` | Ruido nuevo del paso, `N(0, I)` | las de `x_0` | Es la fuente de variedad: no cambia la estructura, cambia los detalles. Ponerlo a cero quita la diversidad entre muestras |
| `1 / √(1 − β_t)` | Factor que deshace la escala del paso hacia delante | adimensional | Al subir `β_t`, el factor crece y cada paso corrige una escala mayor: la cadena se vuelve más agresiva y más corta en pasos útiles |
| `β_t / √(1 − ᾱ_t)` | Cuánto del ruido predicho se resta en el paso | adimensional | Al subir `β_t` o al bajar `ᾱ_t` (pasos tardíos), este factor crece mucho: en los últimos pasos una predicción mala mueve la imagen entera |
| `T` | Número de pasos que hay que recorrer para generar | pasos | Más pasos dan muestras mejores y tardan más: es el coste que atacan los muestreadores deterministas, que generan con veinte o cincuenta |
:::

Con esta receta (el muestreo del artículo original) hacen falta los `T` pasos. Los muestreadores
deterministas posteriores permiten saltarse pasos y generar con veinte o cincuenta, porque
reinterpretan el proceso como una ecuación diferencial.

## Ejemplo

Con el calendario lineal `β` de `0,0001` a `0,02` en `T = 1000` pasos, esto es lo que queda de
la señal original:

```
 t      alpha_bar   sqrt(alpha_bar)   sqrt(1-alpha_bar)
 0        0.99990        0.9999            0.0100
 100      0.89514        0.9461            0.3238
 500      0.07780        0.2789            0.9603
 900      0.00027        0.0164            0.9999
 999      0.00004        0.0064            1.0000
```

En el paso 100 todavía queda el 89,5 % de la varianza de la señal; en el 500, menos del 8 %; en
el 999, prácticamente nada. Eso explica por qué la red tiene que saber en qué paso está.

El segundo número interesante es cuánto se amplifica un error al convertir una predicción de
ruido en una estimación de la imagen limpia, `x̂_0 = (x_t − √(1 − ᾱ_t)·ε̂) / √(ᾱ_t)`:

```
 t      SNR        1/SNR     error en x0 si eps falla 0.1
 100     8.53667      0.117        0.034
 500     0.08436     11.854        0.344
 900     0.00027   3699.353        6.082
 999     0.00004  24777.052       15.741
```

Con `x_0 = 0,7` y `ε` conocido, la reconstrucción es exacta (`0,700000`): la fórmula no
introduce error por sí sola. El problema es que `ε` nunca es exacto. Un error de una décima en
la predicción del ruido se traduce en un error de `0,034` en la imagen cuando `t = 100`, pero
de `15,7` cuando `t = 999`. Por eso los últimos pasos apenas cambian la estructura y los
primeros deciden los detalles: la pérdida simple `‖ε − ε_θ‖²` trata todos los pasos por igual
aunque su importancia sea muy distinta, y de ahí salen las variantes con pesos.

## Código

```python verificable
import numpy as np

# Calendario lineal: beta_t crece de 1e-4 a 0.02 en T pasos.
T = 1000
betas = np.linspace(1e-4, 0.02, T)
abar = np.cumprod(1.0 - betas)      # alpha_bar_t = producto de (1 - beta_s), s <= t

for t in (0, 100, 500, 900, 999):
    print(f"t={t:>4}  alpha_bar={abar[t]:.5f}  sqrt(alpha_bar)={np.sqrt(abar[t]):.4f}"
          f"  sqrt(1-alpha_bar)={np.sqrt(1 - abar[t]):.4f}")
# -> t=   0  alpha_bar=0.99990  sqrt(alpha_bar)=0.9999  sqrt(1-alpha_bar)=0.0100
# -> t= 100  alpha_bar=0.89514  sqrt(alpha_bar)=0.9461  sqrt(1-alpha_bar)=0.3238
# -> t= 500  alpha_bar=0.07780  sqrt(alpha_bar)=0.2789  sqrt(1-alpha_bar)=0.9603
# -> t= 900  alpha_bar=0.00027  sqrt(alpha_bar)=0.0164  sqrt(1-alpha_bar)=0.9999
# -> t= 999  alpha_bar=0.00004  sqrt(alpha_bar)=0.0064  sqrt(1-alpha_bar)=1.0000

# Forma cerrada: x_t = sqrt(alpha_bar) * x0 + sqrt(1 - alpha_bar) * eps
rng = np.random.default_rng(0)
x0, paso = 0.7, 500
eps = rng.normal()                  # un unico numero normal estandar, no un array
xt = np.sqrt(abar[paso]) * x0 + np.sqrt(1 - abar[paso]) * eps
# Al despejar x0 con el mismo eps sale 0.7 exacto: la formula no mete error por si sola.
recuperado = (xt - np.sqrt(1 - abar[paso]) * eps) / np.sqrt(abar[paso])
print(f"x_t={xt:.4f}  x0 original={x0}  x0 recuperado con el eps exacto={recuperado:.6f}")
# -> x_t=0.3160  x0 original=0.7  x0 recuperado con el eps exacto=0.700000
```

:::claves
- `np.cumprod(1.0 - betas)` es el producto acumulado, no la suma: `abar[t]` es el producto de
  todos los `(1 − β_s)` hasta `t`. Si usaras `np.cumsum` el número no significaría nada, porque
  las varianzas de pasos independientes se combinan multiplicando los factores.
- `np.linspace(1e-4, 0.02, T)` genera `T` puntos **incluyendo los dos extremos**: con `T = 1000`
  el paso es `0,02/999`, no `0,02/1000`. Cambiar `T` cambia el calendario entero, no solo su
  longitud.
- `abar[t]` se indexa con el paso como entero. En el código real los pasos vienen por lotes, y
  ahí hay que indexar con un array de índices (`abar[t_lote]`), no con un escalar: el
  *broadcasting* hace que cada imagen reciba su propio nivel de ruido.
- `rng.normal()` sin argumentos devuelve **un solo número** de tipo `float` de Python, no un
  array de un elemento. Es justo lo que hace falta para el ejemplo, pero en un modelo real el
  ruido tiene la forma de la imagen: `rng.normal(size=x0.shape)`.
- `np.sqrt(1 - abar[t])`: el `1 - abar` se calcula en flotante y a partir de `t ≈ 500` vale
  prácticamente 1. La resta no pierde precisión aquí porque `abar` es diminuto, pero el mismo
  patrón con números grandes sí la pierde: es la cancelación catastrófica.
- `for t in (100, 500, ...)` recorre una tupla escrita a mano. Si en su lugar pusieras
  `range(T)`, el bucle imprimiría mil líneas y la comparación que quieres ver se perdería.
:::

```python verificable
import numpy as np

T = 1000
abar = np.cumprod(1.0 - np.linspace(1e-4, 0.02, T))

# Al final de la cadena la senal es minima: un error pequeno en eps arruina la estimacion.
for t in (100, 500, 900, 990, 999):
    snr = abar[t] / (1 - abar[t])
    # sqrt((1 - abar) / abar) es el factor que multiplica al error de eps al despejar x0:
    # sale de dividir la formula de x_t entre sqrt(abar).
    ampl = np.sqrt((1 - abar[t]) / abar[t])
    print(f"t={t:>4}  SNR={snr:9.5f}  1/SNR={1 / snr:9.3f}"
          f"  error en x0 por 0.1 de error en eps={ampl * 0.1:8.3f}")
# -> t= 100  SNR=  8.53667  1/SNR=    0.117  error en x0 por 0.1 de error en eps=   0.034
# -> t= 500  SNR=  0.08436  1/SNR=   11.854  error en x0 por 0.1 de error en eps=   0.344
# -> t= 900  SNR=  0.00027  1/SNR= 3699.353  error en x0 por 0.1 de error en eps=   6.082
# -> t= 990  SNR=  0.00005  1/SNR=20672.767  error en x0 por 0.1 de error en eps=  14.378
# -> t= 999  SNR=  0.00004  1/SNR=24777.052  error en x0 por 0.1 de error en eps=  15.741
```

```python ilustrativo
# Esquema del bucle de entrenamiento (necesita GPU y un conjunto de imagenes):
#
#   x0 = lote de imagenes escaladas a [-1, 1]        # (lote, 3, 64, 64)
#   t  = enteros al azar en [0, T)                   # uno distinto por imagen
#   eps = torch.randn_like(x0)                       # el ruido que se anade
#   xt = sqrt(abar[t]) * x0 + sqrt(1 - abar[t]) * eps
#   perdida = mse(red(xt, t), eps)                   # se predice el ruido, no la imagen
#   perdida.backward(); optimizador.step()
#
# Y para generar:
#   x = torch.randn(1, 3, 64, 64)
#   for t in reversed(range(T)):                     # 1000 pasadas de red por muestra
#       x = un_paso_atras(x, red(x, t), t)
```

## Errores típicos

- **Creer que hay que entrenar el proceso de ruido.** El calendario `β_t` es una decisión de
  diseño, no un parámetro: no se aprende. Lo único que se entrena es `ε_θ`. Si tu pérdida baja
  pero las muestras siguen siendo ruido, el problema está en el modelo o en el condicionamiento
  por `t`, no en el calendario.
- **No escalar los datos al rango que espera el proceso.** Si dejas las imágenes en `[0, 255]`,
  la señal pesa 255 y el ruido `ε` pesa 1: el modelo tiene que predecir un ruido insignificante
  y la pérdida se queda plana. Se escala a `[−1, 1]` (o a media 0 y varianza 1) antes de
  definir `x_t`.
- **No condicionar la red por el paso `t`.** Sin `t`, la red ve entradas de niveles de ruido
  incompatibles y aprende la media de todas ellas: produce estimaciones borrosas y el muestreo
  se queda en una mancha gris. `t` entra como embedding posicional, igual que en un
  [[transformers|transformer]].
- **Comparar pérdidas de ruido entre experimentos con calendarios distintos.** El error
  cuadrático sobre `ε` baja automáticamente cuando el calendario destruye más la señal, aunque
  el modelo sea peor. La pérdida de entrenamiento solo es comparable con el mismo calendario y
  la misma parametrización.
- **Interpretar el error de `ε` como calidad de imagen.** Un MSE de ruido bajo no garantiza
  detalle: al final de la cadena, un error de `0,1` en `ε` mueve la estimación de `x_0` en
  `15,7`, y ese error se reparte por toda la imagen. Para juzgar hace falta muestrear y evaluar
  aparte.
- **Reducir los pasos de muestreo sin cambiar de muestreador.** El muestreo original necesita
  los `T` pasos porque en cada uno inyecta ruido calibrado para ese `β_t`. Si quieres 50 pasos,
  usa un muestreador determinista o un integrador diseñado para pasos grandes; recortar la
  cadena a lo bruto devuelve imágenes con ruido.

:::practica
enunciado: Con el calendario lineal de T = 1000 pasos en el que ᾱ₅₀₀ = 0,002778, el dato limpio es x₀ = 0,7 y la red predice el ruido con un error de 0,1. Calcula x_t, la relación señal-ruido y el error que ese fallo provoca en la estimación de x₀. ¿Se puede confiar en los pasos finales?
pista: x_t = √ᾱ·x₀ + √(1−ᾱ)·ε, y el error en x₀ es ε_err · √((1−ᾱ)/ᾱ).
solucion: √ᾱ = 0,0527 y √(1−ᾱ) = 0,9986. Con ε = 1: x_t = 0,0527 · 0,7 + 0,9986 = 1,0355. SNR = 0,002778 / 0,997222 = 0,002785, luego 1/SNR = 359: la señal es el 0,28 % de la varianza. El error en x₀ vale 0,1 · √359 = 1,895, casi tres veces x₀. Conclusión: en los últimos pasos la red no fija estructura, solo elige entre lo ya esbozado.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué se aprende exactamente al entrenar un modelo de difusión como DDPM?
o: El calendario de ruido β_t de cada paso
o: Una red que predice el ruido ε añadido a una versión ruidosa de la muestra, dado el paso t
o: Una función que clasifica si una imagen es real o generada
a: 2
e: El calendario es fijo y se elige a mano; lo que se aprende es ε_θ(x_t, t) minimizando el error cuadrático contra el ruido real. La opción 3 describe el discriminador de una GAN, que aquí no existe.
:::

:::quiz
p: Con el calendario del ejemplo, en t = 900 queda ᾱ = 0,00027. ¿Qué implica eso al generar?
o: Que la red apenas puede aportar estructura en ese paso y que un error pequeño en ε se amplifica mucho al estimar x0
o: Que la imagen ya está reconstruida y los pasos siguientes son decorativos
o: Que el ruido añadido es tan pequeño que se puede ignorar
a: 1
e: Con ᾱ casi cero, la señal original es el 0,027 % de la varianza y el factor de amplificación √((1−ᾱ)/ᾱ) ronda 60: un error de 0,1 en ε mueve la estimación de x0 unas 6 unidades. Los pasos con mucho ruido son los que fijan la estructura global, no los decorativos.
:::

:::quiz
p: ¿Cuál es el principal intercambio entre una GAN y un modelo de difusión?
o: La difusión entrena de forma estable con una pérdida de regresión, pero necesita muchas pasadas de red para generar una muestra
o: La difusión genera en una sola pasada, pero su entrenamiento es inestable
o: Los dos entrenan igual y solo se diferencian en el tamaño del modelo
a: 1
e: La difusión cambia el juego adversarial por una regresión sobre ruido, y eso la hace mucho más estable; el coste aparece en la inferencia, donde hacen falta decenas o cientos de pasos. La opción 2 describe justo lo contrario.
:::
