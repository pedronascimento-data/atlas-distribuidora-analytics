# Power BI — Atlas Distribuidora Analytics

Esta pasta concentra os artefatos necessários para construir e validar a camada de Business Intelligence.

## Arquivos

| Arquivo | Finalidade |
|---|---|
| [medidas.dax](medidas.dax) | Medidas DAX de vendas, tempo, metas, comercial e estoque |
| [tema-atlas.json](tema-atlas.json) | Tema visual importável no Power BI |
| [campos-visuais.md](campos-visuais.md) | Mapa entre páginas, visuais, campos e medidas |

## Documentação

- [Especificação geral](../docs/bi/01-especificacao-dashboard-powerbi.md)
- [Guia de construção](../docs/bi/02-guia-construcao-dashboard.md)
- [Checklist de validação](../docs/bi/03-checklist-validacao-dashboard.md)

## Ordem de construção

1. conectar ao banco `atlas_dw`;
2. carregar dimensões e fatos;
3. configurar os relacionamentos;
4. marcar `dim_data` como tabela de datas;
5. ocultar as chaves técnicas;
6. importar `tema-atlas.json`;
7. criar as medidas de `medidas.dax`;
8. construir as cinco páginas;
9. sincronizar slicers;
10. executar o checklist de validação;
11. salvar o `.pbix`;
12. incluir screenshots no repositório.

## Páginas

1. **Visão Executiva**
2. **Performance Comercial**
3. **Clientes**
4. **Produtos e Categorias**
5. **Estoque**

## Status

A arquitetura, o tema, as medidas e a especificação de construção estão prontos.

O arquivo `Atlas_Distribuidora_Analytics.pbix` ainda precisa ser construído e validado no Power BI Desktop.
