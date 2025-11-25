import pytest
from src.curso import Curso

def test_criar_curso_ok():
    c = Curso("MAT101", "Cálculo I", 60, [])
    assert c.codigo == "MAT101"
    assert c.nome == "Cálculo I"
    assert c.carga_horaria == 60

def test_curso_codigo_vazio():
    with pytest.raises(ValueError):
        Curso("", "Nome", 60, [])

def test_carga_horaria_invalida():
    with pytest.raises(ValueError):
        Curso("MAT101", "Cálculo I", -10, [])

def test_curso_str():
    c = Curso("MAT101", "Cálculo I", 60, [])
    assert "Cálculo I" in str(c)
    assert "MAT101" in str(c)