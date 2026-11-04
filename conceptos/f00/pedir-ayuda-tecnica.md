---
id: pedir-ayuda-tecnica
titulo: Pedir ayuda técnica y que te la den
fase: 0
nivel: básico
rutas: [core]
prerequisitos: [hacer-preguntas-buenas]
tags: [metodo, depuracion, comunicacion]
resumen: Una duda se responde cuando lleva un ejemplo mínimo que falla, lo que ya has probado, las versiones exactas y la diferencia entre lo que esperabas y lo que pasó.
fuentes: ["Raymond y Moen (2014), 'How To Ask Questions The Smart Way'", "Hunt y Thomas (1999), 'The Pragmatic Programmer'"]
---

## En una frase

Empaqueta la duda como un informe corto: un ejemplo mínimo que falle igual que tu problema, qué has
probado ya, las versiones exactas y la diferencia entre lo que esperabas y lo que pasó.

## La idea

Llamas al taller y dices «el coche hace un ruido raro»: el mecánico solo puede citarte y cobrarte la
diagnosis. Si dices «hace un clic al girar a la derecha en frío, desde que cambié las pastillas, y
aquí tienes la grabación», hay muchas papeletas de que te diga qué es por teléfono. La información
no es cortesía: es lo que convierte una pregunta en algo que se puede responder.

Con el código pasa igual, con un agravante: quien te ayuda no tiene tu máquina, ni tus datos, ni tu
pantalla. Todo lo que puede usar es lo que escribes. Y su trabajo crece con lo que le pegues: si le
mandas 800 líneas, tiene 800 sospechosos; si le mandas 6, tiene 6. **Reducir el ejemplo es trabajo
tuyo, no de quien responde.**

Aquí está la parte buena: al construir el ejemplo mínimo, muchas veces encuentras el fallo tú. Vas
quitando trozos y, en el momento en que el error desaparece, acabas de localizar qué trozo lo
causaba. Por eso se le llama depurar hablando con un pato de goma: explicar el problema en voz alta
obliga a ordenarlo, y el desorden es donde se esconden los fallos.

Las cuatro piezas, por orden de importancia:

1. **Qué esperabas y qué pasó.** «Esperaba 1.400 filas y salen 0. El error es
   `ValueError: could not convert string to float: '10,50'`». El texto del error, entero y copiado,
   no una captura de pantalla: el texto se puede buscar, copiar y comparar.
2. **El ejemplo mínimo que falla.** Diez o quince líneas que se ejecutan solas y reproducen el
   problema, con los datos escritos a mano dentro. Sin tu base de datos, sin tu fichero de 40 MB.
3. **Qué has probado y qué descartaste.** «Probé a leer el CSV con `sep=';'` y con `dtype=str`:
   sigue fallando. Descarté el encoding porque el fichero abre bien en el editor.» Ahorra que te
   propongan lo que ya hiciste.
4. **Versiones y entorno.** `python --version`, la versión de la librería, el sistema operativo. El
   mismo código da resultados distintos en pandas 1 y en pandas 3, y quien responde no adivina cuál
   tienes.

Y antes de escribir nada: busca el mensaje de error exacto. Copiado entre comillas en un buscador
suele llevar a la documentación o a alguien con tu mismo problema; es más rápido que esperar
respuesta. Es el mismo reflejo que pide [[hacer-preguntas-buenas]]: pasar de la sensación al dato.

## Definición formal

Buscar el fallo en un script largo es una búsqueda por bisección. Si partes el ejemplo por la mitad
y te quedas con la mitad que sigue fallando, cada intento descarta la mitad de los sospechosos:

:::formula
cortes ≈ log₂(N / n_mín)
:::

- `N` — líneas del script que falla.
- `n_mín` — líneas del ejemplo mínimo que todavía reproduce el fallo.
- `cortes` — veces que hay que partir por la mitad, redondeando hacia arriba.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `N` | Tamaño del script que falla, tal como lo tienes | líneas | Cada línea de más es un sospechoso más: por eso se recorta antes de preguntar |
| `n_mín` | Tamaño del ejemplo mínimo que sigue fallando | líneas | Si sube, quien te ayuda tiene más que leer; si baja a cero, el fallo desapareció y ya has aprendido dónde estaba |
| `cortes` | Intentos necesarios para aislar el fallo | ninguna (recuento) | Es el precio de aislar. Con 5.000 líneas y un objetivo de 3 sale 11, no 4.997 |
:::

Y el paquete completo, como lista de comprobación:

:::formula
duda_respondible = ejemplo_mínimo + intentos + versiones + esperado_frente_a_observado
:::

:::figura
fichero: pedir-ayuda-recortar-por-mitades
pie: Dos formas de recortar un script de 5.000 líneas hasta el ejemplo mínimo. Quitando una línea por intento (naranja) harían falta 4.997; partiendo el ejemplo por la mitad y quedándose con la mitad que sigue fallando (azul) bastan 11 cortes, porque cada uno descarta la mitad de los sospechosos. La línea verde marca el objetivo: el ejemplo más pequeño que todavía reproduce el fallo.
fuente: figuras/pedir-ayuda-tecnica-1.py
:::

## Ejemplo

Un script de 5.000 líneas falla. Dos formas de reducirlo hasta las 3 líneas que reproducen el
fallo:

- **Quitando una línea cada vez:** 5.000 → 4.999 → 4.998… harían falta 4.997 intentos antes de
  llegar a 3 líneas. Nadie hace eso: se abandona antes.
- **Partiendo por la mitad y quedándote con la mitad que falla:** 5.000 → 2.500 → 1.250 → 625 → 313
  → 157 → 79 → 40 → 20 → 10 → 5 → 3. Son **11 cortes**, y en cada uno has descartado la mitad de
  los sospechosos.

Con el ejemplo ya reducido, el mensaje que se envía ocupa nueve líneas:

```text
Esperaba 1.400 filas con importe numérico; salen 0.

  ValueError: could not convert string to float: '10,50'

Ejemplo mínimo (2 líneas de datos, se ejecuta solo):

  import pandas as pd
  print(pd.to_numeric(pd.Series(["10,50", "20,00"]), errors="coerce").tolist())

Probé: leer el CSV con sep=';' y con dtype=str; sigue fallando.
Descarté el encoding: el fichero se abre bien en el editor.

Python 3.12.10 · pandas 3.0.6 · Windows 11
```

Fíjate en lo que ya no hace falta preguntar: con esas nueve líneas, quien responde sabe que el
problema es la coma decimal y no el fichero, el encoding ni la consulta. La conversación empieza en
la respuesta, no en veinte preguntas de ida y vuelta.

## Código

```python verificable
import pandas as pd

# Lo que ve el pipeline: una columna de importes que llega como texto con coma decimal.
importes = pd.Series(["10,50", "20,00", "sin dato"])
try:
    importes.astype(float)
except ValueError as error:
    print(f"error del pipeline: {error}")
# -> error del pipeline: could not convert string to float: '10,50'

# El ejemplo minimo: una sola llamada, sin ficheros ni base de datos de por medio.
# Deja ver que la causa no es el nulo, es la coma.
print(f"to_numeric('10,50') -> {pd.to_numeric('10,50', errors='coerce')}")   # -> nan
print(f"to_numeric('10.50') -> {pd.to_numeric('10.50', errors='coerce')}")   # -> 10.5
```

```python verificable
import pandas as pd

# Un ejemplo minimo tambien lleva escrito lo que esperabas. Sin esa linea, quien
# ayuda no sabe si el fallo esta en el codigo o en tu expectativa.
minimo = pd.Series(["10,50", "20,00"])
esperado = pd.Series([10.5, 20.0])
obtenido = pd.to_numeric(minimo, errors="coerce")

print(f"esperaba {esperado.tolist()}")            # -> [10.5, 20.0]
print(f"obtuve   {obtenido.tolist()}")            # -> [nan, nan]
print(f"coincide {obtenido.equals(esperado)}")    # -> False
```

```text
Plantilla de cuatro campos, para copiar y rellenar:

  QUÉ ESPERABA:  [el resultado que creías correcto, con números]
  QUÉ PASÓ:      [el mensaje de error completo, copiado como texto]

  EJEMPLO MÍNIMO: [10-15 líneas que se ejecutan solas y fallan igual]

  YA PROBÉ:      [qué intentaste y qué descartaste, con el motivo]

  VERSIONES:     python --version, versión de la librería, sistema operativo
```

:::claves
- `astype(float)` no devuelve `NaN` cuando no puede convertir: lanza `ValueError` y se para en el
  primer valor que falla. El mensaje cita el valor culpable, `'10,50'`.
- `pd.to_numeric(..., errors="coerce")` sí convierte a `NaN` lo que no entiende. Cambia un error
  ruidoso por un hueco silencioso: es una decisión tuya, no una solución.
- `errors="coerce"` no arregla la coma decimal: `"10,50"` no es un número ni para Python ni para
  pandas, así que desaparece convertido en `NaN` sin avisar.
- `Series.equals()` devuelve un `bool` de Python y compara valores y tipo. `(a == b).all()` no es lo
  mismo: con un `NaN` en la misma posición da `False` aunque `equals()` diga `True`.
- El ejemplo mínimo no necesita tus datos: dos cadenas de texto bastan para reproducir este fallo, y
  eso es exactamente lo que lo hace compartible.
- El bloque `text` de la plantilla es el mensaje entero. Si tu pregunta no cabe ahí, todavía no has
  reducido el problema.
:::

## Errores típicos

- **Escribir «no funciona» y esperar.** Sin decir qué esperabas y qué viste, quien responde tiene
  que adivinar el problema y el objetivo a la vez. Es la diferencia entre una pregunta y un suspiro.
- **Pegar el proyecto entero.** «Aquí está mi repositorio, ¿por qué falla?» traslada a otra persona
  el trabajo de reducir, que es justamente la parte que te enseña dónde está el fallo.
- **Pegar una captura de pantalla del error.** No se puede buscar, ni copiar, ni pegar en un
  buscador, y en el móvil no se lee. Copia el texto completo, incluida la última línea.
- **No dar las versiones.** El mismo código se comporta distinto entre versiones mayores de una
  librería. Sin ese dato, la respuesta puede ser correcta para otra versión y no servirte.
- **Incluir credenciales, tokens, rutas con tu nombre o datos reales de clientes.** Un ejemplo
  mínimo se escribe con datos inventados; lo que se pega en un foro se queda ahí para siempre.
- **Repetir lo que ya descartaste.** Si no cuentas qué probaste, la primera respuesta será
  proponerte lo que ya hiciste, y la conversación empieza perdiendo el tiempo.

## Comprueba que lo sabes

:::quiz
p: ¿Qué le falta a esta pregunta: «Tengo un error al leer mi CSV con pandas, ¿qué hago?»?
o: Nada: con eso ya se puede responder
o: El mensaje de error, el ejemplo mínimo, lo que ya probaste y la versión de pandas
o: Solo el nombre del fichero y su tamaño
a: 2
e: Falta todo lo que permite reproducir el fallo: sin el mensaje no se sabe qué falla, sin el ejemplo no se puede probar, sin los intentos se repiten pruebas y sin la versión no se sabe qué comportamiento esperar. El nombre y el tamaño del fichero no aportan nada.
:::

:::quiz
p: ¿Por qué conviene reducir el ejemplo partiendo por la mitad en vez de quitando líneas una a una?
o: Porque así el ejemplo queda más ordenado
o: Porque cada corte descarta la mitad de los sospechosos: 1 de 5.000 se aísla en unos 11 intentos y no en 4.997
o: Porque el ejemplo mínimo tiene que tener exactamente 3 líneas
a: 2
e: La bisección es lo que hace viable el trabajo: cada intento elimina la mitad de las posibles causas. Quitar líneas una a una elimina una sola por intento, y el ejemplo mínimo no tiene un tamaño fijo: tiene el tamaño más pequeño que sigue fallando.
:::

:::practica
enunciado: Reescribe esta pregunta con los cuatro campos: «Hola, mi script de ventas da error cuando lo ejecuto en el portátil del trabajo. En casa funcionaba. ¿Alguien sabe qué puede ser? Uso Jupyter».
pista: No tienes los datos, así que rellena los campos con lo que pedirías tú si tuvieras que responder: qué esperabas, qué pasó, un ejemplo que se ejecute solo y las versiones.
solucion: Un ejemplo de reescritura: «QUÉ ESPERABA: el DataFrame con 1.400 filas y la columna 'importe' en float. QUÉ PASÓ: `ValueError: could not convert string to float: '10,50'` al ejecutar la celda 3. EJEMPLO MÍNIMO: `pd.to_numeric(pd.Series(["10,50", "20,00"]), errors="coerce")` devuelve `[nan, nan]`. YA PROBÉ: `sep=';'` y `dtype=str`, sigue fallando; en casa funcionaba porque allí el CSV venía con punto decimal. VERSIONES: Python 3.12.10, pandas 3.0.6, Windows 11». La clave es que la frase «en casa funcionaba» se convierte en un dato: qué cambiaba entre los dos entornos.
:::

:::nota
Cuando un hilo se resuelve, cuenta qué funcionó. Es la parte que casi nadie hace y la que convierte
tu pregunta en la respuesta que encontrará el siguiente con tu problema.
:::
