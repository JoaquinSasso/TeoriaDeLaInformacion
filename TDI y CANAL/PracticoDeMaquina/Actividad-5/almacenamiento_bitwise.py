import csv
import json
import os
import struct


# ==============================================================================
# DATOS DE PRUEBA: 20 PERSONAS CON DATOS REALISTAS
# ==============================================================================

PERSONAS_EJEMPLO = [
    {
        "apellido_nombre": "Gómez, Juan Carlos",
        "direccion": "Av. San Martín 1420, Rosario",
        "dni": 34567890,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": False,
        "vivienda_propia": True,
        "obra_social": True,
        "trabaja": True,
        "tiene_vehiculo": True,
        "cuenta_bancaria": True
    },
    {
        "apellido_nombre": "Rodríguez, Lucía Elena",
        "direccion": "Calle Córdoba 850, Funes",
        "dni": 41234567,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": True,
        "vivienda_propia": False,
        "obra_social": True,
        "trabaja": True,
        "tiene_vehiculo": False,
        "cuenta_bancaria": True
    },
    {
        "apellido_nombre": "Fernández, Martín",
        "direccion": "Bv. Oroño 230, Rosario",
        "dni": 28901234,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": True,
        "vivienda_propia": True,
        "obra_social": True,
        "trabaja": True,
        "tiene_vehiculo": True,
        "cuenta_bancaria": True
    },
    {
        "apellido_nombre": "Pérez, María Soledad",
        "direccion": "Urquiza 3110, Santa Fe",
        "dni": 38456123,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": False,
        "vivienda_propia": False,
        "obra_social": False,
        "trabaja": True,
        "tiene_vehiculo": False,
        "cuenta_bancaria": False
    },
    {
        "apellido_nombre": "López, Matías Agustín",
        "direccion": "Mitre 450, Rafaela",
        "dni": 43567891,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": True,
        "vivienda_propia": False,
        "obra_social": True,
        "trabaja": False,
        "tiene_vehiculo": False,
        "cuenta_bancaria": True
    },
    {
        "apellido_nombre": "Díaz, Valentina",
        "direccion": "Pellegrini 1650, Rosario",
        "dni": 39876543,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": False,
        "vivienda_propia": True,
        "obra_social": True,
        "trabaja": True,
        "tiene_vehiculo": True,
        "cuenta_bancaria": True
    },
    {
        "apellido_nombre": "Sosa, Carlos Alberto",
        "direccion": "Rivadavia 120, Villa Gobernador Gálvez",
        "dni": 22345678,
        "estudios_primarios": True,
        "estudios_secundarios": False,
        "estudios_universitarios": False,
        "vivienda_propia": True,
        "obra_social": False,
        "trabaja": True,
        "tiene_vehiculo": True,
        "cuenta_bancaria": False
    },
    {
        "apellido_nombre": "Álvarez, Camila Rocío",
        "direccion": "Salta 2450, Rosario",
        "dni": 44123890,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": True,
        "vivienda_propia": False,
        "obra_social": True,
        "trabaja": False,
        "tiene_vehiculo": False,
        "cuenta_bancaria": True
    },
    {
        "apellido_nombre": "Torres, Jorge Daniel",
        "direccion": "San Lorenzo 780, San Lorenzo",
        "dni": 31234987,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": False,
        "vivienda_propia": True,
        "obra_social": True,
        "trabaja": True,
        "tiene_vehiculo": True,
        "cuenta_bancaria": True
    },
    {
        "apellido_nombre": "Romero, Ana Paula",
        "direccion": "Laprida 1120, Rosario",
        "dni": 36789456,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": True,
        "vivienda_propia": False,
        "obra_social": True,
        "trabaja": True,
        "tiene_vehiculo": False,
        "cuenta_bancaria": True
    },
    {
        "apellido_nombre": "Suárez, Franco Gastón",
        "direccion": "Mendoza 3940, Rosario",
        "dni": 42567123,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": False,
        "vivienda_propia": False,
        "obra_social": False,
        "trabaja": True,
        "tiene_vehiculo": True,
        "cuenta_bancaria": False
    },
    {
        "apellido_nombre": "Benítez, Marta Susana",
        "direccion": "España 630, Granadero Baigorria",
        "dni": 18234567,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": False,
        "vivienda_propia": True,
        "obra_social": True,
        "trabaja": False,
        "tiene_vehiculo": False,
        "cuenta_bancaria": True
    },
    {
        "apellido_nombre": "Castro, Lucas Ezequiel",
        "direccion": "Sarmiento 1820, Rosario",
        "dni": 40345678,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": True,
        "vivienda_propia": False,
        "obra_social": True,
        "trabaja": True,
        "tiene_vehiculo": True,
        "cuenta_bancaria": True
    },
    {
        "apellido_nombre": "Acosta, Silvina Beatriz",
        "direccion": "Bv. 27 de Febrero 2150, Rosario",
        "dni": 32678912,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": False,
        "vivienda_propia": True,
        "obra_social": True,
        "trabaja": True,
        "tiene_vehiculo": False,
        "cuenta_bancaria": True
    },
    {
        "apellido_nombre": "Ortiz, Gonzalo",
        "direccion": "Alvear 560, Venado Tuerto",
        "dni": 37890123,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": True,
        "vivienda_propia": True,
        "obra_social": True,
        "trabaja": True,
        "tiene_vehiculo": True,
        "cuenta_bancaria": True
    },
    {
        "apellido_nombre": "Morales, Florencia Inés",
        "direccion": "Paraguay 940, Rosario",
        "dni": 45123456,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": False,
        "vivienda_propia": False,
        "obra_social": False,
        "trabaja": False,
        "tiene_vehiculo": False,
        "cuenta_bancaria": False
    },
    {
        "apellido_nombre": "Giménez, Héctor Raúl",
        "direccion": "Av. Wheelwright 1780, Rosario",
        "dni": 25456789,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": True,
        "vivienda_propia": True,
        "obra_social": True,
        "trabaja": True,
        "tiene_vehiculo": True,
        "cuenta_bancaria": True
    },
    {
        "apellido_nombre": "Vázquez, Julieta",
        "direccion": "Dorrego 1410, Rosario",
        "dni": 41890234,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": True,
        "vivienda_propia": False,
        "obra_social": True,
        "trabaja": True,
        "tiene_vehiculo": False,
        "cuenta_bancaria": True
    },
    {
        "apellido_nombre": "Ramos, Diego Fernando",
        "direccion": "Ayacucho 5520, Rosario",
        "dni": 33123789,
        "estudios_primarios": True,
        "estudios_secundarios": False,
        "estudios_universitarios": False,
        "vivienda_propia": False,
        "obra_social": False,
        "trabaja": True,
        "tiene_vehiculo": True,
        "cuenta_bancaria": False
    },
    {
        "apellido_nombre": "Herrera, Micaela Sol",
        "direccion": "Bv. Rondeau 2980, Rosario",
        "dni": 43789012,
        "estudios_primarios": True,
        "estudios_secundarios": True,
        "estudios_universitarios": False,
        "vivienda_propia": True,
        "obra_social": True,
        "trabaja": True,
        "tiene_vehiculo": False,
        "cuenta_bancaria": True
    }
]

CAMPOS_BOOLEANOS = [
    "estudios_primarios",
    "estudios_secundarios",
    "estudios_universitarios",
    "vivienda_propia",
    "obra_social",
    "trabaja",
    "tiene_vehiculo",
    "cuenta_bancaria"
]


# ==============================================================================
# OPERACIONES A NIVEL DE BITS (BITWISE)
# ==============================================================================

def empaquetar_booleanos(b0, b1, b2, b3, b4, b5, b6, b7):
    """
    Empaqueta 8 valores booleanos en 1 único byte (uint8) utilizando
    operadores a nivel de bits (| y <<).

    Distribución de bits dentro del byte:
      Bit 7 (MSB): estudios_primarios
      Bit 6:       estudios_secundarios
      Bit 5:       estudios_universitarios
      Bit 4:       vivienda_propia
      Bit 3:       obra_social
      Bit 2:       trabaja
      Bit 1:       tiene_vehiculo
      Bit 0 (LSB): cuenta_bancaria
    """
    byte_empaquetado = 0
    byte_empaquetado |= (int(bool(b0)) & 1) << 7
    byte_empaquetado |= (int(bool(b1)) & 1) << 6
    byte_empaquetado |= (int(bool(b2)) & 1) << 5
    byte_empaquetado |= (int(bool(b3)) & 1) << 4
    byte_empaquetado |= (int(bool(b4)) & 1) << 3
    byte_empaquetado |= (int(bool(b5)) & 1) << 2
    byte_empaquetado |= (int(bool(b6)) & 1) << 1
    byte_empaquetado |= (int(bool(b7)) & 1)
    return byte_empaquetado


def desempaquetar_booleanos(byte_empaquetado):
    """
    Desempaqueta 1 byte (uint8) en una lista de 8 booleanos usando
    los operadores a nivel de bits >> (desplazamiento) y & (máscara).
    """
    return [
        bool((byte_empaquetado >> 7) & 1),
        bool((byte_empaquetado >> 6) & 1),
        bool((byte_empaquetado >> 5) & 1),
        bool((byte_empaquetado >> 4) & 1),
        bool((byte_empaquetado >> 3) & 1),
        bool((byte_empaquetado >> 2) & 1),
        bool((byte_empaquetado >> 1) & 1),
        bool(byte_empaquetado & 1)
    ]


# ==============================================================================
# MANEJO DE CADENAS DINÁMICAS (PASCAL STRINGS)
# ==============================================================================

def serializar_pascal_string(texto):
    """
    Serializa una cadena de texto en formato Pascal String:
    - Byte 0: longitud L en 1 byte (uint8 sin signo, valores 0 a 255).
    - Bytes 1 a L: el texto codificado en UTF-8.
    """
    bytes_texto = texto.encode("utf-8")
    longitud = len(bytes_texto)
    if longitud > 255:
        raise ValueError(f"La cadena supera los 255 bytes permitidos por Pascal String ({longitud} bytes).")
    # Pack de 1 byte sin signo (!B) seguido de los bytes del texto
    return struct.pack("!B", longitud) + bytes_texto


def deserializar_pascal_string(stream):
    """
    Lee una Pascal String desde un stream de archivo binario abierto en modo 'rb'.
    Retorna la cadena decodificada en UTF-8, o None si se alcanzó el fin de archivo.
    """
    byte_longitud = stream.read(1)
    if not byte_longitud:
        return None
    longitud = struct.unpack("!B", byte_longitud)[0]
    bytes_texto = stream.read(longitud)
    return bytes_texto.decode("utf-8")


# ==============================================================================
# GUARDADO DE ARCHIVOS
# ==============================================================================

def guardar_json(personas, ruta):
    """Guarda los registros en formato texto estructurado JSON."""
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(personas, f, ensure_ascii=False, indent=2)


def guardar_csv(personas, ruta):
    """Guarda los registros en formato texto plano CSV con encabezado."""
    columnas = ["apellido_nombre", "direccion", "dni"] + CAMPOS_BOOLEANOS
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        writer.writeheader()
        for p in personas:
            fila = dict(p)
            for campo in CAMPOS_BOOLEANOS:
                fila[campo] = "True" if p[campo] else "False"
            writer.writerow(fila)


def guardar_binario(personas, ruta):
    """
    Guarda los registros en formato binario optimizado:
    Por cada persona:
      1. Pascal string: Apellido y Nombre (1 byte longitud + bytes UTF-8)
      2. Pascal string: Dirección (1 byte longitud + bytes UTF-8)
      3. Entero uint32: DNI (4 bytes, big-endian '!I')
      4. Entero uint8:  8 booleanos empaquetados en 1 solo byte bitwise (!B)
    """
    with open(ruta, "wb") as f:
        for p in personas:
            # 1. Apellido y Nombre (Pascal String)
            f.write(serializar_pascal_string(p["apellido_nombre"]))

            # 2. Dirección (Pascal String)
            f.write(serializar_pascal_string(p["direccion"]))

            # 3. DNI (4 bytes uint32)
            f.write(struct.pack("!I", int(p["dni"])))

            # 4. 8 Booleanos (1 byte uint8 bitwise)
            byte_flags = empaquetar_booleanos(
                p["estudios_primarios"],
                p["estudios_secundarios"],
                p["estudios_universitarios"],
                p["vivienda_propia"],
                p["obra_social"],
                p["trabaja"],
                p["tiene_vehiculo"],
                p["cuenta_bancaria"]
            )
            f.write(struct.pack("!B", byte_flags))


# ==============================================================================
# LECTURA Y DESEMPAQUETADO DE ARCHIVOS
# ==============================================================================

def leer_json(ruta):
    """Lee y deserializa los registros desde el archivo JSON."""
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def leer_binario(ruta):
    """
    Lee y desempaqueta los registros desde el archivo binario:
    Lee campo por campo utilizando Pascal Strings, desempaqueta el uint32
    y recupera los 8 booleanos mediante operaciones bitwise.
    """
    registros = []
    with open(ruta, "rb") as f:
        while True:
            # 1. Leer Apellido y Nombre (Pascal String)
            apellido_nombre = deserializar_pascal_string(f)
            if apellido_nombre is None:
                break  # Fin de archivo alcanzado limpiamente

            # 2. Leer Dirección (Pascal String)
            direccion = deserializar_pascal_string(f)

            # 3. Leer DNI (4 bytes uint32)
            dni_bytes = f.read(4)
            dni = struct.unpack("!I", dni_bytes)[0]

            # 4. Leer byte de booleanos y desempaquetar con operadores de bits
            flags_byte = f.read(1)
            flags = struct.unpack("!B", flags_byte)[0]
            valores_bool = desempaquetar_booleanos(flags)

            persona = {
                "apellido_nombre": apellido_nombre,
                "direccion": direccion,
                "dni": dni,
                "estudios_primarios": valores_bool[0],
                "estudios_secundarios": valores_bool[1],
                "estudios_universitarios": valores_bool[2],
                "vivienda_propia": valores_bool[3],
                "obra_social": valores_bool[4],
                "trabaja": valores_bool[5],
                "tiene_vehiculo": valores_bool[6],
                "cuenta_bancaria": valores_bool[7],
                "_byte_crudo_flags": flags  # Para inspección didáctica
            }
            registros.append(persona)

    return registros


# ==============================================================================
# VISUALIZACIÓN Y COMPARATIVA
# ==============================================================================

def mostrar_registros(personas, es_binario=False):
    """Muestra en pantalla de forma clara y ordenada los registros leídos."""
    print("=" * 80)
    print(f"REGISTROS RECUPERADOS ({len(personas)} personas)")
    print("=" * 80)

    for i, p in enumerate(personas, 1):
        print(f"[{i:02d}] {p['apellido_nombre']} | DNI: {p['dni']} | Dirección: {p['direccion']}")
        bools_str = (
            f"  Primaria: {'Sí' if p['estudios_primarios'] else 'No'} | "
            f"Secundaria: {'Sí' if p['estudios_secundarios'] else 'No'} | "
            f"Universidad: {'Sí' if p['estudios_universitarios'] else 'No'} | "
            f"Vivienda: {'Sí' if p['vivienda_propia'] else 'No'}\n"
            f"  Obra Social: {'Sí' if p['obra_social'] else 'No'} | "
            f"Trabaja: {'Sí' if p['trabaja'] else 'No'} | "
            f"Vehículo: {'Sí' if p['tiene_vehiculo'] else 'No'} | "
            f"Cuenta Bancaria: {'Sí' if p['cuenta_bancaria'] else 'No'}"
        )
        print(bools_str)
        if es_binario and "_byte_crudo_flags" in p:
            flags = p["_byte_crudo_flags"]
            bin_str = format(flags, "08b")
            print(f"  -> Byte empaquetado: 0x{flags:02X} (binario: {bin_str}b)")
        print("-" * 80)


def comparar_tamanos(ruta_json, ruta_csv, ruta_bin):
    """Compara el tamaño en disco de los 3 formatos y muestra estadísticas."""
    for r in [ruta_json, ruta_csv, ruta_bin]:
        if not os.path.exists(r):
            print(f"Error: No existe el archivo {r}. Por favor generalos primero (Opción 1).")
            return

    tam_json = os.path.getsize(ruta_json)
    tam_csv = os.path.getsize(ruta_csv)
    tam_bin = os.path.getsize(ruta_bin)
    cant_personas = len(PERSONAS_EJEMPLO)

    ahorro_vs_json = ((tam_json - tam_bin) / tam_json) * 100.0
    ahorro_vs_csv = ((tam_csv - tam_bin) / tam_csv) * 100.0

    print("\n" + "=" * 75)
    print("COMPARATIVA DE TAMAÑOS EN DISCO (20 PERSONAS)")
    print("=" * 75)
    print(f"{'Formato':<25} {'Tamaño Total':<18} {'Bytes / Persona':<18} {'Reducción':<12}")
    print("-" * 75)
    print(f"{'Texto JSON (.json)':<25} {tam_json:>6} bytes       {tam_json/cant_personas:>8.1f} B/persona     Base (0.0%)")
    print(f"{'Texto CSV (.csv)':<25} {tam_csv:>6} bytes       {tam_csv/cant_personas:>8.1f} B/persona     -{(tam_json-tam_csv)/tam_json*100:>5.1f}%")
    print(f"{'Binario Bitwise (.bin)':<25} {tam_bin:>6} bytes       {tam_bin/cant_personas:>8.1f} B/persona     -{ahorro_vs_json:>5.1f}%")
    print("=" * 75)

    print("\nDetalle de ahorro del formato binario:")
    print(f"  * Respecto a JSON: {tam_bin} bytes vs {tam_json} bytes -> Ahorro del {ahorro_vs_json:.2f}%")
    print(f"  * Respecto a CSV:  {tam_bin} bytes vs {tam_csv} bytes -> Ahorro del {ahorro_vs_csv:.2f}%")
    print(f"  * Factor de compresión: El binario es {(tam_json / tam_bin):.2f}x más chico que JSON y {(tam_csv / tam_bin):.2f}x más chico que CSV.\n")


# ==============================================================================
# MENÚ PRINCIPAL
# ==============================================================================

def menu():
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_json = os.path.join(directorio_script, "personas.json")
    ruta_csv = os.path.join(directorio_script, "personas.csv")
    ruta_bin = os.path.join(directorio_script, "personas.bin")

    while True:
        print("\n" + "=" * 65)
        print("ACTIVIDAD 5: ALMACENAMIENTO Y EMPAQUETADO BITWISE")
        print("=" * 65)
        print("1. Generar y guardar archivos (JSON, CSV y Binario)")
        print("2. Leer y mostrar registros desde archivo de texto (JSON)")
        print("3. Leer, desempaquetar (Bitwise) y mostrar desde archivo binario (.bin)")
        print("4. Comparar tamaños de archivo y estadísticas de almacenamiento")
        print("5. Ejecutar demostración completa (generar, leer y comparar)")
        print("6. Salir")
        print("=" * 65)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\nGenerando archivos...")
            guardar_json(PERSONAS_EJEMPLO, ruta_json)
            guardar_csv(PERSONAS_EJEMPLO, ruta_csv)
            guardar_binario(PERSONAS_EJEMPLO, ruta_bin)
            print(f" Archivo JSON generado:    {ruta_json}")
            print(f" Archivo CSV generado:     {ruta_csv}")
            print(f" Archivo Binario generado: {ruta_bin}")

        elif opcion == "2":
            if not os.path.exists(ruta_json):
                print(f"\nNo se encontró {ruta_json}. Generalo con la Opción 1.")
            else:
                registros = leer_json(ruta_json)
                mostrar_registros(registros, es_binario=False)

        elif opcion == "3":
            if not os.path.exists(ruta_bin):
                print(f"\nNo se encontró {ruta_bin}. Generalo con la Opción 1.")
            else:
                registros = leer_binario(ruta_bin)
                mostrar_registros(registros, es_binario=True)

        elif opcion == "4":
            comparar_tamanos(ruta_json, ruta_csv, ruta_bin)

        elif opcion == "5":
            print("\n--- PASO 1: Generación de archivos ---")
            guardar_json(PERSONAS_EJEMPLO, ruta_json)
            guardar_csv(PERSONAS_EJEMPLO, ruta_csv)
            guardar_binario(PERSONAS_EJEMPLO, ruta_bin)
            print("Archivos generados exitosamente.")

            print("\n--- PASO 2: Lectura y desempaquetado de archivo binario ---")
            registros_bin = leer_binario(ruta_bin)
            print(f"Se leyeron {len(registros_bin)} registros binarios correctamente.")
            # Mostrar los primeros 3 para muestra
            mostrar_registros(registros_bin[:3], es_binario=True)
            if len(registros_bin) > 3:
                print(f"(Mostrando 3 de {len(registros_bin)} registros para brevedad...)")

            print("\n--- PASO 3: Comparativa de tamaños en disco ---")
            comparar_tamanos(ruta_json, ruta_csv, ruta_bin)

        elif opcion == "6":
            print("\nPrograma finalizado.")
            break

        else:
            print("\nError: opción inválida.")

        input("\nPresione ENTER para continuar...")


if __name__ == "__main__":
    menu()
