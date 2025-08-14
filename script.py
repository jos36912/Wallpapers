import json
import random
import os

# Rutas de los archivos
ARCHIVO_ENLACES = "enlace.txt"
ARCHIVO_JSON = "enlace.json"
ARCHIVO_HTML = "web1/index.html"
ARCHIVO_FRASES = "frases.txt"
ARCHIVO_USADAS = "usadas.txt"

# Cargar frases disponibles y usadas
def cargar_frases():
    with open(ARCHIVO_FRASES, "r", encoding="utf-8") as f:
        frases = [line.strip() for line in f if line.strip()]
    usadas = []
    if os.path.exists(ARCHIVO_USADAS):
        with open(ARCHIVO_USADAS, "r", encoding="utf-8") as f:
            usadas = [line.strip() for line in f if line.strip()]
    disponibles = list(set(frases) - set(usadas))
    return disponibles, usadas

# Cargar JSON de imágenes
def cargar_json():
    if not os.path.exists(ARCHIVO_JSON):
        return []
    with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Guardar JSON actualizado
def guardar_json(data):
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Guardar frases usadas
def guardar_usadas(usadas):
    with open(ARCHIVO_USADAS, "w", encoding="utf-8") as f:
        f.write("\n".join(usadas))

# Agregar nuevas imágenes al HTML
def insertar_en_html(nuevas_imagenes):
    if not os.path.exists(ARCHIVO_HTML):
        print("❌ No se encontró el archivo HTML.")
        return

    with open(ARCHIVO_HTML, "r", encoding="utf-8") as f:
        contenido = f.read()

    if "<!-- GALERIA -->" not in contenido:
        print("❌ No se encontró el marcador <!-- GALERIA --> en el HTML.")
        return

    partes = contenido.split("<!-- GALERIA -->")
    inicio = partes[0] + "<!-- GALERIA -->"
    cuerpo = ""
    final = partes[1]

    for item in nuevas_imagenes:
        cuerpo += f"""
    <div class="card">
      <h2 class="frase">"{item['frase']}"</h2>
      <div class="imagen-contenedor">
        <img src="{item['url']}" alt="Imagen">
        <div class="botones">
          <button class="like-btn">🩶LIKE</button>
          <a href="{item['url']}" download><button class="descargar-btn">Download</button></a>
        </div>
      </div>
    </div>
"""

    nuevo_contenido = inicio + cuerpo + final
    with open(ARCHIVO_HTML, "w", encoding="utf-8") as f:
        f.write(nuevo_contenido)

# Script principal
def main():
    # Leer enlaces
    if not os.path.exists(ARCHIVO_ENLACES):
        print("❌ No se encontró enlace.txt.")
        return

    with open(ARCHIVO_ENLACES, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    if not urls:
        print("⚠️ No hay enlaces nuevos en enlace.txt.")
        return

    existentes = cargar_json()
    existentes_urls = [item["url"] for item in existentes]

    nuevas_imagenes = []
    frases_disponibles, frases_usadas = cargar_frases()

    for url in urls:
        if url in existentes_urls or not url.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue
        if not frases_disponibles:
            print("⚠️ No hay frases disponibles.")
            break
        frase = random.choice(frases_disponibles)
        frases_disponibles.remove(frase)
        frases_usadas.append(frase)

        nuevas_imagenes.append({
            "id": f"img{len(existentes) + len(nuevas_imagenes) + 1}",
            "frase": frase,
            "url": url
        })

    if not nuevas_imagenes:
        print("⚠️ No se agregaron nuevas imágenes.")
        return

    # Actualizar archivos
    existentes.extend(nuevas_imagenes)
    guardar_json(existentes)
    guardar_usadas(frases_usadas)
    insertar_en_html(nuevas_imagenes)

    # Vaciar el enlace.txt
    with open(ARCHIVO_ENLACES, "w", encoding="utf-8") as f:
        f.write("")

    print(f"✅ {len(nuevas_imagenes)} nuevas imágenes agregadas.")

if __name__ == "__main__":
    main()