---
id: control-de-acceso-por-fila-y-columna
titulo: Control de acceso por fila y por columna
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [gobierno-y-privacidad, sql-select-y-filtros]
tags: [seguridad, gobierno, permisos, sql]
resumen: Que el motor recorte filas y columnas según quién consulta, para que la autorización no dependa de que cada aplicación, cuadro o notebook se acuerde de filtrar.
fuentes: ["PostgreSQL Global Development Group, 'PostgreSQL Documentation: Row Security Policies'", "Reis & Housley (2022), 'Fundamentals of Data Engineering', cap. 10", "Snowflake Inc., 'Snowflake Documentation: Row Access Policies and Dynamic Data Masking'"]
---

## En una frase

Es dejar que el motor decida qué filas y qué columnas devuelve cada consulta según quién la
ejecuta, para que la autorización no dependa de que la aplicación se acuerde de filtrar.

## La idea

Una empresa tiene una sola tabla de ventas con las operaciones de cinco países. El equipo de
Francia no debe ver los clientes españoles, así que la aplicación añade `WHERE pais = 'FR'` a
todas sus consultas. Funciona durante tres años. Y luego falla por tres sitios a la vez: alguien
abre un cuaderno con las mismas credenciales y consulta la tabla directamente; un informe nuevo se
escribe sin el filtro porque quien lo hizo no sabía que existía; y una exportación a CSV que
recorre la tabla por lotes se salta el filtro porque el filtro lo ponía la capa web, no ella.

El error de fondo es de sitio, no de código: la comprobación estaba en el lugar donde se
**escribe** la consulta, y tenía que estar en el lugar por donde **sale** el dato. Con la política
en el motor, la consulta se reescribe antes de ejecutarse y da igual quién la escriba: una
herramienta de BI, un `SELECT *` desde un cliente SQL, una función de otro esquema o un proceso
nocturno. No hay consulta que rodear la política porque la política no es una capa que se pueda
saltar: es parte de lo que la tabla devuelve.

Hay tres formas de implementarlo, de menos a más útil:

1. **Permisos por tabla y por columna.** `GRANT SELECT (pais, importe) ON ventas TO rol`. Es
   barato, lo entiende todo el mundo y protege de verdad: la columna no concedida no se puede
   consultar. El problema es que es todo o nada por columna: o ves el importe de todos los
   países, o no ves el importe.
2. **Vistas.** Una vista con el filtro y los permisos sobre la vista, no sobre la tabla. Funciona
   mientras nadie necesite otra combinación (por país, por comercial, por año) y mientras la
   tabla de debajo esté cerrada: si el rol conserva el `SELECT` sobre la tabla base, la vista es
   decorativa.
3. **Políticas dinámicas.** Una política de fila (row access policy) y otra de columna (masking
   policy) que el motor evalúa en cada consulta con la identidad de la sesión. Es lo que permite
   tener una sola tabla, veinte combinaciones de acceso y ninguna vista duplicada.

La condición para que la tercera funcione es que **el motor sepa quién pregunta** y que esa
identidad no la elija quien pregunta. Los nombres reales cambian según el sistema: el usuario de
la conexión, el rol, un grupo, o una variable de sesión como `app.pais`. Si esa variable la fija
el cliente, la política es papel mojado: basta con enviar otro valor para ver otro país. La fija
la capa de confianza —el servicio que abre la conexión, el proxy de autenticación— y el usuario
solo hereda lo que le toca.

En el eje de las columnas hay tres estrategias que se confunden todo el rato y no son lo mismo:

- **Ocultar.** La columna no se concede y desaparece: el informe que la usaba se rompe con un
  error de columna inexistente. Es lo correcto para datos que nadie sin autorización debe ver,
  aunque rompa consultas.
- **Enmascarar.** La columna sigue ahí, con su tipo, pero el valor se sustituye (`***`, un rango,
  un hash). El informe sigue funcionando, la persona no ve el dato. Es lo correcto para correos,
  teléfonos, identificadores fiscales o importes.
- **Seudonimizar.** Se guarda un hash determinista del valor: permite agrupar y unir por ese
  campo sin conocerlo. Cuidado: si el dominio es pequeño —un código postal, una fecha de
  nacimiento— el hash se revierte probando todas las combinaciones posibles.

:::trampa
En PostgreSQL, el **dueño de la tabla** y los roles con el atributo `BYPASSRLS` se saltan las
políticas de fila. Es la peor clase de fallo: el desarrollador que creó la tabla prueba su propia
política, ve que funciona, y no funciona para nadie más. Si el dueño también debe estar sujeto a
la política, hay que activarla con `ALTER TABLE ... FORCE ROW LEVEL SECURITY`, y comprobar la
política con el rol real, no con la cuenta de administración.
:::

## Definición formal

Sea `R` una tabla, `u` el usuario (o rol) que consulta, `p(u)` el predicado de fila que le
corresponde y `C(u)` el conjunto de columnas que puede ver, cada una con su máscara. El motor no
evalúa la consulta sobre `R`, sino sobre la vista restringida:

:::formula
R(u) = π_{C(u)} ( σ_{p(u)} ( R ) )
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube / cambia… |
| --- | --- | --- | --- |
| `R` | La tabla completa, con todas las filas y columnas | filas por columnas | Cuantas más filas y columnas tenga, más superficie hay que cubrir con políticas y más caro es equivocarse |
| `u` | La identidad con la que se ejecuta la consulta: usuario, rol o grupo | no aplica | Si la identidad la puede elegir el cliente, la política deja de proteger: el atacante elige el valor que más le conviene |
| `p(u)` | El predicado de fila del usuario: la condición que deben cumplir las filas que ve | una condición booleana | Cuanto más restrictivo, menos filas ve; si es `TRUE` para todos, la política de fila no hace nada |
| `σ_{p(u)}` | La selección: se queda solo con las filas que cumplen el predicado | conjunto de filas | — |
| `C(u)` | Las columnas que el usuario puede ver, con la máscara de cada una | lista de columnas | Cuantas más columnas entren, más campos sensibles quedan expuestos y más combinaciones hay que probar |
| `π_{C(u)}` | La proyección: de cada fila se queda solo con esas columnas, ya enmascaradas | conjunto de columnas | — |
| `m(c, u)` | La máscara aplicada al valor de la columna `c` para el usuario `u` | el tipo de la columna | Si la máscara depende del propio valor, revela la condición que la activa |
:::

La propiedad que distingue esto de un filtro en la aplicación es que se aplica a **toda** consulta,
la escriba quien la escriba:

:::formula
para toda consulta Q:  el motor evalúa Q sobre R(u),  nunca sobre R
:::

Es decir: `SELECT` con o sin `WHERE`, con `JOIN`, con subconsultas, con funciones de ventana o
desde una herramienta de BI, siempre parte de las mismas filas y las mismas columnas. La única
forma de ver más es cambiar de identidad, y la identidad no la decide la consulta.

## Ejemplo

La tabla `ventas` que aparece en la figura, con cinco filas y cuatro columnas, y dos roles:

| fila | pais | comercial | importe | cliente |
| --- | --- | --- | --- | --- |
| 1 | ES | ana | 1000 | ACME |
| 2 | ES | luis | 250 | PEREZ SL |
| 3 | FR | ana | 4000 | ACME |
| 4 | DE | luis | 150 | GARCIA |
| 5 | ES | ana | 3200 | ACME |

Ana tiene la política de fila `pais = 'ES'` y las columnas `pais`, `comercial` e `importe`. Luis
tiene la política `comercial = 'luis'` y las columnas `pais`, `importe` y `cliente`. Lo que
devuelve el motor:

- Ana ve las filas 1, 2 y 5, con tres columnas. Su total de importe es 4.450.
- Luis ve las filas 2 y 4, con tres columnas. Su total es 400.
- Nadie ve la fila 3: Ana porque es de Francia, Luis porque la comercial es Ana. Y ninguno de los
  dos ve la columna `cliente` de las filas del otro.

Los dos trabajan sobre la misma tabla y obtienen respuestas distintas sin que ninguna consulta
lleve un filtro escrito a mano. Eso es lo que se busca.

Ahora el fallo que se cuela cuando el filtro vive en la aplicación. El código pide las tres
primeras filas y después descarta las que no son de España:

```
traigo filas 1, 2 y 3  ->  descarto la 3 (es de Francia)  ->  me quedo con 2 filas
```

El usuario pidió tres resultados y ve dos, y no porque falten datos: es que una fila ajena ocupó
sitio en el `LIMIT`. El orden de las operaciones cambia el resultado, y ese error no aparece
nunca en las pruebas con datos de un solo país. Con la política en el motor, el `LIMIT` se aplica
después del recorte de filas y las tres filas que llegan son de las que el usuario puede ver.

Y el detalle fino de las máscaras. Enmascarar con una condición sobre el propio valor parece
razonable y filtra el dato:

```
cliente   importe
ACME      ***
PEREZ SL  300
GARCIA    800
LUNA      ***
celdas tapadas: 2
```

Quien ve esa tabla sabe que las dos filas tapadas superan el umbral de 1.000 y las otras dos no.
Con repetir la consulta cambiando el filtro se acota el valor exacto por bisección: «los importes
mayores que 2.000 salen tapados, los menores que 1.500 no» deja el valor en un intervalo estrecho.
Una máscara que depende del dato es una máscara que publica el dato por la puerta de atrás.

:::figura
fichero: acceso-fila-y-columna
pie: A la izquierda, la única tabla que existe en el disco: ni una marca indica quién puede ver qué. A la derecha, la misma tabla celda a celda con las dos políticas aplicadas a la vez: azul donde la ven los dos roles, naranja lo que solo ve Ana, morado lo que solo ve Luis y gris lo que no ve nadie. La fila 3 desaparece para ambos, y cada rol pierde además una columna distinta, así que el recorte no es solo de filas.
fuente: figuras/control-de-acceso-por-fila-y-columna-1.py
:::

## Código

```python verificable
import pandas as pd

# Una sola tabla fisica y una politica por rol: que filas y que columnas ve cada uno.
ventas = pd.DataFrame({
    "pais": ["ES", "ES", "FR", "DE", "ES"],
    "comercial": ["ana", "luis", "ana", "luis", "ana"],
    "importe": [1000, 250, 4000, 150, 3200],
    "cliente": ["ACME", "PEREZ SL", "ACME", "GARCIA", "ACME"],
})

politicas = {
    "ana": {"filas": lambda d: d["pais"] == "ES",
            "columnas": ["pais", "comercial", "importe"]},
    "luis": {"filas": lambda d: d["comercial"] == "luis",
             "columnas": ["pais", "importe", "cliente"]},
}

def vista(df, usuario):
    p = politicas[usuario]
    return df[p["filas"](df)][p["columnas"]]

for usuario in politicas:
    v = vista(ventas, usuario)
    print(usuario, "ve", len(v), "filas y", len(v.columns), "columnas:", ", ".join(v.columns))
# -> ana ve 3 filas y 3 columnas: pais, comercial, importe
# -> luis ve 2 filas y 3 columnas: pais, importe, cliente

# La trampa: filtrar en la aplicacion DESPUES de limitar deja entrar filas de otro pais.
recortado = ventas.head(3)
print("filas de otro pais que se cuelan:", int((recortado["pais"] != "ES").sum()))
# -> 1
```

```sql ilustrativo
-- PostgreSQL: la politica la evalua el motor en cada consulta, no la aplicacion.
ALTER TABLE ventas ENABLE ROW LEVEL SECURITY;          -- por defecto, sin politicas, nadie ve nada
ALTER TABLE ventas FORCE ROW LEVEL SECURITY;           -- el dueño tampoco se libra

CREATE POLICY ventas_por_pais ON ventas
    FOR SELECT TO rol_comercial
    USING (pais = current_setting('app.pais'));        -- la fija la capa de confianza, no el cliente

-- Escritura: USING decide que filas se pueden modificar y WITH CHECK que filas pueden quedar.
CREATE POLICY ventas_solo_propias ON ventas
    FOR UPDATE TO rol_comercial
    USING (comercial = current_user)
    WITH CHECK (comercial = current_user);

-- Columna: se concede lo que se necesita y no la tabla entera.
REVOKE SELECT ON ventas FROM rol_comercial;
GRANT SELECT (pais, comercial, importe) ON ventas TO rol_comercial;

-- Sin mascaras dinamicas, en PostgreSQL el mismo efecto se consigue con una vista:
CREATE VIEW ventas_publicas AS
    SELECT pais, comercial, importe,
           CASE WHEN current_user = 'rol_privacidad' THEN cliente ELSE '***' END AS cliente
    FROM ventas;

-- Snowflake y BigQuery si tienen mascara dinamica: la politica se asocia a la columna y el
-- motor la aplica en cualquier consulta, incluso en un SELECT *.
CREATE MASKING POLICY correo_opaco AS (val STRING) RETURNS STRING ->
    CASE WHEN current_role() IN ('rol_privacidad') THEN val ELSE '***' END;
```

```python verificable
import pandas as pd

# Mascara condicional: solo se tapa lo que supera el umbral.
ventas = pd.DataFrame({
    "cliente": ["ACME", "PEREZ SL", "GARCIA", "LUNA"],
    "importe": [4200, 300, 800, 1500],
})
vista = ventas.assign(importe=ventas["importe"].where(ventas["importe"] <= 1000, "***"))
print("importes que ve el visitante:", list(vista["importe"]))
# -> ['***', 300, 800, '***']
print("celdas tapadas:", int((vista["importe"] == "***").sum()))
# -> 2

# El numero de celdas tapadas publica el umbral de la politica, y repitiendo la consulta
# con otros filtros se acota el valor exacto por biseccion. La mascara no puede depender
# del valor que esconde.
```

## Errores típicos

- **Filtrar en la aplicación y llamarlo control de acceso.** Todo lo que no pase por esa capa
  —un cuaderno, una herramienta de BI, una exportación por lotes, un proceso de otro equipo— ve
  la tabla entera. La comprobación tiene que estar en el motor, y la aplicación no debería ni
  tener permiso para leer la tabla sin recortar.
- **Filtrar después de limitar.** `SELECT ... LIMIT 3` y luego descartar en Python devuelve menos
  filas de las pedidas y mezcla datos de otro ámbito en el recuento. Si el filtro es una política
  del motor, el orden lo decide el motor y el problema desaparece; si no lo es, filtra **en la
  consulta**, nunca después.
- **Probar la política con la cuenta de administración.** En PostgreSQL el dueño de la tabla y los
  roles con `BYPASSRLS` se saltan las políticas de fila: la prueba pasa y la política no existe
  para el resto. Activa `FORCE ROW LEVEL SECURITY` y prueba con un rol normal, uno por cada
  combinación de acceso.
- **Dejar que el cliente fije la identidad de la política.** Si el país de la política se lee de
  una variable de sesión que envía la aplicación —o peor, el usuario—, basta con cambiarla para
  ver otro país. Esa variable la fija la capa autenticada, y la conexión del usuario no tiene
  permiso para escribirla.
- **Enmascarar la columna y olvidar los agregados.** `COUNT(DISTINCT cliente)`, `MIN`, `MAX` o una
  media sobre pocas filas reconstruyen el valor tapado. Si el informe agrupa, hace falta un tamaño
  mínimo de grupo; y si la máscara depende del propio valor, el número de celdas tapadas ya cuenta
  lo que se quería esconder.
- **Ocultar una columna dejando visible la clave.** Quitar `cliente` de la vista no sirve de nada
  si `cliente_id` sigue ahí y la tabla de clientes es legible para el mismo rol: una unión
  recupera el nombre. Proteger una columna obliga a proteger todo lo que la identifica.

:::aviso
Una política de fila añade un predicado a **todas** las consultas que tocan esa tabla. Si la
columna de la política no está indexada o no coincide con la partición por la que se filtra
siempre, un informe que leía treinta días puede acabar leyendo todo el histórico. Mide el plan
antes y después de activar la política, y no solo si el resultado es correcto.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué diferencia hay entre poner el filtro por país en la aplicación y ponerlo como política de fila en el motor?
o: Ninguna práctica: los dos devuelven las mismas filas al usuario final
o: La política la aplica el motor en toda consulta, así que también cubre cuadernos, herramientas de BI y procesos que no pasan por la aplicación
o: La política es más rápida porque el filtro se aplica en paralelo
a: 2
e: El filtro de la aplicación solo actúa donde ese código se ejecuta: cualquier otra vía de acceso a la tabla con las mismas credenciales ve todo. La política de fila se aplica dentro del motor, a toda consulta, la escriba quien la escriba. El rendimiento no es la diferencia: de hecho la política también puede encarecer las consultas si la columna no está indexada.
:::

:::quiz
p: Un rol ve la columna importe enmascarada como *** solo cuando el valor supera 1.000. ¿Qué problema tiene esa máscara?
o: Ninguno: el valor real nunca se muestra
o: Que la propia máscara revela la condición: saber qué filas están tapadas acota el valor, y con varias consultas se puede reconstruir
o: Que las filas con importe menor de 1.000 se ven mal en los informes
a: 2
e: Una máscara que depende del valor esconde el número y publica la condición. El número de celdas tapadas ya da información, y repitiendo la consulta con umbrales distintos se acota el valor real por bisección. Lo correcto es enmascarar siempre, o sustituir por un rango fijo que no se pueda cruzar con otras consultas.
:::

:::quiz
p: El desarrollador que creó la tabla prueba su política de fila y ve todas las filas. ¿Qué está pasando?
o: La política no se ha creado bien y hay que volver a crearla
o: El dueño de la tabla no está sujeto a las políticas de fila salvo que se active FORCE ROW LEVEL SECURITY
o: Las políticas de fila solo se aplican a los usuarios que no son superusuarios ni dueños, y eso no se puede cambiar
a: 2
e: En PostgreSQL, las políticas de fila no se aplican al dueño de la tabla ni a los roles con BYPASSRLS. Por eso la prueba con la cuenta que creó la tabla da un falso aprobado. FORCE ROW LEVEL SECURITY obliga a que el dueño también las cumpla; los superusuarios y BYPASSRLS siguen exentos, así que la prueba debe hacerse con el rol real.
:::
