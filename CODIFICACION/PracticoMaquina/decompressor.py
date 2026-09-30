"""
Uso:  python decompressor.py entrada.tdi reconstruido.txt
"""

import hashlib
import os
import sys
import time

import ppmc
from ppmc import leer_cabecera, crc32, ErrorDeFormato, ORDEN_MAXIMO


def main():
    if len(sys.argv) != 3:
        print("Uso: python decompressor.py entrada.tdi reconstruido.txt")
        sys.exit(1)
    entrada, salida = sys.argv[1], sys.argv[2]

    if not os.path.isfile(entrada):
        print(f"Error: no existe el archivo '{entrada}'")
        sys.exit(1)

    with open(entrada, "rb") as f:
        contenido = f.read()

    try:
        cabecera = leer_cabecera(contenido)
        if cabecera["orden"] != ORDEN_MAXIMO:
            raise ErrorDeFormato(f"orden {cabecera['orden']} no soportado")
        if cabecera["tamano"] > 0 and len(cabecera["datos"]) == 0:
            raise ErrorDeFormato("faltan los datos comprimidos")
    except ErrorDeFormato as error:
        print(f"Error: {error}")
        sys.exit(1)

    inicio = time.perf_counter()
    try:
        reconstruido = ppmc.descomprimir(cabecera["datos"], cabecera["tamano"])
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)
    tiempo = time.perf_counter() - inicio

    with open(salida, "wb") as f:
        f.write(reconstruido)

    integro = crc32(reconstruido) == cabecera["crc32"]
    print(f"Entrada:              {entrada}")
    print(f"Salida:               {salida}")
    print(f"Tamaño reconstruido:  {len(reconstruido)} bytes")
    print(f"Tiempo descompresión: {tiempo * 1000:.1f} ms")
    print(f"SHA-256 reconstruido: {hashlib.sha256(reconstruido).hexdigest()}")
    print(f"Integridad (CRC-32):  {'OK' if integro else 'FALLÓ: el archivo está corrupto'}")
    if not integro:
        sys.exit(2)


if __name__ == "__main__":
    main()
