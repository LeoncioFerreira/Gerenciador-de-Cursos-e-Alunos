import statistics
from src.infra.persistencia import carregar_matriculas, carregar_alunos, carregar_turmas, carregar_cursos
from src.models.aluno import Aluno
from src.models.curso import Curso
from src.models.turma import Turma
from src.models.matricula import Matricula
from src.infra import config 
"""
Serviços de Relatórios Acadêmicos

Responsabilidade:
- Gerar relatórios consolidados a partir dos dados persistidos.
- Calcular estatísticas acadêmicas.
- Fornecer dados prontos para visualização na interface.

Este módulo NÃO altera dados do sistema,
apenas realiza leitura e agregação.
"""

#  Seleciona apenas as matrículas da turma informada desconsiderando as trancadas
def relatorio_aprovacao_turma(cod_oferta):
    m_turma = [m for m in carregar_matriculas() if m["turma"] == cod_oferta and m["status"] != "TRANCADA"]
    total = len(m_turma)
    
    if not total: return {"aprovados": 0, "total": 0, "taxa": 0.0}
    # Conta quantos foram aprovados
    aprovados = sum(1 for m in m_turma if m["status"] == "APROVADO")
    return {"aprovados": aprovados, "total": total, "taxa": round((aprovados / total) * 100, 2)}

def relatorio_aprovacao_curso(cod_curso):
    turmas = carregar_turmas()
    ofertas_do_curso = [t["codigo_oferta"] for t in turmas if t["codigo_curso"] == cod_curso]
    
    matriculas = carregar_matriculas()
    m_curso = [m for m in matriculas if m["turma"] in ofertas_do_curso and m["status"] != "TRANCADA"]
    
    total = len(m_curso)
    
    if total == 0: 
        return {"taxa": 0.0, "total": 0, "aprovados": 0}
    
    aprovados = sum(1 for m in m_curso if m["status"] == "APROVADO")
    taxa = (aprovados / total) * 100
    
    return {"taxa": round(taxa, 2), "total": total, "aprovados": aprovados}

def relatorio_notas_turma(cod_oferta):
    # Pega todas as notas válidas (não nulas)
    notas = [float(m["nota"]) for m in carregar_matriculas() if m["turma"] == cod_oferta and m["nota"] is not None]
    
    # Caso para quando não houver nota
    if not notas: 
        return {
            "media": 0, "mediana": 0, "desvio_padrao": 0, 
            "minima": 0, "maxima": 0, "qtd": 0,
            "distribuicao": {
                "Ruim (0-4)": 0, 
                "Regular (5-6)": 0, 
                "Bom (7-8)": 0, 
                "Excelente (9-10)": 0
            }
        }
    
    # Cálculo do Desvio Padrão (Requer > 1 nota)
    stdev = statistics.stdev(notas) if len(notas) > 1 else 0.0

    # Define a distribuição qualitativa das notas por faixas de desempenho
    distribuicao = {
        "Ruim (0-4)": 0,
        "Regular (5-6)": 0,
        "Bom (7-8)": 0,
        "Excelente (9-10)": 0
    }
    
    for n in notas:
        if n < 5: 
            distribuicao["Ruim (0-4)"] += 1
        elif n < 7: 
            distribuicao["Regular (5-6)"] += 1
        elif n < 9: 
            distribuicao["Bom (7-8)"] += 1
        else: 
            distribuicao["Excelente (9-10)"] += 1

    return {
        "media": round(statistics.mean(notas), 2),
        "mediana": round(statistics.median(notas), 2),
        "desvio_padrao": round(stdev, 2),
        "minima": min(notas),
        "maxima": max(notas),
        "qtd": len(notas),
        "distribuicao": distribuicao
    }

def relatorio_top_alunos():
    # Top N por CR
    map_turmas = {t["codigo_oferta"]: t for t in carregar_turmas()}
    map_cursos = {c["codigo"]: c for c in carregar_cursos()}
    todas_matriculas = carregar_matriculas()
    lista_alunos = []
    
    for d in carregar_alunos():
        aluno = Aluno(d["nome"], d["email"], str(d["matricula"]))
        historico = [m for m in todas_matriculas if str(m["aluno"]) == str(aluno.matricula) and m["status"] in ["APROVADO", "REPROVADO_POR_NOTA", "REPROVADO_POR_FREQUENCIA"]]
        
        for m in historico:
            t_data = map_turmas.get(m["turma"])
            if t_data and (c_data := map_cursos.get(t_data["codigo_curso"])):
                curso = Curso(c_data["codigo"], "Ref", int(c_data["carga_horaria"]), [])
                
                # Proteção contra horário vazio no JSON
                dias = t_data.get("dias_horarios")
                if not dias: dias = {"EAD": [["00:00", "00:00"]]}
                
                # Cria o objeto Matrícula que liga o aluno à turma reconstruída
                turma = Turma(
                    codigo_oferta=t_data["codigo_oferta"], 
                    curso=curso, 
                    semestre=t_data["semestre"], 
                    dias_horarios=dias,
                    vagas=t_data["vagas"],
                    status=t_data["status"]
                )
                # Cria o objeto Matrícula que liga o aluno à turma reconstruída
                obj_mat = Matricula(aluno, turma)
                obj_mat.nota = m["nota"]
                # Esse histórico será usado para calcular o cr
                aluno.adicionar_ao_historico(obj_mat)
        
        lista_alunos.append(aluno)
    # Ordena os alunos pelo CR utilizando o método especial __lt__ definido em Aluno
    lista_alunos.sort(reverse=True)
    n = config.top_n_alunos or 5
    return [{"nome": a.nome, "matricula": a.matricula, "cr": round(a.calcular_cr(), 2)} for a in lista_alunos[:n]]