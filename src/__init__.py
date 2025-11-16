# Indica que 'src' é um módulo Python.

from .pessoa import Pessoa
from .aluno import Aluno
from .curso import Curso
from .oferta import Oferta
from .turma import Turma
from .matricula import Matricula
from .configuracoes import Configuracoes

__all__ = [
    "Pessoa",
    "Aluno",
    "Curso",
    "Oferta",
    "Turma",
    "Matricula",
    "Configuracoes",
]
