---
id: open-source
titulo: Contribuir a código abierto
fase: 12
nivel: intermedio
rutas: [core, alg]
prerequisitos: [git-para-datos, testing-con-pytest, code-review]
tags: [open-source, git, comunidad, carrera]
resumen: Encontrar un fallo reproducible, arreglarlo en un parche pequeño que otro pueda revisar y responder a la revisión: así se entra y se construye reputación.
fuentes: ["Fogel (2005), 'Producing Open Source Software'", "Eghbal (2016), 'Roads and Bridges: The Unseen Labor Behind Our Digital Infrastructure'"]
---

## En una frase

Contribuir a código abierto es resolver un problema pequeño y concreto en un proyecto que ya tiene
sus reglas, con un parche que otra persona pueda revisar en diez minutos.

## La idea

Entrar en un proyecto abierto se parece a entrar en una cocina ajena en plena hora punta. No llegas
y cambias el menú: lees las normas de la casa, empiezas por lo pequeño y, cuando ya te conocen, te
dejan el fuego fuerte. El error de casi todo el mundo es entrar con la reforma entera bajo el brazo.

Hay tres motivos concretos para hacerlo, y ninguno es «queda bien en el currículum»:

- **Revisión de código gratis** de gente que lleva años con ese código. Es la forma más rápida de
  aprender convenciones que en tu repositorio nadie te corrige.
- **Un historial público y verificable.** Tu perfil muestra qué cambiaste y cómo respondiste a una
  crítica; no muestra lo que dices saber.
- **Conoces por dentro las librerías que usas.** Cuando algo falle a las tres de la mañana, haber
  leído ese trozo de código ahorra horas.

El orden de entrada que funciona:

1. **Documentación.** Un párrafo confuso, un ejemplo con una errata, un enlace roto. Nadie discute
   un parche de documentación y aprendes el proceso completo: bifurcar, rama, PR, integración
   continua.
2. **Una prueba que falta.** Reproduces un fallo y escribes la prueba que lo captura, antes del
   arreglo. Esa prueba sola ya es una contribución valiosa ([[testing-con-pytest]]).
3. **Un `good first issue`.** Muchos proyectos etiquetan así las tareas acotadas para quien llega
   nuevo. Están pensadas para que las hagas mal la primera vez sin romper nada.
4. **Un arreglo de verdad**, cuando el mantenedor ya sabe quién eres.

:::aviso
Antes de escribir una línea, lee `CONTRIBUTING.md`, el `README` y las últimas diez PR fusionadas.
Ahí están el estilo, el formato de los mensajes de commit, el comando de las pruebas y si piden
firmar el DCO (una línea al final del mensaje de commit con la que certificas que puedes aportar ese
código). Cada proyecto es distinto y adivinar sale caro.
:::

## Definición formal

Una contribución aceptable es un par (problema, parche) que cumple cuatro condiciones:

1. **Un solo cambio.** Si toca dos cosas, son dos PRs.
2. **Una rama propia**, creada desde el commit actual de la rama principal del proyecto, nunca
   commits directos sobre ella ([[git-para-datos]]).
3. **Una prueba que falla antes del parche y pasa después.** Sin eso, el revisor no tiene forma de
   saber qué arreglaste.
4. **Integración continua en verde** y el linter del proyecto satisfecho.

Y todo PR va precedido de un **informe reproducible** con seis campos: versión instalada, sistema
operativo, pasos exactos, resultado esperado, resultado obtenido y la traza mínima. Si falta
cualquiera de los seis, el mantenedor tiene que adivinar y el informe se queda sin arreglar.

:::formula
PR aceptable = un solo cambio + prueba que lo cubre + CI en verde + discusión previa si toca la API pública
:::

`CI` es la integración continua: el sistema que ejecuta las pruebas automáticamente en cada PR
([[ci-cd]]). `API pública` son las funciones y clases documentadas para quien usa la librería;
cambiarlas rompe el código de otros y exige discusión, aviso y a menudo subir la versión mayor
([[apis-rest]]). Regla práctica: un parche de menos de 200 líneas se revisa en días; uno de 2.000 se
queda abierto meses, o para siempre.

## Ejemplo

Un recorrido completo, con una librería de ejemplo (`validador-datos`) que valida tablas antes de
cargarlas.

Usas la librería y, al pedir una columna que no existe, salta `KeyError: 'moneda'` desde el fondo
del código, sin decirte qué columnas hay. Pierdes media hora buscando el fallo.

- **Paso 1.** Buscas en los issues abiertos si ya lo reportaron. Existe un issue parecido, cerrado,
  sobre otro caso: tu fallo es distinto y lo explicas.
- **Paso 2.** Lo reproduces en seis líneas, con la versión instalada anotada.
- **Paso 3.** Abres el issue con los seis campos. El mantenedor contesta en dos días: «acepto un PR,
  pero el mensaje de error debe listar las columnas disponibles».
- **Paso 4.** Mandas un PR de nueve líneas: la comprobación, el mensaje nuevo y una prueba con
  pytest que espera la excepción.
- **Paso 5.** La CI tarda cuatro minutos y falla la comprobación de estilo. La arreglas. El revisor
  pide cambiar `KeyError` por `ValueError`, porque `KeyError` forma parte de la API pública y hay
  gente capturando esa excepción. Aceptas, empujas a la misma rama, trece pruebas en verde y se
  fusiona.

Saldo: nueve líneas cambiadas, una prueba nueva y tu nombre en el historial del proyecto. La
discusión del `ValueError` vale más que el parche: has aprendido a mirar la compatibilidad antes de
tocar.

## Código

```python verificable
# Reproduccion minima del fallo, en seis lineas y sin el proyecto entero.
def total_por_columna(filas, columna):
    return sum(fila[columna] for fila in filas)

filas = [{"pais": "ES", "importe": 3}, {"pais": "PT", "importe": 5}]
print(f"suma de importe: {total_por_columna(filas, 'importe')}")

try:
    total_por_columna(filas, "moneda")
except KeyError as exc:
    print(f"falla con {type(exc).__name__}: {exc}")
```

```text
suma de importe: 8
falla con KeyError: 'moneda'
```

```python verificable
# El parche: comprobar antes y decir que columnas hay disponibles.
def total_por_columna(filas, columna):
    disponibles = sorted({clave for fila in filas for clave in fila})
    if columna not in disponibles:
        raise ValueError(f"columna '{columna}' no existe; disponibles: {disponibles}")
    return sum(fila[columna] for fila in filas)

filas = [{"pais": "ES", "importe": 3}, {"pais": "PT", "importe": 5}]
try:
    total_por_columna(filas, "moneda")
except ValueError as exc:
    print(f"ahora falla con ValueError: {exc}")
```

```text
ahora falla con ValueError: columna 'moneda' no existe; disponibles: ['importe', 'pais']
```

```text
El PR, en texto plano:

  Titulo: Mensaje claro cuando la columna no existe (cierra #412)

  Que cambia: total_por_columna comprueba la columna antes de sumar y el error
  lista las disponibles. Antes saltaba un KeyError sin contexto.

  Como lo he probado: pytest tests/test_totales.py  ->  13 passed
  Version: validador-datos 2.4.1, Python 3.12, Windows 11
```

## Errores típicos

- **Reformatear el fichero entero.** Tu editor aplica el formateador a todo el archivo y la PR sale
  de 900 líneas cuando el cambio real era de 6. El mantenedor no puede ver qué has tocado. Configura
  el editor para formatear solo lo que cambias.
- **Una PR con cinco cambios.** Cinco discusiones, cinco motivos para rechazarla y una fusión
  imposible. Una PR, una cosa; lo demás, en ramas separadas.
- **Abrir la PR antes de hablar.** Si toca la API pública, el comportamiento por defecto o añade una
  dependencia, primero un issue. Trabajar tres días para oír «esto no lo vamos a aceptar» se evita
  con un mensaje de cinco líneas.
- **No ejecutar las pruebas antes de empujar.** Una CI roja en la primera pasada gasta el tiempo del
  revisor en algo que veías tú en local. Pasa la suite y el linter del proyecto.
- **Desaparecer después de la revisión.** El mantenedor revisa gratis y tarda días. Contesta,
  agradece y, si no estás de acuerdo, argumenta con datos; si ya no puedes seguir, dilo. Abandonar
  una PR deja trabajo a medias en manos de otro ([[code-review]]).
- **Confundir contribuir con hacer marketing.** Meter tu enlace, tu curso o tu logo en el README de
  otro proyecto. Se detecta en seguida y te cierra la puerta.
- **Ignorar la licencia.** Copiar código de un proyecto con licencia copyleft a uno permisivo, o al
  revés, es un problema legal, no un detalle de estilo. Mira la licencia antes de reutilizar y cita
  la autoría.

## Comprueba que lo sabes

:::quiz
p: Tu cambio real son 6 líneas, pero tu formateador ha reescrito 900 líneas del fichero. ¿Qué haces antes de abrir la PR?
o: Deshacer el reformateo y dejar solo el cambio de 6 líneas
o: Abrirla igual y avisar en la descripción de que lo importante son 6 líneas
o: Abrirla igual, porque el código queda más limpio con el formato nuevo
o: Partirla en dos PRs: una con el formato y otra con el arreglo
a: 1
e: Un diff de 900 líneas hace imposible ver el cambio real y suele chocar con el estilo del proyecto, que el mantenedor no ha pedido cambiar. Avisar en la descripción no arregla el problema para quien revisa. Y una PR de solo formato en un proyecto ajeno es exactamente el cambio que nadie ha pedido.
:::

:::quiz
p: ¿Cuál de estos seis campos NO puede faltar en un informe de fallo reproducible?
o: La versión instalada, los pasos exactos y la traza mínima
o: La solución que propones para el fallo
o: El sistema operativo del mantenedor
o: El número de horas que llevas usando la librería
a: 1
e: Sin versión, pasos y traza, el mantenedor no puede reproducir el fallo y el informe se queda parado. Proponer una solución es bienvenido pero opcional, y el sistema operativo del mantenedor no lo conoces tú. Las horas de uso no aportan nada al diagnóstico.
:::

:::quiz
p: Es tu primera contribución a un proyecto que usas a diario. ¿Por dónde empiezas?
o: Por una errata o un párrafo confuso de la documentación, para recorrer el proceso completo
o: Por refactorizar el módulo que peor está escrito
o: Por pedir permiso para ser mantenedor
o: Por abrir una PR con la funcionalidad que a ti te falta
a: 1
e: Un parche de documentación no genera discusión, se acepta rápido y te obliga a pasar por fork, rama, PR y CI: aprendes el circuito sin arriesgar nada. Refactorizar o añadir funcionalidad en la primera visita es la forma más habitual de que te rechacen y no volver.
:::

:::practica
enunciado: Elige una librería que uses de verdad y prepara un PR a un proyecto abierto. Localiza un fallo reproducible en menos de 20 líneas, abre el issue con los seis campos, y manda el parche con su prueba y el linter en verde. Si no encuentras ningún fallo, contribuye con la prueba que falta de un caso límite.
pista: El fallo más fácil de reproducir no es un error de cálculo, es un mensaje de error inútil o un caso límite sin cubrir.
solucion: El orden que funciona: (1) lee CONTRIBUTING.md y ejecuta la suite de pruebas tal cual, para saber que tu entorno está bien antes de tocar nada; (2) busca en los issues abiertos y cerrados si el fallo ya está reportado; (3) escribe el caso mínimo en un fichero suelto, con la versión instalada, y comprueba que falla; (4) abre el issue con los seis campos y espera la respuesta antes de programar, sobre todo si el arreglo cambia un mensaje o una excepción que otros capturan; (5) crea la rama desde la rama principal actualizada, añade la prueba que falla, ejecútala y comprueba que falla por el motivo correcto, y solo entonces arregla; (6) pasa el linter y la suite completa; (7) abre la PR con un título que diga qué cambia y el número del issue, y responde a la revisión en el mismo hilo. Si el mantenedor tarda dos semanas, no es un rechazo: es una persona con un trabajo.
:::
