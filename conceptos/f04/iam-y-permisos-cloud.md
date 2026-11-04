---
id: iam-y-permisos-cloud
titulo: Identidad y permisos en la nube
fase: 4
nivel: intermedio
rutas: [de, alg]
prerequisitos: [nubes-y-servicios-gestionados, autenticacion-y-autorizacion]
tags: [iam, permisos, seguridad]
resumen: Quién puede hacer qué sobre qué recurso: roles, políticas, mínimo privilegio y por qué el comodín de permisos es el fallo de seguridad más caro.
fuentes: ["AWS (2024), 'IAM User Guide'", "NIST (2020), 'SP 800-207, Zero Trust Architecture'"]
---

## En una frase

Una política de identidad es una frase que dice **quién** puede hacer **qué** sobre **qué
recurso**, y el mínimo privilegio consiste en escribirla lo más estrecha posible.

## La idea

En la nube no hay un usuario con contraseña que lo puede todo: hay identidades y políticas. Una
identidad puede ser una persona, un servicio o una máquina. Una política es una lista de permisos
que se adjunta a esa identidad o al recurso.

El error clásico es empezar con «dame acceso completo mientras pruebo» y no volver nunca. Ese
permiso amplio acaba en un pipeline que puede borrar el lago entero, en una clave que se filtra en
un repositorio y en un incidente que nadie sabe explicar. El mínimo privilegio no es una doctrina
de auditoría: es la diferencia entre un fallo y una catástrofe.

La segunda pieza es la **credencial de corta duración**. Una clave permanente que vive en un
`.env` se filtra tarde o temprano. Un rol que el servicio asume y renueva cada hora no tiene nada
que filtrar: si alguien copia el token, caduca solo. Por eso los servicios en la nube no usan
claves, usan roles.

:::trampa
El comodín `"Resource": "*"` con `"Action": "*"` convierte cualquier credencial filtrada en control
total de la cuenta. Si además esa clave está en un repositorio público, el tiempo hasta que alguien
la use se mide en minutos: hay bots que barren GitHub buscando exactamente eso.
:::

## Definición formal

Una política se compone de declaraciones con cuatro campos, y el resultado es la unión de lo
permitido menos lo denegado explícitamente:

:::formula
{ Effect, Principal, Action, Resource }        efectivo = (permitido ∪) − (denegado explícito)
:::

- **Effect** — `Allow` o `Deny`. Un `Deny` explícito gana siempre.
- **Principal** — quién: usuario, rol, cuenta o servicio.
- **Action** — qué operación: `s3:GetObject`, `bigquery.jobs.create`.
- **Resource** — sobre qué: el ARN o el nombre del recurso, con comodines si hace falta.
- **Condition** — opcional: restringe por IP, etiqueta, hora o MFA.

Tres patrones que cubren casi todo:

- **Rol de servicio**: la máquina asume un rol y recibe credenciales temporales.
- **Acceso entre cuentas**: una cuenta confía en un rol de otra mediante `AssumeRole` y una
  condición.
- **Permiso por etiqueta**: el pipeline solo puede tocar recursos con `entorno=dev`, y así no hace
  falta una política por recurso.

## Ejemplo

Un proceso de carga que solo debe escribir en una carpeta del lago y leer de una cola:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": "arn:aws:s3:::lago-datos/entrada/ventas/*"
    },
    {
      "Effect": "Allow",
      "Action": ["sqs:ReceiveMessage", "sqs:DeleteMessage"],
      "Resource": "arn:aws:sqs:eu-west-1:123456789012:cola-ventas"
    },
    {
      "Effect": "Deny",
      "Action": ["s3:DeleteObject", "s3:PutBucketPolicy"],
      "Resource": "*"
    }
  ]
}
```

La tercera declaración no es redundante: aunque otra política permitiera borrar, el `Deny`
explícito lo bloquea. Es la forma de poner un suelo a los permisos cuando varias políticas se
suman.

## Código

```text
Lista de comprobación antes de dar un permiso (cinco minutos que ahorran un incidente):

  1. ¿Qué operación exacta necesita?           s3:PutObject, no s3:*
  2. ¿Sobre qué ruta exacta?                   .../entrada/ventas/*, no *
  3. ¿Durante cuánto tiempo?                   rol temporal, no clave permanente
  4. ¿Desde dónde?                             condición de red o de etiqueta
  5. ¿Quién lo va a auditar?                   registro de accesos activado

Comprobación de que un rol no puede más de la cuenta:

  aws iam simulate-principal-policy \
      --policy-source-arn arn:aws:iam::123456789012:role/carga-ventas \
      --action-names s3:DeleteObject s3:PutObject \
      --resource-arns arn:aws:s3:::lago-datos/entrada/ventas/x.parquet
```

## Errores típicos

- **Empezar con administrador y no recortar nunca.** El permiso temporal se queda para siempre y
  nadie recuerda por qué estaba.
- **Claves de acceso permanentes en el código o en un `.env`.** Usa roles y credenciales
  temporales; si hay que usar una clave, que sea de una identidad sin permisos de escritura.
- **Confundir autenticación con autorización.** Que el servicio esté autenticado no significa que
  pueda tocar ese recurso; son dos controles distintos.
- **Permitir por prefijo de nombre y no por ruta completa.** `*ventas*` incluye
  `ventas_borrador`, `ventas_antiguo` y lo que alguien llame así mañana.
- **No auditar.** Sin registro de accesos no se puede responder «quién borró esto» cuando pasa.
  El log de auditoría es parte del permiso, no un extra.
- **Dar permisos a una persona para lo que hace un servicio.** Si es un pipeline, va un rol de
  servicio; las credenciales de personas rotan y se van con ellas.

:::practica
enunciado: Un analista necesita leer una tabla de BigQuery y no debe poder modificarla. Escribe qué identidad, qué rol y qué condición usarías, y qué comprobarías después.
pista: El rol mínimo de lectura es `roles/bigquery.dataViewer` sobre el dataset, no sobre el proyecto.
solucion: Una cuenta de servicio o el usuario del analista con `roles/bigquery.dataViewer` limitado al dataset concreto, más `roles/bigquery.jobUser` a nivel de proyecto para poder lanzar consultas. Después: probar que un `INSERT` falla, revisar el registro de auditoría y comprobar que no hereda permisos de un grupo con más privilegios.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué es mejor un rol con credenciales temporales que una clave de acceso permanente?
o: Porque el token caduca solo y no hay nada que filtrar de forma permanente
o: Porque el rol tiene más permisos
o: Porque las claves permanentes no funcionan en la nube
a: 1
e: La credencial temporal se renueva y caduca; una copia filtrada deja de servir en horas. La clave permanente, en cambio, sigue válida hasta que alguien la revoca, y para entonces puede llevar meses en un repositorio.
:::

:::quiz
p: Una identidad tiene una política que permite `s3:*` y otra que deniega `s3:DeleteObject`. ¿Puede borrar?
o: No: el Deny explícito gana sobre cualquier Allow
o: Sí: el Allow más amplio prevalece
o: Depende del orden en que se evaluaron las políticas
a: 1
e: La evaluación es determinista: se suman los permisos y se restan los Deny explícitos. El orden no importa. Ese comportamiento es lo que permite poner un suelo de seguridad que ninguna política posterior pueda saltarse.
:::
