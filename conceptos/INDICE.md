# Índice de conceptos — Data School

**Fecha:** 2026-11-04

**Total:** 459 conceptos repartidos en 13 fases (f00–f12).

**Procedencia:** contenido propio del proyecto Data School, escrito en el portal vivo y
importado el 2026-11-04. La fuente se ha leído en modo solo lectura; en esta carpeta no se
copia material de terceros. Cada fila sale del frontmatter YAML del fichero correspondiente,
de modo que `id`, `título`, `nivel`, `rutas` y `resumen` son los del propio concepto.

---

## f00 — Aprender a aprender (14 conceptos)

| id | título | nivel | rutas | resumen |
| --- | --- | --- | --- | --- |
| `como-estudiar` | Cómo estudiar esto | básico | `core` | Recuperar de memoria, repartir los repasos en el tiempo e intercalar temas: eso es estudiar. Releer y subrayar solo… |
| `como-leer-un-paper` | Cómo leer un paper | intermedio | `core`, `ds` | Tres pasadas de coste creciente, saber cuándo abandonar y mirar la tabla de resultados antes que las matemáticas: leer… |
| `escribir-tarjetas-de-repaso` | Escribir tarjetas de repaso | básico | `core` | Una tarjeta se escribe con una sola idea, con el contexto dentro del enunciado y con una respuesta que se pueda dar… |
| `fuentes-y-canales` | Fuentes, canales y datos | básico | `core` | Dónde aprender cada fase, qué fuente sirve para qué y por qué seis activas bastan: el mapa de recursos con enlaces… |
| `hacer-preguntas-buenas` | Formular buenas preguntas | básico | `core`, `ds` | Una pregunta útil dice qué unidad cuenta, sobre quién, con qué métrica, contra qué se compara y qué harás según el… |
| `leer-documentacion-oficial` | Leer la documentación oficial | básico | `core` | La documentación oficial es el contrato de quien lo cumple: se lee buscando la firma exacta en la versión que tienes… |
| `mapa-del-portal` | Cómo usar este portal | básico | `core` | Rutas, fases, prerequisitos, preguntas de repaso y exportación a Anki: cómo moverte por el temario sin perderte ni… |
| `medir-tu-progreso` | Medir tu progreso sin engañarte | básico | `core` | La media acumulada esconde los cambios: mide tu rendimiento por ventanas, compáralo contigo mismo y no conviertas la… |
| `notacion-matematica` | Notación matemática | básico | `core` | Σ, Π, ∈, ∂, ∇ y E[…] no son un idioma aparte: cada símbolo es una abreviatura de una frase. Apréndelos y las fórmulas… |
| `pedir-ayuda-tecnica` | Pedir ayuda técnica y que te la den | básico | `core` | Una duda se responde cuando lleva un ejemplo mínimo que falla, lo que ya has probado, las versiones exactas y la… |
| `practicar-con-datos-reales` | Practicar con datos reales | básico | `core`, `ds` | Los datasets de juguete vienen limpios y con el problema ya resuelto. Practica con datos sucios y de verdad, y termina… |
| `rutas-de-aprendizaje` | Rutas de aprendizaje | básico | `core` | Las cuatro rutas completas —data engineer, data scientist, IA y quant— con el orden de cada paso y lo que hay que… |
| `tomar-notas-tecnicas` | Tomar notas técnicas | básico | `core` | Una nota técnica es un mensaje a tu yo de dentro de seis meses: qué pasaba, qué decidiste, por qué y con qué… |
| `usar-ia-para-aprender` | Usar la IA para aprender sin engañarte | básico | `core` | Un modelo puede ser tu tutor o tu atajo, y solo se distinguen al defender el resultado: pide explicaciones, comprueba… |

## f01 — Fundamentos matemáticos (41 conceptos)

| id | título | nivel | rutas | resumen |
| --- | --- | --- | --- | --- |
| `asimetria-y-curtosis` | Asimetría y curtosis | intermedio | `core`, `ds`, `quant` | La asimetría dice hacia qué lado se estira la cola y la curtosis cuánto pesan los extremos; son los dos números que… |
| `autovalores-y-autovectores` | Autovalores y autovectores | avanzado | `core`, `ds`, `quant`, `alg` | Son las direcciones que una matriz no gira, solo estira; su autovalor dice cuánto, y de ahí salen PCA, PageRank y el… |
| `cadenas-de-markov` | Cadenas de Markov | intermedio | `core`, `ds`, `quant` | Un sistema que salta entre estados sin memoria, y cómo su matriz de transición permite calcular a dónde irá y cuánto… |
| `convexidad` | Convexidad | avanzado | `core`, `ds`, `quant` | Una función convexa tiene un único valle: cualquier mínimo local es el global, y eso convierte un problema de… |
| `correlacion-pearson-spearman` | Correlación de Pearson y Spearman | básico | `core`, `ds` | Pearson mide cuánto se pega la nube de puntos a una recta y Spearman solo el orden; un único valor atípico puede mover… |
| `covarianza-y-correlacion` | Covarianza y correlación | básico | `core`, `ds`, `quant` | Cuanto tienden dos variables a moverse juntas, la versión sin unidades de esa medida y las tres cosas que la… |
| `cuantiles-y-percentiles` | Cuantiles y percentiles | básico | `core`, `ds` | El percentil 95 de latencia es el tiempo que solo superan 5 de cada 100 peticiones; los cuantiles resumen sin suponer… |
| `derivadas-parciales-y-gradiente` | Derivadas parciales y gradiente | intermedio | `core`, `ds` | La derivada parcial mide como cambia una función al mover una sola variable; el gradiente las junta en un vector que… |
| `derivadas-y-reglas` | Derivadas y reglas de derivación | básico | `core`, `ds`, `quant` | La derivada es la pendiente de la recta tangente; las reglas de producto, cociente y cadena permiten derivar sin… |
| `descomposicion-svd` | Descomposición en valores singulares | avanzado | `core`, `ds`, `quant` | Cualquier matriz se escribe como giro, estirado y giro; quedarte con los valores singulares grandes comprime y limpia… |
| `determinante-rango-invertibilidad` | Determinante, rango e inversa | intermedio | `core`, `ds`, `quant` | El determinante mide cuánto deforma una matriz; si vale cero, sus columnas son dependientes, el rango baja y la… |
| `distribuciones-continuas` | Distribuciones continuas | intermedio | `core`, `ds` | Uniforme, normal, exponencial, t, chi-cuadrado, F, beta, gamma y lognormal: qué mecanismo modela cada una y cómo se… |
| `distribuciones-discretas` | Distribuciones discretas | intermedio | `core`, `ds` | Bernoulli, binomial, geométrica, Poisson y multinomial: qué mecanismo genera cada una y cómo elegir la correcta según… |
| `distribucion-normal-multivariante` | Distribución normal multivariante | intermedio | `ds`, `core` | Modela varias variables que se mueven juntas cuando cada una es normal, y explica por qué la correlación cambia la… |
| `entropia-e-informacion` | Entropía e información | avanzado | `ds`, `alg` | Entropía, entropía cruzada, divergencia KL e información mutua: la moneda con la que se mide la incertidumbre y se… |
| `escalares-vectores-matrices` | Escalares, vectores y matrices | básico | `core`, `ds` | Un escalar es un número, un vector es una lista ordenada y una matriz es una tabla; casi todo dataset es una matriz y… |
| `expansion-karhunen-loeve` | Expansión de Karhunen-Loève | experto | `quant`, `ds` | La versión continua del PCA: descomponer un proceso aleatorio en funciones propias de su covarianza y simularlo con… |
| `independencia-y-condicionamiento` | Independencia y condicionamiento | intermedio | `core`, `ds` | Independencia, independencia condicional y la paradoja de Berkson: por qué dos variables sin relación pueden parecer… |
| `integrales` | Integrales | intermedio | `core`, `ds` | Acumular áreas infinitesimales: la integral es la operación inversa de derivar y el motivo de que casi toda… |
| `jacobiano-y-hessiano` | Jacobiano y Hessiano | avanzado | `core`, `quant` | El jacobiano agrupa las derivadas de una función vectorial y el hessiano las segundas derivadas: la curvatura que dice… |
| `ley-de-los-grandes-numeros` | Ley de los grandes números | intermedio | `core`, `ds` | Por qué la media muestral acaba pareciéndose al valor esperado, por qué tarda tanto en parecerse y por qué no… |
| `limites-y-continuidad` | Límites y continuidad | básico | `core` | El límite describe a dónde se acerca una función sin necesidad de llegar; la continuidad exige además que el valor de… |
| `logaritmos-y-escalas-logaritmicas` | Logaritmos y escalas logarítmicas | básico | `core`, `ds` | Un logaritmo cuenta multiplicaciones en vez de sumas, y una escala logarítmica pone factores iguales a distancias… |
| `medidas-de-centralidad` | Medidas de centralidad | básico | `core`, `ds` | Media, mediana y moda resumen un conjunto de datos en un solo número, y cada una miente de una forma distinta. |
| `medidas-de-dispersion` | Medidas de dispersión | básico | `core`, `ds` | Rango, IQR, varianza, desviación típica y coeficiente de variación miden cuánto se alejan los datos; sin ellos, una… |
| `momentos-y-cumulantes` | Momentos y cumulantes | avanzado | `core`, `ds`, `quant` | Media, varianza, asimetría y curtosis como una sola familia de números, y los cumulantes que sí se suman al combinar… |
| `norma-y-distancias` | Normas y distancias | intermedio | `core`, `ds`, `alg` | Una norma mide el tamaño de un vector y una distancia, la separación entre dos puntos; elegir L1, L2, L∞ o Mahalanobis… |
| `operaciones-matriciales` | Operaciones con matrices | básico | `core`, `ds` | Sumar, multiplicar y trasponer matrices tiene reglas propias; el producto no es elemento a elemento y el orden de los… |
| `optimizacion-con-restricciones` | Optimización con restricciones | avanzado | `core`, `quant`, `ds` | Multiplicadores de Lagrange y condiciones KKT: como maximizar o minimizar cuando hay restricciones, y por qué la… |
| `precision-y-error-numerico` | Precisión y error numérico | básico | `core`, `ds` | Los números con decimales no se guardan exactos, así que 0,1 + 0,2 no da 0,3. Por eso se compara con tolerancia, se… |
| `probabilidad-axiomas` | Axiomas de probabilidad | básico | `core`, `ds` | Espacio muestral, sucesos, unión e intersección: los tres axiomas de Kolmogorov y las reglas de suma que sostienen… |
| `probabilidad-condicional` | Probabilidad condicional | básico | `core`, `ds` | La probabilidad de A sabiendo que B ha ocurrido: reduce el espacio muestral al suceso conocido y reescala, y por eso… |
| `producto-punto-y-similitud` | Producto punto y similitud | básico | `core`, `ds`, `quant` | El producto punto mide cuánto apuntan dos vectores en la misma dirección; normalizado da la similitud del coseno, la… |
| `regla-de-la-cadena` | Regla de la cadena | intermedio | `core`, `ds` | Derivar una función compuesta es multiplicar las derivadas de sus piezas en orden, y eso es exactamente la… |
| `teorema-central-del-limite` | Teorema central del límite | intermedio | `core`, `ds`, `quant` | Por qué la media de casi cualquier cosa se distribuye como una normal, de dónde sale el error típico y cuándo la… |
| `teorema-de-bayes` | Teorema de Bayes | intermedio | `core`, `ds` | Como dar la vuelta a una probabilidad condicional: la regla que convierte la tasa de acierto de un test en la… |
| `transformaciones-lineales` | Transformaciones lineales | intermedio | `core`, `ds`, `alg` | Una matriz es una acción sobre el espacio: rota, escala, proyecta o refleja, y sus columnas son las imágenes de los… |
| `valor-esperado` | Valor esperado | básico | `core`, `ds`, `quant` | La media teórica de una variable aleatoria, por qué se suma tan fácilmente y por qué E[X·Y] no es E[X]·E[Y] salvo que… |
| `variable-aleatoria` | Variable aleatoria | básico | `core`, `ds`, `quant` | Una función que asigna un número a cada resultado de un experimento, con su masa o densidad y su función de… |
| `varianza-y-desviacion` | Varianza y desviación típica | básico | `core`, `ds`, `quant` | Cuanto se aleja una variable de su media, por qué se mide en unidades al cuadrado y cómo se combinan las varianzas al… |
| `z-score-y-estandarizacion` | Z-score y estandarización | básico | `core`, `ds` | El z-score dice a cuántas desviaciones típicas está un valor de la media; sirve para comparar escalas distintas y para… |

## f02 — Inferencia y estadística (26 conceptos)

| id | título | nivel | rutas | resumen |
| --- | --- | --- | --- | --- |
| `ab-testing` | Tests A/B | intermedio | `ds`, `de` | Un experimento aleatorizado con métrica decidida de antemano, duración calculada y reglas de parada fijadas antes de… |
| `anova` | ANOVA | intermedio | `ds`, `core` | Comparar las medias de tres o más grupos con un solo contraste, descomponiendo la variabilidad total en la de dentro y… |
| `bootstrap` | Bootstrap y remuestreo | intermedio | `ds`, `core` | Remuestrear tus propios datos con reemplazo para estimar la incertidumbre de casi cualquier estadístico, sin suponer… |
| `causalidad-vs-correlacion` | Causalidad frente a correlación | básico | `ds`, `core` | Dos variables pueden moverse juntas por cuatro motivos distintos, y solo uno de ellos es que una cause a la otra;… |
| `chi-cuadrado` | Test chi-cuadrado | intermedio | `ds`, `core` | Contrastar si dos variables categóricas se relacionan o si unas frecuencias observadas encajan con las esperadas, y… |
| `confusores-y-dag` | Confusores, mediadores y DAG | avanzado | `ds`, `core` | Dibujar el grafo causal antes de tocar la regresión decide qué variables ajustar y, sobre todo, de cuáles no hay que… |
| `contraste-de-hipotesis` | Contraste de hipótesis | intermedio | `ds`, `core` | Un procedimiento que fija de antemano qué resultado contarías como prueba contra la hipótesis nula, y decide si lo… |
| `datos-agrupados-y-errores-tipicos` | Datos agrupados y errores típicos | básico | `ds`, `core` | Cómo calcular la media y el error típico cuando tus datos vienen ya agrupados en frecuencias, y por qué confundir… |
| `disenos-factoriales-e-interacciones` | Diseños factoriales e interacciones | intermedio | `ds`, `core` | Varía varios factores a la vez para estimar cada efecto con todos los datos y para detectar la interacción, que es la… |
| `errores-tipo-i-ii-y-potencia` | Errores tipo I y II, potencia | intermedio | `ds`, `core` | Todo contraste falla de dos maneras: falsa alarma o incendio sin alarma; la potencia mide la segunda y se decide antes… |
| `estimacion-bayesiana-map` | Estimación bayesiana y MAP | avanzado | `ds`, `core` | Priors, posteriors y MAP: cómo la creencia previa entra en la estimación y por qué la regularización L2 es un prior… |
| `estimadores-y-propiedades` | Estimadores y sus propiedades | intermedio | `ds`, `core` | Insesgado, consistente, eficiente y suficiente: lo que hace útil a un estimador y por qué el mejor no siempre es el… |
| `inferencia-causal-metodos` | Métodos de inferencia causal | experto | `ds`, `core` | Cuatro diseños para estimar efectos causales cuando no puedes aleatorizar, cada uno con su supuesto de identificación… |
| `intervalos-de-confianza` | Intervalos de confianza | intermedio | `ds`, `core` | El 95 % no es la probabilidad de que el parámetro caiga dentro: es la frecuencia con la que el procedimiento acierta… |
| `maxima-verosimilitud` | Máxima verosimilitud (MLE) | avanzado | `ds`, `core` | Elegir los parámetros que hacen más probables los datos observados; de ahí salen el MLE de una moneda y la pérdida de… |
| `missing-data` | Datos ausentes | intermedio | `ds`, `de`, `core` | MCAR, MAR y MNAR describen por qué falta cada dato, y ese mecanismo —no el porcentaje de nulos— decide si borrar filas… |
| `multiplicidad-y-fdr` | Multiplicidad y FDR | avanzado | `ds`, `quant` | Comparar cien métricas a la vez dispara los falsos positivos; Bonferroni controla el error en familia y… |
| `poblacion-y-muestra` | Población y muestra | básico | `ds`, `core` | La población es lo que quieres describir y la muestra lo que mides; de esa distancia nacen el error de muestreo y casi… |
| `pruebas-de-equivalencia-y-no-inferioridad` | Pruebas de equivalencia y no inferioridad | avanzado | `ds`, `core` | Cómo demostrar que dos cosas son prácticamente iguales, en lugar de limitarse a no encontrar diferencias, y por qué… |
| `p-valor` | El p-valor | intermedio | `ds`, `core` | La probabilidad de ver un resultado al menos tan extremo como el observado si la nula fuera cierta; no es la… |
| `remuestreo-y-permutacion` | Tests de permutación | avanzado | `ds`, `core` | Construir la distribución nula barajando las etiquetas del propio experimento: un contraste exacto, sin supuestos de… |
| `sesgo-varianza-mse` | Sesgo, varianza y ECM | intermedio | `ds`, `core` | El error que puedes esperar se descompone en ruido irreducible, sesgo al cuadrado y varianza; por eso un modelo algo… |
| `tamano-del-efecto` | Tamaño del efecto | intermedio | `ds`, `core` | Cuanto de grande es una diferencia, en una unidad que no depende de cuántos datos tengas; la d de Cohen y la… |
| `tamano-muestral` | Cálculo de tamaño muestral | intermedio | `ds`, `de` | Cuantas observaciones necesitas para detectar el efecto que te importa, y por qué calcularlo después de ver los datos… |
| `tests-no-parametricos` | Tests no paramétricos | intermedio | `ds`, `core` | Mann-Whitney, Wilcoxon, Kruskal-Wallis y Kolmogorov-Smirnov: contrastar sin suponer una forma concreta para la… |
| `test-t` | Test t | intermedio | `ds`, `core` | Comparar una media con un valor de referencia o dos medias entre sí, eligiendo bien la variante y respetando los… |

## f03 — Python, SQL y herramientas (42 conceptos)

| id | título | nivel | rutas | resumen |
| --- | --- | --- | --- | --- |
| `apis-y-peticiones-http` | APIs y peticiones HTTP | intermedio | `de`, `ds` | Una API es una promesa por escrito con método, ruta, código de estado y formato; aquí se aprende a leerla, paginarla y… |
| `arrow-y-formatos-columnares` | Arrow y formatos columnares | intermedio | `de`, `ds` | Guardar los datos por columnas y no por filas: menos bytes leídos, mejor compresión y una misma representación en… |
| `calidad-de-datos` | Calidad de datos | intermedio | `de`, `ds` | Nulos, duplicados, rangos imposibles y coherencia entre columnas convertidos en proporciones que se miden, se vigilan… |
| `clases-y-objetos` | Clases y objetos | intermedio | `core`, `de`, `ds`, `alg` | Una clase es el molde, cada objeto guarda su propio estado y self es cómo un método sabe sobre qué objeto trabaja. |
| `comprensiones-y-generadores` | Comprensiones y generadores | básico | `core`, `de`, `ds` | Las comprensiones construyen listas y diccionarios en una línea; los generadores producen los valores de uno en uno y… |
| `datos-que-no-caben-en-memoria` | Datos que no caben en memoria | intermedio | `de`, `ds` | Si la tabla no cabe en RAM se lee por bloques y se agrega sobre la marcha; el resultado de una agregación es diminuto… |
| `entorno-python` | Entorno de Python | básico | `de`, `ds`, `core` | Un intérprete concreto más las versiones exactas de sus librerías: aislarlo por proyecto y fijarlas es lo que hace que… |
| `errores-y-depuracion` | Errores y depuración | básico | `core`, `de`, `ds` | Un traceback se lee de abajo arriba: da el tipo de error y la línea exacta. try/except decide qué haces con él y el… |
| `fechas-y-horas` | Fechas, horas y zonas horarias | intermedio | `core`, `de`, `ds` | Un instante y una hora local no son lo mismo; datetime, timedelta, UTC y el horario de verano, que dos días al año… |
| `ficheros-y-encoding` | Ficheros y codificaciones | básico | `de`, `ds`, `core` | El mismo dato cambia de significado según la codificación, el formato y el separador; aquí se aprende a no corromperlo… |
| `funciones-y-modulos` | Funciones, módulos y paquetes | básico | `core`, `de`, `ds` | Una función le pone nombre y argumentos a un cálculo; un módulo lo guarda en un fichero y un paquete agrupa módulos… |
| `gestores-de-contexto` | Gestores de contexto y liberación de recursos | intermedio | `core`, `de` | El bloque with garantiza que el recurso se suelte al salir, aunque el cuerpo falle a mitad, y evita que un proceso… |
| `git-para-datos` | Git para datos | básico | `core`, `de`, `alg` | Ramas, commits y conflictos aplicados a un proyecto de datos, y por qué los ficheros de datos en crudo no se versionan… |
| `json-y-datos-anidados` | JSON y datos anidados | básico | `core`, `de`, `ds` | JSON guarda objetos y listas unas dentro de otras; leerlo es fácil, pero convertirlo en tabla obliga a aplanar y a… |
| `notebooks-vs-scripts` | Notebooks frente a scripts | básico | `core`, `ds`, `de` | Cuándo usar un notebook y cuándo un script, por qué el estado oculto arruina la reproducibilidad y cómo saber si tu… |
| `numpy-broadcasting` | Broadcasting de NumPy | intermedio | `core`, `de`, `ds` | NumPy estira las formas compatibles para operar arrays de tamaños distintos sin copiar datos, y por eso una resta mal… |
| `numpy-fundamentos` | NumPy: fundamentos | básico | `core`, `de`, `ds` | Un ndarray es memoria contigua con un tipo fijo para todos los elementos: la misma operación sobre un millón de… |
| `pandas-agrupaciones-y-joins` | Pandas: agrupaciones y uniones | intermedio | `core`, `ds`, `de` | Agrupar y unir resuelven casi toda la transformación de tablas; el resto es saber cuándo apply es la respuesta… |
| `pandas-fundamentos` | Pandas: fundamentos | básico | `core`, `ds`, `de` | Un DataFrame es una tabla de columnas con tipo propio y un índice compartido; entender qué devuelve cada corchete… |
| `perfilado-de-datos` | Perfilado y EDA automático | intermedio | `de`, `ds` | Describir una tabla desconocida con números -tipo real, nulos, cardinalidad, rangos y valores frecuentes- antes de… |
| `polars` | Polars | intermedio | `de`, `ds` | API de expresiones, plan perezoso y ejecución en paralelo sobre memoria de Arrow: la alternativa a Pandas cuando la… |
| `reformar-tablas-ancho-y-largo` | Reformar tablas: ancho y largo | intermedio | `core`, `ds`, `de` | melt, pivot y stack cambian de sitio la información sin sumar nada; es el paso obligatorio para convertir doce… |
| `regex-y-limpieza-de-texto` | Expresiones regulares | intermedio | `de`, `ds` | Patrones para validar, extraer y sustituir texto; por qué casi siempre «funciona», dónde está la trampa del anclaje y… |
| `scraping-etico` | Web scraping responsable | intermedio | `de`, `ds` | Antes de rascar una web hay que leer robots.txt, limitar el ritmo, cachear lo descargado y comprobar si existe una API… |
| `scripts-ejecutables-y-argumentos` | Scripts ejecutables y argumentos | básico | `core`, `de`, `ds` | De notebook a herramienta: leer los datos por argumentos con argparse, construir las rutas con pathlib y salir con… |
| `series-temporales-en-pandas` | Series temporales en Pandas | intermedio | `ds`, `de`, `quant` | Con la fecha en el índice, Pandas agrega por ventanas, calcula medias móviles por tiempo, desplaza y une series de… |
| `sql-agregaciones-y-group-by` | SQL: agregaciones y GROUP BY | básico | `de`, `ds` | Partir la tabla en montones que comparten una clave y resumir cada montón en una fila; donde va cada filtro y por qué… |
| `sql-indices-y-planes` | SQL: índices y planes | avanzado | `de`, `ds` | Por qué una consulta que devuelve 20 filas tarda un minuto: qué hace un índice, cuándo el motor lo ignora y cómo leer… |
| `sql-joins` | SQL: uniones | básico | `de`, `ds`, `core` | INNER, LEFT, FULL y CROSS, autocombinaciones y el error clásico de duplicar filas al unir antes de agregar. |
| `sql-modelado-y-normalizacion` | SQL: modelado y normalización | intermedio | `de`, `ds` | Que entidades existen, con qué clave se identifican y en qué tabla vive cada hecho; por qué repetir la ciudad del… |
| `sql-select-y-filtros` | SQL: consultas y filtros | básico | `de`, `ds`, `core` | SELECT, WHERE, ORDER BY y LIMIT con su orden de evaluación real, la lógica de tres valores de NULL y lo que cambia… |
| `sql-subconsultas-y-cte` | SQL: subconsultas y CTE | intermedio | `de`, `ds` | Consultas dentro de consultas y el WITH que les pone nombre; cómo se lee una consulta larga de arriba abajo sin… |
| `sql-ventanas` | SQL: funciones de ventana | avanzado | `de`, `ds` | Calcular un valor por fila mirando sus vecinas -ranking, diferencias, acumulados y medias móviles- sin colapsar la… |
| `terminal-y-shell` | Terminal y shell | básico | `core`, `de`, `alg` | Pipes, permisos, códigos de salida y cron: la herramienta con la que se depura un pipeline cuando algo falla a las… |
| `testing-con-pytest` | Tests con pytest | intermedio | `de`, `ds`, `alg` | Fixtures, parametrización y cobertura: qué merece un test en un pipeline de datos y qué es una pérdida de tiempo… |
| `tipado-y-linters` | Tipado y linters | intermedio | `de`, `alg`, `ds` | Anotaciones de tipo, dataclasses y Pydantic: cómo detectar antes de ejecutar los errores que en un pipeline de datos… |
| `tipos-y-estructuras-python` | Tipos y estructuras de Python | básico | `de`, `ds`, `core` | Listas, tuplas, diccionarios y conjuntos guardan varios valores; elegir mal no rompe el programa, lo hace lento o lo… |
| `transacciones-y-bloqueos` | Transacciones, aislamiento y bloqueos | avanzado | `de`, `alg` | Agrupa varias escrituras en una unidad que se aplica entera o no se aplica, y decide qué ve la otra sesión mientras… |
| `vectorizacion` | Vectorización | intermedio | `core`, `de`, `ds` | Sustituir los bucles por operaciones sobre el array entero: máscaras booleanas, where y agregaciones por grupo, sin… |
| `vistas-y-copias` | Vistas, copias y aliasing | intermedio | `core`, `ds`, `de` | Una rebanada no copia nada: comparte memoria con el original. Distinguir vista de copia evita el bug más silencioso y… |
| `visualizacion-estadistica` | Visualización estadística | intermedio | `ds`, `core` | Boxplots, violines, densidades y matrices de correlación: cómo enseñar una distribución entera en vez de un solo… |
| `visualizacion-matplotlib` | Visualización con Matplotlib | básico | `core`, `ds`, `de` | Figuras, ejes, escalas y anotaciones con Matplotlib, y las decisiones de ejes que hacen que un gráfico mienta sin… |

## f04 — Ingeniería de datos (61 conceptos)

| id | título | nivel | rutas | resumen |
| --- | --- | --- | --- | --- |
| `airflow-dagster-prefect` | Airflow, Dagster y Prefect | intermedio | `de` | Los tres orquestadores que aparecen en las ofertas de empleo, en qué se parecen y qué forma distinta de pensar propone… |
| `almacenamiento-de-objetos` | Almacenamiento de objetos | básico | `de` | Un disco remoto al que se accede por HTTP con objetos enteros; el prefijo hace de carpeta, la clase decide el coste y… |
| `arquitectura-medallion` | Arquitectura medallion | intermedio | `de` | Bronce, plata y oro: tres capas con responsabilidades distintas que se reconstruyen en cadena para que la calidad del… |
| `backfill-y-reproceso` | Backfill y reproceso | avanzado | `de` | Rellenar las particiones que faltan y recalcular las que ya existen es rutina; el peligro es aplicar la lógica de hoy… |
| `batch-vs-streaming` | Procesamiento por lotes y en flujo | intermedio | `de` | Procesar cada hora o procesar cada evento: la decisión se toma con la latencia que la decisión tolera, el coste y la… |
| `bi-y-consumo` | BI y capa de consumo | básico | `de`, `core` | Cuadros de mando sobre tablas curadas: cuándo consultar en vivo, cuándo servir un extracto más barato y qué se publica… |
| `calidad-y-slas` | Calidad y acuerdos de nivel de servicio | avanzado | `de` | El SLI es cómo mides la calidad, el SLO el umbral que te exiges y el SLA el acuerdo con consecuencia; sin un número… |
| `capa-semantica-y-metricas` | Capa semántica y métricas | avanzado | `de`, `ds` | Definir cada métrica una sola vez, con su medida, su agregación, su grano y sus filtros, para que el cuadro, la API y… |
| `catalogo-y-linaje` | Catálogo y linaje | intermedio | `de`, `core` | El catálogo dice qué datos existen y de quién son; el linaje dice de dónde vienen y qué se rompe al cambiarlos,… |
| `ciclo-de-vida-del-dato` | Ciclo de vida del dato | básico | `de`, `core` | Todo dato recorre seis etapas, de la captura al borrado, y cada una tiene dueño, coste y plazo; lo que no se borra a… |
| `compresion-y-codificacion` | Compresión y codificación | intermedio | `de`, `ds` | Diccionarios, rachas y delta codifican los valores según su tipo; Snappy, Zstd y gzip comprimen los bytes resultantes.… |
| `contratos-de-datos` | Contratos de datos | avanzado | `de` | El contrato fija esquema, semántica, calidad y política de cambios entre productor y consumidor, y sólo sirve si un… |
| `control-de-acceso-por-fila-y-columna` | Control de acceso por fila y por columna | avanzado | `de` | Que el motor recorte filas y columnas según quién consulta, para que la autorización no dependa de que cada… |
| `correccion-point-in-time` | Corrección point-in-time | avanzado | `de`, `quant` | Guardar cada dato con la fecha en que estuvo disponible y no con la del evento, la disciplina que separa un pipeline… |
| `coste-y-optimizacion` | Coste y optimización | avanzado | `de`, `ds` | En analítica se paga sobre todo por bytes leídos, bytes guardados y horas de cómputo, así que optimizar es leer menos,… |
| `data-lake` | Data lake | intermedio | `de` | Guardar los datos tal como llegan, en ficheros sobre almacenamiento de objetos, y ponerles esquema y orden al leerlos:… |
| `data-mesh` | Data mesh | experto | `de` | Los dominios poseen sus datos y los publican como producto sobre una plataforma self-service, con un gobierno federado… |
| `data-vault` | Modelado Data Vault | avanzado | `de` | Hub, enlace y satélite: un modelado que solo inserta filas y que aguanta que los orígenes cambien sin reescribir el… |
| `data-warehouse` | Data warehouse | intermedio | `de`, `ds` | El almacén curado donde los datos de muchos sistemas se limpian, se integran y se modelan una sola vez para que toda… |
| `datos-de-mercado-y-acciones-corporativas` | Datos de mercado y acciones corporativas | intermedio | `de`, `quant` | Un precio bruto no es comparable consigo mismo en el tiempo: splits, dividendos y cambios de horario obligan a ajustar… |
| `dbt-y-transformacion` | dbt y transformación | intermedio | `de` | dbt convierte tus consultas SQL en un proyecto con dependencias, materializaciones, pruebas y documentación; el grafo… |
| `docker-para-datos` | Docker para datos | intermedio | `de`, `ds` | Una imagen empaqueta tu código con sus librerías y sus versiones exactas, para que el mismo trabajo se ejecute igual… |
| `duckdb-y-analitica-local` | DuckDB y analítica local | intermedio | `de`, `ds` | Un motor SQL analítico dentro de tu propio proceso: consulta Parquet y CSV de varios gigabytes sin servidor, sin… |
| `enmascarado-y-retencion` | Enmascarado y retención | avanzado | `de` | Hash, tokenización y k-anonimato aplicados a un almacén real, y cómo se borra un dato a petición sin romper el… |
| `esquema-estrella-y-copo` | Esquema en estrella y copo de nieve | intermedio | `de` | La estrella deja las dimensiones planas y el copo de nieve las normaliza; la primera gana casi siempre en analítica, y… |
| `etl-vs-elt` | ETL frente a ELT | básico | `de` | Transformar antes o después de cargar los datos: la misma tubería con las etapas en otro orden, y una decisión que… |
| `eventos-push-y-webhooks` | Eventos push y webhooks | intermedio | `de` | Cuando el origen empuja en vez de esperar a que lo consultes: cómo verificar la firma, por qué llegan duplicados y qué… |
| `evolucion-de-esquema` | Evolución de esquema | intermedio | `de` | Cambiar el esquema de una tabla sin romper a quien la lee: qué operaciones son seguras, cuáles exigen coordinación y… |
| `feature-store` | Feature store | experto | `de`, `ds` | Un feature store garantiza que la variable que el modelo vio al entrenar es la misma que verá al predecir, con el… |
| `flink-y-procesamiento-de-eventos` | Flink y procesamiento de eventos | avanzado | `de` | Un motor que procesa evento a evento con estado y watermarks, en lugar de micro-lotes: qué gana, qué complica y cuándo… |
| `gobierno-y-privacidad` | Gobierno y privacidad del dato | avanzado | `de`, `ds` | Quien responde de cada dato, cuánto tiempo se guarda, con qué base jurídica y cómo se borra: gobierno y privacidad son… |
| `hechos-y-dimensiones` | Tablas de hechos y dimensiones | intermedio | `de` | La tabla de hechos guarda lo que se mide y las dimensiones lo que describe; las claves sustitutas y el grano son lo… |
| `iac-y-terraform` | Infraestructura como código | avanzado | `de`, `ds` | Describir servidores, redes y permisos en ficheros versionados permite revisar los cambios como código, recrear el… |
| `iam-y-permisos-cloud` | Identidad y permisos en la nube | intermedio | `de`, `alg` | Quién puede hacer qué sobre qué recurso: roles, políticas, mínimo privilegio y por qué el comodín de permisos es el… |
| `idempotencia-y-reintentos` | Idempotencia y reintentos | avanzado | `de`, `alg` | Una tarea idempotente se puede repetir sin duplicar ni corromper nada; es lo que convierte un reintento en una red de… |
| `ingesta-incremental-y-cdc` | Ingesta incremental y CDC | avanzado | `de` | Leer solo lo que ha cambiado en vez de copiar la tabla entera: tres formas de hacerlo y por qué la más fiable es leer… |
| `kafka-y-colas` | Kafka y colas de mensajes | avanzado | `de` | Un registro distribuido y ordenado por partición donde los productores escriben y cada consumidor lee a su ritmo; la… |
| `kubernetes-basico` | Kubernetes básico | avanzado | `de`, `ds` | Describes cuántas copias de tu contenedor quieres y Kubernetes las mantiene vivas, repartidas y accesibles; el precio… |
| `lakehouse-y-table-formats` | Lakehouse y formatos de tabla | avanzado | `de` | Una capa de metadatos sobre Parquet que aporta transacciones, viaje en el tiempo y esquema evolutivo: Delta Lake,… |
| `lambda-y-kappa` | Arquitecturas lambda y kappa | avanzado | `de` | Dos formas de resolver «lote y tiempo real»: lambda mantiene dos caminos que hay que reconciliar, kappa uno solo que… |
| `mlops-y-cicd-de-modelos` | MLOps y CI/CD de modelos | avanzado | `ds`, `de` | Versionar código, datos, entorno y semilla; validar los datos antes de entrenar y promover un modelo solo si su mejora… |
| `modelado-dimensional` | Modelado dimensional | intermedio | `de` | Organizar los datos analíticos en hechos y dimensiones alrededor de un grano claro: el modelo que entienden las… |
| `monitorizacion-de-drift` | Deriva de datos y de concepto | avanzado | `de`, `ds`, `quant` | Un modelo solo vale para la distribución con la que se entrenó; la deriva es el aviso de que el mundo cambió y la… |
| `normalizacion-vs-desnormalizacion` | Normalización frente a desnormalización | intermedio | `de`, `ds` | Repartir cada dato en un solo sitio para no contradecirte, o duplicarlo a propósito para leer más rápido: el… |
| `nubes-y-servicios-gestionados` | Nubes y servicios gestionados | intermedio | `de` | Alquilar computo, almacen y bases analiticas en vez de montarlos: que se delega, quien paga el tiempo ocioso y por qué… |
| `observabilidad-de-datos` | Observabilidad de datos | avanzado | `de` | Medir frescura, volumen, esquema y distribución contra la historia del propio dato detecta lo que ningún test escrito… |
| `oltp-vs-olap` | OLTP frente a OLAP | básico | `de`, `core` | La base que atiende a la aplicación y la que responde preguntas de negocio tienen formas opuestas; usar una para lo… |
| `orquestacion-y-dag` | Orquestación y DAG | intermedio | `de` | Un grafo dirigido sin ciclos que dice qué tarea depende de cuál, cuándo se ejecuta cada una y qué hacer cuando una… |
| `parquet-avro-orc` | Parquet, Avro y ORC | intermedio | `de`, `ds` | Columnar frente a orientado a fila: por qué Parquet lee solo lo que necesitas, dónde encaja Avro y qué aporta ORC, con… |
| `particionado-y-clustering` | Particionado y clustering | avanzado | `de` | Cortar la tabla por fecha o región para que cada consulta lea solo su trozo, elegir la cardinalidad correcta y ordenar… |
| `problema-de-ficheros-pequenos` | El problema de los ficheros pequeños | avanzado | `de` | Miles de ficheros diminutos hunden un lago porque listar cuesta más que leer: compactación, tamaño objetivo y por qué… |
| `reconciliacion-y-pruebas` | Reconciliación y pruebas de datos | intermedio | `de` | Cuadrar el origen con el destino, escribir pruebas que fallen solas y guardar los recuentos para saber si el dato de… |
| `registro-de-esquemas` | Registro de esquemas | avanzado | `de` | El contrato que productores y consumidores comparten en streaming, y por qué añadir un campo sin valor por defecto… |
| `registros-rechazados-y-cuarentena` | Registros rechazados, cuarentena y parada del pipeline | avanzado | `de` | Qué hacer con la fila que no cumple las reglas: apartarla con su motivo, reprocesarla después o parar el lote entero… |
| `reverse-etl` | Reverse ETL | intermedio | `de` | Devolver al CRM, al soporte y a los anuncios lo que el almacén ya sabe del cliente: escritura por clave, campos con un… |
| `scd-dimensiones-cambiantes` | Dimensiones que cambian (SCD) | avanzado | `de`, `ds` | Como guardar la historia de un atributo que cambia sin reescribir el pasado: tipos 1, 2, 3 y 6, claves sustitutivas y… |
| `spark-fundamentos` | Spark: fundamentos | avanzado | `de`, `core` | Un motor distribuido con evaluación perezosa: qué es un RDD, qué añade el DataFrame y por qué no es «Pandas en grande». |
| `spark-joins-y-skew` | Spark: uniones y asimetría | experto | `de` | Unir tablas reparte claves entre tareas; cuando una clave concentra media tabla, esa tarea decide cuánto tarda el… |
| `spark-particiones-y-shuffle` | Spark: particiones y shuffle | experto | `de` | El shuffle reescribe y reordena todos los datos entre ejecutores; es la operación más cara de Spark y decide si un… |
| `streaming-tiempo-real` | Streaming: ventanas y marcas de agua | experto | `de` | Cuándo ocurrió un evento no es cuándo llegó: ventanas, marcas de agua, tolerancia a tardanzas y la letra pequeña de… |
| `ventanas-y-watermarks` | Ventanas y marcas de agua | avanzado | `de` | Cuándo cerrar una ventana de agregación, cuánto esperar a los datos que llegan tarde y qué hacer con los que aparecen… |

## f05 — Exploración y series temporales (29 conceptos)

| id | título | nivel | rutas | resumen |
| --- | --- | --- | --- | --- |
| `analisis-de-supervivencia` | Análisis de supervivencia | experto | `ds`, `quant` | Modelar el tiempo hasta un evento cuando muchos casos aún no lo han sufrido: función de supervivencia, Kaplan-Meier,… |
| `anomalias-en-series-temporales` | Anomalías en series temporales | intermedio | `ds`, `de` | En una serie con deriva y ciclo, el z-score global no marca nada; hay que detectar sobre el residuo, con una escala… |
| `arima-sarima` | ARIMA y SARIMA | avanzado | `ds`, `quant` | Autorregresión, diferencias y media móvil combinadas para pronosticar una serie, con la versión estacional que repite… |
| `autocorrelacion-acf-pacf` | Autocorrelación, ACF y PACF | intermedio | `ds`, `quant` | Cuanto se parece una serie a sí misma desplazada k pasos, y qué queda de ese parecido cuando descuentas los retardos… |
| `desbalanceo-de-clases` | Desbalanceo de clases | intermedio | `ds`, `quant` | Cuando el 1 % de los casos son positivos, el accuracy engaña; lo que hay que ajustar es la métrica, el peso de las… |
| `descomposicion-stl` | Descomposición STL | intermedio | `ds`, `quant` | Separa una serie en tendencia, estacionalidad y residuo con suavizados locales, y deja que el patrón estacional cambie… |
| `diagnostico-de-residuos` | Diagnóstico de residuos | avanzado | `ds`, `quant` | Los cuatro contrastes que se hacen después de cada ajuste (Ljung-Box, Jarque-Bera, ARCH-LM y Durbin-Watson) y cómo… |
| `distribuciones-en-datos-reales` | Distribuciones en datos reales | intermedio | `core`, `ds`, `quant` | Los datos reales casi nunca son normales: tienen colas gordas, dos picos, cortes por censura, ceros de más o son… |
| `eda-pasos` | Análisis exploratorio: el método | básico | `core`, `ds`, `de` | Una rutina ordenada para conocer un dataset antes de modelarlo: qué es una fila, qué falta, qué rangos son posibles,… |
| `encoding-de-categoricas` | Codificación de categóricas | intermedio | `ds`, `de` | Convertir categorías en números sin inventar un orden y sin colar la variable objetivo: one-hot, ordinal, frecuencia y… |
| `escalado-y-transformacion` | Escalado y transformación | intermedio | `ds`, `core` | Poner las variables en unidades comparables y acercar su forma a la normal: imprescindible en unos modelos,… |
| `estacionariedad` | Estacionariedad | intermedio | `ds`, `quant` | Media, varianza y autocovarianza que no dependen del momento en que miras la serie; el supuesto que casi todo modelo… |
| `frecuencia-y-agregacion-temporal` | Frecuencia, granularidad y agregación | intermedio | `de`, `ds` | Bajar de frecuencia no es resumir: promediar borra los picos, sumar un nivel da un número sin sentido y un ratio mal… |
| `fuga-de-datos` | Fuga de datos (data leakage) | avanzado | `ds`, `de`, `quant` | Información que el modelo ve al entrenar y no existirá al predecir: el error que hace que un modelo parezca perfecto… |
| `garch-volatilidad` | GARCH y volatilidad | avanzado | `quant`, `ds` | La varianza de hoy depende del shock de ayer y de la volatilidad de ayer; modelarla por separado es lo que permite… |
| `hmm-regimenes` | Cadenas de Markov ocultas | experto | `quant`, `ds` | Un modelo de estados ocultos que cambian con una cadena de Markov: estima en qué régimen estas, cuanto dura y cuando… |
| `imputacion-de-datos` | Imputación de datos | intermedio | `ds`, `de` | Rellenar los huecos con media, mediana, modelo o KNN cambia la distribución; casi siempre hay que dejar además una… |
| `ingenieria-de-features` | Ingeniería de variables | avanzado | `ds`, `de`, `quant` | Construir variables que resumen lo que sabes del problema: cocientes, diferencias, ventanas pasadas y agregados por… |
| `outliers-y-deteccion` | Valores atípicos | intermedio | `core`, `ds`, `quant` | Detectar un valor que se aleja del resto es fácil; decidir si es un error de medición, un dato mal tecleado o el… |
| `prediccion-con-incertidumbre` | Predicción con incertidumbre | avanzado | `ds`, `quant` | Un número suelto esconde la parte que más importa: dar un intervalo con la cobertura prometida en vez de un único valor. |
| `prevision-a-varios-pasos` | Previsión a varios pasos | intermedio | `ds`, `quant` | Predecir doce meses no es repetir doce veces la predicción de uno; la recursiva, la directa y la multi-salida se… |
| `pronosticos-de-referencia-y-mase` | Pronósticos de referencia y MASE | básico | `ds`, `quant` | El naive, el naive estacional y la deriva son el listón que hay que batir antes de creerse un modelo, y el MASE es la… |
| `prophet-y-modelos-modernos` | Prophet y modelos modernos | intermedio | `ds`, `quant` | Prophet descompone la serie en tendencia, estacionalidad y festivos; N-BEATS apila bloques densos y DeepAR aprende de… |
| `seleccion-de-features` | Selección de variables | avanzado | `ds`, `core` | Quedarse con las variables que aportan y tirar el resto: filtros, envolventes y métodos embebidos, con la estabilidad… |
| `series-jerarquicas` | Series jerárquicas y reconciliación | avanzado | `ds`, `quant` | Predecir por separado el total, las tiendas y los productos da cifras que no suman; la reconciliación reparte el… |
| `series-temporales-componentes` | Componentes de una serie temporal | básico | `ds`, `quant`, `de` | Toda serie temporal se lee como suma de una tendencia, un patrón que se repite, ciclos largos y ruido; separarlos es… |
| `suavizado-exponencial` | Suavizado exponencial | intermedio | `ds`, `quant` | Media ponderada en la que lo reciente pesa más, con variantes para tendencia y estacionalidad; el pronóstico barato… |
| `test-adf-kpss` | Tests de raíz unitaria: ADF y KPSS | avanzado | `ds`, `quant` | Dos contrastes con hipótesis nulas opuestas para decidir si una serie necesita diferenciarse, y por qué hay que… |
| `validacion-temporal` | Validación temporal | avanzado | `ds`, `quant` | Por qué el K-fold barajado miente con datos ordenados en el tiempo y cómo se evalúa de verdad, con ventanas hacia… |

## f06 — Machine learning clásico (49 conceptos)

| id | título | nivel | rutas | resumen |
| --- | --- | --- | --- | --- |
| `aprendizaje-activo` | Aprendizaje activo | experto | `ds` | Elegir que filas etiquetar para aprender mas con menos anotaciones: incertidumbre, comite, diversidad y criterios de… |
| `aprendizaje-semi-supervisado` | Aprendizaje semisupervisado | experto | `ds` | Aprovechar millones de filas sin etiquetar con autosupervisión, pseudoetiquetado y propagación de etiquetas cuando… |
| `arboles-de-decision` | Árboles de decisión | básico | `ds` | Dividir los datos con preguntas binarias eligiendo el corte que más reduce la impureza: potente, interpretable y… |
| `automl` | AutoML | intermedio | `ds` | Busqueda automática de modelos, variables e hiperparámetros: acelera el punto de partida y no sustituye a entender el… |
| `bagging-y-random-forest` | Bagging y Random Forest | intermedio | `ds`, `quant` | Entrenar muchos árboles sobre muestras bootstrap y promediar: baja la varianza, y el submuestreo de variables evita… |
| `bandits-y-decision-secuencial` | Bandits y decisión secuencial | avanzado | `ds`, `quant` | Decidir y aprender a la vez: epsilon-greedy, UCB y Thompson sampling reparten las pruebas entre la opción que crees… |
| `calibracion` | Calibración de probabilidades | avanzado | `ds` | Que un 0,7 sea de verdad un 70 por ciento: cómo se mide la calibración, cómo se arregla y por qué el AUC no la ve. |
| `clustering-jerarquico` | Clustering jerárquico | intermedio | `ds` | Construir un árbol de agrupaciones de abajo arriba, elegir el criterio de enlace y decidir el número de grupos… |
| `datos-geoespaciales` | Datos geoespaciales | intermedio | `ds`, `de` | Coordenadas, proyecciones y unir por cercanía en vez de por igualdad: por qué un grado de longitud no mide lo mismo en… |
| `dbscan-y-hdbscan` | DBSCAN y HDBSCAN | avanzado | `ds`, `alg` | Agrupar por densidad en vez de por distancia al centro: encuentra formas arbitrarias, marca el ruido y no obliga a… |
| `deteccion-de-anomalias` | Detección de anomalías | avanzado | `ds`, `de` | Encontrar lo raro cuando nadie te ha dicho qué es raro: puntuaciones de rareza, umbrales que son una decisión de… |
| `entrenamiento-frente-a-inferencia` | Coherencia entre entrenamiento e inferencia | avanzado | `ds`, `de` | Un modelo acierta en producción solo si el dato llega transformado igual que en el entrenamiento; la mitad de los… |
| `etiquetas-y-techo-del-modelo` | Calidad de las etiquetas y techo del modelo | avanzado | `ds` | Cuánto rendimiento te está costando el ruido de las etiquetas y cómo estimar el techo real de un modelo antes de… |
| `fairness-y-equidad` | Equidad y métricas de fairness | avanzado | `ds` | Paridad demográfica, igualdad de oportunidades y calibración por grupos: tres definiciones razonables de «justo» que… |
| `glm-y-logistica` | Modelos lineales generalizados y regresión logística | intermedio | `ds`, `core` | Cuando la respuesta no es continua: función de enlace, odds, logit y por qué la regresión logística es el GLM más… |
| `gmm` | Mezclas gaussianas | avanzado | `ds`, `core` | Cada punto pertenece a cada grupo con una probabilidad, y el algoritmo EM alterna asignar esas probabilidades y… |
| `gradient-boosting` | Gradient boosting | avanzado | `ds`, `quant` | Sumar árboles pequeños que corrigen el error del anterior: la receta que domina los datos tabulares y en la que cada… |
| `importancia-de-variables` | Importancia de variables | intermedio | `ds` | La importancia no es una propiedad de la variable sino del modelo y de las demás variables; impureza, permutación y… |
| `interpretabilidad-shap` | Interpretabilidad y SHAP | avanzado | `ds` | Que parte de una predicción concreta se atribuye a cada variable: valores de Shapley, curvas PDP e ICE y los límites… |
| `k-means` | K-means | intermedio | `ds` | Agrupar puntos alrededor de k centroides minimizando la suma de distancias al cuadrado, con el método del codo para… |
| `knn` | K vecinos más cercanos | básico | `ds`, `alg` | Guardar los datos y decidir por mayoría entre los k vecinos más parecidos: el modelo más simple que existe y el que… |
| `maldicion-de-la-dimensionalidad` | Maldición de la dimensionalidad | avanzado | `ds`, `alg` | Al añadir dimensiones el espacio se vacía, las distancias se igualan y el vecino más cercano deja de serlo; qué hacer… |
| `matriz-de-confusion` | Matriz de confusión | básico | `core`, `ds` | La tabla de cuatro casillas que cuenta aciertos y errores de un clasificador binario, y el punto de partida de casi… |
| `metricas-de-clasificacion` | Métricas de clasificación | básico | `core`, `ds` | Exactitud, precisión, exhaustividad, F1 y balanced accuracy: cuál elegir según lo que cueste cada tipo de error. |
| `metricas-de-clustering` | Métricas de clustering | intermedio | `ds` | Sin etiquetas no hay exactitud que calcular, así que un agrupamiento se juzga por su geometría con silueta,… |
| `metricas-de-ranking` | Métricas de ranking | avanzado | `ds`, `alg` | Precision@k, recall@k, MAP, MRR y NDCG: cómo se evalúa un sistema cuando lo que importa es el orden y solo se mira la… |
| `metricas-de-regresion` | Métricas de regresión | básico | `core`, `ds` | MAE, MSE, RMSE, MAPE y R cuadrado: qué mide cada una, en qué unidades está y en qué casos engaña. |
| `naive-bayes` | Naive Bayes | intermedio | `ds` | Clasificador probabilístico que supone que las variables son independientes dada la clase; el supuesto es falso y aun… |
| `paradigmas-de-aprendizaje` | Paradigmas de aprendizaje | básico | `core`, `ds` | Supervisado, no supervisado, semisupervisado, autosupervisado y por refuerzo: lo que cambia entre ellos es de dónde… |
| `pca` | Análisis de componentes principales | intermedio | `ds`, `core` | Sustituye variables correlacionadas por unas pocas direcciones que concentran la varianza, y deja claro qué… |
| `pipelines-de-ml` | Pipelines de machine learning | intermedio | `ds` | Encadenar imputación, escalado y modelo en un solo objeto: la forma practica de que ninguna transformación se ajuste… |
| `precision-recall-y-pr` | Curva precisión-exhaustividad | intermedio | `ds` | La curva que mide lo que de verdad importa cuando el positivo es raro, con una línea base que es la prevalencia y no… |
| `procesamiento-de-texto-clasico` | Procesamiento de texto clásico | intermedio | `ds`, `de` | Contar palabras y ponderarlas por lo raras que son sigue ganando en textos cortos, tabulares o con pocos datos; el… |
| `recomendadores` | Sistemas de recomendación | avanzado | `ds`, `alg` | Filtrado colaborativo, basado en contenido y factorización de matrices, con la parte que casi nadie hace bien: evaluar… |
| `reglas-de-asociacion` | Reglas de asociación | intermedio | `de`, `ds` | Convertir millones de tickets en reglas del tipo «quien compra pan compra mantequilla», con el lift como único número… |
| `regresion-lineal` | Regresión lineal | básico | `core`, `ds` | Ajustar la recta que minimiza la suma de errores al cuadrado, leer sus coeficientes con sentido y no confundirla con… |
| `regularizacion-l1-l2` | Regularización L1 y L2 | intermedio | `ds`, `quant` | Ridge encoge los coeficientes y Lasso lleva algunos a cero: cómo la penalización cambia el equilibrio sesgo-varianza y… |
| `roc-auc` | Curva ROC y AUC | intermedio | `ds` | El rastro que deja un clasificador al mover su umbral y el área bajo esa curva, con el sesgo que esconde cuando el… |
| `seleccion-de-hiperparametros` | Búsqueda de hiperparámetros | intermedio | `ds` | Rejilla, búsqueda aleatoria, bayesiana y Hyperband: cómo repartir el presupuesto de entrenamientos sin sobreajustar la… |
| `sesgo-varianza` | Compromiso sesgo-varianza | intermedio | `core`, `ds` | El error al predecir datos nuevos se reparte entre ruido irreducible, sesgo y varianza; la curva que explica por qué… |
| `stacking-y-blending` | Stacking y blending | experto | `ds`, `quant` | Combinar varios modelos con un metamodelo entrenado sobre predicciones fuera de muestra; la diferencia entre ganar y… |
| `supuestos-de-la-regresion` | Supuestos de la regresión | intermedio | `ds`, `quant` | Linealidad, independencia, homocedasticidad y normalidad: qué rompe cada supuesto, qué sigue funcionando y cómo se… |
| `svm` | Máquinas de vectores de soporte | avanzado | `ds`, `quant` | Separar dos clases con el hiperplano que deja el mayor margen posible, usando solo los puntos fronterizos y un núcleo… |
| `train-val-test` | Conjuntos de entrenamiento, validación y prueba | básico | `core`, `ds` | Tres particiones con tres papeles distintos: entrenar, decidir y medir una sola vez. Mirar el test más de la cuenta lo… |
| `tsne-y-umap` | t-SNE y UMAP | avanzado | `ds` | Dos formas de dibujar datos de muchas dimensiones en un plano que conservan los vecindarios y se inventan el resto:… |
| `umbrales-y-coste` | Umbrales y coste del error | avanzado | `ds`, `quant` | El 0,5 es una convención, no una decisión: el punto de corte correcto sale del coste real de cada falso positivo y… |
| `uplift-y-valor-incremental` | Uplift y valor incremental | avanzado | `ds` | El efecto de intervenir frente a no hacerlo, medido sobre quien de verdad cambia de comportamiento y no sobre quien ya… |
| `validacion-cruzada` | Validación cruzada | intermedio | `core`, `ds` | Partir los datos en k pliegues para estimar y elegir sin gastar un conjunto de prueba, con variantes para clases… |
| `xgboost-lightgbm-catboost` | XGBoost, LightGBM y CatBoost | avanzado | `ds`, `quant` | Los tres motores de boosting que dominan los datos tabulares: en qué se diferencian al crecer los árboles y cuándo… |

## f07 — Deep learning (33 conceptos)

| id | título | nivel | rutas | resumen |
| --- | --- | --- | --- | --- |
| `aprendizaje-por-refuerzo` | Aprendizaje por refuerzo | experto | `ds` | Un agente actua sobre un entorno, recibe recompensas y aprende una política que maximiza el retorno acumulado a base… |
| `atencion` | Mecanismos de atención | experto | `ds` | En vez de comprimir toda la secuencia en un estado fijo, cada posición consulta a todas las demás y se queda con lo… |
| `autoencoders-y-vae` | Autoencoders y VAE | avanzado | `ds` | Comprimir la entrada en un cuello de botella y reconstruirla: sirve para reducir dimensión, detectar anomalías y, con… |
| `cnn` | Redes convolucionales | avanzado | `ds` | Deslizar el mismo filtro diminuto por toda la imagen y compartir los pesos permite ver bordes, texturas y objetos con… |
| `cuantizacion-y-destilacion` | Cuantización y destilación | avanzado | `ds` | Dos formas independientes de encoger un modelo: gastar menos bits por peso (cuantización) o entrenar una red pequeña… |
| `depuracion-de-redes` | Depurar el entrenamiento | avanzado | `ds` | Perdidas que no bajan, perdidas que son NaN y modelos que solo aprenden un lote: el método para aislar cada fallo con… |
| `dropout-y-regularizacion` | Dropout y regularización | intermedio | `ds` | Apagar neuronas al azar, encoger los pesos, parar a tiempo o inventar datos que no cambian la etiqueta: cuatro formas… |
| `embeddings` | Embeddings | intermedio | `ds` | Convertir palabras y categorías en vectores densos donde la distancia significa parecido: la base del texto, los… |
| `evaluacion-de-modelos-generativos` | Evaluar un modelo generativo | avanzado | `ds` | Fidelidad frente a diversidad: por qué ninguna métrica sola dice si un modelo generativo es bueno, qué mide cada… |
| `exportar-y-servir-modelos` | Exportar y servir modelos | avanzado | `ds`, `de` | Pasar un modelo entrenado a algo que corre fuera de tu portátil: ONNX, TorchScript, torch.compile y por qué el… |
| `fine-tuning-y-lora` | Ajuste fino y LoRA | avanzado | `ds` | Entrenar todos los pesos, solo una cabeza nueva o un par de matrices pequenas por capa: la diferencia esta en memoria,… |
| `funciones-de-activacion` | Funciones de activación | intermedio | `ds` | Sigmoide, tanh, ReLU y GELU: por qué sin no linealidad una red de veinte capas equivale a una regresión lineal |
| `funciones-de-perdida` | Funciones de pérdida | intermedio | `ds` | El número que el entrenamiento empuja hacia abajo en cada paso; elegir la pérdida es decidir qué error te importa y… |
| `gan` | Redes generativas adversarias | experto | `ds` | Dos redes que compiten: una fabrica muestras y la otra intenta distinguirlas. El equilibrio existe en teoria y es… |
| `gnn` | Redes sobre grafos | experto | `ds` | Cada nodo se representa agregando información de sus vecinos, capa a capa: la estructura del grafo entra en el modelo… |
| `gpu-y-rendimiento` | GPU y rendimiento | avanzado | `ds` | Por qué una GPU entrena redes y cómo aprovecharla de verdad: memoria, precisión mixta, acumulación de gradiente y los… |
| `grafos-computacionales-y-autograd` | Grafos computacionales y autograd | avanzado | `ds` | Cada operación con tensores construye un grafo; backward lo recorre al revés con la regla de la cadena y deja la… |
| `inicializacion-de-pesos` | Inicialización de pesos | avanzado | `ds` | Los pesos se sortean al azar antes de entrenar y la escala de ese sorteo decide si la señal sobrevive a diez capas o… |
| `modelos-de-difusion` | Modelos de difusión | experto | `ds` | Un proceso fijo que destruye los datos con ruido y una red que aprende a deshacer un paso cada vez: generación estable… |
| `normalizacion-por-lotes` | Normalización por lotes | avanzado | `ds` | Reescala las activaciones de cada capa a media cero y varianza uno dentro del lote, y deja que la red reaprenda con… |
| `optimizadores` | Optimizadores | avanzado | `ds` | La regla que convierte el gradiente en un paso sobre los pesos; SGD, momento, RMSprop, Adam y AdamW hacen cosas… |
| `perceptron-y-mlp` | Perceptrón y perceptrón multicapa | básico | `ds` | La neurona, el sesgo, las capas y el teorema que explica por qué una capa oculta ya resuelve lo que una recta no puede |
| `pytorch-fundamentos` | PyTorch: fundamentos | intermedio | `ds` | Tensores que recuerdan cómo se calcularon, un módulo con sus parámetros, un cargador de lotes y un bucle de cinco… |
| `q-learning-y-policy-gradient` | Q-learning y gradiente de política | experto | `ds` | Las dos familias del refuerzo profundo: aprender el valor de cada accion y actuar con avaricia, o parametrizar la… |
| `reproducibilidad-del-entrenamiento` | Reproducibilidad del entrenamiento | intermedio | `ds`, `alg` | Por qué dos ejecuciones con el mismo código no dan el mismo número, qué fuentes de azar hay que fijar y qué parte del… |
| `retropropagacion` | Retropropagación | avanzado | `ds` | La regla de la cadena aplicada capa a capa, con el grafo computacional, los deltas y una comprobación numérica del… |
| `rnn-lstm-gru` | RNN, LSTM y GRU | avanzado | `ds` | Una red que se pasa su propio estado de un paso al siguiente, y las puertas que añaden LSTM y GRU para que el… |
| `seguimiento-de-experimentos` | Seguimiento de experimentos | intermedio | `ds`, `alg` | Qué guardar de cada ejecución para poder comparar dos configuraciones sin fiarte de la memoria, y cómo saber si una… |
| `sobreajuste-en-redes` | Sobreajuste en redes | intermedio | `ds` | Aprender a leer las dos curvas de un entrenamiento para detectar sobreajuste y decidir en que orden tocar datos,… |
| `tasas-de-aprendizaje-y-schedulers` | Tasa de aprendizaje y planificadores | avanzado | `ds` | El hiperparámetro que más cambia el resultado, y cómo moverlo durante el entrenamiento con calentamiento, escalones o… |
| `tokenizacion` | Tokenización | intermedio | `ds` | Partir el texto en unidades antes de convertirlo en vectores: BPE, WordPiece y por qué los números, los acentos y las… |
| `transfer-learning` | Aprendizaje por transferencia | intermedio | `ds` | Reutilizar un modelo ya entrenado en otra tarea y adaptarlo a la tuya con pocas etiquetas, en vez de empezar de cero… |
| `transformers` | Transformers | experto | `ds` | Autoatención multi-cabeza, sin recurrencia y en paralelo: el bloque que compone casi todos los modelos de lenguaje… |

## f08 — LLMs e IA generativa (22 conceptos)

| id | título | nivel | rutas | resumen |
| --- | --- | --- | --- | --- |
| `agentes-y-herramientas` | Agentes y uso de herramientas | avanzado | `ds` | Un modelo que decide qué herramienta llamar, con qué argumentos y cuándo parar: cómo se cierra el bucle, qué se guarda… |
| `alucinaciones-y-limites` | Alucinaciones y límites | intermedio | `ds` | Por qué un modelo inventa datos con total seguridad, cómo se detecta una respuesta sin apoyo en las fuentes y qué… |
| `bases-de-datos-vectoriales` | Bases de datos vectoriales | avanzado | `ds`, `de` | Índices para buscar el vecino más cercano entre millones de vectores: qué hacen HNSW e IVF, qué recall sacrifican y… |
| `chunking-y-embeddings` | Troceado y embeddings | avanzado | `ds` | Como se corta el texto antes de vectorizarlo: tamaño de fragmento, solapamiento y por qué la frontera elegida decide… |
| `como-funciona-un-llm` | Cómo funciona un LLM | intermedio | `ds` | Un LLM solo predice el siguiente token; todo lo demas (chat, código, resumenes) es repetir esa predicción dentro de… |
| `coste-y-latencia` | Coste y latencia | intermedio | `ds`, `de` | El presupuesto de una consulta se decide con tres números (tokens de entrada, de salida y aciertos de caché) y la… |
| `economia-de-la-inferencia-propia` | Economía de la inferencia propia | avanzado | `ds`, `de` | Pagar por token o alquilar la GPU son dos estructuras de coste distintas, y quien decide no es el precio de la hora… |
| `evaluacion-de-llms` | Evaluación de LLMs | avanzado | `ds` | Como se mide si un sistema con modelos de lenguaje funciona: conjuntos de prueba propios, métricas automáticas, jueces… |
| `fine-tuning-vs-rag` | Ajuste fino frente a RAG | avanzado | `ds` | RAG cambia lo que el modelo lee; el ajuste fino cambia cómo se comporta. Casi siempre se empieza por RAG, y aquí se… |
| `instruccion-y-alineamiento` | Instrucción y alineamiento | avanzado | `ds` | Como se pasa de un modelo que solo continua texto a un asistente que obedece: ajuste sobre instrucciones, modelos de… |
| `mcp-y-servidores-de-herramientas` | MCP y servidores de herramientas | avanzado | `ds`, `alg` | El protocolo que convierte cada herramienta en un servidor reutilizable: un solo cliente habla con todos los… |
| `modelos-multimodales` | Modelos multimodales | intermedio | `ds` | Cómo una imagen o un audio acaban siendo tokens dentro del mismo contexto que el texto, cuánto ocupan de verdad y por… |
| `motores-de-inferencia-para-llms` | Servir un LLM en abierto: motores y cuantización | avanzado | `ds`, `de` | Generar un token está limitado por el ancho de banda de memoria, no por los FLOPs: de ahí salen la cuantización, el… |
| `observabilidad-de-llms` | Observabilidad de una aplicación con LLM | avanzado | `ds`, `alg` | Qué grabar de cada consulta, en qué forma y para qué: sin trazas por paso ni tokens medidos, un sistema con LLM no se… |
| `preentrenamiento-y-escalado` | Preentrenamiento y escalado | avanzado | `ds` | Como se construye un corpus, que se optimiza durante el preentrenamiento y por qué el tamaño de un modelo se decide… |
| `privacidad-y-datos-en-llms` | Privacidad de datos en LLMs | avanzado | `ds` | Cada prompt es una transferencia de datos a un tercero: que sale, quién lo recibe, cuánto se guarda y que no debería… |
| `prompting` | Ingeniería de prompts | básico | `ds` | Un prompt es el enunciado de la tarea: rol, contexto, ejemplos, formato y criterio de exito, y se mejora midiendo, no… |
| `rag-arquitectura` | RAG: arquitectura | avanzado | `ds` | Recuperar, aumentar y generar: el patron completo de RAG, sus seis etapas y los puntos donde se rompe la cadena antes… |
| `reranking` | Reordenación | avanzado | `ds` | Recuperar cien candidatos rápido y barato, y reordenarlos con un modelo que lee consulta y documento juntos: la forma… |
| `seguridad-y-prompt-injection` | Seguridad e inyección de prompts | avanzado | `ds` | El modelo no distingue instrucciones de datos, así que cualquier texto externo es un vector de ataque: la defensa está… |
| `structured-output` | Salida estructurada | intermedio | `ds`, `de` | Pedir al modelo un objeto con campos y tipos, validarlo contra un esquema y reintentar con el error: por qué parsear… |
| `ventanas-de-contexto` | Ventana de contexto | intermedio | `ds` | Cuantos tokens caben a la vez, por qué lo del medio se olvida y como trocear y ordenar la información para que el… |

## f09 — Finanzas cuantitativas (61 conceptos)

| id | título | nivel | rutas | resumen |
| --- | --- | --- | --- | --- |
| `algoritmos-de-ejecucion` | Algoritmos de ejecución: VWAP, TWAP e iceberg | avanzado | `quant` | Cómo partir una orden grande en trozos para que no la vea el mercado, y cómo cada algoritmo cambia lo que pagas por el… |
| `alpha-decay` | Decaimiento del alpha | avanzado | `quant`, `ds` | Toda señal pierde fuerza: cómo medir la vida media del alpha, distinguirla del sobreajuste y decidir cuándo una… |
| `alpha-y-beta` | Alpha y beta | intermedio | `quant`, `ds` | Beta es lo que tu estrategia se mueve con el mercado y alpha lo que queda cuando descuentas esa parte; sin el error… |
| `arbitraje-estadistico` | Arbitraje estadístico | experto | `quant`, `ds` | Cientos de posiciones pequeñas para explotar la reversión de lo que los factores no explican, con una sensibilidad al… |
| `backtesting-por-eventos` | Backtesting por eventos | experto | `quant` | Simular el backtest orden por orden, con cola, latencia y ejecuciones parciales, para saber si tu estrategia sobrevive… |
| `backtesting-vectorizado` | Backtesting vectorizado | avanzado | `quant`, `ds` | Calcular la posición y el resultado de toda la serie de golpe con arrays: rapidísimo para explorar ideas y muy fácil… |
| `cointegracion` | Cointegración | experto | `quant`, `ds` | Dos series que vagan sin rumbo pero mantienen una combinación lineal estacionaria: la base estadística del trading de… |
| `construccion-de-carteras` | Construcción de carteras | avanzado | `quant`, `ds` | Combinar varias estrategias o activos con pesos decididos, de forma que el conjunto tenga mejor relación entre… |
| `criterio-de-kelly` | Criterio de Kelly | avanzado | `quant` | La fracción del capital que maximiza el crecimiento esperado a largo plazo: ni tan poca que desaprovechas la ventaja,… |
| `curva-de-tipos-y-descuento` | Curva de tipos y descuento | intermedio | `quant` | Por qué el tipo de interés depende del plazo, qué es el factor de descuento y cómo un punto de tipos mueve mucho más… |
| `data-snooping-y-multiple-testing` | Data snooping y pruebas múltiples | avanzado | `quant`, `ds` | Si pruebas muchas ideas y te quedas con la mejor, el resultado está sesgado: cuántos intentos hacen falta para que el… |
| `diferenciacion-fraccional` | Diferenciación fraccional | experto | `quant`, `ds` | Diferenciar con orden fraccionario hace estacionaria una serie conservando su memoria: gana el test de raíz unitaria… |
| `ecuaciones-diferenciales-estocasticas` | Ecuaciones diferenciales estocásticas | avanzado | `quant` | Cómo se escribe un modelo de precio como deriva más ruido, y cómo se simula sin que el paso temporal mienta sobre la… |
| `factores-y-fama-french` | Factores y Fama-French | avanzado | `quant`, `ds` | Más allá del mercado: tamaño, valor, momentum y calidad explican parte de lo que el CAPM deja fuera y hunden el alpha… |
| `generacion-de-senales` | Generación de señales | avanzado | `quant`, `ds` | De la idea económica a una regla medible: universo, horizonte, IC, giro y capacidad, en ese orden y antes de escribir… |
| `griegas-y-cobertura` | Griegas y cobertura | experto | `quant` | Las derivadas del precio de una opción, y cómo se resuelve la cartera que deja la exposición a cero sin apostar a la… |
| `hurst-y-memoria` | Exponente de Hurst | experto | `quant`, `ds` | Mide cómo crece la dispersión de una serie con el horizonte: 0,5 es un paseo aleatorio, por encima hay persistencia y… |
| `indicadores-tecnicos` | Indicadores técnicos | básico | `quant` | Qué calcula de verdad cada indicador clásico, para qué sirve y por qué optimizar sus parámetros sobre el histórico es… |
| `latencia-y-ejecucion` | Latencia y ejecución | avanzado | `quant` | El tiempo entre decidir y que el mercado vea tu orden solo importa en relación con lo que dura tu ventaja; medirlo mal… |
| `lema-de-ito` | Lema de Itô | experto | `quant` | La regla de la cadena del cálculo estocástico: el término de segundo orden que aparece al derivar y que explica el… |
| `markowitz-y-frontera` | Markowitz y la frontera eficiente | avanzado | `quant`, `ds` | Para cada nivel de riesgo, la cartera con más rentabilidad esperada: la frontera eficiente, por qué es bonita en… |
| `maximo-drawdown` | Caída máxima (max drawdown) | intermedio | `quant` | La mayor caída desde un pico de tu curva de capital hasta el mínimo anterior a recuperarlo: cuánto duele, cuánto dura… |
| `meta-labeling` | Meta-etiquetado | experto | `quant`, `ds` | Un primer modelo decide la dirección de la apuesta y un segundo decide si merece dinero y cuánto: separa el lado del… |
| `metricas-de-riesgo` | Métricas de riesgo: panorama | intermedio | `quant` | Que se mide cuando se mide el riesgo de una estrategia, qué pregunta responde cada familia de métricas y por qué todas… |
| `microestructura-de-mercado` | Microestructura de mercado | avanzado | `quant` | Como se casan las órdenes, quién asume el riesgo de inventario y por qué esa mecánica decide si tu estrategia es… |
| `momentum` | Momentum | intermedio | `quant`, `ds` | Comprar lo que sube funciona en la muestra y duele en la racha: momentum 12-1, por qué se salta el último mes y por… |
| `movimiento-browniano` | Movimiento browniano | intermedio | `quant`, `ds` | El paseo aleatorio en tiempo continuo que sostiene casi todo modelo de precio, y por qué su varianza crece con el… |
| `mql5-y-metatrader` | MQL5 y MetaTrader | intermedio | `quant` | El entorno donde opera la mayoría del trading minorista: qué permite de verdad su probador de estrategias y qué te… |
| `order-book-y-spread` | Libro de órdenes y diferencial | avanzado | `quant` | Bid, ask, profundidad y desequilibrio: como leer el libro de órdenes, que cuesta cruzarlo y que se puede y no se puede… |
| `pairs-trading` | Trading de pares | avanzado | `quant`, `ds` | Dos activos, un diferencial y un z-score: cómo elegir el par, estimar el ratio de cobertura y decidir la salida sin… |
| `paper-trading` | Paper trading | básico | `quant` | Operar con precios reales y órdenes que no existen: sirve para aprender la mecánica de la plataforma, no para saber si… |
| `protocolo-fix` | Protocolo FIX | experto | `quant` | El estándar de mensajería de órdenes entre bancos, brókers y bolsas: campos numerados, byte separador y una sesión con… |
| `prueba-de-fondeo` | Pruebas de fondeo | avanzado | `quant` | Las reglas de una prueba de fondeo (objetivo, límite diario y drawdown máximo) convierten el trading en un problema de… |
| `psicologia-del-trading` | Psicología del trading | básico | `quant` | Por qué una racha de siete pérdidas no significa que el sistema esté roto: plan escrito, un tamaño que aguante y… |
| `purged-kfold` | K-fold con purga y embargo | experto | `quant`, `ds` | Validación cruzada adaptada a etiquetas que solapan en el tiempo: quita del entrenamiento todo lo que toca al conjunto… |
| `quantconnect-y-lean` | QuantConnect y LEAN | intermedio | `quant` | Una plataforma en la nube con datos incluidos y un motor de código abierto: el mismo algoritmo pasa de backtest a… |
| `que-es-un-mercado` | Qué es un mercado | básico | `quant` | Quien compra, quién vende, quién pone el precio y quién cobra: el mapa del mercado antes de tocar una estrategia. |
| `ratio-de-sharpe` | Ratio de Sharpe | intermedio | `quant`, `ds` | Exceso de rentabilidad por unidad de volatilidad asumida; la métrica más citada del trading y la más fácil de inflar… |
| `rebalanceo` | Rebalanceo | intermedio | `quant`, `ds` | Devolver la cartera a sus pesos objetivo, por calendario o por banda: cuánto cuesta de verdad y por qué es una… |
| `regimenes-de-mercado` | Regímenes de mercado | avanzado | `quant`, `ds` | Detectar el clima antes de elegir modelo o exposición, sabiendo que el estado no se observa, que la detección llega… |
| `retornos-logaritmicos` | Retornos logarítmicos | intermedio | `quant`, `ds` | Mide la variación proporcional de un precio, se suma en el tiempo y se anualiza sin trucos, por eso es la unidad de… |
| `reversion-a-la-media` | Reversión a la media | intermedio | `quant`, `ds` | Si una serie vuelve a su nivel habitual, cada desviación es una oportunidad; si pasea, cada desviación es el principio… |
| `riesgo-de-ruina` | Riesgo de ruina | avanzado | `quant` | La probabilidad de perder el capital, o de llegar a un nivel del que ya no puedes seguir, antes de que la ventaja de… |
| `risk-parity-y-hrp` | Risk parity y HRP | experto | `quant`, `ds` | Repartir el riesgo en vez del capital: pesos de igual contribución y la jerarquía de correlaciones que estabiliza la… |
| `sample-weights` | Pesos de muestra | experto | `quant`, `ds` | Con etiquetas que se solapan, varias observaciones cuentan la misma información: pesarlas por su unicidad evita que el… |
| `sesgo-de-mirar-al-futuro` | Sesgo de mirar al futuro | intermedio | `quant`, `ds` | Usar en la decisión de hoy información que solo existía después: el error que convierte cualquier backtest en una… |
| `sesgo-de-supervivencia` | Sesgo de supervivencia | intermedio | `quant`, `ds` | Analizar solo los fondos, acciones o exchanges que siguen vivos y tomar ese grupo como si fuera el mercado entero: la… |
| `sharpe-deflactado` | Sharpe deflactado | experto | `quant`, `ds` | Ajusta el Sharpe observado por el número de intentos y por la forma de la distribución: la probabilidad de que no sea… |
| `simulacion-de-monte-carlo` | Simulación de Monte Carlo | intermedio | `quant`, `ds` | En vez de mirar la única curva que te dio el backtest, generas miles de curvas alternativas a partir de tus resultados… |
| `slippage-y-comisiones` | Deslizamiento y comisiones | intermedio | `quant` | Comisiones, diferencial e impacto: los tres costes que se pagan en cada operación y que convierten una estrategia… |
| `sortino-y-calmar` | Sortino y Calmar | avanzado | `quant` | Dos correcciones al ratio de Sharpe: penalizar solo la volatilidad que duele y medir la rentabilidad contra la peor… |
| `tamano-de-posicion` | Tamaño de posición | avanzado | `quant` | Cuantas unidades abres por idea: riesgo fijo, volatilidad objetivo y límites por correlación, la decisión que… |
| `tick-data-y-ohlcv` | Datos de transacción y velas | básico | `quant`, `de` | Del tick a la vela: cada agregación resume el mercado y borra parte de la historia; saber qué se pierde evita… |
| `triple-barrera` | Etiquetado por triple barrera | experto | `quant`, `ds` | Tres barreras (beneficio, pérdida y tiempo) deciden cuándo se cierra una operación y cuál es su etiqueta, sin usar… |
| `validacion-combinatoria-cpcv` | Validación combinatoria (CPCV) | experto | `quant`, `ds` | Reparte el histórico en bloques y prueba todas las combinaciones posibles: obtienes la distribución de resultados de… |
| `valoracion-de-opciones` | Valoración de opciones | avanzado | `quant` | Por qué una opción tiene un precio único aunque nadie sepa a dónde va el activo: replicación, medida neutral al riesgo… |
| `var-y-cvar` | VaR y CVaR | avanzado | `quant`, `ds` | El VaR pone el umbral de pérdida que no se supera con cierta probabilidad y el CVaR mide la pérdida media cuando ese… |
| `vectorbt-backtrader-zipline` | VectorBT, Backtrader y Zipline | intermedio | `quant` | Las tres librerías de backtesting que más se usan en Python, qué modelo del mundo tiene cada una y para qué sirve cada… |
| `venta-en-corto-mecanica` | Vender en corto: préstamo, coste y recalls | intermedio | `quant` | Vender algo que no tienes tiene fecha de caducidad y precio: quién te lo presta, cuánto cobra por ello y qué pasa… |
| `volatilidad-realizada` | Volatilidad realizada | avanzado | `quant`, `ds` | La raíz de la suma de los retornos intradía al cuadrado mide cuánto se movió el precio de verdad, y es la variable de… |
| `volatility-drag` | Volatility drag | intermedio | `quant`, `core` | Por qué dos carteras con la misma media acaban en sitios distintos, y cómo la volatilidad se come el interés compuesto… |

## f10 — Algoritmos y estructuras (32 conceptos)

| id | título | nivel | rutas | resumen |
| --- | --- | --- | --- | --- |
| `aleatoriedad-y-muestreo` | Aleatoriedad y muestreo | intermedio | `alg`, `ds` | Generadores pseudoaleatorios, semillas, muestreo uniforme y ponderado, y los sesgos que convierten una muestra en una… |
| `algoritmos-de-aproximacion` | Algoritmos de aproximación | experto | `alg`, `quant` | Cuando el óptimo es inalcanzable en tiempo razonable, se renuncia a él a cambio de una garantía demostrable sobre… |
| `algoritmos-de-join` | Algoritmos de join | intermedio | `alg`, `de`, `ds` | Bucle anidado, hash join y sort-merge join: cuándo es viable cada uno, cómo desborda el Grace hash a disco y por qué… |
| `algoritmos-de-streaming` | Algoritmos de streaming | experto | `alg`, `de` | Muestrear, contar y resumir un flujo que no cabe en memoria y que solo pasa una vez, con estructuras cuyo error está… |
| `algoritmos-greedy` | Algoritmos voraces | intermedio | `alg`, `core` | Elegir en cada paso la opción que parece mejor es rapidísimo y a veces óptimo; la diferencia entre las dos cosas hay… |
| `analisis-amortizado` | Análisis amortizado | avanzado | `alg`, `de` | Repartir el coste de una secuencia entre sus operaciones: por qué añadir al final de una lista sale a O(1) aunque… |
| `arboles-balanceados` | Árboles balanceados | avanzado | `alg` | AVL, rojo-negro y B-árboles garantizan altura logarítmica con reglas locales de reequilibrio, y por eso sostienen los… |
| `arboles-binarios` | Árboles binarios y de búsqueda | intermedio | `alg` | Jerarquías de nodos con dos hijos por nodo; ordenados como BST dan búsqueda logarítmica y, sobre todo, recorrido en… |
| `arrays-y-listas` | Arrays y listas | básico | `alg`, `de` | Un array guarda sus elementos uno detrás de otro: por eso el acceso por índice es instantáneo y por eso insertar en el… |
| `arreglos-de-cache-y-lineas-de-cache` | Jerarquía de memoria y localidad de caché | intermedio | `alg`, `de` | Por qué dos programas con las mismas operaciones tardan mil veces distinto: la distancia entre el dato y el núcleo… |
| `bfs-y-dfs` | Recorridos BFS y DFS | intermedio | `alg` | Dos formas de visitar todos los vértices de un grafo; la primera explora por capas y da distancias, la segunda se… |
| `bloom-filters` | Filtros de Bloom | avanzado | `alg`, `de` | Una estructura de unos pocos bits por elemento que responde «seguro que no está» con certeza y «puede que esté» con… |
| `busqueda-binaria` | Búsqueda binaria | básico | `alg`, `core` | Partir el espacio de búsqueda por la mitad en cada paso convierte mil elementos en diez comparaciones, siempre que la… |
| `caminos-minimos` | Caminos mínimos | avanzado | `alg` | Dijkstra, Bellman-Ford, Floyd-Warshall y A* resuelven el mismo problema con supuestos distintos; elegir el que no toca… |
| `complejidad-asintotica` | Complejidad asintótica | básico | `alg`, `de` | Como crece el trabajo de un algoritmo cuando crece la entrada: O, Ω y Θ sirven para comparar dos soluciones sin… |
| `compresion` | Compresión | avanzado | `alg`, `de` | Huffman, LZ y codificación por diccionario: cómo se quita redundancia a los datos, cuál es el límite teórico y por qué… |
| `concurrencia-algoritmica` | Concurrencia y paralelismo | avanzado | `alg` | Varias tareas en curso a la vez: por qué dos operaciones correctas se estropean al intercalarse y qué garantiza de… |
| `divide-y-venceras` | Divide y vencerás | intermedio | `alg`, `core` | Partir el problema en subproblemas independientes del mismo tipo, resolverlos por separado y combinar; el teorema… |
| `grafos-representacion` | Grafos: representación | intermedio | `alg`, `de` | Lista o matriz de adyacencia cambian el coste de casi todo algoritmo de grafos; elegir mal la estructura arruina un… |
| `heaps-y-prioridad` | Montículos y colas de prioridad | intermedio | `alg` | Un montículo guarda el mínimo o el máximo en la raíz y lo mantiene ahí con dos operaciones de O(log n), sin llegar a… |
| `indices-y-busqueda-en-texto` | Índices y búsqueda en texto | avanzado | `alg`, `de` | Índice invertido, análisis de texto, TF-IDF y BM25: cómo un motor encuentra los documentos relevantes sin leerlos… |
| `map-reduce` | MapReduce y cómputo distribuido | avanzado | `alg`, `de` | El patrón map, shuffle y reduce que sostiene Spark y Hadoop, y la razón de que casi todo el coste esté en el shuffle y… |
| `np-completitud` | NP-completitud | experto | `alg`, `core` | La frontera entre lo que se puede resolver rápido y lo que solo se puede comprobar rápido, y por qué una reducción… |
| `optimizacion-matematica` | Optimización matemática | avanzado | `alg`, `quant` | Programación lineal, entera, descenso de gradiente y metaheurísticas: cómo elegir el método según la forma del… |
| `ordenacion` | Algoritmos de ordenación | intermedio | `alg`, `core` | Ordenar es el paso previo de casi todo; quicksort, mergesort, heapsort y counting sort no son intercambiables y la… |
| `ordenacion-externa` | Ordenación externa | avanzado | `alg`, `de` | Ordenar más datos de los que caben en memoria: trozos que sí quepan, ordenar cada uno y fusionarlos con un montículo… |
| `pilas-y-colas` | Pilas, colas y deques | básico | `alg`, `de` | Dos formas de guardar y sacar: la pila devuelve lo último que entró y la cola lo primero; con ellas se resuelven… |
| `programacion-dinamica` | Programación dinámica | avanzado | `alg`, `core` | Cuando la recursión repite los mismos subproblemas, guardar sus resultados convierte un coste exponencial en uno… |
| `recursion-y-backtracking` | Recursión y backtracking | intermedio | `alg`, `core` | Una función que se llama a sí misma con un problema más pequeño, y la técnica de deshacer pasos para explorar todas… |
| `tablas-hash` | Tablas hash | intermedio | `alg`, `de` | Convierten una clave en una posición de un array para responder en O(1) de media, a cambio de aceptar colisiones y… |
| `tries` | Árboles de prefijos (tries) | avanzado | `alg`, `de` | Un árbol con un carácter por arista que permite buscar, insertar y autocompletar por prefijo en tiempo proporcional a… |
| `union-find` | Conjuntos disjuntos (union-find) | avanzado | `alg` | Mantiene una partición en grupos que se van fusionando, con dos optimizaciones que dejan cada operación en un coste… |

## f11 — Ingeniería de software (34 conceptos)

| id | título | nivel | rutas | resumen |
| --- | --- | --- | --- | --- |
| `accesibilidad` | Accesibilidad | intermedio | `alg` | Que la web que haces la pueda usar cualquiera: contraste suficiente, todo con teclado, estructura que entienda un… |
| `apis-rest` | APIs REST | intermedio | `alg`, `de` | Recursos, verbos y códigos de estado bien elegidos: la API que cualquiera puede usar sin leer tu documentación entera. |
| `arquitectura-de-aplicaciones` | Arquitectura de aplicaciones: capas, límites y dependencias | intermedio | `alg` | Qué puede importar a qué: la regla que evita que un cambio en la base de datos obligue a tocar la interfaz, y cómo se… |
| `autenticacion-y-autorizacion` | Autenticación y autorización | avanzado | `alg` | Quien eres y qué puedes hacer: sesiones, tokens, JWT, OAuth y los errores de seguridad que se repiten en cada proyecto. |
| `cache-y-redis` | Caché y Redis | avanzado | `alg`, `de` | Guardar el resultado caro para no repetirlo: qué cachear, cuándo invalidar y por qué el TTL es solo una parte del… |
| `cap-y-consistencia` | CAP y modelos de consistencia | experto | `de`, `alg` | Que significan exactamente C, A y P, qué se puede y qué no cuando la red se parte, y cómo se paga la consistencia en… |
| `ci-cd` | Integración y despliegue continuos | intermedio | `alg`, `de` | Automatizar pruebas, construcción y publicación para que integrar deje de ser un acontecimiento: qué corre en cada… |
| `code-review` | Revisión de código | intermedio | `alg` | Que mirar en una revisión, cómo comentar para que el cambio se haga y qué conviene delegar en la máquina antes de que… |
| `colas-y-mensajeria` | Colas y mensajería | avanzado | `alg`, `de` | Desacoplar productor y consumidor, reintentar sin duplicar y aceptar que ordenar cuesta dinero. |
| `concurrencia-async-hilos-procesos` | Concurrencia, asincronía, hilos y procesos | avanzado | `alg`, `de` | Esperar a la red, repartir CPU y compartir memoria: qué resuelve cada modelo en Python y cuándo el GIL te deja sin nada. |
| `consenso-y-replicacion` | Consenso y replicación | experto | `de`, `alg` | Cómo un clúster se pone de acuerdo en un valor y en su orden: mayorías, términos, elección de líder y por qué un… |
| `contenedores` | Contenedores | intermedio | `de`, `alg` | Un contenedor no es una máquina virtual pequeña: es un proceso normal con namespaces, límites de recursos y un sistema… |
| `copias-de-seguridad-y-recuperacion` | Copias de seguridad y recuperación ante desastres | intermedio | `de`, `alg` | Cuánto dato puedes permitirte perder y cuánto tardas en volver: RPO y RTO, la regla 3-2-1, copias inmutables y la… |
| `exactamente-una-vez` | Entrega exactamente una vez | experto | `alg`, `de` | Reintentar da al menos una vez y no reintentar da como mucho una vez; exactamente una vez se consigue deduplicando el… |
| `fastapi` | FastAPI | intermedio | `alg`, `ds` | Rutas, validación con Pydantic, inyección de dependencias y documentación automática: el marco para servir un modelo… |
| `gestion-de-memoria` | Gestión de memoria | avanzado | `alg`, `de` | Como se reserva y se libera la memoria de un proceso, por qué el recolector no lo arregla todo y por qué un trabajo de… |
| `git-avanzado` | Git avanzado | avanzado | `alg` | Rebase, bisect y reflog: reescribir la historia con criterio, encontrar el commit que rompió algo y recuperar trabajo… |
| `graphql-y-grpc` | GraphQL y gRPC | avanzado | `alg`, `de` | Consultar por esquema frente a protocolos binarios: cuándo conviene cada uno y qué precio se paga por elegir mal. |
| `idempotencia-en-apis` | Idempotencia en APIs | avanzado | `alg`, `de` | Repetir una petición no debe repetir el efecto: claves de idempotencia, respuestas guardadas y los detalles que… |
| `incidentes-y-postmortem` | Incidentes y postmortem | avanzado | `alg`, `de` | Qué hacer cuando algo se rompe en producción: severidades, runbook, mitigar antes de diagnosticar y un postmortem sin… |
| `logging-y-trazas` | Registro y trazas | intermedio | `alg`, `de` | Registrar para poder depurar: niveles con contrato, mensajes estructurados, identificadores de correlación y trazas… |
| `metricas-y-alertas` | Métricas, SLO y alertas | avanzado | `alg`, `de` | SLI, SLO y presupuesto de error: alertar por lo que sufre el usuario y no por causas, con etiquetas de cardinalidad… |
| `patrones-de-diseno` | Patrones de diseño | avanzado | `alg` | Estrategia, fábrica, observador y repositorio: nombres cortos para problemas de diseño que ya se han resuelto mil… |
| `principios-solid` | Principios SOLID | intermedio | `alg` | Cinco reglas sobre dónde poner las fronteras del código para que añadir algo nuevo no obligue a repasar todo lo que ya… |
| `privacidad-y-gdpr` | Privacidad y RGPD | avanzado | `alg`, `de` | Base legal, minimización, derechos del interesado y retención: cómo se recogen datos personales en una analítica sin… |
| `refactorizacion` | Refactorización | intermedio | `alg` | Cambiar la forma del código sin cambiar lo que hace: pasos pequeños, olores que dicen dónde mirar y una red de pruebas… |
| `rendimiento-y-perfilado` | Rendimiento y perfilado | avanzado | `alg`, `de` | Medir antes de optimizar: dónde se va el tiempo, cuánta memoria ocupa cada objeto y qué cuello de botella atacar… |
| `resiliencia-de-servicios` | Resiliencia de servicios: cortacircuitos y degradación | avanzado | `alg`, `de` | Qué hacer cuando una dependencia se pone lenta: timeouts medidos, reintentos con espera creciente y azar,… |
| `secretos-y-configuracion` | Secretos y configuración | avanzado | `alg`, `de` | Que es un secreto, dónde se guarda, cómo se rota y por qué borrarlo en un commit posterior no lo borra de ninguna parte. |
| `seguridad-owasp` | Seguridad de aplicaciones | avanzado | `alg`, `de` | Las diez trampas que se repiten en cada aplicación: inyección, XSS, CSRF, control de acceso roto y dependencias… |
| `sesgo-y-etica-en-datos` | Sesgo y ética en datos | avanzado | `alg`, `ds` | Un modelo aprende lo que hay en los datos, incluidas las injusticias que ya existían: como detectar sesgo, que mide… |
| `sistemas-distribuidos-bases` | Sistemas distribuidos: bases | avanzado | `de`, `alg` | Que cambia cuando el sistema vive en varias máquinas: particiones, réplicas, relojes que no coinciden y fallos que… |
| `tdd` | Desarrollo guiado por pruebas | intermedio | `alg` | Rojo, verde, refactor: escribir la prueba antes que el código convierte el diseño en una decisión consciente y el… |
| `testing-piramide` | La pirámide de pruebas | intermedio | `alg` | Muchas pruebas unitarias rápidas, algunas de integración y muy pocas de extremo a extremo: la proporción que mantiene… |

## f12 — Comunicación y carrera (15 conceptos)

| id | título | nivel | rutas | resumen |
| --- | --- | --- | --- | --- |
| `certificaciones-de-datos` | Certificaciones de datos | básico | `core`, `de` | Qué certifica cada examen de datos, en qué orden sacarlas según el mercado y cómo se prepara una sin estudiar el doble… |
| `dashboards` | Cuadros de mando | intermedio | `core` | Un cuadro de mando no es una pared de gráficos, sino un puñado de métricas accionables con dueño, frecuencia de… |
| `documentacion-tecnica` | Documentación técnica | intermedio | `core` | Documentación que no miente: un README que arranca el proyecto en un comando, decisiones registradas con su contexto y… |
| `entrevistas-de-datos` | Entrevistas técnicas de datos | intermedio | `core`, `ds`, `de` | Qué se mide de verdad en una entrevista de datos: acotar un problema ambiguo, escribir SQL sin duplicar filas y… |
| `escribir-un-informe` | Escribir un informe técnico | intermedio | `core` | Un informe técnico se lee en cinco minutos y de arriba abajo: conclusión primero, método reproducible, resultados con… |
| `especializacion-y-carrera` | Especialización y carrera | básico | `core` | Analista, analytics engineer, ingeniero de datos, científico, MLE y quant: qué produce cada rol, cómo se define por su… |
| `etica-profesional` | Ética profesional | intermedio | `core` | Decir «no» con argumentos, reportar el resultado incómodo y no vender humo: tres decisiones que se toman en la… |
| `freelance-y-consultoria` | Freelance y consultoría | intermedio | `core` | Presupuestar y cobrar por entregables: días facturables reales, colchón de horas, cláusula de cambios y criterios de… |
| `metricas-de-producto` | Métricas de producto | intermedio | `core`, `ds` | Qué medir para saber si el producto mejora de verdad: métrica norte, guardarraíles, retención por cohortes y estado… |
| `open-source` | Contribuir a código abierto | intermedio | `core`, `alg` | Encontrar un fallo reproducible, arreglarlo en un parche pequeño que otro pueda revisar y responder a la revisión: así… |
| `portfolio-y-proyectos` | Portfolio y proyectos | básico | `core` | Dos o tres proyectos reproducibles donde se ve el problema, las decisiones y el resultado valen más que veinte… |
| `presentaciones` | Presentar a audiencias distintas | intermedio | `core` | La misma conclusión contada a negocio y a técnicos: qué se enseña, qué se guarda para el anexo y cuánto material cabe… |
| `priorizar-y-planificar` | Priorizar: qué se hace, qué se aplaza y qué se descarta | intermedio | `core`, `alg` | Cómo decidir en qué se trabaja cuando todo parece urgente: coste del retraso entre tamaño, capacidad real, trabajo en… |
| `storytelling-con-datos` | Contar historias con datos | intermedio | `core`, `ds` | Un análisis no convence por tener mas gráficos, sino por decir el mensaje en la primera línea, dar contexto para… |
| `visualizacion-honesta` | Visualización honesta | intermedio | `core`, `ds` | Un gráfico puede decir la verdad y mentir a la vez: ejes truncados, escalas mal elegidas, agregaciones que invierten… |

