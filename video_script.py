import os
import json
import random
import uuid
from bs4 import BeautifulSoup

# 🛠️ Archivos involucrados
VIDEOS_TXT = "videos.txt"
VIDEOS_JSON = "videos.json"
FRASES_TXT = "frases.txt"
USADAS_TXT = "usadas.txt"
HTML_PATH = "web1/index.html"

# 🎬 Plantilla HTML para videos
TEMPLATE_VIDEO = '''
    <div class="video-card">
        <h2 class="frase">{frase}</h2>
        <video controls preload="metadata">
            <source src="{url}" type="video/webm">
            Tu navegador no soporta el tag de video.
        </video>
    </div>
'''

# 📖 Cargar frases disponibles (excluyendo usadas)
def obtener_frases_disponibles():
    if not os.path.exists(FRASES_TXT):
        return []
    with open(FRASES_TXT, 'r', encoding='utf-8') as f:
        frases = [line.strip() for line in f if line.strip()]
    usadas = set()
    if os.path.exists(USADAS_TXT):
        with open(USADAS_TXT, 'r', encoding='utf-8') as f:
            usadas = set(line.strip() for line in f if line.strip())
    disponibles = [f for f in frases if f not in usadas]
    random.shuffle(disponibles)
    return disponibles

# 🧠 Cargar el archivo JSON (si existe)
def cargar_json():
    if os.path.exists(VIDEOS_JSON):
        with open(VIDEOS_JSON, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return {"videos": []}
    return {"videos": []}

# 💾 Guardar datos en JSON
def guardar_json(data):
    with open(VIDEOS_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ✅ Marcar frases como usadas
def registrar_frases_usadas(frases_usadas):
    with open(USADAS_TXT, 'a', encoding='utf-8') as f:
        for frase in frases_usadas:
            f.write(frase + '\n')

# 🧪 Verificar si un video ya está en el HTML
def video_ya_en_html(url, soup):
    return soup.find("source", src=url) is not None

# 🧱 Insertar videos en el HTML
def insertar_en_html(videos):
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    contenedor = soup.find("div", id="videos")
    if not contenedor:
        print("⚠️ No se encontró el contenedor de videos en el HTML.")
        return

    nuevos_insertados = 0
    for video in videos:
        if not video_ya_en_html(video["url"], soup):
            html_fragment = BeautifulSoup(TEMPLATE_VIDEO.format(frase=video["frase"], url=video["url"]), 'html.parser')
            contenedor.append(html_fragment)
            nuevos_insertados += 1

    if nuevos_insertados > 0:
        with open(HTML_PATH, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))

# 🚀 Lógica principal
def main():
    frases_disponibles = obtener_frases_disponibles()
    json_data = cargar_json()
    existentes = {v["url"] for v in json_data["videos"]}
    nuevas_frases_usadas = []

    nuevos_videos = []

    if os.path.exists(VIDEOS_TXT):
        with open(VIDEOS_TXT, 'r', encoding='utf-8') as f:
            enlaces = [line.strip() for line in f if line.strip()]
    else:
        enlaces = []

    for url in enlaces:
        if url not in existentes and frases_disponibles:
            frase = frases_disponibles.pop()
            nuevas_frases_usadas.append(frase)
            video_data = {
                "id": f"vid{str(uuid.uuid4())[:8]}",
                "frase": frase,
                "url": url
            }
            json_data["videos"].append(video_data)
            nuevos_videos.append(video_data)

    if nuevos_videos:
        guardar_json(json_data)
        insertar_en_html(nuevos_videos)
        registrar_frases_usadas(nuevas_frases_usadas)
        open(VIDEOS_TXT, 'w').close()  # Limpiar el archivo txt
        print(f"✅ {len(nuevos_videos)} nuevos videos agregados.")
    else:
        # 🕵️ Si no hay nada en videos.txt, revisamos que todo esté en HTML
        insertar_en_html(json_data["videos"])
        print("🔁 No hay nuevos videos, pero se verificó el HTML.")

if __name__ == "__main__":
    main()