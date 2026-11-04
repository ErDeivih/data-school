---
id: como-funciona-un-llm
titulo: Cómo funciona un LLM
fase: 8
nivel: intermedio
rutas: [ds]
prerequisitos: [tokenizacion, atencion, transformers]
tags: [llm, generacion, probabilidad, tokens]
resumen: Un LLM solo predice el siguiente token; todo lo demas (chat, código, resumenes) es repetir esa predicción dentro de una ventana de contexto.
fuentes: ["Jurafsky y Martin (2025), 'Speech and Language Processing'", "Bengio et al. (2003), 'A Neural Probabilistic Language Model'"]
---

## En una frase

Un modelo de lenguaje es una función que, dado un texto, asigna una probabilidad a cada
posible token siguiente; generar una respuesta consiste en elegir un token, añadirlo al texto y
volver a empezar.

## La idea

Olvida por un momento la palabra «inteligencia». Lo que hace el modelo, mecánicamente, es lo
mismo que el autocompletado del móvil: mirar el texto que tiene delante y decidir qué palabra
viene después. La diferencia es la escala y el material de entrenamiento: en lugar de aprender
de tus mensajes, ha leído una cantidad de texto que ninguna persona podría leer en varias
vidas, y en lugar de mirar las últimas tres palabras mira decenas de miles de tokens a la vez.

De esa única tarea salen cosas que no esperarías. Para predecir bien el siguiente token hay que
resolver, sin que nadie lo pida explícitamente, la concordancia gramatical, el género, la
estructura de un párrafo, la aritmética sencilla, el formato de un fichero JSON y una parte
considerable de los hechos del mundo. El modelo no tiene un módulo para cada cosa: todo eso
está repartido en los pesos, como una compresión con pérdida del texto con el que se entrenó.

Tres consecuencias prácticas que cambian cómo se usa la herramienta:

1. **No recuerda nada entre llamadas.** El modelo es una función pura: mismos pesos, misma
   entrada, misma distribución de salida. Cuando un chat «recuerda» lo que dijiste antes, es
   porque la aplicación le reenvía la conversación entera en cada petición. La memoria está en
   el programa, no en el modelo.
2. **No consulta una base de datos.** Cuando el modelo no sabe algo, no se queda callado: como
   su tarea es producir una distribución sobre el siguiente token, siempre elige uno. Si la
   información no está en los pesos ni en el contexto, elige el token que le parece más
   plausible, y eso es una
   [[alucinaciones-y-limites|alucinación]]: no es un fallo del sistema. Es la única salida
   posible para la tarea que tiene encomendada.
3. **La generación es secuencial y tiene coste.** Cada token generado requiere una pasada por
   el modelo, y el token que acabas de generar se convierte en parte de la entrada del
   siguiente. Por eso la respuesta aparece palabra a palabra y no de golpe, y por eso el coste
   crece con la longitud de lo que escribes y de lo que te contesta
   ([[coste-y-latencia|coste y latencia]]).

Un detalle que sorprende a quien empieza: el modelo no ve letras. Ve **tokens**, fragmentos de
texto de longitud variable que salen de un algoritmo de compresión de vocabulario
([[tokenizacion|tokenización]]). «Impresionante» puede ser dos o tres tokens; un número largo
puede ser cinco.

De ahí que contar palabras para estimar el coste o el tamaño de un prompt dé
siempre mal.

## Definición formal

Un modelo de lenguaje autorregresivo define una distribución sobre secuencias factorizándola
token a token:

:::formula
P(t₁, t₂, …, t_N) = Πᵢ₌₁ᴺ P(tᵢ | t₁, …, tᵢ₋₁ ; θ)
:::

- `t₁ … t_N` — la secuencia de tokens (el texto troceado).
- `P(tᵢ | t₁ … tᵢ₋₁ ; θ)` — la probabilidad que el modelo asigna al token `tᵢ` dado todo lo
  anterior y los parámetros `θ`. La salida del modelo es, en cada posición, un vector de
  probabilidades con una entrada por token del vocabulario.
- `θ` — los parámetros: millones o miles de millones de números ajustados durante el
  entrenamiento. **Su número es la cuenta de escalares aprendibles**, no una medida de
  inteligencia.

**Entrenamiento.** Se minimiza la entropía cruzada media sobre una secuencia, que es
la verosimilitud negativa:

:::formula
L = −(1/N) · Σᵢ₌₁ᴺ ln P(tᵢ | t₁, …, tᵢ₋₁ ; θ)
:::

- `N` — número de tokens de la secuencia.
- `ln` — logaritmo neperiano. Si el modelo da probabilidad 1 al token correcto, `L = 0`; si da
  1/C con `C` candidatos equiprobables, `L = ln C`.

**Perplejidad.** Es la exponencial de la pérdida: `PPL = exp(L)`. Se interpreta como «entre
cuántas opciones igualmente plausibles está dudando el modelo». Una perplejidad de 1,6 sobre un
texto significa que el modelo estaba muy seguro; una de 100 significa que no tenía ni idea.

**Muestreo.** La última capa produce logits `z₁ … z_C`. Se convierten en probabilidades con la
temperatura `T`:

:::formula
P(token = k) = exp(z_k / T) / Σⱼ exp(z_j / T)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `t₁ … t_N` | La secuencia de tokens que el modelo tiene delante | tokens | Alarga el contexto y encarece cada paso, pero no cambia los pesos |
| `P(tᵢ dado lo anterior ; θ)` | Probabilidad del token `i` condicionada a todo lo anterior | entre 0 y 1, suman 1 en cada posición | Si el modelo está bien entrenado, sube para el token correcto y baja para el resto |
| `N` | Tokens de la secuencia que se está midiendo | tokens | Más posiciones que promediar: la pérdida se estabiliza, no baja sola |
| `L` | Entropía cruzada media, o verosimilitud negativa | neperios (nats) | Peor modelo. `L = 0` solo si acierta con probabilidad 1 en todas las posiciones |
| `PPL` | Perplejidad: `exp(L)` | adimensional, «entre cuántas opciones duda» | Más incertidumbre. No es un porcentaje ni una probabilidad |
| `θ` | Los parámetros aprendidos | número de escalares | Más capacidad, más coste; no es una medida de inteligencia |
| `z_k` | Logit del token `k` | sin unidades, puede ser negativo | Más peso relativo para ese token en la distribución final |
| `T` | Temperatura del muestreo | positiva | Reparte la probabilidad: con `T` alta aparecen tokens de la cola. Con `T → 0` gana siempre el más probable |
| `k` de top-k | Cuántos tokens candidatos se conservan | tokens | Deja entrar más cola: más variedad y más riesgo de token absurdo |
| `p` de top-p | Probabilidad acumulada que hay que cubrir | entre 0 y 1 | Con `p` cerca de 1 el conjunto crece y la respuesta se vuelve más variable |
:::

- `z_k` — el logit del token `k`, la puntuación sin normalizar que sale de la red.
- `T` — la temperatura. `T = 1` deja las probabilidades como están; `T < 1` las concentra en
  los tokens más probables; `T > 1` las reparte.
- Cuando `T → 0`, todo el peso va al token más probable (**decodificación voraz**).
- **Top-k** limita el muestreo a los `k` tokens más probables; **top-p** (núcleo) limita al
  conjunto más pequeño cuya probabilidad acumulada supera `p`. Los dos se aplican antes de
  muestrear y sirven para no elegir nunca un token absurdo de la cola.

:::figura
fichero: como-funciona-un-llm-temperatura-y-perdida
pie: A la izquierda, los tres mismos logits pasados por la fórmula con tres temperaturas: con T = 0,5 la primera opción se lleva el 86 % de la masa; con T = 2,0 la cola crece y la respuesta deja de ser predecible. A la derecha, la ley de potencia de la pérdida en escala logarítmica: cada multiplicación por diez de parámetros baja la pérdida menos que la anterior y la curva se aplana contra el suelo irreducible. Fíjate en que la temperatura no toca el modelo: solo reparte una distribución que ya estaba calculada.
fuente: figuras/como-funciona-un-llm-1.py
:::

## Ejemplo

**Temperatura.** Un modelo devuelve estos tres logits para el siguiente token:
`[2,0, 1,0, 0,1]`. Aplicando la fórmula:

- Con `T = 1`: 0,659 / 0,242 / 0,099. El modelo duda entre las tres opciones.
- Con `T = 0,5`: 0,864 / 0,117 / 0,019. La primera opción se lleva casi todo.

Los mismos logits, dos comportamientos: con `T = 0,5` la respuesta será casi siempre la misma;
con `T = 1,2` variará entre ejecuciones y aparecerán opciones raras. La temperatura no cambia lo
que el modelo sabe, solo cómo de arriesgado es al elegir.

**Perplejidad.** Si el modelo asigna al token correcto las probabilidades 0,60, 0,50 y 0,80 en
tres posiciones consecutivas, la pérdida media es 0,4757 y la perplejidad 1,61. Un texto donde
el modelo acierta con probabilidad 0,8 en cada posición tiene perplejidad 1/0,8 = 1,25; uno
donde acierta con 0,1 tiene perplejidad 10.

**De dónde salen los parámetros.** Para un transformer con vocabulario de 50.257 tokens,
dimensión de modelo `d = 768`, 12 capas, MLP que expande a `4d` y pesos atados entre la
entrada y la salida:

```
embedding            38,597,376
posiciones              786,432
atencion + MLP        7,080,960 por capa
total               124,355,328
```

Unos 124 millones de parámetros. Fíjate en el reparto: la matriz de tokens y las 12 capas se
llevan casi todo, y la atención es solo una parte del bloque. Si duplicas `d`, la parte de
atención y MLP se multiplica por cuatro, porque todas esas matrices son de `d × d` o `d × 4d`.

## Código

```python verificable
import numpy as np

logits = np.array([2.0, 1.0, 0.1])     # puntuaciones del ultimo token del vocabulario

def softmax(z, temperatura=1.0):
    z = z / temperatura              # T<1 separa los logits (menos dudas); T>1 los acerca
    e = np.exp(z - z.max())            # restar el maximo evita desbordar el exp
    return e / e.sum()                 # divide entre la suma: asi el vector suma 1

p1 = softmax(logits, 1.0)
p05 = softmax(logits, 0.5)

print("temperatura 1.0 ->", " ".join(f"{p:.3f}" for p in p1))     # -> 0.659 0.242 0.099
print("temperatura 0.5 ->", " ".join(f"{p:.3f}" for p in p05))    # -> 0.864 0.117 0.019

# Perplejidad de una frase de tres tokens: exp(entropia cruzada media)
probs = np.array([0.60, 0.50, 0.80])   # probabilidad que el modelo dio al token correcto
entropia = -np.log(probs).mean()       # -log de cada acierto y media de los tres
print(f"entropia cruzada {entropia:.4f}  perplejidad {np.exp(entropia):.2f}")   # -> 0.4757  1.61
```

:::claves
- `softmax` devuelve **un array de NumPy**, no una lista: `p1` y `p05` se pueden restar, multiplicar o imprimir con formato, pero no son el mismo tipo que devuelve una función de Python con `list`.
- El `- z.max()` no cambia el resultado matemático, solo el orden de las cuentas: `exp` desborda a infinito con logits grandes y el máximo se resta para que el mayor valga `exp(0) = 1`. Si lo quitas, con un logit de 800 el resultado sale `nan`.
- El vector que sale de `softmax` **siempre suma 1**, pero eso no lo convierte en una probabilidad calibrada: es la confianza del modelo, y los modelos suelen estar seguros de más.
- Cambia `temperatura=1.0` por `temperatura=0`: la división da infinito o `nan` y el `print` revienta. La decodificación voraz no se consigue con `T = 0` sino con `argmax`.
- `-np.log(probs).mean()` es la entropía cruzada **media**: el signo menos convierte el logaritmo negativo en una pérdida positiva, y `.mean()` promedia posiciones de distinta longitud. Si sumaras en vez de promediar, la pérdida dependería del número de tokens y no podrías comparar dos frases.
- `np.exp(entropia)` es la perplejidad. Se calcula **fuera** del logaritmo porque es una exponencial: `exp(0,4757) = 1,61`, y por eso la perplejidad de acertar siempre con 0,8 es `1/0,8 = 1,25`.
- En el segundo bloque, `embed + posiciones + capas * por_capa` cuenta **parámetros**, no FLOPs: el cómputo de entrenar es otra cosa (`6·N·D`). Y la última línea usa `//`, división entera, para que el factor salga `4` y no `4.0`.
:::

```python verificable
# Cuenta de parametros de un modelo tipo transformer, capa por capa.
# Se supone que la proyeccion de salida reutiliza la matriz de entrada (pesos atados).
vocab, d, capas, contexto = 50257, 768, 12, 1024   # asignacion multiple: cuatro variables de golpe

embed = vocab * d
posiciones = contexto * d
por_capa = 4 * d * d + 8 * d * d + 4 * d   # atencion + MLP (d -> 4d -> d) + dos LayerNorm

total = embed + posiciones + capas * por_capa   # suma de los tres bloques
print(f"embedding            {embed:,}")        # -> 38,597,376
print(f"posiciones           {posiciones:,}")   # -> 786,432
print(f"atencion + MLP       {por_capa:,} por capa")   # -> 7,080,960 por capa
print(f"total                {total:,}")        # -> 124,355,328

# La atencion y el MLP crecen con d al cuadrado: duplicar d cuadruplica esa parte
print("factor al duplicar d:", 12 * (2 * d) ** 2 // (12 * d ** 2))   # -> 4
```

## Errores típicos

- **Creer que el modelo consulta una base de datos.** No busca en ningún sitio: la información
  está comprimida en los pesos, mezclada y con pérdida. Por eso puede recordar mal un detalle
  con total seguridad, y por eso la solución para datos concretos es dárselos en el contexto
  ([[rag-arquitectura|RAG]]) y no confiar en la memoria del modelo.
- **Confundir fluidez con corrección.** El modelo está optimizado para que el texto suene
  plausible, no para que sea verdadero. Una respuesta puede ser gramaticalmente impecable,
  coherente y completamente falsa; la fluidez no es evidencia de nada.
- **Contar palabras en vez de tokens.** La facturación, los límites de la
  [[ventanas-de-contexto|ventana de contexto]] y las estimaciones de coste van en tokens. Como
  regla de andar por casa, en español hay entre 3 y 4 caracteres por token, y los números y el
  código se llevan la peor parte.
- **Suponer que el modelo recuerda la conversación anterior.** Cada llamada es independiente:
  si tu programa no reenvía el historial, el modelo no tiene forma de saber qué se dijo. Y
  reenviarlo todo en cada turno es también la causa principal de que el coste crezca de forma
  cuadrática en una conversación larga.
- **Usar temperatura alta para extraer datos.** Si necesitas que la misma entrada dé siempre la
  misma salida, baja la temperatura y fija la semilla cuando la API lo permita; aun así, el
  muestreo con `T > 0` no garantiza reproducibilidad. Para datos estructurados hay diseños
  específicos ([[structured-output|salida estructurada]]).
- **Asumir que conoce hechos posteriores a su entrenamiento.** El modelo tiene una fecha de
  corte: a partir de ahí no sabe nada, y si le preguntas rellenará el hueco con lo más
  plausible. Cualquier dato que cambie con el tiempo (precios, versiones, normativa) va en el
  contexto, nunca en la memoria del modelo.

## Comprueba que lo sabes

:::quiz
p: ¿Qué calcula exactamente un LLM en cada paso de la generación?
o: La respuesta completa, que luego va escribiendo poco a poco
o: Una distribución de probabilidad sobre el siguiente token, dado todo el texto anterior
o: Una búsqueda del documento más parecido en su base de conocimiento
a: 2
e: El modelo es autorregresivo: en cada paso produce una distribución sobre el vocabulario y se elige un token, que pasa a formar parte de la entrada del paso siguiente. La respuesta no existe completa en ningún momento, y no hay ninguna base de documentos que consultar.
:::

:::quiz
p: Bajar la temperatura de 1,0 a 0,5, ¿qué cambia?
o: Hace que el modelo sepa más y cometa menos errores de contenido
o: Concentra la probabilidad en los tokens más probables, así que la salida es más repetitiva y menos variada
o: Aumenta la ventana de contexto disponible
a: 2
e: La temperatura solo reescala los logits antes de normalizarlos: no añade información ni toca el contexto. Con valores bajos el modelo elige casi siempre la opción más probable, lo que da respuestas más estables pero también más planas y con menos capacidad de explorar alternativas.
:::

:::quiz
p: Le preguntas por un dato que se publicó después de su fecha de corte. ¿Qué esperas?
o: Que diga que no lo sabe, siempre
o: Que produzca una respuesta plausible que puede ser falsa, porque su tarea es elegir el siguiente token más verosímil
o: Que consulte internet si el dato es público
a: 2
e: El modelo no tiene un mecanismo interno para distinguir «no lo sé» de «no estoy seguro»: siempre debe emitir una distribución. Si el dato no está en los pesos ni en el contexto, rellenará el hueco con lo más plausible, que es la definición práctica de alucinación.
:::
