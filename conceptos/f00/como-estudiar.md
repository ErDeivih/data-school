---
id: como-estudiar
titulo: Cómo estudiar esto
fase: 0
nivel: básico
rutas: [core]
prerequisitos: []
tags: [estudio, metodo, memoria, habito]
resumen: Recuperar de memoria, repartir los repasos en el tiempo e intercalar temas: eso es estudiar. Releer y subrayar solo dan sensación de aprender.
fuentes: ["Ebbinghaus (1885), 'Über das Gedächtnis'", "Roediger y Karpicke (2006), 'Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention'", "Rohrer y Taylor (2007), 'The shuffling of mathematics problems improves learning'"]
---

## En una frase

Estudiar no es leer: es intentar recordar sin mirar, fallar, corregir y volver a intentarlo unos
días después. Lo demás —releer, subrayar, ver vídeos— se siente productivo y deja muy poco.

## La idea

Piensa en el gimnasio. Nadie se pone fuerte viendo a otro levantar peso: el músculo crece con el
esfuerzo de levantarlo tú. La memoria funciona parecido, con un matiz que lo cambia todo: no
crece al **meter** información, sino al intentar **sacarla**. Cada vez que recuperas algo con
esfuerzo, esa huella se refuerza; cada vez que solo lo relees, se hace más familiar y nada más.

Ebbinghaus midió esto sobre sí mismo a finales del siglo XIX y dibujó la **curva del olvido**: lo
que aprendes sin repasar se cae muy rápido las primeras horas y los primeros días, y después la
pérdida se estabiliza. La buena noticia es que cada repaso exitoso aplana esa curva: lo que hoy
se te escapa en dos días, tras varios repasos aguanta semanas. De ahí salen tres prácticas que
juntas hacen casi todo el trabajo:

1. **Recuperación activa.** Cierra el texto y responde de memoria. Es lo que hacen las
   [[mapa-del-portal|preguntas de repaso del portal]]. Si algo «te suena» pero no te sale, no lo
   sabes.
2. **Repaso espaciado.** Reparte los repasos en el tiempo, con intervalos cada vez más largos
   (hoy, mañana, en tres días, en una semana). Los mismos minutos repartidos enseñan mucho más
   que los mismos minutos de golpe.
3. **Práctica deliberada.** Trabaja justo lo que te falla, con corrección inmediata, en lugar de
   repasar lo que ya te sale. Es incómodo, y precisamente por eso funciona.

Hay una cuarta que casi todo el mundo ignora: el **intercalado**. Mezclar tipos de problema en la
misma sesión se siente peor que hacer veinte ejercicios iguales seguidos, y rinde mejor en la
prueba de después, porque te obliga a decidir *qué* herramienta usar y no solo a aplicarla. Y un
aviso que ahorra meses: la **ilusión de fluidez**, que es confundir «me suena» con «lo sé».

## Definición formal

Un modelo habitual de la retención, cómodo para razonar aunque no sea una ley:

:::formula
R(t) = R₀ · e^(−t/S)
:::

- `R(t)` — retención al cabo de `t` días, entre 0 y 1 (1 = lo recuerdas entero).
- `R₀` — retención justo después de estudiar; si lo has entendido, cerca de 1.
- `t` — días transcurridos desde el último repaso.
- `S` — fuerza o estabilidad de la huella: cuanto mayor es, más plano es el olvido.
- `e` — base del logaritmo natural, ≈ 2,718.

Con `S = 8`, un día después retienes `e^(−1/8) ≈ 0,88`; a los 35 días, `e^(−35/8) ≈ 0,01`. Si
cinco repasos han elevado la fuerza a `S ≈ 187` (el ejemplo de abajo lo calcula: cada repaso la
multiplica por 2,2), el día 35, contando desde el último repaso el día 16, la retención sigue en
`0,90`; esos mismos 19 días con `S = 8` darían `0,09`. El número exacto da igual: lo que importa
es que `S` crece con cada recuperación y el intervalo que aguanta crece con ella.

Los términos, uno a uno:

- **olvido** — pérdida de acceso a algo que estaba almacenado.
- **repaso espaciado** — repartir los repasos en intervalos crecientes.
- **recuperación activa** — traer la información a la memoria sin mirarla.
- **intercalado** — alternar temas o tipos de problema dentro de una sesión, frente al estudio en
  bloques del mismo tipo.
- **práctica deliberada** — entrenar la parte concreta que falla, con corrección inmediata.

## Ejemplo

Supón que dedicas 80 minutos a un concepto. Dos formas de gastarlos:

| Reparto | Sesiones | Minutos | Qué pasa el día 20 |
| --- | --- | --- | --- |
| De golpe | día 1 | 80 | Has leído el tema cuatro veces seguidas; no puedes resolver un ejercicio sin volver al texto |
| Espaciado | días 1, 2, 4, 8 y 20 | 40 + 10 + 10 + 10 + 10 | Cada sesión empieza intentando recordar; el día 20 resuelves el ejercicio sin ayuda |

Mismo coste, resultado distinto. Fíjate en la primera sesión del plan espaciado: 40 minutos para
leer y **resumir de memoria** lo leído, tapando el texto. Esa parte es la que casi nadie hace,
porque es la que resulta incómoda.

Añade intercalado al final: el día 20, mezcla el tema nuevo con el anterior (cinco preguntas de
cada uno, en orden aleatorio). Si te toca decidir cuál de las dos herramientas aplicar, has
aprendido algo que el estudio en bloques no entrena.

## Código

```python verificable
import numpy as np

# Curva del olvido: R(t) = exp(-t/S). Cada repaso exitoso multiplica S (la fuerza
# de la huella) y por eso el intervalo que aguanta se puede alargar.
dias_repaso = [0, 1, 3, 7, 16]
factor, S0 = 2.2, 8.0

fuerza_final = S0 * factor ** (len(dias_repaso) - 1)
dias_desde_ultimo = 35 - dias_repaso[-1]

print(f"fuerza tras 5 repasos       {fuerza_final:6.1f}")                     # ->  187.4
print(f"retencion el dia 35         {np.exp(-dias_desde_ultimo / fuerza_final):.2f}")  # -> 0.90
print(f"retencion el dia 35 sin nada {np.exp(-35 / S0):.3f}")                  # -> 0.013
```

```python verificable
import numpy as np

# El mismo modelo aplicado a tres planes hasta un examen el dia 30. Es un modelo,
# no una medida: compara planes, no predice tu nota.
def retencion(dia_examen, repasos, S0=8.0, factor=2.2):
    fuerza = S0 * factor ** (len(repasos) - 1)      # cada repaso multiplica la fuerza
    return np.exp(-(dia_examen - repasos[-1]) / fuerza)

print(f"plan A (solo el dia 1)         {retencion(30, [1]):.3f}")                  # -> 0.027
print(f"plan B (dias 1, 2, 4 y 8)      {retencion(30, [1, 2, 4, 8]):.3f}")          # -> 0.772
print(f"plan C (dias 1, 2, 4, 8, 16, 30) {retencion(30, [1, 2, 4, 8, 16, 30]):.3f}")  # -> 1.000
```

## Errores típicos

- **Releer y subrayar como método principal.** Es cómodo y produce familiaridad, no recuerdo. Si
  no hay un momento de recuperación sin mirar, no hay aprendizaje duradero.
- **Estudiar en bloques largos de un solo tema.** Veinte ejercicios idénticos seguidos te hacen
  sentir competente. Mezcla tipos de problema: decidir cuál usar es la mitad del trabajo real.
- **Ver tutoriales sin escribir código.** El vídeo avanza y tú asientes. Cierra la pestaña y
  reproduce el ejemplo desde cero; si no te sale, ese es el trozo que toca estudiar. Es la razón
  de que [[practicar-con-datos-reales|practicar con datos reales]] rinda tanto.
- **Dejarlo todo para el último día.** El atracón funciona para un examen de mañana y falla a las
  dos semanas. Sirve para aprobar, no para saber.
- **Mirar la solución a los veinte segundos.** Intenta en papel, escribe lo que sepas aunque esté
  a medias y solo entonces consulta. El rato de atasco es donde se consolida.
- **Medir el progreso en horas o en páginas.** La única medida útil es cuántas preguntas sabes
  responder sin mirar. Diez minutos de preguntas valen más que una hora de lectura.

## Comprueba que lo sabes

:::quiz
p: ¿Cuál de estas actividades produce más aprendizaje por minuto?
o: Releer el tema subrayando las frases importantes
o: Responder de memoria a una pregunta y luego comprobar si acertaste
o: Copiar los apuntes a limpio para que queden ordenados
a: 2
e: La recuperación con esfuerzo es la que refuerza la huella; subrayar y copiar solo aumentan la familiaridad con el texto, que es justo lo que te hace creer que ya lo sabes. Comprobar después es lo que corrige el error.
:::

:::quiz
p: ¿Por qué el repaso espaciado rinde más que estudiar lo mismo de una vez?
o: Porque el cerebro necesita descansar entre lecturas para no saturarse
o: Porque recuperar algo parcialmente olvidado cuesta más esfuerzo y deja una huella más fuerte, y el intervalo se puede ir alargando
o: Porque así se estudia menos cantidad de materia
a: 2
e: El olvido parcial es la oportunidad: la dificultad de recuperar es la que consolida. Descansar ayuda, pero el motivo central es el esfuerzo de recuperación distribuido en el tiempo; y se estudia exactamente la misma materia, solo repartida.
:::

:::practica
enunciado: Tienes 6 conceptos nuevos por delante y 3 horas esta semana. Reparte el tiempo entre primera lectura, repasos y preguntas, sabiendo que quieres poder responder a las preguntas de los 6 conceptos el día 30.
pista: Piensa en cuántas sesiones necesitas por concepto y en cuánto dura una recuperación.
solucion: Dedica 20 minutos por concepto a la primera lectura con resumen de memoria (120 minutos en total, 2 horas). Reserva los 60 minutos restantes para cinco sesiones de 12 minutos repartidas en los días 2, 4, 8, 15 y 30, mezclando conceptos y respondiendo primero sin mirar. No hace falta releer nada: si una pregunta falla dos veces, ese concepto se lleva 5 minutos extra el día siguiente.
:::

:::trampa
Sentir que un tema «ya te suena» es la señal más peligrosa: es fluidez, no conocimiento. Antes
de marcar un concepto como dominado, tapa la página y explícalo en voz alta en un minuto. Si te
atasco en la segunda frase, vuelve al texto.
:::
