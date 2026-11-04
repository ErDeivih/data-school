# Datasets — criterio, procedencia y verificación

Esta carpeta reúne los **datos base de Data School**: 10 conjuntos sintéticos que se alojan aquí
porque son propios y su licencia lo permite, más el manifiesto que los describe y el generador que
los produce. Los datasets de terceros **no se copian ni se alojan**: se enlazan (ver
[`FUENTES-EXTERNAS.md`](FUENTES-EXTERNAS.md)).

## Qué hay aquí

| Ruta | Qué es | Se aloja |
|---|---|---|
| [`csv/`](csv/) | Los 10 datasets en CSV, copiados byte a byte del proyecto de origen. | Sí |
| [`datasets.json`](datasets.json) | Manifiesto: id, título, fichero, filas, columnas con tipo y unidad, origen, licencia y `sha256` de cada conjunto. | Sí |
| [`generar-datasets.mjs`](generar-datasets.mjs) | Generador determinista con semilla fija por conjunto; copia literal del proyecto de origen. | Sí (es la procedencia) |
| [`CATALOGO.md`](CATALOGO.md) | Catálogo legible, generado desde `datasets.json`, con la tabla de verificación sha256 (10/10). | Sí (generado) |
| [`FICHAS.md`](FICHAS.md) | Una ficha por dataset con los mismos 12 campos: id, título, fichero, licencia, procedencia, tamaño, columnas y tipos, checksum, dificultad, preguntas que permite responder, proyectos que lo usan y limitaciones. | Sí |
| [`VERIFICACION.md`](VERIFICACION.md) | Los 10 CSV perfilados uno a uno (`data_profile`) y contrastados con `datasets.json`: filas, columnas, tipos, nulos, duplicados, outliers y desajustes. | Sí |
| [`_verificar-fichas.ps1`](_verificar-fichas.ps1) | Comprobador reproducible de esta carpeta: 10 fichas × 12 campos, 10 perfiles, cifras de tipos y filas contra `datasets.json`, 30 citas de proyecto contra `proyectos/CATALOGO.md`, enlaces relativos, cabeceras y checksums. Imprime el recuento de criterios; exit 0 solo si pasan todos. | Sí (auxiliar) |
| [`FUENTES-EXTERNAS.md`](FUENTES-EXTERNAS.md) | Catálogos externos de datasets: solo enlace y licencia por ítem. | No (no se copia nada) |
| `README.md` | Este documento. | — |

**Documentación de los 10 conjuntos**: una ficha por dataset en [FICHAS.md](FICHAS.md) (id, título,
fichero, licencia, procedencia, tamaño, columnas y tipos, checksum, dificultad, preguntas, proyectos y
limitaciones) y el resultado de cargar y contrastar los 10 CSV en
[VERIFICACION.md](VERIFICACION.md) (filas, columnas, tipos, nulos, duplicados, outliers y desajustes).

## Criterio de admisión

Un dataset se enlaza o se aloja solo si cumple las tres condiciones:

1. **Licencia declarada por escrito.** Sin licencia clara no entra: como mucho se enlaza desde el
   catálogo de fuentes. «Gratis» no significa «reutilizable», y «se puede descargar» no significa
   «se puede redistribuir».
2. **Procedencia.** Consta de dónde sale: autor o institución, URL original, fecha de consulta y, si
   se genera, el script y la semilla.
3. **Derechos de terceros y datos personales.** No se alojan aquí datos de personas ni material con
   derechos de terceros. Si un ejercicio necesita un dataset ajeno, se enlaza su ficha oficial y se
   anotan licencia y procedencia en el propio ejercicio.

La licencia **por ítem** no se hereda del catálogo: si la fuente dice «una licencia por dataset»
(Kaggle, Hugging Face, data.gov, datos.gob.es, UCI), hay que abrir la ficha del dataset concreto
antes de usarlo. Los catálogos externos están en [`FUENTES-EXTERNAS.md`](FUENTES-EXTERNAS.md).

## Por qué estos 10 son propios y se alojan

- **Son sintéticos.** No salen de personas reales ni de datos con derechos de terceros: los genera
  un PRNG de semilla fija. Alojarlos no plantea ningún problema de derechos.
- **Son CC0-1.0.** El manifiesto declara `CC0-1.0` para los 10. Es una renuncia a derechos: se
  pueden copiar, modificar y redistribuir sin pedir permiso ni atribución.
- **Son reproducibles.** Cada conjunto tiene su semilla fija en el generador: los mismos bytes, y
  por tanto el mismo SHA-256, siempre. Un dataset que no se puede regenerar con el mismo checksum
  es un fichero con suerte.
- **Son el material de práctica común.** Se alojan para que los ejercicios arranquen sin depender de
  una descarga externa ni de que un catálogo ajeno cambie de licencia o de URL.

**10, no 6.** El comentario de cabecera de `generar-datasets.mjs` habla de «los seis datasets»; el
array `CONJUNTOS` tiene **10**: los seis primeros (ventas, churn, precios, sensores, encuestas,
algoritmos) y cuatro añadidos después (telemetría F1, cartera de acciones, clasificación F1 y
partidos de fútbol). El recuento que manda es el del manifiesto: **10 conjuntos, 2530 filas y 63
definiciones de columna** (ver [`CATALOGO.md`](CATALOGO.md)). El comentario está desfasado, no el
manifiesto.

**Copia byte a byte.** Los CSV de `csv/` son copia exacta de los del proyecto de origen (`aprender`,
`web/datos/datasets/`). No se reescribieron ni se abrieron y guardaron con otra herramienta: por eso
sus checksums coinciden con los del manifiesto, que también se copió tal cual (sus rutas `fichero`
siguen apuntando a `datos/datasets/…`, la ruta del proyecto de origen).

## Cómo se verifica

El manifiesto declara un `checksum` con prefijo `sha256:` por conjunto. La comprobación recalcula el
SHA-256 de los **bytes completos del CSV** (cabecera incluida) y lo compara con el declarado. Es
igualdad byte a byte: si un fichero se toca, aunque sea un salto de línea, el hash cambia.

Resultado de la comprobación del **2026-11-04**: **10/10 coinciden**. La tabla completa, con los dos
hashes de cada conjunto y la columna «sha256 coincide (sí/no)», está en [`CATALOGO.md`](CATALOGO.md).

Para repetirla desde esta carpeta (`datasets/`):

```powershell
node -e "const fs=require('fs'),c=require('crypto'),m=require('./datasets.json');let ok=0;for(const s of m.conjuntos){const h='sha256:'+c.createHash('sha256').update(fs.readFileSync('./csv/'+s.id+'.csv')).digest('hex');const v=h===s.checksum;ok+=v?1:0;console.log((v?'OK  ':'MAL ')+s.id)};console.log(ok+'/'+m.conjuntos.length+' coinciden')"
```

Salida esperada: diez líneas `OK` y `10/10 coinciden`. Si aparece un `MAL`, el CSV no es el que
declara el manifiesto: se regenera (siguiente apartado) y se vuelve a comprobar; **no se edita el CSV
a mano**.

## Cómo se regeneran

El generador está en [`generar-datasets.mjs`](generar-datasets.mjs), copiado del proyecto de origen.
Se ejecuta con Node 20 o superior y es determinista: PRNG con semilla fija por conjunto, fechas
fijas, orden fijo de filas. Misma semilla y mismo script → mismos bytes → mismo SHA-256.

- **En el proyecto de origen** (es su sitio natural): desde la raíz de `aprender`,
  `node datos/generar-datasets.mjs`, que escribe `web/datos/datasets/*.csv` y
  `web/datos/datasets.json`.
- **En este repositorio**: la copia conserva las rutas del origen. Sus dos constantes,
  `SALIDA = RAIZ/web/datos/datasets` y `MANIFIESTO = RAIZ/web/datos/datasets.json`, no existen en
  `data-school`. Para regenerar aquí hay que ajustar esas dos constantes a `datasets/csv` y
  `datasets/datasets.json`, o regenerar en el origen y volver a copiar. La copia no se toca sin
  dejar constancia: es la prueba de cómo se generó cada fila.

Después de regenerar: recalcular los checksums, actualizar `datasets.json` si cambian (no deberían)
y regenerar `CATALOGO.md` desde el manifiesto.

## Datasets externos: se enlazan, no se copian

Los datasets ajenos **no se copian ni se alojan** aquí, aunque su licencia lo permitiera. Se
enlazan, se lee la licencia de cada ítem y se anota la procedencia. Motivos:

- la licencia es **por dataset** y cambia de uno a otro: alojar el fichero obliga a vigilarla para
  siempre, y basta un cambio para quedarse con una copia sin derechos;
- algunas licencias exigen atribución, no comercial o compartir igual: cada copia arrastra sus
  condiciones y se pierden de vista al mezclarla con material propio;
- el criterio del proyecto es claro: **el material de terceros nunca se copia**.

Los seis catálogos externos (Kaggle Datasets, Hugging Face Datasets, data.gov, datos.gob.es, UCI ML
Repository e IMDb non-commercial) están descritos en [`FUENTES-EXTERNAS.md`](FUENTES-EXTERNAS.md),
con su licencia por ítem y el aviso de IMDb (solo uso personal y no comercial).

## CSV de los proyectos

En este repositorio también hay CSV dentro de `proyectos/` (por ejemplo
`proyectos/pf-01-pulso-poblacion/data/poblacion.csv` o `proyectos/pf-02-openf1/data/vueltas.csv`).
Son los datos de cada proyecto concreto, no material base del catálogo: **su procedencia, fecha de
obtención y licencia están en el README de cada proyecto**. No se mezclan con `datasets/csv/`: aquí
está el material sintético común; allí, los datos de cada caso. `proyectos/CATALOGO.md` asigna a cada
proyecto el id del dataset del catálogo con el que se practica.

## Resumen (2026-11-04)

- 10 CSV en `csv/`, 10 conjuntos en `datasets.json`, 10/10 checksums coincidentes.
- 2530 filas y 63 definiciones de columna en total; todos sintéticos y CC0-1.0.
- Manifiesto y generador presentes; el catálogo legible es `CATALOGO.md`.
- Datasets externos: enlazados, nunca copiados.
