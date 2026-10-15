# 🎓 Dashboard Acadêmico

### Sistema de acompanhamento e visualização de desempenho acadêmico

O **Dashboard Acadêmico** é uma aplicação web desenvolvida em Python para organizar, acompanhar e analisar notas de disciplinas acadêmicas por meio de gráficos interativos e indicadores de desempenho.

O projeto foi desenvolvido com o objetivo de aplicar conhecimentos de **desenvolvimento de software, análise de dados, visualização de informações e integração com banco de dados em nuvem**.

A aplicação disponibiliza um painel público para consulta dos resultados acadêmicos e uma área administrativa protegida por autenticação.

---

## 🚀 Funcionalidades

### 📊 Visualização de dados
- Consulta de disciplinas e notas acadêmicas.
- Indicadores de média geral, maior nota e quantidade de disciplinas.
- Identificação de disciplinas aprovadas com base na pontuação mínima de 60 pontos.
- Gráfico de evolução e comparação das notas finais.
- Gráfico de desempenho nas avaliações.
- Comparação de notas de exercícios, trabalhos e atividades de progresso.
- Tabelas detalhadas dos registros acadêmicos.

### 🔐 Área administrativa
- Autenticação de usuário pelo Supabase Auth.
- Cadastro de novas disciplinas.
- Definição das notas máximas de cada avaliação.
- Atualização das notas obtidas.
- Exclusão de disciplinas.
- Importação de registros acadêmicos em formato CSV.

### 🌐 Acesso público
- Visualização dos resultados sem necessidade de login.
- Consulta de gráficos e indicadores.
- Interface de somente leitura para visitantes.
- Operações de alteração protegidas por autenticação e políticas de acesso no banco de dados.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| Streamlit | Desenvolvimento da interface web |
| Pandas | Manipulação e organização de dados |
| Plotly Express | Criação de gráficos interativos |
| Supabase | Armazenamento de dados em nuvem |
| PostgreSQL | Banco de dados relacional |
| Supabase Auth | Autenticação de usuários |
| SQL | Consultas e configuração de permissões |
| Git e GitHub | Versionamento e publicação do código |

---

## 🎨 Interface

O dashboard utiliza um tema escuro com predominância de **preto, grafite, vermelho e branco**, priorizando a organização das informações e a leitura dos resultados.

A interface apresenta indicadores acadêmicos, gráficos interativos e um menu lateral com funcionalidades administrativas disponíveis após autenticação.

---

## 🗂️ Estrutura do projeto

```text
dashboard-academico/
│
├── Dashboard_notas.py
├── banco_supabase.py
├── publicar_notas.sql
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml  # Arquivo local, não publicado
```

**Descrição dos principais arquivos:**

- `Dashboard_notas.py`: interface principal, gráficos, indicadores e formulários.
- `banco_supabase.py`: conexão com Supabase, autenticação e operações de banco de dados.
- `publicar_notas.sql`: configuração da visualização pública dos registros acadêmicos.
- `requirements.txt`: dependências necessárias para executar o projeto.
- `.gitignore`: exclusão de arquivos locais e configurações privadas do versionamento.

---

## ⚙️ Executando o projeto localmente

**1. Clone o repositório**

```bash
git clone https://github.com/SEU-USUARIO/dashboard-academico.git
cd dashboard-academico
```

**2. Instale as dependências**

```bash
py -m pip install -r requirements.txt
```

**3. Configure a conexão com o Supabase**

Crie o arquivo `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "URL_DO_PROJETO"
SUPABASE_ANON_KEY = "CHAVE_PUBLICA_DO_PROJETO"
ADMIN_USER_ID = "UID_DO_ADMINISTRADOR"
```

É necessário configurar previamente o banco de dados, a autenticação e as políticas de acesso do Supabase.

**Nunca publique senhas, chaves secretas ou o arquivo `secrets.toml` no repositório.**

**4. Inicie a aplicação**

```bash
py -m streamlit run Dashboard_notas.py
```

A aplicação estará disponível no navegador, normalmente em `http://localhost:8501`.

---

## 🔒 Segurança e controle de acesso

O projeto utiliza autenticação do Supabase e políticas de segurança no PostgreSQL.

A consulta pública é realizada por meio da VIEW `notas_publicas`, enquanto as operações administrativas utilizam a tabela `notas_academicas`.

As permissões de leitura e escrita devem ser configuradas no banco de dados para garantir que visitantes não possam modificar os registros.

---

## 🎯 Objetivo do projeto

O desenvolvimento deste dashboard faz parte da minha trajetória acadêmica em **Análise e Desenvolvimento de Sistemas (ADS)**.

O projeto permitiu colocar em prática conceitos relacionados a:

- Programação em Python.
- Desenvolvimento de aplicações web.
- Integração entre sistemas e banco de dados.
- Análise e visualização de dados.
- Operações CRUD.
- Autenticação e controle de acesso.
- Organização e manutenção de código.

Além de acompanhar meu desempenho acadêmico, o dashboard representa uma experiência prática de desenvolvimento de uma aplicação conectada a serviços em nuvem.

---

## 👨‍💻 Desenvolvedor

**Wenndy Ferreira dos Santos**

Estudante de Análise e Desenvolvimento de Sistemas (ADS), com interesse em desenvolvimento de software, análise de dados e Segurança da Informação.

Projeto desenvolvido para fins acadêmicos e de portfólio profissional.

---

**Python · Streamlit · Pandas · Plotly · PostgreSQL · Supabase**