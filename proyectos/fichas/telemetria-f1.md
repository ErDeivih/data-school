# Ficha · telemetria-f1 — ritmo, compuesto y parada en tres carreras

**Estado:** ficha de enunciado. No hay implementación de este proyecto en la carpeta: aquí se fija
qué construir, con qué datos del catálogo y cómo se demuestra que está terminado. Las fichas
hermanas son [cartera-acciones](cartera-acciones.md), [f1-clasificacion](f1-clasificacion.md) y
[futbol-partidos](futbol-partidos.md).

## Datos asignados

- **CSV:** [`datasets/csv/telemetria-f1.csv`](../../datasets/csv/telemetria-f1.csv) — **180 filas** y
  **10 columnas**; sintético, semilla fija y licencia CC0-1.0. Tamaño y checksum en
  [`datasets/CATALOGO.md`](../../datasets/CATALOGO.md).
- **Catálogo de proyectos:** [`proyectos/CATALOGO.md`](../CATALOGO.md) — cubre los proyectos P11, P12
  y P13.
- **Ficha del dataset:** [`datasets/FICHAS.md`](../../datasets/FICHAS.md) — procedencia, checksum y
  preguntas que permite responder.
- **Columnas:** `carrera`, `piloto`, `vuelta`, `compuesto`, `edad_neumatico`, `sector1_s`,
  `sector2_s`, `sector3_s`, `tiempo_vuelta_s`, `parada`.

## Proyectos del catálogo que cubre

| ID | Título del catálogo | Nivel |
| --- | --- | --- |
| P11 | Limpiar y unir la telemetria de una carrera | intermedio |
| P12 | Un panel de carrera con una sola pregunta | intermedio |
| P13 | ¿Le costo la carrera la parada? | intermedio |

## Nivel y rutas

- **P11 y P12:** intermedio, ruta **DE** (data engineering). P11 es la base de datos limpia; P12 es
  la capa de presentación sobre esa base.
- **P13:** intermedio, ruta **DS** (data science). Es el análisis del efecto de la parada, y depende
  de que P11 haya dejado el ritmo bien separado.
- **Requisitos previos:** Python (o SQL + pandas), lectura de CSV, agregación por grupos y
  estadística descriptiva básica. No hace falta ninguna librería de F1.

## Tiempo estimado

| Proyecto | Horas |
| --- | --- |
| P11 | 6–8 h |
| P12 | 5–7 h |
| P13 | 8–10 h |

Total de la ficha: **19–25 h**. Si se hacen los tres seguidos, P11 se reutiliza entero en P12 y P13.

## Enunciado

El CSV contiene tres carreras sintéticas (Baréin, Monza y Suzuka) con dos pilotos, A y B, y treinta
vueltas por piloto y carrera. Construye un pipeline que deje una tabla de vueltas limpia y
comparable, con el **tramo de neumático** y la **vuelta de parada** explícitos, y encima de ella tres
piezas: un panel de una sola pregunta (P12), un análisis del coste de la parada (P13) y la propia
tabla limpia con su informe de recuentos (P11).

El objetivo no es «cargar el CSV»: es demostrar que un ritmo medio mal calculado se puede fabricar
sin querer incluyendo la vuelta de parada, mezclando compuesto con tramo o ignorando la edad del
neumático. Cada cifra del resultado debe poder reproducirse desde el CSV con un comando.

## Datos y preparación

- **Estructura:** 3 carreras × 2 pilotos × 30 vueltas = 180 filas. La clave natural es
  `(carrera, piloto, vuelta)`; no hay nulos ni claves repetidas en el fichero, pero el pipeline debe
  **comprobarlo** y fallar si deja de ser cierto, no suponerlo.
- **Compuesto:** el primer tramo va con `medio` y el segundo con `duro`. El compuesto cambia en la
  misma vuelta de parada; `edad_neumatico` vuelve a 1 en la vuelta siguiente. Esa coincidencia hace
  que compuesto, tramo y fase de carrera estén confundidos: no se pueden separar del todo con este
  CSV.
- **Parada:** hay exactamente una parada por piloto y carrera. A para en la vuelta 18 y B en la 22, en
  las tres carreras. `parada = 1` marca la **vuelta de entrada a boxes**: su tiempo ronda los 115 s
  frente a los ~92 s de una vuelta verde. Incluirla en una media de ritmo desplaza el resultado más
  de 20 s, que es el error que este proyecto existe para evitar.
- **Sectores:** `sector1_s + sector2_s + sector3_s` reconstruye `tiempo_vuelta_s` salvo milésimas.
  No son tres predictores independientes del tiempo: son un desglose del mismo dato. Úsalos para
  diagnosticar dónde se pierde tiempo, no como features de un modelo de ritmo.
- **Fuera del CSV:** no hay combustible, tráfico, safety cars, temperatura ni coches rivales. La
  degradación real del neumático no se puede aislar; como mucho, describir la evolución del ritmo
  dentro del tramo declarando esa limitación.
- **Muestras pequeñas:** 3 carreras, 2 pilotos, 6 pares carrera–piloto y 12 stints. Cualquier
  diferencia entre A y B se declara con su incertidumbre y con el aviso de que no generaliza a una
  temporada.

## Pasos

1. **Cargar y tipar (P11).** Leer el CSV, convertir tiempos y vueltas a numérico, comprobar 180 filas,
   10 columnas y clave `(carrera, piloto, vuelta)` única. Escribir una tabla base sin transformar.
2. **Reconstruir tramos (P11).** Derivar `stint` (1/2) por piloto y carrera, verificar que la edad del
   neumático crece 1 a 1 dentro del tramo y que el compuesto no cambia sin parada.
3. **Etiquetar la parada (P11).** Marcar como no comparables las vueltas con `parada = 1`; documentar
   el desvío de su tiempo respecto a la mediana de vueltas verdes del mismo tramo.
4. **Calcular ritmo (P11).** Por compuesto, tramo y piloto: mediana o media recortada, n por celda y
   dispersión. Comparar A y B solo dentro del mismo compuesto y tramo, y anotar el confusor.
5. **Panel de una pregunta (P12).** Elegir una sola pregunta respondible con esta tabla (por ejemplo,
   cuánto cuesta la parada o cómo evoluciona el ritmo por tramo), agregar por stint y publicar un HTML
   estático con la fuente, el filtro aplicado y el límite del dato.
6. **Efecto de la parada (P13).** Definir una medida del coste (pérdida en la vuelta de parada y
   diferencia de ritmo antes/después), estimarla por piloto y carrera, y calcular un intervalo de
   confianza por bootstrap agrupando por carrera.
7. **Verificar y documentar.** Un `verificar.py` con comprobaciones de filas, claves, edades y
   recuentos; `README.md` con los comandos y los números; reejecutar y comprobar que los resultados
   no cambian.

## Criterios de terminado

- [ ] `verificar.py` comprueba 180 filas, 10 columnas, 6 pares `(carrera, piloto)` y 30 vueltas por
      par; devuelve código 0 si todo cuadra y distinto de 0 si falta o sobra una vuelta.
- [ ] La tabla de trabajo tiene `stint` y una marca de vuelta de parada; ninguna fila con
      `parada = 1` entra en un cálculo de ritmo, y el informe muestra su tiempo aparte.
- [ ] El ritmo por compuesto se publica con n por celda y con la edad del neumático controlada
      (estratificada o como covariable), no como una media simple de todas las vueltas.
- [ ] La comparación A–B está restringida al mismo compuesto y tramo, y el README dice por qué no se
      puede separar compuesto de fase de carrera con estos datos.
- [ ] El panel de P12 responde a **una** pregunta, cita el CSV y el filtro usados, muestra el tamaño
      de muestra y se abre en el navegador sin servidor.
- [ ] P13 publica una estimación del coste de la parada con intervalo (bootstrap por carrera) y
      concluye explícitamente si la diferencia observada puede ser ruido.
- [ ] `README.md` permite reproducir todo con comandos copiables; reejecutar produce los mismos
      ficheros de resultados (o un `diff` vacío).

## Entregables

- Código de la cadena: `cargar.py` (o SQL), `preparar.py`, `analisis.py`, `verificar.py`.
- `data/vueltas-limpio.csv` con una fila por vuelta y las columnas derivadas (`stint`,
  `vuelta_parada`, `vuelta_comparable`).
- Resultados en `resultados/`: tabla de ritmo por compuesto y tramo, tabla del coste de parada y su
  intervalo.
- Panel de P12: `panel.html` autocontenido, con la fuente y el límite visibles.
- `README.md` con comandos, recuentos y la lista de límites del CSV.
- Registro de comprobaciones (salida de `verificar.py`) guardado junto a los resultados.

## Qué demuestra y cómo se evalúa

Demuestra que sabes convertir telemetría bruta en una comparación de ritmo defendible: separar
tramos, aislar la vuelta de parada, controlar la edad del neumático y no confundir compuesto con
fase de carrera. También demuestra criterio de comunicación: una pregunta, un panel, una fuente.

| Criterio | Peso |
| --- | --- |
| Datos y preparación: estructura, claves, tipos y auditoría de nulos/duplicados | 20 % |
| Separación de stints y paradas; exclusión razonada de la vuelta de parada | 20 % |
| Análisis de ritmo con n y control de edad del neumático y compuesto | 25 % |
| Verificación reproducible (recuentos, clave, reejecución) | 20 % |
| Informe, panel y límites declarados sin sobreafirmar causalidad | 15 % |

## Riesgos típicos

- **Fuga por la vuelta de parada:** incluir `parada = 1` en la media de ritmo. El resultado sale
  peor de lo que es y nadie lo nota si no se revisa el n por celda.
- **Confusor compuesto–tramo:** comparar «medio» contra «duro» cuando en realidad se compara el
  primer tramo contra el segundo (y el coche va más ligero después). No es un efecto del neumático.
- **Denominadores:** promediar vueltas sin decir cuántas hay por celda; una celda con 8 vueltas y
  otra con 21 no pesan igual.
- **Duplicados y nulos silenciosos:** el CSV actual no los tiene, pero un `groupby` que los ignore
  convierte una comprobación fallida en un resultado aparentemente válido.
- **Muestra mínima:** 3 carreras y 2 pilotos no permiten afirmar nada sobre pilotos ni circuitos.
- **Sectores como features:** usarlos para «predecir» el tiempo de vuelta es una tautología
  aritmética, no un modelo.
