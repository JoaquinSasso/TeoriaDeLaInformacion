"""
Uso:  python compressor.py entrada.txt salida.tdi [--traza]
"""

import hashlib
import os
import sys
import time

import ppmc
from ppmc import armar_cabecera, TAMANO_CABECERA, ORDEN_MAXIMO


def main():
    argumentos = [a for a in sys.argv[1:] if a != "--traza"]
    traza = "--traza" in sys.argv
    if len(argumentos) != 2:
        print("Uso: python compressor.py entrada.txt salida.tdi [--traza]")
        sys.exit(1)
    entrada, salida = argumentos

    if not os.path.isfile(entrada):
        print(f"Error: no existe el archivo '{entrada}'")
        sys.exit(1)

    with open(entrada, "rb") as f:
        original = f.read()

    # El total de O0 (hasta tamaño + 256) debe entrar en 1/4 del rango de 32 bits
    if len(original) > (1 << 30) - 256:
        print("Error: archivo demasiado grande para 32 bits de precisión (máx. ~1 GiB)")
        sys.exit(1)

    inicio = time.perf_counter()
    stream = ppmc.comprimir(original, traza=traza)
    cabecera = armar_cabecera(ORDEN_MAXIMO, original)
    tiempo = time.perf_counter() - inicio

    with open(salida, "wb") as f:
        f.write(cabecera + stream)

    tam_original = len(original)
    tam_comprimido = len(cabecera) + len(stream)
    print(f"Entrada:            {entrada}")
    print(f"Salida:             {salida}")
    print(f"Algoritmo:          PPM-C orden {ORDEN_MAXIMO} + codificación aritmética (32 bits)")
    print(f"Tamaño original:    {tam_original} bytes")
    print(f"Tamaño comprimido:  {tam_comprimido} bytes  (cabecera {TAMANO_CABECERA} + datos {len(stream)})")
    if tam_original > 0:
        print(f"Ratio:              {tam_original / tam_comprimido:.4f}")
        print(f"Ahorro:             {(1 - tam_comprimido / tam_original) * 100:.2f} %")
    print(f"Overhead cabecera:  {TAMANO_CABECERA / tam_comprimido * 100:.2f} %")
    print(f"Tiempo compresión:  {tiempo * 1000:.1f} ms")
    print(f"SHA-256 original:   {hashlib.sha256(original).hexdigest()}")


if __name__ == "__main__":
    main()
