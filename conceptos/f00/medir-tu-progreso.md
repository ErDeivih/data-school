---
id: medir-tu-progreso
titulo: Medir tu progreso sin engañarte
fase: 0
nivel: básico
rutas: [core]
prerequisitos: [como-estudiar]
tags: [progreso, metricas, ventanas]
resumen: La media acumulada esconde los cambios: mide tu rendimiento por ventanas, compáralo contigo mismo y no conviertas la métrica en el objetivo.
fuentes: ["Heath y Starr (1999), 'Adaptive Spaced Repetition'", "Dweck (2006), 'Mindset'"]
---

## En una frase

Si mides tu progreso con el total acumulado nunca verás que has empeorado esta semana; con una
ventana móvil, sí.

## La idea

La media de todo lo que has hecho arrastra el pasado y pesa igual una sesión de hace seis meses
que la de ayer. Por eso el número sube despacio, se estabiliza y da una sensación tranquilizadora
que no tiene nada que ver con lo que está pasando ahora.

Tu rendimiento no es una constante: cambia por rachas, por sueño, por dificultad del tema y por
el orden en que estudias. Es una serie no estacionaria, igual que un precio o una métrica de
producto. Y se analiza igual: mirando la ventana reciente y comparándola con tu propia línea base,
no con la de nadie más.

Hay una segunda trampa, más sutil: convertir la métrica en el objetivo. Si empiezas a medir
«minutos estudiados», acabarás acumulando minutos que no enseñan nada. La métrica tiene que medir
algo que te importe —aciertos, capacidad de explicar, problemas resueltos— y no una actividad que
puedas inflar sin aprender.

:::aviso
La ventana móvil tampoco es magia: con pocos datos es ruidosa. Tres sesiones malas pueden ser una
racha normal. La regla práctica es no cambiar nada por una ventana de una semana, y sí mirarla
cuando lleve tres o cuatro semanas en la misma dirección.
:::

## Definición formal

Con una serie de resultados por sesión `x₁, …, x_t` (por ejemplo, la proporción de aciertos del
repaso):

:::formula
media acumulada:  x̄_t = (1/t) · Σ x_i          ventana:  m_t(w) = (1/w) · Σ x_i  para i en [t−w+1, t]
:::

- `x_i` — el resultado de la sesión `i`, en la unidad que hayas elegido (aciertos, problemas
  resueltos, minutos de recuperación activa).
- `t` — número de sesiones hasta hoy.
- `w` — tamaño de la ventana: cuántas sesiones recientes entran en la media.
- `x̄_t` — media acumulada: reacciona cada vez menos, porque cada dato nuevo pesa `1/t`.
- `m_t(w)` — media de la ventana: reacciona en cuanto cambian las últimas `w` sesiones.

La media acumulada converge a la media histórica; la de la ventana sigue al presente. Para ver
tendencia se puede mirar la diferencia entre dos ventanas consecutivas, o una media de la ventana
más corta frente a una más larga.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `w` | Tamaño de la ventana | sesiones | Alarga la memoria: menos ruido y más retraso en detectar un cambio |
| `x_i` | Resultado de una sesión | la unidad elegida | Es el dato que decide todo: si mide actividad en vez de aprendizaje, la métrica te engaña |
| `x̄_t` | Media acumulada | misma unidad | Se vuelve insensible: con 100 sesiones, una nueva apenas la mueve un 1 % |
| `m_t(w)` | Media de la ventana | misma unidad | Reacciona rápido, pero con `w` pequeño confunde racha con tendencia |
:::

## Ejemplo

Aciertos del repaso en diez sesiones: `5, 6, 4, 5, 6, 4, 5, 3, 4, 3`.

- Media acumulada al final: `45/10 = 4,5`. Sugiere estabilidad.
- Ventana de 3: `(4 + 3 + 3)/3 = 3,33`.
- Ventana de 5: `(5 + 3 + 4 + 3 + 3)/5 = 3,8`.

Las tres cifras describen lo mismo desde sitios distintos. La acumulada dice «vas bien de media»;
las ventanas dicen «estás bajando». Ninguna es falsa, pero solo una sirve para decidir qué hacer
esta semana.

## Código

```python verificable
import pandas as pd

aciertos = pd.Series([5, 6, 4, 5, 6, 4, 5, 3, 4, 3])

print(f"acumulada {aciertos.expanding().mean().iloc[-1]:.2f}")   # -> acumulada 4.50
print(f"ventana 3 {aciertos.rolling(3).mean().iloc[-1]:.2f}")     # -> ventana 3 3.33
print(f"ventana 5 {aciertos.rolling(5).mean().iloc[-1]:.2f}")     # -> ventana 5 3.80

print(aciertos.rolling(3).mean().round(2).tail(4).to_string(index=False))
```

La última salida muestra las cuatro últimas medias de la ventana de 3: si vienen bajando tres
semanas seguidas, hay una señal; si solo baja la última, es ruido.

:::claves
- `expanding().mean()` recalcula la media con todo lo anterior. Es la acumulada clásica y, por
  construcción, la última fila es la media de toda la serie.
- `rolling(3).mean()` devuelve NaN en las dos primeras filas: no hay tres datos. Esos NaN no son un
  error y no hay que rellenarlos con cero.
- `.iloc[-1]` toma la última fila. Con `.iloc[0]` estarías mirando la primera ventana completa, que
  es el pasado remoto.
- `.tail(4)` y `.to_string(index=False)` sirven para ver la tendencia sin que el índice estorbe. Es
  una decisión de presentación, no de cálculo.
- La unidad importa: si `aciertos` fueran minutos, la misma cuenta mediría actividad. El código es
  el mismo; el significado, no.
:::

## Errores típicos

- **Medir minutos de estudio en vez de recuperación.** Los minutos se acumulan solos y no dicen si
  aprendiste. Mide lo que puedes recuperar sin mirar: aciertos, explicaciones, problemas
  resueltos.
- **Compararte con otra persona.** Su línea base, su punto de partida y su temario son distintos.
  La única comparación que informa es contigo mismo hace un mes.
- **Cambiar de métrica cuando baja.** Es la forma más eficaz de no ver nunca una tendencia. Elige
  una, mantenla un trimestre y cámbiala solo por una razón escrita.
- **Usar la racha como prueba de dominio.** Cinco días seguidos de aciertos pueden ser un tema
  fácil. El dominio se prueba con un problema nuevo, no con el mismo repetido.
- **Decidir por una sola sesión.** La varianza de una sesión es enorme: dormir mal mueve el
  resultado más que estudiar. Mira ventanas, no puntos.
- **Convertir la métrica en el objetivo.** Si el número se puede subir sin aprender, lo vas a
  subir sin aprender. Es la ley de Goodhart aplicada a tu propio cuaderno.

:::practica
enunciado: Tienes estos aciertos en seis sesiones: 7, 8, 6, 5, 4, 4. Calcula la acumulada, la ventana de 2 y la ventana de 3 al final, y decide si hay tendencia.
pista: La ventana de 2 usa las dos últimas; la de 3, las tres últimas.
solucion: Acumulada = 34/6 = 5,67. Ventana de 2 = (4 + 4)/2 = 4,0. Ventana de 3 = (5 + 4 + 4)/3 = 4,33. La acumulada (5,67) sigue alta por las tres primeras sesiones, mientras las ventanas se han estabilizado en 4: hay un cambio de nivel, no una caída puntual. Con seis puntos no se puede afirmar la causa; sí se puede decir que la tendencia es a la baja.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué ventaja tiene la ventana móvil sobre la media acumulada?
o: Detecta el cambio de tendencia, que la acumulada diluye con el histórico
o: Es más precisa porque usa más datos
o: Elimina el ruido de las sesiones malas
a: 1
e: La acumulada pesa cada dato nuevo con `1/t` y por eso tarda en reflejar un cambio. La ventana mira solo lo reciente y reacciona antes. No es más precisa: es más sensible, y eso tiene un precio en ruido.
:::

:::quiz
p: Llevas tres sesiones bajando y decides cambiar de métrica para que refleje mejor tu esfuerzo. ¿Qué está mal?
o: Que el cambio coincide con una racha mala y elimina justo la señal que querías ver
o: Nada: si la métrica no te representa, se cambia
o: Que las métricas no se pueden cambiar nunca
a: 1
e: Cambiar la métrica cuando baja es la forma clásica de no ver una tendencia. Si la métrica era mala, el cambio debía haberse hecho antes y con un motivo escrito; hacerlo justo ahora convierte el cuaderno en un adorno.
:::
