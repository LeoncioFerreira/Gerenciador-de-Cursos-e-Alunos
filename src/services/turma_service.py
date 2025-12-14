from src.infra.persistencia import carregar_turmas, salvar_turmas, carregar_cursos
from src.models.turma import Turma
from src.models.curso import Curso
"""
Serviços de Turma

Responsabilidade:
- Criar e configurar turmas (ofertas).
- Garantir unicidade do código da oferta.
- Validar existência do curso associado.
- Delegar validações estruturais à classe Turma.

Este módulo representa a camada de serviço para
operações relacionadas a turmas.
"""

def servico_criar_turma(cod_oferta, cod_curso, semestre, vagas, dia, inicio, fim, local):
    lista_turmas = carregar_turmas()
    
    # Valida Unicidade 
    if any(str(t['codigo_oferta']) == str(cod_oferta) for t in lista_turmas):
        raise ValueError(f"Erro: O código de oferta {cod_oferta} já existe!")

    # Busca o Curso é necessário para criar o objeto Turma
    cursos = carregar_cursos()
    dado_curso = next((c for c in cursos if str(c["codigo"]) == str(cod_curso)), None)
    
    if not dado_curso:
        raise ValueError("Curso não encontrado.")
    
    # Recria o objeto curso apenas para passar para a turma
    obj_curso = Curso(dado_curso["codigo"], dado_curso["nome"], dado_curso["carga_horaria"], [])
    
    # Ao instanciar a Turma, os setters da classe são acionados e validam os dados
    nova_turma = Turma(
        codigo_oferta=cod_oferta,
        curso=obj_curso,
        semestre=semestre,
        dias_horarios={dia: [[inicio, fim]]},
        vagas=int(vagas),
        local=local
    )

    # Se chegou aqui, é porque os dados são válidos. Salvamos no json
    lista_turmas.append({
        "codigo_oferta": nova_turma.codigo_oferta, 
        "codigo_curso": nova_turma.codigo_curso, 
        "semestre": nova_turma.semestre, 
        "dias_horarios": nova_turma.dias_horarios, 
        "vagas": nova_turma.vagas, 
        "status": nova_turma.status, 
        "local": nova_turma.local
    })
    salvar_turmas(lista_turmas)