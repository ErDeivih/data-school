# Detectar el ciclo: componentes fuertemente conexas (algoritmo de Tarjan, iterativo)
dependencias = {
    "dominio": [],
    "informe": ["dominio"],
    "adaptador": ["dominio"],
    "servicio": ["dominio", "informe"],
    "composicion": ["servicio", "adaptador", "informe"],
}

indice, pila, en_pila, componentes = 0, [], set(), []
orden, bajo, visto = {}, {}, set()

for origen in dependencias:
    if origen in visto:
        continue
    trabajo = [(origen, 0)]
    while trabajo:
        nodo, siguiente = trabajo.pop()
        if siguiente == 0:                     # primera vez que se visita el nodo
            visto.add(nodo)
            orden[nodo] = bajo[nodo] = indice
            indice += 1
            pila.append(nodo)
            en_pila.add(nodo)
        hijos = dependencias[nodo]
        if siguiente < len(hijos):
            trabajo.append((nodo, siguiente + 1))
            hijo = hijos[siguiente]
            if hijo not in visto:
                trabajo.append((hijo, 0))       # se visita al hijo y se vuelve a este nodo
            elif hijo in en_pila:
                bajo[nodo] = min(bajo[nodo], orden[hijo])
        else:                                   # el nodo ya no tiene hijos pendientes
            if bajo[nodo] == orden[nodo]:
                componente = []
                while True:
                    salido = pila.pop()
                    en_pila.discard(salido)
                    componente.append(salido)
                    if salido == nodo:
                        break
                componentes.append(sorted(componente))
print("componentes (de hojas a raices):", componentes)
# -> componentes (de hojas a raices): [['dominio'], ['informe'], ['adaptador'], ['servicio'], ['composicion']]
ciclos = [c for c in componentes if len(c) > 1]
print("ciclos:", len(ciclos), " - modulos aislados:", sum(len(c) == 1 for c in componentes))
# -> ciclos: 0  - modulos aislados: 5
