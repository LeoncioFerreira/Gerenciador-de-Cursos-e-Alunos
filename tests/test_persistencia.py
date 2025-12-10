import os
import tempfile
from src.infra.persistencia import salvar, carregar

def test_persistencia_salvar_e_carregar():
    # Cria diretório e arquivo temporários
    with tempfile.TemporaryDirectory() as tmpdir:
        caminho = os.path.join(tmpdir, "teste.json")

        dados_original = [
            {"nome": "João", "matricula": "2025001"},
            {"nome": "Maria", "matricula": "2025002"}
        ]

        # Salva no json
        salvar(caminho, dados_original)

        # Garante que o arquivo realmente existe
        assert os.path.exists(caminho)

        # Carrega do JSON
        dados_carregados = carregar(caminho)

        # Verifica se o conteúdo é igual
        assert dados_carregados == dados_original