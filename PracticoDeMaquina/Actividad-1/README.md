# Práctico de Máquina 1: Análisis de Audio (WAV vs. MP3)

**Materia:** Teoría de la Información  
**Carrera:** Licenciatura en Ciencias de la Computación  
**Año:** 2026  

---

## 1. ¿De qué trata este trabajo?

El objetivo de esta actividad es comparar cómo se guardan los datos de audio en dos formatos diferentes:
- **WAV:** Es audio en bruto, sin compresión (las muestras de sonido se guardan tal cual se graban).
- **MP3:** Es audio comprimido (reduce el tamaño del archivo eliminando información repetitiva o imperceptible para el oído humano).

Para hacer una comparación justa, usamos la misma pista de audio en ambos formatos: el *Himno Nacional Argentino* (`himno-nacional-argentino.wav` y `himno-nacional-argentino.mp3`).

El programa en Python (`Actividad1.py`) hace lo siguiente:
1. Comprueba que ambos archivos existan y tengan el formato correcto.
2. Lee la cabecera del archivo WAV (los primeros 44 bytes) para ver detalles como la frecuencia de muestreo o si es estéreo.
3. Cuenta qué tan seguido aparece cada byte (del 0 al 255) en cada archivo.
4. Dibuja dos gráficos (histogramas) para ver visualmente cómo se distribuyen los datos.
5. Calcula la **Entropía de Shannon** para medir el grado de incertidumbre y qué tan comprimida está la información.

---

## 2. ¿Qué necesitamos para ejecutarlo?

El script está hecho en **Python 3**.

### Librerías necesarias
- **Librería externa a instalar:**
  - `matplotlib`: Se usa para dibujar los gráficos de los histogramas.
- **Librerías propias de Python (ya vienen con Python):**
  - `os`: Para verificar que los archivos existan en la carpeta.
  - `math`: Para calcular el logaritmo en base 2 de la fórmula de entropía.
  - `struct`: Para leer los bytes de la cabecera WAV de forma ordenada.
  - `collections`: Usa `Counter` para contar de manera rápida cuántas veces aparece cada byte.

---

## 3. Instalación

Solo hay que instalar la librería `matplotlib`. Abrí una terminal o consola y ejecutá:

```bash
pip install matplotlib
```

---

## 4. Cómo ejecutar el script

1. Abrí la terminal y parate en la carpeta de la Actividad 1:
   ```bash
   cd PracticoDeMaquina/Actividad-1
   ```
2. Ejecutá el programa con Python:
   ```bash
   python Actividad1.py
   ```
3. **¿Qué vas a ver al ejecutarlo?**
   - En la consola aparecerán los datos de la cabecera del archivo WAV (canales, frecuencia, etc.) y los valores de entropía de ambos archivos.
   - Se abrirá una ventana con dos gráficos comparando las frecuencias de los bytes de ambos archivos. Cuando cierres esa ventana, el programa finaliza.

---

## 5. Explicación sencilla de cómo funciona el código

El archivo `Actividad1.py` está dividido en funciones claras:

* `validar_archivos`: Revisa que existan los archivos `.wav` y `.mp3` antes de empezar. Si falta alguno, avisa con un mensaje de error.
* `analizar_cabecera_wav`: Abre el archivo WAV y lee los primeros 44 bytes. Ahí está guardada la información técnica del audio:
  - Formato del archivo ("RIFF" / "WAVE").
  - Frecuencia de muestreo (por ejemplo, 44.100 Hz).
  - Canales (1 para Mono, 2 para Estéreo).
  - Bits por muestra (por ejemplo, 16 o 24 bits).
* `calcular_probabilidades_y_entropia`: Lee todo el archivo byte por byte. Cada byte tiene un valor entre 0 y 255. Cuenta cuántas veces se repite cada valor y calcula su porcentaje de aparición. Con esos datos, aplica la fórmula de Shannon:
  $$H = -\sum p_i \cdot \log_2(p_i)$$
  La entropía nos indica qué tan variada o impredecible es la información.
* `graficar_histogramas`: Genera dos gráficos de barras con `matplotlib` (uno al lado del otro) para ver la diferencia visual entre el archivo sin comprimir y el comprimido.
* `main`: Es la función principal que ejecuta los pasos en orden.

---

## 6. Respuestas de la Actividad 1

A continuación se detallan las respuestas a los puntos solicitados en la guía:

### a) Carga y Validación
El programa verifica mediante la función `validar_archivos` que los archivos `himno-nacional-argentino.wav` e `himno-nacional-argentino.mp3` existan en la carpeta y tengan la extensión correcta. Ambos archivos pasaron la validación sin problemas.

### b) Análisis de Cabecera del archivo WAV
Al analizar los primeros 44 bytes de `himno-nacional-argentino.wav`, se obtuvieron los siguientes datos:

| Campo de la cabecera | Valor obtenido | Explicación |
| :--- | :--- | :--- |
| **ChunkID** | `RIFF` | Identifica que el archivo usa el formato contenedor RIFF. |
| **Chunk Size** | `63.647.182 bytes` | Tamaño total del archivo menos 8 bytes (~60.7 MB). |
| **Format** | `WAVE` | Indica que dentro del contenedor hay audio tipo WAVE. |
| **Formato de audio** | `1 (PCM)` | Significa que el audio no tiene compresión. |
| **Canales** | `2` | Es audio estéreo (dos canales: izquierdo y derecho). |
| **Frecuencia de muestreo** | `44.100 Hz` | Se toman 44.100 muestras de sonido por segundo (calidad de CD). |
| **Bits por muestra** | `24 bits` | Cada muestra usa 24 bits de resolución. |
| **Subchunk2 ID** | `bext` | Contiene metadatos de emisión (*Broadcast Wave*) que van antes de los datos de sonido. |

### c) Distribución de Probabilidades
El programa lee cada archivo como una secuencia de bytes. Como cada byte puede tomar 256 valores posibles (del 0 al 255), se calcula la probabilidad de cada uno dividiendo la cantidad de veces que aparece entre el total de bytes del archivo.

### d) Histogramas
* **WAV:** El gráfico muestra picos claros en ciertos valores. Esto se debe a que en el audio sin comprimir hay momentos de silencio o notas suaves donde los valores de las muestras se repiten con frecuencia.
* **MP3:** El gráfico es mucho más plano y uniforme. Casi todos los valores del 0 al 255 aparecen una cantidad similar de veces.

### e) Cálculo de Entropía
Aplicando la fórmula de Shannon a los datos de cada archivo, obtuvimos:

* **Entropía del WAV:** $\approx 7,8029 \text{ bits/símbolo}$
* **Entropía del MP3:** $\approx 7,9773 \text{ bits/símbolo}$
* **Entropía máxima posible (para 256 valores):** $8,0000 \text{ bits/símbolo}$

### f) Comparación y Explicación
¿Por qué hay tanta diferencia entre ambos archivos?

1. **En el archivo WAV (sin compresión):**  
   El sonido se almacena de manera directa, tal como fue grabado. En cualquier canción existen notas que duran varios instantes, momentos de silencio o cambios de volumen suaves, por lo que muchas muestras seguidas tienen valores parecidos. Esto crea **redundancia** (información que se repite o que resulta fácil de predecir). Al haber más orden y redundancia, la entropía es menor ($7,80$).

2. **En el archivo MP3 (comprimido):**  
   El formato MP3 analiza la música para quitar lo que el oído no puede percibir y aplica algoritmos de compresión (como la codificación Huffman) para eliminar datos repetitivos. Al comprimir, la redundancia desaparece y la información queda repartida de forma mucho más uniforme. Cuanto mejor comprimido está un archivo, más se parece a una secuencia aleatoria donde todos los valores son igualmente probables. Por esta razón, la entropía del MP3 sube y se acerca prácticamente al límite teórico máximo ($7,98$ de un máximo de $8$).
