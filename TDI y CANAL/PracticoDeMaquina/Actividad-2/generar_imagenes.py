# ==============================================================================
# TEORÍA DE LA INFORMACIÓN - PRÁCTICO DE MÁQUINA 1
# Actividad 2: Generador de Imágenes de Prueba (Color Sólido, Foto y Ruido)
# ==============================================================================
# Este script crea 3 pares de imágenes en formato BMP (24 bits sin compresión)
# y JPG (comprimido con pérdida) con una resolución idéntica de 512x512 píxeles.
#
# Casos generados:
#   1. Color Sólido (color_solido.bmp / .jpg): Máxima redundancia espacial.
#   2. Fotografía / Paisaje (foto.bmp / .jpg): Redundancia espacial intermedia real.
#   3. Ruido Aleatorio (ruido.bmp / .jpg): Nula redundancia espacial.
# ==============================================================================

import os
import random
from PIL import Image, ImageDraw


def generar_imagenes():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)

    ancho, alto = 512, 512
    print(f"Generando imágenes de prueba ({ancho} por {alto} píxeles, 24 bpp)...")

    # 1. Color Sólido: Un solo color en toda la imagen (RGB: 41, 128, 185)
    img_solido = Image.new("RGB", (ancho, alto), color=(41, 128, 185))
    img_solido.save("color_solido.bmp")
    img_solido.save("color_solido.jpg", quality=85)
    print("[OK] 1. Color Sólido: 'color_solido.bmp' y 'color_solido.jpg'")

    # 2. Fotografía / Paisaje: Elementos con gradientes suaves y formas continuas
    img_foto = Image.new("RGB", (ancho, alto))
    draw = ImageDraw.Draw(img_foto)

    # Cielo en gradiente
    for y in range(260):
        t = y / 260.0
        r = int(135 + (245 - 135) * t)
        g = int(206 + (180 - 206) * t)
        b = int(235 + (120 - 235) * t)
        draw.line([(0, y), (ancho, y)], fill=(r, g, b))

    # Sol en el horizonte
    draw.ellipse([210, 160, 300, 250], fill=(255, 230, 110))

    # Montañas
    montanias = [
        (0, 280), (80, 210), (160, 270), (250, 190),
        (350, 260), (430, 200), (512, 280), (512, 330), (0, 330)
    ]
    draw.polygon(montanias, fill=(60, 80, 70))

    # Lago con gradiente y reflejos
    for y in range(280, 512):
        t = (y - 280) / (512.0 - 280.0)
        r = int(40 + t * 20)
        g = int(90 + t * 30)
        b = int(140 + t * 40)
        draw.line([(0, y), (ancho, y)], fill=(r, g, b))

    # Orilla de pasto
    draw.polygon([(0, 470), (120, 460), (280, 490), (512, 470), (512, 512), (0, 512)], fill=(46, 125, 50))

    img_foto.save("foto.bmp")
    img_foto.save("foto.jpg", quality=85)
    print("[OK] 2. Fotografía / Paisaje: 'foto.bmp' y 'foto.jpg'")

    # 3. Ruido Aleatorio: Píxeles completamente aleatorios e independientes
    random.seed(2026)
    bytes_ruido = bytes([random.randint(0, 255) for _ in range(ancho * alto * 3)])
    img_ruido = Image.frombytes("RGB", (ancho, alto), bytes_ruido)
    img_ruido.save("ruido.bmp")
    img_ruido.save("ruido.jpg", quality=85)
    print("[OK] 3. Ruido Aleatorio: 'ruido.bmp' y 'ruido.jpg'")

    print("¡Todas las imágenes fueron generadas correctamente!")


if __name__ == "__main__":
    generar_imagenes()
