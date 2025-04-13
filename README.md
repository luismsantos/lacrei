# 📚 Lacrei Saúde API - Documentação

## 👀 Visão Geral

Lacrei Saúde é uma API REST desenvolvida com Django para gerenciamento de profissionais de saúde e consultas médicas. A aplicação permite cadastrar profissionais com suas especialidades e agendar consultas para pacientes, facilitando o gerenciamento de atendimentos em ambientes médicos.

## 🐳 Setup com Docker

### Requisitos

- Docker
- Docker Compose

### Instruções para Rodar o Projeto

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/lacrei-saude.git
cd lacrei-saude
```

2. Execute o docker-compose para construir e iniciar a aplicação:

```bash
docker-compose up --build
```

3. A API estará disponível em `http://localhost:8000`
4. Para executar em segundo plano:

```bash
docker-compose up -d
```

5. Para visualizar os logs da aplicação:

```bash
docker-compose logs -f app
```


## 🚀 Endpoints da API

### Profissionais

#### Listar todos os profissionais

```
GET /api/profissionais/
```

#### Cadastrar novo profissional

```
POST /api/profissionais/
```

#### Detalhes de um profissional

```
GET /api/profissionais/{id}/
```

**Descrição**: Retorna detalhes do profissional, incluindo suas consultas agendadas

#### Atualizar profissional

```
PATCH /api/profissionais/{id}/
```

#### Excluir profissional

```
DELETE /api/profissionais/{id}/
```


### Consultas

#### Listar todas as consultas

```
GET /api/consultas/
```

#### Agendar nova consulta

```
POST /api/consultas/
```

#### Detalhes de uma consulta

```
GET /api/consultas/{id}/
```

**Descrição**: Retorna detalhes completos da consulta

#### Atualizar consulta

```
PATCH /api/consultas/{id}/
```

#### Excluir consulta

```
DELETE /api/consultas/{id}/
```


## 🧪 Testes

O projeto utiliza `APITestCase` do Django REST Framework para testes de integração. Para executar os testes:

```bash
docker-compose run app python manage.py test
```

### Exemplos de Testes Implementados

1. **Testes de Profissionais**:
    - Criação de profissionais com dados válidos
    - Validação da idade mínima (18 anos)
    - Atualização e remoção de profissionais
2. **Testes de Consultas**:
    - Agendamento de consultas
    - Validação de datas futuras para consultas
    - Atualização de status de consultas
    - Listagem de consultas por profissional


## 🧠 Decisões Técnicas

1. **Docker e Docker Compose**
    - Adotados para facilitar o setup do ambiente e garantir consistência entre ambientes de desenvolvimento
    - Uso de volumes para persistência de dados do PostgreSQL
2. **Django + DRF**
    - Framework Django escolhido pela robustez, segurança e comunidade ativa
    - Django REST Framework para facilitar a criação de API RESTful
3. **Validações Personalizadas**
    - Implementada validação de idade mínima (18 anos) para profissionais
    - Validação que impede agendamento de consultas no passado
    - Suporte a múltiplos formatos de data para melhor experiência do usuário
4. **Serialização Flexível**
    - Serializers diferentes para listagem e detalhes
    - Suporte a formatos de data brasileiros (DD/MM/YYYY)
    - Campos calculados para enriquecer as respostas da API
5. **Otimizações de Consulta**
    - Uso de `select_related` e `prefetch_related` para reduzir queries N+1
    - Ordenação padrão de consultas para melhorar a experiência do usuário
6. **Documentação com Swagger**
    - Implementação do drf-yasg para gerar documentação interativa da API
    - Anotações nos endpoints para melhorar a documentação


## 🔍 Erros Encontrados e Melhorias Propostas

### Erros Identificados

1. **Tratamento de Datas**:
    - **Problema**: Inconsistência no formato de datas entre front-end e back-end
    - **Solução**: Implementada validação mais flexível para aceitar múltiplos formatos de data
2. **Validação de Profissionais**:
    - **Problema**: Inicialmente não havia validação de idade mínima
    - **Solução**: Adicionada validação de 18 anos mínimos para cadastro de profissionais
3. **Consultas no Passado**:
    - **Problema**: Era possível agendar consultas em datas passadas
    - **Solução**: Implementada validação para impedir agendamento em datas anteriores à atual
4. **Deploy na AWS**:
    - **Problema**: Ainda não foi configurado para acessar via IP externo, a porta está inacessivel por enquanto

### Melhorias Propostas

1. **Autenticação e Autorização**:
    - Implementar JWT para segurança da API
    - Criar níveis de permissão (admin, profissional, paciente)
2. **Paginação e Filtros**:
    - Adicionar paginação para endpoints que retornam muitos registros
    - Implementar filtros por especialidade, data e status das consultas
3. **Melhorias de Performance**:
    - Otimizar queries com índices adicionais no banco de dados
    - Implementar compressão de respostas
4. **Testes Automatizados**:
    - Aumentar cobertura de testes
    - Adicionar testes de carga/performance
5. **Internacionalização**:
    - Suporte a múltiplos idiomas para mensagens de erro
    - Adaptação a diferentes formatos de data/hora

---

## 📝 Documentação Swagger

A documentação interativa da API está disponível em:

```
http://localhost:8000/swagger/
```

Esta interface permite visualizar e testar todos os endpoints diretamente no navegador, facilitando o desenvolvimento e integração com a API.

---
