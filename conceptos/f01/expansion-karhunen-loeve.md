---
id: expansion-karhunen-loeve
titulo: Expansión de Karhunen-Loève
fase: 1
nivel: experto
rutas: [quant, ds]
prerequisitos: [autovalores-y-autovectores, covarianza-y-correlacion]
tags: [kl, autovalores, procesos]
resumen: La versión continua del PCA: descomponer un proceso aleatorio en funciones propias de su covarianza y simularlo con muy pocos términos.
fuentes: ["Karhunen (1947), 'Über lineare Methoden in der Wahrscheinlichkeitsrechnung'", "Loève (1948), 'Fonctions aléatoires du second ordre'"]
---

## En una frase

Cualquier proceso gaussiano centrado se puede escribir como una suma de funciones fijas del
tiempo multiplicadas por números aleatorios independientes, ordenadas por la varianza que aporta
cada una.

## La idea

Un PCA descompone una tabla de datos en direcciones ordenadas por varianza. Una expansión de
Karhunen-Loève hace lo mismo con un proceso: en vez de columnas, tiene un continuo de instantes,
y en vez de vectores propios, funciones propias. El resultado es una serie infinita de senos
—para el puente browniano— con coeficientes aleatorios independientes.

La gracia está en cómo decaen los pesos. En el puente browniano el término `k` aporta una varianza
proporcional a `1/k²`, así que los primeros términos se llevan casi todo y los demás apenas
matizan. Eso convierte una serie infinita en una suma de tres o cuatro términos que se puede
simular, almacenar y analizar.

¿Para qué sirve en la práctica? Para tres cosas concretas: simular trayectorias suaves con la
estructura de correlación correcta, reducir la dimensión de una familia de curvas (tipos de
interés, superficies de volatilidad) y entender qué modos dominan un proceso. Es la misma idea que
un PCA de curvas, con la ventaja de que aquí la covarianza está definida en tiempo continuo y la
descomposición es exacta.

:::aviso
Que los tres primeros términos expliquen el 83 % de la varianza no significa que el proceso sea de
tres dimensiones. Significa que, para la varianza **total**, el resto aporta poco. Si tu pregunta
depende de un detalle local —un pico, un cambio brusco—, los términos que descartas pueden ser
justo los que lo contienen.
:::

## Definición formal

Para un proceso gaussiano centrado `B_t` en `[0, 1]` con función de covarianza `K(s, t)`, la
expansión es:

:::formula
B_t = Σ_k √λ_k · Z_k · e_k(t)        Z_k ~ N(0, 1) independientes
:::

donde `λ_k` y `e_k` resuelven la ecuación integral de Fredholm:

:::formula
∫ K(s, t) · e_k(s) ds = λ_k · e_k(t)
:::

- `K(s, t)` — covarianza entre dos instantes; para el puente browniano vale `min(s, t) − s·t`.
- `λ_k` — autovalores: la varianza que aporta el término `k`.
- `e_k(t)` — autofunciones ortonormales: los «vectores propios» del proceso.
- `Z_k` — coeficientes aleatorios independientes, normales estándar.
- `√λ_k` — el peso que convierte un número normal en una contribución con la varianza correcta.

Para el puente browniano las soluciones son explícitas:

:::formula
λ_k = 1 / (k·π)²        e_k(t) = √2 · sin(k·π·t)        k = 1, 2, 3, …
:::

La varianza total del proceso es la suma de los autovalores, `Σλ_k = 1/6`, que es también
`∫ K(t, t) dt = ∫ (t − t²) dt`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `k` | Índice del término | entero | Sube la frecuencia del seno y baja su peso como `1/k²` |
| `λ_k` | Varianza del término `k` | varianza del proceso | Reparte la varianza total: el primero se lleva el 60,8 % |
| `e_k(t)` | Autofunción | adimensional, norma 1 | Define la forma del modo: senos de frecuencia creciente |
| `Z_k` | Coeficiente aleatorio | normal estándar | Sortea la amplitud de cada modo en cada trayectoria |
:::

## Ejemplo

La varianza total es `1/6 = 0,16667`.

- Con 3 términos: `(1 + 1/4 + 1/9)/π² = 0,13791`, el **82,75 %** de la varianza.
- Con 10 términos: `0,15702`, el **94,21 %**.
- Con 50 términos: `0,16466`, el **98,80 %**.

El primer término se lleva `1/π² = 0,10132`, es decir, el 60,8 % él solo: es el modo de menor
frecuencia, un arco amplio que sube y baja una vez en el intervalo. Los términos siguientes
añaden ondulaciones cada vez más finas y cada vez menos importantes.

Esa es la cuenta que justifica truncar la serie. No es una aproximación por comodidad: es una
decisión cuantificada.

## Código

```python verificable
import numpy as np

t = np.linspace(0, 1, 2000, endpoint=False)

def e(k):
    return np.sqrt(2) * np.sin(k * np.pi * t)

total = 1 / 6
for k in (3, 10, 50):
    lam = sum(1 / (j * np.pi) ** 2 for j in range(1, k + 1))
    print(f"{k} terminos varianza {lam:.6f} fraccion {lam / total:.2%}")

print(f"producto 1,2 {(e(1) * e(2)).mean():+.6f}")   # -> producto 1,2 +0.000000
print(f"norma 1 {(e(1) ** 2).mean():.6f}")           # -> norma 1 1.000000
```

Las tres primeras líneas dan la fracción de varianza capturada; las dos últimas comprueban que
las autofunciones son ortonormales en la rejilla, que es la condición para que la serie funcione.

:::claves
- `np.sqrt(2) * np.sin(k * np.pi * t)` es la autofunción normalizada. Sin el `√2`, la norma sería
  ½ y la suma de varianzas saldría la mitad de la correcta.
- `np.linspace(0, 1, 2000, endpoint=False)` deja fuera el 1 para que la integral sea la media
  exacta sobre el periodo. Con `endpoint=True` se duplica el punto 1 y la norma se desvía.
- `(e(1) * e(2)).mean()` aproxima la integral del producto porque la rejilla es uniforme en `[0,1)`:
  media y integral coinciden en ese caso.
- `sum(1 / (j * np.pi) ** 2 ...)` calcula la varianza truncada **analíticamente**. Simular 1.000
  trayectorias para estimarla añadiría ruido de Monte Carlo a una cuenta exacta.
- `lam / total` convierte la varianza acumulada en una fracción que se puede leer. El total `1/6`
  sale de integrar la varianza del puente en cada instante, no de la suma de la serie.
:::

## Errores típicos

- **Confundirla con la serie de Fourier.** En Fourier los coeficientes son fijos y la serie
  describe una función concreta; aquí los coeficientes son aleatorios y la serie describe un
  proceso.
- **Truncar sin medir cuánto se pierde.** Decir «con tres términos vale» sin calcular la fracción
  de varianza es una opinión. La cuenta es una línea de código.
- **Olvidar normalizar las autofunciones.** Si no son ortonormales, la varianza de la suma no es la
  suma de varianzas y la simulación sale con la escala equivocada.
- **Aplicarla a un proceso no gaussiano y creer que la truncación conserva la ley.** La expansión
  reproduce la covarianza, no la distribución completa. Si el proceso tiene saltos o colas gordas,
  la serie truncada los pierde.
- **Usar el kernel equivocado.** `min(s,t) − s·t` es el del puente browniano (atado en los dos
  extremos). El browniano normal usa `min(s,t)`; cambiar uno por otro da autofunciones distintas y
  el resultado no cuadra.
- **Creer que los autovalores son «importancia» en cualquier sentido.** Son varianza explicada. Si
  tu pregunta es sobre la forma de las trayectorias, la importancia puede ser otra.

:::practica
enunciado: Un analista dice que con dos términos ya tiene el proceso. Comprueba qué fracción de la varianza captura y decide si es defendible para simular un puente browniano.
pista: Suma 1/(kπ)² para k = 1 y 2 y divide por 1/6.
solucion: λ₁ + λ₂ = (1 + 0,25)/π² = 0,12665, frente a 0,16667 totales: el 75,99 %. Es defendible si solo interesa la forma gruesa de la trayectoria, pero no si el análisis depende de los extremos o de las oscilaciones rápidas, que viven en los términos altos.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué los pesos de la expansión del puente browniano decaen tan rápido?
o: Porque su covarianza es muy suave y un proceso suave se describe con pocos modos
o: Porque el proceso tiene media cero
o: Porque los senos son funciones periódicas
a: 1
e: Cuanto más suave es la covarianza, más rápido decaen los autovalores. El puente browniano tiene covarianza `min(s,t) − st`, que es continua y con una sola esquina, y por eso los pesos caen como `1/k²`. Un proceso con más rugosidad necesitaría más términos.
:::

:::quiz
p: ¿Qué mide la suma de los autovalores de la expansión?
o: La varianza total del proceso, que es la integral de la covarianza en la diagonal
o: El número de términos necesarios para la serie
o: La media del proceso en el intervalo
a: 1
e: `Σλ_k = ∫K(t,t)dt` es la varianza total. Para el puente browniano vale 1/6. No dice cuántos términos hacen falta —eso depende de la tolerancia— y no tiene relación con la media, que es cero por construcción.
:::
