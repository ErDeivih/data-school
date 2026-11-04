# Las etapas del ciclo de vida, aplicadas a pedidos que van avanzando de estado
from datetime import date

HOY = date(2026, 3, 1)
RETENCION_DIAS = 365 * 5           # obligacion fiscal: cinco anios
ARCHIVO_DIAS = 365 * 2             # a partir de dos anios, almacenamiento frio

def etapa(alta, hoy=HOY, retencion=RETENCION_DIAS, archivo=ARCHIVO_DIAS):
    dias = (hoy - alta).days
    if dias > retencion:
        return "borrado"
    if dias > archivo:
        return "archivado"
    if dias > 1:
        return "servicio"
    return "captura"

pedidos = [("P-1", date(2026, 2, 28)), ("P-2", date(2025, 6, 1)),
           ("P-3", date(2023, 1, 10)), ("P-4", date(2020, 1, 15))]

for pid, alta in pedidos:
    print(f"{pid}: {(HOY - alta).days:>5} dias -> {etapa(alta)}")
