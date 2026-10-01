# Dados do projeto

Os dados utilizados pelo **Atlas Distribuidora Analytics** são totalmente sintéticos.

Os CSVs não são versionados no repositório para evitar arquivos pesados e duplicação desnecessária. Eles podem ser reconstruídos a qualquer momento por meio do script:

```bash
python python/generate_mock_data.py --scale portfolio
```

## Escalas disponíveis

| Escala | Clientes | Produtos | Pedidos | Fornecedores |
|---|---:|---:|---:|---:|
| `small` | 250 | 120 | 2.000 | 40 |
| `portfolio` | 1.500 | 500 | 18.000 | 120 |
| `full` | 12.000 | 4.500 | 100.000 | 350 |

A escala `portfolio` é o padrão e foi pensada para desenvolvimento local e demonstrações.

A escala `full` aproxima o cenário definido no manual da empresa fictícia e é indicada para testes de volume.

## Saída

Por padrão, os arquivos são gerados em:

`data/generated/`

Entre os conjuntos produzidos estão:

- estados e cidades;
- filiais;
- gerentes, supervisores e representantes;
- clientes;
- categorias, marcas e fornecedores;
- produtos;
- pedidos e itens;
- estoque;
- metas mensais.

O arquivo `_summary.csv` registra a quantidade de linhas gerada por tabela.

## Reprodutibilidade

O gerador utiliza uma semente fixa (`SEED = 42`). Com os mesmos parâmetros, a massa de dados é reproduzível.

Nenhum dado representa pessoas, empresas, documentos fiscais ou resultados reais.
