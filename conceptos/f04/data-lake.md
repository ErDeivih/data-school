---
id: data-lake
titulo: Data lake
fase: 4
nivel: intermedio
rutas: [de]
prerequisitos: [ciclo-de-vida-del-dato, ficheros-y-encoding]
tags: [almacenamiento, crudo, gobierno, objetos]
resumen: Guardar los datos tal como llegan, en ficheros sobre almacenamiento de objetos, y ponerles esquema y orden al leerlos: mucha potencia y mucho pantano posible.
fuentes: ["Reis y Housley (2022), 'Fundamentals of Data Engineering'", "Kleppmann (2017), 'Designing Data-Intensive Applications'"]
---

## En una frase

Un **data lake** es un almacén de ficheros (normalmente en almacenamiento de objetos) donde los
datos se guardan primero, tal como llegan, y se les pone estructura y significado después, en
el momento de leerlos; su gran ventaja es que nunca pierdes el original, y su gran riesgo es
que nadie sepa qué hay dentro.

## La idea

Antes, el orden era: decidir qué datos hacen falta, diseñar el esquema y cargar. El lago invierte
el orden: **carga todo, decide después**. Eso resuelve tres problemas reales de golpe:

1. **El esquema aún no se conoce.** Una API nueva devuelve un JSON con campos que cambian cada
   mes. Si esperas a modelarlo, pierdes datos que ya no podrás recuperar.
2. **Reprocesar es inevitable.** Encontrarás un error en una transformación de hace seis meses.
   Si guardaste el original, reejecutas; si solo guardaste el resultado, ese dato se perdió.
3. **Formatos de consumo distintos.** El mismo evento en crudo lo quieren el equipo de
   analítica, el de machine learning y el de auditoría, cada uno con sus reglas.

La analogía útil es el **trastero frente a la cocina**. El trastero guarda cajas tal como
llegaron, sin abrirlas: cabe mucho, es barato y siempre puedes volver a mirar dentro. La cocina
tiene lo necesario, preparado y etiquetado para cocinar hoy. Nadie cocina desde el trastero, y
nadie tira la caja original antes de comprobar que el guiso salió bien.

El pantano (*data swamp*) aparece cuando solo se hace la primera mitad. Se vuelca todo durante
dos años y entonces:

- No sabes qué tablas existen ni quién las usa, porque no hay catálogo.
- Nadie sabe qué significa la columna `status`, porque el diccionario estaba en la cabeza de
  alguien que se fue.
- El mismo dato está en tres carpetas con tres nombres, cargado por tres equipos.
- Hay 800.000 ficheros de 200 kB, y una consulta tarda más en abrir ficheros que en leerlos.
- Se guardó el resultado transformado y se tiró el crudo: ya no se puede reprocesar nada.

Nada de eso es culpa del formato ni de la tecnología: es ausencia de gobierno. Un lago sano se
organiza en zonas con responsabilidades distintas ([[arquitectura-medallion]] las llama bronce,
plata y oro):

- **Crudo (bronce):** copia fiel del origen, **inmutable y de solo añadir**, con metadatos de
  carga. Nunca se edita un fichero que ya está aquí: se añade otro.
- **Depurado (plata):** tipado, deduplicado, con claves y particiones. Es donde vive la verdad
  operativa.
- **Servicio (oro):** agregados y tablas listas para BI o modelos, normalmente ya en un
  [[data-warehouse|almacén]] o en un [[lakehouse-y-table-formats|lakehouse]].

Entre el lago y el almacén no hay rivalidad: el lago guarda el crudo y el histórico completo; el
almacén guarda lo curado y modelado para responder preguntas. Muchos equipos acaban con las dos
cosas sobre el mismo almacenamiento de objetos.

## Definición formal

Vocabulario y reglas, porque casi todos los problemas del lago son de convención:

- **Objeto:** la unidad que guarda el almacenamiento de objetos, identificada por un *bucket* y
  una **clave** (la ruta). No hay directorios de verdad: `tabla=pais=ES/` es un prefijo de la
  clave, no una carpeta.
- **Tabla:** un prefijo más una convención de particiones más un esquema registrado en un
  catálogo. Sin esquema registrado no es una tabla, es un conjunto de ficheros.
- **Esquema al leer** (*schema-on-read*): los ficheros no validan nada al escribirse; el esquema
  se aplica al consultarlos. El precio es que un fichero corrupto se descubre en la consulta.
- **Zona cruda inmutable:** el fichero original se escribe una vez y se conserva con su huella
  (`sha256`) y su tamaño. Cualquier corrección va a una zona posterior, nunca al crudo.

Convención de rutas particionada por fecha y origen, la más común:

:::formula
ruta = origen/tabla/fecha_carga=AAAA-MM-DD/parte-0001.parquet
:::

Y la regla que decide si el lago seguirá siendo útil dentro de dos años: **todo objeto debe
poder rastrearse hasta su origen y su momento de carga**. Se guardan, como mínimo, el origen, la
fecha y hora de ingesta, el identificador del lote y el número de filas. Sin esos cuatro
metadatos, un fichero suelto es basura indistinguible de un dato valioso.

## Ejemplo

Una plataforma recibe 10 millones de eventos al día, de 400 bytes cada uno en JSON: unos 4 GB
diarios en crudo ([[compresion-y-codificacion|comprimir]] lo reduce, pero primero se guarda tal
cual).

- Escrito en micro-lotes de un minuto: `24 × 60 = 1.440` ficheros al día, `2,8 MB` cada uno, y
  **525.600 ficheros al año**. Una consulta de un solo día abre 1.440 ficheros.
- Compactado a ficheros horarios antes de publicar la zona depurada: 24 ficheros al día, de
  unos 170 MB. La misma consulta abre 24.
- Retención del crudo: 5 años son `4 GB × 365 × 5 ≈ 7,3 TB`. Barato de almacenar, caro de
  listar y de consultar si nadie particiona.

La diferencia entre las dos primeras cifras no es de espacio, es de **número de aperturas**: el
problema de los ficheros pequeños se paga en latencia y en peticiones facturadas, no en bytes.

## Código

```python verificable
import gzip, json

# 3.000 eventos con las mismas claves: en JSON la clave se repite en cada linea
eventos = [{"id": i, "ciudad": ["Madrid", "Barcelona", "Sevilla"][i % 3],
            "importe": round(10.0 + (i % 7), 2)} for i in range(3000)]

jsonl = "\n".join(json.dumps(e, ensure_ascii=False) for e in eventos).encode()
# Misma informacion en columnas: cada valor junto a los de su tipo
columnar = json.dumps({
    "id": [e["id"] for e in eventos],
    "ciudad": [e["ciudad"] for e in eventos],
    "importe": [e["importe"] for e in eventos],
}).encode()

print("bytes en JSON por lineas:", len(jsonl))     # -> bytes en JSON por lineas: 152889
print("bytes en columnar:", len(columnar))         # -> bytes en columnar: 68923
print("columnar mas pequeno:", len(columnar) < len(jsonl))   # -> columnar mas pequeno: True
print("gzip baja de la mitad:", len(gzip.compress(jsonl)) < len(jsonl) // 2)  # -> gzip baja de la mitad: True
```

```python verificable
# Coste de los ficheros pequenos: no es el espacio, es el numero de aperturas
tam_dia_gb = 4
print("ficheros al dia con micro-lotes de 1 minuto:", 24 * 60)                 # -> ficheros al dia con micro-lotes de 1 minuto: 1440
print("MB por fichero de 1 minuto:", round(tam_dia_gb * 1024 / (24 * 60), 1))  # -> MB por fichero de 1 minuto: 2.8
print("ficheros al ano:", 24 * 60 * 365)                                       # -> ficheros al ano: 525600
print("ficheros al dia compactando por hora:", 24)                             # -> ficheros al dia compactando por hora: 24
print("GB retenidos en 5 anos:", tam_dia_gb * 365 * 5)                         # -> GB retenidos en 5 anos: 7300
```

## Errores típicos

- **Volcar sin catálogo ni metadatos.** Un lago sin catálogo ([[catalogo-y-linaje]]) no es un
  activo, es un vertedero. Como mínimo: qué tablas hay, quién las produce, qué contienen y
  cuándo se actualizaron por última vez.
- **Guardar solo lo transformado o editar el crudo.** Si el crudo no se conserva, un fallo en la
  transformación es irreversible. Y corregir un fichero «a mano» rompe la trazabilidad y hace que
  dos ejecuciones del mismo proceso den resultados distintos: la zona cruda es de solo añadir.
- **Particionar por una columna de cardinalidad altísima.** Particionar por `id_cliente` crea
  millones de micro-ficheros y arruina el rendimiento y la factura. Particiona por fecha y
  ordena o agrupa por el resto ([[particionado-y-clustering]]).
- **Consultar el crudo desde el cuadro de mando.** El crudo está sin tipar, con duplicados y sin
  garantías de calidad. La capa de servicio es la depurada; el crudo es para reprocesar
  ([[calidad-de-datos]]).
- **No borrar nunca.** Guardar todo para siempre también tiene coste y obligaciones legales: hay
  que definir retención por tipo de dato y cumplirla ([[gobierno-y-privacidad]],
  [[coste-y-optimizacion]]).
- **Ignorar el coste por petición.** El almacenamiento de objetos cobra por guardar, pero también
  por listar y por leer. Un proceso que lista un prefijo con millones de claves cada cinco
  minutos genera una factura sorprendente sin mover ni un dato.

## Comprueba que lo sabes

:::quiz
p: ¿Qué significa «esquema al leer» en un data lake?
o: Que el esquema se valida al escribir cada fichero y se rechaza el que no encaje
o: Que los ficheros se escriben sin validar y el esquema se aplica cuando se consultan
o: Que no hace falta definir ningún esquema nunca
a: 2
e: Al escribir solo se guardan bytes; la estructura se interpreta al leer. Eso permite cargar datos cuyo esquema aún no conoces, pero traslada la detección de errores al momento de la consulta, así que el esquema debe estar registrado y versionado en un catálogo.
:::

:::quiz
p: ¿Por qué hay que conservar el fichero original en la zona cruda aunque esté sucio o duplicado?
o: Porque ocupa poco y nunca molesta
o: Porque es la única forma de reprocesar cuando aparezca un error en la transformación
o: Porque las herramientas de BI lo necesitan para pintar los gráficos
a: 2
e: El crudo es la fuente de verdad de la que se puede reconstruir todo lo demás. Si solo guardas el resultado transformado y la transformación estaba mal, esos datos son irrecuperables. La BI consume la capa depurada, no el crudo.
:::

:::quiz
p: Un proceso escribe un fichero por minuto durante un año. ¿Cuál es el problema principal?
o: Que ocupa demasiado espacio en disco
o: Que las consultas tienen que abrir cientos de miles de ficheros pequeños y se vuelven lentas y caras
o: Que no se puede comprimir cada fichero por separado
a: 2
e: El espacio total es el mismo; lo que cambia es el número de objetos que hay que listar y abrir en cada consulta, más la sobrecarga de metadatos. La solución es compactar periódicamente a ficheros de tamaño razonable antes de publicarlos.
:::

:::nota
«Lago» no significa «sin reglas». Las reglas cambian de sitio: en lugar de validar al escribir,
el lago exige metadatos de carga, zonas con responsabilidad definida, catálogo y particionado.
Un lago sin esas cuatro cosas no tarda en convertirse en el pantano del que todo el mundo se
queja.
:::
