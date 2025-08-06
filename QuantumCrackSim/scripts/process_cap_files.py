import os
import scapy.all as scapy
from tqdm import tqdm
from rich.console import Console
from rich.table import Table

console = Console()

def list_cap_files(folder_path):
    return [f for f in os.listdir(folder_path) if f.endswith('.cap')]

def extract_handshake_info(file_path):
    packets = scapy.rdpcap(file_path)
    ssid = set()
    bssid = set()
    for pkt in packets:
        if pkt.haslayer(scapy.Dot11):
            if pkt.type == 0 and pkt.subtype == 8:  # Beacon frame
                ssid.add(pkt.info.decode('utf-8', 'ignore'))
                bssid.add(pkt.addr2)
    return {'file': os.path.basename(file_path), 'ssids': list(ssid), 'bssids': list(bssid)}

def scan_folder(folder_path):
    cap_files = list_cap_files(folder_path)
    data = []
    for cap_file in tqdm(cap_files, desc="🔍 Analizando archivos .cap"):
        path = os.path.join(folder_path, cap_file)
        info = extract_handshake_info(path)
        data.append(info)
    return data

def show_summary(data):
    table = Table(title="📡 Resumen de Capturas")
    table.add_column("Archivo", style="cyan")
    table.add_column("SSIDs", style="green")
    table.add_column("BSSIDs", style="magenta")
    for entry in data:
        table.add_row(entry['file'], ", ".join(entry['ssids']), ", ".join(entry['bssids']))
    console.print(table)

if __name__ == "__main__":
    folder = input("📁 Ruta a carpeta con archivos .cap: ")
    results = scan_folder(folder)
    show_summary(results)
