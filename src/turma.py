from .oferta import Oferta
from .curso import Curso # Importado para validação de tipo no setter
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

    def __init__(self, codigo_oferta, curso, semestre, dias_horarios,
                 vagas, status="ABERTA", local=None):
        super().__init__( # Inicializa a classe pai Oferta
            codigo_oferta=codigo_oferta,
            codigo_curso=curso.codigo,  
            semestre=semestre,
            dias_horarios=dias_horarios,
            vagas=vagas,
            status=status,
            local=local,
        )
        self.__matriculas = []
        self.curso = curso

   
    @property
    def matriculas(self):
        return self.__matriculas[:]

    @matriculas.setter
    def matriculas(self, lista):
        raise AttributeError("A lista de matrículas não pode ser substituída diretamente.") # Validação para não ser possível atribuir a lista diretamente
    
    @property
    def curso(self):
        return self.__curso

    @curso.setter
    def curso(self, novo_curso):
        if not isinstance(novo_curso, Curso):
            raise TypeError("curso deve ser um objeto da classe Curso.") # Validação para garantir que é da classe Curso
        self.__curso = novo_curso

    def matricular(self, matricula):
        from .matricula import Matricula # Importação local para evitar erro de importação circular 

        if not isinstance(matricula, Matricula):
            raise TypeError("O objeto não é uma Matrícula válida.") 

        if self.status != "ABERTA": # Validação de status
            raise ValueError("Turma fechada.")
        
        if len(self) >= self.vagas: # Validação de vagas
            raise ValueError("Turma lotada.")
        
        if matricula in self.__matriculas: # Validação para não haver aluno repetido
             raise ValueError("Aluno já matriculado.")

        self.__matriculas.append(matricula) # Adiciona a matrícula após passar por todas as validações

    def __len__(self):
       return len(self.__matriculas)

    def __str__(self): # Método __str__ que retorna uma string com código da turma, nome do curso, semestre e ocupação
        return (
            f"Turma {self.codigo_oferta} | Curso: {self.curso.nome} | "
            f"Semestre: {self.semestre} | Ocupação: {len(self)}/{self.vagas}"
        )