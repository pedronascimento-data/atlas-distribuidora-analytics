from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida integridade básica dos CSVs gerados para o Atlas."
    )
    parser.add_argument("--data-dir", default="data/generated")
    return parser.parse_args()


def load(data_dir: Path, table: str) -> pd.DataFrame:
    path = data_dir / f"{table}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    return pd.read_csv(path)


def check(name: str, condition: bool, failures: list[str]) -> None:
    status = "OK" if condition else "FALHOU"
    print(f"[{status}] {name}")
    if not condition:
        failures.append(name)


def main() -> None:
    args = parse_args()
    data_dir = Path(args.data_dir)

    estado = load(data_dir, "estado")
    cidade = load(data_dir, "cidade")
    filial = load(data_dir, "filial")
    gerente = load(data_dir, "gerente")
    supervisor = load(data_dir, "supervisor")
    representante = load(data_dir, "representante")
    cliente = load(data_dir, "cliente")
    categoria = load(data_dir, "categoria")
    marca = load(data_dir, "marca")
    fornecedor = load(data_dir, "fornecedor")
    produto = load(data_dir, "produto")
    pedido = load(data_dir, "pedido")
    pedido_item = load(data_dir, "pedido_item")
    estoque = load(data_dir, "estoque")
    meta = load(data_dir, "meta_representante")

    failures: list[str] = []

    check(
        "cidades referenciam estados existentes",
        set(cidade["id_estado"]).issubset(set(estado["id_estado"])),
        failures,
    )

    check(
        "filiais referenciam cidades existentes",
        set(filial["id_cidade"]).issubset(set(cidade["id_cidade"])),
        failures,
    )

    check(
        "supervisores referenciam gerentes existentes",
        set(supervisor["id_gerente"]).issubset(set(gerente["id_gerente"])),
        failures,
    )

    check(
        "representantes referenciam supervisores existentes",
        set(representante["id_supervisor"]).issubset(
            set(supervisor["id_supervisor"])
        ),
        failures,
    )

    check(
        "clientes referenciam representantes existentes",
        set(cliente["id_representante"]).issubset(
            set(representante["id_representante"])
        ),
        failures,
    )

    check(
        "clientes referenciam cidades existentes",
        set(cliente["id_cidade"]).issubset(set(cidade["id_cidade"])),
        failures,
    )

    check(
        "produtos referenciam categorias existentes",
        set(produto["id_categoria"]).issubset(set(categoria["id_categoria"])),
        failures,
    )

    check(
        "produtos referenciam marcas existentes",
        set(produto["id_marca"]).issubset(set(marca["id_marca"])),
        failures,
    )

    check(
        "produtos referenciam fornecedores existentes",
        set(produto["id_fornecedor"]).issubset(
            set(fornecedor["id_fornecedor"])
        ),
        failures,
    )

    check(
        "pedidos referenciam clientes existentes",
        set(pedido["id_cliente"]).issubset(set(cliente["id_cliente"])),
        failures,
    )

    check(
        "pedidos referenciam representantes existentes",
        set(pedido["id_representante"]).issubset(
            set(representante["id_representante"])
        ),
        failures,
    )

    check(
        "itens referenciam pedidos existentes",
        set(pedido_item["id_pedido"]).issubset(set(pedido["id_pedido"])),
        failures,
    )

    check(
        "itens referenciam produtos existentes",
        set(pedido_item["id_produto"]).issubset(set(produto["id_produto"])),
        failures,
    )

    check(
        "estoque possui combinação filial/produto única",
        not estoque.duplicated(["id_filial", "id_produto"]).any(),
        failures,
    )

    check(
        "metas possuem combinação representante/competência única",
        not meta.duplicated(["id_representante", "competencia"]).any(),
        failures,
    )

    check(
        "quantidades dos itens são positivas",
        (pedido_item["quantidade"] > 0).all(),
        failures,
    )

    check(
        "preços e custos dos itens não são negativos",
        (
            (pedido_item["preco_unitario"] >= 0)
            & (pedido_item["custo_unitario"] >= 0)
            & (pedido_item["desconto_item"] >= 0)
        ).all(),
        failures,
    )

    item_discount = (
        pedido_item.groupby("id_pedido", as_index=False)["desconto_item"]
        .sum()
        .rename(columns={"desconto_item": "desconto_calculado"})
    )

    discount_check = pedido[
        ["id_pedido", "valor_desconto"]
    ].merge(
        item_discount,
        on="id_pedido",
        how="left",
    )

    discount_check["desconto_calculado"] = (
        discount_check["desconto_calculado"].fillna(0)
    )

    check(
        "desconto do pedido reconcilia com os descontos dos itens",
        (
            (
                discount_check["valor_desconto"]
                - discount_check["desconto_calculado"]
            ).abs()
            < 0.02
        ).all(),
        failures,
    )

    valid_invoice = pedido.loc[
        pedido["status"].isin(["FATURADO", "ENTREGUE"]),
        "data_faturamento",
    ].notna().all()

    check(
        "pedidos faturados/entregues possuem data de faturamento",
        bool(valid_invoice),
        failures,
    )

    if failures:
        print("\nValidação concluída com falhas:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("\nValidação concluída sem falhas.")


if __name__ == "__main__":
    main()
