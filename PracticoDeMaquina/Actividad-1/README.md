# Práctico de Máquina 1: Análisis de Audio (WAV vs. MP3)

## 1. ¿De qué trata este trabajo?

El objetivo de esta actividad es comparar cómo se guardan los datos de audio en dos formatos diferentes:
- **WAV:** Es audio en bruto, sin compresión (las muestras de sonido se guardan tal cual se graban en modulación PCM).
- **MP3:** Es audio comprimido con pérdida (reduce el tamaño del archivo eliminando información redundante o imperceptible para el oído mediante modelos psicoacústicos y codificación entrópica).

Para realizar un análisis riguroso y explorar cómo influye la naturaleza de la señal en la compresión, se implementó una **triple comparativa empírica** con tres tipos contrastantes de audio (cada uno presente en `.wav` y `.mp3`):
1. **Himno Nacional Argentino** (`himno-nacional-argentino.wav` y `.mp3`): Grabación orquestal sinfónica completa y densa, codificada en **24 bits**.
2. **Sillycat Shore** (`Sillycat_Shore.wav` y `.mp3`): Música retro estilo **chiptune / 8-bit** con ondas sintéticas geométricas y patrones periódicos, codificada en **16 bits**.
3. **Voz Hablada** (`persona.wav` y `.mp3`): Locución de una persona hablando con pausas naturales y silencios entre palabras, codificada en **16 bits**.

El programa en Python (`Actividad1.py`) hace lo siguiente:
1. Valida la existencia y formato de los 3 pares de archivos.
2. Lee e interpreta las cabeceras canónicas RIFF/WAVE (los primeros 44 bytes de cada WAV).
3. Cuenta las ocurrencias de cada uno de los 256 valores de byte (0 al 255) y calcula su distribución de probabilidad empírica.
4. Genera una cuadrícula comparativa de gráficos (histogramas 3x2) guardada en `Histograma.png`.
5. Calcula la **Entropía empírica de Shannon** $H(X)$ y el salto de entropía $\Delta H = H(MP3) - H(WAV)$ para contrastar la eliminación de redundancia en cada caso.

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
   - En la consola se validan los 3 pares de archivos, se imprimen los campos de la cabecera canónica de cada WAV y se presenta una **tabla comparativa consolidada** con tamaños, ratios de compresión, entropías y saltos de incertidumbre ($\Delta H$).
   - Se genera, guarda y muestra una figura con 6 gráficos en cuadrícula $3 \times 2$ (`Histograma.png`) comparando los histogramas de frecuencias de cada señal.

---

## 5. Explicación sencilla de cómo funciona el código

El archivo `Actividad1.py` está estructurado de forma modular y documentada:

* `validar_archivos`: Comprueba la existencia y extensión de cada par de archivos `.wav` y `.mp3`.
* `analizar_cabecera_wav`: Lee y desempaqueta los primeros 44 bytes de la cabecera canónica RIFF/WAVE utilizando `struct`, extrayendo la resolución, canales, frecuencia de muestreo y tamaño del bloque de datos.
* `calcular_probabilidades_y_entropia`: Modela el archivo como una fuente de información de memoria nula (DMS) sobre el alfabeto de 256 bytes ($0$ a $255$), calcula las frecuencias relativas ($p_i$) y aplica la ecuación de Shannon:
  $$H(X) = -\sum_{i=0}^{255} p_i \cdot \log_2(p_i)$$
* `graficar_triple_comparativa`: Genera una figura de 3 filas $\times$ 2 columnas con `matplotlib`, mostrando a la izquierda el audio sin compresión (WAV) y a la derecha el comprimido (MP3) para cada caso, guardándola en `Histograma.png`.
* `main`: Coordina el procesamiento de las 3 señales, imprime el cuadro comparativo en consola y despliega la gráfica.

---

## 6. Respuestas de la Actividad 1 (Triple Comparativa)

A continuación se detallan las respuestas a las consignas solicitadas en la guía:

### a) Carga y Validación
El script valida programáticamente la existencia y extensión de los tres pares de archivos utilizados en el estudio:
1. `himno-nacional-argentino.wav` y `.mp3`
2. `Sillycat_Shore.wav` y `.mp3`
3. `persona.wav` y `.mp3`

Todos los archivos superaron exitosamente la validación.

### b) Análisis de Cabeceras de los archivos WAV
Al analizar los primeros 44 bytes de cada archivo WAV mediante la función `analizar_cabecera_wav`, se obtuvieron los siguientes metadatos canónicos:

| Parámetro técnico | Himno Nacional | Sillycat Shore | Voz Hablada |
| :--- | :---: | :---: | :---: |
| **Identificador (ChunkID)** | `RIFF` | `RIFF` | `RIFF` |
| **Tamaño de datos (ChunkSize)** | `63.647.182 bytes` (~60,7 MB) | `53.154.178 bytes` (~50,7 MB) | `14.918.936 bytes` (~14,2 MB) |
| **Formato contenedor** | `WAVE` | `WAVE` | `WAVE` |
| **Codificación (AudioFormat)** | `1` (PCM lineal sin compresión) | `1` (PCM lineal sin compresión) | `1` (PCM lineal sin compresión) |
| **Canales (NumChannels)** | `2` (Estéreo) | `2` (Estéreo) | `2` (Estéreo) |
| **Frecuencia de muestreo** | `44.100 Hz` | `44.100 Hz` | `48.000 Hz` |
| **Resolución por muestra** | **`24 bits`** | **`16 bits`** | **`16 bits`** |
| **Subchunk2 ID detectado** | `bext` (Metadata de broadcast) | `data` (Datos de sonido) | `data` (Datos de sonido) |

---

### c) Distribución de Probabilidades
Cada archivo fue procesado byte a byte considerando un alfabeto finito de 256 símbolos ($s_i \in \{0, 1, \dots, 255\}$). La probabilidad empírica de cada valor de byte se calculó como su frecuencia relativa sobre el total de bytes:
$$p(s_i) = \frac{n_i}{N}$$

---

### d) Histogramas Comparativos

La siguiente figura reúne la triple comparativa en una cuadrícula $3 \times 2$:

<div align="center">

![Triple Comparativa de Histogramas WAV vs. MP3](./Histograma.png)

</div>

* **Columna Izquierda (WAV - Sin compresión):**
  * **1. Himno Nacional (Orquestal):** Muestra una base central ancha y elevada (~170.000 repeticiones por cada valor). Prácticamente todos los bytes del alfabeto se usan con frecuencia.
  * **2. Sillycat Shore (Chiptune 8-bit):** El valle central es notablemente más profundo y plano (~90.000 repeticiones) y los picos en los polos `0` y `255` crecen marcadamente.
  * **3. Voz Hablada (Locución):** Presenta un pico colosal en el valor `0` con casi **3,5 millones de ocurrencias** (cerca del 25% de todo el archivo), mientras que el rango medio (valores 30 a 230) permanece casi pegado al suelo.
* **Columna Derecha (MP3 - Comprimido con pérdida):**
  * En los tres casos, la compresión MP3 desmantela la redundancia estadística y distribuye la probabilidad de forma prácticamente uniforme sobre los 256 símbolos, aproximándose al estado de máxima entropía ($H \to 8,00$).

---

### e) Cálculo de Entropía y Métricas de Rendimiento

Aplicando la fórmula de Shannon a los tres escenarios, se obtuvieron las siguientes mediciones:

| Caso de Estudio | Tipo de Señal | Bits/muestra | Tamaño WAV | Tamaño MP3 | Ratio de Compresión | Entropía WAV | Entropía MP3 | Salto $\Delta H$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Himno Nacional** | Orquesta polifónica densa | 24 bits | 60,70 MB | 5,33 MB | **11,40 : 1** (-91,2%) | **$7,8029$** | $7,9773$ | **$+0,1744$** |
| **2. Sillycat Shore** | Chiptune 8-bit retro | 16 bits | 50,69 MB | 6,45 MB | **7,86 : 1** (-87,3%) | **$7,4124$** | $7,9787$ | **$+0,5663$** |
| **3. Voz Hablada** | Locución con pausas | 16 bits | 14,23 MB | 0,96 MB | **14,89 : 1** (-93,3%) | **$6,4968$** | $7,8019$ | **$+1,3050$** |

> **Nota:** El límite teórico máximo de entropía para un alfabeto de 256 símbolos es $\log_2(256) = 8,0000 \text{ bits/símbolo}$.

---

### f) Comparación y Explicación Teórica

¿Por qué se produce esta progresión tan marcada en la entropía y en el salto $\Delta H$?

#### 1. ¿Por qué el Himno Nacional tiene una entropía inicial tan alta ($7,80$)?
* **Riqueza espectral continua:** Una orquesta sinfónica posee decenas de instrumentos acústicos que suenan simultáneamente (cuerdas, vientos, bronces, coro y percusión) con reverberación continua de sala, ocupando todo el rango de amplitudes de forma constante.
* **Resolución de 24 bits:** Cada muestra utiliza 3 bytes (LSB, byte medio y MSB). El byte menos significativo (LSB) y el intermedio registran microfluctuaciones y ruido de fondo casi aleatorio, actuando como un "piso de ruido" uniforme que eleva artificialmente la entropía marginal de orden 0. Por eso, su salto $\Delta H$ es de apenas $+0,17 \text{ bits}$.

#### 2. ¿Por qué Sillycat Shore reduce su entropía a $7,41$ y triplica el salto $\Delta H$ (+0,57)?
* **Síntesis geométrica simple:** La música chiptune / 8-bit se basa en osciladores que generan ondas cuadradas, triangulares y pulsos de ciclo fijo. Al no existir la complejidad acústica ni la reverberación analógica continua, hay mayor periodicidad y predictibilidad de amplitud.
* **Resolución de 16 bits:** Al tener 2 bytes por muestra en lugar de 3, el byte más significativo (MSB, que contiene la envolvente del sonido y el signo) representa el **50% de los bytes leídos** (en vez del 33% en 24 bits), permitiendo que la redundancia del reposo y silencio se refleje con mayor nitidez.

#### 3. ¿Por qué la Voz Hablada se desploma a $6,50$ y logra un salto récord de $+1,31$ bits y un ratio de $14,89:1$?
* **Redundancia de Amplitud (Pausas y Silencios):** En una conversación o locución natural, existen constantes pausas entre palabras, frases y respiraciones. En modulación PCM, el silencio digital es una repetición continua de muestras idénticas en cero (`0x0000`). Como casi el **25% de todo el archivo son ceros**, la incertidumbre de la fuente se desploma drásticamente.
* **Redundancia Espectral (Transformada MDCT de MP3):** El habla humana concentra casi toda su energía acústica en una banda muy estrecha (300 Hz a 3.400 Hz). El estándar MP3 divide el espectro en 32 subbandas de frecuencia; en voz humana, **la gran mayoría de las subbandas de agudos altos y graves profundos quedan completamente vacías (coeficientes en cero)**.
* **Codificación Entrópica Óptima:** El compresor MP3 aprovecha estas secuencias masivas de ceros aplicando *Run-Length Encoding* (RLE) y árboles de Huffman, logrando una reducción de tamaño del **$93,3\%$** y distribuyendo la información resultante de forma cuasi-aleatoria en el archivo comprimido.
