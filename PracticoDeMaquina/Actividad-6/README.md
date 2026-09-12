# Ejercicio 6 - Medición de Distancia entre Cadenas

## 1. ¿De qué se trata este trabajo?

En este ejercicio se comparan dos cadenas de texto para determinar qué tan diferentes son desde el punto de vista algorítmico.

Se implementan dos medidas:

- **Distancia de Hamming:** cuenta cuántas posiciones son diferentes entre dos cadenas de igual longitud.
- **Distancia de Levenshtein:** calcula la cantidad mínima de operaciones necesarias para transformar una cadena en otra. Las operaciones permitidas son inserción, eliminación y sustitución.

El objetivo es observar por qué la Distancia de Hamming es limitada cuando aparecen desfases o longitudes diferentes, mientras que Levenshtein permite trabajar con esos casos.

---

## 2. ¿Cómo funciona el programa?

### Distancia de Hamming

Se recorren las dos cadenas posición por posición.

Cada vez que los caracteres de una misma posición son diferentes, se incrementa la distancia en 1.

Por ejemplo:

```text
Juan Perez
Jaun Perez
```

Las cadenas tienen la misma longitud, por lo que Hamming puede calcularse. En este caso cuenta las posiciones que quedaron diferentes.

Si las cadenas tienen distinta longitud, Hamming no se puede aplicar directamente.

### Distancia de Levenshtein

Se utiliza una matriz de programación dinámica.

Cada posición de la matriz representa la cantidad mínima de operaciones necesarias para transformar un prefijo de la primera cadena en un prefijo de la segunda.

Las operaciones consideradas son:

- Inserción
- Eliminación
- Sustitución

Por ejemplo:

```text
Juan Perez
Juaan Perez
```

En este caso aparece un carácter adicional. Levenshtein puede detectarlo mediante una inserción.

---

## 3. ¿Cómo ejecutar el programa?

El programa está hecho en **Python 3** y no necesita librerías externas.

Desde la terminal, ubicarse en la carpeta:

```bash
cd PracticoDeMaquina/Actividad-6
```

Ejecutar:

```bash
python distancia_cadenas.py
```

También puede utilizarse:

```bash
python3 distancia_cadenas.py
```

El menú permite:

1. Comparar dos cadenas ingresadas por teclado.
2. Ejecutar los ejemplos del práctico.
3. Salir.

---

## 4. Ejemplos de prueba

### Ejemplo 1: Juan Perez vs Jaun Perez

```text
Distancia de Hamming: 2
Distancia de Levenshtein: 2
```

Hamming puede calcularse porque ambas cadenas tienen la misma longitud.

Sin embargo, este ejemplo muestra una modificación que cambia la posición de dos caracteres. Para un verdadero desfase de longitud se puede observar el siguiente caso.

### Ejemplo 2: Juan Perez vs Juaan Perez

```text
Distancia de Hamming: no aplicable (longitudes diferentes)
Distancia de Levenshtein: 1
```

Levenshtein detecta que alcanza con una inserción para transformar una cadena en la otra.

### Ejemplo 3: Horacio López vs Oracio López

Este es el ejemplo indicado en el enunciado. La distancia permite cuantificar el error producido al escribir el nombre.

---

## 5. Propuesta de solución / heurística

Para comparar textos se puede utilizar el siguiente proceso:

1. Normalizar las cadenas, por ejemplo pasando ambas a minúsculas y eliminando espacios innecesarios.
2. Verificar si tienen la misma longitud.
3. Si tienen la misma longitud, calcular Hamming para obtener una medida rápida de diferencias posición por posición.
4. Calcular Levenshtein cuando se necesite una comparación más flexible.
5. Interpretar una distancia pequeña como una alta similitud y una distancia grande como una menor similitud.

La principal ventaja de Levenshtein es que contempla inserciones, eliminaciones y sustituciones, por lo que resulta más apropiada para detectar errores de tipeo.

---

## 6. Conclusión

La Distancia de Hamming es sencilla y rápida, pero depende de que las cadenas tengan la misma longitud y compara únicamente posiciones correspondientes.

La Distancia de Levenshtein es más flexible porque permite encontrar la cantidad mínima de operaciones necesarias para transformar una cadena en otra. Por este motivo resulta más adecuada para comparar nombres o textos que pueden contener errores de tipeo, inserciones o eliminaciones.
