# Secretly API

API simples para gerenciamento de amigo secreto desenvolvida com FastAPI, SQLAlchemy e SQLite3.

## Funcionalidades

- **Gestão de Grupos**: Criar e gerenciar grupos de amigo secreto
- **Participantes**: Adicionar e gerenciar participantes dos grupos  
- **Sorteios**: Realizar sorteios automáticos e justos
- **API RESTful**: Endpoints simples e bem documentados

## Pré-requisitos

### Opção 1: Docker (Recomendado)
- Docker
- Docker Compose

### Opção 2: Instalação Manual
- Python 3.8+
- pip
- SQLite3 (já vem com Python)

## Executando com Docker

A forma mais fácil de executar a aplicação é usando Docker Compose:

1. **Clone o repositório**
```bash
git clone <seu-repositorio>
cd secretly-api
```

2. **Execute com Docker Compose**
```bash
docker-compose up --build
```

Isso irá:
- Criar e iniciar o container da API FastAPI
- Inicializar o banco de dados SQLite automaticamente
- Disponibilizar a API em `http://localhost:8000`

3. **Acesse a documentação**
```
http://localhost:8000/docs
```

### Comandos úteis do Docker

```bash
# Iniciar em background
docker-compose up -d

# Parar os containers
docker-compose down

# Parar e remover volumes (limpar banco de dados)
docker-compose down -v

# Ver logs
docker-compose logs -f web

# Reconstruir após mudanças
docker-compose up --build
```

## 🛠️ Instalação Manual

1. **Clone o repositório**
```bash
git clone <seu-repositorio>
cd secretly-api
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados (opcional)**
```bash
# Copie o arquivo de exemplo
cp env.example .env

# O SQLite é usado por padrão, mas você pode personalizar:
# DATABASE_URL=sqlite:///./secretly.db
```

5. **Inicialize o banco de dados**
```bash
python init_db.py
```

6. **Execute a aplicação**
```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## Como usar

### 1. Criar um grupo
```bash
POST /api/v1/groups
{
  "name": "Amigo Secreto da Família",
  "description": "Sorteio de Natal 2024"
}
```

### 2. Adicionar participantes
```bash
POST /api/v1/participants
{
  "name": "João Silva",
  "email": "joao@email.com",
  "group_id": 1
}
```

### 3. Realizar o sorteio
```bash
POST /api/v1/draws/group/1/perform
```

### 4. Ver resultados
```bash
GET /api/v1/draws/group/1
```

## Estrutura do Projeto

```
app/
├── api/v1/          # Endpoints da API
├── crud/           # Operações de banco de dados
├── db/             # Configuração do banco
├── models/         # Modelos SQLAlchemy
├── schemas/        # Schemas Pydantic
└── main.py         # Aplicação principal
```

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para Python
- **SQLite3**: Banco de dados relacional embutido
- **Pydantic**: Validação de dados

## Endpoints Principais

### Grupos
- `GET /api/v1/groups` - Listar grupos
- `POST /api/v1/groups` - Criar grupo
- `GET /api/v1/groups/{id}` - Buscar grupo
- `PUT /api/v1/groups/{id}` - Atualizar grupo
- `DELETE /api/v1/groups/{id}` - Deletar grupo

### Participantes
- `GET /api/v1/participants` - Listar participantes
- `POST /api/v1/participants` - Adicionar participante
- `GET /api/v1/participants/group/{group_id}` - Participantes do grupo
- `PUT /api/v1/participants/{id}` - Atualizar participante
- `DELETE /api/v1/participants/{id}` - Remover participante

### Sorteios
- `POST /api/v1/draws/group/{group_id}/perform` - Realizar sorteio
- `GET /api/v1/draws/group/{group_id}` - Sorteios do grupo
- `GET /api/v1/draws/group/{group_id}/summary` - Resumo dos sorteios
