from flask import Blueprint, render_template, request, redirect
from src.infra.persistencia import carregar_alunos, salvar_alunos
from src.models.aluno import Aluno
from src.services.servicos import servico_criar_aluno

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
   
    try:
        mat_busca = int(matricula)
    except ValueError:
        return redirect("/alunos") # Se não for número, volta

    aluno = next((a for a in alunos if a["matricula"] == mat_busca), None)

    if not aluno: return redirect("/alunos")

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
    try:
        mat_busca = int(matricula) # Converte pra número
    except ValueError:
        return redirect("/alunos")
        
    lista = carregar_alunos()
    # Remove quem tiver o número igual
    nova_lista = [a for a in lista if a["matricula"] != mat_busca]
    
    salvar_alunos(nova_lista)
    return redirect("/alunos")