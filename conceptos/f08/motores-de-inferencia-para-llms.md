---
id: motores-de-inferencia-para-llms
titulo: Servir un LLM en abierto: motores y cuantización
fase: 8
nivel: avanzado
rutas: [ds, de]
prerequisitos: [como-funciona-un-llm, economia-de-la-inferencia-propia, coste-y-latencia]
tags: [inferencia, cuantizacion, gpu, servidores]
resumen: Generar un token está limitado por el ancho de banda de memoria, no por los FLOPs: de ahí salen la cuantización, el lote continuo y la caché de claves.
fuentes: ["Kwon et al. (2023), 'Efficient Memory Management for Large Language Model Serving with PagedAttention'", "Pope et al. (2023), 'Efficiently Scaling Transformer Inference'", "Dettmers et al. (2023), 'QLoRA: Efficient Finetuning of Quantized LLMs'"]
---

## En una frase

Servir un modelo abierto es un problema de **memoria**: hay que meter los pesos y la caché de claves
en la tarjeta, y cada token generado obliga a releer todo lo que ocupa, así que se gana comprimiendo
los pesos, agrupando peticiones y midiendo cuánto ocupa de verdad el contexto de cada una.

## La idea

Cuando pediste prestada una GPU para entrenar, el cuello de botella eran las operaciones: la tarjeta
estaba llena de multiplicaciones y el trabajo se medía en FLOPs. Servir un modelo es lo contrario, y
entenderlo es la mitad de la página.

Generar texto tiene dos fases que se comportan de forma opuesta:

- **Prellenado** (*prefill*). El modelo lee toda la entrada de golpe. Cada token nuevo atiende a
  todos los anteriores, así que hay muchísimo trabajo por token y las matrices se multiplican de
  forma densa. Esta fase sí es intensiva en cómputo.
- **Decodificación** (*decode*). Se genera un token, luego otro, luego otro. Cada token depende del
  anterior: es estrictamente secuencial, y no hay forma de calcular dos a la vez. Para producir **un**
  token hay que leer **toda** la matriz de pesos y toda la caché de claves.

Ahí está el hallazgo que ordena todo lo demás: en la decodificación, la tarjeta calcula casi nada y
espera a la memoria. El tiempo por token no lo marca la capacidad de cálculo, sino el **ancho de
banda**: cuántos gigabytes por segundo puede mover la tarjeta. Con pesos de 13,04 GiB en una tarjeta
que mueve 900 GB/s, cada token exige leer 13,04 GiB y por tanto tarda, como mínimo, unos 14,5 ms.
Unos 69 tokens por segundo, con la GPU prácticamente ociosa calculando. Está esperando a la memoria.

:::nota
En toda la página se miden los pesos en **gibibytes** (GiB, potencias de 1024), que es lo que
devuelven las cuentas de memoria, y el ancho de banda en **gigabytes** por segundo (GB/s, potencias
de 1000), que es como lo publican los fabricantes. La diferencia entre las dos convenciones es del
7 %, así que confundirlas no cambia ninguna decisión; ignorarla hace que las cifras no cuadren.
:::

De ese diagnóstico salen las tres palancas reales, y ninguna es «comprar más FLOPs»:

1. **Comprimir los pesos.** Si el modelo ocupa la mitad, hay que leer la mitad y se genera el doble
   de rápido. Es lo que hace la **cuantización**.
2. **Agrupar peticiones.** Si la tarjeta lee los pesos una vez por token, que esa lectura sirva para
   ocho secuencias en lugar de una. El trabajo de memoria no cambia y la producción se multiplica.
3. **Gestionar bien la caché de claves.** El contexto de cada conversación ocupa memoria y crece con
   cada token. Una gestión mala la fragmenta y te deja fuera peticiones que sí cabrían.

La cuantización consiste en guardar los pesos con menos bits por número. En lugar de 16 bits por
peso, 8 o 4. El ahorro es aritmética pura: un modelo de 7.000 millones de parámetros ocupa 13,04 GiB a
16 bits, 6,52 GiB a 8 bits y 3,26 GiB a 4 bits, más una pequeña tabla de escalas que se guarda junto a
cada bloque de pesos. El precio se paga en precisión: cada peso ya no es el que se entrenó, y en
formatos agresivos la calidad se resiente. La regla de trabajo es que **la cuantización se mide, no
se supone**: se aplica, se evalúa con el mismo conjunto de evaluación del modelo original y se
compara.

El tercer frente, el que más cuesta ver, es la caché de claves. Cada token que ya se ha procesado
guarda dos vectores por capa y por cabeza de atención: la clave y el valor. Sin ella habría que
recalcular todo el contexto en cada token. Con ella, el coste de memoria crece de forma lineal con el
contexto y con el número de secuencias simultáneas. Un modelo de 7.000 millones de parámetros con 32
capas, 32 cabezas y una dimensión de cabeza de 128 ocupa 0,5 MB por token en 16 bits: 1,95 GiB por cada
conversación de 4.000 tokens. Diez conversaciones simultáneas son 19,5 GiB solo de caché, más que los
pesos del modelo entero. Ese es el motivo de que existan gestores de memoria dedicados, que reparten
la caché en bloques de tamaño fijo y los van asignando a medida que hacen falta, como hace un sistema
operativo con la memoria virtual.

Y el lote continuo: en lugar de esperar a que terminen todas las peticiones del lote, el motor mete
una nueva en cuanto se libera un hueco, token a token. Con eso la tarjeta no se queda esperando a la
petición más larga del grupo. Es la diferencia entre una utilización del 10 % y una del 60 %, y no
consiste en cambiar de tarjeta.

Conviene ver las dos caras del trade-off antes de escribir código, porque se mueven en direcciones
opuestas:

:::figura
fichero: motores-memoria-y-lote
pie: Arriba a la izquierda, cuánto ocupan los pesos de un modelo de 7.000 millones de parámetros según los bits por peso: de 26,08 GiB en coma flotante de 32 bits a 3,26 GiB en 4 bits, que es lo que decide si el modelo cabe en la tarjeta o no; la línea negra marca los 24 GiB nominales. Arriba a la derecha, los tokens por segundo por secuencia si el cuello de botella es el ancho de banda de memoria: comprimir los pesos de 16 a 4 bits multiplica por cuatro la velocidad de generación, con la misma tarjeta. Abajo a la izquierda, qué pasa al agrupar peticiones: el tiempo por token crece de forma suave, pero los tokens por segundo del conjunto suben hasta que la tarjeta se satura. Abajo a la derecha, cómo se reparte la memoria de la tarjeta: los pesos son un coste fijo y la caché de claves crece con el contexto, así que la pregunta «cuántas conversaciones caben» se contesta restando, no adivinando.
fuente: figuras/motores-de-inferencia-para-llms-1.py
:::

## Definición formal

Todo el cálculo de capacidad sale de una suma de cuatro términos que tienen que caber en la memoria
de la tarjeta:

:::formula
M_pesos + M_caché + M_activaciones + M_reserva ≤ M_gpu
:::

El peso de los pesos es directamente el número de parámetros por los bits de cada uno:

:::formula
M_pesos = N_parámetros · bits / 8        M_caché = 2 · L · n_cabezas · d_cabeza · bits_kv · (contexto · lotes)
:::

Y el tiempo por token de la decodificación, si manda el ancho de banda, es el volumen que hay que
leer dividido por la velocidad a la que se puede leer:

:::formula
t_token ≈ (M_pesos + M_caché) / B        tokens_por_segundo ≈ B / (M_pesos + M_caché)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `N_parámetros` | Parámetros del modelo: 7.000 millones, 70.000 millones | cuentas | Sube el coste de memoria de forma lineal. El doble de parámetros es el doble de peso que leer por token, así que la velocidad de generación cae a la mitad con la misma tarjeta |
| `bits` | Bits por peso: 32, 16, 8 o 4 | bits | Bajarlo reduce `M_pesos` proporcionalmente y acelera la decodificación, pero quita precisión. A 4 bits un modelo de 7.000 millones baja de 13,04 GiB a 3,26 GiB |
| `M_gpu` | Memoria de la tarjeta, por ejemplo 24 GiB | gibibytes | Es el techo de la suma. Todo lo demás se decide restando de aquí: no hay configuración que haga caber lo que no cabe |
| `L` | Capas del transformer | capas | Cada capa guarda su propia caché de claves, así que la caché crece de forma lineal con `L`. Es el término que más crece cuando se alarga el contexto |
| `contexto` | Tokens que ya tiene la conversación | tokens | La caché crece con él de forma lineal. Un contexto de 32.000 tokens ocupa ocho veces más que uno de 4.000, en **cada** secuencia simultánea |
| `lotes` | Secuencias que se atienden a la vez | secuencias | Multiplica la caché y no toca los pesos. Esa es toda la gracia: el coste fijo se reparte entre más trabajo, hasta que la memoria se agota o el cálculo empieza a mandar |
| `B` | Ancho de banda de memoria de la tarjeta | gigabytes por segundo | Es el divisor del tiempo por token en la decodificación. Es la cifra que hay que mirar antes que los TFLOPS al elegir tarjeta para servir |
| `t_token` | Tiempo para generar un token | milisegundos | Es el inverso de la velocidad por secuencia. Con 13,04 GiB de pesos y 900 GB/s no baja de 14,5 ms, haga lo que haga el resto del sistema |
| `tokens_por_segundo` | Velocidad de generación de una secuencia | tokens por segundo | En decodificación es `B` dividido entre lo que hay que leer. En prellenado manda otra cosa (los FLOPs) y la cifra es mucho mayor |
:::

Y la latencia que percibe la persona es la suma de las dos fases, con el primer token como frontera:

:::formula
t_primer_token ≈ t_prellenado(contexto)        t_total ≈ t_primer_token + n_salida · t_token
:::

## Ejemplo

Un equipo sirve un modelo abierto de 7.000 millones de parámetros en una tarjeta de 24 GiB con 900 GB/s
de ancho de banda. La cuenta de capacidad, término a término:

| Concepto | En 16 bits | En 4 bits |
| --- | --- | --- |
| Pesos | 13,04 GiB | 3,26 GiB |
| Caché de claves (contexto 4.000, 1 secuencia) | 1,95 GiB | 1,95 GiB |
| Activaciones y reserva del motor | 2,00 GiB | 2,00 GiB |
| Total con una secuencia | 16,99 GiB | 7,21 GiB |
| Margen para más caché | 8,96 GiB | 18,74 GiB |
| Secuencias simultáneas a 4.000 tokens | 4 | 9 |
| Secuencias simultáneas a 16.000 tokens | 1 | 2 |

La última fila es la que decide el producto: en 16 bits y contexto largo, **una** conversación. Con el
modelo cuantizado a 4 bits, dos. No es una mejora de rendimiento, es la diferencia entre un servicio
que atiende una conversación larga y uno que atiende dos con la misma tarjeta. Y fíjate en la fila
del margen: 8,96 GiB de 24 no son un error de suma, son los 13,04 GiB de pesos y los 2 GiB de
activaciones que ya estaban gastados antes de guardar un solo token de contexto.

Y ahora la velocidad, con el mismo modelo:

| Formato | Pesos que se leen por token | Tiempo mínimo por token | Tokens por segundo por secuencia |
| --- | --- | --- | --- |
| 16 bits | 13,04 GiB | 14,5 ms | 69 |
| 8 bits | 6,52 GiB | 7,2 ms | 138 |
| 4 bits | 3,26 GiB | 3,6 ms | 276 |

Estos números son la **cota inferior** que impone el ancho de banda: en la práctica se pierde algo en
lanzar las operaciones, así que un motor real rinde menos. Lo que importa es la dirección: el tiempo
por token es proporcional a lo que ocupan los pesos, así que comprimirlos acelera la generación casi
en la misma proporción. Y el coste de esa compresión se paga en calidad, que se mide con el mismo
conjunto de evaluación que usaste para elegir el modelo.

El segundo efecto, el del lote, explica por qué agrupar es la palanca de la factura. Con el modelo en
16 bits y 16,7 ms por token en régimen de una sola secuencia, atender cuatro secuencias a la vez
cuesta 23,2 ms por token, no cuatro veces más: los 13,04 GiB de pesos se leen una sola vez por paso y
sirven para las cuatro, así que el conjunto pasa de 60 a 173 tokens por segundo. La memoria de la
caché, en cambio, sí se multiplica: 7,80 GiB para cuatro secuencias de 4.000 tokens. Es un intercambio
explícito, se cambia memoria por rendimiento.

Y la letra pequeña que arruina las cuentas optimistas: **las peticiones no tienen la misma longitud**.
Si metes en el mismo lote una consulta de 200 tokens de entrada y otra de 20.000, el trabajo de
prellenado se desequilibra y la tarjeta espera. De ahí que los motores modernos repartan la memoria
en bloques y vayan metiendo peticiones nuevas en los huecos que se liberan, en lugar de esperar a que
termine todo el lote. Antes de elegir motor, mide la **distribución** de contextos de tu tráfico: con
contextos parecidos cualquier motor vale, con una distribución muy abierta la diferencia entre
motores se nota en la factura.

## Código

```python verificable
# Cuanto ocupa un modelo y cuantas secuencias caben: la cuenta que decide si el servicio
# es viable antes de escribir una linea de codigo.
M_GPU = 24.0                 # GiB de la tarjeta
N_PARAMETROS = 7.0e9         # 7.000 millones de parametros
BYTES_POR_GB = 1024 ** 3

# Pesos del modelo: parametros por bits dividido entre 8. La tabla de escalas de la
# cuantizacion anade un poco, pero es un porcentaje pequeno y se deja fuera del calculo.
for bits in (32, 16, 8, 4):
    gb = N_PARAMETROS * bits / 8 / BYTES_POR_GB
    print(f"{bits:2d} bits -> {gb:6.2f} GiB de pesos   "
          f"{'cabe' if gb < M_GPU else 'NO CABE en la tarjeta'}")
# -> 32 bits ->  26.08 GiB de pesos   NO CABE en la tarjeta
# -> 16 bits ->  13.04 GiB de pesos   cabe
# ->  8 bits ->   6.52 GiB de pesos   cabe
# ->  4 bits ->   3.26 GiB de pesos   cabe

# La cache de claves crece con el contexto y con el numero de secuencias simultaneas.
# Modelo con 32 capas de atencion y dimension de cabeza de 128.
def cache_gb(segundos_contexto_tokens, bits_kv=16, lotes=1, capas=32, dim_cabeza=128, cabezas=32):
    bytes_por_token = 2 * capas * cabezas * dim_cabeza * bits_kv / 8
    return segundos_contexto_tokens * bytes_por_token * lotes / BYTES_POR_GB

for contexto in (4_000, 16_000, 32_000):
    print(f"contexto {contexto:6d} -> cache de {cache_gb(contexto):5.2f} GiB por secuencia")
# -> contexto   4000 -> cache de  1.95 GiB por secuencia
# -> contexto  16000 -> cache de  7.81 GiB por secuencia
# -> contexto  32000 -> cache de 15.62 GiB por secuencia

# Cuantas secuencias caben: el margen que queda despues de pesos, activaciones y reserva.
ACTIVACIONES = 2.0
for bits in (16, 8, 4):
    pesos = N_PARAMETROS * bits / 8 / BYTES_POR_GB
    margen = M_GPU - pesos - ACTIVACIONES
    for contexto in (4_000, 16_000):
        caben = int(margen / cache_gb(contexto))
        print(f"{bits:2d} bits, contexto {contexto:6d} -> margen {margen:5.2f} GiB, "
              f"caben {caben} secuencias")
# -> 16 bits, contexto   4000 -> margen  8.96 GiB, caben 4 secuencias
# -> 16 bits, contexto  16000 -> margen  8.96 GiB, caben 1 secuencias
# ->  8 bits, contexto   4000 -> margen 15.48 GiB, caben 7 secuencias
# ->  8 bits, contexto  16000 -> margen 15.48 GiB, caben 1 secuencias
# ->  4 bits, contexto   4000 -> margen 18.74 GiB, caben 9 secuencias
# ->  4 bits, contexto  16000 -> margen 18.74 GiB, caben 2 secuencias
```

:::claves
- `N_PARAMETROS * bits / 8` da **bytes**, y `BYTES_POR_GB` los pasa a gibibytes. Ese `1024 ** 3` es la diferencia entre 13,04 GiB y 14 GB: el mismo número con dos convenciones. Los fabricantes de tarjetas mezclan las dos, así que conviene calcular siempre en GiB y comparar contra la memoria real disponible, que es menor que la nominal.
- `M_GPU = 24.0` es memoria **nominal**. El motor reserva parte para su propio estado y el sistema operativo se queda con otra: en la práctica hay que dejar un 10 % de margen. Si el cálculo da 23,8 GiB de 24, el servicio no arranca.
- La caché de claves se cuenta con `2 * capas * cabezas * dim_cabeza`: dos vectores (clave y valor) por capa y por cabeza. Con 32 capas, 32 cabezas y dimensión 128, cada token cuesta 0,5 MB en 16 bits. Multiplicar por 32.000 tokens da 15,62 GiB: la caché de una sola conversación larga puede pesar más que un modelo cuantizado entero.
- `int(margen / cache_gb(contexto))` trunca hacia abajo a propósito. Caben 1,8 secuencias significa que caben 1: redondear hacia arriba es la forma de que el servicio se caiga en producción.
- Con 8 bits y contexto 16.000 el resultado es 1 secuencia, igual que con 16 bits. La cuantización ayuda, pero **no cambia el orden de magnitud** cuando el contexto es muy largo: la caché crece con el contexto y no se comprime sola.
- Los números de `bits_kv` para la caché se dejan en 16 en todos los casos, que es lo habitual: los pesos se cuantizan y la caché se guarda en precisión alta, porque comprimirla degrada más la calidad.
:::

```python verificable
# El modelo de tiempo por token cuando manda el ancho de banda: por que agrupar sale
# casi gratis y por que la cuantizacion acelera la generacion.
B_GB_S = 900.0               # ancho de banda de la tarjeta, GB/s
PESOS_16BITS = 13.04         # GiB de pesos
PESOS_4BITS = 3.26           # GiB de pesos
CACHE_POR_SECUENCIA = 1.95   # GiB con 4.000 tokens de contexto

def ms_por_token(pesos_gib, cache_gib, lotes=1):
    # Se leen los pesos una vez por paso (sirven para todo el lote) y la cache de cada
    # secuencia, que si se paga entera por secuencia.
    return (pesos_gib + cache_gib * lotes) / B_GB_S * 1000

for bits, pesos in (("16 bits", PESOS_16BITS), ("4 bits", PESOS_4BITS)):
    t = ms_por_token(pesos, 0.0)
    print(f"{bits}: {t:5.1f} ms por token -> {1000 / t:6.1f} tokens por segundo")
# -> 16 bits:  14.5 ms por token ->   69.0 tokens por segundo
# ->  4 bits:   3.6 ms por token ->  276.1 tokens por segundo

# El lote no multiplica el tiempo: los pesos se leen una vez y sirven para todos.
print("lote  tiempo_por_token  tokens_por_segundo_del_conjunto")
for lotes in (1, 2, 4, 8, 16):
    t = ms_por_token(PESOS_16BITS, CACHE_POR_SECUENCIA, lotes)
    print(f"{lotes:4d}  {t:15.1f}  {lotes * 1000 / t:28.1f}")
# -> lote  tiempo_por_token  tokens_por_segundo_del_conjunto
# ->    1             16.7                          60.0
# ->    2             18.8                         106.3
# ->    4             23.2                         172.7
# ->    8             31.8                         251.4
# ->   16             49.2                         325.5

# Y de donde sale la memoria que ocupa cada lote: la cache si se multiplica.
for lotes in (4, 8, 16):
    print(f"  lote {lotes:2d} -> {lotes * CACHE_POR_SECUENCIA:5.2f} GiB de cache")
# -> lote 4 ->  7.80 GiB de cache
# -> lote 8 -> 15.60 GiB de cache
# -> lote 16 -> 31.20 GiB de cache
# ojo: el lote 16 pide 31,20 GiB de cache y no cabe en una tarjeta de 24
```

:::claves
- La diferencia entre las dos fórmulas es `cache_gib * lotes` frente a `pesos_gib`: los pesos entran **una vez** en la suma y la caché una vez **por secuencia**. Todo el negocio de agrupar está en ese detalle, y todo el límite también.
- Los tokens por segundo del conjunto salen de `lotes * 1000 / t`. Fíjate en que con lote 16 el tiempo por token se triplica (de 16,7 a 49,2 ms) pero el conjunto produce más de cinco veces más: 325,5 frente a 60,0. Agrupar empeora la latencia individual y mejora el rendimiento agregado, y esas dos cosas se eligen según el producto.
- `1000 / t` convierte milisegundos por token en tokens por segundo. Es el inverso, no una división por mil: si tarda 14,5 ms en cada token, hace 69 por segundo.
- Los 31,20 GiB de caché del último caso no caben en la tarjeta de 24 GiB junto a los 13,04 GiB de pesos. El cálculo lo dice antes de intentarlo: **el límite real del lote es la memoria, no el ancho de banda**. Primero se agrupa hasta donde deja la memoria, y solo después se mira si la tarjeta se satura.
- Aquí no hay ninguna medición de hardware: es el modelo de ancho de banda con las constantes declaradas arriba. Un motor real pierde entre un 10 % y un 40 % por lanzamiento de operaciones y desequilibrio del lote, así que estas cifras son una cota optimista y sirven para comparar configuraciones, no para prometer latencias.
- `PESOS_16BITS = 13.04` viene del bloque anterior: un modelo de 7.000 millones de parámetros. Si cambias de modelo, cambia esta constante y todas las cuentas de la página se recalculan solas.
:::

```python verificable
# Medir en vez de suponer: la cuantizacion se evalua. Este bloque compara una senal
# sintetica de calidad y de velocidad para dejar claro que las dos se miden juntas.
import numpy as np

rng = np.random.default_rng(3)

# "Calidad": la discrepancia entre lo que daria un modelo de referencia y lo que da el
# cuantizado. Aqui se simula con ruido proporcional a lo agresivo del formato.
FORMATOS = {"16 bits": (0.000, 1.00), "8 bits": (0.010, 1.28), "4 bits": (0.045, 1.60)}

print("formato   error_medio   acierto   tokens_por_segundo")
for nombre, (ruido, factor) in FORMATOS.items():
    referencia = rng.normal(1.0, 0.30, size=2_000)
    cuantizado = referencia + rng.normal(0.0, ruido, size=2_000)
    error = float(np.abs(cuantizado - referencia).mean())
    # El acierto se simula como la fraccion de casos que quedan dentro de una tolerancia.
    acierto = float((np.abs(cuantizado - referencia) < 0.05).mean())
    print(f"{nombre:9s} {error:11.4f}   {acierto:7.3f}   {69.0 * factor:17.1f}")
# -> formato   error_medio   acierto   tokens_por_segundo
# -> 16 bits      0.0000     1.000                69.0
# -> 8 bits       0.0080     1.000                88.3
# -> 4 bits       0.0362     0.736               110.4

# La decision no sale de la tabla sola: hay un umbral de acierto por debajo del cual
# el ahorro de velocidad no compensa. Aqui, el 90 %.
UMBRAL_ACIERTO = 0.90
for nombre, (ruido, factor) in FORMATOS.items():
    referencia = rng.normal(1.0, 0.30, size=2_000)
    cuantizado = referencia + rng.normal(0.0, ruido, size=2_000)
    acierto = float((np.abs(cuantizado - referencia) < 0.05).mean())
    velocidad = 69.0 * factor
    print(f"{nombre:9s} acierto {acierto:5.3f}  velocidad {velocidad:5.1f}  "
          f"{'vale' if acierto >= UMBRAL_ACIERTO else 'no vale: se pierde calidad'}")
# -> 16 bits acierto 1.000  velocidad  69.0  vale
# ->  8 bits acierto 1.000  velocidad  88.3  vale
# ->  4 bits acierto 0.723  velocidad 110.4  no vale: se pierde calidad
```

:::claves
- Este bloque no mide un modelo real: el ruido es sintético y las cifras de velocidad son proporciones fijas. Lo que enseña es el **procedimiento**, que es lo que se traslada a producción: se define una métrica de calidad, se mide la del formato original, se mide la del cuantizado y se comparan con un umbral escrito de antemano.
- `rng.normal(0.0, ruido, size=2_000)` con `ruido = 0.0` devuelve ceros, así que el error medio del formato de 16 bits es exactamente 0,0000. Es la comprobación de que el código funciona: si el «original» tuviera error, el experimento estaría mal montado.
- El umbral (`UMBRAL_ACIERTO = 0.90`) se fija **antes** de mirar los resultados. Si se elige después de ver la tabla, se acaba justificando la decisión que ya se quería tomar: es el mismo vicio que en cualquier validación de modelo.
- Con una tolerancia de 0,05, `4 bits` deja fuera más de una cuarta parte de los casos: el acierto baja a 0,723. La lección práctica es que la cuantización agresiva no falla en promedio, falla en la cola, y la cola es justo donde están las consultas que importan.
- El error medio y el acierto se imprimen juntos porque solo tienen sentido juntos. Un error medio bajo con un acierto bajo significa que hay pocos casos muy malos, que suele ser el patrón de la cuantización a 4 bits.
- La velocidad se multiplica por un factor fijo (1,00, 1,28 y 1,60) en lugar de medirse. En un banco de pruebas real se mide con el mismo prompt, la misma salida y el mismo motor, y se repite varias veces: la primera ejecución incluye la carga del modelo y no vale como medida.
:::

## Errores típicos

- **Elegir la tarjeta por los TFLOPS.** La decodificación está limitada por el ancho de banda de
  memoria. Una tarjeta con más cómputo y menos ancho de banda puede generar **más despacio**. Mira
  primero `B`, después la memoria, y el cómputo al final.
- **Cuantizar y no volver a evaluar.** El ahorro de memoria es seguro; el de calidad no. Un modelo a 4
  bits se evalúa con el mismo conjunto que el original, y si la métrica baja, el ahorro no sirve.
- **Olvidar la caché de claves al presupuestar memoria.** Los pesos son el número que todo el mundo
  calcula y la caché es la que rompe el servicio: 1,95 GiB por conversación de 4.000 tokens en un
  modelo de 7.000 millones, y crece con cada token y con cada usuario a la vez.
- **Cuantizar un modelo que no es el cuello de botella.** Si tu latencia se va en el prellenado de
  contextos largos, comprimir los pesos acelera la parte que no te está frenando. Mide primero qué
  fase manda: primer token o generación.
- **Suponer que todas las peticiones son iguales.** Un lote con una consulta de 200 tokens y otra de
  20.000 desequilibra la tarjeta. Mide la distribución de contextos de tu tráfico real antes de
  elegir motor y tamaño de lote.
- **Confundir el primer token con la velocidad.** El tiempo hasta el primer token depende del
  prellenado; la velocidad de generación, de la decodificación. Un cambio puede mejorar uno y
  empeorar el otro, y hay que medir los dos por separado.
- **Prometer una latencia con una cota teórica.** El cálculo de ancho de banda es el mínimo posible.
  Un servicio real añade colas, lanzamiento de operaciones y desequilibrio del lote. Presupuesta con
  margen y verifica con carga.

:::aviso
Servir un modelo abierto es asumir su mantenimiento: actualizaciones del motor, avisos de seguridad
de las dependencias, parches del sistema y una GPU que hay que vigilar. Antes de montarlo, compara el
coste total con pagar por token: muchas veces el servicio propio gana en control y en privacidad, y
pierde en dinero. La decisión completa está en
[[economia-de-la-inferencia-propia|economía de la inferencia propia]].
:::

:::trampa
El error más caro es medir con el modelo recién cargado y el primer lote. La primera ejecución
incluye la compilación de los núcleos y la carga de los pesos, y da cifras tres o cuatro veces
peores que el régimen estable. Calienta el motor con una docena de peticiones antes de cronometrar
nada, y repite la medida varias veces.
:::

## Comprueba que lo sabes

:::quiz
p: Duplicas el número de tokens por segundo que necesitas y compras una tarjeta con el doble de TFLOPS. ¿Qué pasa con la velocidad de generación?
o: Se duplica, porque la decodificación es intensiva en cómputo
o: Casi nada: la decodificación está limitada por el ancho de banda de memoria, que es el que marca cuánto tarda en releer los pesos en cada token
o: Se reduce, porque más cómputo implica más consumo y menos frecuencia
a: 2
e: Generar cada token exige releer todos los pesos y la caché, y el tiempo lo fija el ancho de banda, no la capacidad de cálculo. En la fase de decodificación la tarjeta está casi ociosa en cómputo. Lo que sí ayuda es comprimir los pesos (cuantizar), agrupar peticiones para repartir la misma lectura o reducir el contexto.
:::

:::quiz
p: Un modelo de 7.000 millones de parámetros con 32 capas y dimensión de cabeza 128 atiende conversaciones de 16.000 tokens. ¿Por qué la caché de claves puede ser el límite antes que los pesos?
o: Porque la caché se guarda en disco y es más lenta
o: Porque ocupa unos 7,8 GiB por conversación y crece con el contexto y con cada secuencia simultánea, mientras que los pesos son un coste fijo que se puede comprimir
o: Porque la caché hay que recalcularla en cada token
a: 2
e: La caché son dos vectores por capa y por cabeza por cada token ya procesado: unos 0,5 MB por token en 16 bits, es decir 7,81 GiB para 16.000 tokens en una sola conversación. Los pesos, en cambio, se pagan una vez y se pueden cuantizar. Cuando el contexto es largo, la caché manda. La tercera opción es justo lo que la caché evita: para eso existe.
:::

:::quiz
p: Pasas el modelo de 16 bits a 4 bits y la velocidad por secuencia casi se cuadruplica. ¿Qué falta antes de desplegarlo?
o: Nada: si es más rápido y ocupa menos, es mejor en todo
o: Medir la calidad con el mismo conjunto de evaluación del modelo original, porque la cuantización agresiva cambia las respuestas
o: Comprobar que la tarjeta soporta 4 bits, que es lo único que puede fallar
a: 2
e: El ahorro de memoria y de tiempo es aritmética; el de calidad hay que medirlo. Un formato agresivo puede mantener la media y fallar en la cola, que es donde están los casos difíciles. Lo de la compatibilidad del hardware también importa, pero no es la comprobación que decide: un modelo rápido que responde peor no es una mejora.
:::

:::quiz
p: Con 13,04 GiB de pesos y 900 GB/s de ancho de banda, generar un token tarda unos 14,5 ms. ¿Por qué agrupar 8 peticiones no multiplica el tiempo por 8?
o: Porque el motor reparte el trabajo entre varios núcleos
o: Porque los pesos se leen una sola vez por paso y esa lectura sirve para todas las secuencias del lote; lo que sí se multiplica es la caché de claves
o: Porque las peticiones del lote se atienden en serie y se solapan
a: 2
e: En cada paso de decodificación los pesos se leen una vez, y esa lectura alimenta a todo el lote: el coste fijo se reparte. El término que crece con el número de secuencias es la caché de claves, y por eso el límite real del lote es la memoria de la tarjeta. Repartir entre núcleos no cambia el ancho de banda disponible, que es el recurso escaso.
:::
