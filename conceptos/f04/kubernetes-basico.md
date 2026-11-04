---
id: kubernetes-basico
titulo: Kubernetes básico
fase: 4
nivel: avanzado
rutas: [de, ds]
prerequisitos: [docker-para-datos, orquestacion-y-dag]
tags: [kubernetes, contenedores, despliegue, operacion]
resumen: Describes cuántas copias de tu contenedor quieres y Kubernetes las mantiene vivas, repartidas y accesibles; el precio es un clúster que hay que operar.
fuentes: ["Documentación oficial de Kubernetes, 'Concepts'"]
---

## En una frase

Kubernetes es un bucle de control que compara el estado que has **declarado** en ficheros con
el estado real del clúster y actúa para igualarlos: si un contenedor se muere, arranca otro; si
declaras ocho copias, mantiene ocho; y les da una dirección estable para que nadie tenga que
saber en qué máquina están.

## La idea

Con [[docker-para-datos]] resuelves el «funciona en mi portátil». Te queda el problema
siguiente: ese contenedor tiene que estar corriendo a las tres de la mañana, en una máquina que
se puede caer, con más tráfico a las diez de la mañana y con una versión nueva cada semana. Un
contenedor suelto no se reinicia solo si el proceso muere, nadie lo mueve si el servidor se
apaga y su dirección IP cambia cada vez que arranca.

La analogía exacta es un termostato. Tú no enciendes y apagas la caldera: dices «21 grados» y
el sistema mide, compara y actúa en bucle. En Kubernetes escribes «quiero ocho réplicas de esta
imagen» y dejas que el controlador se encargue. Esa es la diferencia mental importante: **no
das órdenes, describes el resultado**. Si borras un pod a mano, no has destruido nada: el
controlador verá siete donde debería haber ocho y creará otro en segundos.

Lo que compras con eso:

- **Autorreparación**: si el proceso muere, se reinicia; si el nodo entero se cae, sus pods se
  recolocan en los que quedan.
- **Escalado**: cambias un número (o lo deja cambiar una regla) y el número de copias sube o
  baja, sin tocar servidores.
- **Direcciones estables**: un `Service` da un nombre y una IP virtual que no cambian aunque
  los pods detrás vayan y vengan.
- **Despliegues graduales**: una versión nueva entra pod a pod y, si algo va mal, se vuelve
  atrás con un comando.

Lo que pagas: un plano de control que hay que actualizar, nodos que cuestan dinero aunque no
hagan nada, una capa de YAML que hay que aprender y, sobre todo, **alguien que entienda el
sistema cuando a las tres de la mañana no arranca nada**. Un clúster mal operado es menos fiable
que un `cron` en una máquina.

:::aviso
**Cuándo NO usar Kubernetes.** Si tienes un job nocturno, un portátil con datos, un equipo de
dos personas o un servicio que cabe en una máquina, la respuesta correcta casi siempre es un
`cron`, un `systemd` o un servicio gestionado. Kubernetes resuelve un problema de escala
organizativa: muchas aplicaciones, muchos equipos, muchos despliegues al día. Si no tienes ese
problema, la complejidad es coste puro.
:::

## Definición formal

Los objetos que hay que conocer, de abajo arriba:

| Objeto | Qué declara |
| --- | --- |
| `Pod` | La unidad mínima: uno o más contenedores que comparten red y volúmenes. Efímero |
| `ReplicaSet` | Que existan N copias de un pod. Rara vez se escribe a mano |
| `Deployment` | El ReplicaSet más el historial de versiones y la actualización gradual |
| `Service` | Una dirección estable y balanceo entre los pods que coinciden con su selector |
| `Ingress` | Enrutado HTTP desde fuera del clúster hacia los servicios |
| `ConfigMap` | Configuración no secreta, como variables de entorno o ficheros |
| `Secret` | Lo mismo para credenciales: en base64, no cifrado por defecto |
| `Job` y `CronJob` | Trabajo que termina; el segundo, con horario |
| `PersistentVolumeClaim` | Una petición de disco que sobrevive al pod |
| `Namespace` | Una separación lógica de nombres dentro del clúster |

Dos parejas de conceptos que deciden si tu despliegue funciona o se cae solo:

- **`requests` y `limits`.** `requests` es lo que el planificador (*scheduler*) reserva en un
  nodo antes de colocar el pod; `limits` es el techo que el contenedor no puede pasar. Un pod
  solo entra en un nodo que tenga libres sus `requests`. Si se pasa de su límite de CPU, se le
  frena; si se pasa de su límite de memoria, **lo matan** (`OOMKilled`).
- **`readinessProbe` y `livenessProbe`.** La de *readiness* decide si el pod recibe tráfico; la
  de *liveness*, si hay que reiniciarlo. Confundirlas es el error clásico: una comprobación de
  vida que consulta la base de datos reinicia todos tus pods cuando la base de datos va lenta.

En una actualización gradual (`RollingUpdate`) el número de pods que se pueden añadir y quitar
a la vez se controla con dos parámetros:

:::formula
pods_max = ceil(réplicas · (1 + maxSurge))          pods_min = floor(réplicas · (1 − maxUnavailable))
:::

Con `réplicas = 8`, `maxSurge = 25 %` y `maxUnavailable = 25 %`, el despliegue pasa por 10 pods
como máximo y 6 como mínimo en cada momento. Bajar `maxUnavailable` a 0 y subir `maxSurge` es
lo habitual en servicios con tráfico: nunca reduces capacidad, a cambio pagas pico de recursos
durante el despliegue.

## Ejemplo

Un servicio que atiende 1 800 peticiones por segundo en el pico, con pods que sostienen 250
peticiones por segundo cada uno, en un clúster de 3 nodos que admiten 4 pods cada uno:

- Pods necesarios para el pico: 1 800 / 250 = 7,2, es decir **8 pods** (siempre hacia arriba).
- Con un nodo caído quedan 2 nodos × 4 pods = 8 pods, que aguantan 8 · 250 = **2 000 rps**.
- El pico de 1 800 rps entra **por los pelos**: no hay margen para un segundo fallo ni para el
  pico del despliegue, que con `maxSurge = 25 %` pide 10 pods a la vez.

De ahí sale una decisión de diseño concreta: o subes el tamaño del nodo, o pasas a 4 nodos, o
bajas el `maxSurge` a 1 para que el despliegue no intente levantar 10 pods cuando solo hay hueco
para 8. Ese pico lo fija `maxSurge` y nada más: dejar `maxUnavailable` en 1 solo limita cuántos
pods pueden faltar a la vez (el suelo, 7), no el techo. Las tres son válidas; lo que no es válido
es descubrirlo durante el incidente.

Fíjate además en el detalle que enlaza las dos cosas: con `maxSurge: 1` y
`maxUnavailable: 0`, el despliegue tiene que colocar un pod **extra** antes de quitar el
primero. Si el clúster está justo de hueco, ese pod se queda en `Pending` y la actualización no
avanza. No se cae nada —es un fallo seguro— pero tampoco despliegas. El margen de capacidad no
es un lujo: es lo que permite desplegar.

Y el otro número que importa: si cada pod declara `requests: cpu: 500m`, 8 pods piden 4 vCPU
repartidas. En un nodo de 4 vCPU caben 8 pods por CPU y solo 4 por el límite de 4 pods que
hemos supuesto, así que manda el que sea más restrictivo. Los `requests` son reservas reales en
el planificador: ponerlos a ojo, a la baja, sobrevende el nodo y convierte cualquier pico en
una guerra por la CPU.

## Código

```python verificable
# Cuantos pods hacen falta y cuanta capacidad queda si cae un nodo.
pico_rps = 1800          # peticiones por segundo en la hora punta
capacidad_pod = 250      # rps que sostiene un pod con sus requests actuales
nodos = 3
pods_por_nodo = 4        # limite de colocacion por nodo (CPU o memoria)

pods = -(-pico_rps // capacidad_pod)              # division hacia arriba
capacidad_n1 = (nodos - 1) * pods_por_nodo * capacidad_pod

print("pods para el pico:", pods)                 # -> 8
print("rps con un nodo caido:", capacidad_n1)     # -> 2000
print("aguanta el pico con N+1:", capacidad_n1 >= pico_rps)  # -> True
```

```yaml
# Despliegue: estado deseado. Kubectl aplica y el controlador persigue este estado.
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scoring
spec:
  replicas: 8
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: scoring
  template:
    metadata:
      labels:
        app: scoring
    spec:
      containers:
        - name: api
          image: analitica/scoring:1.4.0
          ports:
            - containerPort: 8000
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              memory: 2Gi
          readinessProbe:          # decide si recibe trafico
            httpGet:
              path: /salud
              port: 8000
            initialDelaySeconds: 5
          livenessProbe:           # decide si hay que reiniciarlo
            httpGet:
              path: /vivo
              port: 8000
            initialDelaySeconds: 30
```

```yaml
# Servicio: direccion estable y balanceo. Los pods cambian, el nombre no.
apiVersion: v1
kind: Service
metadata:
  name: scoring
spec:
  selector:
    app: scoring
  ports:
    - port: 80
      targetPort: 8000
```

```bash
kubectl apply -f despliegue.yaml          # declarar el estado deseado
kubectl get pods -l app=scoring           # cuantos hay y en que estado
kubectl describe pod scoring-7d9f-abcde   # por que no arranca este
kubectl rollout undo deploy/scoring       # volver a la version anterior
```

## Errores típicos

- **Poner `limits` de memoria por debajo de lo que el proceso necesita de verdad.** Kubernetes no
  degrada: mata el contenedor y lo reinicia en bucle (`OOMKilled`). Mide el consumo real en
  carga antes de fijar el límite, y deja el `requests` cerca del uso típico.
- **Una `livenessProbe` que comprueba la base de datos.** Cuando la base de datos va lenta, la
  sonda falla, Kubernetes reinicia todos tus pods a la vez, y el servicio pasa de lento a caído.
  La vida del proceso se comprueba sin dependencias; la disponibilidad de la dependencia va en
  la *readiness*.
- **No declarar `readinessProbe`.** Sin ella, el pod recibe tráfico desde el primer segundo,
  cuando todavía está cargando el modelo o calentando la caché: los primeros usuarios comen
  errores en cada despliegue.
- **Usar un `Deployment` para un trabajo por lotes.** Un proceso que termina no encaja en un
  objeto que garantiza que siempre haya N copias vivas: se reiniciará en bucle. Para eso están
  `Job` y `CronJob`, coordinados con [[orquestacion-y-dag]] si el trabajo forma parte de un
  pipeline.
- **Guardar secretos en un `ConfigMap` o en el repositorio.** Un `Secret` de Kubernetes viaja en
  base64, que no es cifrado: cualquiera con permiso de lectura en el espacio de nombres lo lee.
  Los ficheros de YAML con credenciales no se versionan.
- **Escalar solo por CPU.** Una API que espera a una base de datos puede tener la CPU al 15 % y
  estar saturada de peticiones en cola. Escala por la métrica que representa la carga real
  (longitud de cola, latencia, peticiones en vuelo) y usa la CPU como señal secundaria.

## Comprueba que lo sabes

:::quiz
p: Declaras un Deployment con 8 réplicas y borras un pod a mano con `kubectl delete pod`. ¿Qué ocurre?
o: Quedan 7 réplicas hasta que lo vuelvas a aplicar
o: El controlador detecta que hay 7 donde debería haber 8 y crea otro pod en segundos
o: Se reinicia el clúster para restaurar el estado declarado
a: 2
e: Kubernetes es un bucle de reconciliación: compara el estado declarado con el real y actúa. Borrar un pod no cambia el estado deseado, así que el ReplicaSet crea otro. Lo mismo se aplica a un nodo que se cae: sus pods se recolocan en los nodos que quedan.
:::

:::quiz
p: El servicio va lento porque la base de datos está saturada, y de repente todos los pods se reinician en cascada. ¿Cuál es la causa más probable?
o: Que la `livenessProbe` consulta la base de datos y falla cuando esta va lenta
o: Que falta el `readinessProbe`
o: Que los `limits` de CPU están demasiado altos
a: 1
e: Una sonda de vida que depende de un sistema externo convierte una degradación en una caída: si la base de datos tarda, la sonda falla y Kubernetes mata pods que estaban funcionando. La liveness debe comprobar solo que el propio proceso responde; la dependencia externa se comprueba en la readiness o en un circuito de protección.
:::

:::truco
Antes de tocar nada en un incidente, mira `kubectl describe pod` y busca la sección de eventos.
Ahí aparece lo que de verdad ha pasado: `OOMKilled`, `FailedScheduling` por falta de recursos,
`ImagePullBackOff` por una credencial del registro de imágenes o una sonda que lleva diez
intentos fallidos. Los eventos son la única fuente que te dice *por qué*, no solo *qué*.
:::
