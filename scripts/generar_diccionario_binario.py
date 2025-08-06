import json

def string_to_binary(s):
    return ''.join(format(ord(c), '08b') for c in s)

def save_encoded_with_index_streamed(path, encoding="binary", output_prefix="mega_diccionario_tolima", block_size=100000):
    encoded_path = f"{output_prefix}_binary.json"
    index_path = f"{output_prefix}_index.json"
    index = {}

    with open(path, "r", encoding="utf-8", errors="ignore") as f_in, \
         open(encoded_path, "w") as f_bin, \
         open(index_path, "w") as f_idx:

        f_bin.write("{\n")
        f_idx.write("{\n")

        for i, line in enumerate(f_in):
            word = line.strip()
            if not word:
                continue

            encoded = string_to_binary(word) if encoding == "binary" else word
            entry = f'"{i}": "{encoded}"'
            idx_entry = f'"{i}": "{word}"'

            if i > 0:
                f_bin.write(",\n")
                f_idx.write(",\n")

            f_bin.write(entry)
            f_idx.write(idx_entry)
            index[i] = word

            if (i + 1) % block_size == 0:
                print(f"[INFO] Procesadas {i + 1} contraseñas...")

        f_bin.write("\n}")
        f_idx.write("\n}")

    print(f"\n✅ Diccionario codificado guardado como: {encoded_path}")
    print(f"📑 Índice de palabras original guardado como: {index_path}")

if __name__ == "__main__":
    ruta_archivo = "mega_diccionario_tolima.txt"  # Asegúrate de que esté en la misma carpeta
    save_encoded_with_index_streamed('mega_diccionario_tolima.txt')
