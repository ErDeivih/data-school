---
id: escribir-tarjetas-de-repaso
titulo: Escribir tarjetas de repaso
fase: 0
nivel: básico
rutas: [core]
prerequisitos: [como-estudiar, mapa-del-portal]
tags: [estudio, repaso, memoria, anki]
resumen: Una tarjeta se escribe con una sola idea, con el contexto dentro del enunciado y con una respuesta que se pueda dar por buena o por mala sin discusión.
fuentes: ["Wozniak (1999), 'Effective learning: Twenty rules of formulating knowledge'", "Brown, Roediger y McDaniel (2014), 'Make It Stick: The Science of Successful Learning'", "Anki (2025), 'Anki Manual: Adding Cards'"]
---

## En una frase

Una tarjeta de repaso es la pregunta más pequeña que puedes contestarte a ti mismo en veinte
segundos: una sola idea, con el contexto dentro del enunciado y con una respuesta que no admita
discusión sobre si acertaste o no.

## La idea

El día del repaso la tarjeta aparece sola. Nadie te recuerda de qué capítulo salía, ni qué
librería estabas usando, ni en qué unidades medías. Lo único que tienes para responder es lo que
haya escrito en el enunciado, así que la primera regla es que **el contexto va dentro de la
tarjeta**: «¿qué separador usa `read_csv` por defecto?» se contesta en cualquier momento, mientras
que «¿cuál es el valor por defecto?» no significa nada fuera de su página.

La segunda regla es que la tarjeta tiene que **exigir recuperación**, no reconocimiento. Si la
respuesta se deduce de las opciones, si está medio escrita en el enunciado o si basta con leerla y
pensar «sí, eso era», no estás entrenando lo que necesitas en el trabajo. Reconocer es fácil y
produce una sensación de dominio que se cae en cuanto hay que producir la respuesta desde cero:
es exactamente la ilusión de fluidez contra la que avisa [[como-estudiar]].

La tercera es **una idea por tarjeta**, y no es una manía de purista. Una tarjeta que pregunta por
cuatro parámetros a la vez solo puede fallar en bloque: no te dice cuál de los cuatro no sabías y
te obliga a repasar los cuatro otra vez. Cuatro tarjetas de una idea fallan de una en una, y el
fallo señala justo el hueco.

La cuarta se olvida siempre: **la respuesta tiene que ser calificable**. El programador de repaso
de [[mapa-del-portal|el portal]] decide cuándo volver a preguntarte según lo que tú le dices. Si
ante una respuesta a medias dudas entre «bien» y «mal», el problema no es tu criterio: es que la
tarjeta está mal escrita. Una tarjeta que se puede contestar «depende» no programa nada, y acertarla
a la tercera no significa que la sepas.

De dónde salen las tarjetas nuevas: de cada concepto que leas (una o dos, no siete), de cada error
de depuración que te haya costado más de diez minutos, y de las [[tomar-notas-tecnicas|notas
técnicas]]. Y se tiran sin drama. Una tarjeta que fallas ocho veces no dice nada de tu memoria: dice
que está mal escrita o que el concepto no está entendido. Vuelve a la ficha, pártela en dos y sigue.

## Definición formal

Una tarjeta de repaso es un par ordenado `(enunciado, respuesta)` que cumple tres condiciones:

1. **Cerrada.** La respuesta es única y se puede comprobar sin criterio: un número, un nombre, una
   palabra, una línea de código o una lista corta y completa.
2. **Autosuficiente.** El enunciado lleva el contexto que haría falta fuera de su página: la
   librería, las unidades, el momento del pipeline.
3. **Atómica.** Contiene una sola idea. Si la respuesta pide un «y además», son dos tarjetas.

Cuando una tarjeta lleva `n` ideas y cada una se recuerda con probabilidad `p` —suponiendo que son
independientes entre sí—, la probabilidad de acertarla entera es:

:::formula
P(n) = p^n
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `p` | Probabilidad de recordar bien una idea suelta en el momento del repaso | entre 0 y 1 | La tarjeta se acierta más veces y su intervalo crece antes, así que sale de la cola |
| `n` | Número de ideas distintas metidas en la misma tarjeta | ninguna (recuento) | La probabilidad de acertarla entera se hunde: cada idea de más multiplica el fallo |
| `P` | Probabilidad de acertar la tarjeta entera | entre 0 y 1 | Si baja, la tarjeta vuelve a un día una y otra vez y no llega nunca a los intervalos largos |
:::

El precio de fallar no es el fallo, es que la tarjeta **no dice qué falló**. Con una idea, un fallo
es un dato; con cuatro, es una alarma sin dirección.

Y el intervalo que se juega la tarjeta es lo que decide si sale de la cola o se queda dando vueltas.
El programador del portal fija los dos primeros repasos (1 día y 6 días) y a partir de ahí alarga el
intervalo multiplicándolo por el factor de facilidad en cada acierto:

:::formula
intervalo_k = 6 · EF^(k−2)   para k ≥ 2
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `k` | Aciertos seguidos que lleva la tarjeta | ninguna (recuento) | El intervalo crece de forma multiplicativa (6, 15, 38, 95 días) y la tarjeta se aleja: es justo lo que se busca |
| `EF` | Factor de facilidad: cuánto se alarga el intervalo con cada acierto | ninguna (es un multiplicador) | Los intervalos se disparan y la tarjeta vuelve cada vez menos. Empieza en 2,5 y nunca baja de 1,3 |
| `intervalo_k` | Días hasta el siguiente repaso después del acierto número `k` | días | Es el hueco que se gana. Un fallo devuelve `k` a cero y con él el intervalo a 1 día |
:::

## Ejemplo

Una tarjeta real, de las que se escriben con prisa:

```text
P: ¿Qué parámetros tiene read_csv y para qué sirve cada uno?
R: sep, header, dtype, usecols, encoding, parse_dates, na_values, chunksize...
```

No se puede contestar de memoria, no se puede calificar y no te dice nada cuando falla. La misma
materia repartida en cuatro tarjetas cerradas, con una probabilidad de recordar cada idea de 0,9:

| Tarjeta | Ideas | Probabilidad de acertarla | Qué te enseña el fallo |
| --- | --- | --- | --- |
| La de arriba, entera | 4 | 0,66 | Que falla alguno de los cuatro, sin decir cuál |
| ¿Qué separador usa `read_csv` por defecto? | 1 | 0,90 | Que no tenías claro que es la coma |
| ¿Con qué codificación se abre un CSV que empieza con BOM? | 1 | 0,90 | Que `utf-8-sig` no te salía |
| ¿Para qué sirve `dtype=str` al leer un CSV? | 1 | 0,90 | Que no sabías que sirve para que Pandas no adivine los tipos |
| ¿Qué hace `na_values`? | 1 | 0,90 | Que no sabías convertir un centinela en nulo |

La aritmética de la columna del medio es toda la lección: 0,9 elevado a 4 es 0,66, así que la
tarjeta larga se falla una vez de cada tres y, cuando falla, no sabes por dónde empezar. Las cuatro
cortas se fallan una de cada diez veces cada una y cada fallo es una instrucción concreta.

El coste a largo plazo lo pone el programador. Con el intervalo que crece por `EF`, una tarjeta que
siempre se acierta recorre 1, 6, 15, 38, 95, 238, 595 y 1.488 días: ocho repasos cubren casi siete
años. Ocho repasos de una tarjeta que alterna acierto y fallo se quedan en 8 días, porque cada
fallo la devuelve al principio. Mismo esfuerzo, siete años de distancia.

## Código

```python verificable
# Una tarjeta con n ideas se acierta entera solo si se aciertan las n: P = p**n.
# Y como cada intento es independiente, los repasos hasta acertarla son 1/P.
p = 0.9
for n in (1, 2, 4, 8):
    print(f"{n} idea(s) en la tarjeta -> P = {p ** n:.3f}   repasos hasta acertar = {1 / p ** n:.2f}")
```

```python verificable
# Programador SM-2 simplificado, el mismo que usa el portal. Compara una tarjeta que se
# acierta siempre con una que alterna acierto y fallo: los mismos 8 repasos, otro resultado.
def redondear(v):
    return int(v + 0.5)

def programar(secuencia, ef=2.5):
    reps, intervalo, salida = 0, 0, []
    for acierto in secuencia:
        calidad = 4 if acierto else 1
        if calidad < 3:
            reps, intervalo = 0, 1                 # fallo: la tarjeta vuelve a 1 dia
        else:
            reps += 1
            intervalo = 1 if reps == 1 else 6 if reps == 2 else redondear(intervalo * ef)
        ef = max(1.3, ef + (0.1 - (5 - calidad) * (0.08 + (5 - calidad) * 0.02)))
        salida.append(intervalo)
    return salida

buena = [True] * 8
atascada = [True, False] * 4                       # se falla una de cada dos

print("tarjeta buena   :", programar(buena))
print("dias cubiertos  :", sum(programar(buena)), "con", len(buena), "repasos")
print("tarjeta atascada:", programar(atascada))
print("dias cubiertos  :", sum(programar(atascada)), "con", len(atascada), "repasos")
```

:::claves
- `p ** n` con `n = 4` y `p = 0,9` es 0,656: la tarjeta larga se falla un tercio de las veces. Si
  dentro de un mes te parece que «casi la sabes», ese 0,66 es la explicación.
- `1 / p ** n` es el número esperado de intentos hasta acertar, no una garantía. Con `P = 0,43` (ocho
  ideas) salen 2,32 intentos de media, y una racha de cinco fallos seguidos es perfectamente posible.
- `calidad = 4` deja el factor de facilidad intacto y `calidad = 1` lo baja. En el portal la
  calificación la pones tú: mentir en ese botón no cambia el algoritmo, solo te programa peor.
- El intervalo se calcula con el `ef` viejo y la facilidad se actualiza después, igual que en el
  portal. Cambiar ese orden mueve los números de la lista.
- `[True, False] * 4` no es una tarjeta «regular»: es una tarjeta que nunca encadena dos aciertos, y
  por eso se queda clavada en 1 día. Un solo fallo cada seis aciertos ya deja intervalos de cientos
  de días; es el patrón de una tarjeta mal escrita, no de una memoria mala.
:::

:::truco
Escribe la respuesta antes que la pregunta. Si al intentar redactar la respuesta te sale un párrafo
con un «y», ya sabes dónde cortar, y la pregunta se escribe sola. Y para las definiciones, la
variante de hueco («`________` devuelve el número de filas de un DataFrame») es más rápida de
escribir y más difícil de reconocer que la pregunta directa: entrena producción, no lectura.
:::

## Errores típicos

- **Meter varias ideas en una tarjeta.** La fórmula de la probabilidad de acertarla lo castiga en cada
  repaso, y el fallo deja de ser informativo. Si la respuesta lleva una enumeración, es una tarjeta
  por elemento.
- **Escribir la tarjeta sin contexto.** «¿Cuál es la diferencia?» no se puede contestar tres meses
  después, y en el repaso no tienes la página delante. El contexto va en el enunciado, aunque
  parezca redundante el día que la escribes.
- **Preguntas que se contestan reconociendo.** Opción múltiple donde la correcta es la más larga, o
  un enunciado que ya contiene medio término. Si no hay que producir la respuesta, no se está
  entrenando nada.
- **Respuestas que no se pueden calificar.** «Depende del caso» o «hay que tener cuidado» no son
  respuestas: son la señal de que el concepto no está cerrado. Vuelve a la ficha antes de escribir
  la tarjeta.
- **Copiar un mazo descargado.** Las tarjetas de otro llevan su contexto, su vocabulario y su orden;
  muchas se contestan por la posición. Sirven como índice de temas, no como material de repaso.
- **Marcar como acertado algo que te ha salido a medias.** Se siente bien y rompe el sistema: el
  intervalo se dispara y la tarjeta tarda meses en volver, justo cuando ya la has olvidado. El
  criterio es si la habrías producido sin ayuda, no si te suena.
- **Insistir en una tarjeta que fallas siempre.** Pasada la octava vez, seguir repasándola es el
  error. El problema está en la tarjeta o en el concepto: pártela, cámbiale el ejemplo o vuelve a la
  ficha del concepto con [[como-estudiar|el método]] delante.

## Comprueba que lo sabes

:::quiz
p: ¿Por qué una tarjeta con cuatro ideas se falla mucho más que cuatro tarjetas con una idea cada una?
o: Porque el cerebro tiene un límite de información por tarjeta que se satura
o: Porque hay que acertar las cuatro a la vez: con un 90 % por idea, la tarjeta larga se acierta el 66 % de las veces y la corta el 90 %
o: Porque las tarjetas largas tardan más en leerse y se repasan con menos frecuencia
a: 2
e: La probabilidad de acertar la tarjeta entera es el producto de las cuatro probabilidades, y 0,9 elevado a 4 es 0,66. No hay ningún límite misterioso de información: es multiplicación. Y el fallo de la tarjeta larga no te dice cuál de las cuatro ideas falló.
:::

:::quiz
p: ¿Qué convierte una pregunta en una tarjeta de repaso utilizable?
o: Que sea corta y esté bien redactada, con un lenguaje cuidado
o: Que tenga una sola idea, el contexto dentro del enunciado y una respuesta que se pueda calificar sin dudar
o: Que incluya la página de la ficha donde se explica, para poder consultarla
a: 2
e: La brevedad ayuda, pero lo que hace utilizable una tarjeta es que sea cerrada, autosuficiente y atómica. Incluir la referencia está bien como enlace, pero la tarjeta tiene que poder contestarse sin ir a buscar nada.
:::

:::quiz
p: Una tarjeta se te ha fallado ocho veces seguidas. ¿Qué toca?
o: Repasarla más a menudo hasta que entre, porque la constancia es lo que funciona
o: Borrarla del mazo: si se falla tanto, no interesa
o: Reescribirla: partirla en dos, cambiar el ejemplo o volver al concepto que la originó
a: 3
e: Ocho fallos no son un problema de memoria, son un aviso de que la tarjeta está mal escrita o de que el concepto no está entendido. Borrarla esconde el hueco y repetirla tal cual gasta repasos: lo que se hace es reescribirla o volver a la ficha.
:::

:::practica
enunciado: Convierte este desastre en tarjetas útiles, decidiendo cuántas hacen falta y justificando cada corte: «P: Explícame todo lo que hay que saber sobre los nulos en Pandas. R: Depende, hay que estudiar cómo se representan, cómo se detectan y qué se hace con ellos.»
pista: Busca respuestas cerradas, cada una con una sola idea y con el contexto dentro. La respuesta «depende» es la señal de que hay que dividir.
solucion: Salen cuatro tarjetas cerradas. 1) «¿Con qué valor representa Pandas un nulo numérico?» (con `np.nan`, que es un float). 2) «¿Qué devuelve `df.isna().sum()`?» (el número de nulos por columna). 3) «¿Qué hace `dropna(subset=['importe'])`?» (quita las filas con nulo solo en esa columna). 4) «¿Qué pasa al sumar una columna con `np.nan`?» (la suma lo ignora, pero un `mean` también: el resultado no cuenta esas filas). Cada una tiene una única respuesta comprobable y su contexto dentro. La pregunta original no se puede contestar ni calificar, y su respuesta «depende» lo demuestra.
:::

:::nota
Las tarjetas no sustituyen a las fichas: son su índice de acceso rápido. Un concepto que solo
conoces por sus cuatro tarjetas se te cae en cuanto cambia el ejemplo, y por eso cada tarjeta
debería poder rastrearse hasta la ficha de la que salió.
:::
