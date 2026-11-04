import html

comentario = "<script>fetch('/robar?c='+document.cookie)</script>"   # si se pinta tal cual, roba la sesion
plantilla = "<p>{}</p>"

# MAL: el texto se inyecta tal cual y el navegador lo ejecuta como codigo.
print("sin escapar:", plantilla.format(comentario)[:34], "...")

# BIEN: se escapan los caracteres con significado en HTML antes de pintarlos.
print("escapado   :", plantilla.format(html.escape(comentario))[:34], "...")   # < pasa a ser &lt;
