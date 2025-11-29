"""
Módulo de persistência em JSON.

Responsabilidades:
- Salvar e carregar dados do sistema de forma centralizada.
- Definir caminhos fixos para arquivos (alunos, cursos, turmas, matrículas).
- Fornecer funções simples como salvar_alunos() e carregar_turmas() para
evitar repetição de código e manter o sistema organizado.

Este módulo separa a persistência da lógica de negócio, seguindo o
princípio de responsabilidade única.

Exemplo de uso:
from persistencia import carregar_alunos, salvar_alunos

alunos = carregar_alunos()
alunos.append({"nome": "Ana"})
salvar_alunos(alunos)
"""
import json
import os

def salvar(caminho, dados):
    # Salva dados em um arquivo JSON.
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


def carregar(caminho):
    # Carrega dados de um arquivo JSON.
    # Se o arquivo não existir, retorna uma lista vazia.
   
    if not os.path.exists(caminho):
        return []

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


# Caminhos fixos pré-definidos para cada tipo de dado
ARQ_ALUNOS = "data/alunos.json"
ARQ_CURSOS = "data/cursos.json"
ARQ_TURMAS = "data/turmas.json"
ARQ_MATRICULAS = "data/matriculas.json"


# Funções para alunos
def carregar_alunos():
    return carregar(ARQ_ALUNOS)

def salvar_alunos(lista):
    salvar(ARQ_ALUNOS, lista)


# Funções para cursos
def carregar_cursos():
    return carregar(ARQ_CURSOS)

def salvar_cursos(lista):
    salvar(ARQ_CURSOS, lista)


# Funções para turmas
def carregar_turmas():
    return carregar(ARQ_TURMAS)

def salvar_turmas(lista):
    salvar(ARQ_TURMAS, lista)


# Funções para matrículas
def carregar_matriculas():
    return carregar(ARQ_MATRICULAS)

def salvar_matriculas(lista):
    salvar(ARQ_MATRICULAS, lista)
