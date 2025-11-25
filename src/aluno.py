from .pessoa import Pessoa

class  Aluno(Pessoa):
    """
    Representa um aluno da universidade.

    Responsabilidades:
    - Armazenar matrícula, histórico, CR
    - Implementar métodos de cálculo de CR
    - Especializar Pessoa com dados acadêmicos

    Será relacionado com Turma e Matricula.
    """
    #Metodo construtor
    def __init__(self, nome, email, matricula):
        super().__init__(nome, email)  # Herda nome e email da Pessoa (classe pai)
        self.matricula = matricula
        self.__historico = []

    @property 
    def matricula(self):
        return self.__matricula  # Faz o método se comportar como atributo
    
    @matricula.setter
    def matricula (self,matricula):
        if not matricula.strip(): # Faz a validação para que matrícula não fique vazia
            raise ValueError("A matricula não pode ser vazio")
        self.__matricula = matricula
    
    @property
    def historico(self):
        return self.__historico[:] # Retorna uma copia segura do historico
    
    def adicionar_ao_historico(self, matricula):
        # Adiciona uma matrícula já concluída ao histórico do aluno.
        self.__historico.append(matricula)

    def calcular_cr(self):
        
        # Coeficiente de Redimento = soma(nota * carga_horaria) / soma(carga_horaria)
        
        total_pesos = 0
        total_acumulado = 0

        for matricula in self.__historico:
            # Ignora matrículas sem nota lançada
            if matricula.nota is None:
                continue

            carga = matricula.turma.curso.carga_horaria # Acessa a carga horária do Curso através de : Matricula,Turma e Curso
            total_pesos += carga
            total_acumulado += matricula.nota * carga

        if total_pesos == 0:
            return 0
        
        return total_acumulado / total_pesos

    # Metodo __lt__ (menor que) serve para comparar o cf do objeto com outro
    def __lt__(self, other):
        if not isinstance(other, Aluno):
            return NotImplemented

        cr_self = self.calcular_cr()
        cr_other = other.calcular_cr()

    # Primeiro compara pelo CR
        if cr_self != cr_other:
            return cr_self < cr_other  # menor CR = "menor" aluno na ordenação

    # Desempate por nome
        return self.nome < other.nome