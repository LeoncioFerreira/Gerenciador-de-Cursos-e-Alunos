from flask import Blueprint, render_template, request, redirect
from src.infra.persistencia import carregar_cursos, salvar_cursos
from src.models.curso import Curso
from src.services.curso_service import servico_criar_curso
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
@cursos_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_curso():
    if request.method == "POST":
        try:
            # Pega os dados do formulário
            codigo = request.form["codigo"]
            nome = request.form["nome"]
            ch = request.form["ch"]
            pre_requisitos = request.form.getlist("pre_requisitos")

            # --- AQUI ESTÁ A MUDANÇA ---
            # Chamamos o serviço. Se o código já existir, ele lança ValueError
            servico_criar_curso(codigo, nome, ch, pre_requisitos)
            
            return redirect("/cursos")

        except Exception as e:
            # Se der erro (código duplicado ou carga horária inválida), volta pro form
            lista = carregar_cursos()
            return render_template("cursos/cad_curso.html", erro=str(e), cursos=lista)

    # GET: Exibe formulário
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
            # Instancia um objeto temporário para acionar as validações da classe
            # Usamos o código original para manter a consistência
            temp_obj = Curso(codigo, nome, ch, prereqs)
            
            # Se não deu erro, atualizamos o dicionário com os dados validados
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

# Remover Curso
@cursos_bp.route("/remover/<codigo>", methods=["GET"])
def remover_curso(codigo):
    cursos = carregar_cursos()

    # Filtra cursos mantendo todos menos o removido
    nova_lista = [c for c in cursos if c["codigo"] != codigo]

    # Se nada foi removido, apenas volta para a lista
    if len(nova_lista) == len(cursos):
        return redirect("/cursos")

    # Salva nova lista sem o curso removido
    salvar_cursos(nova_lista)

    return redirect("/cursos")