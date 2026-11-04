---
id: bloom-filters
titulo: Filtros de Bloom
fase: 10
nivel: avanzado
rutas: [alg, de]
prerequisitos: [tablas-hash, complejidad-asintotica, probabilidad-axiomas]
tags: [estructuras, hashing, memoria, probabilistico]
resumen: Una estructura de unos pocos bits por elemento que responde «seguro que no está» con certeza y «puede que esté» con una probabilidad que tú eliges.
fuentes: ["Broder y Mitzenmacher (2004), 'Network Applications of Bloom Filters: A Survey'", "Bloom (1970), 'Space/Time Trade-offs in Hash Coding with Allowable Errors'"]
---

## En una frase

Un filtro de Bloom guarda un conjunto usando unos pocos bits por elemento: si dice que un
elemento **no** está, es verdad con total seguridad; si dice que sí está, puede equivocarse,
y esa tasa de error la decides tú antes de construirlo.

## La idea

Tienes que comprobar si 10 millones de URL ya han sido visitadas por tu rastreador. Guardarlas
como texto ocupa del orden de 400 MB. Guardar solo su hash de 64 bits ocupa 80 MB y sigue
teniendo el problema de que un hash de 64 bits puede colisionar, aunque sea raro.

Un filtro de Bloom cambia el trato: en lugar de guardar los elementos, guarda un **tablero de
interruptores**. Al registrar una URL, enciendes `k` interruptores elegidos por `k` funciones
hash. Para preguntar si una URL está, miras esos mismos `k` interruptores:

- Si **alguno está apagado**, esa URL no se registró nunca. Certeza absoluta: si se hubiera
  registrado, habría encendido ese interruptor.
- Si **todos están encendidos**, o se registró ella, o entre todas las demás URL encendieron
  justo esos `k` interruptores por casualidad. Es un **falso positivo**.

Ese es todo el truco, y suena demasiado bueno hasta que ves el precio: no puedes listar los
elementos guardados, no puedes borrar uno sin ensuciar a los demás (apagar un interruptor
compartido crearía un falso negativo) y no puedes saber cuántos hay. A cambio, la consulta es
`O(k)` y la memoria es una fracción de la de guardar los datos.

El caso de uso canónico es **evitar trabajo caro**: antes de ir a disco o a la red a buscar una
clave, pregunta al filtro. Si dice «no está», te has ahorrado la consulta y no has mentido. Si
dice «puede que esté», vas y compruebas de verdad. El filtro nunca sustituye a la fuente de
verdad; la filtra.

## Definición formal

Un filtro de Bloom se define por dos parámetros:

- `m` — número de bits del tablero.
- `k` — número de funciones hash distintas, cada una con salida en `{0, …, m − 1}`.

Con `n` elementos insertados:

- **Insertar `x`:** poner a 1 los bits `h₁(x), h₂(x), …, h_k(x)`.
- **Consultar `x`:** devolver «puede que esté» si los `k` bits valen 1, y «no está» si alguno
  vale 0.

La probabilidad de falso positivo, suponiendo hashes uniformes e independientes, es:

:::formula
p ≈ (1 − e^(−k·n/m))^k
:::

- `e` — la base de los logaritmos naturales, aproximadamente 2,71828.
- `n/m` — elementos por bit; su inverso, `m/n`, es el número de **bits por elemento**.
- `e^(−k·n/m)` — probabilidad de que un bit concreto siga a 0 después de insertar los `n`
  elementos (cada inserción toca `k` de los `m` bits).
- `(1 − …)^k` — probabilidad de que los `k` bits que consulta un elemento ausente estén todos
  a 1.

Esa expresión se minimiza con:

:::formula
k óptimo = (m/n) · ln 2 ≈ 0,693 · (m/n)
:::

donde `ln 2 ≈ 0,693` es el logaritmo natural de 2. En ese óptimo, la tasa de error se reduce a
`p ≈ 0,6185^(m/n)`, una regla muy cómoda: **cada 4,8 bits por elemento divides el error por
10**. De ahí la tabla de uso común: 10 bits por elemento y `k = 7` dan en torno al 1 % de
falsos positivos; 8 bits y `k = 5` dan en torno al 2 %.

Dos propiedades que hay que tener grabadas:

1. **No hay falsos negativos** mientras no se borre nada. Esa asimetría es la que hace útil la
   estructura: el «no» es una prueba, el «sí» es una sospecha.
2. **La tasa real se degrada al llenar.** La fórmula supone `n` elementos y nada más. Si tu
   filtro recibe el doble de elementos de los previstos sin crecer, `m/n` se hala y el error se
   dispara: con `m/n = 4` y `k = 3`, `p ≈ (1 − e^(−0,75))³ ≈ 0,15`, un 15 %.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `m` | Bits del tablero | bits | Con `n` fijo, cada bit de más baja el error: `p ≈ 0,6185^(m/n)`, unos 4,8 bits por elemento para dividir el error por 10 |
| `k` | Funciones hash distintas | funciones | El error baja hasta el óptimo `k = (m/n)·ln 2` y vuelve a subir: con demasiadas, los bits se saturan |
| `n` | Elementos insertados | elementos | Es el parámetro que se escapa: sin crecer `m`, el error sube muy rápido al acercarse a la capacidad prevista |
| `m/n` | Bits por elemento (el cociente que de verdad manda) | bits por elemento | Es lo único que decide la tasa mínima alcanzable; los valores de `m` y `n` por separado no dicen nada |
| `p` | Tasa de falsos positivos | probabilidad | No es una palanca, es el resultado: se fija al dimensionar el filtro y se degrada solo al llenarse |
:::

:::figura
fichero: bloom-filters-k-y-llenado
pie: A la izquierda, la tasa de falsos positivos de un filtro de 1 MB (8 millones de bits) al ir insertando elementos. El punto rojo es el dimensionamiento previsto, 8 bits por elemento y k = 5, que da un 2,2 %; si acabas insertando el doble, el error sube al 18,5 %, nueve veces más, y la curva naranja muestra cuánto mejora la cosa si recalculas k para cada tamaño (poco: el problema es la memoria, no el número de hashes). A la derecha, la curva en U del número de funciones hash con 8 bits por elemento: el mínimo está en k = 6 y la curva es muy plana alrededor, de 5 a 7 apenas cambia. Los puntos rojos son la medición con un filtro de verdad, y siguen a la teoría.
fuente: figuras/bloom-filters-1.py
:::

## Ejemplo

Supón `n = 1.000.000` de elementos y `m = 8.000.000` de bits, es decir 8 bits por elemento, o
1 MB de memoria.

- `k` óptimo: `8 · 0,693 = 5,54`, así que se usan `k = 5` o `k = 6`.
- Con `k = 5`: `p ≈ (1 − e^(−5/8))⁵ = (1 − 0,5353)⁵ ≈ 0,0217`, un **2,2 %**.
- Con `k = 6`: `p ≈ (1 − e^(−6/8))⁶ ≈ 0,0216`, prácticamente igual.
- Comparación de memoria: guardar los 10⁶ elementos como hashes de 64 bits son 8 MB; el filtro
  son 1 MB. Ocho veces menos, a cambio de un 2 % de consultas de más.

El experimento del bloque de código, con 1.000 claves presentes y 1.000 ausentes, `m = 8.000` y
`k = 5`, da **0 falsos negativos** y **23 falsos positivos de 1.000**, es decir un 2,3 % medido
frente al 2,2 % teórico. Que la medición quede a un pelo de la fórmula es la señal de que el
doble hashing está funcionando.

## Código

```python verificable
import hashlib
import numpy as np


class FiltroBloom:
    def __init__(self, m, k):
        self.m, self.k = m, k
        self.bits = np.zeros(m, dtype=bool)

    def _posiciones(self, elemento):
        # Doble hashing: dos mitades de un hash fuerte simulan k funciones independientes.
        d = hashlib.blake2b(elemento.encode(), digest_size=16).digest()
        h1 = int.from_bytes(d[:8], "big")
        h2 = int.from_bytes(d[8:], "big") | 1     # impar: recorre todos los bits
        return [(h1 + i * h2) % self.m for i in range(self.k)]

    def anadir(self, elemento):
        self.bits[self._posiciones(elemento)] = True

    def podria_estar(self, elemento):
        return bool(self.bits[self._posiciones(elemento)].all())


presentes = ["clave-{}".format(i) for i in range(1000)]
ausentes = ["otra-{}".format(i) for i in range(1000)]
m_bits, k_hash = 8000, 5
filtro = FiltroBloom(m_bits, k_hash)
for p in presentes:
    filtro.anadir(p)

falsos_negativos = sum(not filtro.podria_estar(p) for p in presentes)
falsos_positivos = sum(filtro.podria_estar(a) for a in ausentes)
p_teorica = (1 - np.exp(-k_hash * len(presentes) / m_bits)) ** k_hash

print("bits por elemento:", m_bits / len(presentes))                      # -> 8.0
print("falsos negativos:", falsos_negativos)                             # -> 0
print("falsos positivos:", falsos_positivos, "de", len(ausentes))        # -> 23 de 1000
print("tasa teorica: {:.3f}".format(p_teorica))                          # -> 0.022
```

:::claves
- `self.bits` es un `np.array` de `bool`: cada elemento ocupa un **byte**, no un bit (NumPy no tiene un tipo de un bit). El filtro de verdad empaqueta los bits; este de juguete gasta ocho veces más memoria, y por eso el ejemplo usa 8.000 bits y no 8 millones.
- `self.bits[[3, 7, 11]] = True` asigna con una **lista de índices** a la vez, no en un bucle. Y `self.bits[[3, 7, 11]].all()` devuelve un único `bool` (¿están los tres a 1?), que es exactamente la consulta del filtro.
- `h2 = ... | 1` fuerza que `h2` sea **impar**. Si fuera par, el paso `i * h2` sería múltiplo de un divisor de `m` y las `k` posiciones caerían en menos celdas de las debidas; la garantía del doble hashing depende de eso.
- `p_teorica` usa `len(presentes)` como `n`. Si cambiaras la lista de presentes sin tocar `m_bits`, la teoría se recalcula sola, pero los `falsos_positivos` medidos variarían: con 2.000 elementos y los mismos 8.000 bits, `m/n` baja a 4 y la tasa teórica se va por encima del 15 %.
- `falsos_positivos = sum(filtro.podria_estar(a) for a in ausentes)` suma **booleanos**: en Python `True` es 1 y `False` es 0, así que `sum` cuenta directamente. No hace falta `if`.
- `hashlib.blake2b(...).digest()` devuelve `bytes`, no un número: hay que pasarlo por `int.from_bytes(..., "big")` para poder hacer aritmética modular. Y el `elemento.encode()` es obligatorio, porque `blake2b` no acepta `str`.
:::

```bash ilustrativo
# Un filtro de Bloom real, el de Redis, se maneja con dos ordenes.
# Aqui el filtro se crea con una tasa de error del 1 % para 100.000 elementos.
redis-cli BF.RESERVE visitadas 0.01 100000
redis-cli BF.ADD visitadas https://ejemplo.test/a
redis-cli BF.EXISTS visitadas https://ejemplo.test/a   # responde 1: puede estar
redis-cli BF.EXISTS visitadas https://ejemplo.test/zzz # responde 0 (certeza) o 1 (falso positivo)
redis-cli BF.INFO visitadas                            # tamano, numero de hashes, etc.
```

## Errores típicos

- **Creer que hay falsos negativos.** En un filtro clásico no los hay: si un elemento insertado
  no se encuentra, tienes un fallo de implementación, no de probabilidad. Casi siempre es que
  estás consultando con otro tipo de dato (bytes frente a `str`) o que has borrado bits.
- **Borrar elementos apagando bits.** Apagar los `k` bits de un elemento apaga también los que
  comparte con otros, y ahí aparecen los falsos negativos que creías imposibles. Si necesitas
  borrar, usa un **counting Bloom filter**, que guarda contadores en lugar de bits, o un
  **cuckoo filter**, que sí soporta borrado.
- **Elegir el tamaño a ojo.** «Le pongo un millón de bits» sin calcular `m/n` ni `k` es dejar la
  tasa de error al azar. Fija primero la `p` que toleras, de ahí `m/n ≈ 1,4427 · log₂(1/p)`, y
  después `k = 0,693 · (m/n)`.
- **Usar `hash()` de Python o cualquier hash aleatorizado.** Cambia entre ejecuciones (salvo que
  fijes `PYTHONHASHSEED`) y, peor, no está diseñado para repartir bien. Usa `hashlib`, MurmurHash
  o xxHash, y comprueba el reparto.
- **Tomar decisiones irreversibles con el «puede que esté».** Si el filtro decide si un usuario
  ha pagado, si una contraseña está en una lista negra o si un paquete se descarta, el 2 % de
  falsos positivos son usuarios o paquetes legítimos tratados como culpables. El filtro solo vale
  para descartar trabajo cuyo coste sea comprobar de verdad.
- **Consultar el tamaño o la intersección.** `¿cuántos elementos hay?` no tiene respuesta: los
  bits compartidos hacen que el recuento se infle. Se estima, con mucha menos precisión, con
  `n ≈ −(m/k) · ln(1 − X/m)`, donde `X` es el número de bits a 1.

:::practica
enunciado: Necesitas un filtro de Bloom para 2.000.000 de elementos con una tasa de falsos positivos del 1 %. Calcula los bits por elemento, el tamaño total en megabytes y cuántas funciones hash usar. Compara con guardar hashes de 64 bits.
pista: m/n ≈ 1,4427 · log₂(1/p), y después k = 0,693 · (m/n).
solucion: log₂(100) = 6,644, así que m/n = 1,4427 · 6,644 = 9,59 bits por elemento y k = 0,693 · 9,59 = 6,64, es decir 7 funciones. Total: 2·10⁶ · 9,59 = 19,18 millones de bits = 2,4 MB. Los 2 millones de hashes de 64 bits ocuparían 16 MB, casi siete veces más, a cambio de verificar de verdad el 1 % de consultas que dan positivo sin estarlo.
:::

## Comprueba que lo sabes

:::quiz
p: Un filtro de Bloom dice que la clave que buscas puede estar, pero al ir a la base de datos no aparece. ¿Qué ha pasado?
o: El filtro tiene un falso negativo y hay que reconstruirlo
o: Es un falso positivo: todos los bits de esa clave estaban encendidos por otras claves
o: La base de datos y el filtro se han desincronizado necesariamente
a: 2
e: El «sí» del filtro nunca es una prueba, solo una probabilidad. Cuando otras claves han encendido por casualidad los mismos k bits, la consulta da positivo sin que el elemento esté. El «no» sí es concluyente, y un falso negativo solo aparece si se borran bits o se consulta con un dato de otro tipo.
:::

:::quiz
p: Con 1.000.000 de elementos y 8 bits por elemento, ¿cuántas funciones hash conviene usar y por qué?
o: 1, porque cada función adicional aumenta el error
o: Unas 6, porque el óptimo es (m/n) · ln 2 = 8 · 0,693
o: 64, una por bit disponible
a: 2
e: Añadir funciones baja la probabilidad de que todos los bits consultados estén a 1 por azar, pero también llena el filtro más deprisa. El equilibrio está en k = (m/n)·ln2. Con 8 bits por elemento sale 5,5, y en la práctica se usan 5 o 6 indistintamente.
:::

:::aviso
Un filtro de Bloom dimensionado para `n` elementos y usado con `4n` no falla de forma elegante:
si estaba a 8 bits por elemento, ahora está a 2, y con `k = 5` la tasa de error pasa del 2 % al
65 % sin ningún aviso. Si el conjunto puede crecer, dimensiona para el crecimiento previsto o
usa una variante escalable (por ejemplo, una cadena de filtros de tamaño creciente), y
monitoriza el porcentaje de bits a 1.
:::
