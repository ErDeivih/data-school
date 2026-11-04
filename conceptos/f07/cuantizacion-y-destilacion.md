---
id: cuantizacion-y-destilacion
titulo: Cuantización y destilación
fase: 7
nivel: avanzado
rutas: [ds]
prerequisitos: [gpu-y-rendimiento, funciones-de-perdida, entropia-e-informacion, optimizadores]
tags: [cuantizacion, destilacion, inferencia, memoria]
resumen: Dos formas independientes de encoger un modelo: gastar menos bits por peso (cuantización) o entrenar una red pequeña que imite a una grande (destilación).
fuentes: ["Hinton et al. (2015), 'Distilling the Knowledge in a Neural Network'", "Jacob et al. (2018), 'Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference'"]
---

## En una frase

La cuantización reduce el número de bits con los que se guarda cada peso (de 32 a 8 o a 4) sin
cambiar la arquitectura; la destilación entrena un modelo pequeño para que reproduzca las
salidas de uno grande, y cambia el modelo en lugar de su precisión.

## La idea

Tienes un modelo que funciona y necesitas que quepa o que corra más rápido. Hay dos formas de
encogerlo y son independientes: **gastar menos bits por peso** o **tener menos pesos**.

La primera es como redondear la lista de precios de una tienda a céntimos en lugar de a
milésimas. Si un peso vale `0,0238471`, guardarlo como `0,0238` no cambia gran cosa el
resultado; si lo guardas con dos decimales, `0,02`, empiezas a notarlo. La ventaja es que
redondear no requiere reentrenar y reduce la memoria a la mitad (int8) o a la cuarta parte
(int4). La desventaja es que el error se acumula a lo largo de cientos de capas y que el rango
de cuantización lo decide el valor más extremo de cada grupo de pesos.

La segunda es como contratar a un aprendiz. El modelo grande (el profesor) no solo dice la
respuesta correcta: da una **distribución completa** sobre las clases, y esa distribución es
información valiosa. Si el profesor ve una imagen borrosa de un 3 y reparte `0,7` a la clase
«3», `0,25` a «8» y `0,05` al resto, está diciendo que ese 8 es una confusión razonable. El
aprendiz que aprende de esas probabilidades recibe mucha más señal por ejemplo que el que solo
ve la etiqueta «3». A eso se le llama conocimiento oscuro (dark knowledge) y es lo que hace
que un modelo pequeño destilado supere al mismo modelo pequeño entrenado con etiquetas duras.
La temperatura existe para **exagerar** esas probabilidades pequeñas: sin ella, un softmax con
logits muy separados da `0,999` a la clase correcta y deja el resto en ruido invisible.

Las dos técnicas se combinan: cuantizas el modelo destilado y acabas con un modelo pequeño y de
4 bits. También se combinan con el ajuste fino: QLoRA usa una base cuantizada y adaptadores en
precisión completa ([[fine-tuning-y-lora|QLoRA]]).

:::figura
fichero: cuantizacion-escalones-y-densidad
pie: Arriba, lo que se quería guardar (la recta gris) contra lo que se guarda de verdad: con 8 bits la escalera es tan fina que se confunde con la recta, y con 4 bits cada escalón mide 0,0017 y ningún peso cae donde debería. Abajo, los 4.000 pesos de una capa: con 8 bits la forma se conserva, con 4 bits se rompe en catorce barrotes. Ese es el sentido de la tabla de errores de más abajo: el salto de 8 a 4 bits multiplica el error por dieciocho porque los niveles positivos bajan de 127 a 7.
fuente: figuras/cuantizacion-y-destilacion-1.py
:::

:::figura
fichero: destilacion-temperatura-y-sennal
pie: A la izquierda, la misma salida del profesor con tres temperaturas: con τ = 1 la clase absurda recibe 0,011 y su señal se pierde en el gradiente; con τ = 4 recibe 0,181, diecisiete veces más. A la derecha está el motivo de fondo: si el estudiante entrena solo con la etiqueta dura, su pérdida es idéntica mueva lo que mueva el logit de la clase «confusión» (línea roja plana); el profesor con temperatura sí distingue, y por eso el estudiante pequeño destilado acaba superando al mismo modelo pequeño entrenado con etiquetas duras.
fuente: figuras/cuantizacion-y-destilacion-2.py
:::

## Definición formal

**Cuantización simétrica por grupo.** Dado un vector de pesos `w` y `b` bits, se elige una
escala `s` y se guarda un entero por peso:

:::formula
s = max|w| / (2^(b−1) − 1) ,   q_i = redondea(w_i / s)  ,   ŵ_i = s · q_i
:::

- `b` — bits por peso; `2^(b−1) − 1` es el mayor entero representable con signo (`127` para 8 bits).
- `s` — la escala, un único número real por grupo (todo el tensor o cada canal). Se toma el máximo
  del **valor absoluto**, porque la escala es simétrica respecto a cero.
- `q_i` — el entero que se guarda; ocupa `b` bits en lugar de 32.
- `w_i`, `ŵ_i` — el peso original y su reconstrucción `float`.
- `redondea(·)` — al entero más cercano; el error de cada peso queda acotado por `s / 2`.

Con escala **por tensor** el rango lo fija el peso más extremo del tensor entero, así que los
canales con valores pequeños pierden resolución. Con escala **por canal** (una `s` por fila o
por columna) cada grupo aprovecha su propio rango y el error baja, a cambio de más escalas que
guardar.

**Destilación con temperatura.** Sea `z_t` el vector de logits del profesor y `z_s` el del
estudiante para el mismo ejemplo. Se definen las probabilidades suavizadas `p^τ = softmax(z/τ)`
y la pérdida:

:::formula
L = (1 − λ) · CE( y , p_s^(1) )  +  λ · τ² · KL( p_t^τ ‖ p_s^τ )
:::

- `τ` — la temperatura; `τ = 1` es el softmax normal y `τ > 1` reparte la masa entre más clases.
- `λ` — cuánto pesa imitar al profesor frente a acertar la etiqueta.
- `y` — la etiqueta verdadera; `CE` es la entropía cruzada (véase [[entropia-e-informacion]]).
- `KL` — la divergencia de Kullback-Leibler entre la distribución del profesor y la del estudiante.
- `τ²` — factor de corrección: al derivar, el gradiente de la parte suave lleva un `1/τ²`, así
  que multiplicar por `τ²` mantiene el equilibrio entre los dos términos cuando cambias `τ`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `b` | Bits con los que se guarda cada peso | bits por peso (8, 4, 3) | El error de reconstrucción crece muy rápido: los niveles positivos pasan de 127 con 8 bits a 7 con 4, así que la escala se multiplica por 18 y con ella la cota `s/2` del error de cada peso. Por debajo de 4 bits casi siempre hace falta calibración o reentrenamiento |
| `s` | Escala de la cuantización: el paso entre niveles consecutivos | las del peso | Con `s` grande caben valores más extremos y cada escalón es más tosco: el error de cualquier peso queda acotado por `s/2`, así que doblar `s` dobla el error máximo. Un solo peso atípico que fije `s` para todo el grupo empobrece a todos los demás |
| `q_i` | El entero que se guarda en lugar del peso | adimensional, en el rango de `b` bits | No es una palanca: es lo que ocupa los `b` bits. Al subir `b` hay más enteros disponibles y `q_i` representa el mismo peso con más fidelidad |
| `w_i`, `ŵ_i` | El peso original y su reconstrucción tras cuantizar | las del peso | La diferencia `ŵ_i − w_i` es el error que se acumula capa a capa. Ojo: `ŵ_i` no es el peso que se usó al entrenar, es un valor nuevo que el modelo nunca vio |
| `redondea(·)` | Al entero más cercano | adimensional | Es el origen de todo el error: redondear hacia arriba o hacia abajo introduce como mucho medio escalón. Si truncaras en vez de redondear, el error se duplicaría y además sería siempre del mismo signo |
| escala del grupo | Si `s` es una sola para todo el tensor o una por canal | número de escalas a guardar | Pasar de una escala por tensor a una por canal baja el error sin tocar los bits (18,8 % en el ejemplo), a cambio de guardar un `float` más por grupo. Con valores atípicos persistentes en unos canales, es la primera palanca |
| `τ` | Temperatura del softmax del profesor | adimensional (τ = 1 es el softmax normal) | Reparte la masa entre las clases que no ganan: con τ = 1 la clase absurda recibe 0,011 y con τ = 4 recibe 0,181. Sube la entropía de la distribución del profesor y hace visible el conocimiento oscuro, pero por encima de cierto punto todas las clases se parecen y la señal se vuelve ruido |
| `λ` | Cuánto pesa imitar al profesor frente a acertar la etiqueta | adimensional, entre 0 y 1 | Con `λ → 1` el estudiante copia la distribución del profesor y puede heredar sus sesgos; con `λ → 0` la destilación desaparece y queda un entrenamiento normal con etiquetas duras, que es justo lo que se quería evitar |
| `z_t`, `z_s` | Logits del profesor y del estudiante para el mismo ejemplo | adimensionales (puntuaciones sin normalizar) | Son la entrada del softmax con temperatura. Si el profesor devuelve probabilidades ya normalizadas en lugar de logits, el softmax las vuelve a comprimir y la temperatura deja de tener el efecto buscado |
| `KL(·‖·)` | Divergencia de Kullback-Leibler entre las dos distribuciones suavizadas | bits o nats | Mide cuánto se desvía el estudiante del profesor. Al subir, el estudiante está menos parecido al profesor; el mínimo es 0 y no tiene techo, así que un valor alto domina el gradiente |
:::

## Ejemplo

Vector de 1.024 pesos con desviación típica `0,05`. Error de reconstrucción según los bits:

```
bits   error cuadratico medio   relativo a la desviacion tipica
  8              0.00045                        0.92%
  4              0.00816                       16.79%
  3              0.01860                       38.27%
```

Con 8 bits el error es menos del 1 % de la desviación de los pesos: en la práctica
imperceptible. Con 4 bits ya es el 17 %, y con 3 bits el 38 %: por eso el salto de 8 a 4 bits
suele necesitar calibración o reentrenamiento, y el de 4 a 3 es donde los modelos empiezan a
degradarse de verdad. La segunda mitad del ejemplo muestra el efecto de la escala por canal,
con la misma cuantización de 4 bits:

```
4 bits por tensor = 0.00816
4 bits por canal  = 0.00662
mejora            = 18.8%
```

Solo cambiando **cómo se elige la escala**, sin tocar el número de bits, el error cae un
`18,8 %`. Es el ajuste más barato que existe en cuantización.

Para la destilación, los logits `[5,0; 2,0; 0,5]` de un ejemplo (clase correcta, confusión
razonable, clase absurda) con tres temperaturas:

```
tau   correcta   erronea   absurda   entropia
  1     0.9426    0.0469    0.0105    0.2470
  2     0.7527    0.1680    0.0793    0.7145
  4     0.5565    0.2629    0.1807    0.9865
```

Con `τ = 1` la clase absurda recibe `0,0105`: prácticamente invisible en el gradiente. Con
`τ = 4` recibe `0,1807`, un valor diecisiete veces mayor, y la entropía sube de `0,247` a
`0,987`. Eso es exactamente lo que se quiere: que el estudiante reciba señal sobre **todas** las
clases, no solo sobre la ganadora.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(0)
w = rng.normal(0, 0.05, size=1024)      # los pesos de una capa, en float32


def cuantiza(w, bits):
    qmax = 2 ** (bits - 1) - 1
    escala = np.abs(w).max() / qmax     # escala simetrica respecto a cero
    return np.clip(np.round(w / escala), -qmax - 1, qmax) * escala


for bits in (8, 4, 3):
    error = np.sqrt(((w - cuantiza(w, bits)) ** 2).mean())
    print(f"{bits} bits  error cuadratico medio={error:.5f}"
          f"  relativo a la desviacion={error / w.std():.2%}")
# -> 8 bits  error cuadratico medio=0.00045  relativo a la desviacion=0.92%
# -> 4 bits  error cuadratico medio=0.00816  relativo a la desviacion=16.79%
# -> 3 bits  error cuadratico medio=0.01860  relativo a la desviacion=38.27%

# La misma cuantizacion de 4 bits, pero con una escala por canal de 256 pesos.
por_canal = np.concatenate([cuantiza(c, 4) for c in w.reshape(4, -1)])
print(f"4 bits por tensor={np.sqrt(((w - cuantiza(w, 4)) ** 2).mean()):.5f}"
      f"  4 bits por canal={np.sqrt(((w - por_canal) ** 2).mean()):.5f}")
# -> 4 bits por tensor=0.00816  4 bits por canal=0.00662
```

:::claves
- `np.round` usa el **redondeo bancario**: 0,5 va al entero par más cercano, así que `np.round(2.5)` da 2 y `np.round(3.5)` da 4. Con miles de pesos el sesgo se compensa y no se nota; con un grupo de pocos valores, sí.
- El `np.clip(..., -qmax - 1, qmax)` es defensivo y con esta escala no llega a hacer nada: como
  `s = max|w| / qmax`, el cociente vive en `[−qmax, qmax]` y `np.round` no puede salirse de ahí. El
  límite `−qmax − 1` solo se alcanza con la convención `s = max|w| / 2^(b−1)`, en la que el extremo
  negativo sí llega a `−128`.
- `cuantiza` **no modifica** `w`: devuelve un array nuevo (`np.round` y `*` crean copias). Eso importa porque al cuantizar en el sitio te quedarías sin los pesos originales para calcular el error.
- `w.reshape(4, -1)` parte el vector en 4 filas de 256 sin copiar datos, y las tres líneas del `concatenate` hacen **tres cuantizaciones independientes**: cada bloque calcula su propia escala con su propio máximo. Por eso `por_canal` tiene 4 escalas y `cuantiza(w, 4)` una sola.
- `np.sqrt(((w - cuantiza(w, bits)) ** 2).mean())` es la raíz del error cuadrático medio, no el error medio. `mean()` de NumPy promedia sobre todos los elementos sin que haya que decirle el eje.
- El error relativo se divide entre `w.std()` porque la desviación típica no cambia al cuantizar: así el número dice cuánto pesa el error comparado con el tamaño típico de los pesos. El cociente es adimensional, pero **no** es un porcentaje de acierto: un 16,79 % aquí significa un error de reconstrucción de ese tamaño, no que el modelo falle el 17 % de las predicciones.
- Ojo si pruebas el bloque con otros bits: hasta 53 sigue funcionando igual de bien, porque `float64` representa enteros exactos hasta `2^53`. Con 32 bits la escala sale del orden de `1e-10` y el error de reconstrucción es de `2,6e-11`: la cuantización es casi exacta. Por encima de unos 53 bits el redondeo al entero deja de ser exacto y el error se estanca en el propio límite de `float64`.
:::

```python verificable
import numpy as np

logits = np.array([5.0, 2.0, 0.5])      # la clase correcta, una confusion, una absurda


def softmax(z):
    e = np.exp(z - z.max())             # se resta el maximo por estabilidad numerica
    return e / e.sum()


for temperatura in (1, 2, 4):
    p = softmax(logits / temperatura)
    entropia = -(p * np.log(p)).sum()
    print(f"T={temperatura}  correcta={p[0]:.4f}  erronea={p[1]:.4f}"
          f"  absurda={p[2]:.4f}  entropia={entropia:.4f}")
# -> T=1  correcta=0.9426  erronea=0.0469  absurda=0.0105  entropia=0.2470
# -> T=2  correcta=0.7527  erronea=0.1680  absurda=0.0793  entropia=0.7145
# -> T=4  correcta=0.5565  erronea=0.2629  absurda=0.1807  entropia=0.9865
```

:::claves
- El bucle `for temperatura in (1, 2, 4)` pasa **enteros**, y `logits / temperatura` los convierte en `float64` sin avisar. Si escribieras `logits // temperatura` (división entera) obtendrías `[5, 1, 0]` con τ = 2 y las probabilidades no tendrían nada que ver.
- `z - z.max()` es la corrección de estabilidad, y no es opcional: `np.exp(5.0)` aún cabe, pero con logits de 800 (habituales en modelos grandes) `np.exp` desborda a `inf`, y `inf / inf` da `nan`. Restar el máximo deja el exponente mayor en 0, así que el mayor vale exactamente 1 y la suma nunca desborda. El resultado es idéntico al softmax sin corregir, solo que calculable.
- `p * np.log(p)` se calcula con `p` ya normalizado y la suma de las tres probabilidades es exactamente 1, así que `p[i]` y `1 - p[i]` coinciden al cuarto decimal. Con `np.log(p)` y una probabilidad de 0 saldría `-inf` y `0 * -inf` es `nan`: en una red real se usa `log_softmax` por eso.
- El softmax **no es invariante a la temperatura**: cambiar `τ` cambia la distribución, pero no los logits originales, que se quedan intactos. Con `τ` tendiendo a infinito las tres clases tienden a 1/3; con `τ` tendiendo a 0 la ganadora se lleva todo y las otras reciben 0.
:::

```python ilustrativo
# Cuantizacion con conocimiento del entrenamiento: cuantiza en el paso hacia delante
# y usa el estimador recto (straight-through) para que el gradiente siga pasando.
# Necesita GPU y un conjunto de calibracion.
import torch

class LinealCuantizada(torch.nn.Module):
    def __init__(self, entrada, salida, bits=8):
        super().__init__()
        self.peso = torch.nn.Parameter(torch.randn(salida, entrada) * 0.02)
        self.bits = bits

    def forward(self, x):
        qmax = 2 ** (self.bits - 1) - 1
        escala = self.peso.abs().amax(dim=1, keepdim=True) / qmax
        q = torch.clamp(torch.round(self.peso / escala), -qmax - 1, qmax)
        peso_falso = (q * escala - self.peso).detach() + self.peso   # recto: gradiente identidad
        return torch.nn.functional.linear(x, peso_falso)

# Con transformers, el equivalente ya empaquetado seria:
#   BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4")
```

## Errores típicos

- **Cuantizar todo, incluidas las capas sensibles.** Las primeras y las últimas capas, las
  normalizaciones y la salida suelen ser las más sensibles: cuantizarlas a 4 bits destroza la
  métrica mientras el resto aguanta. Lo habitual es mantener esas capas en 8 bits o en `float`,
  y cuantizar solo las capas lineales grandes.
- **Usar una escala por tensor con valores extremos.** Un solo peso outlier fija `s` para todo
  el grupo y deja a los demás con dos o tres niveles útiles. Con la misma cuantización de 4
  bits, pasar de escala por tensor a escala por canal mejora el error un `18,8 %` en el ejemplo.
  Si además hay outliers persistentes en unos canales concretos, se separan esos canales.
- **Cuantizar sin calibrar.** Para cuantizar activaciones (no solo pesos) hace falta un
  conjunto de datos representativo que fije los rangos: si calibras con recetas de cocina y
  sirves imágenes médicas, los rangos están mal y la precisión se hunde. La calibración es
  parte del procedimiento, no un detalle.
- **Suponer que 4 bits siempre es más rápido.** Menos memoria no es automáticamente menos
  tiempo: si el núcleo de cómputo no tiene instrucciones para ese formato, se descomprime a
  `float` para operar y se pierde la ventaja. Hay que medir latencia en el hardware de destino,
  no extrapolarla del tamaño del fichero.
- **Confundir destilación con comprimir el mismo modelo, y destilar con datos que no se
  parecen a los de despliegue.** Destilar exige entrenar otro modelo, con datos y cómputo, y con
  una arquitectura de estudiante elegida a mano: no es un comando que se aplica al fichero de
  pesos. Y el estudiante aprende la distribución del profesor **sobre los datos que le des**: con
  un conjunto de destilación estrecho hereda el sesgo y encima con menos capacidad para
  corregirlo.
- **Olvidar el factor τ² al cambiar de temperatura.** Si subes `τ` y no tocas la ponderación, el
  término suave pierde peso relativo porque su gradiente escala con `1/τ²`: el estudiante deja
  de mirar al profesor justo cuando más suave querías la señal.

:::practica
enunciado: Un grupo de 128 pesos tiene su valor máximo en 0,40. Cuantiza en 8 bits simétricos el peso 0,0238471: calcula la escala s, el entero q, el peso reconstruido y el error, y comprueba que no supera la cota s/2.
pista: Con 8 bits, 2^(8−1) − 1 = 127 es el mayor entero; la escala sale del peso más extremo del grupo, no de cada peso.
solucion: s = 0,40 / 127 = 0,0031496. q = redondea(0,0238471 / 0,0031496) = redondea(7,5715) = 8. ŵ = 8 · 0,0031496 = 0,025197. El error es 0,025197 − 0,0238471 = 0,00135, que queda por debajo de la cota s/2 = 0,001575. Conclusión: 8 bits reconstruye ese peso con un error de 1,3 milésimas, despreciable frente al rango del grupo.
:::

## Comprueba que lo sabes

:::quiz
p: Pasando de 8 a 4 bits en el ejemplo, el error relativo pasa de 0,92 % a 16,79 %. ¿Qué conclusión es correcta?
o: Que 4 bits es inutilizable siempre y hay que quedarse en 8
o: Que 8 bits es casi indoloro y 4 bits necesita calibración, escalas por canal o reentrenamiento para ser aceptable
o: Que el error es independiente del número de bits y solo depende del número de pesos
a: 2
e: El error de reconstrucción crece porque al pasar de 8 a 4 bits los niveles positivos bajan de 127 a 7, así que la escala s se multiplica por unas 18 veces y con ella la cota s/2 del error de cada peso. Con 8 bits el error es menos del 1 % de la desviación de los pesos; con 4 hay que compensar con escalas por canal, calibración o entrenamiento consciente de la cuantización.
:::

:::quiz
p: ¿Para qué sirve la temperatura τ en la destilación?
o: Para repartir la probabilidad entre las clases que no ganan y que el estudiante reciba señal sobre todas ellas
o: Para acelerar el entrenamiento del profesor
o: Para cuantizar los logits del profesor a menos bits
a: 1
e: Con τ = 1 la clase absurda recibe 0,0105 y su aporte al gradiente es casi nulo; con τ = 4 recibe 0,1807. La temperatura no toca al profesor, que ya está entrenado, ni tiene nada que ver con la cuantización.
:::

:::quiz
p: ¿Por qué se multiplica el término de destilación por τ²?
o: Porque la divergencia de Kullback-Leibler está definida en unidades al cuadrado
o: Porque el gradiente de la parte suave escala con 1/τ² y sin ese factor cambiaría el equilibrio entre imitar al profesor y acertar la etiqueta
o: Porque el softmax con temperatura alta devuelve valores más pequeños y hay que compensarlos para que la suma siga siendo 1
a: 2
e: Al derivar softmax(z/τ) respecto de los logits aparece un factor 1/τ²; multiplicar la pérdida suave por τ² deja su magnitud comparable a la del término con etiquetas duras. El softmax siempre suma 1 sea cual sea la temperatura, así que la opción 3 no aplica.
:::
