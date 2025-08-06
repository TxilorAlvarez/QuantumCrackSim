import math
import pandas as pd
from collections import Counter
from tqdm import tqdm
from rich.console import Console
from rich.table import Table

console = Console()

def calcular_entropia(texto):
    contador = Counter(texto)
    total = sum(contador.values())
    entropia = -sum((f / total) * math.log2(f / total) for f in contador.values())
    return entropia

def analizar_diccionario(ruta_diccionario):
    with open(ruta_diccionario, 'r', encoding='utf-8', errors='ignore') as f:
        claves = [line.strip() for line in f if line.strip()]

    longitudes = [len(c) for c in claves]
    todas_concatenadas = ''.join(claves)
    entropia_global = calcular_entropia(todas_concatenadas)
    frecuencia_total = Counter(todas_concatenadas)

    resumen = {
        "Claves totales": len(claves),
        "Longitud promedio": sum(longitudes) / len(longitudes),
        "Entropía de Shannon": round(entropia_global, 4),
        "Caracteres únicos": len(frecuencia_total)
    }
    return resumen, frecuencia_total

def mostrar_resumen(resumen):
    table = Table(title="🔬 Análisis de Entropía del Diccionario")
    for k, v in resumen.items():
        table.add_row(k, str(v))
    console.print(table)

def mostrar_top_caracteres(freq_counter, top_n=10):
    table = Table(title=f"🔡 Caracteres Más Frecuentes (top {top_n})")
    table.add_column("Caracter", style="cyan")
    table.add_column("Frecuencia", style="magenta")
    for char, freq in freq_counter.most_common(top_n):
        table.add_row(repr(char), str(freq))
    console.print(table)

if __name__ == "__main__":
    ruta = input("📘 Ruta al mega diccionario: ")
    resumen, frecuencia = analizar_diccionario(ruta)
    mostrar_resumen(resumen)
    mostrar_top_caracteres(frecuencia)
