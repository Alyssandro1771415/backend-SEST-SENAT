# Backend SEST SENAT

API backend para análise de dados de atendimentos, relatórios de saúde e personas do SEST SENAT. Este projeto fornece endpoints para análises panorâmicas, relatórios de saúde, qualidade de vida e personas regionais/nacionais.

## 📋 Pré-requisitos

- Python 3.11+
- pip (gerenciador de pacotes Python)

## 🚀 Configuração do Ambiente

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd backend-SEST-SENAT
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
```

### 3. Ative o ambiente virtual
**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:

```bash
cp .env.example .env
```

### Variáveis de Ambiente:

```env
# Configurações do servidor
HOST=localhost
PORT_SERVER=5000
WORKERS=1

# Ambiente (development ou production)
ENVIRONMENT=development

# URLs
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:5000
```

### Para Produção:
```env
ENVIRONMENT=production
HOST=0.0.0.0
WORKERS=4
FRONTEND_URL=https://seu-frontend.com
BACKEND_URL=https://sua-api.com
```

## 📁 Estrutura de Arquivos de Dados

### Pasta `db/`

A pasta `db/` deve conter os seguintes arquivos de dados **obrigatórios**:

#### Arquivos CSV (separador: `|`, encoding: `utf-8`)
- **`Atendimentos_SEST_SENAT.csv`** - Dados de atendimentos para análises panorâmicas
- **`Relatorio_de_saude.csv`** - Dados de relatórios de saúde
- **`Relatorio_de_saude_2025.csv`** - Dados de relatórios de saúde para 2025

#### Arquivo Excel
- **`Perfis_SEST_SENAT_2025.xlsx`** - Dados de personas com as seguintes abas:
  - `nacional`
  - `regional`
  - `nacional_doencas`
  - `regional_doencas`
  - `nacional_ocupacional`
  - `regional_ocupacional`

#### Pasta de Imagens
- **`db/PERSONAS/`** - Pasta contendo as imagens das personas em formato PNG
  - As imagens devem seguir o padrão: `{NOME} - Cluster 0 {GENERO}.png`
  - Exemplo: `BEATRIZ - Cluster 0 Feminino.png`

### Estrutura completa da pasta `db/`:
```
db/
├── Atendimentos_SEST_SENAT.csv
├── Relatorio_de_saude.csv
├── Relatorio_de_saude_2025.csv
├── Perfis_SEST_SENAT_2025.xlsx
└── PERSONAS/
    ├── BEATRIZ - Cluster 0 Feminino.png
    ├── CARLOS - Cluster 0 Masculino.png
    ├── CLÁUDIO - Cluster 0 Masculino.png
    ├── JOÃO - Cluster 0 Masculino.png
    ├── MARINA - Cluster 0 Feminino.png
    ├── MÁRCIA - Cluster 0 Feminino.png
    ├── PAULO - Cluster 0 Masculino.png
    ├── PEDRO - Cluster 0 Masculino.png
    ├── RENATA - Cluster 0 Feminino.png
    ├── ROBERTO - Cluster 0 Masculino.png
    ├── SANDRA - Cluster 0 Feminino.png
    └── VERA - Cluster 0 Feminino.png
```

## 🏃‍♂️ Executando o Projeto

### Desenvolvimento Local
```bash
python server.py
```

O servidor será iniciado em `http://localhost:5000` (ou conforme configurado no `.env`)

### Docker - Desenvolvimento
```bash
docker build -t backend-sest-senat .
docker run -p 5000:5000 --env-file .env backend-sest-senat
```

### Docker - Produção
```bash
# Usando docker-compose (recomendado)
docker-compose up -d

# Ou manualmente
docker build -t backend-sest-senat .
docker run -d \
  --name backend-sest-senat \
  -p 5000:5000 \
  -e ENVIRONMENT=production \
  -e HOST=0.0.0.0 \
  -e WORKERS=4 \
  -v $(pwd)/db:/app/db:ro \
  -v $(pwd)/cache:/app/cache \
  --restart unless-stopped \
  backend-sest-senat
```

### Verificar Status
```bash
# Com docker-compose
docker-compose ps

# Logs
docker-compose logs -f

# Parar serviços
docker-compose down
```

## 📚 Endpoints da API

### Análises Panorâmicas
- **GET** `/consultation_analyses/{regiao}` - Análises de atendimentos por região

### Relatórios de Saúde
- **GET** `/health_report/{regiao}` - Relatórios de saúde por região

### Qualidade de Vida
- **GET** `/lifestyle_quality/{regiao}` - Dados de qualidade de vida por região

### Personas
- **GET** `/general_personas/{regiao}` - Personas gerais por região

### Imagens das Personas
- **GET** `/db/PERSONAS/{nome_arquivo}.png` - Acesso às imagens das personas

### Parâmetros de Filtro Disponíveis
- `unidade` - Unidade de atendimento
- `ano` - Ano do atendimento
- `idade` / `faixa_etaria` - Faixa etária
- `genero` / `sexo` - Gênero
- `conselho` - Conselho regional
- `estado` - Estado (UF)
- `modal` - Modal de atendimento
- `cnpj` - CNPJ da empresa
- `nome_empresa` - Nome da empresa

## 🔧 Funcionalidades

### Sistema de Cache
- Cache automático para otimização de performance
- Pré-carregamento de dados mais utilizados
- Armazenamento em `cache/cache_data.json`

### Processamento de Dados
- Leitura e processamento de arquivos CSV e Excel
- Formatação automática de chaves de dados
- Cálculos estatísticos e tendências
- Previsões de atendimentos

### Servir Imagens
- Endpoint estático para servir imagens das personas
- Integração automática com URLs do frontend

## 🏗️ Arquitetura

### Controllers
- `GeneralPersonasController` - Gerencia dados de personas
- `HealthReportController` - Processa relatórios de saúde
- `LifestyleQualityController` - Analisa qualidade de vida
- `PanoramicAnalysesController` - Realiza análises panorâmicas

### Services
- `CacheService` - Gerenciamento de cache
- `FiltersService` - Processamento de filtros
- `FormatationService` - Formatação de dados

### Models
- `ConsultationsModel` - Modelo de consultas
- `PatientModel` - Modelo de pacientes

## 🚀 Deploy em Produção

### Configurações Recomendadas para Produção

1. **Variáveis de Ambiente:**
   ```env
   ENVIRONMENT=production
   HOST=0.0.0.0
   WORKERS=4
   ```

2. **Recursos do Sistema:**
   - CPU: 2+ cores
   - RAM: 4GB+ (devido ao processamento de dados com pandas)
   - Armazenamento: 10GB+ (para dados e cache)

### Deploy com Docker Compose (Recomendado)

1. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o .env com valores de produção
   ```

2. Execute o deploy:
   ```bash
   docker-compose up -d
   ```

3. Verifique o status:
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

## 🐛 Troubleshooting

### Erro: Arquivo não encontrado
Verifique se todos os arquivos obrigatórios estão na pasta `db/` com os nomes exatos especificados.

### Erro: Encoding
Certifique-se de que os arquivos CSV estão salvos com encoding UTF-8 e separador `|`.

### Erro: Pandas/Excel
Verifique se o arquivo Excel possui todas as abas necessárias com os nomes corretos.

### Erro: Imagens não carregam
Confirme se as imagens estão na pasta `db/PERSONAS/` e seguem o padrão de nomenclatura correto.

### Erro: Container não inicia
- Verifique se a porta 5000 não está em uso
- Confirme se os volumes estão montados corretamente
- Verifique os logs: `docker-compose logs`

### Performance em Produção
- Ajuste o número de workers conforme CPU disponível
- Monitore uso de memória (pandas consome bastante RAM)
- Configure cache adequadamente

## 📝 Logs

O sistema exibe logs coloridos para facilitar o debug:
- 🔴 Vermelho: Controller de personas
- 🟢 Verde: Controller de relatórios de saúde
- 🟣 Roxo: Controller de qualidade de vida
- 🔵 Azul: Controller de análises panorâmicas
- 🟡 Amarelo: Sistema de cache


## Observações

projeto teve continuidade posterior e alterações, essas foram realizadas no repositório da organização do projeto do SEST SENAT e não está disponível para público.
