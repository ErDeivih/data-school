---
id: tokenizacion
titulo: Tokenización
fase: 7
nivel: intermedio
rutas: [ds]
prerequisitos: [regex-y-limpieza-de-texto, embeddings, procesamiento-de-texto-clasico]
tags: [texto, nlp, vocabulario, bpe]
resumen: Partir el texto en unidades antes de convertirlo en vectores: BPE, WordPiece y por qué los números, los acentos y las palabras raras se fragmentan de más.
fuentes: ["Sennrich, Haddow y Birch (2016), 'Neural Machine Translation of Rare Words with Subword Units'", "Schuster y Nakajima (2012), 'Japanese and Korean Voice Search'", "Kudo (2018), 'Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates'"]
---

## En una frase

Tokenizar es decidir en qué trozos se parte el texto antes de convertirlo en números: ni letras
sueltas (secuencias larguísimas sin significado propio) ni palabras enteras (vocabulario enorme
y palabras desconocidas), sino piezas intermedias que se repiten.

## La idea

Antes de que un modelo vea una sola letra, el texto pasa por el tokenizador. Es una decisión de
diseño con consecuencias muy visibles, y hay tres opciones posibles:

1. **Por caracteres.** Vocabulario diminuto y ninguna palabra desconocida, pero todo significado
   se diluye: «casa» son cuatro pasos y una frase de 20 palabras pasa a ser una secuencia de 100
   elementos. Gastas contexto en deletrear.
2. **Por palabras.** Cada token es una palabra. El vocabulario se dispara (en español, contar
   formas superficiales pasa de cien mil: correr, corrí, correré, corriendo...) y aparece el
   problema fatal: la palabra desconocida. Si el modelo nunca ha visto «microplasticos», se
   convierte en un símbolo especial que no aporta nada.
3. **Por subpalabras.** El término medio y el que se usa hoy. Las palabras frecuentes tienen su
   propio token; las raras se parten en trozos que sí se repiten. «microplasticos» puede quedar
   como «micro» + «plastic» + «os», y cada trozo tiene vector propio.

La forma clásica de construir ese vocabulario es **BPE** (*byte pair encoding*), que viene de la
compresión de datos. Su idea es de una simplicidad engañosa: empieza con símbolos sueltos y
**fusiona repetidamente el par de símbolos adyacentes más frecuente** del corpus, añadiendo un
token nuevo en cada fusión. Si «c» y «a» aparecen juntas muchísimo, se fusionan en «ca»; si «ca»
y «s», en «cas». Lo que más se repite acaba formando tokens largos y lo raro se queda en trozos
pequeños.

**WordPiece** (el tokenizador de BERT) es primo hermano con otra regla para elegir la fusión:
elige el par que más aumenta la verosimilitud del corpus, con una puntuación que divide la
frecuencia del par entre el producto de las frecuencias de sus partes. Los trozos que van en
medio de una palabra se marcan con un prefijo, en BERT `##`: «token» + «##ización».

**Byte-level BPE** (GPT-2 en adelante) da una vuelta más: parte de los **256 bytes** posibles en
lugar de caracteres. Como cualquier texto en UTF-8 se puede escribir byte a byte, **no existe la
palabra desconocida**: puede gastar más tokens, pero nunca se queda sin representación. Es el
motivo por el que los modelos actuales manejan emojis y alfabetos raros sin romperse.

Y un detalle que se cobra caro: **tokenizar no es lo mismo que normalizar**. Pasar a minúsculas o
quitar acentos cambia lo que el modelo ve: a veces interesa (búsqueda insensible a mayúsculas) y a
veces destruye información que el modelo usa (nombres propios, signos de interrogación). Lo
importante es que la decisión sea consciente y **la misma** en entrenamiento y en producción.

## Definición formal

Un tokenizador es una función `T` que lleva texto a una secuencia de identificadores enteros,
más un vocabulario `V` que asigna a cada identificador su trozo de texto:

:::formula
T(texto) = [i₁, i₂, …, i_L] ,  V = { (id_k, pieza_k) }
:::

- `L` — número de tokens de la secuencia. Es la unidad con la que se mide todo: el contexto del
  modelo, el coste por consulta y la longitud de las secuencias de entrenamiento.
- `pieza_k` — el trozo de texto del token `k`. Puede ser una palabra entera, un fragmento o un
  carácter.
- Si una palabra no está en `V`, se descompone en las piezas que sí están: por eso casi nunca
  aparece el token de desconocido.
- **Tokens especiales**: además del texto, el vocabulario reserva identificadores para marcar
  principio y fin de secuencia, separador entre dos frases, relleno y máscara. Ocupan sitio en la
  cuenta del contexto.

**BPE, paso a paso.** Sea `C` el corpus como secuencia de palabras, cada una descompuesta en
símbolos y con un marcador de fin `</w>`. Sea `V₀` el conjunto de símbolos iniciales:

1. Cuenta la frecuencia de cada par de símbolos adyacentes en todo el corpus.
2. Sea `(a, b)` el par más frecuente (los empates se rompen con un criterio fijo, p. ej. orden
   alfabético). Añade `ab` a `V` y sustituye todas las apariciones de `a` seguido de `b` por
   `ab`, en una única pasada.
3. Repite 1-2 hasta alcanzar el tamaño de vocabulario deseado.

El tamaño del vocabulario es, por tanto, `|V₀| + número de fusiones`.

**WordPiece.** La puntuación del par `(a, b)` es:

:::formula
puntua(a, b) = frec(ab) / ( frec(a) · frec(b) )
:::

- `frec(ab)` — veces que aparece el par unido en el corpus.
- `frec(a)`, `frec(b)` — veces que aparece cada símbolo por separado.
- Favorece pares que aparecen juntos **más de lo que el azar explicaría**, no los más frecuentes.

**WordPiece al codificar** no fusiona: busca la segmentación más larga posible de izquierda a
derecha y, si no puede cubrir la palabra, emite el token de desconocido.

**Presupuesto de contexto.** Si el modelo admite `M` tokens de contexto y el prompt consume `P`,
caben `M − P`; en palabras, aproximadamente `(M − P) / r`, con `r` el número de tokens por palabra
de **tu** idioma y **tu** tokenizador. `r` no es universal: depende del idioma, del dominio y de
cuántos números y símbolos haya.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `L` | número de tokens de la secuencia | tokens | Es la unidad con la que se mide todo: el contexto que ocupa, el coste de la consulta y la longitud con la que se entrena. Sube más deprisa que las palabras del texto, sobre todo con números y símbolos |
| `V` | vocabulario del tokenizador | piezas distintas | Un vocabulario mayor tiene piezas más largas y gasta menos tokens por palabra, a cambio de una tabla de embeddings más grande y de peor entrenamiento para las piezas raras |
| `pieza_k` | el trozo de texto del token `k` | — | Puede ser una palabra entera, un fragmento o un byte. Cuanto más cortas son las piezas, más tokens necesita la misma frase |
| `frec(ab)` | veces que aparece el par unido en el corpus | apariciones | Es el numerador de la puntuación de WordPiece: lo que se repite acaba formando tokens largos |
| `frec(a)`, `frec(b)` | veces que aparece cada símbolo por separado | apariciones | Son el denominador: si un símbolo es muy frecuente por su cuenta, la división baja la puntuación y el par no se fusiona aunque aparezca mucho |
| `V₀` | conjunto inicial de símbolos (caracteres, o los 256 bytes en byte-level) | símbolos | Su **tamaño** fija el suelo del vocabulario. Con byte-level son 256 fijos y por eso nunca hay palabra desconocida; el precio es más tokens por carácter |
| `M` | tokens de contexto que admite el modelo | tokens | Subir `M` da más sitio, pero multiplica la memoria de la atención con `M²`. El número de parámetros no cambia |
| `P` | tokens que consume el prompt | tokens | Cada token del prompt es uno menos para la respuesta. Es lo primero que se dispara cuando metes ejemplos en el mensaje |
| `r` | tokens por palabra de tu idioma y tu tokenizador | tokens/palabra | Es la regla de tres con la que estimas si algo cabe. En español con números y siglas sube mucho; usar el 1,3 del inglés subestima el consumo alrededor de un 25 % |
:::

## Ejemplo

Corpus de juguete con tres palabras y sus frecuencias: «baja» 5 veces, «bajo» 3 y «bajada» 2.
Cada palabra empieza como sus símbolos: `b a j a</w>`.

Cuatro fusiones, con los pares contados sobre todo el corpus:

- Pares más frecuentes al principio: `(a, j)` y `(b, a)`, los dos con 10 apariciones. Desempata
  el orden alfabético: se fusiona `(a, j)` → **`aj`**.
- Ahora `(b, aj)` tiene 10 apariciones → **`baj`**.
- Después `(baj, a</w>)` con 5 y `(baj, o</w>)` con 3 (el `</w>` impide que «baja» y «bajada» se
  fusionen por error).

Resultado sobre las tres palabras:

- «baja» (aparece 5 veces) → **1 token**: `baja</w>`.
- «bajo» (3 veces) → **1 token**: `bajo</w>`.
- «bajada» (2 veces) → **4 tokens**: `baj`, `a`, `d`, `a</w>`.

Eso es exactamente el compromiso: lo frecuente se comprime, lo raro se fragmenta. Y el
tokenizador nunca ha visto morfología: ha descubierto que «baj-» es una raíz útil solo contando
pares.

Otro ejemplo, con números, sobre el texto del bloque de código de abajo:

- 11 palabras y 68 caracteres: **6,18 caracteres por palabra**. A poco más de cuatro caracteres
  por pieza, esa frase no cabe en 11 tokens.
- 10 de los 68 caracteres son dígitos (el **15 %**), en solo dos cifras. Los números son densos en
  información y caros en tokens.
- Y la misma cantidad escrita de otra forma no gasta lo mismo: «1.234,56» son 8 caracteres y
  «1234.56» son 7. Con el trozo «1234» aprendido, la segunda versión puede costar un token y la
  primera varios.

:::figura
fichero: tokenizacion-bpe-y-coste
pie: La izquierda es el corpus de juguete de esta página, con las tres palabras y las fusiones que salen de contar pares: «baja» aparece 5 veces y acaba en una sola pieza, «bajo» 3 veces y también en una, y «bajada», que solo aparece 2 veces, se queda en cuatro trozos. Ese es todo el compromiso de la tokenización por subpalabras y conviene mirarlo en los dos sentidos: lo frecuente se comprime y sale barato, lo raro se fragmenta y cuesta cuatro veces más. Y no es un fallo del algoritmo: es exactamente lo que se le pide, porque el tokenizador nunca ha visto morfología y ha descubierto que «baj-» es una raíz útil solo contando pares. La consecuencia práctica está en la derecha. Una palabra normal en español se lleva alrededor de 1,35 tokens, pero una que contiene dígitos se va a 4: en un texto con números, contar tokens como si fueran palabras subestima el consumo alrededor de un 25 %. Eso significa que un documento que creías que cabía puede no caber, y que la factura de una API se calcula sobre algo que no has medido. La comprobación es siempre la misma y es barata: pasa el tokenizador real del modelo que vas a usar por una muestra representativa de tus datos y cuenta `input_ids`, no palabras.
fuente: figuras/tokenizacion-1.py
:::

## Código

```python verificable
from collections import Counter

# BPE minimo: fusiona el par de simbolos adyacentes mas frecuente del corpus.
corpus = {"baja": 5, "bajo": 3, "bajada": 2}

def piezas(p):
    return list(p[:-1]) + [p[-1] + "</w>"]      # </w> marca el fin de palabra

def contar(vocab):
    pares = Counter()                           # Counter devuelve 0 en una clave que no existe
    for pzas, n in vocab:
        for a, b in zip(pzas, pzas[1:]):        # empareja cada simbolo con el siguiente
            pares[(a, b)] += n                  # la clave es una TUPLA de dos simbolos
    return pares

vocab = [(piezas(p), n) for p, n in corpus.items()]
print("inicio:", vocab[0][0])                   # -> ['b', 'a', 'j', 'a</w>']

merges = []
for _ in range(4):
    # En caso de empate gana el par alfabeticamente menor: el criterio debe ser fijo.
    # El - delante de kv[1] ordena de mas a menos frecuente; str(kv[0]) desempata siempre igual.
    (a, b), n = sorted(contar(vocab).items(), key=lambda kv: (-kv[1], str(kv[0])))[0]
    merges.append((a + b, n))
    nuevo = []
    for pzas, cnt in vocab:
        salida, i = [], 0
        while i < len(pzas):
            if i < len(pzas) - 1 and pzas[i] == a and pzas[i + 1] == b:
                salida.append(a + b); i += 2    # una sola pasada: no se refusiona lo ya fusionado
            else:
                salida.append(pzas[i]); i += 1
        nuevo.append((salida, cnt))
    vocab = nuevo                               # se reasigna el nombre, no se toca la lista vieja

print("merges:", merges)
# -> [('aj', 10), ('baj', 10), ('baja</w>', 5), ('bajo</w>', 3)]
print("final :", [(cnt, pzas) for pzas, cnt in vocab])
# -> [(5, ['baja</w>']), (3, ['bajo</w>']), (2, ['baj', 'a', 'd', 'a</w>'])]
```

:::claves
- `pares = Counter()` y luego `pares[(a, b)] += n`: un `Counter` devuelve **0** para una clave que
  no existe, así que se puede sumar sin inicializar. Con un `dict` normal esa línea lanzaría
  `KeyError` la primera vez. Y la clave es una **tupla** `(a, b)`, no una cadena: por eso el par
  `('a', 'b')` no se confunde con el símbolo ya fusionado `'ab'`.
- `zip(pzas, pzas[1:])` recorre pares adyacentes: `pzas[1:]` es una **copia** de la lista sin el
  primer elemento, y `zip` se detiene en la más corta. Con una palabra de un solo símbolo,
  `pzas[1:]` está vacía y no se cuenta ningún par, que es justo lo que toca.
- `sorted(..., key=lambda kv: (-kv[1], str(kv[0])))[0]` ordena de menor a mayor y coge el primero:
  el `-` delante de la frecuencia lo convierte en «de mayor a menor». El `str(...)` no es
  decorativo: fija el desempate para que dos ejecuciones sobre el mismo corpus den **el mismo**
  vocabulario. Sin un criterio fijo los identificadores cambian entre entrenamientos y el
  tokenizador deja de encajar con el modelo.
- `i += 2` cuando hay fusión impide encadenar dos fusiones solapadas en la misma pasada. Con
  `i += 1` el resultado dependería del orden de recorrido y el mismo corpus daría vocabularios
  distintos según cómo estuviera escrito.
- `vocab = nuevo` **reasigna** el nombre a la lista nueva; no modifica la lista anterior, que se
  queda sin referencias. Con `vocab[:] = nuevo` cambiarías la lista original en el sitio: aquí da
  igual, pero no lo da si algo más la estuviera mirando.
- `merges.append((a + b, n))` guarda la frecuencia **en el momento de la fusión**, no la final.
  Por eso la lista `[('aj', 10), ('baj', 10), ('baja</w>', 5), ('bajo</w>', 3)]` se lee en orden:
  lo que más se repetía al principio es lo que acaba formando las piezas largas.
:::

```python verificable
# Los numeros son caros: miden poco y gastan muchos tokens.
texto = "El modelo cuesta 1.234,56 euros y pesa 7.000 millones de parametros."
# split() sin argumentos parte por cualquier espacio y agrupa los repetidos.
palabras, caracteres = texto.split(), len(texto)
print("palabras:", len(palabras))                                        # -> 11
print("caracteres:", caracteres)                                         # -> 68
print("caracteres por palabra:", round(caracteres / len(palabras), 2))   # -> 6.18
# El generador produce True y False; sum los cuenta como 1 y 0.
print("digitos:", sum(c.isdigit() for c in texto), "de", caracteres)     # -> 10 de 68

# La misma cantidad escrita de otra forma no ocupa lo mismo. len() cuenta CARACTERES, que
# no es lo que cuenta el tokenizador: el numero de tokens hay que medirlo con el.
print("1.234,56 ->", len("1.234,56"), "caracteres")   # -> 8 caracteres
print("1234.56  ->", len("1234.56"), "caracteres")    # -> 7 caracteres
```

```python ilustrativo
from transformers import AutoTokenizer

# El tokenizador debe ser exactamente el del modelo: otro parte el texto de otra forma.
tok = AutoTokenizer.from_pretrained("dccuchile/bert-base-spanish-wwm-cased")
piezas = tok.tokenize("Los microplasticos del mar Mediterraneo, en 2024.")
print(piezas)

# Cuantos tokens gasta un texto, y si cabe en el contexto disponible.
# tok(texto) devuelve un diccionario; los identificadores estan en "input_ids".
ids = tok("Un texto largo...")["input_ids"]
# model_max_length es el limite del MODELO, no del tokenizador que acabas de cargar.
print(len(ids), "tokens; quedan", tok.model_max_length - len(ids), "para la respuesta")
```

## Errores típicos

- **Contar tokens como si fueran palabras.** El contexto, el coste y la velocidad se miden en
  tokens. Un texto en español gasta bastante más de un token por palabra, y los números y las
  siglas mucho más. Mide con el tokenizador real de tu modelo: «una palabra, un token» solo vale
  para inglés sencillo.
- **Usar un tokenizador distinto del que espera el modelo, o suponer que dos modelos parten
  igual.** Los identificadores son posiciones en una tabla: si le pasas a un modelo los ids de
  otro tokenizador, no da error, simplemente produce basura. Y el mismo párrafo puede dar 400
  tokens con un tokenizador y 520 con otro: al cambiar de modelo, vuelve a medir tus datos antes
  de dar por hecho que caben. El tokenizador se guarda y se versiona **con** el modelo.
- **Elegir la longitud de fragmento en caracteres en lugar de en tokens.** Cortar por caracteres
  parte entidades por la mitad. Cuenta tokens con el tokenizador del modelo que vas a usar para
  incrustar y respeta un pequeño solapamiento. Es el primer punto donde falla un
  [[chunking-y-embeddings|sistema de troceado]].
- **Normalizar por costumbre.** Pasar a minúsculas y quitar acentos puede mejorar una búsqueda,
  pero destruye información si el modelo fue entrenado con texto normal (o al contrario: si espera
  minúsculas y le mandas mayúsculas, empeora sin dar ningún error). Comprueba qué normalización
  aplica el tokenizador y no añadas otra encima.
- **Confiar en que el modelo «ve» los dígitos.** La tokenización de números es irregular y heredada
  del corpus: unos se parten en trozos y otros en dígitos sueltos. Si tu tarea depende de comparar
  o calcular con números, dales un formato estable y haz el cálculo fuera del modelo.

:::practica
enunciado: Un documento tiene 4.000 caracteres y 700 palabras. En una muestra comprobaste que tu tokenizador gasta 1,35 tokens por palabra, pero las palabras con dígitos se fragmentan: este documento tiene 90 palabras así, a 4 tokens cada una en vez de 1,35. El modelo admite 2.048 tokens de contexto. ¿Cabe el documento entero?
pista: Separa las palabras normales de las numéricas y suma los dos presupuestos.
solucion: Palabras normales: 700 − 90 = 610, a 1,35 tokens = 824 tokens. Palabras con dígitos: 90 · 4 = 360 tokens. Total: 824 + 360 = 1.184 tokens. Cabe en 2.048 y sobran 864 para la respuesta. Ojo: sin contar la fragmentación de los números habrías estimado 700 · 1,35 = 945 tokens y subestimado el consumo un 25 %.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué hace exactamente una fusión de BPE?
o: Sustituye todas las apariciones del par de símbolos adyacentes más frecuente por un símbolo nuevo, en una sola pasada
o: Elimina del vocabulario las palabras que aparecen una sola vez
o: Divide las palabras largas en sílabas según reglas lingüísticas
a: 1
e: BPE no usa conocimiento lingüístico: cuenta pares adyacentes en el corpus y fusiona el más frecuente, añadiendo un token nuevo al vocabulario. Las palabras raras no se eliminan, se quedan fragmentadas en las piezas que sí sobrevivieron a las fusiones. La sustitución se hace en una pasada para que el resultado no dependa del orden de recorrido.
:::

:::quiz
p: ¿Por qué un tokenizador byte-level nunca produce una palabra desconocida?
o: Porque su vocabulario contiene todas las palabras de todos los idiomas
o: Porque parte de los 256 bytes posibles y cualquier texto en UTF-8 es una secuencia de bytes, así que siempre hay una descomposición válida
o: Porque traduce las palabras desconocidas a un símbolo especial con vector propio
a: 2
e: Con 256 símbolos base, cualquier cadena de bytes se puede representar, aunque sean muchos tokens por carácter. Es la razón de que los modelos actuales manejen emojis y alfabetos raros sin romperse. Ningún vocabulario contiene todas las palabras, y el símbolo de desconocido es precisamente lo que se quiere evitar.
:::

:::aviso
Antes de contar el coste de un sistema, mide con el tokenizador real: `len(tok(texto)["input_ids"])`
sobre una muestra representativa de tus datos, no sobre una frase de ejemplo. En textos en
español con números, siglas y signos, la estimación optimista se queda corta, y eso se paga en
factura o en fragmentos que no caben.
:::
