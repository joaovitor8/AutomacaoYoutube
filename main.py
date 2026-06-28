import sys          # Permite ler argumentos passados no terminal
import importlib    # Permite importar arquivos Python pelo nome dinamicamente
from queue_processor import processar_fila  # Função que processa a fila de vídeos


def carregar_perfil(nome: str) -> dict:
  try:
    # Importa o arquivo profiles/<nome>.py dinamicamente
    modulo = importlib.import_module(f"profiles.{nome}")
    return modulo.PERFIL  # Retorna o dicionário PERFIL do arquivo

  except ModuleNotFoundError:
    return None  # Retorna None se o arquivo não existir


# Garante que esse bloco só roda quando o arquivo é executado diretamente
if __name__ == "__main__":

  # sys.argv é a lista de argumentos do terminal
  if len(sys.argv) < 2:
    print("Uso: python main.py <nome_do_perfil>")
    print("Exemplo: python main.py astronautium")
    sys.exit(1)  # Encerra o programa com erro

  nome_perfil = sys.argv[1]  # Pega o nome do perfil passado no terminal
  perfil = carregar_perfil(nome_perfil)  # Tenta carregar o perfil

  if perfil is None:
    print(f"Perfil '{nome_perfil}' não encontrado.")
    print("Crie o arquivo correspondente em profiles/<nome>.py")
    sys.exit(1)

  processar_fila(perfil)  # Inicia o processamento da fila do canal

