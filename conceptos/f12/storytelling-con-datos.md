---
id: storytelling-con-datos
titulo: Contar historias con datos
fase: 12
nivel: intermedio
rutas: [core, ds]
prerequisitos: [metricas-de-clasificacion]
tags: [comunicacion, narrativa, informes, decision]
resumen: Un análisis no convence por tener mas gráficos, sino por decir el mensaje en la primera línea, dar contexto para comparar y no ocultar lo que no sabes.
fuentes: ["Minto (2008), 'The Pyramid Principle: Logic in Writing and Thinking'", "Tufte (2001), 'The Visual Display of Quantitative Information'"]
---

## En una frase

Contar con datos es decidir de antemano qué tiene que entender y hacer quien te lee, y
construir el análisis hacia atrás desde ahí: primero el mensaje, después la evidencia, y
siempre con un término de comparación.

## La idea

Imagina que llegas a una reunión y sueltas: «he analizado las ventas de los últimos tres
años». La sala se prepara para veinte minutos de gráficos. Ahora imagina que empiezas con:
«las ventas caen un 8 % desde marzo, y la caída está concentrada en dos regiones». La sala ya
está pensando en las regiones. El mismo análisis, dos reuniones distintas.

Esa es toda la idea: **el mensaje va primero**. Quien te lee o te escucha tiene poco tiempo y
mucha prisa, y va a construir su propio relato con lo que le des. Si no le das el tuyo, se
inventará otro, y normalmente será el que más le convenga a sus ideas previas. La estructura
que funciona se llama **pirámide**: la conclusión arriba, los tres o cuatro argumentos que la
sostienen debajo, y los datos detrás de cada argumento. Es lo contrario del orden en que
trabajaste (datos, análisis, conclusión), y eso confunde a mucha gente buena: el informe no es
el diario de tu investigación, es el resumen de lo que has averiguado.

Tres piezas hacen que un análisis con datos aguante:

1. **El mensaje.** Una frase, con un verbo y una cifra, que alguien pueda repetir de memoria
   al salir de la reunión. «La conversión sube 0,3 puntos» no es un mensaje; «la conversión no
   ha cambiado de forma medible y necesitamos más datos» sí lo es.
2. **El contexto.** Ningún número significa nada solo. Se compara con el periodo anterior,
   con el mismo periodo del año pasado, con el objetivo o con otro grupo. Y la comparación
   tiene que ser **justa**: mismo número de días, misma población, misma definición de la
   métrica. Comparar febrero con enero y sorprenderse de que baje la venta es un clásico
   (febrero tiene menos días).
3. **La incertidumbre.** Cuántos datos sostienen la afirmación, qué no has podido medir y qué
   cambiaría tu conclusión. Un informe que oculta sus límites no es más convincente: es más
   frágil, porque el primero que note el hueco desconfiará de todo lo demás.

Una advertencia sobre la palabra «historia»: no significa adornar ni exagerar. Significa
**estructurar**. El dato no cambia; cambia el orden en que se presenta y qué se pone al lado de
qué. Si para que la historia funcione necesitas exagerar, lo que falta no es narrativa, es
evidencia.

## Definición formal

Un contraste honesto se escribe con tres cosas: una magnitud, su intervalo y su base. Para una
proporción estimada con `n` observaciones y `x` éxitos:

:::formula
p̂ = x / n   ·   error típico ≈ √(p̂·(1 − p̂) / n)   ·   intervalo ≈ p̂ ± 2·error típico
:::

Símbolos: `x` es el número de casos que cumplen la condición (por ejemplo, conversiones); `n`
es el número total de observaciones (por ejemplo, visitas); `p̂` es la proporción estimada
(conversión); el **error típico** mide cuánto bailaría `p̂` si repitieras la medición con otra
muestra del mismo tamaño; `± 2` errores típicos dan un intervalo aproximado del 95 %.

La regla práctica que sale de ahí y que resuelve la mitad de las discusiones de una reunión:
**si la diferencia entre dos periodos es menor que dos veces el error típico, no puedes afirmar
que haya cambiado nada.** No es que no haya cambio, es que tu muestra no lo distingue del
ruido.

## Ejemplo

Dos periodos de 400 visitas con 13 y 14 conversiones:

- Tasa del primer periodo: 13 / 400 = **3,25 %**.
- Tasa del segundo: 14 / 400 = **3,50 %**.
- Cambio relativo: (3,50 − 3,25) / 3,25 = **+7,7 %**, que suena a mucho.
- Diferencia absoluta: **una sola conversión**.
- Con `p = 27/800 = 3,375 %`, el error típico de la diferencia es
  `√(0,03375 · 0,96625 · 2/400) ≈ 1,28 %`, y la diferencia observada (0,25 puntos) es muy
  inferior a dos errores típicos.

Conclusión honesta: **«la conversión parece haber subido, pero con 400 visitas por periodo no
podemos distinguirlo del azar; con este ritmo harían falta unos 80.000 usuarios por rama para
detectar una mejora de este tamaño»** (número por rama de la fórmula de [[tamano-muestral]]:
`n = 2 · (1,96 + 0,842)² · 0,0325 · 0,9675 / 0,0025² ≈ 79.000`). Esa frase es menos bonita que
«hemos mejorado un 7,7 %» y es infinitamente más útil: evita tomar una decisión de producto
sobre ruido.

## Código

```python verificable
import math

# Conversiones en dos periodos de 400 visitas cada uno.
visitas, antes, despues = 400, 13, 14
tasa_antes, tasa_despues = antes / visitas, despues / visitas

# Error tipico de una diferencia de proporciones con muestras del mismo tamano.
p = (antes + despues) / (2 * visitas)
error = math.sqrt(p * (1 - p) * (2 / visitas))

print(f"tasa antes {tasa_antes:.1%}  tasa despues {tasa_despues:.1%}")
print(f"cambio relativo {(tasa_despues - tasa_antes) / tasa_antes:+.1%}")
print(f"diferencia observada {despues - antes} conversion, error tipico {error:.2%}")
print("cambio creible:", abs(tasa_despues - tasa_antes) > 2 * error)
```

```text
tasa antes 3.2%  tasa despues 3.5%
cambio relativo +7.7%
diferencia observada 1 conversion, error tipico 1.28%
cambio creible: False
```
```python ilustrativo
# La misma cifra contada de tres formas. Solo la tercera es un mensaje util.
print("Hemos mejorado la conversion un 7,7 %.")                      # sin incertidumbre
print("La conversion pasa de 3,2 % a 3,5 %.")                         # sin contexto ni base
print("La conversion sube 0,3 puntos, dentro del margen de error de 400 visitas; "
      "hacen falta ~80.000 usuarios por rama para confirmarlo.")      # accionable
```

## Errores típicos

- **Enseñar el proceso en lugar del resultado.** Empezar por «primero limpié los nulos, luego
  probé tres modelos…» pierde a la audiencia en la primera frase. El método va en un anexo;
  lo primero es qué has encontrado y qué propones.
- **Dar porcentajes sin base.** «Un 50 % más de errores» con 2 errores que pasan a 3 no
  significa nada. Da siempre el numerador, el denominador y el periodo: «de 2 a 3 errores
  sobre 10.000 peticiones».
- **Comparar cosas que no son comparables.** Enero contra febrero (31 días contra 28), esta
  semana contra la semana de un puente, usuarios nuevos contra todos los usuarios. Si las
  bases no son iguales, el número no es un cambio, es un artefacto del calendario.
- **Confundir correlación con causa.** Que dos series suban juntas no significa que una cause
  la otra. Si has hecho un experimento, dilo; si es observacional, usa «asociado a» y explica
  qué confusores podrían explicarlo ([[sesgo-y-etica-en-datos]]).
- **Esconder la incertidumbre para que la decisión sea más fácil.** Presentar una proyección
  con un solo número invita a tratarla como un hecho. Da el rango y di qué supuestos lo
  sostienen; si no, la primera desviación destruirá tu credibilidad.
- **Contar demasiadas historias.** Un informe con nueve conclusiones no tiene ninguna. Elige
  la que importa, sostenla con dos o tres argumentos y deja el resto como anexo.

:::truco
El test de la primera línea: escribe el mensaje en una sola frase con un sujeto, un verbo y una
cifra, y pregúntate si alguien podría **actuar** con ella. Si la frase es «los datos muestran
tendencias interesantes», no has terminado el análisis. Si es «el 40 % de las devoluciones
viene de tres tallas mal etiquetadas», ya sabes qué hacer mañana.
:::

## Comprueba que lo sabes

:::quiz
p: La conversión pasa del 3,2 % al 3,5 % con 400 visitas en cada periodo. ¿Cuál es la conclusión defendible?
o: La conversión ha mejorado un 7,7 % y hay que mantener el cambio
o: La diferencia es de una conversión y está dentro del margen de error, así que no se puede afirmar que haya cambiado nada
o: La conversión ha empeorado porque 3,5 es mayor que 3,2
a: 2
e: Con 400 visitas por periodo, el error típico de la diferencia ronda 1,3 puntos porcentuales, muy por encima de los 0,3 puntos observados: la diferencia es indistinguible del azar. La primera opción convierte ruido en decisión y la tercera confunde el signo del cambio.
:::

:::quiz
p: ¿Por qué el mensaje va al principio y no al final del informe?
o: Porque ahorra tiempo a quien lee y evita que construya su propia interpretación de los datos
o: Porque los gráficos y las tablas deben ir siempre en anexos
o: Porque así el informe es más corto
a: 1
e: La estructura piramidal existe porque la audiencia decide rápido y con poca atención: si no le das la conclusión primero, la sacará de donde pueda. La segunda opción es una exageración (los gráficos van junto al argumento que sostienen) y la tercera no tiene nada que ver con el orden.
:::

:::quiz
p: «Un 50 % más de incidencias» con 2 incidencias que pasan a 3. ¿Qué falta en esa afirmación?
o: Nada: el porcentaje ya resume el cambio
o: La base: sobre cuántas operaciones, en qué periodo, y que 2 y 3 son números demasiado pequeños para un porcentaje
o: El color de las incidencias
a: 2
e: Un porcentaje sin denominador es una cifra sin significado, y con números de un dígito el porcentaje amplifica el ruido en lugar de resumirlo. Lo correcto es dar el conteo absoluto y el total: «pasamos de 2 a 3 incidencias entre 10.000 peticiones».
:::
