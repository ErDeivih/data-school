---
id: git-avanzado
titulo: Git avanzado
fase: 11
nivel: avanzado
rutas: [alg]
prerequisitos: [git-para-datos]
tags: [git, versiones, rebase, bisect]
resumen: Rebase, bisect y reflog: reescribir la historia con criterio, encontrar el commit que rompió algo y recuperar trabajo que dabas por perdido.
fuentes: ["Chacon y Straub (2014), 'Pro Git', 2.ª ed.", "Loeliger y McCullough (2012), 'Version Control with Git', 2.ª ed.", "Git, 'Fighting regressions with git bisect' (documentación oficial)"]
---

## En una frase

Git avanzado no es memorizar comandos raros, sino tener claro que el historial es un grafo que
se puede reescribir en local, que cada desastre reciente tiene una salida por el reflog y que
encontrar el commit que rompió algo es una búsqueda binaria y no una lectura de 300 diferencias.

## La idea

Git guarda un **cuaderno de laboratorio**, no una novela publicada. Un commit no es «la versión
3»: es una foto con un puntero a las fotos anteriores, identificada por el hash de su contenido
y de sus padres. Cambiar el padre cambia el hash, y ahí está toda la diferencia entre reescribir
tu historia local —cosa que puedes hacer mil veces— y reescribir la historia que otros ya tienen
en su clon, que es un problema para el equipo entero.

Con el grafo en la cabeza, casi todo se explica solo:

- Una **rama** es un puntero a un commit. Crear una rama no copia nada.
- **HEAD** es dónde estás. `git switch` mueve HEAD; `git reset` mueve la rama.
- Un **merge** conserva la historia real: crea un commit con dos padres y deja la bifurcación
  visible. Se ve cuándo se integró cada cosa.
- Un **rebase** vuelve a aplicar tus commits sobre otra base. Los commits resultantes son
  nuevos, con hash nuevo, y la historia queda lineal. Es más limpio de leer y **cambia el
  pasado**: si alguien había construido trabajo encima de los hashes viejos, se encuentra con
  dos historias que contienen los mismos cambios pero no son la misma.

La regla práctica que evita el 90 % de los accidentes: **rebase solo en ramas que nadie más ha
tomado como base**. Tu rama de trabajo antes del PR, sí. La rama principal, no. Y si tienes que
forzar el empujón de una rama tuya que ya subiste, `--force-with-lease` en lugar de `--force`:
comprueba que el remoto sigue donde creías, y falla en vez de pisar el trabajo de otro.

Las otras dos piezas que separan a quien usa Git de quien lo sufre:

**Bisect.** Cuando algo funcionaba hace 400 commits y ya no funciona, no hay que leer 400
diferencias: hay que hacer búsqueda binaria. Con 1.000 commits hacen falta 10 comprobaciones,
porque 2¹⁰ = 1.024. Y se puede automatizar: `git bisect run ./prueba.sh` deja que Git haga las
10 vueltas mientras tú haces otra cosa. Esto solo funciona si los commits son pequeños y
compilan: un historial con commits gigantes que mezclan formateo y lógica hace que la bisección
señale un commit que cambió 4.000 líneas.

**Reflog.** Git apunta en el repositorio local por dónde ha pasado HEAD y por dónde han estado
las ramas. Un `reset --hard` que te dejó sin commits «desaparecidos» casi siempre se deshace
con `git reflog` y un `reset` al hash anterior. Por defecto esos registros se conservan 90 días
(30 para los commits que ya no alcanza ninguna referencia), así que el margen es amplio… pero
solo para lo que llegó a ser un commit: **un fichero modificado y nunca confirmado no está en
el reflog**, y eso no se recupera.

Y una consecuencia de equipo: los conflictos son más pequeños si las ramas duran días y no
meses. Un PR de 40 líneas se integra tras una [[code-review|revisión]] corta; uno de 4.000
arrastra conflictos en cada fichero, y su revisión se convierte en un trámite.

## Definición formal

- **Objeto commit.** Inmutable. Contiene: árbol de ficheros, autor, fecha, mensaje y lista de
  hashes de sus padres (cero para el inicial, uno para el normal, dos o más para un merge). Su
  identificador es el hash de ese contenido: **cambiar cualquier cosa, incluido el padre, cambia
  el hash**.
- **Referencia.** Nombre que apunta a un hash: una rama (`refs/heads/x`), una etiqueta
  (`refs/tags/v1`), `HEAD`, `ORIG_HEAD`, o las entradas del reflog. `git log` recorre el grafo
  desde una referencia.
- **Ancestro común (LCA).** El commit más reciente que es antecesor de dos ramas. Todo merge de
  tres vías trabaja con él: los cambios de cada lado son las diferencias contra ese ancestro.
- **Fast-forward.** Si la rama destino no tiene commits propios desde el ancestro común, basta
  con mover el puntero: no hace falta ningún commit de merge.
- **Rebase.** Dado un conjunto de commits `C₁ … Cₖ` con ancestro común `A` y una base nueva `B`,
  el rebase aplica los parches de `C₁ … Cₖ` en orden sobre `B`, produciendo commits nuevos
  `C'₁ … C'ₖ` cuyos hashes difieren de los originales. El número de conflictos posibles es como
  mucho `k`, uno por commit reaplicado.
- **Bisect.** Búsqueda binaria sobre una secuencia ordenada de commits, sabiendo que existe un
  commit bueno `g` y uno malo `b` con `g` antecesor de `b`. Número de pasos:

:::formula
pasos = ⌈log₂ (n)⌉
:::

  con `n` el número de commits entre `g` y `b`. Cada paso reduce el intervalo a la mitad, así
  que 64 commits son 6 pasos y 1.024 son 10.
- **Cherry-pick.** Aplicar el parche de un commit concreto sobre la rama actual, creando un
  commit nuevo. Útil para llevar un arreglo puntual a una rama de mantenimiento; peligroso para
  integrar ramas enteras, porque duplica cambios que luego chocan en el merge.
- **Revert.** Crear un commit nuevo que deshace otro. A diferencia del reset, no reescribe
  nada: es la forma correcta de deshacer algo que ya está publicado.

## Ejemplo

Un historial de 64 commits entre la versión que funcionaba (`c00`) y la que falla (`c63`). El
primer commit con el fallo es `c41`, dato que quien hace la bisección no conoce.

Secuencia de sondas de `git bisect`: 31 (bueno), 47 (malo), 39 (bueno), 43 (malo), 41 (malo),
40 (bueno). Seis comprobaciones y el intervalo queda entre 40 y 41: el culpable es el 41.

Sin bisección, una búsqueda lineal desde el principio habría comprobado 42 commits —del 0 al 41—
en lugar de 6. Y con 1.000 commits en lugar de 64, la bisección necesita 10 comprobaciones
mientras la búsqueda lineal necesitaría, en el peor caso, 1.000.

:::figura
fichero: git-avanzado-bisect
pie: Izquierda, las seis sondas del ejemplo: cada barra es el intervalo de commits que sigue siendo candidato después de esa comprobación, y cada sonda lo parte por la mitad (31 bueno, 47 malo, 39 bueno, 43 malo, 41 malo, 40 bueno). En seis vueltas el intervalo pasa de 63 commits a uno solo, y el culpable es la frontera: el 41. Derecha, lo que costaría cada estrategia en este historial: 6 comprobaciones de la suite frente a las 42 de una búsqueda lineal. La conclusión práctica es que el coste de la bisección depende del logaritmo del número de commits, no de dónde esté el fallo.
fuente: figuras/git-avanzado-1.py
:::

El otro caso típico: te das cuenta de que borraste una rama con `git branch -D` y tenía tres
commits sin integrar. El reflog guarda el hash al que apuntaba esa rama; con
`git reflog` y `git branch recuperada HASH` vuelve. Si esos commits nunca llegaron a
confirmarse, no hay nada que recuperar.

## Código

```python verificable
# La logica de git bisect: busqueda binaria hasta el primer commit que rompio algo.
n_commits = 64
primer_malo = 41        # el bisect no conoce este dato: lo descubre probando

def esta_malo(commit):
    # Hace de suite de pruebas: dice si ese commit ya tiene el fallo.
    return commit >= primer_malo

izquierda, derecha = 0, n_commits - 1    # izquierda: se sabe bueno; derecha: se sabe malo
sondas = []
# Se para cuando quedan dos commits seguidos: el malo es el de la derecha.
while derecha - izquierda > 1:
    # // es division entera: trunca hacia abajo y siempre da un commit valido.
    medio = (izquierda + derecha) // 2
    sondas.append(medio)
    if esta_malo(medio):
        derecha = medio         # el fallo ya estaba: se descarta la mitad derecha
    else:
        izquierda = medio       # el fallo vino despues: se descarta la mitad izquierda

print("commits en el historial:", n_commits)           # -> 64
print("sondas realizadas:", len(sondas))               # -> 6
print("secuencia:", sondas)                            # -> [31, 47, 39, 43, 41, 40]
print("primer commit malo:", derecha)                  # -> 41
print("con busqueda lineal:", primer_malo + 1)         # -> 42
```

:::claves
- La búsqueda binaria **necesita el intervalo ordenado y con los dos extremos conocidos**:
  aquí `0` es bueno y `63` es malo. `git bisect` pide exactamente esos dos datos (`good` y
  `bad`) y sin ellos no puede empezar.
- El bucle para cuando `derecha - izquierda == 1`, no cuando son iguales: al final quedan dos
  commits consecutivos y el culpable es el de la derecha, que es el que se imprime. Si
  imprimieras `izquierda` darías el commit anterior, que es el bueno.
- `//` es división entera. Con `/` saldría un `float` como `31.5` y `sondas` guardaría
  números que no son commits: el fallo aparecería mucho más tarde, al indexar.
- La mitad de las **sondas** no son comparaciones de la lista: cada sonda ejecuta la suite de
  pruebas entera sobre ese commit. El coste de la bisección es el coste de la suite
  multiplicado por el número de sondas, y por eso `git bisect run` importa.
- El número de sondas depende de **cuántos commits hay**, no de dónde esté el culpable. Con
  64 commits son 6 vueltas tanto si el fallo entró en el commit 5 como en el 60.
- Si los commits no compilan por separado, la bisección no puede decidir y `git bisect` te
  pide que marques ese commit como `skip`: cada `skip` quita una sonda del cálculo y alarga
  la búsqueda.
:::

```bash ilustrativo
# Limpiar tu propia rama antes del PR, sin tocar nada publicado
git switch mi-rama
git rebase -i main          # squash, reword, drop: la historia que quieres ensenar

# Empujar despues de reescribir: comprueba que el remoto no se ha movido
git push --force-with-lease origin mi-rama

# Encontrar el commit que rompio la suite, automatizado
git bisect start
git bisect bad                      # HEAD esta mal
git bisect good v2.3.0              # esta etiqueta funcionaba
git bisect run pytest -q tests/test_pagos.py
git bisect reset                    # vuelve al estado inicial

# Recuperar commits que un reset --hard dejo fuera de la rama
git reflog
git branch recuperada a1b2c3d
```

```text
Ejemplo de salida de `git reflog` (hashes acortados):

a1b2c3d HEAD@{0}: reset: moving to HEAD~3
9f8e7d6 HEAD@{1}: commit: corrige el redondeo del IVA
4c5b6a7 HEAD@{2}: commit: extrae la funcion de descuento
1d2e3f4 HEAD@{3}: checkout: moving from main to mi-rama
```

## Errores típicos

- **`git push --force` sobre una rama compartida.** Reescribes commits que otros ya tienen: sus
  clones quedan con dos historias divergentes y, al traer los cambios, vuelven a aparecer los
  commits viejos. Usa `--force-with-lease`, y solo en ramas tuyas.
- **Rebasar commits ya publicados porque «queda más limpio».** El historial lineal es agradable
  de leer, pero la limpieza se paga con hashes nuevos y conflictos para todo el equipo. La
  historia compartida se integra con merge; el rebase se reserva para lo que aún no ha salido de
  tu máquina.
- **Confiar en el reflog para todo.** Recupera commits, no ficheros. Un `git checkout -- fichero`
  o un `reset --hard` con cambios sin confirmar destruyen trabajo que nunca existió como objeto
  de Git: no hay hash, no hay entrada, no hay recuperación.
- **Commits que mezclan formateo y lógica.** La bisección apunta a un commit que cambió 4.000
  líneas y no dice nada; el `revert` de un arreglo se lleva por delante el reformateo de medio
  proyecto. Un cambio lógico por commit, con mensaje que explique el porqué.
- **Bisecar a mano cuando la suite puede decidir.** `git bisect run` automatiza las vueltas; a
  mano se abandona a la tercera. Y si la suite tarda veinte minutos, la bisección se vuelve
  inviable: otra razón para tener una [[testing-piramide|suite rápida]] en la base.
- **Resolver los conflictos con prisa.** Quedarse con «mi versión» o «la suya» sin entender las
  dos partes borra cambios que la otra persona necesitaba. Un conflicto es una pregunta, no un
  estorbo: si no sabes qué quiere cada lado, pregunta antes de confirmar.

## Comprueba que lo sabes

:::quiz
p: ¿Por qué un rebase cambia los hashes de los commits, y un merge no?
o: Porque el rebase comprime los commits
o: Porque cada commit reaplicado tiene un padre distinto, y el hash depende del contenido y de los padres
o: Porque el rebase solo funciona en repositorios vacíos
a: 2
e: El hash es el resumen del contenido del commit, que incluye la referencia a sus padres. Un merge crea un commit nuevo y deja los anteriores intactos; el rebase crea copias con otra base, así que son objetos distintos.
:::

:::quiz
p: Un historial tiene 1.024 commits entre la versión buena y la mala. ¿Cuántas comprobaciones necesita una bisección, en el peor caso?
o: 10, porque 2¹⁰ = 1.024
o: 512, la mitad
o: 1.024, una por commit
a: 1
e: Cada sonda descarta la mitad del intervalo restante, así que el número de pasos es el techo del logaritmo en base 2 del número de commits. Con 1.024 commits son 10 vueltas, y por eso la bisección se puede automatizar con `git bisect run`.
:::

:::quiz
p: Hiciste `git reset --hard HEAD~3` y quieres recuperar los commits. ¿Qué haces?
o: Buscar el hash en `git reflog` y volver a apuntar una rama ahí
o: Volver a escribir el código, porque Git no guarda esa información
o: Ejecutar `git fsck` y esperar a que aparezca solo
a: 1
e: El reflog registra por dónde ha pasado HEAD en el repositorio local y conserva esos commits alcanzables durante 90 días, así que basta con crear una rama en el hash anterior. Lo que no se recupera son los cambios de fichero que nunca se confirmaron.
:::
