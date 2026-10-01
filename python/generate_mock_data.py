from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
import random

import numpy as np
import pandas as pd


SEED = 42

STATES = {
    "BA": ["Salvador", "Feira de Santana", "Vitória da Conquista", "Ilhéus", "Juazeiro", "Barreiras"],
    "SE": ["Aracaju", "Itabaiana", "Lagarto", "Estância"],
    "AL": ["Maceió", "Arapiraca", "Palmeira dos Índios", "Penedo"],
    "PE": ["Recife", "Caruaru", "Petrolina", "Garanhuns", "Olinda"],
    "PB": ["João Pessoa", "Campina Grande", "Patos", "Sousa"],
}

STATE_NAMES = {
    "BA": "Bahia",
    "SE": "Sergipe",
    "AL": "Alagoas",
    "PE": "Pernambuco",
    "PB": "Paraíba",
}

CATEGORIES = [
    "Tintas", "Ferragens", "Ferramentas", "Hidráulica", "Elétrica",
    "Louças", "Metais", "Pisos", "Revestimentos", "Argamassas",
    "Impermeabilizantes",
]

BRANDS = [
    "Aquarela", "Concretto", "HidroMax", "EletroSul", "FerroMais",
    "CasaForte", "PisoNobre", "Ceramix", "Vedaplus", "ObraPro",
    "Metalux", "Construmax", "Nivelar", "Pratika", "Durafix",
]

PRODUCT_TEMPLATES = {
    "Tintas": ["Tinta Acrílica", "Tinta Esmalte", "Massa Corrida", "Selador"],
    "Ferragens": ["Arame Recozido", "Prego", "Parafuso", "Dobradiça"],
    "Ferramentas": ["Martelo", "Alicate", "Trena", "Chave de Fenda"],
    "Hidráulica": ["Tubo PVC", "Joelho PVC", "Registro", "Caixa d'Água"],
    "Elétrica": ["Tomada", "Interruptor", "Cabo Flexível", "Disjuntor"],
    "Louças": ["Bacia Sanitária", "Cuba", "Lavatório"],
    "Metais": ["Torneira", "Misturador", "Válvula"],
    "Pisos": ["Piso Cerâmico", "Porcelanato"],
    "Revestimentos": ["Revestimento Cerâmico", "Pastilha"],
    "Argamassas": ["Argamassa AC-I", "Argamassa AC-II", "Argamassa AC-III"],
    "Impermeabilizantes": [
        "Manta Líquida",
        "Impermeabilizante Acrílico",
        "Aditivo Impermeabilizante",
    ],
}

FIRST_NAMES = [
    "Ana", "Bruno", "Carla", "Diego", "Elisa", "Fabio", "Gabriela", "Henrique",
    "Isabela", "João", "Karen", "Lucas", "Mariana", "Nicolas", "Olivia", "Paulo",
    "Renata", "Samuel", "Talita", "Victor", "Yasmin", "Rafael", "Eduarda", "Marcos",
]

LAST_NAMES = [
    "Souza", "Lima", "Mendes", "Alves", "Rocha", "Nunes", "Santos", "Oliveira",
    "Costa", "Pereira", "Martins", "Ferreira", "Barbosa", "Ribeiro", "Carvalho",
    "Nascimento", "Araújo", "Cardoso", "Freitas", "Gomes",
]

BUSINESS_PREFIXES = [
    "Casa", "Depósito", "Constrular", "Center", "Comercial", "Rede",
    "Construmais", "Lar",
]

BUSINESS_SUFFIXES = [
    "Materiais", "Construção", "Home Center", "Ferragens", "Acabamentos",
    "Construir", "Obra Certa",
]


@dataclass(frozen=True)
class Scale:
    clients: int
    products: int
    orders: int
    suppliers: int


SCALES = {
    "small": Scale(clients=250, products=120, orders=2_000, suppliers=40),
    "portfolio": Scale(clients=1_500, products=500, orders=18_000, suppliers=120),
    "full": Scale(clients=12_000, products=4_500, orders=100_000, suppliers=350),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera dados sintéticos para o Atlas Distribuidora Analytics."
    )
    parser.add_argument("--scale", choices=SCALES, default="portfolio")
    parser.add_argument("--output", default="data/generated")
    parser.add_argument("--start-date", default="2024-01-01")
    parser.add_argument("--end-date", default="2026-09-30")
    return parser.parse_args()


def person_name(rng: np.random.Generator) -> str:
    return f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"


def business_name(rng: np.random.Generator, idx: int) -> str:
    return f"{rng.choice(BUSINESS_PREFIXES)} {rng.choice(BUSINESS_SUFFIXES)} {idx:05d}"


def fake_document(idx: int) -> str:
    raw = f"{idx:014d}"
    return f"{raw[:2]}.{raw[2:5]}.{raw[5:8]}/{raw[8:12]}-{raw[12:14]}"


def choose_date(
    rng: np.random.Generator,
    start: date,
    end: date,
) -> date:
    span = (end - start).days
    return start + timedelta(days=int(rng.integers(0, span + 1)))


def main() -> None:
    args = parse_args()
    rng = np.random.default_rng(SEED)
    random.seed(SEED)

    scale = SCALES[args.scale]
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    start_date = date.fromisoformat(args.start_date)
    end_date = date.fromisoformat(args.end_date)

    if end_date <= start_date:
        raise ValueError("end-date deve ser posterior a start-date")

    # --------------------------------------------------------
    # Estados e cidades
    # --------------------------------------------------------

    estados = pd.DataFrame([
        {"id_estado": i + 1, "nome": STATE_NAMES[uf], "uf": uf}
        for i, uf in enumerate(STATES)
    ])

    city_rows = []
    city_id = 1

    for state_id, uf in enumerate(STATES, start=1):
        for city in STATES[uf]:
            city_rows.append({
                "id_cidade": city_id,
                "nome": city,
                "id_estado": state_id,
            })
            city_id += 1

    cidades = pd.DataFrame(city_rows)

    # --------------------------------------------------------
    # Filiais
    # --------------------------------------------------------

    branch_cities = {
        "BA": "Salvador",
        "SE": "Aracaju",
        "AL": "Maceió",
        "PE": "Recife",
        "PB": "João Pessoa",
    }

    filial_rows = []

    for i, (uf, city) in enumerate(branch_cities.items(), start=1):
        state_id = int(estados.loc[estados["uf"] == uf, "id_estado"].iloc[0])
        city_id_value = int(
            cidades.loc[
                (cidades["nome"] == city)
                & (cidades["id_estado"] == state_id),
                "id_cidade",
            ].iloc[0]
        )

        filial_rows.append({
            "id_filial": i,
            "codigo": f"FIL{i:02d}",
            "nome": f"Atlas {city}",
            "id_cidade": city_id_value,
            "ativa": 1,
        })

    filiais = pd.DataFrame(filial_rows)

    # --------------------------------------------------------
    # Estrutura comercial
    # --------------------------------------------------------

    gerentes = pd.DataFrame([
        {
            "id_gerente": i,
            "codigo": f"GER{i:02d}",
            "nome": person_name(rng),
            "ativo": 1,
        }
        for i in range(1, 4)
    ])

    supervisores = pd.DataFrame([
        {
            "id_supervisor": i,
            "codigo": f"SUP{i:02d}",
            "nome": person_name(rng),
            "id_gerente": 1 + ((i - 1) % len(gerentes)),
            "ativo": 1,
        }
        for i in range(1, 9)
    ])

    representantes = pd.DataFrame([
        {
            "id_representante": i,
            "codigo": f"REP{i:03d}",
            "nome": person_name(rng),
            "id_supervisor": 1 + ((i - 1) % len(supervisores)),
            "ativo": 1,
        }
        for i in range(1, 43)
    ])

    # --------------------------------------------------------
    # Produtos e fornecedores
    # --------------------------------------------------------

    categorias = pd.DataFrame([
        {"id_categoria": i + 1, "nome": name}
        for i, name in enumerate(CATEGORIES)
    ])

    marcas = pd.DataFrame([
        {"id_marca": i + 1, "nome": name}
        for i, name in enumerate(BRANDS)
    ])

    fornecedores = pd.DataFrame([
        {
            "id_fornecedor": i,
            "codigo": f"FOR{i:04d}",
            "razao_social": f"Fornecedor {i:04d} Ltda",
            "nome_fantasia": f"Fornecedor {i:04d}",
            "documento": fake_document(10_000_000 + i),
            "ativo": 1 if rng.random() > 0.03 else 0,
        }
        for i in range(1, scale.suppliers + 1)
    ])

    product_rows = []

    for i in range(1, scale.products + 1):
        category_id = int(rng.integers(1, len(categorias) + 1))
        category_name = categorias.loc[
            categorias["id_categoria"] == category_id,
            "nome",
        ].iloc[0]

        brand_id = int(rng.integers(1, len(marcas) + 1))
        supplier_id = int(rng.integers(1, len(fornecedores) + 1))
        cost = round(float(rng.uniform(3, 900)), 2)
        markup = float(rng.uniform(1.18, 1.75))

        product_rows.append({
            "id_produto": i,
            "sku": f"SKU{i:06d}",
            "descricao": f"{rng.choice(PRODUCT_TEMPLATES[category_name])} {i:04d}",
            "id_categoria": category_id,
            "id_marca": brand_id,
            "id_fornecedor": supplier_id,
            "custo_atual": cost,
            "preco_atual": round(cost * markup, 2),
            "ativo": 1 if rng.random() > 0.025 else 0,
        })

    produtos = pd.DataFrame(product_rows)

    # --------------------------------------------------------
    # Clientes
    # --------------------------------------------------------

    client_rows = []
    city_ids = cidades["id_cidade"].to_numpy()
    rep_ids = representantes["id_representante"].to_numpy()
    registration_end = min(
        end_date,
        start_date + timedelta(days=365),
    )

    for i in range(1, scale.clients + 1):
        status = rng.choice(
            ["ATIVO", "INATIVO", "BLOQUEADO"],
            p=[0.91, 0.07, 0.02],
        )

        client_rows.append({
            "id_cliente": i,
            "codigo": f"CLI{i:06d}",
            "razao_social": f"{business_name(rng, i)} Ltda",
            "nome_fantasia": business_name(rng, i),
            "documento": fake_document(20_000_000 + i),
            "id_cidade": int(rng.choice(city_ids)),
            "id_representante": int(rng.choice(rep_ids)),
            "status": status,
            "data_cadastro": choose_date(
                rng,
                start_date - timedelta(days=730),
                registration_end,
            ).isoformat(),
        })

    clientes = pd.DataFrame(client_rows)

    # --------------------------------------------------------
    # Metas mensais
    # --------------------------------------------------------

    month_starts = pd.date_range(
        start=start_date.replace(day=1),
        end=end_date.replace(day=1),
        freq="MS",
    )

    target_rows = []
    target_id = 1

    for competence in month_starts:
        seasonal = 1 + 0.08 * np.sin(
            (competence.month - 1) / 12 * 2 * np.pi
        )

        for rep_id in rep_ids:
            base = rng.uniform(90_000, 190_000)

            target_rows.append({
                "id_meta": target_id,
                "id_representante": int(rep_id),
                "competencia": competence.date().isoformat(),
                "valor_meta": round(float(base * seasonal), 2),
            })

            target_id += 1

    metas = pd.DataFrame(target_rows)

    # --------------------------------------------------------
    # Estoque
    # --------------------------------------------------------

    stock_rows = []
    stock_id = 1

    for branch_id in filiais["id_filial"]:
        selected_products = rng.choice(
            produtos["id_produto"],
            size=max(1, int(len(produtos) * 0.90)),
            replace=False,
        )

        for product_id in selected_products:
            minimum = round(float(rng.uniform(5, 40)), 3)
            maximum = round(float(minimum * rng.uniform(2.5, 6.0)), 3)
            current = round(float(rng.uniform(0, maximum * 1.15)), 3)

            stock_rows.append({
                "id_estoque": stock_id,
                "id_filial": int(branch_id),
                "id_produto": int(product_id),
                "estoque_atual": current,
                "estoque_minimo": minimum,
                "estoque_maximo": maximum,
                "atualizado_em": f"{end_date.isoformat()} 18:00:00",
            })

            stock_id += 1

    estoque = pd.DataFrame(stock_rows)

    # --------------------------------------------------------
    # Pedidos e itens
    # --------------------------------------------------------

    active_clients = clientes.loc[clientes["status"] == "ATIVO"]
    active_products = produtos.loc[produtos["ativo"] == 1].set_index(
        "id_produto"
    )

    order_rows = []
    item_rows = []
    item_id = 1

    day_count = (end_date - start_date).days
    offsets = np.arange(day_count + 1)

    # Crescimento moderado do volume ao longo do período.
    weights = 1 + (offsets / max(day_count, 1)) * 0.35
    weights = weights / weights.sum()

    for order_id in range(1, scale.orders + 1):
        day_offset = int(rng.choice(offsets, p=weights))
        order_date = start_date + timedelta(days=day_offset)

        client = active_clients.iloc[
            int(rng.integers(0, len(active_clients)))
        ]

        representative_id = int(client["id_representante"])
        branch_id = int(rng.choice(filiais["id_filial"]))

        status = rng.choice(
            ["FATURADO", "ENTREGUE", "CANCELADO", "APROVADO"],
            p=[0.48, 0.42, 0.05, 0.05],
        )

        invoice_datetime = None

        if status in ("FATURADO", "ENTREGUE"):
            invoice_date = min(
                order_date + timedelta(days=int(rng.integers(0, 4))),
                end_date,
            )
            invoice_datetime = (
                datetime.combine(invoice_date, datetime.min.time())
                + timedelta(hours=int(rng.integers(8, 18)))
            )

        order_rows.append({
            "id_pedido": order_id,
            "numero_pedido": f"PED{order_id:08d}",
            "data_pedido": (
                f"{order_date.isoformat()} "
                f"{int(rng.integers(8, 18)):02d}:"
                f"{int(rng.integers(0, 60)):02d}:00"
            ),
            "data_faturamento": (
                invoice_datetime.strftime("%Y-%m-%d %H:%M:%S")
                if invoice_datetime
                else ""
            ),
            "id_cliente": int(client["id_cliente"]),
            "id_representante": representative_id,
            "id_filial": branch_id,
            "status": status,
            "valor_frete": round(float(rng.uniform(0, 350)), 2),
            "valor_desconto": 0.00,
        })

        number_of_items = int(rng.integers(1, 7))
        chosen_products = rng.choice(
            active_products.index.to_numpy(),
            size=number_of_items,
            replace=False,
        )

        order_discount = 0.0

        for product_id in chosen_products:
            product = active_products.loc[int(product_id)]
            quantity = int(rng.integers(1, 15))
            unit_price = round(
                float(product["preco_atual"]) * float(rng.uniform(0.95, 1.05)),
                2,
            )
            unit_cost = round(
                float(product["custo_atual"]) * float(rng.uniform(0.97, 1.03)),
                2,
            )
            gross = quantity * unit_price
            discount = round(float(rng.uniform(0, gross * 0.08)), 2)
            order_discount += discount

            item_rows.append({
                "id_pedido_item": item_id,
                "id_pedido": order_id,
                "id_produto": int(product_id),
                "quantidade": quantity,
                "preco_unitario": unit_price,
                "custo_unitario": unit_cost,
                "desconto_item": discount,
            })

            item_id += 1

        order_rows[-1]["valor_desconto"] = round(order_discount, 2)

    pedidos = pd.DataFrame(order_rows)
    itens = pd.DataFrame(item_rows)

    # --------------------------------------------------------
    # Exportação
    # --------------------------------------------------------

    tables = {
        "estado": estados,
        "cidade": cidades,
        "filial": filiais,
        "gerente": gerentes,
        "supervisor": supervisores,
        "representante": representantes,
        "cliente": clientes,
        "categoria": categorias,
        "marca": marcas,
        "fornecedor": fornecedores,
        "produto": produtos,
        "pedido": pedidos,
        "pedido_item": itens,
        "estoque": estoque,
        "meta_representante": metas,
    }

    for name, dataframe in tables.items():
        dataframe.to_csv(
            output / f"{name}.csv",
            index=False,
            encoding="utf-8",
        )

    summary = pd.DataFrame([
        {"tabela": name, "registros": len(dataframe)}
        for name, dataframe in tables.items()
    ])

    summary.to_csv(
        output / "_summary.csv",
        index=False,
        encoding="utf-8",
    )

    print(f"Dados gerados em: {output.resolve()}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
