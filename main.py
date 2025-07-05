from fastapi import FastAPI
from api.v1 import scan_router
from infrastructure.database.connection import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Scan Orchestrator Service",
    description="Accepts and initiates new scan requests via Kafka.",
    version="1.0.0"
)

app.include_router(scan_router.router, prefix="/api/v1/scans", tags=["Scans"])

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}