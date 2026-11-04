---
id: etica-profesional
titulo: Ética profesional
fase: 12
nivel: intermedio
rutas: [core]
prerequisitos: [sesgo-y-etica-en-datos, visualizacion-honesta, escribir-un-informe]
tags: [etica, carrera, comunicacion, incertidumbre]
resumen: Decir «no» con argumentos, reportar el resultado incómodo y no vender humo: tres decisiones que se toman en la reunión, no en un código deontológico.
fuentes: ["Simmons, Nelson y Simonsohn (2011), 'False-Positive Psychology'", "Wasserstein y Lazar (2016), 'The ASA Statement on p-Values'", "O'Neil (2016), 'Weapons of Math Destruction'"]
---

## En una frase

La ética profesional en datos no es un código abstracto: es lo que haces cuando el resultado no
le gusta a quien paga, cuando el dato no se puede usar y cuando te piden el análisis que ya trae
la conclusión escrita.

## La idea

Tres escenas que ocurren todas las semanas:

1. **La conclusión ya está escrita.** Te piden «validar» una campaña que ya se ha decidido
   lanzar, o «demostrar» que el proveedor actual es peor. Un análisis no puede validar una
   decisión: mide un efecto y dice con cuánta incertidumbre lo mide. La salida honesta no es
   negarse en redondo, es convertir el encargo en una pregunta con respuesta posible: «puedo
   estimar cuánto cambió la conversión en el grupo expuesto, con su intervalo, y puedo decirte
   qué haría falta para atribuirlo a la campaña». Si lo que quieren es la diapositiva con la
   flecha hacia arriba, eso no es análisis.
2. **El resultado es incómodo.** El experimento no da significativo; el modelo nuevo pierde
   contra la regla de tres líneas que usa el equipo desde 2019; el informe dice que el problema
   no era la logística sino los precios. Publicarlo cuesta una reunión difícil. Callarlo cuesta
   un año de decisiones tomadas sobre una mejora que nunca existió, y lo paga gente que no sabe
   que el dato era falso. La asimetría es la clave: tú eres la única persona que ve el resultado
   antes de que se convierta en decisión.
3. **El dato no se puede usar así.** Hay identificadores personales en un fichero que se va a
   compartir, una base legal dudosa para reutilizar datos recogidos con otra finalidad, o un
   proveedor que pide el conjunto completo. Aquí la respuesta es corta: no se hace, y se propone
   qué sí se puede hacer con datos agregados o minimizados
   ([[privacidad-y-gdpr]], [[gobierno-y-privacidad]]).

Las tres escenas comparten un mismo problema de fondo: **la información asimétrica**. Nadie puede
auditar desde fuera cuántas variantes probaste, qué filas quitaste ni por qué elegiste ese
segmento. Por eso la honestidad no es un rasgo de carácter, es una práctica con reglas
verificables: dejar por escrito la regla de decisión antes de ver los datos, el número de
pruebas, la incertidumbre y los intereses en juego.

Decir «no» funciona cuando tiene tres partes: un hecho técnico, una alternativa y un registro.

- Hecho técnico: «con 1.000 visitas por variante, el intervalo de la diferencia va de −1,4 a
  +2,6 puntos; no puedo afirmar que mejore».
- Alternativa: «puedo dejarlo corriendo dos semanas más o probarlo solo en la página de pago,
  donde hay más margen por visita».
- Registro: un correo con la recomendación y la fecha. No es para cubrirte las espaldas, es para
  que la próxima persona sepa qué se decidió y con qué información.

Un «no» sin alternativa es una opinión. Un «sí» sin registro es un problema futuro.

## Definición formal

Un informe se considera **reportable** si cumple tres condiciones, todas comprobables por un
tercero que no haya participado:

1. **La regla de decisión es anterior a los datos.** Métrica, umbral, tamaño de muestra y
   criterio de parada están fijados antes de mirar el resultado. Cualquier decisión tomada
   después (quitar un valor extremo, cambiar el periodo, mirar un subgrupo) convierte el análisis
   en exploratorio, y el informe tiene que usar esa palabra.
2. **El número de pruebas es explícito.** Si has comparado `k` variantes, el informe dice `k`. La
   probabilidad de que *alguna* salga significativa por casualidad no es `α`, sino la que calcula
   la fórmula de más abajo, y el umbral contra el que contrastas tiene que reflejarlo.
3. **Se declaran la incertidumbre, la fuente y el interés.** El efecto se da con su intervalo de
   confianza y no solo con su valor central ([[intervalos-de-confianza]]); los datos, con su
   origen y su base legal; y se declara cualquier interés que un lector razonable consideraría
   capaz de inclinar el criterio: te paga el proveedor que evalúas, tienes participación en la
   empresa, o tu bonus depende de que el número salga alto. Se declara antes de entregar, no
   después de que alguien lo pregunte.

La corrección que menciona la condición 2, para `k` comparaciones independientes:

:::formula
P(al menos uno) = 1 − (1 − α)^k
:::

- `α` — probabilidad de falso positivo en una sola prueba; 0,05 por convención.
- `k` — número de comparaciones independientes que has mirado.
- `1 − α` — probabilidad de no equivocarse en una prueba concreta.
- Umbral de Bonferroni: `α / k`. Controla la inflación cuando `k` es pequeño; con muchas pruebas
  correlacionadas es preferible un control de la tasa de falsos descubrimientos
  ([[multiplicidad-y-fdr]], [[data-snooping-y-multiple-testing]]).

Con esas tres piezas se puede definir con precisión lo que coloquialmente llamamos **vender
humo**: presentar una afirmación con más seguridad de la que sostienen los datos. No hace falta
mentir; basta con omitir el intervalo, el número de intentos o el tamaño de la muestra.

## Ejemplo

Un test A/B con 1.000 visitas por variante: 50 conversiones en la variante A (5,0 %) y 56 en la
B (5,6 %).

- Diferencia: +0,6 puntos porcentuales, que en relativo es un +12 %.
- Error típico de la diferencia: 1,0 puntos.
- `z` = 0,6 / 1,0 = 0,60, con un p-valor aproximado de 0,55.
- Intervalo de confianza al 95 %: [−1,36; +2,56] puntos.

Lo que pide el cliente es la frase «hemos mejorado un 12 %». Lo que dicen los datos es que la
diferencia es compatible con perder 1,4 puntos y con ganar 2,6, y que con esta muestra no hay
nada decidido. Ninguna de las dos frases es mentira; la primera es la que se usará en una
reunión para justificar una inversión.

Segunda parte de la misma tarde: has mirado 12 subgrupos y en uno el efecto sale con un p-valor
de 0,03. Sin haber probado nada antes, la probabilidad de que aparezca al menos un subgrupo
«significativo» es 1 − 0,95¹² = 0,46: casi la mitad de las veces que partes una muestra en 12
trozos encuentras uno que parece un hallazgo sin que haya pasado nada. El umbral corregido sería
0,05 / 12 = 0,0042, y 0,03 no lo pasa. Ese subgrupo se reporta como exploratorio y pendiente de
replicar, nunca como conclusión.

## Código

```python verificable
# Cuantas veces basta mirar los datos para "encontrar" un efecto que no existe.
for k in (1, 5, 20, 100):
    al_menos_uno = 1 - (1 - 0.05) ** k
    # umbral de Bonferroni: reparte el 5 % entre todas las pruebas hechas
    print(f"{k:>3} pruebas  P(algun falso positivo) = {al_menos_uno:.4f}"
          f"  umbral Bonferroni = {0.05 / k:.4f}")
```

```python verificable
import math

# Dos variantes de una pagina: 50 y 56 conversiones sobre 1.000 visitas cada una.
n_a, x_a = 1000, 50
n_b, x_b = 1000, 56
p_a, p_b = x_a / n_a, x_b / n_b
diferencia = p_b - p_a

# Error tipico de la diferencia de dos proporciones independientes.
se = math.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
z = diferencia / se
p_valor = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))

print(f"conversion A {p_a:.3%}  B {p_b:.3%}")   # -> conversion A 5.000%  B 5.600%
print(f"diferencia {diferencia:.4f} = {diferencia * 100:.2f} puntos")  # -> diferencia 0.0060 = 0.60 puntos
print(f"error tipico {se:.4f}")                # -> error tipico 0.0100
print(f"z {z:.2f}  p {p_valor:.3f}")           # -> z 0.60  p 0.549
print(f"IC 95%  [{diferencia - 1.96 * se:+.4f}, {diferencia + 1.96 * se:+.4f}]")
```

```python verificable
# La exactitud que no hay que vender: un problema con un 1 % de casos positivos.
n = 10000
positivos = 100                    # 1 % de los casos; el resto son negativos
vp, fn, fp, vn = 60, 40, 90, 9810  # matriz de confusion del modelo

exactitud = (vp + vn) / n
sensibilidad = vp / (vp + fn)      # de los positivos reales, cuantos detecta
precision = vp / (vp + fp)         # de los que marca, cuantos lo son

print(f"el que dice siempre 'no' acierta {(n - positivos) / n:.2%}")  # -> 99.00%
print(f"exactitud {exactitud:.2%}")        # -> 98.70%
print(f"sensibilidad {sensibilidad:.2%}")  # -> 60.00%
print(f"precision {precision:.2%}")        # -> 40.00%
```

## Errores típicos

- **Elegir la métrica, el periodo o el subgrupo después de ver los resultados.** Es la trampa
  más común y la más fácil de cometer sin mala intención: buscas «el ángulo» y acabas
  seleccionando el corte que sale bonito. Fija el criterio antes y, si exploras después,
  etiqueta el hallazgo como exploratorio ([[data-snooping-y-multiple-testing]]).
- **Reportar el resultado que salió bien y callar los otros diecinueve.** El informe debe decir
  cuántas comparaciones has hecho, porque el lector no puede adivinarlo. Con 20 pruebas, la
  probabilidad de al menos un falso positivo es 0,64.
- **Leer «no significativo» como «no hay efecto».** Son cosas distintas: el intervalo puede
  incluir perfectamente el efecto que te importaba, y lo que falta es muestra o potencia
  ([[errores-tipo-i-ii-y-potencia]], [[tamano-muestral]]).
- **Aceptar el encargo con la conclusión ya decidida.** Si la pregunta es «¿cómo demuestro que
  esto funciona?», la respuesta profesional es reescribirla como una pregunta contrastable y
  ofrecer un diseño que pueda responderla ([[ab-testing]], [[inferencia-causal-metodos]]).
  Correlación no es causa, por alta que sea ([[causalidad-vs-correlacion]]).
- **Vender una métrica que suena bien y mide mal.** Un 98,7 % de exactitud en un problema con un
  1 % de positivos es peor que decir siempre que no, y la sensibilidad del 60 % con una precisión
  del 40 % cuenta la historia real ([[desbalanceo-de-clases]], [[matriz-de-confusion]]).
- **Maquillar el gráfico o el eje para que el efecto parezca grande.** Truncar el eje, cambiar
  la escala o agregar en la unidad que más conviene es una decisión técnica con consecuencias
  éticas: [[visualizacion-honesta]] explica cómo se hace bien. Lo mismo con quitar dos valores
  extremos justo después de ver que el p-valor estaba en 0,06.

:::practica
enunciado: En un experimento has mirado 4 métricas principales y 9 subgrupos de usuarios. Ninguna métrica principal es significativa (el p-valor menor es 0,31), pero en el subgrupo de usuarios de móvil el efecto sale con un p-valor de 0,02. ¿Qué reportas y con qué umbral?
pista: Cuenta todas las comparaciones que has mirado, no solo las que salieron bien.
solucion: Se han hecho 4 + 9 = 13 contrastes, así que el umbral de Bonferroni es 0,05 / 13 = 0,0038, muy por debajo de 0,02: el hallazgo del subgrupo móvil no se sostiene. Lo que se entrega es la métrica principal con su intervalo de confianza y el resultado no concluyente, la lista completa de los 13 contrastes y el subgrupo móvil marcado como exploratorio y pendiente de replicar en un experimento nuevo con esa hipótesis fijada de antemano. Publicar solo el 0,02 y omitir los otros 12 contrastes es exactamente vender humo.
:::

## Comprueba que lo sabes

:::quiz
p: Has probado 20 variantes y una sale con un p-valor de 0,01. ¿Cuál es la lectura correcta?
o: Se publica, porque 0,01 es menor que 0,05
o: Se contrasta contra un umbral corregido por las 20 pruebas y se informa de que se probaron 20
o: Se descarta, porque con 20 pruebas nada puede ser significativo
a: 2
e: Con 20 pruebas independientes la probabilidad de al menos un falso positivo es 1 − 0,95²⁰ = 0,64, así que un 0,01 aislado no es raro. El umbral de Bonferroni sería 0,05 / 20 = 0,0025 y el hallazgo no lo pasa, pero eso no lo invalida: lo convierte en exploratorio y hay que replicarlo. Descartarlo sin más también sería un error.
:::

:::quiz
p: El intervalo de confianza al 95 % de la diferencia de conversión es [−1,4; +2,6] puntos. ¿Qué se puede afirmar?
o: Que no hay ninguna diferencia entre las variantes
o: Que los datos son compatibles con una pérdida y con una ganancia, así que no hay evidencia suficiente para decidir
o: Que la mejora es del 12 % y se puede lanzar la variante B
a: 2
e: El intervalo incluye el cero, de modo que la ausencia de evidencia es lo único sólido. Eso no prueba que el efecto sea nulo: el extremo superior admite una ganancia notable y el inferior admite una pérdida de hasta 1,4 puntos. La opción 1 confunde «no concluyente» con «sin efecto», y la 3 se queda con el valor central e ignora todo lo que cabe dentro del intervalo.
:::

:::quiz
p: Un cliente te pide un modelo que demuestre que su proveedor actual es peor. ¿Cuál es la respuesta profesional?
o: Construirlo, porque el cliente decide qué necesita
o: Explicar qué se puede estimar con esos datos, proponer un diseño que sí responda a la pregunta y dejar la recomendación por escrito
o: Negarse a hacer el trabajo sin dar más explicaciones
a: 2
e: Un modelo no demuestra una conclusión predeterminada: estima un efecto con su incertidumbre. La respuesta útil separa el hecho técnico (qué admite el dato), la alternativa (un diseño contrastable) y el registro (la recomendación por escrito). Hacerlo sin más es vender humo y negarse sin alternativa deja al cliente sin salida.
:::

:::aviso
La presión casi nunca llega como una orden explícita. Llega como una fecha, una pregunta repetida
tres veces o un «bueno, tú verás». Escribe tu recomendación por correo en el momento en que la
tomas, con la fecha y las limitaciones: es la única defensa que funciona cuando seis meses
después alguien pregunta por qué se decidió aquello.
:::
