from flask import Blueprint, render_template, request, redirect
from src.infra.persistencia import carregar_alunos, salvar_alunos
from src.models.aluno import Aluno
from src.services.aluno_service import servico_criar_aluno
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

alunos_bp = Blueprint("alunos", __name__)
# Lista alunoa
@alunos_bp.route("/")
def alunos():
    lista = carregar_alunos()
    return render_template("alunos/alunos.html", alunos=lista)

# Cadastra aluno
@alunos_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_aluno():
    if request.method == "POST":
        matricula = request.form["matricula"]
        nome = request.form["nome"]
        email = request.form["email"]

        try:
            servico_criar_aluno(nome, email, matricula)
            
            return redirect("/alunos")

        except ValueError as e:
            return render_template("alunos/cad_aluno.html", erro=str(e))
        

    return render_template("alunos/cad_aluno.html")

# Edita aluno
@alunos_bp.route("/editar/<matricula>", methods=["GET", "POST"])
def editar_aluno(matricula):
    alunos = carregar_alunos()
    # Assim ele acha o aluno sendo número ou texto no JSON.
    aluno = next((a for a in alunos if str(a["matricula"]) == str(matricula)), None)

    # Se ainda assim não achar, imprime no terminal para sabermos o motivo
    if not aluno: 
        print(f"ERRO: Aluno com matrícula '{matricula}' não encontrado na lista.")
        return redirect("/alunos")
    if request.method == "POST":
        try:
            temp = Aluno(request.form["nome"], request.form["email"], str(matricula))
            aluno["nome"] = temp.nome
            aluno["email"] = temp.email
            salvar_alunos(alunos)
            return redirect("/alunos")
        except Exception as e:
            return render_template("alunos/editar_aluno.html", aluno=aluno, erro=str(e))

    return render_template("alunos/editar_aluno.html", aluno=aluno)

# Remove aluno
@alunos_bp.route("/remover/<matricula>")
def remover_aluno(matricula):
    lista_alunos = carregar_alunos()
    # Convertemos tudo para STRING antes de comparar.
    # Filtramos a lista mantendo apenas quem tem matrícula DIFERENTE da que queremos apagar.
    nova_lista = [a for a in lista_alunos if str(a["matricula"]) != str(matricula)]
    
    # Se o tamanho da lista não mudou, significa que não achou ninguém
    if len(nova_lista) == len(lista_alunos):
        print(f"Aviso: Ninguém foi removido. Matrícula {matricula} não encontrada.")
    
    salvar_alunos(nova_lista)
    return redirect("/alunos")