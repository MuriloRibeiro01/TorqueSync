# 🚗 TorqueSync - Sistema de Gestão de Frota para Locadoras

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

O TorqueSync é uma aplicação web completa para a gestão inteligente de frotas de veículos. Este repositório contém o **backend** da aplicação, uma API RESTful construída com Python e Flask.

**➡️ O frontend, construído com React, está em seu próprio repositório e pode ser encontrado [aqui](https://github.com/MuriloRibeiro01/torquesync-frontend).**

## ✨ A História por Trás do Projeto

A ideia do TorqueSync nasceu de uma necessidade real: ajudar meu pai a gerenciar sua locadora de veículos de forma mais eficiente. O controle manual em planilhas e anotações dificultava a visão geral do negócio, o rastreamento de manutenções e a análise de custos e receitas.

Este projeto é a solução para esse desafio. Uma ferramenta criada para ser o braço direito do gestor da frota, centralizando todas as informações cruciais do negócio: desde o status de cada carro até a lucratividade que cada um gera. É um projeto de pai e filho que une tecnologia e empreendedorismo.

## 🚀 Status e Funcionalidades do Projeto

### O que já foi feito (Fases Concluídas):
- [X] Levantamento e definição completa dos requisitos do sistema (modelo de locadora).
- [X] Modelagem e criação do banco de dados relacional (MySQL) com todas as tabelas e relacionamentos.
- [X] Configuração inicial do ambiente de desenvolvimento com Python e Flask.
- [X] Inserção de dados de teste para simular um ambiente real de produção.

### Funcionalidades Planejadas (Roadmap):

O objetivo é criar um sistema robusto e intuitivo. As funcionalidades serão desenvolvidas nos seguintes módulos:

#### Módulo 1: Gestão da Frota
- [ ] Cadastro completo de veículos com status (`Disponível`, `Alugado`, `Em Manutenção`).
- [ ] Edição e visualização dos detalhes de cada veículo.

#### Módulo 2: Gestão de Operações
- [ ] Cadastro de clientes (locatários).
- [ ] Criação e gerenciamento de registros de locação (aluguéis).
- [ ] Registro de devolução com atualização de quilometragem.
- [ ] Registro de manutenções detalhadas com custos associados.

#### Módulo 3: Gestão de Estoque
- [ ] Cadastro de peças e controle de quantidade em estoque.
- [ ] Baixa automática de peças ao registrar uma manutenção.
- [ ] Alertas visuais para itens com estoque baixo.

#### Módulo 4: Inteligência e Relatórios
- [ ] Dashboard principal com visão geral da frota e alertas.
- [ ] Cálculo e notificação de próximas manutenções preventivas.
- [ ] Relatório de lucratividade por veículo (Receita vs. Custo).
- [ ] (Upgrade Futuro) Geração de contratos de locação em PDF.

## 🖥️ Telas do Sistema

*(Seção em construção! Em breve, os primeiros wireframes e protótipos do TorqueSync aparecerão aqui, mostrando a cara da nossa aplicação.)*

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python com o micro-framework Flask.
* **Banco de Dados:** MySQL.
* **Frontend:** HTML5, CSS3 e JavaScript.
* **Gerenciamento de Dependências:** Pip.

## ⚙️ Como Rodar o Projeto Localmente

**Pré-requisitos:**
* Python 3.8+
* Git
* Servidor MySQL

```bash
# 1. Clone o repositório
$ git clone [https://github.com/seu-usuario/TorqueSync.git](https://github.com/seu-usuario/TorqueSync.git)

# 2. Navegue até o diretório do projeto
$ cd TorqueSync

# 3. Crie e ative um ambiente virtual (venv)
$ python -m venv venv
$ source venv/bin/activate  # No Windows, use `venv\Scripts\activate`

# 4. Instale as dependências do projeto
# (O arquivo requirements.txt será criado em breve)
$ pip install Flask mysql-connector-python flask-cors

# 5. Configure o Banco de Dados
# - Certifique-se de que seu servidor MySQL está rodando.
# - Crie um novo banco de dados (schema) com o nome 'database_torquesync'.
# - Execute o script 'database/schema.sql' para criar todas as tabelas.
# - (Opcional) Execute o script 'database/data.sql' para popular o banco com dados de teste.
# - Altere suas credenciais do banco no arquivo app.py.

# 6. Rode a aplicação
$ flask run

## 🤝 Como Contribuir

Este é um projeto em desenvolvimento. Sinta-se à vontade para abrir uma **Issue** para relatar bugs ou sugerir novas funcionalidades. Pull Requests são bem-vindos!

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
Feito com ☕, código e a ambição da "Operação TorqueSync GT" por **Murilo Ribeiro da Silveira**.
