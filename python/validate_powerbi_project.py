#!/usr/bin/env python3
"""Static QA for the Atlas Power BI Project (PBIP/PBIR/TMDL).

Checks that can run without Power BI Desktop:
- JSON parsing and optional validation against each file's public $schema;
- PBIP -> Report -> SemanticModel relative paths;
- PBIR page order and active page consistency;
- page/visual IDs versus folder names;
- visual references to existing TMDL measures and columns;
- model.tmdl table references;
- relationship endpoints;
- PBIR vs PBIR-Legacy mutual exclusivity.

This does not replace opening and rendering the project in Power BI Desktop.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PBIP_ROOT = ROOT / "powerbi" / "pbip"
REPORT_DIR = PBIP_ROOT / "AtlasDistribuidoraAnalytics.Report"
MODEL_DIR = PBIP_ROOT / "AtlasDistribuidoraAnalytics.SemanticModel"
DEFINITION_DIR = REPORT_DIR / "definition"
TABLES_DIR = MODEL_DIR / "definition" / "tables"


class QA:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0

    def ok(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.errors.append(message)

    def warn(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.warnings.append(message)


def load_json(path: Path, qa: QA) -> dict[str, Any] | list[Any] | None:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:  # noqa: BLE001
        qa.errors.append(f"JSON inválido em {path.relative_to(ROOT)}: {exc}")
        return None


def unquote_tmdl(name: str) -> str:
    name = name.strip()
    if len(name) >= 2 and name[0] == "'" and name[-1] == "'":
        return name[1:-1].replace("''", "'")
    return name


def parse_tmdl_tables(qa: QA) -> tuple[dict[str, set[str]], set[str]]:
    columns: dict[str, set[str]] = {}
    measures: set[str] = set()

    for path in sorted(TABLES_DIR.glob("*.tmdl")):
        text = path.read_text(encoding="utf-8")
        table_name: str | None = None

        for raw in text.splitlines():
            stripped = raw.strip()
            if stripped.startswith("table "):
                table_name = unquote_tmdl(stripped[len("table "):])
                columns.setdefault(table_name, set())
            elif stripped.startswith("column ") and table_name:
                columns[table_name].add(
                    unquote_tmdl(stripped[len("column "):])
                )
            elif stripped.startswith("measure ") and " = " in stripped:
                name = stripped[len("measure "):].split(" = ", 1)[0]
                measures.add(unquote_tmdl(name))

    qa.ok(bool(columns), "Nenhuma tabela TMDL encontrada.")
    qa.ok("_Medidas" in columns, "Tabela _Medidas ausente no TMDL.")
    qa.ok(bool(measures), "Nenhuma medida TMDL encontrada.")
    return columns, measures


def walk_refs(node: Any):
    if isinstance(node, dict):
        if "Measure" in node and isinstance(node["Measure"], dict):
            yield "measure", node["Measure"]
        if "Column" in node and isinstance(node["Column"], dict):
            yield "column", node["Column"]
        for value in node.values():
            yield from walk_refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_refs(value)


def ref_entity_property(ref: dict[str, Any]) -> tuple[str | None, str | None]:
    prop = ref.get("Property")
    expression = ref.get("Expression", {})
    entity = expression.get("SourceRef", {}).get("Entity")
    return entity, prop


def validate_visual_references(
    path: Path,
    data: dict[str, Any],
    columns: dict[str, set[str]],
    measures: set[str],
    qa: QA,
) -> None:
    for kind, ref in walk_refs(data):
        entity, prop = ref_entity_property(ref)
        rel = path.relative_to(ROOT)

        if not entity or not prop:
            qa.errors.append(f"Referência {kind} incompleta em {rel}: {ref}")
            continue

        if kind == "measure":
            qa.ok(
                entity == "_Medidas" and prop in measures,
                f"Medida inexistente em {rel}: {entity}[{prop}]",
            )
        else:
            qa.ok(
                entity in columns and prop in columns[entity],
                f"Coluna inexistente em {rel}: {entity}[{prop}]",
            )


def schema_validator(strict: bool):
    try:
        from jsonschema.validators import validator_for
        from referencing import Registry, Resource
    except ImportError:
        raise RuntimeError(
            "Validação por schema requer requirements-dev.txt."
        )

    cache: dict[str, Any] = {}

    def retrieve(uri: str):
        if uri not in cache:
            with urllib.request.urlopen(uri, timeout=20) as response:
                cache[uri] = json.loads(response.read().decode("utf-8"))
        return Resource.from_contents(cache[uri])

    registry = Registry(retrieve=retrieve)

    def validate(path: Path, instance: Any, qa: QA) -> None:
        if not isinstance(instance, dict):
            return
        uri = instance.get("$schema")
        if not uri:
            qa.warn(False, f"Arquivo JSON sem $schema: {path.relative_to(ROOT)}")
            return
        try:
            if uri not in cache:
                with urllib.request.urlopen(uri, timeout=20) as response:
                    cache[uri] = json.loads(response.read().decode("utf-8"))
            schema = cache[uri]
            cls = validator_for(schema)
            cls.check_schema(schema)
            validator = cls(schema, registry=registry)
            errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
            for error in errors:
                location = ".".join(str(x) for x in error.path) or "<root>"
                qa.errors.append(
                    f"Schema inválido em {path.relative_to(ROOT)} [{location}]: "
                    f"{error.message}"
                )
            qa.checks += 1
        except Exception as exc:  # noqa: BLE001
            msg = f"Falha ao validar schema de {path.relative_to(ROOT)}: {exc}"
            if strict:
                qa.errors.append(msg)
            else:
                qa.warnings.append(msg)

    return validate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--schema",
        action="store_true",
        help="Valida JSONs contra os $schema públicos declarados.",
    )
    parser.add_argument(
        "--strict-schema",
        action="store_true",
        help="Falha caso o schema remoto não possa ser obtido.",
    )
    args = parser.parse_args()

    qa = QA()

    project_files = list(PBIP_ROOT.glob("*.pbip"))
    qa.ok(len(project_files) == 1, "Deve existir exatamente um arquivo .pbip.")
    if not project_files:
        return 1

    project = load_json(project_files[0], qa)
    definition_pbir = load_json(REPORT_DIR / "definition.pbir", qa)
    pages_meta = load_json(DEFINITION_DIR / "pages" / "pages.json", qa)

    qa.ok(
        DEFINITION_DIR.is_dir() and not (REPORT_DIR / "report.json").exists(),
        "PBIR enhanced e PBIR-Legacy não devem coexistir no diretório do relatório.",
    )

    if isinstance(project, dict):
        artifacts = project.get("artifacts", [])
        report_paths = [
            item.get("report", {}).get("path")
            for item in artifacts
            if isinstance(item, dict) and item.get("report")
        ]
        qa.ok(
            REPORT_DIR.name in report_paths,
            "O .pbip não aponta para AtlasDistribuidoraAnalytics.Report.",
        )

    if isinstance(definition_pbir, dict):
        model_path = (
            definition_pbir.get("datasetReference", {})
            .get("byPath", {})
            .get("path")
        )
        resolved = (REPORT_DIR / model_path).resolve() if model_path else None
        qa.ok(
            resolved == MODEL_DIR.resolve(),
            "definition.pbir não aponta para o modelo semântico esperado.",
        )

    columns, measures = parse_tmdl_tables(qa)

    model_tmdl = (MODEL_DIR / "definition" / "model.tmdl").read_text(encoding="utf-8")
    referenced_tables = {
        unquote_tmdl(m.group(1))
        for m in re.finditer(r"^ref table\s+(.+?)\s*$", model_tmdl, flags=re.MULTILINE)
    }
    qa.ok(
        referenced_tables == set(columns),
        "model.tmdl e arquivos de tabela TMDL não possuem o mesmo conjunto de tabelas. "
        f"model={sorted(referenced_tables)} files={sorted(columns)}",
    )

    rel_text = (MODEL_DIR / "definition" / "relationships.tmdl").read_text(
        encoding="utf-8"
    )
    for table, column in re.findall(
        r"^(?:fromColumn|toColumn):\s+([\w]+)\.([\w]+)\s*$",
        rel_text,
        flags=re.MULTILINE,
    ):
        qa.ok(
            table in columns and column in columns[table],
            f"Relacionamento aponta para coluna inexistente: {table}.{column}",
        )

    pages_dir = DEFINITION_DIR / "pages"
    page_dirs = sorted(
        p for p in pages_dir.iterdir() if p.is_dir()
    )
    actual_page_ids = {p.name for p in page_dirs}

    if isinstance(pages_meta, dict):
        order = pages_meta.get("pageOrder", [])
        active = pages_meta.get("activePageName")
        qa.ok(set(order) == actual_page_ids, "pageOrder não coincide com as pastas de páginas.")
        qa.ok(active in actual_page_ids, "activePageName aponta para página inexistente.")
        qa.ok(len(order) == len(set(order)), "pageOrder possui IDs duplicados.")

    visual_ids: set[str] = set()
    total_visuals = 0

    for page_dir in page_dirs:
        page_json_path = page_dir / "page.json"
        page_json = load_json(page_json_path, qa)
        if isinstance(page_json, dict):
            qa.ok(
                page_json.get("name") == page_dir.name,
                f"ID da página difere da pasta: {page_dir.name}",
            )
            qa.ok(page_json.get("width") == 1280, f"{page_dir.name}: width deve ser 1280.")
            qa.ok(page_json.get("height") == 720, f"{page_dir.name}: height deve ser 720.")

        visuals_dir = page_dir / "visuals"
        if not visuals_dir.exists():
            qa.warnings.append(f"Página sem pasta visuals: {page_dir.name}")
            continue

        for visual_dir in sorted(p for p in visuals_dir.iterdir() if p.is_dir()):
            visual_json_path = visual_dir / "visual.json"
            visual_json = load_json(visual_json_path, qa)
            if not isinstance(visual_json, dict):
                continue

            total_visuals += 1
            visual_name = visual_json.get("name")
            qa.ok(
                visual_name == visual_dir.name,
                f"ID do visual difere da pasta: {visual_dir.relative_to(ROOT)}",
            )
            qa.ok(
                visual_dir.name not in visual_ids,
                f"ID de visual duplicado: {visual_dir.name}",
            )
            visual_ids.add(visual_dir.name)
            validate_visual_references(
                visual_json_path, visual_json, columns, measures, qa
            )

    qa.ok(len(page_dirs) == 5, f"Esperadas 5 páginas, encontradas {len(page_dirs)}.")
    qa.ok(total_visuals == 42, f"Esperados 42 visuais, encontrados {total_visuals}.")

    if args.schema:
        validate_schema = schema_validator(args.strict_schema)
        json_files = [
            project_files[0],
            REPORT_DIR / "definition.pbir",
            *sorted(DEFINITION_DIR.rglob("*.json")),
        ]
        for path in json_files:
            instance = load_json(path, qa)
            if instance is not None:
                validate_schema(path, instance, qa)

    print(f"Checks executados: {qa.checks}")
    print(f"Páginas: {len(page_dirs)}")
    print(f"Visuais: {total_visuals}")
    print(f"Tabelas TMDL: {len(columns)}")
    print(f"Medidas TMDL: {len(measures)}")

    if qa.warnings:
        print("\nAVISOS:")
        for item in qa.warnings:
            print(f"- {item}")

    if qa.errors:
        print("\nFALHAS:")
        for item in qa.errors:
            print(f"- {item}")
        return 1

    print("\n[OK] Estrutura PBIP/PBIR/TMDL consistente nas validações estáticas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
