from flask import Blueprint, render_template, request, redirect
from src.persistencia import carregar_cursos, salvar_cursos
from src.curso import Curso

cursos_bp = Blueprint("cursos", __name__)

@cursos_bp.route("/") # Rota para listar cursos listados
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
        c["pre_requisitos_formatado"] = nomes # Cria a chave pre_requisitos_formatado com a lista código - nome para mostrar no html
    return render_template("cursos/cursos.html", cursos=lista)

# Cadastra Curso
@cursos_bp.route("/cadastrar_curso", methods=["GET", "POST"])
def cadastrar_curso():
    if request.method == "POST": # Se o metodo for POST carrega o formulario

        codigo = request.form["codigo"] # Pega o codigo do Html
        nome = request.form["nome"] # Pega o nome do Html

        try:
            carga_horaria = int(request.form["ch"]) # Pega carga horaria como int 
        except ValueError:
            return render_template("cursos/cad_curso.html", erro="Carga horária deve ser um número.") # Se não for int retorna o erro

        # Le lista de pre requisitos marcados
        pre_requisitos = request.form.getlist("pre_requisitos") # Pega os pre requisitos do html

        try:
            curso_obj = Curso(codigo, nome, carga_horaria, pre_requisitos) # Transforma os dados do html em um objeto Curso (passa pelos setters)

        except Exception as e:
            lista = carregar_cursos()
            return render_template("cursos/cad_curso.html", erro=str(e), cursos=lista)# Se der erro mostra a mensagem gerada pelos setters em curso.py

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
    return render_template("cursos/cad_curso.html", cursos=lista)

# Edita Curso
@cursos_bp.route("/editar/<codigo>", methods=["GET", "POST"])

def editar_curso(codigo):
    cursos = carregar_cursos()
    # Busca o curso pelo código (dicionário)
    curso_dict = next((c for c in cursos if c["codigo"] == codigo), None)
    
    if curso_dict is None:
        return redirect("/cursos")

    if request.method == "POST":
        nome = request.form["nome"]
        
        try:
            ch = int(request.form["ch"])
        except ValueError:
             return render_template("cursos/editar_curso.html", 
                                    curso=curso_dict, 
                                    cursos=cursos, 
                                    erro="Carga horária deve ser um número.")

        prereqs = request.form.getlist("pre_requisitos")

        try:
            # 1. Instancia um objeto temporário para acionar as validações da classe
            # Usamos o código original para manter a consistência
            temp_obj = Curso(codigo, nome, ch, prereqs)
            
            # 2. Se não deu erro, atualizamos o dicionário com os dados validados
            curso_dict["nome"] = temp_obj.nome
            curso_dict["carga_horaria"] = temp_obj.carga_horaria
            curso_dict["pre_requisitos"] = temp_obj.pre_requisitos
            
            salvar_cursos(cursos)
            return redirect("/cursos")
            
        except Exception as e:
            # Se a classe Curso lançar erro (ex: carga negativa), capturamos aqui
            return render_template("cursos/editar_curso.html", 
                                   curso=curso_dict, 
                                   cursos=cursos, 
                                   erro=str(e))

    return render_template("cursos/editar_curso.html", curso=curso_dict, cursos=cursos)