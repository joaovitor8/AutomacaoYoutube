from googleapiclient.discovery import build  # Função que constrói o cliente de qualquer API do Google
from auth import get_credentials             # Nossa função de autenticação OAuth


def get_youtube_client(credentials_file: str, token_file: str):
  # Obtém as credenciais OAuth do canal (carrega o token salvo ou inicia novo login)
  creds = get_credentials(credentials_file, token_file)

  # Constrói o cliente da API do YouTube
  # "youtube" → nome da API
  # "v3"      → versão da API
  # credentials → credenciais OAuth para autenticar as requisições
  youtube = build("youtube", "v3", credentials=creds)

  return youtube  # Retorna o cliente pronto para fazer chamadas à API

