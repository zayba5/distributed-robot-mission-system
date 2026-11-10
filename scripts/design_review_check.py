

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(path: str) -> None:
    target = ROOT / path
    if not target.is_file():
        raise SystemExit(f"FAIL: missing {path}")


for path in (
    "docker-compose.yml",
    "database/init.sql",
    "services/mission-service/Dockerfile",
    "services/mission-service/app/app.py",
    "services/scheduler-service/app.py",
    "services/robot-simulator/app.py",
    "scripts/smoke_test.py",
    "scripts/load_test.py",
    "docs/design-review.md",
    "docs/architecture.md",
    "docs/consistency.md",
    "docs/runbook.md",
):
    require(path)


compose = (ROOT / "docker-compose.yml").read_text()
for expected in (
    "build: ./services/mission-service",
    "build: ./services/scheduler-service",
    "build: ./services/robot-simulator",
    "./database/init.sql:/docker-entrypoint-initdb.d/init.sql",
):
    if expected not in compose:
        raise SystemExit(f"FAIL: Compose is missing: {expected}")


dockerfile = (ROOT / "services/mission-service/Dockerfile").read_text()
if "COPY app ./app" not in dockerfile:
    raise SystemExit("FAIL: mission Dockerfile must copy the app package")

if 'CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5000"]' not in dockerfile:
    raise SystemExit("FAIL: mission Dockerfile must start FastAPI with Uvicorn")

for service in ("mission-service", "scheduler-service", "robot-simulator"):
    requirements = (ROOT / "services" / service / "requirements.txt").read_text()
    if "fastapi" not in requirements or "uvicorn" not in requirements:
        raise SystemExit(f"FAIL: {service} is not configured for FastAPI")

for path in (
    ROOT / "services" / "mission-service" / "app" / "app.py",
    ROOT / "services" / "scheduler-service" / "app.py",
    ROOT / "services" / "robot-simulator" / "app.py",
):
    if "from fastapi import FastAPI" not in path.read_text():
        raise SystemExit(f"FAIL: {path.relative_to(ROOT)} is not using FastAPI")


print("DESIGN REVIEW CHECK PASSED")
print("Runtime paths, database initialization, tests, and review documents are present.")
