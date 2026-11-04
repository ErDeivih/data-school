import bisect

# Con valores repetidos, "encontrar x" no basta: hacen falta las dos fronteras.
a = [0, 0, 0, 0, 1, 1, 1, 2, 5]
print("primera posicion del 1:", bisect.bisect_left(a, 1))    # -> primera posicion del 1: 4
print("tras el ultimo 1:    ", bisect.bisect_right(a, 1))     # -> tras el ultimo 1:     7

# El bloque entero de unos se saca restando las dos fronteras.
print("cuantos unos hay:", bisect.bisect_right(a, 1) - bisect.bisect_left(a, 1))  # -> cuantos unos hay: 3

# Si el valor no esta, las dos fronteras coinciden: es el punto de insercion.
print("donde iria el 3:", bisect.bisect_left(a, 3))           # -> donde iria el 3: 8
print("y el 9:", bisect.bisect_left(a, 9))                    # -> y el 9: 9
