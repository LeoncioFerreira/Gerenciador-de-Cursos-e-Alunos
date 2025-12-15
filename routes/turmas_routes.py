from flask import Blueprint, render_template, request, redirect
from src.infra.persistencia import carregar_cursos, carregar_turmas, salvar_turmas
from src.models.turma import Turma
from src.models.curso import Curso
from src.services.turma_service import servico_criar_turma
from src.models.curso import Curso

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
        f = request.form 
            
        try:
            # 1. Tenta converter para inteiro (pode falhar se o usuário digitar texto)
            vagas_int = int(f["vagas"])
            
            # 2. Cria o curso fake apenas para satisfazer o construtor
            curso_fake = Curso("X", "X", 10, []) 

            # 3. Cria a Turma temporária. 
            # SE vagas for negativo ou semestre vazio, a classe Turma lança ValueError AQUI.
            temp_turma = Turma(
                codigo_oferta=codigo_oferta,
                curso=curso_fake,
                semestre=f["semestre"],
                dias_horarios={f["dia"]: [[f["inicio"], f["fim"]]]},
                vagas=vagas_int, 
                local=f.get("local", "")
            )

            # 4. Se chegou aqui, os dados são válidos. Atualizamos o dicionário.
            turma.update({
                "semestre": temp_turma.semestre,
                "codigo_curso": f["codigo_curso"], # Mantemos o ID original do curso
                "vagas": temp_turma.vagas,
                "local": temp_turma.local,
                "dias_horarios": temp_turma.dias_horarios
            })
            
            salvar_turmas(turmas)
            return redirect("/turmas")
            
        except ValueError as e:
            # Captura tanto erro de conversão (int) quanto erro de validação da classe Turma
            return render_template("turmas/editar_turma.html", 
                                turma=turma, 
                                cursos=carregar_cursos(), 
                                erro=str(e)) # Mostra a mensagem real (ex: "Vagas devem ser positivas")

    # Retorno do GET
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