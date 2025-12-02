import pytest
from src.curso import Curso
from src.turma import Turma
from src.aluno import Aluno
from src.matricula import Matricula

def test_matricula_criacao_ok():
    # Verifica se a matrícula é criada corretamente e passa como parametro aluno e turma
    c = Curso("MAT101", "Cálculo", 60, [])
    t = Turma("T1", c, "2025.1",{"seg": [("08:00", "10:00")]}, vagas=2)
    a = Aluno("João", "j@test.com", "1")

    m = Matricula(a, t)

    assert m.aluno is a # Verifica se o aluno é o mesmo da matricula
    assert m.turma is t # Verifica se a turma é a mesmo da matricula

def test_matricula_nota_invalida():
    # Verifica se a classe impede a atribuição de uma nota inválida (> 10 ou < 0)
    c = Curso("MAT101", "Cálculo", 60, [])
    t = Turma("T1", c, "2025.1", {"seg": [("08:00", "10:00")]}, vagas=2)
    a = Aluno("João", "j@test.com", "1")

    m = Matricula(a, t)
    with pytest.raises(ValueError):
        m.nota = 20 # Retorna um erro pois 20 é >10

def test_matricula_eq():
    # Verifica se duas matrículas com o mesmo aluno e a mesma turma são consideradas iguais
    c = Curso("MAT101", "Cálculo", 60, [])
    t = Turma("T1", c, "2025.1", {"seg": [("08:00", "10:00")]}, vagas=2)
    a = Aluno("João", "j@test.com", "1")

    m1 = Matricula(a, t)
    m2 = Matricula(a, t)

    assert m1 == m2 # Deve retornar True se __eq__ existir e estiver correto