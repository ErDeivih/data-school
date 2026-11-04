---
id: data-mesh
titulo: Data mesh
fase: 4
nivel: experto
rutas: [de]
prerequisitos: [data-lake, gobierno-y-privacidad, catalogo-y-linaje]
tags: [organizacion, dominios, gobierno, plataforma]
resumen: Los dominios poseen sus datos y los publican como producto sobre una plataforma self-service, con un gobierno federado que se aplica como código.
fuentes: ["Dehghani (2022), 'Data Mesh: Delivering Data-Driven Value at Scale'"]
---

## En una frase

Data mesh no es una tecnología sino una forma de organizarse: cada dominio de negocio posee sus
datos y los publica como un producto con dueño, contrato y nivel de servicio, sobre una
plataforma común y unas reglas globales que se aplican solas.

## La idea

Durante veinte años, la receta fue: **un equipo central de datos** que recoge los datos de todos
los sistemas, los limpia y los publica. Funciona mientras la empresa tiene cinco dominios y el
equipo central conoce todos los sistemas. Deja de funcionar cuando hay cuarenta dominios, cada
uno con su vocabulario, su ritmo de cambio y sus prioridades. En ese momento el equipo central
es un embudo: todo el mundo espera, y quien espera no sabe por qué su petición es la número 37
de la cola.

La analogía útil es un **mercado de food trucks**. Una sola cocina central preparando 40 menús
distintos es imposible: no escala. En su lugar, cada puesto cocina lo suyo (conoce su producto
mejor que nadie) pero todos comparten las reglas sanitarias, la toma de agua, la corriente, el
sistema de cobro y la normativa de etiquetado. Nadie negocia con el ayuntamiento cada vez que
quiere encender la plancha.

Eso es data mesh: **descentralizar la propiedad, centralizar las reglas y las capacidades**.
Cuatro principios:

**1. Propiedad por dominio.** Quien genera el dato operacional es el dueño de su dato analítico.
El dominio de pedidos entiende qué es un pedido cancelado; el equipo central, no. Poner la
propiedad donde está el conocimiento elimina la traducción, y con ella la mitad de los errores
de interpretación.

**2. El dato como producto.** Un producto de datos no es «una tabla publicada». Es una unidad
con **dueño identificado**, **contrato** de esquema y semántica, **nivel de servicio** (frescura
y disponibilidad), **documentación**, **versionado**, **canal de soporte** y **forma de acceso**
definida. Sin esas siete cosas tienes una tabla que alguien dejó ahí, y el consumidor no sabe si
puede depender de ella.

**3. Plataforma self-service.** Las capacidades comunes (almacenamiento, cómputo, catálogo,
control de acceso, linaje, motor de transformación) se ofrecen como producto interno, con
autoservicio real. La prueba del algodón es concreta: **si para crear un producto de datos hace
falta una reunión con el equipo de plataforma, no es self-service**.

**4. Gobierno computacional federado.** Las reglas globales —qué es un dato personal, cuánto se
retiene, qué calidad mínima se exige, qué definiciones de métricas son vinculantes— se deciden
entre todos (federado) y se **aplican como código** en la plataforma (computacional). El
gobierno deja de ser un comité que aprueba permisos y pasa a ser una política que el sistema
evalúa sola.

Lo que hay que tener claro antes de empezar es lo que data mesh **no** es:

- No es una herramienta. No se compra. Si alguien te vende «la plataforma de data mesh», te está
  vendiendo la parte fácil y llamándola el todo.
- No es una reorganización y ya está. Sin ingenieros de datos en los dominios, el equipo central
  sigue siendo el cuello de botella, solo que ahora con más reuniones.
- No es «cada uno hace lo que quiere». Justo lo contrario: es más gobierno que antes, pero
  automatizado y negociado, no impuesto por un comité.

## Definición formal

Cuatro elementos, con su condición de coherencia:

- **Dominio `d`:** unidad organizativa que posee un conjunto de datos operacionales y responde de
  sus productos de datos analíticos. Es una unidad de **responsabilidad**, no una carpeta.
- **Producto de datos `p = (D, C, S, docs, versión, soporte)`:** sobre el conjunto de datos `D`,
  un contrato `C` (esquema, granularidad, semántica, claves), un nivel de servicio `S`
  (frescura máxima y disponibilidad objetivo), documentación, versión y un canal de soporte.
- **Plataforma `P`:** conjunto de capacidades compartidas que permite a cualquier dominio
  publicar y consumir un producto sin coordinación manual.
- **Gobierno federado `G`:** conjunto de políticas globales expresadas de forma ejecutable
  (etiquetas de clasificación, retención, controles de calidad).

Condiciones que se pueden comprobar, no debatir:

1. **Todo producto tiene dueño nombrado.** Un equipo, no una persona indefinida, y con un canal
   de contacto que responde.
2. **Todo producto tiene un contrato versionado** y los cambios incompatibles se anuncian antes
   ([[contratos-de-datos|contratos de datos]]).
3. **La utilización del equipo central es menor que 1.** Si `ρ = demanda / capacidad ≥ 1`, la
   cola crece sin límite y ninguna priorización arregla nada. Es la condición matemática que
   justifica el cambio.
4. **`ρ < 1` no basta:** el tiempo de espera crece de forma no lineal al acercarse a 1. En un
   modelo simple de una sola cola con llegadas aleatorias, la espera relativa al tiempo de
   servicio es `ρ / (1 − ρ)`: con `ρ = 0,9` esperas nueve veces lo que tardas en atender, y con
   `ρ = 0,5` esperas una vez. Es un modelo, no una predicción exacta, pero captura lo importante:
   acercarse al 100 % de utilización es mucho peor que estar al 50 %.

:::formula
ρ = peticiones por mes ÷ capacidad por mes
si ρ ≥ 1 → la cola crece sin límite  ·  con ρ → 1, la espera → ∞
:::

## Ejemplo

Una empresa con **40 dominios**. Cada dominio pide de media **2 cosas al mes** al equipo central
de datos: 80 peticiones mensuales. El equipo central son **3 personas**, cada una con unas
**120 horas útiles** al mes, y cada petición consume **12 horas** entre reuniones, desarrollo y
revisión. Capacidad: 3 · 120 / 12 = **30 peticiones al mes**.

`ρ = 80 / 30 = 2,67`. La utilización es del **267 %**, y eso no significa «van un poco
apretados»: significa que la cola crece cada mes y que el tiempo de espera no tiene techo. Las
peticiones que llegan hoy no se atenderán nunca a este ritmo.

Refuerzos, en la misma aritmética:

- Con **6 personas**: `ρ = 80 / 60 = 133 %`. Sigue creciendo.
- Con **12 personas**: `ρ = 80 / 120 = 67 %`. La cola se estabiliza, pero has multiplicado por
  cuatro el equipo central y sigues dependiendo de que conozca 40 sistemas.
- Para atender 80 peticiones al mes con `ρ = 0,7` harían falta unas **11-12 personas**.

Ahí está el argumento entero de data mesh en tres números: **no puedes contratar tu salida de
este problema**. La única forma de bajar la demanda del equipo central es que los dominios dejen
de pedirle cosas, y para eso tienen que poder hacerlas ellos. Eso cuesta: cada dominio necesita
al menos una persona con conocimientos de ingeniería de datos, y esa persona la pagas igual.
La diferencia es que ahora escala: 40 dominios con su capacidad propia crecen con la empresa, y
un equipo central de 12 personas con 40 sistemas que aprender, no.

## Código

```python verificable
# La condicion de utilizacion: por que el equipo central no escala con la demanda.
dominios = 40
peticiones_por_dominio = 2
demanda = dominios * peticiones_por_dominio

horas_utiles_mes = 120
horas_por_peticion = 12

for personas in (3, 6, 12):
    capacidad = personas * horas_utiles_mes / horas_por_peticion
    print(f"{personas:>2} personas -> capacidad {capacidad:>4.0f}, utilizacion {demanda / capacidad:>5.0%}")
```

```text
# Un contrato de producto de datos: lo minimo que un consumidor necesita saber.
producto: ventas_pedidos_diarios
dominio: pedidos                      # quien responde
version: 2.1.0
grano: un registro por dia y pais
claves: [fecha, pais]
frescura_sla: 06:00 UTC del dia siguiente
disponibilidad_sla: 99,5 % mensual
clasificacion: interno                # etiqueta que aplica el gobierno
retencion: 400 dias
cambios_incompatibles: se anuncian con 30 dias de antelacion
contacto: #datos-pedidos
```

## Errores típicos

- **Vender data mesh como una compra de tecnología.** Se acaba con la misma organización
  centralizada y una herramienta nueva que nadie pidió. La parte tecnológica (catálogo,
  contratos, políticas como código) es necesaria pero no es la dificultad: la dificultad es
  ceder propiedad y asumir responsabilidad.
- **Declarar «dominios» sin darles ingenieros.** Es el fallo más frecuente: se reparten
  responsabilidades en un organigrama, pero los dominios no tienen con qué cumplirlas. El
  equipo central sigue apagando fuegos, ahora llamados «soporte a dominios».
- **Confundir producto de datos con una tabla publicada.** Sin dueño, contrato ni nivel de
  servicio, el consumidor no puede decidir si depende de ese dato. Un producto sin soporte es
  una trampa aplazada.
- **Convertir el gobierno federado en un comité manual.** Si cada permiso, cada etiqueta y cada
  excepción necesita una reunión mensual, el self-service es un eslogan. Las políticas tienen
  que estar en el sistema y evaluarse solas ([[gobierno-y-privacidad|gobierno y privacidad del
  dato]]).
- **Dejar que cada dominio defina la misma métrica a su manera.** «Cliente activo» con cuatro
  definiciones distintas produce cuatro informes incompatibles. El gobierno federado existe
  precisamente para fijar las definiciones compartidas y que se apliquen por código.
- **Aplicar la malla a una empresa de 15 personas.** El coste de coordinación de 5 dominios con
  una persona cada uno supera cualquier beneficio: el equipo central de dos personas era más
  simple y más rápido. Data mesh es una respuesta a un problema de escala que hay que tener
  antes de adoptarla.

## Comprueba que lo sabes

:::quiz
p: Un equipo central de datos tiene 3 personas, recibe 80 peticiones al mes y cada petición consume 12 horas de una persona que trabaja 120 horas al mes. ¿Qué implica el resultado?
o: Que van un 30 % por encima de su capacidad y basta con priorizar mejor
o: Que la utilización es del 267 %, la cola crece sin límite y el tiempo de espera no tiene techo
o: Que la capacidad es de 80 peticiones y están justo en el límite
a: 2
e: La capacidad es 3 · 120 / 12 = 30 peticiones al mes frente a 80 de demanda: 267 %. Cuando la utilización supera el 100 %, el trabajo pendiente se acumula indefinidamente; priorizar cambia el orden, no el crecimiento de la cola.
:::

:::quiz
p: ¿Qué distingue un producto de datos de una tabla publicada en el lago?
o: Que el producto tiene dueño, contrato, nivel de servicio, versión y canal de soporte
o: Que el producto ocupa menos espacio porque está comprimido
o: Que el producto solo lo puede leer el dominio que lo creó
a: 1
e: El producto de datos es una unidad de responsabilidad: alguien responde de él, hay un contrato de esquema y semántica, un SLA de frescura, versiones y un sitio donde preguntar. Una tabla suelta puede ser cualquier cosa y el consumidor no puede depender de ella.
:::

:::aviso
Data mesh no elimina el equipo central: lo **encoge y lo cambia de trabajo**. Pasa de construir
pipeline por encargo a construir la plataforma, las políticas y las herramientas que hacen que
los dominios puedan publicar solos. Si ese equipo sigue atendiendo peticiones, has hecho la
reorganización y has conservado el cuello de botella.
:::
