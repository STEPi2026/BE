"""Read-only consistency audit for docs/api/API_MASTER.md and FastAPI OpenAPI."""

from __future__ import annotations

import os
from collections import Counter
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "docs" / "api" / "API_MASTER.md"
ROW = re.compile(r"^\| ([A-Z]+-\d{2}) \| (GET|POST|PATCH|DELETE) \| `([^`]+)` \| (.*?) \| .*? \| (BE_ONLY|CONTRACT_REQUIRED|AI_INTEGRATION) \| (NOT_STARTED|IN_PROGRESS|IMPLEMENTED|VERIFIED|BLOCKED) \|")


def inventory_rows() -> list[dict[str, str]]:
    rows = []
    for line in MASTER.read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if match:
            api_id, method, endpoint, actual, dependency, status = match.groups()
            rows.append({"id": api_id, "method": method, "endpoint": endpoint, "actual": actual, "dependency": dependency, "status": status})
    return rows


def openapi_routes() -> set[tuple[str, str]]:
    os.environ.setdefault("DB_HOST", "localhost")
    os.environ.setdefault("DB_PORT", "3306")
    os.environ.setdefault("DB_NAME", "stepi_audit")
    os.environ.setdefault("DB_USER", "stepi_audit")
    os.environ.setdefault("DB_PASSWORD", "not-a-real-password")
    os.environ.setdefault("JWT_SECRET_KEY", "audit-only-secret-key-that-is-longer-than-32-characters")
    sys.path.insert(0, str(ROOT))
    from app.main import app

    result = set()
    for path, operations in app.openapi()["paths"].items():
        for method in operations:
            if method.upper() in {"GET", "POST", "PATCH", "DELETE"}:
                result.add((method.upper(), path))
    return result


def main() -> int:
    rows = inventory_rows()
    ids = [row["id"] for row in rows]
    pairs = [(row["method"], row["endpoint"]) for row in rows]
    domains = Counter(api_id.split("-")[0] for api_id in ids)
    dependencies = Counter(row["dependency"] for row in rows)
    duplicate_ids = [item for item, count in Counter(ids).items() if count > 1]
    duplicate_pairs = [item for item, count in Counter(pairs).items() if count > 1]
    routes = openapi_routes()
    official_pairs = set(pairs)
    missing = sorted(official_pairs - routes)
    extra = sorted(routes - official_pairs)
    status_mismatch = [row["id"] for row in rows if row["status"] == "VERIFIED" and (row["method"], row["endpoint"]) not in routes]

    print(f"official_rows={len(rows)} expected=119")
    print(f"domains={len(domains)} expected=14")
    print("domain_counts=" + ", ".join(f"{key}:{domains[key]}" for key in sorted(domains)))
    print("dependency_counts=" + ", ".join(f"{key}:{dependencies[key]}" for key in sorted(dependencies)))
    print(f"duplicate_api_ids={len(duplicate_ids)}")
    print(f"duplicate_method_endpoint={len(duplicate_pairs)}")
    print(f"openapi_routes={len(routes)}")
    print("extra_openapi=" + ", ".join(f"{method} {path}" for method, path in extra))
    print(f"spec_not_registered={len(missing)}")
    print(f"verified_status_mismatch={len(status_mismatch)}")
    if len(rows) != 119 or len(domains) != 14 or duplicate_ids or duplicate_pairs or status_mismatch:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
