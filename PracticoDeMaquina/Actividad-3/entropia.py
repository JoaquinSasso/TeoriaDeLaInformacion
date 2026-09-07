import math
import os
import sys

def calcular_entropia_y_redundancia(ruta_archivo):
    """
    Lee un archivo byte por byte de manera eficiente y calcula su entropía empírica y redundancia.
    La complejidad de tiempo es O(N) donde N es el número de bytes del archivo.
    """
    if not os.path.isfile(ruta_archivo):
        print(f"Error: El archivo {ruta_archivo} no existe.")
        return None

    # Array de tamaño fijo (256) para contar la frecuencia de cada byte (valores del 0 al 255)
    frecuencias = [0] * 256
    total_bytes = 0

    # Lectura del archivo en modo binario
    # Leer en bloques (chunks) garantiza que el tiempo siga siendo O(N) pero reduce 
    # la carga de I/O en comparación con leer estrictamente un byte por iteración.
    with open(ruta_archivo, 'rb') as archivo:
        while True:
            chunk = archivo.read(8192) # Leer en bloques de 8KB
            if not chunk:
                break
            for byte in chunk:
                frecuencias[byte] += 1
                total_bytes += 1

    if total_bytes == 0:
        print("El archivo está vacío.")
        return 0.0, 0.0

    entropia = 0.0
    
    # Calcular la entropía empírica usando la fórmula de Shannon
    for frec in frecuencias:
        if frec > 0:
            # Probabilidad de aparición de cada símbolo (byte)
            p_i = frec / total_bytes
            # Sumatoria de p_i * log2(p_i)
            entropia -= p_i * math.log2(p_i)

    # El tamaño del alfabeto es de 256 símbolos (1 byte). 
    # La entropía máxima teórica es log2(256) = 8 bits/símbolo.
    entropia_maxima = 8.0
    
    # Redundancia absoluta (en bits)
    redundancia = entropia_maxima - entropia

    return entropia, redundancia, total_bytes

def analizar_archivo(ruta):
    print(f"--- Analizando: {ruta} ---")
    resultado = calcular_entropia_y_redundancia(ruta)
    if resultado:
        entropia, redundancia, tamano = resultado
        print(f"Tamaño del archivo: {tamano} bytes")
        print(f"Entropía Empírica:  {entropia:.4f} bits/símbolo")
        print(f"Redundancia:        {redundancia:.4f} bits/símbolo\n")

if __name__ == "__main__":
    # Ejecución del programa (Inciso b)
    # Aquí puedes poner el nombre de los archivos generados o pasar tus propios archivos
    archivo_txt = r"G:\Mi unidad\Facultad\4to año\Segundo Cuatrimestre\Teoría de la Información\TeoriaDeLaInformacion\PracticoDeMaquina\Actividad-3\texto_prueba.txt"
    archivo_zip = r"G:\Mi unidad\Facultad\4to año\Segundo Cuatrimestre\Teoría de la Información\TeoriaDeLaInformacion\PracticoDeMaquina\Actividad-3\texto_prueba.zip"
    
    analizar_archivo(archivo_txt)
    analizar_archivo(archivo_zip)