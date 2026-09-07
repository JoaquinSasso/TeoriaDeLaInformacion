import os

def calcular_indice_coincidencia(ruta_archivo):
    """
    Lee un archivo byte por byte de manera eficiente y calcula su Índice de Coincidencia (IC).
    """
    if not os.path.isfile(ruta_archivo):
        print(f"Error: El archivo {ruta_archivo} no existe.")
        return None

    # Array de tamaño fijo (256) para contar la frecuencia de cada byte, indexado desde 0
    frecuencias = [0] * 256
    total_bytes = 0

    with open(ruta_archivo, 'rb') as archivo:
        while True:
            chunk = archivo.read(8192)
            if not chunk:
                break
            for byte in chunk:
                frecuencias[byte] += 1
                total_bytes += 1

    if total_bytes <= 1:
        print("El archivo es demasiado pequeño para calcular el IC.")
        return 0.0, total_bytes

    suma_coincidencias = 0
    
    # Cálculo de sumatoria(f_i * (f_i - 1))
    for f in frecuencias:
        if f > 1:
            suma_coincidencias += f * (f - 1)

    # Aplicación de la fórmula del IC
    ic = suma_coincidencias / (total_bytes * (total_bytes - 1))

    return ic, total_bytes

def analizar_ic(ruta):
    print(f"--- Analizando IC: {ruta} ---")
    resultado = calcular_indice_coincidencia(ruta)
    if resultado:
        ic, tamano = resultado
        print(f"Tamaño del archivo:       {tamano} bytes")
        print(f"Índice de Coincidencia:   {ic:.6f}\n")

if __name__ == "__main__":
    # Usando las mismas rutas con 'r' (raw string) que configuraste previamente
    archivo_txt = r"G:\Mi unidad\Facultad\4to año\Segundo Cuatrimestre\Teoría de la Información\TeoriaDeLaInformacion\PracticoDeMaquina\Actividad-4\texto_prueba.txt"
    archivo_zip = r"G:\Mi unidad\Facultad\4to año\Segundo Cuatrimestre\Teoría de la Información\TeoriaDeLaInformacion\PracticoDeMaquina\Actividad-4\texto_prueba.zip"
    
    analizar_ic(archivo_txt)
    analizar_ic(archivo_zip)