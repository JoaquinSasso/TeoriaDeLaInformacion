# Práctico de Máquina 1: Actividad 5 — Almacenamiento y Empaquetado a Nivel de Bits (Bitwise)

## 1. ¿De qué trata este trabajo?

En este ejercicio analizamos cómo la elección del formato de datos y las técnicas de codificación a bajo nivel impactan directamente en el espacio que ocupan los archivos en disco.

La consigna pide gestionar el registro de **20 personas**, donde cada persona cuenta con:
- **Apellido y Nombre** (texto)
- **Dirección** (texto)
- **DNI** (número entero)
- **8 campos booleanos (Verdadero / Falso):**
  1. `estudios_primarios`
  2. `estudios_secundarios`
  3. `estudios_universitarios`
  4. `vivienda_propia`
  5. `obra_social`
  6. `trabaja`
  7. `tiene_vehiculo`
  8. `cuenta_bancaria`

Comparamos el almacenamiento en formatos de texto comunes (**JSON** y **CSV**) contra un **formato binario optimizado** que aprovecha técnicas eficientes de codificación.

---

## 2. ¿Cómo se guardan los datos en cada formato?

### 2.1. Formatos de Texto (JSON y CSV)
* **JSON (`personas.json`):** Es el formato estándar de las aplicaciones web. Es muy cómodo y fácil de leer para los humanos, pero es sumamente redundante porque repite el nombre de cada atributo (`"apellido_nombre":`, `"direccion":`, etc.), usa comillas, llaves y escribe los booleanos como texto plano (`true` o `false`, ocupando de 4 a 5 bytes por cada uno).
* **CSV (`personas.csv`):** Guarda los datos en filas separadas por comas. Es más liviano que JSON porque no repite las claves en cada registro, pero sigue guardando los números como caracteres ASCII (por ejemplo, el DNI de 8 cifras ocupa 8 bytes de texto) y los booleanos como palabras (`"True"` o `"False"`).

---

### 2.2. Formato Binario Optimizado (`personas.bin`)

Para lograr el tamaño más compacto posible sin perder ningún dato, aplicamos tres técnicas de codificación:

#### A) Cadenas de Texto Dinámicas (Pascal Strings)
En lugar de reservar un tamaño fijo en bytes para los textos (como rellenar siempre con 40 espacios o ceros cada nombre y dirección), usamos **Pascal Strings**:
- **Byte 0:** Un entero sin signo de 1 byte (`uint8`) que indica la longitud exacta $L$ del texto (de 0 a 255 caracteres).
- **Bytes 1 a $L$:** Los caracteres del texto codificados en UTF-8.

> 💡 **Ventaja:** Si un nombre tiene 14 letras, ocupa exactamente $1 + 14 = 15$ bytes en lugar de 40 bytes fijos, ahorrando espacio en cada persona sin desperdiciar bytes de relleno.

#### B) DNI como Entero de 4 Bytes (`uint32`)
En texto, un DNI como `34567890` ocupa 8 bytes (un byte por cada dígito). En el archivo binario lo guardamos directamente como su valor numérico en un entero sin signo de 32 bits (`uint32` de 4 bytes, que permite almacenar números hasta $4.294.967.295$). Con esto **reducimos el tamaño del DNI a la mitad**.

#### C) Empaquetado a Nivel de Bits (Bitwise) para los 8 Booleanos
En los archivos de texto, los 8 campos booleanos ocupan entre 40 y 50 bytes por persona (palabras como `"True"` y `"False"`).  
Dado que un booleano solo necesita **1 bit** de información ($1$ para Verdadero, $0$ para Falso) y $1 \text{ byte} = 8 \text{ bits}$, podemos **empaquetar los 8 atributos lógicos en un único byte** de memoria.

```text
Distribución de los 8 booleanos dentro del byte:

  Bit 7      Bit 6      Bit 5      Bit 4      Bit 3      Bit 2      Bit 1      Bit 0
┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Primaria │ Secund.  │ Univ.    │ Vivienda │ O.Social │ Trabaja  │ Vehículo │ Cta.Banc │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
 (Más significativo)                                                   (Menos significativo)
```

---

## 3. Operaciones Bitwise utilizadas

### Empaquetado (Guardar)
Para armar el byte, empezamos en $0$ y usamos desplazamientos a la izquierda (`<<`) y el operador OR bit a bit (`|`):

```python
byte_flags = 0
byte_flags |= (int(primaria)   & 1) << 7
byte_flags |= (int(secundaria) & 1) << 6
byte_flags |= (int(universidad)& 1) << 5
byte_flags |= (int(vivienda)   & 1) << 4
byte_flags |= (int(obra_social)& 1) << 3
byte_flags |= (int(trabaja)    & 1) << 2
byte_flags |= (int(vehiculo)   & 1) << 1
byte_flags |= (int(banco)      & 1)
```

*Por ejemplo:* Si una persona tiene primaria (1), secundaria (1), no fue a la facultad (0), tiene casa (1), obra social (1), trabaja (1), auto (1) y cuenta bancaria (1), el byte resultante es `11011111` en binario (`0xDF` en hexadecimal), ocupando **1 solo byte** en disco.

### Desempaquetado (Leer)
Al leer el byte del archivo, usamos desplazamientos a la derecha (`>>`) y una máscara AND (`& 1`) para aislar cada bit:

```python
primaria    = bool((byte_flags >> 7) & 1)
secundaria  = bool((byte_flags >> 6) & 1)
universidad = bool((byte_flags >> 5) & 1)
vivienda    = bool((byte_flags >> 4) & 1)
obra_social = bool((byte_flags >> 3) & 1)
trabaja     = bool((byte_flags >> 2) & 1)
vehiculo    = bool((byte_flags >> 1) & 1)
banco       = bool(byte_flags & 1)
```

---

## 4. ¿Cómo ejecutar el programa?

El script fue programado en **Python 3** y no necesita librerías externas.

1. Abrí la terminal y parate en la carpeta de la actividad:
   ```bash
   cd PracticoDeMaquina/Actividad-5
   ```

2. Ejecutá el programa:
   ```bash
   python almacenamiento_bitwise.py
   ```

3. El menú principal te permite probar todas las opciones:
   ```text
   =================================================================
   ACTIVIDAD 5: ALMACENAMIENTO Y EMPAQUETADO BITWISE
   =================================================================
   1. Generar y guardar archivos (JSON, CSV y Binario)
   2. Leer y mostrar registros desde archivo de texto (JSON)
   3. Leer, desempaquetar (Bitwise) y mostrar desde archivo binario (.bin)
   4. Comparar tamaños de archivo y estadísticas de almacenamiento
   5. Ejecutar demostración completa (generar, leer y comparar)
   6. Salir
   =================================================================
   ```

---

## 5. Resultados y Comparativa de Almacenamiento

Al generar los 20 registros con los mismos datos en los tres formatos, obtuvimos los siguientes tamaños reales en disco:

| Formato de Archivo | Tamaño Total (20 personas) | Promedio por Persona | Ahorro vs. JSON | Ahorro vs. CSV |
| :--- | :---: | :---: | :---: | :---: |
| **Texto JSON (`personas.json`)** | **7.461 bytes** | ~373,1 bytes | *Base (0 %)* | — |
| **Texto CSV (`personas.csv`)** | **2.240 bytes** | ~112,0 bytes | **- 70,0 %** | *Base (0 %)* |
| **Binario Optimizado (`personas.bin`)** | **1.051 bytes** | **~52,5 bytes** | **- 85,9 %** | **- 53,1 %** |

### Conclusiones de los números:
* **El binario es 7,1 veces más chico que el JSON** y **2,1 veces más chico que el CSV**.
* En el formato binario, cada persona ocupa en promedio apenas **52 bytes** (incluyendo nombre completo, dirección, DNI y los 8 estados lógicos).
* Los 8 booleanos, que en JSON gastaban casi 45 bytes de texto por persona, en el archivo binario quedan reducidos a **1 único byte**.

---

## 6. Análisis Teórico: Impacto en Sistemas de Alta Escala

La consigna pide analizar qué consecuencias tiene esta diferencia de codificación cuando los sistemas crecen a gran escala.

Imaginemos un padrón o base de datos con **10.000.000 de personas** (como el padrón electoral de un país o los usuarios de una red social):

| Métrica para 10 Millones de Personas | Almacenamiento con JSON | Almacenamiento con Binario Bitwise | Diferencia / Ahorro |
| :--- | :---: | :---: | :---: |
| **Espacio en disco requerido** | **~3,73 Gigabytes** | **~0,52 Gigabytes (525 MB)** | **Ahorro de más de 3,2 GB** |
| **Transferencia de red (Ancho de banda)** | Mucho más lenta, satura la red | Muy liviana, menor tiempo de descarga | **7 veces menos consumo de datos** |
| **Uso de memoria RAM del servidor** | Alto consumo parseando strings | Carga directa en buffers de memoria | **Menor consumo y sin garbage collection pesado** |
| **Tiempo de lectura/escritura (I/O)** | Lectura lenta caracter por caracter | Lectura veloz por bloques de bytes | **Mayor velocidad de respuesta** |

### Conclusión Final
Elegir la estructura de datos correcta no es solo una cuestión de ahorrar unos pocos bytes en la computadora personal. En sistemas masivos o en dispositivos con recursos limitados (como chips IoT, satélites o teléfonos móviles), el **empaquetado a nivel de bits** y las **cadenas dinámicas** marcan la diferencia entre un sistema lento y costoso frente a uno rápido, eficiente y escalable.
