from src.models.matricula import Matricula
from src.models.turma import Turma
from src.models.aluno import Aluno
from src.infra import config
"""
Coordenador de regras de aplicação do sistema.

Responsabilidades:
- Realizar matrícula (checando vagas, status e choque de horário)
- Criar e registrar objeto Matricula
- Funções auxiliares para horários
- Relatório de alunos por turma

é a camada que integra Aluno, Turma e Matricula.
"""

# Classes vazias, para serem marcadores de erro
class TurmaFechadaError(Exception): 
    pass
class TurmaLotadaError(Exception): 
    pass
class ChoqueHorarioError(Exception): 
    pass
class PreRequisitoError(Exception):
    pass
# Funções para horários

def minutos(hora): # Função que recebe horas e minutos e retorna a carga horária 
    h, m = map(int, hora.split(":"))
    return h * 60 + m


def intervalos_se_chocam(i1, i2): # Função que recebe horario de inicio e fim depois verifica se 1 termina antes do outro termina
    s1, e1 = map(minutos, i1)
    s2, e2 = map(minutos, i2)
    return max(s1, s2) < min(e1, e2)

def matricular(aluno: Aluno, turma: Turma):
    
    # Valida Pré-requisitos
    for cod_pre in turma.curso.pre_requisitos:
            if not aluno.aprovou(cod_pre):
                raise PreRequisitoError(f"Pré-requisito não atendido: {cod_pre}")
    
    # Valida Status da Turma
    if turma.status != "ABERTA": 
        raise TurmaFechadaError()

    # # Se turma não tiver vaga retorna o erro de turma fechada
    if not turma.tem_vaga(): 
        raise TurmaLotadaError()

    #  Se turma tiver um choque de horário a se matricula na turma retorna o erro de Choque de horário
    if aluno.tem_choque(turma): 
        raise ChoqueHorarioError()

    # Criar matrícula
    m = Matricula(aluno, turma) 

    # Ligar bidirecionalmente
    turma.adicionar_matricula(m) 
    
    aluno.adicionar_matricula_ativa(m)

    return m
    
# Relatório básico (alunos por turma)
def alunos_por_turma(turma):
    return [
        {
            "nome": m.aluno.nome,
            "matricula": m.aluno.matricula,
            "nota": m.nota,
            "frequencia": m.frequencia
        }
        for m in turma.matriculas
    ]