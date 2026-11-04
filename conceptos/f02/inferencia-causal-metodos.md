---
id: inferencia-causal-metodos
titulo: Métodos de inferencia causal
fase: 2
nivel: experto
rutas: [ds, core]
prerequisitos: [causalidad-vs-correlacion, confusores-y-dag, estimadores-y-propiedades]
tags: [causalidad, cuasi-experimento, identificacion]
resumen: Cuatro diseños para estimar efectos causales cuando no puedes aleatorizar, cada uno con su supuesto de identificación y su forma característica de fallar.
fuentes: ["Angrist y Pischke (2009), 'Mostly Harmless Econometrics'", "Rubin (1974), 'Estimating Causal Effects of Treatments in Randomized and Nonrandomized Studies'", "Imbens y Lemieux (2008), 'Regression Discontinuity Designs: A Guide to Practice'"]
---

## En una frase

Cuando no puedes asignar el tratamiento al azar, estimar un efecto causal exige encontrar una
fuente de variación en el tratamiento que sea «casi aleatoria» —un instrumento, un cambio paralelo
en el tiempo, un corte en una variable continua o un grupo de comparación con las mismas
probabilidades— y cada uno de esos diseños compra credibilidad a cambio de un supuesto que hay que
defender con datos.

## La idea

El problema central se ve en una frase: solo puedes observar a cada persona en uno de los dos
mundos. Si Ana tomó el fármaco, sabes cuánto mejoró **con** el fármaco; nunca sabrás cuánto habría
mejorado sin él. Ese contrafactual es la mitad de la información que necesitas, y no existe. Esto
se llama problema fundamental de la inferencia causal, y todo lo demás en esta página son estrategias
para reconstruir esa mitad que falta.

La solución de referencia es el experimento aleatorizado. Si sorteas quién recibe el tratamiento,
los dos grupos son comparables en todo (edad, gravedad, motivación, lo que no has medido), porque el
sorteo no mira esas cosas. La diferencia de medias entre los grupos es entonces el efecto causal, sin
supuestos adicionales aparte de que el sorteo se hizo bien. Los cuatro métodos de esta página
existen porque aleatorizar es a menudo imposible: nadie va a sortear quién fuma, quién estudia
medicina o a qué colegio va un niño.

La idea común a los cuatro es la misma: buscar un pedazo de variación en el tratamiento que no esté
correlacionado con nada más. Se cambia «aleatorizar el tratamiento» por «encontrar un experimento
natural», y el precio es que cada diseño trae un supuesto que no se puede verificar con los datos y
que hay que argumentar con conocimiento del dominio.

1. **Variables instrumentales (IV).** Hay una variable `Z` que empuja el tratamiento sin afectar al
   resultado por otra vía. Ejemplo: una lotería de admisión a un programa de formación. La lotería
   cambia la probabilidad de asistir al curso (primera etapa) y, si solo influye en el salario a
   través del curso, el cociente entre su efecto en el salario y su efecto en la asistencia estima el
   efecto del curso para quien cambia de decisión por la lotería.
2. **Diferencias en diferencias (DiD).** Hay dos grupos y dos periodos. En lugar de comparar niveles
   (que difieren por mil razones), se comparan **cambios**: cuánto mejoró el grupo tratado menos
   cuánto mejoró el control. Funciona si, sin tratamiento, los dos grupos habrían evolucionado en
   paralelo. Ejemplo clásico: subir el salario mínimo en un estado y no en el vecino, comparando el
   empleo antes y después en cada uno.
3. **Propensity score.** Con muchas covariables observadas, comparar a tratados y controles similares
   en una sola dimensión: la probabilidad estimada de recibir el tratamiento. Si dos personas tienen
   la misma propensión de 0,4 y una fue tratada, la otra es un buen contrafactual suyo. Exige que
   todas las variables relevantes estén medidas, que es exactamente lo que no puedes comprobar.
4. **Regresión discontinua (RDD).** Hay una regla con umbral: una beca si la nota supera 7,0, un
   tratamiento si el marcador supera 200. Justo alrededor del corte, los de 6,99 y los de 7,01 son
   casi idénticos, así que la diferencia en el resultado es atribuible a la regla. Solo funciona si
   los individuos no pueden manipular con precisión su posición respecto al corte.

Lo que distingue a un analista competente no es saber estas cuatro etiquetas, sino saber decir en
qué supuesto se apoya cada una y qué evidencia enseña de que se sostiene. Sin ese paso, has cambiado
una regresión por otra con nombre más elegante.

:::figura
fichero: did-y-discontinuidad
pie: Los dos diseños compran credibilidad a un supuesto que hay que enseñar. A la izquierda, el efecto es la brecha que queda entre lo que pasó y la prolongación paralela del control: si las tendencias ya divergían antes, esa brecha no es el efecto. A la derecha, la nube es continua salvo en el 7,00, y ese salto solo es atribuible a la beca si nadie puede colocarse justo por encima del corte.
fuente: figuras/inferencia-causal-metodos-1.py
:::

## Definición formal

Para cada unidad `i` se definen dos resultados potenciales: `Yᵢ(1)` el resultado si recibe el
tratamiento y `Yᵢ(0)` el resultado si no lo recibe.

- `Tᵢ ∈ {0, 1}` — indicador de tratamiento recibido.
- `Yᵢ = Tᵢ·Yᵢ(1) + (1 − Tᵢ)·Yᵢ(0)` — lo único observable: uno de los dos mundos.
- `τᵢ = Yᵢ(1) − Yᵢ(0)` — efecto causal individual. Nunca se observa.
- `ATE = E[τᵢ]` — efecto medio en la población.
- `ATT = E[τᵢ | Tᵢ = 1]` — efecto medio en los tratados, el que suele interesar en política pública.
- `X` — covariables observadas; `Z` — instrumento; `e(X) = P(T = 1 | X)` — propensity score.
- `Cov(·, ·)` — covarianza entre dos variables: cuánto se mueven juntas
  ([[covarianza-y-correlacion]]).

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `Tᵢ` | Si la unidad `i` recibió el tratamiento | 0 o 1 | Si el tratamiento se concentra en quien ya iba a mejorar, el sesgo de selección crece y la comparación cruda se aleja del ATE |
| `Yᵢ(1)`, `Yᵢ(0)` | Los dos resultados potenciales de la misma unidad; solo se observa uno | las del resultado | Su diferencia es el efecto individual, que nunca se mide; lo que se promedia son diferencias entre unidades |
| `τᵢ` | Efecto causal de la unidad `i`: `Yᵢ(1) − Yᵢ(0)` | las del resultado | Es la cantidad de interés y no se puede calcular fila a fila: cualquier estimador es un promedio de efectos que no se ven |
| `ATE` | Media de `τᵢ` en toda la población | las del resultado | Con efectos heterogéneos, un ATE grande puede esconder grupos donde el efecto es cero o negativo |
| `ATT` | Media de `τᵢ` entre los tratados | las del resultado | La distancia entre ATT y ATE **es** el sesgo de selección: con aleatorización ambos coinciden |
| `Z` | Instrumento: variable que mueve `T` y no toca `Y` por otra vía | las de `Z` | Cuanto más débil es su efecto sobre `T`, más se dispara el cociente de Wald y más se amplifica cualquier correlación mínima con el error |
| `e(X)` | Propensity score: probabilidad estimada de ser tratado dadas las covariables | entre 0 y 1 | Pegado a 0 o a 1 hay poco solapamiento y no existe contrafactual comparable: hay que recortar a la región de soporte común |
| `Cov(Z, Y) / Cov(Z, T)` | LATE: forma reducida partida por la primera etapa | las del resultado | Si la primera etapa se acerca a 0 el cociente explota, y no estima el ATE sino el efecto en los cumplidores |
| `(Ȳ_trat,después − Ȳ_trat,antes) − (Ȳ_ctrl,después − Ȳ_ctrl,antes)` | DiD: el cambio del grupo tratado menos el del control | las del resultado | Restar los cambios descuenta lo que ambos grupos tenían en común; solo vale si sin programa las tendencias habrían sido paralelas |
:::

La comparación ingenua es igual al efecto causal en los tratados (`ATT`) **más** un sesgo de
selección:

:::formula
E[Y | T = 1] − E[Y | T = 0] = ATT + ( E[Y(0) | T = 1] − E[Y(0) | T = 0] )
:::

El paréntesis es el sesgo: cómo habrían sido los tratados sin tratamiento. Con efectos homogéneos
`ATT = ATE` y la resta apunta directamente al efecto medio; con efectos heterogéneos, lo que la
comparación cruda contiene es el efecto en los tratados. Todo el trabajo econométrico consiste en
hacer cero ese paréntesis o en acotarlo.

**Identificación por ignorabilidad** (lo que compra el experimento, o el propensity score):

:::formula
( Y(0), Y(1) ) ⊥ T | X        y        0 < e(X) < 1    (solapamiento)
:::

Con eso, `ATE = E[ E[Y | X, T=1] − E[Y | X, T=0] ]`. El solapamiento es tan importante como la
independencia: si ningún control tiene `X` parecido a un tratado, no hay contrafactual que estimar.

**Diferencias en diferencias**, con grupos `trat` y `ctrl` y periodos `antes` y `después`. El
supuesto es de tendencias paralelas: sin tratamiento, `E[Y(0)_después − Y(0)_antes]` es igual en
los dos grupos. Entonces:

:::formula
DiD = ( Ȳ_trat,después − Ȳ_trat,antes ) − ( Ȳ_ctrl,después − Ȳ_ctrl,antes )
:::

**Variables instrumentales.** El estimador de Wald es el cociente entre la forma reducida (efecto de
`Z` sobre `Y`) y la primera etapa (efecto de `Z` sobre `T`), y estima un efecto local:

:::formula
LATE = Cov(Z, Y) / Cov(Z, T) = forma reducida / primera etapa
:::

Sus tres supuestos: **relevancia** (`Cov(Z, T) ≠ 0`, comprobable con la primera etapa),
**exclusión** (`Z` no afecta a `Y` salvo a través de `T`, no comprobable) e **independencia** (`Z` es
como si se hubiera asignado al azar). Con **monotonicidad** (nadie hace lo contrario de lo que
indica `Z`) el estimando es el efecto en los cumplidores: quienes cambian de tratamiento por el
instrumento. No es el ATE.

**Regresión discontinua** con variable de corte `W` (nota, edad, marcador) y umbral `c`, de modo que
`T = 1` si `W ≥ c`:

:::formula
RDD = lím_{w→c⁺} E[Y | W = w] − lím_{w→c⁻} E[Y | W = w]
:::

El supuesto es que `E[Y(0) | W = w]` y `E[Y(1) | W = w]` son continuas en `w = c`: nadie salta en el
corte salvo por el tratamiento. Cualquier discontinuidad en otra variable (edad, renta, esfuerzo)
en el mismo punto rompe el diseño.

## Ejemplo

**Diferencias en diferencias.** Un programa de empleo se implanta en una región y no en la vecina.
Empleo medio, en porcentaje:

```
                 antes    despues
region tratada    20,0      26,0
region control    10,0      12,0
```

- La tratada mejora 6,0 puntos; la control, 2,0 puntos.
- `DiD = 6,0 − 2,0 = 4,0` puntos de efecto atribuido al programa.

Fíjate en lo que has hecho: comparar los niveles (26,0 frente a 12,0) daría un efecto de 14 puntos,
pero esas regiones ya diferían en 10 puntos antes. DiD se queda con el cambio diferencial, y su
supuesto es que esos 2 puntos de mejora del control son los que habría tenido la tratada sin
programa. Si la región tratada estaba además en pleno auge industrial, el supuesto falla y el 4,0
está inflado.

**Variables instrumentales.** Una lotería de admisión a un curso de formación:

- Primera etapa: ganar la lotería sube la probabilidad de hacer el curso en 0,30.
- Forma reducida: ganar la lotería sube el salario mensual en 90 euros.
- `LATE = 90 / 0,30 = 300` euros.

La lectura correcta: 300 euros es el efecto **para quienes hicieron el curso porque ganaron la
lotería**. Para quien habría hecho el curso igualmente, este número no dice nada, y si la lotería
desanima a alguien de hacer el curso (un «defier»), el cociente deja de tener interpretación.

**Regresión discontinua.** Una beca se concede a partir de una nota de corte de 7,00. Con los
expedientes de 6,90 a 6,99 la nota media del segundo curso es 48,2; con los de 7,00 a 7,09 es 51,7.
El salto es de 3,5 puntos y se interpreta como el efecto de la beca para quien está justo en el
corte. Dos advertencias: con 1.800 alumnos solo hay 40 en esa banda, así que la estimación tiene
mucha incertidumbre; y si los profesores redondean las notas hacia arriba para conceder becas, la
densidad de notas salta en el corte y el diseño se cae.

## Código

```python verificable
# Diferencias en diferencias: dos grupos medidos antes y despues
trat_antes, trat_despues = 20.0, 26.0
ctrl_antes, ctrl_despues = 10.0, 12.0

did = (trat_despues - trat_antes) - (ctrl_despues - ctrl_antes)
print(f"cambio del grupo tratado  {trat_despues - trat_antes:+.1f}")   # -> +6.0
print(f"cambio del grupo control  {ctrl_despues - ctrl_antes:+.1f}")  # -> +2.0
print(f"efecto DiD                {did:+.1f}")                         # -> +4.0

# Variables instrumentales: estimador de Wald = forma reducida / primera etapa
primera_etapa, forma_reducida = 0.30, 90.0
print(f"LATE                      {forma_reducida / primera_etapa:.0f}")  # -> 300
```

:::claves
- Los paréntesis de `(trat_despues - trat_antes) - (ctrl_despues - ctrl_antes)` no son decorativos. Sin ellos la resta se encadena de izquierda a derecha y el último término cambia de signo: saldría `26,0 − 20,0 − 10,0 − 12,0 = −16,0` en vez de `+4,0`. Comprobarlo es quitar los paréntesis, volver a ejecutar y leer la línea del efecto.
- `:.0f` redondea, y en el empate Python va al número par: `f"{0.5:.0f}"` imprime `0` y `f"{2.5:.0f}"` imprime `2`. Con 300 exacto no se nota; con una primera etapa de 0,35 el LATE sale 257,142… y el entero que ves depende de esa regla.
- Dividir por cero **no** es igual en Python que en NumPy: `90.0 / 0.0` lanza `ZeroDivisionError` y el bloque se para, mientras que un array de NumPy devolvería `inf` con un aviso y seguiría. En un instrumento débil la primera etapa nunca es exactamente cero, así que el fallo silencioso es el cociente inflado, no la excepción.
- `trat_antes, trat_despues = 20.0, 26.0` es una sola sentencia que desempaqueta una tupla, no dos. Y los valores son `float` por el punto decimal: si escribieras `20`, la resta seguiría dando enteros exactos y el `:.1f` los imprimiría igual, pero una división posterior cambiaría de resultado.
- El cociente de Wald no dice nada por sí solo: el mismo código con `primera_etapa = 0.03` daría 3.000 en lugar de 300 sin ningún error ni aviso. Por eso se mira la `F` de la primera etapa antes que el número final.
- Los comentarios `# -> +6.0` y `# -> 300` están escritos a mano: el portal ejecuta el bloque y enseña la salida real, pero nadie compara esa salida con el comentario. Si cambias un número, el comentario se queda mintiendo.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(0)
n = 4000
u = rng.normal(0, 1, n)                             # confusor: motivacion no observada
t = (u + rng.normal(0, 0.5, n) > 0).astype(float)   # el tratamiento depende de u
y = 2.0 * t + 3.0 * u + rng.normal(0, 0.5, n)       # efecto causal real: 2,0

ingenuo = y[t == 1].mean() - y[t == 0].mean()
# Aqui u SI se observa (es una simulacion); en la vida real no lo tendrias
diseno = np.column_stack([np.ones(n), t, u])
ajustado = np.linalg.lstsq(diseno, y, rcond=None)[0][1]

print(f"diferencia cruda      {ingenuo:.2f}")     # -> 6.32
print(f"controlando por u     {ajustado:.2f}")    # -> 2.01
```

```python verificable
import numpy as np

rng = np.random.default_rng(1)
n = 4000
u = rng.normal(0, 1, n)                                  # confusor, no observado
z = rng.normal(0, 1, n)                                  # instrumento: sorteo
t = (0.8 * z + u + rng.normal(0, 0.5, n) > 0).astype(float)
y = 2.0 * t + 3.0 * u + rng.normal(0, 0.5, n)            # efecto causal real: 2,0

# Wald: covarianza del instrumento con el resultado partido por la primera etapa.
# No hace falta observar u, solo que z no afecte a y por otra via.
iv = np.cov(z, y)[0, 1] / np.cov(z, t)[0, 1]
print(f"primera etapa   {np.cov(z, t)[0, 1] / z.var():.3f}")   # -> 0.226
print(f"estimacion IV   {iv:.2f}")                            # -> 1.87
```

## Errores típicos

- **Controlar por una variable que va después del tratamiento.** Ajustar por un mediador (el
  ingreso actual cuando estudias el efecto de la educación en la salud) elimina parte del efecto que
  quieres medir. La regla sale del DAG, no de la intuición: solo se controla lo que es causa común
  ([[confusores-y-dag]]).
- **Usar un instrumento débil.** Con una primera etapa cercana a cero, el cociente de Wald se
  dispara y su sesgo se amplifica: basta una correlación mínima entre `Z` y el error para que la
  estimación sea basura. Mira siempre la `F` de la primera etapa, no solo el coeficiente.
- **Creer que DiD solo necesita dos periodos cualesquiera.** El supuesto son tendencias paralelas,
  y hay que enseñarlas: si los grupos ya divergían antes del tratamiento, el diseño no vale. Con
  varios periodos previos se comprueba, con dos no.
- **Aplicar DiD con tratamientos escalonados y efectos heterogéneos.** Con adopción a tiempos
  distintos, la regresión de dos vías con efectos fijos compara tratados tardíos con tratados
  tempranos y puede dar efectos de signo contrario al real. Usa estimadores específicos para ese
  caso.
- **Comparar tratados y controles con propensity score sin mirar el solapamiento.** Si las
  propensiones no se solapan, el matching extrapola a zonas sin datos y produce estimaciones
  frágiles. Recorta la muestra a la región de soporte común y dilo.
- **Explicar el RDD con un polinomio global.** Ajustar una única curva a todo el rango de la
  variable de asignación deja que observaciones lejanas al corte manden en la estimación. Usa
  ventanas locales alrededor del corte y comprueba la sensibilidad al ancho.

:::practica
enunciado: Un programa de empleo se aplica en una provincia y no en la vecina. La tasa de empleo pasa del 18,0 % al 25,0 % en la tratada y del 14,0 % al 17,5 % en la control. Un informe compara los niveles finales (25,0 frente a 17,5) y anuncia un efecto de 7,5 puntos. ¿Cuánto da DiD?
pista: DiD resta los cambios, no los niveles: el informe se queda con una diferencia que ya existía antes.
solucion: La tratada mejora 25,0 − 18,0 = +7,0 puntos y la control 17,5 − 14,0 = +3,5, así que DiD = 7,0 − 3,5 = +3,5 puntos. El informe usa 7,5, pero las provincias ya diferían en 18,0 − 14,0 = 4,0 puntos: 7,5 − 4,0 = 3,5. El diseño supone que sin programa ambas habrían evolucionado en paralelo; si la tratada estaba en auge, el 3,5 está inflado.
:::

## Comprueba que lo sabes

:::quiz
p: Un investigador quiere el efecto de un curso de formación sobre el salario y usa como instrumento «haber ganado la lotería de admisión». ¿Qué estima exactamente su cociente de Wald?
o: El efecto medio del curso en toda la población
o: El efecto del curso en quienes asistieron porque ganaron la lotería
o: El efecto de ganar la lotería sobre el salario
a: 2
e: El cociente de Wald estima un efecto local (LATE) sobre los cumplidores: quienes cambian de tratamiento por el instrumento. No es el ATE ni el ATT, y para quienes habrían hecho el curso igualmente el número no informa. El efecto de ganar la lotería sobre el salario es la forma reducida, no el LATE.
:::

:::quiz
p: En un DiD, el grupo tratado mejora 6 puntos y el control 2. ¿Qué supuesto sostiene que el efecto sea 4 y no otra cosa?
o: Que los dos grupos tengan el mismo tamaño
o: Que sin el tratamiento los dos grupos habrían evolucionado en paralelo
o: Que la variable de resultado sea normal
a: 2
e: DiD se queda con el cambio diferencial y atribuye al tratamiento lo que el control no explica, y eso solo es válido si las tendencias habrían sido paralelas sin intervención. El tamaño de los grupos afecta a la precisión, no a la identificación, y no se necesita normalidad.
:::

:::quiz
p: ¿Qué hace inservible un diseño de regresión discontinua?
o: Que la variable de asignación tenga muchos valores distintos
o: Que los individuos puedan manipular con precisión su posición respecto al corte
o: Que el efecto sea pequeño
a: 2
e: El diseño compara a los que quedan justo a cada lado del corte suponiendo que son intercambiables; si alguien puede colocarse justo por encima (redondeos, esfuerzo estratégico), la densidad de la variable salta en el corte y los dos lados dejan de ser comparables. Un efecto pequeño solo reduce la precisión, y muchos valores distintos de la variable son lo normal.
:::
