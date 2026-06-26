import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ["https://www.googleapis.com/auth/youtube"]
CREDENTIALS_FILE = "credentials/client_secret.json"
TOKEN_FILE = "token.json"


# Função para obter as credenciais do usuário
def get_credentials():
  creds = None

  # Se já existe um token salvo, carrega ele
  if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

  # Se não existe ou expirou, inicia o fluxo OAuth
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
      creds = flow.run_local_server(port=0)

    # Salva o token para não precisar logar toda vez
    with open(TOKEN_FILE, "w") as token:
      token.write(creds.to_json())

  return creds
