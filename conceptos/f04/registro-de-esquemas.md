---
id: registro-de-esquemas
titulo: Registro de esquemas
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [evolucion-de-esquema, kafka-y-colas]
tags: [avro, compatibilidad, streaming]
resumen: El contrato que productores y consumidores comparten en streaming, y por qué añadir un campo sin valor por defecto rompe a todos los que leen.
fuentes: ["Confluent (2024), 'Schema Registry documentation'", "Apache Avro (2024), 'Schema Resolution'"]
---

## En una frase

Un registro de esquemas es un servicio que guarda la versión vigente del contrato de cada tema y
rechaza los cambios que romperían a quien ya está leyendo.

## La idea

En un fichero Parquet el esquema viaja con los datos: quien lo lee sabe qué hay dentro. En un tema
de mensajes no. El productor escribe bytes y el consumidor tiene que saber interpretarlos, así que
el contrato vive fuera, en la cabeza de alguien o en un documento que se queda viejo.

El registro resuelve eso guardando el esquema por tema y por versión, con un identificador. Cada
mensaje lleva delante ese identificador —unos pocos bytes—, y el consumidor pide el esquema al
registro la primera vez y lo cachea. Así el productor puede evolucionar el mensaje sin coordinar
una ventana de despliegue con cada consumidor: solo tiene que respetar las reglas de
compatibilidad.

Esas reglas son la parte que se pregunta en las entrevistas. Añadir un campo **con valor por
defecto** es compatible hacia atrás: el lector nuevo rellena el hueco con el defecto cuando lee
datos viejos. Añadirlo **sin defecto** rompe: el lector no sabe qué poner. Quitar un campo rompe a
los lectores antiguos; cambiar un tipo de `int` a `string` rompe a todos.

:::trampa
«Compatible hacia atrás» y «hacia delante» no son lo mismo y se confunden en la mitad de los
diseños. Hacia atrás: el consumidor nuevo lee datos viejos. Hacia delante: el consumidor viejo lee
datos nuevos. Un cambio puede ser una y no la otra, y el modo que elijas depende de quién se
despliega primero.
:::

## Definición formal

Los modos de compatibilidad definen qué cambios acepta el registro:

:::formula
backward: nuevo lee viejo     forward: viejo lee nuevo     full: las dos     none: sin control
:::

- **backward** — se permite añadir campos con defecto y quitar campos opcionales. Es el modo por
  defecto en la mayoría de instalaciones y el más seguro si actualizas consumidores después.
- **forward** — se permite quitar campos y añadir opcionales. Útil si actualizas productores
  después.
- **full** — las dos cosas a la vez: el cambio tiene que ser compatible en ambos sentidos.
- **none** — el registro no valida; es lo mismo que no tener registro, pero con más pasos.

Y una regla de evolución que resume casi todo: **todo campo nuevo lleva valor por defecto y todo
campo retirado deja de leerse, no se borra del contrato hasta que nadie lo use**.

## Ejemplo

Tres versiones de un mensaje de pedido, evaluadas contra la v1:

- v2 añade `moneda: str` obligatorio → **no compatible**: el lector nuevo no sabe qué moneda poner
  al leer un mensaje viejo.
- v3 añade `moneda: str = "EUR"` → **compatible**: el defecto rellena el hueco.
- v4 quita `importe` → **no compatible**: el lector viejo espera un campo que ya no llega.

El registro devolvería error al registrar v2 y v4, y el productor tendría que arreglarlo antes de
publicar. Ese error temprano es todo el valor del servicio.

## Código

```python verificable
# Comprobacion minima de compatibilidad hacia atras: el lector NUEVO lee datos VIEJOS
def compatible(viejo, nuevo):
    # None en el valor significa que el campo lleva valor por defecto
    quitados = [c for c in viejo if c not in nuevo]
    anadidos = [c for c in nuevo if c not in viejo]
    return len(quitados) == 0 and all(nuevo[c] is None for c in anadidos)

v1 = {"pedido_id": "str", "importe": "double"}
v2 = {"pedido_id": "str", "importe": "double", "moneda": "str"}
v3 = {"pedido_id": "str", "importe": "double", "moneda": None}
v4 = {"pedido_id": "str"}

print(f"v1 a v2 {compatible(v1, v2)}")   # -> v1 a v2 False
print(f"v1 a v3 {compatible(v1, v3)}")   # -> v1 a v3 True
print(f"v1 a v4 {compatible(v1, v4)}")   # -> v1 a v4 False
```

Las tres líneas son la regla entera: añadir sin defecto falla, añadir con defecto pasa, quitar
falla.

:::claves
- `quitados` se calcula sobre el esquema viejo: un campo que existía y ya no está es una retirada,
  y rompe a quien lo lee.
- `all(...)` exige que **todos** los campos añadidos tengan defecto. Uno solo obligatorio hunde el
  cambio entero.
- El valor `None` se usa aquí como marca de «tiene defecto». En Avro el defecto es un atributo
  `default` del campo, no el tipo.
- Esta comprobación es hacia atrás. Para el modo `full` habría que comprobar también
  `compatible(nuevo, viejo)`, que es la dirección contraria.
- `v4` no tiene `moneda` ni `importe`: quitar un campo es incompatible aunque el nuevo esquema sea
  más pequeño, porque el consumidor antiguo sigue esperándolo.
:::

## Errores típicos

- **Añadir un campo obligatorio sin defecto.** Es el fallo más común y rompe a todos los
  consumidores que lean mensajes anteriores.
- **Confundir los modos de compatibilidad.** Elegir `forward` cuando despliegas consumidores
  después convierte un cambio seguro en una caída.
- **Validar solo en producción.** El registro debe validar en desarrollo y en CI: el error tiene que
  salir antes del despliegue.
- **Guardar el esquema en el código del productor.** Dos productores con copias distintas acaban
  en dos contratos que se llaman igual y no son iguales.
- **Borrar un campo del contrato el mismo día que se deja de usar.** Los consumidores antiguos
  siguen leyendo datos antiguos. Se retira cuando ya no hay ninguno, y eso se comprueba.
- **No versionar el significado.** Cambiar la unidad de un campo de euros a céntimos no cambia el
  tipo y sí cambia el dato. La compatibilidad de esquema no detecta un cambio semántico.

:::practica
enunciado: Un tema tiene consumidores que se despliegan una semana después del productor. ¿Qué modo de compatibilidad eliges y qué cambio concreto rechazarías?
pista: Si el productor va primero, los consumidores antiguos tienen que poder leer lo nuevo.
solucion: Modo forward o full. Rechazaría añadir un campo obligatorio sin defecto —rompe a los consumidores antiguos— y quitar un campo que los antiguos usan. Añadir un campo con defecto y quitar uno opcional son los cambios que sí pasan.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué significa que un cambio sea compatible hacia atrás?
o: Que el consumidor nuevo puede leer datos escritos con el esquema viejo
o: Que el productor viejo puede escribir con el esquema nuevo
o: Que el esquema se puede revertir sin perder datos
a: 1
e: Hacia atrás mira al pasado: el lector nuevo se enfrenta a mensajes antiguos. La otra dirección, el lector viejo con mensajes nuevos, es la compatibilidad hacia delante.
:::

:::quiz
p: Añades un campo `pais` de tipo texto sin valor por defecto a un tema con consumidores activos. ¿Qué pasa?
o: El registro lo rechaza en modo backward porque el lector nuevo no puede rellenar el hueco en mensajes viejos
o: Nada: añadir campos siempre es compatible
o: Los consumidores nuevos fallan pero los viejos no
a: 1
e: Sin defecto, al leer un mensaje antiguo no hay valor para `pais` y el contrato no dice qué poner. Con `default` el problema desaparece; sin él, la compatibilidad se rompe.
:::
