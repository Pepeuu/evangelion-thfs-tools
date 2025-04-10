import os
import struct

def extrair_thfs(arquivo):
    with open(arquivo, "rb") as f:
        # Lê o cabeçalho (deve começar com "THFS")
        magic = f.read(4)
        if magic != b'THFS':
            print("❌ Arquivo inválido: cabeçalho THFS não encontrado.")
            return

        # Número de entradas (arquivos dentro do THFS)
        qtd_total = struct.unpack("<I", f.read(4))[0]

        if qtd_total > 10000:
            print(f"⚠️ Muito alto: {qtd_total} arquivos? Pode estar corrompido.")
            continuar = input("Deseja continuar assim mesmo? (s/n): ")
            if continuar.lower() != "s":
                return

        print(f"Arquivos detectados: {qtd_total}")
        entradas = []

        for i in range(qtd_total):
            try:
                offset = struct.unpack("<I", f.read(4))[0]
                tamanho = struct.unpack("<I", f.read(4))[0]
                nome_bytes = f.read(32)
                nome = nome_bytes.decode('utf-8', errors='replace').strip('\x00').strip()

                # Corrige nomes inválidos
                if not nome:
                    nome = f"arquivo_{i}"
                else:
                    nome = "".join(c if c.isalnum() or c in "._- " else "_" for c in nome)
                    if nome in ("", ".", ".."):
                        nome = f"arquivo_{i}"

                entradas.append((offset, tamanho, nome))

            except Exception as e:
                print(f"Fim do arquivo atingido prematuramente ao ler entrada {i}")
                break

        print(f"→ Total de entradas lidas com sucesso: {len(entradas)}")

        pasta_saida = "extraidos"
        os.makedirs(pasta_saida, exist_ok=True)

        for i, (offset, tamanho, nome) in enumerate(entradas):
            try:
                f.seek(offset)
                conteudo = f.read(tamanho)

                # Determina o tipo do arquivo (extensão ou conteúdo)
                if tamanho == 0:
                    pasta_destino = "placeholders"
                elif nome.lower().endswith(".txt"):
                    pasta_destino = "txt"
                elif nome.lower().endswith(".bin"):
                    pasta_destino = "binarios"
                else:
                    pasta_destino = "outros"

                caminho_destino = os.path.join(pasta_saida, pasta_destino, nome)
                os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)

                with open(caminho_destino, "wb") as saida:
                    saida.write(conteudo)

                print(f"[{i+1}/{len(entradas)}] Extraído: {nome} → {pasta_destino}")

            except Exception as e:
                print(f"Erro ao extrair '{nome}': {e}")

# Executa a função
extrair_thfs("SCRIPT.THFS")
