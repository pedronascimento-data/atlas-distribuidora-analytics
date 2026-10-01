from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa a análise exploratória dos dados sintéticos do Atlas."
    )
    parser.add_argument("--data-dir", default="data/generated")
    parser.add_argument("--output-dir", default="reports/eda")
    return parser.parse_args()


def load_table(data_dir: Path, name: str, parse_dates: list[str] | None = None) -> pd.DataFrame:
    path = data_dir / f"{name}.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {path}. "
            "Execute generate_mock_data.py antes da EDA."
        )
    return pd.read_csv(path, parse_dates=parse_dates)


def brl(value: float) -> str:
    formatted = f"{value:,.2f}"
    return "R$ " + formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def pct(value: float) -> str:
    return f"{value * 100:.2f}%".replace(".", ",")


def save_bar(
    dataframe: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    output_path: Path,
    horizontal: bool = False,
) -> None:
    figure, axis = plt.subplots(figsize=(10, 6))

    if horizontal:
        dataframe.plot(kind="barh", x=x, y=y, ax=axis, legend=False)
    else:
        dataframe.plot(kind="bar", x=x, y=y, ax=axis, legend=False)

    axis.set_title(title)
    axis.set_xlabel("")
    axis.grid(axis="y" if not horizontal else "x", alpha=0.25)
    figure.tight_layout()
    figure.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(figure)


def save_line(
    dataframe: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    output_path: Path,
) -> None:
    figure, axis = plt.subplots(figsize=(11, 6))
    axis.plot(dataframe[x], dataframe[y], marker="o")
    axis.set_title(title)
    axis.set_xlabel("")
    axis.grid(alpha=0.25)
    figure.autofmt_xdate()
    figure.tight_layout()
    figure.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    args = parse_args()
    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    figures_dir = output_dir / "figures"
    tables_dir = output_dir / "tables"

    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    pedido = load_table(
        data_dir,
        "pedido",
        parse_dates=["data_pedido", "data_faturamento"],
    )
    item = load_table(data_dir, "pedido_item")
    cliente = load_table(data_dir, "cliente")
    produto = load_table(data_dir, "produto")
    categoria = load_table(data_dir, "categoria")
    representante = load_table(data_dir, "representante")
    supervisor = load_table(data_dir, "supervisor")
    meta = load_table(data_dir, "meta_representante", parse_dates=["competencia"])
    estoque = load_table(data_dir, "estoque")
    filial = load_table(data_dir, "filial")

    # --------------------------------------------------------
    # Base analítica de vendas
    # --------------------------------------------------------

    vendas = (
        item.merge(
            pedido.loc[
                pedido["status"].isin(["FATURADO", "ENTREGUE"])
                & pedido["data_faturamento"].notna()
            ],
            on="id_pedido",
            how="inner",
            validate="many_to_one",
        )
        .merge(
            produto[
                ["id_produto", "sku", "descricao", "id_categoria"]
            ],
            on="id_produto",
            how="left",
            validate="many_to_one",
        )
        .merge(
            categoria,
            on="id_categoria",
            how="left",
            validate="many_to_one",
        )
        .merge(
            cliente[
                ["id_cliente", "codigo", "razao_social"]
            ].rename(columns={"codigo": "codigo_cliente"}),
            on="id_cliente",
            how="left",
            validate="many_to_one",
        )
    )

    vendas["valor_bruto"] = (
        vendas["quantidade"] * vendas["preco_unitario"]
    )
    vendas["faturamento"] = (
        vendas["valor_bruto"] - vendas["desconto_item"]
    )
    vendas["custo_total"] = (
        vendas["quantidade"] * vendas["custo_unitario"]
    )
    vendas["margem_bruta"] = (
        vendas["faturamento"] - vendas["custo_total"]
    )
    vendas["competencia"] = (
        vendas["data_faturamento"].dt.to_period("M").dt.to_timestamp()
    )

    # --------------------------------------------------------
    # KPIs executivos
    # --------------------------------------------------------

    faturamento = float(vendas["faturamento"].sum())
    margem_bruta = float(vendas["margem_bruta"].sum())
    pedidos = int(vendas["id_pedido"].nunique())
    clientes_compradores = int(vendas["id_cliente"].nunique())
    ticket_medio = faturamento / pedidos if pedidos else 0
    margem_pct = margem_bruta / faturamento if faturamento else 0

    kpis = pd.DataFrame([
        {"indicador": "Faturamento", "valor": faturamento},
        {"indicador": "Margem Bruta", "valor": margem_bruta},
        {"indicador": "Margem %", "valor": margem_pct},
        {"indicador": "Pedidos", "valor": pedidos},
        {"indicador": "Ticket Médio", "valor": ticket_medio},
        {"indicador": "Clientes Compradores", "valor": clientes_compradores},
    ])
    kpis.to_csv(tables_dir / "kpis_executivos.csv", index=False)

    # --------------------------------------------------------
    # Evolução mensal
    # --------------------------------------------------------

    mensal = (
        vendas.groupby("competencia", as_index=False)
        .agg(
            faturamento=("faturamento", "sum"),
            margem_bruta=("margem_bruta", "sum"),
            pedidos=("id_pedido", "nunique"),
            clientes=("id_cliente", "nunique"),
        )
        .sort_values("competencia")
    )
    mensal["crescimento_mom"] = mensal["faturamento"].pct_change()
    mensal["margem_pct"] = (
        mensal["margem_bruta"] / mensal["faturamento"]
    )
    mensal.to_csv(tables_dir / "evolucao_mensal.csv", index=False)

    save_line(
        mensal,
        "competencia",
        "faturamento",
        "Evolução mensal do faturamento",
        figures_dir / "faturamento_mensal.png",
    )

    # --------------------------------------------------------
    # Categorias e produtos
    # --------------------------------------------------------

    categorias = (
        vendas.groupby("nome", as_index=False)
        .agg(
            faturamento=("faturamento", "sum"),
            margem_bruta=("margem_bruta", "sum"),
            quantidade=("quantidade", "sum"),
        )
        .rename(columns={"nome": "categoria"})
        .sort_values("faturamento", ascending=False)
    )
    categorias["margem_pct"] = (
        categorias["margem_bruta"] / categorias["faturamento"]
    )
    categorias["participacao"] = (
        categorias["faturamento"] / categorias["faturamento"].sum()
    )
    categorias.to_csv(tables_dir / "performance_categorias.csv", index=False)

    save_bar(
        categorias,
        "categoria",
        "faturamento",
        "Faturamento por categoria",
        figures_dir / "faturamento_categoria.png",
    )

    produtos = (
        vendas.groupby(
            ["id_produto", "sku", "descricao"],
            as_index=False,
        )
        .agg(
            faturamento=("faturamento", "sum"),
            margem_bruta=("margem_bruta", "sum"),
            quantidade=("quantidade", "sum"),
            pedidos=("id_pedido", "nunique"),
        )
        .sort_values("faturamento", ascending=False)
    )
    produtos["margem_pct"] = (
        produtos["margem_bruta"] / produtos["faturamento"]
    )
    produtos.head(20).to_csv(
        tables_dir / "top_20_produtos.csv",
        index=False,
    )

    save_bar(
        produtos.head(10).sort_values("faturamento"),
        "descricao",
        "faturamento",
        "Top 10 produtos por faturamento",
        figures_dir / "top_produtos.png",
        horizontal=True,
    )

    # --------------------------------------------------------
    # Clientes e concentração
    # --------------------------------------------------------

    clientes = (
        vendas.groupby(
            ["id_cliente", "codigo_cliente", "razao_social"],
            as_index=False,
        )
        .agg(
            faturamento=("faturamento", "sum"),
            pedidos=("id_pedido", "nunique"),
            margem_bruta=("margem_bruta", "sum"),
        )
        .sort_values("faturamento", ascending=False)
    )
    clientes["participacao"] = (
        clientes["faturamento"] / clientes["faturamento"].sum()
    )
    clientes["participacao_acumulada"] = clientes["participacao"].cumsum()
    clientes["ticket_medio"] = (
        clientes["faturamento"] / clientes["pedidos"]
    )
    clientes.head(50).to_csv(
        tables_dir / "top_50_clientes.csv",
        index=False,
    )

    top10_client_share = float(clientes.head(10)["participacao"].sum())

    save_bar(
        clientes.head(10).sort_values("faturamento"),
        "razao_social",
        "faturamento",
        "Top 10 clientes por faturamento",
        figures_dir / "top_clientes.png",
        horizontal=True,
    )

    # --------------------------------------------------------
    # Performance comercial e metas
    # --------------------------------------------------------

    vendas_rep = (
        vendas.groupby("id_representante", as_index=False)
        .agg(
            faturamento=("faturamento", "sum"),
            pedidos=("id_pedido", "nunique"),
            clientes=("id_cliente", "nunique"),
        )
    )

    equipe = (
        representante.merge(
            supervisor[
                ["id_supervisor", "nome", "id_gerente"]
            ].rename(columns={"nome": "supervisor"}),
            on="id_supervisor",
            how="left",
            validate="many_to_one",
        )
        .rename(columns={"nome": "representante"})
    )

    performance_rep = (
        equipe.merge(
            vendas_rep,
            on="id_representante",
            how="left",
        )
        .fillna({
            "faturamento": 0,
            "pedidos": 0,
            "clientes": 0,
        })
        .sort_values("faturamento", ascending=False)
    )
    performance_rep["ranking"] = (
        performance_rep["faturamento"]
        .rank(method="dense", ascending=False)
        .astype(int)
    )
    performance_rep.to_csv(
        tables_dir / "performance_representantes.csv",
        index=False,
    )

    meta_mensal = (
        meta.groupby(["competencia", "id_representante"], as_index=False)
        ["valor_meta"]
        .sum()
    )

    vendas_meta = (
        vendas.groupby(
            ["competencia", "id_representante"],
            as_index=False,
        )
        ["faturamento"]
        .sum()
        .merge(
            meta_mensal,
            on=["competencia", "id_representante"],
            how="outer",
        )
        .fillna({"faturamento": 0, "valor_meta": 0})
    )

    vendas_meta["atingimento"] = (
        vendas_meta["faturamento"]
        / vendas_meta["valor_meta"].where(
            vendas_meta["valor_meta"] != 0
        )
    )

    vendas_meta.to_csv(
        tables_dir / "atingimento_metas.csv",
        index=False,
    )

    meta_total = float(vendas_meta["valor_meta"].sum())
    atingimento_total = faturamento / meta_total if meta_total else 0

    # --------------------------------------------------------
    # Estoque
    # --------------------------------------------------------

    estoque_analise = (
        estoque.merge(
            produto[
                ["id_produto", "sku", "descricao", "id_categoria", "custo_atual"]
            ],
            on="id_produto",
            how="left",
            validate="many_to_one",
        )
        .merge(
            categoria[
                ["id_categoria", "categoria"]
            ],
            on="id_categoria",
            how="left",
            validate="many_to_one",
        )
        .merge(
            filial[
                ["id_filial", "nome"]
            ].rename(columns={"nome": "filial"}),
            on="id_filial",
            how="left",
            validate="many_to_one",
        )
    )

    estoque_analise["status_estoque"] = "ADEQUADO"
    estoque_analise.loc[
        estoque_analise["estoque_atual"]
        < estoque_analise["estoque_minimo"],
        "status_estoque",
    ] = "ABAIXO_MINIMO"
    estoque_analise.loc[
        estoque_analise["estoque_atual"]
        > estoque_analise["estoque_maximo"],
        "status_estoque",
    ] = "ACIMA_MAXIMO"
    estoque_analise["valor_estoque"] = (
        estoque_analise["estoque_atual"]
        * estoque_analise["custo_atual"]
    )

    estoque_resumo = (
        estoque_analise.groupby(
            "status_estoque",
            as_index=False,
        )
        .agg(
            combinacoes_produto_filial=("id_estoque", "count"),
            valor_estoque=("valor_estoque", "sum"),
        )
    )
    estoque_resumo.to_csv(
        tables_dir / "resumo_estoque.csv",
        index=False,
    )

    abaixo_minimo = int(
        (estoque_analise["status_estoque"] == "ABAIXO_MINIMO").sum()
    )
    total_posicoes = len(estoque_analise)
    estoque_critico_pct = (
        abaixo_minimo / total_posicoes if total_posicoes else 0
    )

    # --------------------------------------------------------
    # Resumo em Markdown
    # --------------------------------------------------------

    melhor_mes = mensal.loc[mensal["faturamento"].idxmax()]
    melhor_categoria = categorias.iloc[0]
    top_cliente = clientes.iloc[0]
    top_rep = performance_rep.iloc[0]

    report = f"""# Resumo da Análise Exploratória — Atlas Distribuidora

> Relatório gerado automaticamente por `python/eda_analysis.py`.

## KPIs principais

| Indicador | Resultado |
|---|---:|
| Faturamento | {brl(faturamento)} |
| Margem bruta | {brl(margem_bruta)} |
| Margem % | {pct(margem_pct)} |
| Pedidos faturados/entregues | {pedidos:,} |
| Ticket médio | {brl(ticket_medio)} |
| Clientes compradores | {clientes_compradores:,} |
| Atingimento global da meta | {pct(atingimento_total)} |

## Destaques encontrados

- **Melhor mês:** {melhor_mes["competencia"].strftime("%m/%Y")} com {brl(float(melhor_mes["faturamento"]))}.
- **Categoria líder em faturamento:** {melhor_categoria["categoria"]} com {brl(float(melhor_categoria["faturamento"]))}.
- **Cliente líder:** {top_cliente["razao_social"]} com {brl(float(top_cliente["faturamento"]))}.
- **Representante líder:** {top_rep["representante"]} com {brl(float(top_rep["faturamento"]))}.
- **Concentração dos Top 10 clientes:** {pct(top10_client_share)} do faturamento.
- **Posições de estoque abaixo do mínimo:** {abaixo_minimo:,} de {total_posicoes:,} ({pct(estoque_critico_pct)}).

## Perguntas para o dashboard

1. O crescimento de vendas é consistente ou concentrado em poucos meses?
2. A categoria com maior receita também apresenta boa margem?
3. Quais representantes possuem alto faturamento, mas baixo atingimento de meta?
4. A receita está excessivamente concentrada nos maiores clientes?
5. Produtos com forte faturamento apresentam risco de ruptura de estoque?
6. Quais filiais concentram mais itens abaixo do estoque mínimo?

## Arquivos gerados

### Tabelas

- `kpis_executivos.csv`
- `evolucao_mensal.csv`
- `performance_categorias.csv`
- `top_20_produtos.csv`
- `top_50_clientes.csv`
- `performance_representantes.csv`
- `atingimento_metas.csv`
- `resumo_estoque.csv`

### Figuras

- `faturamento_mensal.png`
- `faturamento_categoria.png`
- `top_produtos.png`
- `top_clientes.png`
"""

    (output_dir / "resumo_eda.md").write_text(
        report,
        encoding="utf-8",
    )

    print(report)
    print(f"\nArtefatos salvos em: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
