---
id: normalizacion-por-lotes
titulo: Normalización por lotes
fase: 7
nivel: avanzado
rutas: [ds]
prerequisitos: [escalado-y-transformacion, inicializacion-de-pesos, retropropagacion]
tags: [normalizacion, entrenamiento, estabilidad, lotes]
resumen: Reescala las activaciones de cada capa a media cero y varianza uno dentro del lote, y deja que la red reaprenda con dos parámetros la escala que le convenga.
fuentes: ["Ioffe y Szegedy (2015), 'Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift'", "Ba, Kiros y Hinton (2016), 'Layer Normalization'", "Santurkar et al. (2018), 'How Does Batch Normalization Help Optimization?'"]
---

## En una frase

Normalizar por lotes estandariza las activaciones que entran en cada capa —media 0 y varianza 1
dentro del lote— y después las reescala con dos parámetros entrenables, para que cada capa
reciba siempre una señal de tamaño parecido mientras las anteriores cambian.

## La idea

Imagina que entrenas a alguien a lanzar a canasta, pero la altura del aro cambia cada vez que
la persona mejora su técnica. Nunca aprende: cada ajuste que hace mueve el objetivo. Eso es lo
que pasa en una red profunda sin normalización. La capa 20 recibe las salidas de la capa 19, y
esas salidas cambian de escala y de distribución cada vez que la capa 19 actualiza sus pesos.
La capa 20 tiene que perseguir un blanco móvil. Normalizar entre capas equivale a **fijar la
altura del aro**: cada capa ve siempre una señal centrada y de escala controlada, y puede
concentrarse en su propio trabajo.

Hay un matiz que casi todo el mundo pasa por alto la primera vez: normalizar **solo** sería un
desastre. Restar la media elimina el sesgo de la capa anterior (el término constante se va con
la resta) y dividir por la desviación deja la señal en un rango estrecho donde, por ejemplo,
una sigmoide trabaja siempre en su zona casi lineal. Por eso la normalización lleva dos
parámetros aprendidos, `γ` y `β`: la red puede deshacer la normalización si le conviene, y de
hecho puede aprender la identidad. Lo que aporta es un punto de partida bien condicionado, no
una restricción.

Existen dos familias, y elegir mal es una fuente clásica de errores:

- **Por lotes (BatchNorm):** las estadísticas se calculan sobre el lote, por canal. Funciona
  muy bien en visión, pero tiene una consecuencia incómoda: la salida de un ejemplo depende de
  los otros ejemplos del lote. En entrenamiento se calculan las estadísticas del lote; en
  inferencia no hay lote, así que se usan unas **estadísticas acumuladas** que se actualizan
  durante el entrenamiento. Y con lotes pequeños esas estadísticas son ruido.
- **Por capa (LayerNorm):** las estadísticas se calculan sobre las características de **cada
  ejemplo por separado**, sin mirar al resto del lote. Da igual el tamaño del lote, funciona con
  secuencias de longitud variable y por eso es la normalización de las RNN y de los
  [[transformers|transformers]]. Su variante `RMSNorm` se salta la resta de la media y solo
  divide por la raíz de la media de cuadrados: más barata y suficiente en la práctica.

La explicación original atribuía la mejora a reducir el «cambio de covariable interno». Trabajos
posteriores —Santurkar y colaboradores, 2018— mostraron que la normalización ayuda sobre todo
porque **suaviza el paisaje de la pérdida** y hace que el gradiente apunte mejor, más que por
corregir ese desplazamiento. La receta funciona aunque la razón que se dio al principio fuera
incompleta.

:::aviso
Como la salida depende del lote, BatchNorm convierte al lote en una fuente de información
compartida entre ejemplos. En métodos contrastivos, donde los positivos y los negativos salen
del mismo lote, esa comunicación filtra información entre ellos y puede inflar los resultados.
:::

## Definición formal

Con un lote `B = {x₁, …, x_m}` de un canal (en una convolución, `m` incluye las posiciones
espaciales), la normalización por lotes hace:

:::formula
μ_B = (1/m) · Σᵢ xᵢ          σ²_B = (1/m) · Σᵢ (xᵢ − μ_B)²
:::

:::formula
x̂ᵢ = (xᵢ − μ_B) / √(σ²_B + ε)          yᵢ = γ · x̂ᵢ + β
:::

- `m` — número de elementos del lote para ese canal.
- `μ_B`, `σ²_B` — media y varianza del lote. La varianza divide por `m`, no por `m − 1`: es la
  varianza exacta del lote que estás normalizando, no una estimación de la población.
- `ε` — constante pequeña (1e-5 por defecto) que evita dividir por cero.
- `x̂ᵢ` — activación normalizada; su media en el lote es 0 y su varianza, 1.
- `γ`, `β` — escala y desplazamiento **aprendidos**, uno por canal. Con `γ = 1` y `β = 0` la
  salida es la normalizada pura.
- `yᵢ` — lo que sale de la capa y entra en la activación.

En inferencia no se usan las estadísticas del lote sino unas acumuladas durante el
entrenamiento, con una media exponencial de factor `α` (0,1 por defecto en PyTorch):

:::formula
μ̄ ← (1 − α) · μ̄ + α · μ_B          σ̄² ← (1 − α) · σ̄² + α · σ²_B
:::

- `μ̄`, `σ̄²` — estadísticas acumuladas; se usan tal cual, sin tocar los parámetros.
- `α` — cuánto pesa el lote actual en la media acumulada; con `α = 0,1` hacen falta unas diez
  actualizaciones para acercarse al valor real.

**LayerNorm** usa exactamente las mismas fórmulas, pero `μ` y `σ²` se calculan sobre las
características de un solo ejemplo (las últimas dimensiones del tensor) en vez de sobre el
lote. Como no dependen del lote, no hacen falta estadísticas acumuladas y el comportamiento en
entrenamiento y en inferencia es idéntico.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `m` | elementos del lote para ese canal (en una convolución incluye las posiciones espaciales) | elementos | Con más elementos las estadísticas del lote son menos ruidosas y el valor normalizado de un ejemplo depende menos de sus compañeros. Con `m = 1` la varianza es 0, la normalización devuelve 0 para todo y la capa se queda solo con `β` |
| `μ_B` | media del lote para ese canal | las de la activación | Se resta de cada valor: al subir, todas las activaciones normalizadas bajan. Es también el término que se lleva por delante el sesgo de la capa anterior |
| `σ²_B` | varianza del lote, dividiendo por `m` y no por `m − 1` | las de la activación al cuadrado | Divide la señal: al subir, la salida normalizada se encoge y esa unidad pierde contraste frente a las demás del mismo canal |
| `ε` | constante pequeña que evita dividir por cero (1e-5 por defecto) | las de la varianza | Con el valor por defecto es despreciable. Al subirlo mucho (1e-2) deja de dividir por la desviación real y la salida se queda centrada pero sin escala, que es justo lo que la normalización tenía que arreglar |
| `x̂` | activación normalizada | adimensional | Por construcción tiene media 0 y varianza 1 dentro del lote: no arrastra unidades ni escala. Es la señal que entra al reescalado, no la salida de la capa |
| `γ` | escala aprendida, una por canal | adimensional | Multiplica la salida: con `γ = 0` la capa queda muerta y solo pasa `β`; con `γ` grande se recupera la escala original y la normalización deja de notarse |
| `β` | desplazamiento aprendido, uno por canal | las de la salida | Mueve la salida en bloque. Es el sesgo que la resta de la media había eliminado y que la red vuelve a introducir aquí si le conviene |
| `α` | peso del lote actual en la estadística acumulada (0,1 por defecto) | adimensional, entre 0 y 1 | Con `α` alto las estadísticas de inferencia siguen al último lote y son ruidosas; con `α` bajo arrastran el sesgo inicial durante decenas de lotes, que es lo que estropea las métricas al principio |
| `μ̄` | media acumulada que se usa en inferencia | las de la activación | Arranca en 0 y sube poco a poco hacia la media real: mientras esté lejos, todas las predicciones en evaluación salen desplazadas |
| `σ̄²` | varianza acumulada que se usa en inferencia | las de la varianza | Igual que `μ̄`: al principio subestima, y una varianza demasiado pequeña infla la salida normalizada y amplifica el ruido |
:::

## Ejemplo

Un lote de cuatro activaciones: `[1, 2, 3, 4]`.

- Media: `μ_B = 10/4 = 2,5`. Varianza: `σ²_B = (2,25 + 0,25 + 0,25 + 2,25)/4 = 5/4 = 1,25`.
  Desviación: `√1,25 = 1,118`.
- Normalizadas: `x̂ = [−1,342, −0,447, 0,447, 1,342]`. Comprueba: la media es 0 y la desviación
  es 1 exactamente (salvo el efecto de `ε`, que aquí es despreciable).
- Con `γ = 2` y `β = 1`: `y = [−1,683, 0,106, 1,894, 3,683]`. La media pasa a 1 y la desviación
  a 2: la red ha recuperado la escala que quería.

Ahora las estadísticas acumuladas, empezando en `μ̄ = 0` y con `α = 0,1`, para tres lotes cuyas
medias son 3, 5 y 7: `μ̄` vale 0,3 tras el primero, 0,77 tras el segundo y 1,393 tras el
tercero. El valor real ronda 5 y la estimación va por 1,4: la media acumulada arrastra un sesgo
inicial importante durante las primeras decenas de lotes. Ese sesgo es la razón de que la
evaluación justo después de empezar a entrenar dé resultados raros.

Y el efecto del tamaño del lote sobre un mismo valor. En un lote `[1, 2]`, el valor 1 se
normaliza a `(1 − 1,5)/0,5 = −1`. En un lote de 1000 valores donde 999 son unos y uno es un 3,
ese mismo 1 se normaliza a `(1 − 1,002)/0,063 = −0,03`. El mismo dato, dos salidas distintas:
con lotes pequeños la normalización depende mucho de quién le acompañe.

:::figura
fichero: normalizacion-por-lotes-tamano-y-estadisticas
pie: El panel izquierdo sigue a un mismo dato —un 1— dentro de lotes donde todos sus compañeros valen 1 y uno solo vale 3. En un lote de dos ese 1 se normaliza a −1, casi el extremo; en uno de mil, a −0,03. El dato no cambió: cambiaron la media y la desviación con las que se normalizó, y por eso en BatchNorm la salida de un ejemplo depende de con quién le toque ir. Ahí está la razón práctica de que los lotes pequeños den resultados inestables y de que, cuando el lote no puede crecer, se pase a LayerNorm o a GroupNorm. El panel derecho enseña el otro extremo del mismo mecanismo: las estadísticas acumuladas que se usan en inferencia arrancan en cero porque nadie las ha visto todavía, y con α = 0,1 tardan unas diez actualizaciones en acercarse al valor real; tras tres lotes de media 3, 5 y 7 valen 1,39 cuando el valor real es 5. Con α = 0,01 el sesgo dura cientos de lotes. Conclusión: evaluar justo después de empezar a entrenar da métricas malas, y no es culpa del modelo.
fuente: figuras/normalizacion-por-lotes-1.py
:::

## Código

```python verificable
import numpy as np

x = np.array([1.0, 2.0, 3.0, 4.0])          # un canal, un lote de 4
media, var = x.mean(), x.var()               # varianza del lote: divide por m, no por m-1
# El 1e-5 va DENTRO de la raiz, como en la formula: sqrt(sigma^2 + eps), no sqrt(sigma^2) + eps
x_sombrero = (x - media) / np.sqrt(var + 1e-5)

gamma, beta = 2.0, 1.0                       # en una red de verdad, estos dos los aprende la capa
print(f"media {media:.2f}  varianza {var:.2f}  desviacion {np.sqrt(var):.3f}")
# -> media 2.50  varianza 1.25  desviacion 1.118
print(f"normalizado   {np.round(x_sombrero, 3)}")
# -> normalizado   [-1.342 -0.447  0.447  1.342]
print(f"con gamma y beta  {np.round(gamma * x_sombrero + beta, 3)}")
# -> con gamma y beta  [-1.683  0.106  1.894  3.683]
print(f"media de la salida {x_sombrero.mean():.4f}  desviacion {x_sombrero.std():.4f}")
# -> media de la salida 0.0000  desviacion 1.0000
```

:::claves
- `x.var()` de NumPy divide entre `m` (`ddof=0`), que es exactamente la varianza del lote que usa
  BatchNorm. Con `x.var(ddof=1)` saldría 1,667 en vez de 1,25: esa corrección sirve para estimar
  la varianza de una población a partir de una muestra, no para normalizar el lote que tienes
  delante. Con lotes grandes casi da igual; con lotes de 4, no.
- `(x - media)` **no modifica** `x`: crea un array nuevo. Si después del cálculo volvieras a usar
  `x`, seguirías teniendo `[1, 2, 3, 4]`. Solo `x -= media` cambia el original, y en una función
  eso sería un efecto colateral que nadie espera.
- `np.sqrt(var + 1e-5)` va con la suma **dentro** de la raíz, que es la convención de la fórmula
  `√(σ² + ε)`. Escribir `np.sqrt(var) + 1e-5` da prácticamente lo mismo, pero deja de coincidir
  con lo que dice el artículo y con lo que implementa PyTorch.
- `x_sombrero.mean()` no da 0 **exacto** ni `std()` da 1 exacto: el `ε` deja la desviación en
  0,999995 y el redondeo hace el resto. Con `:.4f` se ve `0.0000` y `1.0000`, pero la igualdad
  exacta no se cumple nunca. La propiedad se cumple «salvo el efecto de ε», no de verdad.
- `x.std()` divide también entre `m`, así que es coherente con `x.var()`. Mezclar `x.var()` con
  `x.std(ddof=1)` da una comprobación que no cierra por unos milésimos, y eso desconcierta
  cuando estás depurando una normalización propia.
- `x_sombrero` es un array de NumPy, no una lista: `np.round(x_sombrero, 3)` devuelve otro array y
  por eso al imprimirlo se ven los corchetes y los puntos, no las comas del texto de la página.
:::

```python verificable
import numpy as np

# El mismo valor se normaliza distinto segun el lote en el que caiga.
print(f"lote de 2     media {np.array([1.0, 2.0]).mean():.2f}  desviacion {np.array([1.0, 2.0]).std():.2f}")
# -> lote de 2     media 1.50  desviacion 0.50
grande = np.r_[np.full(999, 1.0), 3.0]   # np.full crea 999 unos y np.r_ los pega con el 3
print(f"lote de 1000  media {grande.mean():.3f}  desviacion {grande.std():.3f}")
# -> lote de 1000  media 1.002  desviacion 0.063

# Las estadisticas acumuladas arrancan sesgadas: es lo que se usa en inferencia.
media_movil = 0.0
for lote in (np.array([2.0, 4.0]), np.array([4.0, 6.0]), np.array([6.0, 8.0])):
    media_movil = 0.9 * media_movil + 0.1 * lote.mean()   # 0,9 y 0,1 son 1 - alfa y alfa
    print(f"lote de media {lote.mean():.1f}  media movil {media_movil:.3f}")
# -> lote de media 3.0  media movil 0.300
# -> lote de media 5.0  media movil 0.770
# -> lote de media 7.0  media movil 1.393
```

```python ilustrativo
import torch
import torch.nn as nn

# bias=False porque la normalizacion que viene despues ya resta la media
self.capa = nn.Linear(256, 256, bias=False)
self.bn = nn.BatchNorm1d(256)           # estadisticas por lote, un gamma y un beta por canal

def forward(self, x):
    return self.act(self.bn(self.capa(x)))

# En evaluacion hay que cambiar el modo o se usan las estadisticas del lote
modelo.train()
modelo(x_lote)
modelo.eval()                            # imprescindible: usa las medias acumuladas
with torch.no_grad():
    salida = modelo(x_test)

# LayerNorm: independiente del lote, la opcion en transformers y secuencias
self.ln = nn.LayerNorm(768)              # normaliza las 768 caracteristicas de cada ejemplo
self.rms = nn.RMSNorm(768)               # variante sin resta de la media
```

## Errores típicos

- **Olvidar `model.eval()` al evaluar.** En modo entrenamiento, cada predicción se normaliza con
  las estadísticas del lote en el que va: el mismo ejemplo da resultados distintos según con
  quién se agrupe, y las métricas de validación son basura. Es el error número uno con
  BatchNorm y con [[dropout-y-regularizacion|dropout]].
- **Usar BatchNorm con lotes de 1 o 2 en entrenamiento.** Con un solo elemento, la varianza del
  lote es 0 y la normalización devuelve 0 para todo: la capa se queda solo con `β`. PyTorch
  directamente lanza un error al detectarlo. Si no puedes subir el lote, pasa a
  `GroupNorm`/`InstanceNorm` o a LayerNorm.
- **Confundir BatchNorm con LayerNorm.** Con un lote de 32 ejemplos y 768 características, una
  normaliza sobre los 32 ejemplos de cada característica y la otra sobre las 768 características
  de cada ejemplo, y el resultado no se parece. En secuencias y en
  texto casi siempre quieres LayerNorm; en imágenes convolucionales, BatchNorm o GroupNorm.
- **Poner dropout justo después de BatchNorm.** En entrenamiento, el dropout cambia la varianza
  de lo que la normalización acabó de fijar; en inferencia el dropout no está y la estadística
  ya no coincide. El desajuste entre entrenamiento e inferencia degrada el resultado; si los
  combinas, revisa el orden y la escala.
- **Meter `γ` y `β` en el decaimiento de pesos.** Son parámetros de escala: encogerlos hacia
  cero deshace justo lo que la capa necesita. Exclúyelos del grupo con decaimiento, igual que
  los sesgos.
- **Calcular las estadísticas con todo el conjunto de datos.** Ajustar un escalador (o dejar que
  la normalización vea el conjunto de prueba) filtra información del test al entrenamiento: es
  [[fuga-de-datos|fuga de datos]] en su forma más silenciosa. Ajusta siempre con el
  entrenamiento y aplica lo aprendido a validación y prueba.

:::practica
enunciado: Un canal recibe el lote [2, 4, 4, 6]. Calcula su media y su varianza, normaliza y aplica γ = 0,5 y β = −1. Después, con α = 0,1 y μ̄ arrancando en 0, ¿cuánto vale μ̄ tras ese primer lote y por qué no se parece a 4?
pista: x̂ = (x − μ)/√(σ² + ε) y la salida es γ·x̂ + β. La media acumulada se actualiza con μ̄ ← 0,9·μ̄ + 0,1·μ_B.
solucion: μ = 16/4 = 4 y σ² = (4 + 0 + 0 + 4)/4 = 2, con desviación 1,414. Las normalizadas son (−1,414; 0; 0; 1,414) y con γ y β quedan (−1,707; −1; −1; −0,293). La media acumulada es 0,9·0 + 0,1·4 = 0,4: arranca en cero y tarda decenas de lotes en acercarse al valor real.
:::

## Comprueba que lo sabes

:::quiz
p: Un lote de un canal tiene los valores `[1, 2, 3, 4]`. ¿Cuál es su media y su varianza (la que usa BatchNorm)?
o: Media 2,5 y varianza 1,25
o: Media 2,5 y varianza 1,67
o: Media 2,5 y desviación 1,25
a: 1
e: La varianza es la media de las diferencias al cuadrado: (2,25 + 0,25 + 0,25 + 2,25)/4 = 1,25. El valor 1,67 saldría de dividir entre m − 1 = 3, que es la corrección de insesgadez para estimar la varianza de una población; BatchNorm usa la varianza exacta del lote. Y la desviación es √1,25 = 1,118, no 1,25.
:::

:::quiz
p: ¿Qué diferencia práctica hay entre BatchNorm y LayerNorm en una red de texto?
o: LayerNorm es más rápida porque no necesita estadísticas acumuladas
o: BatchNorm normaliza con las estadísticas del lote y depende de él; LayerNorm normaliza cada ejemplo por separado, así que funciona con lotes pequeños y secuencias de longitud variable
o: LayerNorm solo se puede usar en la primera capa
a: 2
e: La diferencia clave no es la velocidad sino de dónde salen la media y la varianza. Al depender del lote, BatchNorm hace que la salida de un ejemplo cambie con sus compañeros de lote y obliga a mantener estadísticas acumuladas para la inferencia; LayerNorm calcula sus estadísticas dentro de cada ejemplo y el comportamiento es idéntico en entrenamiento y en evaluación.
:::

:::quiz
p: Con `γ = 2` y `β = 1`, la salida normalizada de un lote que antes tenía media 2,5 y desviación 1,118 pasa a tener...
o: Media 0 y desviación 1
o: Media 1 y desviación 2
o: Media 2,5 y desviación 2,236
a: 2
e: La normalización deja media 0 y desviación 1; al multiplicar por γ y sumar β, la media pasa a ser β = 1 y la desviación se multiplica por el valor absoluto de γ = 2. Los parámetros sirven exactamente para eso: devolver a la capa la escala y el desplazamiento que le convienen, incluso si eso deshace la normalización.
:::

:::trampa
Si entrenas con lotes de 256 y evalúas con lotes de 1, en modo entrenamiento BatchNorm usará
una estadística y en modo evaluación otra muy distinta. Mantén siempre `model.eval()` en la
evaluación y comprueba la diferencia entre la pérdida de entrenamiento y la de validación con
los modos bien puestos antes de culpar al modelo.
:::
