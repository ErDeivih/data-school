---
id: vistas-y-copias
titulo: Vistas, copias y aliasing
fase: 3
nivel: intermedio
rutas: [core, ds, de]
prerequisitos: [numpy-fundamentos, tipos-y-estructuras-python]
tags: [numpy, pandas, memoria, bugs]
resumen: Una rebanada no copia nada: comparte memoria con el original. Distinguir vista de copia evita el bug más silencioso y más caro de los datos.
fuentes: ["Harris et al. (2020), 'Array programming with NumPy', Nature", "McKinney (2017), 'Python for Data Analysis'"]
---

## En una frase

Una **vista** es una segunda ventana sobre los mismos bytes y una **copia** es memoria nueva;
saber cuál te ha devuelto cada operación decide si modificar el resultado cambia o no los datos
de partida.

## La idea

En Python normal, la regla es sencilla: `b = a` para una lista son dos nombres para el mismo
objeto (aliasing), y `b = a[:]` es una copia. La gente memoriza «la rebanada copia» y sigue
programando con esa idea en NumPy, donde es **exactamente al revés**: `a[:]` y `a[1:4]` son
vistas, comparten el bloque de memoria y no cuestan nada; lo que copia es el indexado con una
lista de posiciones, `a[[1, 2, 3]]`.

Esto no es un detalle de rendimiento, es una fuente de bugs. Imagina un DataFrame con las
facturas del año y una función que «limpia» los importes negativos. Si la función recibe una
rebanada y escribe en ella, está modificando el DataFrame original. Y como el cambio es
correcto en apariencia (los negativos desaparecen, el informe sale bien), nadie lo nota hasta
que otro informe, tres pasos más tarde, da cifras que no cuadran.

Hay dos motivos por los que las vistas existen:

- **Rendimiento.** `matriz[0]` sobre una matriz de 10 GB no puede copiar 400 MB cada vez. Una
  vista son tres números (puntero, forma, strides).
- **Memoria.** Con vistas puedes tener mil rebanadas solapadas de un mismo array sin duplicar un
  solo byte.

Y hay un motivo por el que son peligrosas: **compartir memoria es invisible**. `type(vista)` es
`numpy.ndarray`, `vista.shape` y `vista.dtype` se leen igual que en una copia, y el código que
la recibe no tiene forma de saberlo sin preguntarlo explícitamente.

Las reglas, en corto:

- Rebanada básica y `reshape` cuando puede evitar copia → **vista**.
- Indexado avanzado (lista o array de posiciones), máscaras booleanas y **cualquier operación
  aritmética** (`a + 1`, `a * 2`, `np.concatenate`, `np.append`) → **array nuevo**.
- `np.asarray(x)` no copia si `x` ya es un array del dtype pedido; `np.array(x)` copia por
  defecto.

En Pandas, desde las versiones recientes, el modelo es **copia al escribir** (*copy-on-write*):
seleccionar un subconjunto crea un objeto nuevo que comparte memoria con el padre **hasta que
escribes**; en ese momento se copia y el padre no cambia nunca. Es más seguro que el
comportamiento antiguo, pero no te libra de pensar: sigues teniendo que saber si estás
escribiendo en la tabla que crees.

## Definición formal

Dos arrays `a` y `b` **comparten memoria** si alguna región del búfer de `b` pertenece también
al búfer de `a`. Las dos herramientas para comprobarlo:

- `b.base` — devuelve el objeto del que `b` toma prestada la memoria, o `None` si `b` es dueño
  de su propio búfer. Si `b.base is a`, `b` es una vista de `a`.
- `np.shares_memory(a, b)` — `True` si los dos arrays se solapan en memoria, aunque la
  relación no sea directa de padre a hijo (por ejemplo, nietos de un mismo array).

Una vista se describe con la misma terna que cualquier array, solo que el puntero de inicio
apunta dentro del búfer de otro:

:::formula
vista = (puntero_a_un_byte_del_búfer, forma, strides)      copia = (búfer_nuevo, forma, strides)
:::

Definiciones que conviene fijar:

- **Aliasing** — dos nombres distintos que se refieren a los mismos datos. En Python es
  automático con `b = a`; en NumPy aparece además con las vistas.
- **Copia superficial** (`copy.copy`) — un objeto nuevo que sigue apuntando a los mismos
  objetos internos. En Pandas, `df.copy(deep=False)` comparte los mismos bloques.
- **Copia profunda** (`copy.deepcopy`, `np.ndarray.copy`, `df.copy()`) — memoria nueva para los
  datos. Ojo: en un DataFrame con columnas de tipo `object`, `df.copy()` copia los punteros,
  no los objetos de dentro; si una celda contiene una lista, la lista sigue compartida.
- **Coste de una vista**: O(1) en tiempo y memoria. **Coste de una copia**: O(n) en ambos.

## Ejemplo

Con `a = np.arange(10)`, es decir `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`:

```
vista = a[3:6]        # [3, 4, 5]  -> vista: b.base is a
copia = a[[3, 4, 5]]  # [3, 4, 5]  -> copia: b.base is None
```

Los dos imprimen lo mismo y los dos tienen forma `(3,)`. Ahora escribe una vez en cada uno:

```
vista[0] = 99   ->  a pasa a ser [0, 1, 2, 99, 4, 5, 6, 7, 8, 9]
copia[0] = 99   ->  a sigue siendo [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

Dos escrituras idénticas, dos resultados distintos, ningún aviso. Ese es el problema entero.

El caso que de verdad rompe cosas es el de una función que modifica en el sitio:

```
datos = [1.0, 2.0, 3.0, 4.0]

def normaliza(x):
    x -= x.mean()      # -= escribe en el array que le han pasado
    return x / x.std()

salida = normaliza(datos)
```

Después de la llamada, `datos` vale `[-1.5, -0.5, 0.5, 1.5]`: la función se ha llevado por
delante la escala original. Si más adelante alguien suma esos «datos» con otra columna, estará
sumando z-scores con euros. La versión segura es `x = x - x.mean()` (crea un array nuevo) o
`normaliza(datos.copy())` si de verdad quieres trabajar en el sitio.

## Código

```python verificable
import numpy as np

a = np.arange(10)
vista = a[3:6]          # rebanada basica: comparte el buffer de a
copia = a[[3, 4, 5]]    # indexado avanzado: memoria nueva

vista[0] = 99           # escribe dentro del buffer de a
copia[1] = -1           # escribe en memoria propia, a no se entera

print(a.tolist())                    # -> [0, 1, 2, 99, 4, 5, 6, 7, 8, 9]
print(vista.tolist())                # -> [99, 4, 5]
print(copia.tolist())                # -> [3, -1, 5]
print(vista.base is a, copia.base is None)        # -> True True
print(np.shares_memory(a, vista), np.shares_memory(a, copia))   # -> True False
```

```python verificable
import numpy as np

def normaliza(x):
    x -= x.mean()        # -= modifica el array del que llama, no una copia
    return x / x.std()

datos = np.array([1.0, 2.0, 3.0, 4.0])
salida = normaliza(datos)

print(datos.tolist())              # -> [-1.5, -0.5, 0.5, 1.5]  (el original ya no son los datos)
print(np.round(salida, 3).tolist())   # -> [-1.342, -0.447, 0.447, 1.342]

# La rebanada de un array grande mantiene vivo todo el buffer: 8 bytes utiles, 80 MB retenidos
grande = np.zeros(10_000_000)
trocito = grande[:1]               # vista, no copia
print(trocito.nbytes, grande.nbytes)   # -> 8 80000000
print(np.shares_memory(grande, trocito))   # -> True
```

```python verificable
import pandas as pd

df = pd.DataFrame({"importe": [10.0, 20.0, 30.0]})
sub = df[df["importe"] > 10]     # subconjunto: comparte bloques hasta que se escribe
sub.iloc[0, 0] = 999.0           # copia al escribir: el padre no cambia
print(df["importe"].tolist())    # -> [10.0, 20.0, 30.0]

# La forma segura y explicita de escribir en la tabla original
df.loc[df["importe"] > 10, "importe"] = 99.0
print(df["importe"].tolist())    # -> [10.0, 99.0, 99.0]
```

## Errores típicos

- **Suponer que `b = a[:]` copia.** En una lista de Python sí; en NumPy es una vista. Si
  necesitas independencia, `b = a.copy()` o `b = a[:].copy()`, y si quieres que sea explícito en
  la lectura del código, escribe la copia solo donde haga falta.
- **Modificar el argumento dentro de una función.** Cualquier `x -= …`, `x[0] = …`, `x.sort()`,
  `x.fill(0)` o `np.clip(x, …, out=x)` cambia el array de quien llama. Decide y dilo: o
  devuelves un array nuevo (`x = x - …`) o documentas que la función trabaja en el sitio.
- **Escribir con indexado encadenado en Pandas.** `df[df["a"] > 0]["b"] = 0` no escribe en
  `df`: el primer corchete devuelve un objeto intermedio y el segundo escribe en ese intermedio.
  La forma correcta es una sola operación con `.loc`: `df.loc[df["a"] > 0, "b"] = 0`.
- **Creer que `df.copy()` te aísla de todo.** Copia los bloques de datos, pero si una columna es
  de tipo `object` y contiene listas o diccionarios, esos objetos siguen siendo los mismos:
  `df2.loc[0, "lista"].append(1)` también cambia `df`. Para eso hace falta `copy.deepcopy`.
- **Retener un trozo diminuto de un array enorme.** `resumen = datos[:10]` guarda 80 bytes
  útiles y mantiene vivo el búfer completo, porque `base` sigue apuntando a él. Si el trozo va a
  vivir mucho, haz `.copy()`.
- **Dar por hecho que `to_numpy()` copia.** Con un DataFrame de un solo dtype puede devolver una
  vista; escribir ahí modifica el DataFrame. Si vas a modificar, `.to_numpy(copy=True)`.

:::practica
enunciado: Con `datos = np.array([2.0, 4.0, 6.0, 8.0])`, escribe el código de `def ajusta(x): x -= x.mean(); return x`, llama a `ajusta(datos)` e imprime `datos` y el valor devuelto. ¿Qué vale `datos` después y cómo se evita ese efecto?
pista: `-=` no crea un array nuevo: escribe dentro del que le han pasado.
solucion: La media de `[2, 4, 6, 8]` es 5, así que `x -= 5` deja `x` en `[-3, -1, 1, 3]`, que es también lo que devuelve la función. Como `x` es el mismo objeto que `datos`, al volver de la llamada `datos` vale `[-3, -1, 1, 3]`: la escala original se ha perdido y esas cifras ya no son euros. Se evita con `x = x - x.mean()`, que crea un array nuevo, o llamando a `ajusta(datos.copy())`.
:::

## Comprueba que lo sabes

:::quiz
p: Después de `v = a[2:5]` y `v[0] = 0`, ¿qué le ha pasado a `a`?
o: Nada: las rebanadas devuelven copias
o: `a[2]` vale 0, porque `v` es una vista que comparte el búfer
o: Se ha creado un array nuevo y `a` queda intacto
a: 2
e: La rebanada básica es una vista: `v.base is a` y escribir en `v` escribe en la misma memoria. Para que `a` no cambiara habría que haber usado `a[[2, 3, 4]]` o `a[2:5].copy()`.
:::

:::quiz
p: ¿Cuál de estas expresiones devuelve una copia con memoria nueva?
o: `a[10:20]`
o: `a[a > 0]`
o: `a.reshape(2, -1)` cuando los datos ya son contiguos
a: 2
e: La máscara booleana construye un array nuevo con los elementos seleccionados. La rebanada y el `reshape` que no necesita reordenar devuelven vistas: no copian nada.
:::

:::quiz
p: En Pandas escribes `df[df["importe"] > 0]["descuento"] = 0.1` y no ves el cambio. ¿Por qué?
o: Porque hay que usar `inplace=True`
o: Porque el primer corchete devuelve un objeto intermedio y el `= 0.1` escribe en ese intermedio, no en `df`
o: Porque Pandas no permite asignar a columnas con filtros
a: 2
e: El indexado encadenado crea un objeto nuevo en el primer paso y la asignación se aplica a él, que se descarta. La forma correcta es una asignación única con `.loc`: `df.loc[df["importe"] > 0, "descuento"] = 0.1`, que ya no encadena nada.
:::

:::trampa
El bug de aliasing no da error, no da aviso y suele aparecer como «los números del informe no
cuadran» tres pasos más tarde. Cuando un resultado te sorprenda, la primera pregunta no es qué
falla en la fórmula: es quién ha escrito en ese array antes que tú.
:::
