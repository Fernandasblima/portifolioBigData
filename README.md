    Introdução

    ✅ A empresa de comércio eletrônico E-Shop Brasil está em processo de modernização de sua infraestrutura digital e precisa de uma solução prática para gerenciar informações de forma eficiente e escalável. A proposta é desenvolver uma aplicação que permita realizar operações CRUD (Criar, Ler, Atualizar e Deletar) de dados relevantes para a empresa — como produtos, pedidos ou clientes — utilizando MongoDB como banco de dados NoSQL. 

   Descrição do Projeto

 ✅  Uso do Docker
É utilizado para criar um ambiente de desenvolvimento isolado e replicável, evitando problemas de compatibilidade de dependências entre diferentes sistemas operacionais.
A orquestração é realizada com docker-compose, que sobe dois containers:

MongoDB: banco de dados NoSQL para armazenar os dados.


Aplicação Streamlit: interface web que interage com o banco.


✅ Descrição da Aplicação (app.py)
A aplicação desenvolvida com Streamlit permite:
Conectar-se automaticamente ao container MongoDB.


Realizar as seguintes operações:


⭕Inserção: Geração e inserção de dados sintéticos para clientes, produtos e pedidos.


⭕Manipulação: Exclusão de registros pelo ID.

⭕Atualização: Atualização dos dados gerados.