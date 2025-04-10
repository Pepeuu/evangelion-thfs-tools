import os
import struct
import re

arquivo_thfs = "IMAGE.THFS"
pasta_saida = "gim_extraidos"

os.makedirs(pasta_saida, exist_ok=True)

# Remove caracteres inválidos E não imprimíveis
def limpar_nome(nome):
    nome = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', nome)  # Remove inválidos e de controle
    nome = re.sub(r'[\x7F-\x9F]', '_', nome)  # Remove mais caracteres de controle
    return nome.strip()

def extrair_gims():
    with open(arquivo_thfs, "rb") as f:
        header = f.read(4)
        if header != b"THFS":
            print("[ERRO] Arquivo não é um THFS válido.")
            return

        f.seek(0x04)

        extraidos = 0
        while True:
            entrada = f.read(0x60)
            if len(entrada) < 0x60:
                break

            nome = entrada[0x10:0x30].split(b'\x00')[0].decode(errors='ignore')
            if not nome.endswith(".gim"):
                continue

            nome_limpo = limpar_nome(nome)
            offset = struct.unpack("<I", entrada[0x30:0x34])[0]
            tamanho = struct.unpack("<I", entrada[0x34:0x38])[0]

            f_pos_atual = f.tell()
            f.seek(offset)
            dados = f.read(tamanho)
            f.seek(f_pos_atual)

            caminho_saida = os.path.join(pasta_saida, nome_limpo)
            try:
                with open(caminho_saida, "wb") as saida:
                    saida.write(dados)
                print(f"[OK] Extraído: {nome_limpo} (Offset: {offset:08X}, Tamanho: {tamanho})")
                extraidos += 1
            except OSError as e:
                print(f"[ERRO] Não foi possível salvar {nome_limpo}: {e}")

    print(f"\n✅ Extração finalizada. {extraidos} arquivos .GIM salvos em '{pasta_saida}'")

extrair_gims()
