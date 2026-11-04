# La misma deteccion, con la arista prohibida y envuelta en una funcion para poder repetirla
def componentes_fuertemente_conexas(grafo):
    """Devuelve las CFC del grafo, de hojas a raices (Tarjan iterativo)."""
    indice, pila, en_pila, salida = 0, [], set(), []
    orden, bajo, visto = {}, {}, set()
    for origen in grafo:
        if origen in visto:
            continue
        trabajo = [(origen, 0)]
        while trabajo:
            nodo, siguiente = trabajo.pop()
            if siguiente == 0:
                visto.add(nodo)
                orden[nodo] = bajo[nodo] = indice
                indice += 1
                pila.append(nodo)
                en_pila.add(nodo)
            hijos = grafo[nodo]
            if siguiente < len(hijos):
                trabajo.append((nodo, siguiente + 1))
                hijo = hijos[siguiente]
                if hijo not in visto:
                    trabajo.append((hijo, 0))
                elif hijo in en_pila:
                    bajo[nodo] = min(bajo[nodo], orden[hijo])
            else:
                if bajo[nodo] == orden[nodo]:
                    componente = []
                    while True:
                        salido = pila.pop()
                        en_pila.discard(salido)
                        componente.append(salido)
                        if salido == nodo:
                            break
                    salida.append(sorted(componente))
    return salida

sano = {
    "dominio": [],
    "informe": ["dominio"],
    "adaptador": ["dominio"],
    "servicio": ["dominio", "informe"],
    "composicion": ["servicio", "adaptador"],
}
enfermo = dict(sano, dominio=["adaptador"])    # el dominio reutiliza el cliente de la base de datos

for nombre, grafo in (("sano", sano), ("con la arista prohibida", enfermo)):
    componentes = sorted(componentes_fuertemente_conexas(grafo), key=len)
    ciclos = [c for c in componentes if len(c) > 1]
    print(f"{nombre}: {len(ciclos)} ciclo(s) -> {ciclos}")
# -> sano: 0 ciclo(s) -> []
# -> con la arista prohibida: 1 ciclo(s) -> [['adaptador', 'dominio']]
print("el ciclo arrastra a:", sorted({modulo for ciclo in ciclos for modulo in ciclo}))
# -> el ciclo arrastra a: ['adaptador', 'dominio']
