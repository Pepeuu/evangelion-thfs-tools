# Extrator THFS – Versão Revisada com Análise e Entrada Dinâmica
import os
import struct
import json

class THFSExtractor:
    def __init__(self, caminho_arquivo, pasta_saida="extraidos", modo_simulacao=False):
        self.caminho_arquivo = caminho_arquivo
        self.pasta_saida = pasta_saida
        self.arquivos = []
        self.logs = []
        self.modo_simulacao = modo_simulacao

        if not self.modo_simulacao:
            os.makedirs(self.pasta_saida, exist_ok=True)

    def ler_uint32(self, f):
        dados = f.read(4)
        if len(dados) < 4:
            raise ValueError("[ERRO] Dados insuficientes para leitura de uint32.")
        return struct.unpack("<I", dados)[0]

    def ler_header(self, f):
        magic = f.read(4)
        if magic != b'THFS':
            raise ValueError("[ERRO] Arquivo não possui cabeçalho THFS válido!")

        total_entradas = self.ler_uint32(f)
        self.logs.append(f"[INFO] Total de entradas esperadas: {total_entradas}")
        return total_entradas

    def ler_entrada(self, f):
        offset = self.ler_uint32(f)
        tamanho = self.ler_uint32(f)
        id_bytes = f.read(8)
        nome = f.read(32).split(b"\x00")[0].decode('ascii', 'ignore')
        return {
            "offset": offset,
            "tamanho": tamanho,
            "nome": nome,
            "id": id_bytes.hex()
        }

    def extrair(self):
        if not os.path.isfile(self.caminho_arquivo):
            print(f"[ERRO] Arquivo '{self.caminho_arquivo}' não encontrado.")
            return

        with open(self.caminho_arquivo, "rb") as f:
            tamanho_total = os.path.getsize(self.caminho_arquivo)
            try:
                total_entradas = self.ler_header(f)
            except Exception as e:
                print(f"[ERRO] Falha ao ler cabeçalho: {e}")
                return

            entradas_processadas = []

            for i in range(total_entradas):
                try:
                    entrada = self.ler_entrada(f)

                    if entrada['offset'] == 0 or entrada['tamanho'] == 0:
                        self.logs.append(f"[AVISO] Entrada {i} ignorada (offset/tamanho inválido): {entrada['nome']}")
                        continue

                    if entrada['offset'] + entrada['tamanho'] > tamanho_total:
                        self.logs.append(f"[AVISO] Entrada {i} fora dos limites do arquivo: {entrada['nome']}")
                        continue

                    sobrepoe = False
                    for anterior in entradas_processadas:
                        if not (entrada['offset'] + entrada['tamanho'] <= anterior['offset'] or entrada['offset'] >= anterior['offset'] + anterior['tamanho']):
                            sobrepoe = True
                            break
                    if sobrepoe:
                        self.logs.append(f"[AVISO] Entrada {i} sobrepõe outra entrada: {entrada['nome']}")
                        continue

                    entradas_processadas.append(entrada)
                    nome_seguro = entrada['nome'].strip()
                    if not nome_seguro or any(c in nome_seguro for c in "\\/:*?\"<>|"):
                        nome_seguro = f"arquivo_{i}.bin"
                        self.logs.append(f"[AVISO] Nome inválido ajustado para: {nome_seguro}")

                    f.seek(entrada['offset'])
                    dados = f.read(entrada['tamanho'])

                    if not self.modo_simulacao:
                        caminho_saida = os.path.join(self.pasta_saida, nome_seguro)
                        with open(caminho_saida, "wb") as out:
                            out.write(dados)

                    entrada['nome_seguro'] = nome_seguro
                    self.arquivos.append(entrada)
                    self.logs.append(f"[OK] {('Simulado' if self.modo_simulacao else 'Extraído')}: {nome_seguro} ({entrada['tamanho']} bytes)")
                except Exception as e:
                    self.logs.append(f"[ERRO] Entrada {i}: {e}")

        self.logs.append(f"[INFO] Total de entradas processadas: {len(self.arquivos)}")

    def salvar_log(self, caminho_log="log_extracao.txt"):
        try:
            with open(caminho_log, "w", encoding="utf-8") as f:
                f.write("\n".join(self.logs))
        except Exception as e:
            print(f"[ERRO] Falha ao salvar log: {e}")

    def salvar_metadados_json(self, caminho_json="entradas_thfs.json"):
        try:
            with open(caminho_json, "w", encoding="utf-8") as f:
                json.dump(self.arquivos, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[ERRO] Falha ao salvar metadados JSON: {e}")

if __name__ == '__main__':
    print("\n=== EXTRATOR DE ARQUIVOS .THFS ===\n")
    caminho = input("Digite o nome do arquivo .THFS (ex: SCRIPT.THFS): ").strip()
    modo = input("Deseja rodar em modo simulação? (s/n): ").strip().lower() == 's'

    extrator = THFSExtractor(caminho, modo_simulacao=modo)
    extrator.extrair()
    extrator.salvar_log()
    extrator.salvar_metadados_json()

    print("\n[✔] Processo finalizado.")
    print("\nÚltimas mensagens do log:")
    print("\n".join(extrator.logs[-10:]))
