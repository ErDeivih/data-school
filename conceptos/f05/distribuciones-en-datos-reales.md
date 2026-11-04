---
id: distribuciones-en-datos-reales
titulo: Distribuciones en datos reales
fase: 5
nivel: intermedio
rutas: [core, ds, quant]
prerequisitos: [distribuciones-continuas, asimetria-y-curtosis, medidas-de-dispersion]
tags: [distribuciones, colas-gordas, censura, conteo]
resumen: Los datos reales casi nunca son normales: tienen colas gordas, dos picos, cortes por censura, ceros de más o son recuentos, y cada patrón pide otro estadístico.
fuentes: ["Tukey (1977), 'Exploratory Data Analysis'"]
---

## En una frase

Antes de calcular una media o ajustar un modelo, mira la forma de la distribución: si tiene cola
larga, dos picos, está cortada en un límite, tiene un exceso de ceros o son recuentos, los
métodos pensados para la normal te van a mentir.

## La idea

La distribución normal es el invitado famoso de la estadística: aparece en los libros, en los
intervalos de confianza y en el teorema central del límite. Pero en un dataset real es la
excepción. Los ingresos, los tiempos de espera, los siniestros de un seguro, el número de
compras por usuario y el tráfico de una web no se parecen a una campana.

:::figura
fichero: distribuciones-reales-cuatro-patrones
pie: Los cuatro patrones que más veces se confunden con «datos sucios». Arriba a la izquierda, la media (58,7 mil) queda por encima de la mediana (49,1 mil) porque unos pocos ingresos enormes tiran de ella: con cola larga, publica mediana y cuantiles, no la media. Arriba a la derecha, la media global de las dos poblaciones (168,0 cm) cae justo en el valle, donde casi no hay nadie, así que no describe a ningún turno. Abajo, la censura apila en el mismo valor 10 el 5,2 % de los casos, y el 62,7 % de ceros no es «gente que compra poco», es gente que no participa: ninguno de los dos patrones se arregla con un estadístico, se arreglan cambiando el modelo.
fuente: figuras/distribuciones-en-datos-reales-1.py
:::

Cinco patrones que aparecen una y otra vez:

1. **Cola gorda** (*heavy tail*): la mayoría de los valores se concentra en un rango pequeño y
   unos pocos son enormes. En una lognormal, el valor máximo de 100 000 observaciones puede
   estar diez veces por encima de la media.
2. **Bimodalidad**: hay **dos poblaciones mezcladas** en la misma columna. Las alturas de dos
   turnos de fábrica, las transacciones de clientes particulares y de empresas, los tiempos de
   respuesta de dos centros de datos.
3. **Censura**: el instrumento o el proceso **corta** el valor en un límite. Un sensor que
   registra como máximo 10 minutos, un contrato que dura 24 meses y no sabes qué pasa después.
4. **Ceros inflados**: una parte grande de las filas vale exactamente cero, y el resto sigue
   otro patrón. Usuarios que no compran este mes, días sin incidencias.
5. **Datos de conteo**: números enteros no negativos (número de pedidos, de visitas, de
   errores), donde la varianza suele ser **mayor que la media**.

El problema práctico es que la media y la desviación típica, que son la base del z-score, del
test t y de la regresión con errores normales, se comportan fatal con estos patrones. Con cola
gorda, la media depende de si en tu muestra cayó o no el caso extremo; con datos mezclados, la
media cae en el valle entre los dos picos, es decir, en la zona con menos observaciones de todo
el rango. No es que la media esté mal calculada: es que no describe nada.

:::nota
Esto no significa que la normal no sirva para nada. Significa que hay que **comprobarla** en vez
de suponerla. Y hay un lugar donde la normal aparece de verdad: en la distribución de la media
de muchas observaciones, aunque cada observación no sea normal. Eso es
[[teorema-central-del-limite]], y es la razón de que la estadística clásica funcione con datos
que no son normales.
:::

## Definición formal

Los dos números que resumen la forma de una variable, con `μ` la media y `σ` la desviación
típica:

:::formula
asimetría  γ₁ = E[ ((X − μ) / σ)³ ]          curtosis en exceso  γ₂ = E[ ((X − μ) / σ)⁴ ] − 3
:::

- `E[·]` — esperanza matemática, que en la práctica se estima con el promedio.
- `X` — la variable aleatoria.
- `γ₁` — vale 0 en una distribución simétrica y es positivo si la cola larga está a la derecha.
- `γ₂` — vale 0 en la normal; por encima de 0 indica colas más gordas y pico más alto (leptocúrtica).

Los patrones, en fórmula:

:::formula
mezcla      f(x) = π · f₁(x) + (1 − π) · f₂(x)
:::

:::formula
ceros inflados   P(X = 0) = π + (1 − π) · e^(−λ)          censura   Y = mín(X, c)
:::

- `π` — proporción de la primera población, entre 0 y 1.
- `f₁`, `f₂` — densidades de cada población de la mezcla.
- `λ` — media del recuento en la parte que no es cero estructural.
- `c` — el límite donde el proceso corta; `Y = mín(X, c)` es lo que observas.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `μ` | Media de la variable | las de `X` | Arrastra el centro hacia la cola; con cola gorda depende de si en la muestra cayó o no el caso extremo |
| `σ` | Desviación típica | las de `X` | Ensancha la distribución; es el denominador de `(X − μ) / σ`, el cociente que se eleva al cubo y a la cuarta |
| `γ₁` | Asimetría | adimensional | Positiva si la cola larga está a la derecha; por encima de 1 la media ya describe mal el conjunto |
| `γ₂` | Curtosis en exceso | adimensional | Colas más gordas y pico más alto que la normal; por encima de 3 la regla de las tres sigmas deja fuera muchos más casos de los esperados |
| `π` | Proporción de la primera población de la mezcla | tanto por uno, 0 a 1 | Con `π` cerca de 0,5 y las medias separadas aparece el valle: la media global cae donde menos datos hay |
| `f₁`, `f₂` | Densidades de cada población de la mezcla | densidad | Separan los dos picos: cuanto más lejos estén sus medias, menos representa la media global |
| `λ` | Media del recuento en la parte que no es cero estructural | recuentos | Sube la media y la varianza a la vez; en una Poisson pura son iguales, así que una varianza triple no se arregla tocando `λ` |
| `c` | El límite donde el proceso corta | las de `X` | Cuanto más bajo, más casos se apilan en `c` y más se subestima la media real: el dato deja de distinguir «justo en el límite» de «muy por encima» |
:::

Para datos de conteo, la relación clave es la **sobredispersión**:

:::formula
si  varianza > media  ⇒  Poisson no basta
:::

En una Poisson pura la varianza **es igual** a la media. Cuando la varianza observada es el
triple de la media, hay heterogeneidad entre las unidades (unos usuarios compran mucho más que
otros) y el modelo Poisson subestima el error: los intervalos de confianza salen demasiado
estrechos y los contrastes demasiado optimistas.

## Ejemplo

**Cola gorda.** Con 100 000 observaciones simuladas de ingresos:

| Distribución | Media | Mediana | Máximo | Por encima de media + 3σ |
| --- | --- | --- | --- | --- |
| Normal | 49 908 | 49 891 | 138 127 | 163 (0,16 %) |
| Lognormal | 58 667 | 49 055 | 580 674 | 1 713 (1,71 %) |

En la normal, la regla de las tres sigmas deja fuera un 0,16 % —cerca del 0,3 % teórico de las
dos colas—. En la lognormal deja fuera **diez veces más**. Además, la media (58 667) está muy
por encima de la mediana (49 055): más de la mitad de los casos gana menos que la media.

**Bimodalidad.** Dos turnos de una fábrica, 10 000 alturas, uno con media 163 cm y otro con
media 180 cm, ambos con desviación 5. La media global es **171,6 cm**, pero solo un **10,3 %**
de las personas está a menos de 2,5 cm de esa media, frente a un **19,3 %** cerca de 163 y un
**18,7 %** cerca de 180. La media señala el punto del rango donde hay menos gente.

**Censura.** Un sensor registra tiempos de espera con un corte en 10 minutos. El tiempo real
medio es 3,741, el registrado 3,506: la censura tira la media hacia abajo un 6 %. El 5,15 % de
los casos están censurados, y esos casos tienen una media real de 14,553 minutos —el triple que
la media general—. Analizar la columna registrada como si fueran valores completos subestima el
problema justo en la cola, que es donde está el riesgo.

**Ceros inflados.** 10 000 usuarios con visitas semanales: 62,7 % no visita ninguna vez, y los
que visitan lo hacen con una media de 3,621 visitas. La media global es 1,352, que no describe a
nadie: ni al 62,7 % que tiene cero, ni al grupo que visita. La varianza es 4,311 frente a una
media de 1,352, así que hay **sobredispersión**: la Poisson no encaja.

## Código

```python verificable
import numpy as np

# La misma media en dos generaciones distintas: los ingresos no son simetricos.
rng = np.random.default_rng(1)
normal = rng.normal(50_000.0, 20_000.0, size=100_000)
lognormal = rng.lognormal(mean=10.8, sigma=0.6, size=100_000)

for nombre, muestra in (("normal", normal), ("lognormal", lognormal)):
    limite = muestra.mean() + 3 * muestra.std()
    print(nombre, "media", round(float(muestra.mean())),
          "mediana", round(float(np.median(muestra))),
          "maximo", round(float(muestra.max())),
          "fuera de 3 sigma", int((muestra > limite).sum()))
```

:::claves
- `muestra.mean()`, `muestra.std()` y `muestra.max()` devuelven escalares de NumPy (`np.float64`), no enteros ni `float` de Python. Por eso el código los envuelve en `float(...)` antes de `round`: sin eso, en una lista o en un DataFrame acaban como tipo de NumPy, y `int()` sobre un `np.float64` con decimales trunca en vez de redondear.
- Aquí `std()` va **sin** `ddof=1`, así que divide entre `n` (desviación poblacional), no entre `n − 1`. Con 100 000 valores apenas cambia, pero es la misma trampa del `ddof` que aparece en todas las librerías: `np.std` usa 0 por defecto, pandas `.std()` usa 1 por defecto y `StandardScaler` usa 0. Si comparas números calculados con herramientas distintas, la diferencia es el `ddof`.
- `muestra > limite` no filtra: devuelve un array de booleanos con la misma forma (100 000 `True`/`False`). Se convierte en un recuento al sumarlo, porque `True` vale 1. Ese es el motivo de que la comparación y el `.sum()` estén en la misma línea: `(muestra > limite).sum()`, con paréntesis obligatorios.
- `rng.lognormal(mean=10.8, sigma=0.6)` **no** recibe la media y la desviación de la variable, sino las del logaritmo. De ahí que la media salga ≈ 58 667 y la mediana ≈ 49 055: `exp(10.8) ≈ 49 055` es la mediana, y la media queda por encima por la cola. Confundir esos dos parámetros es el error número uno al generar una lognormal.
- Las dos muestras se generan con el **mismo** `rng`, y eso importa: cada llamada a `rng.normal(...)` consume estado del generador, así que la segunda muestra (`lognormal`) empieza donde acabó la primera. Si cambias el orden de esas dos líneas, o cambias el `size` de una, las dos muestras cambian y las cifras de la tabla dejan de salir. Por eso la semilla (`default_rng(1)`) fija el resultado solo mientras el guion sea exactamente este.
- El bucle `for nombre, muestra in (("normal", normal), ("lognormal", lognormal)):` desempaqueta una tupla de tuplas. Si añades una tercera muestra basta con alargar la tupla; si te olvidas de la coma entre dos elementos, Python concatena las cadenas en vez de crear dos tuplas y el `for` falla con «too many values to unpack». Cámbialo por un tercer par y verás el fallo exacto.
:::

```python verificable
import numpy as np

# Ceros inflados: dos procesos mezclados, no una sola distribucion con muchos ceros.
rng = np.random.default_rng(2)
visitas = np.where(rng.random(10_000) < 0.62, 0, rng.poisson(3.5, size=10_000))

print("media global:", round(float(visitas.mean()), 3))                    # -> 1.352
print("media de los que visitan:", round(float(visitas[visitas > 0].mean()), 3))  # -> 3.621
print("proporcion de ceros:", round(float((visitas == 0).mean()), 3))      # -> 0.627
print("varianza:", round(float(visitas.var()), 3))                         # -> 4.311
```

```python verificable
import numpy as np

# Censura por la derecha: el sensor corta en 10 y la media observada baja.
rng = np.random.default_rng(4)
real = rng.lognormal(mean=1.0, sigma=0.8, size=50_000)
registrado = np.minimum(real, 10.0)

print("media real:      ", round(float(real.mean()), 3))        # -> 3.741
print("media registrada:", round(float(registrado.mean()), 3))  # -> 3.506
print("proporcion censurada:", round(float((real > 10).mean()), 4))  # -> 0.0515
print("media de los censurados:", round(float(real[real > 10].mean()), 3))  # -> 14.553
```

## Errores típicos

- **Aplicar la regla de las tres sigmas a una variable de cola gorda.** En la lognormal del
  ejemplo salen diez veces más casos «imposibles» que en la normal. Esos casos no son errores de
  datos: son el fenómeno. Con cola gorda se usan cuantiles, no múltiplos de σ.
- **Describir una distribución sesgada con la media.** La media de los ingresos está por encima
  de más de la mitad de los casos. Publica la mediana y los cuantiles, y si usas la media, di
  por qué.
- **Analizar datos censurados como si estuvieran completos.** El corte tira la media hacia abajo
  y esconde justo la cola que importa. Hay que modelar la censura (o al menos acotarla), y decir
  cuántos casos están en el límite.
- **Rellenar los ceros con la media de los que no son cero.** Son dos procesos distintos: uno
  decide participar y el otro decide cuánto. Mezclarlos destroza cualquier predicción. Lo
  habitual es modelar la participación por separado, con un modelo en dos partes.
- **Ajustar una Poisson a un recuento con sobredispersión.** El modelo da errores estándar
  demasiado pequeños y conclusiones demasiado seguras. Comprueba siempre si la varianza supera a
  la media y pasa a binomial negativa o a cuasi-verosimilitud.
- **Borrar los valores extremos para que la distribución «quede normal».** En un problema de
  riesgo o de fraude, los extremos **son** el objeto de estudio. Si el modelo no los soporta,
  cambia el modelo, no los datos.

:::practica
enunciado: Una fábrica mide 4.000 piezas: 3.000 del turno de mañana, con media 12,5 mm, y 1.000 del turno de noche, con media 16,5 mm. Calcula la media global y decide si sirve para resumir la columna.
pista: Es una mezcla de dos poblaciones: la media ponderada cae entre los dos picos, justo donde casi no hay piezas.
solucion: Media global = (3.000 · 12,5 + 1.000 · 16,5) / 4.000 = (37.500 + 16.500) / 4.000 = 54.000 / 4.000 = 13,5 mm. Ese 13,5 no describe a ningún turno: está en el valle entre 12,5 y 16,5. La conclusión es que hay bimodalidad y que toca analizar los turnos por separado, no resumir la columna con un solo número.
:::

## Comprueba que lo sabes

:::quiz
p: La columna de importes tiene una media de 58 667 y una mediana de 49 055, con un máximo de 580 674. ¿Qué forma esperas?
o: Simétrica, porque la media y la mediana se parecen
o: Sesgada a la derecha, con cola larga y unos pocos valores muy altos
o: Bimodal, porque hay dos números distintos
a: 2
e: Cuando la media supera a la mediana, la cola larga está a la derecha y arrastra el promedio: más de la mitad de los casos están por debajo de la media. La mediana y los cuantiles describen ese conjunto mucho mejor. Media y mediana parecidas indicarían simetría, y aquí difieren en casi 10 000.
:::

:::quiz
p: En un recuento de pedidos por cliente, la varianza es 4,3 y la media 1,35. ¿Qué implica?
o: Que hay sobredispersión y una Poisson simple no es adecuada
o: Que los datos son incorrectos, porque en una Poisson la varianza es igual a la media
o: Que hay que estandarizar la variable antes de modelarla
a: 1
e: En una Poisson pura la varianza iguala a la media. Una varianza tres veces mayor indica heterogeneidad entre clientes: unos compran mucho y otros nada. Eso se modela con binomial negativa o con cuasi-verosimilitud; los datos no están mal, simplemente no son Poisson.
:::

:::aviso
La censura y los ceros inflados se detectan con una pregunta de negocio, no con un test. Antes
de modelar, pregunta cómo se recogió el dato: si hay un valor máximo que se repite demasiado, si
alguien cortó la cola al exportar, o si el cero significa «no se midió» en vez de «no ocurrió».
:::
