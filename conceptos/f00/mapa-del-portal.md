---
id: mapa-del-portal
titulo: Cómo usar este portal
fase: 0
nivel: básico
rutas: [core]
prerequisitos: [como-estudiar]
tags: [estudio, metodo, portal, repaso]
resumen: Rutas, fases, prerequisitos, preguntas de repaso y exportación a Anki: cómo moverte por el temario sin perderte ni repetir lo que ya sabes.
fuentes: []
---

## En una frase

El portal es un temario de más de 360 conceptos repartidos en 13 fases y 5 rutas: tú marcas lo que
vas viendo, el portal programa el repaso con esas preguntas y te dice qué te toca hoy. Cuatro
gestos —elegir ruta, leer, marcar visto, repasar— y ya sabes usarlo entero.

## La idea

No es una biblioteca, es un plan de entrenamiento. En una biblioteca el orden lo pones tú y nadie
te avisa de que te falta una base; aquí el orden está decidido y cada fase se apoya en la
anterior. La diferencia práctica es enorme: cuando algo no te cuadra, no te quedas atascado
releyendo, miras la lista de **prerequisitos** y vuelves exactamente al concepto que te falta.

La **ruta** responde a la otra pregunta: «¿qué necesito para el trabajo que quiero?». Si vas a
data engineering, [[ruta:de|la ruta de data engineering]] te ordena el mismo temario con otro
filtro. Las rutas no son compartimentos estancos: un mismo concepto puede estar en tres.

Y el **repaso** es lo que convierte esto en un plan y no en una lista de lecturas. Cada pregunta
de cada concepto es una tarjeta con fecha de vencimiento, como manda
[[como-estudiar|el repaso espaciado]]. Cuando marcas un concepto como visto, sus preguntas entran
en la cola; cuando las contestas, el portal decide cuándo te las vuelve a preguntar. Tú solo tienes
que abrir el repaso del día y hacer lo que toca.

Un orden que funciona:

1. Elige una ruta y avanza por fases en orden. No empieces por la fase que más te apetece.
2. En cada concepto, lee «En una frase» y «La idea», haz el **Ejemplo** a mano y después el código.
3. Contesta las preguntas antes de mirar la explicación. Cada fallo te dice dónde volver.
4. Marca **visto** al terminar. Marca **dominado** solo cuando puedas explicarlo en voz alta.
5. Al día siguiente, haz el repaso. Son 10-15 minutos, no más.
6. De vez en cuando descarga tu progreso: vive en este navegador y se pierde si limpias los datos.

## Definición formal

Las piezas del portal, definidas:

- **fase** — una de las 13 agrupaciones (`f00` a `f12`), en orden de dificultad creciente. Los
  conceptos de una fase se apoyan en los de las fases anteriores.
- **ruta** — filtro por objetivo: `core` (lo necesitan todas), `de` (data engineering), `ds` (data
  science), `quant` (finanzas cuantitativas) y `alg` (algoritmos y software).
- **nivel** — `básico`, `intermedio`, `avanzado` o `experto`. Dice qué hay que traer puesto, no
  cuánto cuesta leerlo.
- **prerequisito** — concepto que conviene haber leído antes. Aparece en la cabecera como «Antes
  de este», y no es una sugerencia decorativa: son los atajos cuando algo no te cuadra.
- **página de concepto** — siempre las mismas siete secciones, en el mismo orden: En una frase,
  La idea, Definición formal, Ejemplo, Código, Errores típicos y Comprueba que lo sabes.
- **bloque `verificable`** — código que el generador ejecuta cada vez que se construye el sitio;
  si el resultado deja de salir, el sitio no se construye. Los `ilustrativo` necesitan datos,
  claves o máquinas que aquí no hay, y no se ejecutan.
- **tarjeta de repaso** — cada pregunta de cada concepto, con su propia fecha de vencimiento.
- **SM-2 simplificado** — el programador de repasos: el primer acierto vence al día siguiente, el
  segundo a los 6 días, y a partir de ahí el intervalo se multiplica por el factor de facilidad
  (empieza en 2,5 y nunca baja de 1,3). Un fallo devuelve la tarjeta a 1 día.

Las direcciones del portal:

```text
#/                        portada, progreso y repaso de hoy
#/fase/f03                los conceptos de la fase 3, en orden
#/ruta/quant              todo lo de la ruta quant, ordenado por fases
#/c/ratio-de-sharpe       la página de un concepto
#/glosario                los conceptos por orden alfabético
#/repaso                  la sesión de repaso de hoy
#/progreso                progreso, exportación a Anki, guardar y cargar
```

## Ejemplo

Un día normal, con tiempos reales:

| Bloque | Qué haces | Minutos |
| --- | --- | --- |
| Repaso | 20 preguntas de la cola, ~30 segundos cada una | 10 |
| Concepto nuevo | «En una frase» y «La idea» | 15 |
| Concepto nuevo | el Ejemplo a mano, con papel | 10 |
| Concepto nuevo | leer el código y ejecutarlo cambiando un número | 10 |
| Concepto nuevo | las preguntas de la página | 5 |

Total: 50 minutos por concepto nuevo. A cinco días por semana salen unos 21 conceptos al mes, así
que el temario completo es un plan de año y medio a ese ritmo; para bajarlo de un año hay que
subir a ocho conceptos por semana.

La aritmética del repaso también cuadra: con dos o tres preguntas por concepto, tras un mes la
cola ronda las 50 tarjetas, repartidas en intervalos de días. Cada día vencen entre 5 y 10, así
que el límite de 20 preguntas diarias no se queda corto ni convierte el repaso en un segundo
trabajo.

## Código

```python verificable
# El portal programa el repaso con un SM-2 simplificado. Esto lo reproduce tal cual:
# acierto -> 1 dia, 6 dias y luego intervalo x facilidad; fallo -> vuelve a 1 dia y
# penaliza la facilidad, que nunca baja de 1,3.
def redondear(v):            # redondeo a la mitad hacia arriba, como Math.round en JS
    return int(v + 0.5)

def programar(secuencia, ef=2.5):
    reps, intervalo, salida = 0, 0, []
    for acierto in secuencia:
        calidad = 4 if acierto else 1
        if calidad < 3:
            reps, intervalo = 0, 1                  # fallo: la tarjeta vuelve a 1 dia
        else:
            reps += 1
            intervalo = 1 if reps == 1 else 6 if reps == 2 else redondear(intervalo * ef)
        # La facilidad se actualiza despues de calcular el intervalo, igual que en el portal.
        ef = max(1.3, ef + (0.1 - (5 - calidad) * (0.08 + (5 - calidad) * 0.02)))
        salida.append(intervalo)
    return salida

cinco_aciertos = [True, True, True, True, True]
con_fallo = [True, True, True, False, True, True]

print("cinco aciertos:", programar(cinco_aciertos))   # -> [1, 6, 15, 38, 95]
print("con un fallo  :", programar(con_fallo))        # -> [1, 6, 15, 1, 1, 6]
print("dias cubiertos:", sum(programar(cinco_aciertos)), "con solo 5 repasos")
```

## Errores típicos

- **Confundir «visto» con «dominado».** Visto significa que lo has leído; dominado, que puedes
  responder sin mirar. Si marcas todo como dominado, la barra de progreso te miente y el repaso
  se llena de tarjetas que no toca.
- **Mirar la respuesta de las preguntas y pasar a la siguiente.** La explicación es lo mejor de la
  página, pero solo enseña después de haber intentado responder. Si no lo sabes, contesta lo que
  creas, lee el porqué y deja que el repaso te lo vuelva a preguntar mañana.
- **Limpiar los datos del navegador sin descargar el progreso.** El avance y el historial de
  repaso viven en el almacenamiento local del navegador. Entra en «Mi progreso» y descarga el
  fichero JSON de vez en cuando; cargarlo después lo restaura.
- **Saltarse los prerequisitos.** Cuando un concepto no te cuadra, casi siempre falta uno
  anterior. La cabecera de la página te dice cuáles son: ve, léelo y vuelve.
- **Duplicar el repaso en dos sitios.** Si exportas a Anki, decide cuál de los dos es tu fuente de
  verdad. Repasar las mismas tarjetas en el portal y en el móvil sin coordinarlas es tiempo
  perdido y fechas desincronizadas.
- **Empezar por la fase que suena más interesante.** [[fase:7|Deep learning]] o LLMs sin los
  fundamentos cuestan mucho más esfuerzo y se olvidan antes. El orden de las fases no es decorativo.

## Comprueba que lo sabes

:::quiz
p: ¿Qué hace exactamente el botón «Marcar como visto»?
o: Marca el concepto como dominado y lo saca del repaso
o: Registra que lo has leído y mete sus preguntas en la cola de repaso
o: Descarga el concepto en PDF para imprimirlo
a: 2
e: Visto solo registra la lectura, y sus preguntas pasan a la cola con su primera fecha. Dominado es un paso aparte y más exigente: significa que puedes responder sin mirar. Nada de esto imprime ni descarga nada.
:::

:::quiz
p: Con el programador de repaso del portal, ¿en qué orden se alargan los intervalos de una tarjeta que siempre se acierta?
o: 1 día, 3 días, 9 días, multiplicando siempre por 3
o: 1 día, 6 días, y a partir de ahí el intervalo anterior multiplicado por el factor de facilidad
o: Siempre 7 días, porque el repaso es semanal
a: 2
e: El primer acierto vence en 1 día y el segundo en 6; después el intervalo crece multiplicándose por el factor de facilidad, que empieza en 2,5 y nunca baja de 1,3. Los intervalos crecientes son la esencia del repaso espaciado.
:::

:::quiz
p: ¿Qué significa la etiqueta «verificado» en un bloque de código?
o: Que el código se ejecuta al construir el sitio y su resultado se comprueba en cada generación
o: Que el código ha sido revisado por un experto externo
o: Que el código es más rápido que la alternativa escrita en prosa
a: 1
e: «Verificable» significa que el generador lo ejecuta solo, sin red ni ficheros externos, y que si deja de funcionar el sitio no se construye. No es una revisión humana ni una medida de rendimiento; los bloques que necesitan datos o claves van marcados como ilustrativos.
:::

:::truco
Atajos de teclado: `/` abre el buscador, `j` y `k` van al concepto siguiente y al anterior, `v`
marca visto y `d` marca dominado. Con el buscador puedes teclear una etiqueta como `fuga` o una
palabra del resumen, no solo el título.
:::
