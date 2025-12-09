"""
Pacote de Infraestrutura

Responsabilidade:
- Gerenciar a persistência de dados (Salvar/Carregar JSON)
- Gerenciar configurações externas (settings.json)
- Isolar o restante do sistema de detalhes técnicos de arquivos

Garante que as camadas superiores (Models/Services) não precisem saber "como" os dados são salvos, apenas que eles são salvos
"""

from .persistencia import *

import os
from .configuracoes import Configuracoes
from .persistencia import *


# Descobre onde este arquivo (__init__.py) está
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

# Sobe niveis: infra  src  Raiz do Projeto
DIRETORIO_SRC = os.path.dirname(DIRETORIO_ATUAL)
PROJETO_RAIZ = os.path.dirname(DIRETORIO_SRC)

# Aponta para data/settings.json
SETTINGS_PATH = os.path.join(PROJETO_RAIZ, "data", "settings.json")

# Cria a instância única 'config' que todo mundo vai usar
config = Configuracoes(SETTINGS_PATH)