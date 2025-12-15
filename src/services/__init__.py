"""
Pacote de Serviços

Responsabilidade:
- Orquestrar as operações do sistema (Matricular, Trancar, Lançar Notas).
- Validar regras de negócio complexas que envolvem múltiplas classes (ex: Choque de Horário, Pré-requisitos).
- Servir como ponte entre a Interface (Rotas) e a Infraestrutura (Dados).

Aqui residem as funções que garantem a integridade lógica das operações acadêmicas.
"""

# Importa do arquivo aluno_service.py
from .aluno_service import servico_criar_aluno

# Importa do arquivo curso_service.py
from .curso_service import servico_criar_curso

# Importa do arquivo turma_service.py
from .turma_service import servico_criar_turma

# Importa do arquivo matricula_service.py
from .matricula_service import (
    servico_criar_matricula,
    servico_atualizar_nota,
    servico_atualizar_frequencia,
    servico_trancar_matricula
)

# O sistema.py continua independente, mas se quiser expor também:
from .sistema import matricular, alunos_por_turma