# ==============================================================================
# TEORÍA DE LA INFORMACIÓN - PRÁCTICO DE MÁQUINA 1
# Actividad 1: Análisis de Información en Señales de Audio (WAV vs. MP3)
# ==============================================================================
# Este script analiza la distribución estadística de la información y la
# estructura interna de archivos de audio crudos (WAV / PCM sin compresión)
# y comprimidos (MP3 con pérdida).
#
# Cumple con los siguientes objetivos de la guía de trabajos prácticos:
#   a) Validación de existencia y extensión de los archivos de entrada.
#   b) Lectura y análisis de los bytes de la cabecera estándar RIFF/WAVE (44 bytes).
#   c) Cálculo de la distribución de frecuencias y probabilidades byte a byte (0-255).
#   d) Generación y visualización de histogramas de frecuencias comparativos.
#   e) Cálculo de la Entropía Empírica de Shannon: H(X) = - sum(p_i * log2(p_i)).
# ==============================================================================

import os
import math
import struct
from collections import Counter
import matplotlib.pyplot as plt


# Definición de pistas de audio para la comparativa progresiva
PISTAS = [
    {
        "nombre": "Himno Nacional (Orquestal)",
        "wav": "himno-nacional-argentino.wav",
        "mp3": "himno-nacional-argentino.mp3",
        "color_wav": "#1f77b4",
        "color_mp3": "#ff7f0e",
    },
    {
        "nombre": "Sillycat Shore (Chiptune 8-bit)",
        "wav": "Sillycat_Shore.wav",
        "mp3": "Sillycat_Shore.mp3",
        "color_wav": "#2ca02c",
        "color_mp3": "#d62728",
    },
    {
        "nombre": "Voz Hablada (Locución con pausas)",
        "wav": "persona.wav",
        "mp3": "persona.mp3",
        "color_wav": "#9467bd",
        "color_mp3": "#8c564b",
    },
]


def validar_archivos(ruta_wav, ruta_mp3):
    """
    Inciso a) Carga y Validación.
    
    Verifica que:
    1. Los archivos existan físicamente en las rutas indicadas.
    2. Las extensiones de los archivos correspondan estrictamente a '.wav' y '.mp3'.
    
    Parámetros:
        ruta_wav (str): Ruta al archivo de audio en formato WAV.
        ruta_mp3 (str): Ruta al archivo de audio en formato MP3.
        
    Lanza:
        ValueError: Si algún archivo no existe o no tiene la extensión esperada.
    """
    if not os.path.exists(ruta_wav) or not ruta_wav.lower().endswith('.wav'):
        raise ValueError(f"El archivo WAV '{ruta_wav}' no existe o la extensión es incorrecta.")
    
    if not os.path.exists(ruta_mp3) or not ruta_mp3.lower().endswith('.mp3'):
        raise ValueError(f"El archivo MP3 '{ruta_mp3}' no existe o la extensión es incorrecta.")
    
    print("[OK] Archivos validados correctamente.")


def analizar_cabecera_wav(ruta_wav):
    """
    Inciso b) Análisis de Cabecera (Manipulación de bytes).
    
    Lee los primeros 44 bytes del archivo WAV, correspondientes a la cabecera
    canónica RIFF/WAVE (Resource Interchange File Format), y desempaqueta sus
    campos mediante la librería 'struct'.
    
    Estructura de la cabecera canónica (44 bytes):
    --------------------------------------------------------------------------
    Offset | Tamaño | Nombre         | Descripción
    --------------------------------------------------------------------------
      0    | 4      | ChunkID        | "RIFF" en ASCII (0x52494646)
      4    | 4      | ChunkSize      | Tamaño del archivo menos 8 bytes (entero 32 bits Little-Endian)
      8    | 4      | Format         | "WAVE" en ASCII (0x57415645)
     12    | 4      | Subchunk1ID    | "fmt " en ASCII (identificador de subchunk de formato)
     16    | 4      | Subchunk1Size  | 16 bytes para formato PCM lineal
     20    | 2      | AudioFormat    | 1 = PCM (sin compresión), otros valores = comprimido
     22    | 2      | NumChannels    | 1 = Mono, 2 = Estéreo
     24    | 4      | SampleRate     | Frecuencia de muestreo en Hz (ej. 44100 Hz)
     28    | 4      | ByteRate       | SampleRate * NumChannels * BitsPerSample / 8
     32    | 2      | BlockAlign     | NumChannels * BitsPerSample / 8 (bytes por muestra)
     34    | 2      | BitsPerSample  | Resolución por muestra en bits (8, 16, 24 bits)
     36    | 4      | Subchunk2ID    | "data" (o chunk de metadatos como "bext", "LIST")
     40    | 4      | Subchunk2Size  | Tamaño de los datos contenidos en este subchunk
    --------------------------------------------------------------------------
    
    Cadena de formato de struct: '<4sI4s4sIHHIIHH4sI'
      '<' : Little-endian (orden estándar de bytes para arquitectura x86 y formato RIFF)
      '4s': Cadena de 4 bytes (ASCII)
      'I' : Entero sin signo de 32 bits (4 bytes)
      'H' : Entero corto sin signo de 16 bits (2 bytes)
    """
    with open(ruta_wav, 'rb') as f:
        cabecera = f.read(44)
        
    if len(cabecera) < 44:
        raise ValueError("El archivo WAV es demasiado pequeño para contener una cabecera estándar.")

    # Desempaquetado de los 13 campos de la cabecera canónica
    datos = struct.unpack('<4sI4s4sIHHIIHH4sI', cabecera)
    
    chunk_id = datos[0].decode('ascii', errors='ignore')
    chunk_size = datos[1]
    formato = datos[2].decode('ascii', errors='ignore')
    subchunk1_id = datos[3].decode('ascii', errors='ignore')
    subchunk1_size = datos[4]
    audio_format = datos[5]
    num_channels = datos[6]
    sample_rate = datos[7]
    byte_rate = datos[8]
    block_align = datos[9]
    bits_per_sample = datos[10]
    subchunk2_id = datos[11].decode('ascii', errors='ignore')
    subchunk2_size = datos[12]

    print("\n--- Cabecera WAV ---")
    print(f"ChunkID: {chunk_id}")
    print(f"Chunk Size: {chunk_size} bytes (Tamaño total reportado: {chunk_size + 8} bytes)")
    print(f"Format: {formato}")
    print(f"Subchunk1 ID (Fmt): {subchunk1_id}")
    print(f"Subchunk1 Size: {subchunk1_size} bytes")
    print(f"Audio Format: {audio_format} ({'PCM lineal sin compresión' if audio_format == 1 else 'Comprimido / Especial'})")
    print(f"Frecuencia de Muestreo (Sample Rate): {sample_rate} Hz")
    print(f"Canales (Num Channels): {num_channels} ({'Mono' if num_channels == 1 else 'Estéreo' if num_channels == 2 else 'Multicanal'})")
    print(f"Tasa de Transferencia (Byte Rate): {byte_rate} bytes/segundo")
    print(f"Alineación de Bloque (Block Align): {block_align} bytes/muestra")
    print(f"Bits por Muestra (Bit Depth): {bits_per_sample} bits")
    
    # Validación: Comprobamos si el subchunk siguiente a 'fmt ' es 'data' u otro bloque intermedio.
    # En muchos archivos WAV profesionales, existen chunks intermedios como 'bext' (Broadcast Wave Format)
    # o 'LIST' (etiquetas de autor/título) antes del subchunk 'data'.
    if 'data' in subchunk2_id.lower():
        print(f"Subchunk2 ID (Data): {subchunk2_id}")
        print(f"Tamaño de los datos de audio: {subchunk2_size} bytes")
    else:
        print(f"Subchunk2 ID (Metadata detectada): {subchunk2_id}")
        print(f"Tamaño de la metadata extra: {subchunk2_size} bytes")
        print("[!] Nota: Este archivo contiene metadatos intermedios desplazando el chunk 'data'.")
    print("--------------------\n")
    return {
        "chunk_id": chunk_id,
        "chunk_size": chunk_size,
        "format": formato,
        "sample_rate": sample_rate,
        "num_channels": num_channels,
        "bits_per_sample": bits_per_sample,
        "audio_format": audio_format,
    }


def calcular_probabilidades_y_entropia(ruta_archivo):
    """
    Incisos c) y e) Distribución de Probabilidades y Cálculo de Entropía.
    
    Procesa un archivo binario completo considerándolo como una fuente de información
    de memoria nula (DMS) cuyo alfabeto son los 256 posibles valores de un byte (0 a 255).
    
    1. Lee todos los bytes del archivo en modo binario ('rb').
    2. Cuenta las ocurrencias de cada símbolo byte s_i con Counter (frecuencia absoluta n_i).
    3. Calcula la frecuencia relativa (probabilidad empírica) de cada símbolo:
          p(s_i) = n_i / N,  donde N es el total de bytes leídos.
    4. Aplica la fórmula de Entropía de Shannon:
          H(X) = - sum_{i=0}^{255} p(s_i) * log_2(p(s_i))  [bits/símbolo]
          
    Parámetros:
        ruta_archivo (str): Ruta del archivo a analizar.
        
    Retorna:
        tuple: (frecuencias, entropia)
            frecuencias (Counter): Diccionario con las ocurrencias de cada byte (0-255).
            entropia (float): Valor de la entropía empírica en bits/símbolo (máximo teórico = 8 bits).
    """
    with open(ruta_archivo, 'rb') as f:
        datos = f.read()
    
    total_bytes = len(datos)
    if total_bytes == 0:
        raise ValueError(f"El archivo '{ruta_archivo}' está vacío.")

    # Contar la frecuencia absoluta de cada byte individual (0 a 255)
    frecuencias = Counter(datos)
    
    # Calcular la probabilidad empírica de cada símbolo: p_i = frecuencia / total
    probabilidades = {byte: frec / total_bytes for byte, frec in frecuencias.items()}
    
    # Cálculo de Entropía Empírica según Shannon:
    # H(X) = - sum( p_i * log2(p_i) )
    # Solo se evalúan probabilidades p_i > 0 (evitando log2(0))
    entropia = -sum(p * math.log2(p) for p in probabilidades.values() if p > 0)
    
    return frecuencias, entropia


def graficar_histogramas(frec_wav, frec_mp3, titulo_wav="WAV", titulo_mp3="MP3"):
    """
    Inciso d) Histogramas de Frecuencia para un par individual de archivos.
    """
    x_wav, y_wav = zip(*sorted(frec_wav.items()))
    x_mp3, y_mp3 = zip(*sorted(frec_mp3.items()))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.bar(x_wav, y_wav, color='blue', width=1.0)
    ax1.set_title(titulo_wav)
    ax1.set_xlabel("Valor del Byte (0 - 255)")
    ax1.set_ylabel("Frecuencia Absoluta")
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    
    ax2.bar(x_mp3, y_mp3, color='orange', width=1.0)
    ax2.set_title(titulo_mp3)
    ax2.set_xlabel("Valor del Byte (0 - 255)")
    ax2.set_ylabel("Frecuencia Absoluta")
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.show()


def graficar_triple_comparativa(resultados, ruta_salida="Histograma.png"):
    """
    Inciso d) Triple Comparativa Visual de Histogramas (3x2).
    
    Genera y guarda una figura comparativa con 3 filas (una por cada señal de audio)
    y 2 columnas (WAV vs. MP3), permitiendo apreciar de manera contundente la
    eliminación de redundancia y el salto de entropía según el tipo de señal acústica.
    """
    fig, axs = plt.subplots(3, 2, figsize=(15, 12))

    for i, res in enumerate(resultados):
        pista = res["pista"]
        x_w, y_w = zip(*sorted(res["frec_wav"].items()))
        x_m, y_m = zip(*sorted(res["frec_mp3"].items()))
        h_w = res["entropia_wav"]
        h_m = res["entropia_mp3"]
        dh = res["delta_h"]

        # Subgráfico WAV
        axs[i, 0].bar(x_w, y_w, color=pista["color_wav"], width=1.0)
        axs[i, 0].set_title(f"{i+1}. {pista['nombre']} - WAV (H = {h_w:.4f} bits/símbolo)", fontsize=11, fontweight='bold')
        axs[i, 0].set_ylabel("Frecuencia Absoluta")
        axs[i, 0].grid(axis='y', linestyle='--', alpha=0.5)

        # Subgráfico MP3
        axs[i, 1].bar(x_m, y_m, color=pista["color_mp3"], width=1.0)
        axs[i, 1].set_title(f"{i+1}. {pista['nombre']} - MP3 (H = {h_m:.4f} bits/símbolo | ΔH = +{dh:.4f})", fontsize=11, fontweight='bold')
        axs[i, 1].set_ylabel("Frecuencia Absoluta")
        axs[i, 1].grid(axis='y', linestyle='--', alpha=0.5)

        if i == 2:
            axs[i, 0].set_xlabel("Valor del Byte (0 - 255)")
            axs[i, 1].set_xlabel("Valor del Byte (0 - 255)")

    plt.suptitle("Triple Comparativa de Entropía y Redundancia en Audio (WAV vs. MP3)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=150)
    print(f"[OK] Gráfico comparativo guardado exitosamente en '{ruta_salida}'.")
    plt.show()


def main():
    """
    Flujo principal de ejecución:
    1. Procesa y valida cada una de las 3 pistas de audio (Orquestal, Chiptune 8-bit, Voz).
    2. Analiza las cabeceras canónicas RIFF/WAVE.
    3. Calcula frecuencias y entropía empírica de Shannon.
    4. Imprime por consola una tabla comparativa con métricas acústicas y teóricas.
    5. Guarda y muestra el gráfico comparativo integral (Histograma.png).
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)

    print("=" * 95)
    print(" TEORÍA DE LA INFORMACIÓN - PRÁCTICO DE MÁQUINA 1 (ACTIVIDAD 1)")
    print(" TRIPLE COMPARATIVA: MÚSICA ORQUESTAL vs. CHIPTUNE 8-BIT vs. VOZ HABLADA")
    print("=" * 95)

    # a) Validación de todos los archivos
    for pista in PISTAS:
        validar_archivos(pista["wav"], pista["mp3"])
    print("[OK] Todos los archivos de audio existen y tienen la extensión correcta.\n")

    resultados = []

    for pista in PISTAS:
        print(f"\n>>> Procesando: {pista['nombre']}...")
        
        # b) Análisis de cabecera WAV
        cabecera_info = analizar_cabecera_wav(pista["wav"])
        
        # c) y e) Probabilidades y Entropía empírica
        print(f"Analizando '{pista['wav']}'...")
        frec_w, h_w = calcular_probabilidades_y_entropia(pista["wav"])
        size_w = os.path.getsize(pista["wav"])
        
        print(f"Analizando '{pista['mp3']}'...")
        frec_m, h_m = calcular_probabilidades_y_entropia(pista["mp3"])
        size_m = os.path.getsize(pista["mp3"])
        
        ratio = size_w / size_m
        reduccion = (1 - size_m / size_w) * 100
        delta_h = h_m - h_w

        print(f"  -> H(WAV): {h_w:.4f} b/s | H(MP3): {h_m:.4f} b/s | Delta H: +{delta_h:.4f} b/s | Ratio: {ratio:.2f}:1 (-{reduccion:.1f}%)")

        resultados.append({
            "pista": pista,
            "cabecera": cabecera_info,
            "frec_wav": frec_w,
            "entropia_wav": h_w,
            "tamano_wav": size_w,
            "frec_mp3": frec_m,
            "entropia_mp3": h_m,
            "tamano_mp3": size_m,
            "ratio_compresion": ratio,
            "reduccion_porc": reduccion,
            "delta_h": delta_h
        })

    # Resumen comparativo en consola
    print("\n" + "=" * 105)
    print(f"{'CASO DE ESTUDIO':<35} | {'RES':<7} | {'WAV (MB)':<9} | {'MP3 (MB)':<9} | {'RATIO':<7} | {'H(WAV)':<8} | {'H(MP3)':<8} | {'Delta H':<7}")
    print("-" * 105)
    for res in resultados:
        nombre = res["pista"]["nombre"]
        bits = f"{res['cabecera']['bits_per_sample']} bits"
        mb_w = f"{res['tamano_wav'] / (1024**2):.2f}"
        mb_m = f"{res['tamano_mp3'] / (1024**2):.2f}"
        rat = f"{res['ratio_compresion']:.2f}:1"
        hw = f"{res['entropia_wav']:.4f}"
        hm = f"{res['entropia_mp3']:.4f}"
        dh = f"+{res['delta_h']:.4f}"
        print(f"{nombre:<35} | {bits:<7} | {mb_w:<9} | {mb_m:<9} | {rat:<7} | {hw:<8} | {hm:<8} | {dh:<7}")
    print("=" * 105)
    print("Límite teórico máximo de entropía para 256 símbolos (8 bits): 8.0000 bits/símbolo.\n")

    # d) Visualización gráfica comparativa
    graficar_triple_comparativa(resultados, ruta_salida="Histograma.png")


if __name__ == "__main__":
    main()