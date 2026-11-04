---
id: economia-de-la-inferencia-propia
titulo: Economía de la inferencia propia
fase: 8
nivel: avanzado
rutas: [ds, de]
prerequisitos: [como-funciona-un-llm, coste-y-latencia, cuantizacion-y-destilacion]
tags: [inferencia, coste, gpu, autoalojamiento, utilizacion]
resumen: Pagar por token o alquilar la GPU son dos estructuras de coste distintas, y quien decide no es el precio de la hora sino la utilización real y el tamaño de los picos.
fuentes: ["Pope et al. (2023), 'Efficiently Scaling Transformer Inference'", "Databricks (2023), 'LLM Inference Performance Engineering: Best Practices'"]
---

## En una frase

Pagar por token es un coste **variable** que crece con el uso y se paga solo cuando hay tráfico;
alquilar una GPU es un coste **fijo** que se paga entero aunque la máquina esté parada, así que el
precio real de tus tokens lo decide la **utilización**: qué fracción del tiempo está trabajando de
verdad lo que pagas.

## La idea

Piensa en la diferencia entre pagar un gimnasio por sesión o alquilar el local entero por meses.
Por sesión es cómodo: si un mes no vas, no pagas. El local entero sale mucho más barato **por hora
de uso** si lo llenas, pero la factura llega igual en enero y en agosto. Y si tu clase solo tiene
gente los martes de 19 a 21, pagas el local completo para cuatro horas a la semana.

Servir tu propio modelo es exactamente eso:

- **Modelo alojado, precio por token.** Pagas por cada token que entra y cada token que sale. Cero
  tráfico, cero factura; un pico, factura proporcional. El proveedor asume la capacidad y por eso
  cobra un margen.
- **Modelo propio en una GPU alquilada.** Pagas la hora de máquina, trabajes o no. El coste por
  token es la factura dividida entre los tokens servidos: si sirves pocos, sale carísimo.

Esa división es todo el problema, y hay una cifra que lo resume: la **utilización**, la fracción
de la capacidad comprada que se usa de verdad. En el ejemplo de esta página, una GPU con un modelo
abierto sirve unos 5.184 millones de tokens al mes si está ocupada al 100 %, y el alquiler es de
1.800 € al mes pase lo que pase. A pleno rendimiento, un millón de tokens cuesta **0,347 €**; al
10 %, cuesta **3,47 €**: diez veces más por el mismo trabajo.

El precio de equilibrio, el «break-even» que se calcula en una servilleta, es entonces:

:::formula
coste_propio_por_millon = coste_GPU_mes / ( tokens_mes_por_GPU · utilización )
:::

Y el modelo propio gana cuando ese número baja del precio de la API:

:::formula
gana_lo_propio  si  utilización > precio_API / coste_lleno
:::

donde `coste_lleno` es el coste por millón con la GPU al 100 %. Con `coste_lleno = 0,347 €`, contra
una API de 3 €/millón basta con un 864 % de utilización —es decir, la GPU tendría que estar
ocupada 8,6 veces a la vez: **imposible**—, y contra una de 0,50 €/millón haría falta un 144 %,
que tampoco existe. Ese es el resultado que descoloca a quien acaba de ver el precio de la hora de
GPU y cree que autoalojar siempre sale más barato: con el coste lleno de este ejemplo, ninguna API
de las baratas se bate con una sola GPU.

Los **picos** son el mecanismo que hunde la utilización. Si tu tráfico es de 20 millones de tokens
al día de media pero tiene picos de diez veces la media, la máquina que compras es la que aguanta
el pico, no la media: pagas diez veces la capacidad que usas y tu utilización cae al 10 %,
exactamente `1 / 10`, el inverso de la relación pico/media. Lo que lo arregla es **aplanar la
demanda** (encolar trabajos por lotes en horas valle, repartir peticiones, servir con un modelo
más pequeño en los picos) o aceptar que para ti el precio por token es mejor negocio.

Y quedan las palancas técnicas, que mejoran las dos cifras a la vez: **cuantizar** los pesos a int8
o int4 reduce la memoria y el ancho de banda —el cuello de botella real— y sube los tokens por
segundo con el mismo alquiler; **destilar** a un modelo menor cuesta bastante menos de la mitad,
porque la inferencia no crece linealmente con los parámetros; y **agrupar en lotes** es la
diferencia entre usar el 5 % de la GPU y usar el 60 %.

Y una advertencia que no se puede saltar: la factura de la GPU **no es el coste total**. Hay que
sumarle el tiempo de ingeniería, el almacenamiento de los pesos, la supervisión, la evaluación de
cada versión y las réplicas de alta disponibilidad. Para un equipo pequeño, esas partidas suelen
pesar más que la máquina.

## Definición formal

Sea `C_gpu` el coste de alquiler de una GPU por hora, `T` su rendimiento sostenido en tokens por
segundo con el lote que vas a usar, `D` la demanda del periodo y `u` la utilización (fracción de
la capacidad comprada que se usa). Todas las cuentas salen de aquí:

:::formula
capacidad_tokens = T · 3600 · horas · n_GPUs        coste = C_gpu · horas · n_GPUs
u = demanda / capacidad_tokens        coste_por_millon = 10⁶ · coste / demanda
:::

- `T` — tokens por segundo que sirve **una** GPU con el lote y la mezcla de entrada/salida
  previstos. Es el número que más se equivoca la gente: se copia de un banco de pruebas con lote
  1, donde la GPU está casi vacía.
- `n_GPUs` — máquinas que hay que tener encendidas. Lo fija el **pico**, no la media.
- `demanda` — tokens servidos en el periodo, sumando entrada y salida con el peso que cada uno
  tenga en tu factura.
- `u` — utilización: `demanda / capacidad`. Entre 0 y 1 si no te has pasado comprando; por debajo
  del 20 % el coste por token se dispara.
- `coste_por_millon` — lo único comparable con el precio de la API.

Y la condición de indiferencia entre las dos opciones:

:::formula
precio_API  =  coste_lleno / u        ⟺        u_equilibrio = precio_API / coste_lleno
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `C_gpu` | Precio del alquiler de la GPU | euros por hora | Sube el coste por token en la misma proporción, pero **no cambia la utilización de equilibrio**: si la hora se dobla, el precio de la API al que empatas también se dobla. Es la palanca que menos decide |
| `T` | Tokens por segundo que sirve una GPU | tokens por segundo | Es la palanca grande del numerador: doblar `T` divide el coste por token entre dos y deja la utilización igual. Cuantizar, destilar y agrupar en lotes suben `T` |
| `n_GPUs` | GPUs encendidas, fijadas por el pico | máquinas | Si sube sin que suba la demanda, la utilización baja y el coste por token sube en la misma proporción. Comprar por si acaso es la forma más cara de asegurar capacidad |
| `demanda` | Tokens servidos en el periodo | tokens (o millones) | Sube el numerador de la utilización y baja el coste por token: más carga sobre la misma máquina siempre sale a cuenta. Es la palanca que sí controlas a base de aplanar picos |
| `u` | Utilización: fracción de la capacidad que se usa | adimensional (0 a 1) | Es el divisor de todo. Bajar del 10 % multiplica por diez el coste por token; subir del 60 % lo deja cerca del mínimo alcanzable |
| `coste_lleno` | Coste por millón con la GPU al 100 % | euros por millón | Es tu «precio mínimo posible» y el listón contra el que comparas la API. Con una GPU de 2,50 €/hora y 2.000 tokens/s sale 0,347 €/millón |
| `u_equilibrio` | Utilización a la que da igual pagar la API que autoalojar | adimensional | Si tu utilización real es menor, la API gana. Sube con el precio de la API y baja con `T`: por eso contra una API barata el autoalojamiento exige una GPU casi siempre ocupada |
| `precio_API` | Lo que pagas al proveedor por millón de tokens | euros por millón | Es el número que hay que comparar **por tipo de token**: el de salida suele costar varias veces el de entrada, y mezclarlos en una media te da una comparación falsa |
:::

## Ejemplo

Un equipo sirve 20 millones de tokens al día de media con un modelo abierto, y su tráfico tiene
picos de diez veces la media. Los números de trabajo:

- Alquiler: 2,50 € por GPU y hora → **1.800 € al mes** por GPU (24 horas, 30 días).
- Rendimiento sostenido: 2.000 tokens por segundo → **5.184 millones de tokens al mes** por GPU.
- Coste con la GPU al 100 %: 1.800 / 5.184 = **0,347 € por millón**.
- Demanda: 20 · 30 = **600 millones de tokens al mes**.
- Capacidad para el pico: 600 / 5.184 · 10 = **1,157 GPUs**. En la práctica se compran 2, porque no
  se alquilan fracciones y hace falta margen.

Con esas cifras, la utilización media es `600 / (5.184 · 1,157) = 10,0 %`, y el coste por millón
sale a `0,347 / 0,10 =` **3,47 €**. Contra una API de 3 €/millón, autoalojar está prácticamente
empatado; contra una de 15 €/millón, gana por goleada; contra una de 0,50 €/millón, pierde.

La tabla de la utilización deja claro dónde está el dinero:

| Utilización | Coste por millón | ¿Bate a una API de 0,50 €? | ¿Bate a una de 3,00 €? |
| --- | --- | --- | --- |
| 5 % | 6,94 € | No | No |
| 10 % | 3,47 € | No | No (casi) |
| 20 % | 1,74 € | No | Sí |
| 30 % | 1,16 € | No | Sí |
| 60 % | 0,58 € | No | Sí |
| 100 % | 0,35 € | Sí | Sí |

Fíjate en la forma de la tabla: el coste por millón **se divide entre dos** cada vez que la
utilización se dobla. Bajar de 10 % a 20 % ahorra más dinero que cualquier optimización de kernel.

Las facturas del mes, con 600 millones de tokens, lo dicen en euros:

| Opción | Factura mensual |
| --- | --- |
| Propio, dimensionado para el pico (2 GPUs) | 3.600 € |
| API a 0,50 €/millón | 300 € |
| API a 1,00 €/millón | 600 € |
| API a 3,00 €/millón | 1.800 € |
| API a 15,00 €/millón | 9.000 € |

Y ahora la parte que casi nadie mira: **la palanca de la cuantización**. Si comprimir el modelo
sube el rendimiento de 2.000 a 3.200 tokens por segundo (un factor 1,6, típico de un buen int8),
el coste con la GPU llena baja de 0,347 a **0,217 € por millón**, un 37 % menos, con el mismo
alquiler y sin tocar la demanda. Con un factor 2,3 (int4), baja a **0,151 €/millón**, un 57 %
menos. Las dos cifras hay que pagarlas en calidad: se miden con el mismo conjunto de evaluación
que usaste para elegir el modelo, y si la métrica aguanta, el ahorro es real.

:::figura
fichero: inferencia-propia-utilizacion-y-equilibrio
pie: Arriba, el coste por millón de tokens según la utilización de la GPU, en escala logarítmica: con la máquina al 3 % sale a 11,57 € por millón y con la máquina al 100 % baja a 0,35 €, y el punto rojo marca dónde cae una carga dimensionada para picos de diez veces la media: 10 % de utilización y 3,47 € por millón. Las líneas discontinuas son los precios de tres APIs de referencia: contra la de 0,50 € no hay manera de competir, y contra la de 15 € se gana en casi cualquier escenario. Abajo, la utilización que haría falta para empatar con cada precio de API: 28,8 % para una API de 0,10 €/millón, 144 % para una de 0,50 € —imposible, porque la GPU no puede estar ocupada más del 100 % del tiempo— y 4.320 % para una de 15 €. La raya roja marca el 100 %: todo lo que quede a su derecha es una quimera aritmética.
fuente: figuras/inferencia-propia-1.py
:::

## Código

```python verificable
# Todos los numeros de la pagina salen de estas seis constantes.
PRECIO_GPU_HORA = 2.50          # alquiler de una GPU por hora, bajo demanda
TOKENS_POR_SEGUNDO = 2000.0     # tokens de salida por segundo con un lote razonable
HORAS_MES = 24 * 30

capacidad_mes = TOKENS_POR_SEGUNDO * 3600 * HORAS_MES / 1e6    # millones de tokens
coste_gpu_mes = PRECIO_GPU_HORA * HORAS_MES
coste_lleno = coste_gpu_mes / capacidad_mes                    # EUR por millon al 100 %

print(round(capacidad_mes, 1))          # -> 5184.0 millones de tokens al mes
print(round(coste_gpu_mes, 2))          # -> 1800.0 EUR al mes
print(round(coste_lleno, 4))            # -> 0.3472 EUR por millon con la GPU llena

# La utilizacion es el divisor: el mismo trabajo, repartido sobre mas o menos capacidad.
for utilizacion in (1.0, 0.6, 0.3, 0.2, 0.1, 0.05):
    print(f"utilizacion {utilizacion:5.0%}  ->  {coste_lleno / utilizacion:7.4f} EUR por millon")
# -> utilizacion  100%  ->   0.3472 EUR por millon
# -> utilizacion   60%  ->   0.5787 EUR por millon
# -> utilizacion   30%  ->   1.1574 EUR por millon
# -> utilizacion   20%  ->   1.7361 EUR por millon
# -> utilizacion   10%  ->   3.4722 EUR por millon
# -> utilizacion    5%  ->   6.9444 EUR por millon

# Cuanta utilizacion hace falta para empatar con cada precio de API.
for precio in (0.10, 0.50, 1.00, 3.00, 15.00):
    print(f"API {precio:6.2f} EUR/M  ->  utilizacion de equilibrio {precio / coste_lleno:.2%}")
# -> API   0.10 EUR/M  ->  utilizacion de equilibrio 28.80%
# -> API   0.50 EUR/M  ->  utilizacion de equilibrio 144.00%
# -> API   1.00 EUR/M  ->  utilizacion de equilibrio 288.00%
# -> API   3.00 EUR/M  ->  utilizacion de equilibrio 864.00%
# -> API  15.00 EUR/M  ->  utilizacion de equilibrio 4320.00%
```

:::claves
- El `1e6` de `capacidad_mes` deja el resultado en **millones de tokens**, no en tokens. Sin él, la capacidad serían 5.184.000.000 y el coste por millón saldría mil millones de veces pequeño: el error típico de comparar peras con manzanas y creer que autoalojar es gratis.
- `coste_lleno` es un **suelo**, no una previsión: es lo que costaría si la GPU estuviera ocupada cada segundo del mes. Ningún sistema real llega ahí, entre otras cosas porque nadie quiere que las peticiones hagan cola detrás de otras.
- Los porcentajes por encima del 100 % no son un error de la fórmula: son la respuesta. Una API de 0,50 €/millón exigiría una GPU ocupada el 144 % del tiempo, y eso no existe. Cuando el número pasa de 100, la conclusión es «no lo hagas» y no «afina más».
- `utilizacion` entra **dividiendo**, así que la relación no es lineal: pasar de 10 % a 20 % ahorra 1,74 € por millón, y pasar de 60 % a 100 % solo ahorra 0,23 €. La primera mitad de la curva es donde está todo el dinero.
- Todas las cifras llevan `round` o formato `:.2%` porque son valores de presentación. Guárdate el número sin redondear para las cuentas siguientes: encadenar redondeos en una comparación de costes es cómo se acaba eligiendo la opción equivocada por dos céntimos.
- `TOKENS_POR_SEGUNDO` es **el parámetro que más se equivoca**. Los 2.000 de este ejemplo corresponden a un modelo de miles de millones de parámetros con lote agrupado; con lote 1 y sin agrupar, la misma GPU sirve una fracción de eso y el coste por token se multiplica. Mídelo en tu hardware, con tu modelo y tu mezcla de entrada y salida.
:::

```python verificable
PRECIO_GPU_HORA = 2.50
TOKENS_POR_SEGUNDO = 2000.0
HORAS_MES = 24 * 30
capacidad_mes = TOKENS_POR_SEGUNDO * 3600 * HORAS_MES / 1e6
coste_gpu_mes = PRECIO_GPU_HORA * HORAS_MES

# Escenario: 20 millones de tokens al dia y picos de diez veces la media.
MEDIA_DIARIA = 20.0
DEMANDA_MES = MEDIA_DIARIA * 30
PICO_SOBRE_MEDIA = 10.0

gpus = DEMANDA_MES / capacidad_mes * PICO_SOBRE_MEDIA
print(round(gpus, 3))                     # -> 1.157 GPUs para aguantar el pico

# En la practica se compran 2: no se alquilan fracciones y hace falta margen. Eso no cambia la
# utilizacion; lo que la cambiaria es que la demanda subiera.
utilizacion = DEMANDA_MES / (capacidad_mes * gpus)
print(f"{utilizacion:.2%}")              # -> 10.00%

# La factura mensual de cada opcion, con los mismos 600 millones de tokens.
for precio in (0.50, 1.00, 3.00, 15.00):
    print(f"API {precio:6.2f} EUR/M  ->  {DEMANDA_MES * precio:9,.0f} EUR al mes")
print(f"propio, 1 GPU            ->  {coste_gpu_mes:9,.0f} EUR al mes")
print(f"propio, 2 GPUs (pico)    ->  {coste_gpu_mes * 2:9,.0f} EUR al mes")
# -> API   0.50 EUR/M  ->        300 EUR al mes
# -> API   1.00 EUR/M  ->        600 EUR al mes
# -> API   3.00 EUR/M  ->      1,800 EUR al mes
# -> API  15.00 EUR/M  ->      9,000 EUR al mes
# -> propio, 1 GPU            ->      1,800 EUR al mes
# -> propio, 2 GPUs (pico)    ->      3,600 EUR al mes

# Los picos SON la utilizacion: la utilizacion de equilibrio es 1 / (pico sobre media).
print(1 / PICO_SOBRE_MEDIA)               # -> 0.1
print(1 / 3.0)                            # -> 0.3333... (con picos de solo 3x)
```

:::claves
- `gpus` sale **fraccionario** (1,157) a propósito: para comparar costes conviene el valor continuo, aunque al comprar haya que redondear hacia arriba. Si se compran 2, la utilización **no** cambia en esta cuenta, porque la demanda es la misma y la capacidad también: el coste por millón sube y la utilización baja solo si divides por las 2 máquinas, que es lo correcto si las tienes encendidas.
- `f"{DEMANDA_MES * precio:9,.0f}"` usa la coma como separador de millares. Es formato de presentación: el número sigue siendo el mismo y no debe volver a entrar en ningún cálculo en forma de cadena.
- `print(1 / PICO_SOBRE_MEDIA)` es la línea que más enseña de todo el bloque: con picos de diez veces la media, la utilización es exactamente 0,1. No hay margen de ingeniería: si compras para el pico, el techo de tu utilización **es** el inverso de la relación pico/media.
- Los `# ->` con `1,800` y `9,000` son el formato inglés del separador de miles; el texto de la página los escribe en la convención española, 1.800 y 9.000. Es el mismo número.
- La comparación de la factura mensual no incluye el coste de ingeniería, supervisión ni las réplicas de alta disponibilidad. Con dos réplicas en lugar de dos máquinas para el pico, el propio pasa a 3.600 € y la conclusión contra la API de 0,50 € no cambia, pero contra la de 3 € sí.
- `DEMANDA_MES = MEDIA_DIARIA * 30` supone un mes de 30 días y tráfico plano dentro de cada día. Si tu tráfico se concentra en ocho horas, los picos dentro del día son peores que los picos entre días y la utilización real baja otra vez.
:::

```python verificable
PRECIO_GPU_HORA = 2.50
TOKENS_POR_SEGUNDO = 2000.0
HORAS_MES = 24 * 30
coste_gpu_mes = PRECIO_GPU_HORA * HORAS_MES

# Palanca 1: cuantizar sube los tokens por segundo del mismo hardware. Los factores son
# orientativos (dependen del modelo y de la GPU); lo que se comprueba aqui es la aritmetica.
for factor, etiqueta in ((1.0, "sin cuantizar"), (1.6, "int8"), (2.3, "int4")):
    tokens_mes = TOKENS_POR_SEGUNDO * factor * 3600 * HORAS_MES / 1e6
    coste = coste_gpu_mes / tokens_mes
    print(f"{etiqueta:14s} {factor:4.1f}x tokens/segundo -> {coste:.4f} EUR por millon al 100%")
# -> sin cuantizar  1.0x tokens/segundo -> 0.3472 EUR por millon al 100%
# -> int8           1.6x tokens/segundo -> 0.2170 EUR por millon al 100%
# -> int4           2.3x tokens/segundo -> 0.1510 EUR por millon al 100%

# Palanca 2: el coste por millon no depende del PRECIO de la hora, depende de la utilizacion.
for precio_hora in (1.00, 2.50, 5.00):
    lleno = (precio_hora * HORAS_MES) / (TOKENS_POR_SEGUNDO * 3600 * HORAS_MES / 1e6)
    print(f"GPU a {precio_hora:4.2f} EUR/h -> coste lleno {lleno:.4f} EUR/M"
          f"   equilibrio contra 3.00 EUR/M: {3.00 / lleno:.2%}")
# -> GPU a 1.00 EUR/h -> coste lleno 0.1389 EUR/M   equilibrio contra 3.00 EUR/M: 2160.00%
# -> GPU a 2.50 EUR/h -> coste lleno 0.3472 EUR/M   equilibrio contra 3.00 EUR/M: 864.00%
# -> GPU a 5.00 EUR/h -> coste lleno 0.6944 EUR/M   equilibrio contra 3.00 EUR/M: 432.00%
```

:::claves
- El ahorro de la cuantización es **proporcional al factor de rendimiento**, no al ahorro de memoria: int8 ocupa la cuarta parte y hace 1,6 veces más tokens por segundo, y el coste baja un 37 %, no un 75 %. La memoria decide si el modelo cabe; el rendimiento decide la factura.
- Los factores 1,6 y 2,3 son **orientativos** y hay que medirlos. En un modelo limitado por ancho de banda de memoria el int8 ayuda mucho; en uno limitado por cómputo, menos. Y si el hardware no tiene instrucciones nativas para el formato, el motor descomprime y no gana nada.
- La segunda cuenta es la que desmonta el argumento de «he encontrado una GPU más barata»: bajar la hora de 2,50 a 1,00 € mejora el coste lleno de 0,347 a 0,139 €, pero **no cambia la utilización**. Si tu utilización es del 10 %, sigues necesitando que la API cueste más de 1,39 €/millón para que salga a cuenta.
- `equilibrio contra 3.00 EUR/M` sale por encima del 100 % en los tres casos y eso no invalida la cuenta: está diciendo que, contra una API de 3 €/millón y con esta utilización del 10 %, autoalojar pierde... salvo que el coste lleno sea mayor que 3 € por millón, cosa que aquí no ocurre. La cuenta se lee como «cuánto tendría que subir la API para que empate».
- El `f"{precio_hora:4.2f}"` fija dos decimales y alinea; el `:.2%` convierte a porcentaje. Ninguno de los dos cambia el valor, solo el texto. Si copias la salida a una hoja de cálculo, vuelve a los números, no a las cadenas.
- Este bloque no mide nada en hardware real: no hay GPU ni modelo. Es aritmética de costes con los parámetros declarados arriba, y por eso va como `verificable`: lo que se comprueba es la fórmula, no el rendimiento.
:::

## Errores típicos

- **Comparar el precio de la GPU por hora con el precio de la API por token.** Son unidades
  distintas y la conversión (tokens por segundo × utilización) es justo donde está el resultado.
  Sin ese paso, cualquier conclusión es azar.
- **Suponer que la GPU estará al 100 %.** El 100 % no existe: hay picos, hay colas, hay
  mantenimiento y hay horas valle. Un modelo realista usa entre el 10 % y el 40 % para tráfico
  interactivo, y ahí el coste por token es de tres a diez veces el mínimo teórico.
- **Dimensionar por la media.** Si compras para la media, en el primer pico el sistema se cae y
  pierdes clientes; si compras para el pico, tu utilización es el inverso de la relación
  pico/media. La decisión de verdad es si puedes **aplanar** la demanda con colas y procesos por
  lotes, no cuántas máquinas comprar.
- **Ignorar el coste de entrada y de salida por separado.** Generar un token cuesta mucho más
  tiempo que procesar uno de entrada, porque la generación es secuencial y la entrada se procesa
  en paralelo. Si tu carga es de 3.000 tokens de entrada por cada 100 de salida, el cuello de
  botella y el coste no se parecen en nada a los de un chatbot.
- **Contar solo la máquina.** El tiempo de ingeniería para montar el servicio, el
  almacenamiento de pesos y registros, la supervisión, la evaluación de cada versión y las
  réplicas de alta disponibilidad no aparecen en la factura de la GPU y suelen pesar más que ella
  en un equipo pequeño. Compáralo con el coste de un ingeniero y verás que la máquina es la parte
  barata.
- **Cuantizar y no volver a medir la calidad.** El ahorro del 37 % es real, y también lo es que la
  métrica cambia. Un modelo destilado o cuantizado se evalúa con el mismo conjunto que el
  original, y si la diferencia importa, no hay ahorro que lo justifique (ver
  [[evaluacion-de-llms|evaluación de LLMs]]).
- **Olvidar la latencia.** Un sistema al 90 % de utilización tiene colas y picos de latencia: el
  coste por token baja y la experiencia del usuario empeora. La utilización objetivo de un servicio
  interactivo es más baja que la de un proceso por lotes, y eso es una decisión de producto, no de
  contabilidad.

:::trampa
El error de comparación más caro es usar la media de tokens por petición y el precio medio de la
API. El coste del propio se dispara con los picos y el de la API con las respuestas largas. Antes
de decidir, mira el percentil 95 de tokens por petición y la distribución horaria del tráfico, no
los promedios: son justo las dos colas las que deciden qué opción es más barata.
:::

## Comprueba que lo sabes

:::quiz
p: Alquilas una GPU por 2,50 €/hora y sirve 2.000 tokens por segundo. Tu carga es de 600 millones de tokens al mes y compras 2 máquinas para aguantar los picos. ¿Cuál es tu coste por millón de tokens?
o: 0,35 €, el coste con la máquina al 100 %
o: Unos 6 €, porque pagas 3.600 € al mes y sirves 600 millones de tokens
o: Depende del precio de la API con la que lo compares
a: 2
e: La factura es 2,50 € · 720 horas · 2 máquinas = 3.600 € al mes, y sirves 600 millones de tokens: 3.600 / 600 = 6 € por millón. El 0,35 € es el suelo teórico con la GPU ocupada cada segundo del mes, que en este escenario está al 10 %. El precio de la API no entra en tu coste: es la referencia contra la que lo comparas, no un componente.
:::

:::quiz
p: Una API cuesta 0,50 € por millón de tokens. Con un coste lleno de 0,347 €/millón, ¿qué utilización necesitarías para que te saliera igual autoalojar?
o: Un 50 %, que es una utilización exigente pero realista
o: Un 144 %, que es imposible: no se puede usar la GPU más del 100 % del tiempo
o: Un 8,6 %, porque 3 / 0,347 es 8,64
a: 2
e: La utilización de equilibrio es `precio_API / coste_lleno` = 0,50 / 0,347 = 1,44, es decir un 144 %. Cuando ese número pasa del 100 %, la conclusión no es «afinemos el cálculo»: es que contra una API de ese precio el autoalojamiento no compite, salvo que subas el rendimiento por GPU o tengas mucha más carga. El 8,64 lo da la API de 3 €/millón: 3 / 0,347 = 8,64, o sea un 864 %, y la opción que dice «8,6 %» divide al revés.
:::

:::quiz
p: Tienes 20 millones de tokens al día de media y picos de diez veces la media. Compras la capacidad para el pico. ¿Qué utilización media te queda, y qué la mejoraría de verdad?
o: Un 10 %, y lo que la mejora es comprar GPUs más baratas
o: Un 10 %, y lo que la mejora es aplanar la demanda, por ejemplo encolando trabajo por lotes en horas valle
o: Un 50 %, porque los picos solo duran un rato
a: 2
e: La utilización queda en `1 / 10 = 10 %`, exactamente el inverso de la relación pico/media, y el precio de la GPU no la cambia: abaratar la hora baja el coste por millón pero deja la utilización igual. Lo único que sube la utilización es meter más tokens en la misma capacidad: aplanar los picos, encolar procesos por lotes fuera de las horas punta o servir con un modelo más pequeño cuando la demanda aprieta.
:::

:::practica
enunciado: Un equipo gasta 400 € al mes en una API a 2 € por millón de tokens de salida. Se plantea autoalojar con una GPU de 3 €/hora que sirve 1.500 tokens por segundo. Si su tráfico es plano (sin picos), ¿cuántas GPUs necesita y a partir de qué demanda mensual le sale mejor el modelo propio?
pista: Calcula primero la capacidad mensual de una GPU y el coste por millón con la máquina al 100 %. Después, la utilización de equilibrio contra el precio de la API.
solucion: Una GPU da 1.500 · 3.600 · 720 / 10⁶ = 3.888 millones de tokens al mes, y su alquiler es 3 · 720 = 2.160 € al mes, así que el coste lleno es 2.160 / 3.888 = 0,556 € por millón con la máquina al 100 %. Tu demanda es 400 / 2 = 200 millones de tokens al mes y cabe en una sola GPU, así que la comparación es 2.160 € de alquiler contra 400 € de API: hoy el propio es cinco veces más caro. El punto de empate es la demanda a la que la API te costaría 2.160 €: 2.160 / 2 = 1.080 millones de tokens al mes, es decir 5,4 veces tu tráfico actual. En ese punto la GPU estaría al 1.080 / 3.888 = 27,8 %, y todavía sería una utilización baja: para tenerla a un 50 % razonable harían falta 1.944 millones de tokens al mes, diez veces lo de hoy. Conclusión: mientras el tráfico no crezca un orden de magnitud, la API es la opción correcta; el coste de la GPU por hora no cambia esa respuesta.
:::

:::nota
Esta página cierra el bloque de coste de la fase 8 por el lado de la infraestructura. La parte de
factura por consulta —tokens de entrada, de salida y caché— está en
[[coste-y-latencia|coste y latencia]], y las dos técnicas que mueven la aguja del rendimiento
están en [[cuantizacion-y-destilacion|cuantización y destilación]] y en
[[exportar-y-servir-modelos|exportar y servir modelos]], donde el batching y la precisión deciden
cuántos tokens por segundo saca la misma máquina. Y si el modelo propio va a manejar datos de
personas, la decisión deja de ser económica: [[privacidad-y-datos-en-llms|privacidad de datos en
LLMs]] es la que manda.
:::
