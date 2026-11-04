---
id: escribir-un-informe
titulo: Escribir un informe técnico
fase: 12
nivel: intermedio
rutas: [core]
prerequisitos: [storytelling-con-datos]
tags: [comunicacion, informes, decision, reproducibilidad]
resumen: Un informe técnico se lee en cinco minutos y de arriba abajo: conclusión primero, método reproducible, resultados con su incertidumbre, límites y qué hacer.
fuentes: ["Minto (2008), 'The Pyramid Principle: Logic in Writing and Thinking'", "Alley (2018), 'The Craft of Scientific Writing'"]
---

## En una frase

Un informe técnico no es el diario de tu análisis, sino la decisión que propones escrita para
que otra persona pueda revisarla, repetirla y discutirla sin tenerte delante.

## La idea

Imagina el parte médico después de una analítica. No empieza contando cómo se calibró el
aparato: empieza diciendo qué tienes y qué hay que hacer. El método y los valores están detrás,
disponibles para quien quiera comprobarlos, pero el que tiene prisa se queda con la primera
línea y decide bien. Un informe técnico funciona igual, y casi todos se escriben al revés: el
autor cuenta lo que hizo en el orden en que lo hizo (datos, limpieza, pruebas, modelo, gráfico)
y deja la conclusión en la última diapositiva, cuando ya nadie escucha.

La estructura que aguanta tiene cinco piezas, en este orden:

1. **Resumen.** Qué se preguntaba, qué se ha encontrado y qué recomiendas, en medio folio. Si
   quien decide solo lee esto, tiene que poder actuar.
2. **Método.** De dónde salen los datos (fuente, periodo, filtros, cuántas filas quedaron
   después de limpiar), cómo se ha medido cada cosa y qué se descartó por el camino. Esta
   sección no es un trámite: es lo que permite que alguien repita tu resultado y lo discuta en
   vez de creértelo.
3. **Resultados.** Las cifras con su base y su incertidumbre. Un resultado sin `n` y sin margen
   de error no es un resultado, es una anécdota.
4. **Límites.** Qué no has podido medir, qué supuestos sostienen las conclusiones y qué
   evidencia las daría la vuelta. Escribirlo tú es lo que impide que lo escriba tu crítico.
5. **Recomendaciones.** Qué hacer, quién lo hace, cuánto cuesta y cómo se sabrá si funcionó.

El informe técnico tiene tres lectores distintos y conviene escribir para los tres a la vez:
quien decide (lee el resumen y las recomendaciones), quien revisa (lee el método y busca el
fallo) y quien hereda el trabajo dentro de un año (lee todo y necesita poder ejecutarlo). De ahí
salen dos reglas prácticas. La primera: **cada afirmación importante lleva su base** («de 1.240
tickets del trimestre», no «de los tickets»). La segunda: **nada de resultados sin comparación**;
absoluto sin referencia no significa nada, así que todo número va con el periodo anterior, el
objetivo o el grupo de control.

Hay una prueba de fuego para el resumen: léelo en voz alta y pregúntate si alguien podría
tomar una decisión distinta después de leerlo. «Se ha analizado el rendimiento del modelo y se
proponen mejoras» no pasa la prueba. «Con el umbral en 0,30 el coste esperado baja de 173.500 a
96.000 euros por cada 1.000 solicitudes; recomiendo bajarlo y revisar en un mes» sí.

## Definición formal

Un informe es una lista ordenada de secciones, pero cada afirmación que contiene tiene tres
componentes obligatorios:

:::formula
afirmación = efecto ± incertidumbre, sobre n = …, en el periodo …
:::

- `efecto` — la magnitud del cambio, en unidades o en porcentaje, siempre con su dirección.
- `incertidumbre` — el error típico, el intervalo de confianza o, como mínimo, el número de
  observaciones que lo sostienen ([[intervalos-de-confianza]]).
- `n` — la base: cuántos casos hay detrás ([[tamano-muestral]]).
- `periodo` — el tramo de tiempo al que se refiere, y si es comparable con aquello con lo que
  lo comparas.

Y cuando el informe termina en una decisión con costes distintos según el error, la
recomendación se escribe como una cuenta, no como una opinión:

:::formula
coste = FN · C_falso_negativo + FP · C_falso_positivo
:::

- `FN` — falsos negativos: los casos que el modelo deja pasar y resultan caros (por ejemplo,
  un impago concedido).
- `FP` — falsos positivos: los casos que el modelo rechaza y no debía (un buen cliente al que
  se le niega el crédito).
- `C_falso_negativo`, `C_falso_positivo` — lo que cuesta cada uno de esos dos errores, en
  dinero o en la unidad que uses.

Elegir el umbral minimizando esa suma es una decisión de negocio explícita: si cambias los
costes, cambia el umbral, y eso queda escrito en el informe en vez de escondido en el código
([[umbrales-y-coste]]).

## Ejemplo

Un modelo de concesión de crédito sobre 1.000 solicitudes, de las que 100 acaban en impago y
900 se pagan. Cada impago concedido cuesta 4.000 € y cada buen cliente rechazado deja de aportar
300 € de margen.

- **Umbral 0,50:** deja pasar 40 impagos y rechaza a 45 buenos clientes.
  `40 · 4.000 + 45 · 300 = 160.000 + 13.500 =` **173.500 €** de coste esperado.
- **Umbral 0,30:** deja pasar 15 impagos y rechaza a 120 buenos clientes.
  `15 · 4.000 + 120 · 300 = 60.000 + 36.000 =` **96.000 €**.
- Bajar el umbral ahorra **77.500 €** por cada 1.000 solicitudes, a costa de rechazar 75
  clientes buenos más.

El informe no debería terminar en «el modelo tiene un AUC de 0,81» ([[roc-auc]]), porque eso no
es una decisión. Termina así: *«Recomiendo fijar el umbral en 0,30. Con los costes actuales, el
coste esperado baja un 45 % frente al umbral de 0,50. El resultado depende de que el margen por
buen cliente sea realmente 300 €: si el rechazo provoca además la pérdida del cliente a largo
plazo, el umbral óptimo sube. Revisar en un mes con los datos del primer lote.»* Ahí están la
recomendación, la cifra, la sensibilidad al supuesto y la revisión.

## Código

```python verificable
# Un informe no acaba en la metrica: acaba en la decision. Matriz de confusion de un
# modelo de impago sobre 1.000 solicitudes (100 impagan y 900 pagan), a dos umbrales.
coste_impago = 4000.0   # EUR que se pierden si se concede y no paga
margen_bueno = 300.0    # EUR que se dejan de ganar si se rechaza a quien si pagaba

def coste(impagos_concedidos, buenos_rechazados):
    return impagos_concedidos * coste_impago + buenos_rechazados * margen_bueno

for umbral, impagos, buenos in [("0.50", 40, 45), ("0.30", 15, 120)]:
    print(f"umbral {umbral}: {impagos} impagos concedidos, {buenos} buenos rechazados, "
          f"coste {coste(impagos, buenos):,.0f} EUR por 1.000 solicitudes")
# -> umbral 0.50: 40 impagos concedidos, 45 buenos rechazados, coste 173,500 EUR por 1.000 solicitudes
# -> umbral 0.30: 15 impagos concedidos, 120 buenos rechazados, coste 96,000 EUR por 1.000 solicitudes

print(f"ahorro al bajar el umbral: {coste(40, 45) - coste(15, 120):,.0f} EUR")
# -> ahorro al bajar el umbral: 77,500 EUR
```

```text
1. Resumen (medio folio)
   - Que se preguntaba, que se ha encontrado, que se recomienda.
   - La cifra principal, con su base y su incertidumbre.
2. Metodo (una pagina)
   - Datos: fuente, periodo, filtros y cuantas filas quedaron.
   - Definicion de cada metrica y como se midio.
   - Que se probo, que se descarto y por que.
3. Resultados (una o dos paginas)
   - Tablas y graficos con n, comparacion y margen de error.
4. Limites (medio folio)
   - Que no se ha podido medir.
   - Que evidencia cambiaria la conclusion.
5. Recomendaciones (medio folio)
   - Que hacer, quien, cuanto cuesta y como se revisa.
Anexo: consultas, definiciones, detalle por segmento.
```

```python ilustrativo
# La misma cifra con tres redacciones. Solo la tercera permite decidir.
antes_h, despues_h, tickets, error_h = 9.2, 8.1, 1240, 0.3

print(f"El tiempo de resolucion medio baja {antes_h - despues_h:.1f} h.")
print(f"El tiempo de resolucion medio baja {antes_h - despues_h:.1f} h sobre {tickets} tickets.")
print(f"Baja {antes_h - despues_h:.1f} h sobre {tickets} tickets del trimestre, con un error "
      f"tipico de {error_h:.1f} h: la bajada supera el margen y se sostiene.")
```

## Errores típicos

- **Escribir en el orden en que trabajaste.** Datos, limpieza, pruebas, modelo y conclusión al
  final. Quien decide se pierde en la segunda página. La conclusión va en el resumen, aunque
  para llegar a ella hayas tardado tres semanas.
- **Dar el resultado sin base.** «La conversión mejora un 7 %» con 30 usuarios no es un
  resultado. Cada cifra lleva su `n` y su periodo; y si el `n` es pequeño, dilo tú antes de que
  lo diga el que revisa ([[p-valor]]).
- **Esconder los límites.** Un informe que solo cuenta lo que salió bien se cae en cuanto
  alguien prueba el caso que no cubriste. La sección de límites no debilita el informe: le
  quita al crítico su mejor argumento.
- **Terminar en «hay que seguir investigando».** Una recomendación vaga no se puede ejecutar ni
  rebatir. Di qué harías, con qué coste y qué haría falta para confirmarlo.
- **No ser reproducible.** Sin versión de los datos, sin semilla y sin los filtros escritos, el
  resultado no se puede repetir y por tanto no se puede defender ([[notebooks-vs-scripts]],
  [[fuga-de-datos]]).
- **Confundir el informe con la presentación.** Un informe se lee y se cita; una presentación
  se escucha y se recuerda. Si pegas las 40 diapositivas como documento, nadie encontrará la
  decisión ([[presentaciones]]).

:::truco
Escribe primero el resumen, antes de hacer el análisis. Te obliga a decidir de antemano qué
pregunta respondes y qué haría que cambiaras de opinión. Si al terminar el análisis el resumen
ya no encaja, has aprendido algo: el titular lo dictan los datos, no el plan.
:::

:::practica
enunciado: Un informe afirma: «el nuevo proceso de despliegue reduce los fallos en producción un 40 %». En el anexo se ve que hubo 5 fallos en los 3 meses anteriores y 3 fallos en los 3 meses posteriores. ¿Qué le falta al titular y cómo lo reescribirías?
pista: Calcula la cifra absoluta del cambio y piensa cuánta incertidumbre cabe en números de un dígito.
solucion: El 40 % sale de 5 a 3 fallos: dos fallos menos. Con esas cifras, el porcentaje amplifica el ruido en lugar de resumirlo, porque un solo fallo distinto cambia el resultado decenas de puntos. El titular honesto es «los fallos en producción pasan de 5 a 3 en trimestres comparables; con números tan pequeños no se puede afirmar una reducción del 40 %: harían falta varios trimestres o más despliegues». Además falta el denominador (cuántos despliegues hubo en cada periodo) y el periodo exacto.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es el orden correcto de un informe técnico?
o: Método, resultados, resumen y recomendaciones
o: Resumen con la conclusión, método, resultados, límites y recomendaciones
o: Resultados, límites, método y resumen al final
a: 2
e: El resumen va primero porque quien decide puede leerlo y actuar sin llegar al resto, y los límites van antes de las recomendaciones porque una recomendación sin sus supuestos es una opinión. El orden en que investigaste no es el orden en que se lee.
:::

:::quiz
p: Con 1.000 solicitudes, cada impago concedido cuesta 4.000 euros y cada buen cliente rechazado 300, ¿qué umbral conviene entre los dos evaluados?
o: El de 0,50, porque rechaza a menos clientes buenos
o: El de 0,30, porque el coste esperado es 96.000 euros frente a 173.500
o: Da igual, porque los dos modelos tienen la misma capacidad de discriminación
a: 2
e: El umbral se elige por el coste de los dos errores, no por el número de rechazos. Bajar de 0,50 a 0,30 deja pasar 25 impagos menos y rechaza 75 buenos más, y la cuenta sale claramente a favor del 0,30. La tercera opción confunde la calidad del modelo con el punto de corte.
:::

:::quiz
p: ¿Para qué sirve la sección de límites?
o: Para justificar por qué no has hecho más trabajo
o: Para decir qué no se ha podido medir y qué evidencia daría la vuelta a la conclusión
o: Para que el informe parezca más largo y formal
a: 2
e: Los límites acotan el alcance de la afirmación y te protegen: si el informe dice en qué condiciones deja de valer, el que lo lea sabe cuándo aplicarlo. La primera opción es una excusa y la tercera no aporta nada.
:::
