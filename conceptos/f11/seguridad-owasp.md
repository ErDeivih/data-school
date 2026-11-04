---
id: seguridad-owasp
titulo: Seguridad de aplicaciones
fase: 11
nivel: avanzado
rutas: [alg, de]
prerequisitos: [autenticacion-y-autorizacion, apis-rest, secretos-y-configuracion]
tags: [seguridad, owasp, inyeccion, dependencias]
resumen: Las diez trampas que se repiten en cada aplicación: inyección, XSS, CSRF, control de acceso roto y dependencias abandonadas, con lo que hay que revisar siempre.
fuentes: ["OWASP Foundation, 'OWASP Top 10' (documentacion oficial)", "OWASP Foundation, 'Application Security Verification Standard'"]
---

## En una frase

La mayoría de las brechas no vienen de un ataque sofisticado, sino de tres o cuatro errores
de siempre: mezclar datos del usuario con código, confiar en que el cliente hará lo correcto,
y no actualizar las dependencias.

## La idea

Piensa en una biblioteca con un mostrador. El bibliotecario tiene dos libros: uno con las
reglas («qué se puede pedir») y otro con las peticiones de los usuarios. Mientras los datos
del usuario se escriban **solo en el libro de peticiones**, todo va bien. El desastre ocurre
cuando el texto del usuario acaba escrito en el libro de reglas: entonces el usuario ya no
pide, ordena. Eso es una inyección, en cualquiera de sus formas —SQL, comandos del sistema,
plantillas— y es la misma idea con distinto libro.

La segunda idea, igual de importante: **el cliente es territorio enemigo**. Cualquiera puede
abrir las herramientas del navegador, cambiar un campo oculto, llamar a tu API sin pasar por
tu interfaz y repetir peticiones mil veces por segundo. Todo lo que tu aplicación decida
mirando solo el navegador (precios, descuentos, permisos, estados) es una decisión que el
atacante controla. La regla práctica: **valida y autoriza en el servidor, siempre, aunque el
cliente ya lo haya hecho**.

La tercera: casi todo el código que ejecutas no lo has escrito tú. Una aplicación mediana
arrastra cientos de dependencias transitivas, y una vulnerabilidad en cualquiera de ellas es
una vulnerabilidad tuya. No es algo que se arregle una vez, es una rutina.

Estas tres ideas cubren la mayor parte del catálogo de OWASP, que se organiza alrededor de
categorías estables desde hace años:

- **Control de acceso roto.** El número uno. No es que el usuario no esté autenticado, es que
  está autenticado y accede a lo que no es suyo, porque la comprobación se hace en el cliente
  o falta directamente en un endpoint. Cambiar `/facturas/1041` por `/facturas/1042` se llama
  **referencia directa insegura a objetos** y no requiere ninguna herramienta. En esta misma
  categoría entra la **falsificación de petición en sitios cruzados** (CSRF): el navegador
  adjunta la cookie de sesión por su cuenta, así que una página ajena puede provocar una
  petición que cambia estado en tu aplicación sin que el usuario se entere. Se corta con cookies
  `SameSite`, un token por formulario y no aceptando cambios de estado por `GET`.
- **Fallas criptográficas.** Guardar contraseñas con SHA-256 a secas, usar HTTP en
  producción, cifrar con una clave que está en el repositorio.
- **Inyección.** SQL, NoSQL, comandos, LDAP, plantillas. La defensa es la misma en todos:
  separar el dato de la estructura y usar la API parametrizada del motor.
- **Diseño inseguro.** El flujo en sí es explotable: un restablecimiento de contraseña que no
  caduca, un cupón reutilizable, un carrito que acepta precios negativos.
- **Configuración incorrecta.** Modo depuración activo en producción (que muestra trazas con
  consultas y variables), almacenamiento en la nube abierto al mundo, credenciales por
  defecto sin cambiar.
- **Componentes vulnerables y obsoletos.** Dependencias sin actualizar y sin mirar.
- **Fallos de identificación y autenticación.** Fuerza bruta sin límite de intentos, sesiones
  que no se invalidan al cerrar sesión, tokens sin caducidad. Los detalles finos están en
  [[autenticacion-y-autorizacion]].
- **Fallos de integridad de software y datos.** Deserializar datos del usuario con formatos
  que ejecutan código, o actualizar dependencias sin verificar su origen.
- **Fallos de registro y monitorización.** Un ataque que dura semanas porque nadie mira las
  alertas. No es glamuroso, pero es el que decide cuánto dura una brecha.
- **Falsificación de peticiones del lado del servidor (SSRF).** Tu servidor hace una petición
  a una URL que eligió el usuario, y el usuario pone `http://169.254.169.254/` para leer las
  credenciales de la máquina. Todo endpoint que reciba una URL debe validar el destino contra
  una lista blanca, no solo comprobar que «empieza por http».

:::aviso
Ninguna herramienta automática sustituye a pensar. Un escáner encuentra inyecciones obvias y
dependencias conocidas; no encuentra un control de acceso que falta ni un flujo de negocio
manipulable. Y al revés: casi ningún escáner entiende tu lógica de negocio, así que un informe
limpio no es una garantía.
:::

## Definición formal

No hay una fórmula única, pero sí dos comprobaciones que conviene escribir como invariantes y
revisar en cada *pull request*:

1. **Invariante de separación dato/estructura.** Para toda entrada del usuario `x` y toda
   consulta o comando `q`, la ejecución debe cumplir `parse(q(x)) = parse(q)` con `x`
   tratado como valor. Es decir: **el texto de `x` nunca cambia la estructura de `q`**. Se
   garantiza usando parámetros (`?`, `:nombre`, `%s` del conector) o una API que no construya
   texto, nunca concatenando.
2. **Invariante de autorización en el servidor.** Para todo recurso `r` propiedad de un sujeto
   `s`, toda petición debe satisfacer `peticion.sujeto = s` **o** `peticion.sujeto` tiene un
   rol explícito sobre `r`. La comprobación ocurre en el servidor, en el endpoint que lee o
   escribe `r`, no en la interfaz.

Símbolos: `x` es el valor aportado por el usuario; `q` es la consulta o el comando con su
estructura fija; `parse` es la función que el motor aplica para interpretar `q`; `r` es un
recurso con propietario; `s` es el sujeto autenticado de la petición.

:::truco
Tres comprobaciones que pillan la mayoría de los fallos en una revisión de código, en menos de
un minuto: busca `f"SELECT` o `+ "SELECT` (concatenación en SQL), busca `shell=True` y
`eval(`, y busca endpoints que reciben un `id` y no comparan el propietario con el usuario de
la sesión. El 80 % de los hallazgos graves están en esas tres líneas.
:::

## Ejemplo

Una tabla de usuarios y una búsqueda por correo. El valor que llega de fuera es:

```
x = x' OR '1'='1
```

- **Consultando con concatenación:**
  `SELECT email, rol FROM usuarios WHERE email = 'x' OR '1'='1'`.
  El motor interpreta `OR '1'='1'` como estructura, la condición es siempre verdadera y
  devuelve **todas** las filas de la tabla.
- **Consultando con parámetro:**
  `SELECT email, rol FROM usuarios WHERE email = ?`, con el parámetro `x' OR '1'='1`.
  El motor busca un correo que, literalmente, se llama así. Devuelve **0 filas**.

El mismo texto, el mismo usuario, el mismo motor y dos resultados opuestos. La diferencia no
está en la entrada: está en si la consulta se construyó como texto o se envió como estructura
más parámetros.

:::figura
fichero: seguridad-owasp-filas-devuelta
pie: La misma entrada hostil (`x' OR '1'='1`) contra el mismo motor, según cómo se construya la consulta. Concatenando el texto, la condición queda siempre verdadera y la respuesta trae TODAS las filas de la tabla: la línea roja crece con el número de usuarios. Enviando el valor como parámetro, ese texto no coincide con ningún correo (línea verde, cero filas) y solo devuelve una fila si el correo existe de verdad (línea azul). Fíjate en el extremo izquierdo: con un único usuario las tres formas coinciden en una fila, y por eso este fallo no se ve en un ejemplo pequeño.
fuente: figuras/seguridad-owasp-1.py
:::

## Código

```python verificable
import sqlite3

con = sqlite3.connect(":memory:")        # base en RAM: no crea fichero y se pierde al terminar
con.execute("CREATE TABLE usuarios (email TEXT, rol TEXT)")
con.execute("INSERT INTO usuarios VALUES ('ana@ejemplo.es', 'admin')")

# MAL: la consulta se construye pegando el texto que llega del usuario.
email = "x' OR '1'='1"                   # la comilla suelta cierra el literal de la consulta
mala = f"SELECT email, rol FROM usuarios WHERE email = '{email}'"   # el dato acaba dentro del SQL
print("concatenando:", len(con.execute(mala).fetchall()), "filas (esperabamos 0)")

# BIEN: el valor viaja como parametro y el motor lo trata como dato, no como SQL.
buena = "SELECT email, rol FROM usuarios WHERE email = ?"
print("con parametro:", len(con.execute(buena, (email,)).fetchall()), "filas")
print("usuario real  :", con.execute(buena, ("ana@ejemplo.es",)).fetchall())   # la coma hace la tupla
```

:::claves
- `con.execute(...)` no devuelve filas: devuelve un `Cursor`, y las filas salen al llamar a `.fetchall()`, que las trae como lista de tuplas (una por fila, en el orden del `SELECT`).
- `sqlite3.connect(":memory:")` abre la base en memoria RAM, no un fichero: todo desaparece al terminar el programa y por eso el ejemplo no hace `commit`.
- El segundo argumento de `execute` son los valores de los huecos `?`, en orden. Con un solo valor hay que escribir `(email,)`: sin la coma, `(email)` es el propio texto, SQLite intenta repartirlo letra a letra y falla con `ProgrammingError: Incorrect number of bindings supplied`.
- La consulta con `?` se puede repetir con valores distintos, `(email,)` y `("ana@ejemplo.es",)`: el texto de fuera nunca llega a formar parte de la estructura de la consulta.
- Un `f-string` no limpia ni escapa nada. La comilla que trae el usuario cierra el literal y lo que viene detrás lo lee el motor como SQL, así que `mala` no devuelve cero filas.
- La tabla del ejemplo tiene **una sola fila**, y por eso la consulta mala imprime 1 en lugar de un número llamativo. Con cien usuarios imprimiría 100: el fallo se mide en proporción, no en el número.
:::

```python verificable
import html

comentario = "<script>fetch('/robar?c='+document.cookie)</script>"   # si se pinta tal cual, roba la sesion
plantilla = "<p>{}</p>"

# MAL: el texto se inyecta tal cual y el navegador lo ejecuta como codigo.
print("sin escapar:", plantilla.format(comentario)[:34], "...")

# BIEN: se escapan los caracteres con significado en HTML antes de pintarlos.
print("escapado   :", plantilla.format(html.escape(comentario))[:34], "...")   # < pasa a ser &lt;
```

```sql ilustrativo
-- Nunca se construye asi en el cliente: el motor recibe estructura y parametros.
-- El valor no aparece dentro del texto de la consulta.
SELECT email, rol FROM usuarios WHERE email = ?;

-- Lo que hay que buscar en una revision: concatenacion de texto con entradas.
-- NO USAR: "SELECT email FROM usuarios WHERE email = '" + entrada + "'"
```

## Errores típicos

- **Escapar en lugar de parametrizar.** Sustituir comillas por comillas dobles en el texto de
  la consulta es una carrera perdida: siempre hay una codificación, un juego de caracteres o
  un caso raro que se te escapa. Parametriza y deja de escapar.
- **Creer que el *frontend* valida.** Un `required` en un campo del formulario o una
  comprobación en JavaScript son comodidad para el usuario, no seguridad. Cualquiera envía la
  petición sin pasar por tu formulario con `curl` en dos líneas.
- **Autorizar solo en la interfaz.** Ocultar el botón «borrar» a quien no es administrador no
  protege el endpoint de borrado. La comprobación de permiso va en el servidor, en cada
  endpoint, y se revisa con la misma seriedad que la de autenticación.
- **Confiar en el identificador que manda el cliente.** Un `usuario_id` en el cuerpo de la
  petición, un `precio` en un campo oculto o un `es_admin: false` son datos del atacante. El
  servidor debe tomar el usuario de la sesión o del token, y el precio de su propia base de
  datos.
- **Deserializar entradas con formatos que ejecutan código.** `pickle`, `yaml.load` sin
  `SafeLoader` o un `eval` disfrazado de conversión de tipos permiten ejecución remota de
  código con una petición. Usa JSON, que solo describe datos.
- **Dejar el modo depuración activo en producción.** Las trazas de un marco en modo desarrollo
  muestran rutas, consultas y a veces variables de entorno y claves. Un error provocado a
  propósito se convierte en un mapa de tu aplicación.
- **No mirar las dependencias.** Una librería con una vulnerabilidad conocida y publicada es
  una puerta abierta documentada. Revisa el árbol de dependencias en cada integración continua
  y actualiza; el aviso llegará de todas formas, mejor que llegue antes.

:::trampa
Un secreto *commiteado* a Git hay que considerarlo comprometido para siempre, aunque lo borres
en el siguiente commit: queda en el historial, en las copias de los compañeros y en las cachés
de los servidores. La respuesta correcta es **rotar la credencial**, no reescribir el
historial. Lo mismo con los ficheros `.env` colados en una imagen de contenedor.
:::

## Comprueba que lo sabes

:::quiz
p: Una consulta se construye con el texto que llega del usuario, y ese texto es `x' OR '1'='1`. ¿Qué pasa y cómo se evita?
o: La consulta falla con error de sintaxis; se evita validando que el correo tenga arroba
o: La condición se vuelve siempre verdadera y devuelve todas las filas; se evita enviando el valor como parámetro
o: El motor detecta la inyección y la bloquea; no hay nada que hacer
a: 2
e: Al concatenar, la comilla cierra el literal y el `OR` pasa a formar parte de la estructura de la consulta, así que la condición es verdadera para todas las filas. La defensa es la consulta parametrizada, que envía estructura y valor por separado. Validar el formato del correo ayuda, pero no es la defensa: hay inyecciones que pasan cualquier validación de formato.
:::

:::quiz
p: El endpoint `GET /facturas/{id}` devuelve la factura sin comprobar de quién es. ¿Qué categoría de riesgo es y cómo se arregla?
o: Control de acceso roto: hay que comprobar en el servidor que la factura pertenece al usuario autenticado
o: Inyección: hay que parametrizar el identificador en la consulta
o: XSS: hay que escapar el contenido de la factura al pintarlo
a: 1
e: El problema no es cómo se construye la consulta, sino que falta la comprobación de propiedad: cambiar el número de factura da acceso a la de otro. Parametrizar evita inyección pero no cambia de quién es la factura, y escapar afecta a cómo se muestra el contenido, no a quién puede leerlo.
:::

:::quiz
p: ¿Por qué comprobar el rol del usuario solo con JavaScript antes de mostrar un botón de borrado no protege nada?
o: Porque JavaScript es lento y el usuario puede adelantarse
o: Porque el usuario puede llamar al endpoint directamente, sin pasar por la interfaz
o: Porque los navegadores no ejecutan JavaScript en producción
a: 2
e: La interfaz es una conveniencia, no un control. Si el endpoint no comprueba el permiso, una petición directa con `curl` hace exactamente lo mismo que el botón. Las otras dos opciones son falsas: el problema no es de rendimiento ni de que el JavaScript no se ejecute.
:::
