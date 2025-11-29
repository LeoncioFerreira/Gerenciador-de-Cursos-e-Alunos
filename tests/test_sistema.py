import pytest
from src.curso import Curso
from src.turma import Turma
from src.aluno import Aluno
from src.sistema import (
    matricular,
    alunos_por_turma,
    TurmaFechadaError,
    TurmaLotadaError,
    ChoqueHorarioError
)
 # Cria objetos necessários: curso, turma aberta e aluno
def test_matricular_ok():
    c = Curso("COMP101", "Programação I", 60, [])
    t = Turma("T1", c, "2025.1", {"SEG": [("08:00", "10:00")]}, vagas=2, status="ABERTA")
    a = Aluno("João", "j@test.com", "1")

# Realiza matrícula com sucesso passa também os objetos aluno e turma 
    m = matricular(a, t)

    # Verifica se a matrícula está ligada ao aluno e à turma correta
    assert m.aluno is a
    assert m.turma is t
    
    # Turma passa a ter 1 matrícula
    assert len(t) == 1
   
    # Verifica se o aluno registrou a matrícula ativa
    assert a.matriculas_ativas[0] is m


def test_turma_lotada():
   # Cria turma com 2 vagas
    c = Curso("COMP101", "Programação I", 60, [])
    t = Turma("T1", c, "2025.1", {"SEG": [("08:00", "10:00")]}, vagas=2, status="ABERTA")

    a1 = Aluno("A1", "a1@test.com", "1")
    a2 = Aluno("A2", "a2@test.com", "2")
    a3 = Aluno("A3", "a3@test.com", "3")

# Preenche a turma
    matricular(a1, t)
    matricular(a2, t)

# Terceira matrícula deve levantar erro de turma lotada
    with pytest.raises(TurmaLotadaError):
        matricular(a3, t)


def test_turma_fechada():
    # Cria uma turma com status FECHADA
    c = Curso("COMP101", "Programação I", 60, [])
    t = Turma("T2", c, "2025.1", {"TER": [("14:00", "16:00")]}, vagas=2, status="FECHADA")

    a = Aluno("João", "j@test.com", "1")
    
    # Matrícula deve falhar pois turma está fechada
    with pytest.raises(TurmaFechadaError):
        matricular(a, t)


def test_choque_horario():
    # Cria duas turmas com horários conflitantes
    c = Curso("COMP101", "Programação I", 60, [])

    t1 = Turma("T1", c, "2025.1", {"SEG": [("08:00", "10:00")]}, vagas=3, status="ABERTA")
    t2 = Turma("T2", c, "2025.1", {"SEG": [("09:00", "11:00")]}, vagas=3, status="ABERTA")

    a = Aluno("João", "j@test.com", "1")

    matricular(a, t1)

     # Matricula o aluno na primeira turma
    with pytest.raises(ChoqueHorarioError):
        matricular(a, t2)

    # Segunda matrícula deve falhar devido ao choque de horário
def test_relatorio():
    c = Curso("COMP101", "Programação I", 60, [])
    t = Turma("T1", c, "2025.1", {"QUI": [("08:00", "10:00")]}, vagas=3, status="ABERTA")

    # Cria uma turma e dois alunos
    a1 = Aluno("A1", "a1@test.com", "1")
    a2 = Aluno("A2", "a2@test.com", "2")

    # Matricula ambos na turma
    matricular(a1, t)
    matricular(a2, t)

    # Gera relatório da turma
    rel = alunos_por_turma(t)

    # Verifica tamanho e conteúdo do relatório
    assert len(rel) == 2
    assert rel[0]["nome"] == "A1"
    assert rel[1]["nome"] == "A2"
    assert "nota" in rel[0] # relatório inclui nota
    assert "frequencia" in rel[1] # relatório inclui frequência
