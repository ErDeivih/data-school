---
id: ci-cd
titulo: Integración y despliegue continuos
fase: 11
nivel: intermedio
rutas: [alg, de]
prerequisitos: [git-para-datos, testing-piramide]
tags: [ci, cd, automatizacion, despliegue]
resumen: Automatizar pruebas, construcción y publicación para que integrar deje de ser un acontecimiento: qué corre en cada fase y qué se construye una sola vez.
fuentes: ["Humble, Farley (2010), 'Continuous Delivery'", "Forsgren, Humble, Kim (2018), 'Accelerate'"]
---

## En una frase

Integración continua significa que cada cambio se prueba y se construye solo, sin que nadie
tenga que acordarse; despliegue continuo significa que ese artefacto llega a producción por un
camino automático, repetible y reversible.

## La idea

Sin automatización, integrar es un acontecimiento: cada persona trabaja semanas en su rama, y
el día de la verdad se juntan cinco cambios que nadie ha probado juntos. Ese día se descubre
que dos migraciones chocan, que una dependencia subió de versión y que el entorno de pruebas
llevaba tres semanas roto sin que nadie lo mirara. El coste de arreglarlo crece con el tiempo
que ha estado escondido.

La integración continua cambia la unidad de trabajo: **la rama principal siempre está verde y
desplegable**, y para conseguirlo cada empujón dispara el mismo proceso. Un proceso así tiene
dos virtudes que no se ven a simple vista. La primera es que el fallo aparece cerca del cambio
que lo causó: si algo se rompe, sabes que fue el último empujón, no una de las cuarenta cosas
que cambiaron esta semana. La segunda es que convierte el entorno en código: si el pipeline
funciona en una máquina limpia, funciona en la tuya y en la de producción.

Conviene separar dos cosas que se llaman igual:

- **Entrega continua** (*continuous delivery*): cada cambio que pasa el pipeline queda
  **desplegable**. El despliegue a producción existe, está automatizado y probado, pero lo
  dispara una persona cuando quiere.
- **Despliegue continuo** (*continuous deployment*): además, se despliega solo. Eso exige
  confianza en las pruebas y capacidad de revertir rápido, y no todos los dominios la tienen:
  en un sistema con dinero o con datos de salud, la puerta humana puede ser una decisión
  deliberada, no una carencia.

Un pipeline tiene fases con naturalezas distintas: análisis estático y formato (segundos),
pruebas unitarias (segundos o minutos), pruebas de integración contra una base de datos real
levantada en un contenedor ([[contenedores]]), pruebas de contrato entre servicios, pruebas de
extremo a extremo (lentas y frágiles), construcción de la imagen, publicación en el registro y
despliegue por entornos. El orden importa: **lo que tarda poco y falla mucho va primero**,
porque lo que se optimiza no es la duración total del pipeline, sino el tiempo que un
desarrollador tarda en saber que ha roto algo.

Y una regla que evita la mitad de los incidentes: **se construye una vez y se promueve el mismo
artefacto**. Si reconstruyes para producción, lo que despliegas no es lo que probaste, aunque
el código sea el mismo. La diferencia entre entornos es configuración y secretos
([[secretos-y-configuracion]]), nunca una compilación distinta.

## Definición formal

**El pipeline como grafo.** Un pipeline es un conjunto de etapas con dependencias; una etapa se
ejecuta solo si todas sus dependencias han terminado bien. Si una falla, las que dependen de
ella no corren y el resultado es «rojo».

**Tiempo esperado hasta saber que algo falla.** Con `k` etapas en serie, `d_j` la duración de
la etapa `j` y `p_j` la probabilidad de que falle:

:::formula
E[T] = ( Σⱼ [ Πᵢ<ⱼ (1 − pᵢ) ] · pⱼ · (d₁ + … + dⱼ) ) / (1 − Πᵢ (1 − pᵢ))
:::

- `d_j` — duración típica de la etapa `j` en segundos.
- `p_j` — probabilidad de que la etapa `j` falle en una ejecución cualquiera (se estima con el
  histórico de fallos).
- `Πᵢ<ⱼ (1 − pᵢ)` — probabilidad de que la ejecución llegue hasta la etapa `j`; es el factor
  que pondera.
- `1 − Πᵢ (1 − pᵢ)` — probabilidad de que algo falle. Se divide por ella para obtener la media
  **condicionada a que haya fallo**, que es el caso que le importa a quien espera el resultado.

**Reproducibilidad.** Un artefacto es reproducible si el mismo contenido de código, las mismas
dependencias y el mismo entorno de construcción producen el mismo digest:

:::formula
digest = H(fuente, dependencias_fijadas, imagen_de_construcción)
:::

Si la lista de dependencias no está fijada (por ejemplo `pip install pandas` sin fichero de
bloqueo), el segundo término cambia solo y el digest también. Ahí se acaba la reproducibilidad
y con ella la promoción del mismo artefacto.

**Promoción.** Un despliegue es una pareja de artefacto y configuración:

:::formula
despliegue(entorno) = digest_del_artefacto + configuración(entorno)
:::

El digest es idéntico en todos los entornos; lo que cambia es la configuración.

**Indicadores del proceso.** El marco habitual mide cuatro cosas: frecuencia de despliegue,
tiempo desde el commit hasta producción, porcentaje de despliegues que causan un fallo y tiempo
de recuperación. Son indicadores del sistema, no de las personas: sirven para saber si el
pipeline ayuda o estorba.

## Ejemplo

Cuatro etapas con estas duraciones y probabilidades de fallo (cifras de este ejemplo, tomadas
de un histórico imaginario):

| Etapa | Duración | Probabilidad de fallo |
| --- | --- | --- |
| extremo a extremo | 600 s | 0,05 |
| integración | 240 s | 0,15 |
| unitarias | 40 s | 0,25 |
| análisis estático | 5 s | 0,02 |

- Si el pipeline corre en el orden «extremo a extremo → integración → unitarias → análisis
  estático», la media de tiempo hasta el primer fallo es de unos 832 s. Casi catorce minutos
  esperando para enterarte de que faltaba un espacio en blanco.
- Si se ordena por coste por unidad de probabilidad de fallo (unitarias, análisis estático,
  integración, extremo a extremo), la misma media baja a unos 172 s, casi cinco veces menos.
- El pipeline completo cuando todo va bien tarda 885 s en los dos órdenes: lo que se ha
  mejorado no es el caso bueno, es el caso frecuente.

Y el segundo ejemplo, el artefacto: si construyes una imagen en el pipeline y la vuelves a
construir para producción siete minutos después, el digest cambia aunque el código sea el
mismo. Esa imagen «nueva» no es la que pasó las pruebas de extremo a extremo. Se construye una
vez, se publica en el registro con el identificador del commit y se promueve ese digest.

:::figura
fichero: ci-cd-orden-de-etapas
pie: Izquierda, lo que aporta cada etapa a la espera hasta el primer fallo: su duración multiplicada por su probabilidad de fallo. La integración es la que más pesa (240 s · 0,15 = 36 s), seguida de las de extremo a extremo, que duran quince veces más que las unitarias y pesan 30 s (600 s · 0,05): casi lo mismo, porque solo fallan un 5 % de las veces. Las unitarias, con 40 s · 0,25 = 10 s, pesan un tercio que las de extremo a extremo. Derecha, la media de tiempo hasta el primer fallo en los dos órdenes: 832 s con las etapas lentas delante y 172 s poniendo primero las que fallan mucho. La línea morada marca lo que tarda el pipeline completo, 885 s, que es idéntico en los dos casos: lo que se ha mejorado no es el camino feliz, es el caso frecuente.
fuente: figuras/ci-cd-1.py
:::

## Código

```python verificable
# El orden de las etapas decide cuanto tarda un desarrollador en saber que ha roto algo.
etapas = {"e2e": (600, 0.05), "integracion": (240, 0.15),
          "unitarias": (40, 0.25), "lint": (5, 0.02)}

def espera_hasta_fallo(orden):
    """Media del tiempo hasta la primera etapa que falla, condicionada a que algo falle."""
    total, llega, acumulado = 0.0, 1.0, 0
    for nombre in orden:
        duracion, p_fallo = etapas[nombre]        # desempaqueta la tupla (segundos, probabilidad)
        acumulado += duracion                     # lo que se lleva esperado al llegar aqui
        # Solo suma si la ejecucion llego hasta esta etapa: de ahi el factor `llega`.
        total += llega * p_fallo * acumulado
        llega *= 1 - p_fallo                      # probabilidad de pasar a la siguiente
    return total / (1 - llega)          # normalizamos por la probabilidad de fallar

actual = ["e2e", "integracion", "unitarias", "lint"]
# sorted SIN reverse: pone delante la etapa con menor coste por unidad de probabilidad de fallo.
mejor = sorted(etapas, key=lambda n: etapas[n][0] / etapas[n][1])

print(f"orden actual          {espera_hasta_fallo(actual):7.1f} s")   # ->   831.7 s
print(f"orden por coste/fallo {espera_hasta_fallo(mejor):7.1f} s")   # ->   171.6 s
print("orden propuesto:", " ".join(mejor))          # -> unitarias lint integracion e2e
# El guion bajo del generador descarta la probabilidad: la duracion total no depende del orden.
print("duracion si todo pasa:", sum(d for d, _ in etapas.values()), "s")   # -> 885 s
```

:::claves
- `espera_hasta_fallo` devuelve una media **condicionada a que algo falle**: la última línea
  divide entre `1 - llega`. Sin esa división el resultado sería «tiempo esperado del fallo
  contando también las ejecuciones que no fallan», que es una cifra más pequeña y no responde a
  la pregunta de quien está esperando delante de la pantalla.
- El bucle **acumula tiempo aunque el fallo sea improbable**: `acumulado += duracion` corre
  siempre, y el factor `llega * p_fallo` decide cuánto de ese tiempo pesa. Si mueves una etapa
  al principio, su duración entra en el acumulado de todas las siguientes.
- `llega *= 1 - p_fallo` es la probabilidad de que la ejecución pase de etapa. Con 0,25 de
  fallo en unitarias, solo el 75 % de las ejecuciones llega al análisis estático: las etapas
  tardías casi no contribuyen a la media, y por eso adelantarlas no arregla nada.
- `sorted(etapas, ...)` recorre un **diccionario**, así que devuelve una lista de claves
  ordenadas, no de tuplas. Después, `espera_hasta_fallo(mejor)` vuelve a buscar cada etapa en
  el diccionario: el orden está en la lista, no en el diccionario.
- La duración total (885 s) es **la misma en los dos órdenes**: la suma no depende del orden y
  el generador del último `print` descarta la probabilidad con `_`. Lo que cambia es solo el
  caso malo, y el caso malo es el frecuente.
- En el segundo bloque, la función `construir` mete el **momento** dentro del hash a propósito:
  es la forma de enseñar en una línea que reconstruir el mismo código en otro minuto da otro
  digest. En un sistema real el momento no se escribe a mano, pero el efecto es el mismo si las
  dependencias no están fijadas.
- `staging = produccion = construido_en_ci` no copia nada: las tres variables apuntan a la
  misma cadena, y por eso `staging == produccion` es `True` por construcción. La comparación
  que importa es la última, la que falla: el artefacto reconstruido **no** es el que se probó.
:::

```python verificable
import hashlib

def construir(fuente, dependencias, momento):
    """El digest depende del codigo, de las dependencias y del entorno de construccion."""
    # El momento de la construccion entra en el hash: por eso reconstruir da otro digest.
    # [:12] es solo para que la salida se lea; un digest real son 64 caracteres.
    return hashlib.sha256(f"{fuente}:{dependencias}:{momento}".encode()).hexdigest()[:12]

codigo, deps = "app-v3", "numpy-2.1.0"
construido_en_ci = construir(codigo, deps, "2026-01-01T10:00")
reconstruido_en_prod = construir(codigo, deps, "2026-01-01T10:07")   # mismo codigo, otra hora

# Cadena de asignacion: las tres variables apuntan a la MISMA cadena, no a tres copias.
staging = produccion = construido_en_ci        # se promueve el mismo artefacto

print("digest construido una vez en CI:", construido_en_ci)
print("staging y produccion usan el mismo digest:", staging == produccion)                  # -> True
print("digest reconstruido siete minutos despues:", reconstruido_en_prod)
print("lo que se probo es lo que se despliega:", construido_en_ci == reconstruido_en_prod)  # -> False
```

```yaml
on: [push]
jobs:
  pruebas:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: ruff check .
      - run: pytest -q --maxfail=1
  imagen:
    needs: pruebas
    runs-on: ubuntu-latest
    steps:
      - run: docker build -t registro/api:${{ github.sha }} .
      - run: docker push registro/api:${{ github.sha }}
```

## Errores típicos

- **Reconstruir para cada entorno.** Lo que se prueba en integración y lo que llega a
  producción son dos compilaciones distintas, con dependencias resueltas en momentos distintos.
  Construye una vez, publica por digest y promueve ese mismo artefacto.
- **Etapas lentas primero.** Poner las pruebas de extremo a extremo al principio del pipeline
  multiplica el tiempo hasta el primer fallo por cinco, como muestra el ejemplo, y todas las
  horas de máquina se gastan en cambios que ni compilan.
- **Dejar que la rama principal se ponga roja y seguir trabajando.** Cuando el rojo es normal,
  deja de ser información: nadie mira. Arreglar o revertir es la primera tarea, por delante de
  cualquier funcionalidad nueva.
- **Reintentar las pruebas inestables en vez de arreglarlas.** Los reintentos automáticos
  convierten un fallo real e intermitente en un verde falso, y el día que el fallo es de
  verdad el reintento también lo tapa. Marca la prueba como inestable, sácala de la ruta
  crítica y arréglala con fecha.
- **Guardar secretos en el fichero del pipeline.** Van en el gestor de secretos del sistema de
  integración, con credenciales de vida corta; y cuidado con imprimirlos: un `echo` en un
  registro los deja escritos para siempre ([[secretos-y-configuracion]]).
- **Dependencias sin fijar.** Sin fichero de bloqueo, cada construcción puede resolver
  versiones distintas. El mismo commit construye artefactos distintos según el día.
- **Migraciones incompatibles con la versión anterior.** Si al desplegar cambias una columna
  que el código viejo todavía usa, la reversión deja de ser una opción. Los cambios de esquema
  se hacen en dos despliegues (ampliar, rellenar, cambiar el uso, retirar).
- **Medir el éxito por la cobertura.** Un 95 % de cobertura con pruebas que no comprueban nada
  da una falsa sensación de seguridad. Lo que mide el pipeline es si detecta los fallos que
  importan, y eso se comprueba rompiendo el código a propósito alguna vez.

## Comprueba que lo sabes

:::quiz
p: ¿Qué diferencia hay entre entrega continua y despliegue continuo?
o: La entrega continua no usa pruebas automáticas y el despliegue continuo sí
o: En la entrega continua cada cambio queda desplegable y el despliegue a producción lo dispara una persona; en el despliegue continuo se despliega automáticamente
o: La entrega continua solo se aplica a bibliotecas y el despliegue continuo a servicios web
a: 2
e: En los dos casos el pipeline es idéntico y automático. Lo que cambia es la última puerta: en entrega continua está automatizada pero la abre una persona; en despliegue continuo se abre sola en cuanto el pipeline está verde. Elegir una u otra es una decisión sobre cuánta confianza tienes en tus pruebas y en tu capacidad de revertir.
:::

:::quiz
p: ¿Por qué se insiste en construir la imagen una sola vez y promoverla entre entornos?
o: Porque construir es caro y así se ahorra tiempo de máquina
o: Porque dos construcciones del mismo código pueden dar artefactos distintos, y lo que pruebas deja de ser lo que despliegas
o: Porque los registros de imágenes solo admiten una construcción por commit
a: 2
e: El digest depende del código, de las dependencias resueltas y del entorno de construcción. Una dependencia sin fijar o una marca de tiempo basta para que el artefacto cambie. Promover el mismo digest garantiza que lo probado es exactamente lo desplegado; el ahorro de tiempo es un efecto secundario.
:::

:::quiz
p: Tu pipeline tarda 12 minutos y las pruebas de extremo a extremo son las últimas. ¿Qué ganas si mueves delante las unitarias y el análisis estático?
o: Que el pipeline completo tarde menos cuando todo va bien
o: Que el tiempo medio hasta detectar un fallo baje mucho, porque los errores frecuentes se ven en segundos
o: Nada, el orden de las etapas no influye en el tiempo total
a: 2
e: La duración del camino feliz no cambia: hay que ejecutarlo todo. Lo que cambia es el caso frecuente, el del fallo. Si el 25 % de las ejecuciones rompen una prueba unitaria de 40 segundos, ponerla antes ahorra minutos en la mayoría de los casos. Ordenar por coste partido por probabilidad de fallo es la heurística.
:::

:::aviso
Un pipeline que tarda más de diez o quince minutos deja de ser una herramienta y se convierte
en un cuello de botella que la gente sortea: se empiezan a juntar cambios, a saltarse pasos y a
desplegar los viernes a mano. Si no cabe, paraleliza por etapas, cachea dependencias y quita de
la ruta crítica lo que no aporta señal.
:::
