from .pessoa import Pessoa

class  Aluno(Pessoa):
    """
Representa um aluno da instituição.

Responsabilidades:
- Armazenar matrícula, histórico e matrículas ativas    
- Calcular CR a partir do histórico
- Verificar choque de horário ao tentar nova matrícula
 - Comparar alunos pelo CR (__lt__)

Ligação: Aluno → Matricula → Turma.
    """
    #Metodo construtor
    def __init__(self, nome, email, matricula):
        super().__init__(nome, email)  # Herda nome e email da Pessoa (classe pai)
        self.matricula = matricula
        self.__historico = []
        self.__matriculas_ativas = [] # Lista de matriculas em andamento
    
    @property 
    def matricula(self):
        return self.__matricula  # Faz o método se comportar como atributo
    
    @matricula.setter
    def matricula (self,matricula):
        if not matricula.strip(): # Faz a validação para que matrícula não fique vazia
            raise ValueError("A matricula não pode ser vazio")
        self.__matricula = matricula
    
    @property
    def matriculas_ativas(self):
        return self.__matriculas_ativas[:] # Retorna uma copia segura da matricula 

    @property
    def historico(self):
        return self.__historico[:] # Retorna uma copia segura do historico
    
    def adicionar_ao_historico(self, matricula):
        # Adiciona uma matrícula já concluída ao histórico do aluno
        self.__historico.append(matricula)

    # Adiciona uma matrícula ativa (em andamento) ao aluno
    def adicionar_matricula_ativa(self, matricula):
        self.__matriculas_ativas.append(matricula)

    def tem_choque(self, nova_turma):
        """
        Verifica se o aluno tem choque de horário com uma nova turma.
        Compara os horários das matrículas ativas.
        """

        for matricula in self.__matriculas_ativas: # Laço para comparar os horarios das turma do aluno com a nova turma
            turma_atual = matricula.turma
        
            for dia, horarios in turma_atual.dias_horarios.items(): # Laço para verificar se no dia da semana o aluno tem aula
                if dia not in nova_turma.dias_horarios:
                    continue

                for h1 in horarios: # Laço para caso forem no mesmo dia comprara horario de inicio e fim
                    for h2 in nova_turma.dias_horarios[dia]:
                        # h = ("08:00", "10:00")
                        inicio1, fim1 = h1
                        inicio2, fim2 = h2

                        if max(inicio1, inicio2) < min(fim1, fim2):
                            return True
        return False
           
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