import argparse
import json
import subprocess
import os
import qsharp
from qsharp.azure import connect, target, execute
import GroverSearch  # Q# operation


# -------------------------------
# 📂 LOADERS
# -------------------------------

def load_dictionary(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def load_mask(path):
    with open(path, "r") as f:
        return json.load(f)

def load_target(path):
    with open(path, "r") as f:
        return json.load(f)


# -------------------------------
# 🔤 ENCODING / DECODING
# -------------------------------

def encode_ascii(word):
    return [ord(c) for c in word]

def encode_binary(word):
    return [int(b) for c in word for b in format(ord(c), "08b")]

def decode_binary(bits):
    try:
        chars = [chr(int("".join(map(str, bits[i:i+8])), 2)) for i in range(0, len(bits), 8)]
        return "".join(chars)
    except Exception:
        return "[Invalid Binary Sequence]"

def decode_ascii(bits):
    try:
        return "".join([chr(b) for b in bits])
    except Exception:
        return "[Invalid ASCII Sequence]"

def save_encoded_with_index(dictionary, mode="ascii", output="encoded.json", index_map_out="index_map.json"):
    encoded = []
    index_map = {}
    for i, word in enumerate(dictionary):
        if mode == "ascii":
            enc = encode_ascii(word)
        elif mode == "binary":
            enc = encode_binary(word)
        encoded.append(enc)
        index_map[i] = word
    with open(output, "w") as f:
        json.dump(encoded, f, indent=2)
    with open(index_map_out, "w") as f:
        json.dump(index_map, f, indent=2)

def batch_encode_dictionaries(folder_path, mode="binary"):
    for fname in os.listdir(folder_path):
        if fname.endswith(".txt"):
            full_path = os.path.join(folder_path, fname)
            print(f"📄 Procesando: {fname}")
            dictionary = load_dictionary(full_path)
            base_name = os.path.splitext(fname)[0]
            save_encoded_with_index(
                dictionary,
                mode=mode,
                output=f"{folder_path}/{base_name}_{mode}.json",
                index_map_out=f"{folder_path}/{base_name}_index.json"
            )


# -------------------------------
# 🔧 HASHCAT EXECUTION
# -------------------------------

def run_hashcat(target, mask):
    hash_file = "target.hash"
    hash_type = "0"  # MD5 (modifiable)

    with open(hash_file, "w") as hf:
        hf.write(target)

    mask_string = mask["masks"][0]

    subprocess.run([
        "hashcat", "-a", "3", "-m", hash_type,
        hash_file, mask_string,
        f"--custom-charset1={mask['charset_map']['?u']}",
        f"--custom-charset2={mask['charset_map']['?l']}",
        f"--custom-charset3={mask['charset_map']['?d']}",
        f"--custom-charset4={mask['charset_map']['?s']}"
    ])


# -------------------------------
# ⚛️ AZURE QUANTUM GROVER
# -------------------------------

def run_simulation(dictionary, mask, target, encoding):
    if encoding == "binary":
        target_bits = encode_binary(target)
    else:
        target_bits = encode_ascii(target)

    print(f"🔍 Grover Searching for: {target} as {target_bits}")

    result_int = GroverSearch.SearchPassword(match=target_bits, iterations=0)
    print(f"🧠 Quantum Output (int): {result_int}")

    result_bits = [int(b) for b in bin(result_int)[2:].zfill(len(target_bits))]

    if encoding == "binary":
        candidate = decode_binary(result_bits)
    else:
        candidate = decode_ascii(result_bits)

    match = candidate in dictionary

    print(f"🎯 Candidate Decoded: {candidate}")
    print(f"✅ Dictionary Match Found: {match}")

    result_log = {
        "crack_method": "quantum",
        "target": target,
        "decoded_candidate": candidate,
        "match_found": match,
        "entropy": estimate_entropy(mask, dictionary),
        "engine": "Azure Quantum Grover Search"
    }

    with open("results.json", "w") as f:
        json.dump(result_log, f, indent=2)


# -------------------------------
# 🔀 DISPATCHER
# -------------------------------

def estimate_entropy(mask, dictionary):
    base_size = len(dictionary)
    mask_factor = sum(len(mask["charset_map"].get(token, "")) for token in mask["masks"][0])
    return base_size * mask_factor

def hybrid_dispatch(dictionary, mask, target_cfg):
    target = target_cfg["target"]
    encoding = target_cfg.get("encoding", "ascii")

    entropy = estimate_entropy(mask, dictionary)
    print(f"📊 Estimated Entropy: {entropy}")

    threshold = 1_000_000
    if entropy < threshold:
        print("🧠 Strategy: GPU Brute Force via Hashcat")
        run_hashcat(target, mask)
    else:
        print("⚛️ Strategy: Azure Quantum Grover Simulation")
        run_simulation(dictionary, mask, target, encoding)


# -------------------------------
# 🚀 MAIN EXECUTION
# -------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hybrid Cracking Dispatcher")
    parser.add_argument("--dictionary", required=True, help="Path to dictionary file")
    parser.add_argument("--mask", required=True, help="Path to mask config")
    parser.add_argument("--target", required=True, help="Path to target config")
    parser.add_argument("--encode-only", action="store_true", help="Only encode dictionary and exit")
    parser.add_argument("--mode", choices=["ascii", "binary"], default="binary", help="Encoding mode")
    parser.add_argument("--batch", action="store_true", help="Batch process all dictionaries in folder")
    args = parser.parse_args()

    if args.batch:
        batch_encode_dictionaries(args.dictionary, mode=args.mode)
    elif args.encode_only:
        dictionary = load_dictionary(args.dictionary)
        save_encoded_with_index(dictionary, mode=args.mode)
    else:
        dictionary = load_dictionary(args.dictionary)
        mask = load_mask(args.mask)
        target_cfg = load_target(args.target)
        hybrid_dispatch(dictionary, mask, target_cfg)
