# Data School

Academia de datos: **data engineer**, **data scientist** y **AI engineer** en una sola casa.

Los recursos de internet se **enlazan y se resumen**, no se copian.

## Documentos

- `ESPECIFICACION.md` — qué se construye, pantallas y decisiones pendientes.
- `AGENTE.md` — misión, reglas de autonomía y primera tarea.
- `ESTADO-AGENTE.md` — estado que lee el panel de proyectos.
- `FUENTES.md` — las 32 fuentes candidatas verificadas una a una (licencia, coste, idioma, estado, tramo) y los descartes.
- `INVESTIGACION.md` — cómo presentan su catálogo seis plataformas y qué se adopta aquí.
- `BACKLOG.md` — tareas ordenadas por valor; nunca menos de cinco listas.
- `DECISIONES.md` — decisiones de nivel 2 con su motivo.
- `INFORMES/` — informes automáticos de enlaces, con fecha.

## Sistema de diseño

Vive en `designs/data-school/` y se creó **antes de la primera pantalla**:

- `project/tokens.json` — color (claro y oscuro), tipografía, espacio, forma y elevación.
- `project/README.md` — el brand book: voz, fundamentos, contraste verificado y estados `verified` / `pending` / `broken`.
- `project/components/Cover/preview.html` — la portada del sistema.

Se abre con el visor del sistema de diseño (servidor local):

```
node "C:\Users\David\.dsh\profiles\desktop\node_modules\dsh-claude-design-system\skills\claude-design-system\scripts\artifact.mjs" open "F:\Proyectos\data-school\designs\data-school"
```

## Herramientas

Node 20 o superior, **sin dependencias**:

```
npm test              # pruebas del comprobador (8)
npm run check:links   # comprueba FUENTES.md y escribe INFORMES/enlaces-AAAA-MM-DD.md
```

El comprobador clasifica los enlaces en `vivo`, `redirige`, `bloqueado`, `caído` y `error`; un sitio que rechaza bots no se declara muerto.

## Panel de proyectos

```
& F:\\EspacioCodigo\\_flujo-dsh\\Estado-Proyectos.ps1
```
