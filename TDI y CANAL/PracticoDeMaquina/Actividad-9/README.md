# Ejercicio 9 - Simulación y Análisis de un Canal Binario Simétrico (BSC) con Sockets TCP

## 1. ¿De qué trata este trabajo?

En esta actividad simulamos un **Canal Binario Simétrico (BSC)** mediante una arquitectura Cliente-Servidor en Python usando sockets TCP.

El canal funciona de la siguiente manera:
- **El Servidor** actúa como una *"caja negra"*: tiene una probabilidad oculta de error ($p$) que no conocemos de antemano. Recibe secuencias de bits enviadas por el cliente, invierte algunos ceros y unos al azar con esa probabilidad, y devuelve la secuencia alterada.
- **El Cliente** tiene como tarea:
  1. Descubrir experimentalmente ese porcentaje de error midiendo la tasa de error de bit (**BER - Bit Error Rate**) sobre tramas de $10^2$, $10^4$ y $10^6$ bits.
  2. Comprobar la **Ley de los Grandes Números** viendo cómo el BER se estabiliza a medida que mandamos tramas más grandes.
  3. Ver en la práctica cómo el ruido del canal altera una frase de texto legible.
  4. Realizar el **modelado matemático** del canal descubierto: calcular su matriz de transición, el ruido $H(p)$, la información mutua $I(X;Y)$ y la capacidad del canal $C$.
  5. Responder a las preguntas del práctico sobre qué condiciones debe tener la entrada para aprovechar al máximo la capacidad del canal.

---

## 2. ¿Cómo ejecutar los programas?

El sistema está desarrollado en **Python 3** y utiliza únicamente librerías estándar de Python (no hace falta instalar nada con `pip`).

Se deben abrir **dos consolas o terminales** diferentes:

1. **Terminal 1 (Servidor):**
   ```bash
   cd PracticoDeMaquina/Actividad-9
   python servidor_bsc_ejercicio_9.py
   ```
   *El servidor arranca con la semilla fijada por la cátedra (`SEMILLA_CANAL = 2026`) y se queda esperando conexiones en el puerto 5555.*

2. **Terminal 2 (Cliente):**
   ```bash
   cd PracticoDeMaquina/Actividad-9
   python cliente_bsc_ejercicio_9.py
   ```
   *El cliente se conecta, hace automáticamente las pruebas de bits de la Fase 1, imprime los cálculos teóricos de la Fase 2 y al final te pide escribir una frase para mostrar cómo el ruido altera el texto.*

---

## 3. Fase 1: Resultados Experimentales y Análisis del BER

### 3.1. Batería de Pruebas y Mediciones

Para cada tamaño de trama se enviaron $5$ secuencias aleatorias consecutivas al servidor. Los resultados promedio obtenidos fueron:

| Tamaño de Trama ($N$) | Bits Totales Transmitidos | Errores Promedio por Trama | Rango de BER Empírico Observado | Comportamiento Observado |
| :---: | :---: | :---: | :---: | :--- |
| **$100$ bits** | $500$ bits | $4$ a $7$ errores | $0,040000$ — $0,070000$ | **Mucha variación:** al ser una muestra muy chica, un solo error de más o de menos cambia el resultado un punto porcentual entero ($\pm 25\%$). |
| **$10.000$ bits** | $50.000$ bits | $\approx 610$ errores | $0,059500$ — $0,064000$ | **Variación moderada:** el resultado se vuelve bastante más estable (menos del $5\%$ de diferencia). |
| **$1.000.000$ bits** | $5.000.000$ bits | $\approx 60.830$ errores | $0,060800$ — $0,060970$ | **Casi exacto:** el valor se estabiliza con precisión de 4 decimales. |

* **Estimación empírica del error:**
  $$\hat{p} \approx 0,06097 \quad (6,10\%)$$
* **Probabilidad real oculta en el servidor:**
  Calculada a partir de la semilla `2026`, el valor exacto es $p = 0,06096826\dots$

### 3.2. ¿Cómo se explica esto con la Ley de los Grandes Números?

Cada bit que enviamos tiene una chance fija $p$ de fallar. Cuando enviamos tramas muy cortas (como 100 bits), el azar influye demasiado: si justo en esa tanda fallan 4 bits o fallan 7 bits, el error calculado salta de 4% a 7% (una variación enorme respecto al valor real).

En cambio, cuando transmitimos tandas masivas de **1.000.000 de bits**, la cantidad de errores se promedia y se equilibra. La **Ley de los Grandes Números** dice justamente esto: a medida que aumenta la cantidad de repeticiones de un experimento aleatorio, la frecuencia observada en la práctica se acerca cada vez más a la probabilidad real del sistema.

Gracias a esto, pudimos averiguar con total precisión que el servidor tiene configurado un error de aproximadamente **$6,10\%$** ($p \approx 0,06097$) sin necesidad de mirar su código fuente.

---

## 4. Efecto del Ruido en Mensajes de Texto

Para ver el impacto del canal sobre datos reales, convertimos una frase a código binario ASCII (8 bits por letra) y la transmitimos por el canal ruidoso:

* **Frase original enviada:**
  ```text
  Teoria de la Informacion 2026
  ```
* **Frase recibida tras el canal:**
  ```text
  Teoria de  I^jOsoacin 202r
  ```

### ¿Por qué se producen estos cambios?
1. **Inversión de bits:** Con un $6,10\%$ de error, en una frase de 29 letras ($232$ bits) se dan vuelta alrededor de $14$ bits al azar a lo largo del mensaje.
2. **Posición del bit que cambia:**
   * Si el bit que se invierte está al final del byte (bits menos significativos), la letra suele cambiarse por otra letra o número parecido en la tabla ASCII (por ejemplo, el dígito `'6'` se transformó en la letra `'r'`).
   * Si el bit que se invierte está al principio del byte (bits de mayor peso), el valor del byte cae en códigos de control o caracteres no imprimibles, lo que genera espacios en blanco raros o símbolos extraños.

---

## 5. Fase 2: Modelado Matemático y Capacidad del Canal BSC

Con el valor de error que descubrimos ($p \approx 0,060968$), calculamos las propiedades teóricas del canal:

### 5.1. Matriz de Transición del Canal
La matriz simplemente indica qué probabilidad tiene cada bit de llegar bien o de fallar:

$$P(Y|X) = \begin{pmatrix} 1 - p & p \\ p & 1 - p \end{pmatrix} = \begin{pmatrix} 0,939032 & 0,060968 \\ 0,060968 & 0,939032 \end{pmatrix}$$

Esto significa que un cero tiene $93,9\%$ de probabilidad de llegar como cero y $6,1\%$ de convertirse en uno, y al revés con el uno.

### 5.2. Ruido del Canal ($H(p)$)
El ruido que mete el canal al dar vuelta los bits se calcula con la fórmula de entropía binaria:
$$H(p) = -p \log_2(p) - (1-p) \log_2(1-p)$$
$$H(0,060968) = -(0,060968 \log_2 0,060968 + 0,939032 \log_2 0,939032) \approx \mathbf{0,331277 \text{ bits/símbolo}}$$

Esto significa que por cada bit que transmitimos, el ruido del canal nos "come" o nos hace perder alrededor de un tercio de bit de información.

### 5.3. Capacidad del Canal ($C$)
La capacidad máxima teórica de este canal es:
$$C = 1 - H(p) = 1 - 0,331277 = \mathbf{0,668723 \text{ bits/símbolo}}$$

Es la cantidad neta máxima de información limpia que el canal puede llegar a transportar por cada símbolo enviado.

---

## 6. Respuestas a las Preguntas Teóricas

### Pregunta 1: ¿Logró su mensaje maximizar la capacidad del canal?
* **Con la trama aleatoria de 1.000.000 de bits: SÍ.**  
  Al generar los bits al azar, la cantidad de ceros y unos quedó casi exactamente igualada ($50\%$ ceros y $50\%$ unos).  
  La Información Mutua obtenida fue:
  $$I(X;Y) \approx 0,66872 \text{ bits/símbolo}$$
  La diferencia respecto a la capacidad teórica ($0,668723$) fue menor al **$0,01\%$**, cumpliendo con holgura el margen del $5\text{--}10\%$ pedido en el práctico.

* **Con el mensaje de texto en español: NO.**  
  En el lenguaje humano los caracteres no son aleatorios: hay letras muy frecuentes (como las vocales) y en el código ASCII estándar el primer bit de cada letra siempre es cero. Al estar desbalanceada la cantidad de ceros y unos, la información transmitida queda por debajo de la capacidad máxima.

---

### Pregunta 2: ¿Qué característica debe tener la trama de bits enviada para que $I(X;Y) = C$?
Para que la Información Mutua $I(X;Y)$ alcance exactamente la Capacidad del Canal $C$, la fuente de entrada debe ser **estrictamente equiprobable**:
$$P(X=0) = P(X=1) = 0,50$$

#### Explicación:
La información neta que pasa por el canal es:
$$I(X;Y) = H(\text{salida}) - H(\text{ruido})$$

En un canal simétrico, el ruido siempre resta lo mismo ($0,3313$ bits) sin importar qué mandemos. Por lo tanto, para que la información que llega al final sea la máxima posible, la salida tiene que aprovechar todo su rango (alcanzar $1$ bit entero de entropía).

Como la salida es binaria, la única forma de que la salida tenga entropía máxima ($H(Y) = 1$) es que reciba mitad de ceros y mitad de unos ($50\%$ y $50\%$). Y por la simetría del canal, esto solo se logra si desde la entrada transmitimos la misma cantidad de ceros que de unos ($P(X=0) = P(X=1) = 0,50$).

En ese caso exacto:
$$I(X;Y) = 1 - H(p) = C$$
