from src.aluno import Aluno
from src.curso import Curso
from src.turma import Turma
from src.matricula import Matricula

def test_cr_calculo():
    a = Aluno("João", "j@test.com", "1")
    c = Curso("MAT101", "Cálculo", 60, [])
    t = Turma("T1", c, "2025.1", {"seg": "08-10"}, vagas=5)

    m = Matricula(a, t)
    m.nota = 8.0
    
    a.adicionar_ao_historico(m)
    assert a.calcular_cr() == 8.0

def test_lt_comparacao():
    c = Curso("MAT101", "Cálculo", 60, [])
    t = Turma("T1", c, "2025.1", {"seg": "08-10"}, vagas=5)

    a1 = Aluno("João", "j1@test.com", "1")
    a2 = Aluno("Maria", "j2@test.com", "2")

    m1 = Matricula(a1, t); m1.nota = 5
    m2 = Matricula(a2, t); m2.nota = 9

    a1.adicionar_ao_historico(m1)
    a2.adicionar_ao_historico(m2)

    assert a1 < a2
