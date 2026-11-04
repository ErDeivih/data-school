# Figuras y scripts de figuras — qué hay, qué está en uso y qué se conserva

**Fecha:** 2026-11-04

**Qué es este documento.** El recuento razonado de `figuras/` (370 `.svg`) y `figuras-fuente/`
(350 `.py`): qué ficheros están en uso en el temario, cuáles son material de apoyo, cómo se
distinguen unos de otros y por qué se conservan todos. Los conceptos y sus bloques `:::figura`
están en `f00/` … `f12/`; la evidencia de ejecución del código, en `verificacion/`.

## 1. Recuento

| Zona | Ficheros | En uso | Material de apoyo |
| --- | ---: | ---: | --- |
| `figuras/` (`.svg`) | 370 | 349 | 21 |
| `figuras-fuente/` (`.py`) | 350 | 347 scripts de figura | 3 módulos |

- Los **349 bloques `:::figura`** de los 459 conceptos citan **349 figuras distintas**: cada bloque
  tiene una línea `fichero:` y las 349 resuelven a un SVG de `figuras/` (0 ausencias). Ningún bloque
  repite figura.
- Esos 349 bloques apuntan con su línea `fuente:` a **347 scripts distintos**: dos scripts generan
  dos figuras cada uno (`autocorrelacion-acf-pacf-1.py` produce `acf-decaimiento-lento` y
  `acf-pacf-de-un-ar1`; `series-temporales-componentes-1.py` produce
  `series-temporales-tendencia-y-patron` y `series-temporales-aditiva-y-multiplicativa`). Las 347
  fuentes resuelven a un `.py` de `figuras-fuente/` (0 ausencias).
- 370 = 349 figuras en uso + 21 sin bloque. 350 = 347 scripts de figura + 3 módulos.
- Comprobación: `370 - 349 = 21` y `350 - 347 = 3`; el listado completo está en las secciones 3 y 4.

## 2. Criterio: figura en uso o variante

Una figura está **en uso** si y solo si algún bloque `:::figura` de los 459 `.md` la enlaza. La vía
es siempre la misma: la línea `fichero: <nombre>` del bloque se lee como `figuras/<nombre>.svg`.

```
:::figura
fichero: asimetria-y-curtosis-misma-media-distinta-forma
pie: Arriba, los dos primeros conjuntos estandarizados contra la campana de Gauss...
fuente: figuras/asimetria-y-curtosis-1.py
:::
```

- Si `figuras/<nombre>.svg` existe y tiene bloque → **figura en uso** (349).
- Si el SVG existe pero ningún bloque lo cita → **material de apoyo**: variante de una figura en
  uso o sonda de prueba (21).
- El criterio no depende de la fecha del fichero, del nombre ni de si el script existe: solo del
  bloque. Es el criterio con el que el temario resuelve cada figura.

## 3. Las 21 figuras sin bloque

Ningún bloque `:::figura` ni ningún texto de los 459 conceptos menciona estas 21 figuras; están en
`figuras/` y no las sirve ninguna página del temario.

### 3.1 Veinte variantes con tilde

20 de las 21 son **la misma figura que una figura en uso, pero con el nombre acentuado**: existe un
SVG gemelo sin tildes que sí tiene bloque. Los dos ficheros no son byte a byte iguales (matplotlib
sella su fecha de render en `<dc:date>` y algunas variantes cambian de geometría), pero son la misma
figura del mismo script.

| SVG sin bloque | Figura en uso con la que empareja | Script (`figuras-fuente/`) |
| --- | --- | --- |
| `apis-rest-coste-paginación` | `apis-rest-coste-paginacion` | `apis-rest-1.py` |
| `bayes-positivos-y-repetición` | `bayes-positivos-y-repeticion` | `teorema-de-bayes-1.py` |
| `consenso-mayorias-y-elección` | `consenso-mayorias-y-eleccion` | `consenso-y-replicacion-1.py` |
| `contenedores-capas-y-deducción` | `contenedores-capas-y-deduccion` | `contenedores-1.py` |
| `cpcv-caminos-y-dispersión` | `cpcv-caminos-y-dispersion` | `validacion-combinatoria-cpcv-1.py` |
| `drawdown-profundidad-y-duración` | `drawdown-profundidad-y-duracion` | `maximo-drawdown-1.py` |
| `etiquetas-techo-y-memorización` | `etiquetas-techo-y-memorizacion` | `etiquetas-y-techo-del-modelo-1.py` |
| `exportar-servir-acumulacion-y-precisión` | `exportar-servir-acumulacion-y-precision` | `exportar-y-servir-modelos-1.py` |
| `grafos-computacionales-y-autograd-grafo-y-acumulación` | `grafos-computacionales-y-autograd-grafo-y-acumulacion` | `grafos-computacionales-y-autograd-1.py` |
| `importancia-de-variables-mdi-vs-permutación` | `importancia-de-variables-mdi-vs-permutacion` | `importancia-de-variables-1.py` |
| `independencia-condicionar-cambia-la-relación` | `independencia-condicionar-cambia-la-relacion` | `independencia-y-condicionamiento-1.py` |
| `mql5-repintado-barra-en-formación` | `mql5-repintado-barra-en-formacion` | `mql5-y-metatrader-1.py` |
| `observabilidad-que-mirar-en-producción` | `observabilidad-que-mirar-en-produccion` | `observabilidad-de-llms-1.py` |
| `pca-varianza-y-proyección` | `pca-varianza-y-proyeccion` | `pca-1.py` |
| `pipelines-de-ml-fuga-segun-transformación` | `pipelines-de-ml-fuga-segun-transformacion` | `pipelines-de-ml-1.py` |
| `posicion-riesgo-fijo-y-correlación` | `posicion-riesgo-fijo-y-correlacion` | `tamano-de-posicion-1.py` |
| `producto-punto-coseno-y-proyección` | `producto-punto-coseno-y-proyeccion` | `producto-punto-y-similitud-1.py` |
| `series-jerarquicas-niveles-y-reconciliación` | `series-jerarquicas-niveles-y-reconciliacion` | `series-jerarquicas-1.py` |
| `sesgo-varianza-diana-y-descomposición` | `sesgo-varianza-diana-y-descomposicion` | `sesgo-varianza-mse-1.py` |
| `verosimilitud-maximo-e-información` | `verosimilitud-maximo-e-informacion` | `maxima-verosimilitud-1.py` |

Qué se ha medido sobre las 20:

- Su gemela sin tildes tiene bloque `:::figura` y es la que resuelve el temario.
- El script que cita el bloque llama a `guardar()` con el nombre **con** tilde: la versión acentuada
  es la que produce hoy el script. Las 20 acentuadas se renderizaron el **2026-10-17**
  (08:56–09:17); sus gemelas sin tilde, el **2026-10-14 y 2026-10-15**. Los bloques `:::figura` de
  los conceptos siguen enlazando la versión sin tilde: es la que resuelve el temario.
- Por eso son **variantes**: una segunda versión con el nombre acentuado, generada después, que
  ningún bloque enlaza. Se conservan para poder comparar y para no perder la salida de los scripts.

### 3.2 La sonda de prueba: `_probe_escalado.svg`

La vigesimoprimera no es una variante: es una **sonda de prueba**.

- Nombre con guion bajo inicial y sin concepto: `_probe_escalado.svg`; no tiene bloque
  `:::figura`, no se menciona en ningún `.md` y **ningún script de `figuras-fuente/` la genera**
  (los 347 scripts de figura se cuentan en la sección 1 y ninguno llama a `guardar()` con ese
  nombre).
- Es un SVG de matplotlib con fecha de render `2026-10-14T16:51:29` y 21 KB. Sus rótulos hablan de
  valores y unidades, no de un concepto: «valor original», «el problema no es el valor, es la
  unidad», «los cinco valores de siempre», «Los mismos seis datos en las cuatro filas». Es una
  prueba de escalado/legibilidad del exportador, no una figura del temario.
- `INVENTARIO.md` (fuera de esta carpeta) la registra como la única figura que la viva tiene de más
  frente al archivo de Orca: «SVG servidos | 370 | 369 | +1 en la viva (`_probe_escalado.svg`)».
  Encaja: 369 figuras del archivo + 1 sonda = 370.

## 4. Los 3 `.py` que no son figuras

De los 350 `.py` de `figuras-fuente/`, 347 son scripts de figura (cada uno dibuja una o dos
figuras) y estos 3 son módulos de apoyo: no dibujan nada por sí solos y no tienen bloque.

| Módulo | Líneas | Qué es | Evidencia |
| --- | ---: | --- | --- |
| `comun.py` | 141 | **Base común de todos los scripts.** Fija el estilo (tamaño, rejilla, colores como centinelas que el portal sustituye por variables CSS para tema claro/oscuro), pone la coma decimal en los ejes y ofrece `guardar()`, `titulo()` y `anotar()`. `guardar()` escribe el SVG en `web/figuras/` y, si se pide con `FIGURAS_PNG`, también un PNG para revisar a ojo. | Los **347/347 scripts de figura** hacen `from comun import *`; ninguno dibuja sin él. |
| `_medir.py` | 182 | **Herramienta de control de calidad de figuras.** Ejecuta el script de una figura interceptando `savefig()`, mide la caja de cada texto ya renderizado y avisa de `SOLAPE` (dos textos se cruzan), `FUERA` (texto fuera del lienzo) e `INVADE` (un texto invade el panel de otro eje), además de líneas y barras que atraviesan un texto. Uso: `python figuras/_medir.py figuras/<figura>.py`. | Se usa a mano sobre una figura; no genera ningún SVG. |
| `_tanteo.py` | 55 | **Cuaderno de tanteo.** Ayudante temporal para imprimir números antes de fijar una figura: ajusta una beta por regresión, calcula media y desviación de un spread, cuenta días con la z fuera de ±1,5 en la segunda mitad y simula una estrategia con y sin stop, con coste. No dibuja: imprime resultados para decidir qué figura merece la pena. | Solo imprime por pantalla; nombre `_tanteo` («probar números a ojo»). |

Los dos primeros llevan guion bajo inicial (`_medir`, `_tanteo`), la marca de herramienta interna;
`comun.py` es el módulo importado por todos los scripts. Ninguno de los 349 bloques los cita como
`fuente:`.

## 5. Decisión: se conservan (nivel 2, reversible)

**Se conservan las 370 figuras y los 350 scripts. No se borra nada en `figuras/` ni en
`figuras-fuente/`.** Es una decisión de **nivel 2** y **reversible**: en esta carpeta no se borra
ningún fichero; si alguna vez se quitara una variante, se puede volver a generar ejecutando su
script y compararla con la que enlaza el bloque.

Motivos:

- **Las 20 variantes son salida real de los scripts**, no basura de un rename: el script que cita el
  bloque produce hoy el nombre con tilde. Borrarlas dejaría el directorio sin la salida actual de
  esos 20 scripts y sin término de comparación con lo que sirve el portal.
- **Los 3 módulos son la base de los scripts.** `comun.py` lo importan los 347 scripts de figura:
  sin él no se regenera ninguna figura. `_medir.py` y `_tanteo.py` son las herramientas con las que
  se comprobó que las figuras no se solapan y con las que se eligieron los datos; son parte de cómo
  se hizo el temario.
- **La sonda es evidencia**, no contenido: documenta la prueba de escalado y explica el único SVG
  que la viva tiene de más frente al archivo de Orca. Borrarla dejaría ese +1 sin explicación.
- **Esta carpeta es un archivo de solo lectura** del portal: se conserva lo que hay, y lo que se
  decide (no borrar) se anota. El coste de conservar es 24 ficheros de apoyo (21 SVG + 3 módulos);
  el coste de borrar es perder trazabilidad.

Criterio para una futura limpieza, si alguna vez se plantea: **una figura solo se puede retirar
cuando ningún bloque `:::figura` la cite** (hoy: las 21), y **un módulo, solo cuando ningún script
lo importe o lo invoque**. Mientras el criterio de uso sea el bloque, este documento es la lista
completa de lo que sobra de la cuenta 349 + 21 = 370 y 347 + 3 = 350.
