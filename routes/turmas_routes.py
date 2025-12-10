from flask import Blueprint, render_template, request, redirect
from src.infra.persistencia import carregar_cursos, carregar_turmas, salvar_turmas
from src.models.turma import Turma
from src.models.curso import Curso

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
    cursos = carregar_cursos()

    if request.method == "POST":
        try:
            f = request.form # simplificando request
            
            # 1. Busca o curso selecionado para validação
            dados_curso = next((c for c in cursos if c["codigo"] == f["codigo_curso"]), None)
            if not dados_curso: raise ValueError("Curso não encontrado.")

            # Instancia objetos APENAS para validar as regras de negócio
            # Usa o Curso do módulo curso.py para validar os dados do curso
            obj_curso = Curso(**dados_curso)
            
            # Usa a turma do módulo turma.py para validar atributos de turma
            nova_turma = Turma(
                codigo_oferta=f["codigo_oferta"].strip(),
                curso=obj_curso,
                semestre=f["semestre"].strip(),
                dias_horarios={f["dia"]: [[f["inicio"], f["fim"]]]},
                vagas=int(f["vagas"]),
                local=f.get("local", "").strip()
            )

            # Persistência: Constrói o dict final para salvar no JSON
            # (Já validado pelos objetos acima)
            nova_turma_dict = {
                "codigo_oferta": nova_turma.codigo_oferta,
                "codigo_curso": nova_turma.codigo_curso,
                "semestre": nova_turma.semestre,
                "dias_horarios": nova_turma.dias_horarios,
                "vagas": nova_turma.vagas,
                "status": nova_turma.status,
                "local": nova_turma.local,
            }

            turmas = carregar_turmas()
            turmas.append(nova_turma_dict)
            salvar_turmas(turmas)
            
            return redirect("/turmas")

        except Exception as e:
            return render_template("turmas/cad_turma.html", cursos=cursos, erro=str(e))

    return render_template("turmas/cad_turma.html", cursos=cursos)

@turmas_bp.route("/editar/<codigo_oferta>", methods=["GET", "POST"])
def editar_turma(codigo_oferta):
    turmas = carregar_turmas()
    turma = next((t for t in turmas if t["codigo_oferta"] == codigo_oferta), None)
    
    if not turma: return "Turma não encontrada", 404

    if request.method == "POST":
        f = request.form
        # Atualiza os dados diretamente no dicionário
        turma.update({
            "semestre": f["semestre"],
            "codigo_curso": f["codigo_curso"],
            "vagas": int(f["vagas"]),
            "local": f.get("local", ""),
            "dias_horarios": {f["dia"]: [[f["inicio"], f["fim"]]]}
        })
        salvar_turmas(turmas)
        return redirect("/turmas")

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