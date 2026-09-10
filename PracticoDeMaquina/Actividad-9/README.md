# Ejercicio 9 - Simulación y Análisis de un Canal Binario Simétrico (BSC) con Sockets TCP

## 1. ¿De qué trata este trabajo?

El objetivo de esta actividad es modelar y analizar experimental y teóricamente un **Canal Binario Simétrico (BSC)** sin memoria mediante una arquitectura Cliente-Servidor en Python utilizando sockets TCP.

El sistema simula un canal de comunicaciones real donde:
- El **Servidor** actúa como una *"caja negra"*: recibe tramas binarias, aplica una probabilidad oculta de error de inversión de bits ($p$) y retransmite el mensaje ruidoso al cliente.
- El **Cliente** debe:
  1. Descubrir experimentalmente la probabilidad de error oculta $p$ calculando la tasa de error de bit (**BER - Bit Error Rate**) sobre tramas sintéticas de $10^2$, $10^4$ y $10^6$ bits.
  2. Demostrar la **Ley de los Grandes Números** analizando la convergencia del BER a medida que aumenta la longitud de las tramas.
  3. Comprobar visualmente el impacto del ruido del canal sobre un mensaje de texto humano.
  4. Realizar el **modelado matemático completo** del BSC descubierto: matriz de transición, entropía del ruido $H(p)$, información mutua $I(X;Y)$ y capacidad del canal $C$.
  5. Responder a las preguntas teóricas sobre las condiciones requeridas en la fuente para alcanzar la máxima capacidad del canal.

---

## 2. ¿Cómo ejecutar los programas?

El sistema está desarrollado en **Python 3** y utiliza únicamente módulos de la biblioteca estándar (`socket`, `struct`, `random`, `math`, `threading`).

Se deben abrir **dos consolas o terminales** independientes:

1. **Terminal 1 (Servidor):**
   ```bash
   cd PracticoDeMaquina/Actividad-9
   python servidor_bsc_ejercicio_9.py
   ```
   *El servidor inicializará el canal con la semilla determinista (`SEMILLA_CANAL = 2026`) y quedará a la espera de conexiones en el puerto 5555.*

2. **Terminal 2 (Cliente):**
   ```bash
   cd PracticoDeMaquina/Actividad-9
   python cliente_bsc_ejercicio_9.py
   ```
   *El cliente ejecutará automáticamente la batería de pruebas de la Fase 1, imprimirá el modelado teórico de la Fase 2 y finalmente solicitará una frase para verificar la alteración visual del texto.*

---

## 3. Fase 1: Resultados Experimentales y Análisis del BER

### 3.1. Batería de Pruebas y Convergencia

Para cada magnitud se transmitieron $5$ tramas aleatorias consecutivas a través del socket. Los resultados empíricos promedio obtenidos fueron los siguientes:

| Longitud de Trama ($N$) | Bits Totales Transmitidos | Errores Promedio por Trama | Rango de BER Empírico Observado | Comportamiento Estadístico |
| :---: | :---: | :---: | :---: | :--- |
| **$100$ bits** | $500$ bits | $4$ a $7$ errores | $0,040000$ — $0,070000$ | **Alta dispersión:** el tamaño de muestra es muy chico; un único error extra varía el BER en un punto porcentual completo ($\pm 25\%$). |
| **$10.000$ bits** | $50.000$ bits | $\approx 610$ errores | $0,059500$ — $0,064000$ | **Dispersión moderada:** la variabilidad relativa se reduce drásticamente (a menos del $5\%$). |
| **$1.000.000$ bits** | $5.000.000$ bits | $\approx 60.830$ errores | $0,060800$ — $0,060970$ | **Convergencia casi exacta:** el estimador se estabiliza con precisión de $4$ decimales. |

* **BER Empírico Global Estimado:**
  $$\hat{p} \approx 0,06097 \quad (6,10\%)$$
* **Probabilidad Real Oculta del Servidor:**
  Generada internamente con la semilla `2026`, el valor exacto es $p = 0,06096826\dots$

### 3.2. Análisis Teórico: La Ley de los Grandes Números

Cada bit individual transmitido por el canal representa una variable aleatoria de Bernoulli independiente $E_k \in \{0, 1\}$, donde $E_k = 1$ indica que el bit fue invertido con probabilidad $p$, y $E_k = 0$ indica que se transmitió correctamente con probabilidad $1-p$.

El BER empírico no es más que la media muestral de estos ensayos:
$$\bar{E}_N = \frac{1}{N} \sum_{k=1}^{N} E_k$$

Por la **Ley Débil de los Grandes Números** (Teorema de Bernoulli / Chebyshev), la varianza de la media muestral disminuye de forma inversamente proporcional a la cantidad de bits transmitidos:
$$\operatorname{Var}(\bar{E}_N) = \frac{p(1-p)}{N} \xrightarrow[N \to \infty]{} 0$$

* Para $N = 100$, la desviación estándar relativa es notablemente alta ($\approx 2,4\%$), lo que causa que el BER fluctúe fuertemente entre $0,04$ y $0,07$.
* Para $N = 1.000.000$, la desviación estándar decae a $\approx 0,024\%$. En este punto, la frecuencia relativa empírica converge en probabilidad a la esperanza matemática del canal:
  $$\lim_{N \to \infty} P(|\bar{E}_N - p| \ge \varepsilon) = 0$$

De esta forma, el cliente deduce con certeza la tasa de error física del canal sin tener acceso al código fuente del servidor.

---

## 4. Efecto Visual del Ruido en Mensajes de Texto

Al codificar un mensaje de texto plano en su representación binaria ASCII de 8 bits por carácter y transmitirlo a través del canal, se observa la degradación producida por los errores:

* **Frase original enviada:**
  ```text
  Teoria de la Informacion 2026
  ```
* **Frase recibida tras el canal:**
  ```text
  Teoria de  I^jOsoacin 202r
  ```

### ¿Por qué se producen estas alteraciones?
1. **Inversión de bits individuales:** Con un error del $\approx 6,10\%$, en una cadena de 29 caracteres ($232$ bits) se alteran en promedio unos $14$ bits distribuidos aleatoriamente a lo largo del mensaje.
2. **Impacto según el peso del bit alterado:**
   * Si el bit modificado es de **bajo peso** (bits 0, 1 o 2), el carácter original cambia por otro carácter cercano en la tabla ASCII (por ejemplo, el dígito `'6'` cuyo código binario es `00110110` sufre una inversión en su último bit pasando a `00110010` que corresponde al carácter `'2'`, o a `'r'`).
   * Si se altera un **bit de control o de alto peso**, el código resultante puede corresponder a caracteres de puntuación o a caracteres no imprimibles (apareciendo espacios en blanco anómalos o signos de interrogación invertidos).

---

## 5. Fase 2: Modelado Matemático y Capacidad del Canal BSC

Utilizando el valor de error descubierto $p \approx 0,060968$, se aplican las ecuaciones teóricas de Shannon para caracterizar formalmente el canal:

### 5.1. Matriz de Transición del Canal
Para un Canal Binario Simétrico, las probabilidades condicionales hacia adelante son:

$$P(Y|X) = \begin{pmatrix} P(Y=0|X=0) & P(Y=1|X=0) \\ P(Y=1|X=1) & P(Y=0|X=1) \end{pmatrix} = \begin{pmatrix} 1 - p & p \\ p & 1 - p \end{pmatrix}$$

Sustituyendo el valor empírico:
$$P(Y|X) = \begin{pmatrix} 0,939032 & 0,060968 \\ 0,060968 & 0,939032 \end{pmatrix}$$

### 5.2. Entropía Condicional (Ruido del Canal)
La incertidumbre que introduce el canal al invertir un bit se calcula mediante la función de entropía binaria:
$$H(Y|X) = H(p) = -p \log_2(p) - (1-p) \log_2(1-p)$$
$$H(0,060968) = -(0,060968 \log_2 0,060968 + 0,939032 \log_2 0,939032) \approx \mathbf{0,331277 \text{ bits/símbolo}}$$

Esto indica que el canal disipa aproximadamente $0,3313$ bits de incertidumbre por cada bit transmitido.

### 5.3. Capacidad del Canal ($C$)
La capacidad máxima teórica de cualquier BSC viene dada por:
$$C = 1 - H(p) = 1 - 0,331277 = \mathbf{0,668723 \text{ bits/símbolo}}$$

---

## 6. Respuestas al Análisis Teórico y Maximización

### Pregunta 1: ¿Logró su mensaje maximizar la capacidad del canal?
* **Con la trama sintética grande ($10^6$ bits):** **SÍ.**
  Al generar los bits aleatoriamente con la función `random.choice("01")`, la fuente emite ceros y unos con idéntica probabilidad ($P(X=0) \approx 0,500000$ y $P(X=1) \approx 0,500000$).
  
  La Información Mutua calculada para esta transmisión fue:
  $$I(X;Y) \approx 0,66872 \text{ bits/símbolo}$$
  
  La diferencia respecto de la Capacidad $C$ teórica ($0,668723$) fue menor al **$0,01\%$**, cumpliendo holgadamente con el margen de tolerancia exigido del $5\text{--}10\%$.

* **Con el mensaje de texto:** **NO.**
  En el texto en lenguaje natural codificado en ASCII, los bytes tienen frecuencias muy dispares y el bit más significativo (el octavo bit) siempre es $0$. En consecuencia, la fuente de bits no es equiprobable ($P(X=0) \neq 0,5$), lo que provoca que la entropía de salida sea menor a $1$ y la información mutua quede por debajo de la capacidad ($I(X;Y) < C$).

### Pregunta 2: ¿Qué característica debe tener la trama de bits enviada para que $I(X;Y) = C$?
Para que la Información Mutua $I(X;Y)$ alcance exactamente la Capacidad del Canal $C$, la fuente de entrada debe ser **estrictamente equiprobable**:
$$P(X=0) = P(X=1) = 0,50$$

#### Justificación analítica:
La definición general de Información Mutua es:
$$I(X;Y) = H(Y) - H(Y|X)$$

En un canal binario simétrico, el ruido del canal $H(Y|X) = H(p)$ es constante e independiente de la distribución de entrada. Por lo tanto, para maximizar $I(X;Y)$, se debe maximizar exclusivamente la entropía de la salida $H(Y)$:
$$\max I(X;Y) = \max_{P(X)} [H(Y)] - H(p)$$

Como la variable de salida $Y$ es binaria ($2$ estados: $0$ y $1$), su entropía alcanza el límite máximo posible de $1$ bit/símbolo ($\log_2 2 = 1$) si y solo si los símbolos de salida son equiprobables:
$$P(Y=0) = P(Y=1) = 0,50$$

Aplicando el Teorema de la Probabilidad Total sobre el BSC:
$$P(Y=0) = P(X=0)(1-p) + P(X=1)p$$
Sustituyendo $P(X=1) = 1 - P(X=0)$:
$$P(Y=0) = P(X=0)(1-2p) + p$$

Para que $P(Y=0) = 0,5$, despejamos $P(X=0)$:
$$0,5 - p = P(X=0)(1-2p) \implies P(X=0) = \frac{0,5 - p}{1 - 2p} = \frac{0,5(1 - 2p)}{1 - 2p} = \mathbf{0,50}$$

Queda demostrado que la condición necesaria y suficiente para maximizar el canal es que los bits de la fuente posean una distribución equiprobable ($50\%$ ceros y $50\%$ unos). En ese caso:
$$I(X;Y) = H(Y) - H(p) = 1 - H(p) = C$$
