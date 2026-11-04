import unittest

def precio_con_iva(base, tipo=0.21):
    return round(base * (1 + tipo), 2)

class TestPrecio(unittest.TestCase):
    # Metodos que empiezan por test_: el cargador los encuentra por convencion, sin registro.
    def test_iva_general(self):
        self.assertEqual(precio_con_iva(100), 121.0)
    def test_tipo_reducido(self):
        self.assertEqual(precio_con_iva(100, 0.10), 110.0)
    def test_redondeo_a_dos_decimales(self):
        # 9.99 · 1.21 = 12.0879: sin el round serian 12.09 solo por como imprime Python.
        self.assertEqual(precio_con_iva(9.99), 12.09)

# Carga y ejecuta la clase entera en una linea; verbosity=0 evita el ruido de cada punto.
resultado = unittest.TextTestRunner(verbosity=0).run(
    unittest.defaultTestLoader.loadTestsFromTestCase(TestPrecio))

# Tres comprobaciones sin base de datos, sin red y sin reloj: milisegundos.
print("pruebas ejecutadas:", resultado.testsRun)   # -> 3
print("fallos:", len(resultado.failures))          # -> 0
