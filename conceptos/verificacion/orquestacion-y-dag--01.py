from collections import deque

# Un DAG pequeno: duracion en minutos y predecesoras de cada tarea.
tareas = {
    "extraer_clientes": (12, []),
    "limpiar_clientes": (4, ["extraer_clientes"]),
    "cargar_dimension": (3, ["limpiar_clientes"]),
    "extraer_pedidos": (35, []),
    "limpiar_pedidos": (8, ["extraer_pedidos"]),
    "cargar_hechos": (6, ["cargar_dimension", "limpiar_pedidos"]),
    "validar_totales": (2, ["cargar_hechos"]),
}

grados = {t: len(pre) for t, (_, pre) in tareas.items()}
siguientes = {t: [] for t in tareas}
for t, (_, pre) in tareas.items():
    for p in pre:
        siguientes[p].append(t)

# Orden topologico: solo se encola una tarea cuando no le queda ninguna predecesora pendiente.
cola = deque(sorted(t for t, g in grados.items() if g == 0))
orden = []
while cola:
    t = cola.popleft()
    orden.append(t)
    for s in sorted(siguientes[t]):
        grados[s] -= 1
        if grados[s] == 0:
            cola.append(s)

inicio, fin = {}, {}
for t in orden:                       # el orden topologico garantiza que las predecesoras ya estan
    pre = tareas[t][1]
    inicio[t] = max((fin[p] for p in pre), default=0)
    fin[t] = inicio[t] + tareas[t][0]
    print(f"{t:<18} inicio {inicio[t]:>3}  fin {fin[t]:>3}")

print("tareas ordenadas:", len(orden))                                    # -> tareas ordenadas: 7
print("duracion sumando todo:", sum(d for d, _ in tareas.values()))       # -> duracion sumando todo: 70
print("duracion del DAG:", max(fin.values()))                             # -> duracion del DAG: 51
