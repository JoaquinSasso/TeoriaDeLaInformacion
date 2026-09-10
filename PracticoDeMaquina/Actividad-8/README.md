# Ejercicio 8 - Capacidad de Canal por Búsqueda Exhaustiva (Binario a Cuaternario)

## 1. ¿De qué trata este trabajo?

En este ejercicio calculamos de forma numérica la **Capacidad de Canal ($C$)** de un canal con entrada binaria y salida de 4 símbolos, usando un método de **búsqueda exhaustiva** (probando paso a paso todas las posibles distribuciones de entrada).

El canal funciona de la siguiente manera:
- **Entrada binaria:** enviamos símbolos $X \in \{0, 1\}$ (2 opciones posibles).
- **Salida cuaternaria:** recibimos símbolos $Y \in \{0, 1, 2, 3\}$ (4 opciones posibles).
- **Matriz de transición $P(Y|X)$ ($2 \times 4$):** indica la probabilidad de recibir cada símbolo de salida según lo que se haya transmitido en la entrada.

El programa permite analizar tanto canales **simétricos** (donde el ruido afecta por igual a ambas entradas) como **asimétricos** (donde una entrada sufre más ruido que la otra).

---

## 2. ¿Cómo calcula el programa la capacidad?

El script evalúa cómo viaja la información siguiendo estos pasos:

1. **Barrido de la entrada:**  
   Prueba valores para la probabilidad de enviar un cero ($P(X=0)$) desde $0,00$ hasta $1,00$ en pasos de $0,01$ (101 pruebas en total). Como solo hay dos símbolos, la probabilidad de enviar un uno es:
   $$P(X=1) = 1 - P(X=0)$$

2. **Probabilidades de salida ($P(Y)$):**  
   Con la probabilidad de entrada y la matriz del canal, calcula qué tan probable es recibir cada una de las 4 salidas posibles.

3. **Entropía de salida ($H(Y)$):**  
   Mide la cantidad de incertidumbre o información total que llega al receptor:
   $$H(Y) = -\sum_{j=0}^{3} P(y_j) \log_2 P(y_j)$$

4. **Ruido del canal ($H(Y|X)$):**  
   Mide cuánta información se pierde o confunde en el camino por culpa del canal:
   $$H(Y|X) = \sum_{i=0}^{1} P(x_i) \cdot H(Y|X=x_i)$$

5. **Información Mutua ($I(X;Y)$):**  
   Es la información que realmente logra llegar limpia de la entrada a la salida:
   $$I(X;Y) = H(Y) - H(Y|X)$$

6. **Capacidad del Canal ($C$):**  
   Es el valor más alto de información mutua que se encontró durante todo el barrido, junto con la distribución de entrada ($P(X=0)$ y $P(X=1)$) que permitió alcanzarlo:
   $$C = \max_{P(X)} I(X;Y)$$

---

## 3. ¿Cómo ejecutar el script?

El programa está hecho en **Python 3** y no requiere instalar ninguna librería adicional.

1. Abrí la terminal y parate en la carpeta del ejercicio:
   ```bash
   cd PracticoDeMaquina/Actividad-8
   ```

2. Ejecutá el script:
   ```bash
   python capacidad_canal_ejercicio_8.py
   ```

3. El menú te permite ingresar matrices a mano o probar los casos ya incluidos:
   ```text
   ============================================================
   EJERCICIO 8 - CAPACIDAD DE CANAL
   ============================================================
   1. Ingresar matriz manualmente
   2. Lote 1: Canal uniforme simétrico (ruido idéntico por símbolo)
   3. Lote 2: Canal determinista (sin ruido, C = 1 bit/símbolo)
   4. Lote 3: Canal completamente ruidoso (salida independiente, C = 0)
   5. Lote 4: Canal asimétrico (ruido desigual, óptimo P(X) != 0.5)
   6. Ejecutar todos los lotes de prueba
   7. Salir
   ============================================================
   ```
   * Si elegís la **opción 1**, podés cargar los 8 valores de tu propia matriz. El script valida que cada fila sume exactamente $1$.
   * Las **opciones 2 a 5** corren directamente los casos de prueba cargados.
   * La **opción 6** corre todos los casos juntos.

---

## 4. Resultados y Análisis de los Casos de Prueba

El script incluye cuatro lotes de prueba para comprobar cómo se comporta el canal en distintas situaciones:

### Caso 1: Canal Uniforme Simétrico
* **Matriz $P(Y|X)$:**
  ```text
  X=0 -> [0.7, 0.1, 0.1, 0.1]
  X=1 -> [0.1, 0.7, 0.1, 0.1]
  ```
* **Resultados:**
  * **Capacidad $C$:** $\approx 0,365148 \text{ bits/símbolo}$
  * **Distribución óptima:** $P(X=0) = 0,50 \quad | \quad P(X=1) = 0,50$
* **¿Por qué da este resultado?**  
  El ruido afecta exactamente de la misma manera al $0$ que al $1$ (las dos filas tienen los mismos números, solo cambia el orden). Como el ruido del canal es parejo para ambos símbolos, la forma de transmitir la mayor cantidad de información limpia es enviar mitad de ceros y mitad de unos ($50\%$ y $50\%$).

---

### Caso 2: Canal Determinista (Sin Ruido)
* **Matriz $P(Y|X)$:**
  ```text
  X=0 -> [1.0, 0.0, 0.0, 0.0]
  X=1 -> [0.0, 1.0, 0.0, 0.0]
  ```
* **Resultados:**
  * **Capacidad $C$:** $1,000000 \text{ bit/símbolo}$
  * **Distribución óptima:** $P(X=0) = 0,50 \quad | \quad P(X=1) = 0,50$
* **¿Por qué da este resultado?**  
  No hay ninguna confusión: si mandamos un $0$ siempre sale un $0$, y si mandamos un $1$ siempre sale un $1$. El ruido es cero ($H(Y|X) = 0$). Como la entrada es binaria, lo máximo que se puede transmitir es $1$ bit por símbolo, y se aprovecha al $100\%$ cuando mandamos ambos símbolos con la misma frecuencia.

---

### Caso 3: Canal Completamente Ruidoso
* **Matriz $P(Y|X)$:**
  ```text
  X=0 -> [0.25, 0.25, 0.25, 0.25]
  X=1 -> [0.25, 0.25, 0.25, 0.25]
  ```
* **Resultados:**
  * **Capacidad $C$:** $0,000000 \text{ bits/símbolo}$
  * **Distribución óptima:** Cualquiera (siempre da $0$)
* **¿Por qué da este resultado?**  
  La salida da siempre lo mismo sin importar qué hayamos mandado en la entrada. El receptor no tiene forma de adivinar qué se transmitió, por lo que la información útil transmitida es cero. El ruido destruye por completo el mensaje.

---

### Caso 4: Canal Asimétrico (Ruido Desigual)
* **Matriz $P(Y|X)$:**
  ```text
  X=0 -> [0.7, 0.3, 0.0, 0.0]
  X=1 -> [0.2, 0.2, 0.3, 0.3]
  ```
* **Resultados:**
  * **Capacidad $C$:** $\approx 0,422713 \text{ bits/símbolo}$
  * **Distribución óptima:** $P(X=0) = 0,58 \quad | \quad P(X=1) = 0,42$
* **¿Por qué da este resultado?**  
  Acá las dos entradas sufren ruido diferente:
  - Cuando mandamos $0$, el resultado casi no se dispersa (solo puede salir $Y=0$ o $Y=1$).
  - Cuando mandamos $1$, el resultado se mezcla entre las cuatro salidas posibles con más confusión.
  
  Al ser más confiable el $0$ que el $1$, la mejor estrategia ya **no es $50/50$**: conviene mandar más veces el símbolo limpio ($58\%$ de ceros) y menos el símbolo ruidoso ($42\%$ de unos). Este caso muestra por qué sirve la búsqueda exhaustiva: en canales asimétricos, el óptimo no siempre es mitad y mitad.

---

## 5. Conclusiones

* **Fuerza bruta efectiva:** Al barrer con saltos de $0,01$, el programa evalúa 101 posibilidades en una fracción de segundo y encuentra la capacidad del canal de manera sencilla sin necesidad de resolver derivadas complicadas a mano.
* **Simétrico vs. Asimétrico:** Cuando el canal es parejo para todos los símbolos, la capacidad siempre se logra con una entrada balanceada ($50\%$ y $50\%$). Pero si un símbolo sufre más ruido que otro, el sistema rinde mejor si se usa con más frecuencia el símbolo más confiable.
