from flask import Flask, render_template, request, redirect
from src.persistencia import carregar_cursos, salvar_cursos

app = Flask(__name__)

@app.route("/") # Rota padrão
def index():
    return render_template("index.html") 

@app.route("/cursos") # Rota para listar cursos cadastrados
def cursos():
    lista = carregar_cursos()  # Pega os cursos do JSON com a função de atalho criada
    return render_template("cursos.html", cursos=lista)

@app.route("/cadastrar_curso", methods=["GET", "POST"])
def cadastrar_curso():
    if request.method == "POST": # Se o método for POST o formulário foi enviado
       
        codigo = request.form["codigo"]  # Obtém os dados do formulário enviados pelo usuário
        nome = request.form["nome"]
        ch = request.form["ch"]

        cursos = carregar_cursos()  # Carrega a lista atual de cursos do JSON

        novo = {           # Dicionário representando um novo curso
            "codigo": codigo, 
            "nome": nome,
            "ch": int(ch) }

        cursos.append(novo) # Adiciona o novo curso à lista
        salvar_cursos(cursos) # Atualiza o arquivo JSON com o novo curso

        return redirect("/cursos") # Depois de salvar, redireciona para a lista de cursos

    return render_template("cad_curso.html") # Se for GET, exibe o formulário vazio
if __name__ == "__main__":
    app.run(debug=True)