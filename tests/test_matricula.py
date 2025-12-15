import pytest
from src.models.curso import Curso
from src.models.turma import Turma
from src.models.aluno import Aluno
from src.models.matricula import Matricula
from src.infra import config

HORARIO_PADRAO = {"seg": [("08:00", "10:00")]}

def test_matricula_criacao_ok():
    # Verifica se a matrícula é criada corretamente e passa como parametro aluno e turma
    c = Curso("MAT101", "Cálculo", 60, [])
    t = Turma("T1", c, "2025.1", HORARIO_PADRAO, vagas=2)
    a = Aluno("João", "j@test.com", "1")

    m = Matricula(a, t)

    assert m.aluno is a # Verifica se o aluno é o mesmo da matricula
    assert m.turma is t # Verifica se a turma é a mesmo da matricula

def test_matricula_nota_invalida():
    # Verifica se a classe impede a atribuição de uma nota inválida (> 10 ou < 0)
    c = Curso("MAT101", "Cálculo", 60, [])
    t = Turma("T1", c, "2025.1", HORARIO_PADRAO, vagas=2)
    a = Aluno("João", "j@test.com", "1")
    m = Matricula(a, t)
    
    with pytest.raises(ValueError):
        m.nota = 20 # Retorna um erro pois 20 é >10

def test_matricula_eq():
    # Verifica se duas matrículas com o mesmo aluno e a mesma turma são consideradas iguais
    c = Curso("MAT101", "Cálculo", 60, [])
    t = Turma("T1", c, "2025.1", HORARIO_PADRAO, vagas=2)
    a = Aluno("João", "j@test.com", "1")

    m1 = Matricula(a, t)
    m2 = Matricula(a, t)

    assert m1 == m2 # Deve retornar True se __eq__ existir e estiver correto

def test_matricula_frequencia_invalida():
    # Verifica validação de frequência (0 a 100%)
    c = Curso("MAT101", "Cálculo", 60, [])
    t = Turma("T1", c, "2025.1", HORARIO_PADRAO, vagas=2)
    a = Aluno("João", "j@test.com", "1")
    m = Matricula(a, t)

    with pytest.raises(ValueError):
        m.frequencia = 110  # Maior que 100%
    
    with pytest.raises(ValueError):
        m.frequencia = -5   # Negativa

def test_calculo_situacao_aprovado():
    # Configura valores padrão para o teste não quebrar se o json mudar
    nota_padrao = config.nota_minima_aprovacao
    freq_padrao = config.frequencia_minima

    c = Curso("C1", "Teste", 60, [])
    t = Turma("T1", c, "2025.1", HORARIO_PADRAO, 30)
    a = Aluno("Ana", "a@test.com", "2")
    m = Matricula(a, t)

    m.nota = nota_padrao
    m.frequencia = freq_padrao 
    
    assert m.situacao() == "APROVADO"

def test_calculo_situacao_reprovado_nota():
    nota_padrao = config.nota_minima_aprovacao
    freq_padrao = config.frequencia_minima

    c = Curso("C1", "Teste", 60, [])
    t = Turma("T1", c, "2025.1", HORARIO_PADRAO, 30)
    a = Aluno("Beto", "b@test.com", "3")
    m = Matricula(a, t)

    # Define nota um pouco abaixo da média padrão
    m.nota = nota_padrao - 0.1 
    
    # Frequência perfeita para garantir que a reprovação seja SÓ por nota
    m.frequencia = 100 
    
    assert m.situacao() == "REPROVADO_POR_NOTA"

def test_calculo_situacao_reprovado_frequencia():
    #  Lê configurações
    freq_padrao = config.frequencia_minima

    c = Curso("C1", "Teste", 60, [])
    t = Turma("T1", c, "2025.1", HORARIO_PADRAO, 30)
    a = Aluno("Carla", "c@test.com", "4")
    m = Matricula(a, t)

    # Nota máxima para garantir que a reprovação seja so por falta
    m.nota = 10.0      
    
    # Define frequência um pouco abaixo do mínimo
    m.frequencia = freq_padrao - 1.0  
    
    assert m.situacao() == "REPROVADO_POR_FREQUENCIA"

def test_situacao_cursando():
    c = Curso("C1", "Teste", 60, [])
    t = Turma("T1", c, "2025.1", HORARIO_PADRAO, 30)
    a = Aluno("Duda", "d@test.com", "5")
    m = Matricula(a, t)
    
    # Sem nota e sem frequência = Cursando
    assert m.situacao() == "CURSANDO"

def test_trancar_matricula_ok():
    # Guarda a data original
    data_original = config.data_limite_trancamento

    try:
        # Define uma data futura para garantir que o trancamento seja permitido
        config.data_limite_trancamento = "2999-12-31"

        c = Curso("C1", "Teste", 60, [])
        t = Turma("T1", c, "2025.1", HORARIO_PADRAO, 30)
        a = Aluno("Aluno", "a@test.com", "10")
        m = Matricula(a, t)

        # Ação: trancar a matrícula
        m.trancar()

        # Verificação
        assert m.status == "TRANCADA"

    finally:
        # Restaura a configuração original
        config.data_limite_trancamento = data_original