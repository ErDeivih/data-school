# Cuantos pods hacen falta y cuanta capacidad queda si cae un nodo.
pico_rps = 1800          # peticiones por segundo en la hora punta
capacidad_pod = 250      # rps que sostiene un pod con sus requests actuales
nodos = 3
pods_por_nodo = 4        # limite de colocacion por nodo (CPU o memoria)

pods = -(-pico_rps // capacidad_pod)              # division hacia arriba
capacidad_n1 = (nodos - 1) * pods_por_nodo * capacidad_pod

print("pods para el pico:", pods)                 # -> 8
print("rps con un nodo caido:", capacidad_n1)     # -> 2000
print("aguanta el pico con N+1:", capacidad_n1 >= pico_rps)  # -> True
