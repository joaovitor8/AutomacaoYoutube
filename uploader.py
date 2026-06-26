import datetime
from googleapiclient.http import MediaFileUpload
from youtube_client import get_youtube_client


def agendar_video( arquivo: str, titulo: str, descricao: str, tags: list, data_publicacao: str ):
  
  youtube = get_youtube_client()

  # Converte para o formato UTC exigido pela API
  data_utc = datetime.datetime.fromisoformat(data_publicacao).strftime(
    "%Y-%m-%dT%H:%M:%S.000Z"
  )

  # Metadados do vídeo
  body = {
    "snippet": {
      "title": titulo,
      "description": descricao,
      "tags": tags,
      "categoryId": "10"  # 10 = Music
    },
    "status": {
      "privacyStatus": "private",   # começa privado
      "publishAt": data_utc          # e publica automaticamente nessa data
    }
  }

  # Prepara o arquivo para upload
  media = MediaFileUpload(
    arquivo,
    mimetype="video/mp4",
    resumable=True  # permite retomar se a conexão cair
  )

  print(f"Iniciando upload: {titulo}")
  print(f"Agendado para: {data_publicacao}")
  print("-" * 40)

  # Faz o upload
  request = youtube.videos().insert(
    part="snippet,status",
    body=body,
    media_body=media
  )

  # Progresso do upload em chunks
  response = None
  while response is None:
    status, response = request.next_chunk()
    if status:
      progresso = int(status.progress() * 100)
      print(f"Enviando... {progresso}%")

  video_id = response["id"]
  print(f"\nUpload concluído!")
  print(f"ID do vídeo: {video_id}")
  print(f"Link: https://youtube.com/watch?v={video_id}")

  return video_id

