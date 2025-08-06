# 🧠 Grover Quantum WPA Cracker Edition
Repositorio híbrido de cracking cuántico-tradicional utilizando Grover's Algorithm para acelerar búsquedas de claves WPA2. Alimentado por un diccionario de 14 millones de claves y herramientas de conversión .cap para Hashcat.

🚀 Instalación y entorno
bash
# Clona el repo
git clone https://github.com/TxilorAlvarez/QuantumCrackSim
cd QuantumCrackSim

### 📁 El archivo `mega_diccionario_tolima.txt` es necesario para ejecutar el script.
Debido a su tamaño, puedes descargarlo desde:

🔗 Descarga el diccionario desde [Dropbox](https://www.dropbox.com/scl/fi/f1q8c277h1h7lvgiw1r8q/mega_diccionario_tolima.txt?rlkey=iuafk98vwmltjzg306e5um1tb&st=qtlerzvl&dl=0).

# Crea entorno virtual
bash setup_env.sh | .\setup_env.sh

# (Opcional) Instala utilidades externas:
# - cap2hccapx: https://hashcat.net/cap2hccapx/
# - hcxtools: https://github.com/ZerBea/hcxtools
---

## 🧪 `setup_env.sh` – Virtual Environment Setup

You already have this, but here’s the clean & ready version for Unix/macOS:

```bash
#!/bin/bash

echo "🧪 Setting up Python virtual environment..."

python3 -m venv venv
source venv/bin/activate
deactivate 

echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Virtual environment ready."
1. Eliminar el origin existente:

git remote remove origin
2. Agregar el nuevo origin correcto:

git remote add origin https://github.com/TxilorAlvarez/QuantumCrackSim.git
git branch -M main
git push -u origin main
3. Verifica que está bien configurado:

git remote -v

```

### 🧩 Estructura del proyecto
text
QuantumCrackSim/
├── Quantum/
│   └── GroverSearch.qs              # Quantum algorithm in Q#
├── host/
│   └── host.py                      # Hybrid dispatcher with entropy and cracking logic
├── data/
│   ├── dictionary.txt               # Sample wordlist (useful for testing)
│   └── mega_diccionario_tolima.txt # High-volume dictionary (14M+ entries)
├── config/
│   └── target_config.json           # Hash target + encoding
├── masks/
│   └── mask_config.json             # Hashcat-style mask definitions
├── scripts/
│   ├── process_cap_files.py         # Extracts SSID/BSSID info from .cap
│   ├── cap_to_hashcat.py            # Converts .cap → .hccapx / .22000
│   ├── grover_oracle_builder.py     # Builds Grover oracle from target
│   ├── entropy_analyzer.py          # Entropy stats from dictionary data
│   ├── mask_evaluator.py            # Evaluates mask complexity + pattern entropy
│   └── quantum_launcher.py          # Main Grover executor across masks/dictionary
├── requirements.txt                 # Dependency list for virtual environment
├── setup_env.sh                     # Quick environment setup script
└── README.md                        # Project documentation


### 🛠️ Core Python Modules & Purpose

💻 Script	⚙️ Propósito
process_cap_files.py	Analiza archivos .cap y extrae SSID/BSSID de redes detectadas

cap_to_hashcat.py	Convierte .cap a formatos .hccapx o .22000 compatibles con Hashcat

entropy_analyzer.py	Mide entropía, longitud promedio y distribución de caracteres en el diccionario

mask_evaluator.py	Genera claves de muestra desde cada máscara y calcula su entropía

grover_oracle_builder.py	Crea oráculo cuántico para buscar clave específica basada en su hash

quantum_launcher.py	Lanza Grover iterativo en el backend cuántico usando claves o máscaras

⚛️ Grover on Azure Quantum
To run Grover's Algorithm on real quantum hardware:

👉 Create your Azure Quantum account: azure.microsoft.com/en-us/products/quantum

🛠 Set up your workspace: name, region, and token

📦 Make sure qsharp and azure-quantum are installed in your Python environment

📡 Launch GroverSearch.qs using quantum_launcher.py and send iterations through Azure

### Configurar Visual Studio Code

Extensiones:

Instala:

Python (Microsoft)
Microsoft Quantum Development Kit (para Q#)

Abre el proyecto en VS Code:
cd C:\Users\aleta\OneDrive\Documents\Azure\QuantumCrackSim
code .

### Configura el Intérprete de Python:

Presiona Ctrl+Shift+P, selecciona Python: Select Interpreter, y elige el Python del entorno virtual (.venv\Scripts\python.exe).

### Configura Azure Quantum:

Instala Azure CLI:
winget install Microsoft.AzureCLI
az login

### Crea un workspace:
az quantum workspace create -g <resource-group> -w <workspace-name> -l eastus

Edita config/target_config.json:
json{
  "target": "Pa5$word",
  "encoding": "ascii",
  "azure_quantum": {
    "resource_id": "<your-resource-id>",
    "location": "eastus",
    "provider": "ionq"
  }
}

### Ejecutar el Proyecto

Ejecutar host.py:

En la terminal de VS Code:
python host/host.py --dictionary data/dictionary.txt --mask masks/mask_config.json --target config/target_config.json

# Probar Q#:

Abre Quantum/GroverSearch.qs en VS Code.
Instala .NET SDK:
bash: winget install Microsoft.DotNet.SDK.6

Instala IQ#:
bash: dotnet tool install -g Microsoft.Quantum.IQSharp
dotnet iqsharp install

Ejecuta:
bash: dotnet run --project Quantum

# 🧪 Example Execution
bash
### Run entropy analysis and evaluate masks
python scripts/entropy_analyzer.py
python scripts/mask_evaluator.py

# Launch Grover search based on selected mask or dictionary entry
python scripts/quantum_launcher.py

# Solucionar Problemas

Asegúrate de que scripts/entropy_analyzer.py existe.
Mueve main.py al directorio raíz y actualiza los imports.

Errores de Azure Quantum:

Verifica:
bash: az quantum workspace show

Errores de Q#:

Reinstala IQ#:
bash: dotnet iqsharp install

### Upload to Git-Hub

# 🔧 Pasos para subir tu proyecto a GitHub y clonarlo en tu máquina virtual
1. 📦 Crear el repositorio en GitHub
Ve a github.com y accede con tu cuenta. Haz clic en New Repository. Asigna un nombre como: QuantumCrackSim

Marcar “Initialize with README” si quieres agregar el archivo base.

# ⛓️‍💥 Conectar tu carpeta local con el repo
Desde tu carpeta local (donde está tu proyecto), abre terminal y ejecuta:

    bash
        git init
        git remote add origin https://github.com/TxilorAlvarez/QuantumCrackSim.git
        git add .
        git commit -m "🔮 Initial quantum cracking structure"
        git push -u origin master
        git push -u origin main

### Usar Git Large File Storage (LFS)
GitHub recomienda usar Git LFS para manejar archivos pesados. Aquí tienes los pasos básicos:

# Instala Git LFS si no lo tienes
git lfs install

# Añade el archivo grande a LFS
git lfs track "data/mega_diccionario_tolima.txt"

# Asegúrate de que el cambio esté en el .gitattributes
git add .gitattributes

# Vuelve a agregar y hacer commit
git add data/mega_diccionario_tolima.txt
git commit -m "Add large file to LFS"
git push -u origin main

# 🚀 Para clonar en tu máquina virtual
Desde tu VM (Linux/Windows con Git instalado):
    bash
        git clone https://github.com/TxilorAlvarez/QuantumCrackSim.git
        cd QuantumCrackSim
Y luego puedes iniciar con:
    bash
        bash setup_env.sh
        python main.py

# 📁 Revisa que estén incluidos:
setup_env.sh (y que tenga permisos de ejecución: chmod +x setup_env.sh)

requirements.txt (con todas las dependencias necesarias)

README.md explicando cómo instalar, ejecutar, y qué hace el proyecto

Código fuente (por ejemplo: main.py, simulator.py, etc.)

venv/ no debe estar incluido en el repo (usa .gitignore)

Archivo .gitignore con al menos:

gitignore
venv/
__pycache__/
*.pyc

### 🧠 Author & Credits
Created by txilor_alvarez, the quantum mind from CrackSim ⚡. This project elegantly fuses AI, cybersecurity, and quantum computing into a bold exploration of cracking simulation—where traditional brute force meets futuristic amplitude amplification. Tolima nunca fue tan poderoso. 🚀