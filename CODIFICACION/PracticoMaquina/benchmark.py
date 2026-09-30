"""
Benchmark del práctico: compresor propio (PPM-C) vs. solución externa (ZIP)
vs. baseline de la cátedra (gzip -n -6), sobre el corpus común.

Uso:  python benchmark.py [repeticiones]        (por defecto 7)

Todos los tiempos se miden igual para todas las herramientas: reloj de pared
alrededor del proceso completo (incluye arrancar el programa), en milisegundos.
Se hace una corrida de calentamiento y se toma la MEDIANA de las repeticiones.
"""

import csv
import hashlib
import math
import os
import platform
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
import zipfile

from ppmc import TAMANO_CABECERA

RAIZ = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(RAIZ, "tests", "corpus")
RESULTADOS = os.path.join(RAIZ, "results")

ARCHIVOS = [
    ("Prueba 1", "prueba_1_pequena.txt"),
    ("Prueba 2", "prueba_2_texto_natural.txt"),
    ("Prueba 3", "prueba_3_alta_repeticion.txt"),
    ("Prueba 4", "prueba_4_baja_repeticion.txt"),
]
PRUEBAS_DE_RENDIMIENTO = ["Prueba 2", "Prueba 3", "Prueba 4"]   # la 1 no entra al ranking temporal


# ---------------------------------------------------------------------------
# Herramientas: cómo comprimir y descomprimir con cada una
# Cada función recibe rutas y devuelve la lista de argumentos del comando.
# Si 'salida_por_stdout' es True, lo que imprime el comando se guarda en el archivo.
# ---------------------------------------------------------------------------

def herramientas():
    py = sys.executable
    return [
        {"nombre": "PPM-C (propio)", "ext": ".tdi", "stdout": False,
         "comprimir":    lambda e, s: [py, os.path.join(RAIZ, "compressor.py"), e, s],
         "descomprimir": lambda e, s: [py, os.path.join(RAIZ, "decompressor.py"), e, s],
         "cabecera":     lambda ruta: TAMANO_CABECERA},
        {"nombre": "ZIP -6 (externa)", "ext": ".zip", "stdout": True,
         # -6 nivel normal de Deflate, -X sin atributos extra, -j sin rutas, -q silencioso, '-' a stdout
         "comprimir":    lambda e, s: ["zip", "-6", "-X", "-j", "-q", "-", e],
         "descomprimir": lambda e, s: ["unzip", "-p", e],
         # overhead = todo lo que no es el stream Deflate (headers local + central + nombre)
         "cabecera":     lambda ruta: os.path.getsize(ruta) - zipfile.ZipFile(ruta).infolist()[0].compress_size},
        {"nombre": "gzip -6 (baseline)", "ext": ".gz", "stdout": True,
         "comprimir":    lambda e, s: ["gzip", "-n", "-6", "-c", e],
         "descomprimir": lambda e, s: ["gzip", "-d", "-c", e],
         "cabecera":     lambda ruta: 18},   # 10 bytes de cabecera + 8 de CRC32/tamaño
    ]


def ejecutar(comando, archivo_stdout=None):
    """Corre el comando y devuelve el tiempo de pared en ms."""
    inicio = time.perf_counter()
    if archivo_stdout:
        with open(archivo_stdout, "wb") as f:
            proceso = subprocess.run(comando, stdout=f, stderr=subprocess.PIPE)
    else:
        proceso = subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    fin = time.perf_counter()
    if proceso.returncode != 0:
        raise RuntimeError(f"falló {' '.join(comando)}: {proceso.stderr.decode(errors='replace')}")
    return (fin - inicio) * 1000


def medir(herramienta, entrada, carpeta, repeticiones):
    comprimido = os.path.join(carpeta, "salida" + herramienta["ext"])
    reconstruido = os.path.join(carpeta, "reconstruido.txt")
    usar_stdout = herramienta["stdout"]

    def comprimir():
        if os.path.exists(comprimido):
            os.remove(comprimido)
        cmd = herramienta["comprimir"](entrada, comprimido)
        return ejecutar(cmd, comprimido if usar_stdout else None)

    def descomprimir():
        cmd = herramienta["descomprimir"](comprimido, reconstruido)
        return ejecutar(cmd, reconstruido if usar_stdout else None)

    comprimir(); descomprimir()                       # calentamiento
    tiempos_c = [comprimir() for _ in range(repeticiones)]
    tiempos_d = [descomprimir() for _ in range(repeticiones)]

    with open(entrada, "rb") as f:
        sha_original = hashlib.sha256(f.read()).hexdigest()
    with open(reconstruido, "rb") as f:
        sha_reconstruido = hashlib.sha256(f.read()).hexdigest()

    return {
        "tam_comprimido": os.path.getsize(comprimido),
        "cabecera": herramienta["cabecera"](comprimido),
        "tiempos_c": tiempos_c,
        "tiempos_d": tiempos_d,
        "integro": sha_original == sha_reconstruido,
    }


def weissman(ratio, tiempo_ms, ratio_ref, tiempo_ref_ms):
    """W = α · (R / Rref) · (log Tref / log T), con α = 1 y tiempos en ms."""
    return (ratio / ratio_ref) * (math.log(tiempo_ref_ms) / math.log(tiempo_ms))


def version(cmd, linea=0):
    try:
        salida = subprocess.run(cmd, capture_output=True, text=True)
        return (salida.stdout or salida.stderr).strip().splitlines()[linea]
    except (OSError, IndexError):
        return "no disponible"


def main():
    repeticiones = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    for requerido in ("zip", "unzip", "gzip"):
        if not shutil.which(requerido):
            sys.exit(f"Falta '{requerido}' en el PATH (en Windows vienen con Git Bash).")

    os.makedirs(RESULTADOS, exist_ok=True)
    filas = []
    por_repeticion = {}   # (herramienta, prueba) -> lista de tiempos, para el Weissman global

    with tempfile.TemporaryDirectory() as carpeta:
        for herramienta in herramientas():
            for prueba, nombre in ARCHIVOS:
                entrada = os.path.join(CORPUS, nombre)
                print(f"{herramienta['nombre']:<20} {prueba} ...", flush=True)
                m = medir(herramienta, entrada, carpeta, repeticiones)
                original = os.path.getsize(entrada)
                tc = statistics.median(m["tiempos_c"])
                td = statistics.median(m["tiempos_d"])
                por_repeticion[(herramienta["nombre"], prueba)] = m["tiempos_c"]
                filas.append({
                    "prueba": prueba, "archivo": nombre, "algoritmo": herramienta["nombre"],
                    "original_B": original, "comprimido_B": m["tam_comprimido"],
                    "ratio": original / m["tam_comprimido"],
                    "ahorro_%": (1 - m["tam_comprimido"] / original) * 100,
                    "tam_relativo_%": m["tam_comprimido"] / original * 100,
                    "bits_por_byte": m["tam_comprimido"] * 8 / original,
                    "t_comp_ms": tc, "t_desc_ms": td,
                    "v_comp_MBs": original / 1e6 / (tc / 1000),
                    "v_desc_MBs": original / 1e6 / (td / 1000),
                    "cabecera_B": m["cabecera"],
                    "overhead_%": m["cabecera"] / m["tam_comprimido"] * 100,
                    "integridad": "OK" if m["integro"] else "FALLA",
                })

    # Weissman por archivo, contra gzip en el mismo archivo
    base = {f["prueba"]: f for f in filas if f["algoritmo"].startswith("gzip")}
    for f in filas:
        ref = base[f["prueba"]]
        f["weissman"] = weissman(f["ratio"], f["t_comp_ms"], ref["ratio"], ref["t_comp_ms"])

    # Weissman global (corpus de rendimiento): R = Σorig/Σcomp ; T = mediana del tiempo total
    globales = []
    for herramienta in herramientas():
        nombre = herramienta["nombre"]
        propias = [f for f in filas if f["algoritmo"] == nombre and f["prueba"] in PRUEBAS_DE_RENDIMIENTO]
        r_global = sum(f["original_B"] for f in propias) / sum(f["comprimido_B"] for f in propias)
        totales = [sum(por_repeticion[(nombre, p)][k] for p in PRUEBAS_DE_RENDIMIENTO)
                   for k in range(repeticiones)]
        globales.append({"algoritmo": nombre, "R_global": r_global, "T_global_ms": statistics.median(totales)})
    ref = next(g for g in globales if g["algoritmo"].startswith("gzip"))
    for g in globales:
        g["weissman_global"] = weissman(g["R_global"], g["T_global_ms"], ref["R_global"], ref["T_global_ms"])

    # ---- Guardar resultados ----
    with open(os.path.join(RESULTADOS, "resultados.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        for fila in filas:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in fila.items()})
    with open(os.path.join(RESULTADOS, "weissman_global.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(globales[0].keys()))
        w.writeheader()
        for g in globales:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in g.items()})

    lineas = [f"# Resultados del benchmark ({repeticiones} repeticiones, mediana)\n",
              "| Prueba | Algoritmo | Original (B) | Comprimido (B) | Ratio | Ahorro % | bits/byte | T comp (ms) | T desc (ms) | V comp (MB/s) | V desc (MB/s) | Overhead % | Weissman | SHA |",
              "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for f in sorted(filas, key=lambda x: (x["prueba"], x["algoritmo"])):
        lineas.append(f"| {f['prueba']} | {f['algoritmo']} | {f['original_B']} | {f['comprimido_B']} | "
                      f"{f['ratio']:.3f} | {f['ahorro_%']:.2f} | {f['bits_por_byte']:.3f} | {f['t_comp_ms']:.1f} | "
                      f"{f['t_desc_ms']:.1f} | {f['v_comp_MBs']:.3f} | {f['v_desc_MBs']:.3f} | "
                      f"{f['overhead_%']:.2f} | {f['weissman']:.3f} | {f['integridad']} |")
    lineas += ["", "## Weissman global (Pruebas 2 a 4)\n",
               "| Algoritmo | R global | T global (ms) | Weissman |", "|---|---:|---:|---:|"]
    for g in globales:
        lineas.append(f"| {g['algoritmo']} | {g['R_global']:.3f} | {g['T_global_ms']:.1f} | {g['weissman_global']:.3f} |")
    lineas += ["", "## Entorno\n",
               f"- Sistema: {platform.platform()}",
               f"- Procesador: {platform.processor() or platform.machine()}",
               f"- Python: {platform.python_version()}",
               f"- zip: {version(['zip', '-v'], 1)}",
               f"- gzip: {version(['gzip', '--version'])}"]
    with open(os.path.join(RESULTADOS, "resultados.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")

    print("\n".join(lineas))


if __name__ == "__main__":
    main()
