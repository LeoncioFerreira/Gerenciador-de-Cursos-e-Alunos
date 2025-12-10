from flask import Blueprint, render_template, request, redirect
from src.infra.persistencia import carregar_cursos, carregar_turmas, salvar_turmas
from src.models.turma import Turma
from src.models.curso import Curso
from src.services.servicos import servico_criar_turma

turmas_bp = Blueprint("turmas", __name__)

@turmas_bp.route("/")
def listar_turmas():
    turmas = carregar_turmas()
    # Cria dicionario com codigo: nome para acesso rápido 
    mapa_cursos = {c["codigo"]: c["nome"] for c in carregar_cursos()}

    # Adiciona o nome do curso para exibição (apenas visualização)
    for t in turmas:
        t["nome_curso"] = mapa_cursos.get(t["codigo_curso"], "Desconhecido")

    return render_template("turmas/turmas.html", turmas=turmas)

@turmas_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_turma():
    if request.method == "POST":
        try:
            f = request.form
            # --- CORREÇÃO AQUI ---
            # Delega tudo para o serviço. Ele valida unicidade e existência do curso.
            servico_criar_turma(
                cod_oferta=f["codigo_oferta"],
                cod_curso=f["codigo_curso"],
                semestre=f["semestre"],
                vagas=f["vagas"],
                dia=f["dia"],
                inicio=f["inicio"],
                fim=f["fim"],
                local=f.get("local", "")
            )
            return redirect("/turmas")

        except Exception as e:
            return render_template("turmas/cad_turma.html", cursos=carregar_cursos(), erro=str(e))

    return render_template("turmas/cad_turma.html", cursos=carregar_cursos())

@turmas_bp.route("/editar/<codigo_oferta>", methods=["GET", "POST"])
def editar_turma(codigo_oferta):
    turmas = carregar_turmas()
    turma = next((t for t in turmas if t["codigo_oferta"] == codigo_oferta), None)
    
    if not turma: return "Turma não encontrada", 404

    if request.method == "POST":
        f = request.form # simplificando request
            
        try:
                # Tenta converter e guarda na variável
                vagas_int = int(f["vagas"])
                
                # Atualiza os dados (observe que o alinhamento é igual ao da linha de cima)
                turma.update({
                    "semestre": f["semestre"],
                    "codigo_curso": f["codigo_curso"],
                    "vagas": vagas_int, # USA A VARIÁVEL JÁ CONVERTIDA AQUI
                    "local": f.get("local", ""),
                    "dias_horarios": {f["dia"]: [[f["inicio"], f["fim"]]]}
                })
                
                salvar_turmas(turmas)
                return redirect("/turmas")
            
        except ValueError:
                return render_template("turmas/editar_turma.html", 
                                    turma=turma, 
                                    cursos=carregar_cursos(), 
                                    erro="O campo 'Vagas' deve ser um número inteiro.")

# Retorno do get(fora do if/else do POST)
    return render_template("turmas/editar_turma.html", turma=turma, cursos=carregar_cursos())

@turmas_bp.route("/excluir/<codigo_oferta>")
def excluir_turma(codigo_oferta):
    # Filtra removendo o item desejado e salva a nova lista
    lista_atualizada = [t for t in carregar_turmas() if t["codigo_oferta"] != codigo_oferta]
    salvar_turmas(lista_atualizada)
    return redirect("/turmas")

# Rota unificada para alterar status (ABERTA/FECHADA)
@turmas_bp.route("/status/<codigo_oferta>/<acao>")
def alterar_status(codigo_oferta, acao):
    acao = acao.upper()
    # Validação simples baseada no que a classe Oferta permite
    if acao not in ["ABERTA", "FECHADA"]:
        return redirect("/turmas")
        
    turmas = carregar_turmas()
    for t in turmas:
        if t["codigo_oferta"] == codigo_oferta:
            t["status"] = acao
            break
            
    salvar_turmas(turmas)
    return redirect("/turmas")