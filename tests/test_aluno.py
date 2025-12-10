from src.models.aluno import Aluno
from src.models.curso import Curso
from src.models.turma import Turma
from src.models.matricula import Matricula

def test_cr_calculo():
    # Teste para calcular o coeficiente de rendimento 
    # Criamos aluno, curso e turma para simular uma situação real

    a = Aluno("João", "j@test.com", "1")
    c = Curso("MAT101", "Cálculo", 60, [])
    t = Turma("T1", c, "2025.1", {"seg": [("08:00", "10:00")]}, vagas=5)

    # Criamos uma matrícula passando o aluno e a turma como parametros
    m = Matricula(a, t)

    # Definimos uma nota para essa matrícula
    m.nota = 8.0

    # Adiciona a matrícula ao histórico do aluno
    a.adicionar_ao_historico(m)

    # Define que o cr deve ser igual à nota pois só existe uma disciplina no histórico
    assert a.calcular_cr() == 8.0

def test_lt_comparacao():
    # Teste do método especial __lt__, usado para comparar alunos pelo cr
    # Aqui verificamos se a ordenação funciona como esperado

    c = Curso("MAT101", "Cálculo", 60, [])
    t = Turma("T1", c, "2025.1", {"seg": [("08:00", "10:00")]}, vagas=5)

    # Criamos dois alunos para comparar
    a1 = Aluno("João", "j1@test.com", "1")
    a2 = Aluno("Maria", "j2@test.com", "2")

    # Criamos matrículas para cada aluno e atribuimos notas diferentes
    m1 = Matricula(a1, t); m1.nota = 5   # João tem nota 5
    m2 = Matricula(a2, t); m2.nota = 9   # Maria tem nota 9

    # Adiciona as matrículas ao histórico dos alunos
    a1.adicionar_ao_historico(m1)
    a2.adicionar_ao_historico(m2)

    # Declara que João deve ser considerado menor que Maria
    # porque seu cr é inferior
    assert a1 < a2