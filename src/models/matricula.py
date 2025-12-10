from .aluno import Aluno
from .turma import Turma
from src.infra import config
from datetime import date  # Blibioteca para validarmos a data de trancamento

class Matricula:
    """
Representa a relação entre um Aluno e uma Turma.

Responsabilidades:
- Armazenar nota, frequência e estado da matrícula
- Registrar o vínculo entre aluno e turma
- Implementar métodos especiais (__eq__ e __str__)
- Ajudar o Aluno a compor histórico e cálculo de CR
    """
    # Método construtor
    def __init__(self, aluno, turma):
        self.aluno = aluno
        self.turma = turma
        self.__nota = None
        self.__frequencia = None
        self.status = "ATIVA"

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

    def situacao(self):
        if self.nota is None or self.frequencia is None:
            return "CURSANDO"
        
        if self.frequencia < config.frequencia_minima:
            return "REPROVADO_POR_FREQUENCIA"

        if self.nota < config.nota_minima_aprovacao:
            return "REPROVADO_POR_NOTA"

        return "APROVADO"
    
    def trancar(self):
            hoje = date.today().isoformat()
            if hoje > config.data_limite_trancamento:
                raise Exception("Fora do prazo de trancamento.")
    
            self.status = "TRANCADA"

    def __eq__(self, outro):
        # Matrículas são iguais se:
        # Mesmo aluno
        # Mesma turma
       
        if not isinstance(outro, Matricula):
            return False
        return self.aluno == outro.aluno and self.turma == outro.turma

    def __str__(self):
        return f"Matricula: {self.aluno.nome} → {self.turma.codigo_oferta}"