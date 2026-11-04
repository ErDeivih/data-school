import time

datos = list(range(1_000_000))          # sin numpy: queremos un recorrido lineal de verdad
valores = list(range(0, 1_000_000, 20_000))   # 50 consultas

inicio = time.perf_counter()
# `v in datos` sobre una lista recorre posiciones hasta encontrar v: O(n) por consulta.
en_lista = sum(1 for v in valores if v in datos)
t_lista = time.perf_counter() - inicio

# Convertir a conjunto cuesta un recorrido completo (O(n))... una vez.
conjunto = set(datos)
inicio = time.perf_counter()
# ...que se paga con creces: la pertenencia en un conjunto es O(1) por consulta.
en_conjunto = sum(1 for v in valores if v in conjunto)
t_conjunto = time.perf_counter() - inicio

print("encontrados:", en_lista, "y", en_conjunto)     # -> 50 y 50 (las dos formas coinciden)
print(f"buscar en la lista   {t_lista * 1000:8.1f} ms")
print(f"buscar en el conjunto {t_conjunto * 1000:7.3f} ms")
# max() evita dividir entre cero: con una lista diminuta el conjunto puede tardar 0.0 ms.
print("mejora:", round(t_lista / max(t_conjunto, 1e-9)), "x  (O(n) frente a O(1))")
