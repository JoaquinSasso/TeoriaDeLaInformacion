# Práctico de Máquina 1: Actividad 3 — Entropía Empírica en Archivos (Texto vs. Comprimidos)

## 1. ¿De qué trata este trabajo?

El objetivo de esta actividad es analizar y comparar la cantidad de información real y redundancia estadística que contienen dos tipos de archivos muy diferentes:
- **Archivo de texto plano (`texto_prueba.txt`):** Contiene lenguaje natural humano (texto en español).
- **Archivo comprimido (`texto_prueba.zip`):** El mismo texto procesado por un algoritmo de compresión (formato ZIP / DEFLATE).

Para cumplir con la consigna del práctico, desarrollamos un programa en Python (`entropia.py`) que lee cualquier archivo **byte por byte** con una complejidad temporal lineal `O(N)` (donde `N` es el tamaño del archivo en bytes), calculando:
1. La frecuencia relativa de aparición de cada uno de los 256 bytes posibles (valores del 0 al 255).
2. La **Entropía Empírica de Shannon** (medida en bits/símbolo).
3. La **Redundancia Absoluta** (cuántos bits por byte representan repetición o datos predecibles).

---

## 2. Requisitos y Librerías

El script está desarrollado en **Python 3** y utiliza únicamente módulos de la biblioteca estándar de Python:
- `math`: Para el cálculo del logaritmo en base 2 de la fórmula de entropía.
- `os`: Para verificar la existencia de los archivos y manejar las rutas del sistema.
- `sys`: Para el manejo de argumentos y salida estándar.

> 💡 **Nota:** No requiere instalar ninguna librería externa con `pip`.

---

## 3. Cómo ejecutar el script

1. Abrí una terminal o consola.
2. Posicionate en la carpeta de la Actividad 3:
   ```bash
   cd PracticoDeMaquina/Actividad-3
   ```
3. Ejecutá el script de Python:
   ```bash
   python entropia.py
   ```

*(El script buscará automáticamente los archivos `texto_prueba.txt` y `texto_prueba.zip` ubicados en la misma carpeta).*

---

## 4. Documentación del Código y Complejidad `O(N)`

El código fuente (`entropia.py`) fue diseñado para cumplir estrictamente con el requerimiento de complejidad lineal `O(N)` y máxima eficiencia:

1. **Lectura por bloques (Chunks):**
   Aunque la consigna pide procesar "byte por byte", hacer lecturas individuales al disco por cada byte causaría una gran lentitud debido al costo de Entrada/Salida (I/O). Por ello, el archivo se abre en modo binario (`'rb'`) y se lee en bloques de 8192 bytes (8 KB). Luego se itera en memoria RAM sobre los bytes de cada bloque. De esta manera, cada byte del archivo se lee exactamente una vez, manteniendo la complejidad en tiempo estrictamente `O(N)`.

2. **Conteo en arreglo estático:**
   Se utiliza una lista de 256 posiciones inicializada en ceros (`frecuencias = [0] * 256`). Como un byte toma valores enteros entre 0 y 255, el valor del byte se utiliza directamente como índice (`frecuencias[byte] += 1`). Esto permite que cada operación de conteo se realice en tiempo constante `O(1)`.

3. **Cálculo de la Entropía de Shannon:**
   Una vez contabilizados todos los bytes, se calcula la probabilidad `p_i` de cada símbolo (donde `p_i = frecuencia / total_bytes`). Si `p_i > 0`, se aplica la sumatoria de Shannon:

   $$H = -\sum_{i=0}^{255} p_i \cdot \log_2(p_i)$$

4. **Cálculo de la Redundancia:**
   La entropía máxima posible para una fuente de 256 símbolos equiprobables es:

   $$H_{\max} = \log_2(256) = 8 \text{ bits/símbolo}$$

   La redundancia absoluta (`R`) mide la diferencia entre ese máximo teórico y la entropía real obtenida:

   $$R = H_{\max} - H = 8 - H$$

---

## 5. Resultados Obtenidos

Al ejecutar el programa sobre los dos archivos de prueba, obtuvimos los siguientes valores:

| Métrica | Texto Plano (`texto_prueba.txt`) | Archivo Comprimido (`texto_prueba.zip`) | Límite Teórico Máximo |
| :--- | :---: | :---: | :---: |
| **Tamaño del archivo** | **58.900 bytes** (~57,5 KB) | **1.247 bytes** (~1,2 KB) | — |
| **Entropía Empírica ($H$)** | **4,4394 bits/símbolo** | **6,7045 bits/símbolo** | 8,0000 bits/símbolo |
| **Redundancia Absoluta ($R$)** | **3,5606 bits/símbolo** | **1,2955 bits/símbolo** | 0,0000 bits/símbolo |
| **Reducción de Tamaño** | Base de comparación | **97,88 % más chico** | — |

---

## 6. Análisis Conceptual y Respuestas a las Preguntas

### ¿Por qué la entropía del archivo `.zip` se acerca al máximo teórico (8 bits/símbolo)?

1. **La naturaleza del texto plano:**
   En el lenguaje humano, los caracteres no tienen la misma probabilidad de aparecer. Por ejemplo, en español las vocales (como la 'a' y la 'e') y el carácter de espacio en blanco aparecen miles de veces, mientras que letras como la 'k', 'w' o 'x' aparecen muy poco. Además, existen pares de letras que se repiten con frecuencia (como "de", "que", "ción").
   
   Esta falta de uniformidad hace que la fuente sea muy predecible, lo que se traduce en una **entropía baja (4,44 bits/símbolo)** y una **alta redundancia (3,56 bits/símbolo)**. Casi la mitad de cada byte se gasta en información que estadísticamente ya es predecible.

2. **Cómo actúa la compresión ZIP:**
   Los algoritmos de compresión sin pérdida (como DEFLATE, combinación de LZ77 y codificación Huffman):
   - Buscan secuencias repetidas y las reemplazan por referencias cortas a apariciones previas (eliminando redundancia de repetición).
   - Asignan códigos de menos bits a los patrones más frecuentes y códigos más largos a los infrecuentes (codificación entrópica).

3. **Efecto sobre la distribución y la información:**
   Al eliminar casi todas las repeticiones y correlaciones estadísticas, los bytes que quedan en el archivo comprimido pasan a comportarse de forma prácticamente independiente y aleatoria:
   - Casi no hay patrones que se repitan en forma evidente.
   - La probabilidad de aparición de cada uno de los 256 bytes se vuelve mucho más uniforme.
   - La incertidumbre por byte aumenta significativamente, llevando la entropía empírica a **6,7045 bits/símbolo**, mucho más cerca del límite teórico de **8 bits/símbolo**.

### Conclusión

La compresión no "crea" ni "destruye" la información real del mensaje original: lo que hace es **empaquetarla en menos bytes**, eliminando los bits de redundancia. Por esa razón, a medida que un archivo está más eficientemente comprimido, cada uno de sus bytes individuales transporta más incertidumbre e información neta, acercando su entropía al valor máximo de 8 bits por símbolo.
