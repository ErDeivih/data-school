---
id: accesibilidad
titulo: Accesibilidad
fase: 11
nivel: intermedio
rutas: [alg]
prerequisitos: [apis-rest]
tags: [accesibilidad, wcag, contraste, usabilidad]
resumen: Que la web que haces la pueda usar cualquiera: contraste suficiente, todo con teclado, estructura que entienda un lector de pantalla y por qué no basta un escaner.
fuentes: ["W3C (2018), 'Web Content Accessibility Guidelines (WCAG) 2.1'", "W3C, 'Understanding WCAG 2.1' (documentacion oficial)"]
---

## En una frase

Accesibilidad es hacer que tu interfaz funcione para alguien que no ve la pantalla, que no
puede usar el ratón, que oye mal o que mira con un contraste distinto: en la práctica, cuatro
reglas concretas que además te benefician a ti.

## La idea

Piensa en los rebajes de las aceras. Se hicieron para sillas de ruedas, y los usan los carritos
de bebé, las maletas con ruedas y cualquiera que vaya cargado. La accesibilidad web funciona
igual: el subtítulo de un vídeo sirve para quien no oye y para quien lo ve en el metro sin
auriculares; el contraste suficiente sirve para quien tiene baja visión y para quien mira el
móvil a pleno sol.

Hay una diferencia importante con la rampa de la acera: en la web, la accesibilidad **no es un
añadido, es el uso correcto del material**. Cuando escribes `<button>` en lugar de un `<div>`
con un `onclick`, no estás haciendo accesibilidad: estás usando el elemento que ya trae teclado,
anuncio de lector de pantalla y estados. Cuando pones un `<label>` asociado a un campo, el clic
en el texto funciona para todos. El 80 % de la accesibilidad de una aplicación normal no
requiere trabajo extra, requiere **no romper lo que ya venía hecho**.

Las cuatro reglas que hay que tener en la cabeza (son el resumen de las WCAG, el estándar del
W3C):

1. **Perceptible.** Todo lo importante se percibe por más de un canal. Las imágenes con
   información llevan texto alternativo; un vídeo con voz lleva subtítulos; el color nunca es
   la única forma de distinguir algo (un gráfico con líneas roja y verde necesita además
   etiquetas o patrones distintos, porque hay daltonismo).
2. **Operable.** Todo se puede hacer solo con teclado: tabular, activar, cerrar un diálogo y
   volver al sitio. Sin trampas de foco (quedarse atrapado dentro de un componente) y sin
   acciones que dependan de un gesto concreto.
3. **Comprensible.** El texto se lee, los errores de formulario dicen qué pasa y cómo
   arreglarlo, y el orden de tabulación sigue el orden visual.
4. **Robusto.** El HTML es válido y usa los nombres accesibles correctos, para que las ayudas
   técnicas (lectores de pantalla, magnificadores, conmutadores) puedan interpretarlo hoy y
   mañana.

Y los tres niveles de conformidad: **A** (lo mínimo), **AA** (el objetivo habitual, y el que
citan casi todas las normativas) y **AAA** (exigente, no obligatorio en general). Cuando
alguien dice «cumplimos WCAG 2.1 AA» está diciendo que pasa los criterios de nivel A y AA.

## Definición formal

El criterio más medible de todos es el **contraste**, y tiene fórmula exacta. Se calcula la
luminancia relativa `L` de cada color y después el cociente entre la más clara y la más oscura:

:::formula
L = 0,2126·R + 0,7152·G + 0,0722·B   ·   contraste = (L_claro + 0,05) / (L_oscuro + 0,05)
:::

Cada canal (`R`, `G`, `B`) se normaliza a `[0, 1]` dividiendo entre 255 y luego se aplica la
transformación de la gamma:

```
c = canal / 255
c' = c / 12,92                  si c <= 0,03928
c' = ((c + 0,055) / 1,055)^2,4   si c > 0,03928
```

Símbolos: `R`, `G`, `B` son los canales linealizados del color; `L` es la luminancia relativa,
entre 0 (negro) y 1 (blanco); `L_claro` y `L_oscuro` son las luminancias del más claro y del
más oscuro de los dos colores comparados; el `+ 0,05` evita que un contraste de colores muy
oscuros dé un cociente enorme.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `R`, `G`, `B` | Los canales del color ya linealizados con la gamma | de 0 a 1 | El color se aclara, y la luminancia sube sobre todo si el que sube es `G` |
| `L` | Luminancia relativa de un color | de 0 (negro) a 1 (blanco) | El color se percibe más claro y el contraste contra un fondo claro baja |
| `L_claro` / `L_oscuro` | Luminancias del más claro y del más oscuro de los dos colores comparados | de 0 a 1 | Si sube la del claro, el cociente crece; si sube la del oscuro, el cociente baja |
| `+ 0,05` | Constante que se suma arriba y abajo del cociente | adimensional | No aplica: es fija. Evita que dos colores casi negros den un cociente enorme y que el negro puro divida por cero |
| `4,5:1` y `3:1` | Umbrales del nivel AA para texto normal y para texto grande | cociente | Es el listón a superar: por encima cumple y por debajo no, sin zonas intermedias |
:::

Umbrales del nivel AA: **4,5:1** para texto normal, **3:1** para texto grande (a partir de
24 px, o 18,66 px en negrita) y **3:1** para los bordes e iconos que son la única forma de
identificar un control. El nivel AAA pide 7:1 para texto normal.

## Ejemplo

Comprobando tres pares de colores con la fórmula anterior:

```
gris #767676 sobre blanco   ->  4,54:1   AA texto normal: si
gris #999999 sobre blanco   ->  2,85:1   AA texto normal: no
azul #0057b8 sobre blanco   ->  6,87:1   AA texto normal: si
```

Fíjate en lo estrecho del margen: el gris que casi todo el mundo usa para los textos
secundarios (`#767676`) pasa por muy poco, y un gris un punto más claro (`#999999`, que se ve
casi igual en una pantalla de escritorio) se queda fuera. Es un buen recordatorio de que el
contraste no se estima a ojo: se calcula.

:::figura
fichero: accesibilidad-contraste
pie: A la izquierda, los tres colores del ejemplo sobre blanco con los dos umbrales del nivel AA: #767676 llega a 4,54:1 y cumple por muy poco, #999999 se queda en 2,85:1 y no cumple, y #0057b8 sube a 6,87:1. A la derecha, la misma cuenta para todos los grises: el contraste se desploma al aclarar el color y la frontera del texto normal cae entre el gris 118 (#767676, que pasa) y el 119 (#777777, que ya no). El contraste no se estima a ojo, se calcula, y entre cumplir y no cumplir hay un solo nivel de gris de diferencia.
fuente: figuras/accesibilidad-1.py
:::

## Código

```python verificable
def contraste(rgb1, rgb2):
    """Cociente de contraste WCAG entre dos colores RGB (0-255)."""
    def lineal(v):
        v = v / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4   # gamma del estandar

    def luminancia(c):
        return 0.2126 * lineal(c[0]) + 0.7152 * lineal(c[1]) + 0.0722 * lineal(c[2])   # el verde pesa mas

    claro, oscuro = sorted([luminancia(rgb1), luminancia(rgb2)], reverse=True)   # el mas claro primero
    return (claro + 0.05) / (oscuro + 0.05)      # el +0.05 evita el cociente infinito del negro puro

casos = {
    "gris #767676": ((118, 118, 118), (255, 255, 255)),
    "gris #999999": ((153, 153, 153), (255, 255, 255)),
    "azul #0057b8": ((0, 87, 184), (255, 255, 255)),
}
for nombre, (frente, fondo) in casos.items():    # cada valor es una tupla con los dos colores
    r = contraste(frente, fondo)
    print(f"{nombre} sobre blanco: {r:.2f}:1  AA normal: {'si' if r >= 4.5 else 'no'}")   # umbral 4,5:1
```

:::claves
- La función devuelve un número (siempre mayor o igual que 1), no un «sí o no»: el listón lo pones tú, 4,5:1 para texto normal y 3:1 para texto grande. Ordenar las dos luminancias con `reverse=True` es lo que garantiza que el cociente salga ≥ 1; al revés, `#767676` daría 0,22 en lugar de 4,54.
- El `+ 0.05` está en el numerador **y** en el denominador. No es decorativo: sin él, dos colores casi negros darían un cociente enorme y el negro puro dividiría por cero.
- Los canales no se promedian: el verde pesa 0,7152 y el azul solo 0,0722. Dos colores que se ven igual de claros pueden dar contrastes muy distintos, así que la cuenta no se puede hacer a ojo.
- La comparación `r >= 4.5` usa el valor completo, pero el mensaje imprime dos decimales: un 4,495 sale por pantalla como «4,50» y aun así dice «no». Redondear antes de comparar cambia el veredicto de los colores que están justo en el borde.
- `lineal` recibe un canal suelto (0-255), no la tupla del color: `luminancia` la llama tres veces, una por canal.
- `casos.items()` recorre el diccionario devolviendo pares `(clave, valor)`, y el `for` desempaqueta además el valor en sus dos colores, `(frente, fondo)`. Si un caso tuviera tres colores, esa línea fallaría con `ValueError`.
:::

```html ilustrativo
<!-- El mismo boton, dos veces. El segundo ya trae teclado, foco y anuncio de lector. -->
<div class="boton" onclick="enviar()">Enviar</div>

<button type="submit">Enviar</button>

<!-- Una imagen informativa necesita texto alternativo; una decorativa, alt vacio. -->
<img src="grafico-ventas.png" alt="Ventas por trimestre: sube de 120 a 180 mil euros">

<!-- El label se asocia con for/id: el clic en el texto enfoca el campo. -->
<label for="email">Correo electronico</label>
<input id="email" name="email" type="email" autocomplete="email" required>
```

## Errores típicos

- **Usar un `div` como botón.** Un `div` con `onclick` no recibe el foco con el tabulador, no
  se activa con la barra espaciadora y no se anuncia como botón. Usa `<button>` (o `<a>` para
  navegar) y deja que el navegador haga el trabajo; si necesitas un componente raro, `role` y
  manejo de teclado a mano, y entonces pruébalo con teclado de verdad.
- **Quitar el contorno de foco.** `outline: none` sin nada que lo sustituya deja a quien navega
  con teclado sin saber dónde está. Si el contorno por defecto te parece feo, sustitúyelo por
  uno propio visible, no lo elimines.
- **Confiar en el color.** Un formulario que marca los campos con error solo en rojo, o un
  gráfico con líneas distinguidas solo por color, es inutilizable para una parte de la gente.
  Añade texto, icono, subrayado o patrón.
- **Texto alternativo inútil.** `alt="imagen"` o `alt="grafico1.png"` no aporta nada. El
  alternativo describe la información, no el fichero; y si la imagen es puramente decorativa,
  el correcto es `alt=""` (vacío, sin espacio) para que el lector la salte.
- **Poner etiquetas solo con `placeholder`.** El texto de ejemplo desaparece al escribir, tiene
  poco contraste y muchos lectores no lo anuncian de forma fiable. El `placeholder` es una
  ayuda adicional; la etiqueta va en un `<label>`.
- **Romper el orden de tabulación con CSS.** Si con `float`, `order` o posicionamiento absoluto
  el orden visual no coincide con el orden del DOM, el foco salta de forma impredecible. El
  orden del HTML es el que manda: diséñalo bien y no lo corrijas con estilos.
- **Dar por bueno el informe de un escáner automático.** Las herramientas detectan una parte de
  los problemas (contraste, `alt` ausente, etiquetas sueltas) y no detectan ninguno de los que
  dependen del significado. Hay que probar con teclado y con un lector de pantalla.

:::trampa
Un diálogo modal mal hecho es la pesadilla clásica: abre, el foco se queda detrás en la página
de fondo, y quien navega con teclado tabula por contenido invisible. Un modal correcto mueve el
foco dentro al abrirse, lo mantiene ahí mientras está abierto, cierra con `Escape` y **devuelve
el foco al elemento que lo abrió**. Si usas un componente de una librería, comprueba esas
cuatro cosas antes de fiarte.
:::

## Comprueba que lo sabes

:::quiz
p: Un texto gris #999999 sobre fondo blanco tiene un contraste de 2,85:1. ¿Cumple el nivel AA para texto normal?
o: Sí, porque el gris claro se lee bien en pantallas modernas
o: No: el nivel AA exige 4,5:1 para texto normal, y 2,85:1 se queda corto
o: Sí, siempre que el texto esté en negrita
a: 2
e: El umbral de AA es 4,5:1 para texto normal y 3:1 para texto grande (a partir de 24 px, o 18,66 px en negrita). 2,85:1 no llega a ninguno de los dos, y la negrita no cambia el contraste: solo cambia el tamaño a partir del cual se aplica el umbral menor.
:::

:::quiz
p: ¿Por qué usar `<button>` es mejor que un `<div>` con `onclick` para un botón?
o: Porque ocupa menos código y carga más rápido
o: Porque el elemento nativo recibe el foco con el tabulador, se activa con el teclado y se anuncia como botón
o: Porque los `div` no pueden ejecutar JavaScript en todos los navegadores
a: 2
e: El elemento nativo trae gratis el comportamiento de teclado, el estado de foco y el rol para las ayudas técnicas. Con un `div` hay que reproducir todo eso a mano (tabindex, papel ARIA, manejo de teclas) y es fácil que falte algo. Las otras dos opciones son falsas.
:::

:::quiz
p: Un gráfico distingue las series solo por color (rojo y verde). ¿Cuál es el problema y la solución?
o: Ninguno, si los colores tienen contraste suficiente entre sí
o: Que el color no es perceptible para parte de la gente; hay que añadir además etiquetas, patrones o formas distintas
o: Que el rojo y el verde consumen más batería
a: 2
e: El color nunca puede ser el único canal de información, porque hay daltonismo y porque el gráfico se imprime en blanco y negro. El contraste entre series no resuelve el problema: se necesita redundancia, como líneas con trazo distinto, marcas por punto o etiquetas directas sobre cada serie.
:::
