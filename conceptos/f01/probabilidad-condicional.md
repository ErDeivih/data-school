---
id: probabilidad-condicional
titulo: Probabilidad condicional
fase: 1
nivel: básico
rutas: [core, ds]
prerequisitos: [probabilidad-axiomas]
tags: [probabilidad, condicionamiento, tablas]
resumen: La probabilidad de A sabiendo que B ha ocurrido: reduce el espacio muestral al suceso conocido y reescala, y por eso cambia cualquier conclusión.
fuentes: ["Ross (2014), 'A First Course in Probability'"]
---

## En una frase

La probabilidad condicional de `A` dado `B` es la probabilidad de que ocurran los dos, dividida
entre la probabilidad de `B`: al saber que `B` ha pasado, el mundo posible se reduce a `B` y hay
que repartir toda la probabilidad dentro de ese trozo.

## La idea

Te dicen que una familia tiene dos hijos y que **al menos uno es niño**. ¿Cuál es la probabilidad
de que los dos sean niños? La respuesta ingenua es 1/2 («el otro hijo será niño o niña»). La
correcta es 1/3, y la diferencia lo explica todo el concepto. Sin información, los cuatro casos
equiprobables son (niño, niño), (niño, niña), (niña, niño) y (niña, niña). Saber que «al menos
uno es niño» descarta solo (niña, niña) y deja tres casos, de los cuales únicamente uno tiene dos
niños. Has cambiado el espacio muestral: ya no son 4 casos, son 3.

Eso es condicionar: **no cambias los datos, cambias el conjunto de referencia**. Es la razón de
que en un filtro de spam, en un test médico o en un modelo de riesgo la probabilidad cambie de
forma radical al incorporar información. Y es también el motivo de que la «tasa de acierto» de
un test no responda a la pregunta que le haces al médico: él quiere saber la probabilidad de
estar enfermo sabiendo que el test es positivo, no la de dar positivo sabiendo que estás
enfermo. Son dos números distintos, y confundirlos tiene consecuencias reales.

Otro detalle que se pasa por alto: **el condicionamiento corta el espacio, no reordena**. Si `B`
tiene probabilidad pequeña, condicionar a `B` puede hacer que un suceso raro pase a ser muy
probable, porque el denominador se encoge. Toda la maquinaria bayesiana nace de ahí.

## Definición formal

Dados dos sucesos `A` y `B` con `P(B) > 0`, la **probabilidad condicional de `A` dado `B`** es:

:::formula
P(A | B) = P(A ∩ B) / P(B)
:::

- `P(A | B)` — probabilidad de `A` **sabiendo** que ha ocurrido `B`; la barra vertical se lee
  «dado» o «sabiendo que».
- `A ∩ B` — el suceso «ocurren `A` y `B` a la vez», la parte de `A` que cae dentro de `B`.
- `P(B)` — el denominador; debe ser estrictamente mayor que cero. Condicionar a un suceso
  imposible no está definido.

:::figura
fichero: condicional-encoge-el-espacio
pie: El primer panel tiene los 6 casos del dado y el segundo los separa en conjuntos: `A` está dentro de `B`, pero solo ocupa un tercio. El panel de abajo a la izquierda es el paso que se olvida: al saber que ha salido par, los 6 casos se reducen a 3, y hay que repartir toda la probabilidad entre esos 3 hasta que vuelvan a sumar 1. El último panel es el mismo mecanismo con un test médico, donde la probabilidad se da la vuelta: 0,99 y 0,167 no son el mismo número leído de dos formas.
fuente: figuras/probabilidad-condicional-1.py
:::

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| La probabilidad de `A` sabiendo `B` | Condicional: la parte de `A` que cae dentro de `B`, reescalada | adimensional, entre 0 y 1 | Sube si crece la parte de `A` que cae dentro de `B`, o si `P(B)` se hace mas pequeña |
| `A ∩ B` | Los dos sucesos a la vez | subconjunto de `Ω` | Es el numerador del cociente: nunca puede superar a `P(B)` |
| `P(B)` | Probabilidad del suceso que ya sabes cierto | adimensional, entre 0 y 1 | Es el denominador: cuanto mas raro es `B`, mas se agranda todo lo condicionado a el |
| `P(A)` | Probabilidad de `A` sin información | adimensional, entre 0 y 1 | Es la referencia: condicionar la sube, la baja o la deja igual, pero no la «corrige» |
| P(B dado A) | La condición leida al reves | adimensional, entre 0 y 1 | No tiene por qué parecerse a la de arriba; solo coinciden si los dos sucesos son independientes |
| La tasa de A dentro del grupo i | Tasa dentro del grupo `i` de la partición | adimensional, entre 0 y 1 | En la probabilidad total cada tasa pesa por el tamaño del grupo, no por su valor |
| `P(Bᵢ)` | Peso del grupo `i` en la partición | adimensional, suman 1 | Si un grupo pesa mas, su tasa manda mas en el promedio; los pesos deben sumar 1 sin huecos |
:::

De la definición salen tres fórmulas que se usan continuamente:

- **Regla del producto:** `P(A ∩ B) = P(A | B) · P(B) = P(B | A) · P(A)`. Las dos formas son
  válidas; se elige la que tenga los números más fáciles.
- **Ley de la probabilidad total.** Si `B₁, B₂, …, B_k` son disjuntos y su unión es todo el
  espacio muestral (una **partición**), entonces
  `P(A) = Σᵢ P(A | Bᵢ) · P(Bᵢ)`. Es la herramienta para promediar casos.
- **Regla de Bayes:** `P(B | A) = P(A | B) · P(B) / P(A)`. Es la regla del producto leída al
  revés, y tiene su propia página: [[teorema-de-bayes|el teorema de Bayes]].

Un aviso importante: **el condicionamiento no es una operación simétrica**. `P(A | B)` y
`P(B | A)` son números distintos salvo casualidad. La probabilidad de ser millonario sabiendo
que juegas a la lotería no es la probabilidad de jugar a la lotería sabiendo que eres millonario.

## Ejemplo

Tiramos un dado de seis caras. Sea `A` = «sale un 6» y `B` = «sale par».

- `P(A) = 1/6 ≈ 0,1667`.
- `P(B) = 3/6 = 0,5`.
- `P(A ∩ B) = 1/6 ≈ 0,1667` (el 6 es par, así que la intersección es el propio `A`).
- `P(A | B) = (1/6) / (1/2) = 1/3 ≈ 0,3333`: sabiendo que ha salido par, la probabilidad de que
  sea 6 se **duplica**. Condicionar ha eliminado tres de los seis casos posibles.

Ahora, un ejemplo de probabilidad total. Una fábrica tiene dos máquinas: la M1 produce el 70 %
de las piezas y la M2 el 30 % restante. La M1 genera un 2 % de piezas defectuosas y la M2 un
5 %. ¿Cuál es la probabilidad de que una pieza al azar sea defectuosa?

- `P(M1) = 0,70`, `P(M2) = 0,30`.
- `P(D | M1) = 0,02`, `P(D | M2) = 0,05`.
- `P(D) = 0,70 · 0,02 + 0,30 · 0,05 = 0,014 + 0,015 = 0,029`, es decir un 2,9 %.

Fíjate en que la máquina **menos** fiable (M2) aporta más defectos que la más fiable casi en
proporción a su volumen: 0,015 frente a 0,014. Sumar los dos porcentajes de defectos (7 %) o
promediarlos (3,5 %) son los dos errores clásicos aquí.

## Código

```python verificable
# Dado y moneda simulados sobre una rejilla determinista: 6 caras x 2 lados x 10 repeticiones.
caras = [1, 2, 3, 4, 5, 6] * 20                      # cada cara aparece 20 veces
lados = ["cara", "cruz"] * 60                        # 60 caras y 60 cruces
n = len(caras)
assert n == len(lados) == 120

seis = [c == 6 for c in caras]
pares = [c % 2 == 0 for c in caras]

p_seis = sum(seis) / n
p_par = sum(pares) / n
p_seis_y_par = sum(s and p for s, p in zip(seis, pares)) / n

print("P(seis)          ", round(p_seis, 4))                        # salida: 0.1667
print("P(par)           ", round(p_par, 4))                         # salida: 0.5
print("P(seis y par)    ", round(p_seis_y_par, 4))                  # salida: 0.1667
print("P(seis sabiendo par)", round(p_seis_y_par / p_par, 4))       # salida: 0.3333
```

:::claves
- `lados = ["cara", "cruz"] * 60` construye una lista de 120 elementos, pero **no se usa para nada** en el calculo: solo existe para el `assert` de la longitud. La probabilidad se calcula solo con las caras del dado, así que ese dato es decorativo y el resultado no cambia si lo borras.
- La condicional se calcula como el cociente de dos proporciones: `p_seis_y_par / p_par`. Al dividir numerador y denominador entre `n`, sale el mismo número que contando casos directamente: `sum(s and p for s, p in zip(seis, pares)) / sum(pares)` da también 0,3333, y no es casualidad, es la misma cuenta escrita de otra forma. Lo que ese cociente **no** es, en ningún caso, es una media.
- `seis` y `pares` son listas de `bool`, no de números. `s and p` funciona porque Python los trata como 0 y 1, y `sum(...)` de una lista de booleanos cuenta los `True`. En Python `bool` es una subclase de `int`: `True + True` vale 2 y `True * True` vale 1, los dos enteros. (En un array de NumPy, en cambio, el producto de dos booleanos sigue siendo booleano.)
- `caras = [1, 2, 3, 4, 5, 6] * 20` no es una multiplicación: es repetir la lista 20 veces. El total son 120 elementos y el dado sale perfectamente equilibrado. Si en vez de repetir generaras números al azar, el cociente saldria cerca de 0,3333 pero no exacto.
- `assert n == len(lados) == 120` es una comprobación encadenada: en Python significa `n == len(lados) and len(lados) == 120`. Se salta si ejecutas el fichero con `python -O`, así que no sirve como validación de producción.
- La diferencia entre `p_seis` (0,1667) y la condicional (0,3333) es exactamente el efecto de condicionar: el numerador no cambia, lo que cambia es el denominador. Si divides solo entre los casos de `B` en vez de entre los 120, sale el doble.
:::

```python verificable
# Ley de la probabilidad total con las dos máquinas de la fábrica.
p_m1, p_m2 = 0.70, 0.30
p_def_m1, p_def_m2 = 0.02, 0.05

p_defectuosa = p_m1 * p_def_m1 + p_m2 * p_def_m2
aporte_m1 = p_m1 * p_def_m1
aporte_m2 = p_m2 * p_def_m2

print("P(defectuosa)      ", round(p_defectuosa, 4))       # salida: 0.029
print("aporta la maquina 1", round(aporte_m1, 4))          # salida: 0.014
print("aporta la maquina 2", round(aporte_m2, 4))          # salida: 0.015
print("promedio ingenuo   ", round((p_def_m1 + p_def_m2) / 2, 4))  # salida: 0.035
```

## Errores típicos

- **Intercambiar `P(A | B)` con `P(B | A)`.** La probabilidad de tener fiebre sabiendo que hay
  gripe es altísima; la de tener gripe sabiendo que hay fiebre, mucho menor. Se confunden porque
  el lenguaje natural no distingue el orden, y es la fuente de la mayoría de los titulares
  médicos malos.
- **Condicionar sin comprobar que `P(B) > 0`.** Dividir entre cero no es un detalle técnico: si
  el suceso condicionante es imposible, la probabilidad condicional no está definida y cualquier
  número que salga es inventado.
- **Aplicar la ley de la probabilidad total sin una partición de verdad.** Los casos por los que
  promedias no pueden solaparse ni dejar huecos. Con dos categorías que se solapan, la suma pesa
  dos veces ese trozo.
- **Creer que condicionar «corrige» o «actualiza» sin más.** Condicionar **cambia** la
  probabilidad, en cualquier dirección. Puede subirla, bajarla o dejarla igual (esto último
  ocurre exactamente cuando los sucesos son independientes).
- **Confundir `P(A ∩ B)` con `P(A | B)`.** La primera es una probabilidad conjunta sobre todo el
  espacio; la segunda es un cociente dentro de `B`. Siempre `P(A ∩ B) ≤ P(A | B)` cuando
  `P(B) ≤ 1`, así que un resultado de intersección mayor que la condicional indica un error.
- **Olvidar que la probabilidad total puede calcularse por el suceso complementario.**
  `P(A) = 1 − P(Aᶜ)` y, condicionando, `P(A) = P(A | B)·P(B) + P(A | Bᶜ)·P(Bᶜ)`. Es la versión
  con dos ramas que resuelve la mitad de los problemas sin escribir una partición larga.

:::practica
enunciado: Un ayuntamiento revisa 400 expedientes. El 65 % los tramita la oficina A y el 35 % la oficina B. La A comete un error en el 4 % de sus expedientes y la B en el 10 %. Calcula la probabilidad de que un expediente tenga error.
pista: Es una partición: pondera cada tasa de error por el peso de su oficina.
solucion: P(error) = 0,65 · 0,04 + 0,35 · 0,10 = 0,026 + 0,035 = 0,061, un 6,1 %: unos 24 expedientes con error. La oficina B, con menos carga, aporta mas errores (0,035 frente a 0,026). Promediar las dos tasas (0,07) o sumarlas sería incorrecto.
:::

## Comprueba que lo sabes

:::quiz
p: Se lanza un dado. Sabiendo que ha salido par, ¿cuál es la probabilidad de que sea un 6?
o: 1/6
o: 1/3
o: 1/2
a: 2
e: P(par) = 1/2 y P(6 y par) = 1/6, así que P(6 sabiendo par) = (1/6)/(1/2) = 1/3. La probabilidad sube de 1/6 a 1/3 porque el espacio posible se ha reducido de seis casos a tres.
:::

:::quiz
p: Una prueba detecta el 99 % de las enfermedades cuando existen. ¿Significa eso que un resultado positivo implica casi con seguridad estar enfermo?
o: Sí, un 99 % de probabilidad de enfermedad
o: No: eso es la probabilidad de dar positivo estando enfermo, no la de estar enfermo dando positivo
o: Depende solo del número de pruebas realizadas
a: 2
e: Confundes P(positivo sabiendo enfermo) con P(enfermo sabiendo positivo). La segunda depende también de la prevalencia de la enfermedad: si es rara, la mayoría de los positivos son falsos positivos. Cuantificarlo es exactamente el teorema de Bayes.
:::

:::quiz
p: En la fábrica del ejemplo, la M1 produce el 70 % de las piezas con un 2 % de defectos y la M2 el 30 % con un 5 %. Se elige una pieza y resulta defectuosa. ¿De qué máquina es más probable que venga?
o: De la M1, porque produce más piezas
o: De la M2, porque su tasa de defectos es mayor y su aporte de defectos también (0,015 frente a 0,014)
o: Es igual de probable en las dos
a: 2
e: Comparando los aportes a la probabilidad total: la M2 aporta 0,015 y la M1 0,014, así que dado que la pieza es defectuosa es algo más probable que venga de la M2, aunque produzca menos. Concretamente P(M2 sabiendo defectuosa) = 0,015/0,029 = 0,517.
:::

:::trampa
La probabilidad condicional no es conmutativa y el lenguaje no lo perdona: «el 90 % de los
accidentes los provocan conductores sobrios» y «el 90 % de los conductores sobrios provocan
accidentes» son frases con las mismas palabras y significados opuestos. Escribe siempre la
condición explícitamente con «sabiendo que».
:::
