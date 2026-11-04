---
id: bootstrap
titulo: Bootstrap y remuestreo
fase: 2
nivel: intermedio
rutas: [ds, core]
prerequisitos: [estimadores-y-propiedades, intervalos-de-confianza, medidas-de-dispersion]
tags: [remuestreo, incertidumbre, simulacion]
resumen: Remuestrear tus propios datos con reemplazo para estimar la incertidumbre de casi cualquier estadístico, sin suponer una distribución.
fuentes: ["Efron (1979), 'Bootstrap Methods: Another Look at the Jackknife'", "Efron y Tibshirani (1993), 'An Introduction to the Bootstrap'"]
---

## En una frase

El bootstrap estima la incertidumbre de cualquier estadístico tratando tu muestra como si fuera la
población: remuestrea con reemplazo muchas veces, recalcula el estadístico en cada remuestra y usa
la dispersión de esos valores como si fuera la del muestreo real.

## La idea

El problema que resuelve el bootstrap es muy concreto. Sabes calcular el intervalo de confianza de
una media porque alguien demostró que `x̄` se distribuye de forma conocida (ver
[[intervalos-de-confianza]]). Pero ¿y el intervalo de la **mediana**? ¿Y del percentil 90 del tiempo
de respuesta? ¿Y del coeficiente de un modelo con 40 variables? Para la mayoría de los estadísticos
no existe una fórmula cerrada, y hasta los años 70 la única salida era la teoría asintótica
(aproximaciones que valen «para `n` grande», sin decir cuánto es grande).

La idea de Efron es de una sencillez desarmante. No conoces la población, solo tienes la muestra.
¿Cuál es tu mejor representación de la población? **La muestra misma**, con cada valor repetido
tantas veces como apareció. Y si la muestra es la población, entonces puedes simular el experimento
original: extrae de ella una muestra del mismo tamaño, con reemplazo, y calcula tu estadístico.
Repite eso 2.000 veces y tendrás 2.000 valores del estadístico. La dispersión de esos valores estima
la dispersión que tendrías si pudieras repetir el estudio de verdad.

:::figura
fichero: bootstrap-distribucion-de-la-mediana
pie: A la izquierda está la única muestra que existe: siete tiempos entre 12 y 15 s y un caso de 96 s que arrastra la media hasta 23,9 s mientras la mediana se queda en 13,85 s. A la derecha, las 4.000 medianas que salen de remuestrear esa muestra con reemplazo: el 95 % central va de 12,8 a 15,1 s —un intervalo que ninguna fórmula da— y la media de esas medianas (14,27) queda por encima de la observada, que es el sesgo del estimador con solo ocho datos. La conclusión es que el bootstrap fabrica una distribución de muestreo a partir de una sola muestra, y que su anchura (4,50 s de error típico) no se ve a simple vista mirando los datos.
fuente: figuras/bootstrap-1.py
:::

Dos detalles que hacen que funcione:

- **Con reemplazo**, porque si extrajeras sin reemplazo obtendrías siempre la misma muestra. Al
  reemplazar, cada remuestra es distinta: unos valores salen tres veces y otros ninguna. Es
  exactamente la variabilidad que buscas.
- **Del mismo tamaño**, `n`. Cada remuestra tiene `n` elementos sacados de la muestra original.

El bootstrap es a la estadística lo que una maqueta a la ingeniería: no es el puente real, pero si
la maqueta aguanta, el puente probablemente también. Su límite es el mismo: si la muestra no
representa a la población (por [[sesgo-de-supervivencia|sesgo de selección]] o por no respuesta), el
bootstrap hereda el sesgo y **jamás lo corrige**. Reproduce fielmente la muestra, incluidos sus
defectos.

¿Cuándo **no** funciona? Tres casos claros: estadísticos que dependen de los extremos (el máximo, el
mínimo, el rango), muestras muy pequeñas (`n < 20`) y datos dependientes en el tiempo (series
temporales, donde hay que usar *block bootstrap*). Fuera de ahí es la herramienta más rentable de la
estadística aplicada: cinco líneas de código y un intervalo para lo que quieras.

## Definición formal

Sea `x = (x₁, …, xₙ)` la muestra observada y `θ̂ = T(x)` el estadístico cuya incertidumbre quieres
medir (una media, una mediana, una correlación, un coeficiente).

- `F̂` — **distribución empírica**: la que asigna probabilidad `1/n` a cada valor observado. Es la
  estimación no paramétrica de la distribución poblacional `F`.
- `x* = (x₁*, …, xₙ*)` — una **remuestra bootstrap**: `n` valores extraídos de `x` con reemplazo.
  Es una muestra aleatoria de `F̂`.
- `θ̂* = T(x*)` — el estadístico recalculado en la remuestra. Es una variable aleatoria.
- `B` — número de remuestras (típicamente 1.000 a 10.000).
- `α` — nivel de significación; para un intervalo del 95 %, `α = 0,05`.

El **principio bootstrap** sustituye la distribución desconocida de `θ̂ − θ` bajo `F` por la
distribución conocida de `θ̂* − θ̂` bajo `F̂`:

:::formula
θ̂ − θ   bajo F     ≈     θ̂* − θ̂   bajo F̂
:::

De ahí salen los dos resúmenes que se usan:

:::formula
Percentil:  [ q*_{α/2} , q*_{1−α/2} ]      (cuantiles de los B valores de θ̂*)
:::

:::formula
Error típico bootstrap:  ET* = √( (1/(B−1)) · Σ_b (θ̂*_b − θ̄*)² )
:::

- `q*_{α/2}` — el cuantil `α/2` de la distribución bootstrap de `θ̂*`. Para el 95 %,
  `α/2 = 0,025`.
- `θ̄*` — la media de los `B` valores bootstrap.
- `ET*` — error típico bootstrap: el análogo muestral del error típico teórico.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `x = (x₁, …, xₙ)` | La muestra observada: los n datos que tienes | las de la variable (segundos, euros…) | Nada, y ese es el punto: el bootstrap no añade información que no esté aquí. Si la muestra es rara, todas las remuestras lo serán |
| `θ̂ = T(x)` | El estadístico calculado en la muestra (media, mediana, pendiente…) | las de `θ` | Es lo que quieres acotar. El bootstrap no lo mejora, solo estima cuánto bailaría si repitieras el estudio |
| `F̂` | Distribución empírica: probabilidad 1/n a cada valor observado | adimensional | Es el sustituto de la población desconocida. Con más datos la representa mejor; con sesgo de selección lo hereda intacto |
| `θ̂* = T(x*)` | El mismo estadístico recalculado en una remuestra | las de `θ` | Es una variable aleatoria: cambia en cada remuestra, y esa dispersión es la que se usa como error típico |
| `B` | Número de remuestras | remuestras (1.000 a 10.000) | Más `B` no estrecha el intervalo: solo lo hace más estable entre ejecuciones. Con B = 50, el cuantil 2,5 % se estima con el segundo valor de la lista ordenada y baila |
| `α` | Nivel de significación del intervalo | tanto por uno (0,05 para el 95 %) | Sube → el intervalo se estrecha y cubre menos: con α = 0,20 el mismo intervalo pierde cerca de un tercio de su longitud |
| `q*_{α/2}`, `q*_{1−α/2}` | Cuantiles de los B valores bootstrap | las de `θ` | Son los extremos del intervalo por percentiles. Con B pequeño se apoyan en los valores más extremos, que son justo los menos estables |
| `ET*` | Error típico bootstrap: la desviación de los B valores de `θ̂*` | las de `θ` | Sube con la dispersión de los datos y baja con `√n`. Aquí vale 4,50 s para la mediana de ocho datos |
| `Sesgo* = θ̄* − θ̂` | Desplazamiento del centro bootstrap respecto al valor observado | las de `θ` | Si es grande frente a `ET*`, el estimador es inestable (típico con n < 20). Avisa, pero no corrige el sesgo de la muestra |
:::

Tres propiedades que conviene saber:

1. **Consistencia.** Bajo condiciones de regularidad, la distribución bootstrap de `θ̂*` converge a
   la verdadera. No es una aproximación de conveniencia: es un teorema.
2. **El bootstrap solo ve lo que hay en la muestra.** El rango de `θ̂*` está acotado por los valores
   presentes en la muestra original. Si tu estadístico es el máximo, ninguna remuestra puede superar
   el máximo observado: el intervalo será siempre demasiado estrecho por el lado alto.
3. **Corrección de sesgo.** `Sesgo* = θ̄* − θ̂` estima el sesgo del estimador, así que
   `θ̂ − Sesgo*` es una versión corregida. Es útil, pero puede exagerar si el estimador es muy
   inestable.

## Ejemplo

**Caso 1: la mediana de unos tiempos de espera.** Ocho medidas, con un valor extremo:
12,0 · 14,5 · 13,2 · 15,1 · 12,8 · 14,0 · 13,7 · 96,0 (segundos).

- Media: 23,9 s. Mediana: 13,8 s. La media está contaminada por el 96; la mediana no.
- Para la media hay fórmula (`s/√n`), para la mediana no. Bootstrap con 4.000 remuestras:
  - Error típico de la mediana: **4,50 s**. Nada desdeñable, y mucho mayor de lo que sugiere mirar
    los datos (la mayoría están entre 12 y 15).
  - Intervalo del 95 % por percentiles: **`[12,80 , 15,10]`**. El valor extremo ensancha el
    intervalo porque en algunas remuestras el 96 aparece varias veces y arrastra la mediana.
  - La media de las 4.000 medianas bootstrap es 14,27, por encima de la mediana observada (13,8):
    ese desplazamiento es la corrección de sesgo, y avisa de que con `n = 8` la mediana es un
    estimador inestable.
- Detalle revelador: el 96 aparece en el 65 % de las remuestras. No es un dato raro que se pueda
  ignorar: está en dos tercios de los mundos posibles.

**Caso 2: la pendiente de una regresión.** Con 40 puntos de `y = 0,3·x + ruido(0; 1)`, la pendiente
observada sale 0,305. Remuestreando pares `(x, y)` 4.000 veces:

- Error típico bootstrap: **0,155**.
- Intervalo del 95 % por percentiles: **`[−0,003 , 0,603]`**.
- Casi roza el cero por abajo. La lectura honesta es «la pendiente es positiva pero la muestra no
  permite descartar el cero», y coincide con la teoría: con un error típico de 0,155,
  `0,305 ± 1,96·0,155` da `[0,00 , 0,61]`.

El bootstrap, en dos líneas de código, da el mismo intervalo que la fórmula clásica en el caso donde
la fórmula existe, y funciona igual en el caso donde no existe. Ese es el argumento entero.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(0)

# Tiempos de espera con un valor extremo: la media no es robusta, la mediana si
datos = np.array([12.0, 14.5, 13.2, 15.1, 12.8, 14.0, 13.7, 96.0])
print(f"media    {datos.mean():.1f}")            # -> 23.9
print(f"mediana  {np.median(datos):.1f}")        # -> 13.8

# Bootstrap: remuestreamos con reemplazo 4000 veces para ver la incertidumbre
remuestras = rng.choice(datos, size=(4000, datos.size), replace=True)
medianas = np.median(remuestras, axis=1)

# El 96 aparece en dos tercios de las remuestras: es parte del problema, no un error
print(f"proporcion de remuestras con el 96    {(remuestras == 96.0).any(axis=1).mean():.2f}")  # -> 0.65
print(f"error tipico bootstrap de la mediana  {medianas.std(ddof=1):.2f}")  # -> 4.50
print(f"IC 95 % percentil  [{np.percentile(medianas, 2.5):.2f}, {np.percentile(medianas, 97.5):.2f}]")  # -> [12.80, 15.10]
```

:::claves
- `rng.choice(datos, size=(4000, datos.size), replace=True)` devuelve un array **nuevo** de 4000×8 y no toca `datos`. Sin `replace=True` (que es el valor por defecto) cada fila sería una permutación de la misma muestra, las 4000 medianas valdrían lo mismo y el error típico saldría exactamente 0.
- `np.median(remuestras, axis=1)` devuelve 4000 números, uno por fila. Con `axis=0` devolvería 8, uno por columna, y el intervalo saldría sin sentido. El eje es el error número uno al remuestrear.
- `medianas.std(ddof=1)` divide entre B − 1 = 3999, que es lo que pide la fórmula de `ET*`; el `std()` por defecto es `ddof=0` (divide entre B) y da un valor algo menor. NumPy usa 0 y pandas 1: si pasas estas medianas a una Serie y llamas a `.std()`, el número cambia sin que hayas tocado el cálculo.
- `np.percentile(medianas, 2.5)` no devuelve un valor de la lista: interpola entre los dos valores ordenados vecinos (método `linear`). Por eso el intervalo se mueve en la segunda cifra decimal al cambiar la semilla, y con `B = 100` se movería en la primera.
- `(remuestras == 96.0).any(axis=1).mean()` compara float a float. Aquí es seguro porque 96,0 se representa exacto y los valores son copias del original; con valores como 0,1 esa comparación falla por redondeo. Promediar un array de booleanos los trata como 1 y 0, así que `.mean()` da la proporción directamente.
- El generador `rng` tiene estado: cada llamada avanza la secuencia, así que reordenar las líneas cambia los números aunque la semilla sea la misma. Si quieres que un tramo no dependa de lo anterior, crea otro generador (`np.random.default_rng(3)`) en vez de reutilizar el mismo.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(3)
n = 40
x = rng.normal(0, 1, size=n)
y = 0.3 * x + rng.normal(0, 1, size=n)
xc, yc = x - x.mean(), y - y.mean()
pendiente = (xc @ yc) / (xc @ xc)
print(f"pendiente observada {pendiente:.3f}")   # -> 0.305

# Remuestreamos pares (x, y) y recalculamos la pendiente en cada remuestra
pendientes = np.empty(4000)
for i in range(4000):
    idx = rng.integers(0, n, size=n)
    a, b = xc[idx], yc[idx]
    pendientes[i] = (a @ b) / (a @ a)

print(f"error tipico bootstrap {pendientes.std(ddof=1):.3f}")   # -> 0.155
print(f"IC 95 %  [{np.percentile(pendientes, 2.5):.3f}, {np.percentile(pendientes, 97.5):.3f}]")  # -> [-0.003, 0.603]
```

```python ilustrativo
# El bootstrap en bloque para series temporales: si remuestreas filas sueltas
# destruyes la autocorrelacion y el intervalo sale falsamente estrecho.
#   bloques = [serie[i:i+20] for i in range(0, len(serie), 20)]
#   remuestra = np.concatenate([bloques[i] for i in rng.integers(0, len(bloques), len(bloques))])
# Se remuestrean bloques contiguos, no observaciones individuales.
```

## Errores típicos

- **Remuestrear sin reemplazo.** `rng.choice(datos, size=n)` sin `replace=True` devuelve una
  permutación de la muestra original, así que `θ̂*` vale siempre lo mismo y el error típico sale
  cero. Con reemplazo, o no hay bootstrap.
- **Usar bootstrap para el máximo, el mínimo o el rango.** Ningún remuestreo puede producir un valor
  que no esté en la muestra, así que el máximo bootstrap nunca supera el máximo observado y el
  intervalo es sistemáticamente demasiado estrecho. Para extremos hace falta teoría de valores
  extremos.
- **Aplicarlo a series temporales sin bloques.** Con datos dependientes, remuestrear observaciones
  sueltas rompe la autocorrelación y produce intervalos falsamente estrechos. Se remuestrean bloques
  contiguos lo bastante largos para cubrir la dependencia.
- **Confundir el intervalo bootstrap con un intervalo bayesiano.** El percentil bootstrap es
  frecuentista: no dice «hay un 95 % de probabilidad de que `θ` esté aquí». Dice que ese
  procedimiento cubre el parámetro en el 95 % de los casos, igual que un intervalo de confianza
  clásico.
- **Creer que arregla el sesgo de selección.** Si tu muestra son los clientes que contestaron, el
  bootstrap te dará un intervalo precioso alrededor de una estimación sesgada. Remuestrea la muestra
  que tienes, no la población que querías ([[poblacion-y-muestra]]).
- **Usar `B` demasiado pequeño.** Con 50 remuestras, el cuantil 2,5 % se estima con el segundo valor
  más pequeño de la lista ordenada y el intervalo baila de una ejecución a otra. Con 1.000
  remuestras vas sobrado para un intervalo del 95 %; para el 99 % necesitas más.

:::nota
El bootstrap **paramétrico** es una variante: en vez de remuestrear los datos, generas datos
sintéticos del modelo ajustado (por ejemplo, de una normal con la media y la desviación estimadas) y
repites el proceso. Funciona mejor cuando el modelo es correcto y peor cuando no lo es; el no
paramétrico que se explica aquí no supone ninguna forma de distribución.
:::

:::truco
El bootstrap y los tests de permutación son primos hermanos: el primero remuestrea para estimar la
incertidumbre de un estimador, el segundo baraja etiquetas para construir la distribución nula de un
contraste. Si dominas uno, el otro es cambiar `replace=True` por `rng.permutation`.
:::

:::practica
enunciado: En la muestra de ocho tiempos de espera (12,0 · 14,5 · 13,2 · 15,1 · 12,8 · 14,0 · 13,7 · 96,0), ¿qué probabilidad hay de que una remuestra bootstrap contenga el valor extremo 96,0 al menos una vez? ¿Cuántas de 4.000 remuestras lo contendrían?
pista: Al remuestrear con reemplazo, la probabilidad de no sacar un valor concreto en ninguna de las n extracciones es (1 − 1/n) elevado a n.
solucion: Con n = 8, la probabilidad de no extraer nunca el 96 es (7/8)⁸ = 0,875⁸ = 0,344. Así que la de que aparezca al menos una vez es 1 − 0,344 = 0,656. De 4.000 remuestras, unas 0,656 · 4.000 = 2.624 lo contendrían. Conclusión: el valor extremo está en dos tercios de los mundos bootstrap, y por eso ensancha el intervalo de la mediana aunque sea un solo dato de ocho.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué el bootstrap remuestrea con reemplazo y no sin reemplazo?
o: Porque sin reemplazo cada remuestra sería una permutación de la muestra original y el estadístico valdría siempre lo mismo
o: Porque con reemplazo se obtienen muestras más grandes que la original
o: Porque el reemplazo elimina el sesgo de la muestra original
a: 1
e: Sin reemplazo, cualquier remuestra del mismo tamaño contiene exactamente los mismos valores, así que el estadístico no cambia y su dispersión es cero. El reemplazo es lo que crea la variabilidad entre remuestras que estima el error de muestreo. Nada de esto corrige el sesgo de la muestra.
:::

:::quiz
p: Quieres el intervalo de confianza del máximo de una distribución. ¿Sirve el bootstrap por percentiles?
o: Sí, funciona igual que con la mediana
o: No, porque ninguna remuestra puede superar el máximo observado, así que el intervalo es demasiado estrecho por arriba
o: Sí, pero hay que subir B a 100.000
a: 2
e: El bootstrap solo puede generar valores presentes en la muestra. Para el máximo, todos los valores bootstrap son menores o iguales que el máximo observado, así que la cola superior de la distribución bootstrap está truncada y el intervalo infravalora la incertidumbre real. Los estadísticos de extremos necesitan teoría específica.
:::

:::quiz
p: Un intervalo bootstrap del 95 % para una pendiente sale [−0,003 , 0,603]. ¿Qué conclusión es correcta?
o: La pendiente es positiva con seguridad, porque el intervalo es casi todo positivo
o: Los datos son compatibles con una pendiente nula: el intervalo roza el cero por abajo
o: El bootstrap ha fallado, porque un intervalo no puede incluir el cero si la pendiente estimada es 0,305
a: 2
e: El intervalo incluye el cero (por −0,003), así que no se puede descartar que la pendiente sea nula con un 5 % de significación. Además coincide con la aproximación clásica, 0,305 ± 1,96·0,155 = [0,00 , 0,61], lo que confirma que el bootstrap está funcionando.
:::
