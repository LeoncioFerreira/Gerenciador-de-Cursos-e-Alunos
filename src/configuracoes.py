import json
class Configuracoes:
    """
    Carrega e gerencia parâmetros do arquivo settings.json

    Exemplos de parâmetros:
    - nota_minima_aprovacao
    - frequencia_minima
    - data_limite_trancamento

    Responsável por:
    - Ler e validar o arquivo de configuração
    - Fornecer acesso padronizado aos valores
    """
    def __init__(self, caminho="settings.json"):
        # Abre e lê o arquivo de configuração usando encoding utf-8 para evitar erros de acentuação
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f) 
        # O método .get serve para caso a chave não existir no JSON
        self.nota_minima_aprovacao = dados.get("nota_minima_aprovacao", 7.0)
        self.frequencia_minima = dados.get("frequencia_minima", 75)
        self.data_limite_trancamento = dados.get("data_limite_trancamento", "2025-12-31")
        self.max_turmas_por_aluno = dados.get("max_turmas_por_aluno", None)
        self.top_n_alunos = dados.get("top_n_alunos", 5)