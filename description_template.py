

def montar_descricao(frase_do_video: str, tags_do_video: list, perfil: dict) -> str:
  # Junta as tags fixas do canal com as tags específicas do vídeo em uma única lista
  # Exemplo: ["SpaceMusic", "Astronaut"] + ["nebula", "ambient"] → ["SpaceMusic", "Astronaut", "nebula", "ambient"]
  todas_tags = perfil["tags_fixas"] + tags_do_video

  # Transforma a lista de tags em uma string de hashtags separadas por vírgula
  # Exemplo: ["SpaceMusic", "nebula"] → "#SpaceMusic, #nebula"
  hashtags = ", ".join(f"#{tag}" for tag in todas_tags)

  # Monta a descrição final combinando as três partes:
  # 1. Frase única do vídeo (vem do CSV)
  # 2. Texto fixo do canal (vem do perfil)
  # 3. Hashtags (geradas acima)
  descricao = f"{frase_do_video}\n{perfil['descricao_fixa']}\n{hashtags}"
  return descricao


def montar_tags(tags_do_video: list, perfil: dict) -> list:
  # Retorna a lista completa de tags: fixas do canal + específicas do vídeo
  # Essa lista é enviada separadamente para a API do YouTube (diferente das hashtags da descrição)
  return perfil["tags_fixas"] + tags_do_video

