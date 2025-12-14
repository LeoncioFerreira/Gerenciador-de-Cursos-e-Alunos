from src.infra.persistencia import carregar_cursos, salvar_cursos
from src.models.curso import Curso
"""
Serviços de Curso

Responsabilidade:
- Gerenciar a criação de cursos.
- Garantir unicidade do código do curso.
- Validar dados de cursos antes da persistência.

Este módulo centraliza as regras relacionadas a cursos,
mantendo a lógica fora das rotas e da persistência.
"""
def servico_criar_curso(codigo, nome, ch, pre_reqs):
    lista_cursos = carregar_cursos()
    
    # Verifica duplicidade convertendo para string
    if any(str(c['codigo']) == str(codigo) for c in lista_cursos):
         raise ValueError(f"Erro: O código de curso {codigo} já existe!")

    # Caso passe da validação vira um objeto curso
    obj = Curso(codigo, nome, int(ch), pre_reqs)
    
    # Adiciona os dados a uma lista e manda para o json
    lista_cursos.append({
        "codigo": obj.codigo, 
        "nome": obj.nome, 
        "carga_horaria": obj.carga_horaria, 
        "pre_requisitos": obj.pre_requisitos
    })
    salvar_cursos(lista_cursos)