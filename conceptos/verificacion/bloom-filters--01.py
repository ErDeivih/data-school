import hashlib
import numpy as np


class FiltroBloom:
    def __init__(self, m, k):
        self.m, self.k = m, k
        self.bits = np.zeros(m, dtype=bool)

    def _posiciones(self, elemento):
        # Doble hashing: dos mitades de un hash fuerte simulan k funciones independientes.
        d = hashlib.blake2b(elemento.encode(), digest_size=16).digest()
        h1 = int.from_bytes(d[:8], "big")
        h2 = int.from_bytes(d[8:], "big") | 1     # impar: recorre todos los bits
        return [(h1 + i * h2) % self.m for i in range(self.k)]

    def anadir(self, elemento):
        self.bits[self._posiciones(elemento)] = True

    def podria_estar(self, elemento):
        return bool(self.bits[self._posiciones(elemento)].all())


presentes = ["clave-{}".format(i) for i in range(1000)]
ausentes = ["otra-{}".format(i) for i in range(1000)]
m_bits, k_hash = 8000, 5
filtro = FiltroBloom(m_bits, k_hash)
for p in presentes:
    filtro.anadir(p)

falsos_negativos = sum(not filtro.podria_estar(p) for p in presentes)
falsos_positivos = sum(filtro.podria_estar(a) for a in ausentes)
p_teorica = (1 - np.exp(-k_hash * len(presentes) / m_bits)) ** k_hash

print("bits por elemento:", m_bits / len(presentes))                      # -> 8.0
print("falsos negativos:", falsos_negativos)                             # -> 0
print("falsos positivos:", falsos_positivos, "de", len(ausentes))        # -> 23 de 1000
print("tasa teorica: {:.3f}".format(p_teorica))                          # -> 0.022
