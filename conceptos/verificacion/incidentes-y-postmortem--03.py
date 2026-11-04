# Registro de acciones de un postmortem: con dueño, con fecha y sin cierres regalados.
acciones = [
    {"id": 1, "que": "revertir el ultimo despliegue antes de depurar", "dueno": "ana", "abierta": 4},
    {"id": 2, "que": "alerta de tasa de error en la pasarela",          "dueno": "luis", "abierta": 12},
    {"id": 3, "que": "boton de revertir en el primer nivel del panel",  "dueno": "ana", "abierta": 45},
]

def estado(a, limite=30):
    # Una accion sin cerrar no se queda abierta para siempre: caduca.
    if not a["abierta"]:
        return "cerrada"
    return "caducada: reprogramar o borrar" if a["abierta"] > limite else "abierta"

abiertas = [a for a in acciones if not a["abierta"]]
# any() se para en el primer True: sirve para preguntar "¿hay alguna...?" sin recorrer todo.
sin_dueno = any(not a["dueno"] for a in acciones)

print("acciones totales:", len(acciones))          # -> 3
print("cerradas:", len(abiertas))                  # -> 0
print("hay acciones sin dueno:", sin_dueno)        # -> False
for a in acciones:
    print(f"  #{a['id']} {estado(a):32} {a['que']}")
# -> el #3 sale "caducada: reprogramar o borrar": 45 dias sin cerrar no es una accion, es una
#    intencion. Se reprograma con una fecha nueva o se borra y se dice en voz alta.
