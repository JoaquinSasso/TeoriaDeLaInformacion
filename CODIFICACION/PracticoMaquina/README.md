# Compresor PPM-C — Práctico de Máquina 2

Teoría de la Información · 2026

Como "proveedor de compresión", nuestro grupo ofrece dos soluciones:

- **Solución propia:** PPM-C con codificación aritmética, escrito en Python sin librerías de compresión.
- **Solución externa:** ZIP (Deflate, preset normal).

Las dos se comparan contra el compresor de referencia de la cátedra, `gzip -6`, usando los archivos del corpus común.

## Cómo se usa

```
python compressor.py entrada.txt salida.tdi
python decompressor.py salida.tdi reconstruido.txt
```

El compresor muestra el tamaño original y comprimido, el ratio, el ahorro, el tiempo y el SHA-256 del original. El descompresor muestra el tiempo y el SHA-256 del archivo reconstruido; si los dos hashes coinciden, el archivo es idéntico al original.

Agregando `--traza` al compresor se ve cada paso del algoritmo, igual que en el Excel de la cátedra. Lo usamos para explicar la Prueba 1.

Para repetir el benchmark: `python benchmark.py`. Necesita tener `zip`, `unzip` y `gzip` instalados; en Windows vienen con Git Bash.

## Archivos

| Archivo | Contenido |
|---|---|
| `compressor.py` | compresor |
| `decompressor.py` | descompresor |
| `ppmc.py` | el algoritmo (modelo PPM-C y codificador aritmético), usado por los dos anteriores |
| `benchmark.py` | mide las tres soluciones sobre el corpus y guarda los resultados |
| `tests/corpus/` | archivos de prueba de la cátedra |
| `results/` | resultados del benchmark |

## Cómo funciona

La idea de fondo es simple: si podemos adivinar bien qué letra viene, podemos escribirla con pocos bits. Una letra muy probable cuesta menos de un bit; una inesperada cuesta varios.

**PPM-C se encarga de adivinar.** Mira las dos letras anteriores y se fija qué vino después de ellas las veces anteriores. Por ejemplo, si después de "AB" siempre vino "R", la próxima "R" después de "AB" va a ser muy barata.

Si la letra nunca apareció después de esas dos, el programa escribe un aviso de **escape** y prueba con menos información. Primero mira solo la letra anterior, después cuenta cuántas veces apareció cada letra en todo el texto y, como último recurso, trata todos los caracteres posibles como igual de probables. En cada nivel, la probabilidad de cada letra es cuántas veces apareció, y el escape recibe tanto peso como letras distintas haya en ese nivel. Esa regla es lo que distingue a la variante "C" de PPM.

Después de escribir cada letra, el modelo actualiza sus cuentas. Así va aprendiendo mientras avanza.

**La codificación aritmética convierte esas probabilidades en bits.** Representa todo el mensaje como un único número entre 0 y 1. Cada letra achica el intervalo donde puede estar ese número: mucho si era improbable, poco si era esperable. Cuando el intervalo queda de un solo lado de la mitad, el primer bit ya está decidido y se escribe. Son las reglas E1, E2 y E3 del apunte.

**Descomprimir es hacer lo mismo al revés.** El descompresor arranca sin saber nada, igual que el compresor, y aprende exactamente las mismas cuentas a medida que recupera letras. Por eso no hace falta guardar ninguna tabla en el archivo.

Respecto del ejemplo del Excel hicimos dos cambios, necesarios para comprimir archivos reales:

- El nivel más bajo tiene los 256 valores posibles de un byte en vez de 64 letras. Así funciona con tildes, ñ, saltos de línea o cualquier otro carácter.
- Las cuentas se hacen con números enteros en vez de decimales. Con decimales, el compresor y el descompresor pueden redondear distinto y el archivo se reconstruye mal.

## Qué guarda el archivo `.tdi`

Una cabecera de 14 bytes y después los bits comprimidos:

| Campo | Bytes | Para qué |
|---|---:|---|
| `PPMC` | 4 | reconocer que el archivo es nuestro |
| versión | 1 | reconocer el formato |
| orden | 1 | cuántas letras anteriores mira el modelo (2) |
| tamaño original | 4 | indica al descompresor cuándo parar |
| CRC-32 | 4 | detecta si el archivo se dañó |

Al principio guardábamos el SHA-256 completo en la cabecera, pero ocupaba 32 bytes y en el archivo pequeño eso nos hacía perder. Como la consigna pide una cabecera mínima, lo cambiamos por un CRC-32, el mismo control que usa gzip. La comparación de SHA-256 se sigue haciendo con los hashes que muestran los programas.

El descompresor avisa si el archivo no existe, si no es un `.tdi`, si la cabecera está incompleta o si el contenido está dañado.

## Solución externa: ZIP

Usamos Info-ZIP 3.0 con `zip -6 -X -j`: nivel normal, sin cifrado, sin atributos extra ni rutas de carpetas. Para descomprimir, `unzip -p`.

ZIP usa Deflate. Primero busca fragmentos que ya aparecieron antes y los reemplaza por una referencia del tipo "copiar 200 letras desde 2000 posiciones atrás". Después codifica el resultado con Huffman. Es el mismo método de gzip; la diferencia es que ZIP guarda más información alrededor (nombre del archivo, índice), porque está pensado para empaquetar muchos archivos juntos.

## Resultados

Mediana de 15 repeticiones. En todos los casos el archivo reconstruido fue idéntico al original (SHA-256).

| Archivo | Solución | Tamaño comprimido | Ratio | Ahorro | T. compresión | T. descompresión |
|---|---|---:|---:|---:|---:|---:|
| Prueba 1 (64 B) | **PPM-C** | **50 B** | **1.28** | **21.9 %** | 15.0 ms | 15.6 ms |
| | ZIP | 179 B | 0.36 | −179.7 % | 1.4 ms | 1.9 ms |
| | gzip | 59 B | 1.09 | 7.8 % | 1.0 ms | 1.6 ms |
| Prueba 2 (100 KiB) | PPM-C | 25 484 B | 4.02 | 75.1 % | 396 ms | 390 ms |
| | ZIP | 2 051 B | 49.93 | 98.0 % | 1.8 ms | 2.5 ms |
| | **gzip** | **1 919 B** | **53.36** | **98.1 %** | 1.6 ms | 1.9 ms |
| Prueba 3 (100 KiB) | PPM-C | 5 177 B | 19.78 | 94.9 % | 304 ms | 299 ms |
| | ZIP | 1 050 B | 97.52 | 99.0 % | 1.8 ms | 3.2 ms |
| | **gzip** | **914 B** | **112.04** | **99.1 %** | 1.8 ms | 1.9 ms |
| Prueba 4 (100 KiB) | PPM-C | 98 631 B | 1.04 | 3.7 % | 947 ms | 1038 ms |
| | ZIP | 85 343 B | 1.20 | 16.7 % | 5.4 ms | 3.3 ms |
| | **gzip** | **85 207 B** | **1.20** | **16.8 %** | 4.3 ms | 2.6 ms |

**Weissman Score** (Pruebas 2 a 4 juntas, tiempos en ms, gzip = 1):

| Solución | Ratio global | Tiempo total | Weissman |
|---|---:|---:|---:|
| gzip | 3.49 | 7.9 ms | 1.00 |
| ZIP | 3.47 | 8.9 ms | 0.94 |
| PPM-C | 2.38 | 1661 ms | 0.19 |

La tabla completa, con throughput, overhead de cabecera y Weissman por archivo, está en `results/resultados.md`.

## Análisis

**Prueba 1 (archivo pequeño).** Es la única que gana PPM-C. En un archivo de 64 bytes pesa mucho lo que cada formato agrega además de los datos. Nuestra cabecera es de 14 bytes y la de gzip, de 18. Además, PPM-C aprende rápido: la segunda vez que aparece "ABRA" ya predice cada letra casi sin error. ZIP agranda el archivo casi tres veces solo por la información de contenedor que guarda.

**Pruebas 2 y 3 (texto y alta repetición).** Acá ZIP y gzip comprimen entre 5 y 13 veces más que PPM-C. Al mirar los archivos se entiende por qué: el "texto natural" tiene más de mil líneas, pero solo 68 distintas, porque los mismos párrafos se repiten una y otra vez. La prueba 3 es parecida, con siete tipos de línea repetidos. Deflate detecta que un párrafo entero ya apareció y lo reemplaza por una referencia corta. PPM-C, en cambio, solo mira las dos letras anteriores: sabe qué letra suele venir después de "la", pero no puede darse cuenta de que está en un párrafo que ya vio completo. Para este tipo de datos, un método que busca repeticiones largas es claramente mejor.

**Prueba 4 (baja repetición).** El texto es casi aleatorio, así que nadie comprime mucho: gzip ahorra 17 % y PPM-C solo 4 %. PPM-C rinde peor porque intenta aprender qué letra sigue a cada par de letras. Con 95 caracteres distintos hay más de 9000 pares posibles, y casi ninguno se repite lo suficiente para aprender algo útil. El modelo termina pagando muchos escapes sin obtener nada a cambio.

**Tiempos.** PPM-C es mucho más lento. Por un lado, el método hace más trabajo por cada letra: consulta tablas, calcula probabilidades y actualiza cuentas, mientras que Deflate puede copiar párrafos enteros de una vez. Por otro, el **lenguaje influye mucho en el benchmark**: nuestro compresor está en Python, un lenguaje interpretado, y ZIP y gzip son programas en C muy optimizados. Solo iniciar Python ya cuesta unos 13 ms, más que comprimir cualquiera de los archivos con gzip. Por eso el Weissman de PPM-C (0.19) refleja tanto el algoritmo como el lenguaje, y conviene leerlo junto con el ratio.

**ZIP contra gzip.** Los datos comprimidos por los dos tienen exactamente el mismo tamaño, porque usan el mismo Deflate. Toda la diferencia está en los 140–150 bytes extra que guarda ZIP como contenedor. Para un solo archivo, gzip es más eficiente; ZIP conviene cuando hay que empaquetar varios.
