"""seguridad-y-prompt-injection-1.py — por qué la comprobación tiene que estar en el
ejecutor: dos listas blancas comparadas con cuatro URLs, y qué ataque tapa cada defensa.
La figura de la página de inyección de prompts (fase 8)."""

from urllib.parse import urlparse

from comun import *

estilo()

PERMITIDOS = {"api.interna.example"}

URLS = [
    ("URL legítima", "https://api.interna.example/v1/tarifas"),
    ("host falso", "https://api.interna.example.evil.test/roba"),
    ("subdominio interno", "https://file.interna.example/v1"),
    ("usuario falso", "https://api.interna.example@evil.test/roba"),
]


def por_coincidencia_parcial(url):
    """El error clásico: buscar el nombre del host en cualquier parte del texto."""
    return "interna.example" in url


def por_host_exacto(url):
    """Lo correcto: sacar el host y compararlo entero contra la lista blanca."""
    return (urlparse(url).hostname or "").lower() in PERMITIDOS


COMPROBACIONES = [
    ("buscar el nombre\nen el texto", por_coincidencia_parcial),
    ("comparar el host\nexacto", por_host_exacto),
]

# --- Izquierda: dos formas de comprobar la misma lista blanca -----------------
# La figura sube a 9,2 de alto: con 8,6 las etiquetas de dos lineas del eje x de un panel
# quedaban pegadas al titulo del panel siguiente (medido: acababan en y=433 y el titulo
# empezaba en y=485, con el xlabel del primero en medio).
fig, (izq, der) = plt.subplots(2, 1, figsize=(9.8, 9.2))
fig.set_constrained_layout_pads(h_pad=0.14)   # aire entre los dos paneles

for j, (_, comprobar) in enumerate(COMPROBACIONES):
    for i, (_, url) in enumerate(URLS):
        color = VERDE if comprobar(url) else ROJO
        izq.scatter(j, i, marker="s", s=520, color=color, zorder=3)

izq.set_xticks(range(len(COMPROBACIONES)))
izq.set_xticklabels([c[0] for c in COMPROBACIONES], fontsize=9)
izq.set_yticks(range(len(URLS)))
izq.set_yticklabels([u[0] for u in URLS], fontsize=9)
izq.set_xlim(-0.6, len(COMPROBACIONES) - 0.4)
izq.set_ylim(-0.7, len(URLS) - 0.3)
izq.invert_yaxis()
# El significado del color va como nota en la esquina de abajo a la derecha, que es la
# única zona del panel sin cuadros; en el eje x se pisaba con las etiquetas de abajo.
# Va con ax.text() y no con anotar(): en un eje con invert_yaxis(), la anotación de
# matplotlib se queda con un IdentityTransform y el texto NO se dibuja (comprobado: la
# nota del panel de abajo desaparecía del SVG). text() con transform=transAxes sí sale.
izq.text(0.30, 0.05, "verde: la deja pasar\nrojo: la bloquea", transform=izq.transAxes,
         fontsize=8.5, color=TEXTO, va="center", ha="left")
titulo(izq, "La misma lista blanca, dos comprobaciones")
izq.set_xlabel("cada columna es una forma de comprobar la misma lista", labelpad=9)
rejilla(izq, "x")

# --- Derecha: qué ataque detiene cada defensa ---------------------------------
DEFENSAS = ["filtro de\nfrases prohibidas", "lista blanca\nde egreso"]
ATAQUES = ["«ignora lo\nanterior»", "una letra\ncambiada", "orden en\notro idioma",
           "URL a un host\nno permitido"]
# True = esa defensa detiene ese ataque: el filtro caza la frase que tiene en su lista,
# la lista blanca no mira el texto, mira el destino de la llamada.
TAPA = [
    [True, False, False, False],
    [False, False, False, True],
]

for j, defensa in enumerate(DEFENSAS):
    for i, ataque in enumerate(ATAQUES):
        color = VERDE if TAPA[j][i] else ROJO
        der.scatter(i, j, marker="s", s=520, color=color, zorder=3)

der.set_xticks(range(len(ATAQUES)))
der.set_xticklabels(ATAQUES, fontsize=8.5)
der.set_yticks(range(len(DEFENSAS)))
der.set_yticklabels(DEFENSAS, fontsize=9)
der.set_xlim(-0.6, len(ATAQUES) - 0.4)
der.set_ylim(-0.7, len(DEFENSAS) - 0.3)
der.invert_yaxis()
# Misma nota que arriba, en la franja sin cuadros de la derecha. Con anotar() no se
# dibujaba: ver el comentario del panel de arriba.
der.text(0.45, 0.05, "verde: lo detiene\nrojo: lo deja pasar", transform=der.transAxes,
         fontsize=8.5, color=TEXTO, va="center", ha="left")
titulo(der, "Ninguna capa sola cubre los cuatro ataques")
der.set_xlabel("cada ataque que la defensa deja pasar es una puerta abierta", labelpad=9)
rejilla(der, "x")

guardar(fig, "seguridad-y-prompt-injection-capas-que-tapan")
