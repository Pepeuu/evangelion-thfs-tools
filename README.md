🛠 evangelion-thfs-tools
Ferramentas de extração e análise de arquivos .THFS do jogo Neon Genesis Evangelion: Girlfriend of Steel Portable (PSP).

Este projeto visa criar scripts em Python para realizar engenharia reversa, extração e tratamento de arquivos contidos nos pacotes .THFS, usados para armazenar textos, imagens e outros dados do jogo.

📁 Estrutura Atual do Projeto
evangelion-thfs-tools/
├── exemplos de arquivos/        # Exemplos de arquivos .THFS, .gim etc
├── scripts python/              # Scripts de extração, análise e conversão
│   ├── extrator_thfs.py         # Script principal para extrair arquivos .THFS
│   ├── converter.py             # Conversor de arquivos .GIM usando gimconv.exe
│   ├── codigov4.py              # Versões anteriores ou de teste
│   └── outros scripts...        # Scripts auxiliares
├── LICENSE                      # Licença do projeto (MIT)
└── README.md                    # Este arquivo
🚀 Como usar
📦 1. Extração de arquivos .THFS
Coloque seu arquivo .THFS (ex: SCRIPT.THFS) na raiz do projeto.

Execute o script principal:
python scripts\python\extrator_thfs.py
Será criado o diretório extraidos/ com todos os arquivos extraídos.

🖼 2. Conversão de imagens .GIM
Este projeto usa o gimconv.exe da Sony para converter arquivos .gim em imagens .png.

Baixe ou copie o gimconv.exe e seus arquivos auxiliares para a pasta correta.

Coloque os arquivos .gim extraídos na pasta gim_extraidos/.

Execute:
python scripts\python\converter.py
📄 Arquivos Gerados
entradas_thfs.json – Metadados dos arquivos extraídos (.offset, tamanho, nome, etc.)

log_extracao.txt – Registro completo do processo de extração

📚 Objetivo do Projeto
Compreender como o PSP lida com arquivos .THFS

Realizar engenharia reversa dos formatos usados no jogo

Traduzir os arquivos de texto do japonês/inglês para o português

Criar uma ferramenta universal de extração/recompactação .THFS

🧪 Status atual
🚧 Extração básica de arquivos .THFS quase funcinando

✅ Leitura segura de headers e checagem de sobreposição

✅ Extração e nomeação segura de arquivos

🚧 Conversão de .gim ainda em testes

🔜 Leitura de arquivos de texto internos e recompilação futura

🤝 Contribuindo
Estamos construindo uma documentação técnica passo a passo sobre:

Como o PSP carrega os arquivos

Como manipular a RAM dump

Como identificar padrões em Shift-JIS

Como melhorar a precisão do extrator

💡 Toda ajuda é bem-vinda!

📜 Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
