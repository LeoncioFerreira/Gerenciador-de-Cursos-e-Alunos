from src.infra.persistencia import carregar_alunos, salvar_alunos
from src.models.aluno import Aluno
"""
Serviços de Aluno

Responsabilidade:
- Orquestrar operações relacionadas a alunos.
- Garantir regras de negócio como unicidade de matrícula.
- Criar objetos Aluno de forma validada.
- Persistir dados de alunos utilizando a camada de infraestrutura.

Este módulo NÃO contém lógica de interface (Flask)
e NÃO acessa diretamente templates HTML.
"""

# Serviços de cadastro
def servico_criar_aluno(nome, email, matricula):
    lista_alunos = carregar_alunos()

    # Garante que é um  str limpo e não vazia
    nova_matricula = str(matricula).strip()
    
    # Valida duplicidade (comparando strings)
    for a in lista_alunos:
        if str(a["matricula"]) == nova_matricula:
            raise ValueError(f"Erro: A matrícula {nova_matricula} já está cadastrada!")
    # Caso passe passe pelas validaçoẽs cria o objeto matricula
    obj = Aluno(nome, email, nova_matricula)
    
    # Adiciona os dados a uma lista e manda para o json
    lista_alunos.append({
        "matricula": nova_matricula, 
        "nome": obj.nome, 
        "email": obj.email
    })
    salvar_alunos(lista_alunos)