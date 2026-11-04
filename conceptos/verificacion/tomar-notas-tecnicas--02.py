import doctest

# Una nota con el ejemplo en formato doctest se comprueba sola: si el resultado del ejemplo
# cambia, `python -m doctest nota.md` avisa antes de que te fies de ella.
nota = """>>> import json
>>> json.loads('{"filas": 3}')["filas"]
3"""

prueba = doctest.DocTestParser().get_doctest(nota, {}, "nota", "nota.md", 0)
resultado = doctest.DocTestRunner(verbose=False).run(prueba)
print("comprobaciones:", resultado.attempted, "  fallos:", resultado.failed)
