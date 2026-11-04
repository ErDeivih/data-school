---
id: calidad-de-datos
titulo: Calidad de datos
fase: 3
nivel: intermedio
rutas: [de, ds]
prerequisitos: [sql-agregaciones-y-group-by, pandas-fundamentos]
tags: [calidad, validacion, nulos, duplicados]
resumen: Nulos, duplicados, rangos imposibles y coherencia entre columnas convertidos en proporciones que se miden, se vigilan y se reclaman al origen.
fuentes: ["McCallum (2012), 'Bad Data Handbook'", "Kimball y Ross (2013), 'The Data Warehouse Toolkit'"]
---

## En una frase

La calidad de un dato se mide con proporciones —completitud, unicidad, validez, coherencia,
exactitud y puntualidad— calculadas sobre **todas** las filas y por segmentos, no con la
impresión que deja mirar veinte a ojo.

## La idea

Imagina una tabla de un millón de clientes. Parece razonable, y sin embargo:

- 87.000 no tienen correo electrónico (falta un dato).
- 12.000 están duplicados (el mismo cliente dos veces, con identificadores distintos).
- 4 tienen 139 años (el dato está, pero es imposible).
- 3.000 tienen una provincia que no cuadra con el código postal (cada dato suelto es plausible,
  juntos se contradicen).
- 20.000 se dieron de alta antes que la empresa (la fecha no puede ser anterior al origen del
  sistema).
- Un 2 % de las filas llega con más de 48 horas de retraso (el dato es correcto, pero tarde).

Son seis problemas distintos, con seis arreglos distintos. Meterlos todos en el saco de «los
datos están sucios» es lo que impide arreglar ninguno. Por eso la calidad se descompone en
dimensiones y cada dimensión se convierte en un número.

Tres distinciones que ahorran discusiones:

1. **Completitud no es validez.** Un campo con `no-es-un-email` está relleno y no sirve. Si solo
   mides nulos, tu informe dice 100 % de completitud mientras la mitad de los correos rebotan.
2. **Coherencia no es exactitud.** Que el código postal y la provincia cuadren entre sí no
   significa que sea la dirección de esa persona: puede ser la de su madre. La exactitud exige
   contrastar con la realidad (una fuente externa, una llamada, una muestra auditada) y casi nunca
   se puede calcular dentro de la base de datos. Las otras cinco dimensiones sí.
3. **Nulo, cero y «desconocido» son tres cosas.** `importe = 0` significa que no se cobró nada;
   `importe IS NULL` significa que no se sabe. Decidir cuál es cuál es trabajo del modelado, y
   confundirlos estropea todas las medias que se calculen después.

Y una consecuencia práctica: la calidad **se degrada sola**. Cada fuente nueva, cada cambio en un
formulario, cada migración y cada proceso manual la mueven hacia abajo. Medirla una vez, el día de
la migración, no sirve de nada: hay que medirla en la ingesta (con contratos y pruebas, ver
[[contratos-de-datos]]) y a lo largo del tiempo (con alertas de volumen, frescura y distribución,
ver [[observabilidad-de-datos]]).

Por último, la calidad no es un objetivo absoluto. Hay que saber qué duele: un nulo en la
preferencia de newsletter no bloquea nada; un nulo en el identificador fiscal de una factura
impide emitirla. Se arregla primero lo que rompe un proceso, y se documenta el resto.

## Definición formal

Sea `N` el número de filas de la tabla y `x` una columna:

- **Completitud(x)** = filas con `x` no nulo / `N`.
- **Unicidad** = 1 − filas duplicadas / `N`, con la **clave de deduplicación declarada**. Sin decir
  qué columnas forman la clave, la cifra no significa nada: por nombre hay 2 duplicados y por
  identificador fiscal hay 1.
- **Validez(x)** = filas donde `x` cumple su dominio / `N`. El dominio es un rango, un formato o
  un conjunto de valores permitidos.
- **Coherencia** = filas que cumplen una regla que cruza dos o más columnas / `N`. Por ejemplo:
  la provincia se deduce del código postal, o `fecha_fin` no es anterior a `fecha_inicio`.
- **Puntualidad** = filas con su marca temporal dentro del plazo acordado / `N`.
- **Exactitud** = filas cuyo valor coincide con la realidad / `N`. Requiere una fuente de verdad
  externa; no se calcula mirando solo la tabla.

Dos decisiones que hay que explicitar siempre, porque cambian el número:

1. **El denominador.** `N` (todas las filas) es lo habitual, pero a veces la regla solo aplica a
   un subconjunto: la completitud del número de identificación fiscal solo tiene sentido sobre
  clientes de empresa. Mide con `N` y con el subconjunto, y di cuál usas.
2. **El nivel de agregación.** Un 98 % global puede esconder un 30 % en el segmento que más
   factura. Mide siempre por las dimensiones que te importan (país, canal, antigüedad, fuente) y
   no solo en total: los fallos de calidad casi nunca se reparten de forma uniforme.

Un nulo y un valor inválido son fallos distintos y por eso van en columnas distintas del informe.
Y ojo con `between` en pandas o con las comparaciones en SQL: la comparación con un nulo da
*falso* o *desconocido*, nunca verdadero, así que un nulo siempre incumple una regla de validez.
Eso es correcto para el informe y peligroso para el `WHERE` que crees que filtra otra cosa.

## Ejemplo

Ocho filas de clientes con cuatro problemas distintos:

| id | email | edad | provincia | cp |
| --- | --- | --- | --- | --- |
| 1 | ana@x.com | 34 | Valencia | 46001 |
| 2 | luis@x.com | 41 | Bilbao | 48001 |
| 3 | (nulo) | 29 | Valencia | 46002 |
| 4 | marta@x.com | 150 | Bilbao | 48002 |
| 5 | pau@x.com | 38 | Sevilla | 41001 |
| 5 | pau@x.com | 38 | Sevilla | 41001 |
| 6 | eva@x.com | 45 | Madrid | 28001 |
| 7 | no-es-un-email | (nulo) | Madrid | 99999 |

Los números que salen:

- **Completitud del email: 88 %.** Siete de ocho tienen algo; la fila 3 está vacía.
- **Validez del email: 75 %.** Fallan dos filas: la 3, que está nula, y la 8, que tiene
  `no-es-un-email`. La completitud solo ve la primera; la validez ve las dos, y por eso son
  columnas distintas del informe.
- **Unicidad: 88 %.** El identificador 5 aparece dos veces. Aquí la clave es el `id`; si
  deduplicases por correo, `pau@x.com` también saldría como duplicado y el resultado sería el
  mismo por casualidad, no por razón.
- **Validez de la edad: 75 %.** Fallan dos filas: el 150 (imposible) y el nulo (desconocido). Se
  cuentan juntos en la proporción y se separan en el informe: uno se corrige, el otro se reclama.
- **Coherencia provincia/código postal: 88 %.** El `99999` no tiene el prefijo de Madrid. Cada
  valor por separado es formalmente válido; el problema solo aparece al cruzar las dos columnas.

Cada cifra lleva a una acción distinta: la completitud al formulario que permite enviar sin
correo, la validez a la validación de formato, la unicidad a decidir la clave de negocio, la
coherencia a una comprobación cruzada en la carga. Un informe con un solo «calidad: 87 %» no
permite hacer ninguna de las cuatro.

## Código

```python verificable
# Cuatro dimensiones, cada una una proporcion sobre el total de filas.
id_ = [1, 2, 3, 4, 5, 5, 6, 7]
email = ["ana@x.com", "luis@x.com", None, "marta@x.com", "pau@x.com",
         "pau@x.com", "eva@x.com", "no-es-un-email"]
edad = [34, 41, 29, 150, 38, 38, 45, None]
provincia = ["Valencia", "Bilbao", "Valencia", "Bilbao", "Sevilla",
             "Sevilla", "Madrid", "Madrid"]
cp = ["46001", "48001", "46002", "48002", "41001", "41001", "28001", "99999"]
n = len(id_)

completitud = sum(1 for e in email if e is not None) / n
unicidad = 1 - (n - len(set(id_))) / n
validez = sum(1 for e in edad if e is not None and 0 <= e <= 120) / n

# Coherencia: el prefijo del codigo postal tiene que cuadrar con la provincia.
prefijo = {"Valencia": "46", "Bilbao": "48", "Sevilla": "41", "Madrid": "28"}
coherencia = sum(1 for p, c in zip(provincia, cp) if c[:2] == prefijo[p]) / n

print(f"filas {n}  completitud {completitud:.0%}  unicidad {unicidad:.0%}  "
      f"validez {validez:.0%}  coherencia {coherencia:.0%}")
# -> filas 8  completitud 88%  unicidad 88%  validez 75%  coherencia 88%
```

```python verificable
# El mismo grupo de filas y dos claves de deduplicacion distintas: dos respuestas.
personas = [
    ("Ana Perez", "11111111H"),
    ("Ana Perez", "11111111H"),
    ("Ana Perez", "22222222J"),
]

def duplicados(filas, columna):
    """Filas repetidas de una clave: filas totales menos valores distintos de esa clave."""
    return len(filas) - len({fila[columna] for fila in filas})

print("filas", len(personas))   # -> filas 3
# Por nombre parecen tres la misma persona; por NIF solo hay una repetida de verdad.
print("duplicados por nombre ", duplicados(personas, 0))
# -> duplicados por nombre  2
print("duplicados por nif    ", duplicados(personas, 1))
# -> duplicados por nif     1
```

## Errores típicos

- **Medir solo nulos y llamarlo calidad.** La completitud es una de seis dimensiones. Un campo
  relleno con `N/A`, `-1` o `1900-01-01` está completo y es basura: son los llamados valores
  centinela, y hay que buscarlos explícitamente porque no son nulos para el motor.
- **Deduplicar por el nombre o por el correo.** Decide primero qué identifica de verdad a una
  fila (el identificador de negocio, no el texto). Deduplicar por nombre borra personas distintas
  con el mismo nombre, y deduplicar por correo borra a quien comparte el correo familiar.
- **Confundir nulo con cero.** Cambia la media, cambia el conteo y cambia la conclusión. Si el
  origen no distingue «no compró» de «no se sabe», el problema está en el origen.
- **Corregir en el informe y no en el origen.** El `CASE WHEN` que arregla el país mal escrito
  funciona, pero el mes siguiente vuelve el mismo error y ya hay doce versiones del arreglo
  repartidas por doce consultas. La corrección va en la ingesta o en una capa de limpieza
  documentada y única.
- **Publicar un único porcentaje global.** Oculta justo los segmentos que fallan. Mide por fuente,
  por país, por canal y por antigüedad: los problemas de calidad se concentran.
- **Confundir coherencia con exactitud.** Un código postal y una provincia coherentes pueden ser
  los de otra persona. La exactitud se audita contra la realidad; la coherencia solo contra sí
  misma.

:::practica
enunciado: Diez filas de pedidos. id = [1,2,3,4,4,5,6,7,8,9]; email = ["ana@x.com","luis@x.com",nulo,"marta@x.com",nulo,"pau@x.com","eva@x.com","sin-arroba","ana@x.com","juan@x.com"]; importe = [10,20,30,40,50,60,70,80,-15,100]. Calcula completitud y validez del email, validez del importe (importe ≥ 0) y unicidad por id, diciendo qué filas fallan.
pista: La completitud pregunta si hay valor y la validez si cumple el dominio; un nulo incumple la validez aunque no sea un formato distinto.
solucion: Completitud del email = 8/10 = 80 % (nulos en las filas 3 y 5). Validez del email = 7/10 = 70 %: además de los dos nulos falla la fila 8, "sin-arroba". Validez del importe = 9/10 = 90 %: la fila 9 con −15 incumple el rango. Unicidad = 1 − 1/10 = 90 %: el id 4 aparece dos veces. Tres cifras, tres arreglos: formulario, validación de formato y clave de negocio.
:::

## Comprueba que lo sabes

:::quiz
p: En la tabla del ejemplo, la fila 8 tiene email = "no-es-un-email" y la fila 3 lo tiene vacío. ¿Cómo aparecen en las métricas?
o: Las dos bajan la completitud, porque ninguna de las dos es un correo utilizable
o: La fila 3 baja la completitud y la fila 8 la validez: son dimensiones distintas
o: Las dos bajan la validez, porque la completitud solo cuenta valores nulos
a: 2
e: La completitud pregunta si hay valor; la validez, si el valor cumple el formato. La fila 3 no tiene nada (completitud) y la fila 8 tiene algo que no es un correo (validez). Por eso un informe que solo mide nulos puede dar 100 % con la mitad de los correos inservibles.
:::

:::quiz
p: ¿Por qué no basta con publicar un porcentaje global de calidad, por ejemplo «92 % de filas correctas»?
o: Porque los porcentajes globales siempre están mal calculados
o: Porque los fallos se concentran por segmentos y la media los diluye
o: Porque la calidad no se puede medir con números
a: 2
e: Un 92 % global puede convivir con un 40 % de fallos en el canal o el país que más factura. Medir por fuente, país, canal y antigüedad localiza el problema y permite reclamarlo a quien lo produce. Los porcentajes no están mal por ser globales: están incompletos si son solo globales.
:::

:::quiz
p: Quieres deduplicar una lista de clientes. ¿Cuál es el primer paso?
o: Borrar las filas cuyo nombre se repite
o: Decidir qué columnas identifican de verdad a un cliente y usar esa clave
o: Quedarse siempre con la fila más reciente, sin mirar más
a: 2
e: La clave de deduplicación decide el resultado: en el ejemplo, por nombre hay 2 duplicados y por NIF hay 1. El nombre se repite entre personas distintas y el correo se comparte en una familia. Quedarse con la más reciente es una política razonable, pero es el paso siguiente, no el primero.
:::

:::aviso
Los valores centinela (`-1`, `9999`, `1900-01-01`, `N/A`, cadena vacía) no son nulos y pasan todos
los controles de completitud. Búscalos con un perfilado explícito de valores frecuentes: un
`1900-01-01` repetido 40.000 veces en una columna de fechas no es una coincidencia, es la forma
que tiene el sistema de origen de decir «no lo sé».
:::
