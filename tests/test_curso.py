import pytest
from src.models.curso import Curso

def test_criar_curso_ok():
    # Testa a criação de um curso com atributos válidos
    c = Curso("MAT101", "Cálculo I", 60, [])
    assert c.codigo == "MAT101"
    assert c.nome == "Cálculo I"
    assert c.carga_horaria == 60

def test_curso_codigo_vazio():
    # Testa se um erro é lançado quando o código do curso é vazio
    with pytest.raises(ValueError):
        Curso("", "Nome", 60, [])

def test_carga_horaria_invalida():
    # Testa se um erro é lançado quando a carga horária não é positiva
    with pytest.raises(ValueError):
        Curso("MAT101", "Cálculo I", -10, [])

def test_curso_str():
    # Testa o método especial __str__ do curso
    c = Curso("MAT101", "Cálculo I", 60, [])
    assert "Cálculo I" in str(c)
    assert "MAT101" in str(c)