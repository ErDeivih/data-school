# Especificación — Data School

Estado: **borrador para revisar**. Proyecto nuevo, sin material previo en el disco: se construye desde cero.

## Objetivo

Una **academia de datos**: el sitio donde David aprende a ser *data engineer*, *data scientist* y *AI engineer*, con las tres rutas en una sola casa y los mejores recursos que existen en internet, ordenados y verificados.

No es un curso. Es **el índice maestro**: qué aprender, en qué orden, con qué recurso, con qué dataset y con qué proyecto para demostrarlo.

## Qué significa «todo en uno»

El producto tiene cinco piezas, y todas cuelgan del mismo modelo de datos:

1. **Rutas** — itinerarios por perfil: data engineer, data scientist, AI engineer. Y los puntos donde se cruzan.
2. **Recursos** — cursos, documentación, vídeos, libros, artículos, repositorios. **Enlazados, no copiados** (ver riesgos).
3. **Proyectos** — qué construir para demostrar cada tramo, con su enunciado, sus criterios de terminado y su nivel.
4. **Datasets** — conjuntos de datos reales, con su licencia, su tamaño y para qué sirven.
5. **Progreso y apuntes** — qué está estudiado, qué está practicado, qué está demostrado con un proyecto.

**La regla de oro**: un recurso sin licencia clara no entra; un temario ajeno no se copia, se enlaza y se resume con criterio propio.

## Familia y recetas

Familias **F (documentación)** para el catálogo, **A (panel)** para el progreso y **B (SaaS)** para rutas e itinerarios. Ver `F:\Inforepositorios\indice\RECETAS-UI.md`.

Para el diseño visual: existen ya las skills `claude-design`, `claude-design-system` y `claude-dashboard` instaladas en DSH. **Hay que crear el sistema de diseño antes de la primera pantalla**, no después.

## Pantallas de esta tanda

### 1. Portada
- [ ] Las tres rutas presentadas en una línea cada una
- [ ] Qué toca hoy: el siguiente paso pendiente
- [ ] Estado vacío: «todavía no has elegido ruta»

### 2. Lista de rutas
- [ ] Las tres rutas con su duración estimada y su nivel de entrada
- [ ] Qué comparten y en qué se separan

### 3. Ficha de ruta (itinerario)
- [ ] Tramos ordenados, con sus recursos y sus proyectos
- [ ] Marca de lo completado
- [ ] Qué requisito tiene cada tramo

### 4. Ficha de recurso
- [ ] Tipo, idioma, duración, coste, licencia
- [ ] A qué tramo sirve
- [ ] **Enlace original** y fecha en que se comprobó que sigue vivo
- [ ] Estado vacío para recurso caído: marcar, no ocultar

### 5. Catálogo de proyectos
- [ ] Enunciado, nivel y criterios de terminado
- [ ] Qué demuestra y a qué tramo pertenece

### 6. Catálogo de datasets
- [ ] Licencia, tamaño, dominio y dificultad
- [ ] Para qué proyecto sirve

### 7. Mi progreso
- [ ] Por ruta, por tramo y total
- [ ] Qué está pendiente y qué está demostrado

## Estados obligatorios

- [ ] Vacío · [ ] Cargando · [ ] Error · [ ] Sin permiso · [ ] **Enlace caído** (propio de este producto)

## Decisiones que hay que tomar antes de construir

| Decisión | Por qué manda | Estado |
|---|---|---|
| ¿Tres rutas separadas o una sola con tres salidas? | decide el modelo entero | **pendiente** |
| ¿El progreso es por recurso, por tramo o por proyecto? | decide la pantalla de progreso | **pendiente** |
| ¿Los apuntes son texto propio dentro de la plataforma, o enlaces a un cuaderno externo? | decide si hay editor | **pendiente** |
| ¿Los datasets se enlazan o se descargan a un almacén local? | decide coste de disco y de mantenimiento | **pendiente** |
| ¿El catálogo es privado o público? | decide si hay cuentas | **pendiente** |

## Fuentes candidatas — **el agente debe verificarlas una a una antes de darlas por buenas**

Ninguna de estas está comprobada todavía. Todas entran como **candidatas**, y cada una necesita: licencia, si el contenido es gratis o de pago, idioma, y si sigue viva.

- **Itinerarios**: roadmap.sh, DataTalksClub (DE Zoomcamp), MIT OCW, freeCodeCamp, Kaggle Learn, dbt Learn, Google Cloud Skills Boost.
- **Cursos y vídeos**: Coursera, edX, DeepLearning.AI, fast.ai, YouTube (canales técnicos).
- **Libros y documentación**: documentación oficial de las herramientas (Python, SQL, dbt, Spark, Airflow, DuckDB) y libros abiertos.
- **Datasets**: Kaggle, Hugging Face Datasets, data.gov, datos.gob.es, UCI ML Repository, IMDb/otros dominios de práctica.
- **Papers**: arXiv, Papers with Code.

El agente **no puede copiar el temario de un curso**: enlaza, resume con sus palabras y acredita la fuente.

## Riesgos

- **Derechos de autor.** Enlazar y resumir está bien; copiar temarios, vídeos o PDFs ajenos, no. Un recurso de pago solo se enlaza.
- **Enlaces que mueren.** Hace falta un comprobador de enlaces y una fecha de última comprobación por recurso. Sin eso, el catálogo se pudre en meses.
- **Anuncios de «aprende IA en 3 meses».** El criterio de calidad no son las vistas: es si el recurso enseña y si se puede verificar.
- **Sobreabundancia.** Cien recursos por tramo paralizan. La regla: **un principal y dos alternativas por tramo**, no veinte.

## Puertas antes de dar una pantalla por buena

1. Pruebas en verde.
2. Comprobador de enlaces ejecutado: 0 enlaces caídos sin marcar.
3. `ai-design-check` o la lista de diez de las recetas.
4. Ojos frescos con este fichero y una captura.

## Primera tarea

**Investigar y verificar fuentes.** Antes de escribir una sola pantalla: comprobar las candidatas de arriba, descartar las muertas o de pago sin avisar, y escribir `FUENTES.md` con licencia, idioma, coste y estado de cada una. Solo después se decide el modelo de datos.
