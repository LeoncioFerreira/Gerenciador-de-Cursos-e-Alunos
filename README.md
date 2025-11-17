# Projeto 1 — Programação Orientada a Objetos  
### Tema 6 — Gerenciador de Cursos e Alunos  

## 👨‍💻 Autor
| Nome | GitHub |
|------|--------|
| Leôncio Ferreira Flores Neto | [@LeoncioFerreira](https://github.com/LeoncioFerreira)|
---
# 📌 Descrição do Projeto

Este projeto implementa um **Gerenciador de Cursos e Alunos**, conforme o **Tema 6** da disciplina de Programação Orientada a Objetos (UFCA).

O sistema deverá contemplar:

- Cursos e pré-requisitos  
- Turmas (ofertas) com horários, vagas e status  
- Alunos e históricos  
- Matrículas com regras de pré-requisito, vagas e choque de horário  
- Notas, frequência e situação acadêmica  
- Relatórios gerais (taxa de aprovação, top N alunos, etc.)  

Nesta primeira etapa (Semana 1), o foco é construir a **modelagem inicial**, incluindo:
- UML textual  
- Estrutura de pastas  
- Classes vazias com docstrings de propósito  

---

# 🎯 Objetivo Geral

Criar uma arquitetura orientada a objetos clara, modular e extensível, servindo de base para as entregas progressivas das próximas semanas.

---

# 🧩 UML TEXTUAL

A seguir, a UML textual solicitada pelo professor, contendo **classes, atributos, métodos e relacionamentos**.

---

## **Classe: Pessoa**

### **Atributos**
- nome: str  
- email: str  

### **Métodos**
- `__str__()`  

### **Relacionamentos**
- Superclasse de → Aluno  

---

## **Classe: Aluno (subclasse de Pessoa)**

### **Atributos**
- matricula: str  
- historico: list[Matricula]  

### **Métodos**
- calcular_cr()  
- verificar_prerequisito_cumprido(curso)  
- `__lt__()`  

### **Relacionamentos**
- Subclasse de → Pessoa  
- 1:N com Matricula  

---

## **Classe: Oferta**

### **Atributos**
- id_oferta: str  
- periodo_semestre: str  
- dias_horarios: dict  
- vagas: int  
- status: str  
- local: str (opcional)

### **Métodos**
- abrir()  
- fechar()  
- `__str__()`  

### **Relacionamentos**
- Superclasse de → Turma  

---

## **Classe: Turma (subclasse de Oferta)**

### **Atributos**
- numero_turma: int  
- curso: Curso  
- matriculas: list[Matricula]  

### **Métodos**
- tem_vaga()  
- verificar_choque_horario(aluno)  
- matricular(aluno)  
- calcular_taxa_aprovacao()  
- `__len__()`  

### **Relacionamentos**
- Subclasse de → Oferta  
- 1:1 com Curso  
- 1:N com Matricula  

---

## **Classe: Curso**

### **Atributos**
- codigo: str  
- nome: str  
- carga_horaria: int  
- prerequisitos: list[str]  
- ementa: str (opcional)

### **Métodos**
- validar_prerequisitos()  
- `__str__()`  

### **Relacionamentos**
- 1:N com Turma  

---

## **Classe: Matricula**

### **Atributos**
- aluno: Aluno  
- turma: Turma  
- nota: float  
- frequencia: float  
- situacao: str  

### **Métodos**
- lancar_nota(valor)  
- lancar_frequencia(valor)  
- calcular_situacao(config)  
- trancar(data_atual, config)  
- `__eq__()`  

### **Relacionamentos**
- N:1 com Aluno  
- N:1 com Turma  
- Associação bidirecional Aluno ↔ Turma  

---

## **Classe: Configuracoes**

### **Atributos**
- nota_minima_aprovacao: float  
- frequencia_minima: float  
- data_limite_trancamento: date  
- max_turmas_por_aluno: int  
- top_n_alunos: int  

### **Métodos**
- carregar()  
- salvar()  
- obter_parametro(chave)  

### **Relacionamentos**
- Dependência com Matricula  
- Dependência com Turma  

---

# 🔗 Tabela Resumida de Relacionamentos

| Classe Origem | Tipo de Relação | Classe Destino     | Descrição                                                                 |
|---------------|------------------|----------------------|---------------------------------------------------------------------------|
| Pessoa        | Superclasse      | Aluno               | Aluno herda atributos e comportamentos de Pessoa                         |
| Oferta        | Superclasse      | Turma               | Turma é uma especialização de Oferta                                     |
| Curso         | 1:N              | Turma               | Um Curso pode ter várias Turmas (ofertas)                                 |
| Aluno         | 1:N              | Matricula           | Um Aluno pode ter várias Matrículas                                      |
| Turma         | 1:N              | Matricula           | Uma Turma pode ter várias Matrículas                                     |
| Matricula     | Associação N:N   | Aluno ↔ Turma       | Matricula conecta um Aluno a uma Turma                                   |
| Configuracoes | Dependência      | Matricula           | Matrícula usa Configurações para determinar situações acadêmicas         |
| Configuracoes | Dependência      | Turma               | Turma depende de Configurações para regras de matrícula e limite         |

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

