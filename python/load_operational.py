from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
from typing import Iterable

import mysql.connector


TABLES = [
    "estado",
    "cidade",
    "filial",
    "gerente",
    "supervisor",
    "representante",
    "cliente",
    "categoria",
    "marca",
    "fornecedor",
    "produto",
    "pedido",
    "pedido_item",
    "estoque",
    "meta_representante",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Carrega os CSVs sintéticos no banco operacional do Atlas."
    )
    parser.add_argument("--data-dir", default="data/generated")
    parser.add_argument("--truncate", action="store_true")
    return parser.parse_args()


def normalize(row: dict[str, str]) -> dict[str, str | None]:
    return {key: (None if value == "" else value) for key, value in row.items()}


def chunks(rows: list[dict[str, str | None]], size: int = 1000) -> Iterable[list[dict[str, str | None]]]:
    for start in range(0, len(rows), size):
        yield rows[start:start + size]


def load_table(cursor, data_dir: Path, table: str) -> int:
    path = data_dir / f"{table}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = [normalize(row) for row in reader]

    if not rows:
        return 0

    columns = list(rows[0].keys())
    column_sql = ", ".join(f"`{column}`" for column in columns)
    placeholders = ", ".join(f"%({column})s" for column in columns)
    sql = f"INSERT INTO `{table}` ({column_sql}) VALUES ({placeholders})"

    for batch in chunks(rows):
        cursor.executemany(sql, batch)

    return len(rows)


def main() -> None:
    args = parse_args()
    data_dir = Path(args.data_dir)

    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DATABASE", "atlas_distribuidora"),
    }

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    try:
        if args.truncate:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            for table in reversed(TABLES):
                cursor.execute(f"TRUNCATE TABLE `{table}`")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        total = 0
        for table in TABLES:
            count = load_table(cursor, data_dir, table)
            total += count
            print(f"{table:<22} {count:>10} registros")

        connection.commit()
        print(f"\nCarga concluída: {total} registros inseridos.")
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
