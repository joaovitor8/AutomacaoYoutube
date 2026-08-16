# Automação YouTube

Bot em Python para upload, agendamento e publicação automática de vídeos no YouTube, com suporte a múltiplos canais.

## Funcionalidades

- Upload e agendamento de vídeos a partir de uma fila em JSON
- Suporte a múltiplos canais, cada um com seu próprio perfil e credenciais
- Adição automática a playlists (padrão por canal ou específica por vídeo)
- Definição automática de thumbnail
- Declaração de conteúdo gerado/alterado por IA (exigência da política do YouTube)
- Log detalhado de cada execução, com timestamp
- Retomada segura: um vídeo com erro não trava os demais, e cada item da fila guarda seu próprio status

## Estrutura de pastas

```
AutomacaoYoutube/
├── credentials/            # Chaves OAuth (não versionado, exceto o exemplo)
├── lista/
│   └── <nome-canal>/
│       └── agendar.json    # Fila de vídeos daquele canal
├── profiles/
│   └── <nome-canal>.py     # Configuração de cada canal
├── videos/                 # Arquivos de vídeo (não versionado)
├── imagens/                # Thumbnails (não versionado)
├── tokens/                 # Tokens OAuth gerados automaticamente (não versionado)
├── logs/                   # Log de cada execução (não versionado)
├── main.py                 # Ponto de entrada — recebe o nome do perfil
├── queue_processor.py      # Lê a fila, faz upload, playlist e thumbnail
├── uploader.py              # Chamadas à API: agendar vídeo, playlist, thumbnail
├── youtube_client.py        # Constrói o cliente autenticado da API
├── auth.py                  # Fluxo OAuth (login + renovação de token)
├── description_template.py  # Monta descrição e tags de cada vídeo
└── logger.py                 # Log em arquivo e no terminal
```

## Pré-requisitos

- Python 3.10+
- Projeto no [Google Cloud Console](https://console.cloud.google.com) com a **YouTube Data API v3** ativada

## Instalação

```bash
git clone https://github.com/joaovitor8/AutomacaoYoutube.git
cd AutomacaoYoutube
pip install -r requirements.txt
```

## Configuração

### 1. Credenciais OAuth

No Google Cloud Console:
1. Crie um projeto e ative a **YouTube Data API v3**
2. Crie uma credencial do tipo **OAuth Client ID** → aplicativo de desktop
3. Baixe o JSON e salve em `credentials/client_secret-<nome_canal>.json`

Na primeira execução de cada canal, o script abre o navegador pra você autorizar o acesso. O token fica salvo em `tokens/` e é renovado sozinho depois.

### 2. Perfil do canal

Copie `profiles/_nome-canal.py` para `profiles/<nome_do_canal>.py`:

```python
PERFIL = {
  "nome": "Nome do Canal",
  "credentials_file": "credentials/client_secret-nome_canal.json",
  "token_file": "tokens/nome_canal.json",
  "queue_file": "lista/nome-canal/agendar.json",
  "category_id": "10",  # 10 = Music, 22 = People & Blogs, etc.
  "playlist_id": "PLxxxxxxxxxxxxxxxxxxxxxxxx",  # opcional — playlist padrão do canal
  "tags_fixas": ["tag1", "tag2"],
  "descricao_fixa": "Texto fixo que entra em toda descrição..."
}
```

### 3. Fila de vídeos

Copie `lista/_nome-canal/agendar.json` para `lista/<nome_do_canal>/agendar.json` e adicione um item por vídeo:

```json
[
  {
    "arquivo": "videos/meu-video.mp4",
    "titulo": "Título do vídeo",
    "frase": "Frase/descrição única desse vídeo.",
    "tags_extras": ["tag1", "tag2"],
    "data_publicacao": "2026-12-25T18:00:00",
    "status": "pending",
    "playlist_id": "PLxxxx",
    "thumbnail": "imagens/capa.jpg",
    "conteudo_ia": true
  }
]
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `arquivo` | sim | Caminho do arquivo de vídeo |
| `titulo` | sim | Título do vídeo no YouTube |
| `frase` | sim | Texto único que entra na descrição |
| `tags_extras` | sim | Lista de tags específicas do vídeo |
| `data_publicacao` | sim | Data/hora de publicação, formato ISO 8601 (`AAAA-MM-DDTHH:MM:SS`) |
| `status` | sim | `pending`, `done` ou `error` — atualizado automaticamente pelo script |
| `playlist_id` | não | Playlist onde o vídeo entra (sobrepõe a do perfil) |
| `thumbnail` | não | Caminho da imagem de capa |
| `conteudo_ia` | não | `true`/`false` — declara conteúdo sintético/alterado por IA. Padrão: `false` |

## Uso

```bash
python main.py <nome_do_perfil>
```

Exemplo: `python main.py astronautium` carrega `profiles/astronautium.py` e processa a fila daquele canal.

Em cada execução, o script:
1. Lê os vídeos com `status: "pending"` na fila do canal
2. Faz upload, agenda a publicação, adiciona à playlist e define a thumbnail (quando informados)
3. Atualiza o `status` de cada vídeo no próprio JSON (`done` ou `error`)
4. Grava um log da execução em `logs/`

Um vídeo com erro fica marcado como `error` e não interrompe os demais — corrija e rode de novo, só ele será reprocessado.

## Limitações conhecidas

- **Tela final (end screen)**: a API do YouTube não permite configurar isso — precisa ser feito manualmente no YouTube Studio depois do upload.
- **Thumbnail customizada**: alguns canais precisam de verificação de identidade habilitada no YouTube pra essa permissão funcionar.

## Licença

MIT — veja [LICENSE](LICENSE).