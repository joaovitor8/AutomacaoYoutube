from googleapiclient.discovery import build
from auth import get_credentials


# Função para obter o cliente do YouTube
def get_youtube_client():
  creds = get_credentials()
  youtube = build("youtube", "v3", credentials=creds)
  return youtube
