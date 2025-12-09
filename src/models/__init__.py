"""
Pacote de Modelos 

Responsabilidade:
- Definir as entidades principais do sistema (Aluno, Curso, Turma, etc.).
- Implementar as regras de negócio essenciais às entidades (ex: cálculo de CR).
- Aplicar conceitos de POO: Herança, Encapsulamento (@property) e Polimorfismo.
"""
from .pessoa import Pessoa
from .aluno import Aluno
from .curso import Curso
from .oferta import Oferta
from .turma import Turma
from .matricula import Matricula