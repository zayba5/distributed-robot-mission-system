from fastapi import FastAPI

app = FastAPI(title="Mission Service")


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {"service": "mission-service", "healthy": True}
