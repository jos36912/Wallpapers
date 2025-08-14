# /storage/emulated/0/CORTANA/admin.py

import os

def add_multiple_entries(file_path, prompt, run_script=None):
    while True:
        entry = input(prompt)
        if entry.lower() == 'done':  # Palabra clave para terminar
            break
        with open(file_path, 'a') as f:
            f.write(entry + '\n')
        print(f"{entry} añadido correctamente.")
    print("Entradas completadas.")
    if run_script:
        print(f"Ejecutando {run_script} para actualizar el contenido...")
        os.system(f"python {run_script}")

while True:
    print("\nOpciones:")
    print("1. Agregar enlaces de imágenes (enlaces.txt) - Activa script.py")
    print("2. Agregar enlaces de videos (videos.txt) - Activa video_script.py")
    print("3. Agregar frases (frases.txt) - No activa scripts")
    print("4. Mostrar ayuda y descripción de uso")
    print("5. Salir")
    
    choice = input("Elige una opción (1-5): ")

    if choice == '1':
        add_multiple_entries('/storage/emulated/0/CORTANA/enlaces.txt', 
                           "Ingresa un enlace de imagen (o 'done' para terminar): ",
                           '/storage/emulated/0/CORTANA/script.py')
    elif choice == '2':
        add_multiple_entries('/storage/emulated/0/CORTANA/videos.txt', 
                           "Ingresa un enlace de video (o 'done' para terminar): ",
                           '/storage/emulated/0/CORTANA/video_script.py')
    elif choice == '3':
        add_multiple_entries('/storage/emulated/0/CORTANA/frases.txt', 
                           "Ingresa una frase (o 'done' para terminar): ")
    elif choice == '4':
        print("\n=== Ayuda y Descripción de Uso ===")
        print("Este script te permite gestionar el contenido de tu proyecto 'CORTANA'.")
        print("- Opción 1: Añade enlaces de imágenes a 'enlaces.txt' y actualiza automáticamente con 'script.py'.")
        print("- Opción 2: Añade enlaces de videos a 'videos.txt' y actualiza automáticamente con 'video_script.py'.")
        print("- Opción 3: Añade frases a 'frases.txt' sin activar scripts (ejecuta manualmente si es necesario).")
        print("- Opción 4: Muestra esta ayuda.")
        print("- Opción 5: Sale del programa.")
        print("Para agregar múltiples entradas, escribe cada una y usa 'done' cuando termines.")
        print("Ejecuta este script con 'python admin.py' desde la terminal.\n")
    elif choice == '5':
        print("Saliendo del administrador. ¡Hasta luego!")
        break
    else:
        print("Opción inválida. Por favor, elige 1, 2, 3, 4 o 5.")

print("Administrador cerrado.")
