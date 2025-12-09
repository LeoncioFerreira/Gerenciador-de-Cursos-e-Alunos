class Curso:
    """
Modelo de um curso da instituição.

Responsabilidades:
- Armazenar código, nome e carga horária
- Validar dados de criação
- Associar-se a turmas através das ofertas

Não contém regras de matrícula; apenas define informações do curso.
    """
# Método construtor
    def __init__(self, codigo, nome,carga_horaria,pre_requisitos):
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.pre_requisitos = pre_requisitos

    @property 
    def codigo(self):
        return self.__codigo
    
    @codigo.setter
    def codigo(self,valor):
        if not valor.strip(): # Validação para o código  não ser vazio 
            raise ValueError("O código não pode ser vazio")
        self.__codigo = valor 

    @property 
    def carga_horaria(self):
        return self.__carga_horaria
    
    @carga_horaria.setter
    def carga_horaria(self, valor):
        if valor<= 0: # Validação para a carga horária ser positiva
            raise ValueError("A carga horária precisa ser positiva.")
        self.__carga_horaria = valor 
        
    @property 
    def nome (self):
        return self.__nome

    @nome.setter
    def nome(self,nome):
        if not nome: # Validação para o nome não ser vazio 
            raise ValueError("O nome não pode ser vazio")
        self.__nome = nome
    
    @property 
    def pre_requisitos(self):
        return self.__pre_requisitos

    @pre_requisitos.setter
    def pre_requisitos(self, lista):

    # Permitir lista vazia ou None
        if lista is None:
            self.__pre_requisitos = []
            return

        if not isinstance(lista, list):
            raise TypeError("Os pré-requisitos devem ser uma lista.")

        # Limpar entradas vazias vindas do formulário
        limpa = [c for c in lista if isinstance(c, str) and c.strip() != ""]

        self.__pre_requisitos = limpa


# Método __str__ que retorna uma string com nome do curso, codigo e carga horária
    def __str__(self):
       return f"Curso: {self.__nome} ({self.__codigo}) - CH: {self.carga_horaria}"