---
id: paper-trading
titulo: Paper trading
fase: 9
nivel: básico
rutas: [quant]
prerequisitos: [que-es-un-mercado, slippage-y-comisiones]
tags: [ejecucion, practica, riesgo]
resumen: Operar con precios reales y órdenes que no existen: sirve para aprender la mecánica de la plataforma, no para saber si la estrategia gana dinero.
fuentes: ["Harris (2003), 'Trading and Exchanges: Market Microstructure for Practitioners'"]
---

## En una frase

El paper trading es operar en el mercado real con órdenes simuladas: ves precios de verdad,
mandas órdenes de verdad al simulador y este te apunta una ejecución ideal, así que te enseña
la mecánica de la plataforma pero **no** te dice si tu estrategia gana dinero.

## La idea

Casi todos los brókers ofrecen una cuenta de prueba: mismos gráficos, mismos precios, mismos
horarios, pero las órdenes no salen al mercado. Cuando das a comprar, el programa te apunta
la compra al precio que marca el libro en ese instante y actualiza tu saldo ficticio. Parece
una prueba gratuita de la estrategia y en realidad es una prueba del **proceso**: de ti
manejando la herramienta.

Sirve para cosas muy concretas y valiosas. Aprender dónde está cada tipo de orden y qué pasa
cuando cancelas una que ya se ha ejecutado. Medir cuánto tardas desde que ves la señal hasta
que la orden está puesta, que suele ser bastante más de lo que crees. Acostumbrarte a ver
números rojos en pantalla sin tomar decisiones raras. Y montar el hábito del registro: qué
operación, por qué, con qué tamaño y cómo salió. Todo eso lo puedes practicar sin arriesgar
un euro y sin él llegarías al mercado real a estrenarte con dinero.

Lo que no te dice es más importante. En paper trading tu orden **no existe**: no consume
liquidez, no ocupa posición en la cola del libro, no mueve el precio y nadie la ve. El
simulador te la llena siempre, al precio que le conviene para que la demo sea cómoda. En el
mercado real, si hay 3.000 acciones delante de ti en el mismo precio, tocar el precio no
significa que te hayan llenado, y si tu orden es grande en un valor pequeño, tu propia compra
empuja el precio hacia arriba. Tampoco hay rechazos por margen, ni ejecuciones parciales, ni
huecos de apertura, ni caídas de conexión justo cuando querías salir.

Hay un segundo motivo, más incómodo: en paper trading el resultado no te cuesta nada. Cuando
el dinero es real, mucha gente cierra las ganadoras antes de tiempo y aguanta las perdedoras
esperando a que vuelvan; con dinero ficticio esa tensión no aparece. Un paper trading
rentable demuestra que sabes usar el programa. No demuestra que vayas a ejecutar el sistema
igual cuando cada operación te cueste dinero.

Y un tercer motivo, estadístico: la muestra. Cien operaciones en paper son cien operaciones en
**un** régimen de mercado, tomadas casi siempre en un mercado que sube. Sin
[[backtesting-vectorizado|backtest]] previo con muchos más datos y sin costes modelados, lo
único que tienes es una anécdota.

El paper trading no sustituye al backtest: lo complementa
por el otro lado, porque en el backtest ves el futuro entero y en paper decides en tiempo real
con información parcial.

La forma de aprovecharlo es tratarlo como un examen con reglas fijadas de antemano: mismo
instrumento, mismo tamaño de posición y mismo horario que usarás en real, costes apuntados a
mano en cada operación, un mínimo de operaciones pactado antes de empezar y la obligación de
no cambiar las reglas a mitad de camino. Si haces eso, el paper trading te da una cosa que el
backtest no puede darte: la métrica de **tu** ejecución.

:::figura
fichero: paper-trading-el-coste-que-falta
pie: Arriba, el acierto mínimo que hace falta para ganar según lo que cueste cada ida y vuelta: con la línea rosa (coste cero, la del simulador) basta acertar un 45 %; con la azul, un 57 %. Abajo, lo que pasa al repetir el ejemplo 200 veces: la línea que te enseña la demo acaba en +840 EUR y la realista en −160. La conclusión no es que el simulador mienta, es que no cobra: el coste no cambia el porcentaje de aciertos, cambia el signo del resultado.
fuente: figuras/paper-trading-1.py
:::

## Definición formal

Lo que el paper trading sí puede estimar es la esperanza por operación, siempre que le sumes
a mano el coste que el simulador no te cobra:

:::formula
E[por operación] = p · G − (1 − p) · P − c
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `p` | Proporción de operaciones ganadoras | tanto por uno, entre 0 y 1 | La esperanza sube, y sube más de lo que parece porque cada acierto entra en `p` y sale de `(1 − p)` a la vez |
| `G` | Ganancia media de las ganadoras | % sobre el capital de la operación | Sube la esperanza en proporción a `p`: dejar correr las ganadoras vale más que acertar más veces |
| `P` | Pérdida media de las perdedoras, en positivo | % sobre el capital de la operación | Baja la esperanza en proporción a `(1 − p)`. Si escribes aquí la pérdida en negativo, el signo de toda la fórmula se invierte |
| `c` | Coste de ida y vuelta: comisiones, diferencial y deslizamiento | % por operación | Se resta **una vez en cada operación**, gane o pierda. Es el único término que el simulador deja en cero, y basta que supere `p · G − (1 − p) · P` para que la estrategia pierda |
| `E[por operación]` | Beneficio esperado de una operación | % del capital arriesgado | Por debajo de cero la estrategia no se arregla con más operaciones: se arruina más deprisa |
| `n` | Número de operaciones del periodo | operaciones | El capital crece de forma exponencial, no proporcional: con `E` negativa, el daño también se acelera |
| `Capital_inicial` | Capital que se pone a trabajar | EUR | Multiplica el resultado final sin cambiar su signo: doblar el capital no arregla una esperanza negativa, dobla la pérdida |
:::

- `p` — proporción de operaciones ganadoras (entre 0 y 1).
- `G` — ganancia media de las ganadoras, en porcentaje sobre el capital de la operación.
- `P` — pérdida media de las perdedoras, en porcentaje (se toma en positivo).
- `c` — coste de ida y vuelta en porcentaje: comisiones, [[order-book-y-spread|diferencial]] y
  [[slippage-y-comisiones|deslizamiento]] juntos.
- `E[por operación]` — beneficio esperado por operación, en porcentaje. La estrategia gana
  dinero solo si `p · G > (1 − p) · P + c`.

Y el resultado acumulado no es `n · E`, porque las operaciones se componen:

:::formula
Capital_final ≈ Capital_inicial · exp( n · E / 100 )
:::

donde `n` es el número de operaciones. Es una aproximación: supone que todas las operaciones
arriesgan lo mismo y que `E` es pequeño frente a 100.

## Ejemplo

Supón que tras 200 operaciones en paper tienes un 55 % de aciertos, con ganancia media del
1,2 % y pérdida media del 1,0 % sobre el capital arriesgado en cada operación.

- Esperanza bruta: `0,55 · 1,2 − 0,45 · 1,0 = 0,66 − 0,45 = +0,21 %` por operación.
- Esperanza con coste de ida y vuelta del 0,10 %: `0,21 − 0,10 = +0,11 %`.
- Esperanza con coste del 0,25 % (realista en un valor de mediana liquidez): `0,21 − 0,25 =
  −0,04 %`. **Negativa.**

Puesto en euros, con 2.000 € por operación:

| Coste de ida y vuelta | Esperanza por operación | En 200 operaciones |
| --- | --- | --- |
| 0,00 % (lo que te da el simulador) | +4,20 € | +840 € |
| 0,10 % | +2,20 € | +440 € |
| 0,25 % | −0,80 € | −160 € |

El simulador te habría enseñado la primera fila, con la que celebrarías el resultado. La fila
que te importa es la tercera. El paper trading no miente: simplemente no cobra.

## Código

```python verificable
# Lo que el simulador no cobra, y como cambia el signo de la esperanza
p, ganancia, perdida = 0.55, 1.2, 1.0     # 55 % de aciertos, +1,2 % y -1,0 % de media

for coste in (0.0, 0.10, 0.25, 0.40):
    esperanza = p * ganancia - (1 - p) * perdida - coste
    print(f"coste {coste:.2f} % -> esperanza {esperanza:+.2f} % por operacion")
# -> coste 0.00 % -> esperanza +0.21 % por operacion
# -> coste 0.10 % -> esperanza +0.11 % por operacion
# -> coste 0.25 % -> esperanza -0.04 % por operacion
# -> coste 0.40 % -> esperanza -0.19 % por operacion
```

:::claves
- `p, ganancia, perdida = 0.55, 1.2, 1.0` es un **desempaquetado**: los tres nombres se crean de golpe y en ese orden exacto. Cambiar el orden de los números no da error, solo una estrategia distinta, y es un fallo que no salta a la vista hasta que el resultado es absurdo.
- `ganancia` y `perdida` están en **porcentaje** (1,2 significa 1,2 %), no en tanto por uno. Si las escribieras como 0,012, la esperanza saldría cien veces menor y el coste de 0,10 la aplastaría siempre.
- `perdida` se guarda en **positivo** y se resta con el signo delante. Es una convención: si la guardaras como −1,0, la fórmula tendría que sumarla y el `print` mostraría un signo distinto al esperado.
- La fórmula `p * ganancia - (1 - p) * perdida - coste` se evalúa de izquierda a derecha, pero `*` va antes que `-`. Los paréntesis de `(1 - p)` no son decorativos: sin ellos, `p * ganancia - 1 - p * perdida` es otra cuenta completamente distinta.
- `for coste in (0.0, 0.10, 0.25, 0.40):` recorre cuatro escenarios y **no** modifica la estrategia: `p`, `ganancia` y `perdida` siguen igual dentro y fuera del bucle. Solo cambia lo que se paga por operar.
- La línea de comentario `# -> coste 0.25 % -> esperanza -0.04 %` está escrita a mano. Si cambias el valor de `p`, esos comentarios quedan mintiendo mientras el programa sigue diciendo que todo va bien: compara la salida real antes de darlos por buenos.
:::

```text
Diario de paper trading: los campos que hay que rellenar SIEMPRE
fecha | hora | instrumento | direccion | tamano | motivo de entrada
precio de entrada | precio de salida | comision | spread estimado | deslizamiento
resultado en % | resultado en EUR | regla que aplicaste | que sentiste al entrar
```

## Errores típicos

- **Creer que un paper trading rentable valida la estrategia.** El simulador te llena siempre
  y al precio que le conviene. Sin impacto, sin cola y sin fills parciales, el resultado está
  sesgado a favor. Valida el backtest, y usa el paper para validar tu ejecución.
- **No apuntar los costes.** Muchos simuladores no aplican comisión o la aplican sin
  diferencial. Si no los metes a mano, la esperanza que ves no es la que vas a tener: en el
  ejemplo, un coste del 0,25 % convierte 200 operaciones ganadoras en 160 € de pérdida.
- **Operar en paper valores ilíquidos y luego en real los mismos.** En un valor con 50.000 €
  de volumen diario, tu orden de 5.000 € mueve el precio. En paper esa orden no existe.
- **Cambiar las reglas a mitad del periodo de prueba.** Si al ver tres pérdidas seguidas
  añades un filtro, ya no estás probando el sistema que empezaste: estás haciendo
  [[seleccion-de-hiperparametros|búsqueda de hiperparámetros]] a mano sobre una muestra
  diminuta. Fija las reglas por escrito antes de la primera operación.
- **Confundir paper trading con backtest.** Son cosas distintas: en el backtest ves toda la
  serie y puedes mirar el futuro sin darte cuenta; en paper decides con información parcial,
  en tiempo real, y eso incluye dudar. Necesitas los dos, y por motivos distintos.
- **Probar solo en un mercado alcista.** Cien operaciones en seis meses de subida no dicen
  nada de tu estrategia en una corrección. Anota en qué régimen hiciste la prueba.

:::practica
enunciado: Tras 120 operaciones en paper: 48 % de aciertos, ganancia media 1,8 % y pérdida media 1,1 %. El simulador no te cobró nada; el coste real de ida y vuelta es 0,20 %. Calcula la esperanza por operación con y sin coste, y el resultado en euros con 1.500 EUR por operación.
pista: La esperanza bruta es la suma ponderada de ganadoras y perdedoras, y el coste se resta una vez por operación, en todas.
solucion: Esperanza bruta: 0,48 · 1,8 − 0,52 · 1,1 = 0,864 − 0,572 = +0,292 % por operación. Con el coste: 0,292 − 0,20 = +0,092 %, la tercera parte, así que el sistema solo aguanta con costes por debajo de 0,292 %. Con 1.500 EUR por operación, 0,092 % son 1,38 EUR y 120 operaciones dan 165,60 EUR; el simulador te habría enseñado 4,38 EUR.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es el principal problema del paper trading para evaluar una estrategia?
o: Que los precios que muestra no son los del mercado real
o: Que las órdenes simuladas no consumen liquidez ni ocupan cola, así que las ejecuciones son mejores que las reales
o: Que no permite operar en corto
a: 2
e: Los precios sí son reales: el problema está en las ejecuciones. Tu orden simulada no compite por liquidez, no espera en la cola y no mueve el precio, así que te llena en condiciones que en el mercado no se darían. El corto depende de la plataforma de demo, no del concepto.
:::

:::quiz
p: Una estrategia en paper da 55 % de aciertos, ganancia media 1,2 % y pérdida media 1,0 %. ¿Con qué coste de ida y vuelta deja de ser rentable?
o: Con cualquier coste superior a 0,21 %, porque la esperanza bruta es 0,21 %
o: Solo con costes superiores al 1,2 %, que es la ganancia media
o: Con ningún coste, porque la esperanza ya es negativa
a: 1
e: La esperanza bruta es 0,55 · 1,2 − 0,45 · 1,0 = +0,21 %, así que el coste se la come entera a partir de 0,21 %. Comparar el coste con la ganancia media es un error de referencia: el coste se paga en todas las operaciones, no solo en las ganadoras.
:::

:::quiz
p: ¿Para qué sirve de verdad el paper trading?
o: Para estimar el retorno esperado de la estrategia con datos reales
o: Para practicar la mecánica, los tiempos y el registro de operaciones sin arriesgar dinero
o: Para sustituir al backtest cuando no tienes datos históricos
a: 2
e: Su valor está en el proceso: tipos de orden, tiempos de reacción, hábitos de registro y tolerancia a ver pérdidas. Para estimar el retorno hace falta un backtest con costes modelados, y sin datos históricos el paper trading tampoco los crea: solo acumula muy pocas observaciones de un único régimen.
:::

:::trampa
Un resultado espectacular en demo casi siempre significa una de estas tres cosas: el
simulador te está llenando a precios que no existen, el instrumento es tan ilíquido que en
real no podrías entrar, o has probado tantas configuraciones en paper que te has quedado con
la mejor. Antes de pasarte a real, replica ese mismo periodo en un backtest con costes.
:::
