# Ejercicio 9 - Simulación y Análisis de un Canal Binario Simétrico (BSC)

## ¿Qué pide el ejercicio?

Desarrollar una aplicación **Cliente-Servidor mediante sockets TCP** para simular un **Canal Binario Simétrico (BSC)**.

El servidor funciona como una "caja negra" y oculta la probabilidad de error `p` del canal. El cliente debe descubrirla experimentalmente mediante el cálculo del **BER (Bit Error Rate)**.

Para esto se deben transmitir tramas binarias aleatorias de diferentes magnitudes, compararlas bit a bit con las tramas recibidas y analizar la convergencia del BER.

Finalmente se debe transmitir una frase de texto convertida a binario para observar visualmente el efecto del ruido.

## ¿Cómo funciona?

El sistema está compuesto por dos programas:

```text
servidor_bsc_ejercicio_9.py
cliente_bsc_ejercicio_9.py
```

El servidor recibe una trama binaria, aplica errores de acuerdo con la probabilidad `p` del canal y devuelve una trama de la misma longitud.

El cliente realiza las pruebas con:

```text
100 bits
10.000 bits
1.000.000 bits
```

Para cada trama calcula:

```text
BER = bits erróneos / bits transmitidos
```

Se realizan varias transmisiones para cada tamaño y se observa cómo el BER empírico se aproxima a un valor estable al aumentar la cantidad de bits, de acuerdo con la **Ley de los Grandes Números**.

Además, el cliente realiza el análisis teórico del BSC:

- Matriz de transición.
- Probabilidades de la fuente.
- Información Mutua `I(X;Y)`.
- Capacidad del Canal `C`.
- Comparación entre `I(X;Y)` y `C`.

Por último, se solicita una frase, se convierte a una secuencia de bits, se transmite por el canal y se vuelve a convertir a texto para observar los errores producidos.

## ¿Cómo ejecutarlo?

Se necesita **Python 3.x** y no se requieren librerías externas.

Se deben utilizar **dos terminales**.

### Windows

En la primera terminal iniciar el servidor:

```bash
python servidor_bsc_ejercicio_9.py
```

En la segunda terminal ejecutar el cliente:

```bash
python cliente_bsc_ejercicio_9.py
```

### Linux / Ubuntu

En la primera terminal:

```bash
python3 servidor_bsc_ejercicio_9.py
```

En la segunda terminal:

```bash
python3 cliente_bsc_ejercicio_9.py
```

El servidor debe permanecer ejecutándose mientras el cliente realiza las pruebas.

## Resultados esperados

Las tramas pequeñas pueden producir valores de BER con mayor variación debido a la menor cantidad de bits analizados.

Al aumentar el tamaño de las tramas, el BER empírico debería estabilizarse alrededor de la probabilidad de error `p` del canal.

El análisis teórico permite relacionar los resultados experimentales con la información mutua y la capacidad del BSC.

La transmisión de texto permite visualizar directamente el efecto de los errores sobre un mensaje.

## Archivos de la entrega

```text
servidor_bsc_ejercicio_9.py
cliente_bsc_ejercicio_9.py
README_ejercicio_9.md
```

Las pruebas experimentales y los cálculos teóricos están incluidos directamente en `cliente_bsc_ejercicio_9.py`, por lo que no se necesita un archivo de pruebas separado.
