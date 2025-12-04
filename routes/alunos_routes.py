from flask import Blueprint, render_template, request, redirect
from src.persistencia import carregar_alunos, salvar_alunos
from src.aluno import Aluno

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
            obj = Aluno(nome, email, matricula)  # valida via classe Aluno
        except Exception as e:
            return render_template("alunos/cad_aluno.html", erro=str(e))

        novo = {
            "matricula": obj.matricula,
            "nome": obj.nome,
            "email": obj.email
        }

        alunos = carregar_alunos()
        alunos.append(novo)
        salvar_alunos(alunos)

        return redirect("/alunos")

    return render_template("alunos/cad_aluno.html")

# Edita aluno
@alunos_bp.route("/editar/<matricula>", methods=["GET", "POST"])
def editar_aluno(matricula):
    alunos = carregar_alunos()
    aluno = next((a for a in alunos if a["matricula"] == matricula), None)

    if not aluno:
        return redirect("/alunos")

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]

        try:
            temp = Aluno(nome, email, matricula)
        except Exception as e:
            return render_template("alunos/editar_aluno.html",
                                   aluno=aluno, erro=str(e))

        aluno["nome"] = temp.nome
        aluno["email"] = temp.email

        salvar_alunos(alunos)
        return redirect("/alunos")

    return render_template("alunos/editar_aluno.html", aluno=aluno)

# Remove aluno
@alunos_bp.route("/remover/<matricula>")
def remover_aluno(matricula):
    lista = carregar_alunos()
    nova_lista = [a for a in lista if a["matricula"] != matricula]
    salvar_alunos(nova_lista)
    return redirect("/alunos")
