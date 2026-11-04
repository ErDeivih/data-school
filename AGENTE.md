# Ficha del agente — Data School

**Id en el panel**: `data-school`
**Ruta**: `F:\Proyectos\data-school`
**Rama de trabajo**: `main`
**Familia de interfaz**: F (documentación) + A (panel)

## Misión

**Reunir en un solo sitio todo el material de datos e IA** —conceptos, fuentes, proyectos, datasets— cogiendo lo mejor de cada origen, y dejarlo de forma que sirva para aprender y para construir.

Data School dejó de ser un producto aparte: el portal es **Muestra**. Esta carpeta es **la casa del contenido**: el catálogo que alimenta al portal y el archivo del que se tira.

## Qué hay aquí y qué se hace

| Carpeta | Qué va |
|---|---|
| `fuentes/` | catálogo de fuentes con licencia, coste, idioma y estado. **32 ya verificadas** |
| `conceptos/` | conceptos de datos e IA, con definición, ejemplo, código verificado y errores típicos |
| `proyectos/` | proyectos prácticos con enunciado, nivel y criterio de terminado |
| `datasets/` | conjuntos de datos reales con licencia y para qué sirven |
| `investigacion/` | cómo lo hacen otros, APIs gratuitas, qué adoptamos y qué no |
| `tools/` | el comprobador de enlaces (sin dependencias) |

## La tarea ya está creada: consolidar

**Medir los cinco orígenes, comparar con números e importar aquí lo que falte.** En `README.md` están los cinco:

1. `F:\Proyectos\ProyectoServidor\aprender` — el portal vivo (438 conceptos, 13 fases, datasets).
2. `...\aprender\docs\data-school-import` — la importación de Data School (32 fuentes, tools, designs).
3. `E:\orca-workspaces-archivo-2026-11-03\aprender\equipo-ia` — el archivo de Orca (13 fases, 6 CSV, figuras).
4. `C:\Users\David\orca\preview-data` — la vista previa de Orca.
5. `F:\Proyectos\data-school` — esta carpeta.

Dato ya medido en coordinación: **la versión viva va por delante** del archivo de Orca (fases más grandes) y **los 6 CSV de Orca ya están en la viva**. Hay que confirmarlo con números, no darlo por hecho.

## Reglas

- **Los orígenes son de solo lectura.** No se escribe en el portal ni en el archivo de Orca: se lee y se trae aquí.
- Hay **otra sesión trabajando en el portal (Muestra)**. Si algo hay que cambiar allí, se anota en `CONSOLIDACION.md`; no se toca.
- **Se enlaza y se resume, no se copia**: 11 de las 32 fuentes solo admiten enlace.
- Todo concepto lleva **código ejecutado**, no código de ejemplo sin probar.
- Todo dataset lleva **licencia y procedencia**.
- Sin GitHub Actions. Commit local; push selectivo.

## Cómo trabajas

Lee y sigue `F:\EspacioCodigo\_flujo-dsh\PROTOCOLO-AUTONOMIA.md` y `DOCTRINA-CALIDAD.md`.
Nivel 1 decides solo, nivel 2 anotas en `DECISIONES.md`, nivel 3 preguntas y sigues con otra tarea.

## Primera tarea

Escribir `INVENTARIO.md` con la medición de los cinco orígenes (conceptos, fases, datasets, figuras, recursos) y la comparación entre ellos. Después, `CONSOLIDACION.md` con lo que se trae, lo que se descarta y por qué.

## Al terminar cada sesión

`ESTADO-AGENTE.md` con el formato del protocolo, incluida la línea `resumen:` en lenguaje llano.
