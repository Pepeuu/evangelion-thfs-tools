import os
import struct

def ler_string(f, tamanho=64):
    data = f.read(tamanho)
    return data.split(b'\x00', 1)[0].decode("utf-8", errors="ignore")

def criar_pasta(nome):
    if not os.path.exists(nome):
        os.makedirs(nome)

def extrair_thfs(caminho_arquivo, pasta_saida="extraidos"):
    with open(caminho_arquivo, "rb") as f:
        header = f.read(4)
        if header != b'THFS':
            print("Formato inválido. Esse arquivo não é um THFS.")
            return

        num_arquivos = struct.unpack("<I", f.read(4))[0]
        print(f"Arquivos detectados: {num_arquivos}")

        criar_pasta(pasta_saida)
        criar_pasta(os.path.join(pasta_saida, "textos"))
        criar_pasta(os.path.join(pasta_saida, "binarios"))
        criar_pasta(os.path.join(pasta_saida, "placeholders"))

        entradas = []

        for i in range(num_arquivos):
            nome = ler_string(f)
            offset = struct.unpack("<I", f.read(4))[0]
            tamanho = struct.unpack("<I", f.read(4))[0]
            flag = struct.unpack("<I", f.read(4))[0]
            checksum = f.read(8)
            entradas.append((nome, offset, tamanho, flag, checksum))

        for i, (nome, offset, tamanho, flag, checksum) in enumerate(entradas):
            f.seek(offset)
            conteudo = f.read(tamanho)

            # Decide o tipo de saída
            if tamanho == 0:
                pasta_destino = "placeholders"
            elif nome.endswith(".txt"):
                pasta_destino = "textos"
            else:
                pasta_destino = "binarios"

            caminho_destino = os.path.join(pasta_saida, pasta_destino, nome)

            with open(caminho_destino, "wb") as saida:
                saida.write(conteudo)

            print(f"[{i+1}/{num_arquivos}] Extraído: {nome} → {pasta_destino}")

if __name__ == "__main__":
    extrair_thfs("SCRIPT.THFS")
