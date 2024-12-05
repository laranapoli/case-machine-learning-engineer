# MLE Case - Machine Learning Engineer

Este projeto é uma API FastAPI para servir modelos de machine learning, obter predições, bem como retornar o histórico delas. O código foi containerizado usando Docker e pode ser executado e implantado com facilidade através de comandos `task`.

## Requisitos

Antes de rodar o projeto, garanta que você tenha as seguintes ferramentas instaladas:

- [Python 3.10+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Task](https://taskfile.dev/)
- [Poetry](https://python-poetry.org/)

## Comandos principais

### Deploy da aplicação
Para fazer o deploy da aplicação em um container:
```bash
task deploy
```

### Logs do container
Para visualizar os logs do container:
```bash
task logs-container
```

### Limpeza do ambiente
Para parar e remover o container, execute o comando:
```bash
task clean
```

### Rodar os testes

Execute o seguinte comando para rodar os testes da aplicação:

```bash
task test
```

### Build e execução do container
- Para criar a imagem Docker, execute:
```bash
task build-container
```

- Para rodar o container em segundo plano:
```bash
task run-container
```

- Para parar o container:
```bash
task stop-container
```

- Para remover o container:
```bash
task remove-container
```

## Estrutura de Diretórios
- `src/`: Código-fonte da aplicação.
- `tests/`: Testes da aplicação.
- `Dockerfile`: Arquivo Docker para containerização.
- `pyproject.toml`: Gerenciamento de dependências com Poetry.