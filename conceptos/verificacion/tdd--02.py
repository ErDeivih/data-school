from datetime import date

# Inyectar la dependencia hace el codigo comprobable sin red, sin reloj real y sin base de datos.
class RelojFijo:
    def __init__(self, dia):
        self._dia = dia                 # el guion bajo es solo una convencion: "no lo toques"
    def hoy(self):
        return self._dia                # siempre el mismo dia: la prueba es determinista

def es_fin_de_semana(reloj):
    # weekday() cuenta desde 0 el lunes: sabado es 5 y domingo 6, de ahi el >= 5.
    return reloj.hoy().weekday() >= 5

# La funcion no llama a date.today(): recibe el dia desde fuera, y eso la hace testeable.
print(es_fin_de_semana(RelojFijo(date(2024, 3, 9))))     # -> True
print(es_fin_de_semana(RelojFijo(date(2024, 3, 11))))    # -> False
