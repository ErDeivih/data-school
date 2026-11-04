---
id: modelos-multimodales
titulo: Modelos multimodales
fase: 8
nivel: intermedio
rutas: [ds]
prerequisitos: [como-funciona-un-llm, ventanas-de-contexto, embeddings]
tags: [multimodal, vision, audio, contexto]
resumen: Cómo una imagen o un audio acaban siendo tokens dentro del mismo contexto que el texto, cuánto ocupan de verdad y por qué el presupuesto manda antes que la calidad.
fuentes: ["Dosovitskiy et al. (2021), 'An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale'", "Radford et al. (2021), 'Learning Transferable Visual Models From Natural Language Supervision'", "Alayrac et al. (2022), 'Flamingo: a Visual Language Model for Few-Shot Learning'"]
---

## En una frase

Un modelo multimodal es un modelo de lenguaje al que se le ha enseñado a convertir imágenes, audio o
vídeo en el mismo tipo de número que ya usaba para el texto, de modo que todo entra por la misma
ventana de contexto y se paga por tokens, exactamente igual que una frase.

## La idea

Un modelo de lenguaje solo entiende una cosa: secuencias de vectores. Cuando le das texto, el
tokenizador convierte las palabras en identificadores y la tabla de *embeddings* los convierte en
vectores. Ahí dentro no hay letras: hay números.

La pregunta de los modelos multimodales es muy simple de enunciar: si dentro todo son vectores,
¿por qué no meter una imagen? La respuesta es que sí, y el truco está en el paso intermedio. Una
imagen no se tokeniza como el texto; se **codifica**:

1. **Trocear.** La imagen se corta en una rejilla de parches cuadrados. Cada parche son unos píxeles
   y se aplana en un vector.
2. **Codificar.** Cada parche pasa por un codificador de visión (típicamente un transformer de
   visión), que lo convierte en un vector. Un parche no significa nada por sí solo; después de
   codificarlo lleva información de su entorno, porque la atención ya lo ha mezclado con los demás.
3. **Proyectar.** Una capa lineal lleva ese vector a la dimensión que espera el modelo de lenguaje.
   Es el paso que hace que el vector de un parche y el de la palabra «gato» vivan en el mismo sitio.
4. **Encadenar.** Los vectores resultantes se pegan delante del texto y el transformer los procesa
   como cualquier otro token.

Eso es todo. El modelo no «ve»: recibe una lista más larga de vectores. Por eso la consecuencia más
importante de esta página es de contabilidad, no de arquitectura: **una imagen cuesta tokens**, y una
imagen grande cuesta miles. La factura y la ventana de contexto no distinguen entre un token de
texto y uno de imagen, aunque el trabajo de la máquina sí sea distinto.

La segunda decisión de diseño es dónde se juntan las dos modalidades:

- **Fusión temprana.** La imagen se convierte en tokens y entra en el mismo transformer que el texto
  desde la primera capa. Es más sencillo y más barato, y suele ser lo que hay detrás de un modelo
  abierto que acepta imágenes.
- **Fusión tardía.** Hay dos torres separadas y capas de atención cruzada por las que el texto
  consulta a la visión. Permite congelar el modelo de lenguaje y entrenar solo el conector, así que
  cuesta mucho menos entrenar; a cambio, la arquitectura es más complicada.

La tercera pieza, y la que más se olvida: **el conector se entrena con pares**. Para que el vector de
un parche de imagen caiga cerca del vector de su descripción, hace falta un corpus enorme de
imágenes con texto. Los modelos contrastivos tipo CLIP hacen precisamente eso: acercan la imagen a su
pie y alejan la imagen de los pies de las demás. Sin ese entrenamiento, la capa de proyección sería
una transformación lineal que no significa nada.

Y queda la advertencia que hay que leer antes de montar nada: **una tarea multimodal se rompe igual
que cualquier otra**, pero el diagnóstico es distinto. Si el modelo no encuentra un dato en un PDF
escaneado, puede ser que no esté, que esté en un parche que se cortó al trocear, que la resolución
haya quedado por debajo de lo legible o que el dato esté en una zona que el modelo no mira. Con
texto, verificar es fácil; con una imagen, la primera pregunta tiene que ser **cuántos tokens
ocupaba eso y a qué resolución entró**.

Conviene ver la forma del problema antes de seguir, porque aquí los órdenes de magnitud no son
intuitivos: una hora de audio con un codificador que emite 50 vectores por segundo ocupa 180.000
tokens, y eso no cabe en ninguna ventana de contexto que exista.

:::figura
fichero: multimodal-el-precio-en-tokens
pie: Arriba, cuántos tokens ocupa cada cosa según el parámetro que de verdad los mueve: los caracteres de texto, el lado de la imagen con parches de 16 píxeles y los segundos de audio con un codificador de 50 vectores por segundo. La barra del texto es tan corta que casi no se ve: una imagen de 336 por 336 píxeles ocupa más contexto que 2.000 palabras. Abajo a la izquierda, la misma imagen troceada en parches según su lado, en escala logarítmica: pasar de 224 a 448 píxeles no duplica el coste, lo multiplica por cuatro, porque el número de parches crece con el cuadrado del lado; el punto de 1.008 píxeles son 3.969 parches. Abajo a la derecha, el coste de atención con una imagen añadida a 600 tokens de texto: 1,8 veces con la imagen pequeña y 58 veces con la grande, porque la atención va con el cuadrado de toda la secuencia.
fuente: figuras/modelos-multimodales-1.py
:::

## Definición formal

Una imagen de lado `L` píxeles troceada en parches de lado `P` produce un número de vectores que
crece con el cuadrado del lado:

:::formula
n_parches = ⌈L / P⌉²        n_vectores ≈ n_parches
:::

Y la secuencia que ve el transformer es la concatenación de todas las modalidades:

:::formula
n_total = n_texto + n_visión + n_audio        coste_atención ∝ n_total²
:::

El coste de la atención crece con el cuadrado de la longitud total, así que los vectores de imagen no
solo ocupan sitio: multiplican el trabajo de cada capa.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `L` | Lado de la imagen cuadrada que entra al codificador | píxeles | El número de parches crece con `L²`: doblar el lado multiplica por cuatro los tokens de esa imagen, y multiplica por cuatro el coste de atención de esa parte |
| `P` | Lado del parche en que se trocea la imagen | píxeles | Parches más grandes dan menos tokens y menos detalle. Con `P = 16` y `L = 448` salen 784 tokens; con `P = 32`, solo 196. Es la palanca directa entre coste y resolución efectiva |
| `n_parches` | Número de vectores que produce la imagen | vectores | Es lo que se suma al contexto. Una sola imagen a 1.008 píxeles con parches de 16 son 3.969 vectores, más que muchas conversaciones completas de texto |
| `n_texto` | Vectores que ocupan las instrucciones y los datos en texto | tokens | Se suma a los de imagen antes de entrar al modelo, así que compite con ellos por la misma ventana |
| `n_audio` | Vectores que produce el audio, `segundos · vectores_por_segundo` | tokens | Un codificador a 50 vectores por segundo hace 3.000 tokens por minuto y 180.000 por hora: una hora de audio no cabe en la mayoría de ventanas. Se trocea, se resume o se transcribe antes |
| `n_total` | Longitud total de la secuencia que procesa el modelo | tokens | El coste de atención va con `n_total²` y la memoria con `n_total`. Es el número que hay que vigilar, no el de cada modalidad por separado |
| `d_modelo` | Dimensión a la que se proyectan todos los vectores | números por vector | No cambia cuánto ocupa la imagen en el contexto, pero sí el tamaño de la capa de proyección y el coste por token una vez dentro |
| `resolución efectiva` | Detalle que sobrevive al troceado | píxeles por parche | Es lo que decide si un texto pequeño de un documento se puede leer. Bajarla ahorra tokens y es la causa habitual de que el modelo «no vea» un número que sí está en la imagen |
:::

La parte que separa una prueba de concepto de un sistema que funciona es el presupuesto:

:::formula
tokens_disponibles = ventana − n_salida − margen        n_imágenes ≤ tokens_disponibles / n_parches
:::

Y la cuenta de dinero, que es donde se decide el diseño:

:::formula
coste_consulta = (n_texto + n_visión + n_audio) · precio_entrada + n_salida · precio_salida
:::

## Ejemplo

Una empresa digitaliza facturas. Cada factura se manda como imagen y el modelo tiene que extraer
proveedor, fecha e importe. Los números de la prueba de carga:

- Imagen escaneada a 1.008 por 1.008 píxeles, troceada en parches de 16 → 63 · 63 = **3.969 tokens**.
- Instrucciones y ejemplos en texto → **600 tokens**.
- Salida en JSON → **80 tokens**.
- Ventana del modelo → **128.000 tokens**.

El contexto de una consulta son 3.969 + 600 + 80 = 4.649 tokens, y cabe de sobra. El problema
aparece al mirar cuántas caben y qué cuesta cada una:

| Resolución de entrada | Parches con `P = 16` | Tokens de la imagen | € por 1.000 imágenes |
| --- | --- | --- | --- |
| 224 por 224 | 14 · 14 | 196 | 1,19 € |
| 336 por 336 | 21 · 21 | 441 | 1,92 € |
| 448 por 448 | 28 · 28 | 784 | 2,95 € |
| 672 por 672 | 42 · 42 | 1.764 | 5,89 € |
| 1.008 por 1.008 | 63 · 63 | 3.969 | 12,51 € |

Con un precio de entrada de 2,50 € por millón de tokens, la misma factura cuesta **diez veces más** a
1.008 píxeles que a 224. Y aquí viene la parte que decide: si a 224 píxeles el número de factura se
lee, no hay ninguna razón para mandar 1.008. La resolución no es una decisión de calidad abstracta;
es una decisión que se mide con el conjunto de facturas reales y se comprueba con la tasa de acierto
por campo.

El segundo número que sorprende es el del audio:

| Duración | Vectores por segundo | Tokens | ¿Cabe en 128.000 con 600 de texto? |
| --- | --- | --- | --- |
| 30 segundos | 50 | 1.500 | Sí, y sobrado |
| 10 minutos | 50 | 30.000 | Sí, con margen |
| 1 hora | 50 | 180.000 | No: ni siquiera cabe sin texto |

Una reunión de una hora no se manda entera. Se trocea por turnos, se transcribe a texto y se resume,
o se le pasa al modelo solo lo que se necesita. El codificador de audio no es caro por segundo; es
que **hay muchos segundos**.

Y el detalle fino de la ingeniería: no todas las imágenes cuestan igual aunque tengan el mismo
tamaño. Si el modelo sube la resolución interna cuando la imagen trae texto pequeño (algunos
sistemas ajustan el troceado a la resolución nativa), la misma factura puede consumir 3.969 tokens en
un caso y varias veces más en otro. Por eso la primera métrica que hay que instrumentar en un sistema
multimodal no es la latencia: es **tokens por documento**, con la resolución y el número de parches
al lado.

## Código

```python verificable
# Cuantos tokens ocupa una imagen segun como se trocee. La cuenta es cuadratica en el lado,
# y de ahi sale la regla practica: la resolucion se elige, no se hereda del escaner.
def parches(lado, troceado=16):
    import math
    n = math.ceil(lado / troceado)
    return n, n * n

print("lado  troceado  rejilla  tokens")
for lado in (224, 336, 448, 672, 1008):
    n, total = parches(lado)
    print(f"{lado:4d}  {16:8d}  {n:3d}x{n:<3d}  {total:6d}")
# ->  224        16   14x14      196
# ->  336        16   21x21      441
# ->  448        16   28x28      784
# ->  672        16   42x42     1764
# -> 1008        16   63x63     3969

# Con un parche mas grande hay menos tokens... y menos detalle por token.
print("mismo lado, distinto troceado:")
for troceado in (8, 16, 32):
    n, total = parches(1008, troceado)
    print(f"  parche de {troceado:2d} px -> {n:3d}x{n:<3d} = {total:6d} tokens")
# -> parche de  8 px -> 126x126   =  15876 tokens
# -> parche de 16 px ->  63x63    =   3969 tokens
# -> parche de 32 px ->  32x32    =   1024 tokens
```

:::claves
- La cuenta es `ceil(L / P)²`, no `(L / P)²`. Con `L = 1008` y `P = 32` la división da 31,5, y el `ceil` lo sube a 32: 1.024 tokens en lugar de 992. En una imagen da igual; en un documento de 200 páginas, ese redondeo es dinero.
- `parches` devuelve la rejilla y su cuadrado. La rejilla se imprime como `63x63` porque es lo que se piensa al depurar: si el modelo «no ve» algo, lo primero que se mira es en qué parche cayó.
- Bajar el troceado de 16 a 8 píxeles **multiplica por cuatro** los tokens (3.969 → 15.876), no los divide. Es la dirección que se olvida cuando alguien dice «aumentemos la resolución para que lea mejor»: cada mejora de detalle se paga al cuadrado.
- El lado se redondea hacia arriba antes de trocear: un parche incompleto en el borde suele rellenarse con ceros o descartarse, según el modelo, y eso también cambia la cuenta. Si vas a presupuestar en serio, mídelo con el tokenizador y el preprocesado reales, no con esta fórmula.
:::

```python verificable
# El presupuesto de contexto de un sistema multimodal: una sola consulta, tres modalidades.
VENTANA = 128_000
MARGEN_SALIDA = 2_000          # reservado para la respuesta, no se toca

def consulta(imagenes, lado, texto_tokens, segundos_audio, vectores_por_segundo=50, troceado=16):
    import math
    n = math.ceil(lado / troceado)
    tokens_imagen = n * n * imagenes
    tokens_audio = segundos_audio * vectores_por_segundo
    total = tokens_imagen + tokens_audio + texto_tokens
    cabe = total + MARGEN_SALIDA <= VENTANA
    return tokens_imagen, tokens_audio, total, cabe

for caso, imagenes, lado, texto, segundos in (
    ("una factura", 1, 1008, 600, 0),
    ("diez facturas", 10, 448, 800, 0),
    ("factura y llamada de 10 min", 1, 672, 600, 600),
    ("reunion de una hora", 0, 0, 600, 3600),
):
    timg, taud, total, cabe = consulta(imagenes, lado, texto, segundos)
    print(f"{caso:30s} imagen {timg:6d}  audio {taud:6d}  total {total:7d}  "
          f"{'cabe' if cabe else 'NO CABE'}")
# -> una factura                    imagen   3969  audio      0  total    4569  cabe
# -> diez facturas                  imagen   7840  audio      0  total    8640  cabe
# -> factura y llamada de 10 min    imagen   1764  audio  30000  total   32364  cabe
# -> reunion de una hora            imagen      0  audio 180000  total  180600  NO CABE

# Cuanto de la ventana se come cada modalidad: es el numero que hay que graficar en produccion.
for caso, imagenes, lado, texto, segundos in (
    ("diez facturas", 10, 448, 800, 0),
    ("factura y llamada de 10 min", 1, 672, 600, 600),
):
    timg, taud, total, _ = consulta(imagenes, lado, texto, segundos)
    print(f"{caso:30s} imagen {timg / total:5.1%}  audio {taud / total:5.1%}  "
          f"texto {texto / total:5.1%}")
# -> diez facturas                  imagen 90.7%  audio  0.0%  texto  9.3%
# -> factura y llamada de 10 min    imagen  5.5%  audio 92.7%  texto  1.9%
```

:::claves
- `MARGEN_SALIDA` se resta **antes** de comparar con la ventana. El error clásico es llenar el contexto con documentos de entrada y descubrir en producción que el modelo no tiene sitio para responder: la respuesta no sale truncada, sale peor.
- `n * n * imagenes` supone que todas las imágenes se trocean igual. En un sistema real no es así: una foto de móvil y un escaneo de fax no tienen los mismos píxeles, y el número de parches depende de la resolución que se use al preprocesar. Redimensiona tú a un lado fijo antes de contar; si dejas que lo haga el servidor, no sabrás por qué la factura del mes se dobló.
- Los porcentajes del segundo bloque son la herramienta de diagnóstico más útil: cuando una consulta multimodal se dispara de precio o de latencia, casi siempre hay una modalidad comiéndose más del 90 % de la ventana y nadie lo había medido. Con texto es raro; con audio es lo normal.
- `vectores_por_segundo = 50` es un valor de trabajo, no una constante del protocolo: cada codificador de audio emite a su ritmo y algunos comprimen mucho más. Lo que se comprueba aquí es la aritmética `segundos · vectores_por_segundo`; sustituye el 50 por el de tu modelo.
- Los dos casos se calculan por separado y no se comparan entre sí: son cargas distintas. Lo que se lee es la proporción dentro de cada uno.
:::

```python verificable
# El coste de atencion crece con el CUADRADO de la secuencia total. Los vectores de imagen
# no solo ocupan contexto: multiplican el trabajo de cada capa.
import numpy as np

N_TEXTO = 600
lados = np.array([224, 336, 448, 672, 1008])
parches = np.ceil(lados / 16) ** 2          # una imagen por consulta

for lado, n_vis in zip(lados, parches):
    total = N_TEXTO + int(n_vis)
    print(f"lado {lado:4d} -> {int(n_vis):5d} vectores de imagen, "
          f"secuencia {total:5d}, atencion relativa {total ** 2 / N_TEXTO ** 2:8.1f}x")
# -> lado  224 ->   196 vectores de imagen, secuencia   796, atencion relativa      1.8x
# -> lado  336 ->   441 vectores de imagen, secuencia  1041, atencion relativa      3.0x
# -> lado  448 ->   784 vectores de imagen, secuencia  1384, atencion relativa      5.3x
# -> lado  672 ->  1764 vectores de imagen, secuencia  2364, atencion relativa     15.5x
# -> lado 1008 ->  3969 vectores de imagen, secuencia  4569, atencion relativa     58.0x

# La memoria de la atencion va con la longitud, no con su cuadrado: hay que vigilar las dos.
for lado, n_vis in zip(lados, parches):
    total = N_TEXTO + int(n_vis)
    print(f"secuencia {total:5d} -> memoria de atencion relativa al texto solo: "
          f"{total / N_TEXTO:5.1f}x")
# -> secuencia   796 -> memoria de atencion relativa al texto solo:   1.3x
# -> secuencia  1041 -> memoria de atencion relativa al texto solo:   1.7x
# -> secuencia  1384 -> memoria de atencion relativa al texto solo:   2.3x
# -> secuencia  2364 -> memoria de atencion relativa al texto solo:   3.9x
# -> secuencia  4569 -> memoria de atencion relativa al texto solo:   7.6x
```

:::claves
- `np.ceil(lados / 16) ** 2` funciona porque NumPy aplica la operación a todo el vector de una vez. Con listas de Python haría falta una comprensión, y el `**` sobre una lista no existe: es el error de pasar de NumPy a listas sin darse cuenta.
- La «atención relativa» está normalizada contra el caso de solo texto (600 tokens), no contra el caso de imagen más pequeña. Es lo que hace legible la tabla: la imagen de 224 ya cuesta 1,8 veces más atención que el texto solo, y la de 1.008 casi 60 veces.
- `total ** 2` usa enteros de Python, que crecen sin desbordarse. Si lo hicieras con `np.int32` sobre secuencias de un millón de tokens, el cuadrado se sale del rango y el número sale negativo: otro motivo para no hacer estas cuentas dentro de un array con tipo fijo.
- Las dos tablas se leen juntas, y de ahí sale la decisión de ingeniería: la memoria crece de forma manejable (7,6 veces), pero el cómputo de atención crece 58 veces. Por eso se limita el número de parches y se agrupan las imágenes, en vez de subir la resolución «a ver si mejora».
:::

## Errores típicos

- **Creer que la imagen «no cuesta contexto».** Ocupa tokens exactamente igual que el texto, y una
  sola imagen a resolución completa puede ser más larga que toda la conversación. Si no mides tokens
  por documento, no sabes por qué se agota la [[ventanas-de-contexto|ventana de contexto]].
- **Subir la resolución para que lea mejor.** El número de parches crece con el cuadrado del lado:
  doblar el lado multiplica por cuatro los tokens y por cuatro el coste de atención de esa parte. Si
  el dato no se lee a 336 píxeles, muchas veces el problema es el troceado o el contraste, no la
  resolución.
- **Mandar una hora de audio entera.** A 50 vectores por segundo son 180.000 tokens: no cabe. Se
  trocea por turnos, se transcribe o se resume antes de entrar al modelo.
- **Suponer que el modelo «ve» como tú.** Un parche de 16 por 16 píxeles pierde los detalles finos:
  texto pequeño, sellos, firmas, casillas marcadas a lápiz. Lo que no sobrevive al troceado no llega
  al modelo, por mucho que esté en el fichero original.
- **Mezclar modalidades sin separadores ni etiquetas.** Si pegas tres imágenes y un texto sin decir
  qué es cada cosa, el modelo no sabe si la segunda imagen es el «después» o el «antes». Marca cada
  entrada con su papel, igual que harías con los documentos de un RAG.
- **Evaluar solo con ejemplos limpios.** Las capturas de móvil, los escaneos torcidos y las fotos con
  sombra son la mayoría de las entradas reales. Un conjunto de evaluación con documentos perfectos
  esconde justo los fallos que aparecen en producción.
- **Confundir multimodalidad de entrada con multimodalidad de salida.** Aceptar imágenes es una
  cosa; generar imágenes, otra completamente distinta, con otro modelo y otros problemas. Que el
  sistema entienda un gráfico no significa que pueda dibujarlo.

:::trampa
El error más caro es medir el coste con **una** imagen de prueba. Como el número de tokens depende
del cuadrado del lado, un conjunto de evaluación con documentos pequeños da un presupuesto optimista
que se rompe en el primer lote de escaneos a resolución completa. Mide la distribución de tokens por
documento (mediana y percentil 95), no la media de tres ejemplos.
:::

:::aviso
Los vectores que salen de una imagen no son texto: no los puedes loguear ni inspeccionar como una
cadena, así que un fallo de calidad se diagnostica mucho peor. Guarda la imagen original, la
resolución con la que entró y el número de parches de cada consulta. Sin esos tres datos, un
«el modelo se equivocó» no se puede reproducir.
:::

## Comprueba que lo sabes

:::quiz
p: Pasas de enviar imágenes de 224 por 224 píxeles a enviarlas de 448 por 448, con el mismo troceado de 16. ¿Qué pasa con los tokens de la imagen?
o: Se duplican, porque el lado se ha duplicado
o: Se multiplican por cuatro, porque el número de parches crece con el cuadrado del lado
o: No cambian: el troceado es el mismo, así que el número de parches es el mismo
a: 2
e: Con parches de 16, una imagen de 224 da 14 por 14 = 196 parches y una de 448 da 28 por 28 = 784: cuatro veces más. El troceado es el mismo, pero hay cuatro veces más trozos. Es la razón de que la resolución sea una decisión de coste y no solo de calidad.
:::

:::quiz
p: Una reunión de una hora se quiere pasar a un modelo multimodal por audio, con un codificador que emite 50 vectores por segundo. ¿Qué ocurre?
o: Cabe sin problema: 60 minutos son un dato pequeño
o: Son 180.000 tokens, así que no cabe en una ventana típica: hay que trocear, transcribir o resumir antes
o: Da igual, porque el audio no ocupa contexto, solo los primeros segundos
a: 2
e: La cuenta es 3.600 segundos por 50 vectores = 180.000 tokens, más que la mayoría de ventanas completas. El texto equivalente de una transcripción suele ocupar una fracción de eso, así que muchas veces sale más barato transcribir y pasar texto. La tercera opción confunde el audio con un resumen: los vectores entran todos.
:::

:::quiz
p: En un sistema de facturas, la imagen ocupa 3.969 tokens, las instrucciones 600 y la respuesta 80. Con una ventana de 128.000, ¿dónde está el problema real?
o: En la ventana, que se queda corta
o: En el coste por consulta y en la resolución elegida: la misma factura a 224 píxeles cuesta diez veces menos
o: En la salida, que ocupa demasiado
a: 2
e: 4.649 tokens caben de sobra en 128.000: el problema no es el tamaño, es el precio por documento y la decisión de resolución. La regla que ahorra dinero es mandar la resolución mínima con la que el campo se lee bien, comprobada contra facturas reales, no la resolución a la que venía el escáner.
:::

:::quiz
p: ¿Qué hace exactamente la capa de proyección de un modelo multimodal?
o: Comprimir la imagen para que ocupe menos tokens
o: Llevar los vectores que salen del codificador de visión a la dimensión que espera el modelo de lenguaje, para que convivan con los vectores del texto
o: Traducir la imagen a una descripción en texto que luego se tokeniza
a: 2
e: Es una transformación lineal que ajusta la dimensión, y se entrena con pares de imagen y texto para que el vector de un parche caiga cerca del de su descripción. No comprime (el número de parches lo fija el troceado) ni describe: si hubiera una descripción de texto por medio, el modelo no sería multimodal, estaría usando un modelo de texto sobre un resumen.
:::
