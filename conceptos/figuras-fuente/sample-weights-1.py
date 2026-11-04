"""sample-weights-1.py — etiquetas que se solapan: cuantas veces cuenta cada barra de
mercado y como sale el peso por unicidad. Figura de la pagina de pesos de muestra (fase 9)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Seis operaciones sobre 60 barras, con vidas que se pisan (como etiquetas de triple barrera).
n_barras = 60
n_etiquetas = 6
t0 = np.sort(azar.choice(n_barras - 14, n_etiquetas, replace=False))
largos = azar.integers(8, 15, n_etiquetas)
t1 = np.minimum(t0 + largos, n_barras)

# Concurrencia por barra: cuantas etiquetas estan vivas a la vez.
concurrencia = np.zeros(n_barras)
for a, b in zip(t0, t1):
    concurrencia[a:b] += 1
c_max = int(concurrencia.max())
t_pico = int(np.argmax(concurrencia))

# Unicidad media de cada etiqueta: la media de 1 / concurrencia a lo largo de su vida.
unicidad = np.array([np.mean(1.0 / concurrencia[a:b]) for a, b in zip(t0, t1)])
pesos = unicidad / unicidad.sum() * unicidad.size
etiquetas = [chr(ord("A") + i) for i in range(n_etiquetas)]

fig, ejes = plt.subplots(2, 1, figsize=(7.2, 6.2), sharex=True)

# --- Arriba: el calendario de las etiquetas, con su unicidad escrita al lado ----------
for i, (a, b, u, w) in enumerate(zip(t0, t1, unicidad, pesos)):
    ejes[0].broken_barh([(a, b - a)], (i - 0.36, 0.72), facecolors=AZUL, alpha=0.85)
    ejes[0].text(b + 0.6, i, f"ū = {u:.2f}  →  w = {w:.2f}".replace(".", ","),
                 va="center", fontsize=8, color=TEXTO)
ejes[0].set_ylim(-0.7, n_etiquetas + 1.3)
ejes[0].set_yticks(range(n_etiquetas))
ejes[0].set_yticklabels([f"operación {e}" for e in etiquetas])
ejes[0].set_xlim(0, n_barras + 26)
titulo(ejes[0], "Seis operaciones que se pisan: no son seis trozos de mercado",
       "cada barra azul es la vida de una etiqueta; ū es su unicidad media y w el peso ya normalizado")
ejes[0].axvline(t_pico, color=REJILLA, linewidth=1.1, linestyle="--")
anotar(ejes[0], f"aquí viven {c_max} etiquetas a la vez: ese tramo\nde precios cuenta {c_max} veces",
       xy=(float(t_pico), n_etiquetas + 0.4), xytext=(0.02, 0.95), color=ROJO)

# --- Abajo: la concurrencia, que es lo que reparte el peso ----------------------------
paso = np.append(concurrencia, concurrencia[-1])
ejes[1].step(np.arange(n_barras + 1), paso, where="post", color=CIAN, linewidth=1.6)
ejes[1].fill_between(np.arange(n_barras + 1), paso, 0, step="post", color=CIAN, alpha=0.15)
ejes[1].axhline(1, color=REJILLA, linewidth=1.0, linestyle="--")
ejes[1].set_ylim(0, c_max + 2.6)
ejes[1].set_xlabel("barra de mercado")
ejes[1].set_ylabel("etiquetas vivas")
titulo(ejes[1], "Donde la línea sube, tu muestra vale menos de lo que parece",
       "con c etiquetas vivas, esa barra aporta 1/c de observación a cada una de ellas")
anotar(ejes[1], f"información efectiva: Σū = {unicidad.sum():.2f}".replace(".", ",") +
       f"\n({n_etiquetas} etiquetas no son {n_etiquetas} observaciones)",
       xy=(float(t_pico), float(c_max)), xytext=(0.02, 0.94), color=MORADO)
rejilla(ejes[1])
numeros(ejes[1], "y")

guardar(fig, "pesos-unicidad-solapamiento")
