---
id: especializacion-y-carrera
titulo: Especialización y carrera
fase: 12
nivel: básico
rutas: [core]
prerequisitos: [mapa-del-portal, practicar-con-datos-reales]
tags: [carrera, roles, especializacion, aprendizaje]
resumen: Analista, analytics engineer, ingeniero de datos, científico, MLE y quant: qué produce cada rol, cómo se define por su interfaz y cómo se pasa de uno a otro.
fuentes: ["Newport (2012), 'So Good They Can't Ignore You'"]
---

## En una frase

Elegir especialidad es elegir qué problemas vas a resolver cada día y con quién, y eso se decide por
lo que aguantas hacer repetido, no por el título que aparece en la oferta.

## La idea

Los títulos de los puestos funcionan como los nombres de los platos en cartas de restaurantes
distintos: «ensalada de la casa» puede ser cualquier cosa. Dos ofertas que dicen «data scientist»
pueden ser una de cuadros de mando y otra de investigación; dos que dicen «data engineer» pueden ser
una de SQL y otra de Kubernetes. Lo que define el trabajo no es el título: es lo que entra, lo que
sale y quién usa lo que sale.

Los roles que verás en las ofertas, con su salida principal:

| Rol | Entrada | Salida principal | Latencia | Con quién habla |
| --- | --- | --- | --- | --- |
| Analista de datos | Preguntas de negocio y tablas | Cifra defendible y cuadro de mando | Días | Producto, marketing, dirección |
| Analytics engineer | Datos en crudo y reglas de negocio | Tablas modeladas, probadas y documentadas | Días | Analistas y negocio |
| Ingeniero de datos | Fuentes, contratos y volumen | Datos completos, a tiempo y con coste conocido | Horas | Backend, analistas, ciencia de datos |
| Científico de datos | Preguntas abiertas y experimentos | Estimación con incertidumbre y modelos | Semanas | Producto y dirección |
| Ingeniero de machine learning | Modelos que ya funcionan en un notebook | Modelo desplegado, con latencia y monitorización | Días, con guardias | Backend, plataforma, producto |
| Quant | Series de precios y reglas de riesgo | Señal medida con costes y riesgo | Días | Mesa, riesgo, tecnología |

Cómo se elige, en la práctica: coge cinco ofertas del título que te atrae y **cuenta los verbos**.
Si cuatro de cada cinco dicen «construir y mantener pipelines», el puesto es de ingeniería con otro
nombre, y a ti te tocará hacer eso, no lo que imaginas al leer el título. Después habla con tres
personas que hoy hagan ese trabajo y pregúntales qué ocupó su última semana. La conversación de
veinte minutos ahorra seis meses de estudios equivocados.

Sobre la forma del perfil: lo que se busca es una **T**. Una barra vertical, una competencia en la
que puedas defender decisiones con artefactos, y una barra horizontal, lo justo para entender a
quien está al lado y pedirle bien las cosas. Dos deformaciones frecuentes:

- **La raya horizontal.** Sabes un poco de todo y nada en profundidad; pasas cribas y caes en la
  entrevista técnica, donde te piden un caso con números.
- **La torre sin base.** Dominas un tema de nicho que nadie cerca necesita, y no puedes aplicarlo
  porque no sabes desplegar, ni medir, ni explicarlo.

Y una advertencia sobre los cambios de rol: no se pasa de un rol a otro estudiando, se pasa por
**haber hecho ya dos o tres tareas del rol destino** en el puesto que tienes. Al analista que quiere
ser científico no le falta un máster: le falta haber diseñado un experimento, haberse equivocado con
la métrica y haberlo defendido delante de negocio.

## Definición formal

Un rol se define por su interfaz, no por su nombre:

:::formula
rol = (entrada, salida, latencia, consumidor)
:::

`entrada` es lo que te llega y con lo que trabajas; `salida` es el artefacto que otra persona usa
(una tabla, una cifra, un modelo en producción, una señal); `latencia` es el tiempo entre que te
piden algo y lo entregas; `consumidor` es quien toma decisiones con tu salida. Dos puestos con el
mismo título y distinta interfaz son trabajos distintos, y por eso dos ofertas idénticas se parecen
tan poco por dentro.

Para el perfil en T: `d` es la profundidad, el nivel que puedes respaldar con artefactos revisables
([[portfolio-y-proyectos]]), y `b` es la anchura mínima, lo que sabes de las disciplinas vecinas
para no pedir imposibles. No se mide en cursos: se mide en cosas que otro puede inspeccionar.

Y el coste de un cambio de especialidad se planifica como cualquier proyecto, con horas:

:::formula
semanas ≈ (Σ horas por hito) / (horas disponibles por semana)
:::

`Σ horas por hito` es la suma de lo que cuesta cada artefacto que te falta y `horas disponibles por
semana` es el ritmo que puedes sostener durante meses, no el de una semana buena. Un plan con 120
horas a 6 horas semanales son 20 semanas: cinco meses, no un fin de semana.

## Ejemplo

Ana lleva dos años como analista de datos. Su semana se reparte así: unas 16 horas de SQL, 10 de
cuadros de mando, 8 de reuniones y 6 de peticiones sueltas. Quiere pasar a científica de datos.

Su interfaz actual es (preguntas de negocio, cifras y cuadros, días, producto). La del rol destino
es (preguntas abiertas, estimaciones con incertidumbre, semanas, producto y dirección). Lo que le
falta, con horas estimadas y un artefacto por hito:

- Un experimento diseñado de principio a fin, con su tamaño muestral: 30 horas.
- Un modelo con validación temporal y sus límites escritos: 45 horas.
- Un informe defendido ante negocio con la incertidumbre incluida: 20 horas.
- SQL de ventanas sin mirar la documentación: 25 horas.

Total: 120 horas. A 6 horas por semana, 20 semanas. La trampa que hay que evitar está en la última
columna: hacer esos 120 horas en cursos da cero artefactos y el mismo currículum que ahora. Hacerlas
construyendo los cuatro artefactos da cuatro respuestas concretas en la entrevista.

## Código

```python verificable
# Plan de transicion: horas por hito repartidas al ritmo semanal que puedes sostener.
hitos = {
    "experimento_ab": 30,
    "modelo_con_validacion_temporal": 45,
    "informe_defendido": 20,
    "sql_ventanas": 25,
}
horas_semana = 6
total = sum(hitos.values())

print(f"total {total} h -> {total / horas_semana:.0f} semanas a {horas_semana} h/semana")
# Ordenados por coste: lo que mas tarda es lo que hay que empezar antes.
for nombre, horas in sorted(hitos.items(), key=lambda par: -par[1]):
    print(f"{nombre:32s} {horas:3d} h  {horas / horas_semana:.1f} semanas")
```

```text
total 120 h -> 20 semanas a 6 h/semana
modelo_con_validacion_temporal    45 h  7.5 semanas
experimento_ab                    30 h  5.0 semanas
sql_ventanas                      25 h  4.2 semanas
informe_defendido                 20 h  3.3 semanas
```

```text
Cómo leer una oferta, en cinco preguntas:

1. Qué verbos se repiten en las tareas (construir, analizar, desplegar, decidir).
2. Cuál es la salida: tabla, informe, modelo en producción, señal.
3. Quién consume esa salida dentro de la empresa.
4. Qué se espera de ti en la primera semana y a los tres meses.
5. Con qué herramientas se trabaja hoy, no con cuáles se empezó.
```

## Errores típicos

- **Elegir por el título o por el salario.** El título varía entre empresas y el salario se paga por
  lo que produces. Lee las tareas y pregúntate si aguantarías hacerlas cuatro días a la semana
  durante dos años.
- **Coleccionar certificados en vez de artefactos.** Veinte cursos no equivalen a un experimento
  defendido y a un modelo con sus límites escritos. Lo primero se lee en una línea del currículum;
  lo segundo se discute veinte minutos en la entrevista.
- **Cambiar de especialidad cada seis meses.** Empiezas SQL, luego deep learning, luego
  infraestructura, y a los dos años no tienes profundidad en nada. La barra vertical tarda meses en
  crecer y se cae con cada cambio.
- **Confundir herramienta con rol.** «Sé Spark, luego soy ingeniero de datos». El puesto se juzga
  por datos completos, a tiempo y con coste conocido, no por la herramienta con la que lo consigues
  ([[calidad-y-slas]], [[coste-y-optimizacion]]).
- **Decidir con información de segunda mano.** Lo que cuenta un vídeo de hace cuatro años se parece
  poco a la semana real del puesto. Pregunta a quien lo hace hoy.
- **Esperar a que la empresa te forme.** El proyecto que te falta no te lo van a asignar: pídelo, o
  hazlo con los datos que ya tienes. Nadie va a organizarte la carrera.

## Comprueba que lo sabes

:::quiz
p: Dos ofertas se titulan «data scientist» y parecen idénticas. ¿Qué miras para saber si son el mismo trabajo?
o: La interfaz del rol: qué entra, qué sale, con qué latencia y quién consume la salida
o: El salario, que es lo que mejor resume el puesto
o: Las herramientas listadas, que definen el trabajo diario
o: El tamaño de la empresa, que determina las tareas
a: 1
e: La interfaz separa un puesto de cuadros de mando de uno de investigación aunque compartan título, y se ve en las tareas de la oferta y en quién consume el resultado. El salario refleja el mercado, no las tareas; la lista de herramientas cambia cada año; y el tamaño de la empresa influye, pero no decide qué harás los martes.
:::

:::quiz
p: Eres analista y quieres pasar a científica de datos. ¿Qué demuestra el salto en una entrevista?
o: Un máster o un certificado de estadística
o: Haber diseñado un experimento y defendido una estimación con su incertidumbre
o: Saber usar la librería de moda para gradient boosting
o: Llevar tres años en el mismo equipo
a: 2
e: El salto se demuestra con tareas del rol destino ya hechas: un experimento con tamaño muestral, una estimación con intervalo y un informe defendido. El título académico ayuda a entrar, pero no sustituye al artefacto; la librería de moda es una herramienta, y la antigüedad no cambia lo que haces.
:::

:::quiz
p: Llevas dos años estudiando un poco de SQL, algo de Python, un curso de Spark y otro de deep learning. ¿Qué problema tiene ese perfil?
o: Es una raya horizontal: mucha anchura y ninguna profundidad defendible con artefactos
o: Nada, es el perfil más demandado porque es flexible
o: Que debería haber hecho más cursos para completar el temario
o: Que falta la parte de visualización
a: 1
e: La forma en T exige una barra vertical: una competencia donde puedas defender decisiones con números y artefactos, porque es ahí donde te ponen a prueba. Sin ella, pasas las cribas y caes en la entrevista técnica. Más cursos de lo mismo engorda la raya horizontal en lugar de arreglarla.
:::

:::practica
enunciado: Elige tu especialización para los próximos seis meses y escribe el plan. Necesitas: los dos roles entre los que dudas, la interfaz de cada uno (entrada, salida, latencia, consumidor), los tres o cuatro artefactos que te faltan para el elegido, las horas de cada uno y el ritmo semanal que puedes sostener de verdad. Que quepa en una página y que la última línea diga qué vas a hacer esta semana.
pista: Elige por las tareas diarias, no por el título; y cuenta como horas solo las que puedes sostener un mes entero, no las de una semana perfecta.
solucion: Un plan aceptable tiene esta forma. Roles: ingeniero de datos frente a científico de datos. Interfaces: el ingeniero entrega tablas completas y a tiempo para analistas y científicos, latencia de horas; el científico entrega estimaciones con incertidumbre para producto, latencia de semanas. Decisión: científico, porque lo que te engancha es la pregunta, no el pipeline. Artefactos que faltan: un experimento con tamaño muestral (30 h), un modelo con validación temporal y sus límites (45 h), un informe defendido en negocio (20 h), SQL de ventanas (25 h). Ritmo: 6 h por semana, sostenido; total 120 h y 20 semanas. Esta semana: escribir la hipótesis del experimento y calcular el tamaño muestral con la conversión actual. Y el criterio de abandono: si a las ocho semanas no tienes dos artefactos enseñables, el plan era demasiado grande y hay que recortarlo a dos hitos.
:::
