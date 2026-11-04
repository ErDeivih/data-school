def contraste(rgb1, rgb2):
    """Cociente de contraste WCAG entre dos colores RGB (0-255)."""
    def lineal(v):
        v = v / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4   # gamma del estandar

    def luminancia(c):
        return 0.2126 * lineal(c[0]) + 0.7152 * lineal(c[1]) + 0.0722 * lineal(c[2])   # el verde pesa mas

    claro, oscuro = sorted([luminancia(rgb1), luminancia(rgb2)], reverse=True)   # el mas claro primero
    return (claro + 0.05) / (oscuro + 0.05)      # el +0.05 evita el cociente infinito del negro puro

casos = {
    "gris #767676": ((118, 118, 118), (255, 255, 255)),
    "gris #999999": ((153, 153, 153), (255, 255, 255)),
    "azul #0057b8": ((0, 87, 184), (255, 255, 255)),
}
for nombre, (frente, fondo) in casos.items():    # cada valor es una tupla con los dos colores
    r = contraste(frente, fondo)
    print(f"{nombre} sobre blanco: {r:.2f}:1  AA normal: {'si' if r >= 4.5 else 'no'}")   # umbral 4,5:1
