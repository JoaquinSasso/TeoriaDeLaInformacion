# Ejercicio 8 - Capacidad de Canal por Búsqueda Exhaustiva (Binario a Cuaternario)

## 1. ¿De qué trata este trabajo?

El objetivo de este ejercicio es calcular numéricamente la **Capacidad de Canal ($C$)** de un canal discreto sin memoria (DMC) mediante un algoritmo de búsqueda exhaustiva (fuerza bruta).

El sistema modelado cuenta con:
- **Entrada binaria:** $X \in \{0, 1\}$ ($2$ símbolos posibles).
- **Salida cuaternaria:** $Y \in \{0, 1, 2, 3\}$ ($4$ símbolos posibles).
- **Matriz de transición hacia adelante:** $P(Y|X)$ de tamaño $2 \times 4$, donde cada elemento $P(y_j|x_i)$ representa la probabilidad condicional de recibir el símbolo $y_j$ dado que se transmitió $x_i$.

El programa permite resolver tanto canales **uniformes** (simétricos) como **no uniformes** (asimétricos).

---

## 2. Fundamento Matemático y Algoritmo

Para determinar la capacidad, el programa aplica las definiciones formales de la Teoría de la Información:

1. **Barrido Exhaustivo de la Fuente de Entrada:**
   Se varía la probabilidad del símbolo de entrada $P(X=0)$ en incrementos de $0,01$ desde $0,00$ hasta $1,00$ ($101$ distribuciones evaluadas en total):
   $$P(X=1) = 1 - P(X=0)$$

2. **Probabilidades de Salida (Teorema de la Probabilidad Total):**
   Para cada distribución de entrada, se calculan las probabilidades de los 4 símbolos de salida:
   $$P(y_j) = \sum_{i=0}^{1} P(x_i) \cdot P(y_j|x_i) = P(X=0) \cdot P(y_j|X=0) + P(X=1) \cdot P(y_j|X=1)$$

3. **Entropía de la Salida ($H(Y)$):**
   Mide la incertidumbre promedio recibida en el destino:
   $$H(Y) = -\sum_{j=0}^{3} P(y_j) \log_2 P(y_j)$$

4. **Entropía Condicional o Ruido del Canal ($H(Y|X)$):**
   Mide la incertidumbre que subsiste en la salida conociendo la entrada transmitida:
   $$H(Y|X) = \sum_{i=0}^{1} P(x_i) \cdot H(Y|X=x_i) = - \sum_{i=0}^{1} \sum_{j=0}^{3} P(x_i) P(y_j|x_i) \log_2 P(y_j|x_i)$$

5. **Información Mutua ($I(X;Y)$):**
   Representa la cantidad neta de información que atraviesa el canal con éxito:
   $$I(X;Y) = H(Y) - H(Y|X)$$

6. **Capacidad de Canal ($C$):**
   La capacidad es el valor máximo posible de información mutua sobre todas las posibles distribuciones de entrada:
   $$C = \max_{P(X)} I(X;Y)$$

---

## 3. ¿Cómo ejecutar el script?

El programa está desarrollado en **Python 3** y no requiere librerías externas (solo utiliza el módulo estándar `math`).

1. Abrir la terminal y situarse en la carpeta de la actividad:
   ```bash
   cd PracticoDeMaquina/Actividad-8
   ```

2. Ejecutar el script:
   ```bash
   python capacidad_canal_ejercicio_8.py
   ```

3. El programa presenta un menú interactivo:
   ```text
   ============================================================
   EJERCICIO 8 - CAPACIDAD DE CANAL
   ============================================================
   1. Ingresar matriz manualmente
   2. Ejecutar lote de prueba 1
   3. Ejecutar lote de prueba 2
   4. Ejecutar lote de prueba 3
   5. Ejecutar todos los lotes de prueba
   6. Salir
   ============================================================
   ```
   * Si se elige la **opción 1**, se pueden ingresar los 8 valores de la matriz separando por espacios. El programa valida automáticamente que cada fila sume exactamente $1$ y que todas las probabilidades estén entre $0$ y $1$.
   * Las **opciones 2 a 5** ejecutan los lotes de prueba predeterminados incorporados en el código.

---

## 4. Resultados Obtenidos y Análisis Teórico

El código incluye tres casos de estudio representativos para validar el comportamiento del algoritmo frente a distintos niveles de simetría y ruido:

### Caso 1: Canal Uniforme Simétrico
* **Matriz de transición $P(Y|X)$:**
  ```text
  X=0 -> [0.7, 0.1, 0.1, 0.1]
  X=1 -> [0.1, 0.7, 0.1, 0.1]
  ```
* **Resultados:**
  * **Capacidad $C$:** $\approx 0,365148 \text{ bits/símbolo}$
  * **Distribución óptima:** $P(X=0) = 0,50 \quad | \quad P(X=1) = 0,50$
* **Análisis Teórico:**
  Las filas de la matriz son permutaciones entre sí (el canal es simétrico respecto a la dispersión de ruido). En este tipo de canales, la entropía condicional de cada fila es idéntica:
  $$H(Y|X=0) = H(Y|X=1) = -(0,7 \log_2 0,7 + 3 \times 0,1 \log_2 0,1) \approx 1,3568 \text{ bits/símbolo}$$
  Como el ruido $H(Y|X)$ es constante independientemente de $P(X)$, maximizar $I(X;Y) = H(Y) - H(Y|X)$ equivale puramente a maximizar la entropía de salida $H(Y)$. La distribución de entrada equiprobable ($P(X=0) = P(X=1) = 0,50$) genera la salida más uniforme posible, maximizando la información transmitida.

---

### Caso 2: Canal Determinista (Sin Ruido)
* **Matriz de transición $P(Y|X)$:**
  ```text
  X=0 -> [1.0, 0.0, 0.0, 0.0]
  X=1 -> [0.0, 1.0, 0.0, 0.0]
  ```
* **Resultados:**
  * **Capacidad $C$:** $1,000000 \text{ bit/símbolo}$
  * **Distribución óptima:** $P(X=0) = 0,50 \quad | \quad P(X=1) = 0,50$
* **Análisis Teórico:**
  Cada entrada produce una salida única e inequívoca ($Y=0$ para $X=0$, $Y=1$ para $X=1$). Por lo tanto, no existe ninguna pérdida por ruido:
  $$H(Y|X) = 0 \text{ bits/símbolo} \implies I(X;Y) = H(X)$$
  Dado que la entrada es binaria ($2$ estados), la máxima entropía de la fuente es $\log_2(2) = 1$ bit/símbolo, lo que se alcanza con equiprobabilidad ($P(X=0) = P(X=1) = 0,50$). Toda la información emitida por la fuente llega intacta al receptor.

---

### Caso 3: Canal Completamente Ruidoso (Inútil)
* **Matriz de transición $P(Y|X)$:**
  ```text
  X=0 -> [0.25, 0.25, 0.25, 0.25]
  X=1 -> [0.25, 0.25, 0.25, 0.25]
  ```
* **Resultados:**
  * **Capacidad $C$:** $0,000000 \text{ bits/símbolo}$
  * **Distribución óptima:** Indiferente (cualquier distribución da $0$)
* **Análisis Teórico:**
  Las filas de la matriz son idénticas: sin importar qué símbolo se envíe ($X=0$ o $X=1$), la salida siempre presenta una distribución uniforme entre los 4 estados ($P(Y=j) = 0,25$). La salida $Y$ es estadísticamente independiente de la entrada $X$.
  En consecuencia:
  $$H(Y) = \log_2(4) = 2 \text{ bits/símbolo}, \quad H(Y|X) = 2 \text{ bits/símbolo}$$
  $$I(X;Y) = H(Y) - H(Y|X) = 2 - 2 = 0 \text{ bits/símbolo}$$
  El canal es incapaz de transmitir información; el ruido destruye por completo cualquier señal enviada.

---

## 5. Conclusiones
* **Precisión de la búsqueda numérica:** El barrido en pasos de $\Delta p = 0,01$ evalúa exhaustivamente el espacio de probabilidades de una fuente binaria en cuestión de milisegundos, encontrando la capacidad y las probabilidades óptimas sin necesidad de cálculos diferenciales complejos.
* **Impacto de la simetría:** En canales donde el ruido afecta a todos los símbolos de igual manera, la capacidad se alcanza siempre con una fuente balanceada ($50\%$ ceros y $50\%$ unos). En canales asimétricos, la búsqueda exhaustiva permite identificar qué símbolo conviene enviar con mayor frecuencia para evadir las transiciones más ruidosas.
