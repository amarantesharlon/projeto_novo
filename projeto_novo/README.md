# projeto_novo

Este projeto utiliza Docker para orquestrar um contêiner PostgreSQL.

## Estrutura do Projeto

- **Dockerfile1**: Define uma imagem Docker baseada na versão 17.5 do PostgreSQL, com o comando padrão configurado para executar o servidor PostgreSQL.
- **docker-compose.yml**: Orquestra os serviços definidos no Dockerfile, especificando a configuração para executar o contêiner PostgreSQL, incluindo variáveis de ambiente, portas e mapeamentos de volume.
- **README.md**: Este arquivo contém a documentação do projeto, fornecendo uma visão geral e instruções para configuração e uso.

## Instruções de Uso

1. **Pré-requisitos**: Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.
2. **Construir a Imagem**: Execute o comando abaixo para construir a imagem Docker a partir do Dockerfile:
   ```
   docker build -t meu_postgres .
   ```
3. **Executar o Contêiner**: Utilize o Docker Compose para iniciar o contêiner:
   ```
   docker-compose up
   ```
4. **Acessar o PostgreSQL**: Após o contêiner estar em execução, você pode acessar o PostgreSQL na porta especificada no arquivo `docker-compose.yml`.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.