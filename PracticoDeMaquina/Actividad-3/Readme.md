
# Cálculo de Entropía Empírica y Redundancia



## Descripción del Proyecto
Esta aplicación de software en Python lee un archivo arbitrario byte por byte (con una complejidad temporal de $O(N)$, siendo $N$ el tamaño del archivo en bytes) para calcular su entropía empírica y su redundancia absoluta. 

El programa permite comparar el nivel de información pura y redundancia estadística entre un archivo de texto plano (`.txt`) y su versión fuertemente comprimida (`.zip`).

## Ejecución
Para ejecutar el script, posicionarse en el directorio del proyecto y utilizar el intérprete de Python:
```bash
python entropia.py

```

*(Requiere tener los archivos de prueba en el mismo directorio que el script).*

## Documentación del Código

El script fue diseñado priorizando la eficiencia temporal para cumplir con la restricción $O(N)$.

1. **Lectura Eficiente ($O(N)$):**
Aunque el requerimiento lógico es procesar "byte por byte", realizar operaciones de I/O a nivel de disco por cada byte genera un cuello de botella severo. Para resolverlo, el archivo se lee en modo binario (`'rb'`) utilizando bloques (chunks) de 8192 bytes. Luego, se itera sobre los bytes de cada bloque en memoria RAM. La complejidad teórica se mantiene estrictamente lineal $O(N)$.
2. **Estructura de Datos de Frecuencias:**
Se utiliza un arreglo estático de 256 posiciones (`frecuencias = [0] * 256`). Dado que un byte tiene 8 bits, sus valores decimales van de 0 a 255. Acceder al índice correspondiente al valor del byte toma tiempo $O(1)$, evitando el costo de las funciones de hash asociadas a los diccionarios.
3. **Cálculo de Entropía (Fórmula de Shannon):**
Una vez contabilizadas las frecuencias totales, el programa calcula la probabilidad $p_i$ de cada símbolo (frecuencia del símbolo / total de bytes) y aplica la sumatoria: $H = -\sum p_i \log_2(p_i)$.
4. **Cálculo de Redundancia:**
La entropía máxima teórica para un alfabeto de 256 símbolos equiprobables es $\log_2(256) = 8$ bits/símbolo. La redundancia absoluta de los datos se calcula restando la entropía empírica obtenida del máximo teórico ($8 - H$).

---

## Interpretación de Resultados (Texto vs. Comprimido)

Al ejecutar el programa con un archivo de texto y su equivalente comprimido, se obtuvieron los siguientes resultados:

**1. Archivo de Texto Puro (`texto_prueba.txt`)**

* Tamaño: 58,250 bytes
* Entropía Empírica: 4.4004 bits/símbolo
* Redundancia: 3.5996 bits/símbolo

**2. Archivo Comprimido (`texto_prueba.zip`)**

* Tamaño: 1,247 bytes
* Entropía Empírica: 6.7045 bits/símbolo
* Redundancia: 1.2955 bits/símbolo

### Análisis Conceptual

Los resultados demuestran empíricamente cómo funcionan los algoritmos de compresión de datos (como DEFLATE, utilizado en formato ZIP) y su relación con la Teoría de la Información:

* **El archivo de texto plano** posee una entropía baja (4.40 bits/símbolo) y una alta redundancia (casi 3.6 bits/símbolo desperdiciados). Esto se debe a la naturaleza de los lenguajes naturales: ciertas letras (como las vocales o el espacio en blanco) tienen una frecuencia de aparición muchísimo mayor que otras. Esta distribución de probabilidad tan desigual genera "huecos" que el algoritmo de compresión aprovecha.
* **El archivo `.zip**`, por el contrario, reduce drásticamente el tamaño del archivo (de ~58KB a 1.2KB) al eliminar la redundancia estadística. El algoritmo agrupa los patrones repetitivos y los sustituye. Al hacer esto, los bytes resultantes en el archivo comprimido presentan una distribución de probabilidad mucho más uniforme.
* **Conclusión:** A medida que se elimina la redundancia en los datos, la entropía empírica se acerca al límite teórico máximo (8 bits/símbolo). El valor de 6.7045 bits en el archivo comprimido indica que la incertidumbre por byte aumentó significativamente; es decir, cada byte en el `.zip` aporta mayor "información pura" estadísticamente impredecible en comparación con el texto original.
