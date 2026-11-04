---
id: freelance-y-consultoria
titulo: Freelance y consultoría
fase: 12
nivel: intermedio
rutas: [core]
prerequisitos: [especializacion-y-carrera, portfolio-y-proyectos, escribir-un-informe]
tags: [carrera, consultoria, precios, negocio]
resumen: Presupuestar y cobrar por entregables: días facturables reales, colchón de horas, cláusula de cambios y criterios de aceptación por escrito.
fuentes: ["Gerber (1995), 'The E-Myth Revisited'"]
---

## En una frase

Como freelance no te pagan por estar disponible sino por entregar algo concreto, así que tu
trabajo empieza antes de tocar los datos: decidir cuántas horas puedes facturar de verdad, qué
entra en el precio y qué ocurre cuando el cliente pide «una cosa más». Es la versión comercial de
elegir en qué te especializas y qué enseñas: [[especializacion-y-carrera|especialización]] y
[[portfolio-y-proyectos|portafolio]].

## La idea

Cobrar por horas parece lo más justo y es lo que más te limita. Si facturas 40 horas, cobras 40
horas, aunque el problema que has resuelto le ahorre al cliente cien veces ese importe. Y si
tardas menos, cobras menos: el modelo premia ir despacio. La alternativa, cerrar un precio por un
entregable definido, traslada el riesgo de las horas a ti, y eso solo se puede hacer con dos cosas
escritas: un alcance cerrado y un criterio para saber cuándo has terminado.

La trampa no es intelectual, es diaria. El cliente ve tu trabajo desde fuera y cada petición nueva
le parece pequeña: «ya que estás conectado a la base de datos, ¿puedes añadir también las
devoluciones?». Para él son dos minutos de conversación; para ti son tres días que desaparecen de
un presupuesto ya cerrado. Sin una regla previa, cada petición se convierte en una negociación
incómoda, y la mayoría de la gente cede porque el cliente es simpático y la relación importa.

Hay tres cuentas que conviene hacer antes de dar un precio:

1. **Cuántas horas facturas de verdad.** Un asalariado tiene unas 1.760 horas anuales de jornada;
   tú no. De los días laborables se van formación, propuestas que no se cierran, facturas,
   gestoría, bajas y tiempo comercial. En la práctica, entre el 60 % y el 75 % de tu jornada es
   facturable, y eso sube la tarifa necesaria entre un 33 % y un 67 % respecto a dividir tu
   objetivo entre las horas «oficiales».
2. **Qué entra en el precio.** Una lista de entregables con nombre y formato («dos procesos de
   ingesta en producción», «un [[escribir-un-informe|informe]] de 8 páginas», «una sesión de
   formación de 3 horas para 6 personas»), y la lista de lo que queda fuera, también por escrito.
3. **Qué pasa si cambia.** Un cambio de alcance no es un problema: es trabajo nuevo a precio
   nuevo. La fórmula más sencilla es una bolsa de horas firmada de antemano que se consume y se
   documenta.

Y algo que casi nadie escribe y que evita casi todas las discusiones: el **criterio de
aceptación**. Un entregable se considera aceptado si en 10 días laborables nadie ha objetado por
escrito. Sin esa frase, «terminado» lo define el cliente, y siempre puede quedar «casi».

Los cuatro modelos de cobro habituales:

| Modelo | Quién asume el riesgo de las horas | Cuándo tiene sentido |
| --- | --- | --- |
| Por horas | El cliente | Auditorías, exploración, soporte continuo |
| Precio fijo | Tú | Alcance estable y medible, con colchón del 20-30 % |
| Retainer mensual | Compartido | Mantenimiento, guardias, disponibilidad pactada |
| Por resultado | Tú, casi todo | Solo si puedes medir el resultado y controlas las variables |

## Definición formal

Sea `D_lab` el número de días laborables netos del año (de lunes a viernes, sin festivos ni
vacaciones: del orden de 220-230 en España) y `D_nof` los días laborables que no facturas
(formación, propuestas, administración, bajas, tiempo comercial). Las horas que puedes vender en
un año son:

:::formula
H_fact = (D_lab − D_nof) · h_día
:::

- `D_lab` — días laborables del año, de lunes a viernes y descontando festivos y vacaciones.
- `D_nof` — días laborables que no facturas: formación, propuestas, administración, comercial.
- `h_día` — horas de trabajo de cliente en un día laborable, descontando correo, reuniones
  internas y descansos. Es realista contar 6 o 7,5, no 8.
- `H_fact` — techo realista de horas vendibles en el año.

La **tarifa mínima** que cubre tus costes y tu objetivo:

:::formula
Tarifa = (Objetivo_anual + Costes_fijos) / H_fact
:::

- `Objetivo_anual` — lo que quieres ingresar antes de impuestos, el equivalente al salario bruto
  que te pondrías.
- `Costes_fijos` — cuota de autónomos, gestoría, seguros, software, equipo, formación. Los pagas
  tú, así que van en el numerador; no salen del margen.
- La tarifa que sale es un **mínimo**, no un precio. El IVA que cobras no es tuyo y los impuestos
  sobre el beneficio salen de ahí.

El **precio a precio fijo** añade un colchón por incertidumbre:

:::formula
Precio = Horas_estimadas · Tarifa · (1 + colchón)
:::

- `Horas_estimadas` — suma de horas del alcance, contadas por ti y desglosadas por entregable.
- `colchón` — fracción entre 0,15 y 0,30 cuando los requisitos no están cerrados. Cubre
  reestimaciones y aclaraciones, no cambios de alcance.
- **Cambio de alcance** — cualquier entregable, dato, informe, integración o reunión que no
  aparezca en el anexo firmado. Se factura aparte como `horas_extra · Tarifa`, o se descuenta de
  la bolsa de horas pactada (por ejemplo, 15 horas).

## Ejemplo

Consultoría de tres meses para una empresa de logística:

- Alcance cerrado: 40 h de descubrimiento y definición de métricas, 60 h de construcción de dos
  procesos de ingesta y 20 h de formación a dos personas. Total: 120 h.
- Tarifa: 80 €/h. Trabajo estimado: 120 · 80 = 9.600 €.
- Se firma a precio fijo con un colchón del 25 %: 120 · 1,25 = 150 h, es decir **12.000 €**. Ese
  precio aguanta hasta 150 horas reales; a partir de ahí, cada hora la pagas tú.
- Durante el proyecto el cliente añade un tercer proceso (22 h) y cambia el destino del informe
  (12 h). Son 34 horas extra.

Con cláusula de cambios, esas 34 h se facturan a 80 €/h: 34 · 80 = 2.720 €. Total facturado
14.720 € por 154 h reales, que son **95,58 €/h efectivos**.

Sin cláusula, el cliente paga 12.000 € por esas mismas 154 h: **77,92 €/h**. Has trabajado un
28 % más de lo previsto y has cobrado un 2,6 % menos por hora. Si el proyecto acaba en 190 h,
tras dos rondas más de cambios, la tarifa efectiva cae a **63,16 €/h**, un 21 % por debajo de tu
objetivo, y ese margen ya no se recupera.

## Código

```python verificable
# Tarifa minima: los dias que de verdad puedes facturar no son los laborables.
dias_laborables = 220        # laborables netos: sin festivos ni vacaciones
dias_no_facturables = 55     # formacion, propuestas, administracion, comercial
horas_dia = 7.5              # de 8 horas, media se va en correo y reuniones internas
horas_facturables = (dias_laborables - dias_no_facturables) * horas_dia
objetivo_neto = 45000        # lo que quieres llevarte antes de impuestos
costes_fijos = 12000         # cuota, gestoria, seguros, software, equipo
tarifa = (objetivo_neto + costes_fijos) / horas_facturables

print(f"dias facturables   {dias_laborables - dias_no_facturables}")  # -> 165
print(f"horas facturables  {horas_facturables:.0f}")                 # -> 1238
print(f"tarifa minima      {tarifa:.2f} EUR/h")                      # -> 46.06 EUR/h
```

```python verificable
# Precio fijo: la tarifa que cobras de verdad baja con cada hora extra.
estimacion_horas = 120
precio_cerrado = 12000       # sale a 100 EUR/h si el alcance no se mueve
objetivo = 80                # por debajo de esto el proyecto no compensa

print(f"tarifa con el alcance previsto {precio_cerrado / estimacion_horas:.2f} EUR/h")  # -> 100.00 EUR/h
print(f"horas maximas antes del limite {precio_cerrado / objetivo:.0f} h")             # -> 150 h
for h in (120, 138, 154, 190):
    # 154 h son las del ejemplo: dos rondas de cambios sobre la estimacion
    print(f"  {h:>3} h facturadas  tarifa real {precio_cerrado / h:>6.2f} EUR/h")
```

## Errores típicos

- **Calcular la tarifa dividiendo el sueldo que quieres entre 1.760 horas.** Con un objetivo de
  45.000 € sale 25,57 €/h; con los costes fijos incluidos y los días que realmente facturas, la
  cuenta del bloque anterior da 46,06 €/h. Es un 80 % más, y esa diferencia es la que decide si
  el año acaba con beneficio o trabajando gratis.
- **Firmar a precio fijo sin colchón ni cláusula de cambios.** El precio fijo no es un descuento
  por confianza: es un seguro que tú vendes, y se cobra. Si no pones colchón, el primer imprevisto
  se come el beneficio; si no pones cláusula, el tercer cambio te deja trabajando gratis.
- **Definir el final del trabajo de palabra.** «Cuando el informe esté bien» no es un criterio:
  sin una definición escrita, el entregable se queda en «casi» para siempre. Escribe qué se
  entrega, en qué formato y cuántos días laborables tiene el cliente para objetar, con el mismo
  rigor con el que se escribe una [[documentacion-tecnica|documentación técnica]].
- **Cobrar todo al terminar o, peor, a los 60 días de facturar.** Un 30 % a la firma, pagos por
  hito y una última factura al entregar convierten una posible discusión judicial en una
  conversación. Tú no eres el banco del cliente.
- **Confundir facturación con beneficio.** El IVA no es tuyo, la retención de IRPF se ingresa y
  los costes fijos siguen corriendo los meses sin proyecto. Un mes de 8.000 € facturados puede
  dejar menos en el bolsillo que uno de 5.000 € con menos gastos.
- **Vender solo horas cuando el resultado vale mucho más.** Cobrar 46 €/h por un modelo que ahorra
  200.000 € al año al cliente es dejar dinero encima de la mesa y, además, incentivar que el
  proyecto se alargue. Si puedes medir el ahorro, cobra por él, con un suelo y un techo pactados;
  si no puedes medirlo, no lo prometas, porque eso ya es vender humo ([[etica-profesional]]).

:::practica
enunciado: Un cliente te pide un modelo de previsión de demanda. Estimas 90 horas a 75 €/h, quieres un colchón del 20 % y acuerdas una bolsa de 15 horas para cambios a la misma tarifa. Al cabo de tres meses has dedicado 118 horas y el cliente ha consumido las 15 horas de bolsa. Calcula el total facturado y la tarifa efectiva por hora.
pista: El colchón se aplica a las horas estimadas para fijar el precio; la bolsa se factura aparte y solo si se consume.
solucion: Precio base = 90 · 1,20 = 108 h · 75 €/h = 8.100 €. Bolsa consumida = 15 · 75 = 1.125 €. Total facturado = 9.225 €. Horas reales = 118, así que la tarifa efectiva es 9.225 / 118 = 78,18 €/h, todavía por encima de los 75 €/h de partida. La lección está en la última línea: la bolsa ya está agotada y quedan horas de trabajo por hacer; a partir de aquí todo lo que pidan se factura como cambio nuevo o el proyecto entra en pérdidas.
:::

## Comprueba que lo sabes

:::quiz
p: Quieres ganar 45.000 € al año, tienes 12.000 € de costes fijos y calculas 1.238 horas facturables. ¿Qué tarifa mínima por hora necesitas?
o: 36,35 €/h, dividiendo el objetivo entre las horas facturables
o: 46,06 €/h, sumando objetivo y costes antes de dividir
o: 25,57 €/h, dividiendo el objetivo entre las 1.760 horas del año
a: 2
e: Los costes fijos los pagas tú, así que van en el numerador: (45.000 + 12.000) / 1.237,5 = 46,06 €/h. Dividir solo el objetivo deja 12.000 € sin cubrir, y dividir entre 1.760 horas usa días que no facturas: formación, propuestas que no se cobran, administración y bajas.
:::

:::quiz
p: Firmas a precio fijo 12.000 € una estimación de 120 h a 100 €/h. El cliente añade trabajo y acabas dedicando 150 h. ¿Qué ha pasado?
o: Nada, porque el cliente paga la cantidad pactada
o: Que tu tarifa real baja a 80 €/h y has regalado 30 horas
o: Que tu tarifa sube, porque has trabajado más horas
a: 2
e: A precio fijo el riesgo de las horas extra lo asumes tú: 12.000 / 150 = 80 €/h. Sin cláusula de cambios, cada hora añadida sale de tu margen, no del presupuesto del cliente. La opción 3 describe el modelo por horas, no el precio fijo.
:::

:::quiz
p: ¿Para qué sirve un criterio de aceptación por escrito?
o: Para fijar el precio antes de conocer el alcance
o: Para decidir cuándo el entregable está terminado y cuánto tiempo tiene el cliente para objetar
o: Para impedir que el cliente pida cambios durante el proyecto
a: 2
e: El criterio de aceptación define el final: qué se entrega, con qué formato y con cuántos días laborables para reclamar por escrito. No impide cambios, los convierte en algo que se puede facturar; y no tiene nada que ver con fijar el precio, que se decide antes.
:::

:::trampa
«Solo una cosita más» repetido seis veces es un proyecto distinto. La primera vez se acepta con
una frase: «eso entra en la bolsa de horas, te confirmo cuánto consume». Si no hay bolsa, se
manda un presupuesto pequeño el mismo día. Lo que hunde a los freelances no es el cliente
abusivo, es el cambio pequeño que nunca se factura porque da vergüenza pedirlo.
:::
