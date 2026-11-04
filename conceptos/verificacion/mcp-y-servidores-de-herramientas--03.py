# La cuenta que justifica el protocolo: conectores con y sin acuerdo comun.
def sin_protocolo(M, N):
    return M * N            # un conector por cada pareja aplicacion-sistema

def con_mcp(M, N):
    # un cliente por aplicacion, un servidor por sistema; el protocolo es compartido
    return M + N

for M, N in ((3, 3), (5, 8), (10, 20)):
    print(f"{M:2d} aplicaciones y {N:2d} sistemas -> "
          f"{sin_protocolo(M, N):4d} conectores sin protocolo, {con_mcp(M, N):3d} con MCP")
# ->  3 aplicaciones y  3 sistemas ->    9 conectores sin protocolo,   6 con MCP
# ->  5 aplicaciones y  8 sistemas ->   40 conectores sin protocolo,  13 con MCP
# -> 10 aplicaciones y 20 sistemas ->  200 conectores sin protocolo,  30 con MCP

# El ahorro no es un factor fijo: crece con el tamano del sistema.
for M, N in ((3, 3), (5, 8), (10, 20)):
    print(f"{M:2d}x{N:2d}: {sin_protocolo(M, N) / con_mcp(M, N):.1f} veces menos piezas")
# ->  3x 3: 1.5 veces menos piezas
# ->  5x 8: 3.1 veces menos piezas
# -> 10x20: 6.7 veces menos piezas
