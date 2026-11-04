---
id: pruebas-de-equivalencia-y-no-inferioridad
titulo: Pruebas de equivalencia y no inferioridad
fase: 2
nivel: avanzado
rutas: [ds, core]
prerequisitos: [contraste-de-hipotesis, intervalos-de-confianza, errores-tipo-i-ii-y-potencia, tamano-muestral, test-t]
tags: [inferencia, equivalencia, no-inferioridad, bioestadistica]
resumen: Cómo demostrar que dos cosas son prácticamente iguales, en lugar de limitarse a no encontrar diferencias, y por qué «no significativo» no es «equivalente».
fuentes: ["Schuirmann (1987), 'A comparison of the two one-sided tests procedure and the power approach for assessing the equivalence of average bioavailability'", "Wellek (2010), 'Testing Statistical Hypotheses of Equivalence and Noninferiority', 2ª ed.", "FDA (2022), 'Guidance for Industry: Statistical Approaches to Establishing Bioequivalence'"]
---

## En una frase

Las pruebas de equivalencia dan la vuelta al contraste clásico: en lugar de asumir que no hay
diferencia y buscar pruebas en contra, asumen que la diferencia importa y exigen datos que
demuestren que se queda dentro de un margen pequeño que se fijó antes.

## La idea

El contraste clásico no puede demostrar una igualdad. Su hipótesis nula es «no hay diferencia» y
solo se rechaza con evidencia suficiente en contra. Si no rechazas, lo único que has demostrado
es que tu muestra no era lo bastante grande para distinguir la diferencia de cero: un
experimento con tres ratones tampoco rechaza. El p-valor de 0,42 no distingue entre «son
idénticos» y «no tengo ni idea».

Y hay situaciones donde lo que necesitas demostrar es precisamente la igualdad. Un genérico tiene
que demostrar que su absorción es **equivalente** a la del medicamento de referencia, no que «no
se ha detectado diferencia». Una versión nueva de un algoritmo tiene que demostrar que no es
**peor** que la anterior (no inferior), porque es más barata o más rápida. Un lote de piezas tiene
que demostrar que su medida está dentro de tolerancia. En los tres casos, la carga de la prueba
está en el que afirma la igualdad.

El truco de las pruebas de equivalencia es invertir las hipótesis. Se fija de antemano un margen
`Δ` que marca la frontera de lo que se considera irrelevante: un 0,5 % en un ensayo de
bioequivalencia, 2 puntos en una escala clínica, 10 milisegundos en una latencia. Ese margen no
sale de los datos: sale del contexto, y hay que justificarlo. Con el margen ya fijado, la
hipótesis nula pasa a ser «la diferencia es mayor que el margen» y lo que hay que rechazar es esa.
Rechazarla es afirmar la equivalencia, y solo se consigue con datos que la demuestren.

En la práctica se hace con dos contrastes de una cola, y de ahí el nombre de TOST, del inglés
*two one-sided tests*. Uno comprueba que la diferencia no es demasiado negativa (no está por
debajo de `−Δ`) y el otro que no es demasiado positiva (no está por encima de `+Δ`). Hay que
rechazar los dos, y el p-valor que se informa es el mayor de los dos. No es un p-valor al uso: es
un p-valor que solo es pequeño cuando los datos están **dentro** de la zona de equivalencia.

De ahí sale la regla que más se repite en la práctica: la equivalencia se decide mirando un
intervalo de confianza, y no es el del 95 %. Como el TOST son dos contrastes de una cola con
`α = 0,05` cada uno, el intervalo que le corresponde es el de **dos colas al 90 %**. Si todo ese
intervalo cae dentro de `(−Δ, +Δ)`, la equivalencia queda establecida al 5 %. Este detalle es el
que más se falla: con el intervalo del 95 %, que es más ancho, se rechazan muchas equivalencias
que en realidad estaban demostradas.

La no inferioridad es el caso de una sola cola. No se exige que el nuevo tratamiento sea igual:
se exige que no sea peor por más de un margen `Δ`, y mejorarlo todo lo que quiera es aceptable.
Por eso la hipótesis nula es «el nuevo es peor por `Δ` o más» y solo se rechaza mirando un lado.
El intervalo que le corresponde es el de una cola al 95 %, que es el mismo que el de dos colas al
90 %: por eso en los informes de no inferioridad se ve el límite inferior al 90 % y el superior
suele pasar de largo del margen. Si el nuevo resulta ser mejor, no se puede afirmar equivalencia
con este diseño, porque la diferencia real puede haber salido por el otro lado.

Y la consecuencia incómoda de todo esto: demostrar equivalencia es **mucho más caro** que
demostrar superioridad. El tamaño de muestra crece como `1/Δ²`, así que apretar el margen a la
mitad multiplica por cuatro el número de observaciones. Y como hay que demostrar que una
diferencia *no existe*, no hay atajo: la única palanca es medir mucho y con poco ruido.

## Definición formal

Sea `δ = μ_nuevo − μ_referencia` la diferencia de medias que se quiere acotar y `Δ > 0` el margen
de equivalencia, fijado antes de ver los datos. El contraste de equivalencia (TOST) plantea dos
pares de hipótesis:

:::formula
H0₁: δ ≤ −Δ   frente a   H1₁: δ > −Δ        y        H0₂: δ ≥ +Δ   frente a   H1₂: δ < +Δ
:::

La equivalencia se declara cuando se rechazan las **dos** hipótesis nulas a la vez, es decir,
cuando el intervalo de confianza del 90 % para `δ` cae entero dentro de `(−Δ, +Δ)`.

:::formula
p_TOST = máx( p₁ , p₂ )     con     p₁ = P(T ≥ (δ̂ + Δ) / EE)   y   p₂ = P(T ≤ (δ̂ − Δ) / EE)
:::

- `δ` — diferencia real de medias entre los dos grupos, en unidades de la variable. Es lo que se
  quiere acotar.
- `δ̂` — diferencia observada en la muestra, el estimador de `δ`.
- `Δ` — margen de equivalencia. Unidades de la variable. Se fija antes del experimento a partir
  de criterio clínico, técnico o regulatorio, nunca a partir de los datos.
- `EE` — error típico de la diferencia de medias, `s·√(1/n₁ + 1/n₂)` con `s` la desviación típica
  combinada. Unidades de la variable.
- `T` — estadístico t con `n₁ + n₂ − 2` grados de libertad.
- `p₁` — p-valor del contraste de que la diferencia no es demasiado negativa.
- `p₂` — p-valor del contraste de que la diferencia no es demasiado positiva.
- `p_TOST` — el mayor de los dos. Solo es pequeño si las **dos** colas están descartadas.

Para la no inferioridad, con margen `Δ`, solo se contrasta el lado malo:

:::formula
H0: δ ≤ −Δ   frente a   H1: δ > −Δ        y se rechaza si el límite inferior del IC del 90 % supera −Δ
:::

Y la fórmula del tamaño de muestra, suponiendo que la diferencia real es cero, que es la que
decide si un estudio de equivalencia es viable:

:::formula
n por grupo ≈ 2 · σ² · (z_(1−α) + z_(1−β))² / Δ²
:::

- `σ²` — varianza de la variable respuesta, en unidades al cuadrado. Se estima de un estudio
  piloto o de la literatura.
- `z_(1−α)` — cuantil normal para el nivel de significación; con `α = 0,05` es 1,645.
- `z_(1−β)` — cuantil normal para la potencia; con potencia 0,80 es 0,842.
- `Δ²` — el margen al cuadrado en el denominador. Si la diferencia real no es cero, el margen útil
  se reduce a `Δ` menos esa diferencia y el tamaño sube: de ahí que el esfuerzo crezca como el
  inverso del cuadrado del margen.

:::parametros
| Símbolo | Qué es | Unidades | Si sube |
| --- | --- | --- | --- |
| `δ` | Diferencia real de medias entre los dos grupos | las de la variable | Es lo que hay que acotar. Cuanto más se aleje de cero, más difícil es que quepa en el margen: el estudio pierde potencia y, si supera `Δ`, la equivalencia es falsa por mucho que se mida |
| `δ̂` | Diferencia observada en la muestra | las de la variable | Mueve el centro del intervalo de confianza. Una diferencia observada grande puede dejar el intervalo fuera del margen aunque la real fuera pequeña, y al revés |
| `Δ` | Margen de equivalencia: la frontera de lo que se considera irrelevante | las de la variable | Ensancha la zona que hay que alcanzar, así que hace el estudio más fácil y barato. Pero un margen grande es una afirmación más débil: «equivalente en ±10 ms» no dice lo mismo que «equivalente en ±1 ms». El margen se justifica, no se elige a conveniencia |
| `EE` | Error típico de la diferencia: `s·√(1/n₁ + 1/n₂)` | las de la variable | Con `δ̂` fijo, un `EE` mayor ensancha el intervalo de confianza y hace más difícil que quepa en `(−Δ, Δ)`. Se reduce subiendo `n` o midiendo con menos ruido |
| `α` | Nivel de significación de **cada** contraste de una cola, normalmente 0,05 | probabilidad | Subirlo facilita declarar equivalencia y aumenta los falsos positivos (declarar equivalentes dos cosas que no lo son). El 0,05 habitual aquí significa un intervalo del 90 %, no del 95 % |
| `β` | Riesgo de no detectar la diferencia cuando está fuera del margen | probabilidad | Bajarlo exige más datos. Con `β = 0,20` (potencia 0,80), `σ = 1,5` y `Δ = 0,5` hacen falta 112 observaciones por grupo; con potencia 0,90, 155. La potencia se paga en muestra, no en margen |
| `σ` | Desviación típica de la variable respuesta | las de la variable | Es el enemigo: el tamaño de muestra crece con su cuadrado. Duplicar la variabilidad del ensayo multiplica por cuatro las observaciones necesarias, así que a veces conviene más medir mejor que reclutar más |
| `n` | Observaciones por grupo | observaciones | Sube la precisión del intervalo de confianza como `1/√n`: para estrecharlo a la mitad hace falta cuatro veces más muestra. En equivalencia, `n` es lo único que compensa una diferencia observada que no está en el centro |
:::

:::trampa
Un resultado no significativo no es una equivalencia. Es el error más frecuente y el más grave:
informar «no hay diferencias» con p = 0,6 cuando el estudio no tenía potencia para detectar ni
una diferencia del triple del margen. Antes de escribir esa frase, mira el intervalo de confianza:
si es ancho, lo que tienes es una duda, no una igualdad.
:::

:::figura
fichero: equivalencia-tost-y-su-intervalo
pie: Cada barra es el intervalo de confianza del 90 % de la diferencia entre dos tratamientos, sobre la misma zona de equivalencia de ±0,5. El estudio A tiene el intervalo entero dentro del margen y declara equivalencia. El B también cae dentro, pero su intervalo es ancho: si el margen fuera de 0,3, no lo sería. El C no llega a demostrar equivalencia ni superioridad, y el D tiene el intervalo fuera del margen por arriba, así que la equivalencia no se sostiene y sí hay evidencia de diferencia.
fuente: figuras/pruebas-de-equivalencia-y-no-inferioridad-1.py
:::

## Ejemplo

Un genérico se compara con el medicamento de referencia. La variable es la concentración máxima en
sangre y el margen de equivalencia fijado por el regulador es `Δ = 0,5`. Con 100 sujetos por
grupo, la diferencia observada es `δ̂ = 0,20` y la desviación típica combinada `s = 1,5`:

`EE = 1,5 · √(1/100 + 1/100) = 1,5 · 0,1414 = 0,212`.

Con 198 grados de libertad, el cuantil t para una cola al 5 % es 1,6526, así que el intervalo de
confianza del 90 % es

`0,20 ± 1,6526 · 0,212 = 0,20 ± 0,351` → `(−0,151; +0,551)`.

El intervalo **no** cabe entero dentro de `(−0,5; +0,5)`: el extremo superior se sale por 0,051.
Los dos contrastes de una cola dan

```text
p1: que la diferencia no sea menor que -0,5    p = 0,00057
p2: que la diferencia no sea mayor que +0,5    p = 0,07943
p_TOST = max(0,00057; 0,07943) = 0,07943       ->  no se rechaza al 5 %
```

Fíjate en que el contraste bilateral clásico de «hay diferencia» da `p = 0,347`: con el mismo
experimento, no se detecta diferencia y tampoco se demuestra equivalencia. Son dos preguntas
distintas y ninguna de las dos tiene respuesta con estos datos. Es exactamente la situación que
esta página existe para describir.

Si el límite del 95 % se hubiera usado en lugar del 90 %, el intervalo sería `(−0,218; +0,618)`,
todavía peor. Y si el margen hubiera sido `Δ = 0,6`, el mismo estudio habría declarado la
equivalencia sin tocar un solo dato: el margen decide el resultado, y por eso se fija antes y se
justifica.

Para la no inferioridad, con un margen de `Δ = 0,4` y la misma diferencia de 0,20 (el genérico
absorbe un poco más, que es la dirección buena):

```text
H0: la diferencia es <= -0,4        H1: la diferencia > -0,4
p de una cola = 0,0026     ->  se rechaza
```

La lectura aquí es la contraria a la del ejemplo de arriba: con el margen en 0,4 este estudio
**sí** demuestra no inferioridad, y con holgura, porque el límite inferior del intervalo del 90 %
(`−0,151`) queda muy por encima de `−0,4` y la diferencia observada está a `0,6 / 0,212 ≈ 2,8`
errores típicos de la frontera. Cuánto cuesta apretar el margen lo dice la fórmula del tamaño
muestral: con `σ = 1,5`, para demostrar equivalencia con `Δ = 0,5` y una diferencia real de cero
hacen falta

`n ≈ 2 · 2,25 · (1,645 + 0,842)² / 0,25 = 10,125 · 6,185 / 0,25 ≈ 251` en total, unos **112 por
grupo**. Con `Δ = 0,3` la cuenta se dispara a **310 por grupo**, y con `Δ = 0,2`, a **696**. El
margen manda.

## Código

```python verificable
import numpy as np
from scipy import stats

# Ensayo de bioequivalencia: 100 sujetos por grupo, diferencia observada 0,20, s combinada 1,5.
d, s, n1, n2, margen = 0.20, 1.5, 100, 100, 0.5
ee = s * np.sqrt(1.0 / n1 + 1.0 / n2)
gl = n1 + n2 - 2

t90 = stats.t.ppf(0.95, gl)                       # una cola al 5 % = dos colas al 90 %
print(f"EE {ee:.3f}  IC90 ({d - t90 * ee:+.3f}, {d + t90 * ee:+.3f})  dentro del margen: "
      f"{abs(d) + t90 * ee < margen}")
# -> EE 0.212  IC90 (-0.151, +0.551)  dentro del margen: False

p1 = stats.t.sf((d + margen) / ee, gl)            # el limite de abajo, -margen
p2 = stats.t.cdf((d - margen) / ee, gl)           # el limite de arriba, +margen
print(f"p TOST = max({p1:.5f}, {p2:.5f}) = {max(p1, p2):.5f}   se rechaza: {max(p1, p2) < 0.05}")
# -> p TOST = max(0.00057, 0.07943) = 0.07943   se rechaza: False

# El contraste clasico da otra cosa: no detecta diferencia... y tampoco demuestra igualdad.
print(f"p bilateral clasico {2 * stats.t.sf(abs(d) / ee, gl):.3f}")
# -> p bilateral clasico 0.347
```

:::claves
- El intervalo que decide la equivalencia es el del **90 %**, porque `stats.t.ppf(0.95, gl)` es el
  cuantil de una cola al 5 %. Escribir `stats.t.ppf(0.975, gl)` da el intervalo del 95 %, que es
  más ancho, y es el fallo más común: se declaran no equivalentes estudios que sí lo eran.
- `stats.t.sf((d + margen) / ee, gl)` calcula la cola derecha del contraste «la diferencia no es
  menor que `−margen`». Fíjate en el signo: el límite de abajo es `−margen` y por eso aparece
  `d + margen`. Cambiar los dos signos intercambia `p1` y `p2`, y como se informa el máximo, el
  resultado no cambia; pero si solo informas uno, sí.
- `max(p1, p2)` y no `min`. La equivalencia exige rechazar **las dos** hipótesis nulas, y como
  cada p-valor mide la evidencia contra una de ellas, hay que quedarse con el peor. `min(p1, p2)`
  es el error de quien viene de los contrastes de superioridad, donde el p-valor bueno es el
  pequeño.
- Los grados de libertad son `n1 + n2 - 2` con la desviación típica combinada. Si los dos grupos
  tienen varianzas muy distintas, toca la versión de Welch (grados de libertad aproximados), y
  entonces `stats.ttest_ind(..., equal_var=False)` da el p-valor bilateral, no los del TOST. Para
  el TOST hay que calcular el error típico y los grados de libertad a mano.
- `abs(d) + t90 * ee < margen` es la prueba del intervalo pero solo vale si `d` es positivo. Con
  `d` negativo hay que comprobar que `d − t90·ee > −margen` y `d + t90·ee < margen` por separado.
  Usar el valor absoluto en una sola línea es una fuente silenciosa de errores de signo.
:::

```python verificable
import numpy as np
from scipy import stats

# Cuanto cuesta demostrar equivalencia: manda el margen, y el coste va como 1/margen^2.
def n_por_grupo(margen, sd=1.5, alpha=0.05, potencia=0.80, delta=0.0):
    za, zb = stats.norm.ppf(1 - alpha), stats.norm.ppf(potencia)
    return 2 * sd**2 * (za + zb) ** 2 / (margen - abs(delta)) ** 2

for margen in (0.5, 0.4, 0.3, 0.2):
    print(f"margen {margen:.1f}  n por grupo {np.ceil(n_por_grupo(margen)):.0f}")
# -> margen 0.5  n por grupo 112
# -> margen 0.4  n por grupo 174
# -> margen 0.3  n por grupo 310
# -> margen 0.2  n por grupo 696

# Si la diferencia real no es cero, el estudio se encarece: se pierde margen util.
print(f"con margen 0,3 y una diferencia real de 0,1 hacen falta "
      f"{np.ceil(n_por_grupo(0.3, delta=0.1)):.0f} por grupo")
# -> con margen 0,3 y una diferencia real de 0,1 hacen falta 696 por grupo
print(f"con la formula de superioridad para la misma diferencia de 0,1: "
      f"{np.ceil(2 * 1.5**2 * (stats.norm.ppf(0.95) + stats.norm.ppf(0.80))**2 / 0.1**2):.0f} por grupo")
# -> con la formula de superioridad para la misma diferencia de 0,1: 2783 por grupo
```

La primera cifra lo dice todo: pasar de un margen de 0,5 a uno de 0,2 no multiplica el esfuerzo
por 2,5, lo multiplica por 6,2, porque el tamaño va como `1/Δ²`. La segunda es el error caro de
verdad: con una diferencia real de 0,1, el margen útil baja a 0,3 − 0,1 = 0,2 punto, y el estudio
pasa de 310 a 696 observaciones por grupo. Y la comparación final separa las dos preguntas: para
**detectar** una diferencia de 0,1 con la fórmula clásica de superioridad hacen falta 2783
observaciones por grupo, mientras que el TOST con `Δ = 0,3` pide 696 para **descartar** que la
diferencia llegue a 0,3. Son hipótesis invertidas y fórmulas distintas: diseñar un estudio de
equivalencia con la fórmula de superioridad lo deja infrapotenciado, y al revés, gastar la
fórmula del TOST para un ensayo de superioridad es tirar el dinero.
## Errores típicos

- **Confundir «no significativo» con «equivalente».** Es el error central. Un p-valor alto en un
  contraste bilateral solo dice que la muestra no distingue la diferencia de cero, y con poca
  muestra eso pasa con diferencias enormes. La equivalencia se demuestra con un TOST y con el
  intervalo del 90 % dentro del margen, no con un p-valor grande.
- **Usar el intervalo del 95 % para decidir la equivalencia.** El TOST son dos contrastes de una
  cola al 5 %, así que el intervalo que le corresponde es el del 90 %. Con el del 95 % se pierden
  equivalencias verdaderas y el estudio se declara fallido sin motivo.
- **Elegir el margen después de ver los datos.** Es el equivalente exacto del p-hacking: si
  empiezas con `Δ = 0,2`, ves que el intervalo queda en `(−0,4; +0,45)` y lo cambias a 0,5, has
  comprado el resultado. El margen se fija y se justifica antes de mirar nada, y queda escrito en
  el protocolo.
- **Aplicar el TOST con el p-valor bilateral de una librería estándar.** `ttest_ind` devuelve el
  p-valor de dos colas del contraste de igualdad, que no sirve. Hay que construir los dos
  contrastes de una cola con el error típico y los grados de libertad, o usar una función
  específica de TOST.
- **Declarar equivalencia cuando lo que se ha demostrado es no inferioridad.** Si el intervalo
  del 90 % está en `(−0,1; +0,9)` con margen 0,5, el nuevo tratamiento no es inferior, pero no se
  puede afirmar que sea equivalente: la diferencia podría llegar a 0,9. Son dos afirmaciones con
  exigencias distintas y no se pueden intercambiar.
- **Calcular el tamaño muestral con la fórmula de superioridad.** La fórmula de dos medias
  clásica da `n ≈ 2·(z+z)²·σ²/δ²`, y con `δ` la diferencia que quieres detectar, no el margen. Para
  equivalencia el denominador es `Δ − /δ_real/`, que es mucho más pequeño y da un `n` mucho mayor.
  Confundirlas produce estudios infrapotenciados en un factor 3 o más.
- **No informar del margen junto al intervalo.** Un «equivalente» sin el margen y sin el intervalo
  no es un resultado: es una opinión. El lector tiene que poder ver si el intervalo cabía por poco
  o por mucho.

:::practica
enunciado: Una empresa cambia el motor de búsqueda y quiere demostrar que el tiempo de respuesta no es inferior al anterior en más de 10 ms. Mide 60 consultas con cada motor: el nuevo tarda 3,5 ms más de media, con una desviación típica combinada de 12 ms. Calcula el intervalo del 90 % para la diferencia y decide si se puede declarar no inferioridad. Después calcula cuántas consultas harían falta por motor para demostrar equivalencia con un margen de 5 ms si la diferencia real fuera cero.
pista: Para la no inferioridad solo importa el extremo inferior del intervalo del 90 % frente a −10 ms. Para el tamaño muestral usa la fórmula del TOST con Δ = 5 y σ = 12.
solucion: EE = 12·√(1/60 + 1/60) = 12·0,1826 = 2,191 ms, con 118 grados de libertad. El cuantil t de una cola al 5 % es 1,658, así que el intervalo del 90 % es 3,5 ± 1,658·2,191 = 3,5 ± 3,63, es decir (−0,13; +7,13) ms. El límite inferior, −0,13 ms, está muy por encima del margen de no inferioridad, −10 ms: se declara no inferioridad con holgura. Pero no se puede declarar equivalencia con margen 10 ms sin más cuidado, porque el intervalo entero (−0,13; +7,13) sí cae dentro de (−10; +10), así que en este caso la equivalencia también se sostendría; la distinción importa cuando el extremo superior se sale del margen. Para el tamaño muestral con Δ = 5 ms, σ = 12 ms, potencia 0,80 y diferencia real 0: n = 2·144·(1,645+0,842)²/25 = 288·6,185/25 = 71,3, es decir 72 consultas por motor. Con la fórmula de superioridad y una diferencia de 5 ms saldrían 2·6,185·144/25 = 71,3 también, porque aquí la diferencia real es cero y coincide; la diferencia entre las dos fórmulas aparece cuando la diferencia real no es cero, y entonces la de equivalencia pide muchas más.
:::

## Comprueba que lo sabes

:::quiz
p: Un estudio compara dos tratamientos y obtiene p = 0,62 en el contraste bilateral. ¿Qué se puede concluir?
o: Que los dos tratamientos son equivalentes
o: Nada sobre equivalencia: hace falta un margen fijado de antemano, un TOST y el intervalo del 90 % dentro de ese margen
o: Que el estudio está mal hecho
a: 2
e: Un p-valor alto solo dice que la muestra no distingue la diferencia de cero, y con poca muestra eso ocurre incluso con diferencias grandes. Para afirmar equivalencia hay que invertir las hipótesis con un margen preespecificado y comprobar que el intervalo del 90 % cae entero dentro de él. El estudio puede estar perfectamente bien hecho y simplemente no haberse diseñado para demostrar equivalencia.
:::

:::quiz
p: ¿Por qué el intervalo de confianza que decide un TOST con α = 0,05 es el del 90 % y no el del 95 %?
o: Porque el 90 % es más conservador
o: Porque el TOST son dos contrastes de una cola al 5 % y el intervalo equivalente a esa decisión es el de dos colas al 90 %
o: Porque en bioequivalencia siempre se usa el 90 %
a: 2
e: Cada contraste de una cola al 5 % corresponde a un límite del intervalo del 90 %: el inferior y el superior. La equivalencia exige rechazar los dos, así que el intervalo que resume la decisión es el del 90 %. El del 95 % es más ancho y por tanto más exigente: no es «más conservador» en el sentido de proteger mejor, es que rechaza equivalencias que el TOST sí acepta.
:::

:::quiz
p: Un ensayo de no inferioridad tiene margen 0,4 y el intervalo del 90 % de la diferencia sale (−0,1; +0,55). ¿Qué se ha demostrado?
o: Equivalencia, porque el intervalo es pequeño
o: No inferioridad, porque el límite inferior supera −0,4, pero no equivalencia, porque el superior pasa de +0,4
o: Nada, porque el intervalo contiene el cero
a: 2
e: La no inferioridad solo mira un lado: el límite inferior −0,1 está muy por encima del margen −0,4, así que el nuevo tratamiento no es peor de forma relevante. Para declarar equivalencia haría falta que el límite superior también quedara por debajo de +0,4, y está en +0,55. Que el intervalo contenga el cero es irrelevante en no inferioridad: lo que importa es dónde caen los límites respecto al margen.
:::

:::aviso
Las pruebas de equivalencia son el terreno donde más caro sale un margen mal puesto. Un margen
demasiado ancho convierte cualquier cosa en «equivalente» y no informa de nada; uno demasiado
estrecho hace el estudio imposible de financiar. Justificar el margen con criterio externo, y
escribirlo antes de ver los datos, es la parte del trabajo que no se puede automatizar.
:::
