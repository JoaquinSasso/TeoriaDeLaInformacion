import math


def calcular_entropia(probabilidades):
    """Calcula la entropía en bits/símbolo."""
    entropia = 0.0
    for p in probabilidades:
        if p > 0.0:
            entropia -= p * math.log2(p)
    return entropia


def calcular_probabilidades_salida(P_X, P_Y_dado_X):
    """Calcula P(Y) mediante el Teorema de la Probabilidad Total."""
    P_Y = [0.0] * 4

    for j in range(4):
        P_Y[j] = (
            P_X[0] * P_Y_dado_X[0][j]
            + P_X[1] * P_Y_dado_X[1][j]
        )

    return P_Y


def calcular_entropia_condicional(P_X, P_Y_dado_X):
    """Calcula H(Y|X)."""
    H_Y_dado_X = 0.0

    for i in range(2):
        H_Y_dado_X += P_X[i] * calcular_entropia(P_Y_dado_X[i])

    return H_Y_dado_X


def ingresar_matriz():
    """Solicita y valida la matriz de transición P(Y|X) de 2x4."""
    matriz = []
    tolerancia = 1e-9

    print("\nIngrese la matriz P(Y|X) de 2x4.")
    print("Cada fila debe tener 4 probabilidades entre 0 y 1.")
    print("La suma de cada fila debe ser 1.\n")

    for i in range(2):
        while True:
            try:
                valores = input(
                    f"Ingrese los 4 valores de la fila X={i}, "
                    "separados por espacios: "
                ).replace(",", " ").split()

                if len(valores) != 4:
                    print("Error: debe ingresar exactamente 4 valores.\n")
                    continue

                fila = [float(valor) for valor in valores]

                if any(p < 0.0 or p > 1.0 for p in fila):
                    print(
                        "Error: todas las probabilidades deben estar "
                        "entre 0 y 1.\n"
                    )
                    continue

                suma = sum(fila)

                # Tolerancia mínima para evitar problemas de representación
                # de números de punto flotante.
                if abs(suma - 1.0) > tolerancia:
                    print(
                        f"Error: la suma de la fila es {suma:.10f}. "
                        "Debe ser 1.0.\n"
                    )
                    continue

                matriz.append(fila)
                break

            except ValueError:
                print("Error: ingrese únicamente valores numéricos.\n")

    return matriz


def calcular_capacidad(P_Y_dado_X):
    """
    Busca exhaustivamente la capacidad del canal.

    Evalúa las 101 distribuciones:
    P(X=0) = 0.00, 0.01, ..., 1.00
    P(X=1) = 1 - P(X=0)
    """
    capacidad = -1.0
    p0_optimo = 0.0
    p1_optimo = 1.0

    for paso in range(101):
        p0 = paso / 100
        p1 = 1.0 - p0
        P_X = [p0, p1]

        P_Y = calcular_probabilidades_salida(
            P_X,
            P_Y_dado_X
        )

        H_Y = calcular_entropia(P_Y)

        H_Y_dado_X = calcular_entropia_condicional(
            P_X,
            P_Y_dado_X
        )

        I_XY = H_Y - H_Y_dado_X

        if I_XY > capacidad:
            capacidad = I_XY
            p0_optimo = p0
            p1_optimo = p1

    return capacidad, p0_optimo, p1_optimo


def mostrar_resultado(P_Y_dado_X, nombre_caso):
    """Calcula y muestra el resultado de un caso."""
    capacidad, p0_optimo, p1_optimo = calcular_capacidad(
        P_Y_dado_X
    )

    print("\n" + "=" * 60)
    print(f"RESULTADO - {nombre_caso}")
    print("=" * 60)

    print("\nMatriz P(Y|X):")
    print(f"X=0 -> {P_Y_dado_X[0]}")
    print(f"X=1 -> {P_Y_dado_X[1]}")

    print(f"\nCapacidad del canal: {capacidad:.6f} bits/símbolo")
    print(f"P(X=0) óptima:       {p0_optimo:.2f}")
    print(f"P(X=1) óptima:       {p1_optimo:.2f}")

    print("=" * 60)


def menu_pruebas():
    """
    Permite elegir entre ingresar la matriz manualmente
    o ejecutar los lotes de prueba.
    """
    casos_prueba = {
        "2": (
            "Caso 1 - Canal uniforme simétrico",
            [
                [0.7, 0.1, 0.1, 0.1],
                [0.1, 0.7, 0.1, 0.1]
            ]
        ),
        "3": (
            "Caso 2 - Canal determinista",
            [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0]
            ]
        ),
        "4": (
            "Caso 3 - Canal completamente ruidoso",
            [
                [0.25, 0.25, 0.25, 0.25],
                [0.25, 0.25, 0.25, 0.25]
            ]
        )
    }

    while True:
        print("\n" + "=" * 60)
        print("EJERCICIO 8 - CAPACIDAD DE CANAL")
        print("=" * 60)
        print("1. Ingresar matriz manualmente")
        print("2. Ejecutar lote de prueba 1")
        print("3. Ejecutar lote de prueba 2")
        print("4. Ejecutar lote de prueba 3")
        print("5. Ejecutar todos los lotes de prueba")
        print("6. Salir")
        print("=" * 60)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            matriz = ingresar_matriz()
            mostrar_resultado(
                matriz,
                "Canal ingresado manualmente"
            )

        elif opcion in casos_prueba:
            nombre, matriz = casos_prueba[opcion]
            mostrar_resultado(matriz, nombre)

        elif opcion == "5":
            for nombre, matriz in casos_prueba.values():
                mostrar_resultado(matriz, nombre)

        elif opcion == "6":
            print("\nPrograma finalizado.")
            break

        else:
            print("\nError: opción inválida.")

        input("\nPresione ENTER para volver al menú...")


def main():
    menu_pruebas()


if __name__ == "__main__":
    main()
