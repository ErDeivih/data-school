# Nueve operaciones con su hora, precio y volumen: los datos de partida.
horas = ["09:00:01", "09:00:03", "09:00:12", "09:00:45", "09:01:05",
         "09:01:41", "09:02:00", "09:02:19", "09:02:55"]
precios = [100.00, 100.02, 99.98, 100.01, 100.05, 100.03, 100.07, 100.04, 100.09]
volumenes = [120, 340, 80, 500, 220, 75, 640, 90, 310]

# Agregar por minuto: el primero y el ultimo precio dan apertura y cierre,
# y el numero de operaciones se pierde al sumar.
velas = {}
for hora, precio, volumen in zip(horas, precios, volumenes):
    minuto = hora[:5]
    v = velas.setdefault(minuto, {"apertura": precio, "maximo": precio,
                                  "minimo": precio, "cierre": precio,
                                  "volumen": 0, "operaciones": 0})
    v["maximo"] = max(v["maximo"], precio)
    v["minimo"] = min(v["minimo"], precio)
    v["cierre"] = precio
    v["volumen"] += volumen
    v["operaciones"] += 1

print("minuto  apertura  maximo  minimo  cierre  volumen")
for minuto in sorted(velas):
    v = velas[minuto]
    print(f"{minuto}  {v['apertura']:8.2f}  {v['maximo']:6.2f}  "
          f"{v['minimo']:6.2f}  {v['cierre']:6.2f}  {v['volumen']:7d}")
# -> 09:00    100.00  100.02   99.98  100.01     1040
# -> 09:01    100.05  100.05  100.03  100.03      295
# -> 09:02    100.07  100.09  100.04  100.09     1040
print("operaciones agregadas:", len(horas),
      "volumen total:", sum(v["volumen"] for v in velas.values()))
# -> operaciones agregadas: 9 volumen total: 2375
