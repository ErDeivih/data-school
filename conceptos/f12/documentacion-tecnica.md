---
id: documentacion-tecnica
titulo: Documentación técnica
fase: 12
nivel: intermedio
rutas: [core]
prerequisitos: [escribir-un-informe]
tags: [comunicacion, documentacion, mantenimiento, decisiones]
resumen: Documentación que no miente: un README que arranca el proyecto en un comando, decisiones registradas con su contexto y docstrings que respetan la firma.
fuentes: ["Nygard (2011), 'Documenting Architecture Decisions'", "Hunt y Thomas (1999), 'The Pragmatic Programmer'"]
---

## En una frase

La documentación técnica es todo lo que otra persona necesita para usar, cambiar o repetir tu
trabajo sin preguntarte, y solo vale mientras siga siendo cierta: una guía desactualizada es
peor que no tener ninguna, porque hace perder el tiempo con confianza.

## La idea

Hay tres tipos de documento y cada uno responde a una pregunta distinta. Confundirlos es la
razón de que casi nadie encuentre lo que busca:

1. **La guía de arranque (README).** Responde «¿qué es esto y cómo lo pongo en marcha?». Se lee
   una vez, al principio, y tiene que funcionar a la primera en una máquina limpia.
2. **La referencia.** Responde «¿qué hace exactamente esta función, con qué argumentos y qué
   devuelve?». Son los docstrings y la documentación de la API. Se consulta a trozos, mientras
   se programa.
3. **El registro de decisiones (ADR).** Responde «¿por qué está hecho así y no de la otra
   forma?». Esto no se puede deducir leyendo el código: el código dice lo que haces, no las
   alternativas que descartaste ni el motivo.

El README es la portada del proyecto y se juega en las primeras líneas. En una frase tiene que
decir qué problema resuelve; después, cómo se ejecuta (idealmente un comando, con su gestión de
dependencias descrita), un ejemplo mínimo de entrada y salida, de dónde salen los datos y con
qué licencia. Si alguien tiene que leer el código para saber cómo lanzarlo, el README no está
terminado. Y si el proyecto es un análisis, el README debe incluir el orden en que se ejecutan
los pasos y la semilla con la que se generan los resultados.

El **ADR** es la pieza que casi nadie escribe y la que más se agradece a los seis meses. Es un
fichero corto, numerado y con fecha, que no se edita nunca: si cambias de opinión, escribes otro
que sustituye al anterior y lo enlazas. Su estructura es siempre la misma: contexto (qué
problema teníamos y qué restricciones), decisión (qué se eligió, en una frase), consecuencias
(qué se gana, qué se pierde y qué queda pendiente). Así, dentro de un año, cuando alguien
pregunte «¿por qué guardamos esto en Parquet en vez de CSV?», la respuesta está escrita por
quien lo decidió, con el contexto de entonces, en lugar de inventada por quien lo lee ahora.

Los **docstrings** son un contrato, no un adorno. Un docstring útil dice qué hace la función,
qué recibe (tipos, unidades y qué valores no admite), qué devuelve, qué excepciones lanza y qué
efectos secundarios tiene (escribir un fichero, modificar un argumento). Lo que no aporta nada es
repetir el nombre: `# calcula la media movil` debajo de `def media_movil` no documenta nada. Y
sobre todo: la documentación vive junto al código, en el mismo repositorio y en el mismo cambio.
Una guía en un wiki que nadie actualiza se convierte en una trampa en semanas.

## Definición formal

Cada documento tiene una estructura mínima, y el criterio para saber si sirve es siempre el
mismo: **¿puede alguien hacer la tarea sin preguntarte?**

```
README   = propósito · requisitos · instalación · ejemplo mínimo · datos · licencia
ADR      = número · fecha · estado · contexto · decisión · consecuencias
docstring = resumen · parámetros (tipo y unidades) · retorno · errores · efectos
```

El docstring se puede comprobar de forma automática, porque su parte de parámetros tiene que
coincidir con la firma real de la función:

:::formula
sin_documentar = parámetros(firma) − parámetros(docstring)
:::

Si ese conjunto no está vacío, hay un argumento que el código acepta y que nadie ha explicado:
exactamente el sitio por donde entra el error de quien lo usa. Y si el conjunto va al revés
(parámetros en el docstring que ya no existen en la firma), la documentación está mintiendo.

## Ejemplo

Esta es la función y su docstring, y debajo la comprobación automática:

```python ilustrativo
def media_movil(serie, ventana):
    """Media movil simple.

    Args:
        serie: valores en orden temporal.
        ventana: numero de puntos que entran en cada media.

    Returns:
        Lista de medias; su longitud es len(serie) - ventana + 1.
    """
```

- Firma real: `serie`, `ventana`.
- Documentados: `serie`, `ventana`.
- Sin documentar: (ninguno) → la comprobación pasa.
- Resultado de `media_movil([1, 2, 3, 4], 2)`: `[1.5, 2.5, 3.5]`, cuatro valores de entrada y
  tres de salida: cada media necesita dos valores, así que la primera posición no tiene ventana
  completa y se pierde un punto. En general se pierden `ventana − 1` valores.

Ahora supón que alguien añade un argumento `rellenar=False` para que, en lugar de acortar la
lista, rellene con nulos al principio. La firma pasa a tener tres parámetros y el docstring sigue
explicando dos: la comprobación devuelve `['rellenar']` y ese test falla. Con el test en la
integración continua, el cambio no se puede fusionar sin documentar el argumento nuevo
([[ci-cd]]). Eso es documentación que no miente: no depende de la memoria de nadie.

## Código

```python verificable
import inspect

def media_movil(serie, ventana):
    """Media movil simple.

    Args:
        serie: valores en orden temporal.
        ventana: numero de puntos que entran en cada media.

    Returns:
        Lista de medias; su longitud es len(serie) - ventana + 1.
    """
    return [sum(serie[i:i + ventana]) / ventana for i in range(len(serie) - ventana + 1)]

# La documentacion miente cuando alguien anade un argumento y no toca el docstring.
# Esta comprobacion cabe en un test y detecta justo eso.
firma = set(inspect.signature(media_movil).parameters)
documentados = {linea.strip().split(":")[0] for linea in inspect.getdoc(media_movil).splitlines()
                if linea.startswith("    ") and ":" in linea}

print("firma:        ", sorted(firma))
# -> firma:         ['serie', 'ventana']
print("docstring:    ", sorted(documentados))
# -> docstring:     ['serie', 'ventana']
print("sin documentar:", sorted(firma - documentados))
# -> sin documentar: []
print("resultado media_movil([1, 2, 3, 4], 2):", media_movil([1, 2, 3, 4], 2))
# -> resultado media_movil([1, 2, 3, 4], 2): [1.5, 2.5, 3.5]
```

```text
# README.md

# Ventas-ETL

Carga los pedidos diarios del ERP en la capa de plata y publica la tabla
`ventas_diarias` para el equipo comercial. Sustituye al script manual de 2023.

## Requisitos
Python 3.12. Los paquetes estan en requirements.txt.

## Puesta en marcha
    python -m venv .venv
    .venv/Scripts/pip install -r requirements.txt
    python -m ventas_etl --fecha 2024-05-07 --destino local

## Ejemplo
Entrada: data/raw/pedidos_2024-05-07.csv (12.418 filas)
Salida:  data/plata/ventas_diarias.parquet (12.402 filas, 16 descartadas
         por pedido duplicado y fecha nula)

## Datos y licencia
Los datos de ejemplo son sinteticos. Licencia MIT.
```

```text
# docs/adr/007-parquet-en-plata.md

# 007. Guardar la capa de plata en Parquet

- Fecha: 2024-05-08
- Estado: aceptada (sustituye a la 003, que proponia CSV comprimido)

## Contexto
La capa de plata se lee 30 veces al dia desde tres equipos y pesa 40 GB al mes
con los ficheros de un ano. En CSV, cada consulta lee las 20 columnas aunque
solo necesite dos.

## Decisión
Escribir la capa de plata en Parquet, particionada por mes, con Zstd.

## Consecuencias
- Se lee solo las columnas necesarias y la lectura baja de minutos a segundos.
- El fichero no se puede abrir con Excel ni editar a mano: quien depure tendra
  que usar DuckDB o Pandas (documentado en el README).
- Pendiente: fijar la politica de compactacion de ficheros pequenos.
```

## Errores típicos

- **Un README que empieza por la arquitectura.** La primera línea tiene que decir qué hace el
  proyecto y cómo se ejecuta; el diagrama de componentes va después, para quien ya lo ha hecho
  funcionar. Si la puesta en marcha no cabe en tres comandos, algo del proyecto está mal, no de
  la documentación.
- **Docstrings que repiten el nombre.** `# devuelve la media movil` debajo de `def media_movil`
  no informa de nada. Lo que se necesita saber es la unidad de la ventana, si admite nulos y
  qué pasa cuando la serie es más corta que la ventana.
- **Documentar el qué en lugar del por qué.** El código ya dice qué hace; lo que no dice es por
  qué se descartó la otra opción. Eso es exactamente lo que va en un ADR ([[refactorizacion]]).
- **Duplicar la documentación en tres sitios.** El mismo texto en el README, en el wiki y en un
  comentario del código se desincroniza en la primera semana. Una sola fuente, cerca del código
  y versionada con él ([[git-para-datos]]).
- **Ejemplos que ya no funcionan.** Un ejemplo copiable que falla destruye la confianza en todo
  el documento. Si puedes, convierte los ejemplos del README en pruebas que se ejecutan
  ([[testing-con-pytest]]).
- **Dejar la documentación para el final.** Nunca llega. La decisión se documenta cuando se
  toma, porque es cuando recuerdas las alternativas; el README se actualiza en el mismo cambio
  que introduce la funcionalidad.

:::aviso
La documentación generada a partir del código (listas de funciones, firmas, esquemas) es útil
como referencia, pero no sustituye a la explicación escrita por una persona: nadie ha decidido
nunca nada importante por leer una lista de parámetros. Genera lo mecánico y escribe a mano lo
que explica el porqué.
:::

:::practica
enunciado: Un compañero se va de vacaciones y su pipeline falla. Encuentras un fichero `etl.py` de 600 líneas sin docstrings, un README de tres párrafos que habla de la arquitectura y una carpeta `notas/` con un documento de 2022. ¿Qué escribes primero y qué dejas para después?
pista: Piensa en qué te habría permitido resolver la incidencia sin depender de tu compañero, y en qué se puede comprobar automáticamente.
solucion: Primero, el README con la puesta en marcha y el orden de ejecución, porque es lo que desbloquea la incidencia hoy, y un ADR corto con lo que averigües del diseño mientras lo arreglas. Después, docstrings en las funciones que has tenido que leer para entenderlo (entradas, unidades, errores y efectos), empezando por las que tocan datos. Al final, la referencia exhaustiva y el documento viejo de 2022: mejor borrarlo o marcarlo como histórico que dejarlo ahí pareciendo vigente. Lo que no debe esperar es el registro de la decisión, porque el contexto se olvida en días.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál de estas tres cosas es un ADR?
o: La lista de funciones de un módulo con sus parámetros
o: Un fichero fechado que explica qué se decidió, con qué alternativas y qué consecuencias tiene
o: El manual de instalación del proyecto
a: 2
e: El ADR registra decisiones y su contexto: es lo único que el código no puede contar por sí solo. La lista de funciones es referencia y el manual de instalación es la guía de arranque; los tres documentos responden a preguntas distintas y no se sustituyen entre sí.
:::

:::quiz
p: Un test comprueba que `set(inspect.signature(f).parameters)` es igual al conjunto de parámetros documentados. ¿Qué error detecta?
o: Que la función devuelve un tipo equivocado
o: Que alguien ha añadido o quitado un argumento y no ha tocado el docstring
o: Que el docstring tiene faltas de ortografía
a: 2
e: La comprobación compara la firma real con lo que el docstring declara, así que salta cuando las dos listas dejan de coincidir: es el caso típico de argumento nuevo sin documentar. No dice nada del tipo devuelto (eso lo cubren los tests de comportamiento) ni de la redacción.
:::

:::quiz
p: ¿Por qué una guía desactualizada es peor que no tener guía?
o: Porque ocupa espacio en el repositorio
o: Porque quien la sigue pierde el tiempo con confianza y deja de buscar la fuente correcta
o: Porque el generador de documentación falla
a: 2
e: Sin documentación, la persona va al código o pregunta, y encontrará la verdad. Con una guía obsoleta, hace lo que dice y el fallo aparece más tarde y más lejos de la causa. La solución no es borrar toda la documentación, sino mantenerla en el mismo cambio que el código.
:::
