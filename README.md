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


## 🎯 Status do Desenvolvimento: Semana 3 (Concluída)

A entrega desta semana focou em **herança**, **relacionamentos** e **persistência**.

### ✔ 1. Herança funcional
* `Pessoa` → `Aluno`
* `Oferta` → `Turma`

### ✔ 2. Relacionamentos entre classes
A classe `Matricula` gerencia a ligação **Aluno ↔ Turma**, validando:
* Vagas disponíveis
* Choque de horário
* Status da turma (`ABERTA`/`FECHADA`)

### ✔ 3. Persistência simples (JSON)
Módulo `persistencia.py` implementado com:
* `salvar_*()` e `carregar_*()`
* Estrutura padronizada em `data/*.json`

### ✔ 4. Relatório básico
A função `alunos_por_turma(turma)` gera listagem contendo:
* Nome, Matrícula, Nota e Frequência

### ✔ 5. Testes automatizados (pytest)
Cobertura de testes para:
* **Aluno:** CR e método `__lt__`
* **Curso:** Validações e `__str__`
* **Turma:** Vagas, `__len__`, matrícula
* **Matricula:** Validação e igualdade (`__eq__`)
* **Sistema:** Fluxo de matrícula, tratamento de erros e relatórios
* **Persistência:** Leitura e escrita de JSON

---

# 🧩 UML TEXTUAL
⚠️ Importante:
Esta UML representa o *planejamento completo* do sistema, incluindo funcionalidades 
que serão adicionadas nas próximas semanas (4 e 5).

A seguir, a UML textual contendo **classes, atributos, métodos e relacionamentos**.

---

## **Classe: Pessoa**

### **Atributos**

* `nome: str`
* `email: str`

### **Métodos**

* `__str__()`

### **Relacionamentos**

* **Superclasse de → Aluno**

---

## **Classe: Aluno (subclasse de Pessoa)**

### **Atributos**

* `matricula: str`
* `historico: list[Matricula]`
* `matriculas_ativas: list[Matricula]`

### **Métodos (atuais + futuros)**

* `adicionar_ao_historico(matricula)`
* `adicionar_matricula_ativa(matricula)`
* `tem_choque(nova_turma)` *(choque é verificado aqui agora)*
* `calcular_cr()`
* `verificar_prerequisito_cumprido(curso)` *(futuro)*
* `__lt__(other)`

### **Relacionamentos**

* **Subclasse de Pessoa**
* **1:N com Matricula**

---

## **Classe: Curso**

### **Atributos**

* `codigo: str`
* `nome: str`
* `carga_horaria: int`
* `pre_requisitos: list[str]`

### **Métodos (atuais + futuros)**

* `validar_prerequisitos()` *(futuro)*
* `__str__()`

### **Relacionamentos**

* **1:N com Turma**

---

## **Classe: Oferta**

*(classe base para Turma)*

### **Atributos**

* `codigo_oferta: str`
* `codigo_curso: str`
* `semestre: str`
* `dias_horarios: dict[str, list[(inicio, fim)]]`
* `vagas: int`
* `status: str`
* `local: str | None`

### **Métodos**

* `abrir()`
* `fechar()`
* `__str__()`

### **Relacionamentos**

* **Superclasse de Turma**
* **N:1 com Curso**

---

## **Classe: Turma (subclasse de Oferta)**

### **Atributos**

* `curso: Curso`
* `matriculas: list[Matricula]`

### **Métodos (atuais + futuros)**

* `tem_vaga()`
* `matricular(matricula)`
* `__len__()`
* `__str__()`
* `calcular_taxa_aprovacao()` *(futuro)*
* `calcular_distribuicao_notas()` *(futuro)*

### **Relacionamentos**

* **Subclasse de Oferta**
* **1:N com Matricula**

---

## **Classe: Matricula**

### **Atributos**

* `aluno: Aluno`
* `turma: Turma`
* `nota: float | None`
* `frequencia: float | None`
* `situacao: str` *(futuro)*

### **Métodos (atuais + futuros)**

* `lancar_nota(valor)` *(futuro)*
* `lancar_frequencia(valor)` *(futuro)*
* `calcular_situacao(config)` *(futuro)*
* `trancar(data_atual, config)` *(futuro)*
* `__eq__()`
* `__str__()`

### **Relacionamentos**

* **N:1 com Aluno**
* **N:1 com Turma**
* **Associação Aluno ↔ Turma**

---

## **Classe: Configuracoes**

### **Atributos**

* `nota_minima_aprovacao`
* `frequencia_minima`
* `data_limite_trancamento`
* `max_turmas_por_aluno`
* `top_n_alunos`

### **Métodos (atuais + futuros)**

* `carregar()`
* `salvar()`
* `obter_parametro(chave)` *(futuro)*

### **Relacionamentos**

* **Dependência com Matricula**
* **Dependência com Sistema**

---



# 🔗 Tabela Resumida de Relacionamentos

| Classe Origem | Tipo de Relação | Classe Destino  | Descrição |
|---------------|------------------|------------------|-----------|
| Pessoa        | Superclasse      | Aluno            | Aluno herda nome, email e validações de Pessoa |
| Curso         | 1:N              | Turma            | Um curso pode ter várias turmas ofertadas |
| Oferta        | Superclasse      | Turma            | Turma é uma especialização da classe Oferta |
| Aluno         | 1:N              | Matricula        | Um aluno possui várias matrículas (ativas e no histórico) |
| Turma         | 1:N              | Matricula        | Uma turma possui várias matrículas dos alunos inscritos |
| Matricula     | Associação       | Aluno ↔ Turma    | Matrícula conecta aluno e turma de forma bidirecional |
| Configuracoes | Dependência      | Matricula        | Matrícula usa regras acadêmicas definidas em Configuracoes |

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
│   ├── persistencia.py
│   ├── sistema.py
│   └── turma.py
│
├── tests/
│   ├── test_aluno.py
│   ├── test_curso.py
│   ├── test_matricula.py
│   ├── test_sistema.py
│   ├── test_turma.py
│   ├── test_persistencia.py 
│
├── LICENSE
├── pytest.ini
├── requirements.txt
└── README.md

```
## 🚀 Como Executar o Projeto

A seguir estão as instruções completas para instalar dependências, ativar ambiente virtual e executar os testes da Semana 3.

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
