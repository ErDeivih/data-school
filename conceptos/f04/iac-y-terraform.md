---
id: iac-y-terraform
titulo: Infraestructura como código
fase: 4
nivel: avanzado
rutas: [de, ds]
prerequisitos: [kubernetes-basico, docker-para-datos, git-para-datos]
tags: [iac, terraform, infraestructura, reproducibilidad]
resumen: Describir servidores, redes y permisos en ficheros versionados permite revisar los cambios como código, recrear el entorno entero y saber qué hay contratado.
fuentes: ["Documentación oficial de HashiCorp, 'Terraform Documentation'"]
---

## En una frase

La infraestructura como código (IaC) es escribir en ficheros de texto todo lo que hay montado
—servidores, redes, permisos, almacenamiento— para que esos ficheros sean la única verdad, se
revisen como cualquier cambio de código y permitan reconstruir el entorno desde cero.

## La idea

Pregunta en cualquier empresa quién creó el *bucket* de datos y por qué ese usuario tiene
permisos de escritura sobre él. La respuesta habitual es «se hizo a mano en 2022 y funcionaba».
Ese es el punto de partida: la infraestructura real existe, nadie la ha descrito y nadie sabe
qué pasaría si hubiera que rehacerla. IaC convierte ese conocimiento en un artefacto
comprobable.

La analogía es la diferencia entre el plano de un edificio y el edificio. Con el plano puedes
discutir si la pared va aquí, calcular si cabe un despacho más y reconstruir la planta después
de un incendio. Sin plano, solo puedes mirar las paredes y deducir.

Hay una pieza que sorprende a todo el mundo la primera vez: **el fichero de estado**
(`terraform.tfstate`). Terraform no deduce lo que hay en la nube mirando el mundo; guarda en ese
fichero la correspondencia entre cada recurso de tu código y el identificador real del recurso
creado. Por eso el estado es la pieza más crítica y la que más problemas da: si lo pierdes, no
sabe qué gestiona; si lo compartes mal, dos personas pueden destruir el trabajo de la otra; y
como contiene los valores de tus recursos, **contiene secretos en texto plano**.

El otro concepto es la **deriva** (*drift*): el estado real se ha separado del declarado porque
alguien tocó la consola, un script antiguo o un autoescalado. La herramienta no oculta ese
cambio, lo enseña en el plan. Esa es justamente su virtud: convierte «creo que alguien cambió
algo» en una lista de diferencias concretas.

:::nota
**Declarativo no es lo mismo que imperativo.** Terraform, CloudFormation y los manifiestos de
[[kubernetes-basico]] son declarativos: describes el resultado y la herramienta calcula los
pasos. Ansible es sobre todo imperativo, aunque sus módulos sean idempotentes: describes tareas
en orden. Pulumi es declarativo pero se escribe en un lenguaje de programación real. La
diferencia importa cuando algo falla a medias: en declarativo vuelves a aplicar, en imperativo
piensas en qué paso quedó a medias.
:::

## Definición formal

Un proyecto de Terraform se organiza así:

| Pieza | Qué es |
| --- | --- |
| Provider | El complemento que habla con una plataforma (nube, base de datos, DNS) |
| Resource | Un objeto gestionado: una máquina, una red, un permiso |
| Data source | Una consulta de solo lectura a algo que ya existe y no gestionas |
| Variable | Un valor de entrada, para no repetir el mismo dato en diez sitios |
| Output | Un valor de salida que otros módulos o personas consumen |
| Módulo | Un conjunto de recursos reutilizable con entradas y salidas |
| Estado | El fichero que liga tu código con los recursos reales |
| Plan | La diferencia calculada entre el estado declarado y el real |

El ciclo de trabajo tiene tres pasos y son siempre los mismos:

:::formula
init → plan → apply          y después, plan otra vez: debe salir vacío
:::

Que el plan salga vacío después de aplicar es la definición operativa de **idempotencia**: la
segunda aplicación no tiene nada que hacer porque el mundo ya coincide con lo declarado. Si
aplicas dos veces y el plan sigue proponiendo cambios, tienes un recurso que se define a sí
mismo con un valor nuevo cada vez (una marca de tiempo, un identificador aleatorio) y nunca
convergerá.

Dos reglas que evitan la mayor parte de los incidentes:

- **El estado va en un backend remoto con bloqueo.** El bloqueo impide que dos `apply`
  simultáneos escriban a la vez; el backend remoto evita que el estado viva en un portátil.
- **Lo que no está en el código no existe.** Si alguien crea un recurso a mano, IaC no lo ve
  —no aparece en el plan— hasta que lo importas con `terraform import`. La consola se usa para
  leer y depurar, no para crear.

## Ejemplo

Tienes declarado un grupo de servidores con 3 nodos y un tipo de máquina. Alguien entra en la
consola una noche y sube el número a 5 «para probar». El plan del día siguiente lo detecta:

```text
$ terraform plan
...
  ~ recurso grupo_de_servidores
      nodos: 5 -> 3
      tipo:  "standard-4" -> "standard-4"

Plan: 0 to add, 1 to change, 0 to destroy.
```

La huella del estado declarado y la del estado real no coinciden; la diferencia es exactamente
un campo, `nodos`. Después de aplicar, la huella vuelve a coincidir con la declarada y un plan
nuevo sale vacío. Si nadie hubiera revisado el plan y se hubiera aplicado en automático, el
`apply` habría destruido dos nodos a las tres de la mañana, posiblemente con trabajo encima.

Ese es el motivo de que el plan se lea siempre, aunque el pipeline sea automático: la frase
«0 to add, 1 to change, 0 to destroy» es la que decide si puedes irte a dormir.

## Código

```text
# variables.tf: lo que cambia entre entornos esta declarado, no escondido
variable "entorno" {
  type        = string
  description = "dev, staging o prod"
}

variable "nodos" {
  type    = number
  default = 3
}

# main.tf: el recurso y su version de provider fijada
terraform {
  required_version = ">= 1.6"
  required_providers {
    plataforma = {
      source  = "ejemplo/plataforma"
      version = "~> 2.4"
    }
  }
}

resource "plataforma_grupo" "procesamiento" {
  nombre = "procesamiento-${var.entorno}"
  nodos  = var.nodos
  etiquetas = {
    entorno = var.entorno
    equipo  = "datos"
  }
}

output "id_del_grupo" {
  value = plataforma_grupo.procesamiento.id
}
```

```python verificable
import hashlib, json

def huella(estado):
    # Resumen estable del estado: el mismo contenido da siempre la misma huella
    return hashlib.sha256(json.dumps(estado, sort_keys=True).encode()).hexdigest()[:12]

declarado = {"nodos": 3, "tipo": "standard-4", "autoscaling": True}
observado = {"nodos": 5, "tipo": "standard-4", "autoscaling": True}   # alguien toco la consola

campos = sorted(set(declarado) | set(observado))
deriva = [c for c in campos if declarado[c] != observado.get(c)]

print("huella declarada:", huella(declarado))        # -> 6fadfd3a9ebf
print("huella observada:", huella(observado))        # -> c0651201979b
print("campos con deriva:", deriva)                  # -> ['nodos']
print("coincide tras aplicar:", huella({**observado, "nodos": 3}) == huella(declarado))  # -> True
```

```bash
terraform init                       # descarga providers y prepara el backend
terraform plan -out=plan.tfplan      # calcula el cambio y lo guarda
terraform apply plan.tfplan          # aplica exactamente el plan revisado
terraform plan                       # debe salir: No changes
terraform state list                 # que recursos gestiona este estado
```

## Errores típicos

- **Guardar el estado en el portátil o en Git.** El estado contiene credenciales en texto plano
  y, si está en local, dos personas aplicando a la vez se pisan. Va en un backend remoto con
  cifrado y bloqueo, y nunca en el repositorio.
- **Tocar la consola «solo esta vez».** Es la forma número uno de crear deriva: el cambio no
  está en el código, el siguiente plan lo revierte sin avisar a nadie y la persona que lo hizo a
  mano se enterará cuando desaparezca. Si alguna vez hay que hacerlo, se importa después.
- **Aplicar sin leer el plan.** Un cambio de una propiedad inmutable no se modifica: se destruye
  el recurso y se crea otro. Con una base de datos en medio, eso es una pérdida de datos. Lee
  siempre la línea de `destroy` y desconfía de cualquier plan que no hayas generado tú.
- **Dejar los secretos en variables del código.** `var.contrasena` acaba escrita en el estado y
  en el historial del pipeline. Los secretos viven en un gestor de secretos y se referencian;
  los ficheros `*.tfvars` con credenciales se ignoran en Git.
- **No fijar la versión del provider.** Sin `required_providers` con versión, un `init` dentro
  de seis meses descarga una versión mayor con cambios de sintaxis y el pipeline se rompe solo,
  el día que nadie ha tocado nada.
- **Un único estado para toda la organización.** Con desarrollo y producción en el mismo estado,
  un `apply` equivocado en una rama puede tocar los recursos de producción. Separa por entorno y
  por ciclo de vida: lo que se crea una vez (redes, cuentas) no debería vivir junto a lo que
  cambia cada semana.

## Comprueba que lo sabes

:::quiz
p: ¿Para qué sirve el fichero de estado de Terraform?
o: Para guardar una copia de seguridad de los datos de la infraestructura
o: Para relacionar cada recurso del código con el identificador real del recurso creado
o: Para acelerar la descarga de los providers
a: 2
e: Terraform no deduce el mundo mirando la plataforma: consulta su estado para saber qué gestiona. Por eso el estado es crítico y por eso contiene credenciales en claro: no es una copia de seguridad ni un fichero de configuración.
:::

:::quiz
p: Aplicas Terraform, y al volver a ejecutar `plan` sigue proponiendo cambios en el mismo recurso. ¿Qué significa?
o: Que el estado está corrupto y hay que recrearlo
o: Que el recurso no es idempotente: alguno de sus campos toma un valor nuevo en cada ejecución
o: Que alguien ha tocado la consola y hay deriva
a: 2
e: Tras aplicar, el plan debe salir vacío. Si no lo hace, el valor declarado no se corresponde con el real de forma estable: suele ser un campo que genera un valor nuevo cada vez (marca de tiempo, identificador aleatorio) o un campo que la plataforma normaliza a otro formato. La deriva también produce cambios, pero desaparece después de aplicarlos.
:::

:::aviso
Importar un recurso creado a mano con `terraform import` lo mete en el estado, pero **no** escribe
el código por ti. Hasta que escribas el bloque a mano y coincida con lo que hay, el plan
propondrá modificaciones o destrucciones. Importa siempre en un entorno de pruebas primero.
:::
