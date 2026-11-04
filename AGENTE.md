# Ficha del agente — Data School

**Id en el panel**: `data-school`
**Ruta**: `F:\Proyectos\data-school`
**Rama de trabajo**: `main`
**Familia de interfaz**: F (documentación) + A (panel) + B (SaaS) — ver `F:\Inforepositorios\indice\RECETAS-UI.md`

## Misión

Una academia de datos: **data engineer**, **data scientist** y **AI engineer** en una sola casa, con los mejores recursos de internet ordenados, verificados y atados a proyectos y datasets reales.

La regla de oro: **se enlaza y se resume, no se copia**. Copiar temarios ajenos es un problema de derechos y además convierte el producto en una copia peor.

## Cómo trabajas

Lee y sigue `F:\EspacioCodigo\_flujo-dsh\PROTOCOLO-AUTONOMIA.md`.

- **Nivel 1**: decide solo (refactor, pruebas, docs, accesibilidad).
- **Nivel 2**: decide solo y lo anotas en `DECISIONES.md` (pantallas ya especificadas, dependencias pequeñas, esquema reversible).
- **Nivel 3**: paras y preguntas (alcance, datos, credenciales, dinero, otro proyecto, ramas).
- **Una tarea bloqueada no para la sesión**: la marcas y sigues con la siguiente.

Antes de escribir código, lee `ESPECIFICACION.md`. **Tu primera tarea está escrita allí y no es código.**

## Tu backlog

Vive en `BACKLOG.md`. Nunca puede tener menos de 5 tareas listas. Si baja, las generas de:

1. **Huecos de la especificación**: pantallas prometidas sin hacer, estados sin cubrir, decisiones pendientes.
2. **Calidad del catálogo**: enlaces caídos, recursos sin licencia, tramos sin proyecto, datasets sin criterio de uso.
3. **Competencia**: cómo organizan su catálogo las academias y plataformas del sector.

## Investigación encomendada

Antes de construir: **verificar cada fuente candidata** de la especificación. Para cada una, licencia, idioma, coste y si sigue viva. Se deja en `FUENTES.md` con fecha de comprobación.

Y en paralelo, una investigación de producto: cómo presentan su catálogo roadmap.sh, DataTalksClub, Kaggle Learn y las academias del sector. Qué hacen bien y qué se puede adoptar.

## Primera tarea

**Investigar y verificar fuentes** y escribir `FUENTES.md`. Sin eso no se decide el modelo de datos ni se escribe una pantalla.

## Diseño

Hay skills instaladas en DSH para esto: `claude-design-system` (crear el sistema de diseño), `claude-design` (artboards) y `claude-dashboard` (paneles con datos). **El sistema de diseño se crea antes de la primera pantalla.**

## Al terminar cada sesión

Deja `ESTADO-AGENTE.md` actualizado con este formato exacto. De ahí lo lee el panel:

```
titulo: Data School — academia de datos
estado: en-curso
tarea: lo que estabas haciendo
nivel: 1 | 2 | 3
siguiente: lo próximo que harás
bloqueado: la pregunta de nivel 3, si la hay
fecha: AAAA-MM-DD
```

Y recuerda: **sin commit y sin push, no está terminado.**
