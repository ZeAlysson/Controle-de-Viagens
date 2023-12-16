# Controle de Veículos e motoristas

# 1. Introdução

Este projeto consiste em um sistema de gestão de veículos e motoristas, desenvolvido utilizando o framework Django em Python. A aplicação proporciona funcionalidades para a manutenção de registros e monitoramento das atividades associadas aos veículos e motoristas, incluindo o acompanhamento de suas movimentações e troca de óleo quando necessário.

# 2. Estrutura do Projeto
O projeto está organizado em 3 aplicativos do Django, cada um responsável por uma área específica:

- **controle**: Responsável pela gestão do controle de veículos.
- **motoristas**: Responsável pelo cadastro e gerenciamento de motoristas.
- **veiculos**: Responsável pelo cadastro e gerenciamento de veículos.

# Funcionalidades Principais
### Controle de Veículos
- **Cadastro de Controle:**
  - Permite o cadastro de informações relacionadas a cada viagem, como veículo utilizado, motorista, data e hora de saída e retorno, quilometragem percorrida, etc.
- **Listagem de Controles:**
  - Apresenta uma lista de todos os controles realizados, exibindo informações resumidas.
- **Edição e Exclusão de Controle:**
  - Possibilita a edição e exclusão de registros existentes.

### Cadastro de Motoristas
- **Cadastro de Motorista:**
  - Permite o cadastro de informações sobre motoristas, incluindo nome, telefone, CNH, etc.
- **Listagem de Motoristas:**
  - Apresenta uma lista de todos os motoristas cadastrados.
- **Edição e Exclusão de Motorista:**
  - Permite editar as informações de um motorista existente e também excluí-lo.

## Cadastro de Veículos
- **Cadastro de Veículo:**
  - Permite o cadastro de informações sobre veículos, incluindo placa, marca, modelo, etc.
- **Listagem de Veículos:**
  - Apresenta uma lista de todos os veículos cadastrados.
- **Edição e Exclusão de Veículo:**
  - Permite editar as informações de um veículo existente e também excluí-lo.

# 3. Tecnologias Utilizadas
- Linguagem de Programação: Python
- Framework Web: Django
- Banco de Dados: MySQL
- Frontend: HTML, CSS, Bootstrap
- Controle de Versão: Git


Com o objetivo de simplificar testes e demais processos, o projeto está utilizando o banco de dados SQLite. Vale ressaltar que, para ambientes de produção ou aplicações em larga escala, é altamente recomendável considerar a migração para bancos de dados mais robustos, como MySQL.

# 4. Crie e ative um ambiente virtual para isolar as dependências do projeto:

- **Windows**

```sh
python -m venv venv
venv\Scripts\activate
```

- **Linux**

```sh
python -m venv venv
source venv/bin/activate
```

# 6. Configuração do Ambiente de Desenvolvimento
Siga os passos abaixo para configurar e executar o projeto:
1. Clone o repositório para sua máquina local. `https://github.com/gnneto/django_ag_test.git`
2. Configure o ambiente virtual e instale as dependências utilizando `pip install -r requirements.txt`.
3. Execute as migrações do banco de dados com `python manage.py migrate`.
4. Crie um superusuário com `python manage.py createsuperuser`.
5. Inicie o servidor de desenvolvimento com `python manage.py runserver`.

Para evitar problemas com o banco de dados, é necessário migrar os modelos de cada aplicativo separadamente para evitar conflitos inesperados no banco de dados. Siga os passos abaixo:

1. Migrar modelos do aplicativo Controle:
   ```sh
   python manage.py makemigrations controle
   ```
2. Migrar modelos do aplicativo Motoristas:
   ```sh
   python manage.py makemigrations motoristas
   ```
3. Migrar modelos do aplicativo Veículos:
   ```sh
   python manage.py makemigrations veiculos
   ```
4. Aplicar as migrações:
   ```sh
   python manage.py migrate
   ```
## Requisitos:
- Python
- Django
- MySQL
