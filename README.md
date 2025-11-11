# GERENCIADOR DE CURSOS E ALUNOS 🎓

## 📝 Descrição do Projeto e Objetivo

Este projeto consiste no desenvolvimento de um **Sistema de Gerenciamento de Cursos, Turmas, Alunos e Matrículas**.

O foco principal é aplicar os conceitos de **Programação Orientada a Objetos (POO)**, como encapsulamento, herança, métodos especiais, e validações rigorosas entre classes.

### 🎯 Objetivo Principal

O objetivo é gerenciar o fluxo acadêmico, incluindo:
* Controle de **pré-requisitos** para cursos.
* Detecção de **choque de horário** em matrículas.
* Controle de **limite de vagas** e a situação da matrícula (Aprovado, Reprovado).
* Cálculo do **CR (Coeficiente de Rendimento)**.
* Emissão de **relatórios acadêmicos** (ex: taxa de aprovação, Top N alunos).

A persistência dos dados será feita de forma simples, utilizando **JSON ou SQLite**.

---

## 🏗️ Estrutura Planejada de Classes

A modelagem do projeto seguirá a seguinte estrutura de classes, conforme os Requisitos Técnicos de POO:

| Classe | Objetivo e Responsabilidade | Base/Relacionamento |
| :--- | :--- | :--- |
| `Pessoa` | Classe base para conter atributos comuns a indivíduos. | - (Base) |
| `Aluno` | Representa o estudante. Possui **matrícula** e **histórico** acadêmico. Calcula o **CR**. | Herda de `Pessoa` |
| `Oferta` | Classe base abstrata para conter atributos comuns a ofertas de disciplina/curso. | - (Base) |
| `Turma` | Representa uma oferta específica de um `Curso` em um período/semestre. Controla **horários** e **vagas**. | Herda de `Oferta` |
| `Curso` | Define a disciplina acadêmica: código, nome, carga horária, e lista de **pré-requisitos**. | - |
| `Matricula` | Objeto de relacionamento que liga um **`Aluno`** a uma **`Turma`**. Armazena **notas**, **frequência** e **estado** (situação). | Relaciona `Aluno` e `Turma` |

### 🛠️ Focos de POO

* **Herança:** `Aluno` herda de `Pessoa`; `Turma` herda de `Oferta`.
* **Encapsulamento:** Uso de `@property` para validar atributos como nota (0-10), frequência (0-100), CR ($\ge0$) e vagas ($\ge0$).
* **Métodos Especiais:** Implementação mínima de 4 métodos, como:
    * `Aluno.__lt__`: para ordenação por CR.
    * `Turma.__len__`: retorna a ocupação (quantidade de matrículas ativas).
    * `Curso.__str__`/`__repr__`: para resumos.
    * `Matricula.__eq__`: para comparação única (aluno + turma).

---
