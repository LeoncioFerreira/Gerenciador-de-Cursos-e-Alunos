import json
from .matricula import Matricula
from .turma import Turma
from .aluno import Aluno

"""
Coordenador de regras de aplicação do sistema.

Responsabilidades:
- Realizar matrícula (checando vagas, status e choque de horário)
- Criar e registrar objeto Matricula
- Funções auxiliares para horários
- Persistência simples em JSON
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

# Funções para horários

def minutos(hora): # Função que recebe horas e minutos e retorna a carga horária 
    h, m = map(int, hora.split(":"))
    return h * 60 + m


def intervalos_se_chocam(i1, i2): #Função que recebe horario de inicio e fim depois verifica se 1 termina antes do outro termina
    s1, e1 = map(minutos, i1)
    s2, e2 = map(minutos, i2)
    return max(s1, s2) < min(e1, e2)

def matricular(aluno: Aluno, turma: Turma):
    if turma.status != "ABERTA": # Se turma for diferente de aberta retorna o erro de turma fechada 
        raise TurmaFechadaError()

    if not turma.tem_vaga(): # Se turma não tiver vaga retorna o erro de turma fechada
        raise TurmaLotadaError()

    if aluno.tem_choque(turma): #  Se turma tiver um choque de horário a se matricula na turma retorna o erro dw Choque de horário
        raise ChoqueHorarioError()

    # criar matrícula
    m = Matricula(aluno, turma)

    # ligar bidirecionalmente
    turma.matricular(m) # Se ele passar das verificaçoes registra que a turma tem esse aluno
    aluno.adicionar_matricula_ativa(m)# Adiciona essa matrícula a lista de matrículas ativas do Aluno

    return m # retorna a matricula

# Persistência simples com JSON 
def salvar(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def carregar(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)
    
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