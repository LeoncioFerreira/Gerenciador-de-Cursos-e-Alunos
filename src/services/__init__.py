"""
Pacote de Serviços

Responsabilidade:
- Orquestrar as operações do sistema (Matricular, Trancar, Lançar Notas).
- Validar regras de negócio complexas que envolvem múltiplas classes (ex: Choque de Horário, Pré-requisitos).
- Servir como ponte entre a Interface (Rotas) e a Infraestrutura (Dados).

Aqui residem as funções que garantem a integridade lógica das operações acadêmicas.
"""

from .sistema import matricular
from .servicos import *