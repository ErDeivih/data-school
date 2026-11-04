---
id: logaritmos-y-escalas-logaritmicas
titulo: Logaritmos y escalas logarítmicas
fase: 1
nivel: básico
rutas: [core, ds]
prerequisitos: [notacion-matematica]
tags: [matematicas, escala, logaritmos, visualizacion]
resumen: Un logaritmo cuenta multiplicaciones en vez de sumas, y una escala logarítmica pone factores iguales a distancias iguales para que quepan órdenes muy distintos.
fuentes: ["Stewart (2018), 'Cálculo de una variable: trascendentes tempranas'", "Cleveland (1993), 'Visualizing Data'", "Python Software Foundation (2025), 'math — Mathematical functions'"]
---

## En una frase

Un logaritmo responde a «¿cuántas veces hay que multiplicar la base para llegar a este número?», y
una escala logarítmica dibuja factores iguales a distancias iguales, que es lo que permite poner en
el mismo gráfico un valor de 10 y otro de 10 millones sin que el primero desaparezca.

## La idea

Nadie dice «tengo diez millones de veces más». Decimos «un millón de veces más», contamos
multiplicaciones. Con el dinero pasa lo mismo: un piso que sube un 5 % multiplica el precio por 1,05,
y dos pisos distintos se comparan por su factor, no por su diferencia. Los decibelios, el pH, la
magnitud de un terremoto, el tamaño de un fichero en KB, MB y GB, la latencia en microsegundos y
milisegundos: todo eso son escalas logarítmicas disfrazadas, y todas existen por el mismo motivo.

El motivo es que una escala lineal está pensada para **sumar**. Dos centímetros más son dos
centímetros más estés donde estés. Pero hay magnitudes que se comportan multiplicando, y ahí la
distancia lineal miente: de 1 a 1.000.000 de habitantes hay un millón de habitantes de diferencia, y
de 1.000.000 a 2.000.000 hay otro millón, aunque uno sea una ciudad y el otro el doble de la misma
ciudad. La pregunta que ordena esto es «¿cuántos ceros?», y esa pregunta tiene nombre: `log10`.

Un logaritmo es la operación inversa de la potencia, igual que la resta lo es de la suma. Y tiene una propiedad que lo convierte en la herramienta natural para lo que crece
multiplicándose: **multiplicar dos números se convierte en sumar sus logaritmos**, y dividir, en
restar. Esa es toda la gracia, y es lo que se desarrolla en la definición formal.

Con esa propiedad, si algo crece un porcentaje fijo cada periodo, en una escala logarítmica sale una
recta: cada paso añade la misma cantidad al logaritmo. Y por eso también un eje logarítmico se lee en
factores: la distancia entre 1 y 10 es la misma que entre 10 y 100, y la misma que entre 100.000 y
1.000.000.
La base solo cambia la unidad. Base 10 cuenta órdenes de magnitud (y responde a «cuántos ceros»),
base 2 cuenta doblajes y es la de la informática (diez bits cubren 1.024 combinaciones), y base `e`
es la del crecimiento continuo y el cálculo, que es la que aparece en
[[retornos-logaritmicos|los retornos logarítmicos]] y en [[entropia-e-informacion|la entropía]].

:::trampa
«Logaritmo» sin base es una frase a medias. En matemáticas puras `log` suele ser el neperiano, en
ingeniería es el decimal y en informática el binario. Un mismo dato cambia de número según la base, y
comparar dos series construidas con bases distintas es comparar centímetros con pulgadas.
:::

## Definición formal

El logaritmo en base `b` de un número `x` es el exponente al que hay que elevar `b` para obtener `x`:

:::formula
log_b(x) = y   ⟺   b^y = x
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `b` | Base del logaritmo: 10, 2 o el número `e` (≈ 2,718) | ninguna | Con una base mayor, el mismo número da un logaritmo más pequeño: cambia la unidad de medida, no la forma de la curva |
| `x` | El número del que se toma el logaritmo | las de la variable, o ninguna | El logaritmo sube mucho más despacio: multiplicar `x` por la base suma 1 al logaritmo, sumar 1 a `x` casi no lo mueve |
| `y` | El logaritmo: cuántas veces se multiplica la base | ninguna (es un exponente) | Es la distancia en el papel. Un `y` más alto no dice «más cantidad», dice «más multiplicaciones» |
:::

Propiedades que se usan a diario, todas consecuencias de la definición, y que conviene tener en
bloque porque son las que se aplican al vuelo:

:::formula
log(x · y) = log(x) + log(y)      log(x / y) = log(x) − log(y)
log(x^k) = k · log(x)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `x`, `y` | Dos números positivos cualesquiera de los que se toma el logaritmo | las de la variable, o ninguna | El logaritmo de su producto, de su cociente o de su potencia se calcula con sumas, restas y productos: nunca hace falta multiplicar los originales |
| `k` | Exponente al que se eleva `x` | ninguna | Baja fuera del logaritmo: multiplicar la potencia por 2 solo duplica el logaritmo |
| `log` | Logaritmo en una base cualquiera, siempre la misma en los dos lados | ninguna | La base no cambia las propiedades: valen para base 10, 2 o `e`. Sí cambia el número que sale |
:::

Y dos casos límite que se usan para recordar la forma de la curva: el logaritmo de 1 es 0 en cualquier
base, y el logaritmo no existe en 0 —la curva se escapa hacia abajo sin tocarlo— ni en los números
negativos.

La tercera fórmula es la que se usa para **leer un eje logarítmico**. Si dos marcas están separadas
por `d` pasos de la base, los valores se relacionan así:

:::formula
x₂ = x₁ · b^(d₂ − d₁)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `x₁`, `x₂` | Los dos valores que se comparan en el eje | las de la variable | Lo que importa no es su diferencia, sino su cociente: el eje mide `x₂ / x₁` |
| `d₂ − d₁` | La distancia medida sobre el papel | pasos de la base: décadas si `b` es 10, doblajes si es 2 | Cada paso más multiplica el valor, no lo incrementa: es la lectura directa del gráfico |
| `b` | La base de la escala | ninguna | Fija cuánto vale un paso: con base 10, un paso es multiplicar por 10; con base 2, por 2 |
:::

La consecuencia es el detalle que más veces se lee mal: el punto **visualmente** central de un eje
logarítmico que va de `x₁` a `x₂` es la raíz de su producto (su media geométrica), no la media
aritmética de los dos. Un eje de 1 a 1.000 tiene su mitad en 31,6.

:::figura
fichero: logaritmos-escala-lineal-y-logaritmica
pie: Arriba, la misma serie de casos dibujada dos veces: con el eje lineal, los primeros pasos son invisibles y el último se lleva todo el alto; con el eje logarítmico sale una recta, porque multiplicar por lo mismo ocupa siempre lo mismo. Abajo, la curva de log10 de x: cada multiplicación por 10 sube exactamente un escalón, el logaritmo de 1 es 0 en cualquier base y en 0 la curva no existe.
fuente: figuras/logaritmos-y-escalas-logaritmicas-1.py
:::

## Ejemplo

Cuatro importes: 1, 10, 100 y 1.000 euros.

En una escala lineal, los tres primeros son invisibles: son el 0,1 %, el 1 % y el 10 % del eje. En
una escala logarítmica ocupan el mismo tramo: sus logaritmos decimales son 0, 1, 2 y 3, cuatro
posiciones equiespaciadas.

| Resumen de los cuatro valores | Resultado | Qué pregunta responde |
| --- | --- | --- |
| Media aritmética | 277,75 € | Si los cuatro importes se repartieran a partes iguales |
| Mediana | 55 € | Cuál es el valor central del conjunto ordenado |
| Media geométrica | 31,62 € | Cuál es el valor central cuando se mide en factores |
| Mitad visual del eje de 1 a 1.000 | 31,6 | Dónde queda el centro de un eje logarítmico |

Fíjate en que la media geométrica y la mitad visual del eje coinciden, y hay una razón: la media
geométrica es la media de los logaritmos devuelta a la escala original, y eso mismo es el centro de
un eje
logarítmico. Ninguna de las dos es «la correcta»: 277,75 € responde a la pregunta
de repartir, y 31,62 € responde a la pregunta de comparar factores. Lo que no se puede hacer es
promediar logaritmos y creer que has promediado euros.

Un segundo caso, con una tasa de crecimiento. Un 7 % anual se convierte en una recta cuya pendiente
es el logaritmo decimal de 1,07, que vale 0,0294 por año. Diez años son 0,294 décadas, es decir un
factor de 1,97: el capital casi se dobla. Y el logaritmo decimal de un millón es 6, que es la forma
rápida de decir «seis ceros».

## Código

```python verificable
import numpy as np

# Cuatro valores muy dispares: 1, 10, 100 y 1000. En escala logaritmica ocupan lo mismo.
valores = np.array([1.0, 10.0, 100.0, 1000.0])
logaritmos = np.log10(valores)
print("log10 de cada valor:", logaritmos)
print("media aritmetica  :", round(float(valores.mean()), 2))
print("media geometrica  :", round(float(10.0 ** logaritmos.mean()), 2))
print("log10(100*1000)   :", np.log10(100 * 1000), "=", np.log10(100) + np.log10(1000))
```

```python verificable
import numpy as np

# Un crecimiento multiplicativo constante es una recta en escala logaritmica: los pasos
# de log10 son todos iguales. La recta no dice "suma", dice "multiplica por lo mismo".
capital = 100.0 * 1.26 ** np.arange(6)
print("capital por paso:", np.round(capital, 1))
print("pasos de log10  :", np.round(np.diff(np.log10(capital)), 3))

# El punto medio VISUAL de un eje logaritmico no es la media de los extremos: es su raiz.
print("mitad de 1 a 1000:", round(float(np.sqrt(1 * 1000)), 1), "y no 500")

# Aviso numerico: log(1+x) se come los incrementos diminutos y log1p no.
print("log(1 + 1e-16)   :", np.log(1 + 1e-16))
print("log1p(1e-16)     :", np.log1p(1e-16))
```

:::claves
- `np.log10` es el logaritmo decimal, `np.log` es el neperiano y `np.log2` el binario. Elegir mal la
  base no da un error: da otro número, y hay que saber con cuál estás trabajando.
- `valores.mean()` y `10 ** logaritmos.mean()` no son lo mismo y la diferencia no es un redondeo:
  277,75 frente a 31,62. El segundo es la media geométrica, que es lo que quieres cuando la magnitud
  se comporta multiplicándose.
- La identidad `log10(100 * 1000) == log10(100) + log10(1000)` se cumple con exactitud de coma
  flotante porque ambos lados valen 5. Es la propiedad que convierte productos en sumas.
- `log1p(x)` calcula `log(1 + x)` sin perder precisión cuando `x` es diminuto. Con `x = 1e-16`,
  `1 + x` se redondea a 1 y el logaritmo sale 0: el incremento desaparece. Es el mismo problema de
  precisión que describe [[precision-y-error-numerico]].
- `np.log(0)` no lanza una excepción: devuelve `-inf` con un aviso. Y `np.log(-1)` devuelve `nan`. Los
  ceros y los negativos hay que tratarlos antes, no después.
- La raíz cuadrada del producto de los extremos es el punto medio de un eje logarítmico: con 1 y
  1.000 sale 31,6 en lugar de 500. Cualquier gráfico con eje logarítmico se lee con esa regla.
:::

:::truco
Para una variable con ceros (número de incidencias, de clics, de accesos), la transformación que se
usa no es `log(x)` sino `log(1 + x)`: mantiene el cero en cero y comprime la cola. En Pandas y NumPy
está escrita de forma precisa como `np.log1p(x)`, y después toca revisar cuántos valores han quedado
fuera, igual que con cualquier transformación.
:::

## Errores típicos

- **Meter ceros o negativos en un logaritmo.** `log(0)` no existe y el resultado es `-inf`; `log` de
  un negativo es `nan`. No hay error visible: aparecen huecos o infinitos en medio de la serie.
- **Leer la mitad del eje como la mitad del valor.** En un eje de 1 a 1.000 el centro es 31,6, no
  500. Comparar distancias en el papel como si fueran diferencias absolutas es la forma más rápida de
  sacar una conclusión falsa de un gráfico.
- **Decir «log» sin decir la base.** El mismo dato vale 3 en base 10, 9,97 en base 2 y 6,91 en base
  `e`. Comparar pendientes de dos gráficos construidos con bases distintas no significa nada.
- **Promediar logaritmos y creer que has promediado los datos.** La media de los logaritmos devuelta a
  la escala original es la media geométrica, que es la respuesta correcta para factores y la
  equivocada para dinero. Elige la pregunta antes que la fórmula.
- **Confundir cualquier recta en una escala logarítmica con un crecimiento exponencial.** Una recta
  en un gráfico semilog significa un factor constante por paso; un crecimiento que se frena también
  puede parecer recto si el tramo es corto. Mira el rango completo antes de afirmarlo.
- **Aplicar el logaritmo y no revisar qué ha pasado con los ausentes.** La transformación crea nulos
  silenciosos allí donde había ceros, y a partir de ahí todo lo que calcules —correlaciones, medias,
  modelos— se hace sobre un subconjunto distinto del que crees. Es el mismo problema que trata
  [[missing-data]].
- **Usar la escala logarítmica para esconder datos incómodos.** Comprime las colas, que es lo que
  queremos, pero también puede disimular que dos series se separan. Si una conclusión depende de la
  escala, hay que enseñar las dos versiones.

## Comprueba que lo sabes

:::quiz
p: Un eje logarítmico va de 1 a 1.000. ¿Qué valor queda en su punto medio visual?
o: 500, porque es la media entre los dos extremos
o: 31,6, porque la distancia es logarítmica y el centro es la raíz del producto
o: 100, porque es la marca que hay a un tercio del eje
a: 2
e: En un eje logarítmico, distancias iguales son factores iguales, así que el centro es la media geométrica: la raíz de 1 por 1.000, que es 31,6. La media aritmética (500) sería el centro de un eje lineal, y 100 es simplemente una de las marcas de década.
:::

:::quiz
p: ¿Qué significa que una serie salga recta en un gráfico con el eje vertical logarítmico?
o: Que crece multiplicándose por un factor parecido en cada paso
o: Que crece sumando la misma cantidad en cada paso
o: Que los datos son normales
a: 1
e: En una escala logarítmica, una recta quiere decir que el logaritmo crece con pendiente constante, y eso equivale a multiplicar por un factor fijo en cada paso: un crecimiento porcentual estable. Sumar una cantidad fija daría una curva que se aplana, no una recta.
:::

:::quiz
p: Tienes una columna con el número de incidencias diarias de un servicio, y muchos días valen 0. ¿Qué haces antes de dibujarla en escala logarítmica?
o: Sumar 1 a todos los valores y usar la escala logarítmica, revisando después cómo queda el cero
o: Quitar los días con cero, porque no aportan información
o: Dibujarla en escala lineal, porque con ceros no se puede
a: 1
e: El logaritmo de 0 no existe, así que la convención habitual es trabajar con log(1 + x), que deja el cero en cero y comprime la cola. Borrar los ceros cambia el significado de la serie: esos días sin incidencias son el mejor dato que tienes. Y en escala lineal la serie con picos de dos órdenes de magnitud es ilegible.
:::

:::practica
enunciado: Los tiempos de respuesta de una API van de 3 milisegundos a 40 segundos, con la mayoría por debajo de 200 milisegundos. Explica por qué un histograma en escala lineal no sirve, qué escala usarías y cómo leerías el resultado, sabiendo que el eje va de 1 milisegundo a 100 segundos.
pista: Cuenta cuántas décadas hay entre el mínimo y el máximo, y piensa dónde cae el centro del eje si es logarítmico.
solucion: Entre 3 milisegundos y 40 segundos hay más de cuatro órdenes de magnitud (de 3 a 40.000 milisegundos), así que en un eje lineal todas las observaciones por debajo de 200 milisegundos se apiñan en el primer 0,2 % del eje y el resto parece una cola inexistente. La escala adecuada es logarítmica en el eje de los tiempos, con contenedores del histograma también logarítmicos (por ejemplo, uno por década o varios por década): así cada intervalo abarca el mismo factor y todas las zonas tienen resolución. Para leerlo: el eje va de 1 a 100.000 milisegundos, o sea cinco décadas, y su centro visual es la raíz de 1 por 100.000, unos 316 milisegundos; que la masa esté a la izquierda de esa marca significa que la mayoría de las llamadas van más rápido que un tercio de segundo, y la cola de la derecha se lee como «cuántas llamadas multiplican por 10 el tiempo típico», no como «cuántos milisegundos de más».
:::

:::nota
La escala logarítmica no inventa información ni la esconde por sí sola: cambia la pregunta que
responde el gráfico, de «cuánto más» a «cuántas veces más». Casi todos los datos que genera una
máquina —tamaños, tiempos, conteos, poblaciones— se entienden mejor en la segunda.
:::
