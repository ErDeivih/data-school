---
id: datos-geoespaciales
titulo: Datos geoespaciales
fase: 6
nivel: intermedio
rutas: [ds, de]
prerequisitos: [norma-y-distancias, pandas-agrupaciones-y-joins, sql-joins]
tags: [geoespacial, distancias, indices, uniones]
resumen: Coordenadas, proyecciones y unir por cercanía en vez de por igualdad: por qué un grado de longitud no mide lo mismo en Oslo que en Dakar.
fuentes: ["Snyder (1987), 'Map Projections: A Working Manual', USGS Professional Paper 1395", "Obe y Hsu (2020), 'PostGIS in Action', 3ª edición", "Uber Engineering (2018), 'H3: A Hexagonal Hierarchical Spatial Index'"]
---

## En una frase

Una latitud y una longitud no son dos números cualesquiera: son ángulos, así que hay que proyectarlos
o medir sobre la esfera, y unir tablas por cercanía exige un índice espacial en vez de una igualdad.

## La idea

`lat = 40.4168` no identifica un lugar, identifica un ángulo. Esa frase explica casi todos los fallos
que se cometen con datos de mapa, y son fallos silenciosos: no dan error, dan resultados plausibles y
equivocados.

Piensa en cómo unir dos tablas de direcciones postales. Nadie une por la cadena completa del
domicilio, porque «Calle Mayor 3, 2ºB» y «CL MAYOR 3 2-B» son la misma casa y nunca coincidirían.
Con las coordenadas pasa lo mismo: dos representaciones del mismo punto se diferencian en el sexto
decimal, y una unión por igualdad devuelve cero filas sin protestar. Y «cerca» tampoco es una
igualdad: es una condición de distancia, y para medirla hay que decidir en qué unidades.

Tres decisiones, en este orden:

1. **En qué sistema están las coordenadas.** El estándar del GPS es `EPSG:4326`, con latitud y
   longitud en grados. Casi todos los mapas web usan `EPSG:3857` (Web Mercator), con metros. Y para
   medir distancias en una ciudad se usa una proyección local (`UTM`), también en metros. Guardar en
   4326 y calcular en una proyección es la práctica habitual; lo que no vale es mezclar.
2. **Cómo se mide la distancia.** En grados planos, no. Un grado de latitud son 111,32 km en
   cualquier parte, pero un grado de longitud son 111,32 km en el ecuador y 55,7 km a 60° de latitud,
   porque los meridianos se juntan hacia los polos. La fórmula de la esfera (haversine) lo tiene en
   cuenta con un coseno y cuesta seis líneas.
3. **Cómo se busca rápido.** Comparar cada punto con todos los demás es `N · M` distancias: 200.000
   locales contra 50.000 colegios son 10.000 millones de operaciones. Un **índice espacial** (R-tree
   en PostGIS, geohash en texto, H3 en hexágonos) hace lo mismo en dos fases: primero descarta con
   rectángulos, que solo necesitan comparaciones de coordenadas, y solo con los supervivientes
   calcula la distancia de verdad. Es el mismo truco que un índice de base de datos, pero en dos
   dimensiones ([[sql-indices-y-planes]]).

Ese filtro en dos fases es la razón de que existan funciones como `ST_DWithin` en PostGIS o
`sjoin_nearest` en GeoPandas: la lógica de la consulta es «a menos de 500 metros», pero por debajo se
ejecuta «caja primero, distancia después». En pandas puro no hay índice espacial, así que la misma
consulta de cercanía recorre todos los pares; con dos tablas grandes eso no termina.

Y una distinción que se confunde mucho: unir por **cercanía** no es lo mismo que unir por
**contención**. Lo primero asigna a cada punto su vecino más próximo o todo lo que esté a menos de
un radio; lo segundo comprueba si un punto cae dentro de un polígono (barrio, provincia, área de
servicio). Son operaciones distintas y se equivocan de formas distintas.

## Definición formal

La distancia sobre la esfera entre dos puntos, con sus coordenadas en radianes:

:::formula
a = sin²(Δφ/2) + cos φ₁ · cos φ₂ · sin²(Δλ/2)        d = 2 · R · arcsin(√a)
:::

- `R` — radio de la Tierra. Se usa el radio medio, 6.371,0088 km. Con el elipsoide WGS84 el error de
  tratar la Tierra como una esfera llega a un 0,5 %, suficiente para casi todo.
- `φ₁`, `φ₂` — latitudes de los dos puntos, en radianes (en los datos vienen en grados).
- `Δφ` — diferencia de latitud, `φ₂ − φ₁`.
- `Δλ` — diferencia de longitud, `λ₂ − λ₁`.
- `a` — término intermedio, entre 0 y 1: el cuadrado del seno de la mitad del ángulo central que
  separa los dos puntos.
- `d` — distancia sobre la esfera, en las unidades de `R`: kilómetros.

La versión tramposa, que es la que aparece en la mitad de los notebooks, sustituye `cos φ` por 1:

:::formula
d_plano = √( (Δφ · 111,32)² + (Δλ · 111,32)² )     ← solo vale cerca del ecuador
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `R` | Radio terrestre medio | km | Escala la distancia entera de forma lineal |
| `φ₁`, `φ₂` | Latitudes de los dos puntos | radianes (grados en el fichero) | Cuanto mayor la latitud, menos separa un mismo `Δλ`: la distancia este-oeste se encoge |
| `Δφ` | Diferencia de latitud | radianes | Aporta la separación norte-sur, que no depende de dónde estés |
| `Δλ` | Diferencia de longitud | radianes | Su efecto viene multiplicado por `cos φ`: vale 1 en el ecuador y 0 en el polo |
| `a` | Término intermedio de la fórmula | adimensional, de 0 a 1 | Con `a` cerca de 1 los puntos están casi en las antípodas |
| `d` | Distancia sobre la esfera | km | Es lo que filtras: `d <= r` decide quién entra |
| `r` | Radio del vecindario que buscas | km | Más candidatos: la caja crece y el ahorro del índice baja |
| celda | Lado de la rejilla espacial (geohash, H3) | km o nivel | Celdas grandes: menos claves y más candidatos cada una; pequeñas: al contrario |
:::

:::figura
fichero: datos-geoespaciales-grados-y-caja
pie: A la izquierda, cuántos kilómetros hay de verdad en un grado de longitud según la latitud. La línea roja discontinua es lo que asume quien multiplica por 111,32 sin mirar dónde está: en el ecuador acierta y a 60° duplica la distancia. A la derecha, por qué un índice espacial sirve: la cruz roja es el punto consultado, el círculo naranja el radio de búsqueda de 8 km y el cuadrado azul la caja que un índice usaría como primer filtro. De los 400 puntos de la región, solo 6 caen en la caja: el 98 % se descarta con dos comparaciones de coordenadas por punto, sin calcular ni una raíz cuadrada.
fuente: figuras/datos-geoespaciales-1.py
:::

## Ejemplo

Dos pares de ciudades europeas, con las dos fórmulas:

| Par | Haversine | Plano (111,32 fijo) | Error |
| --- | --- | --- | --- |
| Madrid (40,4168 · −3,7038) y Barcelona (41,3874 · 2,1686) | 505,1 km | 662,6 km | 31,2 % |
| Helsinki (60,1699 · 24,9384) y Oslo (59,9139 · 10,7522) | 786,7 km | 1.579,5 km | 100,8 % |

Las dos parejas se llevan 5,9° y 14,2° de longitud respectivamente, y en Madrid el error es del 31 %
mientras en Helsinki es del 101 %. La diferencia no está en la fórmula plana: está en la latitud. El
factor que falta es `1 / cos φ − 1`, que vale 0,32 a 40,9° y exactamente 1,00 a 60°. Con eso, la
distancia este-oeste se multiplica por dos en Helsinki, y la norte-sur (28 km en ese par) se queda
igual: por eso el error total sale del 100,8 % y no del 100 % clavado.

La lección práctica es que el error no es un detalle de precisión: en Madrid el método plano pone
Barcelona un 31 % más lejos de lo que está, y en Helsinki duplica la distancia. Cualquier umbral del
tipo «a menos de 600 km» cambia de significado según dónde mires el mapa.

## Código

```python verificable
import numpy as np

R = 6371.0088   # radio medio de la Tierra en kilometros


def haversine(lat1, lon1, lat2, lon2):
    """Distancia en km sobre la esfera; latitudes y longitudes en grados."""
    f1, f2 = np.radians(lat1), np.radians(lat2)
    df, dl = f2 - f1, np.radians(lon2 - lon1)
    a = np.sin(df / 2) ** 2 + np.cos(f1) * np.cos(f2) * np.sin(dl / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


def plano(lat1, lon1, lat2, lon2):
    """Version tramposa: trata los grados como kilometros fijos."""
    dy, dx = (lat2 - lat1) * 111.32, (lon2 - lon1) * 111.32
    return float(np.hypot(dx, dy))


for nombre, p1, p2 in (("Madrid-Barcelona", (40.4168, -3.7038), (41.3874, 2.1686)),
                       ("Helsinki-Oslo", (60.1699, 24.9384), (59.9139, 10.7522))):
    real = float(haversine(*p1, *p2))
    mal = plano(*p1, *p2)
    print(f"{nombre:>16}  real {real:7.1f} km  plano {mal:7.1f} km"
          f"  error {100 * (mal / real - 1):5.1f} %")
# -> Madrid-Barcelona  real   505.1 km  plano   662.6 km  error  31.2 %
# ->    Helsinki-Oslo  real   786.7 km  plano  1579.5 km  error 100.8 %
```

:::claves
- `np.radians` convierte grados a radianes **elemento a elemento** y devuelve un array nuevo. Las funciones trigonométricas de NumPy trabajan siempre en radianes: si le pasas grados, `np.cos(60)` da −0,952 en vez de 0,5 y el error no avisa.
- `*p1, *p2` desempaqueta las dos tuplas de coordenadas en los cuatro argumentos. El orden es el de la firma, `(lat1, lon1, lat2, lon2)`: cambiar latitud y longitud aquí no da error, da una distancia creíble de un sitio equivocado.
- `np.arcsin(np.sqrt(a))` con `a` ligeramente mayor que 1 por error de redondeo devuelve `nan` con un aviso. En la práctica ocurre con puntos casi antípodas; se blinda con `np.clip(a, 0.0, 1.0)`.
- `float(...)` convierte el array de un elemento (o el escalar de NumPy) en un `float` de Python. Sin esa conversión, el `f"{real:7.1f}"` funciona igual, pero comparar con `==` o guardarlo en JSON se comporta de otra manera.
- `np.hypot(dx, dy)` calcula `√(dx² + dy²)` sin desbordar con valores enormes, y aquí es la parte tramposa: usa 111,32 para las dos componentes, cuando la componente horizontal debería llevar `· cos φ`.
:::

```python verificable
import numpy as np
import pandas as pd

# 4.000 locales en una region de 100 x 100 km. Buscamos parejas a menos de 1 km.
rng = np.random.default_rng(0)
df = pd.DataFrame(rng.uniform(0.0, 100.0, (4000, 2)), columns=["x", "y"])
df["i"] = np.arange(len(df))
df["cx"] = (df.x // 5).astype(int)      # rejilla de 5 km: la clave de un geohash
df["cy"] = (df.y // 5).astype(int)

calculadas, pares = 0, 0
izq = df.rename(columns={"cx": "kx", "cy": "ky"})
for dx in (-1, 0, 1):                    # la celda y sus ocho vecinas
    for dy in (-1, 0, 1):
        der = df.assign(kx=df.cx + dx, ky=df.cy + dy)[["kx", "ky", "x", "y", "i"]]
        m = izq.merge(der, on=["kx", "ky"], suffixes=("_a", "_b"))
        calculadas += len(m)             # solo estos pares llegan a medir una distancia
        d = np.hypot(m.x_a - m.x_b, m.y_a - m.y_b)
        pares += int(((d <= 1.0) & (m.i_a != m.i_b)).sum())

print(f"pares posibles         {df.shape[0] ** 2}")     # -> 16000000
print(f"distancias calculadas  {calculadas}")           # -> 342032
print(f"parejas a menos de 1 km {pares // 2}")          # -> 2507
```

## Errores típicos

- **Unir dos tablas por igualdad de coordenadas.** Es un fallo silencioso: la consulta se ejecuta y
  devuelve pocas filas o ninguna. Une por identificador de zona o por una celda redondeada, y cuenta
  cuántas filas quedan sin unir antes de dar el resultado por bueno ([[sql-joins]]).
- **Restar grados y llamarlo distancia.** `(lat2 − lat1)² + (lon2 − lon1)²` mezcla dos escalas: un
  grado de longitud vale entre 0 y 111 km según la latitud. Si el resultado se usa para ordenar
  distancias en España, casi siempre acierta; si se usa como umbral en kilómetros, miente.
- **Medir en EPSG:3857 porque es el sistema del mapa.** Web Mercator está hecho para pintar: a 60° de
  latitud infla todas las distancias por dos. Para medir, una proyección local en metros (UTM) o
  haversine.
- **Confundir el orden de los argumentos.** Casi todo el mundo escribe `(lat, lon)`; GeoJSON, PostGIS
  y la mayoría de las librerías de mapas usan `(x, y)`, es decir `(lon, lat)`. Un cruce te manda el
  punto al otro lado del planeta sin lanzar un solo error.
- **Hacer la unión por cercanía sin índice espacial.** Es la operación que convierte una consulta de
  dos segundos en una de dos horas. Si el motor no tiene índice espacial, reduce primero por caja con
  una rejilla, como en el bloque de código.
- **Olvidar los casos límite.** El antimeridiano (longitudes que saltan de +179,9 a −179,9), los
  polos, los puntos exactamente en el borde de un polígono y las geometrías inválidas
  (autointersectadas) que el motor rechaza al indexar.
- **Confundir «el más cercano» con «a menos de X».** El vecino más próximo siempre existe, aunque
  esté a 300 km; un radio puede devolver cero filas. Y con empates a la misma distancia, el resultado
  depende del orden de las filas: fija un desempate.

:::practica
enunciado: Dos ciudades están en la misma latitud, 45° N, y sus longitudes se diferencian en 2°. Calcula la distancia entre ellas con la aproximación plana corregida por la latitud y di cuánto se equivoca quien multiplica por 111,32 sin corregir.
pista: A una latitud φ, un grado de longitud mide 111,32 · cos φ kilómetros.
solucion: cos 45° = 0,7071, así que un grado de longitud mide 111,32 · 0,7071 = 78,72 km, y dos grados son 157,4 km. Sin la corrección saldrían 222,6 km: un 41,4 % de más, que es justo 1/cos 45° − 1 = 0,414. Haversine da 157,2 km, prácticamente lo mismo: a distancias cortas la esfera y el plano local coinciden, y la curvatura solo se nota en miles de kilómetros.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué un grado de longitud no vale lo mismo en Oslo que en Dakar?
o: Porque los meridianos convergen hacia los polos y la separación se multiplica por el coseno de la latitud
o: Porque la Tierra es un elipsoide y su radio cambia con la latitud
o: Porque las longitudes se cuentan en sentido contrario en cada hemisferio
a: 1
e: Los meridianos se juntan en los polos: un grado de longitud abarca 111,32 km en el ecuador y la mitad a 60° de latitud. El achatamiento del elipsoide también existe, pero su efecto es de menos del 0,5 %, no del 100 %. Y las longitudes se miden igual en los dos hemisferios, con signo negativo al oeste de Greenwich.
:::

:::quiz
p: ¿Para qué sirve la caja envolvente antes de calcular distancias?
o: Para redondear las coordenadas y que la distancia salga más exacta
o: Para descartar candidatos con comparaciones de coordenadas y calcular la distancia solo con los que quedan
o: Para convertir grados en metros
a: 2
e: Es la primera fase de cualquier índice espacial: comparar diferencias por eje es mucho más barato que calcular una distancia, y descarta la mayor parte de los pares. Después se mide de verdad y se filtra por el radio. La caja no convierte unidades ni mejora la precisión: solo evita cuentas.
:::

:::quiz
p: Tienes dos tablas con columnas de latitud y longitud y las unes con un merge por esas dos columnas. ¿Qué pasa?
o: Funciona, siempre que las dos tablas usen el mismo sistema de coordenadas
o: Casi no une nada: dos representaciones del mismo punto rara vez coinciden decimal a decimal
o: Da error, porque no se puede unir por columnas de tipo float
a: 2
e: La unión se ejecuta sin protestar y devuelve muy pocas filas o ninguna: es un fallo silencioso. Se arregla uniendo por un identificador de zona o por una celda redondeada, y comprobando cuántas filas quedan sin unir.
:::

:::aviso
Antes de calcular nada, mira el orden de las columnas y el sistema de referencia. Un `(lon, lat)`
metido en una función que espera `(lat, lon)` devuelve una distancia perfectamente plausible entre
dos puntos que no son los tuyos, y ningún test lo detecta si solo compruebas que el número es
positivo. Guarda el sistema de coordenadas junto a los datos y compruébalo al leerlos.
:::
