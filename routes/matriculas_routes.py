from flask import Blueprint, render_template, request, redirect
from src.infra.persistencia import carregar_alunos, carregar_turmas, carregar_matriculas
from src.services.matricula_service import (
    servico_criar_matricula, 
    servico_atualizar_nota, 
    servico_atualizar_frequencia, 
    servico_trancar_matricula
)
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

matriculas_bp = Blueprint("matriculas", __name__)

@matriculas_bp.route("/")
def listar():
    return render_template("matriculas/matriculas.html", matriculas=carregar_matriculas(),alunos=carregar_alunos())

@matriculas_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        try:
            # Chama o serviço que valida e salva
            servico_criar_matricula(request.form["aluno"], request.form["turma"])
            return redirect("/matriculas")
        except Exception as e:
            return render_template("matriculas/cad_matriculas.html", 
                                   alunos=carregar_alunos(), 
                                   turmas=carregar_turmas(), 
                                   erro=str(e))

    return render_template("matriculas/cad_matriculas.html", 
                           alunos=carregar_alunos(), 
                           turmas=carregar_turmas())

@matriculas_bp.route("/nota/<int:index>", methods=["GET", "POST"]) 
def lancar_nota(index):
    # get: Só exibe o form
    if request.method == "GET":
        return render_template("matriculas/lancar_nota.html", 
                               matricula=carregar_matriculas()[index], index=index)
    
    # post: Chama o serviço
    try:
        servico_atualizar_nota(index, request.form["nota"])
        return redirect("/matriculas")
    except Exception as e:
        return render_template("matriculas/lancar_nota.html", 
                               matricula=carregar_matriculas()[index], index=index, erro=str(e))

@matriculas_bp.route("/frequencia/<int:index>", methods=["GET", "POST"])
def lancar_frequencia(index):
    if request.method == "GET":
        return render_template("matriculas/lancar_frequencia.html", 
                               matricula=carregar_matriculas()[index], index=index)

    try:
        servico_atualizar_frequencia(index, request.form["frequencia"])
        return redirect("/matriculas")
    except Exception as e:
        return render_template("matriculas/lancar_frequencia.html", 
                               matricula=carregar_matriculas()[index], index=index, erro=str(e))

@matriculas_bp.route("/trancar/<int:index>")
def trancar(index):
    try:
        servico_trancar_matricula(index)
        return redirect("/matriculas")
    except Exception as e:
        return render_template("erro_padrao.html", mensagem=f"Erro: {e}")