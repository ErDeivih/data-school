# P17 · De la API de F1 a una tabla que no se duplica

**Estado:** hecho el 2026-11-02 con **datos reales** de OpenF1. Sin clave, sin suscripción.

## La pregunta

¿Puedo ingerir vueltas reales de tres carreras y dejar una tabla que, al reejecutarse, no duplique
ni pierda nada?

## La fuente

**OpenF1** (`https://api.openf1.org/v1`), API gratuita y sin clave. Tres carreras de 2024:
Sakhir, Jeddah y Melbourne. Se descargan sesiones, pilotos y vueltas; el bruto se guarda con la
fecha de descarga.

## Cómo se ejecuta

```sh
python ingerir.py     # descarga y escribe data/vueltas.csv
python verificar.py   # 8 comprobaciones
python degradacion.py # cruza stints y vueltas: 155 stints con su pendiente
```

## Resultado real

| Carrera | Pilotos | Vueltas | Mejor vuelta |
| --- | --- | --- | --- |
| Sakhir | 20 | 1.129 | 92,608 s (piloto 1) |
| Jeddah | 20 | 902 | 91,632 s (piloto 16) |
| Melbourne | 19 | 998 | 79,813 s (piloto 16) |

**3.029 vueltas únicas**, 59 pares sesión-piloto, 6 vueltas sin duración (salidas de box y
banderas) y cero duplicados. El verificador comprueba además que todas las duraciones superan los
30 segundos y que el bruto está guardado.

## Decisiones y por qué

- **Clave de idempotencia `(sesión, piloto, vuelta)`.** Es la identidad real de una vuelta: si la
  API devuelve una repetida, se descarta; si se relanza la ingesta, el resultado es el mismo.
- **Bruto con fecha en el nombre.** Si OpenF1 cambia un campo, el fichero viejo permite comparar.
- **Sin dependencias.** `urllib` y `csv`: funciona en cualquier máquina sin `pip install`.
- **Reintentos con espera creciente.** La API limita peticiones y un reintento ciego empeora.
- **Las vueltas sin duración se conservan.** No son errores: son salidas de box o vueltas
  invalidadas. Borrarlas sin decirlo falsearía el recuento.

## Límites

- Tres carreras no son una temporada. El histórico de OpenF1 empieza en 2023.
- La API no trae el compuesto de neumático en vueltas: para estrategia hay que cruzar con
  `stints` o usar FastF1 (que desde la 3.9 pide F1TV Access).
- No hay orquestación: es un script que se ejecuta a mano.

## Degradación por compuesto (y el detalle que importa)

`degradacion.py` cruza `stints` con vueltas y calcula la pendiente de cada tramo. Salen **155
stints** y las pendientes son negativas: HARD −0,226, MEDIUM −0,319, SOFT −0,147 s/vuelta.

No es un error del cálculo: el coche se aligera de combustible más rápido de lo que el neumático se
degrada en tramos cortos. Para aislar la degradación real hay que corregir por combustible (o
comparar la misma vuelta del stint entre pilotos). Ese detalle es la mitad del proyecto de
estrategia y está explicado en `docs/integracion/10-F1-PREDICCION.md`.

## Lo que falta para portfolio

1. Orquestarlo (Dagster o Airflow) con ejecución diaria durante una temporada.
2. Cruzar con `stints` y `pit` para calcular degradación por compuesto.
3. Panel con la evolución de posiciones por vuelta.

## Qué se aprende

`idempotencia-y-reintentos`, `ingesta-incremental-y-cdc`, `contratos-de-datos` y, en la parte de
análisis, `series-temporales-componentes` y `visualizacion-honesta`.
