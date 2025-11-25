# Projeto 1 — Programação Orientada a Objetos

### Tema 6 — Gerenciador de Cursos e Alunos

## 👨‍💻 Autor

| Nome                         | GitHub           |
| ---------------------------- | ---------------- |
| Leôncio Ferreira Flores Neto | [@LeoncioFerreira](https://github.com/LeoncioFerreira)|

---

# 📌 Descrição do Projeto

Este projeto implementa um **Gerenciador de Cursos e Alunos**, conforme o Tema 6 da disciplina de **Programação Orientada a Objetos (UFCA)**.

O sistema deverá contemplar:

* Cursos e pré-requisitos
* Ofertas de disciplinas (turmas) com horários, vagas e status
* Alunos e histórico acadêmico
* Matrículas com validações de pré-requisitos, vagas e choque de horário
* Lançamento de notas e frequência
* Cálculo de situação acadêmica
* Relatórios gerais (taxa de aprovação, top N alunos, etc.)

Na **Semana 2**, o foco é:

✔ Implementar as classes fundamentais  
✔ Usar herança e encapsulamento  
✔ Criar validações robustas  
✔ Implementar métodos especiais  
✔ Desenvolver testes automatizados (pytest)

---

# 🎯 Objetivos da Semana 2

- Estruturar as classes centrais do sistema.  
- Garantir o uso correto de **@property** para encapsulamento.  
- Implementar métodos especiais obrigatórios:
  - `__str__`
  - `__len__`
  - `__eq__`
  - `__lt__`
- Criar testes unitários básicos com pytest.  
- Carregar configurações via JSON.  

Todos os requisitos foram atendidos.

# 🧩 UML TEXTUAL
⚠️ Importante:
Esta UML representa o *planejamento completo* do sistema, incluindo funcionalidades 
que serão adicionadas nas próximas semanas (3, 4 e 5).
Nem todos os métodos mostrados aqui fazem parte da implementação da Semana 2.

A seguir, a UML textual contendo **classes, atributos, métodos e relacionamentos**.

---

## **Classe: Pessoa**

### Atributos

* nome: str
* email: str

### Métodos

* `__str__()`

### Relacionamentos

* Superclasse de → Aluno

---

## **Classe: Aluno (subclasse de Pessoa)**

### Atributos

* matricula: str
* historico: list[Matricula]

### Métodos

* calcular_cr()
* verificar_prerequisito_cumprido(curso)
* `__lt__()`

### Relacionamentos

* Subclasse de → Pessoa
* 1:N com Matricula

---

## **Classe: Curso**

### Atributos

* codigo: str
* nome: str
* carga_horaria: int
* prerequisitos: list[str]
* ementa: str (opcional)

### Métodos

* validar_prerequisitos()
* `__str__()`

### Relacionamentos

* 1:N com Oferta/Turma

---

## **Classe: Oferta**

(Representa uma oferta de disciplina em um semestre – base para Turma)

### Atributos

* codigo_oferta: str
* codigo_curso: str
* semestre: str
* dias_horarios: dict
* vagas: int
* status: str
* local: str | None

### Métodos

* abrir()
* fechar()
* `__str__()`

### Relacionamentos

* Superclasse de → Turma
* N:1 com Curso

---

## **Classe: Turma (subclasse de Oferta)**

(Estende a oferta com comportamento e vínculos com alunos)

### Atributos

* curso: Curso
* matriculas: list[Matricula]

### Métodos

* tem_vaga()
* verificar_choque_horario(aluno)
* matricular(aluno)
* calcular_taxa_aprovacao()
* `__len__()`

### Relacionamentos

* Subclasse de → Oferta
* 1:N com Matricula

---

## **Classe: Matricula**

### Atributos

* aluno: Aluno
* turma: Turma
* nota: float
* frequencia: float
* situacao: str

### Métodos

* lancar_nota(valor)
* lancar_frequencia(valor)
* calcular_situacao(config)
* trancar(data_atual, config)
* `__eq__()`

### Relacionamentos

* N:1 com Aluno
* N:1 com Turma
* Associação Aluno ↔ Turma

---

## **Classe: Configuracoes**

### Atributos

* nota_minima_aprovacao: float
* frequencia_minima: float
* data_limite_trancamento: date
* max_turmas_por_aluno: int
* top_n_alunos: int

### Métodos

* carregar()
* salvar()
* obter_parametro(chave)

### Relacionamentos

* Dependência com Matricula
* Dependência com Turma

---

# 🔗 Tabela Resumida de Relacionamentos

| Classe Origem | Tipo de Relação | Classe Destino  | Descrição                              |
| ------------- | --------------- | --------------- | -------------------------------------- |
| Pessoa        | Superclasse     | Aluno           | Aluno herda atributos e comportamentos |
| Curso         | 1:N             | Oferta/Turma    | Um curso pode ter diversas ofertas     |
| Oferta        | Superclasse     | Turma           | Turma é uma especialização da Oferta   |
| Aluno         | 1:N             | Matricula       | Um aluno pode ter várias matrículas    |
| Turma         | 1:N             | Matricula       | Uma turma pode ter várias matrículas   |
| Matricula     | Associação      | Aluno ↔ Turma   | Relaciona aluno e turma                |
| Configuracoes | Dependência     | Matricula/Turma | Regras acadêmicas                      |

---

# 📁 Estrutura inicial do projeto

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
├── tests/
│   ├── test_aluno.py
│   ├── test_curso.py
│   ├── test_matricula.py
│   └── test_turma.py
│
├── LICENSE
├── pytest.ini
├── requirements.txt
└── README.md

```
## 🚀 Como Executar o Projeto

A seguir estão as instruções completas para instalar dependências, ativar ambiente virtual e executar os testes da Semana 2.

---
### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/LeoncioFerreira/Gerenciador-de-Cursos-e-Alunos.git
cd Gerenciador-de-Cursos-e-Alunos
```
### 2️⃣ Criar ambiente virtual (Opcional, mas recomendado)

Isolar as dependências do projeto evita conflitos com outras bibliotecas instaladas no sistema.

**Linux/MacOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```
***Windows:***

```PowerShell

python -m venv venv
venv\Scripts\activate
```
### 3️⃣ Instalar as dependências
O projeto utiliza o pytest. Certifique-se de que o arquivo requirements.txt esteja na raiz do projeto e execute:

```bash
pip install -r requirements.txt
```
### 4️⃣ Executar os testes automatizados
Para rodar todos os testes com saída detalhada:
```bash
pytest -v
```
Para parar no primeiro erro:
```bash
pytest --maxfail=1
```
