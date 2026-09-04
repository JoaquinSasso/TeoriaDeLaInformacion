import os
import math
import struct
from collections import Counter
import matplotlib.pyplot as plt

def validar_archivos(ruta_wav, ruta_mp3):
    """Valida la existencia y extensión de los archivos."""
    if not os.path.exists(ruta_wav) or not ruta_wav.lower().endswith('.wav'):
        raise ValueError("El archivo WAV no existe o la extensión es incorrecta.")
    
    if not os.path.exists(ruta_mp3) or not ruta_mp3.lower().endswith('.mp3'):
        raise ValueError("El archivo MP3 no existe o la extensión es incorrecta.")
    
    print("[OK] Archivos validados correctamente.")

def analizar_cabecera_wav(ruta_wav):
    """Lee y aísla la cabecera estándar RIFF/WAVE (primeros 44 bytes)."""
    with open(ruta_wav, 'rb') as f:
        cabecera = f.read(44)
        
    if len(cabecera) < 44:
        raise ValueError("El archivo WAV es demasiado pequeño para contener una cabecera estándar.")

    # Desempaquetado de los 13 elementos (índices 0 al 12)
    datos = struct.unpack('<4sI4s4sIHHIIHH4sI', cabecera)
    
    chunk_id = datos[0].decode('ascii', errors='ignore')
    formato = datos[2].decode('ascii', errors='ignore')
    subchunk1_id = datos[3].decode('ascii', errors='ignore')
    bits_per_sample = datos[10]
    subchunk2_id = datos[11].decode('ascii', errors='ignore')
    subchunk2_size = datos[12]

    print("\n--- Cabecera WAV ---")
    print(f"ChunkID: {chunk_id}")
    print(f"Chunk Size: {datos[1]} bytes")
    print(f"Format: {formato}")
    print(f"Subchunk1 ID (Fmt): {subchunk1_id}")
    print(f"Frecuencia de Muestreo (Sample Rate): {datos[7]} Hz")
    print(f"Canales (Num Channels): {datos[6]}")
    print(f"Bits por Muestra: {bits_per_sample} bits")
    
    # Validación: Revisamos si el subchunk 2 es 'data' u otra metadata
    if 'data' in subchunk2_id.lower():
        print(f"Subchunk2 ID (Data): {subchunk2_id}")
        print(f"Tamaño de los datos de audio: {subchunk2_size} bytes")
    else:
        print(f"Subchunk2 ID (Metadata detectada): {subchunk2_id}")
        print(f"Tamaño de la metadata extra: {subchunk2_size} bytes")
        print("[!] Nota: Este archivo contiene metadatos desplazando el chunk 'data'.")
    print("--------------------\n")
    
    
def calcular_probabilidades_y_entropia(ruta_archivo):
    """Lee el archivo byte a byte, calcula probabilidades y entropía empírica."""
    with open(ruta_archivo, 'rb') as f:
        datos = f.read()
    
    total_bytes = len(datos)
    frecuencias = Counter(datos)
    
    probabilidades = {byte: frec / total_bytes for byte, frec in frecuencias.items()}
    
    # Cálculo de Entropía Empírica utilizando la fórmula de Shannon
    entropia = -sum(p * math.log2(p) for p in probabilidades.values())
    
    return frecuencias, entropia

def graficar_histogramas(frec_wav, frec_mp3):
    """Genera el gráfico del histograma de frecuencias comparativo."""
    x_wav, y_wav = zip(*sorted(frec_wav.items()))
    x_mp3, y_mp3 = zip(*sorted(frec_mp3.items()))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.bar(x_wav, y_wav, color='blue', width=1.0)
    ax1.set_title("Histograma WAV (Sin compresión)")
    ax1.set_xlabel("Valor del Byte (0-255)")
    ax1.set_ylabel("Frecuencia")
    
    ax2.bar(x_mp3, y_mp3, color='orange', width=1.0)
    ax2.set_title("Histograma MP3 (Comprimido)")
    ax2.set_xlabel("Valor del Byte (0-255)")
    ax2.set_ylabel("Frecuencia")
    
    plt.tight_layout()
    plt.show()

def main():
    # Rutas de los archivos con el Himno Nacional Argentino
    ruta_wav = "himno-nacional-argentino.wav"
    ruta_mp3 = "himno-nacional-argentino.mp3"
    
    try:
        validar_archivos(ruta_wav, ruta_mp3)
        analizar_cabecera_wav(ruta_wav)
        
        print("Analizando archivo WAV...")
        frec_wav, entropia_wav = calcular_probabilidades_y_entropia(ruta_wav)
        
        print("Analizando archivo MP3...")
        frec_mp3, entropia_mp3 = calcular_probabilidades_y_entropia(ruta_mp3)
        
        print(f"\nEntropía Empírica WAV: {entropia_wav:.4f} bits/símbolo")
        print(f"Entropía Empírica MP3: {entropia_mp3:.4f} bits/símbolo")
        
        graficar_histogramas(frec_wav, frec_mp3)
        
    except Exception as e:
        print(f"Error durante la ejecución: {e}")

if __name__ == "__main__":
    main()