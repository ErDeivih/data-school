---
id: medidas-de-centralidad
titulo: Medidas de centralidad
fase: 1
nivel: básico
rutas: [core, ds]
prerequisitos: [notacion-matematica]
tags: [estadistica, descriptiva, resumen]
resumen: Media, mediana y moda resumen un conjunto de datos en un solo número, y cada una miente de una forma distinta.
fuentes: ["Tukey (1977), 'Exploratory Data Analysis'"]
---

## En una frase

La media, la mediana y la moda son tres formas de responder a «¿cuál es el valor típico?», y
eliges una u otra según lo que quieras protegerte: la media usa toda la información pero se
deja arrastrar por un solo dato raro; la mediana ignora los extremos y por eso es robusta.

## La idea

Imagina que quieres saber cuánto gana la gente en tu ciudad. Preguntas a 9 vecinos y sus
salarios son: 1.200, 1.300, 1.400, 1.500, 1.600, 1.700, 1.800, 1.900 y 2.000 euros. La media
es 1.600 y la mediana también. Nadie discute.

Ahora supón que en esa lista vivía alguien que no contestó: un jugador de fútbol que gana
40.000 euros al mes. La media salta a 5.440 euros, pero la mediana apenas se mueve: pasa de
1.600 a 1.650, porque los dos valores centrales de los diez pasan a ser 1.600 y 1.700. ¿Cuál
de las dos describe mejor «lo típico»? La mediana, sin duda: 9 de los 10 vecinos ganan menos
que la media. Ese es el problema central de este concepto: **la media es un punto de
equilibrio, no un valor representativo**. Se mueve hasta que el total de lo que está por
encima compensa el total de lo que está por debajo, y un solo valor enorme puede empujarla
donde quiera.

La moda es la tercera respuesta y la más primitiva: el valor que más se repite. En datos
continuos casi nunca sirve (¿cuántas personas ganan exactamente 1.600,00 €?), pero en datos
categóricos es la única que tiene sentido: la moda de «color de coche» es el color más
vendido, y ahí la media no existe.

Una forma de recordar cuál usar: **la media es para sumas (lo que se reparte), la mediana
para posiciones (lo que ordena), y la moda para categorías.**

:::figura
fichero: centralidad-media-fragil-mediana-robusta
pie: Arriba, los nueve vecinos y el sueldo del jugador: la línea roja (la media, 5.440 €) cae en una zona donde no vive nadie, mientras la verde (la mediana) se queda entre la gente. Abajo, la escalera de sueldos ordenados: la mediana cae entre el 5.º y el 6.º, y la media no cae sobre ningún vecino. Si publicas «sueldo medio», describes el total repartido, no a una persona.
fuente: figuras/medidas-de-centralidad-1.py
:::

## Definición formal

Con `n` observaciones `x₁, x₂, …, xₙ`:

- **Media aritmética:** x̄ = (1/n) · Σᵢ xᵢ. Es el valor que iguala la suma total si todas
  las observaciones valieran lo mismo. Aquí `Σᵢ` significa «suma de todos los valores desde
  i = 1 hasta i = n».
- **Mediana:** el valor que deja la mitad de los datos por debajo. Con los datos ordenados,
  si `n` es impar es el que ocupa la posición (n+1)/2; si `n` es par, la media de los dos
  centrales.
- **Moda:** el valor con mayor frecuencia. Puede haber varias (distribución bimodal) o
  ninguna si todos los valores son distintos.

Propiedades que conviene tener presentes:

1. La media es el único de los tres que **usa todos los valores**, y por eso es la más
   eficiente cuando los datos son limpios, y la más frágil cuando no lo son.
2. La media es sensible a la escala: si multiplicas todos los datos por 10, la media se
   multiplica por 10 y la mediana también. Pero si sumas 100 a todos, ambas suman 100.
3. La media **minimiza la suma de las diferencias al cuadrado**; la mediana **minimiza la
   suma de las diferencias absolutas**. De ahí sale su robustez: elevar al cuadrado castiga
   muchísimo los valores extremos, el valor absoluto no.
4. Con distribuciones asimétricas hacia la derecha (salarios, precios de vivienda, tiempos
   de espera) se cumple aproximadamente: **moda < mediana < media**.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Número de observaciones que entran en el resumen | ninguna (recuento) | No cambia el valor de la media ni el de la mediana, pero sí su estabilidad: con `n = 5` un solo valor extremo manda, con `n = 5.000` casi no se nota |
| `xᵢ` | Cada uno de los valores observados | las de la variable (euros, segundos, kg) | Un `xᵢ` disparado sube la media en `xᵢ/n` y deja la mediana igual, salvo que sea tan grande que cruce la mitad de la lista: es el 40.000 € del ejemplo |
| `x̄` | La media aritmética, `(1/n) · Σᵢ xᵢ` | las de la variable | Es el resultado, no una palanca. Se mueve con cualquier `xᵢ`, aunque solo sea uno, y por eso no dice qué es «lo típico» |
| `Σᵢ` | La suma de todos los valores, de `i = 1` a `i = n` | las de la variable | Al añadir un dato, el sumatorio crece (o decrece) y la media se recoloca; la mediana solo cambia si el nuevo valor cae en el centro de la lista |
| `x₍₁₎, x₍₂₎, …, x₍ₙ₎` | Los mismos valores, ya ordenados de menor a mayor | las de la variable | Es el orden, no el valor, lo que decide la mediana: multiplicar todos los datos por 100 deja la mediana en la misma posición, y la media se multiplica por 100 |
| `moda` | El valor que más veces aparece | las de la variable | Puede no existir (todos distintos) o haber varias (dos montañas). Con datos continuos no sirve: casi ningún sueldo se repite al céntimo |
:::

## Ejemplo

Salarios mensuales, en euros, de un equipo de 7 personas:

```
1.800  1.900  2.000  2.100  2.200  2.400  9.000
```

- Media: (1.800 + 1.900 + 2.000 + 2.100 + 2.200 + 2.400 + 9.000) / 7 = 21.400 / 7 = **3.057 €**
- Mediana: el valor central de los 7 ordenados = **2.100 €**
- Moda: no hay (todos distintos)

La media (3.057) está por encima de 6 de las 7 personas. Si publicas «salario medio: 3.057 €»
estás diciendo algo técnicamente cierto y prácticamente engañoso. El salario mediano, 2.100 €,
es el que describe al equipo. Este es exactamente el motivo de que los organismos oficiales
publiquen **salario mediano** y no medio.

## Código

```python verificable
import numpy as np

salarios = np.array([1800, 1900, 2000, 2100, 2200, 2400, 9000])

print(f"media   {salarios.mean():>8.0f}")     # -> 3057
print(f"mediana {np.median(salarios):>8.0f}")  # -> 2100

# Cuántas personas ganan menos que la media: la media no representa a la mayoría
print("por debajo de la media:", int((salarios < salarios.mean()).sum()), "de", salarios.size)  # -> 6 de 7
```

:::claves
- `salarios.mean()` devuelve un `float` de Python y **no** toca el array: `mean` no es de los métodos que modifican en el sitio (los que sí lo hacen, como `sort()` o `fill()`, acaban en `_` o se anuncian). Puedes llamarlo las veces que quieras.
- `np.array([1800, 1900, ...])` guarda enteros, pero `mean()` siempre devuelve coma flotante porque suma y divide. Si el array fuera de verdad todo entero y usaras `//`, el resultado se truncaría sin avisar: 21.400 // 7 daría 3.057 y 21.401 // 7 seguiría dando 3.057.
- `np.median` **no** ordena tu array: trabaja sobre una copia (internamente hace `np.partition`). Si quieres comprobarlo, imprime `salarios` antes y después: sale en el mismo orden en que lo escribiste.
- `salarios < salarios.mean()` no da un `True` ni un `False`: da un array de booleanos, uno por sueldo. Comparar un array con un número se aplica a cada elemento.
- `.sum()` sobre ese array de booleanos cuenta los `True` (cada uno vale 1), y devuelve un entero de NumPy. Por eso el `int(...)` de fuera solo sirve para que el `print` no muestre `np.int64(6)`.
- `salarios.size` es el número de elementos y `len(salarios)` da lo mismo para un vector, pero dejan de coincidir en cuanto el array tiene dos dimensiones: en uno de forma `(7, 1)`, `size` vale 7 y `len` también, mientras que en uno de `(2, 7)` el `len` es 2.
:::

```python verificable
import numpy as np

# La media minimiza la suma de cuadrados; la mediana, la suma de valores absolutos.
datos = np.array([1800.0, 1900, 2000, 2100, 2200, 2400, 9000])
candidatos = np.linspace(1500, 3500, 2001)

cuadrados = [((datos - c) ** 2).sum() for c in candidatos]
absolutos = [np.abs(datos - c).sum() for c in candidatos]

print("minimiza cuadrados:", round(candidatos[int(np.argmin(cuadrados))]))   # -> 3057  (la media)
print("minimiza absolutos:", round(candidatos[int(np.argmin(absolutos))]))   # -> 2100  (la mediana)
```

## Errores típicos

- **Usar la media con datos asimétricos.** Con ingresos, precios de vivienda, tiempos de
  respuesta o visitas a urgencias, la media queda por encima de la mayoría. Usa la mediana y,
  mejor aún, muestra la distribución.
- **Decir «la media de los salarios es X, así que el trabajador típico gana X».** La media no
  describe a nadie en particular. Es una afirmación sobre el total repartido, no sobre una
  persona.
- **Promediar medias sin ponderar.** Si un grupo tiene 10 personas y otro 1.000, la media de
  las dos medias no es la media global. Hay que ponderar por tamaño:
  (n₁·x̄₁ + n₂·x̄₂) / (n₁ + n₂).
- **Calcular la media de una variable categórica codificada con números.** El «código postal
  medio» o el «estado civil medio» (1 = soltero, 2 = casado) no significan nada.
- **Confundir moda con mayoría.** La moda es el valor más frecuente, aunque solo aparezca 3
  veces de 100. Si necesitas «la categoría mayoritaria», comprueba su proporción.
- **Borrar los outliers para que la media quede bonita.** Si son errores de medición, se
  corrigen; si son reales, son parte del fenómeno y la mediana ya los maneja.

:::practica
enunciado: En una empresa, 12 personas cobran un salario medio de 2.100 € y 4 personas cobran una media de 3.600 €. Calcula el salario medio global, compáralo con el promedio simple de las dos medias y di cuál de los dos números describe a la plantilla.
pista: La media global pondera cada grupo por su tamaño, no por el número de grupos que hay.
solucion: Media global = (12 · 2.100 + 4 · 3.600) / 16 = (25.200 + 14.400) / 16 = 39.600 / 16 = 2.475 €. El promedio simple de las dos medias, (2.100 + 3.600) / 2 = 2.850 €, está 375 € por encima, porque da al grupo de 4 personas el mismo peso que al de 12. Conclusión: el número correcto es 2.475 €; publicar 2.850 € sería describir una plantilla que no existe.
:::

## Comprueba que lo sabes

:::quiz
p: Siete personas ganan 1.800, 1.900, 2.000, 2.100, 2.200, 2.400 y 9.000 €. ¿Qué afirmación es correcta?
o: La media (3.057 €) describe mejor al grupo porque usa todos los datos
o: La mediana (2.100 €) describe mejor al grupo porque no la arrastra el valor extremo
o: La moda (2.100 €) es la mejor medida porque es el valor más repetido
a: 2
e: Con un valor extremo, la media se desplaza por encima de 6 de las 7 personas. La mediana es robusta porque solo depende del orden. La moda no existe aquí: los siete valores son distintos.
:::

:::quiz
p: ¿Por qué la mediana es más robusta que la media frente a valores extremos?
o: Porque ignora los valores pequeños
o: Porque minimiza la suma de diferencias absolutas en vez de las diferencias al cuadrado
o: Porque siempre está más cerca de cero
a: 2
e: Elevar al cuadrado hace que un valor extremo pese muchísimo en el punto de equilibrio, así que la media se mueve hacia él. El valor absoluto crece de forma lineal, y por eso el punto que minimiza esa suma (la mediana) apenas se mueve.
:::

:::trampa
Un «tiempo de respuesta medio» de 200 ms con mediana de 80 ms significa que la mayoría de
peticiones van rápido y unas pocas van lentísimas. Para latencia se publican percentiles
(p50, p95, p99), nunca la media.
:::
