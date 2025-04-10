import os
import struct

def is_probably_text(data):
    try:
        data.decode('utf-8')
        return True
    except:
        return False

def extract_thfs(file_path, output_folder):
    with open(file_path, 'rb') as f:
        magic = f.read(4)
        if magic != b'THFS':
            print("Formato inválido!")
            return
        
        os.makedirs(output_folder, exist_ok=True)

        entry_count = 0
        while True:
            entry_start = f.tell()
            header = f.read(0x80)
            if len(header) < 0x80:
                break

            filename = header[24:56].split(b'\x00')[0].decode(errors='ignore')
            offset = struct.unpack('<I', header[0x40:0x44])[0]
            size = struct.unpack('<I', header[0x44:0x48])[0]

            if not filename:
                continue

            current_pos = f.tell()
            f.seek(offset)
            data = f.read(size)
            f.seek(current_pos)

            # Verifica se é texto e converte
            if is_probably_text(data):
                out_path = os.path.join(output_folder, filename)
                with open(out_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(data.decode('utf-8', errors='ignore'))
            else:
                out_path = os.path.join(output_folder, filename)
                with open(out_path, 'wb') as out_f:
                    out_f.write(data)

            print(f"[{entry_count}] Extraído: {filename} ({size} bytes)")
            entry_count += 1

    print("\nExtração concluída!")

# Executar
extract_thfs("SCRIPT.THFS", "arquivos_extraidos")
