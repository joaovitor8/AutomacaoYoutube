import datetime
from googleapiclient.http import MediaFileUpload  # Prepara o arquivo de vídeo para envio via API


def agendar_video(youtube, arquivo: str, titulo: str, descricao: str, tags: list, data_publicacao: str, category_id: str = "10"):
  # Converte a data do formato ISO (ex: "2026-08-01T18:00:00")
  # para o formato UTC exigido pela API do YouTube (ex: "2026-08-01T18:00:00.000Z")
  data_utc = datetime.datetime.fromisoformat(data_publicacao).strftime(
    "%Y-%m-%dT%H:%M:%S.000Z"
  )

  # Dicionário com todos os metadados do vídeo enviados para a API
  body = {
    "snippet": {
      "title": titulo,            # Título do vídeo
      "description": descricao,   # Descrição completa
      "tags": tags,               # Lista de tags
      "categoryId": category_id   # Categoria do YouTube (10 = Music, 22 = People & Blogs)
    },
    "status": {
      "privacyStatus": "private",  # Sobe como privado para não aparecer antes da hora
      "publishAt": data_utc        # Data em que o YouTube tornará o vídeo público automaticamente
    }
  }

  # Prepara o arquivo .mp4 para upload
  # resumable=True permite retomar o envio se a conexão cair durante o upload
  media = MediaFileUpload(arquivo, mimetype="video/mp4", resumable=True)

  print(f"Iniciando upload: {titulo}")
  print(f"Agendado para: {data_publicacao}")
  print("-" * 40)

  # Cria a requisição de upload para a API do YouTube
  # part="snippet,status" indica quais seções do body estamos enviando
  request = youtube.videos().insert(
    part="snippet,status",
    body=body,
    media_body=media
  )

  # Envia o vídeo em partes (chunks) e exibe o progresso
  # next_chunk() envia o próximo pedaço do arquivo
  # Retorna (status, response): status tem o progresso, response vem preenchido só quando termina
  response = None
  while response is None:
    status, response = request.next_chunk()
    if status:
      progresso = int(status.progress() * 100)
      print(f"Enviando... {progresso}%")

  # Quando response não é None, o upload foi concluído
  # A API retorna um dicionário com os dados do vídeo criado, incluindo o ID
  video_id = response["id"]
  print(f"\nUpload concluído!")
  print(f"ID do vídeo: {video_id}")
  print(f"Link: https://youtube.com/watch?v={video_id}")

  return video_id  # Retorna o ID para ser salvo no CSV pelo queue_processor

