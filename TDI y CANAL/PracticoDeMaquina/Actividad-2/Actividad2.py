# ==============================================================================
# TEORÍA DE LA INFORMACIÓN - PRÁCTICO DE MÁQUINA 1
# Actividad 2: Análisis de Entropía, Histogramas y Estructura de Archivos (BMP vs. JPG)
# ==============================================================================
# Este script analiza la distribución estadística de la información y la
# estructura interna de archivos de imagen sin compresión espacial (BMP)
# y comprimidos con pérdida (JPG).
#
# Para estudiar cómo influye la redundancia espacial en la compresión, se
# comparan tres casos con características acústico-visuales extremas:
#   1. Color Sólido (color_solido.bmp / .jpg): Máxima redundancia espacial.
#   2. Fotografía / Paisaje (foto.bmp / .jpg): Redundancia espacial natural.
#   3. Ruido Aleatorio (ruido.bmp / .jpg): Nula redundancia espacial.
#
# Objetivos de la actividad:
#   a) Validación de existencia y formato de las imágenes.
#   b) Lectura y análisis de la cabecera estándar BMP (primeros 54 bytes).
#   c) Frecuencia de aparición de cada byte (0 al 255) y probabilidades.
#   d) Generación de histogramas comparativos (cuadrícula 3x2).
#   e) Cálculo de la Entropía de Shannon: H(X) = - sum(p_i * log2(p_i)).
#   f) Análisis conceptual de los resultados y de la redundancia espacial.
# ==============================================================================

import os
import math
import struct
from collections import Counter
import matplotlib.pyplot as plt


# Lista de imágenes de prueba para la comparativa
IMAGENES = [
    {
        "nombre": "Color Sólido",
        "bmp": "color_solido.bmp",
        "jpg": "color_solido.jpg",
        "color_bmp": "#1f77b4",
        "color_jpg": "#ff7f0e",
    },
    {
        "nombre": "Fotografía (Paisaje)",
        "bmp": "foto.bmp",
        "jpg": "foto.jpg",
        "color_bmp": "#2ca02c",
        "color_jpg": "#d62728",
    },
    {
        "nombre": "Ruido Aleatorio",
        "bmp": "ruido.bmp",
        "jpg": "ruido.jpg",
        "color_bmp": "#9467bd",
        "color_jpg": "#8c564b",
    },
]


def validar_archivos(ruta_bmp, ruta_jpg):
    """
    Inciso a) Carga y Validación.
    
    Verifica que:
    1. Los archivos existan físicamente en la carpeta.
    2. Las extensiones correspondan a '.bmp' y '.jpg' (o '.jpeg').
    """
    if not os.path.exists(ruta_bmp) or not ruta_bmp.lower().endswith('.bmp'):
        raise ValueError(f"El archivo BMP '{ruta_bmp}' no existe o no tiene extensión .bmp")
    
    if not os.path.exists(ruta_jpg) or not (ruta_jpg.lower().endswith('.jpg') or ruta_jpg.lower().endswith('.jpeg')):
        raise ValueError(f"El archivo JPG '{ruta_jpg}' no existe o no tiene extensión .jpg")


def analizar_cabecera_bmp(ruta_bmp):
    """
    Inciso b) Análisis de Cabecera (Manipulación de bytes).
    
    Lee los primeros 54 bytes de un archivo BMP estándar en color verdadero (24 bits).
    La cabecera se compone de dos bloques consecutivos:
    
    1. BITMAPFILEHEADER (14 bytes):
       - Firma / Signature (2 bytes): Siempre contiene las letras 'BM' (0x42 0x4D en ASCII).
       - FileSize (4 bytes, uint32 little-endian): Tamaño total del archivo en bytes.
       - Reserved1 (2 bytes, uint16): Reservado (normalmente 0).
       - Reserved2 (2 bytes, uint16): Reservado (normalmente 0).
       - DataOffset (4 bytes, uint32 little-endian): Posición donde empiezan los datos de píxeles.
         En imágenes estándar de 24 bpp, este desplazamiento es exactamente 54 bytes.
         
    2. BITMAPINFOHEADER (40 bytes):
       - HeaderSize (4 bytes, uint32): Tamaño de esta cabecera DIB (siempre 40 bytes).
       - Width (4 bytes, int32): Anchura de la imagen en píxeles.
       - Height (4 bytes, int32): Altura de la imagen en píxeles.
       - Planes (2 bytes, uint16): Planos de color (siempre es 1).
       - BitCount (2 bytes, uint16): Profundidad de color en bits por píxel (ej. 24 bits).
       - Compression (4 bytes, uint32): Tipo de compresión (0 = BI_RGB, sin compresión).
       - ImageSize (4 bytes, uint32): Tamaño de los datos de imagen en bytes.
       - XPixelsPerM (4 bytes, int32): Resolución horizontal (píxeles por metro).
       - YPixelsPerM (4 bytes, int32): Resolución vertical (píxeles por metro).
       - ColorsUsed (4 bytes, uint32): Cantidad de colores en la paleta (0 si no usa paleta).
       - ColorsImportant (4 bytes, uint32): Colores importantes (0 = todos importantes).
       
    Formato de struct: '<2sIHHI IiiHHIIiiII' (54 bytes en total).
    """
    with open(ruta_bmp, 'rb') as f:
        cabecera = f.read(54)

    if len(cabecera) < 54:
        raise ValueError(f"El archivo '{ruta_bmp}' es demasiado chico para tener una cabecera BMP válida.")

    # Formato little-endian ('<') para los 16 campos
    fmt = '<2sIHHI' + 'IiiHHIIiiII'
    datos = struct.unpack(fmt, cabecera)

    info = {
        "signature": datos[0].decode('ascii', errors='ignore'),
        "file_size": datos[1],
        "data_offset": datos[4],
        "header_size": datos[5],
        "width": datos[6],
        "height": datos[7],
        "planes": datos[8],
        "bit_count": datos[9],
        "compression": datos[10],
        "image_size": datos[11],
        "x_pixels_m": datos[12],
        "y_pixels_m": datos[13],
        "colors_used": datos[14],
        "colors_important": datos[15]
    }
    return info


def imprimir_cabecera_bmp(ruta_bmp, info):
    """Muestra en pantalla los datos técnicos leídos de la cabecera BMP."""
    print(f"\n--- Cabecera BMP: {os.path.basename(ruta_bmp)} ---")
    print(f"Firma (Signature): {info['signature']} ({'Válida' if info['signature'] == 'BM' else 'Inválida'})")
    print(f"Tamaño reportado del archivo: {info['file_size']:,} bytes")
    print(f"Comienzo de datos de píxeles (DataOffset): byte {info['data_offset']}")
    print(f"Tamaño de cabecera de información: {info['header_size']} bytes")
    print(f"Dimensiones: {info['width']} x {abs(info['height'])} píxeles")
    print(f"Planos de color: {info['planes']}")
    print(f"Profundidad de color: {info['bit_count']} bits por píxel")
    comp_txt = "Sin compresión (BI_RGB)" if info['compression'] == 0 else f"Tipo {info['compression']}"
    print(f"Compresión: {info['compression']} ({comp_txt})")
    print(f"Tamaño de datos de imagen: {info['image_size']:,} bytes")
    print(f"Resolución: {info['x_pixels_m']} x {info['y_pixels_m']} píxeles/metro")
    print("--------------------------------------------------")


def calcular_probabilidades_y_entropia(ruta_archivo):
    """
    Incisos c) y e) Distribución de Probabilidades y Cálculo de Entropía.
    
    Trata al archivo binario como una fuente de información de memoria nula (DMS),
    cuyo alfabeto son los 256 posibles valores de un byte (del 0 al 255):
    
    1. Lee todos los bytes del archivo.
    2. Cuenta cuántas veces se repite cada byte con Counter (frecuencia absoluta n_i).
    3. Calcula la frecuencia relativa (probabilidad empírica):
          p_i = n_i / N
    4. Aplica la fórmula de Shannon para la entropía:
          H(X) = - sum_{i=0}^{255} p_i * log2(p_i)   [bits/símbolo]
          
    Retorna:
        tuple: (frecuencias, probabilidades, entropia, total_bytes)
    """
    with open(ruta_archivo, 'rb') as f:
        datos = f.read()

    total_bytes = len(datos)
    if total_bytes == 0:
        raise ValueError(f"El archivo '{ruta_archivo}' está vacío.")

    frecuencias = Counter(datos)
    probabilidades = {b: count / total_bytes for b, count in frecuencias.items()}
    entropia = -sum(p * math.log2(p) for p in probabilidades.values() if p > 0)

    return frecuencias, probabilidades, entropia, total_bytes


def graficar_histogramas_comparativos(resultados, ruta_salida="Histograma.png"):
    """
    Inciso d) Histogramas de Frecuencia Comparativos (Cuadrícula 3x2).
    
    Genera una figura con 3 filas (Color Sólido, Foto, Ruido) y 2 columnas (BMP vs. JPG):
    - Columna izquierda (BMP): Muestra picos muy marcados en los colores repetidos
      (evidenciando la redundancia espacial de los píxeles).
    - Columna derecha (JPG): Muestra una distribución mucho más uniforme, donde
      los bytes se reparten parejos por la codificación Huffman.
    """
    fig, axs = plt.subplots(3, 2, figsize=(15, 12))

    for i, res in enumerate(resultados):
        img_info = res["imagen"]
        x_b, y_b = zip(*sorted(res["frec_bmp"].items()))
        x_j, y_j = zip(*sorted(res["frec_jpg"].items()))
        h_b = res["entropia_bmp"]
        h_j = res["entropia_jpg"]
        dh = res["delta_h"]

        # Subgráfico BMP
        axs[i, 0].bar(x_b, y_b, color=img_info["color_bmp"], width=1.0)
        axs[i, 0].set_title(f"{i+1}. {img_info['nombre']} - BMP (H = {h_b:.4f} bits/símbolo)", fontsize=11, fontweight='bold')
        axs[i, 0].set_ylabel("Frecuencia Absoluta")
        axs[i, 0].grid(axis='y', linestyle='--', alpha=0.5)

        # Subgráfico JPG
        axs[i, 1].bar(x_j, y_j, color=img_info["color_jpg"], width=1.0)
        axs[i, 1].set_title(f"{i+1}. {img_info['nombre']} - JPG (H = {h_j:.4f} bits/símbolo | Delta H = {dh:+.4f})", fontsize=11, fontweight='bold')
        axs[i, 1].set_ylabel("Frecuencia Absoluta")
        axs[i, 1].grid(axis='y', linestyle='--', alpha=0.5)

        if i == 2:
            axs[i, 0].set_xlabel("Valor del Byte (0 - 255)")
            axs[i, 1].set_xlabel("Valor del Byte (0 - 255)")

    plt.suptitle("Comparativa de Entropía y Redundancia Espacial en Imágenes (BMP vs. JPG)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=150)
    print(f"[OK] Gráfico comparativo guardado exitosamente en '{ruta_salida}'.")
    plt.show()


def main():
    """
    Flujo principal de ejecución:
    1. Verifica la existencia de las imágenes de prueba.
    2. Lee e interpreta las cabeceras estándar BMP de 54 bytes.
    3. Calcula frecuencias y entropía empírica de Shannon para BMP y JPG.
    4. Muestra una tabla comparativa con tamaños, ratios de compresión y entropías.
    5. Guarda y muestra el gráfico comparativo (Histograma.png).
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)

    print("=" * 95)
    print(" TEORÍA DE LA INFORMACIÓN - PRÁCTICO DE MÁQUINA 1 (ACTIVIDAD 2)")
    print(" ANÁLISIS DE IMÁGENES: COLOR SÓLIDO vs. FOTOGRAFÍA vs. RUIDO ALEATORIO (BMP vs. JPG)")
    print("=" * 95)

    # a) Validación de existencia de archivos
    for img in IMAGENES:
        validar_archivos(img["bmp"], img["jpg"])
    print("[OK] Todas las imágenes de prueba existen y tienen el formato correcto.\n")

    resultados = []

    for img in IMAGENES:
        print(f"\n>>> Procesando: {img['nombre']}...")

        # b) Análisis de cabecera BMP
        cabecera = analizar_cabecera_bmp(img["bmp"])
        imprimir_cabecera_bmp(img["bmp"], cabecera)

        # c) y e) Probabilidades y Entropía empírica
        print(f"Analizando '{img['bmp']}'...")
        frec_b, prob_b, h_b, size_b = calcular_probabilidades_y_entropia(img["bmp"])

        print(f"Analizando '{img['jpg']}'...")
        frec_j, prob_j, h_j, size_j = calcular_probabilidades_y_entropia(img["jpg"])

        ratio = size_b / size_j
        reduccion = (1 - size_j / size_b) * 100
        delta_h = h_j - h_b

        print(f"  -> H(BMP): {h_b:.4f} b/s | H(JPG): {h_j:.4f} b/s | Delta H: {delta_h:+.4f} b/s | Ratio: {ratio:.2f}:1 (-{reduccion:.1f}%)")

        resultados.append({
            "imagen": img,
            "cabecera": cabecera,
            "frec_bmp": frec_b,
            "entropia_bmp": h_b,
            "tamano_bmp": size_b,
            "frec_jpg": frec_j,
            "entropia_jpg": h_j,
            "tamano_jpg": size_j,
            "ratio_compresion": ratio,
            "reduccion_porc": reduccion,
            "delta_h": delta_h
        })

    # Resumen comparativo en consola
    print("\n" + "=" * 105)
    print(f"{'CASO DE ESTUDIO':<25} | {'BMP (KB)':<10} | {'JPG (KB)':<10} | {'REDUCCIÓN':<11} | {'RATIO':<8} | {'H(BMP)':<8} | {'H(JPG)':<8} | {'Delta H':<8}")
    print("-" * 105)
    for res in resultados:
        nombre = res["imagen"]["nombre"]
        kb_b = f"{res['tamano_bmp'] / 1024:.1f} KB"
        kb_j = f"{res['tamano_jpg'] / 1024:.1f} KB"
        red = f"-{res['reduccion_porc']:.1f}%"
        rat = f"{res['ratio_compresion']:.2f}:1"
        hb = f"{res['entropia_bmp']:.4f}"
        hj = f"{res['entropia_jpg']:.4f}"
        dh = f"{res['delta_h']:+.4f}"
        print(f"{nombre:<25} | {kb_b:<10} | {kb_j:<10} | {red:<11} | {rat:<8} | {hb:<8} | {hj:<8} | {dh:<8}")
    print("=" * 105)
    print("Límite teórico máximo de entropía para 256 valores (8 bits): 8.0000 bits/símbolo.\n")

    # d) Generación y guardado del gráfico comparativo
    graficar_histogramas_comparativos(resultados, ruta_salida="Histograma.png")


if __name__ == "__main__":
    main()
