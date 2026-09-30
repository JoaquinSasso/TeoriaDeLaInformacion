# Ejercicio 7 - Detección de Errores: Códigos de Control (Checksum)

## 1. ¿De qué se trata este trabajo?

El objetivo de este ejercicio es implementar un sistema de detección de errores utilizando el dígito verificador del **CUIT/CUIL**.

El CUIT/CUIL está formado por 11 dígitos:

```text
XX-XXXXXXXX-X
```

Los primeros 10 dígitos se utilizan para calcular el último dígito, llamado **dígito verificador**.

El programa solicita un CUIT/CUIL, calcula cuál debería ser su dígito verificador mediante el algoritmo de **Módulo 11** y lo compara con el último dígito ingresado.

---

## 2. ¿Cómo funciona el algoritmo?

Se toman los primeros 10 dígitos y se multiplican por los siguientes pesos:

```text
5 4 3 2 7 6 5 4 3 2
```

Se suman todos los productos.

Luego:

```text
resto = suma % 11
digito = 11 - resto
```

Para obtener el dígito verificador se aplican las reglas:

```text
si digito = 11 -> 0
si digito = 10 -> 9
```

El resultado se compara con el undécimo dígito ingresado.

Si coinciden:

```text
CUIT/CUIL -> Válida
```

Si no coinciden:

```text
CUIT/CUIL -> Inválida
```

---

## 3. ¿Por qué funciona como código de detección de errores?

El último dígito no es independiente de los otros 10.

Se obtiene matemáticamente a partir de ellos. Por lo tanto, si uno de los primeros dígitos cambia accidentalmente, en general el cálculo produce otro dígito verificador.

Al comparar el dígito ingresado con el dígito esperado, el programa puede detectar muchas alteraciones o errores de tipeo.

Es un **código de detección de errores**, no un mecanismo de corrección: permite detectar que existe una inconsistencia, pero no necesariamente determinar cuál fue el dígito original.

---

## 4. ¿Cómo ejecutar el programa?

El programa está hecho en **Python 3** y no necesita librerías externas.

Desde la terminal, ubicarse en la carpeta:

```bash
cd PracticoDeMaquina/Actividad-7
```

Ejecutar:

```bash
python validar_cuit.py
```

También puede utilizarse:

```bash
python3 validar_cuit.py
```

El programa permite ingresar el CUIT/CUIL con o sin guiones.

Por ejemplo:

```text
20-27003456-0
```

o:

```text
20270034560
```

Ambos formatos son aceptados porque el programa elimina los guiones antes de realizar el cálculo.

---

## 5. Ejemplo de cálculo

Para:

```text
20-27003456-0
```

Se utilizan los primeros 10 dígitos:

```text
2 0 2 7 0 0 3 4 5 6
```

y los pesos:

```text
5 4 3 2 7 6 5 4 3 2
```

Se calcula:

```text
2×5 + 0×4 + 2×3 + 7×2 + 0×7
+ 0×6 + 3×5 + 4×4 + 5×3 + 6×2
```

La suma es:

```text
110
```

Entonces:

```text
110 % 11 = 0
11 - 0 = 11
```

Como el resultado es 11, el dígito verificador es:

```text
0
```

Por lo tanto:

```text
20-27003456-0
```

pasa la validación del algoritmo.

---

## 6. Pruebas que realiza el programa

El programa verifica:

- Que se hayan ingresado exactamente 11 dígitos.
- Que todos los caracteres sean numéricos después de eliminar guiones y espacios.
- El cálculo del dígito verificador.
- La comparación entre el dígito ingresado y el esperado.

También muestra por pantalla cada multiplicación, la suma total, el resto y el dígito verificador esperado.

---

## 7. Conclusión

El dígito verificador del CUIT/CUIL puede utilizarse como un mecanismo de detección de errores porque existe una relación matemática entre los primeros 10 dígitos y el último.

El algoritmo de Módulo 11 permite comprobar esa relación de manera sencilla. Si el dígito calculado no coincide con el ingresado, el número presenta una inconsistencia y se informa como inválido.

El método permite detectar errores comunes de tipeo, aunque no constituye un sistema de corrección de errores.
