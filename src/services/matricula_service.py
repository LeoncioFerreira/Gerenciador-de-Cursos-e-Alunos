from src.infra.persistencia import (
    carregar_alunos, carregar_turmas, carregar_cursos, carregar_matriculas, salvar_matriculas
)
from src.models.aluno import Aluno
from src.models.turma import Turma
from src.models.curso import Curso
from src.models.matricula import Matricula
from src.services.sistema import (
    matricular, 
    TurmaLotadaError, 
    ChoqueHorarioError, 
    PreRequisitoError, 
    TurmaFechadaError
)

"""
Serviços de Matrícula

Responsabilidade:
- Coordenar o processo de matrícula.
- Reconstruir objetos a partir da persistência.
- Delegar regras complexas ao módulo sistema.
- Atualizar nota, frequência e status da matrícula.

Este módulo atua como ponte entre a interface
e o núcleo de regras de negócio.
"""

# Funções Auxiliares
def buscar_objeto(lista, chave, valor, msg_erro="Objeto não encontrado"):
    item = next((i for i in lista if str(i[chave]) == str(valor)), None)
    if not item: raise ValueError(msg_erro)
    return item

def get_aluno_obj(mat):
    dado = buscar_objeto(carregar_alunos(), "matricula", mat, f"Aluno {mat} não encontrado")
    return Aluno(dado["nome"], dado["email"], str(dado["matricula"]))

def get_turma_obj(cod_oferta):
    dado_t = buscar_objeto(carregar_turmas(), "codigo_oferta", cod_oferta, f"Turma {cod_oferta} não encontrada")
    dado_c = buscar_objeto(carregar_cursos(), "codigo", dado_t["codigo_curso"], "Curso não encontrado")
    
    curso = Curso(dado_c["codigo"], dado_c["nome"], dado_c["carga_horaria"], dado_c.get("pre_requisitos", []))
    
    turma = Turma(dado_t["codigo_oferta"], curso, dado_t["semestre"], dado_t["dias_horarios"], 
                  dado_t["vagas"], dado_t["status"], dado_t.get("local", ""))
    return turma

def recriar_matricula(dado_dict):
    aluno = get_aluno_obj(dado_dict["aluno"])
    turma = get_turma_obj(dado_dict["turma"])
    m = Matricula(aluno, turma)
    
    if dado_dict["nota"] is not None:
        m.lancar_nota(dado_dict["nota"])
        
    if dado_dict["frequencia"] is not None:
        m.lancar_frequencia(dado_dict["frequencia"])
    
    m.status = dado_dict["status"]
    return m

# Serviços

def servico_criar_matricula(mat_aluno, cod_turma):
    lista_matriculas = carregar_matriculas()
    
    # Validação rápida de duplicidade no json
    for m in lista_matriculas:
        if str(m["aluno"]) == str(mat_aluno) and str(m["turma"]) == str(cod_turma):
            if m["status"] != "TRANCADA":
                raise ValueError(f"O aluno {mat_aluno} já está matriculado nesta turma!")

    # Instancia os objetos base
    aluno = get_aluno_obj(mat_aluno)
    turma = get_turma_obj(cod_turma)

    # Popula o ALUNO com Histórico (Para validar pré-requisitos)
    dados_historico = [m for m in lista_matriculas if str(m["aluno"]) == str(mat_aluno) and m["status"] == "APROVADO"]
    for d in dados_historico:
        try:
            aluno.adicionar_ao_historico(recriar_matricula(d))
        except: continue 

    # Popula o ALUNO com Grade Ativa (Para validar choque de horário)
    dados_ativas = [m for m in lista_matriculas if str(m["aluno"]) == str(mat_aluno) and m["status"] == "ATIVA"]
    for d in dados_ativas:
        try:
            aluno.adicionar_matricula_ativa(recriar_matricula(d))
        except: continue

    #  Popula a TURMA com Ocupação (Para validar Vagas)
    ocupacao_dicts = [m for m in lista_matriculas if str(m["turma"]) == str(cod_turma) and m["status"] in ["ATIVA", "APROVADO"]]
    ocupacao_objs = []
    for d in ocupacao_dicts:
        try:
            ocupacao_objs.append(recriar_matricula(d))
        except: continue
        
    # Injeta a lista de ocupação na turma
    turma.inicializar_matriculas(ocupacao_objs)

    # Tenta matricula 
    try:
        nova_matricula = matricular(aluno, turma)
        
    except (TurmaLotadaError, ChoqueHorarioError, PreRequisitoError, TurmaFechadaError) as e:
        # Captura os erros de domínio e transforma em erro de valor para o Flask exibir
        raise ValueError(str(e))
    except ValueError as e:
        # Repassa erros genéricos (ex: aluno duplicado na lista interna da turma)
        raise e

    # Se passou, salva no JSON
    lista_matriculas.append({
        "aluno": nova_matricula.aluno.matricula, 
        "turma": nova_matricula.turma.codigo_oferta,
        "nota": None, 
        "frequencia": None, 
        "status": "ATIVA"
    })
    salvar_matriculas(lista_matriculas)

# Serviços para atualizar_nota, atualizar_frequencia e trancar 
def servico_atualizar_nota(index, valor_nota):
    lista = carregar_matriculas()
    try: dado = lista[index]
    except IndexError: raise ValueError("Matrícula não encontrada.")
    if dado["status"] == "TRANCADA": raise ValueError("Matrícula trancada!")
    obj = recriar_matricula(dado)
    obj.lancar_nota(valor_nota) 
    dado["nota"] = obj.nota
    dado["status"] = obj.situacao()
    salvar_matriculas(lista)

def servico_atualizar_frequencia(index, valor_freq):
    lista = carregar_matriculas()
    try: dado = lista[index]
    except IndexError: raise ValueError("Matrícula não encontrada.")
    if dado["status"] == "TRANCADA": raise ValueError("Matrícula trancada!")
    obj = recriar_matricula(dado)
    obj.lancar_frequencia(valor_freq)
    dado["frequencia"] = obj.frequencia
    dado["status"] = obj.situacao()
    salvar_matriculas(lista)

def servico_trancar_matricula(index):
    lista = carregar_matriculas()
    try: dado = lista[index]
    except IndexError: raise ValueError("Matrícula não encontrada.")
    obj = recriar_matricula(dado)
    obj.trancar()
    dado["status"] = obj.status
    salvar_matriculas(lista)