"""
PPM-C (orden 2) + codificación aritmética.
Lo usan compressor.py y decompressor.py.

Partes del archivo:
  1. Codificador aritmético (intervalo [L,H), reglas E1/E2/E3, flush)
  2. Modelo PPM-C (tablas de frecuencias por contexto)
  3. Comprimir / descomprimir (recorrido O2 -> O1 -> O0 -> O-1)
  4. Cabecera del archivo .tdi
"""

import binascii
import struct


# ===========================================================================
# 1. CODIFICADOR ARITMÉTICO
# ===========================================================================
# Se usan números enteros en lugar de decimales para que el compresor y el
# descompresor hagan exactamente las mismas cuentas (sin errores de redondeo).
# Equivalencias con el Excel de la cátedra:
#   0.25 -> CUARTO    0.5 -> MITAD    0.75 -> TRES_CUARTOS    1.0 -> TOPE
PRECISION = 32
TOPE = (1 << PRECISION) - 1
MITAD = 1 << (PRECISION - 1)
CUARTO = 1 << (PRECISION - 2)
TRES_CUARTOS = 3 * CUARTO


# ---------------------------------------------------------------------------
# Manejo de bits sueltos
# ---------------------------------------------------------------------------

class EscritorDeBits:
    """Junta bits de a uno y los guarda agrupados en bytes."""

    def __init__(self):
        self.salida = bytearray()
        self.byte_actual = 0
        self.bits_en_byte = 0

    def escribir(self, bit):
        self.byte_actual = (self.byte_actual << 1) | bit
        self.bits_en_byte += 1
        if self.bits_en_byte == 8:
            self.salida.append(self.byte_actual)
            self.byte_actual = 0
            self.bits_en_byte = 0

    def terminar(self):
        # Completa el último byte con ceros.
        while self.bits_en_byte != 0:
            self.escribir(0)
        return bytes(self.salida)


class LectorDeBits:
    """Entrega los bits de un bloque de bytes de a uno."""

    def __init__(self, datos):
        self.datos = datos
        self.posicion = 0  # número de bit

    def leer(self):
        indice_byte = self.posicion // 8
        indice_bit = 7 - (self.posicion % 8)
        self.posicion += 1
        if indice_byte >= len(self.datos):
            return 0  # pasado el final se leen ceros (el flush lo tiene en cuenta)
        return (self.datos[indice_byte] >> indice_bit) & 1


# ---------------------------------------------------------------------------
# Codificador
# ---------------------------------------------------------------------------

class Codificador:

    def __init__(self):
        self.low = 0
        self.high = TOPE
        self.pendientes = 0
        self.bits = EscritorDeBits()

    def codificar(self, acum_bajo, acum_alto, total):
        """
        Achica el intervalo al subintervalo [acum_bajo/total, acum_alto/total).
        Es la fórmula del Excel:  newL = L + range * C_low ;  newH = L + range * C_high
        """
        rango = self.high - self.low + 1
        self.high = self.low + (rango * acum_alto) // total - 1
        self.low = self.low + (rango * acum_bajo) // total
        self._renormalizar()

    def _emitir(self, bit):
        """Emite un bit y después los pendientes de E3 con el valor contrario."""
        self.bits.escribir(bit)
        for _ in range(self.pendientes):
            self.bits.escribir(1 - bit)
        self.pendientes = 0

    def _renormalizar(self):
        while True:
            if self.high < MITAD:
                # E1: todo en la mitad inferior -> emitir 0
                self._emitir(0)
            elif self.low >= MITAD:
                # E2: todo en la mitad superior -> emitir 1
                self._emitir(1)
                self.low -= MITAD
                self.high -= MITAD
            elif self.low >= CUARTO and self.high < TRES_CUARTOS:
                # E3: zona central -> no se emite, se guarda un pendiente
                self.pendientes += 1
                self.low -= CUARTO
                self.high -= CUARTO
            else:
                return  # ninguna regla aplica: esperar al próximo evento
            # Zoom x2 (junto con las restas de arriba da 2L, 2L-1 o 2L-0.5)
            self.low = 2 * self.low
            self.high = 2 * self.high + 1

    def terminar(self):
        """Flush: la regla de cierre de la cátedra."""
        self.pendientes += 1
        if self.low < CUARTO:
            self._emitir(0)
        else:
            self._emitir(1)
        return self.bits.terminar()


# ---------------------------------------------------------------------------
# Decodificador (proceso espejo)
# ---------------------------------------------------------------------------

class Decodificador:

    def __init__(self, datos):
        self.low = 0
        self.high = TOPE
        self.bits = LectorDeBits(datos)
        # V: los primeros 32 bits del stream
        self.valor = 0
        for _ in range(PRECISION):
            self.valor = 2 * self.valor + self.bits.leer()

    def objetivo(self, total):
        """
        Indica en qué posición de la tabla (entre 0 y total-1) cae V.
        Es la versión entera de "¿en qué subintervalo cae V?".
        """
        rango = self.high - self.low + 1
        return ((self.valor - self.low + 1) * total - 1) // rango

    def consumir(self, acum_bajo, acum_alto, total):
        """Hace exactamente lo mismo que el codificador, pero leyendo bits."""
        rango = self.high - self.low + 1
        self.high = self.low + (rango * acum_alto) // total - 1
        self.low = self.low + (rango * acum_bajo) // total
        self._renormalizar()

    def _renormalizar(self):
        while True:
            if self.high < MITAD:
                pass  # E1
            elif self.low >= MITAD:
                # E2
                self.low -= MITAD
                self.high -= MITAD
                self.valor -= MITAD
            elif self.low >= CUARTO and self.high < TRES_CUARTOS:
                # E3
                self.low -= CUARTO
                self.high -= CUARTO
                self.valor -= CUARTO
            else:
                return
            self.low = 2 * self.low
            self.high = 2 * self.high + 1
            self.valor = 2 * self.valor + self.bits.leer()  # consume un bit


# ===========================================================================
# 2. MODELO PPM-C
# ===========================================================================

ESC = "ESC"
ORDEN_MAXIMO = 2
TAMANO_ALFABETO = 256   # O-1: los 256 valores posibles de un byte


def obtener_contexto(datos, posicion, orden):
    """Los 'orden' bytes anteriores a 'posicion'. Orden 0 -> b'' (contexto global)."""
    return bytes(datos[posicion - orden:posicion])


class ModeloPPMC:

    def __init__(self, orden_maximo=ORDEN_MAXIMO):
        self.orden_maximo = orden_maximo
        # Una tabla por contexto:  b'AB' -> {ord('R'): 1}
        # El largo del contexto indica el orden (b'' es O0).
        # Los dict de Python mantienen el orden de inserción = orden de aparición.
        self.tablas = {}

    def tabla(self, contexto):
        return self.tablas.get(contexto, {})

    def actualizar(self, datos, posicion, simbolo):
        """Después de codificar un símbolo, se suma 1 en O2, O1 y O0."""
        for orden in range(self.orden_maximo + 1):
            if posicion >= orden:
                contexto = obtener_contexto(datos, posicion, orden)
                tabla = self.tablas.setdefault(contexto, {})
                tabla[simbolo] = tabla.get(simbolo, 0) + 1


# ---------------------------------------------------------------------------
# Cálculo de probabilidades PPM-C
#   U     = cantidad de símbolos distintos en la tabla  (peso virtual del ESC)
#   total = suma de frecuencias reales
#   P(ESC) = U / (total + U)      P(x) = freq(x) / (total + U)
# ---------------------------------------------------------------------------

def total_con_escape(tabla):
    return sum(tabla.values()) + len(tabla)


def intervalo_en_tabla(tabla, evento):
    """Devuelve (acum_bajo, acum_alto, total) del evento (ESC o un símbolo)."""
    U = len(tabla)
    total = total_con_escape(tabla)
    if evento == ESC:
        return 0, U, total
    acumulado = U
    for simbolo, frecuencia in tabla.items():
        if simbolo == evento:
            return acumulado, acumulado + frecuencia, total
        acumulado += frecuencia
    raise ValueError("el símbolo no está en la tabla")


def buscar_en_tabla(tabla, objetivo):
    """Operación inversa: dado un valor, qué evento lo contiene."""
    U = len(tabla)
    if objetivo < U:
        return ESC, 0, U
    acumulado = U
    for simbolo, frecuencia in tabla.items():
        if objetivo < acumulado + frecuencia:
            return simbolo, acumulado, acumulado + frecuencia
        acumulado += frecuencia
    raise ValueError("datos corruptos: el valor no cae en ningún intervalo")


# ===========================================================================
# 3. COMPRIMIR / DESCOMPRIMIR
# ===========================================================================

def _nombre(simbolo):
    caracter = chr(simbolo)
    return caracter if caracter.isprintable() else f"0x{simbolo:02X}"


def comprimir(datos, traza=False):
    modelo = ModeloPPMC()
    codificador = Codificador()

    for posicion, simbolo in enumerate(datos):
        eventos = []          # sólo para la traza didáctica
        encontrado = False

        for orden in range(ORDEN_MAXIMO, -1, -1):
            if posicion < orden:
                continue      # todavía no hay tantos símbolos previos
            contexto = obtener_contexto(datos, posicion, orden)
            tabla = modelo.tabla(contexto)

            if not tabla:
                # Contexto vacío: ESC con probabilidad 1, no cuesta bits
                eventos.append(f"ESC@O{orden}(1)")
                continue

            if simbolo in tabla:
                bajo, alto, total = intervalo_en_tabla(tabla, simbolo)
                codificador.codificar(bajo, alto, total)
                eventos.append(f"{_nombre(simbolo)}@O{orden}({alto - bajo}/{total})")
                encontrado = True
                break

            bajo, alto, total = intervalo_en_tabla(tabla, ESC)
            codificador.codificar(bajo, alto, total)
            eventos.append(f"ESC@O{orden}({alto - bajo}/{total})")

        if not encontrado:
            # O-1: todos los bytes equiprobables (1/256)
            codificador.codificar(simbolo, simbolo + 1, TAMANO_ALFABETO)
            eventos.append(f"{_nombre(simbolo)}@O-1(1/{TAMANO_ALFABETO})")

        if traza:
            print(f"{posicion + 1:>3}- {_nombre(simbolo)}:  " + "  ".join(eventos))

        modelo.actualizar(datos, posicion, simbolo)

    return codificador.terminar()


def descomprimir(datos_comprimidos, cantidad_simbolos):
    modelo = ModeloPPMC()
    decodificador = Decodificador(datos_comprimidos)
    salida = bytearray()

    for posicion in range(cantidad_simbolos):
        simbolo = None

        for orden in range(ORDEN_MAXIMO, -1, -1):
            if posicion < orden:
                continue
            contexto = obtener_contexto(salida, posicion, orden)
            tabla = modelo.tabla(contexto)
            if not tabla:
                continue  # ESC gratis, igual que en el compresor

            total = total_con_escape(tabla)
            evento, bajo, alto = buscar_en_tabla(tabla, decodificador.objetivo(total))
            decodificador.consumir(bajo, alto, total)
            if evento != ESC:
                simbolo = evento
                break

        if simbolo is None:
            simbolo = decodificador.objetivo(TAMANO_ALFABETO)
            decodificador.consumir(simbolo, simbolo + 1, TAMANO_ALFABETO)

        salida.append(simbolo)
        modelo.actualizar(salida, posicion, simbolo)

    return bytes(salida)


# ===========================================================================
# 4. CABECERA .tdi  (14 bytes: magic 'PPMC', versión, orden, tamaño original, CRC-32)
#    El tamaño le indica al descompresor cuándo parar; el CRC-32 detecta corrupción.
# ===========================================================================

MAGIC = b"PPMC"
VERSION = 2
FORMATO = ">4sBBII"             # big-endian, sin relleno
TAMANO_CABECERA = struct.calcsize(FORMATO)


class ErrorDeFormato(Exception):
    pass


def crc32(datos):
    return binascii.crc32(datos) & 0xFFFFFFFF


def armar_cabecera(orden_maximo, original):
    return struct.pack(FORMATO, MAGIC, VERSION, orden_maximo, len(original), crc32(original))


def leer_cabecera(contenido):
    if len(contenido) < TAMANO_CABECERA:
        raise ErrorDeFormato("archivo demasiado corto: cabecera incompleta")
    magic, version, orden, tamano, crc = struct.unpack(FORMATO, contenido[:TAMANO_CABECERA])
    if magic != MAGIC:
        raise ErrorDeFormato("no es un archivo .tdi de PPM-C (magic incorrecto)")
    if version != VERSION:
        raise ErrorDeFormato(f"versión {version} no soportada")
    return {"orden": orden, "tamano": tamano, "crc32": crc,
            "datos": contenido[TAMANO_CABECERA:]}
