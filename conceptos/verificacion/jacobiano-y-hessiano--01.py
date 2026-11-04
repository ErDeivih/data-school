import numpy as np

# f(x, y) = 3x^2*y + y^3 : hessiano analítico y comprobación numérica por diferencias.
# El punto (1, 2) NO es crítico (su gradiente es (12, 15)), así que este hessiano mide la
# curvatura en ese punto: para hablar de mínimos hay que evaluarlo donde el gradiente se anule.
def f(v):
    x, y = v
    return 3 * x**2 * y + y**3

def hessiano_numerico(v, h=1e-4):
    x, y = v
    fxx = (f([x + h, y]) - 2 * f([x, y]) + f([x - h, y])) / h**2
    fyy = (f([x, y + h]) - 2 * f([x, y]) + f([x, y - h])) / h**2
    fxy = (f([x + h, y + h]) - f([x + h, y - h]) - f([x - h, y + h]) + f([x - h, y - h])) / (4 * h**2)
    return np.array([[fxx, fxy], [fxy, fyy]])

H = hessiano_numerico([1.0, 2.0])
print("hessiano en (1,2)  ", np.round(H, 3).tolist())          # salida: [[12.0, 6.0], [6.0, 12.0]]
print("autovalores        ", np.round(np.linalg.eigvalsh(H), 3))  # salida: [ 6. 18.]
print("menores principales", round(H[0, 0], 3), round(float(np.linalg.det(H)), 3))  # salida: 12.0 108.0
