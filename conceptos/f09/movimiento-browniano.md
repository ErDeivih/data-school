---
id: movimiento-browniano
titulo: Movimiento browniano
fase: 9
nivel: intermedio
rutas: [quant, ds]
prerequisitos: [variable-aleatoria, distribuciones-continuas, ley-de-los-grandes-numeros]
tags: [procesos, estocastico, precios]
resumen: El paseo aleatorio en tiempo continuo que sostiene casi todo modelo de precio, y por qué su varianza crece con el tiempo.
fuentes: ["Bachelier (1900), 'Théorie de la spéculation'", "Karatzas y Shreve (1991), 'Brownian Motion and Stochastic Calculus'"]
---

## En una frase

Un movimiento browniano es un proceso cuyo valor cambia por sumas de shocks independientes, de
forma que su desviación típica crece con la raíz del tiempo y su camino no se puede derivar en
ningún punto.

## La idea

Mira un grano de polen en un vaso de agua. No se mueve en línea recta ni se queda quieto: recibe
golpes de moléculas por todos lados, miles por segundo, cada uno de tamaño diminuto e
independiente del anterior. El resultado no es un vaivén ordenado, es un camino que cambia de
dirección en cada instante. Eso es el movimiento browniano.

De ahí salen tres consecuencias que cuesta aceptar al principio, y las tres importan para modelar
precios:

- **La incertidumbre crece con la raíz del tiempo, no con el tiempo.** Al año, la desviación
  típica es √252 veces la de un día, no 252 veces. Sumar varianzas es sumar cuadrados: 252 días de
  varianza diaria dan una varianza anual, y al volver a desviación aparece la raíz.
- **El camino no tiene derivada.** En cualquier escala que mires, sigue teniendo rugosidad. Por eso
  no se puede escribir «la velocidad del precio»: lo que existe es el cambio por unidad de tiempo
  y su tamaño típico, que es la volatilidad.
- **La suma de muchos golpes pequeños da una normal.** Ese es el teorema central del límite
  actuando dentro de un proceso, y es la razón de que la campana aparezca en todas partes.

Para pasar de un paseo a un precio hay dos variantes. El **aritmético** (ABM) suma el ruido
directamente: `dS = μ dt + σ dW`. El **geométrico** (GBM) lo multiplica por el nivel: `dS = μ S dt +
σ S dW`. La diferencia no es cosmética. El aritmético puede dar precios negativos, porque nada le
impide bajar de cero; el geométrico no, porque cada paso es un porcentaje del nivel actual. Un
precio de una acción no puede ser negativo, así que el GBM es el punto de partida razonable; un
tipo de interés sí puede serlo, y por eso en tipos se usan modelos aditivos como el de Bachelier
o el de Vasicek.

Y una advertencia que aparece en todas las páginas de esta fase: que un modelo no pueda dar
precios negativos no lo convierte en verdadero. El GBM tampoco reproduce las colas gordas ni los
saltos de un mercado real. Es el suelo sobre el que se construye lo demás, no el edificio.

## Definición formal

Un movimiento browniano estándar `W_t` es un proceso con `W_0 = 0`, incrementos independientes y
estacionarios, `W_t − W_s ~ N(0, t − s)` para `t > s`, y caminos continuos.

:::formula
ABM:  dS = μ dt + σ dW        GBM:  dS = μ S dt + σ S dW
:::

- `μ` — deriva anual: lo que el activo tiende a subir por unidad de tiempo.
- `σ` — volatilidad anual: el tamaño típico del shock, en las mismas unidades que la deriva.
- `W` — movimiento browniano estándar; su incremento `dW` tiene media cero y varianza `dt`.
- `S` — nivel del activo en cada instante.

El GBM tiene solución cerrada, que es lo que lo hace tan cómodo:

:::formula
S_t = S_0 · exp( (μ − σ²/2) · t + σ · W_t )
:::

Ese `−σ²/2` no es un adorno: es lo que hace que la media de `S_t` sea `S_0 · e^{μt}` mientras la
media del **logaritmo** crece a `μ − σ²/2`. La diferencia entre las dos es el arrastre de
volatilidad que aparece al componer retornos, y es la razón de que un activo apalancado rinda
menos de lo que sugiere su media aritmética.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `μ` | Deriva anual del activo | tanto por uno al año | Sube el nivel medio de todas las trayectorias, pero no cambia su dispersión |
| `σ` | Volatilidad anual | tanto por uno al año | Abre el abanico de trayectorias y baja la media del logaritmo por el término `−σ²/2` |
| `t` | Horizonte de tiempo | años | La desviación típica del nivel crece como `√t`: cuadruplicar el plazo solo dobla la incertidumbre |
| `W_t` | Valor del browniano en `t` | adimensional | Es el sorteo concreto: dos trayectorias con el mismo `μ` y `σ` se separan solo por `W` |
:::

:::trampa
La volatilidad se anualiza con √252 y se desanualiza dividiendo por √252. Si divides la
volatilidad diaria por 252 en vez de por √252, el modelo no falla: da un número plausible y
equivocado, y todo lo que construyas encima hereda el error. Si tu σ diaria es 0,0126, la anual
es 0,20; si la divides por 252 obtienes 0,00005, que parece una volatilidad de bono.
:::

## Ejemplo

Un activo a 100, con `μ = 0,05` y `σ = 0,20`, a un año. El sorteo del browniano da `W₁ = 0,5`.

- **ABM:** `100 + 0,05 · 100 · 1 + 0,20 · 100 · 0,5 = 100 + 5 + 10 = 115`.
- **GBM:** `100 · exp((0,05 − 0,02) · 1 + 0,20 · 0,5) = 100 · exp(0,13) = 113,88`.

Casi el mismo número. Ahora el mismo activo con `W₁ = −0,5`:

- **ABM:** `100 + 5 − 10 = 95`.
- **GBM:** `100 · exp(0,03 − 0,10) = 100 · exp(−0,07) = 93,24`.

Siguen pareciéndose porque el plazo es corto y la volatilidad no es alta. La diferencia se abre
en plazos largos y con volatilidades altas: con `σ = 0,80` y `W₁ = −1,5`, el ABM puede dar un
valor negativo, y ahí el modelo deja de describir un precio.

## Código

```python verificable
import numpy as np

# 20.000 trayectorias de un ano, 252 pasos: el mismo ruido para el ABM y para el GBM
rng = np.random.default_rng(7)
trayectorias, pasos = 20_000, 252
dt = 1 / pasos
w = np.cumsum(rng.standard_normal((trayectorias, pasos)) * np.sqrt(dt), axis=1)[:, -1]

abm = 100 + 0.05 * 100 + 0.20 * 100 * w
gbm = 100 * np.exp((0.05 - 0.5 * 0.20 ** 2) + 0.20 * w)

print(f"ABM media {abm.mean():.2f} desviacion {abm.std():.2f}")      # -> ABM media 104.96 desviacion 19.87
print(f"GBM media {gbm.mean():.2f} desviacion {gbm.std():.2f}")      # -> GBM media 105.06 desviacion 21.05
print(f"ABM negativo {(abm < 0).mean():.2%}")                        # -> ABM negativo 0.00%
print(f"log GBM desviacion {np.log(gbm / 100).std():.4f}")           # -> log GBM desviacion 0.1987
```

La última línea es la que hay que mirar dos veces: la desviación del logaritmo del precio sale
0,1987, es decir, `σ` con error de simulación. El modelo está bien montado. La del nivel sale
21,05 porque el GBM es multiplicativo: un 20 % de 100 no es lo mismo que un 20 % de 120.

:::claves
- `np.cumsum(..., axis=1)` acumula **dentro de cada fila** para construir el browniano paso a
  paso. Sin `axis=1` aplana la matriz y devuelve un vector de 5 millones de números: no falla,
  simplemente el resultado deja de ser una trayectoria.
- `* np.sqrt(dt)` es la pieza que más se equivoca. El incremento browniano escala con la raíz del
  paso, no con el paso. Cambiarlo por `dt` hace que la incertidumbre anual dependa del número de
  pasos que hayas elegido, que es la definición de un error de modelo.
- `[:, -1]` toma el último instante de cada trayectoria. Con `[:, 0]` estarías mirando el primer
  paso, cuando apenas ha pasado un día.
- `np.exp((0.05 - 0.5 * 0.20 ** 2) + 0.20 * w)` aplica la solución exacta en un solo salto. Es más
  honesto que simular 252 pasos del GBM: la solución cerrada no tiene error de discretización.
- `np.log(gbm / 100).std()` mide la dispersión en logaritmo, que es la que crece como `σ√t` y la
  que se usa para comparar plazos distintos.
:::

## Errores típicos

- **Usar ABM para precios.** Un modelo aditivo permite niveles negativos. En una acción es
  absurdo; en un tipo de interés o en un spread de crédito puede ser exactamente lo que quieres.
- **Confundir σ anual con diaria.** La conversión es `σ_diaria = σ_anual / √252`. Dividir por 252
  da un número 15 veces más pequeño que parece razonable y arruina cualquier cálculo de opciones.
- **Olvidar el `−σ²/2`.** Entonces la media del logaritmo sale igual a `μ` y los precios simulados
  se van sistemáticamente por encima de los reales en plazos largos. No es un detalle de
  notación: es la diferencia entre un modelo que respeta la media y uno que la infla.
- **Creer que la trayectoria simulada predice el precio.** El browniano genera futuros posibles,
  no un futuro. Cambiar la semilla cambia el resultado y ninguno es «el» resultado.
- **Suponer que un camino suave se puede derivar.** La rugosidad no es un artefacto del gráfico:
  si intentas calcular la variación del precio por unidad de tiempo en el límite, no converge.
  Por eso la volatilidad se estima sobre intervalos, no sobre instantes.
- **Pensar que el GBM ya resuelve las colas.** Un GBM no tiene saltos ni colas gordas. Para eso
  hacen falta procesos con saltos o volatilidad estocástica, y eso es otra página.

:::practica
enunciado: Un activo cotiza a 80, con volatilidad anual del 30 % y deriva del 4 %. Con un sorteo W₁ = −0,8, calcula el nivel a un año con ABM y con GBM, y explica de dónde sale la diferencia.
pista: En el ABM la deriva y el ruido se suman en unidades del precio; en el GBM, dentro de una exponencial, con el término −σ²/2.
solucion: ABM = 80 + 0,04 · 80 + 0,30 · 80 · (−0,8) = 80 + 3,2 − 19,2 = 64. GBM = 80 · exp((0,04 − 0,045) · 1 + 0,30 · (−0,8)) = 80 · exp(−0,245) = 62,6. La diferencia de 1,4 sale del término −σ²/2 y de que el GBM aplica el porcentaje sobre el nivel, no sobre una cantidad fija de euros.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué la desviación típica de un browniano a un año es √252 veces la de un día y no 252?
o: Porque las varianzas se suman y al volver a desviación aparece la raíz cuadrada
o: Porque el mercado solo abre 252 días al año
o: Porque el browniano tiene media cero y eso reduce la dispersión
a: 1
e: Los incrementos independientes suman sus varianzas, y la varianza de 252 pasos es 252 veces la de uno. La desviación es la raíz de la varianza, de ahí √252. El número de días de cotización es un dato, no la causa.
:::

:::quiz
p: ¿Qué diferencia al ABM del GBM en una frase?
o: El ABM suma el ruido en unidades del precio y el GBM lo aplica como porcentaje del nivel
o: El ABM es discreto y el GBM es continuo
o: El GBM tiene media cero y el ABM no
a: 1
e: En el ABM el término estocástico es σ dW, una cantidad fija de euros; en el GBM es σ S dW, proporcional al nivel. Por eso solo el segundo garantiza que el precio no cambie de signo.
:::
