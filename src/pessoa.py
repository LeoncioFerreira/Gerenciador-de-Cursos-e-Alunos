import re
class Pessoa:
    """
    Classe base que representa uma pessoa no sistema.
    Será utilizada como superclasse para Aluno.

    Responsabilidades:
    - Armazenar informações comuns (nome, e-mail, etc.)
    - Servir como base para herança (extensibilidade)
    """
    # Método construtor
    def __init__(self,nome,email):
        self.nome = nome 
        self.email = email

    @property 
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome (self,nome):
        # Validação para nome não ser vazio
        if not nome.strip():
            raise ValueError("O nome não pode ser vazio")
        self.__nome = nome
    
    @property
    def email(self):
        return self.__email
    @email.setter
    def email(self, valor):
        # Regex simples para validar e-mails no formato geral
        padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(padrao, valor):
            raise ValueError("E-mail inválido.")
        self.__email = valor
    
    # Metodo __str__ que retorna uma string com nome e e-mail
    def __str__(self):
        return f"Pessoa: {self.__nome} <{self.__email}>"
