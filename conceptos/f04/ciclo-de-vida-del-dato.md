---
id: ciclo-de-vida-del-dato
titulo: Ciclo de vida del dato
fase: 4
nivel: básico
rutas: [de, core]
prerequisitos: [calidad-de-datos, ficheros-y-encoding]
tags: [gobernanza, retencion, linaje, archivo, privacidad]
resumen: Todo dato recorre seis etapas, de la captura al borrado, y cada una tiene dueño, coste y plazo; lo que no se borra a tiempo acaba siendo un pasivo.
fuentes: ["DAMA International, 'DAMA-DMBOK: Data Management Body of Knowledge'", "Reglamento (UE) 2016/679 (RGPD), art. 5.1.e"]
---

## En una frase

El ciclo de vida del dato es el recorrido completo de un dato —capturarlo, guardarlo,
transformarlo, servirlo, archivarlo y borrarlo— y cada etapa necesita dueño, formato, coste y
fecha de caducidad.

## La idea

Un dato no nace en una tabla limpia ni muere cuando el informe sale bien. Nace cuando alguien
pulsa un botón o un sensor manda una medida; pasa por copias, transformaciones y modelos; y
sigue existiendo cuando ya nadie lo usa. Ese «sigue existiendo» es la parte que casi nadie
diseña, y es la que genera la mitad de los problemas: consultas lentísimas sobre años de datos
que nadie mira, costes de almacenamiento que crecen sin explicación y datos personales que
deberían haberse borrado hace tres años.

Piensa en un almacén físico. Recepción de mercancía, estanterías, taller donde se transforma el
producto, mostrador donde se vende, almacén de archivo y, por último, destrucción con
certificado. Si te saltas el mostrador, tienes producto que nadie compra; si te saltas la
destrucción, tienes un local lleno de cosas caducadas.

Las seis etapas, con lo que hay que decidir en cada una:

1. **Captura.** De dónde viene el dato y con qué calidad entra. Aquí se decide el **grano**
   (una fila por pedido o por línea de pedido), el formato y si se guarda el dato en crudo tal
   como llegó. Regla práctica: guarda siempre una copia inmutable de lo que recibiste, porque
   las transformaciones se reescriben y lo recibido no.
2. **Almacenamiento.** Dónde vive cada copia: el sistema de la aplicación, el lago en crudo, el
   almacén curado. Influye en el coste y en la velocidad: el mismo terabyte cuesta muy distinto
   en un disco caliente que en almacenamiento frío.
3. **Transformación.** Limpiar, unificar, agregar y calcular. Cada paso debe ser reproducible
   (código versionado) e **idempotente** (ejecutarlo dos veces da el mismo resultado, no el
   doble de filas). Aquí es donde entra el linaje: saber qué informe depende de qué tabla.
4. **Servicio.** Poner el dato donde se consume: un panel, una API, un modelo, un informe.
   Importan la **frescura** (cuánto tarda en estar disponible) y el contrato: qué columnas,
   con qué significado y a qué hora.
5. **Archivado.** Mover a almacenamiento barato lo que ya no se consulta a diario, pero que
   hay que conservar por obligación o por historia. Archivado no es borrado: el dato sigue
   existiendo y sigue contando para la privacidad.
6. **Borrado.** Eliminarlo de verdad, incluidas las copias, las réplicas y las copias de
   seguridad. Un dato «borrado» que sigue en tres backups no está borrado.

La fuerza que ordena todo esto es la **retención**: cuánto tiempo se conserva cada dato y por
qué. Sin plazo, la etapa 6 nunca llega y las etapas 1 a 5 se acumulan. El RGPD lo dice de forma
explícita para datos personales: se conservan «no más tiempo del necesario» para la finalidad
(art. 5.1.e), y eso obliga a que el borrado sea una tarea programada, no una buena intención.

Un aviso de coste real: el almacenamiento caliente es lo caro y las **consultas** sobre él lo
son más. El mismo volumen de datos en almacenamiento frío puede costar del orden de diez veces
menos, y mover a frío lo que no se consulta es la optimización más simple que existe.

## Definición formal

Para cada conjunto de datos `D` se definen seis atributos:

- **Origen** `origen(D)`: el sistema o la fuente que lo produce (formulario, sensor, API de
  terceros, fichero manual).
- **Grano** `grano(D)`: la unidad que representa una fila. Se enuncia siempre en una frase
  («una fila por pedido y día»); si no puedes enunciarlo, tu tabla tiene dos granos mezclados.
- **Frescura** `Δ(D)`: el retraso máximo aceptable entre el hecho y su disponibilidad en el
  punto de servicio. Se mide en minutos, horas o días, y es una promesa, no una observación.
- **Retención** `R(D)`: el plazo durante el cual se conserva, con su base (obligación legal,
  contrato, interés legítimo, histórico).
- **Clasificación** `C(D)`: el nivel de sensibilidad (público, interno, confidencial, datos
  personales, categorías especiales). Determina quién puede verlo y con qué controles.
- **Dueño** `dueño(D)`: la persona o el equipo responsable de que los cinco atributos
  anteriores sigan siendo verdad. Sin dueño, el dato se degrada.

La regla que resume el ciclo:

:::formula
coste total = capturar + almacenar + transformar + servir + archivar + borrar
:::

Si `R(D)` no está definido, el último sumando es cero y todos los demás crecen sin límite.

## Ejemplo

Un comercio electrónico con 40.000 pedidos al mes (unos 480.000 al año) decide el ciclo de
vida de su tabla de pedidos:

| Etapa | Qué se hace | Plazo | Volumen |
| --- | --- | --- | --- |
| Captura | La web escribe el pedido en la base de la aplicación | Inmediato | 40.000 filas al mes |
| Almacenamiento | Copia nocturna al lago en crudo, formato Parquet | Diaria | 480.000 filas al año |
| Transformación | Limpieza y agregados por día, tienda y producto | Cada noche | 365 filas de agregado diario |
| Servicio | Panel de ventas y modelo de previsión de demanda | Frescura 6 h | Consulta diaria |
| Archivado | Pedidos de más de 24 meses a almacenamiento frío | A los 24 meses | Unos 960.000 pedidos en frío |
| Borrado | Datos personales de pedidos cerrados según retención fiscal | 5 años | Automático, mensual |

Decisiones concretas que salen de esta tabla:

- **Frescura**: si el negocio solo mira el panel cada mañana, prometer 5 minutos de frescura es
  pagar por algo que nadie usa. Seis horas bastan, y abaratan todo el diseño.
- **Archivado**: a los 24 meses, los 960.000 pedidos antiguos pasan a almacenamiento frío. Si
  ese almacenamiento cuesta diez veces menos, el ahorro es directo y no se pierde nada: siguen
  consultables, solo que más despacio.
- **Borrado**: a los 5 años se eliminan los datos personales de esos pedidos. Pero el agregado
  diario (365 filas al año, sin datos personales) se conserva: sirve para comparar años y no
  identifica a nadie. Esa es la jugada habitual y correcta: **borrar el detalle personal y
  conservar el agregado**.

## Código

```python verificable
# Las etapas del ciclo de vida, aplicadas a pedidos que van avanzando de estado
from datetime import date

HOY = date(2026, 3, 1)
RETENCION_DIAS = 365 * 5           # obligacion fiscal: cinco anios
ARCHIVO_DIAS = 365 * 2             # a partir de dos anios, almacenamiento frio

def etapa(alta, hoy=HOY, retencion=RETENCION_DIAS, archivo=ARCHIVO_DIAS):
    dias = (hoy - alta).days
    if dias > retencion:
        return "borrado"
    if dias > archivo:
        return "archivado"
    if dias > 1:
        return "servicio"
    return "captura"

pedidos = [("P-1", date(2026, 2, 28)), ("P-2", date(2025, 6, 1)),
           ("P-3", date(2023, 1, 10)), ("P-4", date(2020, 1, 15))]

for pid, alta in pedidos:
    print(f"{pid}: {(HOY - alta).days:>5} dias -> {etapa(alta)}")
```

```python verificable
# El ciclo de vida como datos: dueño, clasificacion y plazo por conjunto
REGISTRO = [
    {"conjunto": "pedidos", "dueno": "equipo-ventas", "clasificacion": "personal", "retencion_dias": 1825},
    {"conjunto": "ventas_diarias", "dueno": "equipo-datos", "clasificacion": "interno", "retencion_dias": 3650},
    {"conjunto": "clics_web", "dueno": "equipo-marketing", "clasificacion": "personal", "retencion_dias": 400},
    {"conjunto": "catalogo", "dueno": "equipo-catalogo", "clasificacion": "publico", "retencion_dias": 3650},
]

# Regla de revision: todo conjunto con datos personales debe caducar en menos de 3 anios
LIMITE_PERSONAL = 1095
revisar = [c["conjunto"] for c in REGISTRO
           if c["clasificacion"] == "personal" and c["retencion_dias"] > LIMITE_PERSONAL]

print("conjuntos con datos personales a revisar:", len(revisar))   # -> 1
print("el que se pasa:", revisar[0])                              # -> pedidos
print("sin dueno:", sum(1 for c in REGISTRO if not c["dueno"].strip()))   # -> 0

media = sum(c["retencion_dias"] for c in REGISTRO) / len(REGISTRO)
print("retencion media en anios:", round(media / 365, 1))          # -> 6.5
```

```text
Un ciclo de vida sano, resumido en una linea por etapa:

captura         -> crudo/2026-03-01/pedidos.jsonl   (inmutable, nunca se edita)
almacenamiento  -> limpio/pedidos/                  (Parquet particionado por fecha)
transformacion  -> marts/ventas_diarias/            (dbt, versionado en Git)
servicio        -> panel + API /ventas/diarias      (frescura prometida: 6 h)
archivado       -> frio/pedidos/anio=2023/          (consultable, mas lento y mas barato)
borrado         -> job mensual que purga datos personales con mas de 5 anios
```

## Errores típicos

- **No definir la retención.** «Lo guardamos todo por si acaso» es una decisión, y es la peor:
  el almacenamiento y las consultas crecen cada mes y el borrado, cuando llega la auditoría, se
  hace a mano y con prisa. Define el plazo por conjunto y escríbelo en un sitio que se lea.
- **Confundir archivar con borrar.** Mover a almacenamiento frío no elimina nada: los datos
  personales siguen ahí y siguen sujetos al RGPD. Si la finalidad era el borrado, hay que
  borrar de verdad, incluidas réplicas y copias de seguridad.
- **Olvidar las copias de seguridad en el borrado.** Un borrado que no llega a los backups deja
  el dato vivo. La solución habitual no es tocar los backups, sino documentar que caducan por
  rotación en un plazo máximo (por ejemplo 35 días) y que no se restauran sin pasar el proceso
  de purga.
- **Transformar el dato en crudo en el sitio.** Si la tubería limpia los ficheros originales,
  el día que cambies una regla de negocio ya no podrás recalcular el pasado. Guarda el crudo
  intacto y escribe los resultados aparte.
- **Publicar un dato sin contrato ni frescura prometida.** El consumidor no sabe si el dato de
  ayer está completo o a medias, y empieza a mirar la hora a la que corre el proceso. Declara
  columnas, significado y hora de disponibilidad, y avisa cuando no se cumpla.
- **No tener dueño.** Los conjuntos sin dueño son los que nadie actualiza, los que se rompen en
  silencio y los que se quedan fuera de toda limpieza. El dueño no tiene que programar: tiene
  que responder de que el dato sigue siendo correcto y está vivo.
- **Borrar el detalle y tirar también el agregado.** Cuando purgas datos personales, no borres
  los agregados sin datos personales: son justo lo que necesitas para análisis histórico y no
  identifican a nadie.

## Comprueba que lo sabes

:::quiz
p: Un conjunto con datos personales se mueve a almacenamiento frío a los dos años y se queda ahí diez años más. ¿Está resuelto el problema de privacidad?
o: Sí, porque el almacenamiento frío no es accesible desde la web
o: No, porque archivado no es borrado: el dato sigue existiendo y sigue sujeto a los plazos de conservación
o: Sí, siempre que se guarde cifrado
a: 2
e: Archivar cambia el coste y la velocidad de acceso, no la existencia del dato. Si el plazo de conservación se ha cumplido, hay que borrarlo también del archivo, de las réplicas y de las copias que no caduquen por rotación.
:::

:::quiz
p: ¿Qué significa que el grano de una tabla sea «una fila por pedido y día»?
o: Que la tabla solo guarda un pedido al día
o: Que cada fila representa la combinación de un pedido y una fecha, y no hay dos filas para esa misma combinación
o: Que la tabla se particiona por día
a: 2
e: El grano es la definición de qué representa una fila, y tiene que ser única y enunciable en una frase. Particionar por día es una decisión de almacenamiento distinta del grano, y «un pedido al día» sería una regla de negocio, no el grano.
:::

:::quiz
p: ¿Por qué conviene conservar el agregado diario de ventas aunque se borren los datos personales de los pedidos antiguos?
o: Porque el agregado no identifica a nadie y permite comparar años sin conservar el detalle personal
o: Porque el agregado es obligatorio por ley
o: Porque el agregado ocupa más y compensa el borrado
a: 1
e: El agregado sin datos personales no entra en el ámbito de protección de datos y sirve para el análisis histórico. Es la separación clásica: borras el detalle con identificadores y conservas la serie agregada. Ninguna ley obliga a guardar el agregado, y desde luego no compensa nada por ocupar más.
:::

:::aviso
La frescura es una promesa que se cumple o se rompe, no una aspiración. Si prometes seis horas
y el proceso tarda ocho, tienes un incidente aunque el dato esté bien: alguien tomó una
decisión con la versión de ayer creyendo que era la de hoy.
:::
