from flask import Blueprint, render_template
from src.services.relatorio_service import (
    relatorio_aprovacao_turma, 
    relatorio_notas_turma, 
    relatorio_top_alunos
)
from src.infra.persistencia import carregar_turmas, carregar_cursos

"""
Módulo de Rotas da Aplicação (Flask)

Responsabilidade:
- Definir as rotas HTTP da aplicação.
- Receber dados da interface (formulários HTML).
- Delegar toda a lógica de negócio para a camada de serviços.
- Renderizar templates ou redirecionar respostas.

Observação:
Este módulo NÃO contém regras de negócio.
Toda validação complexa é realizada nas camadas
Services e Sistema, respeitando a separação de responsabilidades.
"""

relatorios_bp = Blueprint("relatorios", __name__)

# Rota padrão de relatorios que  mostra Top n alunoes e desepenho por turma 
@relatorios_bp.route("/")
def dashboard():
    turmas = carregar_turmas()
    cursos = carregar_cursos()
    
    # Cria um dicionário para achar o nome do curso rápido: { "MAT101": "Matemática",}
    mapa_cursos = {c["codigo"]: c["nome"] for c in cursos}
    
    # Top N Alunos
    top_alunos = relatorio_top_alunos()
    
    # Dados por Turma
    stats_turmas = []
    for t in turmas:
        aprovacao = relatorio_aprovacao_turma(t["codigo_oferta"])
        notas = relatorio_notas_turma(t["codigo_oferta"])
        
        # Pega o nome do curso no mapa. Se não achar, usa "Desconhecido"
        nome_curso = mapa_cursos.get(t["codigo_curso"], "Desconhecido")
        
        # Status das turmas
        stats_turmas.append({
            "codigo": t["codigo_oferta"],
            "disciplina": f"{t['codigo_curso']} - {nome_curso}", 
            "taxa_aprovacao": aprovacao["taxa"],
            "media_notas": notas["media"],
            "total_alunos": aprovacao["total"]
        })

    return render_template(
        "relatorios/relatorios.html", 
        top_alunos=top_alunos,
        stats_turmas=stats_turmas,
        cursos=cursos
    )

# Rota detalhada que mostra top n aluno desvio padão meida 
@relatorios_bp.route("/detalhe/turma/<codigo>")
def detalhe_turma(codigo):
    aprovacao = relatorio_aprovacao_turma(codigo)
    notas = relatorio_notas_turma(codigo)
    
    return render_template(
        "relatorios/detalhe_turma.html",
        codigo=codigo,
        aprovacao=aprovacao,
        notas=notas
    )