#!/usr/bin/env python3
"""Validate the MAK4I protocol repository.

Checks (each prints PASS/FAIL; exit status 1 if any check fails):

1. schemas    - every schemas/*.schema.json is a valid JSON Schema
                (draft 2020-12), $ids are unique, and every $ref resolves.
2. examples   - every schemas/examples/<schema>/valid-*.json validates and
                every invalid-*.json is rejected. For mcp-tools the file name
                is <tool>.<input|output>.<valid|invalid>-<label>.json.
3. artifacts  - every artifacts/**/*.json validates against
                schemas/artifact.schema.json (MAK-0001) and is named
                <id>-v<version>.json.
4. links      - every relative Markdown link and #anchor resolves (links in
                fenced code blocks are ignored).
5. standards  - every standards/MAK-*.md is listed in STANDARDS.md and the
                SPEC.md standards table with the status in its header, and
                every listed file exists.
6. status     - architecture-defined definitions ("x-mak4i-status":
                "architecture", SPEC.md "Specification status markers") stay
                out of the implemented contract: no MCP tool schema
                references them, no schema requires an architecture-marked
                property, and every standard whose header says
                "Conformance status: Architecture" or "In progress" (Drafts
                In Progress) has no CONFORMANCE.md criteria section.

7. consistency - MAK-0008 tool table = x-mak4i-tools = $defs; every tool
                has valid input and output examples; MAK-0008 error table =
                error.schema.json codes; one x-mak4i-schema-version across
                schemas, matching SPEC.md's MAJOR.MINOR.

Usage:
    pip install -r scripts/requirements.txt
    python scripts/validate_protocol.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
except ImportError:  # pragma: no cover - environment problem, not a check
    sys.exit("missing dependencies: pip install -r scripts/requirements.txt")

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
EXAMPLES = SCHEMAS / "examples"
FAILURES: list[str] = []


def fail(check: str, message: str) -> None:
    FAILURES.append(f"[{check}] {message}")


# --------------------------------------------------------------------------- schemas


def load_schemas() -> tuple[dict[str, dict], Registry]:
    schemas: dict[str, dict] = {}
    ids: dict[str, str] = {}
    for path in sorted(SCHEMAS.glob("*.schema.json")):
        try:
            schema = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            fail("schemas", f"{path.name}: invalid JSON: {exc}")
            continue
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # SchemaError
            fail("schemas", f"{path.name}: not a valid 2020-12 schema: {exc.message}")
        sid = schema.get("$id", "")
        if not sid.endswith("/" + path.name):
            fail("schemas", f"{path.name}: $id must end with /{path.name}")
        if sid in ids:
            fail("schemas", f"{path.name}: duplicate $id with {ids[sid]}")
        ids[sid] = path.name
        if "x-mak4i-schema-version" not in schema:
            fail("schemas", f"{path.name}: missing x-mak4i-schema-version")
        schemas[path.name] = schema
    registry = Registry().with_resources(
        (s["$id"], Resource.from_contents(s)) for s in schemas.values() if "$id" in s
    )
    return schemas, registry


def iter_refs(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str):
                yield value
            else:
                yield from iter_refs(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_refs(item)


def check_refs(schemas: dict[str, dict], registry: Registry) -> None:
    for name, schema in schemas.items():
        resolver = registry.resolver(base_uri=schema["$id"])
        for ref in iter_refs(schema):
            try:
                resolver.lookup(ref)
            except Exception as exc:
                fail("schemas", f"{name}: unresolvable $ref {ref!r}: {exc}")


def validator_for(schema: dict, registry: Registry) -> Draft202012Validator:
    return Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())


def check_examples(schemas: dict[str, dict], registry: Registry) -> int:
    count = 0
    if not EXAMPLES.is_dir():
        fail("examples", "schemas/examples/ is missing")
        return 0
    for folder in sorted(p for p in EXAMPLES.iterdir() if p.is_dir()):
        schema_name = folder.name + ".schema.json"
        schema = schemas.get(schema_name)
        if schema is None:
            fail("examples", f"{folder.name}/: no schema {schema_name}")
            continue
        has_valid = has_invalid = False
        for path in sorted(folder.glob("*.json")):
            count += 1
            target = schema
            stem = path.stem
            if folder.name == "mcp-tools":
                parts = stem.split(".")
                if len(parts) != 3 or parts[1] not in ("input", "output"):
                    fail("examples", f"{path.relative_to(ROOT)}: name must be <tool>.<input|output>.<valid|invalid>-<label>.json")
                    continue
                tool, direction, stem = parts
                if tool not in schema.get("$defs", {}):
                    fail("examples", f"{path.relative_to(ROOT)}: unknown tool {tool}")
                    continue
                target = {"$ref": f"{schema['$id']}#/$defs/{tool}/properties/{direction}"}
            instance = json.loads(path.read_text())
            errors = list(validator_for(target, registry).iter_errors(instance))
            if stem.startswith("valid"):
                has_valid = True
                if errors:
                    fail("examples", f"{path.relative_to(ROOT)} should be valid: {errors[0].message}")
            elif stem.startswith("invalid"):
                has_invalid = True
                if not errors:
                    fail("examples", f"{path.relative_to(ROOT)} should be rejected but validated")
            else:
                fail("examples", f"{path.relative_to(ROOT)}: name must start with valid- or invalid-")
        if not has_valid:
            fail("examples", f"{folder.name}/: needs at least one valid example")
    for name in schemas:
        if name != "common.schema.json" and not (EXAMPLES / name.removesuffix(".schema.json")).is_dir():
            fail("examples", f"{name}: has no examples folder")
    return count


# --------------------------------------------------------------------------- MAK-0001 artifacts


def check_artifacts(schemas: dict[str, dict], registry: Registry) -> int:
    schema = schemas.get("artifact.schema.json")
    if schema is None:
        fail("artifacts", "schemas/artifact.schema.json is missing")
        return 0
    validator = validator_for(schema, registry)
    paths = sorted((ROOT / "artifacts").rglob("*.json"))
    for path in paths:
        rel = path.relative_to(ROOT)
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            fail("artifacts", f"{rel}: invalid JSON: {exc}")
            continue
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
        for error in errors[:3]:
            where = "/".join(str(p) for p in error.absolute_path) or "(root)"
            fail("artifacts", f"{rel}: {where}: {error.message}")
        expected = f"{str(data.get('id', '')).split('/')[-1]}-v{data.get('version', '')}.json"
        if path.name != expected:
            fail("artifacts", f"{rel}: file name must be {expected} (id and version)")
    return len(paths)


# --------------------------------------------------------------------------- cross-document consistency


TOOL_ROW_RE = re.compile(r"^\|\s*`(mak4i_[a-z_]+)`\s*\|", re.M)
ERROR_ROW_RE = re.compile(r"^\|\s*`([a-z_]+)`\s*\|", re.M)


def section(text: str, heading_prefix: str) -> str:
    start = text.index(heading_prefix)
    nxt = re.search(r"^### ", text[start + 1:], re.M)
    return text[start: start + 1 + nxt.start()] if nxt else text[start:]


def check_consistency(schemas: dict[str, dict]) -> int:
    checks = 0
    mak8 = (ROOT / "standards" / "MAK-0008.md").read_text()
    tools_schema = schemas.get("mcp-tools.schema.json", {})
    listed = tools_schema.get("x-mak4i-tools", [])
    defs = sorted(tools_schema.get("$defs", {}))
    table = TOOL_ROW_RE.findall(section(mak8, "### §10 Tool catalog"))
    checks += 1
    if sorted(listed) != defs or sorted(set(table)) != defs:
        fail("consistency", f"tool lists differ: MAK-0008 §10.1 {sorted(set(table))}, x-mak4i-tools {sorted(listed)}, $defs {defs}")
    examples = {p.name for p in (EXAMPLES / "mcp-tools").glob("*.json")}
    for tool in defs:
        checks += 1
        for direction in ("input", "output"):
            if not any(n.startswith(f"{tool}.{direction}.valid") for n in examples):
                fail("consistency", f"{tool}: no valid {direction} example in schemas/examples/mcp-tools/")
    codes = set(ERROR_ROW_RE.findall(section(mak8, "### §9 Error model")))
    enum: set[str] = set()

    def collect(node):
        if isinstance(node, dict):
            if "enum" in node and "access_denied" in node["enum"]:
                enum.update(node["enum"])
            for value in node.values():
                collect(value)
        elif isinstance(node, list):
            for value in node:
                collect(value)

    collect(schemas.get("error.schema.json", {}))
    checks += 1
    if codes != enum:
        fail("consistency", f"error codes differ: MAK-0008 §9 {sorted(codes)}, error.schema.json {sorted(enum)}")
    versions = {s.get("x-mak4i-schema-version") for s in schemas.values()}
    checks += 1
    if len(versions) != 1:
        fail("consistency", f"schemas disagree on x-mak4i-schema-version: {sorted(map(str, versions))}")
    spec = (ROOT / "SPEC.md").read_text()
    match = re.search(r"\*\*Version:\*\* (\d+)\.(\d+)", spec)
    (version,) = versions or {None}
    checks += 1
    if not match or not str(version).startswith(f"{match.group(1)}.{match.group(2)}."):
        fail("consistency", f"SPEC.md version and schema version {version} disagree on MAJOR.MINOR")
    return checks


# --------------------------------------------------------------------------- links

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
SKIP_DIRS = {"node_modules", ".git"}


def github_slug(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def strip_code(lines: list[str]) -> list[str]:
    out, fenced = [], False
    for line in lines:
        if line.lstrip().startswith("```"):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else line)
    return out


def anchors_of(path: Path, cache: dict[Path, set[str]]) -> set[str]:
    if path not in cache:
        seen: dict[str, int] = {}
        result: set[str] = set()
        for line in strip_code(path.read_text().splitlines()):
            match = HEADING_RE.match(line)
            if not match:
                continue
            slug = github_slug(match.group(2))
            n = seen.get(slug, 0)
            result.add(slug if n == 0 else f"{slug}-{n}")
            seen[slug] = n + 1
        cache[path] = result
    return cache[path]


def check_links() -> int:
    cache: dict[Path, set[str]] = {}
    files = [p for p in ROOT.rglob("*.md") if not SKIP_DIRS & set(p.relative_to(ROOT).parts)]
    for path in sorted(files):
        rel = path.relative_to(ROOT)
        for lineno, line in enumerate(strip_code(path.read_text().splitlines()), 1):
            line = re.sub(r"`[^`]*`", "", line)
            for target in LINK_RE.findall(line):
                if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("//"):
                    continue  # absolute URL / mailto
                file_part, _, anchor = target.partition("#")
                dest = path if not file_part else (path.parent / file_part).resolve()
                if not dest.exists():
                    fail("links", f"{rel}:{lineno}: missing target {target}")
                    continue
                if anchor and dest.suffix == ".md" and anchor not in anchors_of(dest, cache):
                    fail("links", f"{rel}:{lineno}: missing anchor #{anchor} in {dest.relative_to(ROOT)}")
    return len(files)


# --------------------------------------------------------------------------- standards index

STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*([A-Za-z]+(?: \(In Progress\))?)", re.M)


def table_rows(text: str) -> dict[str, list[str]]:
    rows = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(r"MAK-\d{4}", cells[0]):
            rows[cells[0]] = cells
    return rows


def check_standards() -> int:
    standards_md = table_rows((ROOT / "STANDARDS.md").read_text())
    spec_md = table_rows((ROOT / "SPEC.md").read_text())
    files = sorted((ROOT / "standards").glob("MAK-*.md"))
    for path in files:
        number = path.stem
        match = STATUS_RE.search(path.read_text())
        if not match:
            fail("standards", f"{path.name}: no **Status:** header")
            continue
        status = match.group(1)
        for index_name, rows in (("STANDARDS.md", standards_md), ("SPEC.md", spec_md)):
            row = rows.get(number)
            if row is None:
                fail("standards", f"{number} is not listed in {index_name}")
            elif status not in row:
                fail("standards", f"{index_name} lists {number} as {row[2] if len(row) > 2 else '?'}, file says {status}")
        row = standards_md.get(number)
        if row and f"standards/{path.name}" not in "|".join(row):
            fail("standards", f"STANDARDS.md row for {number} does not link standards/{path.name}")
    for number, row in standards_md.items():
        linked = re.search(r"\((standards/MAK-\d{4}\.md)\)", "|".join(row))
        if linked and not (ROOT / linked.group(1)).exists():
            fail("standards", f"STANDARDS.md links missing file {linked.group(1)}")
        if not linked and (ROOT / "standards" / f"{number}.md").exists():
            fail("standards", f"STANDARDS.md row for {number} has no file link although the file exists")
    return len(files)


# --------------------------------------------------------------------------- main


# --------------------------------------------------------------------------- status


ARCHITECTURE = "architecture"


def check_status(schemas: dict[str, dict]) -> int:
    architecture = {name for name, s in schemas.items() if s.get("x-mak4i-status") == ARCHITECTURE}
    for name, schema in schemas.items():
        if schema.get("x-mak4i-status") not in (None, ARCHITECTURE):
            fail("status", f"{name}: unknown x-mak4i-status {schema['x-mak4i-status']!r}")
        props = schema.get("properties", {})
        for prop in schema.get("required", []):
            if isinstance(props.get(prop), dict) and props[prop].get("x-mak4i-status") == ARCHITECTURE:
                fail("status", f"{name}: architecture-defined property {prop!r} must not be required")
    tools = schemas.get("mcp-tools.schema.json", {})
    for ref in iter_refs(tools):
        target = ref.split("#")[0].rsplit("/", 1)[-1]
        if target in architecture:
            fail("status", f"mcp-tools.schema.json references architecture-defined {target}; "
                 "an interface binding needs the standard's conformance criteria first")
    conformance = (ROOT / "CONFORMANCE.md").read_text()
    for path in sorted((ROOT / "standards").glob("MAK-*.md")):
        text = path.read_text()
        marker = re.search(r"^\*\*Conformance status:\*\* (Architecture|In progress)", text, re.M)
        in_progress = re.search(r"^\*\*Status:\*\* Draft \(In Progress\)", text, re.M)
        if in_progress and not (marker and marker.group(1) == "In progress"):
            fail("status", f"{path.stem} is a Draft (In Progress) but lacks 'Conformance status: In progress'")
        if marker and re.search(rf"^### {path.stem}\b", conformance, re.M):
            fail("status", f"{path.stem} has conformance status {marker.group(1)!r} but CONFORMANCE.md has a criteria section for it")
    return len(architecture)


def main() -> int:
    schemas, registry = load_schemas()
    check_refs(schemas, registry)
    results = [
        ("schemas", f"{len(schemas)} schema(s)"),
        ("examples", f"{check_examples(schemas, registry)} example(s)"),
        ("artifacts", f"{check_artifacts(schemas, registry)} artifact(s)"),
        ("links", f"{check_links()} Markdown file(s)"),
        ("standards", f"{check_standards()} standard(s)"),
        ("status", f"{check_status(schemas)} architecture-defined schema(s)"),
        ("consistency", f"{check_consistency(schemas)} cross-document check(s)"),
    ]
    for check, summary in results:
        failed = [f for f in FAILURES if f.startswith(f"[{check}]")]
        print(f"{'FAIL' if failed else 'PASS'}  {check:<10} {summary}")
    if FAILURES:
        print()
        for failure in FAILURES:
            print(failure)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
