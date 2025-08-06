import qsharp
from Quantum.Oracles import CheckPassword  # Tu archivo Q# personalizado
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def seleccionar_clave_objetivo(diccionario_path, index=42):
    with open(diccionario_path, 'r') as f:
        lineas = f.readlines()
    clave_objetivo = lineas[index].strip()
    hash_objetivo = hash_password(clave_objetivo)
    return clave_objetivo, hash_objetivo

def construir_oraculo(hash_objetivo):
    resultado = CheckPassword.simulate(InputHash=hash_objetivo)
    return resultado

if __name__ == "__main__":
    diccionario = "mega_diccionario_tolima.txt"
    clave, hash_clave = seleccionar_clave_objetivo(diccionario, index=1420)
    print(f"🔑 Clave objetivo: {clave}")
    print("⚛️ Ejecutando Grover en simulador...")
    resultado = construir_oraculo(hash_clave)
    print(f"✅ Resultado Grover: {resultado}")
