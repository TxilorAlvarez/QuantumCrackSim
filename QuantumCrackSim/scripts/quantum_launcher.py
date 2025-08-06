import qsharp
from Quantum.Oracles import CheckPassword
import hashlib
import random
import json

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def cargar_diccionario(path, limite=10000):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f][:limite]

def cargar_mascaras(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data['masks'], data['charset_map']

def generar_desde_mascara(mask, charset_map):
    resultado = ''
    for c in mask.split('?')[1:]:
        c = '?' + c
        chars = charset_map.get(c, '')
        resultado += random.choice(chars) if chars else ''
    return resultado

def lanzar_grover(hash_objetivo):
    resultado = CheckPassword.simulate(InputHash=hash_objetivo)
    return resultado

def ejecutar_busqueda(modo="mascara", mascara=None, charset_map=None, diccionario=None):
    if modo == "mascara" and mascara and charset_map:
        candidato = generar_desde_mascara(mascara, charset_map)
    elif modo == "diccionario" and diccionario:
        candidato = random.choice(diccionario)
    else:
        print("❌ Modo inválido")
        return

    hash_candidato = hash_password(candidato)
    resultado = lanzar_grover(hash_candidato)

    print(f"🔍 Probando clave: {candidato}")
    print(f"⚛️ Resultado Grover: {resultado}")

if __name__ == "__main__":
    diccionario = cargar_diccionario("mega_diccionario_tolima.txt", limite=10000)
    masks, charset_map = cargar_mascaras("mask/mask.json")

    for mask in masks:
        print(f"\n🎯 Ejecutando Grover con máscara: {mask}")
        ejecutar_busqueda(modo="mascara", mascara=mask, charset_map=charset_map)
