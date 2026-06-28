import csv      # Lê e escreve arquivos CSV (a fila de vídeos)
import os       # Verifica se arquivos existem no disco
import time     # Adiciona pausa entre uploads
from youtube_client import get_youtube_client       # Cria a conexão com a API do YouTube
from uploader import agendar_video                  # Faz o upload e agendamento do vídeo
from logger import iniciar_log, registrar           # Cria e escreve no arquivo de log
from description_template import montar_descricao, montar_tags  # Monta descrição e tags


def processar_fila(perfil: dict):
  log_path = iniciar_log()  # Cria o arquivo de log para essa execução
  registrar(log_path, f"=== Canal: {perfil['nome']} ===")

  # Cria o cliente autenticado da API usando as credenciais do perfil
  youtube = get_youtube_client(perfil["credentials_file"], perfil["token_file"])

  # Abre o CSV da fila e carrega todas as linhas como lista de dicionários
  # Cada linha vira um dict: {"titulo": "...", "status": "pending", ...}
  with open(perfil["queue_file"], "r", encoding="utf-8") as f:
    linhas = list(csv.DictReader(f))

  # Filtra apenas as linhas com status "pending"
  pendentes = [l for l in linhas if l["status"] == "pending"]
  registrar(log_path, f"{len(pendentes)} vídeo(s) pendente(s) encontrado(s)")

  if not pendentes:
    registrar(log_path, "Nenhum vídeo pendente. Encerrando.")
    return  # Encerra a função se não houver nada para processar

  for linha in linhas:
    if linha["status"] != "pending":
      continue  # Pula vídeos já processados (done ou error)

    titulo = linha["titulo"]
    arquivo = linha["arquivo"]

    # Verifica se o arquivo de vídeo existe antes de tentar o upload
    if not os.path.exists(arquivo):
      registrar(log_path, f"ERRO: Arquivo não encontrado — {arquivo}")
      linha["status"] = "error"
      salvar_fila(linhas, perfil["queue_file"])  # Salva o erro no CSV
      continue  # Passa para o próximo vídeo

    try:
      registrar(log_path, f"Iniciando upload: {titulo}")

      # Tags extras vêm separadas por ";" no CSV → transforma em lista
      # Exemplo: "ambient;nebula;scifi" → ["ambient", "nebula", "scifi"]
      tags_extras = linha["tags_extras"].split(";")

      # Monta a descrição completa: frase do vídeo + texto fixo do canal + hashtags
      descricao_completa = montar_descricao(linha["frase"], tags_extras, perfil)

      # Junta as tags fixas do canal com as tags específicas do vídeo
      tags_completas = montar_tags(tags_extras, perfil)

      # Faz o upload e retorna o ID do vídeo criado no YouTube
      video_id = agendar_video(
        youtube=youtube,
        arquivo=arquivo,
        titulo=titulo,
        descricao=descricao_completa,
        tags=tags_completas,
        data_publicacao=linha["data_publicacao"],
        category_id=perfil["category_id"]
      )

      linha["status"] = "done"       # Marca como concluído
      linha["video_id"] = video_id   # Salva o ID retornado pela API
      registrar(log_path, f"OK: {titulo} → https://youtube.com/watch?v={video_id}")

    except Exception as e:
      # Se qualquer erro ocorrer durante o upload, marca como error e continua
      linha["status"] = "error"
      registrar(log_path, f"ERRO em '{titulo}': {str(e)}")

    salvar_fila(linhas, perfil["queue_file"])  # Salva o progresso após cada vídeo
    time.sleep(3)  # Pausa de 3 segundos para não sobrecarregar a API

  registrar(log_path, "=== Processamento concluído ===")
  resumo(linhas, log_path)


def salvar_fila(linhas: list, queue_file: str):
  # Pega os nomes das colunas a partir das chaves do primeiro dicionário
  campos = list(linhas[0].keys())

  # Reescreve o CSV inteiro com os dados atualizados
  with open(queue_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()   # Escreve o cabeçalho (nomes das colunas)
    writer.writerows(linhas)  # Escreve todas as linhas


def resumo(linhas: list, log_path: str):
  total = len(linhas)  # Total de vídeos na fila
  done = sum(1 for l in linhas if l["status"] == "done")    # Quantos foram enviados
  erros = sum(1 for l in linhas if l["status"] == "error")  # Quantos falharam
  registrar(log_path, f"Resumo: {done}/{total} enviados | {erros} erro(s)")

