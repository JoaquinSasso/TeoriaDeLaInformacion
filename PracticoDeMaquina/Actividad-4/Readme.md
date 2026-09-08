

## Descripción del Proyecto
Este proyecto implementa una aplicación en Python que calcula el Índice de Coincidencia (IC) de un archivo leído byte por byte. El IC en criptografía mide la probabilidad de que dos elementos elegidos al azar en una secuencia sean idénticos.

El objetivo de esta actividad (Actividad 4) es calcular el IC para un archivo de texto puro (`.txt`) y su versión comprimida (`.zip`), y luego contrastar estos resultados con los valores de Entropía empírica y Redundancia obtenidos previamente en la Actividad 3.

## Documentación del Código

El script (`IC.py`) está diseñado para procesar archivos arbitrarios de manera eficiente:
1. **Lectura en bloques:** Se utiliza `archivo.read(8192)` para cargar el archivo en trozos (chunks) binarios en la RAM. Esto evita el alto costo computacional de hacer una llamada al disco por cada byte, manteniendo una complejidad temporal estricta de $O(N)$ donde $N$ es el tamaño total del archivo.
2. **Conteo de frecuencias:** Se emplea un arreglo estático de 256 posiciones (`frecuencias = [0] * 256`), el cual representa todos los valores decimales posibles de un byte. Acceder y sumar las repeticiones en este arreglo tiene un costo de $O(1)$.
3. **Cálculo del IC:** Una vez tabuladas las frecuencias absolutas ($f_i$) de todos los bytes y el total de bytes ($N$), se aplica la fórmula matemática iterando sobre el arreglo: sumando $f_i(f_i - 1)$ para las frecuencias mayores a 1, y dividiendo el total por $N(N - 1)$.

---

## Resultados y Comparativa (Actividad 3 vs Actividad 4)

Se analizaron los mismos archivos de prueba para contrastar ambas métricas:

### 1. Archivo de Texto Puro (`texto_prueba.txt`)
* **Tamaño:** 14,678 bytes
* **Índice de Coincidencia (IC):** 0.064664
* **Entropía:** 4.5406 bits/símbolo (Calculada en Ej. 3)
* **Redundancia:** 3.4594 bits/símbolo (Calculada en Ej. 3)

### 2. Archivo Comprimido (`texto_prueba.zip`)
* **Tamaño:** 6,338 bytes
* **Índice de Coincidencia (IC):** 0.004064
* **Entropía:** [COMPLETAR] bits/símbolo (Calculada en Ej. 3)
* **Redundancia:** [COMPLETAR] bits/símbolo (Calculada en Ej. 3)

---

## Interpretación Teórica Integrada

La comparación de estos resultados empíricos evidencia la profunda relación matemática entre el Índice de Coincidencia de la criptografía clásica y el concepto de Entropía de Shannon:

* **Análisis del Archivo de Texto (.txt):**
  El IC obtenido es de **0.0646**, un valor alto que se acerca al esperado para un texto en lenguaje natural. Este valor elevado demuestra que la distribución de probabilidad de los bytes es muy desigual; hay caracteres (como el espacio, las vocales y consonantes comunes) que aparecen repetidamente. Al haber tanta redundancia, es "fácil" adivinar la composición del texto o encontrar coincidencias al azar. Esto se refleja directamente en **su Entropía, que es baja (4.54 bits)**, indicando que cada byte aporta poca información nueva o sorpresa estadística y hay una gran redundancia (3.45 bits desperdiciados).

* **Análisis del Archivo Comprimido (.zip):**
  Los algoritmos de compresión buscan optimizar el espacio sustituyendo esos patrones repetitivos. Al eliminar la redundancia estructural, los bytes resultantes del archivo comprimido asumen una distribución de frecuencia mucho más homogénea (casi uniforme). Como consecuencia, la probabilidad de encontrar dos bytes idénticos al azar decae bruscamente, provocando que **el IC baje a 0.0040**. Este valor es extremadamente cercano al mínimo teórico absoluto para bytes equiprobables, que es $1/256 \approx 0.0039$.
  Simultáneamente, esta imprevisibilidad cuasi-perfecta hace que la cantidad de información pura contenida por cada byte sea mayor, empujando **la Entropía fuertemente hacia arriba**, acercándose al límite teórico de 8 bits por símbolo.

**Conclusión Final:** 
Ambas métricas exponen la misma realidad estadística pero desde ángulos complementarios. Existe una relación inversamente proporcional entre el IC y la Entropía: a mayor redundancia en los datos (como en el texto), mayor es la probabilidad de coincidencia (alto IC) y menor es la Entropía. Cuando se elimina esa redundancia mediante compresión (como en el archivo .zip), los datos se asemejan a ruido aleatorio uniforme, desplomando el Índice de Coincidencia al mínimo y maximizando la Entropía.
