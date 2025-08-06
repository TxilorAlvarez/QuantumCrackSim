import json
import random
import math
from collections import Counter
from rich.console import Console
from rich.table import Table

console = Console()

def cargar_mascaras(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['masks'], data['charset_map'], data.get('mask_descriptions', {})

def generar_muestra(mask, charset_map, muestras=1000):
    conjunto = []
    for _ in range(muestras):
        cadena = ''
        for simbolo in mask.split('?')[1:]:
            simbolo = '?' + simbolo
            chars = charset_map.get(simbolo, '')
            cadena += random.choice(chars) if chars else ''
        conjunto.append(cadena)
    return conjunto

def calcular_entropia(cadenas):
    texto = ''.join(cadenas)
    contador = Counter(texto)
    total = sum(contador.values())
    entropia = -sum((f / total) * math.log2(f / total) for f in contador.values())
    return round(entropia, 4)

def evaluar_mascaras(masks, charset_map, descriptions):
    tabla = Table(title="🔐 Evaluación de Máscaras")
    tabla.add_column("Máscara", style="cyan")
    tabla.add_column("Descripción", style="green")
    tabla.add_column("Entropía", style="magenta")
    tabla.add_column("Longitud", style="yellow")

    for mask in masks:
        muestra = generar_muestra(mask, charset_map)
        entropia = calcular_entropia(muestra)
        longitud = len(muestra[0]) if muestra else 0
        tabla.add_row(mask, descriptions.get(mask, "—"), str(entropia), str(longitud))

    console.print(tabla)

if __name__ == "__main__":
    archivo_mask = input("📁 Ruta al archivo de máscaras (mask.json): ")
    masks, charset_map, descriptions = cargar_mascaras(archivo_mask)
    evaluar_mascaras(masks, charset_map, descriptions)
