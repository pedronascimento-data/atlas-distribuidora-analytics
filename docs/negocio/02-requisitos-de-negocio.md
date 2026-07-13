# Documento 02 — Requisitos de Negócio

> **Projeto:** Atlas Distribuidora Analytics  
> **Documento:** Requisitos de Negócio (Business Requirements Document - BRD)  
> **Versão:** 1.0  
> **Status:** Em desenvolvimento  
> **Autor:** Pedro Nascimento  
> **Última atualização:** Julho de 2026

---

# 1. Objetivo

Este documento define os requisitos de negócio da solução Atlas Distribuidora Analytics.

Seu objetivo é estabelecer quais necessidades da empresa deverão ser atendidas pela plataforma analítica, servindo como referência para a modelagem do banco de dados, desenvolvimento das consultas SQL, construção do modelo dimensional e criação dos dashboards.

---

# 2. Cenário Atual

A Atlas Distribuidora encontra-se em processo de expansão comercial.

O crescimento da empresa aumentou significativamente o volume de informações relacionadas a clientes, pedidos, produtos, estoque e faturamento.

Entretanto, os dados encontram-se distribuídos em diferentes planilhas e sistemas operacionais, dificultando a consolidação das informações e reduzindo a agilidade das análises.

Atualmente não existe uma plataforma única capaz de fornecer indicadores estratégicos confiáveis em tempo real.

---

# 3. Problemas Identificados

Durante o levantamento inicial foram identificados os seguintes desafios.

## Comercial

- Dificuldade para acompanhar metas comerciais.
- Baixa visibilidade do desempenho dos representantes.
- Ausência de indicadores por supervisor.
- Pouca previsibilidade sobre resultados futuros.

## Clientes

- Dificuldade para identificar clientes inativos.
- Pouca visibilidade sobre concentração de receita.
- Ausência de indicadores de recorrência.

## Produtos

- Dificuldade para identificar produtos com baixo giro.
- Falta de análises por categoria e marca.
- Pouca visibilidade sobre margem.

## Estoque

- Controle descentralizado.
- Excesso de produtos parados.
- Falta de indicadores de cobertura.

## Diretoria

- Relatórios demorados.
- Consolidação manual.
- Indicadores inconsistentes.
- Baixa confiabilidade dos dados.

---

# 4. Objetivos Estratégicos

A solução deverá permitir que a empresa consiga responder rapidamente às principais perguntas do negócio.

## Comercial

- Qual é o faturamento total?
- Quanto falta para atingir a meta?
- Qual representante apresenta melhor desempenho?
- Qual supervisor possui a equipe mais eficiente?

## Clientes

- Quem são os principais clientes?
- Quais clientes reduziram suas compras?
- Quais clientes estão inativos?

## Produtos

- Quais produtos mais vendem?
- Quais categorias possuem maior participação?
- Quais produtos possuem menor giro?

## Estoque

- Quais produtos estão abaixo do estoque mínimo?
- Quais produtos apresentam excesso de estoque?

## Gestão

- Como evoluiu o faturamento?
- Qual filial possui melhor resultado?
- Quais estados apresentam maior crescimento?

---

# 5. Stakeholders

| Área | Necessidade |
|--------|------------------------------|
| Diretoria | Indicadores estratégicos |
| Comercial | Metas e faturamento |
| Supervisores | Desempenho das equipes |
| Compras | Giro de produtos |
| Estoque | Cobertura de estoque |
| BI | Dados consolidados |

---

# 6. Requisitos Funcionais

A solução deverá permitir:

### RF01

Cadastrar clientes.

### RF02

Cadastrar produtos.

### RF03

Cadastrar representantes comerciais.

### RF04

Cadastrar supervisores.

### RF05

Cadastrar fornecedores.

### RF06

Registrar pedidos de venda.

### RF07

Controlar estoque por filial.

### RF08

Controlar metas comerciais.

### RF09

Calcular indicadores automaticamente.

### RF10

Disponibilizar dashboards executivos.

---

# 7. Requisitos Não Funcionais

A solução deverá:

- possuir estrutura escalável;
- utilizar banco de dados relacional;
- permitir atualização periódica dos dados;
- possuir documentação técnica;
- utilizar boas práticas de modelagem;
- ser facilmente compreendida por novos desenvolvedores.

---

# 8. Indicadores Esperados

A solução deverá disponibilizar, no mínimo, os seguintes KPIs.

| Indicador |
|------------|
| Faturamento |
| Meta Comercial |
| % Atingimento |
| Ticket Médio |
| Quantidade de Pedidos |
| Clientes Ativos |
| Clientes Inativos |
| Margem Bruta |
| Margem Percentual |
| Giro de Produtos |
| Curva ABC |
| Receita por Estado |
| Receita por Cidade |
| Receita por Categoria |
| Receita por Representante |

---

# 9. Benefícios Esperados

Após a implantação da solução espera-se:

- redução do tempo de elaboração de relatórios;
- aumento da confiabilidade das informações;
- melhoria da tomada de decisão;
- acompanhamento em tempo real dos indicadores;
- redução do trabalho manual;
- padronização dos KPIs.

---

# 10. Critérios de Sucesso

O projeto será considerado concluído quando:

- todos os indicadores forem calculados corretamente;
- o banco de dados suportar todas as regras de negócio;
- os dashboards responderem às perguntas estratégicas;
- toda a documentação estiver disponível no GitHub.

---

# Histórico

| Versão | Data | Autor | Alterações |
|--------|------|--------|------------|
| 1.0 | Julho/2026 | Pedro Nascimento | Criação inicial do documento |
