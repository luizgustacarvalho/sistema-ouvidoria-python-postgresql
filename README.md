Sistema de Ouvidoria com Python e PostgreSQL
Sobre o Projeto
O Sistema de Ouvidoria é uma aplicação desenvolvida em Python para registrar, acompanhar e gerenciar reclamações. O projeto foi criado com foco no aprendizado de Programação Orientada a Objetos (POO), integração com banco de dados PostgreSQL e boas práticas de desenvolvimento.

O sistema permite que usuários registrem reclamações e que supervisores acompanhem o andamento dos chamados, alterem status e consultem estatísticas operacionais.

Tecnologias Utilizadas
Python 3
PostgreSQL 18
Psycopg
Python Dotenv
Pytest
Programação Orientada a Objetos (POO)
Funcionalidades
Área do Usuário
Registro de reclamações
Seleção de categorias
Validação de campos obrigatórios
Geração automática de protocolo
Armazenamento das informações no PostgreSQL
Área do Supervisor
Autenticação por senha
Consulta de reclamações
Busca por protocolo
Alteração de status
Controle de reclamações pendentes
Controle de reclamações em andamento
Controle de reclamações resolvidas
Visualização de estatísticas
Controle de Prazo
Prazo interno de 5 dias úteis
Cálculo automático de data limite
Exclusão de finais de semana da contagem
Consideração de feriados cadastrados
Identificação automática de chamados atrasados
Alertas de prazo para supervisão
Estrutura do Projeto
Projeto-ouvidoria/
│
├── banco_dados.py
├── feriados.py
├── main.py
├── reclamações.py
├── supervisor.py
│
├── tests/
│   ├── test_feriados.py
│   └── test_reclamações.py
│
├── requirements.txt
├── .env
└── .gitignore
Conceitos Aplicados
Programação Orientada a Objetos
Classes e Objetos
Encapsulamento
Tratamento de Exceções
Persistência de Dados
SQL
PostgreSQL
Testes Automatizados com Pytest
Organização Modular de Código
Testes
O projeto possui testes automatizados para:

Validação de chamados
Validação de categorias
Validação de descrições
Cálculo de dias úteis
Tratamento de finais de semana
Tratamento de feriados
Objetivo do Projeto
Este projeto foi desenvolvido como parte da minha formação em tecnologia com o objetivo de praticar o desenvolvimento de aplicações em Python utilizando banco de dados relacional, Programação Orientada a Objetos e regras de negócio aplicadas a um cenário real de atendimento e ouvidoria.

Autor
Luiz Gustavo da Silva Carvalho

GitHub: https://github.com/luizgustacarvalho

LinkedIn: www.linkedin.com/in/luiz-gustavo-carvalho-b105b9411