# Ejercicio 8 - Capacidad de Canal por Búsqueda Exhaustiva

## ¿Qué pide el ejercicio?

Desarrollar un programa que calcule la capacidad de un **canal discreto sin memoria (DMC)** con:

- Entrada binaria: `X = {0, 1}`.
- Salida cuaternaria: `Y = {0, 1, 2, 3}`.
- Matriz de transición `P(Y|X)` de `2 x 4`.

El usuario debe ingresar los 8 valores de la matriz y el programa debe validar que cada fila tenga probabilidades válidas y sume 1.

Luego debe probar todas las distribuciones de entrada:

```text
P(X=0) = 0.00, 0.01, ..., 1.00
P(X=1) = 1 - P(X=0)
```

Para cada una calcula `P(Y)`, `H(Y)`, `H(Y|X)` e:

```text
I(X;Y) = H(Y) - H(Y|X)
```

La capacidad se obtiene mediante:

```text
C = max I(X;Y)
```

y se muestran `C`, `P(X=0)` óptima y `P(X=1)` óptima.

## ¿Cómo funciona?

El programa cuenta con un menú:

```text
1. Ingresar matriz manualmente
2. Ejecutar lote de prueba 1
3. Ejecutar lote de prueba 2
4. Ejecutar lote de prueba 3
5. Ejecutar todos los lotes de prueba
6. Salir
```

Los lotes de prueba están **incorporados directamente en el código**, por lo que no se necesita ningún archivo adicional.

Los casos incluidos son:

### Lote 1 - Canal uniforme simétrico

```text
0.7 0.1 0.1 0.1
0.1 0.7 0.1 0.1
```

Resultado esperado:

```text
C ≈ 0.365148 bits/símbolo
P(X=0) = 0.50
P(X=1) = 0.50
```

### Lote 2 - Canal determinista

```text
1 0 0 0
0 1 0 0
```

Resultado esperado:

```text
C = 1.000000 bits/símbolo
P(X=0) = 0.50
P(X=1) = 0.50
```

### Lote 3 - Canal completamente ruidoso

```text
0.25 0.25 0.25 0.25
0.25 0.25 0.25 0.25
```

Resultado esperado:

```text
C = 0.000000 bits/símbolo
```

## ¿Cómo ejecutarlo?

Se necesita **Python 3.x** y no se requieren librerías externas.

### Windows

```bash
python capacidad_canal_ejercicio_8_menu.py
```

### Linux / Ubuntu

```bash
python3 capacidad_canal_ejercicio_8_menu.py
```

Después simplemente se selecciona una opción del menú.

## Archivos de la entrega

```text
capacidad_canal_ejercicio_8_menu.py
README_ejercicio_8_menu.md
```

Los lotes de prueba están incluidos en `capacidad_canal_ejercicio_8_menu.py`.
