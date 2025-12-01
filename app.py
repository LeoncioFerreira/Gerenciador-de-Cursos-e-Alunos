from flask import Flask, render_template, request, redirect
from src.persistencia import carregar_cursos, salvar_cursos
from src.curso import Curso

app = Flask(__name__)

@app.route("/") # Rota padrão
def index():
    return render_template("index.html") 

@app.route("/cursos") # Rota para listar cursos cadastrados
def cursos():
    lista = carregar_cursos()  # Pega os cursos do JSON com a função de atalho criada
     # Cria um dicionário para buscar nome por código
    mapa = {c["codigo"]: c["nome"] for c in lista}

    # Constrói lista com nomes dos pré-requisitos
    for c in lista:
        nomes = []
        for cod in c.get("pre_requisitos", []): # Pega os pre_requisitos daquela lista
            nome_pr = mapa.get(cod, "Desconhecido") # Pega o nome do pre_requsitos se não existir vira Desconhecido
            nomes.append(f"{cod} - {nome_pr}") # Adiciona "código - nome" na lista nomes
        c["pre_requisitos_formatado"] = nomes # # Cria a chave pre_requisitos_formatado com a lista código - nome para mostrar no html
    return render_template("cursos.html", cursos=lista)

@app.route("/cadastrar_curso", methods=["GET", "POST"])
def cadastrar_curso():
    if request.method == "POST": # Se o metodo for POST carrega o formulario

        codigo = request.form["codigo"] # Pega o codigo do Html
        nome = request.form["nome"] # Pega o nome do Html

        try:
            carga_horaria = int(request.form["ch"]) # Pega carga horaria como int 
        except ValueError:
            return render_template("cad_curso.html", erro="Carga horária deve ser um número.") # Se não for int retorna o erro

        # Le lista de pre requisitos marcados
        pre_requisitos = request.form.getlist("pre_requisitos") # Pega os pre requisitos do html

        try:
            curso_obj = Curso(codigo, nome, carga_horaria, pre_requisitos) # Transforma os dados do html em um objeto Curso (passa pelos setters)

        except Exception as e:
            lista = carregar_cursos()
            return render_template("cad_curso.html", erro=str(e), cursos=lista)# Se der erro mostra a mensagem gerada pelos setters em curso.py

        novo = { # Cria dicionario do novo curso
            "codigo": curso_obj.codigo,
            "nome": curso_obj.nome,
            "carga_horaria": curso_obj.carga_horaria,
            "pre_requisitos": curso_obj.pre_requisitos
        }

        cursos = carregar_cursos()  
        cursos.append(novo) # Adiciona o novo curso no formato do dicionario criado
        salvar_cursos(cursos) # Salva a lista de cursos usando a função auxiliar de persistência

        return redirect("/cursos")

    # Manda lista de cursos para seleção
    lista = carregar_cursos()
    return render_template("cad_curso.html", cursos=lista)

if __name__ == "__main__":
    app.run(debug=True)