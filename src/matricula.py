from .aluno import Aluno
from .turma import Turma
class Matricula:
    """
    Representa a relação entre um Aluno e uma Turma.

    Responsabilidades:
    - Armazenar notas, frequência e estado da matrícula
    - Validar pré-requisitos, choques de horário e vagas
    - Implementar métodos especiais (__eq__)
    - Calcular situação (Aprovado/Reprovado/Cursando)

    É a ligação central entre Aluno e Turma.
    """
    # Método construtor
    def __init__(self, aluno, turma):
        self.aluno = aluno
        self.turma = turma

        # Inicializa atributos opcionais para uso futuro
        self.__nota = None
        self.__frequencia = None

    @property
    def aluno(self):
        return self.__aluno

    @aluno.setter
    def aluno(self, valor):
        if not isinstance(valor, Aluno):  # Validação para garantir que o objeto passado seja da classe Aluno
            raise TypeError("Aluno deve ser um objeto da classe Aluno.")
        self.__aluno = valor
    
    @property
    def turma(self):
        return self.__turma

    @turma.setter
    def turma(self, valor):
        if not isinstance(valor, Turma): # Validação para garantir que o objeto passado seja da classe Turma
            raise TypeError("Turma deve ser um objeto da classe Turma.")
        self.__turma = valor

    @property
    def nota(self):
        return self.__nota

    @nota.setter
    def nota(self, valor):
        if valor is not None: # Validação para a nota ser entre 0 e 10
            if not (0 <= valor <= 10): 
                raise ValueError("A nota deve estar entre 0 e 10.")
        self.__nota = valor
    
    @property
    def frequencia(self):
        return self.__frequencia

    @frequencia.setter
    def frequencia(self, valor):
        if valor is not None: # Validação para a frequencia ser entre 0 e 100%
            if not (0 <= valor <= 100):
                raise ValueError("A frequência deve estar entre 0 e 100%.")
        self.__frequencia = valor

    def __eq__(self, other):
        #Matrículas são iguais se:
        #mesmo aluno
        #mesma turma
       
        if not isinstance(other, Matricula):
            return False
        return self.aluno == other.aluno and self.turma == other.turma

    def __str__(self):
        return f"Matricula: {self.aluno.nome} → {self.turma.codigo_oferta}"
    
