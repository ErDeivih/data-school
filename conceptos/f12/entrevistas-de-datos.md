---
id: entrevistas-de-datos
titulo: Entrevistas técnicas de datos
fase: 12
nivel: intermedio
rutas: [core, ds, de]
prerequisitos: [hacer-preguntas-buenas, sql-ventanas, intervalos-de-confianza]
tags: [entrevistas, sql, carrera, estadistica]
resumen: Qué se mide de verdad en una entrevista de datos: acotar un problema ambiguo, escribir SQL sin duplicar filas y defender cada cifra con su base y su incertidumbre.
fuentes: ["McDowell (2015), 'Cracking the Coding Interview', 6.ª ed.", "Minto (2008), 'The Pyramid Principle'"]
---

## En una frase

Una entrevista de datos no mide si recuerdas la sintaxis: mide si, ante un problema mal definido,
sabes acotarlo, sacar una cifra defendible y decir en voz alta qué te falta por comprobar.

## La idea

Una entrevista técnica se parece menos a un examen y más a una revisión de código en voz alta.
Quien te entrevista no puede ver tu portátil ni tus tres años de experiencia: solo tiene 45 minutos
de tu razonamiento. Todo lo que no digas, no cuenta. Un candidato que acierta en silencio puntúa
menos que uno que se equivoca, se da cuenta y lo corrige delante de todos.

Casi todas las empresas usan las mismas cinco piezas, a veces en una sola sesión y a veces
repartidas en una semana:

1. **Criba de código.** SQL o pandas sobre un caso pequeño. Se busca que sepas unir, agrupar y
   ordenar sin mirar la documentación y, sobre todo, que entiendas el grano de la tabla: qué
   representa exactamente una fila.
2. **Estadística y probabilidad.** Una pregunta de razonamiento: intervalos, p-valor, tamaño de
   muestra, probabilidad condicional. Rara vez te piden demostrar un teorema.
3. **Caso de negocio.** Te dan una métrica que se ha movido y media hoja en blanco. Aquí se decide
   la mayoría de las contrataciones.
4. **Diseño.** Un esquema de datos, un pipeline o un experimento. Se evalúa si tus decisiones
   aguantan un volumen y un fallo.
5. **Conversación de equipo.** Proyectos, conflictos, qué harías distinto. Es la ronda donde más
   gente competente se cae, convencida de que «eso ya se les dará».

Lo que se puntúa en las cinco es el proceso, no la respuesta: preguntar antes de resolver, empezar
por el caso simple, estimar a mano el orden de magnitud, comprobar el resultado y reconocer lo que
no sabes. Que el enunciado sea ambiguo no es un fallo del ejercicio, es el ejercicio. Si empiezas
por «necesito saber si el denominador son sesiones o usuarios», ya has subido un escalón.

:::truco
Prepara un guion de tres pasos y practícalo **en voz alta**, no leyéndolo: (1) reformula el
problema con tus supuestos y pide confirmación, (2) resuélvelo con números pequeños a mano,
(3) comprueba el resultado y di qué falta. Sirve igual para el caso de negocio, para el SQL y para
la pregunta de estadística. La mecánica de formular bien está en [[hacer-preguntas-buenas]].
:::

## Definición formal

Dos piezas se pueden escribir con precisión, y las dos sirven para preparar la entrevista.

Primera: el proceso completo es un producto de filtros. Si cada una de las `k` rondas se pasa con
probabilidad `p` y las rondas son aproximadamente independientes, la probabilidad de recibir la
oferta es:

:::formula
P(oferta) = p₁ · p₂ · … · p_k
:::

`p_i` es la probabilidad de pasar la ronda `i` (un número entre 0 y 1) y `k` es el número de rondas.
Con `k = 5` y `p = 0,6` en todas, `P = 0,078`. La consecuencia práctica: el cuello de botella es tu
peor ronda. Subir de 0,6 a 0,7 en una sola ronda multiplica el total por `0,7 / 0,6 = 1,17`;
hacerlo en las cinco lo multiplica por `(0,7 / 0,6)⁵ = 2,2`. Ahí rinde el esfuerzo, no en pulir lo
que ya dominas.

Segunda: una cifra sin base no es una respuesta. Para una proporción `m = x / n`:

:::formula
error típico ≈ √(m · (1 − m) / n)
:::

`x` es el número de casos que cumplen la condición, `n` el total de observaciones y `m` la
proporción estimada. Si te preguntan si algo ha cambiado, la respuesta defendible compara la
diferencia observada con dos errores típicos ([[intervalos-de-confianza]]).

## Ejemplo

Caso típico de entrevista: «los pedidos cayeron un 4 % la semana pasada, ¿qué miras?». Media hoja
en blanco y diez minutos.

Primero, ¿es real? La semana tiene 7 días en los dos periodos, así que la comparación es justa.
Después, separa los dos efectos que siempre hay detrás de una caída de pedidos: menos tráfico o
menos conversión.

- Sesiones: 210.000 → 208.000 (−1,0 %).
- Pedidos: 12.400 → 11.900 (−500, −4,0 %).
- Conversión: 12.400 / 210.000 = 5,90 % → 11.900 / 208.000 = 5,72 %.
- Si el tráfico hubiera caído y la conversión no: 208.000 · 0,059048 = 12.282 pedidos.
- Efecto tráfico: 12.282 − 12.400 = −118 pedidos. Efecto conversión: 11.900 − 12.282 = −382.

Los dos efectos suman los 500 pedidos perdidos, y el 76 % viene de la conversión. Esa es la
respuesta: «la caída es de conversión, no de tráfico; pido el desglose por dispositivo y la tasa de
error de la pasarela de pago». Fíjate en lo que has hecho: separar dos efectos con aritmética de
colegio antes de tocar un `GROUP BY`.

## Código

```python verificable
# Reconciliacion de una caida de pedidos en dos efectos: trafico y conversion.
ses_antes, ped_antes = 210_000, 12_400
ses_ahora, ped_ahora = 208_000, 11_900

conv_antes, conv_ahora = ped_antes / ses_antes, ped_ahora / ses_ahora
# Pedidos que habria habido si solo hubiera cambiado el trafico.
ped_solo_trafico = ses_ahora * conv_antes

print(f"conversion {conv_antes:.2%} -> {conv_ahora:.2%}")
print(f"pedidos {ped_antes} -> {ped_ahora} ({ped_ahora - ped_antes:+d})")
print(f"efecto trafico {ped_solo_trafico - ped_antes:+.0f}  efecto conversion {ped_ahora - ped_solo_trafico:+.0f}")
```

```text
conversion 5.90% -> 5.72%
pedidos 12400 -> 11900 (-500)
efecto trafico -118  efecto conversion -382
```

Y el SQL que cae en casi todas las cribas: el segundo pedido de cada usuario. La trampa es
resolverlo con un `ORDER BY` global y un `LIMIT 2`, que devuelve dos filas en total en lugar de una
por usuario ([[sql-ventanas]]).

```sql verificable
CREATE TABLE pedidos (usuario VARCHAR, fecha DATE);
INSERT INTO pedidos VALUES
  ('ana', '2026-01-03'), ('ana', '2026-01-19'), ('ana', '2026-02-02'),
  ('luis', '2026-01-07'), ('luis', '2026-01-28'), ('marta', '2026-02-11');

-- Numero las filas dentro de cada usuario: la 2 es su segundo pedido.
SELECT usuario, fecha AS segundo_pedido
FROM (SELECT usuario, fecha, ROW_NUMBER() OVER (PARTITION BY usuario ORDER BY fecha) AS n FROM pedidos)
WHERE n = 2
ORDER BY usuario;
```

```text
usuario | segundo_pedido
ana | 2026-01-19
luis | 2026-01-28
```

## Errores típicos

- **Resolver antes de acotar.** Escribes la unión perfecta para la pregunta equivocada. Si el
  enunciado dice «clientes activos» y no has definido activo (¿un pedido en 30 días?, ¿una
  sesión?), tu resultado no es comprobable. Repite el enunciado con tus supuestos antes de tocar el
  teclado.
- **Ignorar el grano y duplicar filas.** Un `LEFT JOIN` contra una tabla con varias filas por clave
  multiplica los pedidos y el total sale inflado. Cuenta las filas antes y después de unir
  ([[sql-joins]]); es la comprobación que más entrevistas salva.
- **Dar la cifra sin base ni incertidumbre.** «La conversión ha mejorado» no es una respuesta.
  «De 3,25 % a 3,50 % con 400 visitas por rama, dentro del margen de error» sí lo es.
- **Programar antes de estimar.** Un bucle de veinte líneas para contar algo que se estima en diez
  segundos a mano. Estima primero: si el resultado se aleja tres órdenes de magnitud de la
  estimación, el error está en el código, no en la estimación.
- **Sacar herramientas que no vienen al caso.** Proponer Spark o Kafka para dos millones de filas
  que caben en memoria ([[coste-y-optimizacion]]). Justifica volumen, latencia y coste antes de
  nombrar la herramienta.
- **Inventar experiencia.** Si no has usado Airflow, dilo y cuenta con qué lo has resuelto. La
  segunda pregunta desmonta al que exagera, y quien te pilla exagerando ya no te cree nada más.
- **No cerrar.** Termina con una conclusión y una petición concreta de información. Una respuesta
  que se queda a medias se recuerda como una respuesta a medias.

## Comprueba que lo sabes

:::quiz
p: Los pedidos caen un 4 % y las sesiones un 1 %. ¿Cuál es la primera comprobación que harías en voz alta?
o: Separar los dos efectos con la conversión del periodo anterior aplicada al tráfico nuevo, para ver cuánto explica cada uno
o: Revisar el código de la web en busca de un error de instrumentación
o: Comparar con el mismo periodo del año pasado antes que nada
o: Proponer una campaña para recuperar los pedidos perdidos
a: 1
e: Separar tráfico y conversión se hace con aritmética y da una cifra comprobable en un minuto; es la respuesta que se espera en un caso de negocio. Una hipótesis de instrumentación es una posibilidad, no una comprobación, y va después de cuantificar el efecto. La comparación interanual es útil pero no la primera, y proponer una campaña sin diagnóstico es saltarse el ejercicio.
:::

:::quiz
p: Un candidato pasa cada una de las 5 rondas con probabilidad 0,6 y las rondas son independientes. ¿Qué probabilidad tiene de recibir la oferta?
o: 0,6, porque cada ronda se evalúa por separado
o: 0,078, porque hay que pasar las cinco
o: 0,3, la media de las cinco rondas
o: 0,9, porque las probabilidades de las rondas se suman
a: 2
e: La oferta exige pasar todas, así que las probabilidades se multiplican: 0,6⁵ = 0,0778. Sumarlas daría 3, un valor imposible para una probabilidad; promediarlas daría la probabilidad de una ronda media, que no responde a la pregunta. Las rondas no son independientes en la práctica, pero el orden de magnitud se ve igual.
:::

:::quiz
p: Te piden el segundo pedido de cada usuario. ¿Qué devuelve ROW_NUMBER() OVER (PARTITION BY usuario ORDER BY fecha) antes de filtrar?
o: Una fila por usuario, ya con la fecha de su segundo pedido
o: Una fila por pedido, con un número que empieza en 1 dentro de cada usuario
o: Una fila por pedido, con un número que empieza en 1 y sigue en toda la tabla
o: Dos filas por usuario, una por cada pedido contado
a: 2
e: Una función de ventana no agrupa: devuelve todas las filas y añade una columna. PARTITION BY reinicia la numeración en cada usuario, así que hay que filtrar n = 2 en una subconsulta o en una CTE. Sin partición, la numeración sería global y no respondería a la pregunta, que es distinto de responderla mal.
:::

:::practica
enunciado: Treinta minutos, sin datos a mano. El ingreso medio por usuario (ARPU) de tu producto bajó un 3 % el mes pasado y negocio quiere saber por qué. Estructura la respuesta en voz alta como en una entrevista y llega a dos hipótesis comprobables, cada una con la consulta que la probaría.
pista: El ARPU es un cociente. Descompónlo en los factores que lo forman antes de escribir SQL.
solucion: ARPU = ingresos / usuarios = (pedidos / usuarios) · (ingresos / pedidos). Cada factor se consulta por separado: frecuencia de compra y ticket medio. Primera hipótesis: la frecuencia bajó en un segmento concreto; se prueba con pedidos por usuario y mes agrupados por segmento, ordenados por contribución a la caída total. Segunda: el ticket medio bajó por más descuento o por mezcla hacia producto barato; se prueba con ingreso medio por pedido y con el porcentaje de pedidos con descuento. Y antes de dar cualquier cifra, comprueba el calendario: el mes pasado tuvo 31 días y este 30, así que un 3 % de caída puede ser entero efecto de contar un día menos (1/31 = 3,2 %). Compara por día o normaliza por días.
:::
