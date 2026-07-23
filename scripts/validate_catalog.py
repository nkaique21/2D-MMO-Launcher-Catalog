#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema(instance, schema_path: Path, label: str) -> list[str]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"{label}: {error.message}" for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))]


def is_safe_relative_path(value: str) -> bool:
    if not value or "\x00" in value or ":" in value or value.startswith(("/", "\\")):
        return False
    path = PurePosixPath(value.replace("\\", "/"))
    return ".." not in path.parts


def require_https(value: str, label: str, errors: list[str]) -> None:
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        errors.append(f"{label}: a URL precisa usar HTTPS: {value}")


def validate_manifest_semantics(manifest: dict, path: Path, errors: list[str]) -> None:
    game_id = manifest.get("id", path.stem)
    assets = manifest.get("assets", {})
    for key in ("banner", "icon"):
        value = assets.get(key, "")
        if value.startswith("https://"):
            continue
        if not is_safe_relative_path(value):
            errors.append(f"{path}: assets.{key} possui caminho inseguro: {value}")
            continue
        asset_path = ROOT / value
        if not asset_path.is_file():
            errors.append(f"{path}: asset ausente: {value}")

    for index, method in enumerate(manifest.get("installation", {}).get("methods", [])):
        if method.get("url"):
            require_https(method["url"], f"{path}: installation.methods[{index}].url", errors)
        if method.get("installPath") and not is_safe_relative_path(method["installPath"]):
            errors.append(f"{path}: installPath inseguro em método {index}: {method['installPath']}")

    launch = manifest.get("launch", {})
    executable = launch.get("executable")
    if executable and not is_safe_relative_path(executable):
        errors.append(f"{path}: launch.executable inseguro: {executable}")

    battl_eye = launch.get("battlEye")
    if battl_eye:
        for key in ("executable", "workingDir"):
            value = battl_eye.get(key)
            if value and not is_safe_relative_path(value):
                errors.append(f"{path}: launch.battlEye.{key} inseguro: {value}")

    update = manifest.get("update", {})
    if update.get("manifestUrl"):
        require_https(update["manifestUrl"], f"{path}: update.manifestUrl", errors)
    for key in ("executable", "workingDir", "targetDir"):
        value = update.get(key)
        if value and not is_safe_relative_path(value):
            errors.append(f"{path}: update.{key} inseguro: {value}")

    verification = manifest.get("verification", {})
    for value in verification.get("requiredFiles", []):
        if not is_safe_relative_path(value):
            errors.append(f"{path}: requiredFile inseguro: {value}")
    for checksum in verification.get("checksums", []):
        value = checksum.get("path", "")
        if not is_safe_relative_path(value):
            errors.append(f"{path}: checksum.path inseguro: {value}")

    print(f"✓ {game_id}: manifesto e assets validados")


def main() -> int:
    errors: list[str] = []
    catalog_path = ROOT / "catalog.json"
    catalog = load_json(catalog_path)
    errors.extend(validate_schema(catalog, ROOT / "schemas/catalog.schema.json", "catalog.json"))

    seen_ids: set[str] = set()
    referenced_manifests: set[Path] = set()

    for entry in catalog.get("games", []):
        game_id = entry.get("id", "")
        if game_id in seen_ids:
            errors.append(f"catalog.json: ID duplicado: {game_id}")
        seen_ids.add(game_id)

        manifest_relative = entry.get("manifest", "")
        if not is_safe_relative_path(manifest_relative):
            errors.append(f"catalog.json: caminho inseguro para {game_id}: {manifest_relative}")
            continue

        manifest_path = ROOT / manifest_relative
        referenced_manifests.add(manifest_path.resolve())
        if not manifest_path.is_file():
            errors.append(f"catalog.json: manifesto ausente para {game_id}: {manifest_relative}")
            continue

        manifest = load_json(manifest_path)
        errors.extend(validate_schema(manifest, ROOT / "schemas/game-manifest.schema.json", str(manifest_path.relative_to(ROOT))))
        if manifest.get("id") != game_id:
            errors.append(f"{manifest_relative}: id {manifest.get('id')} difere do catálogo {game_id}")
        validate_manifest_semantics(manifest, manifest_path, errors)

    for manifest_path in (ROOT / "manifests").glob("*.json"):
        if manifest_path.resolve() not in referenced_manifests:
            errors.append(f"Manifesto não referenciado por catalog.json: {manifest_path.relative_to(ROOT)}")

    if errors:
        print("\nFalhas de validação:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"\nCatálogo válido: {len(seen_ids)} jogo(s), versão {catalog.get('catalogVersion')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
