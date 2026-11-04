import ast

# Lo que la maquina puede cazar sola: asi el ojo humano se gasta en otra cosa.
# El codigo a revisar va como texto dentro de la cadena: no se ejecuta, solo se analiza.
CODIGO = '''
def anade(item, lista=[]):
    lista.append(item)
    return lista

def lee(ruta):
    try:
        return open(ruta).read()
    except:
        return None
'''

def avisos(fuente):
    encontrados = []
    # ast.parse construye el arbol de sintaxis; walk lo recorre entero, en cualquier orden.
    for nodo in ast.walk(ast.parse(fuente)):
        if isinstance(nodo, ast.FunctionDef):
            # args.defaults son solo los valores por defecto de los parametros.
            for defecto in nodo.args.defaults:
                # List, Dict y Set se crean UNA vez, al definir la funcion, y se comparten.
                if isinstance(defecto, (ast.List, ast.Dict, ast.Set)):
                    encontrados.append(f"linea {nodo.lineno}: argumento por defecto mutable en {nodo.name}")
        # Un except sin tipo es ExceptHandler con type None: se traga cualquier error.
        if isinstance(nodo, ast.ExceptHandler) and nodo.type is None:
            encontrados.append(f"linea {nodo.lineno}: except sin tipo de excepcion")
    return encontrados

for aviso in avisos(CODIGO):
    print(aviso)
# Se vuelve a analizar la cadena entera: la funcion no guarda nada entre llamadas.
print("avisos:", len(avisos(CODIGO)))     # -> 2
