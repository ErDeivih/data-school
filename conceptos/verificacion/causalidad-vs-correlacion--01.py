# Paradoja de Simpson: dentro de cada dispositivo la funcion reduce las bajas,
# pero en el total parece aumentarlas porque se uso mucho mas en movil.
print(f"movil      sin funcion {26/100:.1%}  con funcion {50/200:.1%}")
print(f"escritorio sin funcion {66/600:.1%}  con funcion {10/100:.1%}")
print(f"total      sin funcion {92/700:.1%}  con funcion {60/300:.1%}")
# -> movil      sin funcion 26.0%  con funcion 25.0%
# -> escritorio sin funcion 11.0%  con funcion 10.0%
# -> total      sin funcion 13.1%  con funcion 20.0%
