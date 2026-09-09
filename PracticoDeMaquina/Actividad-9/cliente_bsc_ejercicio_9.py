import math
import random
import socket
import struct


HOST = "127.0.0.1"
PUERTO = 5555

# Longitudes solicitadas para analizar la convergencia del BER.
LONGITUDES = [100, 10000, 1000000]

# Cantidad de tramas de cada longitud.
CANTIDAD_TRAMAS = 5

# Valor teórico de p utilizado en la Fase 2.
# Este valor se obtiene experimentalmente en la Fase 1.
# Para el servidor provisto, el BER converge aproximadamente a 0.06097.
P_ERROR_TEORICO = 0.06097


def enviar_mensaje(sock, mensaje):
    """Envía un mensaje con su longitud en un encabezado de 4 bytes."""
    datos = mensaje.encode("ascii")
    encabezado = struct.pack("!I", len(datos))
    sock.sendall(encabezado + datos)


def recibir_exactamente(sock, cantidad):
    """Recibe exactamente la cantidad de bytes indicada."""
    datos = bytearray()

    while len(datos) < cantidad:
        bloque = sock.recv(cantidad - len(datos))

        if not bloque:
            raise ConnectionError("El servidor cerró la conexión.")

        datos.extend(bloque)

    return bytes(datos)


def recibir_mensaje(sock):
    """Recibe un mensaje utilizando el protocolo del servidor."""
    encabezado = recibir_exactamente(sock, 4)
    longitud = struct.unpack("!I", encabezado)[0]

    datos = recibir_exactamente(sock, longitud)

    return datos.decode("ascii")


def generar_trama(longitud):
    """Genera una trama binaria aleatoria de la longitud indicada."""
    return "".join(random.choice("01") for _ in range(longitud))


def calcular_errores(trama_original, trama_recibida):
    """Cuenta los bits que fueron modificados por el canal."""
    errores = 0

    for original, recibido in zip(trama_original, trama_recibida):
        if original != recibido:
            errores += 1

    return errores


def calcular_ber(errores, cantidad_bits):
    """Calcula la Bit Error Rate (BER)."""
    if cantidad_bits == 0:
        return 0.0

    return errores / cantidad_bits


def calcular_entropia(probabilidades):
    """Calcula la entropía de Shannon en bits/símbolo."""
    entropia = 0.0

    for p in probabilidades:
        if p > 0.0:
            entropia -= p * math.log2(p)

    return entropia


def realizar_pruebas(sock):
    """
    Ejecuta la Fase 1.

    Se generan y transmiten tramas de 100, 10.000 y 1.000.000 bits.
    Para cada longitud se calcula el BER empírico y se conserva la
    trama original más grande para utilizarla posteriormente en la
    Fase 2.
    """
    resultados = []
    trama_mas_grande = None

    for longitud in LONGITUDES:
        errores_totales = 0
        bits_totales = 0

        print("\n" + "-" * 65)
        print(f"Longitud de trama: {longitud} bits")
        print(f"Cantidad de tramas: {CANTIDAD_TRAMAS}")

        for prueba in range(1, CANTIDAD_TRAMAS + 1):
            trama_original = generar_trama(longitud)

            enviar_mensaje(sock, trama_original)
            trama_recibida = recibir_mensaje(sock)

            errores = calcular_errores(
                trama_original,
                trama_recibida
            )

            errores_totales += errores
            bits_totales += longitud

            ber_trama = calcular_ber(errores, longitud)

            print(
                f"  Prueba {prueba}: "
                f"errores = {errores}, "
                f"BER = {ber_trama:.6f}"
            )

            # Se conserva la última trama de la mayor longitud.
            if longitud == max(LONGITUDES):
                trama_mas_grande = trama_original

        ber = calcular_ber(
            errores_totales,
            bits_totales
        )

        resultados.append(
            (longitud, errores_totales, bits_totales, ber)
        )

        print(f"  BER acumulado = {ber:.6f}")

    return resultados, trama_mas_grande


def mostrar_resultados_fase_1(resultados):
    """Muestra el BER acumulado para cada longitud de trama."""
    print("\n" + "=" * 65)
    print("FASE 1 - TRANSMISIÓN Y BER EMPÍRICO")
    print("=" * 65)

    print(
        f"{'Bits':>12}"
        f"{'Errores':>12}"
        f"{'BER':>15}"
    )

    for longitud, errores, bits, ber in resultados:
        print(
            f"{bits:>12}"
            f"{errores:>12}"
            f"{ber:>15.6f}"
        )

    errores_totales = sum(resultado[1] for resultado in resultados)
    bits_totales = sum(resultado[2] for resultado in resultados)

    ber_total = calcular_ber(
        errores_totales,
        bits_totales
    )

    print("-" * 65)
    print(f"BER empírico total: {ber_total:.6f}")
    print(f"Valor teórico configurado: {P_ERROR_TEORICO:.6f}")

    return ber_total


def calcular_probabilidades_fuente(trama):
    """Calcula P(X=0) y P(X=1) a partir de la trama original."""
    cantidad_ceros = trama.count("0")
    cantidad_unos = trama.count("1")
    total = len(trama)

    p0 = cantidad_ceros / total
    p1 = cantidad_unos / total

    return p0, p1


def calcular_informacion_mutua(p0, p1, p_error):
    """
    Calcula I(X;Y) = H(Y) - H(Y|X) para el BSC.
    """

    # Matriz del canal:
    #
    #             Y=0       Y=1
    # X=0       1-p         p
    # X=1        p         1-p

    py0 = (
        p0 * (1.0 - p_error)
        + p1 * p_error
    )

    py1 = (
        p0 * p_error
        + p1 * (1.0 - p_error)
    )

    H_Y = calcular_entropia([py0, py1])

    H_Y_dado_X0 = calcular_entropia(
        [1.0 - p_error, p_error]
    )

    H_Y_dado_X1 = calcular_entropia(
        [p_error, 1.0 - p_error]
    )

    H_Y_dado_X = (
        p0 * H_Y_dado_X0
        + p1 * H_Y_dado_X1
    )

    return H_Y - H_Y_dado_X


def calcular_capacidad(p_error):
    """Calcula C = 1 - H(p) para un BSC."""
    H_p = calcular_entropia(
        [p_error, 1.0 - p_error]
    )

    return 1.0 - H_p


def mostrar_fase_2(trama, p_error):
    """Realiza y muestra todos los cálculos de la Fase 2."""

    print("\n" + "=" * 65)
    print("FASE 2 - MODELADO MATEMÁTICO Y CAPACIDAD DEL CANAL")
    print("=" * 65)

    # 1. Matriz del canal
    print("\n1. Matriz del canal P(Y|X):")
    print("             Y=0          Y=1")
    print(
        f"X=0       {1-p_error:.6f}     {p_error:.6f}"
    )
    print(
        f"X=1       {p_error:.6f}     {1-p_error:.6f}"
    )

    # 2. Probabilidades de la fuente
    p0, p1 = calcular_probabilidades_fuente(trama)

    print("\n2. Probabilidades de la fuente:")
    print(f"P(X=0) = {p0:.6f}")
    print(f"P(X=1) = {p1:.6f}")

    # 3. Información mutua
    I_XY = calcular_informacion_mutua(
        p0,
        p1,
        p_error
    )

    print("\n3. Información Mutua:")
    print(f"I(X;Y) = {I_XY:.6f} bits/símbolo")

    # 4. Capacidad
    capacidad = calcular_capacidad(p_error)

    print("\n4. Capacidad del canal:")
    print(f"C = {capacidad:.6f} bits/símbolo")

    # 5. Análisis de maximización
    diferencia_porcentual = (
        abs(capacidad - I_XY) / capacidad * 100.0
        if capacidad > 0.0
        else 0.0
    )

    print("\n5. Análisis de maximización:")
    print(f"Diferencia respecto de C: {diferencia_porcentual:.2f}%")

    if diferencia_porcentual <= 5.0:
        print(
            "I(X;Y) se encuentra dentro del margen del 5% "
            "respecto de la capacidad."
        )
    elif diferencia_porcentual <= 10.0:
        print(
            "I(X;Y) se encuentra dentro del margen del 5-10% "
            "respecto de la capacidad."
        )
    else:
        print(
            "I(X;Y) no se encuentra dentro del margen "
            "de error permitido del 5-10%."
        )

    print(
        "\nPara maximizar la capacidad de un BSC, la fuente "
        "debe ser equiprobable:"
    )
    print("P(X=0) = 0.5")
    print("P(X=1) = 0.5")

    if abs(p0 - 0.5) <= 0.05:
        print(
            "La trama utilizada tiene una distribución "
            "aproximadamente equiprobable y por eso I(X;Y) "
            "se aproxima a C."
        )
    else:
        print(
            "La trama utilizada no es equiprobable, por lo "
            "que I(X;Y) se encuentra por debajo de C."
        )

    return I_XY, capacidad


def convertir_a_binario(texto):
    """Convierte texto ASCII a una cadena de bits."""
    datos = texto.encode("ascii")

    bits = ""

    for byte in datos:
        bits += format(byte, "08b")

    return bits


def convertir_a_texto(bits):
    """Convierte una cadena de bits de 8 en 8 a texto."""
    texto = ""

    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]

        if len(byte) == 8:
            texto += chr(int(byte, 2))

    return texto


def probar_mensaje_texto(sock):
    """
    Fase 1, punto 5:
    transmite una frase como bits y convierte nuevamente
    la respuesta a texto para mostrar la alteración.
    """
    texto_original = input(
        "\nIngrese una frase ASCII para transmitir: "
    )

    if not texto_original:
        print("No se ingresó ningún texto.")
        return

    try:
        mensaje_binario = convertir_a_binario(texto_original)
    except UnicodeEncodeError:
        print(
            "Error: para esta prueba utilice únicamente "
            "caracteres ASCII."
        )
        return

    enviar_mensaje(sock, mensaje_binario)

    respuesta_binaria = recibir_mensaje(sock)

    texto_recibido = convertir_a_texto(
        respuesta_binaria
    )

    print("\nMensaje original:")
    print(texto_original)

    print("\nMensaje recibido:")
    print(texto_recibido)


def main():
    print("=" * 65)
    print("CLIENTE - CANAL BINARIO SIMÉTRICO (BSC)")
    print("=" * 65)

    try:
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.connect((HOST, PUERTO))

            print(
                f"\nConectado al servidor "
                f"{HOST}:{PUERTO}"
            )

            # FASE 1
            resultados, trama_original = realizar_pruebas(
                sock
            )

            ber_empirico = mostrar_resultados_fase_1(
                resultados
            )

            print(
                "\nEl BER empírico permite estimar la "
                "probabilidad de error p."
            )
            print(
                f"Estimación empírica global: {ber_empirico:.6f}"
            )

            # FASE 2
            # Se utiliza la misma trama original de 1.000.000
            # de bits que fue transmitida en la Fase 1.
            mostrar_fase_2(
                trama_original,
                P_ERROR_TEORICO
            )

            # FASE 1, punto 5
            probar_mensaje_texto(sock)

    except ConnectionRefusedError:
        print(
            "\nNo se pudo conectar al servidor."
        )
        print(
            "Ejecute primero servidor_bsc.py "
            "en el puerto 5555."
        )

    except ConnectionError as error:
        print(f"\nError de conexión: {error}")


if __name__ == "__main__":
    main()
