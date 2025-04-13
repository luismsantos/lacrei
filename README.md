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

## 🌎 Deploy na AWS EC2

O deploy da aplicação foi realizado em uma instância EC2 da AWS e está disponível através do IP:

**http://18.212.64.154**

### Acessos no Ambiente de Produção

- **Admin Django**: http://18.212.64.154/admin/
- **Documentação Swagger**: http://18.212.64.154/swagger/ 

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
    - **Solução**: Configurado e liberado a porta 80 e 443 na AWS
5. **Arquivos estáticos no Deploy**:
    - **Problema**: A interface do projeto não estava aparecendo corretamente, pois não estava configurado corretamente para pegar arquivos estáticos 
    - **Solução**: Configurado no container caminho correto para pegar arquivos estáticos

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

# Proposta de Integração Asaas para Split de Pagamento na Lacrei Saúde

Depois de passar um tempo na documentação (https://asaasv3.docs.apiary.io/\#reference/0/cobrancas), descobri que a Asaas é perfeita para a plataforna. Basicamente, eles oferecem um sistema que permite dividir automaticamente o valor de uma cobrança entre várias partes - exatamente o que precisamos para dividir o valor das consultas entre os profissionais de saúde e a plataforma Lacrei!

A ideia seria assim: quando um paciente marcar uma consulta, enviamos uma solicitação para a API da Asaas criando uma cobrança (pode ser boleto, cartão, pix, etc.) e já informamos como o dinheiro deve ser dividido. Por exemplo, se a consulta custa R$200, podemos configurar para que R$170 vá direto para a conta do profissional e R$30 fique na Lacrei como taxa de serviço.

Olhando na documentação, vi que o processo é bem tranquilo. Primeiro, precisamos criar contas na Asaas tanto para a Lacrei quanto para cada profissional cadastrado. A Asaas chama isso de "wallets" (carteiras). A parte legal é que eles têm um ambiente de sandbox que podemos usar pra testar tudo sem precisar fazer pagamentos reais (https://sandbox.asaas.com).

Para implementar, precisaríamos adicionar alguns campos ao cadastro dos profissionais, tipo um campo pra guardar o ID da carteira deles na Asaas. Também teríamos que criar uma nova tela no sistema para o processo de pagamento, que se comunicaria com a API da Asaas.

O fluxo completo seria mais ou menos assim:

1. Paciente agenda consulta e escolhe forma de pagamento
2. Nossa aplicação envia os dados para a Asaas com as regras de split
3. Asaas gera o link/dados de pagamento que mostramos para o paciente
4. Paciente paga
5. Asaas nos avisa automaticamente quando o pagamento for confirmado (usando webhooks)
6. Atualizamos o status da consulta e enviamos confirmação por email
7. Quando o dinheiro cair, a Asaas já faz a divisão automaticamente!

Um detalhe importante que vi na documentação é que a Asaas cobra uma taxa por transação (aproximadamente 3,49% + R$0,49 para cartão de crédito), então precisamos considerar isso no modelo de negócio. Podemos embutir essa taxa no valor da consulta ou deduzi-la da nossa parte.

O melhor de tudo é que não precisamos nos preocupar com questões de segurança de pagamento, já que a Asaas cuida de toda a parte sensível como armazenamento de dados de cartão.

