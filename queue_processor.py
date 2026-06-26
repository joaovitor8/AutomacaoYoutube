import csv
import os
import time
from uploader import agendar_video
from logger import iniciar_log, registrar
from description_template import montar_descricao, montar_tags


QUEUE_FILE = "list/videos-agendar.csv"


def processar_fila():
  log_path = iniciar_log()
  registrar(log_path, "=== Iniciando processamento da fila ===")

  # Lê o CSV
  with open(QUEUE_FILE, "r", encoding="utf-8") as f:
    linhas = list(csv.DictReader(f))

  pendentes = [l for l in linhas if l["status"] == "pending"]
  registrar(log_path, f"{len(pendentes)} vídeo(s) pendente(s) encontrado(s)")

  if not pendentes:
    registrar(log_path, "Nenhum vídeo pendente. Encerrando.")
    return

  for linha in linhas:
    if linha["status"] != "pending":
      continue

    titulo = linha["titulo"]
    arquivo = linha["arquivo"]

    # Verifica se o arquivo existe antes de tentar upload
    if not os.path.exists(arquivo):
      registrar(log_path, f"ERRO: Arquivo não encontrado — {arquivo}")
      linha["status"] = "error"
      salvar_fila(linhas)
      continue

    try:
      registrar(log_path, f"Iniciando upload: {titulo}")

      tags_extras = linha["tags_extras"].split(";")

      descricao_completa = montar_descricao(
        frase_do_video=linha["frase"],
        tags_do_video=tags_extras
      )

      tags_completas = montar_tags(tags_extras)

      video_id = agendar_video(
        arquivo=arquivo,
        titulo=titulo,
        descricao=descricao_completa,
        tags=tags_completas,
        data_publicacao=linha["data_publicacao"]
      )

      linha["status"] = "done"
      linha["video_id"] = video_id
      registrar(log_path, f"OK: {titulo} → https://youtube.com/watch?v={video_id}")

    except Exception as e:
      linha["status"] = "error"
      registrar(log_path, f"ERRO em '{titulo}': {str(e)}")

    # Salva o progresso após cada vídeo
    salvar_fila(linhas)

    # Pausa entre uploads para não sobrecarregar a API
    time.sleep(3)

  registrar(log_path, "=== Processamento concluído ===")
  resumo(linhas, log_path)

def salvar_fila(linhas: list):
  campos = list(linhas[0].keys())
  with open(QUEUE_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    writer.writerows(linhas)

def resumo(linhas: list, log_path: str):
  total = len(linhas)
  done = sum(1 for l in linhas if l["status"] == "done")
  erros = sum(1 for l in linhas if l["status"] == "error")
  registrar(log_path, f"Resumo: {done}/{total} enviados | {erros} erro(s)")

