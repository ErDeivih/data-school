---
id: sharpe-deflactado
titulo: Sharpe deflactado
fase: 9
nivel: experto
rutas: [quant, ds]
prerequisitos: [ratio-de-sharpe, data-snooping-y-multiple-testing, asimetria-y-curtosis, intervalos-de-confianza]
tags: [metricas, sesgo, backtest, lopez-de-prado]
resumen: Ajusta el Sharpe observado por el número de intentos y por la forma de la distribución: la probabilidad de que no sea el mejor resultado del ruido.
fuentes: ["Bailey y López de Prado (2014), 'The Deflated Sharpe Ratio'"]
---

## En una frase

El **Sharpe deflactado** (DSR) no es un Sharpe corregido, es una probabilidad: la de que tu
Sharpe sea de verdad mayor que el mejor Sharpe que habrías obtenido probando `N` configuraciones
sin ninguna habilidad, teniendo en cuenta además que tus retornos no son normales.

## La idea

Tienes un Sharpe de 1,5 en el backtest y estás contento. Ahora la pregunta incómoda: ¿cuántas
configuraciones has probado hasta llegar a esta? Si la respuesta es «una, la escribí antes de
mirar los datos», un 1,5 es un 1,5. Si la respuesta es «unas doscientas entre ventanas, umbrales
y filtros», entonces tu 1,5 compite contra el mejor de doscientos intentos, y el mejor de
doscientos intentos **no tiene esperanza cero**. Es el mismo problema del
[[data-snooping-y-multiple-testing|data snooping]], pero con una solución específica para el
Sharpe: en lugar de corregir un p-valor genérico, se calcula directamente cuál es el Sharpe que
esperarías del azar y se mide la distancia a él en unidades de probabilidad.

El DSR hace dos correcciones que van en direcciones distintas:

1. **Selección.** La más importante. Bajo la hipótesis nula (ninguna habilidad), si pruebas `N`
   configuraciones y cada una da un Sharpe estimado con cierto error, el máximo de esos `N`
   valores es positivo por construcción. La fórmula del máximo esperado depende de `N` y de la
   dispersión de los Sharpes entre configuraciones: cuantas más pruebas y más dispares, más alto
   el listón. Con un solo intento el listón es cero.
2. **No normalidad.** El Sharpe es una media dividida por una desviación típica, y su error de
   estimación depende de la forma de la distribución de los retornos. Con asimetría negativa y
   colas gruesas (lo normal en estrategias que venden opciones o compran protección), el error
   crece: el mismo Sharpe vale menos como evidencia.

:::figura
fichero: sharpe-deflactado-el-liston-del-ruido
pie: Con un Sharpe observado de 0,15 y una desviación de 0,05 entre intentos, el listón del ruido cruza el Sharpe observado hacia los 423 intentos y el DSR se hunde por debajo de 0,5. Lo que hunde el resultado no es la estrategia: es haberla buscado más veces.
fuente: figuras/sharpe-deflactado-1.py
:::

El resultado final es un número entre 0 y 1. La lectura práctica: por encima de 0,95 puedes
defender el resultado delante de alguien escéptico; entre 0,5 y 0,9 la estrategia es prometedora
pero no está demostrada; por debajo de 0,5 no has aportado nada que el azar no explique.

El detalle que hace que esto se use poco, y que conviene decir sin rodeos: para calcular el DSR
necesitas la **varianza de los Sharpes de todos los intentos**, no solo el del ganador. Si tu
registro de experimentos es una carpeta con el backtest bueno y nada más, no puedes calcularlo. Y
si te inventas la varianza a ojo, el número que salga no significa nada.

:::trampa
Mezclar frecuencias es el error más frecuente. Si pasas el Sharpe anualizado (por ejemplo 2,4) y
una varianza calculada sobre Sharpes diarios (por ejemplo 0,0025), el Sharpe esperado del ruido te
saldrá cien veces mayor o menor de lo que toca y el DSR será absurdo. Todos los parámetros tienen
que estar en la misma unidad de tiempo: o todo diario, o todo anual.
:::

## Definición formal

Con `N` configuraciones probadas, sea `V[SR_n]` la varianza de los Sharpes estimados entre esas
`N` configuraciones (todos medidos por periodo) y `SR` el Sharpe observado de la mejor, también
por periodo.

El Sharpe que se espera del mejor intento bajo la hipótesis nula de nula habilidad es:

:::formula
SR₀ = √V[SR_n] · [ (1 − γ) · Z⁻¹(1 − 1/N) + γ · Z⁻¹(1 − 1/(N·e)) ]
:::

Y el Sharpe deflactado es la probabilidad de superarlo:

:::formula
DSR = Φ( (SR − SR₀) · √(T − 1) / √( 1 − γ₃·SR + ((γ₄ − 1)/4)·SR² ) )
:::

- `SR` — Sharpe observado de la mejor configuración, **por periodo** (no anualizado).
- `V[SR_n]` — varianza de los Sharpes estimados de las `N` configuraciones, en la misma unidad
  por periodo. Mide cuánto se dispersan tus intentos.
- `N` — número de configuraciones probadas, incluidas las que descartaste.
- `SR₀` — el listón: máximo esperado de `N` estimaciones sin habilidad. Con `N = 1` vale 0.
- `γ` — constante de Euler-Mascheroni, 0,5772.
- `Z⁻¹` — inversa de la función de distribución normal estándar; `Φ` es la normal estándar
  acumulada. `e` es 2,7183.
- `T` — número de observaciones (barras o periodos) de la serie de retornos.
- `γ₃` — asimetría de los retornos; `γ₄` — curtosis **sin restar 3**, de modo que una normal tiene
  `γ₄ = 3`. Si tu programa devuelve curtosis en exceso, hay que sumarle 3.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `N` | Configuraciones probadas, incluidas las descartadas | intentos (recuento) | Sube el listón `SR₀` y el DSR baja: el mejor de muchos intentos tiene un máximo esperado más alto |
| `V[SR_n]` | Varianza de los Sharpes de esos `N` intentos | Sharpe² por periodo | El listón se estira en la misma proporción: con `N = 1` da igual, porque `SR₀` vale 0 |
| `SR` | Sharpe observado de la mejor configuración, por periodo | Sharpe por periodo (0,15 diario, no 2,4 anual) | El DSR sube: es la distancia al listón. Si `SR` cae por debajo de `SR₀`, el DSR baja de 0,5 |
| `T` | Observaciones de la serie de retornos | barras o periodos | El DSR se aleja de 0,5 en la dirección en que ya estaba: más datos hacen más concluyente la misma distancia |
| `γ₃` | Asimetría de los retornos | adimensional | Si es negativa, el denominador crece y el DSR se acerca a 0,5 |
| `γ₄` | Curtosis sin restar 3 (la normal vale 3) | adimensional | Con colas gruesas el denominador crece y el DSR se acerca a 0,5. Pasar la curtosis en exceso (normal = 0) es el error que más lo desvía |
| `γ` | Constante de Euler-Mascheroni, 0,5772 | adimensional | No es un parámetro que se elija: es una constante del máximo esperado de `N` normales |
:::

Tres cosas que se leen directamente en la fórmula:

- Si `SR ≤ SR₀`, el numerador es negativo o nulo y el DSR cae por debajo de 0,5. Es la definición
  formal de «esto lo explica el ruido».
- Cuanto mayor `T`, más se separa el DSR de 0,5 en cualquier dirección: con más datos, la misma
  distancia al listón es más concluyente.
- Si `γ₃` es muy negativa o `γ₄` muy grande, el denominador crece y el DSR se acerca a 0,5. Las
  colas gruesas hacen que el Sharpe sea una medida menos fiable, y la fórmula lo cobra.

## Ejemplo

Supón un backtest diario con `T = 1200` observaciones, un Sharpe observado de 0,15 por día (que
anualizado con `√252` sería 0,15 · 15,87 = 2,38, un número de folleto), una asimetría de −0,5 y
una curtosis de 6. Has probado `N = 100` configuraciones y la desviación típica de sus Sharpes es
0,05, así que `V[SR_n] = 0,0025` y `√V[SR_n] = 0,05`.

- Cuantiles: `Z⁻¹(1 − 1/100) = Z⁻¹(0,99) = 2,3263` y
  `Z⁻¹(1 − 1/(100 · 2,7183)) = Z⁻¹(0,99632) = 2,6802`.
- `SR₀ = 0,05 · (0,4228 · 2,3263 + 0,5772 · 2,6802) = 0,05 · 2,5306 = 0,1265`.
- Numerador: `(0,15 − 0,1265) · √1199 = 0,0235 · 34,627 = 0,8127`.
- Denominador: `√(1 − (−0,5)·0,15 + ((6 − 1)/4)·0,15²) = √(1 + 0,075 + 0,0281) = 1,0503`.
- `DSR = Φ(0,8127 / 1,0503) = Φ(0,7738) = 0,7805`.

Un Sharpe anualizado de 2,38 con un DSR de 0,78: no está demostrado. Y el mismo backtest, con el
mismo 0,15, cambia de veredicto según cuántas veces lo intentaste:

```
intentos   Sharpe del ruido   DSR
       1             0,0000   1,0000
      10             0,0787   0,9906
     100             0,1265   0,7805
    1000             0,1628   0,3370
   10000             0,1930   0,0780
```

Con un solo intento, el DSR es prácticamente 1: el Sharpe por periodo es positivo y hay 1.200
observaciones que lo sostienen. Con mil intentos el listón sube a 0,163, por encima de tu 0,15, y
el DSR se desploma a 0,34. Con diez mil, a 0,08. La estrategia no ha cambiado: lo que ha cambiado
es cuántas veces la has buscado.

## Código

```python verificable
import numpy as np
from statistics import NormalDist

Z = NormalDist()
EULER = 0.5772156649

def sharpe_deflactado(sr, T, intentos, var_sr, sesgo, curtosis):
    """Devuelve (DSR, Sharpe esperado del mejor intento bajo la hipotesis nula)."""
    if intentos > 1:
        sr0 = np.sqrt(var_sr) * ((1 - EULER) * Z.inv_cdf(1 - 1 / intentos)
                                 + EULER * Z.inv_cdf(1 - 1 / (intentos * np.e)))
    else:
        sr0 = 0.0
    denominador = np.sqrt(1 - sesgo * sr + (curtosis - 1) / 4 * sr ** 2)
    return Z.cdf((sr - sr0) * np.sqrt(T - 1) / denominador), sr0

# Todo por periodo: Sharpe diario 0,15 y desviacion tipica de los intentos 0,05.
dsr, sr0 = sharpe_deflactado(sr=0.15, T=1200, intentos=100, var_sr=0.05 ** 2,
                             sesgo=-0.5, curtosis=6.0)
print(f"Sharpe esperado del mejor de 100 intentos: {sr0:.4f}")   # -> 0.1265
print(f"DSR: {dsr:.4f}")                                       # -> 0.7805
```

:::claves
- `sharpe_deflactado` devuelve una **tupla** de dos números, no el DSR a secas: `dsr, sr0 = ...`.
  Si te quedas con el primero sin desenvolver, lo que recibes es la tupla y cualquier cuenta
  posterior falla.
- La rama `if intentos > 1` es obligatoria, no una precaución: con `intentos = 1` la fórmula
  pediría `Z⁻¹(1 − 1/1) = Z⁻¹(0)`, y `NormalDist.inv_cdf(0)` lanza un error. Por eso el listón se
  define como cero a mano.
- `Z.inv_cdf` y `Z.cdf` son de `statistics`, no de NumPy: reciben y devuelven `float` de Python, y
  su argumento es una **probabilidad** (0 a 1), no un número de desviaciones. `Z.inv_cdf(0,99)`
  devuelve 2,3263.
- El denominador usa `curtosis` **en bruto**: con `curtosis = 6,0` está diciendo «curtosis 6, la
  normal vale 3». Si tu serie viene de `pandas` o `scipy`, esas dos devuelven curtosis **en
  exceso** y hay que pasar `6,0 - 3,0`: si no, el denominador sale distinto y el DSR cambia.
- `var_sr=0.05 ** 2` es la varianza, no la desviación. Si pasas `0,05` en su lugar, el listón se
  multiplica por `√(1/0,05) = 4,47`: pasa de 0,1265 a 0,566 y el DSR se hunde. Es el error de
  unidades que la propia fórmula castiga.
- Los argumentos van por nombre (`sr=`, `T=`, `intentos=`), así que el orden no importa; lo que sí
  importa es que `sr` esté **por periodo**. El mismo 0,15 diario es 2,38 anual, y si metes el anual
  con la varianza diaria el DSR no significa nada.
:::

```python verificable
import numpy as np
from statistics import NormalDist

Z = NormalDist()
EULER = 0.5772156649

def dsr(sr, T, intentos, var_sr, sesgo, curtosis):
    if intentos > 1:
        sr0 = np.sqrt(var_sr) * ((1 - EULER) * Z.inv_cdf(1 - 1 / intentos)
                                 + EULER * Z.inv_cdf(1 - 1 / (intentos * np.e)))
    else:
        sr0 = 0.0
    den = np.sqrt(1 - sesgo * sr + (curtosis - 1) / 4 * sr ** 2)
    return Z.cdf((sr - sr0) * np.sqrt(T - 1) / den), sr0

# El mismo backtest, el mismo Sharpe, distinto numero de intentos.
print("intentos  Sharpe del ruido  DSR")
for intentos in (1, 10, 100, 1000, 10000):
    valor, sr0 = dsr(0.15, 1200, intentos, 0.05 ** 2, -0.5, 6.0)
    print(f"{intentos:>8}  {sr0:>16.4f}  {valor:.4f}")
# con 1 intento el DSR es 1.0000; con 10000 baja a 0.0780
```

## Errores típicos

- **Mezclar unidades temporales.** El Sharpe, su varianza y el número de observaciones tienen que
  estar en la misma frecuencia. Si el Sharpe es anual y `V[SR_n]` se calculó con Sharpes diarios,
  el listón sale desproporcionado y el DSR no significa nada.
- **No registrar la varianza de los intentos.** `V[SR_n]` es un dato experimental, no una
  estimación de conveniencia: si solo guardaste el mejor backtest, el DSR no se puede calcular.
  Llevar un registro de todos los experimentos con su Sharpe es el requisito previo, y es lo que
  casi nadie hace.
- **Poner `N` igual al número de variantes que aparecen en el informe.** Los intentos son todos
  los que ejecutaste, incluidos los que abandonaste a mitad y los cambios de periodo o de
  universo. Subestimar `N` es subestimar el listón, que es justo lo que el método quiere evitar.
- **Pasar la curtosis en exceso.** `pandas` y `scipy` devuelven por defecto la curtosis en exceso
  (la normal vale 0). En la fórmula, la normal vale 3. Si no sumas 3, el denominador cambia y el
  DSR se va.
- **Leer el DSR como probabilidad de ganar dinero.** El DSR es la probabilidad de que el Sharpe
  supere el listón del ruido. Una estrategia con un Sharpe enorme pero colas terribles puede tener
  un DSR alto y arruinarte igual: eso lo cuentan [[maximo-drawdown|la caída máxima]] y
  [[var-y-cvar|el CVaR]], no el Sharpe.
- **Aplicarlo a un backtest contaminado.** Si hay [[sesgo-de-mirar-al-futuro|fuga de información]]
  o el universo tiene [[sesgo-de-supervivencia|sesgo de supervivencia]], ninguna corrección
  arregla el número: el DSR mide selección estadística, no errores de construcción.

:::practica
enunciado: Un backtest diario de T = 750 barras da un Sharpe de 0,12 por día, con asimetría −0,8 y curtosis 7. Probaste N = 50 configuraciones y la desviación típica de sus Sharpes es 0,04. Con Z⁻¹(0,98) = 2,054 y Z⁻¹(1 − 1/(50 · e)) = 2,440, calcula el listón SR₀ y decide si el Sharpe lo supera.
pista: SR₀ = √V[SR_n] · [(1 − γ) · Z⁻¹(1 − 1/N) + γ · Z⁻¹(1 − 1/(N · e))], con γ = 0,5772 y todo por periodo.
solucion: √V[SR_n] = 0,04, así que SR₀ = 0,04 · (0,4228 · 2,054 + 0,5772 · 2,440) = 0,04 · 2,2768 = 0,0911. El Sharpe lo supera por 0,0289: el numerador del DSR vale 0,0289 · √749 = 0,79 y el denominador √(1 + 0,096 + 0,0216) = 1,057, con lo que el argumento queda en 0,748 y el DSR en 0,77. Prometedor, no demostrado.
:::

## Comprueba que lo sabes

:::quiz
p: Dos analistas obtienen el mismo Sharpe por periodo, 0,15, con la misma serie de 1.200 días y la misma forma de distribución. Uno probó 10 configuraciones y el otro 10.000. ¿Qué diferencia hay en el DSR?
o: Ninguna: el DSR depende del Sharpe, del número de observaciones, de la asimetría y de la curtosis, no de los intentos
o: El primero obtiene un DSR en torno a 0,99 y el segundo en torno a 0,08, porque el listón del ruido sube con el número de intentos
o: El DSR del segundo es mayor, porque ha explorado más el espacio de estrategias
a: 2
e: El Sharpe esperado del mejor intento crece con N: vale 0,079 con 10 intentos, 0,126 con 100, 0,163 con 1.000 y 0,193 con 10.000. Con el Sharpe observado fijo en 0,15, a partir de unos mil intentos el listón lo supera y el DSR cae por debajo de 0,5. Buscar más no mejora el resultado, lo debilita como evidencia.
:::

:::quiz
p: ¿Por qué el DSR incluye un término con la asimetría y la curtosis de los retornos?
o: Porque el Sharpe solo está definido para distribuciones normales y hay que corregirlo para que sea válido
o: Porque el error de estimación del Sharpe depende de la forma de la distribución, y con asimetría negativa y colas gruesas el mismo Sharpe es menos fiable
o: Porque la curtosis alta aumenta el rendimiento esperado y hay que descontarlo
a: 2
e: El Sharpe se puede calcular con cualquier distribución, pero su precisión como estimador empeora cuando la distribución se aleja de la normal: media y desviación típica dejan de resumir bien el riesgo. La fórmula lo refleja en el denominador, que crece y empuja el DSR hacia 0,5. No hay ningún ajuste de rendimiento esperado.
:::

:::quiz
p: ¿Qué es `V[SR_n]` y por qué es el requisito práctico más incómodo del método?
o: La varianza de los retornos de la estrategia, que se estima con la propia serie
o: La varianza de los Sharpes estimados entre todas las configuraciones probadas, que obliga a haber registrado todos los intentos
o: La varianza del error de predicción del modelo
a: 2
e: Es la dispersión de los Sharpes de tus N intentos, y entra en la fórmula como escala del máximo esperado. No se puede estimar a partir del backtest ganador: exige llevar un registro de cada configuración ejecutada con su Sharpe. Sin ese registro, o no hay DSR, o hay un número inventado.
:::
