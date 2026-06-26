import os
import datetime

LOG_DIR = "logs"

def iniciar_log():
  os.makedirs(LOG_DIR, exist_ok=True)
  data_hoje = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  return os.path.join(LOG_DIR, f"upload_{data_hoje}.log")

def registrar(log_path: str, mensagem: str):
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  linha = f"[{timestamp}] {mensagem}"
  print(linha)
  with open(log_path, "a", encoding="utf-8") as f:
    f.write(linha + "\n")

