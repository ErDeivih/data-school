# Descenso de gradiente sobre f(x) = x^2 - 4x + 1, minimo en x = 2.
def f(x):
    return x**2 - 4*x + 1


def grad(x):
    return 2*x - 4


x, paso = 0.0, 0.3
for iteracion in range(1, 21):
    x = x - paso * grad(x)
    if iteracion in (1, 2, 5, 20):
        print("paso {:>2}: x = {:+.6f}  f(x) = {:+.6f}".format(iteracion, x, f(x)))

print("optimo teorico: x = 2, f(x) = -3")
# el paso 20 imprime: paso 20: x = +2.000000  f(x) = -3.000000
