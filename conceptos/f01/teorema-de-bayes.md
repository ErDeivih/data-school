---
id: teorema-de-bayes
titulo: Teorema de Bayes
fase: 1
nivel: intermedio
rutas: [core, ds]
prerequisitos: [probabilidad-condicional, probabilidad-axiomas]
tags: [probabilidad, bayes, actualizacion, test]
resumen: Como dar la vuelta a una probabilidad condicional: la regla que convierte la tasa de acierto de un test en la probabilidad real de estar enfermo.
fuentes: ["Ross (2014), 'A First Course in Probability'", "Kahneman y Tversky (1973), 'On the Psychology of Prediction'"]
---

## En una frase

El teorema de Bayes permite invertir una probabilidad condicional: si conoces la probabilidad de
la evidencia dado cada escenario y lo probable que era cada escenario de antemano, puedes
calcular la probabilidad de cada escenario una vez vista la evidencia.

## La idea

Una prueba médica detecta el 90 % de los casos de una enfermedad y da falsos positivos en el 5 %
de las personas sanas. Te haces la prueba, sale positivo, y tanto tú como tu médico pensáis «un
90 %». La respuesta correcta, si la enfermedad afecta a 1 de cada 100 personas, es un **15 %**.

La razón es que el test no trabaja en el vacío: trabaja sobre una población donde la enfermedad
es rara. Con 10.000 personas, 100 están enfermas y 90 dan positivo; 9.900 están sanas y 495 dan
positivo por error. En total 585 positivos, de los cuales solo 90 son verdaderos: 90/585 = 15 %.
El denominador está lleno de sanos porque hay muchísimos más. Eso es el **sesgo de tasa base**, y
es la razón de que un test excelente pueda dar positivos poco informativos cuando la enfermedad
es rara. La buena noticia: repetir la prueba con un segundo test independiente cambia el
resultado de forma drástica, porque la probabilidad previa del segundo test ya es el 15 % del
primero.

Bayes es la formalización de «aprender de la evidencia»: empiezas con una creencia (la
**previa**), ves un dato, y actualizas (la **posterior**). Si el dato es mucho más probable bajo
una hipótesis que bajo la otra, la creencia se mueve mucho; si el dato es igual de probable en
las dos, la creencia no se mueve nada. Esa es toda la maquinaria, y está detrás de los filtros de
spam, de los clasificadores naive Bayes y de la estadística bayesiana entera.

## Definición formal

Sean `H` una hipótesis y `E` una evidencia, con `P(E) > 0`:

:::formula
P(H | E) = P(E | H) · P(H) / P(E)
:::

- `P(H)` — **probabilidad previa** (prior): lo creíble que era `H` antes de ver la evidencia.
- `P(E | H)` — **verosimilitud**: probabilidad de observar la evidencia si `H` es cierta.
- `P(H | E)` — **probabilidad posterior**: lo creíble que es `H` después de ver `E`.
- `P(E)` — probabilidad de la evidencia, que actúa como constante de normalización. Se calcula
  con la ley de la probabilidad total.

Con un conjunto de hipótesis `H₁, …, H_k` disjuntas que cubren todo el espacio (una partición),
la forma expandida es:

:::formula
P(Hᵢ | E) = P(E | Hᵢ) · P(Hᵢ) / Σⱼ P(E | Hⱼ) · P(Hⱼ)
:::

- El denominador suma sobre **todas** las hipótesis, no solo la que te interesa. Olvidar una
  rama del denominador es el error de cálculo más común.
- Los posteriores suman 1 sobre la partición, lo cual sirve de comprobación.

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `H` | La hipotesis que quieres evaluar (estar enfermo, ser spam) | ninguna | No es una magnitud que se mueva: es la opcion sobre la que calculas |
| `E` | La evidencia observada (el test positivo, la palabra rara) | ninguna | Cuanta mas evidencia, mas se separa el posterior de la previa |
| `P(H)` | Previa: lo creible que era `H` antes de mirar el dato | probabilidad, entre 0 y 1 | El posterior sube en la misma proporción; con previas muy pequenas hace falta mucha evidencia. Si vale 0 o 1, la evidencia no cambia nada |
| `P(E / H)` | Verosimilitud: probabilidad de ver el dato si `H` es cierta (la sensibilidad del test) | probabilidad, entre 0 y 1 | Sube el posterior y de forma fuerte: es el único termino del numerador. Cerca de 1 es un test que casi siempre acierta en los enfermos |
| `P(E / Hc)` | Probabilidad de la evidencia cuando `H` es falsa (la tasa de falsos positivos) | probabilidad, entre 0 y 1 | Baja el posterior, y manda cuando la previa es pequeña: el denominador se llena de sanos y el resultado se hunde |
| `P(E)` | Probabilidad total de la evidencia, sumando todas las hipotesis | probabilidad, entre 0 y 1 | Es el denominador: si sube por falsos positivos, el posterior baja. Tiene que ser mayor que 0 para poder dividir |
| `P(H / E)` | Posterior: lo creible que es `H` después de ver `E` | probabilidad, entre 0 y 1 | Es el resultado. Sobre una partición, los posteriores suman 1: eso sirve de comprobación |
| `P(E / H) / P(E / Hc)` | Razon de verosimilitud: cuanto inclina el test a favor de `H` | adimensional, mayor o igual que 0 | Multiplica las odds previas. Vale 1 cuando el test no informa; por debajo de 1, la evidencia va en contra de `H` |
| `odds(p) = p / (1 - p)` | La razón entre que ocurra y que no | adimensional, mayor o igual que 0 | Conversión que hace la actualización una multiplicación en vez de una división. Pasa de 0 a infinito mientras `p` va de 0 a 1 |
:::

**Forma de odds** (la más útil para razonar sin calculadora):

:::formula
odds(P(H | E)) = [P(E | H) / P(E | Hᶜ)] · odds(P(H))
:::

- `odds(p) = p / (1 − p)` — la razón entre la probabilidad de que ocurra y la de que no.
- El cociente `P(E | H) / P(E | Hᶜ)` se llama **razón de verosimilitud** y es una propiedad del
  test, no de la población.
- Esta forma enseña lo importante: la evidencia multiplica las odds previas por un factor. Un
  test con razón de verosimilitud 18 multiplica por 18 las odds de estar enfermo, sean cuales
  sean.

:::figura
fichero: bayes-positivos-y-repeticion
pie: A la izquierda, los 585 positivos que salen de 10.000 personas: la barra roja (495 sanos mal clasificados) es cinco veces la azul (90 enfermos), y por eso el posterior es 15,4 % y no 90 %. A la derecha, el mismo test repetido con resultados independientes: la previa del 1 % tarda tres positivos en superar el 90 %, que es lo que cuesta mover una creencia muy baja.
fuente: figuras/teorema-de-bayes-1.py
:::

## Ejemplo

Enfermedad con prevalencia `P(H) = 0,01`. Test con sensibilidad `P(+ | H) = 0,90` (detecta el
90 % de los enfermos) y especificidad `P(− | Hᶜ) = 0,95` (el 95 % de los sanos da negativo, luego
`P(+ | Hᶜ) = 0,05`).

- **Denominador** (probabilidad total de dar positivo):
  `P(+) = P(+ | H)·P(H) + P(+ | Hᶜ)·P(Hᶜ) = 0,90 · 0,01 + 0,05 · 0,99 = 0,009 + 0,0495 = 0,0585`.
- **Posterior:** `P(H | +) = 0,009 / 0,0585 = 0,1538`. Un 15,4 %, no un 90 %.
- **Comprobación por odds:** odds previas `0,01/0,99 = 0,0101`; razón de verosimilitud
  `0,90/0,05 = 18`; odds posteriores `0,0101 · 18 = 0,1818`, que corresponden a
  `0,1818/(1 + 0,1818) = 0,1538`. Coincide.
- **¿Y si el test sale negativo?** `P(H | −) = P(− | H)·P(H) / P(−)` con
  `P(−) = 0,10·0,01 + 0,95·0,99 = 0,001 + 0,9405 = 0,9415`, luego
  `P(H | −) = 0,001/0,9415 = 0,0011`. La previa era 0,01 y baja a 0,0011: un factor 9 de
  reducción.

La lección cuantitativa: la evidencia mueve mucho las odds (×18), pero **una previa muy pequeña
aguanta mucho castigo**. Para llegar a una posterior alta con una enfermedad rara hacen falta
varios tests independientes.

## Código

```python verificable
# Test medico: de la tasa de acierto a la probabilidad real de estar enfermo.
prevalencia = 0.01          # P(enfermo)
sensibilidad = 0.90         # P(positivo | enfermo)
especificidad = 0.95        # P(negativo | sano)

p_positivo = sensibilidad * prevalencia + (1 - especificidad) * (1 - prevalencia)
posterior = sensibilidad * prevalencia / p_positivo

print("P(positivo)          ", round(p_positivo, 4))    # salida: 0.0585
print("P(enfermo | positivo)", round(posterior, 4))     # salida: 0.1538
print("falsos positivos     ", round((1 - especificidad) * (1 - prevalencia), 4))  # salida: 0.0495
print("verdaderos positivos ", round(sensibilidad * prevalencia, 4))               # salida: 0.009
```
:::claves
- El primer bloque no usa ninguna libreria: son cuentas con `float`. Eso significa que `0.90 * 0.01` no da exactamente `0.009`, sino un número a un pelo de distancia. Nunca compares resultados así con `==`: usa `abs(a - b) < 1e-9` o redondea al imprimir. Es el mismo motivo por el que la página avisa de que redondear a mitad de calculo ensucia el resultado.
- `round(x, 4)` devuelve otro `float`, no un texto: sirve para leer, no para comparar. Y ojo, no es lo mismo que el formato `f"{x:.4f}"`, que si devuelve una cadena y rellena con ceros.
- El segundo bloque reutiliza la variable `p` como acumulador: en cada vuelta el posterior de hoy pasa a ser la previa de mañana. Si en vez de eso escribieras `p = sensibilidad * prevalencia / (...)`, estarias usando siempre la previa original y los cuatro tests darian el mismo 0,1538.
- `range(1, 5)` genera 1, 2, 3 y 4: el extremo final nunca entra. Es el motivo de que el bucle imprima cuatro líneas y no cinco, y la trampa clasica al pasarlo a `range(1, len(tests))`.
- `sensibilidad, especificidad = 0.90, 0.95` es desempaquetado de una tupla, no dos asignaciones magicas. Si pones tres valores a la izquierda y dos a la derecha, Python lanza `ValueError` en la misma línea.
- En la formula se usa `(1 - especificidad)` en lugar de un número escrito a mano. Es a proposito: la especificidad es `P(negativo / sano)`, así que la tasa de falsos positivos es su complementario. Tocar solo la especificidad en una línea y olvidarse de la otra rama es el error que hace que los dos posteriores dejen de sumar 1.
:::


```python verificable
# Cuántos tests independientes hacen falta para pasar de una previa del 1 % a más del 90 %.
prevalencia = 0.01
sensibilidad, especificidad = 0.90, 0.95

p = prevalencia
for test in range(1, 5):
    p = sensibilidad * p / (sensibilidad * p + (1 - especificidad) * (1 - p))
    print("tras", test, "test(s) positivos:", round(p, 4))

# salida:
# tras 1 test(s) positivos: 0.1538
# tras 2 test(s) positivos: 0.766
# tras 3 test(s) positivos: 0.9833
# tras 4 test(s) positivos: 0.9991
```

## Errores típicos

- **Ignorar la tasa base.** Es el error estrella: interpretar `P(+ | H)` como si fuera
  `P(H | +)`. Con enfermedades raras, la diferencia es de 90 % a 15 %. Antes de calcular, estima
  cuántas personas sanas producen falsos positivos: casi siempre son más que los enfermos.
- **Olvidar ramas en el denominador.** El denominador es la probabilidad total de la evidencia e
  incluye a **todas** las hipótesis. Si solo sumas la rama de la hipótesis que te interesa, el
  resultado es siempre 1 (o mayor).
- **Confundir sensibilidad con especificidad.** La sensibilidad es `P(+ | enfermo)`; la
  especificidad es `P(− | sano)`. Intercambiarlas cambia el resultado de forma brutal cuando la
  prevalencia es baja, y es un error de lectura muy fácil de cometer con la terminología médica.
- **Creer que se puede actualizar sin una previa.** Bayes necesita un punto de partida. Si no
  tienes datos para fijarla, usa una previa débil y comprueba cuánto influye en el resultado; si
  influye mucho, tu conclusión depende de un supuesto, no de los datos.
- **Tratar tests repetidos como independientes cuando no lo son.** Repetir el mismo test el mismo
  día comparte el mismo error sistemático: sus errores están correlacionados y la actualización
  es mucho menor que la que predice el cálculo. Solo tests genuinamente independientes se
  multiplican.
- **Redondear en medio del cálculo.** Con prevalencias pequeñas, redondear el denominador
  `0,009 + 0,0495 = 0,0585` a `0,06` y dejar el numerador en `0,009` da un posterior de
  `0,009 / 0,06 = 0,15` en vez de 0,1538; si redondeas también el numerador a `0,01`, sale
  0,1667. Parece poco, pero si encadenas varios pasos el error crece. Trabaja con precisión
  completa y redondea al imprimir.

:::practica
enunciado: Un filtro marca como spam el 96 % del correo basura y también el 3 % del correo legitimo. Si el 20 % del correo que llega es basura, calcula la probabilidad de que un mensaje marcado sea realmente spam.
pista: El denominador es la probabilidad total de ser marcado: suma la rama del spam y la del correo legitimo.
solucion: P(marcado) = 0,96 · 0,20 + 0,03 · 0,80 = 0,192 + 0,024 = 0,216. P(spam | marcado) = 0,192 / 0,216 = 0,8889, un 88,9 %. La tasa base importa: de cada 1.000 mensajes, 192 spam y 24 legitimos quedan marcados.
:::

## Comprueba que lo sabes

:::quiz
p: Una enfermedad afecta al 1 % de la población. El test detecta el 90 % de los enfermos y da falso positivo en el 5 % de los sanos. Si das positivo, ¿cuál es la probabilidad de estar enfermo?
o: Un 90 %
o: Un 15,4 %
o: Un 50 %
a: 2
e: P(positivo) = 0,90·0,01 + 0,05·0,99 = 0,0585 y P(enfermo y positivo) = 0,009, luego el posterior es 0,009/0,0585 = 0,1538. El 90 % es la sensibilidad, que es la probabilidad de dar positivo estando enfermo, justo la dirección contraria.
:::

:::quiz
p: ¿Qué papel juega P(E) en el teorema de Bayes?
o: Es la constante que normaliza el resultado y se calcula sumando la evidencia bajo todas las hipótesis
o: Es la probabilidad previa de la hipótesis
o: Es la verosimilitud del modelo
a: 1
e: P(E) es la probabilidad total de observar la evidencia, y se obtiene sumando P(E | H_j)·P(H_j) sobre todas las hipótesis de la partición. La previa es P(H) y la verosimilitud es P(E | H); confundir los tres papeles es el origen de casi todos los errores de cálculo.
:::

:::quiz
p: Con previa del 1 %, sensibilidad 0,90 y especificidad 0,95, ¿qué pasa si el test sale negativo?
o: La probabilidad de estar enfermo baja de 0,01 a aproximadamente 0,001
o: Se descarta por completo la enfermedad, la probabilidad es 0
o: La probabilidad sube, porque un negativo también es información
a: 1
e: P(enfermo y negativo) = 0,10·0,01 = 0,001 y P(negativo) = 0,9415, así que el posterior es 0,0011. Baja unas nueve veces, pero no llega a cero: un test nunca demuestra la ausencia absoluta si tiene falsos negativos.
:::

:::trampa
El error del fiscal es el mismo error con otro traje: «la probabilidad de que una huella
coincida por azar es 1 entre un millón, luego la probabilidad de que el acusado sea inocente es
1 entre un millón». Falta la previa: cuántas personas pudieron dejar esa huella. Con muchos
candidatos, una coincidencia casual deja de ser improbable. Siempre hay que preguntar por el
denominador.
:::
