---
id: secretos-y-configuracion
titulo: Secretos y configuración
fase: 11
nivel: avanzado
rutas: [alg, de]
prerequisitos: [entorno-python, git-para-datos, autenticacion-y-autorizacion]
tags: [secretos, configuracion, seguridad, despliegue]
resumen: Que es un secreto, dónde se guarda, cómo se rota y por qué borrarlo en un commit posterior no lo borra de ninguna parte.
fuentes: ["Wiggins (2011), 'The Twelve-Factor App'", "OWASP, 'Secrets Management Cheat Sheet'"]
---

## En una frase

Un secreto es cualquier dato que permite actuar en tu nombre —una clave, un token, una
contraseña, un certificado— y su sitio no es el repositorio: es un gestor que lo entrega con
vida corta, con los permisos justos y dejando rastro de quién lo pidió.

## La idea

Hay que separar dos cosas que a menudo van juntas:

- **Configuración:** lo que cambia entre entornos y no es sensible. La dirección de la base de
  datos, el nivel de registro, el número de reintentos, el interruptor de una funcionalidad.
- **Secreto:** lo que, si se filtra, permite a otro hacer cosas en tu nombre. No solo
  contraseñas: también claves de API, tokens de acceso, claves privadas, cadenas de conexión
  (que llevan la contraseña dentro) y ficheros de credenciales de nube.

Los dos van fuera del código, pero solo el secreto necesita custodia, rotación y auditoría.

**Por qué nunca en Git.** Un repositorio no es un sitio con puerta: es un objeto que se clona
entero, con toda su historia, en cada máquina y en cada caché de integración. Un secreto
empujado una vez deja de ser privado en ese instante, aunque el repositorio sea privado: está
en los clones de tus compañeros, en el sistema de integración y, si algún día el repositorio se
abre o se filtra, en Internet. Y borrarlo en un commit posterior **no lo borra**: el commit que
lo elimina lleva el valor dentro del diff, así que `git log -p` lo sigue mostrando para
siempre. Esto tiene una consecuencia que ordena todas las prioridades: **lo primero es rotar,
no limpiar**. Rotar invalida el dato en segundos; limpiar la historia lleva horas y no garantiza
nada.

**Variables de entorno: buenas, no perfectas.** La receta clásica es sacar la configuración del
código y ponerla en variables de entorno. Funciona muy bien con contenedores
([[contenedores]]) y evita el clásico «este fichero de configuración es distinto en cada
máquina». Pero conviene saber sus límites: las variables de entorno se heredan a los procesos
hijos, son visibles para quien pueda leer el proceso en la misma máquina, acaban en volcados de
memoria y es facilísimo volcarlas sin querer con un `print(os.environ)` o un registro de
depuración. Tampoco se pueden rotar sin reiniciar el proceso.

**El nivel que de verdad resuelve el problema** es el gestor de secretos: un servicio que
guarda los datos cifrados, decide quién puede leerlos según su identidad y los entrega en el
momento de arrancar o de usarlos. Encima de eso está la práctica que reduce el daño de un robo
a casi nada: **credenciales de vida corta**. En vez de una clave estática que dura años, el
proceso se identifica ante la plataforma (por ejemplo con un token de identidad del propio
sistema de integración) y recibe credenciales que caducan en minutos u horas. Si se filtran, ya
están caducadas.

**Permisos, no confianza.** Un secreto no debería dar acceso a todo. La clave que usa el
informe nocturno necesita leer una tabla; no necesita borrar el bucket. Y cada entorno y cada
servicio debería tener su propia credencial: si todos comparten una, no puedes rotarla sin
parar el sistema, no sabes quién hizo qué en el registro de auditoría y el radio de daño de un
robo es «todo».

**Detectar antes de que salga.** El olfato humano falla siempre en el mismo sitio: se prueba
con `git commit -am` y se cuela el `.env`. La defensa es automática: un analizador que busque
patrones de credenciales y cadenas de alta entropía antes de aceptar el empujón, y que falle el
pipeline cuando aparezca uno.

## Definición formal

**Secreto y configuración.**

- **Configuración** `c(e)` — valor que depende del entorno `e` y cuya revelación no da acceso a
  nada. No es sensible.
- **Secreto** `s` — valor cuya revelación permite ejecutar al menos una acción no autorizada.
- **Radio de daño** de `s` — conjunto de acciones que un atacante puede ejecutar con `s`. El
  objetivo del diseño es que ese conjunto sea lo más pequeño posible.

**Fuerza de un secreto generado al azar.** Si el secreto tiene `L` caracteres elegidos de forma
uniforme en un alfabeto de `A` símbolos, la entropía en bits es:

:::formula
H = L · log₂(A)
:::

- `L` — longitud en caracteres.
- `A` — tamaño del alfabeto (26 en minúsculas, 62 con mayúsculas y dígitos).
- `H` — bits de entropía. El número de combinaciones es `2^H`.

**Tiempo de agotamiento.** Con `r` intentos por segundo, el tiempo medio para agotar el espacio
de búsqueda es:

:::formula
t ≈ 2^H / (2 · r)
:::

Esto vale para contraseñas generadas al azar. Las contraseñas humanas no se atacan así, se
atacan con diccionarios: por eso se guardan con una función lenta (`bcrypt`, `argon2`) que
rebaja `r` a decenas de intentos por segundo incluso con hardware dedicado.

**Ciclo de vida.** Todo secreto recorre: emitido → distribuido → usado → rotado → revocado.
Para rotar sin cortar el servicio hace falta una **ventana de solape**: durante un tiempo `W`
se aceptan la credencial vieja y la nueva. La exposición total de una credencial que se rota
cada `T` con solape `W` está acotada por `T + W`.

**Regla de mínima exposición.** Un proceso debe ver solo los secretos que usa:

:::formula
secretos_visibles(proceso) = secretos_que_usa(proceso)
:::

Ni uno más. Cada secreto de más es una copia de más que puede acabar en un registro, en un
volcado o en un portátil.

**Redacción.** Antes de escribir una línea de registro:

:::formula
línea_registrada = redactar(línea, claves_sensibles)
:::

La redacción por nombre de campo es necesaria y **no suficiente**: solo protege lo que se
anuncia como sensible.

## Ejemplo

**Fuerza real.** Una contraseña de 8 letras minúsculas tiene 8 · log₂(26) = 37,6 bits, unas 208
mil millones de combinaciones: a mil millones de intentos por segundo se agota en 209 segundos.
Un token de 32 caracteres alfanuméricos tiene 190,5 bits y no se agota con nada que exista.
La diferencia entre esas dos cifras no es de grado, es de naturaleza.

:::figura
fichero: secretos-longitud-y-alfabeto
pie: Izquierda, el tiempo de agotar el espacio de búsqueda con mil millones de intentos por segundo. El eje va en log₂ de segundos, así que una línea recta aquí es un crecimiento exponencial: cada carácter multiplica el trabajo por 26 o por 62. Las 8 letras minúsculas de la página se agotan en 209 s; con 16 caracteres cualquier ataque directo es irrelevante. La línea morada marca los mil años. Derecha, lo que aporta cada carácter: alargar cuatro posiciones añade 18,8 bits, mientras que cambiar de 26 a 62 símbolos solo añade 1,25. Conclusión práctica: la longitud rinde mucho más que complicar el alfabeto.
fuente: figuras/secretos-y-configuracion-1.py
:::

**Radio de daño.** Un equipo guarda en un `.env` una única clave de nube con permiso de
administración sobre toda la cuenta, y la usan los cinco servicios. Cuando se filtra (por
ejemplo, en el registro de una tarea que imprimía la configuración), hay que ir a la consola,
crear credenciales nuevas, cambiarlas en cinco sitios a la vez y confiar en que ninguno se
quedó atrás. La alternativa: cinco credenciales, cada una con permiso sobre su prefijo de
almacenamiento. Filtrar una afecta a un servicio y se rota reiniciando ese servicio.

**Detección.** El escaneo de secretos encuentra dos commits: el que introdujo la clave y el que
la quitó, porque el segundo lleva el valor en el diff de la eliminación. Conclusión práctica:
el escaneo hay que hacerlo en el momento del empujón, no cuando alguien se acuerda de mirar el
historial.

## Código

```python verificable
import math

def bits(longitud, alfabeto):
    """Entropia de un secreto generado al azar: H = L * log2(A)."""
    return longitud * math.log2(alfabeto)      # log2: en bits, no en neperios ni en base 10

MINUSCULAS, ALFANUMERICO = 26, 62              # el alfabeto decide: 26 letras o 62 simbolos
for n in (8, 16, 32, 64):
    # :>3 alinea a la derecha en 3 caracteres, para que la tabla salga recta
    print(f"{n:>3} caracteres  minusculas {bits(n, MINUSCULAS):6.1f} bits"
          f"   alfanumerico {bits(n, ALFANUMERICO):6.1f} bits")

print(f"un token de 32 caracteres alfanumericos: {bits(32, ALFANUMERICO):.1f} bits")   # -> 190.5 bits

espacio = MINUSCULAS ** 8                      # 2^H combinaciones posibles
print("combinaciones de 8 minusculas:", espacio)                                    # -> 208827064576
# El tiempo medio es la mitad del espacio entre los intentos por segundo (2^H / (2 r)).
print(f"a mil millones de intentos por segundo: {espacio / 1e9:.0f} s")             # -> 209 s
```

:::claves
- `math.log2` devuelve **bits**, no dígitos: 8 letras minúsculas son 37,6 bits, y esa cifra ya
  no se lee como una contraseña sino como un tamaño de espacio de búsqueda. La diferencia entre
  26 y 62 símbolos son 1,25 bits por carácter, que suenan a poco y multiplican el espacio por
  2,4 en cada posición.
- **Cada carácter de más multiplica, no suma.** Pasar de 8 a 16 letras no duplica el trabajo del
  atacante: lo eleva a la octava potencia. Por eso alargar es la medida que más rinde, mucho más
  que cambiar una `a` por un `@`, que solo cambia el alfabeto de esa posición.
- El último `print` da **el tiempo de recorrer todo el espacio**, no la media. La media es la
  mitad (`2^H / (2 · r)`), que es la fórmula de la página; aquí se imprime el total, así que la
  cifra de 209 s es el doble de la media. Da igual para la conclusión: dos minutos o uno.
- `espacio = MINUSCULAS ** 8` se calcula con enteros de precisión arbitraria: Python no desborda
  con 208.827.064.576. En un lenguaje con enteros de 64 bits, `26 ** 20` ya no cabría y el
  cálculo daría la vuelta sin avisar.
- En el bloque de redacción, `SENSIBLES` busca por **nombre de campo**, no por contenido. `re.I`
  cubre mayúsculas y el grupo `api[_-]?key` cubre `api_key`, `api-key` y `apikey`, pero un campo
  llamado `clave`, `iban` o `tarjeta` no coincide con nada y sale entero en el registro.
- La comprensión `{k: ... for k, v in registro.items()}` construye un **diccionario nuevo**: el
  original `registro` conserva los valores sensibles intactos. Si lo que quieres es no tenerlos
  en memoria, la redacción no sirve de nada; hay que no guardarlos.
- `json.dumps(..., sort_keys=True)` ordena las claves alfabéticamente y `ensure_ascii=False`
  deja los acentos tal cual. Ese `sort_keys` es lo que hace que la misma entrada produzca
  siempre la misma línea, que es la única forma de comparar registros entre ejecuciones.
- El patrón del tercer bloque encuentra **los dos commits**, el que añadió el secreto y el que lo
  borró, porque el valor viaja en el diff en ambos casos. De ahí la conclusión práctica: limpiar
  la historia no basta, y por eso lo primero es rotar.
:::

```python verificable
import json
import re

# Lista negra por NOMBRE de campo: lo que no se anuncia como sensible, no se protege.
SENSIBLES = re.compile(r"(password|passwd|secret|token|api[_-]?key|authorization)", re.I)
# re.I hace la busqueda insensible a mayusculas: "Password" y "PASSWORD" tambien entran.

registro = {
    "usuario": "ana",
    "password": "hunter2-que-no-se-ve",
    "tarjeta": "4111111111111111",
    "token_acceso": "eyJhbGciOiJIUzI1NiJ9",
}

# Comprension sobre los .items(): conserva las claves y sustituye solo el valor sensible.
limpio = {k: ("***" if SENSIBLES.search(k) else v) for k, v in registro.items()}
# sort_keys hace la linea reproducible: el mismo diccionario imprime siempre en el mismo orden.
linea = json.dumps(limpio, ensure_ascii=False, sort_keys=True)

print(linea)
print("la contrasena aparece en la linea:", "hunter2-que-no-se-ve" in linea)   # -> False
print("el token aparece en la linea:", "eyJhbGciOiJIUzI1NiJ9" in linea)        # -> False
# La tarjeta no lleva palabra clave en el nombre, asi que pasa el filtro entera.
print("la tarjeta aparece en la linea:", "4111111111111111" in linea)          # -> True
```

```python verificable
import re

# Contenido de dos commits: el que introduce el secreto y el que lo elimina.
historial = [
    ("a1b2c3", '+API_KEY = "sk-fake-NO-ES-UN-SECRETO-REAL"'),
    ("d4e5f6", '-API_KEY = "sk-fake-NO-ES-UN-SECRETO-REAL"'),
]
patron = re.compile(r"sk-fake-[A-Za-z0-9-]+")

# El patron busca en la LINEA entera, y el prefijo + o - del diff no estorba: da igual si el
# secreto se anadio o se quito, en los dos casos el valor esta escrito ahi.
afectados = [sha for sha, linea in historial if patron.search(linea)]
print("commits cuyo diff contiene el secreto:", len(afectados), afectados)   # -> 2 ['a1b2c3', 'd4e5f6']
# all() sobre un generador: False en cuanto encuentra una linea con el patron.
print("el historial esta limpio:", all(not patron.search(l) for _, l in historial))   # -> False
```

## Errores típicos

- **Añadir el fichero al `.gitignore` después de haberlo empujado.** `gitignore` solo evita
  que se añadan ficheros nuevos: lo que ya está en el índice y en la historia sigue ahí. Y en
  general, si el secreto llegó al repositorio, el `.gitignore` ya no arregla nada.
- **Borrar el secreto en un commit posterior y darlo por resuelto.** El valor sigue en la
  historia y en los clones. Primero se rota (se invalida), después se decide si merece la pena
  reescribir la historia, y se asume que el valor antiguo ya es público.
- **Meter secretos en la URL o en la cadena de consulta.** Las direcciones acaban en registros
  de acceso, en servidores intermedios, en el historial del navegador y en los informes de
  errores. Un token en una URL es un token publicado.
- **Imprimir la configuración al arrancar.** Ese `print(os.environ)` o el volcado de la
  configuración completa para «comprobar que llega bien» deja todos los secretos en el sistema
  de registros. Registra las claves presentes y su origen, nunca los valores.
- **Una credencial para todo.** Compartida entre servicios y entornos, no se puede rotar sin
  parar el sistema, no permite saber quién hizo qué y convierte cualquier filtración en un
  incidente total. Una credencial por servicio, por entorno y con los permisos mínimos.
- **Creer que un secreto de Kubernetes está cifrado.** Por defecto es un valor en base64, que
  es una codificación, no un cifrado. Hace falta cifrado en reposo del almacén, control de
  acceso por rol y, si el secreto va en el repositorio, un esquema de cifrado con clave
  externa.
- **Copiar secretos de producción al portátil.** Un cuaderno de pruebas con la clave real es
  la forma más habitual de que un secreto acabe en una captura de pantalla. Los entornos de
  desarrollo usan credenciales propias y con datos no reales
  ([[privacidad-y-gdpr]]).

## Comprueba que lo sabes

:::quiz
p: Descubres que una clave de API lleva dos semanas en un repositorio privado. ¿Cuál es la primera acción correcta?
o: Reescribir la historia del repositorio para eliminar el commit
o: Revocar y rotar la clave, y después investigar su uso
o: Cambiar el repositorio a privado, que ya lo era, y avisar al equipo
a: 2
e: Rotar invalida el valor de inmediato; reescribir la historia lleva horas, exige coordinar a todo el equipo y no elimina las copias que ya existen en clones y cachés. El orden correcto es rotar, revisar el registro de auditoría para ver si se usó y, solo entonces, decidir si se limpia la historia.
:::

:::quiz
p: ¿Por qué las variables de entorno no son el lugar perfecto para un secreto?
o: Porque no admiten caracteres especiales
o: Porque se heredan a los procesos hijos, son visibles para quien puede leer el proceso y acaban en volcados y registros con facilidad
o: Porque el sistema operativo las guarda en disco en texto plano siempre
a: 2
e: Las variables de entorno resuelven el problema de sacar la configuración del código y son cómodas con contenedores, pero no son una caja fuerte: se heredan, se pueden volcar sin querer, aparecen en informes de fallo y no se pueden rotar sin reiniciar. Para secretos de verdad, un gestor que los entregue con vida corta.
:::

:::quiz
p: Un filtro de redacción borra los campos llamados `password` y `token`. ¿Qué se le escapa?
o: Nada, con esos nombres ya está cubierto todo
o: Cualquier dato sensible que no se anuncie con un nombre sospechoso, como un número de tarjeta o un identificador personal
o: Solo los secretos cifrados
a: 2
e: La lista negra por nombre solo protege lo que se llama como esperas. Un número de tarjeta, un IBAN, un correo o un identificador de cliente no llevan ninguna palabra clave y pasan el filtro enteros. La redacción por nombre es necesaria, pero hace falta además clasificar los datos y no registrar los campos sensibles en origen.
:::

:::aviso
El fichero `.env` de tu portátil no es peligroso por existir, sino por lo que contiene. Si
lleva credenciales reales de producción, ya tienes dos problemas: el secreto vive en un disco
sin cifrado y sin auditoría, y tú no puedes saber si alguien lo usó porque lo compartes con
todo el equipo. Usa credenciales de desarrollo propias.
:::

:::truco
Cuando no puedas rotar algo (una clave de un proveedor externo, por ejemplo), al menos acota
el daño: limita por dirección IP de origen, por prefijo de datos o por cuota, y pon una alerta
que salte cuando el consumo se salga de lo normal. Un secreto con límites es mucho menos grave
que un secreto con permiso ilimitado.
:::
