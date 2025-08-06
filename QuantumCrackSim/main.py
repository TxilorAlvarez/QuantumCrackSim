# 📦 System modules
import os
import time
import json

# 🧪 QuantumCrackSim modules
from scripts.entropy_analyzer import analizar_diccionario, mostrar_resumen
from scripts.mask_evaluator import cargar_mascaras, evaluar_mascaras
from scripts.quantum_launcher import ejecutar_busqueda

# 🎨 Rich interface modules
from rich.console import Console
from rich.prompt import Prompt

# 🗂️ Load config (.cap path)
def cargar_config():
    with open("config/run_config.json", "r") as f:
        return json.load(f)

config = cargar_config()
cap_path = config["cap_path"]

# 📂 Console and core paths
console = Console()
DICT_PATH = "data/mega_diccionario_tolima.txt"
MASK_PATH = "masks/mask_config.json"

# 📥 Manual prompt for .cap file
def solicitar_archivo_cap():
    cap_path = Prompt.ask("📂 Ruta del archivo .cap")
    if not os.path.isfile(cap_path):
        console.print(f"[red]Archivo no encontrado:[/red] {cap_path}")
        return None
    console.print(f"[green]✅ Archivo cargado:[/green] {cap_path}")
    return cap_path

cap_file = solicitar_archivo_cap()

# 🎛️ Banner
def banner():
    console.rule("[bold cyan]🧠 QuantumCrackSim Tolima Edition")
    console.print("🚀 Hybrid quantum cracking launcher")
    console.print("🔍 Dictionary:", DICT_PATH)
    console.print("🎭 Masks:", MASK_PATH)
    console.print("💿 CAP:", cap_file or cap_path)
    console.print("⚛️ Mode: Entropy → Mask → Grover\n")

# 🧮 Entropy Analysis
def run_entropy():
    console.print("\n[bold green]🔎 Entropy Analysis[/bold green]")
    resumen, freq = analizar_diccionario(DICT_PATH)
    mostrar_resumen(resumen)
    return resumen

# 🎭 Mask Evaluation
def run_masks():
    console.print("\n[bold yellow]🎭 Mask Evaluation[/bold yellow]")
    masks, charset_map, descriptions = cargar_mascaras(MASK_PATH)
    evaluar_mascaras(masks, charset_map, descriptions)
    return masks, charset_map

# ⚛️ Grover Quantum Execution
def run_grover(masks, charset_map):
    console.print("\n⚛️ [bold magenta]Grover Execution Loop[/bold magenta]")
    for mask in masks[:3]:  # Top 3 masks for demo
        console.print(f"\n[blue]🔬 Mask:[/blue] {mask}")
        ejecutar_busqueda(modo="mascara", mascara=mask, charset_map=charset_map)

# 🧬 Launcher main function
def main():
    banner()
    mode = Prompt.ask("🎛️ Select mode", choices=["full", "entropy", "mask", "grover"], default="full")

    if mode == "entropy":
        run_entropy()
    elif mode == "mask":
        run_masks()
    elif mode == "grover":
        masks, charset_map, _ = cargar_mascaras(MASK_PATH)
        run_grover(masks, charset_map)
    elif mode == "full":
        resumen = run_entropy()
        masks, charset_map = run_masks()
        time.sleep(1)
        run_grover(masks, charset_map)

if __name__ == "__main__":
    main()
