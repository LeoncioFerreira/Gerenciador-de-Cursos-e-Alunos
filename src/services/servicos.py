# src/services/servicos.py
from src.infra.persistencia import carregar_alunos, carregar_turmas, carregar_cursos, carregar_matriculas,salvar_alunos, salvar_matriculas,salvar_cursos,salvar_turmas
from src.models.aluno import Aluno
from src.models.turma import Turma
from src.models.curso import Curso
from src.models.matricula import Matricula
from src.services.sistema import matricular

# Funções Auxiliares

def buscar_objeto(lista, chave, valor, msg_erro):
    # Busca genérica em lista de dicionários
    item = next((i for i in lista if i[chave] == valor), None)
    if not item: raise ValueError(msg_erro)
    return item

def get_aluno_obj(mat):
    dado = buscar_objeto(carregar_alunos(), "matricula", mat, "Aluno não encontrado")
    return Aluno(dado["nome"], dado["email"], dado["matricula"])

def get_turma_obj(cod_oferta):
    dado_t = buscar_objeto(carregar_turmas(), "codigo_oferta", cod_oferta, "Turma não encontrada")
    dado_c = buscar_objeto(carregar_cursos(), "codigo", dado_t["codigo_curso"], "Curso não encontrado")
    
    # Recria Curso e Turma
    curso = Curso(dado_c["codigo"], dado_c["nome"], dado_c["carga_horaria"], dado_c.get("pre_requisitos", []))
    return Turma(dado_t["codigo_oferta"], curso, dado_t["semestre"], dado_t["dias_horarios"], 
                 dado_t["vagas"], dado_t["status"], dado_t.get("local", ""))

def recriar_matricula(dado_dict):
    # Reconstroi o objeto Matrícula completo com dados do json
    aluno = get_aluno_obj(dado_dict["aluno"])
    turma = get_turma_obj(dado_dict["turma"])
    m = Matricula(aluno, turma)
    
    # Restaura estado anterior (bypassando setters se necessário para carga inicial)
    m._Matricula__nota = dado_dict["nota"]
    m._Matricula__frequencia = dado_dict["frequencia"]
    m.status = dado_dict["status"]
    return m

# Serviços Principais (Chamados pelas Rotas) 

# Em src/services/servicos.py

def servico_criar_matricula(mat_aluno, cod_turma):
    # Carrega dados
    lista_matriculas = carregar_matriculas()
    
    # Valida duplicidade
    for m in lista_matriculas:
        if m["aluno"] == mat_aluno and m["turma"] == cod_turma:
            if m["status"] != "TRANCADA":
                raise ValueError(f"O aluno {mat_aluno} já está matriculado na turma {cod_turma}!")

    # Instancia os objetos
    aluno = get_aluno_obj(mat_aluno)
    turma = get_turma_obj(cod_turma) # Turma vem vazia aqui

    # Preenche a turma com as vagas reais do json
    ocupacao_atual = [
        m for m in lista_matriculas 
        if m["turma"] == cod_turma and m["status"] in ["ATIVA", "APROVADO"]
    ]
    # Injeta a lista diretamente na classe para o len() funcionar
    turma.matriculas = ocupacao_atual 

    # CHECK DE VAGAS
    if not turma.tem_vaga():
         raise ValueError(f"A turma {turma.codigo_oferta} está lotada! ({len(turma)}/{turma.vagas} vagas)")

    # Cria a Nova Matrícula
    nova_matricula = Matricula(aluno, turma)

    # Chamamos o método da classe para adicionar matricula:
    turma.adicionar_matricula(nova_matricula) 
    
    # Salva
    lista_matriculas.append({
        "aluno": aluno.matricula, 
        "turma": turma.codigo_oferta,
        "nota": None, 
        "frequencia": None, 
        "status": "ATIVA"
    })
    salvar_matriculas(lista_matriculas)

def servico_atualizar_nota(index, valor_nota):
    lista = carregar_matriculas()
    dado = lista[index]

    if dado["status"] == "TRANCADA":
        raise ValueError("Matrícula trancada!")

    obj = recriar_matricula(dado)
    obj.nota = float(valor_nota) # Valida 0-10
    
    dado["nota"] = obj.nota
    dado["status"] = obj.situacao() # Recalcula status
    salvar_matriculas(lista)

def servico_atualizar_frequencia(index, valor_freq):
    lista = carregar_matriculas()
    dado = lista[index]

    if dado["status"] == "TRANCADA":
        raise ValueError("Matrícula trancada!")

    obj = recriar_matricula(dado)
    obj.frequencia = float(valor_freq) # Valida 0-100
    
    dado["frequencia"] = obj.frequencia
    dado["status"] = obj.situacao() # Recalcula status
    salvar_matriculas(lista)

def servico_trancar_matricula(index):
    lista = carregar_matriculas()
    dado = lista[index]
    
    obj = recriar_matricula(dado)
    obj.trancar() # Valida data limite
    
    dado["status"] = obj.status
    salvar_matriculas(lista)

def servico_criar_aluno(nome, email, matricula):
    lista_alunos = carregar_alunos()

# Regra de unicidade
    # Regra de unicidade:(Aluno)
    # Verifica se já existe alguém com essa matrícula na lista
    for a in lista_alunos:
        if a["matricula"] == matricula:
            raise ValueError(f"Erro: A matrícula {matricula} já está cadastrada!")

    # Se passou, cria e salva
    obj = Aluno(nome, email, matricula)
    novo_dict = {"matricula": obj.matricula, "nome": obj.nome, "email": obj.email}
    
    lista_alunos.append(novo_dict)
    salvar_alunos(lista_alunos)

def servico_criar_curso(codigo, nome, ch, pre_reqs):
    lista_cursos = carregar_cursos()

    # Regra de unicidade:(Curso)
    for c in lista_cursos:
        if c["codigo"] == codigo:
             raise ValueError(f"Erro: O código de curso {codigo} já existe!")

    obj = Curso(codigo, nome, int(ch), pre_reqs)
    
    novo_dict = {
        "codigo": obj.codigo, 
        "nome": obj.nome, 
        "carga_horaria": obj.carga_horaria, 
        "pre_requisitos": obj.pre_requisitos
    }
    
    lista_cursos.append(novo_dict)
    salvar_cursos(lista_cursos)

def servico_criar_turma(cod_oferta, cod_curso, semestre, vagas, dia, inicio, fim, local):
    lista_turmas = carregar_turmas()
    
    # Regra de unicidade:(Curso/Oferta)
    for t in lista_turmas:
        if t["codigo_oferta"] == cod_oferta:
            raise ValueError(f"Erro: O código de oferta {cod_oferta} já existe!")

    # Precisamos validar se o curso existe antes de criar a turma
    # (Aqui você pode usar aquela função buscar_objeto ou fazer direto)
    from src.infra.persistencia import carregar_cursos
    cursos = carregar_cursos()
    dado_curso = next((c for c in cursos if c["codigo"] == cod_curso), None)
    
    if not dado_curso:
        raise ValueError("Curso não encontrado.")
    
    # Cria objeto apenas para validar dados
    obj_curso = Curso(dado_curso["codigo"], dado_curso["nome"], dado_curso["carga_horaria"], [])
    
    nova_turma = Turma(
        codigo_oferta=cod_oferta,
        curso=obj_curso,
        semestre=semestre,
        dias_horarios={dia: [[inicio, fim]]},
        vagas=int(vagas),
        local=local
    )

    # Prepara dicionário final
    novo_dict = {
        "codigo_oferta": nova_turma.codigo_oferta,
        "codigo_curso": nova_turma.codigo_curso,
        "semestre": nova_turma.semestre,
        "dias_horarios": nova_turma.dias_horarios,
        "vagas": nova_turma.vagas,
        "status": nova_turma.status,
        "local": nova_turma.local,
    }
    lista_turmas.append(novo_dict)
    salvar_turmas(lista_turmas)