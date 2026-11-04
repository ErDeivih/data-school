# b = a NO copia: los dos nombres apuntan a la misma lista
a = [1, 2, 3]
b = a
b.append(4)
print("a tras b.append(4):", a)   # -> a tras b.append(4): [1, 2, 3, 4]

# [:] si crea una lista nueva (copia superficial, un solo nivel)
c = a[:]
c.append(5)
print("a tras c.append(5):", a)   # -> a tras c.append(5): [1, 2, 3, 4]
print("c:", c)                    # -> c: [1, 2, 3, 4, 5]
