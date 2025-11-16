# Projeto 1 — Programação Orientada a Objetos  
### Tema 6 — Gerenciador de Cursos e Alunos  
## 👨‍💻 Autor
| Nome | GitHub |
|------|--------|
| Leôncio Ferreira Flores Neto | [@LeoncioFerreira](https://github.com/LeoncioFerreira)|
---

# 📌 **Descrição do Projeto**

Este projeto implementa um **Gerenciador de Cursos e Alunos**, atendendo ao **Tema 6** da disciplina de Programação Orientada a Objetos (UFCA).

O sistema deverá gerenciar:

* Cursos e pré-requisitos
* Turmas e horários
* Alunos e históricos
* Matrículas com validações completas
* Notas, frequência e situação acadêmica
* Relatórios gerais

O foco é aplicar:

* Herança
* Encapsulamento
* Métodos especiais
* Validações
* Regras de negócio
* Persistência simples via JSON

Este README contém a **modelagem da Semana 1**, incluindo a **UML textual** e a **estrutura inicial do projeto**.

---

# 🎯 **Objetivo Geral**

Construir uma arquitetura orientada a objetos clara, coesa e extensível, servindo de base para o desenvolvimento incremental das semanas seguintes.

---

# 🧱 **Estrutura Planejada de Classes**

A seguir está a **UML textual** completa, conforme solicitado pelo professor:

> *“UML textual (classes, atributos, métodos principais, relacionamentos)”*

---

# 🧩 **UML TEXTUAL**

---

## **Classe: Pessoa**

### **Atributos**

* nome: str
* email: str

### **Métodos principais**

* validar_email()
* atualizar_dados(nome, email)
* **str**()

### **Relacionamentos**

* **Superclasse de → Aluno**

---

## **Classe: Aluno (subclasse de Pessoa)**

### **Atributos**

* matricula: str
* historico: list[Matricula]

### **Métodos principais**

* calcular_cr()
* verificar_prerequisito_cumprido(curso)
* checar_choque_horario(turma)
* **lt**()

### **Relacionamentos**

* **Subclasse de → Pessoa**
* 1:N com Matricula

---

## **Classe: Oferta**

### **Atributos**

* periodo_semestre: str
* status: str

### **Métodos principais**

* abrir()
* fechar()
* **str**()

### **Relacionamentos**

* **Superclasse de → Turma**

---

## **Classe: Turma (subclasse de Oferta)**

### **Atributos**

* numero_turma: int
* curso: Curso
* periodo_semestre: str
* dias_horarios: dict
* vagas: int
* status: str
* matriculas: list[Matricula]

### **Métodos principais**

* abrir_turma()
* fechar_turma()
* tem_vaga()
* verificar_choque_horario(aluno)
* registrar_matricula(aluno)
* calcular_taxa_aprovacao()
* gerar_relatorios()
* **len**()

### **Relacionamentos**

* **Subclasse de → Oferta**
* 1:1 com Curso
* 1:N com Matricula

---

## **Classe: Curso**

### **Atributos**

* codigo: str
* nome: str
* carga_horaria: int
* lista_de_prerequisitos: list[str]
* ementa: str

### **Métodos principais**

* validar_prerequisitos()
* **str**()

### **Relacionamentos**

* 1:N com Turma

---

## **Classe: Matricula**

### **Atributos**

* aluno: Aluno
* turma: Turma
* nota: float
* frequencia: float
* situacao: str

### **Métodos principais**

* lancar_nota(valor)
* lancar_frequencia(valor)
* calcular_situacao(configuracoes)
* trancar(data_atual, configuracoes)
* **eq**()

### **Relacionamentos**

* N:1 com Aluno
* N:1 com Turma
* Associação bidirecional Aluno ↔ Turma

---

## **Classe: Configuracoes**

### **Atributos**

* nota_minima_aprovacao: float
* frequencia_minima: float
* data_limite_trancamento: date
* max_turmas_por_aluno: int
* top_n_alunos: int

### **Métodos principais**

* carregar()
* salvar()
* obter_parametro(chave)

### **Relacionamentos**

* Dependência com Matricula
* Dependência com Turma

---

# 🔗 **Tabela Resumida de Relacionamentos**

| De            | Tipo        | Para              | Descrição                                     |
| ------------- | ----------- | ----------------- | --------------------------------------------- |
| Pessoa        | Superclasse | Aluno             | Herança                                       |
| Oferta        | Superclasse | Turma             | Herança                                       |
| Curso         | 1:N         | Turma             | Curso pode ter diversas ofertas               |
| Aluno         | 1:N         | Matricula         | Aluno pode estar matriculado em várias turmas |
| Turma         | 1:N         | Matricula         | Turma pode ter muitos alunos                  |
| Matricula     | Associação  | Aluno ↔ Turma     | Relação bidirecional                          |
| Configurações | Dependência | Matricula / Turma | Regras globais                                |

---

# 📁 **Estrutura Inicial do Projeto**

```
Gerenciador-de-Cursos-e-Alunos/
│
├── data/
│   └── settings.json
│
├── src/
│   ├── __init__.py
│   ├── aluno.py
│   ├── configuracoes.py
│   ├── curso.py
│   ├── matricula.py
│   ├── oferta.py
│   ├── pessoa.py
│   └── turma.py
│
├── LICENSE
└── README.md

