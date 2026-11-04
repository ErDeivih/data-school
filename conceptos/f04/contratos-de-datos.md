---
id: contratos-de-datos
titulo: Contratos de datos
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [calidad-de-datos, calidad-y-slas]
tags: [gobierno, esquema, compatibilidad, productor]
resumen: El contrato fija esquema, semántica, calidad y política de cambios entre productor y consumidor, y sólo sirve si un test lo comprueba en cada despliegue.
fuentes: ["Reis & Housley (2022), 'Fundamentals of Data Engineering'", "Dehghani (2022), 'Data Mesh'"]
---

## En una frase

Un contrato de datos es lo que el productor se compromete a entregar —esquema, significado,
calidad y plazos— y lo que el consumidor puede exigir de forma automática cuando no se cumple.

## La idea

El equipo de marketing renombra la columna `importe` a `amount` en su evento, o cambia su unidad
de euros a céntimos. Nadie avisa. Tres días después, el cuadro de finanzas muestra cifras cien
veces mayores y se descubre por un mensaje en un canal de chat.

La causa no es técnica: es de frontera. Dentro de un equipo los cambios se hablan en la reunión
del lunes. Entre equipos, el productor no sabe quién consume su tabla ni para qué, así que no
tiene a quién avisar; y el consumidor no puede saber que el campo que usa va a cambiar. El
contrato pone esa frontera por escrito **y la automatiza**, que es la parte que de verdad cuenta:
un contrato que sólo vive en una wiki se incumple en la primera semana con prisa.

Un contrato tiene cinco partes:

1. **Identidad y versión.** Nombre del conjunto de datos, productor, consumidores conocidos y
   versión. Sin versión no hay forma de hablar de compatibilidad.
2. **Esquema.** Nombres, tipos, nulabilidad, unidades y dominio permitido. `importe_centimos` y
   `importe_euros` tienen el mismo tipo y significan cosas distintas: la unidad forma parte del
   contrato, no del comentario.
3. **Semántica.** Qué significa cada campo y qué **no** significa. `fecha_pedido` es la fecha de
   creación del pedido, no la de envío; si nadie lo escribe, cada consumidor elegirá una.
4. **Garantías de calidad.** Unicidad de la clave, frescura máxima, completitud mínima, rangos
   válidos. Son los mismos indicadores de [[calidad-y-slas]], pero prometidos a otro equipo.
5. **Política de cambios.** Qué cambios son compatibles, con cuánto aviso, durante cuánto tiempo
   se mantiene la versión antigua y cómo se retira un campo.

La clasificación de cambios que hay que tener clara:

- **Compatible (aditivo).** Añadir una columna **opcional**; añadir un valor nuevo a un campo
  cuya documentación dice «pueden aparecer valores nuevos, ignora los que no conozcas»; relajar
  una restricción (de no nulo a nulo).
- **Incompatible (ruptura).** Renombrar, eliminar, cambiar el tipo, cambiar la unidad, cambiar el
  significado, hacer obligatorio un campo nuevo, o **añadir un valor nuevo a un dominio cerrado**
  que el consumidor valida con `accepted_values`.

Ese último es el que todo el mundo olvida, porque no toca el esquema. Pasar de tres estados a
siete no cambia ni un tipo, y rompe a cualquier consumidor que tenga un `CASE` sobre esos tres.

:::trampa
Un contrato no es un documento: es un test. Si el productor puede desplegar sin que nada se ponga
rojo, el contrato es decorativo. La única forma de que se cumpla es que la validación viva en la
integración continua del productor y que el despliegue se bloquee cuando falla.
:::

## Definición formal

Un contrato `C` sobre un conjunto de datos `D` es una tupla:

:::formula
C = (E, S, Q, V)
:::

Símbolos:

- `E` — el esquema: para cada columna, un nombre, un tipo, si admite nulos, su unidad y su
  dominio de valores permitidos.
- `S` — la semántica: la descripción en una frase de qué representa cada columna y de qué no.
- `Q` — las garantías de calidad: unicidad de la clave, frescura máxima, completitud mínima.
- `V` — la versión, con la política de compatibilidad asociada.

Un lote de datos `L` **cumple** el contrato si pasa todas las comprobaciones de `E` y de `Q`. La
propiedad que hace útil todo esto es la monotonía de los cambios compatibles:

:::formula
si C₁ → C₂ es compatible, todo consumidor que valide contra C₁ sigue funcionando con C₂
:::

Y la definición operativa de cambio incompatible, que es la que se puede comprobar sin discutir:

:::formula
C₁ → C₂ es incompatible si existe un lote válido para C₁ que es rechazado por C₂
:::

Es decir: un cambio es compatible si **ningún dato que antes era válido deja de serlo**. Añadir
una columna opcional no invalida nada; cambiar `importe` de euros a céntimos invalida todos los
valores plausibles del rango anterior.

## Ejemplo

Contrato de `eventos_pedido`, versión 1.2.0. El campo `estado` admite los valores
`creado`, `pagado` y `enviado`. Nueve de cada diez cuadros de mando usan una expresión del tipo
`CASE WHEN estado = 'enviado' THEN 1 ELSE 0 END`, y la métrica «pedidos activos» se calcula
restando los `creado`.

El 3 de junio el productor añade cuatro valores nuevos: `devuelto`, `cancelado`, `en_reparto` y
`entregado`. En el primer lote llegan 12.400 de 380.000 filas con valores nuevos, un **3,3 %**.

- El tipo no ha cambiado: sigue siendo texto. Ningún test de esquema se queja.
- El `CASE WHEN estado = 'enviado'` sigue funcionando, pero ahora sólo cuenta uno de los dos
  estados que significan «ya salió»: `entregado` también lo es.
- La métrica «pedidos activos» cuenta las devoluciones como activas, así que sobreestima un
  4,1 %.

El resultado: nadie ha roto el esquema y tres informes están mal. Si el contrato hubiera dicho
«dominio cerrado: creado, pagado, enviado», el lote habría fallado en la puerta y la conversación
habría ocurrido antes de publicar, que es cuando sale gratis.

## Código

```python verificable
import pandas as pd

# Contrato v1 de un evento de pedido: lo que el productor promete.
contrato = {
    "pedido_id": {"nulos": False, "unico": True},
    "importe_centimos": {"nulos": False, "min": 0},
    "estado": {"nulos": False, "dominio": {"creado", "pagado", "enviado"}},
}

lote = pd.DataFrame({
    "pedido_id": ["P1", "P2", "P3", "P3"],
    "importe_centimos": [1599, -250, 800, 420],
    "estado": ["pagado", "creado", "devuelto", "enviado"],
})

def validar(df, contrato):
    """Devuelve la lista de incumplimientos; vacia significa que el lote cumple."""
    fallos = []
    for col, regla in contrato.items():
        if col not in df.columns:
            fallos.append(f"falta la columna {col}")
            continue
        if not regla["nulos"] and df[col].isna().any():
            fallos.append(f"{col}: hay nulos")
        if regla.get("unico") and df[col].duplicated().any():
            fallos.append(f"{col}: hay duplicados ({int(df[col].duplicated().sum())})")
        if "min" in regla and (df[col] < regla["min"]).any():
            fallos.append(f"{col}: {int((df[col] < regla['min']).sum())} valores por debajo de {regla['min']}")
        if "dominio" in regla:
            fuera = sorted(set(df[col]) - regla["dominio"])
            if fuera:
                fallos.append(f"{col}: valores fuera del dominio {fuera}")
    return fallos

for fallo in validar(lote, contrato):
    print("FALLO", fallo)
# -> FALLO pedido_id: hay duplicados (1)
# -> FALLO importe_centimos: 1 valores por debajo de 0
# -> FALLO estado: valores fuera del dominio ['devuelto']
```

```yaml
# contrato: eventos_pedido  version: 1.2.0  productor: equipo-checkout
# Politica: los campos nuevos se anaden opcionales; el dominio de 'estado'
# es cerrado y anadir un valor exige subir a 2.0.0 y avisar con 30 dias.
campos:
  - nombre: pedido_id
    tipo: string
    nulos: false
    unico: true
  - nombre: importe_centimos
    tipo: integer
    nulos: false
    minimo: 0
    semantica: Importe total en centimos, con impuestos incluidos.
  - nombre: estado
    tipo: string
    nulos: false
    dominio: [creado, pagado, enviado]
    semantica: Estado actual del pedido; 'enviado' no incluye la entrega.
garantias:
  frescura_maxima_minutos: 60
  completitud_minima: 0.995
```

## Errores típicos

- **Un contrato que sólo vive en una wiki.** Si no hay un test en integración continua que lo
  verifique, se incumple en el primer sprint con prisa. El contrato tiene que ser un fichero
  versionado y un trabajo automático que lo comprueba en cada despliegue del productor.
- **Validar sólo los tipos.** `estado` sigue siendo texto cuando pasa de tres valores a siete. El
  tipo no te salva; hay que validar dominio, rango, unidad y nulabilidad. El 80 % de las rupturas
  reales no tocan el tipo.
- **Añadir un campo obligatorio en una versión menor.** Los consumidores no lo rellenan y todo se
  rompe a la vez. Los campos nuevos se añaden opcionales, con un valor por defecto acordado, y se
  hacen obligatorios —si hace falta— en la siguiente versión mayor.
- **Confundir contrato con SLA.** El SLA dice **cuándo** llega el dato; el contrato dice **qué**
  llega. Son cosas distintas, se rompen por motivos distintos y las detecta gente distinta.
- **Versionar el esquema sin versionar el significado.** Cambiar `importe` de euros a céntimos sin
  cambiar el nombre y sin subir la versión es peor que renombrarlo: el consumidor no se entera de
  nada y los números se multiplican por cien en silencio.
- **Escribir el contrato a un solo lado.** Si sólo lo redacta el consumidor, el productor lo vive
  como una carga impuesta; si sólo lo redacta el productor, no cubre lo que de verdad se usa. Se
  negocia entre los dos, aunque «firmar» sea un fichero en Git con dos revisiones.

## Comprueba que lo sabes

:::quiz
p: ¿Cuál de estos cambios en un conjunto de datos es incompatible con los consumidores actuales?
o: Añadir una columna nueva que admite nulos
o: Añadir un valor nuevo a un campo cuyo dominio estaba cerrado y documentado
o: Pasar una columna de obligatoria a admitir nulos
a: 2
e: Añadir una columna opcional no invalida ningún dato anterior. Relajar una restricción tampoco: lo que antes era válido sigue siéndolo. Añadir un valor a un dominio cerrado sí rompe, porque los consumidores filtraron por esos valores y sus reglas de negocio dejan de cubrir todos los casos.
:::

:::quiz
p: ¿Por qué se dice que un contrato de datos no es un documento sino un test?
o: Porque un documento no se puede leer en formato máquina
o: Porque sólo se cumple si algo automático bloquea el despliegue cuando se incumple
o: Porque los tests son más baratos de escribir que la documentación
a: 2
e: Un contrato sin verificación automática se queda obsoleto igual que un comentario. La parte que cambia el comportamiento es la comprobación en el pipeline del productor: si el lote no cumple, no se publica. El documento es la especificación; el test es lo que la hace real.
:::

:::nota
Un contrato no hace falta para todo. Una tabla interna que sólo lee el equipo que la escribe se
gobierna con tests normales. El contrato aparece cuando hay **otro equipo** al otro lado: ahí es
donde el aviso verbal deja de funcionar y donde el coste de una ruptura se multiplica.
:::
