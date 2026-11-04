from datetime import datetime, timedelta

def t(hhmmss):
    return datetime(2024, 3, 1, *map(int, hhmmss.split(":")))

RETRASO = timedelta(minutes=2)    # d: cuanto esperamos antes de cerrar una ventana
TARDANZA = timedelta(minutes=3)   # a: cuanto seguimos aceptando eventos tardios

# (t_evento, t_proceso, id), en el orden en que el flujo los entrega.
eventos = [(t("10:00:30"), t("10:00:31"), "e1"),
           (t("10:01:10"), t("10:01:12"), "e2"),
           (t("10:02:05"), t("10:02:06"), "e4"),
           (t("10:00:45"), t("10:04:20"), "e3"),
           (t("10:01:50"), t("10:06:40"), "e5"),
           (t("10:08:00"), t("10:08:01"), "e6"),
           (t("10:00:10"), t("10:09:00"), "e7")]

ventanas, descartados = {}, []
max_evento, marca = None, None

for te, tp, ident in eventos:
    max_evento = te if max_evento is None else max(max_evento, te)
    nueva = max_evento - RETRASO
    marca = nueva if marca is None else max(marca, nueva)   # la marca nunca retrocede

    inicio = te.replace(second=0, microsecond=0)
    if te < marca and marca > inicio + timedelta(minutes=1) + TARDANZA:
        descartados.append(ident)
    else:
        ventanas.setdefault(inicio, []).append(ident)

for inicio in sorted(ventanas):
    fin = inicio + timedelta(minutes=1)
    print(f"[{inicio:%H:%M}, {fin:%H:%M}) -> {len(ventanas[inicio])} eventos")

print("marca de agua final:", f"{marca:%H:%M:%S}")   # -> marca de agua final: 10:06:00
print("descartados:", descartados)                  # -> descartados: ['e7']
