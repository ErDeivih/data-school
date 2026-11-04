import json

# Respuesta tipica de un listado de objetos (formato de S3 y compatibles).
# Fijate en IsTruncated y NextContinuationToken: el listado NO devuelve todo el prefijo.
respuesta = json.dumps({
    "Name": "datos-ventas",
    "Prefix": "ventas/2026/",
    "KeyCount": 2,
    "IsTruncated": True,
    "NextContinuationToken": "1ueGcxLPRx1Tr/XYExHnhbYLgveDs2J/wm36Hy4vbOwM=",
    "Contents": [
        {"Key": "ventas/2026/01/parte-0001.parquet", "Size": 134217728,
         "StorageClass": "STANDARD", "ETag": "9b2cf535f27731c974343645a3985328"},
        {"Key": "ventas/2026/01/parte-0002.parquet", "Size": 131072000,
         "StorageClass": "STANDARD", "ETag": "5f363e0e58a95f06cbe9bbc662c5dfb6"},
    ],
}, indent=2)
print(respuesta)

# Con IsTruncated en True hay que repetir la llamada pasando el token; sin ese bucle
# te quedas con las primeras claves y crees que el prefijo esta vacio o incompleto.
peticion = {"Bucket": "datos-ventas", "Prefix": "ventas/2026/",
            "ContinuationToken": "1ueGcxLPRx1Tr/XYExHnhbYLgveDs2J/wm36Hy4vbOwM="}
print("siguiente llamada:", peticion["ContinuationToken"][:12] + "...")  # -> 1ueGcxLPRx1T...
