import os
import subprocess
from tqdm import tqdm

def convertir_cap_a_hccapx(archivo_cap, carpeta_salida):
    nombre_base = os.path.splitext(os.path.basename(archivo_cap))[0]
    archivo_hccapx = os.path.join(carpeta_salida, f"{nombre_base}.hccapx")
    comando = ["cap2hccapx", archivo_cap, archivo_hccapx]
    try:
        subprocess.run(comando, check=True)
        return archivo_hccapx
    except subprocess.CalledProcessError:
        return None

def convertir_todos_en_carpeta(carpeta_cap, carpeta_salida):
    os.makedirs(carpeta_salida, exist_ok=True)
    archivos = [f for f in os.listdir(carpeta_cap) if f.endswith(".cap")]
    resultados = []

    for archivo in tqdm(archivos, desc="🔁 Convirtiendo a .hccapx"):
        ruta = os.path.join(carpeta_cap, archivo)
        resultado = convertir_cap_a_hccapx(ruta, carpeta_salida)
        if resultado:
            resultados.append(resultado)
    return resultados

if __name__ == "__main__":
    carpeta_entrada = input("📁 Carpeta con archivos .cap: ")
    carpeta_salida = input("📤 Carpeta de salida (.hccapx): ")
    archivos_convertidos = convertir_todos_en_carpeta(carpeta_entrada, carpeta_salida)
    print(f"✅ {len(archivos_convertidos)} archivos convertidos exitosamente.")
