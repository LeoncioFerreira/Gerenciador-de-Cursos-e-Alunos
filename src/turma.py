from .oferta import Oferta

class Turma(Oferta):
    """
    Representa uma turma aberta para matrícula.

    Responsabilidades:
    - Controlar vagas, horários, estado (aberta/fechada)
    - Manter lista de matrículas
    - Implementar métodos especiais (__len__)
    - Verificar choque de horário

    Relaciona-se com Curso e Matricula.
    """
    pass
