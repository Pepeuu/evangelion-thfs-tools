import os
import re

# CONFIGURAÇÃO
thfs_path = "IMAGE.THFS"  # ou SCRIPT.THFS
base_txt = "base de dados .txt"
pasta_saida = "extraidos"
os.makedirs(pasta_saida, exist_ok=True)

# Função para identificar hexadecimal
def eh_offset(possivel_hex):
    try:
        if possivel_hex.lower().startswith("0x"):
            int(possivel_hex, 16)
            return True
    except:
        pass
    return False

# Processar linhas
with open(base_txt, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

with open(thfs_path, "rb") as f:
    for linha in linhas:
        partes = linha.strip().split()

        # Procurar offset e nome do arquivo na linha
        offset = None
        nome = None
        for parte in partes:
            if eh_offset(parte):
                offset = int(parte, 16)
            elif re.match(r".+\.(gim|txt|bin|dat)", parte, re.IGNORECASE):
                nome = parte

        if offset is not None and nome is not None:
            try:
                f.seek(offset)
                dados = f.read(2 * 1024 * 1024)  # até 2MB

                fim = dados.find(b'\x00\x00\x00\x00')
                if fim != -1:
                    dados = dados[:fim]

                caminho = os.path.join(pasta_saida, nome)
                with open(caminho, "wb") as saida:
                    saida.write(dados)

                print(f"[OK] Extraído: {nome} (Offset: {hex(offset)})")
            except Exception as e:
                print(f"[ERRO] {nome}: {e}")
