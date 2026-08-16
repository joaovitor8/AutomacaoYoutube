import json     # Lê e escreve arquivos JSON (a fila de vídeos)
import os       # Verifica se arquivos existem no disco
import time     # Adiciona pausa entre uploads
from youtube_client import get_youtube_client       # Cria a conexão com a API do YouTube
from uploader import agendar_video, adicionar_a_playlist, definir_thumbnail  # Faz o upload, agendamento, playlist e thumbnail
from logger import iniciar_log, registrar           # Cria e escreve no arquivo de log
from description_template import montar_descricao, montar_tags  # Monta descrição e tags


def processar_fila(perfil: dict):
  log_path = iniciar_log()  # Cria o arquivo de log para essa execução
  registrar(log_path, f"=== Canal: {perfil['nome']} ===")

  # Cria o cliente autenticado da API usando as credenciais do perfil
  youtube = get_youtube_client(perfil["credentials_file"], perfil["token_file"])

  # Abre o JSON da fila e carrega todos os itens como lista de dicionários
  # Cada item já é um dict: {"titulo": "...", "status": "pending", ...}
  with open(perfil["queue_file"], "r", encoding="utf-8") as f:
    linhas = json.load(f)

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
      salvar_fila(linhas, perfil["queue_file"])  # Salva o erro no JSON
      continue  # Passa para o próximo vídeo

    try:
      registrar(log_path, f"Iniciando upload: {titulo}")

      # Tags extras já vêm como lista no JSON
      # Exemplo: ["ambient", "nebula", "scifi"]
      tags_extras = linha["tags_extras"]

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
        category_id=perfil["category_id"],
        conteudo_ia=linha.get("conteudo_ia", False)  # Opcional — declara vídeo com conteúdo gerado/alterado por IA
      )

      linha["status"] = "done"       # Marca como concluído
      linha["video_id"] = video_id   # Salva o ID retornado pela API
      registrar(log_path, f"OK: {titulo} → https://youtube.com/watch?v={video_id}")

      # Playlist é opcional: pode vir no próprio vídeo (linha) ou como padrão do canal (perfil)
      # Se nenhuma das duas existir, o vídeo simplesmente não entra em playlist nenhuma
      playlist_id = linha.get("playlist_id") or perfil.get("playlist_id")
      if playlist_id:
        try:
          adicionar_a_playlist(youtube, video_id, playlist_id)
          registrar(log_path, f"Adicionado à playlist: {playlist_id}")
        except Exception as e:
          # Falha na playlist não desfaz o upload já feito — só registra o aviso
          registrar(log_path, f"AVISO: falha ao adicionar '{titulo}' à playlist — {str(e)}")

      # Thumbnail também é opcional — só define se o vídeo tiver o campo no JSON
      thumbnail = linha.get("thumbnail")
      if thumbnail:
        if os.path.exists(thumbnail):
          try:
            definir_thumbnail(youtube, video_id, thumbnail)
            registrar(log_path, f"Thumbnail definida: {thumbnail}")
          except Exception as e:
            # Falha na thumbnail também não desfaz o upload
            registrar(log_path, f"AVISO: falha ao definir thumbnail de '{titulo}' — {str(e)}")
        else:
          registrar(log_path, f"AVISO: thumbnail não encontrada — {thumbnail}")

    except Exception as e:
      # Se qualquer erro ocorrer durante o upload, marca como error e continua
      linha["status"] = "error"
      registrar(log_path, f"ERRO em '{titulo}': {str(e)}")

    salvar_fila(linhas, perfil["queue_file"])  # Salva o progresso após cada vídeo
    time.sleep(3)  # Pausa de 3 segundos para não sobrecarregar a API

  registrar(log_path, "=== Processamento concluído ===")
  resumo(linhas, log_path)


def salvar_fila(linhas: list, queue_file: str):
  # Reescreve o JSON inteiro com os dados atualizados
  with open(queue_file, "w", encoding="utf-8") as f:
    json.dump(linhas, f, indent=2, ensure_ascii=False)  # Salva formatado e com acentos legíveis


def resumo(linhas: list, log_path: str):
  total = len(linhas)  # Total de vídeos na fila
  done = sum(1 for l in linhas if l["status"] == "done")    # Quantos foram enviados
  erros = sum(1 for l in linhas if l["status"] == "error")  # Quantos falharam
  registrar(log_path, f"Resumo: {done}/{total} enviados | {erros} erro(s)")
