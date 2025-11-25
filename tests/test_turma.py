import pytest
from src.curso import Curso
from src.turma import Turma
from src.matricula import Matricula
from src.aluno import Aluno

def criar_turma_padrao():
    c = Curso("MAT101", "Cálculo I", 60, [])
    return Turma("T1", c, "2025.1", {"seg": "08-10"}, vagas=2)

def test_len_turma():
    t = criar_turma_padrao()
    assert len(t) == 0

def test_matricular_ok():
    t = criar_turma_padrao()
    a = Aluno("João", "j@test.com", "1")
    m = Matricula(a, t)

    t.matricular(m)
    assert len(t) == 1

def test_matricula_tipo_errado():
    t = criar_turma_padrao()
    with pytest.raises(TypeError):
        t.matricular("batata")

def test_turma_lotada():
    t = criar_turma_padrao()

    a1 = Aluno("A1", "a1@test.com", "1")
    a2 = Aluno("A2", "a2@test.com", "2")
    a3 = Aluno("A3", "a3@test.com", "3")

    m1 = Matricula(a1, t)
    m2 = Matricula(a2, t)
    m3 = Matricula(a3, t)

    t.matricular(m1)
    t.matricular(m2)

    with pytest.raises(ValueError):
        t.matricular(m3)
