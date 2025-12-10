import pytest
from src.models.curso import Curso
from src.models.turma import Turma
from src.models.matricula import Matricula
from src.models.aluno import Aluno

def criar_turma_padrao():
    # Cria um curso e retorna uma turma com 2 vagas    
    c = Curso("MAT101", "Cálculo I", 60, [])
    return Turma("T1", c, "2025.1", {"seg": [("08:00", "10:00")]}, vagas=2)

def test_len_turma():
    # Verifica o tamanho inicial da turma 
    t = criar_turma_padrao()
    assert len(t) == 0 # Retorna que a turma tem 0 inscritos 

def test_matricular_ok():
    # Matricula um aluno na turma e valida se o total de inscritos é atualizado
    t = criar_turma_padrao()
    a = Aluno("João", "j@test.com", "1")
    m = Matricula(a, t)

    t.adicionar_matricula(m)
    assert len(t) == 1 # Retorna 1 inscrito na turma 

def test_matricula_tipo_errado():
    # Testa erro ao tentar matricular algo que não seja objeto Matricula
    t = criar_turma_padrao()
    with pytest.raises(TypeError): # Retorna erro pois só aceita objetos do tipo Matricula
        t.adicionar_matricula("batata") # Deve dar erro porque não é um objeto Matricula

def test_turma_lotada():
    # Preenche a turma até o limite de vagas e verifica se impede nova matrícula

    t = criar_turma_padrao()

    a1 = Aluno("A1", "a1@test.com", "1")
    a2 = Aluno("A2", "a2@test.com", "2")
    a3 = Aluno("A3", "a3@test.com", "3")

    m1 = Matricula(a1, t)
    m2 = Matricula(a2, t)
    m3 = Matricula(a3, t)

    t.adicionar_matricula(m1)
    t.adicionar_matricula(m2)

    with pytest.raises(ValueError):
        t.adicionar_matricula(m3) # Retorna erro pois a turma tem 2 vagas e tentamos matricular 3 alunos

