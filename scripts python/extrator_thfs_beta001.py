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

        # Se o número for suspeito, perguntar ao usuário
        if num_arquivos > 10000:
            print(f"⚠️ Muito alto: {num_arquivos} arquivos? Pode estar corrompido.")
            continuar = input("Deseja continuar assim mesmo? (s/n): ")
            if continuar.lower() != 's':
                return

        print(f"Arquivos detectados: {num_arquivos}")

        criar_pasta(pasta_saida)
        criar_pasta(os.path.join(pasta_saida, "textos"))
        criar_pasta(os.path.join(pasta_saida, "binarios"))
        criar_pasta(os.path.join(pasta_saida, "placeholders"))

        entradas = []

        for i in range(num_arquivos):
            try:
                nome = ler_string(f)
                dados = f.read(12)
                if len(dados) < 12:
                    print(f"Fim do arquivo atingido prematuramente ao ler entrada {i}")
                    break
                offset, tamanho, flag = struct.unpack("<III", dados)
                checksum = f.read(8)
                entradas.append((nome, offset, tamanho, flag, checksum))
            except Exception as e:
                print(f"Erro ao ler entrada {i}: {e}")
                break

        print(f"→ Total de entradas lidas com sucesso: {len(entradas)}")

        for i, (nome, offset, tamanho, flag, checksum) in enumerate(entradas):
            f.seek(offset)
            conteudo = f.read(tamanho)

            if tamanho == 0:
                pasta_destino = "placeholders"
            elif nome.endswith(".txt"):
                pasta_destino = "textos"
            else:
                pasta_destino = "binarios"

            caminho_destino = os.path.join(pasta_saida, pasta_destino, nome)

            with open(caminho_destino, "wb") as saida:
                saida.write(conteudo)

            if i % 100 == 0:
                print(f"[{i+1}/{len(entradas)}] Extraído: {nome} → {pasta_destino}")

if __name__ == "__main__":
    extrair_thfs("SCRIPT.THFS")
