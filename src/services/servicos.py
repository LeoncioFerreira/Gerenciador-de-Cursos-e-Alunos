from src.infra.persistencia import (
    carregar_alunos, carregar_turmas, carregar_cursos, carregar_matriculas,
    salvar_alunos, salvar_matriculas, salvar_cursos, salvar_turmas
)
from src.models.aluno import Aluno
from src.models.turma import Turma
from src.models.curso import Curso
from src.models.matricula import Matricula

# Funções Auxiliares

def buscar_objeto(lista, chave, valor, msg_erro="Objeto não encontrado"):
    # Busca item na lista comparando como string para evitar erro de tipo
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
    # Reconstroi Matrícula usando métodos públicos
    aluno = get_aluno_obj(dado_dict["aluno"])
    turma = get_turma_obj(dado_dict["turma"])
    m = Matricula(aluno, turma)
    
    if dado_dict["nota"] is not None:
        m.lancar_nota(dado_dict["nota"])
        
    if dado_dict["frequencia"] is not None:
        m.lancar_frequencia(dado_dict["frequencia"])
    
    m.status = dado_dict["status"]
    return m

# Serviços de cadastro

def servico_criar_aluno(nome, email, matricula):
    lista_alunos = carregar_alunos()

    # Valida a nova matricula se do tipo int
    try:
        nova_matricula = int(matricula)
    except ValueError:
        raise ValueError("A matrícula deve ser um número válido!")

    # Valida duplicidade
    for a in lista_alunos:
        if a["matricula"] == nova_matricula:
            raise ValueError(f"Erro: A matrícula {nova_matricula} já está cadastrada!")

    obj = Aluno(nome, email, str(nova_matricula))
    
    lista_alunos.append({
        "matricula": nova_matricula, 
        "nome": obj.nome, 
        "email": obj.email
    })
    salvar_alunos(lista_alunos)

def servico_criar_curso(codigo, nome, ch, pre_reqs):
    lista_cursos = carregar_cursos()
    
    # Verifica duplicidade convertendo para string
    if any(str(c['codigo']) == str(codigo) for c in lista_cursos):
         raise ValueError(f"Erro: O código de curso {codigo} já existe!")

    obj = Curso(codigo, nome, int(ch), pre_reqs)
    
    lista_cursos.append({
        "codigo": obj.codigo, "nome": obj.nome, 
        "carga_horaria": obj.carga_horaria, "pre_requisitos": obj.pre_requisitos
    })
    salvar_cursos(lista_cursos)

def servico_criar_turma(cod_oferta, cod_curso, semestre, vagas, dia, inicio, fim, local):
    lista_turmas = carregar_turmas()
    
    # Valida Unicidade 
    if any(str(t['codigo_oferta']) == str(cod_oferta) for t in lista_turmas):
        raise ValueError(f"Erro: O código de oferta {cod_oferta} já existe!")

    # Busca o Curso e necessário para criar o objeto Turma
    from src.infra.persistencia import carregar_cursos
    cursos = carregar_cursos()
    dado_curso = next((c for c in cursos if str(c["codigo"]) == str(cod_curso)), None)
    
    if not dado_curso:
        raise ValueError("Curso não encontrado.")
    
    # Recria o objeto curso apenas para passar para a turma
    obj_curso = Curso(dado_curso["codigo"], dado_curso["nome"], dado_curso["carga_horaria"], [])
    

    # Ao instanciar a Turma, os SETTERS da classe são acionados.
    # Se o semestre for vazio (""), a classe Oferta/Turma vai lançar ValueError aqui mesmo
    nova_turma = Turma(
        codigo_oferta=cod_oferta,
        curso=obj_curso,
        semestre=semestre, # O setter da classe vai validar isso
        dias_horarios={dia: [[inicio, fim]]},
        vagas=int(vagas),
        local=local
    )

    # Se chegou aqui, é porque os dados são válidos
    # Salvamos no JSON
    lista_turmas.append({
        "codigo_oferta": nova_turma.codigo_oferta, 
        "codigo_curso": nova_turma.codigo_curso, 
        "semestre": nova_turma.semestre, 
        "dias_horarios": nova_turma.dias_horarios, 
        "vagas": nova_turma.vagas, 
        "status": nova_turma.status, 
        "local": nova_turma.local
    })
    salvar_turmas(lista_turmas)

# Serviços relacionados a matricula 

def servico_criar_matricula(mat_aluno, cod_turma):
    lista_matriculas = carregar_matriculas()
    
    # Valida Duplicidade
    for m in lista_matriculas:
        if str(m["aluno"]) == str(mat_aluno) and str(m["turma"]) == str(cod_turma):
            if m["status"] != "TRANCADA":
                raise ValueError(f"O aluno {mat_aluno} já está matriculado nesta turma!")

    aluno = get_aluno_obj(mat_aluno)
    turma = get_turma_obj(cod_turma)

    # Carrega histórico para  validar pre-requisitos
    # Carrega matrículas passadas (APROVADO) para saber o que ele já fez
    historico_aluno = [
        m for m in lista_matriculas 
        if str(m["aluno"]) == str(mat_aluno) and m["status"] == "APROVADO"
    ]
    
    for dados in historico_aluno:
        try:
            # Recria a matrícula antiga e adiciona ao histórico do objeto aluno
            t_antiga = get_turma_obj(dados["turma"])
            m_antiga = Matricula(aluno, t_antiga)
            m_antiga.lancar_nota(dados["nota"]) # Importante: nota define aprovação
            aluno.adicionar_ao_historico(m_antiga)
        except: continue # Ignora se der erro em dados antigos

    # Validar os pre requisitos
    # O objeto turma.curso tem a lista de códigos necessários
    for pre_req in turma.curso.pre_requisitos:
        # O método .aprovou() do aluno verifica o histórico que acabamos de carregar
        if not aluno.aprovou(pre_req):
            raise ValueError(f"Requisito não atendido: O aluno precisa ter sido aprovado no curso {pre_req}.")


    # Carrrega grade atual para validar choque de horario
    matriculas_ativas = [
        m for m in lista_matriculas 
        if str(m["aluno"]) == str(mat_aluno) and m["status"] == "ATIVA"
    ]
    for dados in matriculas_ativas:
        try:
            t_atual = get_turma_obj(dados["turma"])
            m_atual = Matricula(aluno, t_atual)
            aluno.adicionar_matricula_ativa(m_atual)
        except: continue

    if aluno.tem_choque(turma):
         raise ValueError("Choque de horário! O aluno já tem aula neste intervalo.")

    # Carrega ocupação e Valida Vagas
    ocupacao_atual = [
        m for m in lista_matriculas 
        if str(m["turma"]) == str(cod_turma) and m["status"] in ["ATIVA", "APROVADO"]
    ]
    
    if hasattr(turma, 'inicializar_matriculas'):
        turma.inicializar_matriculas(ocupacao_atual)
    else:
        turma._Turma__matriculas = ocupacao_atual

    # Cria matrícula final
    nova_matricula = Matricula(aluno, turma)
    turma.adicionar_matricula(nova_matricula) 
    
    # Salva
    lista_matriculas.append({
        "aluno": aluno.matricula, "turma": turma.codigo_oferta,
        "nota": None, "frequencia": None, "status": "ATIVA"
    })
    salvar_matriculas(lista_matriculas)

# Serviço para atualizar/lançar

def servico_atualizar_nota(index, valor_nota):
    lista = carregar_matriculas()
    dado = lista[index]

    if dado["status"] == "TRANCADA":
        raise ValueError("Matrícula trancada!")

    obj = recriar_matricula(dado)
    obj.lancar_nota(valor_nota) 
    
    dado["nota"] = obj.nota
    dado["status"] = obj.situacao()
    salvar_matriculas(lista)

def servico_atualizar_frequencia(index, valor_freq):
    lista = carregar_matriculas()
    dado = lista[index]

    if dado["status"] == "TRANCADA":
        raise ValueError("Matrícula trancada!")

    obj = recriar_matricula(dado)
    obj.lancar_frequencia(valor_freq)
    
    dado["frequencia"] = obj.frequencia
    dado["status"] = obj.situacao()
    salvar_matriculas(lista)

def servico_trancar_matricula(index):
    lista = carregar_matriculas()
    dado = lista[index]
    
    obj = recriar_matricula(dado)
    obj.trancar()
    
    dado["status"] = obj.status
    salvar_matriculas(lista)