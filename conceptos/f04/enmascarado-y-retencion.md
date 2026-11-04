---
id: enmascarado-y-retencion
titulo: Enmascarado y retención
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [gobierno-y-privacidad, privacidad-y-gdpr]
tags: [pii, anonimizacion, retencion]
resumen: Hash, tokenización y k-anonimato aplicados a un almacén real, y cómo se borra un dato a petición sin romper el histórico que ya calculaste.
fuentes: ["NIST (2015), 'SP 800-122, Guide to Protecting PII'", "AEPD (2023), 'Guía sobre anonimización y seudonimización'"]
---

## En una frase

Enmascarar es sustituir un dato personal por otro que sirve para lo mismo operativamente pero no
identifica a nadie, y retener es decidir cuánto tiempo guardas el original antes de borrarlo.

## La idea

Un almacén de datos crece copiando todo lo que pasa. En algún punto aparece una columna con un
teléfono, un correo o un Documento Nacional de Identidad, y con ella una obligación legal que nadie
recuerda haber aceptado: ese dato tiene que protegerse, limitarse a la finalidad y borrarse cuando
ya no haga falta.

Hay cuatro técnicas y no son intercambiables. **Enmascarar** tapa parte del valor para que una
persona lo use sin verlo. **Hashear** sustituye el valor por una huella, pero si el dominio es
pequeño (un teléfono, un correo) se puede revertir por fuerza bruta con un diccionario.
**Tokenizar** guarda el original en un sistema aparte y usa un identificador sin significado.
**Anonimizar** de verdad significa que no se puede reidentificar ni cruzando con otros datos, y eso
casi nunca se consigue con una columna sola: es una propiedad del conjunto.

La retención es la otra mitad. Una tabla sin política de borrado crece hasta que alguien pregunta
cuánto cuesta, y para entonces ya hay datos que no deberías tener. La política se escribe antes,
con fechas, y se ejecuta sola.

:::trampa
Un hash sin clave de un correo no es anonimización. Con una lista de correos conocidos, cualquiera
calcula el hash y compara: el espacio de entrada es tan pequeño que la huella deja de ser secreta.
Para que no se pueda revertir hace falta una clave secreta (HMAC) o un sal, y el sal tiene que
guardarse aparte.
:::

## Definición formal

Cada técnica protege de una amenaza distinta; elegir mal es peor que no hacer nada porque da una
sensación falsa de seguridad.

:::formula
seudonimizar: token = HMAC(clave_secreta, dato)        anonimizar: k ≥ k_min en todos los grupos
:::

- **HMAC** — hash con clave; sin la clave no se puede recalcular ni buscar por diccionario.
- **token** — identificador estable que permite cruzar tablas sin exponer el dato.
- **k** — número de individuos que comparten la misma combinación de atributos cuasi
  identificadores (código postal, edad, sexo).
- **k_min** — umbral de tu organización; por debajo, ese grupo identifica a alguien.

**Retención** se escribe como una regla con dos campos: qué se guarda y hasta cuándo, más qué pasa
al vencer (borrar, agregar, archivar). Y el derecho de supresión obliga a poder borrar **todas** las
copias: la tabla, el histórico, las copias de seguridad y los ficheros congelados.

## Ejemplo

Una tabla con código postal y ciudad, tres filas de Madrid y dos de Sevilla.

- Grupos distintos: 3 combinaciones.
- k mínimo: 1, porque Barcelona aparece una sola vez. Con k = 1 no hay anonimato: esa fila es una
  persona identificable si alguien conoce el dato.
- Filas únicas: 1.

Con esas cifras, esa tabla no se puede publicar. Habría que agrupar el código postal en rangos,
subir la edad a tramos de diez años o eliminar la columna de ciudad, y volver a medir hasta que
todos los grupos tengan al menos el k mínimo.

## Código

```python verificable
import hashlib
import hmac
from collections import Counter

clave = b"clave-secreta-de-ejemplo"

def token(texto):
    return hmac.new(clave, texto.encode(), hashlib.sha256).hexdigest()[:12]

print(token("12345678A"), token("12345678A"), token("87654321B"))  # -> a66759ad9738 a66759ad9738 259a6586c28e

filas = [("28", "Madrid"), ("28", "Madrid"), ("28", "Madrid"),
         ("41", "Sevilla"), ("41", "Sevilla"), ("08", "Barcelona")]
grupos = Counter(filas)
print(f"grupos {len(grupos)}")                       # -> grupos 3
print(f"k minimo {min(grupos.values())}")            # -> k minimo 1
print(f"filas unicas {sum(1 for v in grupos.values() if v == 1)}")  # -> filas unicas 1
```

Las dos primeras salidas muestran que el token es estable —el mismo dato da el mismo token— y que
no se puede adivinar sin la clave. Las tres últimas miden si la tabla anonimiza: con k = 1, no.

:::claves
- `hmac.new(clave, ...)` y no `hashlib.sha256(dato)`: el hash simple es reversible por diccionario
  en dominios pequeños, el HMAC no sin la clave.
- `.hexdigest()[:12]` recorta el token. Doce caracteres hexadecimales son 48 bits: suficiente para
  cruzar tablas, insuficiente para que la colisión sea probable en millones de filas.
- El token es **estable**: el mismo dato da siempre el mismo valor. Eso permite cruzar tablas y a la
  vez impide leer el dato. Si el token cambiara en cada ejecución, no serviría para unir.
- `Counter(filas)` cuenta combinaciones completas, no columnas sueltas. La k-anonimidad se mide
  sobre la combinación de cuasi identificadores, que es lo que reidentifica.
- `min(grupos.values())` da el k de la tabla. Un solo grupo de tamaño 1 hunde el anonimato de todo
  el conjunto: no se promedia, se toma el mínimo.
:::

## Errores típicos

- **Confundir hash con anonimización.** Con datos de baja cardinalidad, un hash sin clave se revierte
  probando valores. No protege.
- **Guardar el sal o la clave en la misma tabla.** Si viajan juntos, la protección es decorativa.
- **Publicar una tabla con k = 1.** Un solo registro único reidentifica a una persona aunque el
  resto esté agregado.
- **Enmascarar solo en la vista.** Si la tabla base conserva el dato, cualquiera con permisos lo ve;
  y si el enmascarado es una expresión de la consulta, un `SELECT *` puede saltarlo.
- **No tener política de retención.** Sin fecha de caducidad, los datos se quedan para siempre y el
  coste y el riesgo crecen sin que nadie lo decida.
- **Creer que borrar la fila basta.** El derecho de supresión incluye copias de seguridad,
  históricos y ficheros exportados. Si no está en el procedimiento, no se cumple.

:::practica
enunciado: Tienes una tabla con fecha de nacimiento exacta, código postal de cinco dígitos y sexo. ¿Qué dos cambios aplicarías para que sea publicable y cómo comprobarías que funciona?
pista: Ninguno de los tres campos identifica solo, pero los tres juntos sí.
solucion: Convertir la fecha en tramo de edad de cinco años, agrupar el código postal en los dos primeros dígitos y mantener el sexo; después recalcular el k mínimo de la combinación y comprobar que todos los grupos superan el umbral. Se comprueba contando grupos y tomando el mínimo, no la media.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué un hash simple de un correo no anonimiza?
o: Porque el conjunto de correos posibles es lo bastante pequeño para probarlos y comparar
o: Porque el hash ocupa demasiado espacio
o: Porque el correo no es un dato personal
a: 1
e: Sin clave, el hash es una función pública: cualquiera calcula el de una lista de correos conocidos y busca coincidencias. La protección real exige una clave secreta (HMAC) o no guardar el dato en absoluto.
:::

:::quiz
p: Una tabla tiene grupos de tamaño 5, 5, 5 y 1. ¿Cuál es su k-anonimidad?
o: 1, porque el mínimo manda
o: 4, porque es la media de los grupos
o: 16, porque es el total de filas
a: 1
e: La k-anonimidad se define por el grupo más pequeño: si existe un grupo de uno, esa persona es única y la tabla no protege. Promediar ocultaría justo el caso que rompe la garantía.
:::
