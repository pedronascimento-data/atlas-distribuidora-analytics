# Checklist de Validação do Dashboard

> O objetivo deste checklist é impedir que um dashboard visualmente correto publique números incorretos.

## 1. Modelo

- [ ] `dim_data` está marcada como tabela de datas.
- [ ] As dimensões estão no lado 1 dos relacionamentos.
- [ ] As fatos estão no lado N.
- [ ] Direção de filtro está simples onde possível.
- [ ] Não existem relacionamentos diretos entre fatos.
- [ ] Não existem caminhos ambíguos ativos.
- [ ] Chaves técnicas estão ocultas.

## 2. Reconciliação

Comparar os números do Power BI com `sql/06_validacoes_pipeline.sql`.

- [ ] Faturamento confere.
- [ ] Quantidade de linhas da fato confere.
- [ ] Total de metas confere.
- [ ] Margem bruta confere.
- [ ] Quantidade de pedidos usa DISTINCTCOUNT.
- [ ] Nenhuma dimensão gera perda de linhas.

## 3. Inteligência temporal

- [ ] Faturamento do mês anterior responde corretamente ao filtro.
- [ ] MoM retorna vazio quando não existe período anterior.
- [ ] YoY usa o mesmo intervalo do ano anterior.
- [ ] YTD reinicia a cada ano.
- [ ] `ano_mes` está ordenado por uma coluna cronológica, não alfabeticamente.

## 4. Metas

- [ ] Meta muda com período.
- [ ] Meta muda com representante.
- [ ] Meta consolida corretamente em supervisor e gerente.
- [ ] Atingimento = faturamento / meta.
- [ ] O total não soma percentuais individuais incorretamente.

## 5. Filtros

Testar:

- [ ] data;
- [ ] filial;
- [ ] UF;
- [ ] categoria;
- [ ] gerente;
- [ ] supervisor;
- [ ] representante.

Para cada filtro:

- [ ] os cards respondem;
- [ ] os gráficos respondem;
- [ ] não surgem totais inesperados;
- [ ] o filtro não afeta páginas onde não deveria.

## 6. Página Executiva

- [ ] Faturamento está em destaque.
- [ ] Margem % possui formato percentual.
- [ ] Ticket médio possui formato monetário.
- [ ] Meta % possui contexto claro.
- [ ] Evolução mensal está cronologicamente ordenada.
- [ ] Top 5 realmente mostra apenas cinco representantes.

## 7. Página Comercial

- [ ] Ranking respeita filtros selecionados.
- [ ] Drill-down gerente → supervisor → representante funciona.
- [ ] Gap para meta possui interpretação clara.
- [ ] A formatação condicional não contradiz os valores.

## 8. Página Clientes

- [ ] Clientes compradores são distintos.
- [ ] Top clientes ordena por faturamento.
- [ ] Participação usa o denominador correto dentro do contexto.
- [ ] Cidade e UF correspondem ao cliente.

## 9. Página Produtos

- [ ] Categoria e produto vêm da dimensão de produto.
- [ ] Margem % não é soma de percentuais.
- [ ] Dispersão usa medidas, não colunas agregadas incorretamente.
- [ ] Quantidade vendida responde ao período.

## 10. Página Estoque

- [ ] Snapshot utiliza a data correta.
- [ ] Abaixo do mínimo compara estoque atual x mínimo na mesma linha.
- [ ] Acima do máximo compara estoque atual x máximo.
- [ ] Valor em estoque usa o valor carregado na fato.

## 11. UX

- [ ] Títulos usam linguagem de negócio.
- [ ] Não há nomes como `fato_vendas` visíveis para o usuário.
- [ ] Cores têm função consistente.
- [ ] Cards têm alinhamento e tamanho consistentes.
- [ ] Não há scroll horizontal desnecessário.
- [ ] Navegação funciona em todas as páginas.
- [ ] Tooltips acrescentam informação, sem repetir o visual.

## 12. Critério para marcar o dashboard como concluído

Somente marcar o item **Dashboard Power BI** do roadmap quando:

1. o `.pbix` estiver salvo;
2. as cinco páginas estiverem construídas;
3. o checklist estiver concluído;
4. screenshots estiverem no repositório;
5. os números estiverem reconciliados com SQL.
