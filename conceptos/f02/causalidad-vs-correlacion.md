---
id: causalidad-vs-correlacion
titulo: Causalidad frente a correlación
fase: 2
nivel: básico
rutas: [ds, core]
prerequisitos: [correlacion-pearson-spearman, poblacion-y-muestra, valor-esperado]
tags: [causalidad, correlacion, confusion, diseno]
resumen: Dos variables pueden moverse juntas por cuatro motivos distintos, y solo uno de ellos es que una cause a la otra; estos son los requisitos para poder decirlo.
fuentes: ["Pearl (2009), 'Causality: Models, Reasoning, and Inference'", "Hernán y Robins (2020), 'Causal Inference: What If'"]
---

## En una frase

Que dos variables se muevan juntas no significa que una provoque la otra: para hablar de causa
hacen falta tres cosas —que estén asociadas, que la causa ocurra antes que el efecto y que no
exista una tercera explicación que lo explique todo.

## La idea

La correlación de [[correlacion-pearson-spearman|Pearson]] es simétrica: la correlación entre `X`
e `Y` es exactamente la misma que entre `Y` y `X`. La causalidad no lo es. «Fumar causa cáncer» y
«el cáncer causa fumar» no son la misma frase, y solo una de las dos es verdad. Esa asimetría es
todo el problema: los datos solo te dan la parte simétrica, y la dirección hay que ponerla tú con
conocimiento del mundo.

Hay cuatro historias que producen una correlación, y solo la primera es causal:

1. **`X` causa `Y`.** La que quieres.
2. **`Y` causa `X`** (causalidad inversa). Las empresas con más beneficios contratan más
   consultores, y también los consultores mejoran los beneficios. Mirar los datos no distingue
   las dos direcciones.
3. **Una tercera variable `Z` causa las dos** (confusor). El número de heladerías y el número de
   ahogamientos suben juntos en una ciudad a lo largo del año, y ninguno causa al otro: los mueve
   el calor. Lo mismo con el clásico de las cigüeñas y los nacimientos: ambos son más frecuentes
   en municipios grandes y rurales, y ahí está la explicación.
4. **Las dos son consecuencia de un tercer factor que has filtrado al elegir la muestra**
   (colisionador o sesgo de selección). Entre los pacientes de un hospital, tener una enfermedad
   grave y tener un síntoma concreto pueden aparecer asociados en negativo, porque para llegar al
   hospital basta con una de las dos cosas. No es que la enfermedad proteja del síntoma: es que
   has seleccionado la muestra de una forma que crea la asociación.

La buena noticia es que hay un procedimiento mecánico que resuelve la duda: **la asignación
aleatoria**. Si decides al azar quién recibe el tratamiento, los dos grupos se parecen en todo
—lo que has medido y lo que no—, así que cualquier diferencia posterior se puede atribuir al
tratamiento. Eso es un experimento controlado, y es la única herramienta que garantiza el
resultado sin necesidad de conocer todos los confusores. Cuando no puedes experimentar (no puedes
asignar al azar quién fuma), hay métodos observacionales específicos, que se ven en
[[inferencia-causal-metodos]].

## Definición formal

La diferencia central es entre **observar** y **intervenir**. Se escribe con dos notaciones:

- `P(Y | X = 1)`: probabilidad de `Y` **entre los que observamos con** `X = 1`. Es lo que se puede
  calcular con datos.
- `P(Y | do(X = 1))`: probabilidad de `Y` si **forzáramos** `X` a valer 1 en toda la población.
  Es lo que quiere decir una afirmación causal.

La frase «`X` causa `Y`» significa `P(Y | do(X = 1)) ≠ P(Y | do(X = 0))`, y esa cantidad **no se
puede calcular directamente** con datos observacionales. Solo coincide con la diferencia
observacional cuando no hay confusión.

Con **resultados potenciales** se escribe más claro. Para cada unidad `i` existen dos resultados
posibles:

- `Yᵢ(1)` — lo que le pasaría a la unidad `i` si recibiera el tratamiento.
- `Yᵢ(0)` — lo que le pasaría si no lo recibiera.
- `Tᵢ` — si de hecho lo recibió (1) o no (0). Solo se observa **uno** de los dos resultados
  potenciales: el otro es el **contrafactual**, y es lo que hace el problema difícil.

El efecto causal medio es:

:::formula
ATE = E[ Y(1) − Y(0) ]
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `Y(1)` | El resultado de la misma unidad si recibe el tratamiento | las del resultado (€, puntos, bajas) | Sube el efecto medido: es la mitad «con tratamiento» de la resta |
| `Y(0)` | El resultado de la misma unidad si no lo recibe; es el contrafactual y nunca se observa | las del resultado | Baja el efecto medido: si los no tratados mejoran solos, parte de la mejora no es del tratamiento |
| `Y(1) − Y(0)` | El efecto causal individual; por unidad solo existe uno de los dos términos | las del resultado | Es la cantidad que se quiere promediar, no una que se pueda medir fila a fila |
| `T` | Si la unidad recibió el tratamiento (1) o no (0) | 0 o 1 | Si `T` se reparte por algo relacionado con `Y` (edad, gravedad, motivación), el ATE deja de coincidir con la diferencia de medias observada |
| `E[·]` | Media de esa diferencia en toda la población | las del resultado | El promedio es lo que hace estimable lo individual: la media sí se puede calcular, cada `Yᵢ(1) − Yᵢ(0)` no |
| `do(X = 1)` | Intervención: forzar `X` a valer 1 en toda la población, no solo observarla | 0 o 1 si `X` es binaria | Es la cantidad causal; solo coincide con lo observacional si no hay confusión ni causalidad inversa |
:::

La aleatorización consigue que `(Y(0), Y(1))` sea independiente de `T`, así que la diferencia de
medias observada entre los grupos es un estimador insesgado del ATE. Sin aleatorización, esa
diferencia mezcla el efecto con las diferencias previas entre los grupos.

**Los tres requisitos**, en versión corta:

1. **Asociación**: `X` e `Y` están relacionados (si no, no hay nada que explicar).
2. **Orden temporal**: `X` ocurre antes que `Y`. Los datos deben permitir establecerlo, y no
   basta con que la fila de `X` aparezca antes en la tabla.
3. **No confusión**: no queda ninguna causa común de `X` e `Y`, ni causalidad inversa, ni sesgo
   de selección. En observacional esto se argumenta, no se demuestra con un test.

## Ejemplo

Una tienda de aplicaciones quiere saber si una función nueva reduce las bajas de clientes. Los
datos, separados por tipo de dispositivo:

```text
                         sin funcion      con funcion
movil                    26 / 100 = 26 %  50 / 200 = 25 %
escritorio               66 / 600 = 11 %  10 / 100 = 10 %
--------------------------------------------------------
total                    92 / 700 = 13,1 %  60 / 300 = 20,0 %
```

Lee los tres resultados con calma, porque dicen cosas opuestas:

- En móvil, la función baja las bajas del 26 % al 25 %.
- En escritorio, las baja del 11 % al 10 %.
- En el total, las **sube** del 13,1 % al 20,0 %.

Es la **paradoja de Simpson**. No hay contradicción: el dispositivo es un confusor. La función se
usó sobre todo en móvil (200 de los 300 usos), y el móvil es el dispositivo con más bajas. Al
juntar los dos grupos, el peso del móvil arrastra la tasa global hacia arriba y crea la ilusión de
que la función perjudica.

Si comparas el total, concluyes lo contrario de lo que dicen los datos. Si comparas dentro de cada
dispositivo, la función ayuda (poco). La lección no es «usa porcentajes estratificados»: es que
**la decisión de qué variable separar cambia la respuesta**, y hay que tomarla con un criterio
causal, no probando combinaciones. Ese criterio es lo que formaliza [[confusores-y-dag]].

El segundo bloque de código muestra el mismo fenómeno de otra forma: dos variables sin ninguna
relación entre ellas aparecen asociadas con una correlación de 0,49 solo porque comparten una
causa común. Al descontar esa causa, la correlación se queda en cero.

:::figura
fichero: confusor-correlacion-que-desaparece
pie: Dos variables que no se causan entre sí suben y bajan juntas solo porque las mueve una tercera que no está en los datos. Al descontarla, la recta se aplana y la relación se queda en cero: la correlación por sí sola no distingue «X causa Y» de «Z causa las dos».
fuente: figuras/causalidad-vs-correlacion-1.py
:::

## Código

```python verificable
# Paradoja de Simpson: dentro de cada dispositivo la funcion reduce las bajas,
# pero en el total parece aumentarlas porque se uso mucho mas en movil.
print(f"movil      sin funcion {26/100:.1%}  con funcion {50/200:.1%}")
print(f"escritorio sin funcion {66/600:.1%}  con funcion {10/100:.1%}")
print(f"total      sin funcion {92/700:.1%}  con funcion {60/300:.1%}")
# -> movil      sin funcion 26.0%  con funcion 25.0%
# -> escritorio sin funcion 11.0%  con funcion 10.0%
# -> total      sin funcion 13.1%  con funcion 20.0%
```

:::claves
- `26/100` da 0,26 y no 0: en Python 3 la barra `/` es siempre división real, aunque los dos números sean enteros. Con `//` (división entera) saldría 0 y todos los porcentajes se imprimirían como 0,0 %.
- El `:.1%` de la f-string no calcula nada: solo multiplica por 100 al escribir y añade el signo «%». El valor que hay detrás sigue siendo 0,26, así que para seguir operando con él hay que usar el número, no el texto formateado.
- La alineación de los tres `print` no la hace Python: son los espacios escritos dentro de cada cadena. Si un rótulo cambia de largo, la tabla se descuadra y el programa no avisa.
- La última línea es la que encierra la paradoja: `92/700` no es la media de 26,0 % y 11,0 % (eso daría 18,5 %), porque cada porcentaje pesa según cuántos casos tiene detrás. Promediar porcentajes sin ponderar cambia la conclusión de signo.
- `:.1%` redondea al escribir: 13,1 % es en realidad 13,142…% y 60/300 sale exacto. Cambiar a `:.2%` no toca los datos, solo cuántos decimales se ven (y si el total se calculara con el texto redondeado, el error se acumularía).
- Los comentarios `# ->` de debajo están escritos a mano y no los comprueba nadie: lo que el portal ejecuta y enseña es la salida real. Si se cambia un número del código, el comentario se queda mintiendo aunque el bloque siga funcionando.
:::

```python verificable
import numpy as np

# x e y no se causan entre si: los dos son consecuencia de z (el confusor).
rng = np.random.default_rng(0)
z = rng.normal(size=2000)
x = z + rng.normal(size=2000)
y = z + rng.normal(size=2000)

print(f"correlacion bruta       {np.corrcoef(x, y)[0, 1]:+.2f}")
# -> correlacion bruta       +0.49

# Al quitar de cada variable la parte explicada por z, la relacion desaparece.
sobra_x = x - np.polyval(np.polyfit(z, x, 1), z)
sobra_y = y - np.polyval(np.polyfit(z, y, 1), z)
print(f"correlacion quitando z  {np.corrcoef(sobra_x, sobra_y)[0, 1]:+.2f}")
# -> correlacion quitando z  -0.02
```

## Errores típicos

- **Creer que una correlación alta implica causa, y que una baja la descarta.** Una correlación
  baja puede convivir con un efecto causal fuerte si hay mucho ruido; una correlación altísima
  puede ser puro confusor. El coeficiente no informa sobre la dirección ni sobre la causa.
- **No comprobar el orden temporal.** La causa tiene que ocurrir antes que el efecto. Si mides las
  dos cosas a la vez, no puedes distinguir «`X` causa `Y`» de «`Y` causa `X`».
- **Quedarse con la primera explicación plausible.** «Los que usan la función compran más, luego
  la función vende» ignora que los más activos usan más todas las funciones y compran más.
  Enumera al menos una explicación alternativa antes de aceptar la causal.
- **Intervenir después de un valor extremo y atribuirle la vuelta.** Es la **regresión a la
  media**: si tomas medidas de los que peor puntuaron y les aplicas algo, mejorarán de media
  aunque el algo no haga nada. Para eso hace falta un grupo de comparación.
- **Controlar por una variable que en realidad es consecuencia del tratamiento.** Si separas por
  «usa la función» entre los que ya llevan meses usándola, puedes estar bloqueando parte del
  efecto. Lo que hay que ajustar son las causas comunes, no los efectos intermedios: eso es
  [[confusores-y-dag]].
- **Extrapolar el resultado a otra población.** Un efecto medido en usuarios nuevos de una ciudad
  no tiene por qué valer para los clientes veteranos de otro país. La validez interna y la externa
  son dos preguntas distintas.
- **Confundir «no hay evidencia de efecto» con «hay evidencia de que no hay efecto».** Un estudio
  con poca muestra no descarta nada. Para eso está [[tamano-muestral|el cálculo del tamaño
  muestral]].

:::practica
enunciado: Una academia compara la nota final de 200 alumnos que hicieron su curso (media 6,8) con la de 500 que no (media 6,1), y anuncia un efecto de +0,7 puntos. Por nivel previo: 7,8 con curso y 7,7 sin curso entre los de nivel alto; 5,8 y 5,7 entre los de nivel bajo. ¿Se sostiene ese +0,7?
pista: Compara las diferencias dentro de cada estrato y mira qué proporción de cada grupo es de nivel alto.
solucion: En cada estrato la diferencia es 7,8 − 7,7 = +0,1 y 5,8 − 5,7 = +0,1. Las medias globales son (100·7,8 + 100·5,8)/200 = 6,8 y (100·7,7 + 400·5,7)/500 = 6,1. El +0,7 sale de la composición: el 50 % del grupo con curso es de nivel alto, frente al 20 % del control. El nivel previo es una causa común; el efecto creíble es +0,1.
:::

## Comprueba que lo sabes

:::quiz
p: En el ejemplo, la tasa de bajas es menor con la función dentro de móvil (25 % frente a 26 %) y dentro de escritorio (10 % frente a 11 %), pero en el total es mayor (20,0 % frente a 13,1 %). ¿Cómo se explica?
o: Hay un error de cálculo, porque los totales deben coincidir con los estratos
o: El tipo de dispositivo es una causa común: influye en si se usa la función y en la tasa de bajas, así que distorsiona la comparación global
o: La función reduce las bajas en móvil y las aumenta en escritorio
a: 2
e: Es la paradoja de Simpson. La función se concentró en móvil, que es el grupo con más bajas, y al agregar los grupos ese peso arrastra el total. Los estratos son los que dan la comparación honesta. La opción 3 es imposible: en los dos estratos la tasa baja.
:::

:::quiz
p: Observas que los clientes que contactan más veces con soporte cancelan más el servicio. ¿Qué NO puedes concluir?
o: Que existe una asociación entre contactar con soporte y cancelar
o: Que contactar con soporte provoca la cancelación, porque la insatisfacción previa puede causar las dos cosas
o: Que hace falta más información para decidir si conviene reducir el soporte
a: 2
e: La asociación es un dato. La interpretación causal es la que no se sostiene: un problema con el producto puede generar tanto las llamadas como la baja, así que actúa de causa común. Además hay causalidad inversa: quien ya decidió irse puede llamar para preguntar cómo darse de baja.
:::

:::quiz
p: ¿Qué consigue la asignación aleatoria que no consigue ningún ajuste estadístico?
o: Garantiza que el efecto sea grande
o: Hace que los grupos sean comparables en todo, incluido lo que no has medido ni conoces
o: Elimina la necesidad de medir la variable de resultado
a: 2
e: Al azar, las características previas se reparten entre los grupos y dejan de confundir, incluso las que no aparecen en tu base de datos. Los ajustes estadísticos solo controlan lo que has medido y has incluido bien en el modelo; la aleatorización no necesita conocer la lista de confusores.
:::

:::trampa
Una regresión con muchos controles no convierte un dato observacional en un experimento. Ajustar
por lo que tienes a mano no elimina los confusores que no has medido, y ajustar por la variable
equivocada puede inventar una relación que no existe. Sin diseño, los coeficientes son
descripciones, no causas.
:::
