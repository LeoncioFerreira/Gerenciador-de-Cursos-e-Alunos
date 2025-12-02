class Oferta:
    """
Representa uma oferta de curso em um semestre (serve como base para Turma).

Responsabilidades:
- Armazenar semestre, horários, status e número de vagas
- Validar dados recebidos
- Fornecer estrutura para criação de Turma

Turma herda desta classe para adicionar comportamento próprio.
    """
   
    def __init__(self,codigo_oferta ,codigo_curso , semestre, dias_horarios, vagas, status, local = None):
        self.codigo_oferta = codigo_oferta
        self.codigo_curso = codigo_curso
        self.semestre = semestre
        self.dias_horarios = dias_horarios
        self.vagas = vagas
        self.status = status
        self.local = local
    
    @property
    def vagas(self):
        return self.__vagas
    
    @vagas.setter
    def vagas(self,valor):
        if valor<= 0:  # Validação para que a quantidade de vagas seja positiva
            raise ValueError("A quantidade de vagas precisa ser positiva.")
        self.__vagas = valor 
    
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, valor):
        novo_valor = valor.upper()
        if novo_valor not in ("ABERTA", "FECHADA"): # Validação para que status só possa ser aberto ou fechado
            raise ValueError("Status deve ser 'ABERTA' ou 'FECHADA'.")
        self.__status = novo_valor

    def abrir(self):
        self.status = "ABERTA"

    def fechar(self):
        self.status = "FECHADA"

    @property
    def codigo_oferta(self):
        return self.__codigo_oferta
    
    @codigo_oferta.setter
    def codigo_oferta(self, valor):
        if not valor.strip(): # Validação para que o código da oferta não seja vazio
            raise ValueError("O código da oferta não pode ser vazio.")
        self.__codigo_oferta = valor
    
    @property
    def codigo_curso(self):
        return self.__codigo_curso
    
    @codigo_curso.setter
    def codigo_curso(self, valor):
        if not valor.strip(): # Validação para que o código do curso não seja vazio
            raise ValueError("O código do curso não pode ser vazio.")
        self.__codigo_curso = valor

    @property
    def semestre(self):
        return self.__semestre
    
    @semestre.setter
    def semestre(self, valor):
        if not valor.strip(): # Validação para que o semestre não seja vazio
            raise ValueError("O semestre não pode ser vazio.")
        self.__semestre = valor

    @property
    def dias_horarios(self):
         return self.__dias_horarios
    
    @dias_horarios.setter
    def dias_horarios(self, valor):    
        if not isinstance(valor, dict): # Validação para que dias e horários sejam um dicionário
            raise TypeError("Dias e horários devem ser um dicionário")
        
        if not valor:
            raise ValueError("A oferta deve ter pelo menos um dia e horário definido") # Validação para garantir que haja pelo menos um dia e horário definido
        self.__dias_horarios = valor
        
    def __str__(self): # Método __str__ que retorna uma string com código da oferta, curso, semestre, vagas e status
        return (f"Oferta: {self.codigo_oferta} | Curso: {self.codigo_curso} | "
                f"Semestre: {self.semestre} | Vagas: {self.vagas} | Status: {self.status}")