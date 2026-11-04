---
id: copias-de-seguridad-y-recuperacion
titulo: Copias de seguridad y recuperación ante desastres
fase: 11
nivel: intermedio
rutas: [de, alg]
prerequisitos: [almacenamiento-de-objetos, gobierno-y-privacidad, incidentes-y-postmortem]
tags: [backups, recuperacion, rpo, rto, desastres]
resumen: Cuánto dato puedes permitirte perder y cuánto tardas en volver: RPO y RTO, la regla 3-2-1, copias inmutables y la única prueba que vale, restaurar de verdad.
fuentes: ["Beyer y otros (2016), 'Site Reliability Engineering'", "Kleppmann (2017), 'Designing Data-Intensive Applications'", "PostgreSQL Global Development Group (2024), 'PostgreSQL 16 Documentation: Backup and Restore'"]
---

## En una frase

Una copia de seguridad no es una carpeta con ficheros: es un plan con dos números —cuánto dato
puedes perder y cuánto tiempo puedes tardar en volver— y una única prueba de que existe, que es
haber restaurado de verdad, en el tiempo prometido y sin la máquina original.

## La idea

Cuando alguien dice «tenemos copias de seguridad», la pregunta útil es otra: **si el servidor se
muere ahora mismo, ¿cuántos datos pierdo y cuánto tardo en volver?** La primera cifra se llama
RPO (cuánto dato puedes perder, medido en tiempo) y la segunda RTO (cuánto tardas en volver a
servir). Sin esas dos cifras, «tenemos copias» no significa nada: un volcado de hace un año es una
copia de seguridad y también es una pérdida de un año de trabajo.

La analogía es la llave de repuesto. Guardar una llave en un cajón no te protege: te protege
saber dónde está, que abra la puerta que crees y que alguien haya probado a entrar con ella. Una
copia que nunca se ha restaurado es una hipótesis, no una garantía.

**Una réplica no es una copia.** Es el malentendido más caro del oficio. Una réplica reproduce
todo lo que pasa en el original, en milisegundos, incluidas las cosas que no quieres reproducir:
el `DELETE` sin `WHERE`, la migración que corrompe una columna, el cifrado del secuestrador de
datos. La réplica te protege del disco roto y no te protege del error humano ni del ataque, que
son las dos causas más frecuentes de pérdida de datos. Copia y réplica no compiten: resuelven
problemas distintos y hacen falta las dos.

**La regla 3-2-1**, que lleva décadas funcionando: tres copias de los datos, en dos medios o
tecnologías distintas, y una fuera de la instalación. La versión moderna le añade dos condiciones:
una copia **inmutable** y **cero errores** de verificación. La inmutabilidad (objeto con bloqueo
de escritura, cinta, almacenamiento de solo escritura) es lo que responde al secuestro de datos:
un atacante con credenciales de administrador puede borrar cualquier copia que pueda modificar,
así que la única copia que sobrevive es la que no se puede tocar. La ventana de inmutabilidad
tiene que ser mayor que el tiempo que tardas en darte cuenta de que te han atacado; si guardas
siete días inmutables y tardas quince en detectarlo, la copia buena ya caducó.

**Consistencia.** Copiar el fichero de una base de datos en marcha da una copia desgarrada: la
primera mitad de la copia es de un instante y la segunda de otro, y al restaurarla la base no
arranca o, peor, arranca con datos incoherentes. Por eso se copia con instantánea del volumen, con
la herramienta de copia en caliente del motor, o con registros de escritura (WAL) que permiten
reconstruir el estado exacto de un instante concreto. Eso último es la **recuperación a un punto
en el tiempo**: guardas la copia completa del domingo y todos los registros desde entonces, y
puedes volver a las 14:32:07 del martes, justo antes del error.

**La clave de cifrado es parte de la copia.** Cifrar las copias es obligatorio y custodia mal la
clave es la forma más elegante de perderlo todo: si la clave vive en el mismo llavero, en la misma
cuenta o en la misma región que el sistema que se ha perdido, la copia es un montón de bytes
ilegibles. La clave se guarda aparte, se rota con cuidado y se prueba que abre la copia.

**Restaurar la base no es restaurar el servicio.** Vuelven los datos, y también hay que volver a
levantar la aplicación, los secretos, los certificados, el DNS, los trabajos programados y las
colas. Todo lo que estaba en una cola en el momento del fallo no está en ninguna copia, y hay que
decidir si se descarta o se reconstruye. La infraestructura como código es lo que hace que esa
parte sea aburrida en vez de heroica ([[iac-y-terraform]]).

**Borrar también es un requisito.** Retención no es «guardar todo para siempre»: hay datos
personales, hay plazos legales y hay solicitudes de supresión. La política tiene que decir cuánto
se guarda, qué se borra y cómo se atiende una petición de supresión cuando el dato también está en
una copia ([[gobierno-y-privacidad]]).

## Definición formal

**RPO.** El punto de recuperación objetivo es la antigüedad máxima aceptable del último estado
recuperable. Con una tasa de escritura constante, el dato en riesgo es:

:::formula
datos_en_riesgo = tasa_de_escritura · RPO
:::

**RTO.** El tiempo de recuperación objetivo es la suma de todo lo que ocurre desde el fallo hasta
que el servicio vuelve a atender:

:::formula
RTO = detección + decisión + aprovisionamiento + restauración + verificación + cambio de tráfico
:::

**El tiempo de restauración** es el trozo que se puede medir y ensayar:

:::formula
t_restauración = tamaño_de_la_copia / ancho_de_banda + reproducción_de_registros + verificación
:::

**Copias independientes.** Si cada copia tiene probabilidad `p` de ser inservible por un fallo
propio, la probabilidad de perderlo todo es:

:::formula
P(pérdida_total) = p^n     con n copias independientes
:::

**Disponibilidad y tiempo medio de reparación.** El RTO es el `MTTR` de la ecuación clásica:

:::formula
A = MTBF / (MTBF + MTTR)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `RPO` | Antigüedad máxima aceptable del último estado recuperable | minutos u horas | Sube el dato que se pierde en cada incidente, en línea recta con la tasa de escritura. Un RPO de 24 h con 3.000 pedidos al día pone en riesgo hasta 3.000 pedidos |
| `RTO` | Tiempo máximo aceptable desde el fallo hasta volver a servir | minutos u horas | Al subir, el parón cuesta más y también crece el número de decisiones que hay que tomar con prisa. Es la cifra que se promete al negocio y la que se mide en los ensayos |
| `MTBF` | Tiempo medio entre fallos | horas o días | Al subir, la disponibilidad mejora, pero es caro de mover: casi siempre se mejora más bajando el `MTTR` |
| `MTTR` | Tiempo medio de reparación, del que el RTO es la parte planificada | minutos u horas | Al bajar, la disponibilidad sube de forma casi proporcional. Es la palanca barata: automatizar la restauración baja el `MTTR` sin comprar hardware |
| Frecuencia de copia | Cada cuánto se genera un punto recuperable | minutos u horas | Al subirla, el RPO baja y el coste sube: más ventanas de copia, más espacio y más carga en el origen. La frecuencia no puede ser mayor que el RPO que prometes |
| Retención | Cuánto tiempo se guarda cada copia | días, meses o años | Al subirla, sube el espacio y sube la factura, pero también la probabilidad de tener una copia anterior a un daño que tardaste en detectar. En datos personales, además, hay un límite legal |
| `n` | Número de copias realmente independientes | copias | Con `p = 0,01`, pasar de una a tres copias baja la probabilidad de perderlo todo de 1e-2 a 1e-6. Solo cuenta si los fallos son independientes: tres copias en la misma cuenta son una copia |
| Ancho de banda | Velocidad real de traída de la copia, no la del enlace contratado | MB/s | Al subir, baja el tiempo de restauración y con él el RTO. Es lo primero que se satura en un desastre, porque todo el mundo recupera a la vez |
| `p` | Probabilidad de que una copia sea inservible por un fallo propio | tanto por uno | Al subir (copias que nadie verifica, discos sin comprobar, cifrado sin clave), la probabilidad de pérdida total sube como `p^n`: con `p = 0,1` hacen falta tres copias para bajar de una entre mil |
:::

## Ejemplo

Una base de datos de 400 GB con copia completa diaria a las 03:00, 30 GB de cambios al día y una
red de restauración de 120 MB/s. Supón un fallo a las 09:00 y 3.000 pedidos al día (uno cada 28,8
segundos).

- **Traer la copia completa:** 400 · 1.024 MB / 120 MB/s = 3.413 s = **57 minutos**.
- **RTO:** detección 8 min + decisión 5 min + aprovisionamiento 15 min + restauración 57 min +
  reproducción de registros 40 min + verificación 25 min = **150 minutos**. Dos horas y media
  desde que se rompe hasta que el usuario vuelve.
- **RPO con copia diaria:** se restaura la copia de las 03:00, así que se pierden las 6 horas
  transcurridas: **125 pedidos** que hay que reconstruir a mano o devolver.
- **RPO con recuperación a un punto en el tiempo**, archivando registros cada 5 minutos: se pierden
  **10,4 pedidos** como mucho. La diferencia entre 125 y 10,4 pedidos es lo que cuesta archivar
  registros cada cinco minutos, y casi siempre sale a favor.
- **Coste esperado:** con un coste de parón de 12.000 euros por hora, cada incidente cuesta
  2,5 · 12.000 = 30.000 euros de parón, más 40 euros por pedido que haya que reconstruir. Si un
  incidente grave ocurre una vez cada cinco años, el coste esperado es 0,2 · (30.000 + 125 · 40) =
  **7.000 euros al año**. El ensayo de restauración trimestral cuesta unas horas de una persona:
  no hay comparación posible.
- **Espacio de retención:** guardar 365 copias completas del año son 146.000 GB. Una política de
  abuelo-padre-hijo (7 incrementales diarias, 4 completas semanales y 12 completas mensuales) ocupa
  7 · 30 + 16 · 400 = **6.610 GB**, veintidós veces menos, y cubre el caso que importa: volver a
  un estado anterior a un daño que tardaste un mes en detectar.
- **Copias independientes:** si cada copia tiene un 1 % de probabilidad de ser inservible, una
  copia deja una posibilidad entre cien de perderlo todo; tres copias independientes, una entre un
  millón. Tres copias en la misma cuenta y la misma región no son tres copias: son una con tres
  nombres.

:::figura
fichero: copias-rpo-rto-y-copias
pie: Izquierda, la línea del tiempo de un incidente: la banda roja es el RPO, los datos escritos entre la última copia y el fallo que no vas a poder recuperar, y la banda azul es el RTO, el rato que el servicio está de rodillas mientras se trae la copia, se reproducen los registros y se verifica. Derecha, la probabilidad de perderlo todo según cuántas copias sean de verdad independientes: cada copia que no comparte cuenta, región ni credenciales divide el riesgo entre cien, y la línea roja se queda plana porque tres copias en la misma cuenta son una sola copia con tres nombres.
fuente: figuras/copias-de-seguridad-y-recuperacion-1.py
:::

## Código

```python verificable
# El plan de recuperacion son numeros, no una carpeta con ficheros.
tamano_gb, ancho_mb_s = 400, 120

minutos_copia = tamano_gb * 1024 / ancho_mb_s / 60
print("traer la copia completa: %.0f min" % minutos_copia)          # -> 57

# RTO: todo lo que pasa desde que se rompe hasta que el usuario vuelve.
fases = [("deteccion", 8), ("decision", 5), ("aprovisionar", 15),
         ("restaurar", minutos_copia), ("reproducir registros", 40),
         ("verificar", 25)]
for nombre, m in fases:
    print("  %-22s %5.0f min" % (nombre, m))
total = sum(m for _, m in fases)
print("RTO total: %.0f min (%.1f h)" % (total, total / 60))        # -> 150 min (2.5 h)

# RPO: cuanto dato se pierde con cada frecuencia de copia.
pedidos_dia = 3000
for rpo_min in (1440, 60, 15, 5):
    print("RPO %4d min -> hasta %6.1f pedidos perdidos" % (rpo_min, pedidos_dia * rpo_min / 1440))
# -> RPO 1440 min -> hasta 3000.0 pedidos perdidos
# -> RPO    5 min -> hasta   10.4 pedidos perdidos
```

:::claves
- La división por 60 va al final y por eso `minutos_copia` sale en minutos mientras el ancho de
  banda está en MB/s. Es el error de unidades clásico de este cálculo: mezclar GB con MB multiplica
  o divide el resultado por mil y el plan sale con un RTO diez veces mayor o menor del real.
- `%6.1f` con 31,25 imprime `31.2`, no `31.3`: el redondeo de coma flotante va al par más cercano.
  Si el número va a un informe que alguien va a discutir, redondea tú a mano y dilo.
- El bucle `fases` devuelve los minutos de cada etapa porque la restauración casi nunca es una
  sola operación. Cuando cuentes un RTO de verdad, suma también lo que nadie apunta: avisar a
  quien decide, pedir permiso para restaurar y esperar a que la ventana de mantenimiento lo
  permita.
- El RPO se calcula por tasa de escritura, no por número de filas: 3.000 pedidos al día con sus
  líneas, sus eventos y sus pagos son muchos más registros que 3.000, y el dato en riesgo se mide
  en registros o en euros, no en filas de una sola tabla.
:::

```python verificable
# Cuatro copias no valen cuatro veces mas: valen la probabilidad de que fallen a la vez.
p_copia_inservible = 0.01
for n in (1, 2, 3, 4):
    print("%d copia(s) -> probabilidad de perderlo todo: %.0e" % (n, p_copia_inservible ** n))
# -> 1 copia(s) -> probabilidad de perderlo todo: 1e-02
# -> 3 copia(s) -> probabilidad de perderlo todo: 1e-06

# El coste esperado decide cuanto se gasta en el plan: frecuencia por dano por incidente.
coste_hora_paron = 12000
rto_horas = 2.5
valor_pedido = 40
for frecuencia in (1.0, 0.2, 0.05):        # incidentes graves al ano
    for pedidos_perdidos in (3000, 10):
        dano = rto_horas * coste_hora_paron + pedidos_perdidos * valor_pedido
        print("%.2f incidentes/ano, %5d pedidos perdidos -> %.0f EUR/ano"
              % (frecuencia, pedidos_perdidos, frecuencia * dano))
# -> 0.20 incidentes/ano,  3000 pedidos perdidos -> 30000 EUR/ano
# -> 0.20 incidentes/ano,    10 pedidos perdidos -> 6080 EUR/ano
```

```python verificable
# La retencion pesa mas que la frecuencia: nadie guarda 365 copias completas.
completa_gb, incremental_gb = 400, 30
diarias, semanales, mensuales = 7, 4, 12

gfs = diarias * incremental_gb + (semanales + mensuales) * completa_gb
diario_completo = 365 * completa_gb
print("abuelo-padre-hijo: %6.0f GB" % gfs)                    # ->   6610 GB
print("365 copias completas: %6.0f GB" % diario_completo)     # -> 146000 GB
print("factor de ahorro: %.0f x" % (diario_completo / gfs))   # -> 22 x
```

## Errores típicos

- **Confundir la réplica con la copia.** La réplica reproduce el borrado accidental y el cifrado
  del secuestrador de datos en milisegundos. Sirve para el disco roto; para el error humano y el
  ataque hace falta una copia que no se pueda modificar ni borrar desde la cuenta de producción.
- **Dar por buena la copia porque el trabajo terminó en verde.** Que el proceso acabe sin error
  solo dice que escribió bytes. Lo que hay que verificar es que la copia **restaura** y que los
  datos cuadran: recuentos, sumas de control y una consulta de comprobación sobre la base
  restaurada. Una copia de 400 GB puede estar perfectamente escrita y ser inservible
  ([[reconciliacion-y-pruebas]]).
- **Todas las copias en el mismo sitio.** Misma cuenta, mismo proveedor, mismas credenciales,
  misma región: un error de configuración o un atacante con esas credenciales se lleva las tres a
  la vez, y la fórmula `p^n` deja de valer porque los fallos ya no son independientes.
- **Copias mutables.** Si la credencial que usa el proceso de copia también puede borrar copias,
  el secuestrador de datos borra primero las copias y después cifra el original. La inmutabilidad
  con ventana suficiente es la defensa, no la buena voluntad.
- **Copiar una base de datos en marcha sin instantánea ni registros.** La copia sale desgarrada y
  se descubre el día que hace falta. Si no puedes parar el motor, usa su herramienta de copia en
  caliente o archiva los registros de escritura.
- **Cifrar sin custodiar la clave.** La clave en el mismo llavero, la misma cuenta o la misma
  región que los datos convierte la copia en ruido. Se custodia aparte, se rota y se prueba.
- **Olvidar todo lo que no es la base de datos.** Secretos, certificados, configuración, DNS,
  trabajos programados, ficheros de los usuarios y lo que estaba en las colas. Restaurar la base
  sin esto alarga el RTO horas y nadie lo apunta en el plan.
- **Retención más corta que el tiempo de detección.** Guardar siete días de copias está bien si
  detectas un fraude o una corrupción en tres días. Si tardas un mes, la copia buena ya se borró:
  la retención se elige por el tiempo que tardas en enterarte, no por lo que ocupa el disco.

## Comprueba que lo sabes

:::practica
enunciado: Una tienda online declara RPO de 15 minutos y RTO de 1 hora. La base de datos ocupa 800 GB, la copia completa se hace cada noche a las 02:00, la red de restauración va a 80 MB/s, el archivo de registros se sube cada 5 minutos y el equipo tarda 20 minutos en detectar el fallo y 10 en decidir. ¿Se cumplen el RPO y el RTO prometidos? Si no, ¿qué cambiarías primero?
pista: Separa las dos promesas. El RPO depende de la frecuencia con la que creas puntos recuperables; el RTO, del tamaño de la copia dividido entre el ancho de banda, más todo lo demás.
solucion: El RPO sí se cumple: los registros se archivan cada 5 minutos, así que el último estado recuperable nunca es más viejo que esos 5 minutos, por debajo de los 15 prometidos. El RTO no se cumple: 800 · 1.024 / 80 = 10.240 s = 171 minutos solo para traer la copia, más 20 de detección, 10 de decisión, unos 15 de aprovisionamiento, 40 de reproducción de registros y 25 de verificación dan unas 4,7 horas, muy por encima de la hora prometida. Lo primero que cambiaría no es el ancho de banda, que es caro, sino el formato de la promesa y la estrategia: mantener una réplica en caliente o una copia preparada y verificada lista para arrancar (el RTO baja a minutos), reservar ancho de banda dedicado a la restauración, y ensayar la restauración al menos una vez al trimestre para saber de verdad cuánto tarda. Si el negocio necesita una hora de verdad, la copia del almacén de objetos no es el camino: hace falta un sistema en espera ya poblado.
:::

:::quiz
p: ¿Por qué una réplica de la base de datos no sustituye a una copia de seguridad?
o: Porque la réplica ocupa más espacio y sale más caro
o: Porque la réplica reproduce también el borrado accidental, la corrupción y el cifrado del ataque
o: Porque las réplicas solo sirven para leer y no se pueden restaurar
a: 2
e: Una réplica sigue al original en milisegundos, así que hereda todo lo que le pasa al original: el `DELETE` sin `WHERE`, la migración que rompe una columna y el cifrado del secuestrador de datos. La copia resuelve un problema distinto porque guarda un estado anterior y, si es inmutable, sobrevive al ataque. El coste y el uso de lectura no son la razón.
:::

:::quiz
p: Guardas tres copias de la base de datos, las tres en la misma cuenta de almacenamiento y la misma región, y cada una tiene un 1 % de probabilidad de ser inservible. ¿Cuál es la probabilidad real de perderlo todo?
o: Una entre un millón, porque 0,01 elevado a 3 es 1e-6
o: Bastante mayor que una entre un millón, porque las tres comparten cuenta y región y el fallo no es independiente
o: Un 3 %, porque las probabilidades se suman
a: 2
e: La fórmula 0,01 elevado a 3 = 1e-6 solo vale si los fallos son independientes. Con las tres copias en la misma cuenta y la misma región, un borrado con esas credenciales, un error de configuración o una caída del proveedor se lleva las tres a la vez: eso es un fallo común y la probabilidad se parece mucho más a la de una sola copia. La independencia hay que conseguirla a propósito: otra cuenta, otro proveedor, otra región, otra credencial y, si puede ser, una copia que no se pueda borrar.
:::

:::quiz
p: El trabajo de copia termina todas las noches sin error y con el fichero del tamaño esperado. ¿Qué falta para poder decir que las copias funcionan?
o: Nada, si el tamaño es el correcto la copia está completa
o: Haber restaurado esa copia en un entorno limpio, que los datos cuadren y que el tiempo medido quepa en el RTO
o: Añadir una segunda copia en la misma carpeta, por si acaso
a: 2
e: El tamaño correcto solo demuestra que se copiaron bytes. La prueba es restaurar en un entorno sin la máquina original, comprobar recuentos y sumas de control y cronometrar el proceso: ese cronómetro es el único RTO que existe. Duplicar en la misma carpeta no añade independencia y hereda cualquier fallo de esa ubicación.
:::

:::trampa
El plan de recuperación que solo está en la cabeza de quien lo escribió, o en un wiki que vive en el
mismo sistema que se ha caído. El runbook tiene que estar accesible cuando no hay sistema: una
copia en papel, un repositorio que no dependa del sistema caído y los teléfonos de quien tiene las
credenciales. Durante un desastre nadie lee documentación: se ejecuta lo que se ha ensayado.
:::

:::nota
El RTO que importa es el que se mide en un ensayo, no el que sale de una hoja de cálculo. La
primera restauración real siempre tarda más de lo previsto, casi siempre por algo que nadie
apuntó: una versión distinta del motor, un certificado caducado, una tabla que creció, un
procedimiento que solo una persona sabía ejecutar. Ensayar convierte esas sorpresas en tareas
pendientes en vez de en horas de parón ([[incidentes-y-postmortem]]).
:::
