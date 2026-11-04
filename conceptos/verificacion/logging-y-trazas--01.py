import io
import json
import logging

class FormatoJSON(logging.Formatter):
    """Registro estructurado: mensaje fijo y datos variables en campos aparte."""
    def format(self, record):
        # Formatter se hereda y se sobrescribe format(): cada linea sale como un JSON de una
        # sola linea. Lo que devuelvas aqui es lo que acaba escrito, tal cual.
        return json.dumps({
            "nivel": record.levelname,                  # el nombre del nivel, no el numero
            "logger": record.name,                      # el nombre que se le dio en getLogger
            "mensaje": record.getMessage(),             # interpola el mensaje con sus argumentos
            # getattr con valor por defecto: casi todos los registros no traen "campos", y
            # record.campos directo lanzaria AttributeError; aqui sale un diccionario vacio.
            "campos": getattr(record, "campos", {}),
        }, ensure_ascii=False, sort_keys=True)           # sin escapar tildes y claves ordenadas

flujo = io.StringIO()                          # en produccion, la salida estandar del proceso
manejador = logging.StreamHandler(flujo)       # el "handler" decide DONDE se escribe
manejador.setFormatter(FormatoJSON())          # y el formatter, CON QUE FORMA

logger = logging.getLogger("pagos")            # getLogger devuelve siempre el mismo objeto
logger.setLevel(logging.INFO)                  # por debajo de INFO, el registro ni se crea
logger.propagate = False                       # que no se duplique por el logger raiz
logger.handlers = [manejador]                  # asignar la lista BORRA los handlers heredados

logger.info("cobro aceptado", extra={"campos": {"pedido": 8412, "importe": 19.99}})
logger.warning("reintento de pasarela", extra={"campos": {"pedido": 8412, "intento": 2}})
logger.debug("esta no se escribe: el nivel es INFO")     # el filtro va antes de formatear

registros = [json.loads(linea) for linea in flujo.getvalue().splitlines()]
# getvalue() devuelve el texto acumulado (el StringIO no se vacia al leer); splitlines() lo
# parte por saltos de linea y json.loads() reconstruye cada objeto: el registro se consulta.
print("lineas emitidas:", len(registros))                # -> 2
print("niveles:", [r["nivel"] for r in registros])       # -> ['INFO', 'WARNING']
print("mensajes:", [r["mensaje"] for r in registros])    # -> ['cobro aceptado', 'reintento de pasarela']
print("campos del segundo:", registros[1]["campos"])     # -> {'intento': 2, 'pedido': 8412}
