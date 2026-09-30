"""
Ejercicio 7 - Detección de Errores: Códigos de Control (Checksum)

Valida un CUIT/CUIL de 11 dígitos utilizando el algoritmo
de dígito verificador basado en Módulo 11.
"""


PESOS = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]


def limpiar_cuit(cuit):
    """Elimina separadores habituales y espacios."""
    return cuit.replace("-", "").replace(" ", "").strip()


def calcular_digito_verificador(primeros_10):
    """Calcula el dígito verificador a partir de los primeros 10 dígitos."""
    suma = 0

    for i in range(10):
        suma += int(primeros_10[i]) * PESOS[i]

    resto = suma % 11
    digito = 11 - resto

    # Reglas del Módulo 11 para el dígito verificador.
    if digito == 11:
        digito = 0
    elif digito == 10:
        digito = 9

    return digito


def validar_cuit(cuit):
    """Devuelve True si el CUIT/CUIL tiene un dígito verificador correcto."""
    cuit = limpiar_cuit(cuit)

    if len(cuit) != 11:
        return False

    if not cuit.isdigit():
        return False

    primeros_10 = cuit[:10]
    digito_ingresado = int(cuit[10])

    digito_esperado = calcular_digito_verificador(primeros_10)

    return digito_ingresado == digito_esperado


def analizar_cuit(cuit):
    """Muestra el cálculo completo del dígito verificador."""
    cuit = limpiar_cuit(cuit)

    print("\n--- Análisis del CUIT/CUIL ---")
    print(f"Entrada: {cuit}")

    if len(cuit) != 11 or not cuit.isdigit():
        print("Inválida: debe contener exactamente 11 dígitos.")
        return

    primeros_10 = cuit[:10]
    digito_ingresado = int(cuit[10])

    suma = 0

    print("\nCálculo:")
    print("Dígitos : " + " ".join(primeros_10))
    print("Pesos   : " + " ".join(str(peso) for peso in PESOS))

    for i in range(10):
        producto = int(primeros_10[i]) * PESOS[i]
        suma += producto
        print(
            f"{primeros_10[i]} x {PESOS[i]} = {producto}"
        )

    resto = suma % 11
    digito_esperado = calcular_digito_verificador(primeros_10)

    print(f"\nSuma total: {suma}")
    print(f"Resto de la división por 11: {resto}")
    print(f"Dígito verificador esperado: {digito_esperado}")
    print(f"Dígito verificador ingresado: {digito_ingresado}")

    if digito_ingresado == digito_esperado:
        print("\nResultado: Válida")
    else:
        print("\nResultado: Inválida")


def main():
    while True:
        print("\n============================================================")
        print("EJERCICIO 7 - VALIDACIÓN DE CUIT/CUIL")
        print("============================================================")
        print("1. Validar un CUIT/CUIL")
        print("2. Salir")
        print("============================================================")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            cuit = input("Ingrese el CUIT/CUIL (con o sin guiones): ")
            analizar_cuit(cuit)

        elif opcion == "2":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
