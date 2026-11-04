---
id: presentaciones
titulo: Presentar a audiencias distintas
fase: 12
nivel: intermedio
rutas: [core]
prerequisitos: [storytelling-con-datos]
tags: [comunicacion, presentaciones, audiencia, decision]
resumen: La misma conclusión contada a negocio y a técnicos: qué se enseña, qué se guarda para el anexo y cuánto material cabe en el tiempo que te han dado.
fuentes: ["Duarte (2008), 'slide:ology'", "Anderson (2016), 'TED Talks: The Official TED Guide to Public Speaking'"]
---

## En una frase

Presentar es adaptar el mismo resultado a lo que cada audiencia puede decidir, enseñando solo
lo que sostiene la decisión y guardando el detalle para el anexo y para las preguntas.

## La idea

Imagina que presencias un accidente de tráfico y lo cuentas tres veces: al médico que va a
atender a los heridos, al policía que va a levantar el atestado y a un amigo que te pregunta qué
ha pasado. Es el mismo hecho, pero el médico necesita saber qué lesiones hay, el policía por
dónde venían los coches y el amigo quiere saber si alguien está bien. Si cuentas lo mismo a los
tres, a dos de ellos no les sirves. Con los datos pasa exactamente igual, y el error clásico es
contar la versión del policía (el método, el proceso, los detalles de la investigación) a quien
solo puede decidir sobre el presupuesto.

Hay tres audiencias y cada una tiene su pregunta:

- **Quien decide** (dirección, producto, cliente). Pregunta: *¿qué gano o pierdo, cuánto cuesta
  y qué me estás pidiendo?* Le importan la cifra, el riesgo y la decisión. El método le sobra.
- **Quien revisa** (pares técnicos, arquitectura, seguridad). Pregunta: *¿está bien hecho?*
  Quiere supuestos, validación, límites y alternativas descartadas.
- **Quien ejecuta** (el equipo que seguirá con esto). Pregunta: *¿cómo lo repito o lo
  continúo?* Necesita los detalles operativos, los ficheros y los pasos.

La consecuencia práctica es que **una presentación no es un informe leído en voz alta**: es una
selección. El informe contiene todo porque se lee a trozos y se consulta; la presentación
contiene lo mínimo porque se escucha una vez y en orden. Todo lo que quites del cuerpo va al
anexo, no a la basura: el anexo es lo que te salva en la ronda de preguntas.

Tres reglas que arreglan la mayoría de las presentaciones malas:

1. **El titular primero.** Cada diapositiva lleva una frase con sujeto, verbo y cifra, no un
   título de tema. «Evolución de la conversión» es un tema; «la conversión cae 0,4 puntos desde
   marzo» es un titular que se puede discutir.
2. **Una idea por diapositiva.** Si necesitas dos gráficos y un párrafo para explicar una
   diapositiva, son dos diapositivas. Y si no puedes resumir la idea en una frase, todavía no
   la tienes clara tú.
3. **Ensayo cronometrado.** Los minutos de una charla se consumen mucho más rápido de lo que
   parece: en voz alta, con las pausas y las preguntas intermedias, una diapositiva se lleva
   fácilmente minuto y medio.

Y una regla de honestidad que se aplica igual a las tres audiencias: **no escondas la
incertidumbre para simplificar**. Si la cifra tiene un margen grande, se dice con la misma
claridad que la cifra; si la decisión depende de un supuesto, el supuesto se nombra. Simplificar
es quitar detalle, no quitar límites ([[visualizacion-honesta]]).

## Definición formal

El presupuesto de una presentación se calcula antes de escribirla:

:::formula
minutos_contenido = minutos_totales − minutos_de_preguntas
diapositivas ≈ minutos_contenido / 1,5
:::

- `minutos_totales` — el tiempo que te han asignado, no el que te gustaría.
- `minutos_de_preguntas` — la reserva para la ronda final; con una audiencia de más de diez
  personas, entre un 20 % y un 30 % del total.
- `1,5` — minutos por diapositiva como orden de magnitud, contando la explicación, la pausa y
  la transición. Una diapositiva con un gráfico que hay que interpretar se lleva más.

Y el contenido de cada diapositiva se escribe como un titular contrastable:

:::formula
titular = sujeto + verbo + cifra (+ consecuencia)
:::

Si el titular no tiene cifra, no es un resultado: es una impresión. Si no tiene consecuencia, no
ayuda a decidir. «El modelo mejora» falla las dos cosas; «rechazamos 75 clientes buenos más y
evitamos 25 impagos: el coste esperado baja un 45 %» las cumple.

Para hablar se calcula a partir de unas 140 palabras por minuto:

:::formula
palabras_por_diapositiva = minutos_contenido · 140 / diapositivas
:::

## Ejemplo

Tienes 15 minutos en un comité con audiencia mixta y reservas 3 para preguntas, así que dispones
de 12 minutos de contenido. Con la regla de 1,5 minutos por diapositiva, el presupuesto es de 8
diapositivas; si preparas 20, te quedan 36 segundos por diapositiva y no te da tiempo ni a
nombrarlas.

| Diapositivas | Segundos por diapositiva | Palabras por diapositiva |
| --- | --- | --- |
| 20 | 36 | 84 |
| 12 | 60 | 140 |
| 8 | 90 | 210 |

La conclusión práctica: con 36 segundos por diapositiva solo cabe un titular y un gráfico; no
hay sitio para explicar un método. Con 8 a 12 diapositivas hay espacio para el titular, el
gráfico y dos frases de contexto. Para la misma reunión, estas son las dos versiones del mismo
resultado:

- **A negocio:** «bajando el umbral de decisión de 0,50 a 0,30 evitamos 25 impagos al año por
  cada 1.000 solicitudes y rechazamos 75 buenos clientes más. El coste esperado del crédito cae
  un 45 %. Necesito aprobar el cambio de umbral y una revisión en un mes.»
- **A técnicos:** «el modelo no cambia; cambia el punto de corte. Con los costes actuales
  (4.000 € por impago, 300 € de margen), el umbral óptimo baja a 0,30. El resultado es sensible
  al margen: si el rechazo quema al cliente a largo plazo, el óptimo sube. Anexo con la curva de
  coste por umbral y las matrices de confusión.»

Son el mismo trabajo. La primera no menciona el modelo ni la métrica porque a esa audiencia no
le cambian la decisión; la segunda no explica qué es un umbral porque se da por sabido.

## Código

```python verificable
# Cuanto material cabe: una persona lee unas 140 palabras por minuto de discurso.
# Lo que no cabe en el guion no se cuenta, y lo que no se cuenta sobra en la diapositiva.
palabras_por_minuto = 140
minutos_contenido = 12          # 15 asignados menos 3 reservados para preguntas

for diapositivas in (20, 12, 8):
    segundos = minutos_contenido * 60 / diapositivas
    palabras = minutos_contenido * palabras_por_minuto / diapositivas
    print(f"{diapositivas:>2} diapositivas en {minutos_contenido} min -> "
          f"{segundos:.0f} s y {palabras:.0f} palabras por diapositiva")
# -> 20 diapositivas en 12 min -> 36 s y 84 palabras por diapositiva
# -> 12 diapositivas en 12 min -> 60 s y 140 palabras por diapositiva
# ->  8 diapositivas en 12 min -> 90 s y 210 palabras por diapositiva
```

```text
# Version para negocio (1 diapositiva)

Titular: Bajar el umbral de 0,50 a 0,30 ahorra 77.500 EUR por cada 1.000 solicitudes.

Grafico: dos barras con el coste esperado (173.500 EUR y 96.000 EUR).
Debajo, en una linea: "-25 impagos, +75 buenos clientes rechazados".

Que pido: aprobar el cambio de umbral y revisar en un mes.
Que puede salir mal: si el margen por buen cliente es menor de 300 EUR, el ahorro se
reduce; esta en el anexo.

---

# Version para tecnicos (1 diapositiva)

Titular: el umbral optimo cambia de 0,50 a 0,30 al pasar de accuracy a coste esperado.

Grafico: coste total por umbral, con la curva completa y la linea del minimo.

Debajo: supuestos (coste de impago 4.000 EUR, margen 300 EUR), n = 1.000 y periodo
de validacion. Anexo: matriz de confusion por umbral, curva ROC y prueba de
calibracion.
```

## Errores típicos

- **Leer las diapositivas.** Si la diapositiva lleva el texto que estás diciendo, sobra uno de
  los dos. La diapositiva sostiene el titular con un gráfico; la explicación la pones tú.
- **Empezar por el método.** «Primero cargué los datos, luego limpié los nulos…» gasta los
  primeros dos minutos, que son los únicos en los que tienes la atención completa de la sala.
  El método va después de la conclusión, o en el anexo.
- **Contar todo lo que hiciste.** Una diapositiva por cada paso del análisis es un diario, no
  una presentación. El trabajo que no cambia ninguna decisión se queda fuera del cuerpo.
- **Reutilizar los gráficos del análisis tal cual.** Los gráficos exploratorios tienen cinco
  series, ejes sin unidades y nombres de columna. En una sala no se leen. Cada gráfico que se
  presenta se rediseña para una sola idea ([[visualizacion-honesta]]).
- **Ocultar los límites para no complicar.** Suavizar la incertidumbre para que la decisión sea
  más fácil es la forma más rápida de perder la credibilidad: la primera pregunta técnica la
  destapa y a partir de ahí se duda de todo ([[etica-profesional]]).
- **No preparar el anexo.** Las preguntas difíciles llegan siempre, y la respuesta «no lo sé»
  cuando el dato estaba en tu análisis es el peor desperdicio posible. Prepara tres o cuatro
  diapositivas de reserva con lo que sabes que te van a preguntar.

:::truco
Escribe el titular de cada diapositiva antes de crear la diapositiva, en una lista. Si los
titulares, leídos seguidos, cuentan la historia completa y llevan a la decisión, la
presentación funciona; si al leerlos seguidos no se entiende nada, ningún diseño lo arregla.
:::

:::practica
enunciado: Te dan 10 minutos en una reunión con dirección y con el equipo técnico, y llevas 18 diapositivas. ¿Cómo lo reorganizas sin perder información?
pista: Calcula cuánto tiempo tienes por diapositiva con las dos audiencias sentadas en la misma sala, y decide qué es cuerpo y qué es anexo.
solucion: Con 10 minutos y 18 diapositivas salen 33 segundos por diapositiva: imposible. Reserva 2 minutos para preguntas, quédate con 6 u 8 diapositivas de cuerpo (titular, cifra, decisión que pides y riesgo) y manda el detalle al anexo, que estará disponible para la ronda de preguntas y para quien lo pida después. Si hay que elegir, el cuerpo se escribe para quien decide y el anexo para quien revisa; las diapositivas técnicas no se tiran, se mueven.
:::

## Comprueba que lo sabes

:::quiz
p: Tienes 15 minutos asignados, reservas 3 para preguntas y llevas 20 diapositivas. ¿Cuál es el problema principal?
o: Que 20 diapositivas son demasiadas para cualquier audiencia
o: Que quedan 36 segundos por diapositiva, tiempo para un titular y un gráfico, no para explicar el método
o: Que hay que hablar más rápido para que quepan todas
a: 2
e: El problema es de presupuesto, no de número: con 12 minutos de contenido y 1,5 minutos por diapositiva caben 8. Hablar más rápido hace que la sala deje de seguirte. La primera opción acierta el síntoma pero no la causa: 20 diapositivas serían correctas en una sesión con 30 minutos de contenido.
:::

:::quiz
p: ¿Qué diferencia hay entre lo que se enseña a negocio y lo que se enseña a un equipo técnico?
o: A negocio se le enseña una versión simplificada de los mismos datos y a los técnicos la verdad
o: Cambia la selección: a negocio le importan la cifra, el riesgo y la decisión; a los técnicos, los supuestos, la validación y los límites
o: A negocio se le enseña el resumen y a los técnicos el informe entero, leído en voz alta
a: 2
e: Adaptar la audiencia es seleccionar y jerarquizar el mismo material, no rebajar la verdad. Las dos versiones son ciertas y verificables; lo que cambia es qué se pone delante porque es lo que esa audiencia puede usar para decidir.
:::

:::quiz
p: ¿Para qué sirve el anexo de una presentación?
o: Para demostrar que has trabajado mucho
o: Para tener preparado el detalle que sostiene las respuestas a las preguntas difíciles
o: Para que la presentación parezca más técnica
a: 2
e: El anexo es la red de seguridad de la ronda de preguntas: guarda el detalle que no cabe en el cuerpo pero que alguien va a pedir. Enseñarlo entero en la presentación destruye el presupuesto de tiempo; no tenerlo convierte cada pregunta en un «no lo sé».
:::
