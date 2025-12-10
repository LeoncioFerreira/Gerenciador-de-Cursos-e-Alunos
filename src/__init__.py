# Indica que 'src' é um módulo Python.

from .models.pessoa import Pessoa
from .models.aluno import Aluno
from .models.curso import Curso
from .models.oferta import Oferta
from .models.turma import Turma
from .models.matricula import Matricula
from .infra.configuracoes import Configuracoes

__all__ = [
    "Pessoa",
    "Aluno",
    "Curso",
    "Oferta",
    "Turma",
    "Matricula",
    "Configuracoes",
]
