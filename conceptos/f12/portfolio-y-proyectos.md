---
id: portfolio-y-proyectos
titulo: Portfolio y proyectos
fase: 12
nivel: básico
rutas: [core]
prerequisitos: [practicar-con-datos-reales, git-para-datos]
tags: [carrera, portfolio, proyectos, github]
resumen: Dos o tres proyectos reproducibles donde se ve el problema, las decisiones y el resultado valen más que veinte certificados y que un notebook sin README.
fuentes: ["Kleon (2014), 'Show Your Work!'"]
---

## En una frase

Un portfolio no es una lista de cursos: son dos o tres proyectos de los que se ve el problema, las
decisiones, el resultado y el comando que lo reproduce en tu máquina.

## La idea

El título dice que has ido a clase; la carpeta de obra enseña la casa. Quien contrata quiere ver la
casa, y la quiere ver rápido: con cuarenta candidaturas sobre la mesa, dedica unos noventa segundos
al primer repositorio. En ese tiempo responde cuatro preguntas, en este orden: ¿qué problema
resuelve?, ¿de dónde salen los datos?, ¿puedo ejecutarlo?, ¿qué decidió y qué le falló? Si el README
no contesta las dos primeras en la primera pantalla, cierra la pestaña y no vuelve.

Con dos o tres proyectos bien hechos se cubren todas las casillas que se miran:

- **Datos en crudo.** Coges una fuente real, la limpias y dejas una tabla con comprobaciones de que
  está bien: nulos, duplicados, rangos imposibles ([[calidad-de-datos]]).
- **Una decisión.** Una pregunta que se responde con una cifra: ¿sube el abandono?, ¿qué distrito es
  más caro?, ¿esta campaña compensa? Un notebook que explora y no concluye no es un proyecto.
- **Algo que se usa.** Un cuadro de mando, un endpoint o un script que otra persona ejecuta sin
  hablar contigo ([[dashboards]]).

Nada de Titanic ni Iris. Quien revisa ha visto esos datasets cientos de veces: no demuestran
criterio, demuestran que seguiste un tutorial. Coge datos abiertos con una pregunta tuya, o datos
de tu propio trabajo si los puedes anonimizar. Dónde encontrarlos está en
[[practicar-con-datos-reales]].

Y hay un sesgo que casi nadie evita: documentar solo lo que salió bien. Un proyecto donde el modelo
no batió al baseline y explicas por qué es más informativo que uno con métricas perfectas que no se
sostienen. El segundo hace sospechar; el primero demuestra que sabes medir.

## Definición formal

**Proyecto de portfolio:** un artefacto público y reproducible que responde a una pregunta con datos
cuya procedencia está declarada.

Cuatro piezas, cada una comprobable por un tercero que no te conoce:

1. **Pregunta.** Se contesta con un número o con una decisión. «Explorar el dataset» no es una
   pregunta.
2. **Datos.** Origen, licencia y fecha de descarga escritos en el repositorio. Si no se pueden
   publicar (datos personales, contrato con el cliente), un fichero sintético con el mismo esquema
   **y el generador incluido**, para que el ejemplo corra de verdad ([[privacidad-y-gdpr]]).
3. **Método.** Las decisiones que podrían haber sido otras y por qué no lo fueron: por qué esa
   métrica, por qué esa partición, por qué se descartaron esas filas.
4. **Resultado.** Una cifra con su incertidumbre y, en la misma pantalla, lo que no has podido
   comprobar.

**Reproducible** significa exactamente esto: el mismo commit y el entorno fijado producen el mismo
resultado con un comando. Nada de «a mí me funciona». La medida de lo que le cuesta revisarte:

:::formula
coste de revisión = pasos manuales hasta el resultado + pantallas de README antes de la cifra
:::

`pasos manuales` son las órdenes que hay que escribir a mano después de clonar: instalar
dependencias, descargar datos, arreglar una ruta absoluta. Regla práctica: si pasan de 3, o si la
cifra principal no aparece en la primera pantalla del README, tu proyecto no se revisa. No es que
sea malo; es que no llega.

## Ejemplo

Dos fichas, tal como se leerían en el README.

Proyecto A, precio del alquiler por distrito, datos abiertos de un portal municipal:

- 7.043 anuncios, 12 columnas, 8 % de nulos en la superficie.
- Decisión: descarto los anuncios sin superficie y lo justifico (no imputo, porque el precio por
  metro cuadrado es la variable de interés y ese nulo no es aleatorio).
- Resultado: mediana de 11,8 €/m², rango intercuartílico de 8,1 a 16,4; el distrito Centro casi
  duplica al Sur.
- Límite: son precios ofertados, no precios de cierre, así que la mediana real es más baja.

Proyecto B, abandono de clientes:

- 5.000 clientes, 26,5 % de bajas, validación cruzada de 5 particiones.
- Regresión logística: 0,79 de AUC. Gradient boosting: 0,84.
- Al revisar las variables, «días desde la última factura» solo se conoce **después** de la baja:
  la quito, el AUC cae a 0,81 y el modelo sigue batiendo al baseline.
- Límite: los datos son de una sola campaña; no sé si aguanta el trimestre siguiente
  ([[monitorizacion-de-drift]]).

La línea donde explicas la variable que quitaste vale más que el 0,84. Demuestra que miras antes de
presumir.

## Código

```python verificable
# La ficha del conjunto de datos: lo primero que va en el README del proyecto.
import pandas as pd

df = pd.DataFrame({
    "distrito": ["Centro", "Centro", "Norte", "Norte", "Sur", "Sur", "Este", "Oeste"],
    "precio_m2": [14.2, 13.8, 9.1, None, 7.4, 8.0, 10.5, 11.2],
})
# El resumen que cualquiera tiene que poder ver sin abrir el notebook.
print(f"filas {len(df)}")
print(f"nulos en precio_m2 {int(df['precio_m2'].isna().sum())} de {len(df)}")
print(f"distritos {df['distrito'].nunique()}, mediana {df['precio_m2'].median():.1f} EUR/m2")
```

```text
filas 8
nulos en precio_m2 1 de 8
distritos 5, mediana 10.5 EUR/m2
```

```text
Los cinco bloques del README, en este orden:

1. Qué problema resuelve y qué cifra sale (tres líneas, en la primera pantalla).
2. De dónde salen los datos: origen, licencia y fecha de descarga.
3. Cómo se ejecuta: los comandos, en orden, con el entorno fijado.
4. Decisiones y resultados, incluido lo que no funcionó.
5. Límites: qué no puedes afirmar con estos datos.
```

```python ilustrativo
# Un entorno fijado: sin esto, el revisor no puede reproducir tu resultado.
# requirements.txt con versiones exactas, no rangos:
#   pandas==2.2.3
#   scikit-learn==1.5.2
# Y los datos con su digest, para que se note si cambian:
import hashlib, pathlib

ruta = pathlib.Path("datos/alquiler_2026_01.csv")
print(hashlib.sha256(ruta.read_bytes()).hexdigest()[:12])   # se pega en el README
```

## Errores típicos

- **Enseñar el resultado y no el camino.** Un repositorio con un notebook de 200 celdas y sin README
  no se puede revisar. El README va primero y el notebook es la evidencia, no la portada.
- **Copiar el tutorial de turno.** Titanic, Iris, los precios de casas de Kaggle. Quien revisa los
  reconoce en tres segundos y deduce lo que no has hecho: decidir.
- **No poner cómo se ejecuta.** Sin versión de Python, sin dependencias y con rutas absolutas de tu
  disco. Con eso, tu proyecto no existe para nadie más.
- **Métricas infladas por fuga.** Un R² de 0,99 o un AUC de 0,98 casi siempre significa que una
  variable contiene información del futuro. Búscala antes de publicar y cuéntalo ([[fuga-de-datos]]).
- **Publicar datos que no puedes publicar.** Datos de clientes, con nombres o con contrato de
  confidencialidad. Si dudas, datos sintéticos con el mismo esquema y el generador en el repo.
- **Doce repositorios empezados.** Un portfolio con doce proyectos a medias y un `TODO` en cada uno
  comunica lo contrario de lo que quieres. Tres terminados, mejor.
- **Esconder los límites.** Un README que promete más de lo que mide se cae en la primera pregunta
  de la entrevista. Escribe qué no puedes afirmar y con qué datos lo afirmarías
  ([[escribir-un-informe]]).

## Comprueba que lo sabes

:::quiz
p: ¿Qué tiene que responder el README en la primera pantalla para que alguien siga leyendo?
o: El problema que resuelve y la cifra principal que has obtenido
o: La lista de tecnologías que has usado y tu currículum
o: El historial de commits y las horas que has dedicado
o: Los agradecimientos y el enlace a tus otros repositorios
a: 1
e: Quien revisa busca en noventa segundos qué problema hay y qué ha salido; lo demás es contexto que se lee después. El listado de tecnologías no dice nada del criterio, y el historial de commits solo interesa a quien ya está dentro del proyecto.
:::

:::quiz
p: Tu modelo de abandono saca un AUC de 0,97 con una variable llamada «motivo de baja». ¿Qué haces?
o: Publicarlo: es el mejor resultado que has tenido
o: Quitarla, porque solo existe después del evento que intentas predecir, y reportar el AUC sin ella
o: Cambiar la métrica a exactitud para que el número parezca más razonable
o: Añadir más variables para bajar la correlación entre ellas
a: 2
e: Una variable que se conoce después del evento es fuga de datos: en producción no estará disponible. Cambiar de métrica esconde el problema y añadir variables no lo arregla. La regla es preguntar por cada variable si su valor existiría en el momento de la predicción.
:::

:::quiz
p: Quieres publicar un proyecto con datos de clientes de tu empresa y no tienes permiso. ¿Cuál es la salida correcta?
o: Publicarlos igual, pero sin la columna de nombres
o: Publicar solo capturas de pantalla de los gráficos
o: Generar un conjunto sintético con el mismo esquema, incluirlo con su generador y decirlo en el README
o: No publicar ningún proyecto de ese tema
a: 3
e: Quitar los nombres no elimina la reidentificación: quedan edades, importes y fechas que señalan a personas concretas. Las capturas no permiten reproducir nada. Un conjunto sintético con el mismo esquema conserva el valor didáctico sin exponer a nadie, y declararlo es parte de la ética del trabajo.
:::

:::practica
enunciado: Monta el esqueleto de tu portfolio con dos proyectos y publícalo. Para cada uno: escribe el README con los cinco bloques (problema y cifra, datos y licencia, cómo ejecutarlo, decisiones, límites), deja el entorno fijado con versiones exactas y comprueba que una persona ajena puede clonar el repositorio y ver la cifra en menos de cinco minutos, sin preguntarte nada.
pista: Hazlo al revés de como lo hiciste: escribe primero el README y luego el código que falta para que sea verdad.
solucion: Un README mínimo viable tiene esta forma, y cada bloque se puede comprobar. Problema: «¿en qué distritos el alquiler ha subido más de un 10 % en un año?», con la cifra y su intervalo en la primera pantalla. Datos: enlace al portal, licencia, fecha de descarga y digest del fichero. Ejecución: tres comandos (clonar, crear entorno, ejecutar el script) y una nota de la versión de Python; si hacen falta más de tres pasos, mete los pasos en un `Makefile`. Decisiones: por qué descartaste los nulos de superficie, por qué usaste mediana y no media. Límites: precios ofertados, no de cierre. Y la prueba final: pídeselo a alguien que no sepa nada del proyecto y cronométralo. Si te pregunta algo antes de ver la cifra, el README tiene un agujero.
:::
