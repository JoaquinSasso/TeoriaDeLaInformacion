"""
Ejercicio 6 - Medición de Distancia entre Cadenas

Implementa:
- Distancia de Hamming
- Distancia de Levenshtein
- Ejemplos de ejecución
- Una heurística sencilla de comparación de texto
"""


def distancia_hamming(cadena1, cadena2):
    """Devuelve la cantidad de posiciones diferentes.

    La distancia de Hamming solo se puede aplicar directamente
    a cadenas de igual longitud.
    """
    if len(cadena1) != len(cadena2):
        raise ValueError("La distancia de Hamming requiere cadenas de igual longitud.")

    distancia = 0

    for i in range(len(cadena1)):
        if cadena1[i] != cadena2[i]:
            distancia += 1

    return distancia


def distancia_levenshtein(cadena1, cadena2):
    """Calcula la distancia mínima de edición entre dos cadenas.

    Operaciones permitidas:
    - inserción
    - eliminación
    - sustitución
    """
    filas = len(cadena1) + 1
    columnas = len(cadena2) + 1

    matriz = [[0] * columnas for _ in range(filas)]

    # Transformar una cadena vacía en cadena2 requiere inserciones.
    for j in range(columnas):
        matriz[0][j] = j

    # Transformar cadena1 en una cadena vacía requiere eliminaciones.
    for i in range(filas):
        matriz[i][0] = i

    for i in range(1, filas):
        for j in range(1, columnas):
            if cadena1[i - 1] == cadena2[j - 1]:
                costo_sustitucion = 0
            else:
                costo_sustitucion = 1

            insercion = matriz[i][j - 1] + 1
            eliminacion = matriz[i - 1][j] + 1
            sustitucion = matriz[i - 1][j - 1] + costo_sustitucion

            matriz[i][j] = min(insercion, eliminacion, sustitucion)

    return matriz[-1][-1]


def normalizar_texto(texto):
    """Normalización básica para comparar textos.

    Convierte a minúsculas y elimina espacios de los extremos.
    """
    return texto.strip().lower()


def comparar_cadenas(cadena1, cadena2):
    """Muestra ambas distancias y una conclusión sencilla."""
    print("\n--- Comparación ---")
    print(f"Cadena 1: {cadena1}")
    print(f"Cadena 2: {cadena2}")

    if len(cadena1) == len(cadena2):
        hamming = distancia_hamming(cadena1, cadena2)
        print(f"Distancia de Hamming: {hamming}")
    else:
        print("Distancia de Hamming: no aplicable (longitudes diferentes).")

    levenshtein = distancia_levenshtein(cadena1, cadena2)
    print(f"Distancia de Levenshtein: {levenshtein}")

    if levenshtein == 0:
        print("Resultado: las cadenas son iguales.")
    elif levenshtein <= 2:
        print("Resultado: las cadenas son muy similares.")
    else:
        print("Resultado: las cadenas presentan varias diferencias.")


def ejecutar_ejemplos():
    print("\n============================================================")
    print("EJERCICIO 6 - DISTANCIA ENTRE CADENAS")
    print("============================================================")

    print("\n1. Ejemplo solicitado: 'Juan Perez' vs 'Jaun Perez'")
    comparar_cadenas("Juan Perez", "Jaun Perez")

    print("\n2. Ejemplo con desfase/longitud diferente:")
    comparar_cadenas("Juan Perez", "Juaan Perez")

    print("\n3. Ejemplo del práctico:")
    comparar_cadenas("Horacio López", "Oracio López")


def main():
    while True:
        print("\n============================================================")
        print("EJERCICIO 6 - DISTANCIA ENTRE CADENAS")
        print("============================================================")
        print("1. Comparar dos cadenas")
        print("2. Ejecutar ejemplos del práctico")
        print("3. Salir")
        print("============================================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            cadena1 = input("Ingrese la primera cadena: ")
            cadena2 = input("Ingrese la segunda cadena: ")
            comparar_cadenas(cadena1, cadena2)

        elif opcion == "2":
            ejecutar_ejemplos()

        elif opcion == "3":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
