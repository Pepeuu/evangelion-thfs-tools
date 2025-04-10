import struct
import os
import re

def ler_str(f, tamanho):
    dados = f.read(tamanho)
    return dados.split(b'\x00')[0].decode('utf-8', errors='replace')

with open("SCRIPT.THFS", "rb") as f:
    magic = f.read(4)
    if magic != b'THFS':
        raise ValueError("Não é um arquivo THFS válido")

    f.read(4)  # Desconhecido
    num_entradas = struct.unpack("<I", f.read(4))[0]
    f.read(44)  # Ignora dados irrelevantes do cabeçalho

    entradas = []
    for _ in range(num_entradas):
        name_bytes = f.read(32)
        name = name_bytes.split(b'\x00')[0].decode("utf-8", errors="replace")
        name = re.sub(r'[\\/:*?"<>|\x00-\x1F]', '_', name).strip()

        if not name:
            name = f"arquivo_{len(entradas):03}.bin"

        f.read(16)  # Ignora hash ou algo assim
        offset = struct.unpack("<I", f.read(4))[0]
        size = struct.unpack("<I", f.read(4))[0]
        f.read(4)  # ignorado
        entradas.append((name, offset, size))

    os.makedirs("extraidos", exist_ok=True)

    for nome, offset, tamanho in entradas:
        f.seek(offset)
        dados = f.read(tamanho)
        caminho = os.path.join("extraidos", nome)

        with open(caminho, "wb") as out:
            out.write(dados)

        print(f"Extraído: {nome} ({tamanho} bytes)")
