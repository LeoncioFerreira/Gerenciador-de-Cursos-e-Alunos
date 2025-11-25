import pytest
from src.curso import Curso
from src.turma import Turma
from src.aluno import Aluno
from src.matricula import Matricula

def test_matricula_criacao_ok():
    c = Curso("MAT101", "Cálculo", 60, [])
    t = Turma("T1", c, "2025.1", {"seg":"08-10"}, vagas=2)
    a = Aluno("João", "j@test.com", "1")

    m = Matricula(a, t)

    assert m.aluno is a
    assert m.turma is t

def test_matricula_nota_invalida():
    c = Curso("MAT101", "Cálculo", 60, [])
    t = Turma("T1", c, "2025.1", {"seg":"08-10"}, vagas=2)
    a = Aluno("João", "j@test.com", "1")

    m = Matricula(a, t)
    with pytest.raises(ValueError):
        m.nota = 20  # inválido

def test_matricula_eq():
    c = Curso("MAT101", "Cálculo", 60, [])
    t = Turma("T1", c, "2025.1", {"seg":"08-10"}, vagas=2)
    a = Aluno("João", "j@test.com", "1")

    m1 = Matricula(a, t)
    m2 = Matricula(a, t)

    assert m1 == m2
