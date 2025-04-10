import os
import struct

def extract_thfs(file_path, output_dir):
    with open(file_path, "rb") as f:
        # Cria a pasta de saída se não existir
        os.makedirs(output_dir, exist_ok=True)

        # Lê o número de arquivos (assumindo no começo do arquivo)
        num_files_bytes = f.read(4)
        num_files = struct.unpack("<I", num_files_bytes)[0]

        print(f"Arquivos detectados: {num_files}")

        entries = []

        # Cada entrada possui: nome (32 bytes), offset (4), tamanho (4)
        for _ in range(num_files):
            name_bytes = f.read(32)
            name = name_bytes.decode("ascii", errors="ignore").strip("\x00")
            offset = struct.unpack("<I", f.read(4))[0]
            size = struct.unpack("<I", f.read(4))[0]
            entries.append((name, offset, size))

        for name, offset, size in entries:
            f.seek(offset)
            data = f.read(size)
            out_path = os.path.join(output_dir, name)
            with open(out_path, "wb") as out_file:
                out_file.write(data)
            print(f"Extraído: {name} ({size} bytes)")

if __name__ == "__main__":
    extract_thfs("SCRIPT.THFS", "extraidos")
