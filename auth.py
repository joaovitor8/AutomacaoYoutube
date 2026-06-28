import os
from google.oauth2.credentials import Credentials          # Representa as credenciais OAuth salvas
from google_auth_oauthlib.flow import InstalledAppFlow     # Gerencia o fluxo de login via navegador
from google.auth.transport.requests import Request         # Usado para renovar o token expirado

# Define o nível de acesso que o bot terá na conta do YouTube
# "youtube" = acesso completo (upload, edição, agendamento)
SCOPES = ["https://www.googleapis.com/auth/youtube"]


def get_credentials(credentials_file: str, token_file: str):
  # Cria a pasta "tokens/" se ainda não existir
  os.makedirs("tokens", exist_ok=True)

  creds = None

  # Se já existe um token salvo, carrega ele (evita abrir o navegador toda vez)
  if os.path.exists(token_file):
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)

  # Verifica se as credenciais são inválidas ou inexistentes
  if not creds or not creds.valid:

    if creds and creds.expired and creds.refresh_token:
      # Token expirado mas ainda tem refresh_token → renova automaticamente sem abrir o navegador
      creds.refresh(Request())
    else:
      # Sem token salvo → abre o navegador para o usuário fazer login e autorizar o app
      flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
      creds = flow.run_local_server(port=0)

    # Salva o token em disco para reutilizar nas próximas execuções
    with open(token_file, "w") as token:
      token.write(creds.to_json())

  return creds  # Retorna as credenciais válidas para o youtube_client usar

