from .oferta import Oferta
from .curso import Curso # Importado para validação de tipo no setter
class Turma(Oferta):
    """
Representa uma turma ofertada de um curso.

Responsabilidades:
- Armazenar lista de matrículas
- Verificar se há vagas disponíveis
- Registrar novas matrículas
- Expor quantidade de alunos através de __len__

Não valida choque de horário; isso é feito pelo Aluno.
Não cria a matrícula; isso é feito pelo sistema.
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
        self.matriculas = []
        self.curso = curso
    
    @property
    def curso(self):
        return self.__curso

    @curso.setter
    def curso(self, novo_curso):
        if not isinstance(novo_curso, Curso):
            raise TypeError("curso deve ser um objeto da classe Curso.") # Validação para garantir que é da classe Curso
        self.__curso = novo_curso

    def tem_vaga(self): # Metodo que verifica se ha vaga disponivel na turma retorna true se ainda tiver vagas disponíveis na turma
        return len(self) < self.vagas

    def adicionar_matricula(self, matricula):
        from .matricula import Matricula # Importação local para evitar erro de importação circular 

        if matricula in self.matriculas:
             raise ValueError("Aluno já está na lista desta turma.")
        
        self.matriculas.append(matricula) # Adiciona a matrícula após passar por todas as validações

    def __len__(self):
       return len(self.matriculas)

    def __str__(self): # Método __str__ que retorna uma string com código da turma, nome do curso, semestre e ocupação
        return (
            f"Turma {self.codigo_oferta} | Curso: {self.curso.nome} | "
            f"Semestre: {self.semestre} | Ocupação: {len(self)}/{self.vagas}"
        )