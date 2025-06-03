# Projeto IDA Telecom




Este projeto automatiza o download, extração e armazenamento dos dados do Índice de Desempenho no Atendimento (IDA) das operadoras de telecomunicações do Brasil, utilizando Python, Pandas e PostgreSQL.

## Objetivos

- Baixar todos os arquivos ODS do portal de dados abertos da Anatel.
- Converter os dados para CSV.
- Criar tabelas dinâmicas no PostgreSQL para cada aba de cada arquivo ODS.
- Salvar os arquivos ODS e CSV em pastas organizadas.

## Pré-requisitos
1 - Tenha o Docker Compose instalado em seu computador
2 - Navegador WEB, para visualizar e gerenciar os seus comandos
3 - Um Editor de Texto de sua preferência. Eu uso o Visual Studio!
4 - Para rodar este projeto siga as instruções em como rodar este projeto .

## Algumas observações 

Na pasta View está uma consulta que cria a VIEW que calcula a taxa de variação e a diferença entre a média e os valores individuais dos grupos econômicos.

Na pasta SQL estão algumas consultas:  Criação Data Mart baseado no modelo estrela para organizar os dados e criar a VIEW que calcula a taxa de variação e a diferença entre a média e os valores individuais dos grupos econômicos.

Obs:  Tanto o Data Mart quanto a view precisa ser populada pelas tabelas para encontrar os resultados esperados .


## Tecnologias utilizadas

<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="Python" width="60" height="60"/>
  &nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" alt="PostgreSQL" width="60" height="60"/>
  &nbsp;&nbsp;
  
