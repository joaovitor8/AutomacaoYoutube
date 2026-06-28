import os        # Cria pastas se não existirem
import datetime  # Gera timestamps para o nome do arquivo e para cada linha do log

LOG_DIR = "logs"  # Pasta onde os arquivos de log serão salvos


def iniciar_log():
  # Cria a pasta "logs/" se ela ainda não existir (exist_ok=True evita erro se já existir)
  os.makedirs(LOG_DIR, exist_ok=True)

  # Gera um timestamp com data e hora atual para usar no nome do arquivo
  # Exemplo: "2026-06-25_10-30-00"
  data_hoje = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

  # Retorna o caminho completo do arquivo de log
  # Exemplo: "logs/upload_2026-06-25_10-30-00.log"
  return os.path.join(LOG_DIR, f"upload_{data_hoje}.log")


def registrar(log_path: str, mensagem: str):
  # Gera o timestamp do momento exato em que a mensagem foi registrada
  # Exemplo: "2026-06-25 10:30:05"
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  # Formata a linha com o timestamp entre colchetes
  # Exemplo: "[2026-06-25 10:30:05] Upload concluído!"
  linha = f"[{timestamp}] {mensagem}"

  print(linha)  # Exibe no terminal em tempo real

  # Abre o arquivo de log em modo append ("a") e adiciona a linha
  # Modo "a" adiciona ao final do arquivo sem apagar o conteúdo anterior
  with open(log_path, "a", encoding="utf-8") as f:
    f.write(linha + "\n")

