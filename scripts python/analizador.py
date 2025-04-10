import os
import re

# Função para detectar se uma sequência pode ser texto em Shift-JIS
def is_shift_jis_char(b):
    return (0x81 <= b <= 0x9F) or (0xE0 <= b <= 0xEF)

def procurar_shift_jis(dados, min_tamanho=4):
    resultados = []
    i = 0
    while i < len(dados) - 1:
        if is_shift_jis_char(dados[i]):
            inicio = i
            while i + 1 < len(dados) and is_shift_jis_char(dados[i]):
                i += 2  # Avança dois bytes por caractere
            if i - inicio >= min_tamanho * 2:
                trecho = dados[inicio:i].decode("shift_jis", errors="ignore")
                resultados.append((inicio, trecho))
        else:
            i += 1
    return resultados

# Função para buscar nomes de arquivos e extensões
def procurar_nomes_arquivos(dados):
    padrao = rb'[\w\.\-]{3,}\.(thfs|gim|bin|txt|dat|raw|png|jpg)'
    return [(m.start(), m.group().decode("ascii", errors="ignore")) for m in re.finditer(padrao, dados)]

# Carrega e analisa o dump
def analisar_dump(arquivo_dump):
    with open(arquivo_dump, "rb") as f:
        dados = f.read()

    print("[*] Analisando arquivo de dump...\n")

    print("🔍 Procurando nomes de arquivos relevantes...")
    arquivos_encontrados = procurar_nomes_arquivos(dados)
    for offset, nome in arquivos_encontrados:
        print(f"  [Arquivo] {nome} encontrado no offset {hex(offset)}")

    print("\n🔍 Procurando textos em Shift-JIS (parciais)...")
    textos = procurar_shift_jis(dados)
    for offset, trecho in textos[:20]:  # mostra só os 20 primeiros
        print(f"  [Texto] Offset {hex(offset)}: {trecho}")

    print("\n✅ Análise concluída. Use esses dados como base para entender como o jogo interpreta os arquivos.")

# Caminho do seu arquivo de dump
analisar_dump("RAM.dump")
